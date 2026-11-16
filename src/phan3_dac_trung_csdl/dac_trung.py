"""Trích đặc trưng âm thanh cho một tín hiệu (yêu cầu 3).

Module dùng chung cho tệp trong CSDL và cho tệp truy vấn, nhờ vậy hai bên luôn được tính giống hệt nhau.
Mỗi đặc trưng được tính theo khung (2 048 mẫu, bước nhảy 512), rồi tóm tắt bằng trung bình (mean) và
độ lệch chuẩn (std) theo thời gian -> vector có độ dài cố định, dù tệp dài ngắn khác nhau.

- Bộ ỨNG VIÊN (72 chiều, 7 loại): mọi đặc trưng đã đem ra đánh giá (src/phan4_tim_kiem/chon_dac_trung.py).
- Bộ ĐÃ CHỐT (46 chiều, 5 loại): lưu trong CSDL. Centroid (trùng thông tin với Roll-off, r = 0,98) và
  Chroma (làm giảm kết quả truy vấn, ít thông tin về nhạc cụ) bị bỏ sau đánh giá.
- CHIEU_TRUY_VAN (15 chiều): MFCC 13 mean + Roll-off mean/std, đo độ tương đồng bằng cosine.
  Các chiều còn lại được lưu để giải thích kết quả (kéo vĩ / gảy, nhận ra nhạc cụ không phải dây).
"""
import librosa
import numpy as np

SR = 22050              # tần số lấy mẫu
N_FFT = 2048            # độ dài khung (~92,9 ms)
HOP = 512               # bước nhảy (~23,2 ms)
N_MFCC = 13             # số hệ số MFCC
NGUONG_ROLLOFF = 0.85   # roll-off: tần số chứa 85% tổng biên độ phổ
SO_LOP_CHROMA = 12      # 12 lớp cao độ (chỉ còn trong bộ ứng viên)
SO_DAI_CONTRAST = 7     # Spectral Contrast: 6 dải octave + 1 dải trên cùng
DO_DO = "cosine"        # độ đo tương đồng khi truy vấn
PHIEN_BAN = (f"sr={SR};n_fft={N_FFT};hop={HOP};n_mfcc={N_MFCC};rolloff={NGUONG_ROLLOFF};"
             f"contrast_bands={SO_DAI_CONTRAST};pool=mean+std")

TK = ("mean", "std")
LOAI_UNG_VIEN = {
    "RMS": ["rms_mean", "rms_std"],
    "ZCR": ["zcr_mean", "zcr_std"],
    "Centroid": ["centroid_mean", "centroid_std"],
    "Roll-off": ["rolloff_mean", "rolloff_std"],
    "MFCC": [f"mfcc_{i}_{t}" for i in range(N_MFCC) for t in TK],
    "Chroma": [f"chroma_{i}_{t}" for i in range(SO_LOP_CHROMA) for t in TK],
    "Spectral Contrast": [f"contrast_{i}_{t}" for i in range(SO_DAI_CONTRAST) for t in TK],
}
TEN_CHIEU_UNG_VIEN = [c for ds in LOAI_UNG_VIEN.values() for c in ds]               # 72 chiều

LOAI = {l: LOAI_UNG_VIEN[l] for l in ["RMS", "ZCR", "Roll-off", "MFCC", "Spectral Contrast"]}
TEN_CHIEU = [c for ds in LOAI.values() for c in ds]                                   # 46 chiều lưu CSDL
LOAI_CUA_CHIEU = {c: l for l, ds in LOAI_UNG_VIEN.items() for c in ds}
CHIEU_TRUY_VAN = [f"mfcc_{i}_mean" for i in range(N_MFCC)] + ["rolloff_mean", "rolloff_std"]   # 15 chiều


def doc_tin_hieu(duong_dan):
    """Đọc tệp âm thanh thành tín hiệu mono, tần số lấy mẫu 22 050 Hz."""
    y, _ = librosa.load(duong_dan, sr=SR, mono=True)
    return y


def chuoi_theo_khung(y):
    """Tính 36 chuỗi đặc trưng ứng viên theo khung. Trả về dict: tên chuỗi -> mảng M giá trị (M = số khung)."""
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP))       # biên độ phổ |X(m,k)|, 1025 x M
    P = S ** 2                                                        # phổ công suất |X(m,k)|^2
    mel_db = librosa.power_to_db(librosa.feature.melspectrogram(S=P, sr=SR))   # 128 dải Mel, theo dB
    mfcc = librosa.feature.mfcc(S=mel_db, n_mfcc=N_MFCC)               # 13 x M (DCT của phổ log-Mel)
    chroma = librosa.feature.chroma_stft(S=P, sr=SR)                  # 12 x M
    contrast = librosa.feature.spectral_contrast(S=S, sr=SR)          # 7 x M (dB, đỉnh trừ đáy mỗi dải)

    kq = {
        "rms": librosa.feature.rms(y=y, frame_length=N_FFT, hop_length=HOP)[0],
        "zcr": librosa.feature.zero_crossing_rate(y, frame_length=N_FFT, hop_length=HOP)[0],
        "centroid": librosa.feature.spectral_centroid(S=S, sr=SR)[0],
        "rolloff": librosa.feature.spectral_rolloff(S=S, sr=SR, roll_percent=NGUONG_ROLLOFF)[0],
    }
    kq.update({f"mfcc_{i}": mfcc[i] for i in range(N_MFCC)})
    kq.update({f"chroma_{i}": chroma[i] for i in range(SO_LOP_CHROMA)})
    kq.update({f"contrast_{i}": contrast[i] for i in range(SO_DAI_CONTRAST)})
    return kq


def trich_ung_vien(y):
    """Vector 72 chiều của bộ ứng viên (dict theo thứ tự TEN_CHIEU_UNG_VIEN)."""
    vec = {}
    for ten, g in chuoi_theo_khung(y).items():
        vec[f"{ten}_mean"] = float(np.mean(g))
        vec[f"{ten}_std"] = float(np.std(g))     # độ lệch chuẩn tổng thể (chia cho M)
    return {k: vec[k] for k in TEN_CHIEU_UNG_VIEN}


def trich_dac_trung(y):
    """Vector 46 chiều đã chốt (dict theo thứ tự TEN_CHIEU), dùng cho CSDL và truy vấn."""
    v = trich_ung_vien(y)
    return {k: v[k] for k in TEN_CHIEU}
