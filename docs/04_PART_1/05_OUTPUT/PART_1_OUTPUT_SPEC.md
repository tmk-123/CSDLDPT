# PART 1 OUTPUT SPEC — Hợp đồng bàn giao Phần 1 → Phần 2

> Phần 2 **chỉ đọc** các sản phẩm dưới đây. Đổi định dạng ⇒ phải sửa file này và ghi vào DESIGN_DECISIONS.

## 1. Danh sách sản phẩm

| # | Đường dẫn | Định dạng | Nội dung |
|---|---|---|---|
| O1 | `data/catalog.csv` | CSV UTF-8 | 4 477 dòng; cột: `recording_id, rel_path, instrument, note, midi, duration_label, dynamics, technique, technique_family, duration_sec, sample_rate, channels, md5, status, split` |
| O2 | `data/sequences/{db,query}/*.wav` | WAV 22 050 Hz mono 16-bit | 500 DB + 100 query |
| O3 | `data/sequences/index.csv` | CSV | `file, kind (db/query), instrument, technique_family, n_notes, duration_sec` |
| O4 | `data/ground_truth/{db,query}/*.json` | JSON | Xem [SEQUENCE_SYNTHESIS](../01_DATASET/SEQUENCE_SYNTHESIS.md) §3 |
| O5 | `data/models/v1/` | `.npz` + `params.json` | `scaler_seg.npz`, `prototypes.npz`, `ref_index.npz`, `params.json` (SR, n_fft, hop, k, τ, δ, …) |
| O6 | `data/vectors/v1/vectors.npz` | NumPy | `names` (N,) tên file · `kind` (N,) · `V` (N×52, float32) |
| O7 | `data/vectors/v1/intermediate/<name>.npz` | NumPy | `segments` (n×2, giây) · `S` (n×32) · `W` (n×20) · `nearest_ref` (n,) recording_id · `nearest_ref_dist` (n,) |

## 2. Bất biến (invariant) Phần 2 được phép tin cậy
- `V.shape[1] == 52`; cột 0–19 là `h` (≥ 0, tổng mỗi dòng = 1 ± 1e-6); cột 20–51 là `μ` (đã z-score theo **scaler_seg**, **chưa** qua scaler_file).
- Không có NaN/inf.
- Thứ tự prototype: P1–P4 violin, P5–P8 viola, P9–P12 cello, P13–P16 double-bass, P17–P20 guitar.
- Mọi vector được tạo bởi **cùng** `audio_to_vector()` với cùng `model_version = v1`.
- Không bản ghi nốt nào được dùng chung giữa sequence DB và sequence query.

## 3. Phần 2 tự làm (KHÔNG thuộc Phần 1)
`scaler_file`, cân bằng khối, PCA, R-tree, CSDL, tìm kiếm.

## 4. Giao diện hàm Phần 2 sẽ gọi cho query mới
```python
from strings_mmdb.representation import audio_to_vector
v, info = audio_to_vector("query.wav")   # v: (52,) float32; info: segments, S, W, h, mu, nearest_ref
```
