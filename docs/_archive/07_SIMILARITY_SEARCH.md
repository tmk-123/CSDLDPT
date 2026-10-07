# 07. SIMILARITY SEARCH ENGINE & RANKING ALGORITHM

Tài liệu này giải thích thuật toán tìm kiếm tương đồng và xếp hạng kết quả (Ranking Top-5), áp dụng kiến thức từ [Lecture 7 - Vector database and Clustering](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf) và [Lecture 10 - Indexing and Retrieval for Audio](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf).

---

## 1. Định Nghĩa "Âm Thanh Giống Nhất" (Similarity Criterion)
Trong hệ thống CBAR (Content-Based Audio Retrieval), khái niệm **"giống nhất"** không đồng nghĩa với việc có cùng tên nhãn nhạc cụ hay cùng người biểu diễn.

> **Định nghĩa tiêu chí giống nhất**:
> Hai âm thanh được coi là giống nhau nhất khi chúng có **khoảng cách nhỏ nhất trong không gian đặc trưng âm học đa chiều (Acoustic Feature Space)**.
> Điều này phản ánh sự tương đồng chặt chẽ về:
> 1. **Âm sắc (Timbre)**: Hình bao phổ Fourier và các hệ số MFCC tương đồng (độ dày, độ ấm của tiếng đàn).
> 2. **Độ sáng (Brightness)**: Trọng tâm phổ Spectral Centroid và độ rộng dải phổ Bandwidth nằm trong cùng miền phân bố.
> 3. **Đặc tính thời gian**: Động lực học năng lượng (RMS envelope) và tỷ lệ khoảng lặng (silence ratio) có hành vi kích hoạt tương tự.

---

## 2. Các Độ Đo Tương Đồng & Khoảng Cách

Dựa trên Slide 6-7 và Slide 19 của [Lecture 7](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf):

### 2.1. Độ Đo Cosine Similarity (Chuẩn hóa góc)
* **Ý nghĩa**: Đo góc giữa vector truy vấn $Q$ và vector tài liệu CSDL $D_i$. Độ đo này độc lập với độ dài/độ lớn tuyệt đối của vector.
* **Công thức** (Trích Slide 6, 7 - Lecture 7):
  $$S(D_i, Q) = \frac{D_i \cdot Q}{\|D_i\|_2 \cdot \|Q\|_2} = \frac{\sum_{k=1}^N d_{ik} \cdot q_k}{\sqrt{\sum_{k=1}^N d_{ik}^2} \cdot \sqrt{\sum_{k=1}^N q_k^2}}$$
* **Khoảng giá trị**: $S(D_i, Q) \in [-1, 1]$, đối với vector đặc trưng không âm hoặc chuẩn hóa thường thuộc $[0, 1]$.
* **Cosine Distance**:
  $$d_{\text{cosine}}(D_i, Q) = 1 - S(D_i, Q)$$
* **Tối ưu hóa tính toán**: Nếu tất cả các vector trong CSDL và vector truy vấn đều được chuẩn hóa trước thành vector đơn vị độ dài bằng 1 ($\|D_i\|_2 = 1, \|Q\|_2 = 1$), thì Cosine Similarity đơn giản là **tích vô hướng (Inner Product)**:
  $$S(D_i, Q) = D_i \cdot Q = \sum_{k=1}^N d_{ik} \cdot q_k$$
  Thao tác này chạy cực kỳ nhanh bằng phép nhân ma trận - vector của BLAS/NumPy.

### 2.2. Khoảng Cách Euclid ($L_2$-norm Distance)
* **Công thức** (Trích Slide 19 - Lecture 7):
  $$L_2(D_i, Q) = \sqrt{\sum_{k=1}^N (d_{ik} - q_k)^2}$$
* **Ý nghĩa**: Đo khoảng cách hình học đường thẳng giữa hai điểm trong không gian đặc trưng.
* **Mối liên hệ**: Khi vector đã được chuẩn hóa đơn vị ($L_2\text{-normalized}$), khoảng cách Euclid bình phương và Cosine Similarity có quan hệ tuyến tính trực tiếp:
  $$\|D_i - Q\|_2^2 = \|D_i\|_2^2 + \|Q\|_2^2 - 2 (D_i \cdot Q) = 2 - 2 \cdot S(D_i, Q)$$
  Do đó, xếp hạng theo giảm dần Cosine Similarity hay tăng dần khoảng cách Euclid cho ra **kết quả thứ tự hoàn toàn trùng khớp**!

---

## 3. Quy Trình Chuẩn Hóa Vector (Feature Normalization)
Để các đặc trưng đóng góp công bằng vào độ tương đồng, quy trình gồm hai bước:
1. **Z-Score Standardization (trên từng chiều $k$)**:
   $$\hat{x}_k = \frac{x_k - \mu_k}{\sigma_k}$$
   với $\mu_k, \sigma_k$ được tính toán trên toàn bộ kho CSDL ngoại tuyến (Offline DB).
