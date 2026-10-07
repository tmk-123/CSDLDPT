# Hệ CSDL Lưu Trữ Và Tìm Kiếm Tiếng Nhạc Cụ Bộ Dây
### (Content-Based Audio Retrieval System for String Instruments)

> **Môn học**: Hệ Cơ sở Dữ liệu Đa phương tiện (Multimedia Database Systems - MMDB)
> **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**
> **Giảng viên hướng dẫn**: TS. Nguyễn Đình Hóa (`hoand@ptit.edu.vn`)

---

## 1. Giới thiệu
Hệ thống **tìm kiếm âm thanh theo nội dung (CBAR)** cho nhạc cụ bộ dây. CSDL chứa **500 file multi-note** của 5 nhạc cụ (violin, viola, cello, double bass, guitar). Mỗi file được biểu diễn bằng **một vector đặc trưng 52 chiều**, gồm hồ sơ so khớp với 20 prototype âm sắc học từ thư viện nốt đơn và âm sắc trung bình. Vector được giảm xuống **8 chiều bằng PCA** và đánh chỉ mục bằng **R\*-tree**. Với một file truy vấn (nhạc cụ đã có hoặc chưa có trong CSDL), hệ thống trả về **Top-5** file giống nhất, có kết quả chính xác nhờ cơ chế lọc rồi tinh chỉnh.

## 2. Trạng thái

| Yêu cầu đề bài | Trạng thái |
|---|---|
| 1. Dataset ≥ 500 file | 📝 Đã có 4 477 nốt đơn gốc; 500 file multi-note **chưa được tạo** |
| 2. Bộ đặc trưng | 📝 Đã thiết kế (32D/segment, 52D/file); chưa có code |
| 3. Trích rút + CSDL | 📝 Đã thiết kế; chưa có code |
| 4. Tìm kiếm Top-5 (R-tree) | 📝 Đã thiết kế; chưa có code |
| 5. Đánh giá, demo | ⬜ Chưa làm |

Chi tiết: [docs/00_PROJECT/CURRENT_STATUS.md](docs/00_PROJECT/CURRENT_STATUS.md).

## 3. Tài liệu
Toàn bộ thiết kế nằm trong [docs/](docs/README.md). Bắt đầu đọc từ:
1. [docs/00_PROJECT/PROJECT_OVERVIEW.md](docs/00_PROJECT/PROJECT_OVERVIEW.md): hệ thống làm gì (trả lời nhanh 16 câu hỏi).
2. [docs/02_PLANS/PART_1_PLAN.md](docs/02_PLANS/PART_1_PLAN.md) và [PART_2_PLAN.md](docs/02_PLANS/PART_2_PLAN.md): các bước phải làm.
3. [docs/08_AI_CONTEXT/DESIGN_DECISIONS.md](docs/08_AI_CONTEXT/DESIGN_DECISIONS.md): vì sao chọn như vậy.

## 4. Cấu trúc thư mục hiện tại
```
BTL/
├── CLAUDE.md          # quy tắc làm việc (docs là nguồn thiết kế)
├── README.md
├── yeu_cau.txt        # đề bài
├── MMDB slides/       # slide môn học
├── Strings/           # dữ liệu gốc, 4 477 mp3, 7 nhạc cụ (CHỈ ĐỌC)
└── docs/              # thiết kế (xem docs/README.md)
```
Cấu trúc code dự kiến (`src/`, `scripts/`, `tests/`, `data/`): [docs/02_PLANS/MASTER_PLAN.md](docs/02_PLANS/MASTER_PLAN.md) §3.

## 5. Môi trường
Windows 10, Python 3.13 (hoặc 3.12), FFmpeg. Thư viện: `numpy scipy matplotlib librosa soundfile scikit-learn rtree`. Hướng dẫn: Bước 0 trong [PART_1_PLAN](docs/02_PLANS/PART_1_PLAN.md).
