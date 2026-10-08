# Hệ CSDL Lưu Trữ Và Tìm Kiếm Tiếng Nhạc Cụ Bộ Dây
### (Content-Based Audio Retrieval System for String Instruments)

> **Môn học**: Hệ Cơ sở Dữ liệu Đa phương tiện (Multimedia Database Systems - MMDB)
> **Học viện Công nghệ Bưu chính Viễn thông (PTIT)**
> **Giảng viên hướng dẫn**: TS. Nguyễn Đình Hóa (`hoand@ptit.edu.vn`)

---

## 1. Giới thiệu
Hệ thống **tìm kiếm âm thanh theo nội dung (CBAR)** cho nhạc cụ bộ dây. CSDL chứa **500 file đoạn nhạc** (nhiều nốt) của 5 nhạc cụ: violin, viola, cello, double bass, guitar. Mỗi file được biểu diễn bằng **một vector đặc trưng 52 chiều**, giảm xuống **8 chiều bằng PCA** và đánh chỉ mục bằng **R\*-tree**. Với một file truy vấn (nhạc cụ có hoặc không có trong CSDL), hệ thống trả về **Top-5** file giống nhất.

Thiết kế đầy đủ: [docs/README.md](docs/README.md). Kết quả đã đạt: [docs/00_PROJECT/RESULTS_REPORT.md](docs/00_PROJECT/RESULTS_REPORT.md).

## 2. Trạng thái

| Phần việc | Trạng thái |
|---|---|
| Thiết kế (Phần 1, 2) | ✅ Xong, nằm trong `docs/` (quyết định D01–D28; 7 mục chờ P07–P13) |
| Lý thuyết (`docs/01_THEORY/`) | ✅ 22 bài từ cơ bản tới nâng cao, minh họa bằng số đo trên dataset thật |
| Môi trường (Bước 0) | ⏳ Thư viện ✅ (`requirements.txt`); khung `src/` + `config.py` chưa tạo |
| Dataset: thu thập, cắt nốt, lọc, chia tập, sắp xếp, mô tả | ✅ Xong (Bước 1.1–1.6): 5 906 file, 4 653 nốt dùng được, 12/12 test đạt |
| Đặc trưng, segmentation, vector 52D (Bước 2–7) | ⬜ Chưa làm |
| CSDL, R-tree, truy vấn (Bước 8–11) | ⬜ Chưa làm |
| Đánh giá, demo | ⬜ Chưa làm |

Chi tiết: [docs/00_PROJECT/CURRENT_STATUS.md](docs/00_PROJECT/CURRENT_STATUS.md).

## 3. Cài đặt và chạy

```powershell
# 1. Môi trường (Python 3.13, FFmpeg có trong PATH)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Dữ liệu gốc (không có trong git, xem mục 5)
#    - Philharmonia: tải tại https://philharmonia.co.uk/resources/sound-samples/, giải nén vào raw/philharmonia/<nhạc cụ>/
#    - Iowa MIS guitar: Guitar.mono.1644.1.zip tại https://theremin.music.uiowa.edu/MISguitar.html, giải nén .aif vào raw/iowa_mis/guitar/
python scripts/p01_1_download_iowa.py        # tự tải Iowa arco cho violin, viola, cello, double bass

# 3. Xây dataset (chạy bằng python của .venv)
python scripts/p01_2_slice_iowa.py      # cắt file Iowa thành nốt đơn (≈ 20 phút; dừng giữa chừng thì chạy lại sẽ làm tiếp)
python scripts/p01_3_build_catalog.py   # catalog + lọc + chia tập + sắp xếp file vào data/
python scripts/p01_6_dataset_stats.py   # bảng số liệu + biểu đồ mô tả dataset → reports/dataset/
python tests/test_catalog.py            # kiểm tra dataset (phải ra "12 đạt, 0 lỗi")
python scripts/theory_figures.py        # hình + số đo cho docs/01_THEORY → reports/theory/ (--redo: đo lại đặc trưng)
```

## 4. Cấu trúc thư mục và mô tả từng file

