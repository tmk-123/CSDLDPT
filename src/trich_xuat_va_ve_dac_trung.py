"""Script trích xuất đặc trưng âm học chi tiết trên 600 file trong data/wav
và sinh các ảnh minh họa so sánh đặc trưng phục vụ Báo cáo BTL (theo chuẩn mẫu HCSDLDPT.docx).

Đầu vào : data/metadata.csv, data/wav/
Đầu ra  :
    - reports/hinh/5_so_sanh_dac_trung_6_nhac_cu.png
    - reports/hinh/6_so_sanh_cac_cap_doi_chung.png
    - reports/hinh/7_quy_trinh_trich_xuat_dac_trung.png
    - reports/so_sanh_dac_trung_chi_tiet.csv
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import librosa
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GOC = Path(__file__).resolve().parent.parent
HINH = GOC / "reports" / "hinh"
HINH.mkdir(parents=True, exist_ok=True)

SR = 22050
N = 2048       # Frame length (~92.88 ms)
HOP = 512      # Hop size (~23.22 ms)

THU_TU = ["violin", "viola", "cello", "double_bass", "guitar_acoustic", "guitar_electric"]
TEN_VN = {
    "violin": "Violin",
    "viola": "Viola",
    "cello": "Cello",
    "double_bass": "Double Bass",
    "guitar_acoustic": "Guitar Acoustic",
    "guitar_electric": "Guitar Electric"
}
MAU = {
    "violin": "#1f77b4",
    "viola": "#2ca02c",
    "cello": "#9467bd",
    "double_bass": "#8c564b",
    "guitar_acoustic": "#ff7f0e",
    "guitar_electric": "#d62728"
}

def trich_xuat_toan_bo_du_lieu(meta):
    cache_path = GOC / "reports" / "tat_ca_dac_trung_600_file.csv"
    if cache_path.exists():
        print(f">>> Đã tìm thấy dữ liệu trích xuất sẵn tại {cache_path}, đang nạp...")
        return pd.read_csv(cache_path)

    print(">>> Đang trích xuất đặc trưng trên toàn bộ 600 file...")
    ket_qua = []
    
    for idx, row in meta.iterrows():
        p = GOC / row["file_path"]
        y, _ = librosa.load(p, sr=SR, mono=True)
        
        # 1. RMS
        rms = librosa.feature.rms(y=y, frame_length=N, hop_length=HOP)[0]
        # 2. ZCR
        zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=N, hop_length=HOP)[0]
        # 3. Spectral Centroid
        centroid = librosa.feature.spectral_centroid(y=y, sr=SR, n_fft=N, hop_length=HOP)[0]
        # 4. Spectral Roll-off 85%
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=SR, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
        # 5. MFCC 13
        mfcc = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=13, n_fft=N, hop_length=HOP)
        # 6. Chroma 12
        chroma = librosa.feature.chroma_stft(y=y, sr=SR, n_fft=N, hop_length=HOP)
        
        rec = {
            "file_id": row["file_id"],
            "file_name": row["file_name"],
            "instrument": row["instrument"],
            "rms_mean": np.mean(rms),
            "rms_std": np.std(rms),
            "zcr_mean": np.mean(zcr),
            "zcr_std": np.std(zcr),
            "centroid_mean": np.mean(centroid),
            "centroid_std": np.std(centroid),
            "rolloff_mean": np.mean(rolloff),
            "rolloff_std": np.std(rolloff),
        }
        for i in range(13):
            rec[f"mfcc_{i}_mean"] = np.mean(mfcc[i])
            rec[f"mfcc_{i}_std"] = np.std(mfcc[i])
        for c in range(12):
            rec[f"chroma_{c}_mean"] = np.mean(chroma[c])
            rec[f"chroma_{c}_std"] = np.std(chroma[c])
            
        ket_qua.append(rec)
        if (idx + 1) % 100 == 0:
            print(f"  Đã xử lý {idx + 1}/600 file...")
            
    df_feat = pd.DataFrame(ket_qua)
    df_feat.to_csv(cache_path, index=False, encoding="utf-8-sig")
    print(f"  Đã lưu cache đặc trưng tại: {cache_path}")
    return df_feat


def ve_hinh_5_so_sanh_6_nhac_cu(df_feat):
    print(">>> Đang vẽ Hình 5: So sánh tổng thể các đặc trưng trên 6 nhạc cụ...")
    fig, axs = plt.subplots(2, 2, figsize=(15, 11), constrained_layout=True)
    
    # Tính trung bình theo nhạc cụ
    grp = df_feat.groupby("instrument").mean(numeric_only=True)
    grp = grp.loc[THU_TU]
    
    x = np.arange(len(THU_TU))
    w = 0.35
    labels = [TEN_VN[nc] for nc in THU_TU]
    
    # Panel 1: Centroid & Roll-off
    axs[0, 0].bar(x - w/2, grp["centroid_mean"], width=w, label="Trọng tâm phổ Centroid (Độ sáng)", color="#0d6b70")
    axs[0, 0].bar(x + w/2, grp["rolloff_mean"], width=w, label="Tần số cuộn Roll-off 85% (Trần năng lượng)", color="#d97706")
    axs[0, 0].set_xticks(x)
    axs[0, 0].set_xticklabels(labels, rotation=15, fontweight="bold", fontsize=9)
    axs[0, 0].set_ylabel("Tần số (Hz)", fontsize=10)
    axs[0, 0].set_title("A. Trọng tâm phổ (Spectral Centroid) & Tần số cuộn (Roll-off 85%)", fontweight="bold", fontsize=11)
    axs[0, 0].grid(True, linestyle="--", alpha=0.4)
    axs[0, 0].legend(fontsize=9)
    
    # Panel 2: RMS Std & ZCR Mean
    axs[0, 1].bar(x - w/2, grp["rms_std"], width=w, label="Biến thiên biên độ RMS (Std) - Tắt nhanh vs Bền vững", color="#2563eb")
    axs[0, 1].bar(x + w/2, grp["zcr_mean"], width=w, label="Tốc độ qua điểm không (ZCR) - Độ nhám méo sóng", color="#dc2626")
    axs[0, 1].set_xticks(x)
    axs[0, 1].set_xticklabels(labels, rotation=15, fontweight="bold", fontsize=9)
    axs[0, 1].set_ylabel("Giá trị trung bình", fontsize=10)
    axs[0, 1].set_title("B. Động thái năng lượng RMS (Std) & Độ nhám / Méo sóng (ZCR)", fontweight="bold", fontsize=11)
    axs[0, 1].grid(True, linestyle="--", alpha=0.4)
    axs[0, 1].legend(fontsize=9)
    
    # Panel 3: 13 hệ số MFCC
    mfcc_cols = [f"mfcc_{i}_mean" for i in range(13)]
    for nc in THU_TU:
        vals = grp.loc[nc, mfcc_cols].values
        axs[1, 0].plot(range(13), vals, marker="o", label=TEN_VN[nc], color=MAU[nc], lw=2)
    axs[1, 0].set_xticks(range(13))
    axs[1, 0].set_xticklabels([f"c{i}" for i in range(13)], fontsize=9)
    axs[1, 0].set_xlabel("Chỉ số hệ số MFCC (từ c0 đến c12)", fontsize=10)
    axs[1, 0].set_ylabel("Biên độ hệ số Cepstral", fontsize=10)
    axs[1, 0].set_title("C. 13 hệ số MFCC bóc tách đường bao phổ formant của thùng đàn", fontweight="bold", fontsize=11)
    axs[1, 0].grid(True, linestyle="--", alpha=0.4)
    axs[1, 0].legend(fontsize=8.5, ncol=2)
    
    # Panel 4: 12 nửa cung Chroma
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    chroma_cols = [f"chroma_{c}_mean" for c in range(12)]
    for nc in THU_TU:
        vals = grp.loc[nc, chroma_cols].values
        axs[1, 1].plot(notes, vals, marker="s", label=TEN_VN[nc], color=MAU[nc], lw=1.8)
    axs[1, 1].set_xticks(range(12))
    axs[1, 1].set_xticklabels(notes, fontweight="bold", fontsize=9)
    axs[1, 1].set_xlabel("Nửa cung chuẩn nhạc lý", fontsize=10)
    axs[1, 1].set_ylabel("Mức năng lượng đóng góp (L1 norm)", fontsize=10)
    axs[1, 1].set_title("D. Phân bố 12 lớp cao độ Chroma STFT trung bình", fontweight="bold", fontsize=11)
    axs[1, 1].grid(True, linestyle="--", alpha=0.4)
    axs[1, 1].legend(fontsize=8.5, ncol=2)
    
    out_path = HINH / "5_so_sanh_dac_trung_6_nhac_cu.png"
    plt.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f"  Đã lưu Hình 5 tại: {out_path}")


def ve_hinh_6_cac_cap_doi_chung():
    print(">>> Đang vẽ Hình 6: So sánh các cặp đối chứng cụ thể...")
    fig, axs = plt.subplots(3, 2, figsize=(15, 11), constrained_layout=True)
    
    # Cặp 1: Violin (violin_001.wav) vs Acoustic Guitar (guitar_acoustic_001.wav)
    # Thuộc tính: Động học năng lượng thời gian RMS (Kéo vĩ legato vs Gảy dây decay)
    y_vn, _ = librosa.load(GOC / "data" / "wav" / "violin" / "violin_001.wav", sr=SR)
    y_gt, _ = librosa.load(GOC / "data" / "wav" / "guitar_acoustic" / "guitar_acoustic_001.wav", sr=SR)
    
    rms_vn = librosa.feature.rms(y=y_vn, frame_length=N, hop_length=HOP)[0]
    rms_gt = librosa.feature.rms(y=y_gt, frame_length=N, hop_length=HOP)[0]
    t_vn = np.arange(len(rms_vn)) * HOP / SR
    t_gt = np.arange(len(rms_gt)) * HOP / SR
    
    axs[0, 0].plot(t_vn, rms_vn, color=MAU["violin"], lw=1.8, label=f"Violin (violin_001.wav, std={np.std(rms_vn):.3f})")
    axs[0, 0].plot(t_gt, rms_gt, color=MAU["guitar_acoustic"], lw=1.8, label=f"Guitar acoustic (guitar_acoustic_001.wav, std={np.std(rms_gt):.3f})")
    axs[0, 0].set_title("Cặp 1: Động thái đường bao RMS - Kéo vĩ giữ đều vs Gảy dây tắt dốc", fontweight="bold", fontsize=10.5)
    axs[0, 0].set_xlabel("Thời gian (giây)")
    axs[0, 0].set_ylabel("Biên độ RMS")
    axs[0, 0].grid(True, linestyle="--", alpha=0.4)
    axs[0, 0].legend(fontsize=9)
    
    # Cặp 2: Dạng sóng cận cảnh N=2048 mẫu Cello mộc (cello_001.wav) vs Guitar điện distortion (guitar_electric_001.wav)
    # Thuộc tính: Độ nhám / Méo cắt đỉnh ZCR
    y_vc, _ = librosa.load(GOC / "data" / "wav" / "cello" / "cello_001.wav", sr=SR)
    y_eg, _ = librosa.load(GOC / "data" / "wav" / "guitar_electric" / "guitar_electric_001.wav", sr=SR)
    
    s_vc = y_vc[int(1.0 * SR) : int(1.0 * SR) + 1024]
    s_eg = y_eg[int(1.0 * SR) : int(1.0 * SR) + 1024]
    zcr_vc = librosa.feature.zero_crossing_rate(y_vc, frame_length=N, hop_length=HOP)[0]
    zcr_eg = librosa.feature.zero_crossing_rate(y_eg, frame_length=N, hop_length=HOP)[0]
    
    axs[0, 1].plot(s_vc, color=MAU["cello"], lw=1.5, label=f"Cello mộc (sóng điều hòa trơn, ZCR mean={np.mean(zcr_vc):.3f})")
    axs[0, 1].plot(s_eg, color=MAU["guitar_electric"], lw=1.2, alpha=0.85, label=f"Guitar điện méo tiếng (sóng răng cưa bão hòa, ZCR mean={np.mean(zcr_eg):.3f})")
    axs[0, 1].set_title("Cặp 2: Cận cảnh dạng sóng - Sóng điều hòa mộc vs Méo cắt đỉnh (Clipping)", fontweight="bold", fontsize=10.5)
    axs[0, 1].set_xlabel("Số thứ tự mẫu n (1024 mẫu)")
    axs[0, 1].set_ylabel("Biên độ sóng")
    axs[0, 1].grid(True, linestyle="--", alpha=0.4)
    axs[0, 1].legend(fontsize=9)
    
    # Cặp 3: Trọng tâm phổ Centroid Violin (violin_001.wav) vs Double Bass (double_bass_001.wav)
    # Thuộc tính: Phân tầng độ sáng phổ và kích thước thùng đàn họ vĩ
    y_db, _ = librosa.load(GOC / "data" / "wav" / "double_bass" / "double_bass_001.wav", sr=SR)
    cent_vn = librosa.feature.spectral_centroid(y=y_vn, sr=SR, n_fft=N, hop_length=HOP)[0]
    cent_db = librosa.feature.spectral_centroid(y=y_db, sr=SR, n_fft=N, hop_length=HOP)[0]
    
    axs[1, 0].plot(t_vn, cent_vn, color=MAU["violin"], lw=1.8, label=f"Violin (thùng nhỏ, Centroid mean={np.mean(cent_vn):.0f} Hz)")
    axs[1, 0].plot(np.arange(len(cent_db))*HOP/SR, cent_db, color=MAU["double_bass"], lw=1.8, label=f"Double Bass (thùng khổng lồ, Centroid mean={np.mean(cent_db):.0f} Hz)")
    axs[1, 0].set_title("Cặp 3: Trọng tâm phổ Spectral Centroid - Nhạc cụ dải cao vs Nhạc cụ siêu trầm", fontweight="bold", fontsize=10.5)
    axs[1, 0].set_xlabel("Thời gian (giây)")
    axs[1, 0].set_ylabel("Tần số Centroid (Hz)")
    axs[1, 0].grid(True, linestyle="--", alpha=0.4)
    axs[1, 0].legend(fontsize=9)
    
    # Cặp 4: Roll-off 85% Violin (violin_001) vs Viola (viola_001) vs Cello (cello_001)
    y_va, _ = librosa.load(GOC / "data" / "wav" / "viola" / "viola_001.wav", sr=SR)
    ro_vn = librosa.feature.spectral_rolloff(y=y_vn, sr=SR, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
    ro_va = librosa.feature.spectral_rolloff(y=y_va, sr=SR, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
    ro_vc = librosa.feature.spectral_rolloff(y=y_vc, sr=SR, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
    
    axs[1, 1].plot(t_vn, ro_vn, color=MAU["violin"], lw=1.6, label=f"Violin (Roll-off mean={np.mean(ro_vn):.0f} Hz)")
    axs[1, 1].plot(np.arange(len(ro_va))*HOP/SR, ro_va, color=MAU["viola"], lw=1.6, label=f"Viola (Roll-off mean={np.mean(ro_va):.0f} Hz)")
    axs[1, 1].plot(np.arange(len(ro_vc))*HOP/SR, ro_vc, color=MAU["cello"], lw=1.6, label=f"Cello (Roll-off mean={np.mean(ro_vc):.0f} Hz)")
    axs[1, 1].set_title("Cặp 4: Giới hạn tần số cuộn phổ Roll-off 85% phân cấp 3 đàn họ vĩ", fontweight="bold", fontsize=10.5)
    axs[1, 1].set_xlabel("Thời gian (giây)")
    axs[1, 1].set_ylabel("Tần số Roll-off (Hz)")
    axs[1, 1].grid(True, linestyle="--", alpha=0.4)
    axs[1, 1].legend(fontsize=9)
    
    # Cặp 5: Phổ MFCC trung bình Violin vs Guitar Acoustic vs Guitar Electric
    mfcc_vn = np.mean(librosa.feature.mfcc(y=y_vn, sr=SR, n_mfcc=13, n_fft=N, hop_length=HOP), axis=1)
    mfcc_gt = np.mean(librosa.feature.mfcc(y=y_gt, sr=SR, n_mfcc=13, n_fft=N, hop_length=HOP), axis=1)
    mfcc_eg = np.mean(librosa.feature.mfcc(y=y_eg, sr=SR, n_mfcc=13, n_fft=N, hop_length=HOP), axis=1)
    
    axs[2, 0].plot(range(13), mfcc_vn, marker="o", color=MAU["violin"], lw=2, label="Violin (thùng gỗ vĩ)")
    axs[2, 0].plot(range(13), mfcc_gt, marker="s", color=MAU["guitar_acoustic"], lw=2, label="Guitar acoustic (thùng phẳng mộc)")
    axs[2, 0].plot(range(13), mfcc_eg, marker="^", color=MAU["guitar_electric"], lw=2, label="Guitar điện (thân đặc amply)")
    axs[2, 0].set_title("Cặp 5: 13 hệ số MFCC phân biệt 3 kết cấu thùng đàn / bộ khuếch đại", fontweight="bold", fontsize=10.5)
    axs[2, 0].set_xticks(range(13))
    axs[2, 0].set_xticklabels([f"c{i}" for i in range(13)], fontsize=8.5)
    axs[2, 0].set_xlabel("Hệ số MFCC")
    axs[2, 0].set_ylabel("Biên độ Cepstral")
    axs[2, 0].grid(True, linestyle="--", alpha=0.4)
    axs[2, 0].legend(fontsize=9)
    
    # Cặp 6: Chroma STFT - Đơn âm (Violin) vs Đa âm hợp âm (Guitar acoustic)
    chr_vn = np.mean(librosa.feature.chroma_stft(y=y_vn, sr=SR, n_fft=N, hop_length=HOP), axis=1)
    chr_gt = np.mean(librosa.feature.chroma_stft(y=y_gt, sr=SR, n_fft=N, hop_length=HOP), axis=1)
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    x_c = np.arange(12)
    axs[2, 1].bar(x_c - 0.2, chr_vn, width=0.4, color=MAU["violin"], label="Violin (Đơn âm: đỉnh nốt nhọn tập trung)")
    axs[2, 1].bar(x_c + 0.2, chr_gt, width=0.4, color=MAU["guitar_acoustic"], label="Guitar (Đa âm hợp âm: trải rộng nhiều bin)")
    axs[2, 1].set_title("Cặp 6: Phân bố 12 nửa cung Chroma - Đơn âm giai điệu vs Đa âm hợp âm", fontweight="bold", fontsize=10.5)
    axs[2, 1].set_xticks(x_c)
    axs[2, 1].set_xticklabels(notes, fontweight="bold", fontsize=9)
    axs[2, 1].set_xlabel("Nửa cung chuẩn")
    axs[2, 1].set_ylabel("Năng lượng L1 norm")
    axs[2, 1].grid(True, linestyle="--", alpha=0.4)
    axs[2, 1].legend(fontsize=9)
    
    out_path = HINH / "6_so_sanh_cac_cap_doi_chung.png"
    plt.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f"  Đã lưu Hình 6 tại: {out_path}")


def ve_hinh_7_quy_trinh_trich_xuat():
    print(">>> Đang vẽ Hình 7: Quy trình toán học trích xuất đặc trưng...")
    # Lấy một đoạn âm thanh mẫu từ violin_001.wav
    y, sr = librosa.load(GOC / "data" / "wav" / "violin" / "violin_001.wav", sr=SR)
    
    fig, axs = plt.subplots(4, 1, figsize=(14, 11), constrained_layout=True)
    
    # 1. Tín hiệu gốc và chia khung
    t = np.arange(len(y)) / sr
    axs[0].plot(t, y, color="#475569", lw=0.5, alpha=0.7, label="Dạng sóng tín hiệu số x[n] (22050 Hz)")
    # Minh họa 1 khung N=2048 tại giây thứ 1.0
    frame_idx = int(1.0 * sr / HOP)
    t_start = frame_idx * HOP / sr
    t_end = (frame_idx * HOP + N) / sr
    axs[0].axvspan(t_start, t_end, color="#2563eb", alpha=0.4, label=f"Khung thứ m (N={N} mẫu, H={HOP} mẫu, Overlap=75%)")
    axs[0].set_title("Bước 1: Tín hiệu thời gian liên tục và kỹ thuật chia khung trượt (Framing & Windowing)", fontweight="bold", fontsize=11)
    axs[0].set_xlabel("Thời gian (giây)")
    axs[0].set_ylabel("Biên độ [-1, 1]")
    axs[0].grid(True, linestyle="--", alpha=0.3)
    axs[0].legend(loc="upper right")
    
    # 2. STFT Spectrogram & Ngân hàng bộ lọc Mel
    S = np.abs(librosa.stft(y, n_fft=N, hop_length=HOP))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_db, sr=sr, hop_length=HOP, x_axis="time", y_axis="linear", ax=axs[1], cmap="viridis")
    axs[1].set_ylim(0, 8000)
    axs[1].set_title("Bước 2: Biến đổi Fourier thời gian ngắn STFT -> Phổ công suất P(m, k) = |X(m, k)|^2", fontweight="bold", fontsize=11)
    axs[1].set_ylabel("Tần số (Hz)")
    fig.colorbar(img, ax=axs[1], format="%+2.0f dB", label="Mức công suất (dB)")
    
    # 3. Trích xuất đồng thời 4 đặc trưng khung
    cent = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N, hop_length=HOP)[0]
    ro = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=N, hop_length=HOP, roll_percent=0.85)[0]
    rms = librosa.feature.rms(y=y, frame_length=N, hop_length=HOP)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=N, hop_length=HOP)[0]
    t_frames = np.arange(len(rms)) * HOP / sr
    
    ax3_twin = axs[2].twinx()
    l1 = axs[2].plot(t_frames, cent, color="#0d6b70", lw=1.8, label="Spectral Centroid (Hz) - Trục trái")
    l2 = axs[2].plot(t_frames, ro, color="#d97706", lw=1.8, label="Spectral Roll-off 85% (Hz) - Trục trái")
    l3 = ax3_twin.plot(t_frames, rms * 10, color="#2563eb", lw=1.6, linestyle="--", label="RMS Energy x10 - Trục phải")
    l4 = ax3_twin.plot(t_frames, zcr * 10, color="#dc2626", lw=1.6, linestyle=":", label="ZCR x10 - Trục phải")
    axs[2].set_title("Bước 3: Trích xuất các đại lượng đặc trưng cho từng khung thời gian m", fontweight="bold", fontsize=11)
    axs[2].set_xlabel("Thời gian (giây)")
    axs[2].set_ylabel("Tần số phổ (Hz)")
    ax3_twin.set_ylabel("Biên độ đặc trưng thời gian")
    axs[2].grid(True, linestyle="--", alpha=0.3)
    lines = l1 + l2 + l3 + l4
    axs[2].legend(lines, [l.get_label() for l in lines], loc="upper right", fontsize=8.5)
    
    # 4. Temporal Pooling ra Vector cố định 58 chiều
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=N, hop_length=HOP)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=N, hop_length=HOP)
    
    # Ghép vector 58 chiều
    vec_mu = np.hstack([
        np.mean(mfcc, axis=1), [np.mean(ro)],          # Bộ A: 14 mean
        [np.mean(rms)], [np.mean(zcr)],                 # Bộ B: 2 mean
        [np.mean(cent)], np.mean(chroma, axis=1)        # Bộ C: 13 mean
    ])
    vec_std = np.hstack([
        np.std(mfcc, axis=1), [np.std(ro)],
        [np.std(rms)], [np.std(zcr)],
        [np.std(cent)], np.std(chroma, axis=1)
    ])
    vec_58 = np.concatenate([vec_mu, vec_std])
    
    # Vẽ heatmap biểu diễn vector 58 chiều
    axs[3].imshow([vec_58], aspect="auto", cmap="coolwarm", interpolation="none")
    axs[3].set_yticks([])
    axs[3].set_xticks([0, 14, 28, 42, 57])
    axs[3].set_xticklabels(["0 (MFCC/Ro mean)", "14 (B/C mean)", "29 (MFCC/Ro std)", "43 (B/C std)", "57 (Chroma std)"], fontsize=9)
    axs[3].set_title(f"Bước 4: Temporal Pooling tổng hợp (Mean $\\mu$, Std $\\sigma$) tạo Vector đặc trưng 58 chiều cố định (v ∈ R^58)", fontweight="bold", fontsize=11)
    axs[3].set_xlabel("Chỉ số phần tử trong vector đặc trưng (từ chiều 1 đến chiều 58)")
    
    out_path = HINH / "7_quy_trinh_trich_xuat_dac_trung.png"
    plt.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f"  Đã lưu Hình 7 tại: {out_path}")


def ve_hinh_8_chi_tiet_trich_xuat_3_bo():
    print(">>> Đang vẽ Hình 8: Minh họa chi tiết cơ chế trích xuất của từng bộ đặc trưng (Bộ A, B, C)...")
    fig = plt.figure(figsize=(15, 12), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.1, 1, 1.1])
    
    # Lấy 1 file violin mẫu
    sample_path = GOC / "data" / "wav" / "violin" / "violin_001.wav"
    y, sr = librosa.load(sample_path, sr=SR, mono=True)
    
    # Chọn 1 khung có tiếng ở giữa bản ghi
    frame_idx = 40
    frame_start = frame_idx * HOP
    frame_samples = y[frame_start : frame_start + N]
    
    # ---------------- BỘ A: Âm sắc & Bao phổ (MFCC & Spectral Roll-off) ----------------
    ax_a1 = fig.add_subplot(gs[0, 0])
    ax_a2 = fig.add_subplot(gs[0, 1])
    
    # Tính phổ STFT khung
    S_frame = np.abs(librosa.stft(frame_samples, n_fft=N, hop_length=N+1, window="hann"))[:, 0]
    freqs = librosa.fft_frequencies(sr=SR, n_fft=N)
    power_frame = S_frame ** 2
    
    # Ngưỡng Roll-off 85%
    cum_power = np.cumsum(power_frame)
    idx_ro = np.where(cum_power >= 0.85 * cum_power[-1])[0][0]
    f_ro = freqs[idx_ro]
    
    ax_a1.plot(freqs, 10 * np.log10(power_frame + 1e-9), color="#4b5563", alpha=0.7, label="Phổ công suất STFT (dB)")
    ax_a1.axvline(f_ro, color="#d97706", lw=2, linestyle="--", label=f"Roll-off 85% = {f_ro:.0f} Hz (Ngưỡng 85% công suất)")
    ax_a1.fill_between(freqs[:idx_ro], -80, 10 * np.log10(power_frame[:idx_ro] + 1e-9), color="#d97706", alpha=0.15, label="85% tổng năng lượng tích lũy")
    ax_a1.set_xlim(0, 8000)
    ax_a1.set_ylim(-70, 10)
    ax_a1.set_title("Bộ A1: Spectral Roll-off 85% trên Phổ công suất STFT", fontweight="bold", fontsize=11)
    ax_a1.set_xlabel("Tần số (Hz)")
    ax_a1.set_ylabel("Mức công suất (dB)")
    ax_a1.grid(True, linestyle="--", alpha=0.3)
    ax_a1.legend(loc="upper right", fontsize=8.5)
    
    # MFCC của khung
    mfcc_frame = librosa.feature.mfcc(y=frame_samples, sr=SR, n_mfcc=13, n_fft=N, hop_length=N+1)[:, 0]
    bars = ax_a2.bar(range(13), mfcc_frame, color="#0d6b70", width=0.6, edgecolor="#064e3b")
    ax_a2.axhline(0, color="black", lw=0.8)
    ax_a2.set_xticks(range(13))
    ax_a2.set_xticklabels([f"c{i}" for i in range(13)], fontsize=9)
    ax_a2.set_title("Bộ A2: 13 hệ số Cepstral thang Mel (MFCC - Bóc tách formant)", fontweight="bold", fontsize=11)
    ax_a2.set_xlabel("Chỉ số hệ số Cepstral (c0: năng lượng trung bình, c1..c12: hình dáng formant)")
    ax_a2.set_ylabel("Biên độ hệ số")
    ax_a2.grid(True, linestyle="--", alpha=0.3)
    
    # ---------------- BỘ B: Năng lượng & Động học thời gian (RMS & ZCR) ----------------
    ax_b1 = fig.add_subplot(gs[1, 0])
    ax_b2 = fig.add_subplot(gs[1, 1])
    
    # Sóng và ZCR trên khung
    zc = np.where(np.diff(np.signbit(frame_samples)))[0]
    sample_axis = np.arange(len(frame_samples))
    ax_b1.plot(sample_axis, frame_samples, color="#2563eb", lw=1.2, label="Dạng sóng khung x[n] (2048 mẫu)")
    ax_b1.scatter(zc, frame_samples[zc], color="#dc2626", s=18, zorder=3, label=f"Điểm đổi dấu ({len(zc)} lần cắt -> ZCR={len(zc)/(N-1):.4f})")
    rms_val = np.sqrt(np.mean(frame_samples ** 2))
    ax_b1.axhline(rms_val, color="#059669", lw=1.5, linestyle="--", label=f"+RMS = {rms_val:.3f}")
    ax_b1.axhline(-rms_val, color="#059669", lw=1.5, linestyle="--", label=f"-RMS = -{rms_val:.3f}")
    ax_b1.set_xlim(0, 1000) # zoom 1000 mẫu đầu để thấy rõ
    ax_b1.set_title("Bộ B1: Khung 2048 mẫu - Tính RMS & Các điểm đổi dấu qua 0 (ZCR)", fontweight="bold", fontsize=11)
    ax_b1.set_xlabel("Chỉ số mẫu n trong khung (phóng to 1000 mẫu đầu)")
    ax_b1.set_ylabel("Biên độ sóng")
    ax_b1.grid(True, linestyle="--", alpha=0.3)
    ax_b1.legend(loc="upper right", fontsize=8)
    
    # Đường bao RMS toàn bài: So sánh Violin vs Guitar acoustic
    sample_guitar = GOC / "data" / "wav" / "guitar_acoustic" / "guitar_acoustic_001.wav"
    y_g, _ = librosa.load(sample_guitar, sr=SR, mono=True)
    rms_v = librosa.feature.rms(y=y, frame_length=N, hop_length=HOP)[0]
    rms_g = librosa.feature.rms(y=y_g, frame_length=N, hop_length=HOP)[0]
    t_v = np.arange(len(rms_v)) * HOP / SR
    t_g = np.arange(len(rms_g)) * HOP / SR
    ax_b2.plot(t_v, rms_v, color="#1f77b4", lw=1.8, label="Violin (Kéo vĩ: Duy trì Sustain phẳng)")
    ax_b2.plot(t_g, rms_g, color="#ff7f0e", lw=1.8, label="Guitar Acoustic (Gảy buông: Tắt dốc Decay nhanh)")
    ax_b2.set_title("Bộ B2: Đường bao động thái năng lượng RMS theo thời gian", fontweight="bold", fontsize=11)
    ax_b2.set_xlabel("Thời gian (giây)")
    ax_b2.set_ylabel("Năng lượng hiệu dụng RMS")
    ax_b2.grid(True, linestyle="--", alpha=0.3)
    ax_b2.legend(loc="upper right", fontsize=8.5)
    
    # ---------------- BỘ C: Trọng tâm phổ & Hòa âm cao độ (Centroid & Chroma) ----------------
    ax_c1 = fig.add_subplot(gs[2, 0])
    ax_c2 = fig.add_subplot(gs[2, 1])
    
    # Trọng tâm phổ Centroid
    cent_val = np.sum(freqs * power_frame) / (np.sum(power_frame) + 1e-9)
    ax_c1.plot(freqs, power_frame / np.max(power_frame), color="#0d6b70", lw=1.5, label="Phổ công suất chuẩn hóa")
    ax_c1.axvline(cent_val, color="#dc2626", lw=2.2, linestyle="-", label=f"Trọng tâm phổ Centroid = {cent_val:.1f} Hz (Tâm khối phổ)")
    ax_c1.set_xlim(0, 5000)
    ax_c1.set_title("Bộ C1: Trọng tâm phổ Spectral Centroid (Cảm nhận độ sáng phổ)", fontweight="bold", fontsize=11)
    ax_c1.set_xlabel("Tần số (Hz)")
    ax_c1.set_ylabel("Công suất tương đối")
    ax_c1.grid(True, linestyle="--", alpha=0.3)
    ax_c1.legend(loc="upper right", fontsize=8.5)
    
    # 12 nửa cung Chroma STFT
    chroma_frame = librosa.feature.chroma_stft(y=frame_samples, sr=SR, n_fft=N, hop_length=N+1)[:, 0]
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    ax_c2.bar(note_names, chroma_frame, color="#7c3aed", width=0.6, edgecolor="#5b21b6")
    ax_c2.set_title("Bộ C2: Phân bố năng lượng 12 nửa cung chuẩn nhạc lý (Chroma STFT)", fontweight="bold", fontsize=11)
    ax_c2.set_xlabel("12 nửa cung độc lập quãng tám")
    ax_c2.set_ylabel("Trọng số năng lượng chuẩn hóa L1")
    ax_c2.grid(True, linestyle="--", alpha=0.3)
    
    out_path = HINH / "8_chi_tiet_trich_xuat_3_bo_dac_trung.png"
    plt.savefig(out_path, dpi=160)
    plt.close(fig)
    print(f"  Đã lưu Hình 8 tại: {out_path}")


def xuat_bang_so_sanh_chi_tiet(df_feat):
    print(">>> Đang xuất bảng thống kê đặc trưng chi tiết reports/so_sanh_dac_trung_chi_tiet.csv...")
    bang = df_feat.groupby("instrument").agg({
        "centroid_mean": ["mean", "std"],
        "rolloff_mean": ["mean", "std"],
        "rms_mean": ["mean", "std"],
        "rms_std": ["mean"],
        "zcr_mean": ["mean", "std"],
        "mfcc_0_mean": ["mean"],
        "mfcc_1_mean": ["mean"],
        "mfcc_2_mean": ["mean"],
        "mfcc_3_mean": ["mean"],
    })
    bang = bang.loc[THU_TU].round(2)
    out_csv = GOC / "reports" / "so_sanh_dac_trung_chi_tiet.csv"
    bang.to_csv(out_csv, encoding="utf-8-sig")
    print(f"  Đã lưu bảng tại: {out_csv}")
    print(bang)


def main():
    meta = pd.read_csv(GOC / "data" / "metadata.csv")
    df_feat = trich_xuat_toan_bo_du_lieu(meta)
    ve_hinh_5_so_sanh_6_nhac_cu(df_feat)
    ve_hinh_6_cac_cap_doi_chung()
    ve_hinh_7_quy_trinh_trich_xuat()
    ve_hinh_8_chi_tiet_trich_xuat_3_bo()
    xuat_bang_so_sanh_chi_tiet(df_feat)
    print("\n[HOÀN TẤT] Toàn bộ dữ liệu và ảnh đặc trưng đã được sinh thành công!")


if __name__ == "__main__":
    main()
