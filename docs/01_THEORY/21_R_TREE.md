# 21. R-tree — chỉ mục cho dữ liệu nhiều chiều

> **Đọc xong file này bạn sẽ biết:** vì sao cần chỉ mục; R-tree gom điểm vào các "hộp" lồng nhau ra sao (hình dung, cấu trúc, ví dụ số); chèn một điểm và tách nút; tìm k láng giềng gần nhất bằng MINDIST và cắt tỉa; khung **lọc rồi tinh chỉnh** cho Top-5 chính xác; lời nguyền số chiều; R-tree được cấu hình thế nào trong project, và nói thẳng về hiệu quả của nó với 500 điểm.
> **Cần biết trước:** [19](19_DISTANCE_SIMILARITY.md) (khoảng cách, k-NN), [20](20_PCA.md) (8 chiều, cận dưới).
> **Đọc tiếp:** [22 CSDL đa phương tiện](22_MULTIMEDIA_DATABASE.md).

---

## 1. Vì sao cần chỉ mục

Tìm Top-5 bằng cách **quét toàn bộ** ([19](19_DISTANCE_SIMILARITY.md) §6) phải tính khoảng cách tới **mọi** điểm: N phép tính, mỗi phép d số. Với N = 500 thì rất nhanh, nhưng với hàng triệu bản thu thì không chấp nhận được.

**Ý tưởng của chỉ mục:** sắp xếp dữ liệu trước (một lần, lúc xây CSDL), sao cho khi tìm chỉ cần xem **một phần nhỏ** dữ liệu mà vẫn chắc chắn tìm đúng. Giống như thư viện xếp sách theo kệ, theo ngăn: tìm sách về âm nhạc thì đi thẳng tới kệ âm nhạc, không đọc mọi cuốn sách.

Với dữ liệu **một chiều** (số, chữ), người ta dùng B-tree. Với dữ liệu **nhiều chiều** (điểm trong không gian, như vector đặc trưng), dùng **R-tree**.

---

## 2. Hình dung: gom điểm vào hộp, gom hộp vào hộp lớn

```
 ┌───────────────── Gốc ─────────────────┐
 │ ┌──── Hộp A ────┐        ┌── Hộp C ──┐│
 │ │  ·   ·        │        │   ·  ·    ││
 │ │    ·    ·     │        │ ·    ·    ││
 │ └───────────────┘        └───────────┘│
 │            ┌──── Hộp B ────┐           │
 │            │  ·  ·   ·     │           │
 │            └───────────────┘           │
 └───────────────────────────────────────┘
```
- Các điểm **gần nhau** được gom vào cùng một **hộp chữ nhật nhỏ nhất bao trọn chúng** (MBR).
- Các hộp gần nhau lại được gom vào một hộp lớn hơn, cứ thế tới **gốc**.
- Khi tìm điểm gần truy vấn, ta **bỏ qua cả hộp** nếu thấy ngay cả điểm gần nhất có thể có trong hộp cũng đã xa hơn kết quả đang có.

---

## 3. MBR và cấu trúc cây

**MBR** (*Minimum Bounding Rectangle*): hộp chữ nhật **nhỏ nhất**, **song song với các trục**, bao trọn mọi điểm bên trong. Trong d chiều, MBR là d khoảng [thấp, cao], mỗi chiều một khoảng.

**Ví dụ 2 chiều:** ba điểm (1, 2), (2, 5), (3, 1) → MBR = [1, 3] × [1, 5] (x từ 1 tới 3, y từ 1 tới 5).

**Cấu trúc R-tree:**
| Thành phần | Chứa gì |
|---|---|
| **Nút lá** | Các mục (MBR của điểm, mã định danh). Với **một điểm**, MBR là hộp "dẹt hẳn": thấp = cao = tọa độ điểm |
| **Nút trong** | Các mục (MBR bao toàn bộ nút con, con trỏ tới nút con) |
| **Sức chứa** | Mỗi nút có từ m tới M mục (thường m ≈ 40% M) |
| **Cân bằng** | Mọi nút lá ở **cùng độ sâu** |

```
Gốc [MBR toàn cục]
 ├── N1 [MBR1] ─┬── L1 [MBR] → điểm 3, 17, 42 …
 │              └── L2 [MBR] → …
 └── N2 [MBR2] ─┬── L3 [MBR] → …
                └── L4 [MBR] → …
```

---

## 4. Chèn một điểm và tách nút

**Chèn:**
1. **Chọn lá (ChooseLeaf):** từ gốc đi xuống. Ở mỗi mức, chọn mục mà MBR **phải nới rộng ít nhất** để chứa điểm mới.
2. Thêm điểm vào lá đó.
3. Nếu lá vượt M mục: **tách** thành hai nút.
4. **Cập nhật** MBR từ lá ngược lên gốc. Việc tách có thể lan lên tới gốc; khi gốc bị tách, cây cao thêm một tầng.

