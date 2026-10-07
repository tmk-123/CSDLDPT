# 04. AUDIO FEATURE SPECIFICATION & ANALYSIS

Tài liệu này định nghĩa chi tiết hệ thống đặc trưng âm thanh được thiết kế cho bài toán CBAR (Content-Based Audio Retrieval) đối với nhạc cụ bộ dây, tuân thủ chặt chẽ kiến thức từ [Lecture 10 - Indexing and Retrieval for Audio](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf) và [Lecture 7 - Vector database and Clustering](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf).

---

## 1. Phân Loại Bộ Đặc Trưng: Tương Đồng vs Phân Biệt

Đề bài yêu cầu: *"Các bộ thuộc tính phải bao gồm các đặc trưng giúp tìm sự tương đồng và tìm sự khác biệt giữa các âm thanh nhạc cụ"*.

1. **Nhóm đặc trưng tìm sự TƯƠNG ĐỒNG (Similarity Features)**:
   * **Bản chất**: Những đặc trưng bất biến hoặc ít biến thiên theo cao độ nốt nhạc ($f_0$) và kỹ thuật diễn tấu, phản ánh bản sắc vật lý chung của bộ dây (tính điều hòa cao, tính liên tục của vĩ, cộng hưởng hộp gỗ).
   * **Đại diện**:
     * **MFCC bậc thấp (c1 - c4)**: Phản ánh dáng bao phổ vĩ mô (spectral envelope) và độ ấm của gỗ thùng đàn.
     * **Silence Ratio & RMS Dynamic Range**: Thể hiện hành vi suy giảm năng lượng tự nhiên của dây đàn.
     * **Harmonicity / Spectral Flatness**: Thể hiện tỷ lệ năng lượng sóng hài tập trung so với nhiễu.
2. **Nhóm đặc trưng tìm sự KHÁC BIỆT (Discriminative / Contrast Features)**:
   * **Bản chất**: Những đặc trưng phân tách rõ rệt giữa các kích thước đàn (Double Bass vs Violin) và phương thức kích thích (Plucked vs Bowed).
   * **Đại diện**:
     * **Spectral Centroid (Độ sáng của âm)**: Tách triệt để Violin ($>2,500\text{ Hz}$) khỏi Double Bass ($<800\text{ Hz}$).
     * **Zero Crossing Rate (ZCR)**: Tần suất cắt điểm 0 phân biệt các nốt cao với nốt trầm và phân biệt kỹ thuật gảy bật với kéo vĩ.
     * **Spectral Bandwidth & Spectral Rolloff**: Phân biệt âm thanh dải rộng giàu bồi âm kim loại (Banjo, Mandolin) với âm thanh ấm áp, cuộn tròn (Cello).
     * **MFCC bậc cao (c5 - c12)**: Bắt các cấu trúc vi mô chi tiết của formants riêng cho từng nhạc cụ.

---

## 2. Đặc Tả Từng Đặc Trưng Âm Thanh

### 2.1. Năng Lượng Trung Bình (Average Energy / RMS Energy)
* **Ý nghĩa**: Biểu thị cường độ năng lượng tức thời và độ to (loudness) của tín hiệu tại từng khung thời gian.
* **Công thức** (Trích Slide 10, 12 - Lecture 10):
  $$E = \frac{1}{N} \sum_{n=0}^{N-1} x(n)^2 \quad \text{hoặc} \quad RMS = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x(n)^2}$$
* **Đơn vị**: Không thứ nguyên (biên độ chuẩn hóa trong khoảng $[0.0, 1.0]$) hoặc decibel (dB).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 2 giá trị sau tổng hợp (Mean, Standard Deviation của toàn bộ các frame).
* **Ý nghĩa nhận diện**: Cho biết độ dốc suy giảm năng lượng (decay rate). Dây gảy (guitar, banjo) có RMS giảm dốc hàm mũ; dây kéo vĩ (violin, cello) có RMS ổn định trong suốt pha kéo.
* **Ý nghĩa similarity**: Giúp tìm các đoạn âm thanh có cùng mức độ kích thích và sắc thái (cùng forte hoặc piano).
* **Ưu điểm**: Tính toán $O(N)$ cực nhanh, trực quan.
* **Hạn chế**: Nhạy cảm với âm lượng thu âm nếu tín hiệu chưa được chuẩn hóa biên độ (peak-normalization).

---

### 2.2. Tỷ Lệ Cắt Điểm Không (Zero Crossing Rate - ZCR)
* **Ý nghĩa**: Số lần tín hiệu đổi dấu giữa hai mẫu liên tiếp, tương quan trực tiếp với tần số chi phối của tín hiệu.
* **Công thức** (Trích Slide 10, 12 - Lecture 10):
  $$ZCR = \frac{1}{2N} \sum_{n=1}^{N} \left| \operatorname{sgn}(x[n]) - \operatorname{sgn}(x[n-1]) \right|$$
  Trong đó: $\operatorname{sgn}(a) = 1$ nếu $a > 0$; $0$ nếu $a = 0$; $-1$ nếu $a < 0$.
