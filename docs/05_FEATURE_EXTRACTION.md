# 05. FEATURE EXTRACTION PIPELINE

Tài liệu này mô tả chi tiết quy trình trích xuất đặc trưng âm thanh theo chuẩn CBAR được trình bày trong [Lecture 10 - Indexing and Retrieval for Audio](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf) (Slide 8: *Audio Feature Extraction Pipeline*), áp dụng trực tiếp cho kho dữ liệu MP3 của đề tài.

---

## 1. Sơ Đồ Quy Trình Trích Rút Đặc Trưng

```
   [Audio File (.mp3)]
           │
           ▼
   [1. Audio Decoding & Loading]  (FFmpeg giải mã ra Mono PCM float32, SR = 44,100 Hz)
           │
           ▼
   [2. Preprocessing]             (Cắt bỏ khoảng lặng đầu/cuối, Peak/RMS Normalization)
           │
           ▼
   [3. Framing & Windowing]       (Frame: 2048 mẫu ~46.4ms, Hop: 512 mẫu ~11.6ms, Hann Window)
           │
           ├───────────────────────────────┬───────────────────────────────┐
           ▼                               ▼                               ▼
 [4a. Time-Domain Analysis]      [4b. FFT / STFT Analysis]       [4c. Mel Filterbank & DCT]
  - RMS Energy per frame          - Spectrum |X[k]| per frame     - 13 Mel filterbanks
  - ZCR per frame                 - Spectral Centroid             - Log power & DCT
  - Global Silence Ratio          - Spectral Bandwidth            - 13 MFCCs per frame
           │                      - Spectral Rolloff (85%)                 │
           └───────────────────────────────┼───────────────────────────────┘
                                           │
                                           ▼
                                 [5. Temporal Aggregation]
                                 (Tính Mean và Standard Deviation trên toàn bộ frames)
                                           │
                                           ▼
                                [6. Raw Feature Vector] (35-D)
                                           │
                                           ▼
                            [7. Normalization / Standardization]
                            (Z-Score Standardization: (x - μ) / σ)
                                           │
                                           ▼
                               [8. Store in Database]
                            (Lưu vào bảng AudioFeatures & Vector Index)
```

---

## 2. Chi Tiết Từng Giai Đoạn Trong Pipeline

### Giai đoạn 1: Giải Mã và Nạp Âm Thanh (Audio Decoding)
* **Đầu vào**: File nén `.mp3` từ thư mục `Strings/`.
* **Thao tác**: Dùng `ffmpeg` giải mã luồng bit MP3 thành mảng tín hiệu số thô dạng số thực (Linear PCM float32, phạm vi $[-1.0, 1.0]$).
* **Sample Rate**: Giữ nguyên $44,100\text{ Hz}$ chuẩn của dataset để bảo toàn đầy đủ các bồi âm tần số cao (lên tới $22,050\text{ Hz}$ theo định lý Nyquist).
* **Kênh**: Chuyển đổi thành Mono (kênh đơn). Toàn bộ 4,477 files trong dataset vốn đã là Mono.

### Giai đoạn 2: Tiền Xử Lý Tín Hiệu (Preprocessing)
1. **Cắt khoảng lặng dư thừa (Silence Trimming)**:
   * Nhiều file có đoạn im lặng $0.2 - 0.5\text{ giây}$ ở đầu hoặc đuôi khi phòng thu chưa bấm dừng.
   * Dùng thuật toán quét ngưỡng năng lượng biên độ (ví dụ: ngưỡng $-45\text{ dBFS}$) để cắt gọn chỉ giữ lại phần có âm thanh nhạc cụ thực sự.
2. **Chuẩn hóa biên độ (Peak / Loudness Normalization)**:
   * Nhân toàn bộ mảng mẫu âm thanh với hệ số $\frac{0.95}{\max(|x|)}$ để loại bỏ sự sai lệch âm lượng giữa các file thu âm khác nhau, tránh việc một file chơi nốt nhẹ bị nhầm là nhạc cụ khác chỉ vì âm lượng nhỏ.

