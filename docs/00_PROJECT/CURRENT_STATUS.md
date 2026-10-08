# CURRENT STATUS

> Cập nhật: 08/10/2026. Ghi **trung thực**: chỉ đánh ✅ khi đã có code chạy được và đã kiểm tra.
> Kết quả chi tiết từng phần: [RESULTS_REPORT.md](RESULTS_REPORT.md).

## Đã xong
- ✅ **Thiết kế Phần 1, 2** (bộ docs mới; quyết định D01–D28; 6 mục chờ P07–P12 từ số đo).
- ✅ **Lý thuyết (`docs/01_THEORY/`)**: viết lại 22 file theo yêu cầu `CLAUDE.md` (từ âm thanh cơ bản → từng nhạc cụ → đặc trưng → R-tree), minh họa bằng 16 hình và số đo trên dataset thật (`scripts/theory_figures.py`, `reports/theory/`).
- ⏳ **Bước 0 — Môi trường:** `.venv` (Python 3.13.9, librosa 1.0.0, scikit-learn 1.9.1, rtree 1.4.1) và `requirements.txt` ✅. **Chưa có** `src/strings_mmdb/config.py` và khung thư mục `src/` (sẽ tạo khi bắt đầu Bước 2).
- ✅ **Bước 1 — Dataset (1.1–1.6):**
  - 1.1 Tải Iowa MIS: guitar 45 file + arco 143 file (violin 35, viola 32, cello 41, double bass 35).
  - 1.2 Cắt nốt Iowa: **1 429 / 1 552 nốt (92%)**.
  - 1.3–1.5 Catalog **5 906 file**, lọc, chia tập theo `midi mod 5`, chọn trong giới hạn, sắp xếp vào `data/notes/`, `data/queries/`, `data/excluded/`.
  - 1.6 Thống kê + 2 biểu đồ trong `reports/dataset/`.
  - Lọc tiếng ù hạ âm 25 Hz trước mọi phép đo (D27); sửa nhãn dây Mi của guitar (`lowE`/`highE`, D28).
  - `tests/test_catalog.py`: **12 / 12 đạt**.

| Nhạc cụ | Nốt dùng được | REF / DB_POOL / QUERY_POOL được chọn |
|---|---|---|
| violin | 1 141 | 150 / 200 / 60 |
| viola | 990 | 150 / 200 / 60 |
| cello | 1 047 | 150 / 200 / 60 |
| double bass | 1 030 | 150 / 200 / 60 |
| guitar | 445 | 150 / 181 / 60 |

## Vấn đề đang mở
| Vấn đề | Trạng thái |
|---|---|
| Repo GitHub public còn chứa file Philharmonia trong lịch sử | ⏳ Chờ người dùng chọn: Private / viết lại lịch sử / để vậy |
| Commit `0fcc0cd` (ngừng theo dõi dữ liệu Philharmonia) chưa push | ⏳ Chờ người dùng |
| Scripts, tests, reports, docs mới chưa commit | ⏳ Chờ người dùng |
| Nốt Iowa chưa nghe kiểm tra bằng tai | ⬜ Đề xuất nghe ngẫu nhiên ~20 file |
| Mục chờ P07–P12 (pYIN fmin, MFCC std, RMS-CV, tiếng ồn nền, đặc trưng không chuyển sang nguồn thu khác) | ⏳ Cần quyết định trước/trong Bước 3 ([DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md)) |

## Tiến độ

| Bước | Việc | Trạng thái |
|---|---|---|
| 0 | Môi trường | ⏳ thư viện ✅, `config.py` chưa |
| 1 | Dataset: 1.1 tải Iowa · 1.2 cắt nốt · 1.3 catalog · 1.4 lọc · 1.5 chia tập · 1.6 mô tả | ✅ |
| 2 | `load_audio` | ⬜ |
| 3 | Đặc trưng 32D | ⬜ |
| 4 | Prototype | ⬜ |
| 5 | Ghép 500 file đoạn nhạc + 100 truy vấn | ⬜ |
| 6 | Segmentation | ⬜ |
| 7 | Vector 52D (bàn giao Phần 1) | ⬜ |
| 8–11 | Phần 2 | ⬜ |

## Việc tiếp theo
Tạo khung `src/strings_mmdb/` + `config.py` (hoàn tất Bước 0), rồi **Bước 2:** `load_audio()` dùng chung.
