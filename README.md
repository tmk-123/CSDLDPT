# Hệ CSDL Lưu Trữ Và Tìm Kiếm Tiếng Nhạc Cụ Bộ Dây
### (Content-Based Audio Retrieval System for String Instruments)

> **Môn học**: Hệ Cơ sở Dữ liệu Đa phương tiện (Multimedia Database Systems - MMDB)  
> **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**  
> **Giảng viên hướng dẫn**: TS. Nguyễn Đình Hóa (`hoand@ptit.edu.vn`)  

---

## 📌 1. Giới Thiệu Đề Tài

Hệ thống được xây dựng nhằm giải quyết bài toán **Truy vấn âm thanh dựa trên nội dung (Content-Based Audio Retrieval - CBAR)** dành riêng cho nhóm **nhạc cụ bộ dây (Chordophones)**. 

Khác với các hệ thống tìm kiếm thông thường dựa trên từ khóa hay ký âm nốt nhạc, hệ thống tiếp cận theo nguyên lý trích xuất đặc tính vật lý và âm sắc (**Timbre & Acoustic Features**) từ tín hiệu sóng âm thô. Từ đó, chuyển đổi mỗi file âm thanh thành một **Vector đặc trưng đa chiều (Feature Vector)** trong không gian vector âm học và thực hiện tìm kiếm tương đồng (**Similarity Search**) qua các độ đo hình học (Cosine Similarity, Euclidean Distance).

Hệ thống đáp ứng trọn vẹn yêu cầu xử lý cả hai trường hợp:
1. File truy vấn thuộc loại nhạc cụ **đã có trong cơ sở dữ liệu** (Known Classes).
2. File truy vấn thuộc loại nhạc cụ mới **chưa từng xuất hiện trong cơ sở dữ liệu** (Unseen Classes - ví dụ: đàn Đáy, đàn Nhị, Tỳ bà, Đàn tranh...).

---

## 🎯 2. Yêu Cầu Đề Bài & Mức Độ Đáp Ứng

| STT | Yêu cầu nghiệp vụ | Tình trạng | Mô tả giải pháp thực hiện |
| :---: | :--- | :---: | :--- |
| **1** | Bộ dữ liệu $\ge 500$ file âm thanh nhạc cụ bộ dây | ✅ **Vượt chỉ tiêu** | 4,477 files MP3 chất lượng cao từ Thư viện mẫu âm thanh chuẩn quốc tế **Philharmonia Orchestra**. |
| **2** | Xây dựng bộ đặc trưng nhận diện âm thanh & phân tích giá trị thông tin | ✅ **Hoàn thành** | Bộ đặc trưng 35 chiều kết hợp miền thời gian (RMS, ZCR) và miền tần số/phổ (MFCC 1-13, Spectral Centroid, Bandwidth, Rolloff, Contrast). |
| **3** | Triển khai thuật toán trích xuất & xây dựng hệ CSDL quản trị | ✅ **Hoàn thành** | Pipeline xử lý tín hiệu DSP (Framing, Windowing, FFT) và CSDL hỗn hợp (RDBMS SQLite + Filesystem lưu trữ file nhị phân). |
| **4** | Tìm kiếm Top-5 file tương đồng nhất cho file âm thanh đầu vào | ✅ **Hoàn thành** | Xếp hạng K-Nearest Neighbors (K-NN) dựa trên Cosine Similarity; hiển thị kết quả trung gian trực quan. |
| **5** | Đánh giá & Demo hệ thống | ✅ **Sẵn sàng** | Giao diện Web trực quan (FastAPI + Modern Web UI) & giao diện dòng lệnh (CLI). |

---

## 📊 3. Tổng Quan Bộ Dữ Liệu (Dataset Overview)

