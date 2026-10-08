# DATA FLOW — Script nào đọc gì, ghi gì

| Script | Đọc | Ghi | Bước |
|---|---|---|---|
| `p01_1_download_iowa.py` | Trang web Iowa MIS | `raw/iowa_mis/<instrument>/*.aiff`, `_download/manifest.csv` | 1.1 |
| `p01_2_slice_iowa.py` | `raw/iowa_mis/**/*.aif(f)` | `data/interim/iowa_notes/<instrument>/*.wav`, `notes.csv`, `slice_report.csv` | 1.2 |
| `p01_3_build_catalog.py` | `raw/philharmonia/**/*.mp3`, `data/interim/iowa_notes/` | `data/catalog.csv`, `data/notes/`, `data/queries/`, `data/excluded/` | 1.3–1.5 |
| `p01_6_dataset_stats.py` | `data/catalog.csv`, `data/interim/iowa_notes/slice_report.csv` | `reports/dataset/dataset_stats.md`, `*.csv`, `notes_by_instrument.png`, `pitch_coverage.png` | 1.6 |
| `theory_figures.py` | `data/catalog.csv`, file âm thanh trong `data/` | `reports/theory/*.png` (16 hình), `reports/theory/*.csv` (số đo cho `docs/01_THEORY/`) | lý thuyết |
| `p02_check_audio.py` | `catalog.csv` | `data/logs/audio_check.csv` | 2 |
| `p03_extract_ref_features.py` | `catalog.csv` (REF), mp3 | `data/cache/ref_features.npz`, `reports/figures/feature_corr.png`, `features_by_instrument.png` | 3 |
| `p04_build_reference.py` | `ref_features.npz` | `data/models/v1/scaler_seg.npz`, `prototypes.npz`, `ref_index.npz`, `params.json`; `reports/tables/prototypes.csv` | 4 |
| `p05_synthesize.py` | `catalog.csv` (DB_POOL, QUERY_POOL), mp3 | `data/sequences/{db,query}/*.wav`, `data/sequences/index.csv`, `data/ground_truth/{db,query}/*.json` | 5 |
| `p06_eval_segmentation.py` | sequences + ground truth | `params.json` (δ), `reports/tables/segmentation.csv`, hình waveform | 6 |
| `p07_build_vectors.py` | sequences (+ phrase, unseen), models v1 | `data/vectors/v1/vectors.npz`, `intermediate/*.npz` | 7 |
| `p08_load_db.py` | Toàn bộ ở trên | `data/mmdb.sqlite` | 8 |
| `p09_fit_reduction.py` | `mmdb.sqlite` (v_raw của DB) | `data/models/v1/scaler_file.npz`, `pca.npz`; cột `v_norm`, `u_pca` | 9 |
| `p10_build_index.py` | `mmdb.sqlite` (u_pca, in_index = 1) | `data/index/rtree_v1.{dat,idx}` | 10 |
| `p11_query.py` | File query, models, sqlite, rtree | stdout; `reports/queries/<tên>/` nếu `--save-figs` | 11 |

## Quy tắc
- `raw/philharmonia/` **chỉ đọc**.
- Mọi thứ trong `data/` tạo lại được bằng cách chạy lần lượt p01 → p10 (seed cố định).
- `reports/` là nơi lấy hình và bảng cho báo cáo.

Mức chi tiết hàm (hàm nào, tham số gì): [IMPLEMENTATION](IMPLEMENTATION.md).
