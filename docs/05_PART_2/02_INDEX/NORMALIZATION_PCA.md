# NORMALIZATION + PCA — Từ v (52D) tới vector đánh chỉ mục u (8D)

> Lý thuyết: [19_DISTANCE_SIMILARITY](../../01_THEORY/19_DISTANCE_SIMILARITY.md), [20_PCA](../../01_THEORY/20_PCA.md). Quyết định: D13, D14.

## 1. Vì sao phải chuẩn hóa trước khi tính khoảng cách
Ví dụ chưa chuẩn hóa: centroid 2 400 Hz vs 2 600 Hz; ZCR 0.05 vs 0.15. Ta có d² = 200² + 0.1² ≈ 40 000, nên ZCR **vô hình** dù chênh gấp 3 lần. Euclid chỉ công bằng khi mọi chiều cùng thang đo.

| Kỹ thuật | Nhận xét | Chọn? |
|---|---|---|
| Z-score (StandardScaler) | Mean 0, std 1; ít nhạy ngoại lai; là tiền đề cho PCA | **Có** |
| Min-Max | Một ngoại lai nén mọi giá trị khác; query nằm ngoài [0, 1] | Không |
| L2-normalize | Biến Euclid thành tương đương cosine; mất thông tin "độ lớn" (có nghĩa trong không gian z) | Không |

## 2. Hai scaler (không được nhầm)
| Scaler | Fit trên | Dùng ở | Ghi chú |
|---|---|---|---|
| `scaler_seg` (32D) | Nốt **REF** | Phần 1, trước khi so với prototype | Đã nằm trong v |
| `scaler_file` (52D) | **500 vector DB** | Phần 2, trước PCA | File này |

## 3. Chuỗi biến đổi (Phần 2)
```
v (52D, từ Phần 1)
 → x = (v − mean_file) / std_file                  scaler_file, fit trên DB
 → v' = [ x[0:20] / √20  ‖  x[20:52] / √32 ]       cân bằng khối: mỗi khối tổng phương sai = 1
 → u  = Wᵀ (v' − m)                                PCA 8D, fit trên DB, whiten = False
```
- Nếu muốn ưu tiên một khối: nhân thêm λ / (1−λ) (λ mặc định 0.5; tune trên dev, nâng cao).
- **Query chỉ gọi `transform`.** Fit riêng cho query sẽ ra hệ trục khác, tọa độ không so được với DB.

## 4. PCA
| Câu hỏi | Trả lời |
|---|---|
| Cần không? | Có, vì R-tree. Ở 52D các MBR chồng lấn gần hết, R-tree suy biến thành quét toàn bộ |
| Fit trên tập nào? | 500 vector DB (chính bộ sưu tập được phục vụ). Không dùng query, phrase, unseen |
| Có rò rỉ không? | Fit trên DB là hợp lệ; fit cả trên query đánh giá mới là rò rỉ |
| Bao nhiêu chiều? | **8**. Ghi explained variance (dự kiến 60–85%). Không cần đạt 95%, vì kết quả cuối vẫn chính xác trên 52D; số chiều chỉ ảnh hưởng **số ứng viên** |
| Whitening? | **Không**, vì whitening phá tính chất cận dưới |

## 5. Hai loại vector
| | v' (full) | u (indexed) |
|---|---|---|
| Số chiều | 52 | 8 |
| Dùng cho | **Khoảng cách chính xác, xếp hạng cuối** | **R-tree**: lọc ứng viên |
| Lưu ở | `file_vector.v_norm` | `file_vector.u_pca` + file R-tree |

**Cận dưới:** W có các cột trực chuẩn, nên ‖u_a − u_b‖ = ‖Wᵀ(v'_a − v'_b)‖ ≤ ‖v'_a − v'_b‖. Đây là nền tảng của [KNN_SEARCH](../03_SEARCH/KNN_SEARCH.md).

## 6. Sản phẩm và kiểm tra
- `data/models/v1/scaler_file.npz` (`mean`, `std` 52), `pca.npz` (`components` 8×52, `mean` 52, `explained_variance_ratio` 8).
- Test: mean ≈ 0 và std ≈ 1 trên DB; 10 000 cặp ngẫu nhiên thỏa cận dưới (+1e-6).
