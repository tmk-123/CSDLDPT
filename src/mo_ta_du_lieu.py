"""Mô tả điểm giống và khác nhau giữa tiếng các nhạc cụ trong bộ dữ liệu (yêu cầu 1 của đề).

Cách chạy:
    .venv\\Scripts\\python.exe src\\mo_ta_du_lieu.py

Đầu vào : data/metadata.csv và 600 file trong data/wav
Đầu ra  : reports/hinh/*.png (hình cho báo cáo), reports/mo_ta_du_lieu.csv (số liệu theo nhạc cụ)
    1_song_va_spectrogram.png   dạng sóng + spectrogram của 1 file đại diện mỗi nhạc cụ
    2_am_vuc_f0.png             phân bố cao độ (f0) của từng nhạc cụ
    3_pho_trung_binh.png        phổ trung bình: năng lượng nằm ở vùng tần số nào
    4_duong_bao_sau_onset.png   năng lượng thay đổi thế nào sau khi một nốt bắt đầu
"""
from pathlib import Path

import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")
GOC = Path(__file__).resolve().parent.parent
HINH = GOC / "reports" / "hinh"
HINH.mkdir(parents=True, exist_ok=True)

SR, HOP = 22050, 512
THU_TU = ["violin", "viola", "cello", "double_bass", "guitar_acoustic", "guitar_electric"]
TEN_VN = {"violin": "Violin", "viola": "Viola", "cello": "Cello", "double_bass": "Double bass",
          "guitar_acoustic": "Guitar acoustic", "guitar_electric": "Guitar điện"}
MAU = {"violin": "#1f77b4", "viola": "#2ca02c", "cello": "#9467bd", "double_bass": "#8c564b",
       "guitar_acoustic": "#ff7f0e", "guitar_electric": "#d62728"}
# nốt thấp nhất (dây buông) theo lý thuyết, để so với số đo
NOT_THAP_NHAT = {"violin": ("G3", 196.0), "viola": ("C3", 130.8), "cello": ("C2", 65.4),
                 "double_bass": ("E1", 41.2), "guitar_acoustic": ("E2", 82.4), "guitar_electric": ("E2", 82.4)}


def doc(duong_dan):
    y, _ = librosa.load(GOC / duong_dan, sr=SR)
    return y


# ---------- 1. Dạng sóng + spectrogram ----------
def ve_song_va_spectrogram(meta):
    """Mỗi nhạc cụ một cột: trên là dạng sóng, dưới là spectrogram (thang tần số log, 30 Hz – 11 kHz)."""
    fig, ax = plt.subplots(2, 6, figsize=(20, 6.5), sharey="row")
    for c, nc in enumerate(THU_TU):
        file = meta[meta.instrument == nc].iloc[10]          # file thứ 11 của mỗi nhạc cụ làm đại diện
        y = doc(file.file_path)
        ax[0, c].plot(np.arange(len(y)) / SR, y, lw=0.3, color=MAU[nc])
        ax[0, c].set_title(f"{TEN_VN[nc]}\n{file.file_name}", fontsize=10)
        S = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=HOP)), ref=np.max)
        librosa.display.specshow(S, sr=SR, hop_length=HOP, x_axis="time", y_axis="log", ax=ax[1, c], vmin=-70)
        ax[1, c].set_ylim(30, 11025)
    ax[0, 0].set_ylabel("Biên độ")
    ax[1, 0].set_ylabel("Tần số (Hz)")
    fig.suptitle("Hình 1. Dạng sóng (trên) và spectrogram (dưới) của một file đại diện mỗi nhạc cụ")
    fig.tight_layout()
    fig.savefig(HINH / "1_song_va_spectrogram.png", dpi=110)
    plt.close(fig)


# ---------- 2. Âm vực ----------
def do_am_vuc(meta):
    """Ước lượng cao độ f0 từng khung bằng pYIN, lấy trung vị f0 của mỗi file (chỉ tính các khung có cao độ)."""
    f0_file = []
    for p in meta.file_path:
        f0, co_cao_do, _ = librosa.pyin(doc(p), fmin=30, fmax=2000, sr=SR, hop_length=HOP)
        f0_file.append(np.nanmedian(f0[co_cao_do]) if co_cao_do.any() else np.nan)
    meta = meta.assign(f0_trung_vi=f0_file)

    fig, ax = plt.subplots(figsize=(11, 5))
    du_lieu = [meta[meta.instrument == nc].f0_trung_vi.dropna() for nc in THU_TU]
    bp = ax.boxplot(du_lieu, tick_labels=[TEN_VN[nc] for nc in THU_TU], patch_artist=True, showfliers=True)
    for hop, nc in zip(bp["boxes"], THU_TU):
        hop.set_facecolor(MAU[nc])
        hop.set_alpha(0.6)
    for x, nc in enumerate(THU_TU, 1):
        ten, hz = NOT_THAP_NHAT[nc]
        ax.plot([x - 0.35, x + 0.35], [hz, hz], "k--", lw=1)
        ax.text(x + 0.37, hz, ten, va="center", fontsize=8)
    ax.set_yscale("log")
    ax.set_yticks([40, 65, 100, 200, 400, 800, 1600])
    ax.set_yticklabels(["40", "65", "100", "200", "400", "800", "1600"])
    ax.set_ylabel("Cao độ trung vị mỗi file f0 (Hz, thang log)")
    ax.set_title("Hình 2. Âm vực của từng nhạc cụ (nét đứt: nốt thấp nhất theo lý thuyết)")
    fig.tight_layout()
    fig.savefig(HINH / "2_am_vuc_f0.png", dpi=110)
    plt.close(fig)
    return meta


