"""Chọn đặc trưng cho hệ thống tìm kiếm (cầu nối giữa yêu cầu 3 và yêu cầu 4).

Đọc vector đặc trưng của 600 tệp từ CSDL MySQL, đánh giá khả năng tìm đúng nhạc cụ của từng loại đặc trưng
và từng tổ hợp, để quyết định loại nào dùng để truy vấn, loại nào chỉ giữ trong CSDL, loại nào bỏ.

Cách chạy (từ thư mục gốc project):
    .venv\\Scripts\\python.exe src\\phan4_tim_kiem\\chon_dac_trung.py

Đầu ra: ket_qua/chon_dac_trung/
    e1_tung_loai.csv        mỗi loại đặc trưng dùng riêng
    e2_them_dan.csv         thêm dần từng loại (forward selection)
    e3_bot_dan.csv          bỏ thử từng loại khỏi tổ hợp đủ 6 loại
    e4_bien_the_mfcc.csv    MFCC 26 chiều / chỉ mean / chỉ std / bỏ hệ số c0
    e5_do_do_trong_so.csv   Euclid hay cosine; nối thẳng hay cân bằng giữa các loại
    e6_tuong_quan_cao.csv   các cặp chiều có |r| >= 0,9
    e7_thong_tin_theo_chieu.csv, e7_thong_tin_theo_loai.csv   Fisher F và MI
    *.png                   hình minh họa
"""
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_selection import f_classif, mutual_info_classif
from sklearn.model_selection import StratifiedGroupKFold

matplotlib.use("Agg")
GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "src" / "phan3_dac_trung_csdl"))
import dac_trung as dt  # noqa: E402
import nap_csdl  # noqa: E402

RA = GOC / "ket_qua" / "chon_dac_trung"
SO_PHAN = 5          # chia 5 phần theo nhóm bản thu
SO_LAN_LAP = 5       # lặp lại cách chia với 5 hạt giống ngẫu nhiên khác nhau
TOP = 5              # hệ thống trả về 5 tệp giống nhất
LOAI = list(dt.LOAI_UNG_VIEN)  # 7 loại ứng viên


# ---------- 1. Đọc dữ liệu từ CSDL ----------
def doc_tu_csdl():
    """Nhãn nhạc cụ, nhóm kéo vĩ/gảy và nhóm bản thu lấy từ CSDL; đặc trưng lấy từ bảng ứng viên 72 chiều
    (ket_qua/ung_vien_dac_trung_600_tep.csv, do nap_csdl.py tạo), vì CSDL chỉ lưu các chiều đã chốt."""
    with nap_csdl.ket_noi() as cn:
        cur = cn.cursor()
        cur.execute("SELECT t.tep_id, t.ten_tep, n.ma, n.nhom, t.nhom_ban_thu FROM tep_am_thanh t "
                    "JOIN nhac_cu n ON n.nhac_cu_id = t.nhac_cu_id ORDER BY t.tep_id")
        nhan = pd.DataFrame(cur.fetchall(), columns=["tep_id", "ten_tep", "nhac_cu", "nhom", "nhom_ban_thu"])
    df = nhan.merge(pd.read_csv(nap_csdl.CSV_UNG_VIEN), on="tep_id")
    df[dt.TEN_CHIEU_UNG_VIEN] = df[dt.TEN_CHIEU_UNG_VIEN].astype(float)
    return df


def cot_cua(ds_loai):
    """Danh sách cột (chiều) của một tổ hợp loại đặc trưng."""
    return [c for l in ds_loai for c in dt.LOAI_UNG_VIEN[l]]


