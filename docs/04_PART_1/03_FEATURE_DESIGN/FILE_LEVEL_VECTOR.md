# FILE-LEVEL VECTOR — Một file → MỘT vector 52D

> Quyết định: D11, D12. Lý thuyết bag-of-prototypes: [04_CLUSTERING_PROTOTYPES](../../01_THEORY/04_CLUSTERING_PROTOTYPES.md).

## 1. Các phương án gộp S₁…Sₙ thành vector cố định

| PA | Cách làm | Số chiều | Kết luận |
|---|---|---|---|
| A. Concatenate | [S₁‖…‖Sₙ] | 32·n (thay đổi theo file) | **Loại**: không cố định chiều; padding làm "segment 3 của file A" bị so với "segment 3 của file B", vô nghĩa |
| B. Mean/Std pooling | Trung bình có trọng số | 32 | **Giữ**: đơn giản, bền; nhưng không dùng reference và mất phân bố |
| C. Hard Bag-of-Prototypes | Đếm prototype gần nhất | 20 | Dùng để **giải thích**; không ổn định ở biên giữa hai cụm |
| D. Histogram theo nhạc cụ | 5 bin | 5 | **Loại**: quá thô, mọi file violin ≈ [1,0,0,0,0] |
| E. Soft BoP (gán mềm, trọng số thời lượng) | Softmax khoảng cách | 20 | **CHỌN** |
| F. VLAD/Fisher | Cộng dồn phần dư | 640 | **Loại**: quá nhiều chiều cho R-tree |
| G. Sequence (DTW/HMM) | So khớp chuỗi | Không cố định | **Loại**: không có vector cố định, không đưa được vào R-tree |

**CHỐT: v = [ h (E, 20D) ‖ μ (B, 32D) ] = 52D.**
- `h`: file phân bố ra sao giữa các kiểu âm sắc đã biết. Đây là phần dùng reference.
- `μ`: âm sắc trung bình tuyệt đối. Vẫn có nghĩa khi query là nhạc cụ lạ.

## 2. Công thức
File có n segment; segment i có thời lượng dur_i và vector s_i.
```
z_i  = (s_i − μ_seg) / σ_seg                          scaler REF, KHÔNG fit lại
d_ij = ‖z_i − P_j‖₂                                    j = 1..20
w_ij = exp(−d_ij²/τ) / Σ_j' exp(−d_ij'²/τ)            softmax; Σ_j w_ij = 1
α_i  = dur_i / Σ_k dur_k                               Σ_i α_i = 1
h_j  = Σ_i α_i · w_ij                                  h ∈ ℝ²⁰, Σ h_j = 1
μ    = Σ_i α_i · z_i                                   μ ∈ ℝ³²
v    = [h ‖ μ] ∈ ℝ⁵²
```
(Tính softmax nên trừ đi min d² trước khi lấy exp để tránh tràn số.)

## 3. Ví dụ số (10 prototype, 5 segment)

| Seg | Dur | Gần nhất | Sim |
|---|---|---|---|
| S1 | 0.6 s | P3 | 0.91 |
| S2 | 0.4 s | P3 | 0.87 |
| S3 | 1.0 s | P7 | 0.95 |
| S4 | 0.5 s | P3 | 0.89 |
| S5 | 0.5 s | P9 | 0.92 |

- **Hard count:** `[0,0,3,0,0,0,1,0,1,0]` → chuẩn hóa `[0,0,0.6,0,0,0,0.2,0,0.2,0]`
- **Similarity-weighted:** P3 = 2.67, P7 = 0.95, P9 = 0.92 (tổng 4.54) → `[0,0,0.588,0,0,0,0.209,0,0.203,0]`
- **Duration-weighted:** tổng 3.0 s → P3 = 0.50, P7 = 0.333, P9 = 0.167
- **Soft + duration (CHỐT).** Giả sử phân bố softmax như sau:

| Seg | α | w (các giá trị đáng kể) |
|---|---|---|
| S1 | 0.200 | P3: 0.70 · P4: 0.20 · P1: 0.10 |
| S2 | 0.133 | P3: 0.60 · P4: 0.30 · P7: 0.10 |
| S3 | 0.333 | P7: 0.80 · P8: 0.15 · P3: 0.05 |
| S4 | 0.167 | P3: 0.75 · P4: 0.25 |
| S5 | 0.167 | P9: 0.85 · P10: 0.15 |

```
h1 = 0.020   h3 = 0.140+0.080+0.017+0.125 = 0.362   h4 = 0.040+0.040+0.042 = 0.122
h7 = 0.013+0.267 = 0.280   h8 = 0.050   h9 = 0.142   h10 = 0.025
h  = [0.020, 0, 0.362, 0.122, 0, 0, 0.280, 0.050, 0.142, 0.025]   (Σ ≈ 1)
```
Nếu P1–P4 là violin, P5–P8 là viola, P9–P10 là cello, ta đọc được: **"≈ 50% violin-like, 33% viola-like, 17% cello-like"**.

**Hard vs soft ở sát biên:** d(P3) = 1.01 và d(P4) = 1.00. Hard: trọn vào P4, nhiễu nhẹ là nhảy sang P3 (thay đổi 1.0). Soft: P3 ≈ 0.49, P4 ≈ 0.51 (thay đổi khoảng 0.01).

## 4. Vì sao mọi file có cùng 52 chiều
- Số chiều của h = **số prototype (20)**, cố định từ Bước 4. Số chiều của μ = **số đặc trưng (32)**, cố định theo thiết kế.
- File dài hay ngắn, nhiều hay ít nốt chỉ thay đổi **số hạng trong tổng Σᵢ**. Tổng luôn ra 20 + 32 số, và Σα = 1 khử ảnh hưởng của độ dài.
- File 1 nốt (n = 1) là trường hợp hợp lệ.

## 5. Vì sao chịu được lỗi segmentation
- **Chia thừa:** một nốt 1.2 s bị chia làm 3 mảnh vẫn chỉ đóng góp 1.2 s (nhờ α); các mảnh có w gần nhau ⇒ h gần như không đổi.
- **Gộp sót (legato):** segment gộp có z ≈ trung bình hai nốt cùng nhạc cụ, nên vẫn gần các prototype của nhạc cụ đó.
- **Không phụ thuộc thứ tự nốt:** chủ đích, vì ta tìm theo âm sắc chứ không theo giai điệu.
