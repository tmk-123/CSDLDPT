# CURRENT STATUS

> Cập nhật: 07/10/2026. Ghi **trung thực**: chỉ đánh ✅ khi đã có code chạy được và đã kiểm tra.

## Đã có
- ✅ Dataset gốc: 4 477 MP3, 7 nhạc cụ, trong `Strings/`.
- ✅ **Quét lọc toàn bộ dataset** (script phân tích tạm, chưa phải code project): 1 file hỏng, 2 cặp trùng, 55 nốt quá ngắn, gần như không có clipping. Số nốt dùng được: violin 959, viola 759, cello 756, double-bass 763, **guitar 106** ([DATASET_COLLECTION_AND_FILTERING](../04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md)).
- ✅ Tìm và kiểm tra nguồn bổ sung: đề xuất University of Iowa MIS (D21).
- ✅ Bộ tài liệu thiết kế Phần 1, 2.
- ⚠️ `Strings/scan_dataset.py`: `DATA_DIR` trỏ sai; sẽ được thay bằng `catalog.py`.

## Vấn đề dataset đang mở
| Vấn đề | Hướng xử lý | Trạng thái |
|---|---|---|
| Guitar thiếu khoảng 250 nốt | Tải Iowa MIS (D21) | ✅ Đã tải guitar (45 file, ~353 nốt dự kiến); ⏳ chưa cắt nốt (D2) |
| Pizz quá hiếm | Chỉ dùng arco (D20) | ✅ Đã quyết định |
| Nguồn và giấy phép của `Strings/` chưa xác nhận | Tìm lại nguồn tải | ⬜ |

## Tiến độ

| Bước | Việc | Trạng thái |
|---|---|---|
| 0 | Môi trường + khung thư mục code | ⬜ |
| **1** | **Dataset: D1 tải Iowa · D2 cắt nốt · D3 catalog · D4 lọc · D5 chia tập · D6 mô tả** | ⏳ Đã quét `Strings/`; chưa tải Iowa |
| 2 | `load_audio` | ⬜ |
| 3 | Đặc trưng 32D | ⬜ |
| 4 | Prototype | ⬜ |
| 5 | Ghép sequence | ⬜ |
| 6 | Segmentation | ⬜ |
| 7 | Vector 52D (bàn giao Phần 1) | ⬜ |
| 8–11 | Phần 2 | ⬜ |

## Việc tiếp theo
**Bước D1:** tải Iowa MIS cho 5 nhạc cụ. Song song có thể làm Bước 0.
