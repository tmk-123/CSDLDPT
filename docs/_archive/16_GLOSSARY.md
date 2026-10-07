# 16. GLOSSARY (THUẬT NGỮ CHUYÊN NGÀNH HỆ CSDL ĐA PHƯƠNG TIỆN)

Tài liệu này giải thích chi tiết các thuật ngữ kỹ thuật âm thanh, cơ sở dữ liệu và xử lý tín hiệu đa phương tiện được sử dụng trong đồ án, bám sát các bài giảng môn Hệ CSDL Đa phương tiện (MMDB - PTIT).

---

### 1. Thuật Ngữ Âm Thanh & Xử Lý Tín Hiệu (Audio & DSP)
* **Audio Feature (Đặc trưng âm thanh)**: Các thuộc tính định lượng được trích xuất từ tín hiệu âm thanh thô, phản ánh các khía cạnh vật lý hoặc thính giác cụ thể (như năng lượng, tần số, âm sắc).
* **Timbre (Âm sắc)**: "Màu sắc" của âm thanh, là thuộc tính giúp tai người phân biệt được hai nhạc cụ khác nhau (ví dụ: tiếng Violin và tiếng Guitar) ngay cả khi chúng đang chơi cùng một nốt nhạc ($f_0$) và cùng một âm lượng.
* **Fundamental Frequency ($f_0$ - Tần số cơ bản)**: Tần số dao động tự nhiên thấp nhất của dây đàn, quyết định cao độ (Pitch) của nốt nhạc mà người nghe cảm nhận được.
* **Harmonics / Overtones (Sóng hài / Bồi âm)**: Các thành phần tần số dao động là bội số nguyên của tần số cơ bản ($2f_0, 3f_0, 4f_0, \dots$). Tỷ lệ biên độ giữa các sóng hài định hình nên âm sắc độc nhất của nhạc cụ.
* **FFT (Fast Fourier Transform - Biến đổi Fourier nhanh)**: Thuật toán chuyển đổi tín hiệu từ miền thời gian (biên độ theo thời gian) sang miền tần số (biên độ phổ theo tần số).
* **STFT (Short-Time Fourier Transform - Biến đổi Fourier thời gian ngắn)**: Phương pháp chia tín hiệu âm thanh dài thành nhiều khung ngắn chồng lấn nhau và áp dụng FFT trên từng khung, tạo ra biểu diễn thời gian - tần số.
* **Spectrogram (Phổ đồ)**: Đồ thị 2D trực quan hóa STFT, trong đó trục hoành là thời gian, trục tung là tần số, và cường độ màu sắc biểu thị năng lượng của âm thanh tại tần số đó.
* **RMS Energy (Root Mean Square Energy - Năng lượng hiệu dụng)**: Đại lượng đo lường độ to và cường độ năng lượng trung bình của tín hiệu trong một khung thời gian.
* **ZCR (Zero Crossing Rate - Tỷ lệ cắt điểm không)**: Tần suất tín hiệu đổi dấu từ dương sang âm hoặc ngược lại trong một khung thời gian, tương quan với tần số chiếm ưu thế của âm thanh.
* **Spectral Centroid (Trọng tâm phổ)**: Giá trị tần số trung bình có trọng số bởi biên độ phổ, đại diện cho "độ sáng" (Brightness) của âm sắc.
* **Spectral Bandwidth (Độ rộng dải phổ)**: Thước đo mức độ lan tỏa của năng lượng xung quanh trọng tâm phổ Spectral Centroid.
* **Spectral Rolloff (Tần số cuộn phổ)**: Ngưỡng tần số mà bên dưới nó chứa một tỷ lệ năng lượng nhất định (thường là $85\%$).
* **MFCC (Mel-Frequency Cepstral Coefficients - Các hệ số Cepstrum tần số Mel)**: Bộ đặc trưng tiêu chuẩn công nghiệp đại diện cho âm sắc (Timbre descriptor), được tính toán bằng cách lọc phổ qua ngân hàng bộ lọc Mel (mô phỏng thính giác người) và biến đổi DCT.
* **Single Note / Node đơn (Nốt nhạc đơn lẻ)**: Bản ghi âm ghi lại âm thanh của một nốt nhạc duy nhất được diễn tấu độc lập (isolated note), không bị lẫn tạp âm từ các nhạc cụ khác hay hợp âm phức hợp.

