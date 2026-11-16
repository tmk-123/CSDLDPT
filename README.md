# Hệ CSDL lưu trữ và tìm kiếm tiếng nhạc cụ bộ dây

Bài tập lớn môn Hệ cơ sở dữ liệu đa phương tiện. Đề bài: `requirements.txt`.

Hệ thống nhận một tệp âm thanh mới và trả về **5 tệp giống nhất** trong CSDL 600 đoạn âm thanh của 6 nhạc cụ dây
(Violin, Viola, Cello, Double Bass, Guitar Acoustic, Guitar Electric), xếp giảm dần theo độ tương đồng.

## Cấu trúc thư mục

```
btl_new/
├── requirements.txt            đề bài
├── requirements-python.txt     thư viện Python (phiên bản cố định)
├── .env.example                mẫu cấu hình MySQL -> sao chép thành .env (không đưa lên git)
├── data/                       (không đưa lên git)
│   ├── raw/<nhạc cụ>/          dữ liệu gốc tải về
│   ├── wav/<nhạc cụ>/          600 tệp WAV của CSDL (mono, 22 050 Hz, 2,5–3,5 s)
│   ├── metadata.csv            nguồn gốc từng tệp (được đưa lên git)
│   └── truy_van/goc/           tệp truy vấn ngoài CSDL (nhạc cụ dây chưa có, trống, sáo) + nguon.csv
├── src/
│   ├── phan1_du_lieu/          yêu cầu 1: dựng bộ dữ liệu và mô tả
│   ├── phan3_dac_trung_csdl/   yêu cầu 3: trích đặc trưng, CSDL MySQL
│   ├── phan4_tim_kiem/         yêu cầu 4: chọn đặc trưng, tìm kiếm Top 5, đánh giá
│   └── phan5_demo/             yêu cầu 5: giao diện demo (Streamlit)
├── ket_qua/                    bảng số liệu (csv) và hình (hinh/) dùng cho báo cáo
├── bao_cao/                    báo cáo Word + tai_lieu_tham_khao/
└── ly_thuyet/                  ghi chú lý thuyết, giải thích để bảo vệ
```

## Cài đặt

1. Python 3.13, tạo môi trường và cài thư viện:
   ```
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements-python.txt
   ```
2. MySQL 8 đang chạy. Sao chép `.env.example` thành `.env` và điền thông tin kết nối:
   ```
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=<mật khẩu>
   MYSQL_DATABASE=nhac_cu_bo_day
   ```

## Chạy theo thứ tự (từ thư mục gốc)

| Bước | Lệnh | Kết quả |
|---|---|---|
| 1. Dựng bộ dữ liệu (cần `data/raw/`) | `.venv\Scripts\python.exe src\phan1_du_lieu\tao_bo_du_lieu.py` | 600 tệp `data/wav/`, `data/metadata.csv` |
| 1. Mô tả giống / khác nhau | `.venv\Scripts\python.exe src\phan1_du_lieu\mo_ta_du_lieu.py` | hình và bảng trong `ket_qua/` |
| 3. Trích đặc trưng + nạp CSDL | `.venv\Scripts\python.exe src\phan3_dac_trung_csdl\nap_csdl.py` | CSDL MySQL, `schema.sql`, `ket_qua/*dac_trung_600_tep.csv` |
| Chọn đặc trưng | `.venv\Scripts\python.exe src\phan4_tim_kiem\chon_dac_trung.py` | `ket_qua/chon_dac_trung/` |
| Kiểm tra với nhạc cụ không phải dây | `.venv\Scripts\python.exe src\phan4_tim_kiem\kiem_tra_ngoai_bo_day.py` | `ket_qua/chon_dac_trung/e9_*` |
| 4. Tìm kiếm một tệp | `.venv\Scripts\python.exe src\phan4_tim_kiem\tim_kiem.py <tệp>` | Top 5 + kết quả trung gian (in ra màn hình) |
| 4c. Đánh giá | `.venv\Scripts\python.exe src\phan4_tim_kiem\danh_gia.py` | `ket_qua/danh_gia/` |
| 5. Demo | `.venv\Scripts\streamlit.exe run src\phan5_demo\app.py` | giao diện tại http://localhost:8501 |

## Cấu hình đã chốt

- **CSDL** lưu 46 chiều cho mỗi tệp: MFCC (13 mean + 13 std), Roll-off, RMS, ZCR (mỗi loại mean + std), Spectral Contrast (7 dải x mean + std).
- **Truy vấn** dùng 15 chiều: MFCC 13 mean + Roll-off mean/std; chuẩn hóa z-score theo bảng `thong_ke_chuan_hoa`; độ đo cosine.
- Các chiều còn lại không dùng để so khớp nhưng được lưu để giải thích kết quả (RMS: kéo vĩ / gảy; ZCR, MFCC std,
  Spectral Contrast: nhận ra âm thanh không phải nhạc cụ dây). Centroid và Chroma bị bỏ sau đánh giá
  (lý do trong `ket_qua/chon_dac_trung/`).
- **Đánh giá** (chia theo bản thu, truy vấn luôn là bản thu thư viện chưa có): P@5 = 93,0%, MAP@5 = 91,9%.
