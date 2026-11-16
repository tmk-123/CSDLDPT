"""Yêu cầu 3: trích đặc trưng cho mọi tệp trong data/metadata.csv và nạp vào CSDL MySQL.

Cách chạy (từ thư mục gốc project):
    .venv\\Scripts\\python.exe src\\phan3_dac_trung_csdl\\nap_csdl.py

Đầu vào : data/metadata.csv, data/wav/, .env (thông tin kết nối MySQL)
Đầu ra  : CSDL MySQL tên MYSQL_DATABASE (5 bảng + 1 view), schema.sql (cấu trúc bảng),
          ket_qua/dac_trung_600_tep.csv (46 chiều đã chốt, bản sao bảng dac_trung),
          ket_qua/ung_vien_dac_trung_600_tep.csv (72 chiều ứng viên, dùng cho đánh giá chọn đặc trưng)
Chạy lại nhiều lần được: các bảng của CSDL này được xóa và tạo lại từ đầu.
"""
import re
import time
from pathlib import Path

import mysql.connector
import numpy as np
import pandas as pd

import dac_trung as dt

GOC = Path(__file__).resolve().parents[2]
SCHEMA = Path(__file__).with_name("schema.sql")
CSV_DAC_TRUNG = GOC / "ket_qua" / "dac_trung_600_tep.csv"
CSV_UNG_VIEN = GOC / "ket_qua" / "ung_vien_dac_trung_600_tep.csv"
SO_KET_QUA = 5            # hệ thống trả về 5 tệp giống nhất
NHAC_CU = [  # (nhac_cu_id, mã, tên hiển thị, nhóm theo cách kích âm)
    (1, "violin", "Violin", "kéo vĩ"), (2, "viola", "Viola", "kéo vĩ"),
    (3, "cello", "Cello", "kéo vĩ"), (4, "double_bass", "Double Bass", "kéo vĩ"),
    (5, "guitar_acoustic", "Guitar Acoustic", "gảy"), (6, "guitar_electric", "Guitar Electric", "gảy"),
]
BANG_MO_RONG = "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"


# ---------- 1. Kết nối ----------
def doc_env():
    """Đọc .env ở gốc project thành dict (không in mật khẩu ra màn hình)."""
    cfg = {}
    for dong in (GOC / ".env").read_text(encoding="utf-8").splitlines():
        k, _, v = dong.strip().partition("=")
        if k and not k.startswith("#"):
            cfg[k] = v
    return cfg


def ket_noi(co_csdl=True):
    """Mở kết nối MySQL; co_csdl=False để kết nối khi CSDL chưa được tạo."""
    cfg = doc_env()
    tham_so = dict(host=cfg["MYSQL_HOST"], port=int(cfg["MYSQL_PORT"]),
                   user=cfg["MYSQL_USER"], password=cfg["MYSQL_PASSWORD"])
    if co_csdl:
        tham_so["database"] = cfg["MYSQL_DATABASE"]
    return mysql.connector.connect(**tham_so)


