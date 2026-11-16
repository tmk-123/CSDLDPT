"""Vẽ hai sơ đồ cho chương 4 của báo cáo (bộ đặc trưng). Chỉ là sơ đồ thiết kế, không dùng dữ liệu.

Cách chạy:
    .venv\\Scripts\\python.exe src\\phan1_du_lieu\\ve_hinh_chuong_4.py

Đầu ra (ket_qua/hinh):
    4_1_cau_truc_46_chieu.png           vector 46 chiều -> 3 bộ -> 5 loại đặc trưng
    4_2_quy_trinh_trich_dac_trung.png   6 bước từ tệp âm thanh đến vector 46 chiều
"""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

matplotlib.use("Agg")
plt.rcParams["font.family"] = "Arial"
HINH = Path(__file__).resolve().parents[2] / "ket_qua" / "hinh"
NAVY, XAM = "#24405f", "#56657a"
MAU = {"A": ("#3f6fa3", "#eaf1f9"), "B": ("#2f7f6b", "#e7f4f0"), "C": ("#7a55a8", "#f1ecf8")}


def hop(ax, x, y, w, h, tieu_de, phu, vien, nen, co=13, mau_chu=NAVY):
    """Hộp bo góc: tiêu đề in đậm ở trên, dòng phụ ở dưới."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                lw=2.2, ec=vien, fc=nen))
    hai_dong = "\n" in tieu_de
    ax.text(x + w / 2, y + h * (0.64 if hai_dong else 0.62), tieu_de, ha="center", va="center",
            fontsize=co, weight="bold", color=mau_chu, linespacing=1.3)
    ax.text(x + w / 2, y + h * (0.2 if hai_dong else 0.27), phu, ha="center", va="center",
            fontsize=co - 2.5, color=mau_chu)


def mui_ten(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=XAM, mutation_scale=16))


def cau_truc():
    fig, ax = plt.subplots(figsize=(12, 6.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    hop(ax, 3.9, 5.5, 4.2, 1.1, "Vector đặc trưng âm thanh", "46 chiều", NAVY, NAVY, co=16, mau_chu="white")
    bo = [("A", "Bộ A\nÂm sắc và đường bao phổ", "28 chiều", 2.0,
           [("MFCC", "13 hệ số × 2 = 26"), ("Spectral\nRoll-off", "1 × 2 = 2")]),
          ("B", "Bộ B\nNăng lượng và dạng sóng", "4 chiều", 6.0,
           [("RMS\nEnergy", "1 × 2 = 2"), ("Zero-Crossing\nRate", "1 × 2 = 2")]),
          ("C", "Bộ C\nĐộ tương phản phổ", "14 chiều", 10.0,
           [("Spectral Contrast", "7 dải × 2 = 14")])]
    ax.plot([2.0, 10.0], [5.05, 5.05], color=XAM, lw=2.2)
    ax.plot([6.0, 6.0], [5.5, 5.05], color=XAM, lw=2.2)
    for k, ten, so, cx, con in bo:
        vien, nen = MAU[k]
        mui_ten(ax, cx, 5.05, cx, 4.6)
        hop(ax, cx - 1.85, 3.2, 3.7, 1.4, ten, so, vien, nen, co=12.5)
        ax.plot([cx, cx], [3.2, 2.7], color=XAM, lw=2.2)
        vi_tri = [cx - 0.95, cx + 0.95] if len(con) == 2 else [cx]
        if len(con) == 2:
            ax.plot(vi_tri, [2.7, 2.7], color=XAM, lw=2.2)
        for (t, p), x in zip(con, vi_tri):
            mui_ten(ax, x, 2.7, x, 2.3)
            w = 1.8 if len(con) == 2 else 2.6
            hop(ax, x - w / 2, 1.0, w, 1.3, t, p, vien, "#f7f9fb", co=11.5)
    ax.text(6, 0.4, "× 2: mỗi chuỗi giá trị theo khung được tóm tắt bằng 2 số là trung bình (mean) và độ lệch chuẩn (std)",
            ha="center", fontsize=12, color=XAM)
    fig.savefig(HINH / "4_1_cau_truc_46_chieu.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def quy_trinh():
    buoc = [("1. Tệp âm thanh", "đoạn WAV 2,5–3,5 s", "A"),
            ("2. Tiền xử lý", "mono, 22 050 Hz,\nchuẩn hóa đỉnh", "A"),
            ("3. Chia khung", "khung N = 2 048 mẫu,\nbước nhảy H = 512", "A"),
            ("4. Đặc trưng mỗi khung", "MFCC (13), Roll-off,\nRMS, ZCR, Contrast (7)", "B"),
            ("5. Temporal Pooling", "mean và std\ncủa từng chuỗi", "B"),
            ("6. Ghép vector", "46 chiều: Bộ A (28)\n+ B (4) + C (14)", "C")]
    fig, ax = plt.subplots(figsize=(12, 5.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    w, h = 3.3, 1.9
    xs = [0.3, 4.35, 8.4]
    for i, (t, p, k) in enumerate(buoc):
        hang = i // 3
        cot = i % 3 if hang == 0 else 2 - i % 3            # hàng dưới đi từ phải sang trái
        x, y = xs[cot], 3.2 if hang == 0 else 0.3
        hop(ax, x, y, w, h, t, p, *MAU[k], co=13)
    mui_ten(ax, 3.6, 4.15, 4.35, 4.15)
    mui_ten(ax, 7.65, 4.15, 8.4, 4.15)
    mui_ten(ax, 10.05, 3.2, 10.05, 2.2)
    mui_ten(ax, 8.4, 1.25, 7.65, 1.25)
    mui_ten(ax, 4.35, 1.25, 3.6, 1.25)
    fig.savefig(HINH / "4_2_quy_trinh_trich_dac_trung.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    cau_truc()
    quy_trinh()
    print("Đã lưu 4_1_cau_truc_46_chieu.png, 4_2_quy_trinh_trich_dac_trung.png vào", HINH)
