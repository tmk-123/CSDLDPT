# 13. SYSTEM SETUP & EXECUTION GUIDE

Tài liệu này ghi nhận chính xác môi trường runtime hiện tại và hướng dẫn thiết lập hệ thống.

---

## 1. Thông Số Môi Trường Thực Tế Đã Kiểm Tra

* **Hệ điều hành**: Windows 11 / Windows Server (64-bit).
* **Vị trí thư mục gốc (Root Workspace)**: `D:\Ki1_4\HCSDLDPT\BTL`
* **Phiên bản Python**: `Python 3.13.9` (đã cài đặt).
* **Công cụ xử lý đa phương tiện bên ngoài**:
  * `ffmpeg` version 9.0.2-full_build (đã có trong PATH).
  * `ffprobe` version 9.0.2-full_build (đã có trong PATH).
* **Danh sách thư viện Python đã có sẵn**:
  * `numpy` (2.3.5) - Tính toán đại số tuyến tính và xử lý ma trận.
  * `scipy` (1.16.3) - Biến đổi Fourier (FFT), lọc tín hiệu số (DSP).
  * `matplotlib` (3.10.7) - Trực quan hóa phổ sóng Spectrogram.
  * `SQLAlchemy` (2.0.45) - ORM kết nối và quản trị CSDL quan hệ.
  * `fastapi` (0.128.0) & `uvicorn` (0.40.0) - Khung ứng dụng RESTful API và Web Server.
  * `pydantic` (2.12.5) - Xác thực cấu trúc dữ liệu schema.

---

## 2. Các Bước Vận Hành (Dự Kiến Khi Triển Khai)

### Bước 1: Mở Terminal Tại Thư Mục Gốc
Mở PowerShell tại đường dẫn project:
```powershell
cd D:\Ki1_4\HCSDLDPT\BTL
```

### Bước 2: Kiểm Tra Trạng Thái Dữ Liệu
Kiểm tra thư mục `Strings/` đảm bảo chứa đủ 7 thư mục nhạc cụ:
```powershell
Get-ChildItem -Path Strings -Directory
```

### Bước 3: Lập Chỉ Mục Ngoại Tuyến (Offline Ingestion & Database Build)
*(Sẽ chạy script xây dựng CSDL khi được triển khai)*:
```powershell
python -m src.build_database
```
Lệnh này sẽ:
1. Quét 4,477 files trong `Strings/`.
2. Trích xuất vector đặc trưng 35 chiều bằng FFmpeg + NumPy/SciPy.
3. Tính toán bộ tham số chuẩn hóa $(\mu, \sigma)$ toàn cục.
4. Tạo CSDL SQLite `strings_multimedia.db` và lưu trữ các bảng `audio_files`, `audio_features`, `feature_vectors`.

### Bước 4: Chạy Máy Chủ Tìm Kiếm & Giao Diện Web
*(Khi triển khai Web App)*:
```powershell
python -m src.main
# Hoặc:
uvicorn src.api:app --host 127.0.0.1 --port 8000 --reload
```
Truy cập trình duyệt tại địa chỉ: `http://127.0.0.1:8000` để sử dụng giao diện tìm kiếm âm thanh.

### Bước 5: Chạy Giao Diện Dòng Lệnh (CLI Query)
*(Dành cho kiểm thử nhanh)*:
```powershell
python -m src.cli_search --file "path/to/query_sample.mp3" --top_k 5
```
