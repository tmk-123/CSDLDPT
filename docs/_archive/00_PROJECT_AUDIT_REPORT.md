# PROJECT AUDIT REPORT

**Báo cáo Kiểm tra Toàn diện Đề tài: "Xây dựng hệ CSDL lưu trữ và tìm kiếm tiếng nhạc cụ bộ dây"**  
*Môn học: Hệ Cơ sở Dữ liệu Đa phương tiện (MMDB) - PTIT*  
*Ngày thực hiện audit: 07/10/2026*  
*Người thực hiện: Trợ lý AI Antigravity*  
*Nguyên tắc kiểm toán: Coi codebase và dữ liệu thực tế là nguồn sự thật duy nhất (Single Source of Truth), không suy đoán, không bịa đặt.*

---

## 1. Tôi Đã Đọc Những Gì?

1. **Slide bài giảng môn học (Thư mục `MMDB slides/`)**:
   * [Lecture 10 - Indexing and Retrieval for Audio.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf): Khung CBAR (Content-Based Audio Retrieval), quy trình trích xuất đặc trưng âm thanh (Framing, STFT, MFCC 13 chiều, Spectral Centroid, Bandwidth, ZCR, RMS, Silence Ratio).
   * [Lecture 7 - Vector database and Clustering.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf): Mô hình không gian vector (Vector Space Model), Cosine Similarity, khoảng cách Euclid ($L_2$), Manhattan ($L_1$), k-NN search, phân cụm K-Means/FCM và thuật toán phản hồi Rocchio.
   * [Lecture 6 - Multidimensional data structures.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%206%20-%20Multidimensional%20data%20structures.pdf): Cấu trúc chỉ mục đa chiều k-d tree, Quadtree, R-tree phục vụ tìm kiếm k-NN trong không gian đa chiều.
   * [Lecture 5 - MM data model.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%205%20-%20MM%20data%20model.pdf): Các mô hình CSDL đa phương tiện (Relational, Object-Oriented, Object-Relational, Vector DB, Polyglot Persistence).
   * [Lecture 4 - MMDS Architecture.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%204%20-%20MMDS%20Architecture.pdf): Kiến trúc MMDBMS 3 tầng (Client-Server), nguyên lý lưu trữ hỗn hợp (Hybrid Principle: tách BLOB và Metadata/Vector).
   * [Lecture 9 - Multimedia metadata.pdf](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%209%20-%20Multimedia%20metadata.pdf): 4 loại Metadata (Kỹ thuật, Cấu trúc, Mô tả, Quản trị), 3 cấp độ biểu đạt Panofsky, chuẩn MPEG-7 AudioDescription.
   * Các slide nền tảng: Lecture 1 (Tổng quan, Precision/Recall), Lecture 2 (Lấy mẫu âm thanh, lượng tử hóa PCM), Lecture 3 (Nén dữ liệu), Lecture 8, 11, 12.
