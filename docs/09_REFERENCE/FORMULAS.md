# FORMULAS — Tập hợp công thức của project

## Tín hiệu
| | Công thức |
|---|---|
| MIDI → Hz | f₀ = 440 · 2^((midi − 69)/12) |
| Tên nốt → MIDI | midi = 12·(octave + 1) + pc (C = 0 … B = 11; `s` = thăng) |
| Độ phân giải tần | Δf = SR / N_FFT = 22050/2048 ≈ 10.8 Hz |
| Thời lượng frame/hop | 2048/22050 ≈ 92.9 ms; 512/22050 ≈ 23.2 ms |
| RMS dB tương đối | 20·log10(RMS[t] / max RMS) |
| Peak-normalize | y ← 0.95·y / max\|y\| |

## Đặc trưng
| | Công thức |
|---|---|
| Centroid | C = Σ f_k\|X_k\| / Σ\|X_k\| |
| Bandwidth | √(Σ (f_k − C)²\|X_k\| / Σ\|X_k\|) |
| Rolloff 85% | min f_R : Σ_{f≤f_R}\|X\|² ≥ 0.85·Σ\|X\|² |
| ZCR | (1/(N−1)) Σ 𝟙[x_n x_{n−1} < 0] |
| RMS-CV | std(RMS) / mean(RMS) |
| SuperFlux | SF(t) = Σ_f max(0, M[f,t] − max_{f'∈f±1} M[f', t−2]), M = log(1 + 10·Mel) |

## Biểu diễn
| | Công thức |
|---|---|
| z segment | z = (s − μ_seg)/σ_seg |
| Khoảng cách tới prototype | d_ij = ‖z_i − P_j‖₂ |
| Gán mềm | w_ij = exp(−d_ij²/τ) / Σ_j' exp(−d_ij'²/τ) |
| τ | median_r ( min_j ‖z_r − P_j‖² ) trên REF |
| Trọng số thời lượng | α_i = dur_i / Σ dur |
| Histogram | h_j = Σ_i α_i w_ij |
| Trung bình | μ = Σ_i α_i z_i |
| Vector file | v = [h ‖ μ] ∈ ℝ⁵² |

## Chuẩn hóa, PCA, tìm kiếm
| | Công thức |
|---|---|
| scaler_file | x = (v − mean_DB) / std_DB |
| Cân bằng khối | v' = [x₁..₂₀/√20 ‖ x₂₁..₅₂/√32] |
| PCA | u = Wᵀ(v' − m), W ∈ ℝ^{52×8}, WᵀW = I |
| Cận dưới | ‖u_a − u_b‖ ≤ ‖v'_a − v'_b‖ |
| Khoảng cách | d = ‖v'_q − v'_x‖₂ |
| Similarity hiển thị | sim = 1/(1 + d) |
| Điều kiện dừng k-NN | D(top₅) ≤ r8 |
| MINDIST | √Σᵢ (max(lo_i − q_i, 0, q_i − hi_i))² |

## Đánh giá
| | Công thức |
|---|---|
| P@5 | #relevant trong Top-5 / 5 |
| MRR | (1/\|Q\|) Σ_q 1/rank_q |
| Onset F | 2PR/(P + R), dung sai ±50 ms |
| Fisher ratio (một chiều) | Σ_c n_c(μ_c − μ)² / Σ_c Σ_{i∈c} (x_i − μ_c)² |
