# 02. DATASET ANALYSIS & AUDIT REPORT

## 1. Nguồn Gốc và Cấu Trúc Dataset
* **Nguồn dữ liệu**: **Philharmonia Orchestra Sound Sample Library** (bộ dữ liệu mẫu âm thanh chuẩn quốc tế do Dàn nhạc giao hưởng Philharmonia tại London phát hành công khai cho mục đích nghiên cứu và giáo dục âm nhạc).
* **Vị trí lưu trữ**: Thư mục [Strings/](file:///D:/Ki1_4/HCSDLDPT/BTL/Strings/) tại thư mục gốc của project.
* **Cấu trúc thư mục**:
```
Strings/
├── banjo/            (74 files .mp3, 1 file banjo.zip)
├── cello/            (889 files .mp3, 1 file cello.zip)
├── double bass/      (852 files .mp3, 1 file double bass.zip, 1 thư mục _notes/)
├── guitar/           (106 files .mp3, 1 file guitar.zip)
├── mandolin/         (80 files .mp3, 1 file mandolin.zip)
├── viola/            (974 files .mp3, 1 file viola.zip)
├── violin/           (1,502 files .mp3, 1 file violin.zip)
└── scan_dataset.py   (Script quét metadata bằng ffprobe)
```

---

## 2. Thống Kê Chi Tiết Từng Nhạc Cụ (Kết Quả Quét Thực Tế)

Dữ liệu được trích xuất trực tiếp bằng công cụ `ffprobe` trên toàn bộ 4,477 files trong thư mục `Strings/`:

| Nhạc cụ | Số file MP3 | Dung lượng (MB) | Thời lượng Min (s) | Thời lượng Max (s) | Thời lượng TB (s) | Sample Rate (Hz) | Kênh (Channels) | Số nốt nhạc phân biệt | Kỹ thuật chơi phổ biến nhất |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Banjo** | 74 | 3.11 | 2.82 | 3.87 | 3.50 | 44,100 | Mono (1) | 41 | normal (74) |
| **Cello** | 889 | 22.14 | 0.31 | 23.33 | 2.00 | 44,100 | Mono (1) | 54 | arco-normal (747), col-legno (18) |
| **Double Bass** | 852 | 14.91 | 0.08 | 29.54 | 2.03 | 44,100 | Mono (1) | 44 | arco-normal (764), pizz-normal (15) |
| **Guitar** | 106 | 6.48 | 2.80 | 10.55 | 5.17 | 44,100 | Mono (1) | 42 | normal (71), harmonics (35) |
| **Mandolin** | 80 | 3.04 | 2.17 | 3.92 | 3.15 | 44,100 | Mono (1) | 39 | tremolo (41), normal (39) |
| **Viola** | 974 | 20.04 | 0.08 | 26.62 | 1.63 | 44,100 | Mono (1) | 55 | arco-normal (708), pizz-normal (39) |
| **Violin** | 1,502 | 25.56 | 0.31 | 14.73 | 1.31 | 44,100 | Mono (1) | 55 | arco-normal (852), pizz-normal (49) |
| **TỔNG CỘNG** | **4,477** | **95.28 MB** | **0.08** | **29.54** | **1.81** | **44,100** | **Mono (1)** | - | - |

---

## 3. Bản Chất Dữ Liệu "Node Đơn Chưa Lọc" (Single Note Dataset)

Trong yêu cầu của đề tài, người dùng đề cập đến khái niệm **"node đơn chưa lọc"**:
* **Bản chất thực tế**: Thuật ngữ "node đơn" là cách viết thuần Việt của **"single musical note" (nốt nhạc đơn lẻ)**. Đây là các file ghi lại âm thanh của **từng nốt nhạc riêng rẽ** (isolated notes) được chơi bởi nhạc công chuyên nghiệp.
* **Quy ước đặt tên**: 100% (4,477/4,477) file đều có tên theo cấu trúc 5 thành phần chuẩn:
  $$\text{[Nhạc cụ]\_[Nốt nhạc]\_[Thời lượng quy ước]\_[Cường độ]\_[Kỹ thuật].mp3}$$
  * Ví dụ: `violin_Gs4_1_forte_arco-normal.mp3`
    * `violin`: Nhạc cụ vĩ cầm.
    * `Gs4`: Nốt Sol thăng quãng 4 (G#4, tương đương tần số cơ bản $f_0 \approx 415.3 \text{ Hz}$).
    * `1`: Thời lượng quy ước khi thu âm (1 giây / 1 phách).
    * `forte`: Cường độ âm thanh (mạnh).
    * `arco-normal`: Kỹ thuật kéo vĩ bình thường.
* **Tại sao gọi là "chưa lọc"**:
  1. Chưa cắt lọc khoảng lặng đầu/cuối (lead-in/lead-out silence).
  2. Chưa chuẩn hóa biên độ (loudness normalization): các dynamic từ `pianissimo` đến `fortissimo` có biên độ dao động rất lớn.
  3. Có sự chênh lệch lớn về thời lượng: nốt ngắn nhất chỉ 0.08s (quá ngắn cho một số phân tích biến thiên cửa sổ dài), nốt dài nhất lên tới 29.54s.
  4. Mất cân bằng lớp (Class Imbalance): Violin (1,502 files) gấp 20 lần Banjo (74 files).

---

## 4. Các Vấn Đề Bất Thường Phát Hiện Được Khi Audit

### 4.1. File Âm Thanh Bị Lỗi (Corrupted File)
* **Tên file**: `viola_D6_05_piano_arco-normal.mp3`
* **Vị trí**: `Strings/viola/viola_D6_05_piano_arco-normal.mp3`
* **Thông báo lỗi từ ffprobe**: `[mp3 @ ...] Failed to find two consecutive MPEG audio frames. Invalid data found when processing input`.
* **Đánh giá**: File bị mất header / hỏng dữ liệu luồng audio, không thể giải mã PCM nếu không xử lý sửa lỗi.
* **Khuyến nghị**: Đánh dấu trạng thái `CORRUPT` trong CSDL, không đưa vào vector database để tránh làm crash pipeline trích xuất đặc trưng.

### 4.2. File Trùng Lặp Nội Dung Nhị Phân (Duplicate MD5 Hash)
Kiểm tra băm MD5 toàn bộ nội dung file phát hiện 2 cặp file có nội dung hoàn toàn trùng nhau:
1. **Hash `f4e7dab7e923e2fb3bc47f154568e64c`**:
   * File 1: `Strings/cello/cello_Cs6_1_mezzo-forte_arco-harmonic.mp3`
   * File 2: `Strings/violin/violin_Ds5_phrase_forte_arco-spiccato.mp3`
2. **Hash `c47352fcb023f03b5ba59b75ae88a248`**:
   * File 1: `Strings/cello/cello_Ds5_05_forte_arco-normal.mp3`
   * File 2: `Strings/viola/viola_G6_05_fortissimo_arco-normal.mp3`
* **Nguyên nhân**: Đây là lỗi gán nhầm file trong bộ gốc Philharmonia khi dàn dựng thư viện tải về. Cần lưu vết trong metadata để không gây nhiễu cho mô hình đánh giá tương đồng.

### 4.3. File Rác / Metadata Web
* Trong `Strings/double bass/` có thư mục `_notes/dwsync.xml`: Đây là file đồng bộ hóa web của Macromedia/Adobe Dreamweaver do nguồn phát hành web để lại, không liên quan đến âm thanh.

---

## 5. Đánh Giá Tiêu Chí Số Lượng $\ge 500$ Files
* **Số lượng yêu cầu**: Ít nhất 500 files âm thanh.
* **Số lượng hiện có**: **4,477 files âm thanh** hợp lệ (4,476 file giải mã thành công).
* **Kết luận**: Dataset **hoàn toàn đáp ứng và vượt xa tiêu chuẩn số lượng** quy định trong đề bài (gấp gần 9 lần).
* **Khuyến nghị sử dụng**:
  * Bộ dataset 4,477 file này có thể dùng làm toàn bộ Database để lập chỉ mục.
  * Hoặc trích một tập con cân bằng (ví dụ: mỗi nhạc cụ 70-100 files, tổng cộng 500-700 files) để làm tập thử nghiệm chuẩn hóa cao, giữ toàn bộ 4,477 files trong CSDL đầy đủ.
