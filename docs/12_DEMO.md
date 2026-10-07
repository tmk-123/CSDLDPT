# 12. DEMO SPECIFICATION & SCENARIOS

> **TRẠNG THÁI HIỆN TẠI**: **KỊCH BẢN THIẾT KẾ ĐẦY ĐỦ - CHỜ TRIỂN KHAI CODE DEMO SAU KHI PHÊ DUYỆT**

Tài liệu này chuẩn bị kịch bản demo hoàn chỉnh cho buổi báo cáo / bảo vệ đề tài môn học Hệ CSDL Đa phương tiện.

---

## 1. Kịch Bản Demo End-to-End (Quy Trình 5 Bước)

```
Bước 1: Giới thiệu Kho CSDL & Kiến trúc
        (Trình chiếu Dashboard thống kê 4,477 files, 7 nhạc cụ bộ dây)
                          │
                          ▼
Bước 2: Nạp File Âm Thanh Truy Vấn (Query Audio)
        (Người dùng kéo-thả hoặc chọn file MP3/WAV từ máy tính)
                          │
                          ▼
Bước 3: Hiển thị Kết Quả Trung Gian
        (Hiển thị Spectrogram, giá trị RMS, Centroid, và Vector MFCC)
                          │
                          ▼
Bước 4: Thực Hiện Tìm Kiếm & Hiển Thị Top-5
        (Hệ thống tính toán Cosine Similarity trong <100ms, hiển thị bảng Top 5)
                          │
                          ▼
Bước 5: Nghe Thử Đối Sánh & Giải Thích Cơ Sở Khoa Học
        (Bấm nút Play để nghe file truy vấn và file kết quả tương đồng)
```

---

## 2. Các Ca Kiểm Thử Cụ Thể (Test Scenarios)

### Ca 1: Nhạc cụ ĐÃ CÓ trong CSDL - Nhóm Kéo Vĩ Chuẩn (Bowed Tone)
* **File thử nghiệm**: Một file nốt `Violin` kéo vĩ bình thường (`arco-normal`), ví dụ: `violin_A4_1_forte_arco-normal.mp3`.
* **Kỳ vọng**:
  * Top 1 phải là chính file đó (nếu file nằm trong DB) với Cosine Similarity $\approx 1.0000$.
  * Các vị trí 2, 3, 4, 5 phải là các file `Violin` hoặc `Viola` có cùng nốt hoặc nốt lân cận và cùng kỹ thuật `arco-normal`.
* **Ý nghĩa trình diễn**: Chứng minh tính nhất quán và độ chính xác của bộ đặc trưng MFCC + Spectral Centroid đối với cùng một loại nhạc cụ.

### Ca 2: Nhạc cụ ĐÃ CÓ nhưng Kỹ thuật Diễn tấu Khác Biệt (Cross-Technique)
* **File thử nghiệm**: Nốt `Cello` gảy ngón (`pizzicato`), ví dụ: `cello_C3_025_mezzo-forte_pizz-normal.mp3`.
* **Kỳ vọng**:
  * Top kết quả sẽ tìm ra các file `Cello pizzicato`, hoặc các nốt trầm của `Guitar` gảy nhẹ, vì chúng chia sẻ cùng hình bao năng lượng (Decay nhanh, không có sustain).
* **Ý nghĩa trình diễn**: Chứng minh hệ thống tìm kiếm theo **nội dung âm thanh thực sự** chứ không chỉ đơn thuần lọc theo nhãn `cello`.

### Ca 3: Nhạc cụ HOÀN TOÀN CHƯA CÓ TRONG CSDL (Unseen Instrument)
* **File thử nghiệm**: Một file âm thanh thu âm từ bên ngoài, ví dụ: Tiếng **Đàn Tỳ Bà (Pipa)** hoặc **Đàn Tam Thập Lục (Yangqin)** gảy nốt cao.
* **Kỳ vọng**:
  * Hệ thống trích xuất vector âm học bình thường không hề báo lỗi.
  * Top 5 trả về sẽ tự động hội tụ vào các file **Banjo** hoặc **Mandolin** có tiếng gảy đanh kim loại và dải tần cao tương đương.
* **Ý nghĩa trình diễn**: Thỏa mãn trọn vẹn yêu cầu khó nhất của đề bài: *"Đầu vào là một file âm thanh mới về một nhạc cụ thuộc bộ dây (nhạc cụ thuộc loại chưa có trong dữ liệu)"*.

---

## 3. Danh Sách Tính Năng Cần Có Trên Giao Diện Demo
1. **Khu vực tải file**: Hỗ trợ kéo thả (Drag & Drop) và nạp mẫu nhanh từ danh sách test.
2. **Trình phát âm thanh (Audio Player)**: Tích hợp nút Play/Pause dạng sóng âm trực quan (Waveform Player).
3. **Bảng so sánh trực quan**:
   * Cột hiển thị hình ảnh Spectrogram của file Query và file Top-1 cạnh nhau.
   * Biểu đồ thanh ngang so sánh 13 hệ số MFCC trung bình.
4. **Bảng kết quả xếp hạng**: Hiển thị rõ Rank 1 đến 5, tên file, nhãn nhạc cụ, nốt, kỹ thuật và điểm số tương đồng định lượng.
