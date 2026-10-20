# -*- coding: utf-8 -*-
"""
Sinh Hình 2.1 và Hình 2.2 chuẩn hóa theo BTL.pdf
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
HINH_DIR = BASE_DIR / "reports" / "hinh"
HINH_ROOT = BASE_DIR / "hinh"

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

# 1. HÌNH 2.1: Ghép 3 bước tiền xử lý
def tao_hinh_2_1():
    print(">>> Tạo Hình 2.1: Quy trình tiền xử lý...")
    im1 = Image.open(HINH_DIR / "q1_nguong_co_tieng.png")
    im2 = Image.open(HINH_DIR / "q2_cat_theo_not.png")
    im3 = Image.open(HINH_DIR / "q3_fade.png")
    
    # Ghép dọc 3 ảnh
    w = max(im1.width, im2.width, im3.width)
    h_total = im1.height + im2.height + im3.height
    
    merged = Image.new("RGB", (w, h_total), (255, 255, 255))
    merged.paste(im1, (0, 0))
    merged.paste(im2, (0, im1.height))
    merged.paste(im3, (0, im1.height + im2.height))
    
    merged.save(HINH_DIR / "2_1_quy_trinh_tien_xu_ly.png", dpi=(300, 300))
    merged.save(HINH_ROOT / "2_1_quy_trinh_tien_xu_ly.png", dpi=(300, 300))
    print("  [OK] Saved 2_1_quy_trinh_tien_xu_ly.png")

# 2. HÌNH 2.2: Số lượng tệp của từng nhạc cụ
def tao_hinh_2_2():
    print(">>> Tạo Hình 2.2: Số lượng tệp của từng nhạc cụ...")
    insts = ['Violin', 'Viola', 'Cello', 'Double Bass', 'Guitar Acoustic', 'Guitar Electric']
    counts = [100, 100, 100, 100, 100, 100]
    colors = ['#2B6CB0', '#319795', '#D69E2E', '#E53E3E', '#805AD5', '#DD6B20']
    
    fig, ax = plt.subplots(figsize=(8, 4.2))
    bars = ax.bar(insts, counts, color=colors, edgecolor='black', linewidth=0.8, width=0.55)
    
    # Đường nét đứt trung bình
    ax.axhline(100, color='#C53030', linestyle='--', linewidth=1.8, label='Giá trị trung bình: 100')
    
    ax.set_ylabel('Số lượng tệp âm thanh (WAV)', fontsize=10.5, fontweight='bold')
    ax.set_ylim(0, 125)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(loc='upper right', fontsize=9.5)
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 2.5, f"{int(h)}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    fig.savefig(HINH_DIR / "2_2_so_luong_mau.png", dpi=300)
    fig.savefig(HINH_ROOT / "2_2_so_luong_mau.png", dpi=300)
    plt.close(fig)
    print("  [OK] Saved 2_2_so_luong_mau.png")

if __name__ == "__main__":
    tao_hinh_2_1()
    tao_hinh_2_2()
