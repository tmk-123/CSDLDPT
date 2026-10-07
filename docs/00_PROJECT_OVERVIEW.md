# 00. PROJECT OVERVIEW

## 1. Thông Tin Đề Tài
* **Tên đề tài**: Xây dựng hệ CSDL lưu trữ và tìm kiếm tiếng nhạc cụ bộ dây (String Instruments Sound Storage and Retrieval System).
* **Môn học**: Hệ Cơ sở Dữ liệu Đa phương tiện (Multimedia Database Systems - MMDB).
* **Giảng viên phụ trách môn học**: TS. Nguyễn Đình Hóa (`hoand@ptit.edu.vn`) - Học viện Công nghệ Bưu chính Viễn thông (PTIT).
* **Bối cảnh lý thuyết**: Dựa trên giáo trình và slide bài giảng MMDB (đặc biệt là [Lecture 10 - Indexing and Retrieval for Audio](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf), [Lecture 7 - Vector database and Clustering](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%207%20-%20Vector%20database%20and%20Clustering.pdf), [Lecture 6 - Multidimensional data structures](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%206%20-%20Multidimensional%20data%20structures.pdf), [Lecture 5 - MM data model](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%205%20-%20MM%20data%20model.pdf), [Lecture 4 - MMDS Architecture](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%204%20-%20MMDS%20Architecture.pdf), và [Lecture 9 - Multimedia metadata](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%209%20-%20Multimedia%20metadata.pdf)).

---

## 2. Mục Tiêu Dự Án
1. **Quản lý và chuẩn hóa kho dữ liệu âm thanh**:
   * Sưu tầm, thẩm định và quản lý kho dữ liệu âm thanh nhạc cụ bộ dây (yêu cầu tối thiểu $\ge 500$ files, kho thực tế hiện tại có 4,477 files MP3).
   * Phân tích đặc tính âm học (acoustic properties), âm sắc (timbre), dải tần số (pitch range), và kỹ thuật diễn tấu của từng nhạc cụ trong bộ dây.
2. **Trích xuất đặc trưng âm thanh theo chuẩn CBAR (Content-Based Audio Retrieval)**:
   * Thiết kế bộ đặc trưng đa chiều kết hợp giữa miền thời gian (Time-domain) và miền tần số (Frequency-domain): RMS Energy, Zero Crossing Rate (ZCR), Silence Ratio, Spectral Centroid, Spectral Bandwidth, Spectral Rolloff, Spectral Contrast, và Mel-Frequency Cepstral Coefficients (MFCCs).
   * Thực hiện đóng gói đặc trưng thành vector đặc trưng đa chiều (Feature Vector) đại diện cho nội dung âm thanh độc lập với độ dài bản ghi.
3. **Mô hình hóa và quản trị CSDL đa phương tiện**:
   * Thiết kế hệ CSDL lưu trữ cấu trúc đa phương tiện kết hợp (Hybrid principle): RDBMS (SQLite/PostgreSQL) lưu trữ metadata kỹ thuật, metadata mô tả và feature vector; filesystem lưu trữ file nhị phân (BLOB).
4. **Truy vấn và tìm kiếm âm thanh tương đồng (Content-Based Similarity Search)**:
   * Đầu vào: 1 file âm thanh tùy ý của một nhạc cụ bộ dây (có thể đã có hoặc chưa từng có nhãn trong CSDL).
   * Đầu ra: Top 5 file âm thanh có nội dung và âm sắc tương đồng nhất, xếp theo thứ tự giảm dần của độ tương đồng.
   * Minh họa từng bước tính toán trung gian và trực quan hóa kết quả cho người dùng.

---

## 3. Đầu Vào và Đầu Ra Hệ Thống
```
+-------------------------------------------------------------------------+
|                              ĐẦU VÀO (INPUT)                            |
|  - File âm thanh (.mp3, .wav, ...) của một nhạc cụ bộ dây               |
|  - Trường hợp 1: Nhạc cụ ĐÃ CÓ trong CSDL (Known class)                 |
|  - Trường hợp 2: Nhạc cụ CHƯA CÓ trong CSDL (Unseen/Unknown class)      |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                     HỆ CSDL & CÔNG CỤ TÌM KIẾM (CBAR)                   |
|  - Tiền xử lý (Mono, chuẩn hóa RMS, cắt khoảng lặng)                    |
|  - Trích rút đặc trưng (MFCC, Spectral Centroid, Bandwidth, ZCR, RMS)   |
|  - Chuẩn hóa Feature Vector (Z-Score / L2 Norm)                         |
|  - Tính khoảng cách / độ tương đồng (Cosine Similarity / Euclidean)     |
|  - Ranking K-NN (Top-5)                                                 |
+-------------------------------------------------------------------------+
                                     │
                                     ▼
+-------------------------------------------------------------------------+
|                             ĐẦU RA (OUTPUT)                             |
|  - Danh sách Top 5 file âm thanh giống nhất                             |
|  - Độ tương đồng định lượng (Similarity Score ∈ [0, 1] hoặc Distance)   |
|  - Thông tin Metadata của từng file (Nhạc cụ, Nốt, Kỹ thuật, Cường độ) |
|  - Đồ thị so sánh đặc trưng trung gian (Spectrogram, MFCC comparison)   |
+-------------------------------------------------------------------------+
```

---

## 4. Tóm Tắt Hiện Trạng Kho Dữ Liệu
* **Nguồn gốc dữ liệu**: Thư viện mẫu âm thanh Philharmonia Orchestra Sound Sample Library.
* **Số lượng**: 4,477 files âm thanh định dạng `.mp3`, chia thành 7 thư mục nhạc cụ:
  * `banjo`: 74 files
  * `cello`: 889 files
  * `double bass`: 852 files
  * `guitar`: 106 files
  * `mandolin`: 80 files
  * `viola`: 974 files (trong đó có 1 file lỗi corrupt: `viola_D6_05_piano_arco-normal.mp3`)
  * `violin`: 1,502 files
* **Đặc tính mẫu (Node đơn/Single notes)**: Mỗi file là một nốt nhạc đơn lẻ (isolated note), được đặt tên chuẩn 5 thành phần: `<nhạc_cụ>_<nốt>_<độ_dài>_<cường_độ>_<kỹ_thuật>.mp3`.

---

## 5. Môi Trường Công Nghệ
* **Hệ điều hành**: Windows 11 / Windows Server.
* **Ngôn ngữ lập trình**: Python 3.13.9.
* **Xử lý âm thanh & trích xuất tín hiệu**: FFprobe / FFmpeg 9.0.2 (đã cài đặt), thư viện khoa học `numpy` 2.3.5, `scipy` 1.16.3, `matplotlib` 3.10.7.
* **Cơ sở dữ liệu**: `SQLAlchemy` 2.0.45 kết hợp SQLite / PostgreSQL.
* **Giao diện & API**: `fastapi` 0.128.0, `uvicorn` 0.40.0.