2. **Yêu cầu đề tài**: File [yeu_cau.txt](file:///D:/Ki1_4/HCSDLDPT/BTL/yeu_cau.txt) tại thư mục gốc.
3. **Mã nguồn hiện có**:
   * File [Strings/scan_dataset.py](file:///D:/Ki1_4/HCSDLDPT/BTL/Strings/scan_dataset.py): Script sử dụng `ffprobe` quét metadata thời lượng, sample rate, kênh và kích thước file.
4. **Tập dữ liệu âm thanh (Thư mục `Strings/`)**:
   * Toàn bộ 4,477 files âm thanh MP3 thuộc 7 thư mục con: `banjo`, `cello`, `double bass`, `guitar`, `mandolin`, `viola`, `violin`.
   * Các file lưu trữ đi kèm: 7 file zip nguyên bản của từng nhạc cụ và 1 file `_notes/dwsync.xml`.
5. **Môi trường & Công cụ Runtime**:
   * `Python 3.13.9`
   * `FFmpeg` và `FFprobe` bản 9.0.2 đã có sẵn trong hệ điều hành.
   * Thư viện Python: `numpy`, `scipy`, `matplotlib`, `SQLAlchemy`, `fastapi`, `uvicorn`, `pydantic`.

---

## 2. Project Hiện Tại Đang Làm Gì?

Hiện tại, project đang ở **giai đoạn sơ khởi (Data Ingestion & Inspection Phase)**:
* Người dùng đã sưu tầm và tổ chức thành công một kho dữ liệu âm thanh rất lớn gồm 4,477 files nốt nhạc đơn lẻ (Single Notes) của 7 nhạc cụ bộ dây lấy từ nguồn Philharmonia Orchestra Sound Sample Library.
* Người dùng đã viết một script sơ khởi `scan_dataset.py` (nằm trong thư mục `Strings/`) với mục đích dùng công cụ `ffprobe` đọc các trường metadata cơ bản (thời lượng, sample rate, số kênh) và xuất ra file CSV `metadata_strings.csv`. Tuy nhiên script này chưa được chạy thành công trên đường dẫn hiện tại của project.
* **Chưa có bất kỳ dòng code nào** về: tiền xử lý âm thanh, trích rút đặc trưng âm học (MFCC, Centroid, ZCR...), cấu trúc CSDL quản trị, thuật toán so khớp vector tương đồng, hay giao diện demo.

---

## 3. Dataset Hiện Tại

Toàn bộ thông tin dưới đây được đo đạc trực tiếp bằng công cụ `ffprobe` trên toàn bộ 4,477 files:

| Nhạc cụ (Instrument) | Số lượng file | Dung lượng (MB) | Định dạng (Format) | Sample Rate | Số kênh | Thời lượng TB | Trạng thái (Status) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Banjo** | 74 | 3.11 MB | MP3 | 44,100 Hz | Mono (1) | 3.50s | 100% hợp lệ |
| **Cello** | 889 | 22.14 MB | MP3 | 44,100 Hz | Mono (1) | 2.00s | 100% hợp lệ |
| **Double Bass** | 852 | 14.91 MB | MP3 | 44,100 Hz | Mono (1) | 2.03s | 100% hợp lệ |
| **Guitar** | 106 | 6.48 MB | MP3 | 44,100 Hz | Mono (1) | 5.17s | 100% hợp lệ |
| **Mandolin** | 80 | 3.04 MB | MP3 | 44,100 Hz | Mono (1) | 3.15s | 100% hợp lệ |
| **Viola** | 974 | 20.04 MB | MP3 | 44,100 Hz | Mono (1) | 1.63s | 973 file OK, **1 file lỗi** |
| **Violin** | 1,502 | 25.56 MB | MP3 | 44,100 Hz | Mono (1) | 1.31s | 100% hợp lệ |
| **TỔNG CỘNG** | **4,477 files** | **95.28 MB** | **MP3** | **44,100 Hz** | **Mono** | **1.81s** | **4,476 file sẵn sàng** |

* **Đánh giá yêu cầu $\ge 500$ files**: Vượt chỉ tiêu số lượng (đạt 4,477/500 = gần $900\%$).
* **Vấn đề phát hiện**:
  1. **1 file hỏng (Corrupt)**: `Strings/viola/viola_D6_05_piano_arco-normal.mp3` lỗi giải mã luồng bit MP3.
  2. **2 cặp file trùng hash MD5**:
     * `cello_Cs6_1_mezzo-forte_arco-harmonic.mp3` trùng nhị phân với `violin_Ds5_phrase_forte_arco-spiccato.mp3`.
     * `cello_Ds5_05_forte_arco-normal.mp3` trùng nhị phân với `viola_G6_05_fortissimo_arco-normal.mp3`.
  3. **Mất cân bằng dữ liệu**: Violin (1,502 files) áp đảo so với Banjo (74 files) và Mandolin (80 files).

---

## 4. Feature Hiện Tại

| Đặc trưng (Feature) | Có / Không | Source code hiện tại | Trạng thái kỹ thuật |
| :--- | :---: | :--- | :--- |
| **Thời lượng (Duration)** | **CÓ** | `Strings/scan_dataset.py` (ffprobe) | Chỉ đọc metadata header |
| **Tần số lấy mẫu (Sample Rate)** | **CÓ** | `Strings/scan_dataset.py` (ffprobe) | Chỉ đọc metadata header |
| **Số kênh âm thanh (Channels)** | **CÓ** | `Strings/scan_dataset.py` (ffprobe) | Chỉ đọc metadata header |
| **Kích thước file (File Size)** | **CÓ** | `Strings/scan_dataset.py` (`st_size`) | Chỉ đọc thông số OS |
| **RMS Energy (Năng lượng)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Zero Crossing Rate (ZCR)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Silence Ratio (Tỷ lệ im lặng)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Spectral Centroid (Độ sáng)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Spectral Bandwidth (Dải phổ)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Spectral Rolloff (Cuộn phổ)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **MFCC (13 hệ số Mel)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |
| **Vector đặc trưng kết hợp (35-D)** | **KHÔNG** | Chưa có | **CẦN TRIỂN KHAI** |

---

## 5. Database Hiện Tại

* **Trạng thái**: **CHƯA CÓ**.
* Hiện tại trong toàn bộ workspace chưa có bất kỳ file database nào (chưa có `.db`, `.sqlite`, hay kết nối PostgreSQL).
* Tệp `metadata_strings.csv` được khai báo trong `scan_dataset.py` cũng chưa từng được tạo ra trên đĩa.
* **Giải pháp đề xuất đã thiết kế**: Áp dụng mô hình **Hybrid Storage Principle** theo Lecture 4 & 5. Thiết kế schema SQLite/PostgreSQL gồm các bảng `instruments`, `audio_files`, `audio_metadata`, `audio_features`, và `feature_vectors` (xem chi tiết tại [docs/06_DATABASE_DESIGN.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/06_DATABASE_DESIGN.md)).

---

## 6. Similarity Search Hiện Tại

* **Trạng thái**: **CHƯA CÓ**.
* **Thuật toán dự kiến triển khai**: Mô hình không gian vector (Vector Space Model) theo Lecture 7:
  * Chuẩn hóa Z-Score cho toàn bộ đặc trưng.
  * Chuẩn hóa L2-norm cho vector đặc trưng.
  * Tính độ tương đồng bằng **Cosine Similarity**: $S(D_i, Q) = D_i \cdot Q$.
  * Sắp xếp giảm dần và lấy Top 5 kết quả ($K=5$).
  * Đáp ứng trọn vẹn trường hợp nhạc cụ chưa có trong CSDL (Unseen Instrument) nhờ so khớp hoàn toàn ở mức vector âm học (Content-based).

---

## 7. Đối Chiếu Toàn Diện Với Yêu Cầu Đề Bài

| Yêu cầu đề bài | Trạng thái | Bằng chứng thực tế trong project | Thành phần còn thiếu / Cần làm tiếp |
| :--- | :---: | :--- | :--- |
| **1. Dataset $\ge 500$ files bộ dây** | **ĐẠT** | 4,477 files MP3 trong 7 thư mục `Strings/`. | Cần lọc bỏ 1 file corrupt, đánh dấu 2 cặp file trùng hash. |
| **2. Bộ đặc trưng âm học tương đồng/khác biệt** | **ĐANG THIẾU CODE** | Đã hoàn thiện tài liệu thiết kế đặc tả bộ vector 35-D tại [docs/04_FEATURES.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/04_FEATURES.md). | Cần viết code trích xuất tính toán bằng NumPy / SciPy. |
| **3. Trích xuất đặc trưng & CSDL lưu trữ** | **CHƯA CÓ** | Đã hoàn thiện tài liệu thiết kế schema CSDL tại [docs/06_DATABASE_DESIGN.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/06_DATABASE_DESIGN.md). | Cần viết code tạo CSDL SQLite và nạp toàn bộ vector vào CSDL. |
| **4. Tìm kiếm tương đồng Top-5** | **CHƯA CÓ** | Đã thiết kế thuật toán Cosine/Euclid tại [docs/07_SIMILARITY_SEARCH.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/07_SIMILARITY_SEARCH.md). | Cần viết search engine K-NN và ranking. |
| **4a. Sơ đồ khối, chức năng, I/O từng khối** | **ĐẠT** | Đã trình bày chi tiết tại [docs/08_SYSTEM_ARCHITECTURE.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/08_SYSTEM_ARCHITECTURE.md) và [docs/09_QUERY_PIPELINE.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/09_QUERY_PIPELINE.md). | - |
| **4b. Minh họa kết quả trung gian** | **ĐÃ THIẾT KẾ** | Đã đặc tả khung kết quả trung gian tại [docs/10_INTERMEDIATE_RESULTS.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/10_INTERMEDIATE_RESULTS.md). | Cần tích hợp hiển thị lên giao diện UI / CLI. |
| **4c. Đánh giá chất lượng hệ thống** | **ĐÃ THIẾT KẾ** | Đã xây dựng khung đánh giá tại [docs/11_EVALUATION.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/11_EVALUATION.md). | Cần code script chạy thử nghiệm tính Precision@5. |
| **5. Demo hệ thống** | **CHƯA CÓ** | Đã thiết lập kịch bản demo tại [docs/12_DEMO.md](file:///D:/Ki1_4/HCSDLDPT/BTL/docs/12_DEMO.md). | Cần code giao diện tương tác và máy chủ Web. |

---

## 8. Những Phần Còn Thiếu Theo Mức Độ Ưu Tiên

* **MỨC ĐỘ ƯU TIÊN CAO (HIGH PRIORITY)**:
  1. Viết module trích rút đặc trưng âm học chuẩn CBAR (MFCC, Spectral Centroid, Bandwidth, Rolloff, ZCR, RMS) dựa trên NumPy và SciPy.
  2. Tạo hệ CSDL SQLite và nạp toàn bộ metadata cùng vector đặc trưng của 4,476 files hợp lệ vào CSDL.
  3. Viết Similarity Search Engine tính toán Cosine Similarity và trích xuất Top-5 file giống nhất.
* **MỨC ĐỘ ƯU TIÊN TRUNG BÌNH (MEDIUM PRIORITY)**:
  1. Viết giao diện Web tương tác (HTML/CSS/JS + FastAPI) hỗ trợ upload file, nghe thử âm thanh và trực quan hóa Spectrogram/Vector so sánh.
  2. Viết CLI tool để test nhanh từ terminal.
  3. Viết script tự động đánh giá Precision@5 trên tập kiểm thử.
* **MỨC ĐỘ ƯU TIÊN THẤP (LOW PRIORITY)**:
  1. Thêm chỉ mục cây k-d tree hoặc phân cụm K-Means/FCM nếu muốn minh họa thêm phần nâng cao của slide Lecture 6 & 7.

---

## 9. USER ACTION REQUIRED (Những Việc Cần Người Dùng Quyết Định / Cung Cấp)

1. **Quyết định phạm vi nạp CSDL**:
   * Người dùng muốn hệ thống CSDL nạp **toàn bộ 4,476 files** hiện có hay chỉ chọn một tập con cân bằng hơn (ví dụ khoảng 700 - 1,000 files)?  
   *(Khuyến nghị của trợ lý: Nạp toàn bộ 4,476 files vì tốc độ tính toán ma trận chỉ tốn vài mili-giây, tận dụng tối đa kho dữ liệu đồ sộ)*.
2. **Cung cấp file kiểm thử ngoại vi (Dành cho ca "Nhạc cụ chưa có trong dữ liệu")**:
   * Đề tài yêu cầu test ca nhạc cụ chưa có trong CSDL. Người dùng nên chuẩn bị **1 đến 2 file âm thanh ngắn (3 - 5 giây)** của nhạc cụ dây truyền thống hoặc nhạc cụ khác ngoài 7 loại trên (ví dụ: tiếng Đàn Tranh, Đàn Bầu, Đàn Nhị, Sitar, hoặc Harp).
3. **Lựa chọn hình thức Giao diện Demo**:
   * Xác nhận người dùng muốn demo bằng **Web UI hiện đại** (chạy trên trình duyệt, có player nghe thử, có đồ thị phổ đẹp mắt) hay **Desktop / CLI terminal**. *(Khuyến nghị: Web UI với FastAPI để đạt điểm tối đa)*.
4. **Phê duyệt báo cáo và cho phép chuyển sang giai đoạn Code**.

---

## 10. Đề Xuất Roadmap Triển Khai Tiếp Theo

* **Giai đoạn 1: Làm sạch & Lọc dữ liệu (Data Cleaning)**: Bỏ qua file lỗi `viola_D6_05...`, xử lý 2 file trùng hash.
* **Giai đoạn 2: Module Tiền xử lý & Trích xuất đặc trưng (Feature Extraction Engine)**: Viết mã nguồn Python thuần sử dụng `numpy`, `scipy` và `ffmpeg` trích xuất vector 35 chiều.
* **Giai đoạn 3: Xây dựng Cơ sở dữ liệu (Database Setup & Batch Ingestion)**: Tạo SQLite DB, chạy pipeline nạp toàn bộ 4,476 vector đặc trưng và lưu cache ma trận $V_{\text{norm}}$.
* **Giai đoạn 4: Bộ máy tìm kiếm tương đồng (Similarity Search Engine)**: Viết logic K-NN Cosine Similarity và xếp hạng Top 5.
* **Giai đoạn 5: Xây dựng Giao diện Demo (Web Application & Audio Player)**: Tạo Web UI trực quan, cho phép người dùng kéo thả file, xem Spectrogram, nghe âm thanh kết quả.
* **Giai đoạn 6: Đánh giá & Hoàn thiện Báo cáo (Evaluation & Final Report)**: Chạy thực nghiệm đo Precision@5, tổng hợp slide và báo cáo bài tập lớn.
