# 18. Vector đặc trưng của một file — từ nhiều đoạn tới một điểm

> **Đọc xong file này bạn sẽ biết:** vì sao mỗi file phải thành **đúng một** vector có số chiều cố định; K-means và "prototype" là gì; ý tưởng "túi từ" của tìm kiếm văn bản được mượn sang âm thanh ra sao (bag-of-prototypes); gán cứng và gán mềm khác nhau thế nào; vector 52 chiều của project được tính từng bước ra sao, kèm ví dụ số; vì sao nó chịu được lỗi tách nốt.
> **Cần biết trước:** [15](15_AUDIO_FEATURES.md) (32 đặc trưng mỗi đoạn), [17](17_ONSET_SEGMENTATION.md) (đoạn).
> **Đọc tiếp:** [19 Khoảng cách và độ tương đồng](19_DISTANCE_SIMILARITY.md).

---

## 1. Vấn đề: số đoạn mỗi file khác nhau

Sau khi tách nốt ([17](17_ONSET_SEGMENTATION.md)), một file có **n đoạn**, mỗi đoạn là một vector **32 số** ([15](15_AUDIO_FEATURES.md)). File 4 nốt cho 4 vector; file 7 nốt cho 7 vector.

Nhưng để **tính khoảng cách** giữa hai file và **đặt file vào R-tree**, mỗi file phải là **một điểm** trong một không gian **có số chiều cố định**. Không thể đo khoảng cách giữa một thứ 4×32 và một thứ 7×32.

**Câu hỏi:** gộp n vector 32 chiều thành **một** vector cố định thế nào, để vẫn giữ được thông tin "file này nghe giống nhạc cụ nào"?

| Cách gộp | Số chiều | Nhận xét |
|---|---|---|
| Nối tất cả lại | 32 × n (thay đổi) | **Loại**: không cố định; "đoạn 3 của file A" bị so với "đoạn 3 của file B", vô nghĩa |
| **Trung bình** các đoạn | 32 | **Giữ** (phần μ): đơn giản, bền; nhưng mất phân bố ("nửa giống violin, nửa giống viola") |
| Đếm "đoạn này thuộc nhạc cụ nào" | 5 | **Loại**: quá thô, mọi file violin đều là [1, 0, 0, 0, 0] |
| **Túi prototype, gán mềm** | 20 | **Chọn** (phần h): giữ phân bố, có diễn giải, cố định 20 chiều |
| VLAD / Fisher vector | 640 | **Loại**: quá nhiều chiều cho R-tree |
| So khớp chuỗi (DTW) | không cố định | **Loại**: không ra được một điểm để đặt vào R-tree |

**Kết quả: v = [ h (20 số) ‖ μ (32 số) ] = 52 số.** Lý do chi tiết: [FILE_LEVEL_VECTOR](../04_PART_1/03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md).

---

## 2. Prototype và K-means

### 2.1. Prototype là gì
**Là gì.** Một **prototype** là một điểm **đại diện** cho một nhóm điểm giống nhau. Ví dụ: "kiểu âm violin vùng cao, sáng" là một prototype; "kiểu âm violin dây G, tối" là một prototype khác.

**Vì sao cần.** Một nhạc cụ **không phải một điểm** trong không gian đặc trưng mà là một **đám mây** trải rộng: nốt thấp và nốt cao, to và nhỏ, hai nơi thu ([05](05_VIOLIN.md) §10, [07](07_CELLO.md) §9.1). Vài prototype mỗi nhạc cụ mô tả đám mây đó tốt hơn một điểm trung bình.

**Vì sao KHÔNG làm prototype theo từng nốt** (ví dụ "violin-A4", "violin-B4"…): vector khi đó mã hóa **giai điệu** chứ không phải nhạc cụ. Hai file violin chơi hai giai điệu khác nhau sẽ không có nốt chung, nên trông "khác nhau" y như file violin so với file cello ([REFERENCE_PROTOTYPES](../04_PART_1/03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md) §1).