* **Đơn vị**: Lần đổi dấu / frame (giá trị chuẩn hóa $\in [0.0, 1.0]$).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 2 giá trị sau tổng hợp (Mean, Standard Deviation).
* **Ý nghĩa nhận diện**: Phân biệt các nốt có tần số cơ bản cao (Violin có ZCR cao) với các nốt trầm (Double Bass, Cello có ZCR rất thấp). Phân biệt kỹ thuật gảy/gõ (col-legno có ZCR biến thiên mạnh) với âm thanh ngân đều.
* **Ý nghĩa similarity**: Lọc nhanh các file có cùng miền tần số trước khi tính toán các đặc trưng phức tạp.
* **Ưu điểm**: Chi phí tính toán cực rẻ, không cần biến đổi Fourier.
* **Hạn chế**: Dễ bị ảnh hưởng bởi nhiễu trắng ngẫu nhiên biên độ thấp (khắc phục bằng ngưỡng lọc silence).

---

### 2.3. Tỷ Lệ Khoảng Lặng (Silence Ratio)
* **Ý nghĩa**: Tỷ lệ phần trăm thời gian mà biên độ âm thanh nhỏ hơn ngưỡng mute threshold $A_{\text{thresh}}$ trên toàn bộ độ dài file.
* **Công thức** (Trích Slide 11, 12 - Lecture 10):
  $$\text{Silence Ratio} = \frac{T_{\text{silence}}}{T_{\text{total}}}$$
* **Đơn vị**: Tỷ lệ phần trăm / tỷ số $\in [0.0, 1.0]$.
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 1 giá trị vô hướng cho toàn bộ file.
* **Ý nghĩa nhận diện**: Các nốt ngắn (staccato, pizzicato, spiccato) trong dataset có silence ratio cao vì âm thanh tắt rất nhanh trước khi hết file thu âm; các nốt ngân dài (tenuto, legato) có silence ratio gần bằng 0.
* **Ý nghĩa similarity**: Nhận diện tương đồng về kỹ thuật phát âm (articulation).
* **Ưu điểm**: Phản ánh cấu trúc thời gian vĩ mô của file.
* **Hạn chế**: Không mang nhiều thông tin về âm sắc nếu chỉ đứng độc lập.

---

### 2.4. Trọng Tâm Phổ (Spectral Centroid - Brightness)
* **Ý nghĩa**: "Trọng tâm" phân bố năng lượng trên miền tần số. Trong thính giác của con người, Spectral Centroid tương ứng với cảm nhận về **"độ sáng" (Brightness)** hoặc "độ chói" của âm thanh.
* **Công thức** (Trích Slide 18 - Lecture 10):
  $$SC = \frac{\sum_{k=0}^{K-1} f_k \cdot |X[k]|}{\sum_{k=0}^{K-1} |X[k]|}$$
  Trong đó $|X[k]|$ là biên độ phổ Fourier tại tần số bin $f_k$.
* **Đơn vị**: Hertz (Hz).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 2 giá trị sau tổng hợp (Mean, Standard Deviation).
* **Ý nghĩa nhận diện**: Đây là đặc trưng **quan trọng số 1** để phân biệt kích thước các nhạc cụ họ vĩ cầm. Double Bass có phổ tập trung ở tần số thấp ($SC < 1,000\text{ Hz}$), Cello ($1,000 - 2,200\text{ Hz}$), Viola ($1,800 - 3,200\text{ Hz}$), Violin ($3,000 - 6,000+\text{ Hz}$). Banjo có $SC$ rất cao do màng da tạo nhiều họa âm bậc cao.
* **Ý nghĩa similarity**: Hai âm thanh có cùng $SC$ thường mang lại cảm giác âm sắc cùng độ trong trẻo / độ trầm ấm.
* **Ưu điểm**: Tương quan chặt chẽ với cảm nhận thính giác người.
* **Hạn chế**: Phụ thuộc vào cao độ nốt nhạc ($f_0$ cao thì $SC$ tự nhiên tăng theo).

---

### 2.5. Độ Rộng Dải Phổ (Spectral Bandwidth / Spread)
* **Ý nghĩa**: Độ lệch chuẩn của phổ tần số xung quanh trọng tâm phổ Spectral Centroid, biểu thị năng lượng lan tỏa rộng hay tập trung hẹp quanh đỉnh chính.
* **Công thức** (Dựa trên Slide 17, 18 - Lecture 10):
  $$SB = \sqrt{ \frac{\sum_{k=0}^{K-1} (f_k - SC)^2 \cdot |X[k]|}{\sum_{k=0}^{K-1} |X[k]|} }$$
