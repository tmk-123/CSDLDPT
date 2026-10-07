# MILESTONES

| Mốc | Gồm bước | Bằng chứng hoàn thành | Trạng thái |
|---|---|---|---|
| **M0 – Sẵn sàng** | 0 | Import thư viện OK, có `config.py` | ⬜ |
| **M1 – Dữ liệu sạch** | 1, 2 | `data/catalog.csv` + test catalog qua + mọi file load được | ⬜ |
| **M2 – Đặc trưng và tham chiếu** | 3, 4 | `ref_features.npz`, 20 prototype, accuracy prototype > 70% | ⬜ |
| **M3 – Multi-note** | 5, 6 | 600 sequence + ground truth; onset F ≥ 0.80 | ⬜ |
| **M4 – Bàn giao Phần 1** | 7 | Vector 52D cho mọi file, đúng OUTPUT_SPEC | ⬜ |
| **M5 – CSDL** | 8 | `mmdb.sqlite` tạo lại được bằng một lệnh | ⬜ |
| **M6 – Chỉ mục** | 9, 10 | Test cận dưới qua; R-tree == brute force 100% | ⬜ |
| **M7 – Truy vấn** | 11 | CLI Top-5 + kết quả trung gian; 5 kiểm tra qua | ⬜ |

## Checklist
- [ ] B0 Môi trường + `config.py`
- [ ] B1 Catalog + split
- [ ] B2 `load_audio`
- [ ] B3 Đặc trưng 32D + tương quan + boxplot
- [ ] B4 20 prototype + τ
- [ ] B5 500 DB + 100 query sequence
- [ ] B6 Segmentation F ≥ 0.80
- [ ] B7 `audio_to_vector` → 52D
- [ ] B8 SQLite
- [ ] B9 Scaler + PCA 8D
- [ ] B10 R-tree + k-NN chính xác
- [ ] B11 Query CLI

Cập nhật bảng này **và** [CURRENT_STATUS](../00_PROJECT/CURRENT_STATUS.md) mỗi khi xong một bước.