### 2.2. K-means — tìm prototype tự động
**Là gì.** K-means là thuật toán chia một đám điểm thành **k nhóm**, mỗi nhóm có một **tâm**. Tâm chính là prototype.

**Hình dung.** Rải k "nam châm" ngẫu nhiên vào đám điểm. Mỗi điểm bám vào nam châm gần nhất. Dời mỗi nam châm tới **giữa** các điểm đang bám nó. Lặp lại tới khi không điểm nào đổi nam châm nữa.

**Công thức** (mục tiêu):
```
tìm k tâm P_1 … P_k sao cho   J = Σ_r  min_j ‖ x_r − P_j ‖²   nhỏ nhất
```
| Thành phần | Ý nghĩa |
|---|---|
| `x_r` | Điểm thứ r (một nốt REF, 32 số đã chuẩn hóa) |
| `‖x_r − P_j‖²` | Bình phương khoảng cách từ điểm tới tâm j ([19](19_DISTANCE_SIMILARITY.md)) |
| `min_j` | Mỗi điểm chỉ tính khoảng cách tới **tâm gần nhất** của nó |
| `J` | Tổng "độ lệch" của mọi điểm so với tâm của nhóm; càng nhỏ thì các nhóm càng gọn |

**Thuật toán:**
```
1. Khởi tạo k tâm (cách k-means++: chọn tâm đầu ngẫu nhiên, các tâm sau ưu tiên điểm ở XA các tâm đã chọn)
2. Gán: mỗi điểm vào tâm gần nhất
3. Cập nhật: mỗi tâm = trung bình các điểm của nó
4. Lặp 2–3 tới khi không còn điểm nào đổi nhóm
```
Kết quả phụ thuộc lúc khởi tạo, nên chạy nhiều lần (project: 20 lần) và giữ lần có J nhỏ nhất.

**Ví dụ nhỏ (2 chiều).** 6 điểm: (1,1), (1,2), (2,1) và (8,8), (8,9), (9,8); k = 2.
- Tâm cuối cùng: (1.33, 1.33) và (8.33, 8.33). Đây là 2 prototype.
- Bình phương khoảng cách tới tâm: điểm ở góc (1,1) là 0.22; hai điểm còn lại mỗi điểm 0.56. Nhóm kia đối xứng y hệt. J = 2 × (0.22 + 0.56 + 0.56) = **2.67**.

**Phải chuẩn hóa trước** ([19](19_DISTANCE_SIMILARITY.md) §4): nếu không, chiều có thang lớn (centroid tính bằng Hz) sẽ quyết định một mình.

**Chọn k.** Thử nhiều k, xem **silhouette**: với mỗi điểm, s = (b − a) / max(a, b). Trong đó a là khoảng cách trung bình tới các điểm cùng nhóm, b là khoảng cách trung bình tới nhóm gần nhất khác. s gần 1 là nhóm tách tốt, gần 0 là nằm ở biên.

### 2.3. Trong project
```
Nốt REF (150 nốt / nhạc cụ, chọn theo D23) → 32 đặc trưng → chuẩn hóa z (theo REF)
  → với MỖI nhạc cụ: K-means k = 4
  → P1–P4 violin · P5–P8 viola · P9–P12 cello · P13–P16 double bass · P17–P20 guitar  (20 prototype)
```
- Prototype được học **riêng theo nhạc cụ**, nên mỗi prototype **có nhãn** nhạc cụ và diễn giải được.
- k = 4 là giá trị ban đầu; thử k = 3…6 ở Bước 4 (mục chờ P02).
- **Điều cần kiểm tra khi học prototype:** [15](15_AUDIO_FEATURES.md) cho thấy nơi thu ảnh hưởng mạnh tới một số đặc trưng. K-means có thể chia nhóm theo **nơi thu** (cụm "violin Iowa", cụm "violin Philharmonia") thay vì theo âm vực hay âm sắc. Bảng mô tả prototype nên có thêm **tỉ lệ nguồn thu** trong mỗi cụm để phát hiện điều này.

