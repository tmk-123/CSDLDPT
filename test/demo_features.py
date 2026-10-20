import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import librosa
import numpy as np
import matplotlib.pyplot as plt

WAV_DIR = Path("data/wav")
SR = 22050
N = 2048
HOP = 512

# 4 file đại diện cho 4 phong cách đối lập
samples = {
    "Violin": WAV_DIR / "violin" / "violin_001.wav",
    "Double Bass": WAV_DIR / "double_bass" / "double_bass_001.wav",
    "Guitar Acoustic": WAV_DIR / "guitar_acoustic" / "guitar_acoustic_001.wav",
    "Guitar Electric": WAV_DIR / "guitar_electric" / "guitar_electric_001.wav",
}

data = {}
print("=" * 80)
print("TRÍCH XUẤT ĐẶC TRƯNG THỰC TẾ TRÊN 4 NHẠC CỤ ĐỐI LẬP")
print("=" * 80)

for name, path in samples.items():
    y, sr = librosa.load(path, sr=SR, mono=True)
    rms = librosa.feature.rms(y=y, frame_length=N, hop_length=HOP)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=N, hop_length=HOP)[0]
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N, hop_length=HOP)[0]
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=N, hop_length=HOP)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=N, hop_length=HOP)
    
    data[name] = {
        "y": y,
        "rms_mean": np.mean(rms), "rms_std": np.std(rms),
        "zcr_mean": np.mean(zcr), "zcr_std": np.std(zcr),
        "centroid_mean": np.mean(centroid), "centroid_std": np.std(centroid),
        "rolloff_mean": np.mean(rolloff), "rolloff_std": np.std(rolloff),
        "mfcc_mean": np.mean(mfcc, axis=1),
        "chroma_mean": np.mean(chroma, axis=1),
        "rms": rms, "centroid": centroid, "rolloff": rolloff,
    }
    print(f"\n>>> [{name}]:")
    print(f"  - RMS Mean: {data[name]['rms_mean']:.4f} | RMS Std (độ biến thiên): {data[name]['rms_std']:.4f}")
    print(f"  - ZCR Mean (độ nhám/méo sóng): {data[name]['zcr_mean']:.4f}")
    print(f"  - Spectral Centroid Mean (độ sáng): {data[name]['centroid_mean']:.1f} Hz")
    print(f"  - Spectral Roll-off 85% Mean (trần dải tần): {data[name]['rolloff_mean']:.1f} Hz")
    print(f"  - MFCC c0, c1, c2: [{data[name]['mfcc_mean'][0]:.1f}, {data[name]['mfcc_mean'][1]:.1f}, {data[name]['mfcc_mean'][2]:.1f}]")

# Vẽ biểu đồ so sánh 4 panel cực nét
fig, axs = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
colors = {"Violin": "#0d6b70", "Double Bass": "#2c3e50", "Guitar Acoustic": "#b9770e", "Guitar Electric": "#c0392b"}

# Panel 1: Độ sáng phổ (Centroid) và Trần năng lượng (Roll-off)
inst_names = list(samples.keys())
centroids = [data[k]["centroid_mean"] for k in inst_names]
rolloffs = [data[k]["rolloff_mean"] for k in inst_names]
x = np.arange(len(inst_names))
w = 0.35

axs[0, 0].bar(x - w/2, centroids, width=w, label="Trọng tâm phổ Centroid (Độ sáng)", color="#0d6b70")
axs[0, 0].bar(x + w/2, rolloffs, width=w, label="Tần số cuộn Roll-off 85% (Trần năng lượng)", color="#b9770e")
axs[0, 0].set_xticks(x)
axs[0, 0].set_xticklabels(inst_names, fontweight="bold")
axs[0, 0].set_ylabel("Tần số (Hz)")
axs[0, 0].set_title("1. Trọng tâm phổ Centroid & Spectral Roll-off 85%", fontweight="bold")
axs[0, 0].grid(True, linestyle="--", alpha=0.4)
axs[0, 0].legend()

# Panel 2: Biến thiên RMS (Std) & Độ nhám dạng sóng ZCR
rms_stds = [data[k]["rms_std"] for k in inst_names]
zcr_means = [data[k]["zcr_mean"] for k in inst_names]
axs[0, 1].bar(x - w/2, rms_stds, width=w, label="Độ biến thiên RMS (Std) - Gảy tắt dốc vs Kéo đều", color="#2980b9")
axs[0, 1].bar(x + w/2, zcr_means, width=w, label="Tốc độ qua 0 (ZCR) - Độ méo tiếng/nhám", color="#e74c3c")
axs[0, 1].set_xticks(x)
axs[0, 1].set_xticklabels(inst_names, fontweight="bold")
axs[0, 1].set_ylabel("Giá trị chuẩn hóa")
axs[0, 1].set_title("2. Động thái năng lượng RMS (Std) & Độ nhám méo sóng ZCR", fontweight="bold")
axs[0, 1].grid(True, linestyle="--", alpha=0.4)
axs[0, 1].legend()

# Panel 3: 13 hệ số MFCC bóc tách đường bao phổ thùng đàn
for name in inst_names:
    axs[1, 0].plot(range(13), data[name]["mfcc_mean"], marker="o", label=name, color=colors[name], lw=2)
axs[1, 0].set_title("3. 13 hệ số MFCC bóc tách đặc trưng âm sắc thùng đàn", fontweight="bold")
axs[1, 0].set_xlabel("Hệ số MFCC (từ c0 đến c12)")
axs[1, 0].set_ylabel("Biên độ hệ số Cepstral")
axs[1, 0].grid(True, linestyle="--", alpha=0.4)
axs[1, 0].legend()

# Panel 4: Phân bố năng lượng 12 nửa cung Chroma
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for name in inst_names:
    axs[1, 1].plot(notes, data[name]["chroma_mean"], marker="s", label=name, color=colors[name], lw=1.8)
axs[1, 1].set_title("4. Đặc trưng 12 lớp cao độ Chroma STFT", fontweight="bold")
axs[1, 1].set_xlabel("Nửa cung chuẩn nhạc lý")
axs[1, 1].set_ylabel("Mức năng lượng đóng góp (L1 norm)")
axs[1, 1].grid(True, linestyle="--", alpha=0.4)
axs[1, 1].legend()

out_fig = Path("test/minh_hoa_dac_trung_so_sanh.png")
plt.savefig(out_fig, dpi=180)
print(f"\n[THÀNH CÔNG] Đã lưu đồ thị so sánh đặc trưng tại: {out_fig.resolve()}")
