# scripts/ — Các script chạy từng bước

> **Quy ước tên:** `pXX_…` là script của **Bước XX** trong [kế hoạch](../docs/02_PLANS/PART_1_PLAN.md); `p01_2_…` là bước con **1.2**. Mọi script đọc dữ liệu gốc trong `raw/` và chỉ ghi vào `data/` hoặc `reports/`.
>
> **Chạy bằng Python của môi trường ảo:** `.venv\Scripts\python scripts\<tên>.py` (cài môi trường: `pip install -r requirements.txt`).

## 1. Danh sách và thứ tự chạy

| Thứ tự | Script | Bước | Đọc | Ghi | Thời gian |
|---|---|---|---|---|---|
| 1 | `p01_1_download_iowa.py` | 1.1 Tải Iowa | Trang web Iowa MIS | `raw/iowa_mis/{violin,viola,cello,double-bass}/*.aiff`, `_download/manifest.csv` | Vài phút (tùy mạng) |
| 2 | `p01_2_slice_iowa.py` | 1.2 Cắt nốt Iowa | `raw/iowa_mis/**/*.aif(f)` | `data/interim/iowa_notes/` | ≈ 16 phút |
| 3 | `p01_3_build_catalog.py` | 1.3–1.5 Catalog, lọc, chia tập, sắp xếp | `raw/philharmonia/`, `data/interim/iowa_notes/` | `data/catalog.csv`, `data/notes/`, `data/queries/`, `data/excluded/` | ≈ 4 phút |
| 4 | `p01_6_dataset_stats.py` | 1.6 Mô tả dataset | `data/catalog.csv`, `slice_report.csv` | `reports/dataset/` | < 1 phút |
| 5 | `theory_figures.py` | Hình và số đo cho phần lý thuyết | `data/catalog.csv`, `data/notes/`, `data/queries/unseen/`, `data/excluded/technique/` (violin, cello) | `reports/theory/` | ≈ 2 phút (đo lại đặc trưng bằng `--redo`: ≈ 5 phút) |
| — | `legacy/scan_dataset.py` | (cũ) | — | — | Không dùng nữa; giữ để tham khảo |

Iowa guitar không có script tải, vì trang Iowa cung cấp sẵn một file zip (xem [raw/README.md](../raw/README.md) §3).

## 2. Từng script làm gì

### `p01_1_download_iowa.py`
- Đọc 4 trang Iowa (violin, viola, cello, double bass), lấy mọi link file có chữ `.arco.`.
- Trước khi tải, so dung lượng file trên đĩa với máy chủ. File đã đủ thì bỏ qua; file tải dở thì tải lại. File được ghi ra tên tạm `.part`, tải xong mới đổi tên thật.
- Ghi `manifest.csv` (URL, số byte, MD5) làm bằng chứng nguồn.
- `--dry-run`: chỉ liệt kê, không tải.

### `p01_2_slice_iowa.py`
Mỗi file Iowa là một chuỗi nốt đi lên từng nửa cung (ví dụ `E2B2` = 8 nốt), các nốt **ngân nối nhau, không có khoảng lặng**. Script cắt thành từng nốt:
1. Tìm các điểm bắt đầu nốt (onset) bằng SuperFlux.
2. Đo cao độ ngay sau mỗi onset bằng pYIN; bỏ điểm không có cao độ rõ.
3. Đối chiếu tuần tự với dãy nốt trong tên file; chỉ giữ nốt lệch ≤ 0.6 nửa cung.
4. Ghi mỗi nốt thành một file WAV, tên `<nhạc cụ>_<nốt>_<cường độ>_<kỹ thuật>_<dây>_<khoảng nốt>.wav`. Nhãn dây lấy từ tên file Iowa (`sulG` → `G`); riêng guitar có hai dây Mi: `sulE` → `lowE`, `sul_E` → `highE` (D28).

Script **chạy tiếp được**: mỗi file gốc cắt xong được lưu vào `data/interim/iowa_notes/_cache/`, lần sau bỏ qua. `--fresh` để cắt lại từ đầu. Cache lưu cả tên file và nhãn dây, nên **đổi quy tắc đặt nhãn thì phải xóa cache của các file liên quan** (hoặc dùng `--fresh`). Kết quả gần nhất: 1 429 / 1 552 nốt (92%).