# ---------- 2. Cấu trúc bảng ----------
def lenh_tao_bang():
    """Các lệnh CREATE: 5 bảng và 1 view. Bảng dac_trung có một cột cho mỗi chiều trong dt.TEN_CHIEU."""
    cot_dac_trung = ",\n".join(f"  {c:<16} DOUBLE NOT NULL" for c in dt.TEN_CHIEU)
    cot_view = ", ".join(f"d.{c}" for c in dt.TEN_CHIEU)
    return [
        f"""CREATE TABLE nhac_cu (
  nhac_cu_id   TINYINT UNSIGNED NOT NULL PRIMARY KEY,
  ma           VARCHAR(30) NOT NULL UNIQUE,      -- mã dùng trong data/wav, ví dụ double_bass
  ten_hien_thi VARCHAR(50) NOT NULL,             -- ví dụ Double Bass
  nhom         VARCHAR(20) NOT NULL              -- nhóm theo cách kích âm: kéo vĩ / gảy
) {BANG_MO_RONG}""",
        f"""CREATE TABLE tep_am_thanh (
  tep_id      INT UNSIGNED NOT NULL PRIMARY KEY, -- = file_id trong data/metadata.csv
  ten_tep     VARCHAR(100) NOT NULL UNIQUE,
  duong_dan   VARCHAR(255) NOT NULL UNIQUE,      -- đường dẫn tương đối từ gốc project
  nhac_cu_id  TINYINT UNSIGNED NOT NULL,
  nguon       VARCHAR(50) NOT NULL,              -- bộ dữ liệu gốc: URMP, PHENICX-Anechoic, ...
  ban_thu_goc VARCHAR(255) NOT NULL,             -- tệp gốc mà đoạn được cắt ra
  nhom_ban_thu VARCHAR(255) NOT NULL,            -- lần ghi âm: các đoạn cùng nhóm có cùng người chơi, cùng bản nhạc
  bat_dau_s   DECIMAL(8,2) NOT NULL,             -- vị trí bắt đầu cắt trong tệp gốc (giây)
  do_dai_s    DECIMAL(6,2) NOT NULL,             -- độ dài đoạn (giây)
  tan_so_mau  INT NOT NULL,
  CONSTRAINT fk_tep_nhac_cu FOREIGN KEY (nhac_cu_id) REFERENCES nhac_cu (nhac_cu_id),
  INDEX idx_tep_nhac_cu (nhac_cu_id),
  INDEX idx_tep_nhom_ban_thu (nhom_ban_thu)
) {BANG_MO_RONG}""",
        f"""CREATE TABLE dac_trung (
  tep_id           INT UNSIGNED NOT NULL PRIMARY KEY,
{cot_dac_trung},
  phien_ban        VARCHAR(200) NOT NULL,        -- tham số trích đặc trưng đã dùng
  CONSTRAINT fk_dac_trung_tep FOREIGN KEY (tep_id) REFERENCES tep_am_thanh (tep_id) ON DELETE CASCADE
) {BANG_MO_RONG}""",
        f"""CREATE TABLE thong_ke_chuan_hoa (
  ten_chieu     VARCHAR(40) NOT NULL PRIMARY KEY, -- tên một cột của bảng dac_trung
  thu_tu        TINYINT UNSIGNED NOT NULL UNIQUE, -- vị trí trong vector (1..{len(dt.TEN_CHIEU)})
  loai          VARCHAR(20) NOT NULL,             -- MFCC, Roll-off, RMS, ZCR, Spectral Contrast
  trung_binh    DOUBLE NOT NULL,                  -- trung bình của chiều này trên toàn bộ tệp
  do_lech_chuan DOUBLE NOT NULL,                  -- độ lệch chuẩn của chiều này trên toàn bộ tệp
  dung_truy_van TINYINT(1) NOT NULL               -- 1: dùng để tính độ tương đồng khi truy vấn; 0: chỉ lưu để giải thích
) {BANG_MO_RONG}""",
        f"""CREATE TABLE cau_hinh_truy_van (
  khoa    VARCHAR(40) NOT NULL PRIMARY KEY,       -- tên tham số
  gia_tri VARCHAR(200) NOT NULL                   -- giá trị
) {BANG_MO_RONG}""",
        f"""CREATE VIEW v_tep_dac_trung AS
SELECT t.tep_id, t.ten_tep, t.duong_dan, n.ma AS nhac_cu, n.ten_hien_thi, n.nhom, t.ban_thu_goc, t.nhom_ban_thu, {cot_view}
FROM tep_am_thanh t
JOIN nhac_cu n ON n.nhac_cu_id = t.nhac_cu_id
JOIN dac_trung d ON d.tep_id = t.tep_id""",
    ]


def ghi_schema(lenh):
    dau = ("-- CSDL đặc trưng âm thanh nhạc cụ bộ dây (yêu cầu 3).\n"
           "-- Tệp này được sinh tự động bởi nap_csdl.py từ danh sách đặc trưng trong dac_trung.py; không sửa tay.\n"
           "-- Tên CSDL lấy từ biến MYSQL_DATABASE trong .env.\n\n")
    SCHEMA.write_text(dau + ";\n\n".join(lenh) + ";\n", encoding="utf-8")


def tinh_nhom_ban_thu(meta):
    """Nhóm bản thu của từng đoạn: các đoạn cùng nhóm đến từ cùng một lần ghi âm (cùng người chơi, cùng bản nhạc).

    - URMP, PHENICX-Anechoic: mỗi track là một nhạc công chơi một bè -> nhóm = tên track.
    - GuitarSet: bản đệm (comp) và bản giai điệu (solo) của cùng người chơi, cùng bài -> chung một nhóm.
    - Medley-solos-DB: mỗi đoạn là một tệp riêng nhưng nhiều đoạn cắt từ cùng bài hát -> nhóm = bài hát.
    Khi đánh giá tìm kiếm, cả nhóm phải cùng nằm một phía (cùng là truy vấn hoặc cùng trong thư viện),
    nếu không, đoạn "anh em" cùng bản thu sẽ làm kết quả tốt giả tạo.
    """
    md = pd.read_csv(GOC / "data" / "raw" / "guitar_electric" / "Medley-solos-DB_metadata.csv")
    bai_hat = dict(zip(md["uuid4"], md["song_id"]))

    def mot_dong(r):
        if r.source == "GuitarSet":
            return re.sub(r"_(comp|solo)_mic\.wav$", "", r.source_file)
        if r.source == "Medley-solos-DB":
            return f"medley_song_{bai_hat[Path(r.source_file).stem.split('_')[-1]]}"
        return r.source_file

    return meta.apply(mot_dong, axis=1)


