# 15. MISSING DATA & GAP ANALYSIS

Tài liệu này tổng hợp toàn diện các thành phần còn thiếu trong project hiện tại, phân loại theo mức độ ưu tiên và chỉ rõ những việc người dùng cần bổ sung hoặc quyết định.

---

## 1. Phân Tích Thiếu Sót Trong Kho Dữ Liệu (Dataset Gaps)

### 1.1. Về Số Lượng Tổng Thể
* **Tiêu chuẩn đề bài**: $\ge 500$ files âm thanh.
* **Thực tế hiện tại**: $4,477$ files MP3 (trong đó 4,476 files hợp lệ).
* **Kết luận**: **KHÔNG THIẾU VỀ TỔNG SỐ LƯỢNG**.

### 1.2. Về Độ Cân Bằng Giữa Các Lớp Nhạc Cụ (Class Imbalance)
* Hiện tại có sự chênh lệch lớn giữa các nhạc cụ:
  * Nhóm rất nhiều: `violin` (1,502 files), `viola` (974 files), `cello` (889 files), `double bass` (852 files).
  * Nhóm ít: `banjo` (74 files), `mandolin` (80 files), `guitar` (106 files).
* **USER NEEDS TO ADD (Tùy chọn)**: Nếu người dùng muốn tập dữ liệu cân bằng tuyệt đối giữa các lớp, người dùng có thể bổ sung thêm file cho Banjo và Mandolin. Nếu không, hệ thống vẫn vận hành tốt trên 4,476 file hiện tại mà không bắt buộc phải tải thêm.

### 1.3. Về Tập Dữ Liệu Thử Nghiệm Ngoài CSDL (Test Set for Unseen Instruments)
* Đề bài yêu cầu: *"Input là một file âm thanh mới về một nhạc cụ thuộc bộ dây (nhạc cụ thuộc loại đã có và KHÔNG CÓ trong dữ liệu)"*.
* **Hiện trạng**: Trong thư mục `Strings/` hiện chỉ có 7 loại nhạc cụ đã biết. Chưa có sẵn các file mẫu bên ngoài CSDL để phục vụ demo ca "Nhạc cụ chưa có trong dữ liệu" (như tiếng Đàn Bầu, Đàn Nhị, Đàn Tỳ Bà, v.v.).
* **USER NEEDS TO ADD (Khuyến nghị cao)**:
  * Người dùng nên chuẩn bị sẵn **2 đến 3 file âm thanh ngắn (3-5 giây)** của một loại nhạc cụ bộ dây **chưa có trong 7 loại trên** (ví dụ: file `dan_tranh.wav`, `dan_bau.wav`, `dan_nhi.wav`, hoặc `harp.mp3`) để dùng làm dữ liệu đầu vào kiểm thử thực tế cho buổi demo.

---

## 2. Phân Tích Thiếu Sót Về Thành Phần Kỹ Thuật (Technical Gaps)

| Thành phần | Hiện trạng trong codebase | Trạng thái | Đánh giá ưu tiên |
| :--- | :--- | :---: | :---: |
| **Tiền xử lý âm thanh** | Chưa có code cắt khoảng lặng và chuẩn hóa biên độ. | **THIẾU** | **CAO (HIGH)** |
| **Bộ trích xuất đặc trưng** | Mới chỉ có đọc metadata thời lượng qua ffprobe trong `scan_dataset.py`. Chưa có code STFT, Centroid, MFCC. | **THIẾU** | **CAO (HIGH)** |
| **Cơ sở dữ liệu (Database)** | Chưa có file CSDL SQLite / Postgres nào được khởi tạo. | **THIẾU** | **CAO (HIGH)** |
| **Similarity Search Engine** | Chưa có thuật toán tính độ tương đồng và ranking. | **THIẾU** | **CAO (HIGH)** |
| **Giao diện Demo / API** | Chưa có giao diện Web hoặc script CLI để người dùng thao tác nạp file và xem kết quả. | **THIẾU** | **CAO (HIGH)** |
| **Bộ đánh giá đo lường (Eval)** | Chưa có script đo Precision@5 tự động. | **THIẾU** | **TRUNG BÌNH (MEDIUM)** |

---

## 3. Tổng Hợp Danh Mục "USER NEEDS TO ACTION"

1. **USER NEEDS TO DECIDE (Quyết định phạm vi CSDL)**:
   * Quyết định dùng toàn bộ 4,476 files hiện có làm CSDL hay chọn lọc một tập con 700 - 1,000 files. *(Khuyến nghị: Dùng toàn bộ 4,476 files)*.
2. **USER NEEDS TO PROVIDE (Cung cấp file kiểm thử ngoại vi)**:
   * Cung cấp 1-2 file âm thanh của nhạc cụ ngoài danh mục 7 nhạc cụ hiện có (ví dụ: tiếng đàn Tranh / đàn Bầu / đàn Nhị) để làm bài test ấn tượng nhất khi nghiệm thu.
3. **USER NEEDS TO APPROVE (Phê duyệt)**:
   * Duyệt báo cáo audit và cho phép trợ lý bắt đầu viết code triển khai các module theo lộ trình.