```
BTL/
├── README.md, CLAUDE.md, yeu_cau.txt, requirements.txt, .gitignore
├── MMDB slides/        slide môn học
├── docs/               toàn bộ thiết kế và báo cáo
├── scripts/            script chạy từng bước
├── tests/              kiểm tra tự động
├── reports/            bảng số liệu và biểu đồ sinh ra bằng script (có trong git, dùng cho báo cáo)
├── raw/                dữ liệu gốc tải về (KHÔNG có trong git)
├── data/               dữ liệu sinh ra bằng script (KHÔNG có trong git)
└── .venv/              môi trường Python (KHÔNG có trong git)
```

### 4.1. File ở thư mục gốc
| File | Mô tả |
|---|---|
| `README.md` | File này: giới thiệu, cách chạy, mô tả từng file |
| `CLAUDE.md` | Quy tắc làm việc: `docs/` là nguồn thiết kế; đọc docs và cập nhật thiết kế trước khi code |
| `yeu_cau.txt` | Đề bài gốc của giảng viên |
| `requirements.txt` | Danh sách thư viện Python kèm phiên bản chính xác (`pip install -r requirements.txt`) |
| `.gitignore` | Những gì git bỏ qua: `raw/` (giấy phép Philharmonia không cho công khai file mẫu), `data/`, `.venv/`, file tạm Python |

### 4.2. `MMDB slides/`: bài giảng môn học
12 file PDF, Lecture 1 → 12. Quan trọng nhất cho đề tài: **Lecture 6** (cấu trúc dữ liệu đa chiều, R-tree), **Lecture 7** (vector DB, khoảng cách, phân cụm), **Lecture 10** (truy vấn âm thanh, MFCC).

### 4.3. `scripts/`: script chạy từng bước
| File | Bước | Đọc | Ghi | Mô tả |
|---|---|---|---|---|
| `p01_1_download_iowa.py` | 1.1 | Trang web Iowa MIS | `raw/iowa_mis/<nhạc cụ>/*.aiff`, `_download/manifest.csv` | Tải file **arco** (16-bit 44.1 kHz mono) của violin, viola, cello, double bass; bỏ qua file đã tải đủ; ghi MD5 làm bằng chứng nguồn |
| `p01_2_slice_iowa.py` | 1.2 | `raw/iowa_mis/**/*.aif(f)` | `data/interim/iowa_notes/` | Cắt mỗi file Iowa (nhiều nốt liên tiếp) thành từng nốt: tìm onset (SuperFlux), đo cao độ (pYIN), đối chiếu với dãy nốt trong tên file, loại nốt không khớp; ghi nhãn dây (guitar: `lowE`/`highE`) |
| `p01_3_build_catalog.py` | 1.3–1.5 | `raw/philharmonia/`, `data/interim/iowa_notes/` | `data/catalog.csv`, `data/notes/`, `data/queries/`, `data/excluded/` | Gộp hai nguồn vào một catalog, lọc tiếng ù 25 Hz rồi đo từng file, gắn `status` (lọc), gắn `split` (chia tập), chọn nốt trong giới hạn, rồi **chép file vào thư mục theo nhạc cụ** |
| `p01_6_dataset_stats.py` | 1.6 | `data/catalog.csv`, `slice_report.csv` | `reports/dataset/` | Thống kê dataset: bảng theo nhạc cụ, nguồn, split, lý do loại; độ phủ cao độ; kết quả cắt nốt Iowa; vẽ 2 biểu đồ |
| `theory_figures.py` | lý thuyết | `data/catalog.csv`, file trong `data/` | `reports/theory/` | Đo đặc trưng của 5 190 nốt (centroid, ZCR, RMS-CV, MFCC…), vẽ 16 hình và ghi các bảng số cho `docs/01_THEORY/` (giá trị thông tin của đặc trưng, ảnh hưởng nguồn thu, PCA…). Script minh họa, không phải pipeline Bước 3 |
| `legacy/scan_dataset.py` | — | — | — | Script quét metadata đầu tiên (ffprobe), giữ lại để tham khảo; đã được `p01_3_build_catalog.py` thay thế |

Quy ước tên: `pXX_…` là script của **Bước XX** trong kế hoạch; `p01_2_…` là bước con **1.2**.

