# PART 1 PLAN — Từ dataset tới vector đặc trưng (Bước 0 → 7)

> **Kết quả cuối của Phần 1:** mỗi file (500 DB + 100 query) có **một vector 52D**, kèm metadata và ground truth, đúng như [PART_1_OUTPUT_SPEC](../04_PART_1/05_OUTPUT/PART_1_OUTPUT_SPEC.md).
>
> **Cách làm mỗi bước:** đọc tài liệu ở mục "Đọc trước" → làm các việc theo checklist → chạy phần "Kiểm tra" → chỉ khi mọi ô "Xong khi" đều đạt mới sang bước sau.

```
Bước 0 Môi trường ─► 1 Catalog ─► 2 Đọc audio ─► 3 Đặc trưng 32D ─► 4 Prototype
                         │                                              │
                         └──────► 5 Ghép sequence ─► 6 Segmentation ────┴─► 7 Vector 52D ─► (Phần 2)
```

---

## Bước 0 — Chuẩn bị môi trường
**Mục tiêu:** có môi trường Python chạy được mọi thư viện cần thiết, và có khung thư mục code.

**Việc cần làm** (PowerShell, tại thư mục `BTL/`):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install numpy scipy matplotlib librosa soundfile scikit-learn rtree
python -c "import librosa, sklearn, rtree, soundfile; print('OK', librosa.__version__)"
```
- Nếu `pip install` lỗi với Python 3.13: cài Python 3.12, rồi `py -3.12 -m venv .venv` và làm lại.
- [ ] Tạo `requirements.txt` (ghi phiên bản đã cài: `pip freeze > requirements.txt`).
- [ ] Tạo `.gitignore` gồm: `.venv/`, `data/`, `__pycache__/`, `*.pyc`.
- [ ] Tạo thư mục rỗng: `src/strings_mmdb/`, `scripts/`, `tests/`, `data/`.
- [ ] Tạo `src/strings_mmdb/config.py` chứa **mọi hằng số** (để không rải "con số ma" khắp code):

| Hằng số | Giá trị |
|---|---|
| `STRINGS_DIR` | `<BTL>/Strings` |
| `DATA_DIR` | `<BTL>/data` |
| `SR` | 22050 |
| `N_FFT` | 2048 |
| `HOP` | 512 |
| `TOP_DB_TRIM` | 40 |
| `REF_MAX_SEC` | 1.5 |
| `INSTRUMENTS` | violin, viola, cello, double-bass, guitar |
| `UNSEEN` | banjo, mandolin |
| `K_PER_INSTRUMENT` | 4 |
| `PCA_DIM` | 8 |
| `TOP_K` | 5 |
| `SEED` | 42 |

- [ ] Chuyển `Strings/scan_dataset.py` → `scripts/legacy/scan_dataset.py` (dùng `git mv`).

**Kiểm tra:** lệnh `python -c "import librosa, sklearn, rtree"` không lỗi; `from rtree import index; p = index.Property(); p.dimension = 8` không lỗi.

**Xong khi:** [ ] import OK · [ ] có khung thư mục · [ ] có `config.py`.

---

## Bước 1 — Dataset: thu thập, lọc, catalog ⭐ ĐANG TẬP TRUNG
**Đọc trước:** ⭐ [DATASET_COLLECTION_AND_FILTERING](../04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md), [DATASET_INVENTORY](../04_PART_1/01_DATASET/DATASET_INVENTORY.md), [SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md)

**Mục tiêu:** bộ nốt đơn **đủ cho cả 5 nhạc cụ** (≥ 360 nốt dùng được mỗi nhạc cụ) và một catalog **đáng tin**. Đây là nền móng của mọi bước sau: nếu dữ liệu thiếu hoặc split sai, mọi kết quả về sau đều vô nghĩa.

**Thứ tự làm** (chi tiết ở DATASET_COLLECTION_AND_FILTERING §4):

| Bước con | Việc | Xong khi |
|---|---|---|
| D1 | Tải Iowa MIS cho 5 nhạc cụ → `External/iowa_mis/` | Đủ file, đã ghi nguồn |
| D2 | Cắt file Iowa thành nốt đơn, kiểm tra số nốt theo tên file và cao độ bằng pYIN | Có bảng cắt và kiểm tra |
| D3 | Catalog hợp nhất (Philharmonia + Iowa, thêm cột `source`) | Xem checklist dưới |
| D4 | Áp quy tắc lọc F1–F6 | Mọi file có status |
| D5 | Chia tập theo (nhạc cụ, nguồn) | Bảng đếm nhạc cụ × nguồn × split |
| D6 | Thống kê và mô tả dataset (đề mục 1) | Bảng + biểu đồ |

> Bước D3–D5 làm được **ngay** trên `Strings/` (chưa cần Iowa). Khi có Iowa thì chạy lại, vì script được viết để chạy lại nhiều lần.

**Việc cần làm cho D3–D5** (`src/strings_mmdb/catalog.py` + `scripts/p01_build_catalog.py`):
- [ ] Duyệt `Strings/**/*.mp3`; tách tên file thành 5 trường (`split('_', 4)`).
- [ ] `note → midi`: ví dụ `As2` → 46. Công thức: `midi = 12·(octave+1) + index(tên nốt)`, với C = 0, Cs = 1, D = 2, …, B = 11.
- [ ] `technique → technique_family`: `arco-normal`, `molto-vibrato`, `non-vibrato` → `arco`; `pizz-normal` → `pizz`; `normal` (guitar) → `pluck`; `harmonics`/`*-harmonic` → `harmonic`; còn lại → `special`.
- [ ] Gọi ffprobe lấy `duration_sec`, `sample_rate`, `channels`; tính MD5.
- [ ] Giải mã từng file, đo **phần có âm** (RMS > −40 dB), đỉnh biên độ, số mẫu clipping.
- [ ] Gán `status` theo thứ tự: `CORRUPT` (giải mã lỗi) → `DUPLICATE` (MD5 trùng; gán cho **cả hai** file) → `TOO_SHORT` (phần có âm < 0.35 s) → (Iowa) `PITCH_MISMATCH` → `OK`. Thêm cờ `LOW_LEVEL`, `CLIPPED`.
- [ ] Thêm cột `source` (`philharmonia`/`iowa`), `active_sec`, `peak`.
- [ ] Gán `split` theo quy tắc ở SPLIT_AND_LEAKAGE §2.
- [ ] Ghi `data/catalog.csv`.

**Output:** `data/catalog.csv` gồm các cột: `recording_id, rel_path, instrument, note, midi, duration_label, dynamics, technique, technique_family, duration_sec, sample_rate, channels, md5, status, split`.

**Kiểm tra** (`tests/test_catalog.py`):
- [ ] Đúng 4 477 dòng.
- [ ] Đúng 1 `CORRUPT`, 4 `DUPLICATE`, 55 `TOO_SHORT` trong nốt đơn của 5 nhạc cụ (khớp số đã quét ngày 07/10).
- [ ] Số nốt dùng được khớp DATASET_COLLECTION_AND_FILTERING §1.3 (violin 959, viola 759, cello 756, double-bass 763, guitar 106; chưa tính Iowa).
- [ ] Không có cặp (instrument, midi) nào nằm ở hai split khác nhau.
- [ ] In bảng đếm *nhạc cụ × split* và so với số dự kiến (REF ≈ 40%, DB_POOL ≈ 40%, QUERY_POOL ≈ 20% số nốt cơ bản).
- [ ] Mọi file `phrase` có split = `PHRASE`; mọi file banjo/mandolin có split = `UNSEEN`.

**Xong khi:** mọi test qua và bảng đếm hợp lý.

---

## Bước 2 — Đọc và chuẩn hóa audio
**Đọc trước:** [PREPROCESSING](../04_PART_1/02_AUDIO_ANALYSIS/PREPROCESSING.md)

**Mục tiêu:** **một hàm duy nhất** để đọc mọi file audio trong project.

**Việc cần làm** (`src/strings_mmdb/audio_io.py`):
- [ ] `load_audio(path, trim=False) → y`: decode (librosa/ffmpeg) → mono → 22 050 Hz → float32 → peak-normalize về 0.95 → nếu `trim=True` thì cắt lặng (top_db = 40).
- [ ] Báo lỗi rõ ràng (kèm tên file) khi không decode được hoặc file toàn lặng.
- [ ] `scripts/p02_check_audio.py`: load mọi file `status=OK`, đo thời gian.

**Kiểm tra:** 20 file ngẫu nhiên: `y.dtype == float32`, `max|y| ≈ 0.95`, độ dài/22050 ≈ duration sau trim. File stereo 44.1 kHz tự tạo cũng load được.

**Xong khi:** chạy hết catalog không lỗi; đã ghi thời gian chạy.

---

## Bước 3 — Đặc trưng 32D cho một segment
**Đọc trước:** [01_THEORY/02_AUDIO_FEATURES](../01_THEORY/02_AUDIO_FEATURES.md), [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md), [EXTRACTION_PIPELINE](../04_PART_1/04_FEATURE_EXTRACTION/EXTRACTION_PIPELINE.md)

**Mục tiêu:** `segment_features(y, start, end) → s ∈ ℝ³²`.

**Việc cần làm** (`src/strings_mmdb/features.py`):
- [ ] Tính các đặc trưng theo frame (STFT Hann 2048/512): MFCC (14 hệ số, bỏ c0), centroid, bandwidth, rolloff 85%, ZCR, RMS, f0 (pYIN, fmin 40, fmax 4200).
- [ ] Chỉ giữ **frame active** (RMS > −40 dB so với đỉnh).
- [ ] Gộp đúng thứ tự 32 chiều như FEATURE_SET §3.
- [ ] `scripts/p03_extract_ref_features.py`: chạy trên mọi nốt `split=REF` (chỉ lấy 1.5 s đầu sau trim) → `data/cache/ref_features.npz` (ma trận N×32 + recording_id).
- [ ] Vẽ ma trận tương quan 32×32 → `reports/figures/feature_corr.png`. Nếu có cặp |r| > 0.95, quyết định bỏ chiều nào và ghi vào DESIGN_DECISIONS.
- [ ] Vẽ boxplot vài đặc trưng (centroid, f0, RMS-CV) theo nhạc cụ. Đây là **bằng chứng số cho đề mục 1, 2** (giống/khác, giá trị thông tin).

**Kiểm tra** (`tests/test_features.py`):
- [ ] Sine 440 Hz: chiều 32 ≈ log2(440) = 8.78.
- [ ] Nhiễu trắng: ZCR và centroid cao hơn nhiều so với sine.
- [ ] `y` và `0.1·y` cho vector gần như giống nhau (bất biến với độ to).
- [ ] Không có NaN/inf.

**Xong khi:** có `ref_features.npz`, hình tương quan, hình boxplot.

---

## Bước 4 — Prototype tham chiếu
**Đọc trước:** [01_THEORY/04_CLUSTERING_PROTOTYPES](../01_THEORY/04_CLUSTERING_PROTOTYPES.md), [REFERENCE_PROTOTYPES](../04_PART_1/03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md)

**Mục tiêu:** 20 prototype (4 cho mỗi nhạc cụ) và nhiệt độ τ.

**Việc cần làm** (`src/strings_mmdb/prototypes.py` + `scripts/p04_build_reference.py`):
- [ ] Fit `StandardScaler` trên `ref_features` → lưu mean/std (`scaler_seg`).
- [ ] Với từng nhạc cụ: `KMeans(n_clusters=4, n_init=20, random_state=SEED)` trên z của nhạc cụ đó.
- [ ] Đánh số P1–P4 violin, P5–P8 viola, P9–P12 cello, P13–P16 double-bass, P17–P20 guitar.
- [ ] τ = median trên mọi nốt REF của (khoảng cách bình phương tới prototype gần nhất).
- [ ] Lưu `data/models/v1/scaler_seg.npz`, `prototypes.npz`, `params.json`.
- [ ] Xuất bảng mô tả cụm: số thành viên, khoảng cao độ, tỷ lệ kỹ thuật → `reports/tables/prototypes.csv`.

**Kiểm tra:**
- [ ] Mỗi prototype có ≥ 10 thành viên.
- [ ] Gán mỗi nốt REF vào prototype gần nhất rồi lấy nhạc cụ của prototype đó: accuracy > 70%. Nếu thấp hơn, xem lại Bước 3.
- [ ] Bảng cụm có ý nghĩa: thấy cụm theo âm vực và/hoặc cụm pizz.

**Xong khi:** có model v1 và bảng mô tả 20 prototype.

---

## Bước 5 — Ghép sequence multi-note
**Đọc trước:** [SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md)

**Mục tiêu:** 500 sequence DB (100/nhạc cụ) + 100 sequence query (20/nhạc cụ), kèm ground truth.

**Việc cần làm** (`src/strings_mmdb/synth.py` + `scripts/p05_synthesize.py`):
- [ ] Chỉ dùng nốt `status=OK`; bộ kéo vĩ: technique_family = arco; guitar: pluck, harmonic (D20).
- [ ] DB lấy nốt từ `DB_POOL`; query lấy nốt từ `QUERY_POOL`. **Không bao giờ trộn.**
- [ ] Làm đúng các quy tắc ghép (số nốt, độ dài, gain, khoảng lặng/crossfade, seed cố định).
- [ ] Ghi `data/sequences/{db,query}/*.wav` và `data/ground_truth/{db,query}/*.json`.
- [ ] Ghi `data/sequences/index.csv`: `file, kind, instrument, technique_family, n_notes, duration_sec`.

**Kiểm tra:**
- [ ] Đếm 100 DB + 20 query cho mỗi nhạc cụ.
- [ ] Không bản ghi nào xuất hiện ở cả DB và query.
- [ ] Nghe thử 10 file; vẽ waveform kèm vạch ground truth cho 3 file.
- [ ] Chạy lại script với cùng seed thì ra file giống hệt (so MD5).
- [ ] Thống kê số lần dùng lại mỗi bản ghi (đặc biệt guitar), ghi vào báo cáo.

**Xong khi:** đủ 600 file + ground truth + thống kê tái dùng.

---

## Bước 6 — Segmentation
**Đọc trước:** [01_THEORY/03_ONSET_SEGMENTATION](../01_THEORY/03_ONSET_SEGMENTATION.md), [SEGMENTATION](../04_PART_1/04_FEATURE_EXTRACTION/SEGMENTATION.md)

**Mục tiêu:** `segment(y) → [(start, end), …]` đạt **onset F-measure ≥ 0.80** (dung sai ±50 ms).

**Việc cần làm** (`src/strings_mmdb/segmentation.py` + `scripts/p06_eval_segmentation.py`):
- [ ] Cài đặt 6 bước: active regions → SuperFlux → peak-picking → hợp nhất → (tùy chọn) pitch-split → hậu xử lý.
- [ ] Viết hàm `onset_f_measure(pred, truth, tol=0.05)`.
- [ ] Tune δ trên **sequence DB** (dev); **không** tune trên sequence query.
- [ ] Vẽ 3 hình waveform: vạch xanh là ground truth, vạch đỏ là dự đoán.

**Kiểm tra:**
- [ ] F ≥ 0.80 trên dev.
- [ ] Sai số trung bình |n_detected − n_true| được ghi lại.
- [ ] File lặng hoàn toàn cho 0 segment kèm thông báo lỗi; file nốt đơn guitar cho ra 1 segment.
- [ ] Không segment nào < 120 ms hoặc > 2.0 s.

**Xong khi:** δ đã chốt và ghi vào `params.json`; có bảng P/R/F.

---

## Bước 7 — Vector 52D cho mỗi file (bàn giao Phần 1)
**Đọc trước:** [FILE_LEVEL_VECTOR](../04_PART_1/03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md), [PART_1_OUTPUT_SPEC](../04_PART_1/05_OUTPUT/PART_1_OUTPUT_SPEC.md)

**Mục tiêu:** `audio_to_vector(path) → v ∈ ℝ⁵²` (cùng thông tin trung gian), áp dụng cho mọi file.

**Việc cần làm** (`src/strings_mmdb/representation.py` + `scripts/p07_build_vectors.py`):
- [ ] `match(S) → W (n×20)`, cộng thêm nốt REF gần nhất cho mỗi segment (để giải thích).
- [ ] `audio_to_vector(path)`: load_audio → segment → segment_features → match → h, μ → v. Trả về v **và** thông tin trung gian (segments, S, W).
- [ ] Chạy cho 500 DB + 100 query (và tùy chọn: 446 phrase, 154 unseen).
- [ ] Ghi `data/vectors/v1/vectors.npz` và `data/vectors/v1/intermediate/<name>.npz` đúng định dạng O6, O7 trong OUTPUT_SPEC.

**Kiểm tra** (`tests/test_representation.py`):
- [ ] `v.shape == (52,)` với mọi file, kể cả file chỉ có 1 nốt.
- [ ] `sum(h) == 1` (sai số 1e-6); mọi `h_j ≥ 0`.
- [ ] Chạy hai lần cho kết quả giống hệt nhau.
- [ ] Tính bền: chia đôi nhân tạo một segment thì h thay đổi < 0.05 (chuẩn L1).
- [ ] Tỷ lệ segment của sequence DB có prototype top-1 **đúng nhạc cụ** được ghi lại (kỳ vọng > 60%).

**Xong khi:** có đủ vector + bảng ví dụ "segment → prototype → w" cho 1 file (dùng trong báo cáo). **PHẦN 1 HOÀN THÀNH.**
