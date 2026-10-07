# 06. PCA (Principal Component Analysis)

## 1. Ý tưởng
Tìm các trục mới (thành phần chính) trực giao với nhau, theo thứ tự **phương sai giảm dần**. Giữ d' trục đầu sẽ giữ được nhiều thông tin (phương sai) nhất có thể với d' chiều.

## 2. Thuật toán
```
X: N × d (đã chuẩn hóa)          m = mean(X)
Σ = (X − m)ᵀ(X − m)/(N − 1)      ma trận hiệp phương sai d × d
Σ = Q Λ Qᵀ                       trị riêng λ₁ ≥ λ₂ ≥ …, vector riêng là các cột của Q
W = d' cột đầu của Q             d × d', các cột trực chuẩn
u = Wᵀ (x − m)                   tọa độ mới (d' chiều)
explained variance ratio = Σ_{i≤d'} λᵢ / Σ λᵢ
```
**Whitening** (tùy chọn): chia thêm mỗi tọa độ cho √λᵢ để mọi trục có phương sai 1.

## 3. Tính chất cận dưới (quan trọng cho tìm kiếm)
W có các cột trực chuẩn, nên phép chiếu **không làm dài** vector:
```
‖u_a − u_b‖ = ‖Wᵀ(x_a − x_b)‖ ≤ ‖x_a − x_b‖
```
(Phép chiếu trực giao lên không gian con chỉ bỏ bớt thành phần, không khuếch đại.) Do đó khoảng cách sau PCA là **cận dưới** của khoảng cách gốc. Có whitening thì tính chất này **mất**, vì phép chia cho √λᵢ < 1 có thể làm dài vector.

## 4. Quy tắc dùng đúng
- **Fit một lần** trên tập tham chiếu; mọi điểm mới (kể cả query) chỉ dùng `transform` với cùng m và W.
- Phải chuẩn hóa trước PCA, nếu không trục chính sẽ chỉ chạy theo chiều có thang lớn.

## 5. Giảm chiều và chỉ mục
Cấu trúc như R-tree hiệu quả ở số chiều thấp. PCA đưa dữ liệu về số chiều thấp; kết hợp với cận dưới cho phép **lọc ở chiều thấp, tinh chỉnh ở chiều cao** mà không mất độ chính xác. Đây là khung **GEMINI** (Faloutsos) trong CSDL đa phương tiện.
