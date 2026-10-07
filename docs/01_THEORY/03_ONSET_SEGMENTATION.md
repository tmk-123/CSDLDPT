# 03. ONSET DETECTION & SEGMENTATION

## 1. Onset là gì
**Onset** là thời điểm bắt đầu một nốt (khởi đầu pha attack). **Offset** là thời điểm nốt kết thúc. Segmentation chia tín hiệu tại các onset (và các khoảng lặng).

## 2. Khung chung
```
tín hiệu → hàm "độ mạnh onset" (Onset Detection Function, ODF) → chọn đỉnh (peak picking) → các mốc onset
```

## 3. Các ODF
| ODF | Ý tưởng | Hợp với | Yếu ở |
|---|---|---|---|
| **Năng lượng** | RMS tăng đột ngột | Âm gảy, có lặng xen giữa | Nốt liền nhau (legato) |
| **Spectral flux** | Tổng mức **tăng** biên độ phổ giữa hai frame liên tiếp (chỉ lấy phần dương) | Nốt mới làm xuất hiện bồi âm mới | **Vibrato**: bồi âm dịch tần liên tục ⇒ flux dương giả |
| **SuperFlux** (Böck & Widmer, 2013) | Spectral flux trên log-Mel, nhưng so với **max-filter theo tần số** của frame cách đó μ frame: SF(t) = Σ_f max(0, M[f,t] − max_{f'∈f±1} M[f', t−μ]) | Nhạc cụ có vibrato (bộ dây kéo vĩ) | Cần tinh chỉnh ngưỡng |
| **Phase / complex domain** | Độ lệch pha dự đoán | Onset mềm | Phức tạp hơn |
| **Pitch change** | f₀ thay đổi ổn định | Legato | Chậm, lỗi quãng tám |

**Tại sao SuperFlux khử được vibrato:** khi vibrato làm một bồi âm dịch sang bin bên cạnh, max-filter theo tần số đã "phủ" bin đó ở frame trước, nên phép trừ không còn dương.

## 4. Peak picking thích nghi
Frame t là onset nếu cả ba điều kiện cùng đúng:
1. **Cực đại cục bộ:** ODF[t] = max trong cửa sổ ±w₁.
2. **Vượt ngưỡng thích nghi:** ODF[t] ≥ mean trong cửa sổ ±w₂ + δ.
3. **Cách onset trước** ít nhất một khoảng tối thiểu (min inter-onset interval).

**Backtrack:** dời onset về cực tiểu năng lượng ngay trước đỉnh, để trùng điểm bắt đầu attack.

## 5. HPSS
Tách spectrogram thành phần **harmonic** (vạch ngang, bền theo thời gian) và **percussive** (vạch dọc, tức thời) bằng median filter hai chiều. Hữu ích khi có trống hoặc tiếng gõ chồng lên nhạc.

## 6. Đánh giá onset
So mỗi onset dự đoán với onset thật trong dung sai ±50 ms (khớp một-một):
- Precision = TP / số dự đoán; Recall = TP / số onset thật; F = 2PR/(P + R).