Dữ liệu âm thanh được tổ chức tại thư mục [Strings/](file:///d:/Ki1_4/HCSDLDPT/BTL/Strings/), gồm **7 nhạc cụ bộ dây** được chia thành 2 phân nhóm chính:
* **Nhóm kéo vĩ (Bowed Strings)**: Violin, Viola, Cello, Double Bass.
* **Nhóm gảy (Plucked Strings)**: Guitar, Banjo, Mandolin.

| Nhạc cụ | Số file MP3 | Thời lượng TB | Kỹ thuật biểu diễn chủ đạo | Đặc trưng âm học chính |
| :--- | :---: | :---: | :--- | :--- |
| **Banjo** | 74 | 3.50s | Gảy ngón (plucked) | Mặt cộng hưởng màng da, âm sắc đanh kim loại, tắt nhanh. |
| **Cello** | 889 | 2.00s | Kéo vĩ (arco-normal) | Thùng đàn lớn, âm sắc dày, trầm ấm ($f_0$ từ 65.4 Hz). |
| **Double Bass** | 852 | 2.03s | Kéo vĩ (arco-normal) | Cực trầm ($f_0$ từ 41.2 Hz), trọng tâm phổ $< 1,000\text{ Hz}$. |
| **Guitar** | 106 | 5.17s | Gảy ngón (normal, harmonics) | Âm sắc gỗ mộc, phân rã năng lượng dạng hàm mũ. |
| **Mandolin** | 80 | 3.15s | Rung ngón (tremolo), gảy kép | Dây kim loại kép tạo hiệu ứng rung chorus, phổ rất sáng. |
| **Viola** | 974 | 1.63s | Kéo vĩ (arco-normal) | Trung âm, dày và tối hơn violin. |
| **Violin** | 1,502 | 1.31s | Kéo vĩ (arco-normal) | Thanh thoát, chói sáng, trọng tâm phổ cao ($2,500 - 5,000+\text{ Hz}$). |
| **TỔNG CỘNG** | **4,477 files** | **1.81s** | **Định dạng MP3 (Mono, 44.1 kHz)** | **95.28 MB dữ liệu gốc** |

---

## 🏗️ 4. Kiến Trúc Hệ Thống (System Architecture)

Hệ thống tuân thủ mô hình kiến trúc 3 tầng (**3-Tier Architecture**) và nguyên lý lưu trữ đa phương tiện hỗn hợp (**Hybrid Storage Principle** - theo Slide bài giảng môn MMDB):

```
┌────────────────────────────────────────────────────────────────────────┐
│             1. TẦNG TRÌNH DIỄN (Client / Web Presentation)             │
│   - Tải file âm thanh truy vấn (MP3/WAV)                               │
│   - Trực quan hóa sóng âm (Waveform), Spectrogram                      │
│   - Bảng xếp hạng Top-5 kết quả kèm điểm số tương đồng                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Upload Query Audio
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             2. TẦNG XỬ LÝ ỨNG DỤNG (Application & Processing)          │
│   - Tiền xử lý: Cắt khoảng lặng (Silence Trimming), chuẩn hóa biên độ  │
│   - Trích rút đặc trưng: STFT -> MFCCs, Spectral Centroid, ZCR, RMS    │
│   - Chuẩn hóa: Z-Score Standardization & L2-Norm                       │
│   - Công cụ tìm kiếm: Tính Cosine Similarity / K-NN Ranking            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Query / Fetch Vectors
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             3. TẦNG LƯU TRỮ ĐA PHƯƠNG TIỆN (Multimedia Storage)        │
│   - SQLite Database (strings_multimedia.db): Metadata Catalog,         │
│     thông số thống kê toàn cục (mu, sigma), ma trận Feature Vectors     │
│   - File System: Lưu trữ 4,477 file âm thanh gốc và file truy vấn tạm  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 5. Không Gian Vector Đặc Trưng (35 Chiều)

Mỗi file âm thanh được biểu diễn bằng một vector đặc trưng thống kê cố định:

$$\mathbf{x} = [\mu_1, \sigma_1, \dots, \mu_k, \sigma_k] \in \mathbb{R}^{35}$$

1. **Nhóm đặc trưng miền thời gian (2 chiều)**:
   - `RMS Energy (mean)`: Thể hiện độ mạnh/yếu của năng lượng âm thanh.
   - `Zero Crossing Rate (mean)`: Tần suất đổi dấu của tín hiệu, phân biệt âm xát/vĩ kéo và âm gảy.
2. **Nhóm đặc trưng phổ tần số (6 chiều)**:
   - `Spectral Centroid (mean, std)`: Đo trọng tâm tần số (độ sáng của âm).
   - `Spectral Bandwidth (mean, std)`: Đo độ mở rộng dải tần xung quanh trọng tâm.
   - `Spectral Rolloff (mean, std)`: Tần số giới hạn chứa 85% tổng năng lượng phổ.
3. **Nhóm âm sắc nâng cao - MFCC (26 chiều)**:
   - `MFCC 1 đến 13 (mean, std)`: Mô phỏng cảm nhận thính giác người về hình bao phổ âm sắc (Timbre).
4. **Nhóm tỷ lệ khoảng lặng (1 chiều)**:
   - `Silence Ratio`: Tỷ lệ phần trăm khung có năng lượng dưới ngưỡng im lặng.

---

## 📁 6. Cấu Trúc Thư Mục Dự Án

```
d:/Ki1_4/HCSDLDPT/BTL/
├── README.md                      # Tài liệu tổng quan dự án (File này)
├── yeu_cau.txt                    # Đề bài và yêu cầu chi tiết từ Giảng viên
├── Strings/                       # Kho dữ liệu âm thanh 4,477 files MP3
│   ├── banjo/                     # 74 files
│   ├── cello/                     # 889 files
│   ├── double bass/               # 852 files
│   ├── guitar/                    # 106 files
│   ├── mandolin/                  # 80 files
│   ├── viola/                     # 974 files
│   ├── violin/                    # 1,502 files
│   └── scan_dataset.py            # Script kiểm toán dữ liệu ban đầu
├── MMDB slides/                   # Tập bài giảng lý thuyết môn học (PTIT)
└── docs/                          # Hệ thống tài liệu kỹ thuật hoàn chỉnh
    ├── 00_PROJECT_OVERVIEW.md     # Tổng quan dự án & bối cảnh môn học
    ├── 01_REQUIREMENTS_ANALYSIS.md# Phân tích ma trận đáp ứng yêu cầu
    ├── 02_DATASET.md              # Báo cáo kiểm toán và phân tích bộ dữ liệu
    ├── 03_AUDIO_CHARACTERISTICS.md# Đặc tính âm học của các nhạc cụ bộ dây
    ├── 04_FEATURES.md             # Cơ sở toán học & giá trị thông tin đặc trưng
    ├── 05_FEATURE_EXTRACTION.md   # Pipeline trích xuất đặc trưng DSP
    ├── 06_DATABASE_DESIGN.md      # Thiết kế lược đồ CSDL & quản trị vector
    ├── 07_SIMILARITY_SEARCH.md    # Thuật toán tìm kiếm tương đồng & K-NN
    ├── 08_SYSTEM_ARCHITECTURE.md  # Sơ đồ khối kiến trúc hệ thống
    ├── 09_QUERY_PIPELINE.md       # Quy trình xử lý truy vấn âm thanh
    ├── 10_INTERMEDIATE_RESULTS.md # Minh họa kết quả tính toán trung gian
    ├── 11_EVALUATION.md           # Kế hoạch và phương pháp đánh giá kết quả
    ├── 12_DEMO.md                 # Kịch bản demo phục vụ báo cáo
    ├── 13_SETUP_AND_RUN.md        # Hướng dẫn thiết lập môi trường và vận hành
    ├── 14_CURRENT_STATUS.md       # Báo cáo hiện trạng tiến độ dự án
    ├── 15_MISSING_DATA.md         # Phân tích dữ liệu thiếu và giải pháp bù đắp
    └── 16_GLOSSARY.md             # Bảng thuật ngữ đa phương tiện chuẩn
```

---

## ⚡ 7. Hướng Dẫn Cài Đặt & Vận Hành

### 7.1. Yêu Cầu Môi Trường
- **Hệ điều hành**: Windows 10/11 (64-bit).
- **Python**: Phiên bản `3.10` trở lên (Khuyến nghị `Python 3.13.9`).
- **FFmpeg**: Đã cài đặt và cấu hình sẵn trong biến môi trường `PATH`.
- **Thư viện Python phụ thuộc**:
  ```bash
  pip install numpy scipy matplotlib sqlalchemy fastapi uvicorn pydantic
  ```

### 7.2. Các Bước Vận Hành
1. **Kiểm tra trạng thái dữ liệu**:
   ```powershell
   Get-ChildItem -Path Strings -Directory
   ```
2. **Xây dựng CSDL & Trích xuất đặc trưng ngoại tuyến**:
   ```powershell
   python -m src.build_database
   ```
3. **Khởi chạy máy chủ Web UI & API**:
   ```powershell
   uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
   ```
   *Truy cập trình duyệt tại địa chỉ*: `http://127.0.0.1:8000`

---

## 📚 8. Tài Liệu Tham Khảo Môn Học
- **Lecture 2**: Multimedia data (Continuous and discrete media, PCM Audio).
- **Lecture 4**: Multimedia Database Management System Architecture (3-Tier & Hybrid Storage).
- **Lecture 5**: Multimedia data model.
- **Lecture 6**: Multidimensional data structures (k-d tree, R-tree).
- **Lecture 7**: Vector database and Clustering (Cosine Similarity, Euclidean Distance).
- **Lecture 9**: Multimedia metadata (MPEG-7 Audio standards).
- **Lecture 10**: Indexing and Retrieval for Audio (Acoustic Features, Spectrogram, MFCC, CBAR).