* **Đơn vị**: Hertz (Hz).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 2 giá trị sau tổng hợp (Mean, Standard Deviation).
* **Ý nghĩa nhận diện**: Phân biệt âm sắc giàu bồi âm đa dải (Banjo, Guitar gảy mạnh, Violin kéo mạnh) với các âm có phổ thon gọn đơn giản (nốt trầm Cello, Double Bass).
* **Ý nghĩa similarity**: Đảm bảo âm thanh trả về có độ phong phú sóng hài tương đương bản ghi gốc.

---

### 2.6. Tần Số Cuộn Phổ (Spectral Rolloff - 85%)
* **Ý nghĩa**: Tần số mà bên dưới nó tập trung $85\%$ (hoặc ngưỡng $\gamma = 0.85$) tổng năng lượng của phổ tín hiệu.
* **Công thức**:
  $$\sum_{k=0}^{k_{\text{rolloff}}} |X[k]| = \gamma \sum_{k=0}^{K-1} |X[k]| \quad \Longrightarrow \quad \text{Rolloff} = f_{k_{\text{rolloff}}}$$
* **Đơn vị**: Hertz (Hz).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: 2 giá trị sau tổng hợp (Mean, Standard Deviation).
* **Ý nghĩa nhận diện & similarity**: Đo lường sự hiện diện của năng lượng tần số cao; giúp nhận diện các nhạc cụ có bồi âm mở rộng lên tới cận trên thính giác.

---

### 2.7. Hệ Số Tần Số Mel (Mel-Frequency Cepstral Coefficients - MFCC)
* **Ý nghĩa**: Chuẩn công nghiệp để mô tả **âm sắc (Timbre descriptor)** cho Content-Based Audio Retrieval (Trích Slide 18 - Lecture 10: *"MFCC: standard timbre descriptor for CBAR"*).
* **Quy trình tính toán** (Trích Slide 18 - Lecture 10):
  $$\text{STFT} \longrightarrow \text{Mel filter bank} \longrightarrow \log(\cdot) \longrightarrow \text{DCT} \longrightarrow 13\text{ hệ số MFCC per frame}$$
* **Chi tiết kỹ thuật**:
  * $13$ hệ số (MFCC 0 đến MFCC 12). Hệ số 0 biểu thị năng lượng tổng thể, các hệ số 1-12 biểu thị hình bao phổ chi tiết độc lập với chu kỳ cơ bản $f_0$.
* **Đơn vị**: Không thứ nguyên (cepstral coefficients).
* **Kiểu dữ liệu**: `float32`.
* **Kích thước vector**: $13 \times 2 = 26$ giá trị sau tổng hợp (Mean và Standard Deviation cho từng hệ số).
* **Ý nghĩa nhận diện**: Tách rời âm sắc của đàn ra khỏi cao độ nốt nhạc. Cho phép nhận diện một cây violin dù nó đang chơi nốt C4 hay nốt A5.
* **Ý nghĩa similarity**: Đây là cốt lõi để tính khoảng cách Cosine hoặc Euclidean cho bài toán tìm kiếm tương đồng.
* **Ưu điểm**: Bắt chước trực tiếp hệ thống thính giác con người (thang đo Mel phi tuyến), giảm chiều dữ liệu từ phổ hàng ngàn bin xuống còn 13 hệ số cô đọng.

---

## 3. Tổng Hợp Kích Thước Vector Đặc Trưng Cuối Cùng (Global Feature Vector)

Để biểu diễn một file âm thanh bất kỳ thành **một vector có kích thước cố định** độc lập với độ dài bản ghi (phù hợp với Vector Space Model trong [Lecture 7](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf)), ta tính giá trị thống kê (Mean và Standard Deviation) trên toàn bộ các khung (frames):

| STT | Tên đặc trưng | Thành phần thống kê | Số chiều (Dimensions) |
| :---: | :--- | :--- | :---: |
| 1 | **RMS Energy** | Mean, Std | 2 |
| 2 | **Zero Crossing Rate (ZCR)** | Mean, Std | 2 |
| 3 | **Silence Ratio** | Scalar | 1 |
| 4 | **Spectral Centroid** | Mean, Std | 2 |
| 5 | **Spectral Bandwidth** | Mean, Std | 2 |
| 6 | **Spectral Rolloff** | Mean, Std | 2 |
| 7 | **MFCC (13 coefficients)** | 13 Mean, 13 Std | 26 |
| **TỔNG** | **Toàn bộ Feature Vector** | - | **35 chiều (35-D Vector)** |

Vector 35 chiều này là đại diện hoàn hảo: vừa đủ nhỏ gọn để tính toán ma trận tương đồng cực nhanh trên hàng ngàn bản ghi, vừa đủ thông tin đa chiều để phân biệt chính xác 7 họ nhạc cụ dây.
