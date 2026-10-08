# 19. Khoảng cách và độ tương đồng — "giống nhau" bằng con số

> **Đọc xong file này bạn sẽ biết:** "hai âm thanh giống nhau" được biến thành "hai điểm gần nhau" ra sao; khoảng cách Euclid, Manhattan, cosine; vì sao **phải chuẩn hóa** trước khi đo khoảng cách (ví dụ bằng 3 nốt A4 thật); vì sao chia trọng số theo khối; k-NN và Top-5; cách đổi khoảng cách ra điểm "độ giống"; cách chấm kết quả tìm kiếm.
> **Cần biết trước:** [15](15_AUDIO_FEATURES.md) (đặc trưng), [18](18_FEATURE_VECTOR.md) (vector 52 chiều).
> **Đọc tiếp:** [20 PCA](20_PCA.md).

---

## 1. Ý tưởng: giống nhau = gần nhau

Mỗi file là một **vector**, tức là một **điểm** trong không gian nhiều chiều (mỗi đặc trưng là một trục). Hình dung trường hợp 2 chiều: trục ngang là độ sáng (centroid), trục dọc là RMS-CV:
```
RMS-CV
  ↑        ●● guitar (tắt dần, tối)
  │      ●●●
  │                       ○○ violin (sáng, giữ đều)
  │                     ○○○
  │              △△ viola
  │      □□ cello
  └────────────────────────────→ độ sáng
```
Nếu đặc trưng chọn tốt, các file **cùng nhạc cụ** nằm thành **đám** gần nhau. "Tìm file giống nhất" trở thành "tìm điểm **gần** nhất". Chỉ cần định nghĩa **khoảng cách**.

---

## 2. Khoảng cách Euclid

**Là gì.** Khoảng cách "đường chim bay" giữa hai điểm, mở rộng định lý Pythagore ra nhiều chiều.

**Công thức** (hai vector q và v, mỗi vector d số):
```
d(q, v) = √( Σ_{i=1..d} (q_i − v_i)² )
```
| Thành phần | Ý nghĩa |
|---|---|
| `q_i − v_i` | Chênh lệch ở chiều thứ i (một đặc trưng) |
| `(…)²` | Bình phương: bỏ dấu, phạt nặng chênh lệch lớn |
| `Σ` | Cộng mọi chiều |
| `√` | Đưa về cùng đơn vị với đặc trưng |

**Ví dụ 2 chiều:** q = (0, 0), v = (3, 4) → d = √(9 + 16) = **5**.

---

## 3. Vấn đề thang đo — ví dụ bằng 3 nốt A4 thật

Lấy 3 đặc trưng (centroid Hz, ZCR, RMS-CV) của 4 nốt A4 trong dataset (`reports/theory/note_features.csv`):

| | File | Centroid (Hz) | ZCR | RMS-CV |
|---|---|---|---|---|
| **Q** (truy vấn) | `violin_A4_1_fortissimo_arco-normal` | 1 754.2 | 0.0993 | 0.697 |
| V1 | `viola_A4_1_fortissimo_arco-normal` | 2 031.9 | 0.1290 | 0.382 |
| V2 | `guitar_A4_very-long_forte_normal` | 784.8 | 0.0399 | 0.826 |
| V3 | `violin_A4_15_fortissimo_arco-normal` | 1 898.4 | 0.0748 | 0.465 |

**Khoảng cách Euclid trên số gốc:** Q–V3 = 144.2 · Q–V1 = 277.7 · Q–V2 = 969.3.

Trông hợp lý (violin gần violin nhất), nhưng hãy xem **chiều nào quyết định**: với Q–V1, chênh centroid là 277.7, chênh ZCR 0.03, chênh RMS-CV 0.32. Phần của centroid trong d² là **99.9999%**. ZCR và RMS-CV **hoàn toàn vô hình**, chỉ vì centroid đo bằng hàng trăm Hz còn hai đặc trưng kia là số nhỏ hơn 1. Thứ tự đúng ở đây chỉ là **may mắn**.

### Chuẩn hóa z (z-score)
**Là gì.** Đưa mọi đặc trưng về **cùng thang**: trừ trung bình, chia độ lệch chuẩn.
```
z = (x − μ) / σ
```
| Thành phần | Ý nghĩa |
|---|---|
| `μ` | Trung bình của đặc trưng trên **tập tham chiếu** |
| `σ` | Độ lệch chuẩn trên tập tham chiếu |
| `z` | "Cách trung bình bao nhiêu độ lệch chuẩn". z = 0 là trung bình, z = +1 là cao hơn trung bình một độ lệch chuẩn |

