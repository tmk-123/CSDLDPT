"""Script chạy thực tế trên file test/sample_violin.wav
để bóc tách từng bước tính toán của công thức RMS và Decibel.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import librosa
import numpy as np
import matplotlib.pyplot as plt

# 1. Đường dẫn file
AUDIO_PATH = Path("test/sample_violin.wav")
SR = 22050
N = 2048   # Frame size
HOP = 512  # Hop size

# 2. Đọc file âm thanh chuẩn hóa mono, sr=22050
print("=" * 70)
print("BƯỚC 1: ĐỌC DỮ LIỆU ÂM THANH THỰC TẾ")
print("=" * 70)
y, sr = librosa.load(AUDIO_PATH, sr=SR, mono=True)
print(f"File: {AUDIO_PATH}")
print(f"Tổng số mẫu: {len(y)} mẫu | Tần số mẫu: {sr} Hz")
print(f"Tổng thời lượng: {len(y) / sr:.2f} giây")

# 3. Chia khung và tính RMS bằng librosa
rms_all = librosa.feature.rms(y=y, frame_length=N, hop_length=HOP)[0]
max_rms = np.max(rms_all)
db_all = 20 * np.log10(rms_all / (max_rms + 1e-9))
times = librosa.times_like(rms_all, sr=sr, hop_length=HOP)

# Chọn 2 khung đại diện:
# Khung 1: Đoạn đầu (chưa kéo đàn, chỉ có tiếng xì mic phòng thu)
# Khung 2: Đoạn đang kéo đàn vang to
idx_silence = int(1.5 * sr / HOP)   # khoảng giây thứ 1.5
idx_violin  = int(5.0 * sr / HOP)   # khoảng giây thứ 5.0

print("\n" + "=" * 70)
print("BƯỚC 2: SO SÁNH TỪNG BƯỚC TÍNH TOÁN GIỮA 2 KHUNG THỰC TẾ")
print("=" * 70)

for ten_khung, idx in [("KHUNG IM LẶNG / TẠP ÂM (giây thứ 1.5)", idx_silence),
                       ("KHUNG CÓ TIẾNG VIOLIN (giây thứ 5.0)", idx_violin)]:
    start_sample = idx * HOP
    frame_samples = y[start_sample : start_sample + N]
    
    # Bước S: Square (Bình phương từng mẫu)
    squared = frame_samples ** 2
    
    # Bước M: Mean (Lấy trung bình cộng tổng bình phương)
    sum_squared = np.sum(squared)
    mean_square = sum_squared / N
    
    # Bước R: Root (Khai căn bậc hai)
    rms_val = np.sqrt(mean_square)
    
    # Đổi sang dB
    db_val = 20 * np.log10(rms_val / (max_rms + 1e-9))
    co_tieng = db_val > -25.0

    print(f"\n>>> {ten_khung}:")
    print(f"  - 5 mẫu biên độ đầu tiên x_m[n]   : {np.round(frame_samples[:5], 6)}")
    print(f"  - 5 mẫu bình phương x_m[n]^2      : {np.round(squared[:5], 8)}")
    print(f"  - 1. Tổng bình phương Σ x_m[n]^2  : {sum_squared:.6f}")
    print(f"  - 2. Chia N=2048 (Mean Square)    : {mean_square:.8f}")
    print(f"  - 3. Khai căn sqrt(...) = RMS     : {rms_val:.6f}")
    print(f"  - 4. Max RMS của toàn bài         : {max_rms:.6f}")
    print(f"  - 5. Quy đổi ra Decibel           : {db_val:.2f} dB")
    print(f"  - 6. So sánh ngưỡng -25 dB        : {db_val:.2f} dB > -25 dB ? ==> {'CÓ TIẾNG ĐÀN (Giữ lại)' if co_tieng else 'IM LẶNG / NHIỄU (Bỏ)'}")

# 4. Vẽ đồ thị minh họa trực quan
plt.style.use('default')
fig, axs = plt.subplots(3, 1, figsize=(12, 10), constrained_layout=True)

# Đồ thị 1: Sóng âm toàn bài và vị trí 2 khung
time_axis = np.linspace(0, len(y) / sr, len(y))
axs[0].plot(time_axis, y, color='#55666d', alpha=0.6, label='Tín hiệu sóng âm y(t)')
t_s = idx_silence * HOP / sr
t_v = idx_violin * HOP / sr
axs[0].axvspan(t_s, t_s + N/sr, color='#e74c3c', alpha=0.5, label=f'Khung im lặng ({db_all[idx_silence]:.1f} dB)')
axs[0].axvspan(t_v, t_v + N/sr, color='#0d6b70', alpha=0.6, label=f'Khung kéo đàn ({db_all[idx_violin]:.1f} dB)')
axs[0].set_title('1. Dạng sóng âm thanh toàn bài (Waveform) & Vị trí 2 khung khảo sát', fontsize=12, fontweight='bold')
axs[0].set_xlabel('Thời gian (giây)')
axs[0].set_ylabel('Biên độ [-1, 1]')
axs[0].grid(True, linestyle='--', alpha=0.4)
axs[0].legend(loc='upper right')

# Đồ thị 2: So sánh dạng sóng chi tiết của 2 khung (2048 mẫu)
s_samples = y[idx_silence * HOP : idx_silence * HOP + N]
v_samples = y[idx_violin * HOP : idx_violin * HOP + N]
sample_idx = np.arange(N)

axs[1].plot(sample_idx, v_samples, color='#0d6b70', label=f'Khung kéo đàn (RMS={rms_all[idx_violin]:.4f})')
axs[1].plot(sample_idx, s_samples, color='#e74c3c', label=f'Khung im lặng (RMS={rms_all[idx_silence]:.4f})')
axs[1].set_title('2. Cận cảnh N=2048 mẫu bên trong khung: Dao động mạnh (Xanh) vs Tiếng xì mic (Đỏ)', fontsize=12, fontweight='bold')
axs[1].set_xlabel('Chỉ số mẫu n (từ 0 đến 2047)')
axs[1].set_ylabel('Biên độ x[n]')
axs[1].grid(True, linestyle='--', alpha=0.4)
axs[1].legend(loc='upper right')

# Đồ thị 3: Đường mức Decibel và ngưỡng -25 dB
axs[2].plot(times, db_all, color='#0d6b70', lw=1.5, label='Mức năng lượng L_dB(m)')
axs[2].axhline(-25, color='#e74c3c', linestyle='--', lw=2, label='Ngưỡng lọc -25 dB')
axs[2].fill_between(times, -60, db_all, where=(db_all > -25), color='#2ecc71', alpha=0.25, label='Khung ĐƯỢC CHỌN (Có tiếng > -25 dB)')
axs[2].fill_between(times, -60, db_all, where=(db_all <= -25), color='#95a5a6', alpha=0.3, label='Khung BỊ LOẠI (Khoảng lặng <= -25 dB)')
axs[2].set_title('3. Phân loại Khung có tiếng vs Khung khoảng lặng bằng ngưỡng L_dB > -25 dB', fontsize=12, fontweight='bold')
axs[2].set_xlabel('Thời gian (giây)')
axs[2].set_ylabel('Mức năng lượng (dB)')
axs[2].set_ylim([-55, 5])
axs[2].grid(True, linestyle='--', alpha=0.4)
axs[2].legend(loc='lower right')

output_img = Path("test/minh_hoa_rms.png")
plt.savefig(output_img, dpi=180)
print(f"\n[THÀNH CÔNG] Đã lưu hình ảnh minh họa chi tiết tại: {output_img.resolve()}")