Muốn chạy **độc lập với cửa sổ terminal** (tắt cửa sổ vẫn chạy tiếp), dùng PowerShell:
```powershell
Start-Process -FilePath .venv\Scripts\python.exe -ArgumentList "-u","scripts\p01_2_slice_iowa.py" `
  -RedirectStandardOutput data\interim\iowa_notes\slice.log -RedirectStandardError data\interim\iowa_notes\slice.err -WindowStyle Hidden
```

### `p01_3_build_catalog.py`
1. Gom mọi file của hai nguồn vào một danh sách.
2. Giải mã từng file (ffmpeg → mono 22 050 Hz), đo clipping trên tín hiệu gốc, **lọc thông cao 25 Hz** để bỏ tiếng ù hạ âm (D27), rồi đo thời lượng, phần có âm, đỉnh biên độ, MD5. File không giải mã được: ghi dòng lỗi đầu tiên của ffmpeg (đã bỏ địa chỉ bộ nhớ để kết quả ổn định).
3. Gắn `status` (lọc) và `split` (chia tập theo `midi mod 5`).
4. Chọn tối đa REF 150 / DB_POOL 200 / QUERY_POOL 60 nốt mỗi nhạc cụ, trải đều theo nguồn, cao độ, cường độ.
5. Xóa rồi chép lại `data/notes/`, `data/queries/`, `data/excluded/`; ghi `data/catalog.csv`.

Kết quả giống hệt nhau từng byte giữa các lần chạy (seed cố định). Ý nghĩa các cột: [data/README.md](../data/README.md) §4.

### `p01_6_dataset_stats.py`
Sinh `reports/dataset/dataset_stats.md` (8 bảng), 8 file CSV và 2 biểu đồ. **Không sửa tay** các file đó; chạy lại script để cập nhật.

### `theory_figures.py`
Sinh hình và số đo cho [docs/01_THEORY](../docs/01_THEORY/README.md):
1. **Đo đặc trưng** của 5 190 nốt (mọi nốt dùng được, banjo, mandolin, và các kỹ thuật bị loại của violin, cello): centroid, bandwidth, rolloff, ZCR, flatness, RMS-CV, MFCC c1–c13 (mean và std), trên 1.5 s đầu, chỉ frame có âm, sau khi lọc 25 Hz và chuẩn hóa đỉnh. Kết quả lưu ở `reports/theory/note_features.csv` và được dùng lại ở lần chạy sau; `--redo` để đo lại.
2. **Vẽ 16 hình** (`01_…png` → `16_…png`): sóng sin, công thức harmonic, nốt A3 trên 5 nhạc cụ, đường bao, spectrogram, âm vực, đặc trưng theo nhạc cụ, centroid theo cao độ, kỹ thuật và cường độ, ảnh hưởng nguồn thu, lấy mẫu, frame và phổ, các bước MFCC, vibrato, giá trị thông tin của đặc trưng, PCA.
3. **Ghi các bảng số** mà docs trích dẫn: `feature_information.csv` (η² theo nhạc cụ, theo nguồn thu), `source_transfer_1nn.csv` (láng giềng gần nhất trong cùng / khác nguồn), `pca_notes_*.csv`, `harmonics_A3.csv`, `centroid_by_pitch.csv`…

Đây là **script minh họa**, không phải pipeline chính thức của Bước 3 (F0 lấy theo tên nốt, chỉ đo trên nốt đơn).

## 3. Quy tắc chung
- Không ghi vào `raw/`.
- Mọi đường dẫn tính từ thư mục gốc project, nên chạy từ đâu cũng được.
- Script in tiếng Việt ra màn hình bằng UTF-8 (terminal Windows mặc định không in được).
- Đổi thuật toán hay quy tắc thì ghi vào [DESIGN_DECISIONS](../docs/08_AI_CONTEXT/DESIGN_DECISIONS.md) trước.