---

### 2. Thuật Ngữ CSDL & Tìm Kiếm Tương Đồng (Database & IR)
* **CBAR (Content-Based Audio Retrieval - Tìm kiếm âm thanh dựa trên nội dung)**: Hệ thống tìm kiếm âm thanh dựa trên chính các đặc trưng nội dung tín hiệu âm học (sóng âm, âm sắc), không dựa vào từ khóa gán nhãn thủ công.
* **Query-by-Example (QBE - Truy vấn bằng mẫu)**: Mô hình tìm kiếm trong đó người dùng cung cấp một file đa phương tiện mẫu (file âm thanh) làm đầu vào truy vấn thay vì gõ văn bản.
* **Feature Vector (Vector đặc trưng)**: Một mảng số thực $N$ chiều $v = (v_1, v_2, \dots, v_N)$ tổng hợp toàn bộ các đặc tính đo được của một file âm thanh, biểu diễn file đó thành một điểm trong không gian $N$ chiều.
* **Vector Space Model (Mô hình không gian vector)**: Mô hình toán học biểu diễn cả tài liệu CSDL và truy vấn dưới dạng các vector trong cùng một không gian thuộc tính đa chiều để tính toán khoảng cách.
* **Cosine Similarity (Độ tương đồng Cosine)**: Thước đo góc giữa hai vector trong không gian đa chiều, nhận giá trị từ $[-1, 1]$, độc lập với độ dài tuyệt đối của vector.
* **Euclidean Distance (Khoảng cách Euclid / $L_2$-norm)**: Khoảng cách hình học đường thẳng giữa hai điểm trong không gian Euclid.
* **Z-Score Normalization (Chuẩn hóa điểm Z)**: Phép biến đổi đưa từng chiều đặc trưng về phân phối có kỳ vọng $\mu = 0$ và độ lệch chuẩn $\sigma = 1$, giúp các đặc trưng khác biệt về đơn vị có tầm ảnh hưởng công bằng.
* **Top-K Retrieval / Ranking**: Quá trình sắp xếp toàn bộ các bản ghi trong CSDL theo mức độ tương đồng giảm dần và trích xuất $K$ kết quả đứng đầu ($K = 5$).
* **K-Nearest Neighbors (k-NN)**: Thuật toán tìm kiếm $k$ điểm lân cận gần nhất với điểm truy vấn trong không gian đặc trưng.
* **Semantic Gap (Khoảng cách ngữ nghĩa)**: Sự khác biệt giữa các đặc trưng mức thấp mà máy tính tính toán được (pixel, bin tần số, MFCC) và khái niệm ngữ nghĩa mức cao mà con người cảm nhận (bản nhạc buồn, tiếng vĩ cầm tha thiết).
* **Panofsky's Three Levels of Expression**: Mô hình 3 cấp độ biểu đạt của dữ liệu đa phương tiện: (1) Cấp độ mô tả (Description) - dữ liệu cảm nhận trực quan thô; (2) Cấp độ nhận diện (Identification) - tên đối tượng, nhãn phân loại; (3) Cấp độ diễn giải (Interpretation) - ý nghĩa văn hóa, nghệ thuật sâu xa.
* **Hybrid Storage Principle (Nguyên lý lưu trữ hỗn hợp)**: Nguyên tắc kiến trúc CSDL đa phương tiện kết hợp giữa lưu trữ tập trung có cấu trúc (RDBMS) cho Metadata/Features và hệ thống tệp chuyên biệt (File Server/Blob Store) cho các file nhị phân lớn.
* **Multidimensional Indexing (Chỉ mục đa chiều)**: Các cấu trúc dữ liệu cây (như k-d tree, R-tree, Quadtree) giúp tăng tốc độ tìm kiếm lân cận k-NN trong không gian vector nhiều chiều thay vì phải quét tuyến tính toàn bộ CSDL.
