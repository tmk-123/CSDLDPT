"""Dựng bộ dữ liệu: cắt các bản thu gốc thành đoạn khoảng 3 giây theo ranh giới nốt, chuẩn hóa, lưu WAV và bảng metadata.

Cách chạy:
    .venv\\Scripts\\python.exe src\\tao_bo_du_lieu.py

Đầu vào  (data/raw, mỗi nhạc cụ một thư mục):
    violin/, viola/, cello/, double_bass/   track riêng từng nhạc công: URMP (AuSep_*.wav), PHENICX-Anechoic (PHENICX_*.wav)
    guitar_acoustic/                        guitar acoustic độc tấu của GuitarSet: <...>_mic.wav
    guitar_electric/                        đoạn 3 giây guitar điện của Medley-solos-DB + file metadata.csv
Đầu ra:
    data/wav/<nhạc cụ>/<nhạc cụ>_<số thứ tự>.wav   (mono, 22 050 Hz, 16 bit, dài 2,5–3,5 giây)
    data/metadata.csv                              (mỗi dòng một file)
"""
import random
from collections import defaultdict
from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import soundfile as sf

GOC = Path(__file__).resolve().parent.parent
RAW = GOC / "data" / "raw"
WAV = GOC / "data" / "wav"

SR = 22050          # tần số mẫu (Nyquist = 11 025 Hz, đủ chứa các hài âm quan trọng)
DO_DAI = 3.0        # độ dài mong muốn của mỗi file (giây)
DO_DAI_MIN, DO_DAI_MAX = 2.5, 3.5   # cắt theo ranh giới nốt nên độ dài được phép dao động quanh 3 giây
HOP = 512           # bước nhảy giữa hai khung phân tích (512 mẫu ≈ 23 ms)
NGUONG_GIONG = 0.95  # hai đoạn có độ tương đồng cosine > 0,95 coi là gần trùng, chỉ giữ một
CHO_PHEP_LIEN_KE = {"double_bass"}  # double bass ít dữ liệu nên được phép lấy 2 đoạn liền nhau của cùng track
FADE = 0.05         # làm mềm hai mép mỗi đoạn: to dần 50 ms đầu, nhỏ dần 50 ms cuối
SO_FILE = 100       # số file mỗi nhạc cụ
NGUONG_DB = 25      # khung "có tiếng" nếu năng lượng không thấp hơn đỉnh của track quá 25 dB
                    # (ồn nền phòng thu khoảng -28..-30 dB, tiếng chơi nhẹ khoảng -19 dB)
TI_LE_CO_TIENG = 0.9  # đoạn hợp lệ nếu ít nhất 90% số khung có tiếng
random.seed(42)

NHOM = {"violin": "kéo vĩ", "viola": "kéo vĩ", "cello": "kéo vĩ", "double_bass": "kéo vĩ",
        "guitar_acoustic": "gảy", "guitar_electric": "gảy"}


def doc_mono(duong_dan):
    """Đọc file, trộn về mono, đổi tần số mẫu về SR."""
    y, _ = librosa.load(duong_dan, sr=SR, mono=True)
    return y


def tim_ranh_gioi_not(y):
    """Tìm thời điểm (giây) mà mỗi nốt mới chuẩn bị vang lên.

    onset_detect đo độ thay đổi của phổ giữa hai khung liên tiếp (spectral flux):
    đổi nốt -> các hài âm dịch sang tần số khác -> phổ thay đổi mạnh -> một onset.
    backtrack=True lùi mỗi onset về chỗ năng lượng thấp nhất ngay trước nó.
    """
    return librosa.onset.onset_detect(y=y, sr=SR, hop_length=HOP, backtrack=True, units="time")