# ---------- 2. Đánh giá một cấu hình ----------
def danh_gia(df, cot, do_do="euclid", can_bang=False):
    """Đánh giá tìm kiếm Top 5 với các cột đặc trưng `cot`.

    Mỗi lượt: chia 5 phần theo nhóm bản thu (StratifiedGroupKFold); lần lượt mỗi phần làm truy vấn,
    4 phần còn lại làm thư viện. Chuẩn hóa z-score bằng mean/std của thư viện, xếp hạng theo khoảng cách,
    chấm kết quả theo nhãn nhạc cụ. Lặp 5 lần với 5 cách chia khác nhau; trả về trung bình và độ lệch chuẩn.
    can_bang=True: nhân mỗi chiều với 1/sqrt(số chiều của loại) để mỗi loại đóng góp ngang nhau vào khoảng cách.
    """
    X = df[cot].to_numpy(float)
    y, ho, g = df.nhac_cu.to_numpy(), df.nhom.to_numpy(), df.nhom_ban_thu.to_numpy()
    w = np.ones(len(cot))
    if can_bang:
        so_chieu = {l: sum(dt.LOAI_CUA_CHIEU[c] == l for c in cot) for l in LOAI}
        w = np.array([1 / np.sqrt(so_chieu[dt.LOAI_CUA_CHIEU[c]]) for c in cot])

    lap = []
    for hat in range(SO_LAN_LAP):
        rel_all, ho_all = [], []
        for tv, tq in StratifiedGroupKFold(SO_PHAN, shuffle=True, random_state=hat).split(X, y, g):
            mu, sd = X[tv].mean(0), X[tv].std(0)
            sd[sd == 0] = 1.0
            G, Q = (X[tv] - mu) / sd * w, (X[tq] - mu) / sd * w
            if do_do == "cosine":
                G = G / np.linalg.norm(G, axis=1, keepdims=True)
                Q = Q / np.linalg.norm(Q, axis=1, keepdims=True)
                D = -Q @ G.T                                        # khoảng cách = -cos
            else:
                D = (Q ** 2).sum(1)[:, None] + (G ** 2).sum(1)[None, :] - 2 * Q @ G.T   # Euclid bình phương
            top = np.argsort(D, axis=1)[:, :TOP]
            rel_all.append(y[tv][top] == y[tq][:, None])           # đúng nhạc cụ?
            ho_all.append(ho[tv][top] == ho[tq][:, None])          # đúng nhóm kéo vĩ / gảy?
        rel, dung_ho = np.vstack(rel_all), np.vstack(ho_all)
        pk = np.cumsum(rel, 1) / np.arange(1, TOP + 1)              # Precision@k, k = 1..5
        lap.append({"P@1": rel[:, 0].mean(), "P@5": rel.mean(), "MAP@5": ((pk * rel).sum(1) / TOP).mean(),
                    "P@5_nhom": dung_ho.mean()})
    lap = pd.DataFrame(lap)
    kq = {"so_chieu": len(cot)}
    for m in lap.columns:
        kq[m], kq[m + "_sd"] = lap[m].mean(), lap[m].std(ddof=1)
    return kq


def ten(ds_loai):
    return " + ".join(ds_loai)


# ---------- 3. Các thí nghiệm ----------
def e1_tung_loai(df):
    return pd.DataFrame([{"cau_hinh": l, **danh_gia(df, cot_cua([l]))} for l in LOAI]).sort_values("P@5", ascending=False)


def e2_them_dan(df):
    """Forward selection: mỗi bước thêm loại làm P@5 tăng nhiều nhất (hòa thì xét MAP@5)."""
    da_chon, dong = [], []
    while len(da_chon) < len(LOAI):
        ung_vien = []
        for l in LOAI:
            if l not in da_chon:
                ung_vien.append({"buoc": len(da_chon) + 1, "them": l, "cau_hinh": ten(da_chon + [l]),
                                 **danh_gia(df, cot_cua(da_chon + [l]))})
        ung_vien.sort(key=lambda r: (r["P@5"], r["MAP@5"]), reverse=True)
        for r in ung_vien:
            r["duoc_chon"] = r is ung_vien[0]
        dong += ung_vien
        da_chon.append(ung_vien[0]["them"])
    return pd.DataFrame(dong)


def e3_bot_dan(df):
    dong = [{"bo_ra": "(không bỏ)", "cau_hinh": ten(LOAI), **danh_gia(df, cot_cua(LOAI))}]
    for l in LOAI:
        con = [x for x in LOAI if x != l]
        dong.append({"bo_ra": l, "cau_hinh": ten(con), **danh_gia(df, cot_cua(con))})
    return pd.DataFrame(dong)