**Ví dụ "nới rộng ít nhất".** Điểm mới (4, 4). Hai hộp: A = [1, 3] × [1, 5] (diện tích 2 × 4 = 8) và C = [5, 8] × [5, 8] (diện tích 9).
- Nới A thành [1, 4] × [1, 5]: diện tích 12, tăng **4**.
- Nới C thành [4, 8] × [4, 8]: diện tích 16, tăng **7**.
- → Chọn **A**.

**Tách nút (quadratic split):** chọn hai mục "xa nhau nhất" (gộp chung thì phí diện tích nhiều nhất) làm hai hạt giống, rồi lần lượt chia các mục còn lại về phía hạt giống làm MBR nới ít hơn.

**R\*-tree** (biến thể project dùng) cải tiến hai điểm:
- Khi tách, ưu tiên giảm **phần chồng lấn** giữa các hộp và chu vi hộp.
- Trước khi tách, thử **chèn lại** một phần mục (*forced reinsert*) để chúng tìm chỗ tốt hơn.

Kết quả là các hộp gọn hơn, ít chồng nhau hơn, nên tìm kiếm phải mở ít hộp hơn.

---

## 5. Tìm k láng giềng gần nhất

### 5.1. MINDIST — khoảng cách từ truy vấn tới một hộp
**Là gì.** Khoảng cách **nhỏ nhất có thể** từ điểm truy vấn q tới **bất kỳ** điểm nào nằm trong hộp R. Mọi điểm trong hộp đều cách q ít nhất bằng MINDIST.
```
MINDIST(q, R) = √( Σ_i  δ_i² )      với   δ_i = thấp_i − q_i   nếu q_i < thấp_i
                                           q_i − cao_i   nếu q_i > cao_i
                                           0             nếu q_i nằm trong [thấp_i, cao_i]
```
**Ví dụ:** q = (4, 4).
| Hộp | Khoảng | δ_x | δ_y | MINDIST |
|---|---|---|---|---|
| A = [1, 3] × [1, 5] | x: q bên phải 1; y: q nằm trong | 1 | 0 | **1.00** |
| C = [5, 8] × [5, 8] | x: bên trái 1; y: bên dưới 1 | 1 | 1 | **1.41** |
| B = [6, 9] × [0, 2] | x: bên trái 2; y: bên trên 2 | 2 | 2 | **2.83** |

### 5.2. Tìm theo thứ tự "hộp hứa hẹn nhất trước" (best-first)
```
hàng đợi ưu tiên H ← (MINDIST(q, gốc), gốc)
trong khi H chưa rỗng:
    lấy ra phần tử có MINDIST nhỏ nhất
    nếu là một ĐIỂM: trả ra (đây là láng giềng gần tiếp theo); đủ k điểm thì dừng
    nếu là một NÚT: đẩy mọi con của nó vào H, kèm MINDIST của từng con
```
**Cắt tỉa.** Khi đã có k kết quả, mọi hộp có MINDIST **lớn hơn** khoảng cách tới kết quả thứ k sẽ **không bao giờ được mở**: mọi điểm trong hộp đó chắc chắn xa hơn. Trong ví dụ trên, nếu đã tìm được một điểm trong A cách q 1.2, thì hộp B (MINDIST 2.83) bị bỏ qua mà không cần xem điểm nào bên trong.

### 5.3. Lọc rồi tinh chỉnh (GEMINI) — Top-5 chính xác với PCA
R-tree của project chứa các điểm **8 chiều** (sau PCA), nhưng khoảng cách thật là **52 chiều**. Nhờ tính chất **cận dưới** ([20](20_PCA.md) §4): khoảng cách 8 chiều ≤ khoảng cách 52 chiều.
```
k' ← 20
lặp:
    C  ← k' ứng viên gần nhất theo 8 chiều (R-tree)                        LỌC
    D  ← khoảng cách THẬT 52 chiều tới từng ứng viên trong C               TINH CHỈNH
    top5 ← 5 ứng viên có D nhỏ nhất
    r8 ← khoảng cách 8 chiều tới ứng viên XA NHẤT trong C
    nếu D(top5 thứ 5) ≤ r8 (hoặc đã xét hết): trả top5                    DỪNG
    ngược lại: k' ← 2 × k'
```
**Vì sao chắc chắn đúng.** Mọi điểm y **chưa** được xét có khoảng cách 8 chiều ≥ r8. Theo cận dưới, khoảng cách thật D(y) ≥ khoảng cách 8 chiều ≥ r8 ≥ D(kết quả thứ 5). Vậy y **không thể** chen vào Top-5. Kết quả **giống hệt** quét toàn bộ, không bỏ sót (*no false dismissal*).