def cat_doan(y, ten_goc):
    """Cắt track thành các đoạn dài khoảng 3 giây, đầu và cuối mỗi đoạn đều nằm ở ranh giới nốt.

    Chỉ giữ đoạn gần như liên tục có tiếng. Các đoạn nối tiếp nhau, không chồng lên nhau.
    Trả về danh sách (vị trí bắt đầu tính bằng giây, mảng mẫu, tên file gốc).
    """
    ranh_gioi = tim_ranh_gioi_not(y)
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=HOP)[0]
    db = librosa.amplitude_to_db(rms, ref=np.max)          # 0 dB = khung to nhất của track
    co_tieng = db > -NGUONG_DB

    ket_qua = []
    i = 0
    while i < len(ranh_gioi):
        bat_dau = ranh_gioi[i]
        # các ranh giới phía sau cách điểm bắt đầu từ 2,5 đến 3,5 giây; chọn cái gần 3 giây nhất
        ung_vien = [j for j in range(i + 1, len(ranh_gioi)) if DO_DAI_MIN <= ranh_gioi[j] - bat_dau <= DO_DAI_MAX]
        if not ung_vien:                                     # nốt ngân quá dài, không có chỗ kết thúc hợp lệ
            i += 1
            continue
        j = min(ung_vien, key=lambda k: abs(ranh_gioi[k] - bat_dau - DO_DAI))
        a, b = int(bat_dau * SR), int(ranh_gioi[j] * SR)
        if co_tieng[a // HOP:b // HOP].mean() >= TI_LE_CO_TIENG:
            ket_qua.append((bat_dau, y[a:b], ten_goc))
            i = j                                            # đoạn sau bắt đầu đúng chỗ đoạn này kết thúc
        else:
            i += 1
    return ket_qua


def lam_mem_mep(y):
    """Fade: nhân 50 ms đầu với hệ số tăng dần 0 -> 1 và 50 ms cuối với hệ số giảm dần 1 -> 0.

    Chỉ đổi độ to ở hai mép (không đổi cao độ, màu âm), để đoạn cắt không bị cụt / không có tiếng "tách".
    """
    n = int(FADE * SR)
    y = y.copy()
    y[:n] *= np.linspace(0, 1, n)
    y[-n:] *= np.linspace(1, 0, n)
    return y


def bo_track_trung(files):
    """Bỏ các track là cùng một bản thu.

    URMP phối một số bài cho nhiều đội hình (ví dụ Rondeau 35, 36, 37) và dùng lại y nguyên
    bản thu của bè giống nhau. Hai track coi là trùng nếu dài gần bằng nhau (lệch dưới 1 giây)
    và tín hiệu tương quan trên 0,99. Mỗi nhóm trùng chỉ giữ track đầu tiên.
    Trả về ({file giữ lại: tín hiệu}, [(track bị bỏ, track trùng với nó)]).
    """
    giu, bo = {}, []
    for f in files:
        x = doc_mono(f)
        for g, y in giu.items():
            n = min(len(x), len(y))
            if abs(len(x) - len(y)) < SR and np.corrcoef(x[:n], y[:n])[0, 1] > 0.99:
                bo.append((f.name, g.name))
                break
        else:
            giu[f] = x
    return giu, bo


def dau_van_tay(y):
    """Tóm tắt một đoạn thành vector để so độ giống giữa hai đoạn.

    Spectrogram thang Mel 64 dải (dB), lấy đều 32 thời điểm -> 64 x 32 = 2048 số,
    trừ trung bình rồi chia cho độ dài để vector có độ dài 1 (tích vô hướng = độ tương đồng cosine).
    """
    S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=SR, n_mels=64, hop_length=HOP))
    v = S[:, np.linspace(0, S.shape[1] - 1, 32).astype(int)].ravel()
    v = v - v.mean()
    return v / (np.linalg.norm(v) + 1e-9)


def lien_ke(a, chon):
    """Đoạn a có nối liền (đầu chạm cuối) với một đoạn đã chọn của cùng track không."""
    t_a, y_a, track_a = a
    for t_c, y_c, track_c in chon:
        if track_c == track_a and (abs(t_a - (t_c + len(y_c) / SR)) < 0.05 or abs(t_c - (t_a + len(y_a) / SR)) < 0.05):
            return True
    return False


def chon_rai_deu(theo_track, so_luong, thong_ke, cho_lien_ke=False):
    """Chọn `so_luong` đoạn, lần lượt lấy mỗi track một đoạn (round-robin), loại đoạn liền kề và đoạn gần giống.

    Rải đều trên nhiều track để dữ liệu đến từ nhiều bản nhạc / người chơi.
    Một ứng viên bị loại nếu nối liền với đoạn đã chọn của cùng track,
    hoặc có độ tương đồng cosine > NGUONG_GIONG với bất kỳ đoạn đã chọn nào của cùng nhạc cụ.
    """
    hang_doi = {k: random.sample(v, len(v)) for k, v in theo_track.items() if v}
    chon, van_tay = [], []
    while len(chon) < so_luong and hang_doi:
        for k in list(hang_doi):
            if len(chon) == so_luong:
                break
            while hang_doi[k]:
                ung_vien = hang_doi[k].pop()
                if not cho_lien_ke and lien_ke(ung_vien, chon):
                    thong_ke["bo_lien_ke"] += 1
                    continue
                v = dau_van_tay(ung_vien[1])
                if van_tay and np.max(np.array(van_tay) @ v) > NGUONG_GIONG:
                    thong_ke["bo_gan_giong"] += 1
                    continue
                chon.append(ung_vien)
                van_tay.append(v)
                break
            if not hang_doi[k]:
                del hang_doi[k]
    return chon


def nguon_cua(ten_file):
    """Bộ dữ liệu gốc của một track, suy ra từ tên file."""
    if ten_file.startswith("AuSep_"):
        return "URMP"
    if ten_file.startswith("PHENICX_"):
        return "PHENICX-Anechoic"
    if ten_file.startswith("Medley"):
        return "Medley-solos-DB"
    return "GuitarSet"