def e4_bien_the_mfcc(df):
    m = range(dt.N_MFCC)
    bien_the = {
        "MFCC 26 (mean+std)": [f"mfcc_{i}_{t}" for i in m for t in ("mean", "std")],
        "MFCC 13 mean": [f"mfcc_{i}_mean" for i in m],
        "MFCC 13 std": [f"mfcc_{i}_std" for i in m],
        "MFCC 24 (bỏ c0)": [f"mfcc_{i}_{t}" for i in m if i > 0 for t in ("mean", "std")],
        "MFCC 12 mean (bỏ c0)": [f"mfcc_{i}_mean" for i in m if i > 0],
    }
    dong = []
    for k, cot in bien_the.items():
        dong.append({"cau_hinh": k, **danh_gia(df, cot)})
        dong.append({"cau_hinh": k + " + Roll-off", **danh_gia(df, cot + dt.LOAI["Roll-off"])})
    return pd.DataFrame(dong)


def e5_do_do_trong_so(df, cac_cau_hinh):
    dong = []
    for ds in cac_cau_hinh:
        for do_do in ("euclid", "cosine"):
            for cb in (False, True):
                if cb and len(ds) == 1:
                    continue
                dong.append({"cau_hinh": ten(ds), "do_do": do_do, "can_bang_loai": cb,
                             **danh_gia(df, cot_cua(ds), do_do=do_do, can_bang=cb)})
    return pd.DataFrame(dong)


def e6_tuong_quan(df, nguong=0.9):
    r = df[dt.TEN_CHIEU_UNG_VIEN].corr().to_numpy()
    dong = []
    for i in range(len(dt.TEN_CHIEU_UNG_VIEN)):
        for j in range(i + 1, len(dt.TEN_CHIEU_UNG_VIEN)):
            if abs(r[i, j]) >= nguong:
                a, b = dt.TEN_CHIEU_UNG_VIEN[i], dt.TEN_CHIEU_UNG_VIEN[j]
                dong.append({"chieu_1": a, "loai_1": dt.LOAI_CUA_CHIEU[a], "chieu_2": b,
                             "loai_2": dt.LOAI_CUA_CHIEU[b], "pearson_r": round(r[i, j], 3)})
    return pd.DataFrame(dong).sort_values("pearson_r", key=abs, ascending=False)


def e7_thong_tin(df):
    """Fisher F và MI của từng chiều với nhãn nhạc cụ; Fisher F với nhãn nhóm (kéo vĩ / gảy)."""
    X = df[dt.TEN_CHIEU_UNG_VIEN].to_numpy(float)
    f_nc, _ = f_classif(X, df.nhac_cu)
    f_ho, _ = f_classif(X, df.nhom)
    mi = mutual_info_classif(X, df.nhac_cu, n_neighbors=3, random_state=42)
    chieu = pd.DataFrame({"chieu": dt.TEN_CHIEU_UNG_VIEN, "loai": [dt.LOAI_CUA_CHIEU[c] for c in dt.TEN_CHIEU_UNG_VIEN],
                          "fisher_F_nhac_cu": f_nc, "MI_nhac_cu_nat": mi, "fisher_F_keo_vi_vs_gay": f_ho})
    loai = chieu.groupby("loai").agg(so_chieu=("chieu", "size"),
                                     F_nhac_cu_lon_nhat=("fisher_F_nhac_cu", "max"),
                                     F_nhac_cu_trung_vi=("fisher_F_nhac_cu", "median"),
                                     MI_lon_nhat=("MI_nhac_cu_nat", "max"),
                                     MI_trung_binh=("MI_nhac_cu_nat", "mean"),
                                     F_keo_vi_gay_lon_nhat=("fisher_F_keo_vi_vs_gay", "max"))
    return chieu.sort_values("fisher_F_nhac_cu", ascending=False), loai.sort_values("F_nhac_cu_lon_nhat", ascending=False)


