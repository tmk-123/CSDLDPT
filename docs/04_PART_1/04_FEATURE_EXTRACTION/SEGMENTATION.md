# SEGMENTATION — Tách multi-note thành các đoạn xấp xỉ một nốt

> Lý thuyết: [03_ONSET_SEGMENTATION](../../01_THEORY/03_ONSET_SEGMENTATION.md). Quyết định: D09.

## 1. Mục tiêu
Không phải phiên âm chính xác. Mục tiêu là chia file thành các đơn vị **gần với một nốt** để so được với thư viện nốt đơn. Vector file ([FILE_LEVEL_VECTOR](../03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md) §5) được thiết kế để chịu lỗi chia thừa hoặc gộp sót.

## 2. So sánh phương án
| Phương pháp | Dùng? | Lý do |
|---|---|---|
| Energy-based (RMS) | **Có**, bước 1 | Tách được nốt có lặng xen giữa; loại phần lặng. Không tách được legato |
| Spectral flux thô | Không | Audit thực tế: một nốt kéo vĩ cho 3–5 onset **giả** (do vibrato) |
| **SuperFlux** | **Có**, lõi | Spectral flux có max-filter theo tần số, được thiết kế để khử onset giả do vibrato |
| HPSS | Không | Dữ liệu đơn nhạc cụ, không có nguồn gõ cần tách |
| Pitch tracking | Tùy chọn (nâng cao) | Bắt được legato; chậm, có lỗi quãng tám |

## 3. Thuật toán chốt
```
INPUT  y (mono, 22 050 Hz, peak-normalized)    OUTPUT [(start, end), ...]

1. ACTIVE REGIONS: rms_db[t] = 20·log10(RMS[t]/max RMS); active = rms_db > −40 dB
   gộp các vùng cách nhau < 50 ms; bỏ vùng < 120 ms
2. SUPERFLUX: M = log(1 + 10·Mel(y; 2048, 512, 128 band))
   Mmax = maximum_filter(M, size=3 theo tần số)
   flux[t] = Σ_f max(0, M[f,t] − Mmax[f,t−2]);  chuẩn hóa về [0, 1]
3. PEAK PICKING: t là onset nếu
   flux[t] = max(flux[t−3..t+3])                   (±70 ms)
   flux[t] ≥ mean(flux[t−10..t+10]) + δ            (δ ≈ 0.1, tune ở Bước 6)
   cách onset trước ≥ 100 ms
   backtrack về cực tiểu RMS ngay trước đó
4. HỢP NHẤT: boundaries = {đầu mỗi vùng active} ∪ {onset trong vùng active}
   segment k = [b_k, min(b_{k+1}, cuối vùng active))
5. (tùy chọn) PITCH SPLIT trong segment > 0.8 s: median f₀ đổi > 0.8 semitone, giữ ≥ 60 ms
6. HẬU XỬ LÝ:
   < 120 ms             → gộp vào segment trước (cần khoảng 5 frame để tính std)
   > 2.0 s              → chặt đều thành các khúc ≤ 1.0 s
   mean rms_db < −35 dB → bỏ
   0 segment            → lỗi "không phát hiện âm thanh"
```
Trong librosa, bước 2–3 tương ứng với `librosa.onset.onset_strength(..., lag=2, max_size=3)` và `librosa.onset.onset_detect(..., backtrack=True)`.

## 4. Ví dụ
```
Audio:  |----A----|----B----|-------C-------|---D---|....lặng....
        0.00     0.72      1.41            2.56    3.21
Bước 1: active = [0.00, 3.21]
Bước 2–3: onset 0.00, 0.72, 1.41, 2.56  (đỉnh vibrato nhỏ ở 1.95 không vượt δ → loại)
Bước 4: seg1 [0.00,0.72) · seg2 [0.72,1.41) · seg3 [1.41,2.56) · seg4 [2.56,3.21)
→ 4 segment. Mốc 3.21 là điểm kết thúc (offset), không phải onset.
```

## 5. Giới hạn (KHÔNG đảm bảo mỗi segment = một nốt)
| Tình huống | Điều xảy ra | Chấp nhận? |
|---|---|---|
| Legato | 2 nốt gộp thành 1 | Có; âm sắc vẫn đúng nhạc cụ; luật chặt > 2 s giảm thiểu |
| Hai nốt chồng (vang, double-stop) | Segment chứa 2 nốt | Có; median f₀ giảm ảnh hưởng |
| Vibrato, tremolo, trill | Có thể chia thừa | Có; SuperFlux + min-IOI + α giảm thiểu |
| Nhiễu, lặng | Segment rác | Bỏ segment < −35 dB |

## 6. Đo lường (Bước 6)
- **Onset P/R/F**, dung sai ±50 ms, mỗi onset dự đoán khớp tối đa một onset thật. Mục tiêu **F ≥ 0.80**.
- Sai số số nốt |n_detected − n_true|.
- Tune δ trên **sequence DB**; báo cáo trên **sequence query**.