### 4.3b. `tests/`: kiểm tra tự động
| File | Kiểm tra gì | Chạy |
|---|---|---|
| `test_catalog.py` | 12 kiểm tra trên `data/catalog.csv` và các thư mục `data/`: mỗi file đúng một dòng; đúng số file hỏng/trùng; nhãn quá ngắn đúng quy tắc 0.35 s; nhãn dây đúng vật lý; **không cao độ nào nằm ở hai tập** (chống rò rỉ); đúng quy tắc `midi mod 5`; không vượt giới hạn chọn; mỗi tập có đủ 2 nguồn; banjo/mandolin không lọt vào CSDL; file lỗi chỉ ở `excluded/`; đúng kỹ thuật; mỗi nhạc cụ ≥ 360 nốt | `.venv\Scripts\python tests\test_catalog.py` |

### 4.4. `raw/`: dữ liệu gốc (chỉ đọc, không có trong git)
| Thư mục | Nội dung | Nguồn |
|---|---|---|
| `raw/philharmonia/<nhạc cụ>/` | 4 477 file mp3 của 7 nhạc cụ (banjo, cello, double bass, guitar, mandolin, viola, violin), kèm file zip gốc | [Philharmonia Sound Samples](https://philharmonia.co.uk/resources/sound-samples/). Dùng tự do, **cấm công khai nguyên file mẫu** |
| `raw/iowa_mis/guitar/` | 45 file `.aif`, mỗi file nhiều nốt guitar trên một dây; `_download/` chứa zip gốc | [Iowa MIS](https://theremin.music.uiowa.edu/MIS.html). Dùng không hạn chế |
| `raw/iowa_mis/{violin,viola,cello,double-bass}/` | 143 file `.aiff` arco; `_download/manifest.csv` ghi URL và MD5 từng file | Iowa MIS |

### 4.5. `data/`: dữ liệu sinh ra (không có trong git, tạo lại bằng script)
| Đường dẫn | Nội dung | Tạo bởi |
|---|---|---|
| `data/interim/iowa_notes/<nhạc cụ>/*.wav` | Nốt đơn vừa cắt từ Iowa (kết quả trung gian) | `p01_2_slice_iowa.py` |
| `data/interim/iowa_notes/notes.csv` | Mỗi nốt đã cắt một dòng: file gốc, cao độ, cường độ, dây, thời điểm, độ lệch cao độ | `p01_2_slice_iowa.py` |
| `data/interim/iowa_notes/slice_report.csv` | Mỗi file Iowa gốc một dòng: số nốt dự kiến, cắt được, nốt thiếu | `p01_2_slice_iowa.py` |
| `data/interim/iowa_notes/_cache/` | Kết quả cắt của từng file gốc (JSON), để chạy lại thì bỏ qua file đã xong | `p01_2_slice_iowa.py` |
| `data/interim/iowa_notes/slice.log`, `slice.err` | Nhật ký lần chạy cắt nốt gần nhất | `p01_2_slice_iowa.py` |
| **`data/catalog.csv`** | **Bảng trung tâm**: mỗi file một dòng, gồm nguồn, nhạc cụ, nốt, MIDI, cường độ, kỹ thuật, thời lượng, phần có âm, MD5, `status`, `split`, `selected`, đường dẫn | `p01_3_build_catalog.py` |
| `data/notes/<nhạc cụ>/<nguồn>/` | **Nốt đơn được dùng** của 5 nhạc cụ trong CSDL, gom theo nhạc cụ và nguồn. Tập (REF/DB_POOL/QUERY_POOL) và việc có được chọn hay không xem trong `catalog.csv` | `p01_3_build_catalog.py` |
| `data/queries/unseen/{banjo,mandolin}/` | Truy vấn **nhạc cụ ngoài CSDL** | `p01_3_build_catalog.py` |
| `data/queries/phrases/<nhạc cụ>/` | Đoạn nhạc thật nhiều nốt (Philharmonia `phrase`), dùng làm truy vấn | `p01_3_build_catalog.py` |
| `data/excluded/<lý do>/<nhạc cụ>/` | **File không dùng**, chia theo lý do: `corrupt` (hỏng), `duplicate` (trùng), `too_short` (quá ngắn), `technique` (kỹ thuật đặc biệt, pizz) | `p01_3_build_catalog.py` |

### 4.6. `reports/`: số liệu và biểu đồ cho báo cáo (có trong git)
| File | Nội dung | Tạo bởi |
|---|---|---|
| `reports/dataset/dataset_stats.md` | Toàn bộ bảng thống kê dataset (tự sinh, đừng sửa tay) | `p01_6_dataset_stats.py` |
| `reports/dataset/notes_by_instrument.png` | Biểu đồ số nốt dùng được theo nhạc cụ, tách theo nguồn, có vạch mức cần 360 | `p01_6_dataset_stats.py` |
| `reports/dataset/pitch_coverage.png` | Biểu đồ độ phủ cao độ: số nốt ở mỗi cao độ của từng nhạc cụ | `p01_6_dataset_stats.py` |
| `reports/dataset/status_by_source.csv` | Số file theo nguồn × trạng thái (OK, CORRUPT, DUPLICATE, TOO_SHORT) | `p01_6_dataset_stats.py` |
| `reports/dataset/split_by_instrument.csv` | Số file theo nhạc cụ × split (REF, DB_POOL, QUERY_POOL, PHRASE, UNSEEN, NONE) | `p01_6_dataset_stats.py` |
| `reports/dataset/usable_by_instrument.csv` | Nốt dùng được theo nhạc cụ × nguồn, số được chọn / có trong từng tập, đạt mức 360 hay chưa | `p01_6_dataset_stats.py` |
| `reports/dataset/pitch_coverage.csv` | Âm vực, số cao độ có nốt, số nốt mỗi cao độ, cao độ bị trống của từng nhạc cụ | `p01_6_dataset_stats.py` |
| `reports/dataset/excluded_by_reason.csv` | Số file không dùng theo nhạc cụ × lý do | `p01_6_dataset_stats.py` |
| `reports/dataset/queries.csv` | Số file truy vấn: phrase (nhạc thật) và unseen (nhạc cụ ngoài CSDL) | `p01_6_dataset_stats.py` |
| `reports/dataset/iowa_slicing.csv` | Kết quả cắt nốt Iowa theo nhạc cụ: số file, nốt dự kiến, cắt được, tỷ lệ | `p01_6_dataset_stats.py` |
| `reports/dataset/active_duration.csv` | Trung vị thời lượng phần có âm của nốt dùng được, theo nhạc cụ × nguồn | `p01_6_dataset_stats.py` |
| `reports/theory/01_…png` → `16_…png` | 16 hình minh họa cho phần lý thuyết (danh sách: `docs/01_THEORY/README.md` §4) | `theory_figures.py` |
| `reports/theory/*.csv` | Số đo mà phần lý thuyết trích dẫn: đặc trưng từng nốt, giá trị thông tin, ảnh hưởng nguồn thu, PCA, harmonic A3… (danh sách: `reports/README.md` §2) | `theory_figures.py` |

### 4.7. `docs/`: thiết kế và báo cáo
Bản đồ đầy đủ: [docs/README.md](docs/README.md). Gặp thuật ngữ lạ: [docs/09_REFERENCE/GLOSSARY.md](docs/09_REFERENCE/GLOSSARY.md).

| File | Mô tả |
|---|---|
| `docs/README.md` | Bản đồ tài liệu, quy tắc tránh trùng lặp |
| **00_PROJECT/** | **Đề bài, phạm vi, trạng thái** |
| `PROJECT_OVERVIEW.md` | Đề bài, hệ thống làm gì, chia Phần 1/2, trả lời nhanh 16 câu hỏi cốt lõi |
| `REQUIREMENTS.md` | Ánh xạ từng yêu cầu đề bài sang thiết kế và trạng thái |
| `PROJECT_SCOPE.md` | Phạm vi, bắt buộc và nâng cao, ràng buộc, bảng rủi ro |
| `CURRENT_STATUS.md` | Đã làm gì, đang làm gì, việc tiếp theo |
| `AUDIT_REPORT.md` | Kiểm tra thực tế dataset và project ban đầu |
| `RESULTS_REPORT.md` | **Báo cáo chi tiết kết quả từng phần đã thực hiện** |
| **01_THEORY/** | **Lý thuyết từ cơ bản tới nâng cao, theo yêu cầu `CLAUDE.md`; minh họa bằng số đo trên dataset** |
| `README.md` | Lộ trình đọc, bản đồ khái niệm, câu hỏi nào trả lời ở đâu, danh sách hình, tóm tắt phát hiện |
| `01_SOUND_BASICS.md` | Âm thanh, dao động, sóng sin; tần số, biên độ, pha; dB |
| `02_PITCH_NOTE_OCTAVE_SEMITONE.md` | Cao độ, quãng tám, nửa cung, cent, tên nốt, công thức nốt ↔ tần số, MIDI |
| `03_F0_HARMONICS_TIMBRE.md` | F0, harmonic, âm sắc; phân biệt 6 khái niệm hay nhầm; nốt A3 trên 5 nhạc cụ |
| `04_HOW_STRING_INSTRUMENTS_WORK.md` | Họ nhạc cụ dây, bộ phận, định luật Mersenne, bấm dây, kéo vĩ và gảy, thân đàn, phòng thu |
| `05_VIOLIN.md` · `06_VIOLA.md` · `07_CELLO.md` · `08_DOUBLE_BASS.md` · `09_GUITAR.md` | Từng nhạc cụ: cấu tạo, cơ chế, từng dây (nốt, quãng tám, tần số), bấm từng nửa cung, âm vực, kỹ thuật chơi (có số đo), phổ, âm sắc, đặc trưng nhận dạng, dữ liệu trong dataset |
| `10_BANJO_MANDOLIN.md` | Hai nhạc cụ gảy ngoài CSDL dùng để thử; dự đoán kết quả truy vấn |
| `11_PLAYING_TECHNIQUES.md` | Kỹ thuật chơi theo khâu tạo âm, số đo ảnh hưởng; vì sao CSDL chỉ giữ arco |
| `12_DIGITAL_AUDIO.md` | Lấy mẫu, Nyquist, lượng tử hóa, định dạng; một file âm thanh chứa gì; tiền xử lý |
| `13_WAVEFORM.md` | Dạng sóng, chu kỳ, đường bao (ADSR), RMS, ZCR |
| `14_FFT_STFT_SPECTRUM.md` | DFT/FFT, frame, cửa sổ Hann, STFT, phổ, spectrogram, thang Mel |
| `15_AUDIO_FEATURES.md` | Từng đặc trưng trả lời 9 câu hỏi (đo gì, đổi theo nốt / nhạc cụ / cách chơi / phòng thu, có nên dùng); vector 32D; mục chờ P08–P12 |
| `16_DATASET_MODEL.md` | Cây Instrument → … → Feature Vector, ý nghĩa từng tầng, dữ liệu cần thu thập và vì sao, chia tập |
| `17_ONSET_SEGMENTATION.md` | Tách nốt: năng lượng, spectral flux, SuperFlux, chọn đỉnh; bài học cắt nốt Iowa |
| `18_FEATURE_VECTOR.md` | K-means, prototype, túi prototype, gán mềm, vector 52D |
| `19_DISTANCE_SIMILARITY.md` | Euclid, chuẩn hóa z (ví dụ 3 nốt A4 thật), cân bằng khối, cosine, k-NN, chấm điểm |
| `20_PCA.md` | PCA, cận dưới, whitening; PCA trên 4 653 nốt thật |
| `21_R_TREE.md` | MBR, chèn, MINDIST, best-first k-NN, lọc rồi tinh chỉnh, lời nguyền số chiều |
| `22_MULTIMEDIA_DATABASE.md` | Tìm theo nội dung, lưu trữ hỗn hợp, metadata, mô hình dữ liệu, đường đi của truy vấn, đánh giá trung thực |
| **02_PLANS/** | **Kế hoạch** |
| `MASTER_PLAN.md` | Phương án đã chốt, giải thích từng bước từ dữ liệu gốc tới đánh giá: mục tiêu, input, làm gì theo thứ tự và vì sao, tham số, output, dùng ở đâu; bảng ký hiệu |
| `PART_1_PLAN.md` | Các bước 0–7 (dataset → vector 52D), checklist và tiêu chí xong |
| `PART_2_PLAN.md` | Các bước 8–11 (CSDL → R-tree → truy vấn) |
| `MILESTONES.md` | Các mốc và checklist tổng |
| **03_WORKFLOWS/** | **Luồng dữ liệu** |
| `MASTER_WORKFLOW.md` | Sơ đồ toàn hệ thống (Mermaid), khối chức năng và vào/ra |
| `PART_1_WORKFLOW.md` | Luồng xử lý Phần 1 và bên trong `audio_to_vector` |
| `PART_2_WORKFLOW.md` | Luồng build và truy vấn Phần 2 |
| `DATA_FLOW.md` | Script nào đọc gì, ghi gì |
| `IMPLEMENTATION.md` | Hàm thư viện nào được gọi, ở file nào, tham số và kết quả (phần đã chạy ✅ và phần dự kiến ⬜) |
| **04_PART_1/** | **Thiết kế Phần 1** |
| `01_DATASET/DATASET_COLLECTION_AND_FILTERING.md` | Kết quả lọc thật, nguồn bổ sung, các bước 1.1–1.6 |
| `01_DATASET/DATASET_INVENTORY.md` | Quy ước tên file, nhóm kỹ thuật, status |
| `01_DATASET/DATASET_ROLES.md` | Vai trò REF, DB, QUERY, PHRASE, UNSEEN |
| `01_DATASET/SPLIT_AND_LEAKAGE.md` | Quy tắc chia tập theo cao độ, chống rò rỉ dữ liệu |
| `01_DATASET/SEQUENCE_SYNTHESIS.md` | Cách ghép 500 file đoạn nhạc từ nốt đơn |
| `02_AUDIO_ANALYSIS/INSTRUMENT_CHARACTERISTICS.md` | Điểm giống và khác giữa các nhạc cụ (đề mục 1) |
| `02_AUDIO_ANALYSIS/PREPROCESSING.md` | Tiền xử lý: mono, 22 050 Hz, lọc tiếng ù 25 Hz, chuẩn hóa, cắt lặng |
| `03_FEATURE_DESIGN/FEATURE_SET.md` | Bộ đặc trưng 32D và giá trị thông tin (đề mục 2) |
| `03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md` | 20 prototype âm sắc học từ nốt đơn |
| `03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md` | Gộp segment thành vector 52D; ví dụ số |
| `04_FEATURE_EXTRACTION/EXTRACTION_PIPELINE.md` | Hàm và module trích đặc trưng |
| `04_FEATURE_EXTRACTION/SEGMENTATION.md` | Thuật toán tách nốt trong file nhiều nốt |
| `05_OUTPUT/PART_1_OUTPUT_SPEC.md` | Hợp đồng bàn giao Phần 1 → Phần 2 |
| **05_PART_2/** | **Thiết kế Phần 2** |
| `01_DATABASE/SCHEMA.md` | Lược đồ SQLite (DDL) và truy vấn mẫu |
| `02_INDEX/NORMALIZATION_PCA.md` | Chuẩn hóa và PCA 8D |
| `02_INDEX/RTREE_INDEX.md` | Cấu hình và cấu trúc R\*-tree |
| `03_SEARCH/KNN_SEARCH.md` | Độ đo, thuật toán Top-5 chính xác |
| `04_QUERY/QUERY_PIPELINE.md` | Các bước xử lý một truy vấn |
| `04_QUERY/INTERMEDIATE_RESULTS.md` | Kết quả trung gian phải hiển thị (đề mục 4b) |
| `06_SYSTEM/README.md` | (để sau) Kiến trúc, demo |
| `07_EVALUATION/README.md` | Kế hoạch đánh giá (P@5, MRR…) |
| **08_AI_CONTEXT/** | **Ngữ cảnh nhanh** |
| `PROJECT_CONTEXT.md` | Tóm tắt 10 dòng để trình bày với giảng viên |
| `DESIGN_DECISIONS.md` | **Nhật ký quyết định** D01–D28 và mục chờ P01–P13: chọn gì, vì sao, đã loại gì |
| `TODO.md` | Việc cần làm ngay |
| **09_REFERENCE/** | **Tra cứu** |
| `GLOSSARY.md` | Từ điển thuật ngữ (âm nhạc, kỹ thuật chơi, file, dataset, xử lý tín hiệu, CSDL) |
| `FORMULAS.md` | Tập hợp mọi công thức |
| `REFERENCES.md` | Nguồn dữ liệu (kèm giấy phép), bài báo, slide |
| `_archive/` | 19 file docs **cũ** (00–17), lỗi thời một phần; chỉ để tham khảo lịch sử |
