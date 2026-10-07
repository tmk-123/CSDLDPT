# 01. REQUIREMENTS ANALYSIS & TRACEABILITY MATRIX

## 1. Yêu Cầu Đề Tài Chi Tiết
Đề tài đặt ra 5 yêu cầu chính từ giảng viên (được lưu trữ tại [yeu_cau.txt](file:///D:/Ki1_4/HCSDLDPT/BTL/yeu_cau.txt)):

1. **Yêu cầu 1: Dataset ($\ge 500$ files)**:
   * Xây dựng/sưu tầm bộ dữ liệu âm thanh gồm ít nhất 500 files âm thanh của các nhạc cụ khác nhau thuộc bộ dây.
   * Mỗi file chỉ gồm tiếng của một nhạc cụ (đơn âm sắc/isolated instrument).
   * Độ dài file phù hợp để chứa đựng đủ các đặc tính cần thiết để nhận diện tiếng nhạc cụ.
   * Sinh viên tùy chọn định dạng file âm thanh.
   * Mô tả các đặc điểm giống và khác nhau của tiếng các nhạc cụ trong các file trong bộ dữ liệu.
2. **Yêu cầu 2: Bộ đặc trưng âm thanh**:
   * Xây dựng một hoặc vài bộ đặc trưng để nhận diện âm thanh các nhạc cụ từ bộ dữ liệu đã thu thập.
   * Các đặc trưng phải bao gồm nhóm tìm sự tương đồng (similarity) và nhóm tìm sự khác biệt (distinction/discrimination).
   * Trình bày rõ từng đặc trưng và giải thích giá trị thông tin của từng đặc trưng.
3. **Yêu cầu 3: Thuật toán trích rút & Hệ CSDL**:
   * Triển khai thuật toán/công cụ trích rút các đặc trưng đã xác định.
   * Xây dựng hệ CSDL để quản trị các đặc trưng âm thanh cho toàn bộ dataset.
4. **Yêu cầu 4: Hệ thống tìm kiếm tương đồng**:
   * Đầu vào: một file âm thanh mới về một nhạc cụ thuộc bộ dây (nhạc cụ có thể đã có hoặc chưa từng có trong tập dữ liệu).
   * Đầu ra: 5 file âm thanh giống nhất, xếp thứ tự giảm dần theo độ tương đồng nội dung với âm thanh đầu vào.
   * **4a**: Sơ đồ khối hệ thống, chức năng từng block, I/O từng block, quy trình xử lý truy vấn.
   * **4b**: Minh họa kết quả trung gian (giá trị đặc trưng, các bước tính độ tương đồng, ranking).
   * **4c**: Đánh giá kết quả đạt được, ưu điểm, hạn chế, yếu tố gây sai lệch, hướng cải tiến.
5. **Yêu cầu 5: Demo hệ thống**:
   * Chương trình chạy demo thực tế từ file đầu vào đến kết quả trả về.

---

## 2. Bảng Traceability Matrix (Đối Chiếu Yêu Cầu - Hiện Trạng)

| Mã YC | Nội dung yêu cầu | Hiện trạng mã nguồn & dữ liệu | Đã đạt chưa? | Những thành phần còn thiếu / Cần triển khai |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-1.1** | Kho dữ liệu $\ge 500$ file bộ dây | Thư mục `Strings/` có 4,477 files MP3 của 7 nhạc cụ. | **ĐẠT** (Vượt số lượng) | Dữ liệu mất cân bằng giữa các class; cần lọc file hỏng/trùng. |
| **REQ-1.2** | Mỗi file 1 nhạc cụ, độ dài phù hợp | File ghi âm nốt đơn (`single note`), thời lượng 0.08s - 29.54s (trung bình 1.81s). | **ĐẠT** | Một số file quá ngắn (<0.2s) cần kiểm tra độ tin cậy của FFT/STFT. |
| **REQ-1.3** | Mô tả so sánh đặc tính các nhạc cụ | Chưa có tài liệu phân tích âm học hệ thống trong code gốc. | **CHƯA ĐẠT** | Cần tài liệu hóa tại [docs/03_AUDIO_CHARACTERISTICS.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/03_AUDIO_CHARACTERISTICS.md). |
| **REQ-2.1** | Xây dựng bộ đặc trưng âm thanh | `scan_dataset.py` chỉ mới đọc metadata (duration, sample_rate, channels). Chưa trích xuất đặc trưng nội dung. | **CHƯA ĐẠT** | Cần thiết kế và code bộ trích rút MFCC, Spectral Centroid, Bandwidth, ZCR, RMS. |
| **REQ-2.2** | Giải thích giá trị thông tin từng đặc trưng | Chưa có tài liệu giải thích cơ sở toán học và âm học. | **CHƯA ĐẠT** | Cần tài liệu hóa tại [docs/04_FEATURES.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/04_FEATURES.md) bám sát Lecture 10. |
| **REQ-3.1** | Triển khai thuật toán trích rút đặc trưng | Chưa có module trích rút feature. Môi trường có NumPy, SciPy (có thể viết DSP chuẩn). | **CHƯA ĐẠT** | Cần xây dựng pipeline trích xuất feature (Framing -> Windowing -> STFT -> Feature Extraction). |
| **REQ-3.2** | Xây dựng hệ CSDL quản trị đặc trưng | Chưa có database file nào (chưa có SQLite/Postgres DB). Mới có `metadata_strings.csv` trong script nhưng chưa chạy. | **CHƯA ĐẠT** | Cần thiết kế ERD, triển khai schema SQLite / SQLAlchemy để lưu metadata và vector đặc trưng. |
| **REQ-4.1** | Xử lý input nhạc cụ đã có và chưa có | Chưa có engine tìm kiếm. | **CHƯA ĐẠT** | Thiết kế search engine hoàn toàn dựa trên Feature Vector (không filter cứng theo label) để đáp ứng cả nhạc cụ mới. |
| **REQ-4.2** | Đầu ra 5 file giống nhất (Ranking Top-5) | Chưa triển khai. | **CHƯA ĐẠT** | Cần triển khai Cosine Similarity / Euclidean Distance và K-NN ranking. |
| **REQ-4a** | Sơ đồ khối, chức năng, I/O từng module | Chưa có tài liệu kiến trúc. | **CHƯA ĐẠT** | Cần tài liệu hóa tại [docs/08_SYSTEM_ARCHITECTURE.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/08_SYSTEM_ARCHITECTURE.md). |
| **REQ-4b** | Minh họa kết quả trung gian | Chưa có công cụ xem kết quả trung gian. | **CHƯA ĐẠT** | Cần tài liệu hóa tại [docs/10_INTERMEDIATE_RESULTS.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/10_INTERMEDIATE_RESULTS.md) và thiết kế API/CLI trực quan. |
| **REQ-4c** | Đánh giá kết quả, hạn chế, hướng đi | Chưa có bộ đánh giá định lượng. | **CHƯA ĐẠT** | Cần tài liệu hóa tại [docs/11_EVALUATION.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/11_EVALUATION.md) (Precision@5, Mean Average Precision). |
| **REQ-5.0** | Demo hệ thống | Chưa có code demo hoàn chỉnh. | **CHƯA ĐẠT** | Cần tài liệu kịch bản demo tại [docs/12_DEMO.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/12_DEMO.md) và triển khai sau khi phê duyệt. |

---

## 3. Kết Luận Đánh Giá Yêu Cầu
* Điểm mạnh lớn nhất hiện tại: Đã có sẵn bộ dataset rất phong phú (4,477 files, 7 họ nhạc cụ dây) với quy chuẩn đặt tên chi tiết.
* Khâu đang trống hoàn toàn: **Module trích xuất đặc trưng (Feature Extraction)**, **Cơ sở dữ liệu (Database)**, **Engine tính toán độ tương đồng (Similarity Search Engine)** và **Giao diện Demo**.
* Toàn bộ các yêu cầu này hoàn toàn khả thi để thực hiện đúng tiến độ bằng cách bám sát kiến thức từ bài giảng MMDB.
