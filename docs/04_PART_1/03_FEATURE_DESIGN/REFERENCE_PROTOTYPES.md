# REFERENCE PROTOTYPES — Thư viện tham chiếu từ nốt đơn

> Lý thuyết: [04_CLUSTERING_PROTOTYPES](../../01_THEORY/04_CLUSTERING_PROTOTYPES.md). Quyết định: D10, D11.

## 1. Vì sao KHÔNG dùng prototype theo từng cao độ
Ý tưởng ban đầu: R1 = "G4 violin arco", R2 = "A4 violin arco", … mỗi segment được gán vào reference gần nhất, rồi đếm histogram.

```
File X (violin): G4 A4 B4  → bin {violin-G4, violin-A4, violin-B4}
File Y (violin): D5 E5 F5  → bin {violin-D5, violin-E5, violin-F5}
File Z (cello) : C3 D3 E3  → bin {cello-C3, cello-D3, cello-E3}
‖X − Y‖ = ‖X − Z‖ ≈ 0.816   ⇒ KHÔNG phân biệt được "cùng violin" với "khác nhạc cụ"
```
- Vector mã hóa **giai điệu**, không mã hóa **nhạc cụ**.
- Hàng trăm bin (5 nhạc cụ × khoảng 45 cao độ × kỹ thuật) trong khi file chỉ có 4–8 nốt ⇒ vector rất thưa, PCA và R-tree vô nghĩa.
- Gán đúng "violin-A4" là bài toán nhận dạng cao độ + nhạc cụ, khó hơn nhiều so với cái ta cần.

## 2. Thiết kế đã chốt
**Prototype = cụm âm sắc của MỘT nhạc cụ, học bằng K-means, không gắn với cao độ cụ thể.**

```
Nốt REF (~1 360) → s ∈ ℝ³² (FEATURE_SET)
  → scaler_seg: μ_seg, σ_seg tính trên REF;  z = (s − μ_seg)/σ_seg
  → với mỗi nhạc cụ c: KMeans(k=4, n_init=20, random_state=42) trên {z thuộc c}
  → P1..P4 violin · P5..P8 viola · P9..P12 cello · P13..P16 double-bass · P17..P20 guitar
  → τ = median_r ( min_j ‖z_r − P_j‖² )          (khoảng cách bình phương "điển hình")
```
- **k = 4** mỗi nhạc cụ: thường tách ra âm vực thấp/trung/cao và arco/pizz. Thử k ∈ {3, …, 6} ở Bước 4 và chọn theo silhouette + kết quả dev.
- Prototype **có nhãn nhạc cụ**, nên diễn giải được ("segment này giống cụm cello-2").

## 3. Ý tưởng "so với từng nốt REF" vẫn được giữ, nhưng làm công cụ giải thích
Với mỗi segment, tìm nốt REF gần nhất trong không gian z và hiển thị, ví dụ: *"gần nhất: `cello_D3_1_forte_arco-normal` (d = 1.21)"*. Thông tin này **chỉ để minh họa** (đề mục 4b), không đi vào vector.

## 4. Sản phẩm
| File | Nội dung |
|---|---|
| `data/models/v1/scaler_seg.npz` | `mean` (32), `std` (32) |
| `data/models/v1/prototypes.npz` | `P` (20×32), `instrument` (20), `n_members` (20), `tau` |
| `data/models/v1/ref_index.npz` | z của mọi nốt REF + recording_id (để tìm nốt REF gần nhất) |
| `reports/tables/prototypes.csv` | Mô tả cụm: số thành viên, khoảng cao độ, tỷ lệ kỹ thuật |

## 5. Kiểm tra
- Mỗi cụm có ≥ 10 thành viên.
- Phân loại 1-NN-prototype trên REF đạt accuracy > 70%.