# ---------- 4. Hình ----------
def ve_hinh(e1, e2):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(e1.cau_hinh, e1["P@5"] * 100, yerr=e1["P@5_sd"] * 100, color="#4C72B0", capsize=4)
    ax.axhline(100 / 6, color="gray", ls="--", label="đoán ngẫu nhiên (16,7%)")
    ax.set_ylabel("Precision@5 (%)")
    ax.set_title("Mỗi loại đặc trưng dùng riêng để tìm 5 tệp giống nhất")
    ax.legend()
    fig.tight_layout()
    fig.savefig(RA / "h1_tung_loai.png", dpi=130)
    plt.close(fig)

    duong = e2[e2.duoc_chon]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.errorbar(range(1, len(duong) + 1), duong["P@5"] * 100, yerr=duong["P@5_sd"] * 100, marker="o", capsize=4)
    ax.set_xticks(range(1, len(duong) + 1))
    ax.set_xticklabels(["+ " + t for t in duong.them], rotation=15)
    ax.set_ylabel("Precision@5 (%)")
    ax.set_title("Thêm dần từng loại đặc trưng (mỗi bước chọn loại tốt nhất)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(RA / "h2_them_dan.png", dpi=130)
    plt.close(fig)


def in_bang(tieu_de, bang, cot):
    print(f"\n=== {tieu_de} ===")
    b = bang[cot].copy()
    for c in b.columns:
        if c in ("P@1", "P@5", "MAP@5", "P@5_nhom"):
            b[c] = (b[c] * 100).round(2).astype(str) + " ± " + (bang[c + "_sd"] * 100).round(2).astype(str)
    print(b.to_string(index=False))


def main():
    RA.mkdir(parents=True, exist_ok=True)
    df = doc_tu_csdl()
    print(f"Đọc {len(df)} tệp từ CSDL; {df.nhom_ban_thu.nunique()} nhóm bản thu")
    cot_in = ["cau_hinh", "so_chieu", "P@1", "P@5", "MAP@5", "P@5_nhom"]

    e1 = e1_tung_loai(df)
    e1.to_csv(RA / "e1_tung_loai.csv", index=False, encoding="utf-8-sig")
    in_bang("E1. Từng loại dùng riêng", e1, cot_in)

    e2 = e2_them_dan(df)
    e2.to_csv(RA / "e2_them_dan.csv", index=False, encoding="utf-8-sig")
    in_bang("E2. Thêm dần (chỉ các bước được chọn)", e2[e2.duoc_chon], ["buoc", "them"] + cot_in)

    e3 = e3_bot_dan(df)
    e3.to_csv(RA / "e3_bot_dan.csv", index=False, encoding="utf-8-sig")
    in_bang("E3. Bỏ thử từng loại khỏi tổ hợp đủ 6 loại", e3, ["bo_ra"] + cot_in)

    e4 = e4_bien_the_mfcc(df)
    e4.to_csv(RA / "e4_bien_the_mfcc.csv", index=False, encoding="utf-8-sig")
    in_bang("E4. Biến thể MFCC", e4, cot_in)

    duong = list(e2[e2.duoc_chon].them)
    cac = [duong[:k] for k in range(1, 4)] + [["MFCC", "Roll-off"], LOAI]
    cac = [list(x) for x in dict.fromkeys(tuple(c) for c in cac)]
    e5 = e5_do_do_trong_so(df, cac)
    e5.to_csv(RA / "e5_do_do_trong_so.csv", index=False, encoding="utf-8-sig")
    in_bang("E5. Độ đo và trọng số", e5, ["cau_hinh", "do_do", "can_bang_loai", "so_chieu", "P@5", "MAP@5"])

    e6 = e6_tuong_quan(df)
    e6.to_csv(RA / "e6_tuong_quan_cao.csv", index=False, encoding="utf-8-sig")
    print("\n=== E6. Các cặp chiều tương quan mạnh (|r| >= 0,9) ===")
    print(e6.to_string(index=False))

    chieu, loai = e7_thong_tin(df)
    chieu.to_csv(RA / "e7_thong_tin_theo_chieu.csv", index=False, encoding="utf-8-sig")
    loai.to_csv(RA / "e7_thong_tin_theo_loai.csv", encoding="utf-8-sig")
    print("\n=== E7. Lượng thông tin theo loại (Fisher F, MI) ===")
    print(loai.round(3).to_string())

    ve_hinh(e1, e2)
    print(f"\nĐã lưu kết quả vào {RA.relative_to(GOC)}")


if __name__ == "__main__":
    main()
