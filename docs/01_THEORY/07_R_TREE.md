# 07. R-TREE

## 1. Mục đích
Chỉ mục cho **đối tượng nhiều chiều** (điểm, hộp) để trả lời nhanh truy vấn vùng (range) và láng giềng gần nhất (k-NN), thay vì quét toàn bộ (Lecture 6).

## 2. Cấu trúc
- Mỗi node chứa từ m tới M entry (m ≈ 40% M).
- **Leaf entry:** (MBR của đối tượng, id). Với điểm, MBR là hộp suy biến (min = max).
- **Internal entry:** (MBR bao toàn bộ con, con trỏ tới node con).
- **MBR** (Minimum Bounding Rectangle): hộp nhỏ nhất song song với các trục, bao trọn mọi thứ bên trong.
- Cây **cân bằng**: mọi lá ở cùng độ sâu.

```
Root [MBR toàn cục]
 ├── N1 [MBR1] ─┬── L1 [..] → ids
 │              └── L2 [..] → ids
 └── N2 [MBR2] ─┬── L3 [..] → ids
                └── L4 [..] → ids
```

## 3. Chèn
1. **ChooseLeaf:** từ gốc đi xuống, ở mỗi mức chọn entry có MBR **phải mở rộng ít nhất** để chứa đối tượng mới.
2. Thêm vào lá. Nếu lá vượt M entry thì **Split** (quadratic split: chọn hai entry "xa nhau nhất" làm hạt giống, rồi phân phối các entry còn lại).
3. **AdjustTree:** cập nhật MBR từ dưới lên; split có thể lan lên tới gốc.

**R\*-tree** cải tiến bằng cách chọn split giảm **chồng lấn** và chu vi, đồng thời dùng **forced reinsert** (chèn lại một phần entry trước khi split) ⇒ MBR gọn hơn, tìm kiếm nhanh hơn.

## 4. Tìm k-NN (best-first)
```
MINDIST(q, R) = √Σᵢ ( q_i < lo_i ? lo_i − q_i : q_i > hi_i ? q_i − hi_i : 0 )²
hàng đợi ưu tiên H ← (MINDIST(q, root), root)
while H không rỗng:
    lấy phần tử có MINDIST nhỏ nhất
    nếu là đối tượng: trả ra (đây là láng giềng gần tiếp theo)
    nếu là node: đẩy mọi con vào H với MINDIST của chúng
```
**Cắt tỉa (pruning):** nhánh có MINDIST lớn hơn khoảng cách hiện tại tới láng giềng thứ k thì không bao giờ được mở.

## 5. Filter-and-refine (GEMINI)
Khi khoảng cách trong không gian chỉ mục d_idx là **cận dưới** của khoảng cách thật D (d_idx ≤ D):
1. **Filter:** dùng R-tree lấy ứng viên theo d_idx.
2. **Refine:** tính D thật cho ứng viên.
3. **Dừng:** khi d_idx của ứng viên chưa xét ≥ D của kết quả thứ k hiện tại. Mọi điểm chưa xét chắc chắn xa hơn ⇒ kết quả **chính xác**, không bỏ sót (no false dismissal).

## 6. Lời nguyền số chiều
Khi số chiều tăng, MBR chồng lấn nhiều và gần như mọi điểm có khoảng cách xấp xỉ nhau, nên R-tree phải mở gần hết các node và không còn nhanh hơn quét tuyến tính. Thực tế R-tree hiệu quả ở khoảng ≲ 10 chiều. Cách xử lý: giảm chiều (PCA) + filter-and-refine.

## 7. So sánh ngắn
| Cấu trúc | Ghi chú |
|---|---|
| k-d tree | Chia không gian theo một trục mỗi mức; tốt cho điểm, dữ liệu tĩnh |
| Quadtree | Chia 2^d ô mỗi mức; thực tế chỉ dùng cho 2D/3D |
| **R-tree** | Chia **dữ liệu** bằng MBR; cân bằng; chèn động; phổ biến trong DBMS (SQLite R\*Tree, PostGIS) |
