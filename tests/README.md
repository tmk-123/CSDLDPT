# tests/ — Kiểm tra tự động

> **Tóm tắt:** các kiểm tra chạy được bằng một lệnh, để chắc chắn dữ liệu và kết quả đúng như thiết kế, kể cả sau khi chạy lại script hay đổi quy tắc. Không cần cài thêm thư viện (không bắt buộc pytest).

## Cách chạy
```powershell
.venv\Scripts\python tests\test_catalog.py
```
Kết quả mong đợi: dòng cuối là **`12 đạt, 0 lỗi`**. Nếu đã cài pytest thì `pytest tests\` cũng chạy được.

## `test_catalog.py` — kiểm tra dataset (Bước 1.3–1.5)
Yêu cầu: đã chạy `scripts/p01_3_build_catalog.py`.

| Kiểm tra | Bảo vệ khỏi lỗi gì |
|---|---|
| Mỗi file trong `data/notes`, `queries`, `excluded` có đúng một dòng catalog; mọi đường dẫn tồn tại | Mất file, thừa file, catalog lệch với thư mục |
| Đúng 1 `CORRUPT`, 4 `DUPLICATE` | Quy tắc lọc bị thay đổi ngoài ý muốn |
| `TOO_SHORT` ⇔ phần có âm < 0.35 s (kiểm tra **quy tắc**, không cố định con số) | Gắn nhãn quá ngắn sai. Không cố định con số vì nó đổi khi đổi cách đo (ví dụ khi thêm lọc tiếng ù, D27: 70 → 76) |
| Không cặp (nhạc cụ, cao độ) nào nằm ở hai tập | **Rò rỉ dữ liệu**: cùng một nốt vừa ở tập học vừa ở tập thử khiến kết quả cao ảo |
| Mọi nốt tuân đúng quy tắc `midi mod 5` | Chia tập sai quy tắc |
| Số nốt được chọn không vượt REF 150 / DB_POOL 200 / QUERY_POOL 60 | Mất cân bằng giữa các nhạc cụ |
| Mỗi (nhạc cụ, tập) được chọn đều có cả hai nguồn | Hệ thống học nhầm "phòng thu" thay vì nhạc cụ |
| Banjo, mandolin không lọt vào `data/notes/` | Nhạc cụ dùng để thử "ngoài CSDL" bị lẫn vào CSDL |
| File lỗi chỉ nằm trong `data/excluded/` | Dùng nhầm file hỏng, trùng, quá ngắn |
| `data/notes/` chỉ có arco (bộ kéo vĩ) và pluck/harmonic (guitar) | Lẫn kỹ thuật không dùng (pizz, col legno…) |
| Nhãn dây Iowa là dây có thật của nhạc cụ, và nốt không thấp hơn dây buông | Tầng "dây" của mô hình dữ liệu bị sai, ví dụ gộp hai dây Mi của guitar (D28) |
| Mỗi nhạc cụ có ≥ 360 nốt dùng được | Thiếu dữ liệu cho các bước sau |

Sẽ bổ sung test cho các bước sau (đặc trưng, segmentation, R-tree…) theo [PART_1_PLAN](../docs/02_PLANS/PART_1_PLAN.md) và [PART_2_PLAN](../docs/02_PLANS/PART_2_PLAN.md).
