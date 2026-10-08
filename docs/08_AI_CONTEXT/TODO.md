# TODO

## Cần người dùng quyết định
- [ ] Lịch sử repo public còn chứa file Philharmonia: chuyển **Private** / viết lại lịch sử / để vậy
- [ ] Push commit `0fcc0cd`; commit scripts, tests, reports, docs mới

## Dataset (Bước 1): ✅ xong
- [x] **1.1** Tải Iowa MIS: guitar (45 file) + arco 4 nhạc cụ kéo vĩ (143 file)
- [x] **1.2** Cắt nốt Iowa: 1 429 / 1 552 (92%)
- [x] **1.3–1.5** Catalog 5 906 file + lọc + chia tập + sắp xếp `data/`
- [x] **1.6** Thống kê + biểu đồ (`reports/dataset/`)
- [x] Xác nhận nguồn và giấy phép của `raw/philharmonia/` (Philharmonia Sound Samples)
- [x] Bước 0: `.venv` + `requirements.txt`
- [ ] Bước 0 (phần còn lại): khung `src/strings_mmdb/` + `config.py`
- [ ] (Đề xuất) Nghe ngẫu nhiên ~20 nốt Iowa để kiểm tra bằng tai

## Lý thuyết: ✅ xong
- [x] Viết lại `docs/01_THEORY/` (22 file) theo yêu cầu `CLAUDE.md`, minh họa bằng số đo thật (`scripts/theory_figures.py`)
- [x] Sửa nhãn dây Mi của guitar (`lowE`/`highE`, D28); ghi D27 (lọc 25 Hz)

## Tiếp theo
- [ ] **Quyết định P07–P12** (pYIN fmin, MFCC std, RMS-CV, tiếng ồn nền, đánh giá khác nguồn) trước hoặc trong Bước 3
- [ ] **Bước 2:** `load_audio()`, gồm lọc thông cao 25 Hz trước chuẩn hóa đỉnh (D27)
- [ ] **Bước 3:** đặc trưng 32D + tương quan + boxplot (điền INSTRUMENT_CHARACTERISTICS §5; số sơ bộ đã có ở `docs/01_THEORY/15`)
- [ ] **Bước 4:** 20 prototype
- [ ] **Bước 5:** ghép 500 file CSDL + 100 truy vấn

Chi tiết: [MILESTONES](../02_PLANS/MILESTONES.md).

## Quyết định đang chờ số liệu
Xem [DESIGN_DECISIONS](DESIGN_DECISIONS.md), mục "Chờ quyết định".
