# 11. SYSTEM EVALUATION & PERFORMANCE METRICS

> **TRẠNG THÁI HIỆN TẠI**: **CHƯA CÓ TRONG CODEBASE GỐC / CẦN TRIỂN KHAI**  
> *(Ghi nhận trung thực: Codebase gốc hiện tại chưa có module đo lường hay ma trận nhầm lẫn Confusion Matrix. Tài liệu này xác lập khung đánh giá chuẩn mực để triển khai khi sang giai đoạn thực thi).*

---

## 1. Phương Pháp & Thang Đo Đánh Giá (Evaluation Metrics)

Để đánh giá chất lượng của hệ thống tìm kiếm tương đồng đa phương tiện theo chuẩn [Lecture 1 - Introduction](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%201%20-%20Introduction.pdf) và [Lecture 5 - MM data model](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%205%20-%20MM%20data%20model.pdf) (Slide 55: *Precision@k / Recall@k*):

### 1.1. Thang Đo Precision@5 (Độ chính xác Top 5)
* Với mỗi truy vấn có nhãn đã biết (Ground Truth), trong số 5 file trả về, tỷ lệ file có cùng họ/loại nhạc cụ hoặc cùng phương thức phát âm:
  $$\text{Precision@5} = \frac{\text{Số file trả về có cùng loại nhạc cụ với Query}}{5}$$

### 1.2. Thang Đo Top-1 & Top-5 Hit Rate
* **Top-1 Hit Rate**: Tỷ lệ phần trăm các truy vấn mà file xếp hạng #1 có cùng nhạc cụ với Query.
* **Top-5 Hit Rate**: Tỷ lệ phần trăm các truy vấn mà có ít nhất 1 file trong Top 5 có cùng nhạc cụ với Query.

### 1.3. Thời Gian Phản Hồi Truy Vấn (Query Latency)
* Thời gian tính từ khi nạp file âm thanh, qua tiền xử lý, trích xuất đặc trưng, nhân ma trận tương đồng đến khi trả về danh sách Top 5 (Mục tiêu: $< 150\text{ ms}$ trên máy cá nhân).

---

## 2. Ưu Điểm Của Hệ Thống CBAR Đã Thiết Kế
1. **Tìm kiếm theo nội dung thực sự (True Content-Based Retrieval)**:
   * Không phụ thuộc vào metadata thủ công hay từ khóa văn bản. Tự động lắng nghe và phân tích sóng âm để tìm ra âm sắc tương đồng.
2. **Khả năng khái quát hóa với nhạc cụ mới (Zero-Shot / Unseen Instruments)**:
   * Khi người dùng tải lên tiếng đàn chưa từng có trong CSDL (như Đàn Bầu, Đàn Nhị, Shamisen), hệ thống vẫn hoạt động trơn tru và tìm ra các nhạc cụ có hành vi âm học tương đồng nhất.
3. **Tốc độ xử lý mili-giây**:
   * Nhờ rút gọn tín hiệu âm thanh thành vector 35 chiều và chuẩn hóa L2, toàn bộ 4,476 vector trong CSDL có thể được so khớp bằng một phép nhân ma trận đơn lẻ trong bộ nhớ RAM qua thư viện NumPy BLAS.
4. **Cơ sở khoa học vững chắc**:
   * Các đặc trưng được lựa chọn bám sát giáo trình chuẩn của PTIT và các công trình kinh điển về phân loại âm thanh (Wold et al., Scheirer & Slaney).

---

## 3. Các Yếu Tố Gây Sai Lệch Kết Quả (Failure Cases & Biases)

Trong thực tế nghiệm thu, kết quả tìm kiếm có thể bị sai lệch bởi các yếu tố sau:
1. **Sự khác biệt quá lớn về Kỹ thuật Diễn tấu (Playing Technique)**:
   * Cùng là cây Violin, nhưng tiếng kéo vĩ mượt mà (`arco-normal`) có âm sắc hoàn toàn khác tiếng gảy dây bật ngón (`pizz-normal`) hoặc tiếng gõ thân vĩ (`arco-col-legno-battuto`). Do đó, Query là Violin gảy dây có thể tìm ra Guitar hoặc Mandolin thay vì Violin kéo vĩ. *(Lưu ý: Về mặt âm học, điều này là hoàn toàn chính xác theo nguyên lý tương đồng âm sắc, dù nhãn nhạc cụ khác nhau!)*
2. **Cao độ quá chênh lệch (Pitch Disparity)**:
   * Một nốt nốt cực cao của Cello (ví dụ C6 $\approx 1046\text{ Hz}$) có thể có Spectral Centroid gần với một nốt trung của Violin (A4 $\approx 440\text{ Hz}$) hơn là một nốt cực trầm của chính Cello (C2 $\approx 65\text{ Hz}$).
3. **Mất cân bằng dữ liệu gốc (Class Imbalance)**:
   * Vì Violin chiếm tới 1,502 files (hơn $33\%$ tổng số file), xác suất ngẫu nhiên các file Violin lọt vào Top 5 sẽ cao hơn Banjo (chỉ có 74 files).
4. **File thu âm quá ngắn ($< 0.2\text{ giây}$)**:
   * Các file staccato/spiccato có quá ít khung thời gian để tính toán ổn định độ lệch chuẩn ($\sigma$) của các hệ số MFCC, dẫn đến vector đặc trưng có thể bị biến dạng.
5. **Dữ liệu bất thường trong tập gốc**:
   * File hỏng `viola_D6_05_piano_arco-normal.mp3` nếu không được lọc sẽ làm gián đoạn chương trình.
   * Các file bị trùng nội dung nhưng khác tên nhãn (như `cello_Cs6_1_mezzo-forte_arco-harmonic.mp3` và `violin_Ds5_phrase_forte_arco-spiccato.mp3`).

---

## 4. Hướng Cải Tiến & Mở Rộng Trong Tương Lai
1. **Lập chỉ mục không gian đa chiều (Multidimensional Indexing)**:
   * Hiện tại với 4,476 file, quét tuyến tính ma trận (Flat Matrix Scan) mất chưa tới 5ms. Tuy nhiên khi mở rộng CSDL lên hàng triệu file, cần tích hợp cấu trúc chỉ mục cây **k-d tree / R-tree** theo [Lecture 6](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%206%20-%20Multidimensional%20data%20structures.pdf) hoặc phân cụm **K-Means / Fuzzy c-Means** theo [Lecture 7](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf) (Slide 29-30: *Querying Clustered Vector Data*).
2. **Phản hồi mức độ phù hợp (Relevance Feedback)**:
   * Triển khai thuật toán **Rocchio query update** (Slide 10-13, Lecture 7) cho phép người dùng đánh dấu kết quả đúng/sai trong Top 5 để tinh chỉnh vector truy vấn cho lượt tìm kiếm kế tiếp.
3. **Mô hình học sâu (Deep Audio Embeddings)**:
   * Tích hợp các mạng nơ-ron tiền huấn luyện như VGGish hoặc CLAP (Contrastive Language-Audio Pretraining) để thu được vector nhúng có khả năng nắm bắt ngữ nghĩa âm nhạc sâu hơn.
