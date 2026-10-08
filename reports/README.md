# reports/ — Số liệu và biểu đồ sinh tự động

> **Tóm tắt:** mọi file ở đây do script trong [`scripts/`](../scripts/README.md) sinh ra từ dữ liệu thật. **Không sửa tay**; muốn cập nhật thì chạy lại script. Thư mục này **có trong git** (file nhỏ, dùng trực tiếp cho báo cáo).
>
> Docs chỉ **trích và giải thích** các con số ở đây; nguồn sự thật là script và dữ liệu.

## 1. `reports/dataset/` — mô tả dataset (Bước 1.6)
Tạo bởi: `scripts/p01_6_dataset_stats.py`.

| File | Nội dung |
|---|---|
| `dataset_stats.md` | 8 bảng: tổng quan trạng thái, phân bổ split, nốt dùng được và số được chọn, độ phủ cao độ, file không dùng, file truy vấn, kết quả cắt nốt Iowa, thời lượng |
| `notes_by_instrument.png` | Số nốt dùng được theo nhạc cụ, tách theo nguồn (Philharmonia / Iowa), có vạch mức cần 360 |
| `pitch_coverage.png` | Mỗi nhạc cụ có bao nhiêu nốt ở từng cao độ (ô xám = không có nốt) |
| `status_by_source.csv` | Số file theo nguồn × trạng thái |
| `split_by_instrument.csv` | Số file theo nhạc cụ × split |
| `usable_by_instrument.csv` | Nốt dùng được, số được chọn / có trong từng tập |
| `pitch_coverage.csv` | Âm vực, số cao độ, nốt mỗi cao độ, cao độ trống |
| `excluded_by_reason.csv` | File không dùng theo nhạc cụ × lý do |
| `queries.csv` | Số file truy vấn (phrase, unseen) |
| `iowa_slicing.csv` | Kết quả cắt nốt Iowa theo nhạc cụ |
| `active_duration.csv` | Trung vị thời lượng phần có âm theo nhạc cụ × nguồn |

## 2. `reports/theory/` — hình và số đo cho phần lý thuyết
Tạo bởi: `scripts/theory_figures.py`. Danh sách 16 hình và nơi dùng: [docs/01_THEORY/README.md](../docs/01_THEORY/README.md) §4.

| File | Nội dung |
|---|---|
| `01_…png` → `16_…png` | 16 hình minh họa (mô phỏng có ghi rõ, còn lại là dữ liệu thật) |
| `note_features.csv` | Đặc trưng của 5 190 nốt: centroid, bandwidth, rolloff, ZCR, flatness, RMS-CV, MFCC c1–c13 mean và std |
| `feature_summary_by_instrument.csv` | Trung vị và tứ phân vị của từng đặc trưng theo nhạc cụ |
| `feature_sensitivity.csv` | Tương quan với cao độ, chênh lệch giữa nhạc cụ, độ lệch giữa hai nguồn thu |
| `feature_information.csv` | η²: nhạc cụ / cặp khó / nguồn thu giải thích bao nhiêu % biến thiên của từng đặc trưng |
| `source_transfer_1nn.csv` | Láng giềng gần nhất có cùng nhạc cụ không, khi tìm trong cùng nguồn và sang nguồn khác |
| `pca_notes_explained.csv`, `pca_notes_top_loadings.csv`, `pca_notes_axes_eta2.csv`, `pca_lower_bound_check.csv` | PCA trên vector 32 chiều của nốt: phương sai giữ lại, ý nghĩa các trục, kiểm tra cận dưới |
| `harmonics_A3.csv` | Độ mạnh 15 harmonic đầu của nốt A3 trên 5 nhạc cụ |
| `centroid_by_pitch.csv` | Centroid trung vị theo cao độ và nhạc cụ |
| `source_effect_centroid.csv` | Centroid Iowa so với Philharmonia trên các cao độ chung |
| `violin_technique_dynamics.csv` | Centroid, RMS-CV theo kỹ thuật và cường độ (violin) |
| `vibrato.csv` | Độ dao động cao độ có và không có vibrato |
| `unseen_feature_summary.csv` | Đặc trưng của banjo, mandolin |

## 3. Cách tạo lại
```powershell
.venv\Scripts\python scripts\p01_6_dataset_stats.py
.venv\Scripts\python scripts\theory_figures.py
```
