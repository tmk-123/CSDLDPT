# EXTRACTION PIPELINE — Từ file audio tới vector (code Phần 1)

## 1. Ba mức xử lý
```
FRAME (≈93 ms, hop 23 ms; chỉ trong RAM)
  └─ thống kê trên các frame active ─►  SEGMENT vector s ∈ ℝ³²   (bảng segment)
        └─ so với prototype + gộp có trọng số ─►  FILE vector v ∈ ℝ⁵²  (bàn giao Phần 2)
```
**Frame không bao giờ là một record.** Một file có hàng trăm frame nhưng chỉ có **một** vector file.

## 2. Hàm và module

| Module | Hàm | Input → Output |
|---|---|---|
| `audio_io.py` | `load_audio(path, trim=False)` | path → y (float32, 22 050 Hz, peak 0.95) |
| `features.py` | `frame_features(y)` | y → dict các mảng theo frame: mfcc (14×T), centroid, bandwidth, rolloff, zcr, rms, f0, voiced |
| `features.py` | `segment_features(y, start, end, ff=None)` | Một đoạn → s ∈ ℝ³². Nhận `ff` đã tính sẵn để không tính lại STFT cho từng segment |
| `segmentation.py` | `segment(y)` | y → [(start, end), …] |
| `representation.py` | `match(S)` | S (n×32) → Z, W (n×20), nốt REF gần nhất |
| `representation.py` | `audio_to_vector(path)` | path → v ∈ ℝ⁵² + `info` (segments, S, W, h, μ) |

## 3. Pseudocode `audio_to_vector` (HÀM DUY NHẤT cho DB và query)
```
def audio_to_vector(path, models):
    y   = load_audio(path)                         # không trim; segmentation tự xử lý lặng
    seg = segment(y)                               # [(t0, t1), ...]; rỗng → lỗi
    ff  = frame_features(y)                        # tính STFT và pYIN một lần cho cả file
    S   = [segment_features(y, t0, t1, ff) for (t0, t1) in seg]
    Z   = (S − models.mu_seg) / models.sd_seg
    D2  = ‖Z_i − P_j‖²                             # n×20
    W   = softmax(−D2 / models.tau, axis=1)
    a   = dur / dur.sum()
    h   = a @ W                                    # 20
    mu  = a @ Z                                    # 32
    return concat(h, mu), info
```

## 4. Lưu ý về hiệu năng
- pYIN chậm (khoảng 0.3–1× thời gian thực). Vì vậy tính `frame_features` **một lần cho mỗi file**, rồi cắt theo segment.
- Cache S của từng file vào `data/cache/` để chạy lại nhanh.

## 5. Tham số
Tất cả đọc từ `config.py` và `data/models/v1/params.json`. Không ghi số cứng trong code.
