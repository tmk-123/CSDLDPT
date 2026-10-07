# 04. CLUSTERING & BAG-OF-PROTOTYPES

## 1. K-means
Cho các điểm {x_r} và số cụm k, tìm các tâm {P_j} cực tiểu hóa J = Σ_r min_j ‖x_r − P_j‖².
```
khởi tạo k tâm (k-means++)
lặp: gán mỗi điểm vào tâm gần nhất → cập nhật tâm = trung bình các điểm trong cụm
dừng khi các phép gán không đổi
```
- Kết quả phụ thuộc khởi tạo, nên chạy nhiều lần (`n_init`) và giữ lần có J nhỏ nhất.
- **Chọn k:** phương pháp elbow (J theo k), **silhouette** s = (b − a)/max(a, b), với a là khoảng cách trung bình trong cụm và b là khoảng cách trung bình tới cụm gần nhất khác.
- Phải chuẩn hóa (z-score) trước, nếu không chiều có thang lớn sẽ áp đảo.

## 2. Prototype
Một **prototype** là một điểm đại diện cho một nhóm. Trong bài, nhóm là "một kiểu âm sắc của một nhạc cụ"; tâm K-means chính là prototype.

## 3. Bag-of-Words → Bag-of-Prototypes
Ý tưởng từ truy vấn văn bản (Lecture 8): tài liệu được biểu diễn bằng **histogram tần suất từ**, không quan tâm thứ tự. Áp dụng cho audio:
- "từ" = prototype; "tài liệu" = file; "lần xuất hiện của từ" = segment gần prototype đó.
- Histogram có **số chiều = số prototype**, không phụ thuộc độ dài file.

## 4. Gán cứng và gán mềm
- **Hard:** mỗi segment góp 1 vào bin gần nhất. Không ổn định ở biên giữa hai cụm.
- **Soft (softmax theo khoảng cách):** w_j = exp(−d_j²/τ) / Σ exp(−d_j'²/τ). Mọi bin nhận một phần; τ nhỏ ⇒ gần với hard, τ lớn ⇒ phân bố đều.

## 5. Mở rộng (để biết, không dùng)
- **VLAD:** cộng dồn phần dư (x − P_j) theo cụm ⇒ k·D chiều.
- **Fisher vector:** dùng gradient của GMM ⇒ 2·k·D chiều.
Cả hai mạnh nhưng có số chiều rất lớn.