**Ví dụ.** Lần lặp 1: lấy 20 ứng viên, ứng viên xa nhất cách 1.9 (8 chiều). Tính 52 chiều: kết quả thứ 5 cách **2.3** > 1.9 → chưa chắc chắn (có thể có điểm ngoài 20 ứng viên mà 8 chiều cách 2.0, 52 chiều cách 2.1). Lần lặp 2: lấy 40 ứng viên, xa nhất cách 2.6; kết quả thứ 5 vẫn là 2.3 ≤ 2.6 → **dừng**, kết quả chính xác.

Chi tiết: [KNN_SEARCH](../05_PART_2/03_SEARCH/KNN_SEARCH.md).

---

## 6. Lời nguyền số chiều

**Hiện tượng.** Khi số chiều tăng, mọi điểm trở nên **cách đều nhau**: điểm gần nhất và điểm xa nhất cách truy vấn gần như bằng nhau. Mô phỏng với 500 điểm ngẫu nhiên đều:

| Số chiều | Khoảng cách gần nhất ÷ xa nhất (trung vị) |
|---|---|
| 2 | 0.02: gần nhất **rất** gần so với xa nhất |
| 8 | 0.25 |
| 52 | **0.62**: gần nhất cũng đã xa gần bằng xa nhất |

**Hệ quả cho R-tree.** Ở nhiều chiều, các hộp MBR chồng lên nhau gần hết, và MINDIST tới hầu hết các hộp đều nhỏ hơn khoảng cách tới kết quả thứ k. Không hộp nào bị cắt tỉa, nên R-tree mở gần hết cây: **chậm bằng hoặc hơn** quét toàn bộ. Thực tế R-tree hiệu quả ở khoảng **dưới 10 chiều**. Lời giải là giảm chiều bằng PCA ([20](20_PCA.md)) rồi lọc – tinh chỉnh (§5.3).

---

## 7. R-tree trong project

| Tham số | Giá trị | Vì sao |
|---|---|---|
| R-tree chứa gì | **500 điểm 8 chiều**, mỗi điểm là một sequence của CSDL, khóa là `audio_id` | Không đánh chỉ mục file âm thanh, frame hay đoạn: chỉ **vector của file** ([22](22_MULTIMEDIA_DATABASE.md)) |
| Thư viện | `rtree` (dùng libspatialindex) | Hỗ trợ nhiều chiều, có sẵn tìm láng giềng gần nhất, lưu ra file |
| Biến thể | R\*-tree | Ít chồng lấn hơn (§4) |
| Số chiều | 8 | = số chiều PCA |
| Sức chứa mỗi nút | **10** (mặc định của thư viện là 100) | Với 500 điểm và sức chứa 100, cây chỉ có 5 lá, không minh họa được việc cắt tỉa. Với 10: khoảng 50 lá, cao 3 tầng |

**Nói thẳng về hiệu quả.** Với 500 điểm, quét toàn bộ mất dưới 1 ms và **thường nhanh hơn** R-tree (R-tree tốn thêm công duyệt cây). Trong project, R-tree có giá trị **minh họa** chỉ mục nhiều chiều và cơ chế lọc – tinh chỉnh, không phải để tăng tốc. Báo cáo sẽ đo **số ứng viên trung bình trên 500** và **so kết quả với quét toàn bộ** (phải giống hệt 100%). Chi tiết: [RTREE_INDEX](../05_PART_2/02_INDEX/RTREE_INDEX.md).

---

## 8. So sánh ngắn với các cấu trúc khác

| Cấu trúc | Cách chia | Nhận xét |
|---|---|---|
| k-d tree | Chia **không gian** theo một trục mỗi tầng | Tốt cho điểm, dữ liệu ít thay đổi |
| Quadtree / octree | Chia mỗi ô thành 2^d ô con | Chỉ dùng thực tế cho 2–3 chiều |
| **R-tree** | Chia **dữ liệu** bằng các hộp MBR; cây cân bằng; chèn động | Có trong nhiều hệ CSDL (SQLite R\*Tree, PostGIS) |
| HNSW (pgvector, FAISS) | Đồ thị láng giềng | Rất nhanh ở nhiều chiều nhưng là tìm **gần đúng**, có thể bỏ sót; không phải R-tree, không minh họa được nội dung môn học |

---

## 9. Áp dụng cho 5 nhạc cụ (dự đoán)

Vì các sequence cùng nhạc cụ nằm gần nhau ([20](20_PCA.md) §6), các **lá** của R-tree sẽ phần lớn chứa sequence của **một** nhạc cụ, ví dụ "lá guitar". Ở vùng violin – viola và cello – double bass, các lá sẽ **trộn** nhạc cụ, đúng với các cặp khó đã thấy ở [15](15_AUDIO_FEATURES.md). Kiểm tra được bằng cách đếm nhạc cụ trong từng lá sau khi xây cây (Bước 10).