---

## 3. Túi từ → túi prototype

**Ý tưởng mượn từ tìm kiếm văn bản.** Một tài liệu được biểu diễn bằng **bảng đếm số lần mỗi từ xuất hiện** (*bag of words*), không quan tâm thứ tự từ. Hai tài liệu cùng chủ đề dùng những từ giống nhau, nên bảng đếm giống nhau.

| Văn bản | Âm thanh (project) |
|---|---|
| Từ | **Prototype** |
| Tài liệu | **File** âm thanh |
| Một lần xuất hiện của từ | Một **đoạn** gần prototype đó |
| Bảng đếm (số chiều = số từ trong từ điển) | **Histogram h** (số chiều = 20 prototype) |

Số chiều của h = **số prototype**, không phụ thuộc file dài hay ngắn.

---

## 4. Gán cứng và gán mềm

**Gán cứng:** mỗi đoạn góp **trọn 1** vào prototype gần nhất.
- Vấn đề: đoạn nằm **sát biên** giữa hai prototype. Ví dụ khoảng cách tới P3 = 1.01 và tới P4 = 1.00 → trọn vào P4. Một chút nhiễu làm nó nhảy sang P3: h thay đổi **1.0**.

**Gán mềm (softmax theo khoảng cách):** mỗi đoạn **chia** đóng góp cho mọi prototype, gần thì nhiều, xa thì ít:
```
w_ij = exp( −d_ij² / τ ) / Σ_j' exp( −d_ij'² / τ )          Σ_j w_ij = 1
```
| Thành phần | Ý nghĩa |
|---|---|
| `d_ij` | Khoảng cách từ đoạn i tới prototype j |
| `exp(−d²/τ)` | Gần → gần 1; xa → gần 0 |
| `τ` (tau) | "Độ mềm". τ nhỏ → gần như gán cứng; τ lớn → chia đều. Project: τ = trung vị của (khoảng cách bình phương tới prototype gần nhất) trên REF, tức là một khoảng cách "điển hình" |
| Mẫu số | Chuẩn hóa để tổng các w của một đoạn bằng 1 |

Cùng ví dụ sát biên: P3 ≈ 0.49, P4 ≈ 0.51. Nhiễu nhỏ chỉ làm h đổi khoảng **0.01**. Gán mềm **ổn định** hơn nhiều.

---

## 5. Vector 52 chiều của một file — từng bước

File có n đoạn; đoạn i dài `dur_i` giây, có vector 32 số `s_i`:
```
z_i  = (s_i − μ_seg) / σ_seg               chuẩn hóa bằng thống kê của REF (KHÔNG tính lại cho từng file)
d_ij = ‖ z_i − P_j ‖                        khoảng cách tới 20 prototype
w_ij = softmax_j( −d_ij² / τ )              gán mềm (§4)
α_i  = dur_i / Σ_k dur_k                    trọng số theo độ dài đoạn, Σ α = 1
h_j  = Σ_i α_i · w_ij                       → h: 20 số, tổng = 1     ("file giống từng kiểu âm bao nhiêu %")
μ    = Σ_i α_i · z_i                        → μ: 32 số               ("âm sắc trung bình" của file)
v    = [ h ‖ μ ]                            → 52 số
```

**Ví dụ số** (minh họa, 10 prototype cho gọn; giả sử P1–P4 là violin, P5–P8 viola, P9–P10 cello). File 5 đoạn, tổng 3.0 s:

| Đoạn | Dài | α | w (các giá trị đáng kể) |
|---|---|---|---|
| S1 | 0.6 s | 0.200 | P3: 0.70 · P4: 0.20 · P1: 0.10 |
| S2 | 0.4 s | 0.133 | P3: 0.60 · P4: 0.30 · P7: 0.10 |
| S3 | 1.0 s | 0.333 | P7: 0.80 · P8: 0.15 · P3: 0.05 |
| S4 | 0.5 s | 0.167 | P3: 0.75 · P4: 0.25 |
| S5 | 0.5 s | 0.167 | P9: 0.85 · P10: 0.15 |

```
h3 = 0.200×0.70 + 0.133×0.60 + 0.333×0.05 + 0.167×0.75 = 0.362
h7 = 0.133×0.10 + 0.333×0.80 = 0.280 …
h  = [0.020, 0, 0.362, 0.122, 0, 0, 0.280, 0.050, 0.142, 0.025]
```
**Đọc kết quả:** P1–P4 (violin) cộng lại khoảng **50%**, P5–P8 (viola) khoảng **33%**, P9–P10 (cello) khoảng **17%**. Nghĩa là "file này nghe nửa giống violin, một phần ba giống viola".

**Vì sao cần cả μ:** h chỉ nói file **gần các prototype nào**. Với nhạc cụ **ngoài CSDL** (banjo), mọi prototype đều xa; h vẫn cộng lại bằng 1 nên trông "bình thường". Còn μ (âm sắc trung bình, tuyệt đối) cho thấy file thật sự nằm ở đâu.

---

## 6. Vì sao vector này chịu được lỗi tách nốt

| Lỗi | Điều xảy ra | Vì sao h, μ gần như không đổi |
|---|---|---|
| **Chia thừa** (một nốt 1.2 s thành 3 mảnh) | 3 đoạn thay vì 1 | Trọng số α theo **độ dài**: 3 mảnh cộng lại vẫn là 1.2 s; các mảnh giống nhau nên w gần nhau |
| **Gộp sót** (legato: 2 nốt thành 1 đoạn) | 1 đoạn chứa 2 nốt | Hai nốt cùng nhạc cụ → đoạn gộp vẫn gần các prototype của nhạc cụ đó |
| **Thứ tự nốt** khác | — | Tổng không phụ thuộc thứ tự: đúng chủ đích, vì ta tìm theo âm sắc, không theo giai điệu |
| File chỉ có **1 nốt** | n = 1 | Vẫn hợp lệ: h = w của đoạn đó, μ = z của đoạn đó |

---

## 7. Áp dụng cho 5 nhạc cụ (dự đoán, kiểm tra ở Bước 4–5)

| File | h dự kiến |
|---|---|
| Sequence violin | Dồn vào P1–P4, có phần đáng kể ở viola P5–P8 (cặp khó, [06](06_VIOLA.md) §10) |
| Sequence cello | Dồn vào P9–P12, một phần sang double bass hoặc viola |
| Sequence guitar | Dồn mạnh vào P17–P20 (âm gảy rất khác kéo vĩ) |
| Banjo (ngoài CSDL) | Phần lớn ở guitar P17–P20; μ nằm xa mọi sequence guitar ([10](10_BANJO_MANDOLIN.md) §4) |
| Mandolin vê | Có thể nghiêng sang violin (đường bao giữ đều, [10](10_BANJO_MANDOLIN.md) §3.4) |

---

## 8. Liên hệ với dataset

| Dữ liệu | Dùng để |
|---|---|
| Nốt **REF** (150 / nhạc cụ) | Tính μ_seg, σ_seg (chuẩn hóa z); học 20 prototype; tính τ |
| Sequence **DB** (500) | Tính v → lưu vào CSDL → chỉ mục R-tree |
| Sequence **truy vấn**, phrase, unseen | Tính v bằng **đúng cùng hàm** → tìm kiếm |

**Quy tắc:** μ_seg, σ_seg, prototype và τ chỉ học **một lần** trên REF, rồi dùng nguyên vẹn cho mọi file khác. Học lại trên truy vấn là rò rỉ ([16](16_DATASET_MODEL.md) §7).