2. **L2 Unit Normalization (trên toàn bộ vector)**:
   $$v = \frac{\hat{x}}{\|\hat{x}\|_2}$$

---

## 4. Thuật Toán Xếp Hạng K-NN (Top 5 Ranking)

```python
# Thuật toán xếp hạng Top 5 bằng Cosine Similarity
1. Nhận vector truy vấn q (35 chiều)
2. Chuẩn hóa q theo tham số μ, σ của CSDL
3. L2 normalize q: q_norm = q / norm(q)
4. Tính tích vô hướng với ma trận CSDL V (kích thước M x 35):
       scores = np.dot(V_norm, q_norm)  # M là số file trong DB (4476 files)
5. Sắp xếp giảm dần scores:
       top_indices = np.argsort(scores)[::-1][:5]
6. Trích xuất metadata và file path của 5 bản ghi đứng đầu
7. Trả về kết quả Top-5 kèm điểm Similarity Score và Rank (1 đến 5)
```

---

## 5. Xử Lý Trường Hợp Nhạc Cụ CHƯA CÓ TRONG DATASET (Unseen Class)

Đề bài yêu cầu: *"Input là một file âm thanh mới về một nhạc cụ thuộc bộ dây (nhạc cụ thuộc loại đã có và không có trong dữ liệu)"*.

### 5.1. Phân Tích Bản Chất Vấn Đề
* Nếu hệ thống tìm kiếm theo mô hình phân loại giám sát (Supervised Classification / Label Matching), khi gặp một nhạc cụ chưa từng có trong tập huấn luyện (như đàn Tỳ bà, đàn Đáy, đàn Nhị, Koto, hoặc Harpsichord), hệ thống sẽ bị lỗi hoặc gán cưỡng ép vào 1 trong 7 nhãn có sẵn một cách sai lệch.
* **Giải pháp trong hệ thống của chúng ta**:
  * Hệ thống hoạt động theo mô hình **Query-by-Example (QBE) trên không gian vector đặc trưng nội dung (Content-Based Audio Retrieval - CBAR)** theo đúng [Lecture 10](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf) và [Lecture 7](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf).
  * Hệ thống **hoàn toàn KHÔNG cần biết trước tên nhãn** của nhạc cụ đầu vào.
  * Khi đưa vào file nhạc cụ mới, hệ thống chỉ phân tích tín hiệu âm học thực tế của file đó:
    * Ví dụ: Input là tiếng **đàn Tỳ bà (Pipa)** gảy nốt cao: Hệ thống trích xuất đặc trưng sẽ nhận diện năng lượng transient gảy sắc nhọn, âm sắc kim loại sáng, bồi âm dày -> Top 5 trả về sẽ tự động là các nốt của **Banjo** hoặc **Mandolin** có cùng đặc tính âm sắc!
    * Ví dụ: Input là tiếng **đàn Nhị (Erhu)** kéo vĩ nốt trung: Hệ thống sẽ tìm ra các file tiếng **Violin** hoặc **Viola** có cùng kỹ thuật kéo vĩ (arco) và trọng tâm phổ tương đương.
* **Kết luận**: Cơ chế Content-Based Vector Search là cách tiếp cận duy nhất và hoàn hảo nhất đáp ứng trọn vẹn yêu cầu này của đề bài.

---

## 6. Ví Dụ Tính Toán Số Học Cụ Thể (Numerical Example)
Giả sử vector rút gọn 3 chiều $[SC, ZCR, MFCC_1]$ của Query $Q$ và 3 file trong CSDL $D_1, D_2, D_3$ (đã qua Z-score và chuẩn hóa đơn vị):
* $Q = [0.60, 0.40, 0.69]$
* $D_1 (\text{Violin}) = [0.58, 0.42, 0.70]$
* $D_2 (\text{Viola}) = [0.45, 0.35, 0.82]$
* $D_3 (\text{Double Bass}) = [-0.80, -0.50, 0.33]$

Tính Cosine Similarity (tích vô hướng):
* $S(D_1, Q) = 0.58 \times 0.60 + 0.42 \times 0.40 + 0.70 \times 0.69 = 0.348 + 0.168 + 0.483 = \mathbf{0.999}$ (Gần như trùng khớp hoàn toàn $\to$ Rank 1).
* $S(D_2, Q) = 0.45 \times 0.60 + 0.35 \times 0.40 + 0.82 \times 0.69 = 0.270 + 0.140 + 0.5658 = \mathbf{0.9758}$ (Rất tương đồng $\to$ Rank 2).
* $S(D_3, Q) = -0.80 \times 0.60 - 0.50 \times 0.40 + 0.33 \times 0.69 = -0.48 - 0.20 + 0.2277 = \mathbf{-0.4523}$ (Khác biệt hoàn toàn $\to$ Loại bỏ).