Với 4 653 nốt dùng được: centroid μ = 1 498 Hz, σ = 836; ZCR μ = 0.074, σ = 0.063; RMS-CV μ = 0.623, σ = 0.272.

| | z centroid | z ZCR | z RMS-CV | Khoảng cách tới Q | Chiều đóng góp nhiều nhất |
|---|---|---|---|---|---|
| Q (violin) | 0.31 | 0.41 | 0.27 | — | — |
| V3 (violin) | 0.48 | 0.02 | −0.58 | **0.96** | RMS-CV (0.73 trong d² = 0.91) |
| V1 (viola) | 0.64 | 0.88 | −0.89 | 1.30 | RMS-CV (1.35 trong d² = 1.68) |
| V2 (guitar) | −0.85 | −0.54 | 0.75 | 1.57 | centroid (1.34 trong d² = 2.47) |

Sau chuẩn hóa, **cả ba đặc trưng đều có tiếng nói**, và chiều quyết định thay đổi tùy cặp. Đây mới là điều ta muốn.

**Quy tắc vàng:** μ và σ chỉ được tính **một lần trên tập tham chiếu**, rồi dùng nguyên vẹn cho mọi file sau đó, kể cả truy vấn. Nếu tính lại μ, σ cho riêng truy vấn, cùng một âm thanh sẽ ra tọa độ khác, và không còn so được với CSDL. Trong project có hai bộ chuẩn hóa: `scaler_seg` (32 chiều, tính trên nốt REF, [18](18_FEATURE_VECTOR.md) §5) và `scaler_file` (52 chiều, tính trên 500 vector của CSDL).

### Các cách chuẩn hóa khác (và vì sao không dùng)
| Cách | Công thức | Vấn đề |
|---|---|---|
| Min–max | (x − min) / (max − min) | Một giá trị bất thường nén mọi giá trị khác; truy vấn có thể nằm ngoài [0, 1] |
| Chia độ dài vector (L2) | v / ‖v‖ | Biến Euclid thành tương đương cosine (§5), mất thông tin "độ lớn" |

---

## 4. Cân bằng khối: h (20 chiều) và μ (32 chiều)

Vector file v = [h ‖ μ] gồm hai **khối** có số chiều khác nhau ([18](18_FEATURE_VECTOR.md) §5). Sau chuẩn hóa z, mỗi chiều có phương sai 1. Trung bình, mỗi chiều đóng góp **như nhau** vào d², nên khối μ (32 chiều) sẽ quyết định khoảng **62%** khoảng cách, khối h (20 chiều) chỉ 38%, **chỉ vì nó có nhiều chiều hơn**.

**Cân bằng:** chia mỗi khối cho căn bậc hai số chiều của nó:
```
v' = [ x_h / √20  ‖  x_μ / √32 ]       → mỗi khối đóng góp tổng phương sai = 1 → mỗi khối "nói" 50%
```
Nếu sau này muốn ưu tiên một khối, nhân thêm một hệ số λ (mặc định 0.5, nghĩa là cân bằng; chọn trên tập dev) ([NORMALIZATION_PCA](../05_PART_2/02_INDEX/NORMALIZATION_PCA.md)).

---

## 5. Hai khoảng cách khác: Manhattan và cosine

| Độ đo | Công thức | Ý nghĩa | Ví dụ (q = (0,0), v = (3,4)) |
|---|---|---|---|
| **Euclid (L2)** | √Σ(q_i − v_i)² | Đường chim bay | 5 |
| **Manhattan (L1)** | Σ \|q_i − v_i\| | Đi theo "ô bàn cờ"; ít bị một chiều lệch lớn chi phối | 7 |
| **Cosine** | (q · v) / (‖q‖ × ‖v‖), trong [−1, 1] | Chỉ đo **hướng**, bỏ qua độ dài | — |

**Ví dụ phân biệt** (3 chiều): Q = (0.5, −1, 2); V1 = (1, −0.5, 1); V2 = (−0.5, −1, 2.5); V3 = (1, −2, 4) = **2Q**.

| | Euclid | Manhattan | Cosine |
|---|---|---|---|
| Q – V1 | 1.225 | 2.0 | 0.873 |
| Q – V2 | 1.118 | 1.5 | 0.916 |
| Q – V3 | **2.291** (xa nhất) | 3.5 | **1.000** ("giống hệt") |

Cosine coi V3 = 2Q là "giống hệt" Q vì cùng hướng. Trong không gian z, V3 là một âm thanh có **mọi đặc trưng lệch khỏi trung bình gấp đôi** Q (sáng hơn hẳn, rè hơn hẳn…), tức là một âm thanh **khác**. Euclid thấy điều đó, cosine thì không.

