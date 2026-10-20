# -*- coding: utf-8 -*-
"""
Script sinh các đồ thị phân tích thực nghiệm cho Chương 4
chuẩn hóa theo mẫu BTL.pdf:
- Hình 4.1: Fisher ratio và Thông tin tương hỗ (MI)
- Hình 4.2: Phân bố theo nhạc cụ của 4 đặc trưng có Fisher ratio cao nhất
- Hình 4.3: Ma trận tương quan Pearson giữa các đặc trưng
- Hình 4.4: Phân bố khoảng cách intra-class vs inter-class
- Hình 4.5: Ba truy vấn minh họa (Top-5 retrieval)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import stats
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances

# Cấu hình font tiếng Việt và giao diện đồ thị học thuật
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.autolayout'] = False

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "reports" / "tat_ca_dac_trung_600_file.csv"
OUT_DIR = BASE_DIR / "reports" / "hinh"
OUT_DIR_ROOT = BASE_DIR / "hinh"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR_ROOT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV_PATH)
features = [c for c in df.columns if c not in ['file_id', 'file_name', 'instrument']]
X_raw = df[features].values
y = df['instrument'].values
classes = np.unique(y)

scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

INST_VN = {
    'violin': 'Violin',
    'viola': 'Viola',
    'cello': 'Cello',
    'double_bass': 'Double Bass',
    'guitar_acoustic': 'Guitar Acoustic',
    'guitar_electric': 'Guitar Electric'
}

def save_fig(fig, filename):
    p1 = OUT_DIR / filename
    p2 = OUT_DIR_ROOT / filename
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    fig.savefig(p2, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved {filename}")

# ==============================================================================
# HÌNH 4.1: Fisher Ratio & Mutual Information
# ==============================================================================
def ve_hinh_4_1():
    print(">>> Đang vẽ Hình 4.1: Fisher ratio và MI...")
    f_vals = []
    grand_mean = np.mean(X_raw, axis=0)
    for j in range(len(features)):
        groups = [X_raw[y == c, j] for c in classes]
        f_stat, _ = stats.f_oneway(*groups)
        f_vals.append(f_stat)
    
    mi = mutual_info_classif(X_raw, y, random_state=42)
    
    df_eval = pd.DataFrame({
        'feature': features,
        'fisher': f_vals,
        'mi': mi
    }).sort_values('fisher', ascending=False)
    
    # Chọn top 15 đặc trưng tiêu biểu để hiển thị rõ ràng
    top15 = df_eval.head(15).iloc[::-1] # đảo để xếp từ trên xuống
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6), sharey=True)
    
    y_pos = np.arange(len(top15))
    
    # Phân màu theo nhóm đặc trưng
    colors = []
    for f in top15['feature']:
        if 'mfcc' in f:
            colors.append('#3182CE') # Xanh dương - MFCC
        elif 'centroid' in f or 'rolloff' in f:
            colors.append('#DD6B20') # Cam - Phổ
        elif 'rms' in f or 'zcr' in f:
            colors.append('#38A169') # Xanh lá - Thời gian / Năng lượng
        else:
            colors.append('#805AD5') # Tím - Chroma
            
    ax1.barh(y_pos, top15['fisher'], color=colors, height=0.65, edgecolor='black', linewidth=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top15['feature'], fontsize=9.5, fontweight='medium')
    ax1.set_xlabel('Fisher ratio (ANOVA F-statistic)', fontsize=10.5, fontweight='bold')
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    
    ax2.barh(y_pos, top15['mi'], color=colors, height=0.65, edgecolor='black', linewidth=0.6)
    ax2.set_xlabel('Thông tin tương hỗ - MI (nat)', fontsize=10.5, fontweight='bold')
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Chú thích nhóm màu
    legend_elements = [
        patches.Patch(facecolor='#3182CE', edgecolor='black', label='Nhóm MFCC'),
        patches.Patch(facecolor='#DD6B20', edgecolor='black', label='Nhóm Phổ tần'),
        patches.Patch(facecolor='#38A169', edgecolor='black', label='Nhóm Thời gian / Năng lượng'),
        patches.Patch(facecolor='#805AD5', edgecolor='black', label='Nhóm Chroma')
    ]
    fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.03), ncol=4, fontsize=9.5)
    
    plt.tight_layout()
    save_fig(fig, "4_1_fisher_va_mi.png")

# ==============================================================================
# HÌNH 4.2: Phân bố của 4 đặc trưng có Fisher ratio cao nhất
# ==============================================================================
def ve_hinh_4_2():
    print(">>> Đang vẽ Hình 4.2: Phân bố theo nhạc cụ của 4 đặc trưng hàng đầu...")
    top4 = ['mfcc_1_mean', 'mfcc_2_mean', 'centroid_mean', 'rolloff_mean']
    titles = [
        'mfcc_1_mean (Cân bằng năng lượng trầm / bổng)',
        'mfcc_2_mean (Độ cong phổ tần số)',
        'centroid_mean (Trọng tâm phổ - Hz)',
        'rolloff_mean (Tần số cuộn phổ 85% - Hz)'
    ]
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs = axs.ravel()
    
    inst_order = ['double_bass', 'cello', 'viola', 'violin', 'guitar_acoustic', 'guitar_electric']
    labels = [INST_VN[c] for c in inst_order]
    
    palette = ['#2B6CB0', '#319795', '#D69E2E', '#E53E3E', '#805AD5', '#DD6B20']
    
    for i, col in enumerate(top4):
        ax = axs[i]
        data = [df[df['instrument'] == c][col].values for c in inst_order]
        bp = ax.boxplot(data, tick_labels=labels, patch_artist=True,
                        boxprops=dict(linewidth=1.2),
                        medianprops=dict(color='black', linewidth=1.5),
                        flierprops=dict(marker='o', markersize=3.5, alpha=0.5))
        
        for patch, color in zip(bp['boxes'], palette):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            
        ax.set_title(titles[i], fontsize=11, fontweight='bold', pad=8)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.tick_params(axis='x', rotation=20, labelsize=9)
        
    plt.tight_layout()
    save_fig(fig, "4_2_phan_bo_top_dac_trung.png")

# ==============================================================================
# HÌNH 4.3: Ma trận tương quan Pearson
# ==============================================================================
def ve_hinh_4_3():
    print(">>> Đang vẽ Hình 4.3: Ma trận tương quan Pearson...")
    # Chọn đại diện các đặc trưng cốt lõi từ các nhóm để ma trận trực quan, không bị quá nghẹt
    selected = [
        'rms_mean', 'zcr_mean',
        'centroid_mean', 'rolloff_mean',
        'mfcc_0_mean', 'mfcc_1_mean', 'mfcc_2_mean', 'mfcc_3_mean', 'mfcc_4_mean',
        'chroma_0_mean', 'chroma_4_mean', 'chroma_7_mean'
    ]
    
    sub_df = df[selected]
    corr = sub_df.corr().values
    
    fig, ax = plt.subplots(figsize=(9, 8))
    im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    
    ax.set_xticks(np.arange(len(selected)))
    ax.set_yticks(np.arange(len(selected)))
    ax.set_xticklabels(selected, rotation=45, ha='right', fontsize=9.5)
    ax.set_yticklabels(selected, fontsize=9.5)
    
    # Ghi số giá trị tương quan vào ô
    for i in range(len(selected)):
        for j in range(len(selected)):
            val = corr[i, j]
            text_color = "white" if abs(val) > 0.55 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=text_color, fontsize=8)
            
    # Vẽ đường phân tách các nhóm đặc trưng
    # Nhóm 1: rms, zcr (2)
    # Nhóm 2: centroid, rolloff (2)
    # Nhóm 3: mfcc (5)
    # Nhóm 4: chroma (3)
    splits = [1.5, 3.5, 8.5]
    for s in splits:
        ax.axhline(s, color='black', linewidth=1.8)
        ax.axvline(s, color='black', linewidth=1.8)
        
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Hệ số tương quan Pearson (r)', fontsize=10.5, fontweight='bold')
    
    plt.tight_layout()
    save_fig(fig, "4_3_ma_tran_tuong_quan.png")

# ==============================================================================
# HÌNH 4.4: Phân bố khoảng cách cùng loài vs khác loài
# ==============================================================================
def ve_hinh_4_4():
    print(">>> Đang vẽ Hình 4.4: Khoảng cách cùng loài vs khác loài...")
    dist_matrix = pairwise_distances(X, metric='euclidean')
    intra_dists = []
    inter_dists = []
    
    for i in range(len(y)):
        for j in range(i + 1, len(y)):
            d = dist_matrix[i, j]
            if y[i] == y[j]:
                intra_dists.append(d)
            else:
                inter_dists.append(d)
                
    fig, ax = plt.subplots(figsize=(9, 5.5))
    
    bins = np.linspace(0, 22, 60)
    ax.hist(intra_dists, bins=bins, density=True, alpha=0.65, color='#3182CE',
            edgecolor='black', label=f'Cùng nhạc cụ (29.700 cặp, trung vị = {np.median(intra_dists):.2f})')
    ax.hist(inter_dists, bins=bins, density=True, alpha=0.55, color='#E53E3E',
            edgecolor='black', label=f'Khác nhạc cụ (150.000 cặp, trung vị = {np.median(inter_dists):.2f})')
    
    # Vẽ đường trung vị nét đứt
    ax.axvline(np.median(intra_dists), color='#1A365D', linestyle='--', linewidth=2.2)
    ax.axvline(np.median(inter_dists), color='#742A2A', linestyle='--', linewidth=2.2)
    
    ax.set_xlabel('Khoảng cách Euclid trên vectơ 58 đặc trưng chuẩn hóa', fontsize=10.5, fontweight='bold')
    ax.set_ylabel('Mật độ xác suất (Density)', fontsize=10.5, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10, frameon=True)
    ax.grid(True, linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    save_fig(fig, "4_4_khoang_cach_cung_va_khac_loai.png")

# ==============================================================================
# HÌNH 4.5: Ba truy vấn minh họa (Query demo)
# ==============================================================================
def ve_hinh_4_5():
    print(">>> Đang vẽ Hình 4.5: Ba truy vấn minh họa...")
    dist_mat = pairwise_distances(X)
    
    test_queries = [
        ('violin_001.wav', 'Violin'),
        ('cello_010.wav', 'Cello'),
        ('guitar_electric_005.wav', 'Guitar Electric')
    ]
    
    fig, axs = plt.subplots(3, 1, figsize=(11, 7.5))
    
    for row, (q_file, q_label) in enumerate(test_queries):
        ax = axs[row]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2.2)
        ax.axis('off')
        
        idx = df[df['file_name'] == q_file].index[0]
        q_inst = df.loc[idx, 'instrument']
        order = np.argsort(dist_mat[idx])[1:6]
        
        # Vẽ hộp Query bên trái (Xanh dương đậm)
        q_box = patches.FancyBboxPatch((0.2, 0.4), 1.6, 1.4, boxstyle="round,pad=0.1",
                                       facecolor="#EBF8FF", edgecolor="#2B6CB0", linewidth=2)
        ax.add_patch(q_box)
        ax.text(1.0, 1.3, "TRUY VẤN", ha="center", va="center", fontsize=9, fontweight='bold', color="#2B6CB0")
        ax.text(1.0, 0.95, q_file, ha="center", va="center", fontsize=8, fontweight='medium')
        ax.text(1.0, 0.65, f"[{q_label}]", ha="center", va="center", fontsize=8.5, fontweight='bold', color="#1A365D")
        
        # Mũi tên liên kết
        ax.annotate('', xy=(2.15, 1.1), xytext=(1.85, 1.1),
                    arrowprops=dict(facecolor='black', width=1.5, headwidth=6))
        
        # Vẽ 5 kết quả Top 1 - Top 5
        x_start = 2.3
        box_w = 1.38
        gap = 0.16
        
        for k, oi in enumerate(order):
            bx = x_start + k * (box_w + gap)
            r_file = df.loc[oi, 'file_name']
            r_inst = df.loc[oi, 'instrument']
            d = dist_mat[idx, oi]
            is_correct = (r_inst == q_inst)
            
            # Màu xanh lá nếu đúng, màu đỏ nếu sai
            f_col = "#F0FFF4" if is_correct else "#FFF5F5"
            e_col = "#276749" if is_correct else "#C53030"
            t_col = "#22543D" if is_correct else "#742A2A"
            
            box = patches.FancyBboxPatch((bx, 0.4), box_w, 1.4, boxstyle="round,pad=0.1",
                                         facecolor=f_col, edgecolor=e_col, linewidth=1.8)
            ax.add_patch(box)
            ax.text(bx + box_w/2, 1.45, f"Top {k+1}", ha="center", va="center", fontsize=8.5, fontweight='bold', color=e_col)
            ax.text(bx + box_w/2, 1.15, r_file, ha="center", va="center", fontsize=7.2, fontweight='medium')
            ax.text(bx + box_w/2, 0.85, f"[{INST_VN[r_inst]}]", ha="center", va="center", fontsize=8, fontweight='bold', color=t_col)
            ax.text(bx + box_w/2, 0.58, f"d = {d:.2f}", ha="center", va="center", fontsize=7.5, fontstyle='italic', color='#4A5568')
            
    plt.tight_layout()
    save_fig(fig, "4_5_truy_van_minh_hoa.png")

if __name__ == "__main__":
    ve_hinh_4_1()
    ve_hinh_4_2()
    ve_hinh_4_3()
    ve_hinh_4_4()
    ve_hinh_4_5()
    print(">>> Hoàn thành vẽ toàn bộ 5 hình cho Chương 4!")
