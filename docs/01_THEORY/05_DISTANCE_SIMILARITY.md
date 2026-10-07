# 05. DISTANCE & SIMILARITY

## 1. Độ đo
| Độ đo | Công thức | Tính chất |
|---|---|---|
| Euclid (L2) | √Σ(qᵢ − vᵢ)² | Metric; nhạy với thang đo; tương thích với R-tree (MINDIST) |
| Manhattan (L1) | Σ\|qᵢ − vᵢ\| | Metric; ít nhạy với ngoại lai hơn L2 |
| Cosine similarity | Q·V / (‖Q‖‖V‖) ∈ [−1, 1] | Chỉ đo **hướng**, bỏ qua độ lớn |

Liên hệ: nếu ‖Q‖ = ‖V‖ = 1 thì ‖Q − V‖² = 2 − 2·cos(Q, V). Khi đó xếp hạng theo L2 và theo cosine trùng nhau.

## 2. Chuẩn hóa
| Kỹ thuật | Công thức | Ghi chú |
|---|---|---|
| Z-score | (x − μ)/σ | Mean 0, std 1; dùng μ, σ của tập fit |
| Min-Max | (x − min)/(max − min) | Nhạy ngoại lai |
| L2-normalize | v/‖v‖ | Đưa vector lên mặt cầu đơn vị |

**Tại sao cần:** nếu một chiều có thang lớn hơn chiều khác 10⁴ lần, khoảng cách gần như chỉ phản ánh chiều đó.

**Quy tắc vàng:** μ, σ (và mọi tham số chuẩn hóa khác) chỉ được **fit trên tập dữ liệu tham chiếu**, rồi áp dụng nguyên vẹn cho query.

## 3. Ví dụ 3D
Q = (0.5, −1, 2), V1 = (1, −0.5, 1), V2 = (−0.5, −1, 2.5), V3 = (1, −2, 4) = 2Q.

| | Euclid | Manhattan | Cosine |
|---|---|---|---|
| Q–V1 | √1.5 = 1.225 | 2.0 | 3.0/(2.291·1.5) = 0.873 |
| Q–V2 | √1.25 = 1.118 | 1.5 | 5.75/(2.291·2.739) = 0.916 |
| Q–V3 | √5.25 = 2.291 | 3.5 | **1.000** |

V1 và V2 được cả ba độ đo xếp cùng thứ tự. V3 cho thấy khác biệt: cosine coi V3 "giống hệt" Q, còn Euclid coi V3 xa nhất.

## 4. k-NN và Top-K
**k-NN:** tìm k điểm có khoảng cách nhỏ nhất tới q. Brute force: tính N khoảng cách rồi sắp xếp, chi phí O(N·d). Chỉ mục (R-tree, k-d tree) giúp tránh tính hết N khoảng cách.

## 5. Đánh giá truy vấn (để biết)
Precision@K = (#relevant trong Top-K)/K · Recall@K = (#relevant trong Top-K)/(#relevant) · MRR = trung bình của 1/hạng của relevant đầu tiên.
