# CURRENT STATUS

> Cập nhật: 07/10/2026. Ghi **trung thực**: chỉ đánh ✅ khi đã có code chạy được và đã kiểm tra.

## Đã có
- ✅ Dataset gốc: 4 477 MP3, 7 nhạc cụ, trong `Strings/` ([AUDIT_REPORT](AUDIT_REPORT.md)).
- ✅ Bộ tài liệu thiết kế Phần 1, 2 (cấu trúc docs mới).
- ⚠️ `Strings/scan_dataset.py`: script parse tên file + ffprobe. **`DATA_DIR` trỏ sai** (`D:\Ki1_4\HCSDLDPT\Strings`), nên chưa chạy được. Sẽ được thay bằng `catalog.py` ở Bước 1.

## Chưa có (theo thứ tự sẽ làm)

| Bước | Việc | Trạng thái |
|---|---|---|
| 0 | Môi trường + khung thư mục code | ⬜ |
| 1 | Catalog + split | ⬜ |
| 2 | `load_audio` | ⬜ |
| 3 | Đặc trưng 32D | ⬜ |
| 4 | Prototype | ⬜ |
| 5 | Ghép sequence | ⬜ |
| 6 | Segmentation | ⬜ |
| 7 | Vector 52D (bàn giao Phần 1) | ⬜ |
| 8 | CSDL SQLite | ⬜ |
| 9 | Chuẩn hóa + PCA | ⬜ |
| 10 | R-tree + k-NN chính xác | ⬜ |
| 11 | Query CLI | ⬜ |

Chi tiết từng bước: [PART_1_PLAN](../02_PLANS/PART_1_PLAN.md), [PART_2_PLAN](../02_PLANS/PART_2_PLAN.md).

## Việc tiếp theo
**Bước 0 → Bước 1.**