# Mỗi hàm tu_<...> trả về {nhạc cụ: ({track: [(vị trí, mẫu, tên file gốc), ...]}, số track gốc, [track trùng bị bỏ])}

def tu_bo_keo_vi():
    """4 nhạc cụ kéo vĩ: track riêng từng nhạc công (URMP: AuSep_*.wav, PHENICX: PHENICX_*.wav)."""
    ket_qua = {}
    for nhac_cu in ["violin", "viola", "cello", "double_bass"]:
        files = sorted((RAW / nhac_cu).glob("*.wav"))
        giu, trung = bo_track_trung(files)
        ket_qua[nhac_cu] = ({f.name: cat_doan(y, f.name) for f, y in giu.items()}, len(files), trung)
    return ket_qua


def tu_guitarset():
    """GuitarSet: mỗi file khoảng 30 giây guitar acoustic (đệm hợp âm hoặc chơi giai điệu)."""
    files = sorted((RAW / "guitar_acoustic").glob("*_mic.wav"))
    return {"guitar_acoustic": ({f.name: cat_doan(doc_mono(f), f.name) for f in files}, len(files), [])}


def tu_medley():
    """Medley-solos-DB: các đoạn đã cắt sẵn dài 2,97 giây (giữ nguyên); gom theo bài hát gốc (song_id)."""
    meta = pd.read_csv(RAW / "guitar_electric" / "Medley-solos-DB_metadata.csv")
    bai_hat = dict(zip(meta["uuid4"], meta["song_id"]))
    theo_bai = defaultdict(list)
    for f in sorted((RAW / "guitar_electric").glob("Medley*.wav")):
        theo_bai[bai_hat[f.stem.split("_")[-1]]].append((0.0, doc_mono(f), f.name))
    return {"guitar_electric": (theo_bai, len(theo_bai), [])}


def main():
    tat_ca = {**tu_bo_keo_vi(), **tu_guitarset(), **tu_medley()}
    dong, bang_loc, bang_trung = [], [], []
    for nhac_cu, (theo_track, so_track_goc, trung) in tat_ca.items():
        thong_ke = {"bo_lien_ke": 0, "bo_gan_giong": 0}
        chon = chon_rai_deu(theo_track, SO_FILE, thong_ke, cho_lien_ke=nhac_cu in CHO_PHEP_LIEN_KE)
        bang_loc.append({"instrument": nhac_cu, "so_track_goc": so_track_goc, "so_track_trung_bi_bo": len(trung),
                         "so_track_dung": len(theo_track), "so_doan_hop_le": sum(len(v) for v in theo_track.values()),
                         "bo_vi_lien_ke": thong_ke["bo_lien_ke"], "bo_vi_gan_giong": thong_ke["bo_gan_giong"],
                         "so_file_chon": len(chon)})
        bang_trung += [{"instrument": nhac_cu, "track_bi_bo": a, "trung_voi": b} for a, b in trung]
        print("  ".join(f"{k}={v}" for k, v in bang_loc[-1].items()))

        thu_muc = WAV / nhac_cu
        thu_muc.mkdir(parents=True, exist_ok=True)
        for i, (t, y, ten_goc) in enumerate(sorted(chon, key=lambda x: (x[2], x[0])), 1):
            y = 0.9 * y / (np.max(np.abs(y)) + 1e-9)     # chuẩn hóa biên độ đỉnh về 0,9
            y = lam_mem_mep(y)
            ten = f"{nhac_cu}_{i:03d}.wav"
            sf.write(thu_muc / ten, y, SR, subtype="PCM_16")
            dong.append({"file_name": ten, "file_path": f"data/wav/{nhac_cu}/{ten}", "instrument": nhac_cu,
                         "family": NHOM[nhac_cu], "source": nguon_cua(ten_goc), "source_file": ten_goc,
                         "start_s": round(t, 2), "duration_s": round(len(y) / SR, 2), "sample_rate": SR})

    meta = pd.DataFrame(dong)
    meta.insert(0, "file_id", range(1, len(meta) + 1))
    meta.to_csv(GOC / "data" / "metadata.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(bang_loc).to_csv(GOC / "reports" / "thong_ke_loc_du_lieu.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(bang_trung).to_csv(GOC / "reports" / "track_trung_bi_bo.csv", index=False, encoding="utf-8-sig")
    print(f"\nTổng: {len(meta)} file -> data/wav, bảng metadata -> data/metadata.csv")
    print("Thống kê lọc -> reports/thong_ke_loc_du_lieu.csv, track trùng -> reports/track_trung_bi_bo.csv")


if __name__ == "__main__":
    main()
