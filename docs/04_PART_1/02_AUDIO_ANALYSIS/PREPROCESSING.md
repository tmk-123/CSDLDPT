# PREPROCESSING

> Lý thuyết: [12_DIGITAL_AUDIO](../../01_THEORY/12_DIGITAL_AUDIO.md), [14_FFT_STFT_SPECTRUM](../../01_THEORY/14_FFT_STFT_SPECTRUM.md). Lý do lựa chọn: [DESIGN_DECISIONS](../../08_AI_CONTEXT/DESIGN_DECISIONS.md) D04–D06, D27.

## 1. Chuỗi xử lý (hàm `load_audio`)
```
file (mp3/wav/flac/ogg)
 → decode (librosa/ffmpeg)
 → mono (trung bình các kênh)
 → resample 22 050 Hz
 → float32 trong [-1, 1]
 → lọc thông cao 25 Hz (Butterworth bậc 4, sosfiltfilt) — D27
 → peak-normalize: y ← 0.95 · y / max|y|
 → [chỉ với nốt đơn] trim lặng đầu/cuối, top_db = 40
 → [chỉ với REF] giữ tối đa 1.5 s đầu
```

## 2. Bảng quyết định

| Câu hỏi | Quyết định | Lý do ngắn |
|---|---|---|
| Normalize? | Peak-normalize 0.95 | Mức thu âm tuyệt đối không phụ thuộc nhạc cụ; giúp ngưỡng segmentation ổn định |
| Mono? | Có | Dataset đã mono; query người dùng có thể stereo |
| Sample rate? | **22 050 Hz cho mọi file** | Đủ cho MFCC/Mel; nhanh gấp 2. Quan trọng nhất là DB và query **cùng SR** |
| Silence trimming? | Có với nốt đơn (−40 dB) | Lặng làm lệch mean/std. Multi-note xử lý lặng trong segmentation |
| Lọc tiếng ù hạ âm? | **Có**: thông cao 25 Hz, trước khi chuẩn hóa đỉnh (D27) | Tiếng ù dưới 20 Hz chiếm phần lớn năng lượng ở nhiều bản thu (guitar Iowa: trung vị 92.8%), làm sai đỉnh, phần có âm và mọi đặc trưng năng lượng. C1 = 32.7 Hz chỉ yếu đi khoảng 1 dB. Phải lọc **trước** chuẩn hóa đỉnh, nếu không đỉnh có thể là tiếng ù |
| Pre-emphasis? | **Không** | Là quy ước của xử lý tiếng nói; độ dốc phổ ở đây chính là thông tin âm sắc |
| Frame length | 2048 mẫu ≈ 93 ms | Nốt E1 (41 Hz) có chu kỳ 24 ms; cần ≥ 3 chu kỳ/frame |
| Hop length | 512 mẫu ≈ 23 ms | Đủ mịn cho dung sai onset ±50 ms |
| Window | Hann | Giảm rò rỉ phổ; chuẩn của librosa |
| STFT | Có | Nguồn của mọi đặc trưng phổ |

## 3. Vì sao REF chỉ lấy 1.5 s đầu
Segment trong multi-note thường là **phần đầu** của nốt (0.35–1.2 s). Nếu REF dùng cả nốt (có thể dài tới 25 s) thì phân phối đặc trưng hai phía sẽ lệch nhau. Giới hạn 1.5 s giúp "nốt REF" và "segment" trông giống nhau.

## 4. Kiểm tra
Xem Bước 2 trong [PART_1_PLAN](../../02_PLANS/PART_1_PLAN.md).
