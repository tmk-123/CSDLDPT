"""Xem một file âm thanh: in thông tin file và vẽ 4 hình (dạng sóng, phóng to, phổ, spectrogram).

Cách chạy:
    .venv\\Scripts\\python.exe src\\xem_am_thanh.py <đường dẫn file âm thanh> [giây]

    [giây] không bắt buộc: thời điểm bắt đầu đoạn 0,3 s dùng để vẽ hình 2 và hình 3.
    Bỏ trống thì tự lấy phần ngân của nốt đầu tiên.

Hình được lưu vào reports/thu_nghiem/<tên file>.png
"""
import sys
from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

SR = 22050  # tần số mẫu dùng để phân tích (Nyquist = 11 025 Hz)


def in_thong_tin(duong_dan):
    """In thông tin gốc của file: tần số mẫu, số kênh, độ sâu bit, độ dài."""
    info = sf.info(duong_dan)
    print(f"File           : {Path(duong_dan).name}")
    print(f"Định dạng      : {info.format} / {info.subtype}")
    print(f"Tần số mẫu gốc : {info.samplerate} Hz")
    print(f"Số kênh        : {info.channels} ({'stereo' if info.channels == 2 else 'mono'})")
    print(f"Số mẫu         : {info.frames:,}")
    print(f"Độ dài         : {info.duration:.2f} giây")


def doan_on_dinh(y, sr, giay=None, do_dai=0.3):
    """Lấy đoạn dài `do_dai` giây để vẽ phổ.

    Nếu không chỉ định `giay`: tìm chỗ nốt đầu tiên bắt đầu (onset) rồi lấy từ 0,2 s sau đó,
    tức là bỏ qua phần attack, lấy phần ngân của nốt.
    """
    if giay is None:
        onset = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=True)
        giay = (onset[0] if len(onset) else 0.0) + 0.2
    bat_dau = int(giay * sr)
    return y[bat_dau: bat_dau + int(do_dai * sr)], bat_dau / sr


def main(duong_dan, giay=None):
    in_thong_tin(duong_dan)

    # Đọc file: trộn về mono và đổi tần số mẫu về 22 050 Hz
    y, sr = librosa.load(duong_dan, sr=SR, mono=True)
    print(f"Sau khi load   : mono, {sr} Hz, {len(y):,} mẫu, giá trị trong [{y.min():.3f}, {y.max():.3f}]")

    fig, ax = plt.subplots(4, 1, figsize=(12, 10), layout="constrained")
    fig.suptitle(Path(duong_dan).name)

    # 1. Dạng sóng của cả file
    librosa.display.waveshow(y, sr=sr, ax=ax[0])
    ax[0].set_title("1. Dạng sóng (cả file)")
    ax[0].set_xlabel("thời gian (s)")

    # 2. Phóng to 20 ms trong phần ngân để thấy từng chu kỳ
    doan, t0 = doan_on_dinh(y, sr, giay)
    n = int(0.02 * sr)
    t = t0 + np.arange(n) / sr
    ax[1].plot(t, doan[:n])
    ax[1].set_title(f"2. Phóng to 20 ms (từ giây {t0:.2f}): thấy được các chu kỳ lặp lại")
    ax[1].set_xlabel("thời gian (s)")

    # 3. Phổ của đoạn 0,3 s đó: FFT có nhân cửa sổ Hann
    cua_so = np.hanning(len(doan))
    bien_do = np.abs(np.fft.rfft(doan * cua_so))
    tan_so = np.fft.rfftfreq(len(doan), d=1 / sr)
    db = 20 * np.log10(bien_do / bien_do.max() + 1e-10)
    dinh = tan_so[np.argmax(bien_do)]
    ax[2].plot(tan_so, db)
    ax[2].set_xlim(0, 5000)
    ax[2].set_ylim(-80, 5)
    ax[2].set_title(f"3. Phổ của đoạn 0,3 s: mỗi đỉnh là một hài âm (đỉnh cao nhất ≈ {dinh:.0f} Hz)")
    ax[2].set_xlabel("tần số (Hz)")
    ax[2].set_ylabel("dB")
    ax[2].grid(alpha=0.3)
    print(f"Đỉnh phổ cao nhất của đoạn ngân: {dinh:.1f} Hz")

    # 4. Spectrogram: STFT với khung 2048 mẫu, bước nhảy 512 mẫu
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_db, sr=sr, hop_length=512, x_axis="time", y_axis="log", ax=ax[3])
    ax[3].set_title("4. Spectrogram (trục tần số log, màu = dB)")
    fig.colorbar(img, ax=ax[3], format="%+2.0f dB")

    thu_muc = Path("reports/thu_nghiem")
    thu_muc.mkdir(parents=True, exist_ok=True)
    noi_luu = thu_muc / (Path(duong_dan).stem + ".png")
    fig.savefig(noi_luu, dpi=110)
    print(f"Đã lưu hình    : {noi_luu}")
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) == 3 else None)
