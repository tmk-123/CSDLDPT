"""Vẽ các hình minh họa QUÁ TRÌNH dựng bộ dữ liệu (dùng trong báo cáo phần 1) và in số liệu ví dụ.

Cách chạy:
    .venv\\Scripts\\python.exe src\\ve_hinh_quy_trinh.py

Đầu ra (reports/hinh):
    0_so_do_quy_trinh.png      sơ đồ các bước từ dữ liệu thô đến 600 file
    q1_nguong_co_tieng.png     năng lượng RMS (dB) của track violin Jupiter và hai ngưỡng -30 / -25 dB
    q2_cat_theo_not.png        dạng sóng, spectrogram, spectral flux và các điểm cắt trên track Jupiter
    q3_fade.png                mép một đoạn trước và sau khi làm mềm (fade)
"""
from pathlib import Path

import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import tao_bo_du_lieu as t

matplotlib.use("Agg")
HINH = t.GOC / "reports" / "hinh"
HINH.mkdir(parents=True, exist_ok=True)
JUPITER = t.RAW / "violin" / "AuSep_1_vn_01_Jupiter.wav"


def so_do_quy_trinh():
    buoc = ["Dữ liệu thô\n(URMP, PHENICX, GuitarSet, Medley)", "1. Đọc file\nmono, 22 050 Hz",
            "2. Đánh dấu khung\ncó tiếng (RMS, -25 dB)", "3. Tìm ranh giới nốt\n(spectral flux)",
            "4. Cắt đoạn 2,5–3,5 s\ntheo ranh giới nốt", "5. Bỏ track trùng\n(tương quan > 0,99)",
            "6–8. Chọn 100 đoạn/nhạc cụ\nrải đều, không liền kề,\nbỏ gần giống (cos > 0,95)",
            "9–10. Chuẩn hóa đỉnh 0,9\nfade 50 ms", "11. Ghi WAV + metadata\n600 file"]
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.axis("off")
    for i, b in enumerate(buoc):
        y = 1 - i * 0.11
        ax.text(0.5, y, b, ha="center", va="center", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.5", fc="#e8f0fa" if i else "#fdebd3", ec="#456"))
        if i < len(buoc) - 1:
            ax.annotate("", xy=(0.5, y - 0.075), xytext=(0.5, y - 0.035), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_ylim(0.05, 1.05)
    fig.savefig(HINH / "0_so_do_quy_trinh.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def nguong_co_tieng(y):
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=t.HOP)[0]
    db = librosa.amplitude_to_db(rms, ref=np.max)
    tg = librosa.times_like(rms, sr=t.SR, hop_length=t.HOP)
    m = tg < 15
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(tg[m], db[m], lw=1)
    ax.axhline(-30, color="gray", ls="--", label="ngưỡng cũ -30 dB")
    ax.axhline(-25, color="red", ls="--", label="ngưỡng dùng -25 dB")
    ax.axvline(4.74, color="green", lw=1, label="violin bắt đầu chơi (4,74 s)")
    ax.set_xlabel("Thời gian (giây)")
    ax.set_ylabel("RMS so với khung to nhất (dB)")
    ax.set_title("Năng lượng từng khung của track violin Jupiter (15 giây đầu)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HINH / "q1_nguong_co_tieng.png", dpi=110)
    plt.close(fig)
    print("Ví dụ RMS/dB từng khung:")
    for s in [1.0, 3.0, 4.6, 5.0, 8.0, 13.5]:
        k = int(s * t.SR / t.HOP)
        print(f"  giây {s:4.1f}  khung {k:4d}  RMS={rms[k]:.4f}  dB={db[k]:6.1f}  "
              f"-30dB:{'có' if db[k] > -30 else 'không'}  -25dB:{'có' if db[k] > -25 else 'không'}")
    print(f"  RMS lớn nhất của track = {rms.max():.4f}; số khung = {len(rms)}")


def cat_theo_not(y):
    T = 18
    y18 = y[:int(T * t.SR)]
    rg = t.tim_ranh_gioi_not(y18)
    ds = t.cat_doan(y18, JUPITER.name)
    mep = sorted({round(s, 3) for s, _, _ in ds} | {round(s + len(g) / t.SR, 3) for s, g, _ in ds})
    fig, ax = plt.subplots(3, 1, figsize=(13, 8), sharex=True)
    ax[0].plot(np.arange(len(y18)) / t.SR, y18, lw=0.4)
    ax[0].set_title("1. Dạng sóng")
    S = librosa.amplitude_to_db(np.abs(librosa.stft(y18, hop_length=t.HOP)), ref=np.max)
    librosa.display.specshow(S, sr=t.SR, hop_length=t.HOP, x_axis="time", y_axis="log", ax=ax[1])
    ax[1].set_ylim(150, 6000)
    ax[1].set_title("2. Spectrogram: khi đổi nốt, các vạch hài âm cùng nhảy lên/xuống")
    env = librosa.onset.onset_strength(y=y18, sr=t.SR, hop_length=t.HOP)
    ax[2].plot(librosa.times_like(env, sr=t.SR, hop_length=t.HOP), env, lw=1)
    ax[2].set_title("3. Hàm onset strength (spectral flux): vạch xám = ranh giới nốt, vạch đỏ = điểm cắt đoạn")
    ax[2].set_xlabel("Thời gian (giây)")
    for a in ax:
        for r in rg:
            a.axvline(r, color="gray", lw=0.6, alpha=0.6)
        for b in mep:
            a.axvline(b, color="red", lw=2)
    fig.tight_layout()
    fig.savefig(HINH / "q2_cat_theo_not.png", dpi=100)
    plt.close(fig)

    ds_ca = t.cat_doan(y, JUPITER.name)
    rg_ca = t.tim_ranh_gioi_not(y)
    print(f"\nTrack Jupiter dài {len(y) / t.SR:.1f} s, {len(rg_ca)} ranh giới nốt; 10 ranh giới đầu: {np.round(rg_ca[:10], 2)}")
    print(f"Cắt được {len(ds_ca)} đoạn:")
    for s, g, _ in ds_ca:
        print(f"  {s:6.2f} -> {s + len(g) / t.SR:6.2f} s  (dài {len(g) / t.SR:.2f} s)")
    print("Giá trị onset strength quanh ranh giới đầu tiên (khung, giây, giá trị):")
    k0 = int(rg_ca[0] * t.SR / t.HOP)
    env_ca = librosa.onset.onset_strength(y=y, sr=t.SR, hop_length=t.HOP)
    for k in range(k0 - 2, k0 + 5):
        print(f"  khung {k}  {k * t.HOP / t.SR:.3f} s  {env_ca[k]:.2f}")


def fade(y):
    s, g, _ = t.cat_doan(y, JUPITER.name)[5]
    g = 0.9 * g / np.abs(g).max()
    g2 = t.lam_mem_mep(g)
    n = int(0.12 * t.SR)
    tg = np.arange(n) / t.SR * 1000
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.6), sharey=True)
    ax[0].plot(tg, g[:n], lw=0.6, label="trước fade")
    ax[0].plot(tg, g2[:n], lw=0.6, label="sau fade")
    ax[0].plot(tg, np.clip(tg / 50, 0, 1) * 0.9, "k--", lw=1, label="hệ số nhân (×0,9)")
    ax[0].set_title("Đầu đoạn (120 ms đầu)")
    ax[0].set_xlabel("ms")
    ax[1].plot(tg, g[-n:], lw=0.6)
    ax[1].plot(tg, g2[-n:], lw=0.6)
    ax[1].plot(tg, np.clip((120 - tg) / 50, 0, 1) * 0.9, "k--", lw=1)
    ax[1].set_title("Cuối đoạn (120 ms cuối)")
    ax[1].set_xlabel("ms")
    ax[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HINH / "q3_fade.png", dpi=110)
    plt.close(fig)
    print(f"\nVí dụ fade trên đoạn bắt đầu ở {s:.2f} s: 5 mẫu đầu trước fade {np.round(g[:5], 4)}, sau fade {np.round(g2[:5], 5)}")


def main():
    y = t.doc_mono(JUPITER)
    so_do_quy_trinh()
    nguong_co_tieng(y)
    cat_theo_not(y)
    fade(y)


if __name__ == "__main__":
    main()
