# k-NN SEARCH — Similarity và Top-5 chính xác

> Lý thuyết: [19_DISTANCE_SIMILARITY](../../01_THEORY/19_DISTANCE_SIMILARITY.md), [21_R_TREE](../../01_THEORY/21_R_TREE.md) §5. Quyết định: D15, D17.

## 1. Độ đo: Euclid L2 trên v' (52D)
```
d(q, x) = ‖v'_q − v'_x‖₂ = √Σ (v'_q,i − v'_x,i)²
similarity hiển thị = 1 / (1 + d)          (chỉ để hiển thị; xếp hạng luôn theo d tăng dần)
```
**Vì sao Euclid, không phải cosine:** (1) R-tree cắt tỉa bằng MINDIST Euclid; (2) cận dưới qua PCA đúng với L2; (3) trong không gian z-score, "độ lớn" có nghĩa. Ví dụ V3 = 2Q: cosine cho = 1 ("giống hệt"), nhưng thực chất là âm thanh khác thường gấp đôi Q. Ví dụ tính đầy đủ ở [19_DISTANCE_SIMILARITY](../../01_THEORY/19_DISTANCE_SIMILARITY.md) §5.

## 2. Thuật toán Top-5 chính xác (multi-step k-NN / filter-and-refine)
```
INPUT : v'_q (52D), u_q (8D), K = 5
OUTPUT: K audio_id có d nhỏ nhất (giống hệt brute force)

k' ← 20
loop:
    C   ← rtree.nearest(u_q, k')               # k' ứng viên gần nhất theo khoảng cách 8D   (FILTER)
    D(x)← ‖v'_q − v'_x‖ với x ∈ C              # khoảng cách thật 52D                       (REFINE)
    top ← K phần tử có D nhỏ nhất trong C
    r8  ← khoảng cách 8D tới ứng viên xa nhất trong C
    if D(top[K−1]) ≤ r8 or k' ≥ N: return top
    k' ← 2·k'
```
**Chứng minh:** mọi y ∉ C có d₈(y) ≥ r8. Theo cận dưới, D(y) ≥ d₈(y) ≥ r8 ≥ D(top[K−1]), nên y không thể lọt Top-K. ∎

Ghi chú cài đặt: `rtree.nearest` có thể trả về **nhiều hơn** k' id khi hòa khoảng cách. Luôn tính r8 từ chính tập C trả về.

## 3. Brute force (bắt buộc có, để đối chiếu)
```
D = ‖V'_DB − v'_q‖ theo từng dòng (500 phép tính); trả về argsort(D)[:5]
```

## 4. Output
| Trường | Ví dụ |
|---|---|
| rank | 1..5 |
| audio_id, rel_path | 242, `data/sequences/db/seq_cello_0042.wav` |
| instrument | cello |
| d | 1.873 |
| similarity | 0.348 |
| thống kê tìm kiếm | số ứng viên = 40, số vòng = 2, thời gian (ms) |

## 5. Kiểm tra
Với 100 sequence query: Top-5 của `search` == Top-5 của `brute_force` (cùng id, cùng thứ tự) ở **100%**. Ghi lại số ứng viên trung bình và thời gian.
