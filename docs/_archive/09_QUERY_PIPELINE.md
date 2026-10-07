# 09. QUERY PROCESSING PIPELINE & WORKFLOW

Tài liệu này mô tả chi tiết hai luồng xử lý chính của hệ thống CBAR: **Quy trình lập chỉ mục ngoại tuyến (Offline Indexing Pipeline)** và **Quy trình xử lý truy vấn trực tuyến (Online Query Pipeline)** theo lý thuyết [Lecture 10 - Indexing and Retrieval for Audio](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf) (Slide 6).

---

## 1. Quy Trình Lập Chỉ Mục Ngoại Tuyến (Offline Indexing Pipeline)
Đây là quy trình chạy một lần để xây dựng toàn bộ kho CSDL đặc trưng cho 4,477 files trong dataset:

```
[4,477 Audio Files] 
       │
       ▼
[1. Quét tệp tin & Đọc Metadata] (ffprobe lấy duration, size, sr, channels)
       │
       ▼
[2. Lọc bỏ file lỗi] (Bỏ qua file corrupt như viola_D6_05_piano_arco-normal.mp3)
       │
       ▼
[3. Giải mã & Tiền xử lý] (PCM Mono, cắt khoảng lặng, chuẩn hóa biên độ)
       │
       ▼
[4. Trích xuất đặc trưng 35-D] (Tính RMS, ZCR, Centroid, Bandwidth, Rolloff, MFCCs)
       │
       ▼
[5. Tính tham số chuẩn hóa toàn cục] (Lưu vector kỳ vọng μ ∈ R^35 và độ lệch chuẩn σ ∈ R^35)
       │
       ▼
[6. Chuẩn hóa & Lưu trữ vào CSDL] (Lưu bảng audio_files, audio_features, feature_vectors)
       │
       ▼
[7. Xây dựng Ma trận Vector CSDL] (Lưu file vector cache V_norm phục vụ tìm kiếm mili-giây)
```

---

## 2. Quy Trình Xử Lý Truy Vấn Trực Tuyến (Online Query Pipeline)
Khi người dùng đưa vào một file âm thanh mới bất kỳ (qua Giao diện Web hoặc CLI):

```
       [User Submits Audio File]
                  │
                  ▼
   [Bước 1: Tiếp Nhận & Xác Thực]
   - Kiểm tra định dạng (.mp3, .wav, .ogg, .flac).
   - Kiểm tra dung lượng hợp lệ (> 1KB, < 50MB).
                  │
                  ▼
   [Bước 2: Giải Mã Âm Thanh (Audio Decoding)]
   - Dùng FFmpeg giải mã trực tiếp thành mảng float32 Linear PCM.
   - Resample về 44,100 Hz và chuyển thành Mono nếu file gốc là Stereo.
                  │
                  ▼
   [Bước 3: Tiền Xử Lý Âm Học]
   - Cắt bỏ khoảng lặng đầu/đuôi (ngưỡng -45 dBFS).
   - Chuẩn hóa biên độ tín hiệu (Peak Normalization).
                  │
                  ▼
   [Bước 4: Trích Xuất Đặc Trưng Tức Thời]
   - Phân khung 2048 mẫu, bước nhảy 512 mẫu, cửa sổ Hann.
   - Tính toán phổ STFT.
   - Trích xuất RMS, ZCR, Silence Ratio, Spectral Centroid, Bandwidth, Rolloff, 13 MFCCs.
   - Tính Mean và Std để tạo vector thô q_raw ∈ R^35.
                  │
                  ▼
   [Bước 5: Chuẩn Hóa Vector Truy Vấn]
   - Z-Score chuẩn hóa theo bộ tham số (μ, σ) của CSDL:
         q_zscore = (q_raw - μ) / σ
   - Chuẩn hóa độ dài đơn vị L2:
         q_norm = q_zscore / ||q_zscore||_2
                  │
                  ▼
   [Bước 6: Tính Toán Độ Tương Đồng (Vector Similarity)]
   - Tính tích vô hướng ma trận với toàn bộ kho dữ liệu:
         scores = np.dot(V_norm, q_norm)
   - Hoặc tính khoảng cách Euclid tương ứng.
                  │
                  ▼
   [Bước 7: Sắp Xếp & Chọn Top-5 (Ranking)]
   - Lấy 5 chỉ số có điểm số Similarity cao nhất:
         top_5_idx = np.argsort(scores)[::-1][:5]
                  │
                  ▼
   [Bước 8: Truy Vấn Metadata & Đóng Gói Phản Hồi]
   - Truy vấn CSDL SQLite lấy: Tên file, Nhạc cụ, Nốt nhạc, Kỹ thuật, Cường độ, Đường dẫn.
   - Tính toán các giá trị trung gian (Spectrogram, biểu đồ đặc trưng so sánh).
                  │
                  ▼
   [Bước 9: Trả Về & Trình Diễn Trên Giao Diện]
   - Hiển thị danh sách Top 5 xếp theo thứ tự giảm dần độ tương đồng.
   - Cung cấp trình phát âm thanh (Audio Player) để nghe thử file truy vấn và 5 file kết quả.
```

---

## 3. Xử Lý Các Trường Hợp Ngoại Lệ (Edge Cases)
1. **File âm thanh hoàn toàn im lặng (Pure Silence)**:
   * Tín hiệu có biên độ xấp xỉ 0 trên toàn bộ thời lượng.
   * *Xử lý*: Module tiền xử lý phát hiện năng lượng cực tiểu ($RMS < 10^{-6}$), lập tức dừng pipeline và thông báo cho người dùng: *"File âm thanh không có tín hiệu nhạc cụ hợp lệ"*.
2. **File âm thanh quá ngắn ($< 0.1\text{ giây}$)**:
   * Không đủ mẫu để chia khung STFT tối thiểu.
   * *Xử lý*: Áp dụng cơ chế đệm không (Zero-padding) lên tối thiểu 2048 mẫu để tính toán FFT hoặc cảnh báo người dùng.
3. **File âm thanh của nhạc cụ chưa từng có trong CSDL (Unseen Instrument)**:
   * *Xử lý*: Không có lỗi xảy ra! Hệ thống trích xuất vector âm học bình thường và trả về 5 file có âm sắc gần gũi nhất trong kho dữ liệu dây.
