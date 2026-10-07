# MASTER PLAN — Phương án chính đã chốt

> Đây là "hợp đồng thiết kế". Muốn đổi bất kỳ dòng nào, phải ghi vào [DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md) trước.

## 1. Phương án chính (INPUT → ALGORITHM → OUTPUT)

| # | Bước | INPUT | ALGORITHM | OUTPUT | Phần |
|---|---|---|---|---|---|
| 1 | Dataset | 4 477 MP3 | Parse tên file, ffprobe, MD5, lọc lỗi; split theo cao độ mod 5; ghép sequence | Catalog; 500 DB + 100 query WAV kèm ground truth | P1 |
| 2 | Preprocessing | File audio | Decode → mono → 22 050 Hz → peak-normalize 0.95 (→ trim với nốt đơn) | y (float32) | P1 |
| 3 | Reference | ~1 360 nốt REF | Đặc trưng 32D → scaler_seg → K-means k = 4 mỗi nhạc cụ | 20 prototype + τ | P1 |
| 4 | Feature extraction | y + một segment | STFT Hann 2048/512 → MFCC c1–13 mean+std, log centroid/bandwidth/rolloff, ZCR, RMS-CV, median log2 f0 | s ∈ ℝ³² | P1 |
| 5 | Segmentation | y | Energy gating −40 dB + SuperFlux + peak-picking + hậu xử lý | n segment | P1 |
| 6 | Reference matching | {s_i}, P, τ | z = scaler_seg(s); w_ij = softmax(−‖z_i − P_j‖²/τ) | W (n×20) | P1 |
| 7 | Fixed-length vector | W, z, dur | h = Σα·w, μ = Σα·z | v ∈ ℝ⁵² | P1 |
| 8 | Lưu trữ | v + metadata | SQLite (BLOB float32) | mmdb.sqlite | P2 |
| 9 | Normalization | v | scaler_file (fit trên DB) + chia khối √20, √32 | v' ∈ ℝ⁵² | P2 |
| 10 | PCA | v' | PCA 8D, fit trên DB, không whitening | u ∈ ℝ⁸ | P2 |
| 11 | R-tree | 500 điểm u | R\*-tree, M = 10 | rtree_v1 | P2 |
| 12 | Similarity + Top-5 | u_q, v'_q | Multi-step exact k-NN, Euclid 52D | 5 audio_id + d | P2 |
| 13 | Đánh giá | các tập query | P@5, Top-1, MRR, onset F | Bảng số liệu | sau |

## 2. Công nghệ
Python · numpy/scipy · **librosa** (STFT, Mel, MFCC, pYIN, onset) · **scikit-learn** (StandardScaler, KMeans, PCA) · **rtree** (libspatialindex) · **sqlite3** (có sẵn) · ffmpeg. Demo sau này dùng Streamlit.

## 3. Cấu trúc code dự kiến (chỉ Phần 1, 2)

```
BTL/
├── requirements.txt
├── .gitignore                  # data/, .venv/, __pycache__/
├── src/strings_mmdb/
│   ├── config.py               # Bước 0
│   ├── catalog.py              # Bước 1
│   ├── audio_io.py             # Bước 2
│   ├── features.py             # Bước 3
│   ├── prototypes.py           # Bước 4
│   ├── synth.py                # Bước 5
│   ├── segmentation.py         # Bước 6
│   ├── representation.py       # Bước 7  ← audio_to_vector(): HÀM DUY NHẤT cho DB và query
│   ├── db.py                   # Bước 8
│   ├── reduction.py            # Bước 9
│   ├── index_rtree.py          # Bước 10
│   └── search.py               # Bước 10–11
├── scripts/p01_… → p11_…       # mỗi bước một script
├── tests/                      # mỗi module một file test
└── data/                       # mọi thứ sinh ra (xóa đi tạo lại được)
```

## 4. Kế hoạch chi tiết
- [PART_1_PLAN.md](PART_1_PLAN.md): Bước 0 → 7.
- [PART_2_PLAN.md](PART_2_PLAN.md): Bước 8 → 11.
- [MILESTONES.md](MILESTONES.md): mốc và checklist.
