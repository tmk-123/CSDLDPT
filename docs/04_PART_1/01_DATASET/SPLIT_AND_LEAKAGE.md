# SPLIT AND LEAKAGE — Chia tập và chống rò rỉ dữ liệu

## 1. Các nguồn rò rỉ trong bài này
1. **Cùng một bản ghi** nằm ở cả REF và DB/query → khớp prototype "hoàn hảo" giả tạo.
2. **Gần cùng bản ghi:** cùng nhạc cụ + cao độ + kỹ thuật, chỉ khác dynamics → âm sắc gần như trùng.
3. **Một nốt được dùng lại** trong cả sequence DB và sequence query → query "tìm thấy chính mình".
4. **Tune siêu tham số** (δ, k, τ, λ, số chiều PCA) trên chính tập query.

## 2. Quy tắc chia: theo NHÓM CAO ĐỘ, xen kẽ
Áp dụng cho nốt đơn `status=OK` của 5 nhạc cụ, với `technique_family ∈ {arco}` (bộ kéo vĩ) hoặc `{pluck, harmonic}` (guitar) (D20), **cả hai nguồn** Philharmonia và Iowa.

```
Với mỗi nốt (D24):
  r = midi mod 5
  r ∈ {0,1} → REF          (~40%)
  r ∈ {2,3} → DB_POOL      (~40%)
  r = 4     → QUERY_POOL   (~20%)
Ví dụ: A4 = 69 → 69 mod 5 = 4 → QUERY_POOL (cả A4 Philharmonia lẫn A4 Iowa, của mọi nhạc cụ)
```
- **Xen kẽ** (5 nửa cung liền nhau rơi vào đủ 3 tập) ⇒ mỗi tập phủ đủ âm vực thấp, trung, cao.
- **Theo cao độ** ⇒ mọi dynamics, kỹ thuật **và mọi nguồn** của cùng một cao độ đi chung một tập ⇒ loại rò rỉ (1), (2).
- **Giới hạn số nốt được chọn** (D23): mỗi nhạc cụ chọn tối đa REF 150, DB_POOL 200, QUERY_POOL 60, trải đều theo (nguồn, cao độ, cường độ). Phần dư vẫn giữ split của nó với `selected = 0` (dự trữ).
- Hai nốt cách nhau nửa cung vẫn giống nhau, nhưng đó là **tổng quát hóa hợp lệ**, không phải rò rỉ.

Các file khác:
| Nhóm | split |
|---|---|
| `duration_label = phrase` | `PHRASE` |
| banjo, mandolin | `UNSEEN` |
| `special` technique, status ≠ OK | `NONE` |

## 3. Quy tắc dùng
| Tập | Được dùng cho | **Cấm** dùng cho |
|---|---|---|
| REF | scaler_seg, prototype, τ, "nốt REF gần nhất" | Ghép sequence |
| DB_POOL | Ghép 500 sequence DB | Ghép query |
| QUERY_POOL | Ghép 100 sequence query | Bất kỳ việc fit hay tune nào |
| PHRASE, UNSEEN | Chỉ làm query | Fit hay tune |
| 500 sequence DB | scaler_file, PCA, R-tree, dev để tune | — |

## 4. Validation (dev) để tune
Không lấy dev từ QUERY. Dùng **leave-one-out có loại trừ trên DB**: lấy lần lượt từng sequence DB làm query, tìm trên phần còn lại **sau khi bỏ mọi sequence dùng chung bản ghi nốt với nó**. Mọi tham số chọn trên dev; tập QUERY chỉ chạy **một lần** để lấy số cuối ⇒ loại rò rỉ (4).

## 5. Vấn đề riêng của guitar
> **Cập nhật:** hướng xử lý chính bây giờ là bổ sung dữ liệu Iowa MIS (D21, [DATASET_COLLECTION_AND_FILTERING](DATASET_COLLECTION_AND_FILTERING.md)). Phân tích dưới đây áp dụng cho trường hợp **chỉ** dùng `raw/philharmonia/`.

- 106 bản ghi / 42 cao độ ⇒ khoảng 42 REF / 42 DB_POOL / 22 QUERY_POOL.
- 100 sequence × khoảng 6 nốt = 600 lượt từ 42 bản ghi ⇒ **mỗi bản ghi dùng lại khoảng 14 lần** ⇒ các sequence guitar giống nhau hơn thực tế ⇒ P@5 guitar dễ cao giả.
- Giảm thiểu: (a) mỗi lần dùng cắt **đoạn khác** của nốt (guitar dài khoảng 5 s) và đổi gain; (b) ưu tiên bản ghi ít được dùng; (c) báo cáo P@5 **theo từng nhạc cụ** và nêu rõ hạn chế; (d) nếu có thể, bổ sung ≥ 150 nốt guitar từ nguồn mở (ghi rõ nguồn và giấy phép).
- 4 nhạc cụ kéo vĩ: khoảng 310–390 bản ghi DB_POOL ⇒ dùng lại khoảng 1.5–2 lần. Chấp nhận được.
