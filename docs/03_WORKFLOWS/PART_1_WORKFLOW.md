# PART 1 WORKFLOW

## 1. Luồng offline (chạy một lần, theo thứ tự)
```
[p01_1_download_iowa]    web Iowa MIS ──────────────────► raw/iowa_mis/<nhạc cụ>/*.aiff
[p01_2_slice_iowa]       raw/iowa_mis/ ─────────────────► data/interim/iowa_notes/ (nốt đơn Iowa)
[p01_3_build_catalog]    raw/philharmonia/ + interim ───► data/catalog.csv, data/notes/, data/queries/, data/excluded/
[p01_6_dataset_stats]    catalog ───────────────────────► reports/dataset/ (bảng + biểu đồ mô tả dataset)
[p02_check_audio]        catalog (OK) ─────────────────► log thời gian, danh sách lỗi
[p03_extract_ref_features] catalog (REF) ──────────────► data/cache/ref_features.npz, hình tương quan, boxplot
[p04_build_reference]    ref_features ──────────────────► data/models/v1/{scaler_seg, prototypes, ref_index}.npz
[p05_synthesize]         catalog (DB_POOL, QUERY_POOL) ─► data/sequences/{db,query}/*.wav, data/ground_truth/**.json
[p06_eval_segmentation]  sequences db + ground truth ───► δ chốt (params.json), bảng P/R/F
[p07_build_vectors]      sequences + models v1 ─────────► data/vectors/v1/vectors.npz, intermediate/*.npz
```

## 2. Luồng xử lý MỘT file (bên trong `audio_to_vector`)
```
file.wav
 │ load_audio
 ▼
y: 22 050 mẫu/giây, mono, peak 0.95
 │ segment(y)
 ▼
[(0.00, 0.72), (0.72, 1.41), (1.41, 2.56), (2.56, 3.21)]          n = 4
 │ frame_features(y) một lần → cắt theo segment → thống kê
 ▼
S: 4 × 32
 │ z = (S − μ_seg)/σ_seg ; d² tới 20 prototype ; softmax(−d²/τ)
 ▼
W: 4 × 20 (mỗi dòng tổng = 1)
 │ α = dur/Σdur ; h = αᵀW ; μ = αᵀZ
 ▼
v = [h (20) ‖ μ (32)] = 52 số
```

## 3. Phụ thuộc giữa các bước
| Bước | Cần có trước |
|---|---|
| 2 load_audio | 1 (để biết file nào OK) |
| 3 features | 2 |
| 4 prototypes | 3 |
| 5 synth | 1, 2 |
| 6 segmentation | 5 (cần ground truth để đo) |
| 7 vectors | 4, 6 |

Bước 4 và 5 độc lập với nhau, có thể làm song song.