**Project dùng Euclid** vì ba lý do:
1. Trong không gian z, **độ lớn có nghĩa** (ví dụ V3 ở trên).
2. **R-tree** cắt tỉa bằng khoảng cách Euclid tới hộp chữ nhật (MINDIST, [21](21_R_TREE.md)).
3. Tính chất **cận dưới** qua PCA ([20](20_PCA.md)) đúng với Euclid. Đây là thứ đảm bảo kết quả tìm kiếm chính xác.

---

## 6. k-NN và Top-K

**Là gì.** **k-NN** (k láng giềng gần nhất) là tìm k điểm trong CSDL có khoảng cách **nhỏ nhất** tới điểm truy vấn. Project trả về **Top-5** (k = 5).

**Cách đơn giản nhất (quét toàn bộ, brute force):** tính khoảng cách tới **mọi** điểm, sắp xếp, lấy 5 cái đầu. Với 500 file × 52 chiều là khoảng 26 000 phép nhân, mất dưới 1 ms. Khi CSDL lớn (hàng triệu file) thì quá chậm, nên cần **chỉ mục** ([21](21_R_TREE.md)). Trong project, quét toàn bộ được giữ lại để **đối chiếu**: kết quả của R-tree phải **giống hệt** kết quả quét toàn bộ.

---

## 7. Từ khoảng cách sang điểm "độ giống"

Người dùng dễ hiểu "giống 85%" hơn "khoảng cách 0.18". Project hiển thị:
```
similarity = 1 / (1 + d)
```
| d | 0 | 0.5 | 1 | 1.87 | 4 |
|---|---|---|---|---|---|
| similarity | 1.00 | 0.67 | 0.50 | 0.35 | 0.20 |

Công thức này **giảm dần** theo d, nên xếp theo similarity giảm dần cũng là xếp theo d tăng dần. Nó **chỉ để hiển thị**; mọi phép xếp hạng dùng d. "0.35" không có nghĩa "giống 35%" theo nghĩa xác suất, chỉ là một thang dễ đọc.

---

## 8. Chấm điểm kết quả tìm kiếm

**Một kết quả là "đúng" (relevant)** nếu cùng **nhạc cụ** với truy vấn. Metadata chỉ dùng ở bước chấm này, không dùng để tìm ([16](16_DATASET_MODEL.md) §2).

| Độ đo | Công thức | Ý nghĩa |
|---|---|---|
| **Precision@5** | (số kết quả đúng trong Top-5) / 5 | Trong 5 kết quả trả về, bao nhiêu % đúng nhạc cụ |
| **MRR** | trung bình của 1 / (hạng của kết quả đúng **đầu tiên**) | Kết quả đúng xuất hiện sớm tới đâu |
| **Ma trận nhầm lẫn** | Đếm: truy vấn nhạc cụ A → kết quả nhạc cụ B | Thấy rõ cặp nào hay nhầm (dự kiến violin ↔ viola, cello ↔ double bass) |

**Ví dụ.** Truy vấn violin, Top-5 = [violin, viola, violin, violin, cello] → P@5 = 3/5 = **0.6**; kết quả đúng đầu tiên ở hạng 1 → 1/1 = 1. Một truy vấn khác có kết quả đúng đầu tiên ở hạng 2 → 1/2. MRR của hai truy vấn = (1 + 0.5) / 2 = **0.75**.

**Phải báo cáo theo từng nhạc cụ**, không chỉ con số chung. Một con số chung cao có thể che một nhạc cụ rất kém (ví dụ viola).

**Truy vấn nhạc cụ ngoài CSDL** (banjo, mandolin) không có kết quả "đúng". Với chúng, project xem **khoảng cách tới kết quả gần nhất**. Nếu khoảng cách này thường **lớn hơn hẳn** so với truy vấn nhạc cụ có trong CSDL, có thể đặt một **ngưỡng** để báo "không tìm thấy nhạc cụ tương tự" ([10](10_BANJO_MANDOLIN.md) §4).

---

## 9. Áp dụng cho 5 nhạc cụ (dự đoán, kiểm tra ở Phần 2)

| Truy vấn | Kết quả dự kiến | Lý do (từ các file nhạc cụ) |
|---|---|---|
| Guitar | P@5 cao | Đường bao gảy khác hẳn 4 nhạc cụ kéo vĩ |
| Double bass | Khá cao, nhầm với cello | ZCR thấp, nốt rất trầm; MFCC c5 tách được cello |
| Cello | Nhầm với double bass, viola | Ở giữa; bị phòng thu ảnh hưởng mạnh ([07](07_CELLO.md) §9.1) |
| Violin, viola | **Nhầm lẫn nhau nhiều nhất** | Không đặc trưng nào tách quá 19% ([15](15_AUDIO_FEATURES.md) §13) |