# ---------- 3. Phổ trung bình ----------
def do_pho_trung_binh(meta):
    """Phổ công suất trung bình của mỗi nhạc cụ (trung bình mọi khung của 100 file), chuẩn hóa đỉnh = 0 dB.

    Từ phổ trung bình tính tần số trung vị năng lượng: một nửa năng lượng nằm dưới tần số này.
    """
    tan_so = librosa.fft_frequencies(sr=SR, n_fft=2048)
    pho, f_trung_vi = {}, {}
    for nc in THU_TU:
        P = np.mean([np.mean(np.abs(librosa.stft(doc(p), hop_length=HOP)) ** 2, axis=1)
                     for p in meta[meta.instrument == nc].file_path], axis=0)
        pho[nc] = 10 * np.log10(P / P.max() + 1e-12)
        f_trung_vi[nc] = tan_so[np.searchsorted(np.cumsum(P) / P.sum(), 0.5)]

    fig, ax = plt.subplots(figsize=(11, 5))
    for nc in THU_TU:
        ax.plot(tan_so[1:], pho[nc][1:], color=MAU[nc], lw=1.4, label=f"{TEN_VN[nc]} (trung vị {f_trung_vi[nc]:.0f} Hz)")
    ax.set_xscale("log")
    ax.set_xlim(30, 11025)
    ax.set_ylim(-80, 3)
    ax.set_xlabel("Tần số (Hz, thang log)")
    ax.set_ylabel("Năng lượng (dB, đỉnh = 0)")
    ax.set_title("Hình 3. Phổ trung bình của từng nhạc cụ")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(HINH / "3_pho_trung_binh.png", dpi=110)
    plt.close(fig)
    return f_trung_vi


# ---------- 4. Đường bao năng lượng sau khi nốt bắt đầu ----------
def do_duong_bao(meta, do_dai=0.5, hop=256):
    """Năng lượng của một nốt thay đổi thế nào trong 0,5 giây kể từ lúc to nhất.

    Chỉ lấy các nốt ngân đủ dài (nốt kế tiếp đến sau ít nhất 0,5 giây), để phần tắt dần không bị nốt sau che.
    Với mỗi nốt: tìm đỉnh năng lượng trong 0,1 giây đầu, lấy RMS 0,5 giây kể từ đỉnh, đổi sang dB so với đỉnh.
    Kéo vĩ: vĩ tiếp tục cọ dây nên năng lượng giữ đều. Gảy: dây chỉ được kích một lần nên tắt dần.
    Trả về mức giảm năng lượng (dB) sau 0,4 giây và số nốt dùng để tính, cho mỗi nhạc cụ.
    """
    n, n_dinh = int(do_dai * SR / hop), int(0.1 * SR / hop)
    duong_bao, giam, so_not = {}, {}, {}
    for nc in THU_TU:
        cac_duong = []
        for p in meta[meta.instrument == nc].file_path:
            y = doc(p)
            rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0]
            onset = list(librosa.onset.onset_detect(y=y, sr=SR, hop_length=hop)) + [len(rms)]
            for k, k_sau in zip(onset, onset[1:]):
                if k_sau - k < n:                                   # nốt quá ngắn, bị nốt sau che
                    continue
                dinh = k + int(np.argmax(rms[k:k + n_dinh]))
                doan = rms[dinh:dinh + n]
                if len(doan) == n and dinh + n <= k_sau:
                    cac_duong.append(20 * np.log10(doan / (doan[0] + 1e-9) + 1e-9))
        duong_bao[nc] = np.median(cac_duong, axis=0)
        giam[nc] = duong_bao[nc][int(0.4 * SR / hop)]
        so_not[nc] = len(cac_duong)

    fig, ax = plt.subplots(figsize=(11, 5))
    t = np.arange(n) * hop / SR
    for nc in THU_TU:
        ax.plot(t, duong_bao[nc], color=MAU[nc], lw=2,
                label=f"{TEN_VN[nc]} (sau 0,4 s: {giam[nc]:.1f} dB; {so_not[nc]} nốt)")
    ax.set_xlabel("Thời gian kể từ lúc nốt to nhất (giây)")
    ax.set_ylabel("Năng lượng so với đỉnh (dB)")
    ax.set_title("Hình 4. Đường bao năng lượng trung vị của các nốt ngân dài ≥ 0,5 giây")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HINH / "4_duong_bao_sau_onset.png", dpi=110)
    plt.close(fig)
    return giam


def main():
    meta = pd.read_csv(GOC / "data" / "metadata.csv")
    ve_song_va_spectrogram(meta)
    print("1. đã vẽ dạng sóng + spectrogram")
    f_trung_vi = do_pho_trung_binh(meta)
    print("3. đã vẽ phổ trung bình")
    giam = do_duong_bao(meta)
    print("4. đã vẽ đường bao sau onset")
    meta = do_am_vuc(meta)
    print("2. đã đo âm vực (pYIN)")

    bang = meta.groupby("instrument").f0_trung_vi.describe(percentiles=[0.1, 0.5, 0.9])[["10%", "50%", "90%"]]
    bang.columns = ["f0_p10_Hz", "f0_trung_vi_Hz", "f0_p90_Hz"]
    bang["tan_so_trung_vi_nang_luong_Hz"] = pd.Series(f_trung_vi)
    bang["giam_nang_luong_sau_0_4s_dB"] = pd.Series(giam)
    bang = bang.loc[THU_TU].round(1)
    bang.to_csv(GOC / "reports" / "mo_ta_du_lieu.csv", encoding="utf-8-sig")
    meta[["file_name", "instrument", "f0_trung_vi"]].to_csv(GOC / "reports" / "f0_theo_file.csv", index=False, encoding="utf-8-sig")
    print(bang.to_string())


if __name__ == "__main__":
    main()
