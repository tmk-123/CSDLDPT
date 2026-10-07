# 02. AUDIO FEATURES

Ký hiệu: |X[k]| là biên độ phổ của bin k trong một frame, f[k] là tần số của bin k.

| Đặc trưng | Công thức | Đo gì |
|---|---|---|
| **RMS** | √( (1/N) Σ x[n]² ) | Năng lượng, độ to |
| **ZCR** | (1/(N−1)) Σ 𝟙[x[n]·x[n−1] < 0] | Tần suất đổi dấu: độ "nhiễu"/cao tần |
| **Spectral Centroid** | C = Σ f[k]·\|X[k]\| / Σ \|X[k]\| | "Trọng tâm" phổ: **độ sáng** |
| **Spectral Bandwidth** | √( Σ (f[k] − C)²·\|X[k]\| / Σ \|X[k]\| ) | Độ trải phổ quanh centroid |
| **Spectral Rolloff** | f_R nhỏ nhất sao cho Σ_{f ≤ f_R} \|X\|² ≥ 0.85·Σ \|X\|² | Giới hạn trên của phần lớn năng lượng |
| **MFCC** | STFT → \|X\|² → bộ lọc Mel → log → DCT-II → c₀, c₁, … | **Hình bao phổ** (âm sắc). c₀ ≈ log năng lượng tổng; c₁, c₂… mô tả độ dốc và hình dạng phổ |
| **Chroma** | Gộp năng lượng phổ vào 12 lớp cao độ (C…B), bỏ quãng tám | Hòa âm, giai điệu |
| **f₀ (YIN/pYIN)** | Tìm chu kỳ τ làm cực tiểu hàm sai khác d(τ) = Σ (x[n] − x[n+τ])². pYIN thêm xác suất và HMM để quyết định voiced/unvoiced | Cao độ |
| **Spectral flux** | Σ_k max(0, \|X[k,t]\| − \|X[k,t−1]\|) | Mức thay đổi phổ (dùng cho onset) |

## Từ frame tới vector
Mỗi đặc trưng cho ra **một chuỗi theo thời gian**. Để có vector cố định, ta **tổng hợp (aggregate)** chuỗi đó bằng thống kê:
- **mean:** giá trị điển hình;
- **std:** mức biến thiên (vibrato, tắt dần);
- **median:** bền với ngoại lai;
- **hệ số biến thiên CV = std/mean:** bất biến khi nhân tín hiệu với hằng số.

## Tính bất biến (invariance)
| Biến đổi | Đặc trưng **không đổi** | Đặc trưng **đổi** |
|---|---|---|
| Nhân biên độ ×a | Centroid, bandwidth, rolloff, ZCR, MFCC c₁+, CV(RMS), f₀ | RMS, c₀ |
| Đổi cao độ | (gần như) hình bao phổ lý tưởng | f₀, centroid, rolloff |
| Đổi sample rate | — | **Gần như tất cả** ⇒ phải thống nhất SR |

## Dư thừa
Centroid, rolloff, bandwidth và MFCC c₁ thường tương quan mạnh. Cách kiểm tra: ma trận tương quan Pearson; |r| > 0.95 nghĩa là gần như cùng thông tin.