# ---------- 3. Trích đặc trưng ----------
def trich_toan_bo(meta):
    """Trích vector ứng viên (72 chiều) cho từng tệp trong metadata; trả về DataFrame (tep_id + các chiều)."""
    dong, t0 = [], time.time()
    for i, r in enumerate(meta.itertuples(), 1):
        vec = dt.trich_ung_vien(dt.doc_tin_hieu(GOC / r.file_path))     # 72 chiều; CSDL chỉ nhận 46 chiều đã chốt
        dong.append({"tep_id": r.file_id, **vec})
        if i % 100 == 0 or i == len(meta):
            print(f"  đã trích {i}/{len(meta)} tệp ({time.time() - t0:.0f} s)")
    return pd.DataFrame(dong)


# ---------- 4. Nạp vào CSDL ----------
def nap(meta, bang):
    ten_csdl = doc_env()["MYSQL_DATABASE"]
    with ket_noi(co_csdl=False) as cn:
        cn.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{ten_csdl}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

    lenh = lenh_tao_bang()
    ghi_schema(lenh)
    with ket_noi() as cn:
        cur = cn.cursor()
        cur.execute("DROP VIEW IF EXISTS v_tep_dac_trung")
        cur.execute("DROP TABLE IF EXISTS dac_trung, thong_ke_chuan_hoa, cau_hinh_truy_van, tep_am_thanh, nhac_cu")
        for l in lenh:
            cur.execute(l)

        cur.executemany("INSERT INTO nhac_cu VALUES (%s, %s, %s, %s)", NHAC_CU)
        ma_id = {ma: i for i, ma, _, _ in NHAC_CU}
        nhom = tinh_nhom_ban_thu(meta)
        cur.executemany(
            "INSERT INTO tep_am_thanh VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [(int(r.file_id), r.file_name, r.file_path, ma_id[r.instrument], r.source, r.source_file, g,
              float(r.start_s), float(r.duration_s), int(r.sample_rate)) for r, g in zip(meta.itertuples(), nhom)])

        cot = ", ".join(["tep_id", *dt.TEN_CHIEU, "phien_ban"])
        dau_hoi = ", ".join(["%s"] * (len(dt.TEN_CHIEU) + 2))
        cur.executemany(f"INSERT INTO dac_trung ({cot}) VALUES ({dau_hoi})",
                        [(int(r[0]), *map(float, r[1:]), dt.PHIEN_BAN)
                         for r in bang[["tep_id", *dt.TEN_CHIEU]].itertuples(index=False)])

        # thống kê chuẩn hóa: mu_j và sigma_j của từng chiều trên toàn bộ tệp (dùng để chuẩn hóa tệp truy vấn)
        cur.executemany("INSERT INTO thong_ke_chuan_hoa VALUES (%s, %s, %s, %s, %s, %s)",
                        [(c, j, dt.LOAI_CUA_CHIEU[c], float(bang[c].mean()), float(bang[c].std(ddof=0)),
                          int(c in dt.CHIEU_TRUY_VAN)) for j, c in enumerate(dt.TEN_CHIEU, 1)])
        cur.executemany("INSERT INTO cau_hinh_truy_van VALUES (%s, %s)",
                        [("do_do", dt.DO_DO), ("so_ket_qua", str(SO_KET_QUA)), ("phien_ban", dt.PHIEN_BAN),
                         ("chuan_hoa", "z-score theo trung_binh, do_lech_chuan của thong_ke_chuan_hoa")])
        cn.commit()

        for b in ["nhac_cu", "tep_am_thanh", "dac_trung", "thong_ke_chuan_hoa", "cau_hinh_truy_van", "v_tep_dac_trung"]:
            cur.execute(f"SELECT COUNT(*) FROM {b}")
            print(f"  {b:<20} {cur.fetchone()[0]:>4} dòng")


def main():
    meta = pd.read_csv(GOC / "data" / "metadata.csv")
    thieu = [p for p in meta.file_path if not (GOC / p).exists()]
    if thieu:
        raise SystemExit(f"Thiếu {len(thieu)} tệp WAV, ví dụ {thieu[0]}")

    print(f"1. Trích đặc trưng {len(meta)} tệp ({len(dt.TEN_CHIEU_UNG_VIEN)} chiều ứng viên, lưu CSDL {len(dt.TEN_CHIEU)} chiều)...")
    ung_vien = trich_toan_bo(meta)
    if not np.isfinite(ung_vien[dt.TEN_CHIEU_UNG_VIEN].to_numpy()).all():
        raise SystemExit("Có giá trị đặc trưng không hợp lệ (NaN/vô cực)")
    ung_vien.to_csv(CSV_UNG_VIEN, index=False, encoding="utf-8-sig")
    bang = ung_vien[["tep_id", *dt.TEN_CHIEU]]
    bang.to_csv(CSV_DAC_TRUNG, index=False, encoding="utf-8-sig")
    print(f"   -> {CSV_UNG_VIEN.relative_to(GOC)}, {CSV_DAC_TRUNG.relative_to(GOC)}")

    print(f"2. Nạp vào MySQL (CSDL {doc_env()['MYSQL_DATABASE']})...")
    nap(meta, bang)
    print(f"   -> cấu trúc bảng ghi tại {SCHEMA.relative_to(GOC)}")


if __name__ == "__main__":
    main()