### Giai đoạn 3: Phân Khung và Đặt Cửa Sổ (Framing & Windowing)
* Tín hiệu âm thanh là tín hiệu phi dừng (non-stationary), nhưng trong các khoảng thời gian rất ngắn ($20 - 50\text{ ms}$) nó có thể coi là dừng cục bộ (quasi-stationary).
* **Kích thước khung (Frame length $N$)**: $2,048$ mẫu (tương đương $\approx 46.4\text{ ms}$ tại $f_s = 44,100\text{ Hz}$). Kích thước này đủ dài để đạt độ phân giải tần số mịn $\Delta f = \frac{44,100}{2,048} \approx 21.5\text{ Hz}$, rất quan trọng để tách rõ các bồi âm trầm của Cello và Double Bass (theo slide 15 - Lecture 10).
* **Bước nhảy (Hop size $H$)**: $512$ mẫu ($\approx 11.6\text{ ms}$, chồng lấn $75\%$) giúp chuyển tiếp mượt mà giữa các khung.
* **Hàm cửa sổ (Window Function)**: Sử dụng cửa sổ **Hann (Hanning)**:
  $$w[n] = 0.5 - 0.5 \cos\left(\frac{2\pi n}{N-1}\right)$$
  nhằm giảm thiểu hiện tượng rò rỉ phổ (spectral leakage) ở hai biên của mỗi khung (Slide 15 - Lecture 10).

### Giai đoạn 4: Trích Xuất Đặc Trưng Trên Từng Khung (Per-Frame Extraction)
* **Miền thời gian**: Tính toán $E_{\text{frame}}$ và $ZCR_{\text{frame}}$.
* **Biến đổi Fourier nhanh (STFT)**: Áp dụng FFT cho từng khung để thu được phổ biên độ $|X[k]|$.
* **Miền tần số**: Từ $|X[k]|$, tính toán Spectral Centroid, Bandwidth, và Rolloff.
* **Tính MFCC**:
  1. Chiếu phổ năng lượng $|X[k]|^2$ qua ngân hàng $40$ bộ lọc tam giác cách đều theo thang đo Mel (Mel Filterbank từ $20\text{ Hz}$ đến $f_s/2$).
  2. Lấy logarithm tự nhiên của năng lượng trên từng dải Mel.
  3. Áp dụng biến đổi Cosine rời rạc loại 2 (DCT-II) để giải tương quan năng lượng, giữ lại $13$ hệ số đầu tiên ($c_0$ đến $c_{12}$).

### Giai đoạn 5: Tổng Hợp Thống Kê (Temporal Aggregation)
* Một file có $M$ khung thời gian ($M$ phụ thuộc vào độ dài file).
* Để đưa về vector kích thước cố định cho Vector Space Model ([Lecture 7](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf)), ta tính hai đại lượng thống kê cơ bản trên toàn bộ $M$ khung:
  $$\mu_f = \frac{1}{M}\sum_{m=1}^M f[m], \quad \sigma_f = \sqrt{\frac{1}{M}\sum_{m=1}^M (f[m] - \mu_f)^2}$$
* Kết quả: Thu được vector thô kích thước 35 chiều (Raw 35-D Feature Vector).

### Giai đoạn 6: Chuẩn Hóa Vector (Vector Standardization)
* Do các đặc trưng có thang đo rất khác nhau (ví dụ: Spectral Centroid tính bằng ngàn Hz, trong khi ZCR chỉ từ $0.0$ đến $0.5$), nếu không chuẩn hóa, đặc trưng Centroid sẽ áp đảo toàn bộ khoảng cách Euclid / Cosine.
* Phương pháp: Áp dụng chuẩn hóa **Z-Score Standardization**:
  $$z_i = \frac{x_i - \mu_i}{\sigma_i}$$
  trong đó $\mu_i, \sigma_i$ là kỳ vọng và độ lệch chuẩn của chiều thứ $i$ trên toàn bộ tập dữ liệu CSDL.
* Hoặc chuẩn hóa vector đơn vị ($L_2\text{-norm}$): $\hat{v} = \frac{v}{\|v\|_2}$ để phục vụ tính Cosine Similarity bằng tích vô hướng (Slide 7 - Lecture 7).
