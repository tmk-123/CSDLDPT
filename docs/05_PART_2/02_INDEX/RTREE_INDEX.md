# R-TREE INDEX

> Lý thuyết: [21_R_TREE](../../01_THEORY/21_R_TREE.md). Quyết định: D16, D17.

## 1. R-tree index CÁI GÌ
- **KHÔNG** index file audio, frame hay segment.
- Index **500 điểm 8D**, mỗi điểm là `u` của một sequence DB, khóa là `audio_id`.
```
seq_violin_0001.wav → v (52D) → v' (52D) → u = (0.81, −1.20, 0.33, …, 0.05) ∈ ℝ⁸ → entry id = 1
seq_cello_0042.wav  → …                  → u = (−1.74, 0.62, …)              → entry id = 242
```
Với điểm, MBR là hộp suy biến: min = max = u.

## 2. Cấu hình
| Tham số | Giá trị | Lý do |
|---|---|---|
| Thư viện | `rtree` (libspatialindex) | Hỗ trợ n chiều, có `nearest`, ghi ra file |
| Biến thể | R\*-tree (`RT_Star`) | Giảm chồng lấn MBR bằng forced reinsert |
| dimension | 8 | = PCA_DIM |
| leaf_capacity, index_capacity | **10** | Mặc định là 100: với 500 điểm, cây chỉ có 5 lá, không minh họa được cắt tỉa. Với 10: khoảng 50 lá, cao 3 tầng |
| Lưu trữ | `data/index/rtree_v1.dat`, `.idx` | Đồng bộ theo `model_version` |

## 3. Cấu trúc (minh họa)
```
Root  [MBR bao 500 điểm]
 ├── Internal A [MBR_A]     ← ví dụ vùng "trầm" (cello, bass)
 │     ├── Leaf A1 [MBR] → ids {242, 251, 260, …}  (≤ 10 entry)
 │     └── Leaf A2 [MBR] → …
 ├── Internal B [MBR_B]     ← vùng "kéo vĩ, cao"
 └── Internal C [MBR_C]     ← vùng "âm gảy" (guitar)
```
(Các nhãn "vùng" chỉ minh họa; ranh giới thật do thuật toán chèn quyết định.)

## 4. Pseudocode build
```
p = index.Property(); p.dimension = 8; p.variant = RT_Star
p.leaf_capacity = 10; p.index_capacity = 10
idx = index.Index('data/index/rtree_v1', properties=p)
for audio_id, u in DB: idx.insert(audio_id, (*u, *u))     # hộp (min..., max...)
```

## 5. Hiệu quả trong 8D: nói thẳng
- Với N = 500, quét tuyến tính mất dưới 1 ms và **thường nhanh hơn** R-tree. Trong bài, R-tree có giá trị **minh họa chỉ mục đa chiều và cơ chế lọc rồi tinh chỉnh**, không phải để tăng tốc. Cần ghi rõ trong báo cáo.
- Đo **số ứng viên trung bình / 500**. Nếu > 50%: thử PCA 5–6D (cắt tỉa tốt hơn, cận dưới lỏng hơn), hoặc giữ 8D và báo cáo trung thực. Kết quả **vẫn chính xác** trong mọi trường hợp.
- Nâng cao: dựng thêm R-tree 2D (PC1, PC2) chỉ để **vẽ MBR**.
