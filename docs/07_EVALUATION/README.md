# 07_EVALUATION — Kế hoạch đánh giá (thực hiện sau Phần 1, 2)

> Phần 1, 2 đã có các kiểm tra riêng cho từng bước (onset F, R-tree == brute force). File này là kế hoạch đánh giá **chất lượng truy vấn** (đề mục 4c).

## 1. Ground truth
- **Chính:** relevant ⇔ **cùng nhạc cụ** với query.
- **Phân cấp (nâng cao):** rel = 2 nếu cùng nhạc cụ và cùng technique_family; rel = 1 nếu chỉ cùng nhạc cụ; 0 nếu khác. Dùng để tính nDCG@5.
- **Unseen (banjo/mandolin):** dùng **Excitation-P@5** = tỷ lệ kết quả có cơ chế **gảy** (guitar hoặc sequence pizz). Banjo và mandolin là nhạc cụ gảy, nên đây là tiêu chí kiểm chứng được.

Ví dụ: `q_cello_0007` có 100 relevant (`seq_cello_*`). Kết quả `[cello, cello, viola, cello, cello]` ⇒ P@5 = 0.8, Top-1 = 1, Hit@5 = 1, RR = 1.

## 2. Metric
| Metric | Ghi chú |
|---|---|
| **P@5** (chính) | Trung bình trên các query |
| Top-1 accuracy | Tương đương phân loại 1-NN |
| Hit@5 | Có ít nhất 1 relevant trong Top-5 |
| MRR | 1/hạng của relevant đầu tiên |
| Recall@5 | **Không dùng làm chỉ số chính**: mỗi nhạc cụ có 100 relevant nên R@5 ≤ 0.05; muốn đo recall thì dùng mAP |
| Confusion matrix | Nhạc cụ query × nhạc cụ Top-1 |
| Onset P/R/F | Segmentation, dung sai ±50 ms |
| R-tree == brute force | Phải là 100% |
| Số ứng viên / N, latency, thời gian build | Hiệu năng |

## 3. Bộ query
1. 100 QUERY sequence (con số chính thức, chạy **một lần**).
2. 446 PHRASE thật (khả năng tổng quát sang nhạc thật).
3. 154 UNSEEN (Excitation-P@5 + phân bố nhạc cụ).
4. (Tùy chọn) Nốt đơn QUERY_POOL (n = 1).

Tune tham số bằng **leave-one-out có loại trừ trên DB** ([SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md) §4).

## 4. Ablation
| Cấu hình | P@5 | Top-1 | MRR |
|---|---|---|---|
| Chỉ μ | | | |
| Chỉ h | | | |
| **h + μ (chốt)** | | | |
| Không segmentation (pooling cả file) | | | |
| Hard BoP | | | |
