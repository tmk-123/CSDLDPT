# 22. CSDL đa phương tiện và tìm kiếm theo nội dung

> **Đọc xong file này bạn sẽ biết:** tìm kiếm âm thanh **theo nội dung** khác tìm theo từ khóa ở đâu; hai giai đoạn của hệ thống (xây CSDL và trả lời truy vấn) và vì sao chúng phải dùng **cùng một hàm**; lưu trữ hỗn hợp (file trên đĩa, thông tin trong CSDL); bốn loại metadata; mô hình dữ liệu và cách lưu vector; chỉ mục; đường đi đầy đủ của một truy vấn, kèm các kết quả trung gian; những gì cần trung thực khi đánh giá.
> **Cần biết trước:** [16](16_DATASET_MODEL.md) (mô hình dữ liệu), [18](18_FEATURE_VECTOR.md)–[21](21_R_TREE.md).
> **Đây là file cuối** của phần lý thuyết. Quay lại [README](README.md) để xem bản đồ toàn bộ.

---

## 1. Tìm theo nội dung là gì

| | Tìm theo **từ khóa** | Tìm theo **nội dung** (CBAR) |
|---|---|---|
| Người dùng đưa vào | Chữ: "violin" | **Một file âm thanh mẫu** (*query by example*) |
| Hệ thống so sánh | Chữ với nhãn đã gán sẵn | **Đặc trưng tính từ tín hiệu** ([15](15_AUDIO_FEATURES.md)) |
| Cần nhãn không? | Có, mọi file phải được gán nhãn trước | **Không**: chỉ cần âm thanh |
| Trả lời câu hỏi | "File nào **được gán nhãn** violin?" | "File nào **nghe giống** file này?" |

**CBAR** (*Content-Based Audio Retrieval*) là tìm kiếm âm thanh theo nội dung. Nó cần thiết vì file người dùng đưa vào **không có nhãn** ([12](12_DIGITAL_AUDIO.md) §6), và vì "nghe giống" không phải lúc nào cũng trùng với một nhãn có sẵn: một tiếng banjo vẫn "giống" guitar ở một mức nào đó ([10](10_BANJO_MANDOLIN.md)).

---

## 2. Hai giai đoạn — và một quy tắc bất di bất dịch

```
GIAI ĐOẠN XÂY (offline, làm một lần)
  500 sequence → audio_to_vector() → v (52) → chuẩn hóa + PCA → v' (52), u (8)
               → lưu vào CSDL + đưa u vào R-tree

GIAI ĐOẠN TRUY VẤN (online, mỗi lần người dùng hỏi)
  1 file mới   → audio_to_vector() → v (52) → transform (KHÔNG fit lại) → v', u
               → R-tree lọc → tinh chỉnh 52 chiều → Top-5
```
**Quy tắc:** truy vấn phải đi qua **đúng cùng một hàm** và **cùng tham số** (tần số lấy mẫu, frame, prototype, μ, σ, PCA) như file trong CSDL. Chỉ cần một tham số khác, tọa độ của truy vấn và của CSDL không còn so được với nhau, và khoảng cách trở nên vô nghĩa. Vì vậy trong code **không có hàm riêng cho truy vấn** ([QUERY_PIPELINE](../05_PART_2/04_QUERY/QUERY_PIPELINE.md)), và mọi mô hình đã học được đóng gói theo một **`model_version`**.

---

## 3. Lưu trữ hỗn hợp

| Ở đâu | Lưu gì | Vì sao |
|---|---|---|
| **Hệ thống file** | File âm thanh (`raw/`, `data/notes/`, `data/sequences/`) | File lớn (vài trăm KB tới vài MB); phát trực tiếp được; không cần truy vấn bên trong |
| **CSDL (SQLite)** | Metadata, **đường dẫn** tới file, **vector đặc trưng** | Nhỏ, truy vấn nhanh bằng SQL, ràng buộc toàn vẹn |
| **File chỉ mục** | R-tree (`data/index/rtree_v1.*`) | Thư viện R-tree quản lý riêng; khóa trùng `audio_id` trong CSDL |

Đây là cách làm phổ biến của các hệ CSDL đa phương tiện: CSDL nhỏ gọn, file media được phục vụ trực tiếp.

---

## 4. Bốn loại metadata

| Loại | Nghĩa | Ví dụ trong project |
|---|---|---|
| **Kỹ thuật** | Mô tả **file** | Tần số lấy mẫu, số kênh, thời lượng, định dạng, MD5 |
| **Mô tả** | Mô tả **nội dung âm nhạc** | Nhạc cụ, dây, nốt, cường độ, kỹ thuật chơi |
| **Cấu trúc** | Mô tả **các phần** bên trong | Sequence gồm những nốt nào, bắt đầu lúc nào; các đoạn tách được |
| **Quản trị** | Mô tả **nguồn gốc, trạng thái** | Nguồn thu, giấy phép, trạng thái lọc (OK, TOO_SHORT…), tập dữ liệu, `model_version` |

Metadata **mô tả** là nhãn do con người đặt. Nó dùng để chia dữ liệu và chấm điểm, **không** dùng để tìm ([16](16_DATASET_MODEL.md) §2).

---

## 5. Mô hình dữ liệu và lưu vector

**Nguyên tắc: một đối tượng media = một bản ghi.** Một file âm thanh là một dòng trong bảng `audio_file`. Các đơn vị phân tích nhỏ hơn có vai trò khác nhau:
- **Đoạn** (segment) được lưu (bảng `segment`) để **giải thích** kết quả.
- **Frame** **không** được lưu: hàng trăm frame mỗi file, chỉ là bước tính trung gian.

```
instrument 1──n source_note           (nốt đơn gốc: nhạc cụ, dây, nốt, kỹ thuật, nguồn…)
instrument 1──n audio_file            (đối tượng tìm kiếm: sequence, phrase, truy vấn)
audio_file 1──n sequence_note n──1 source_note   (sequence gồm những nốt nào: ground truth)
audio_file 1──n segment               (các đoạn tách được, 32 đặc trưng mỗi đoạn)
audio_file 1──1 file_vector           (v 52 số, v' 52 số, u 8 số)
instrument 1──n prototype             (20 prototype, 32 số mỗi cái)
```
Chi tiết bảng: [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md).

**Lưu vector thế nào:**
| Cách | Ưu | Nhược | Project |
|---|---|---|---|
| **BLOB nhị phân** (float32) | Gọn (52 × 4 = 208 byte), nhanh, chính xác | Không đọc được bằng mắt | **Chọn** |
| JSON / văn bản | Dễ đọc | Chậm, tốn chỗ, có thể mất độ chính xác | Chỉ khi xuất dữ liệu |
| Kiểu mảng (PostgreSQL `real[]`) | Truy vấn được từng phần tử | Cần PostgreSQL | Không |
| pgvector | Có chỉ mục sẵn | Chỉ mục là HNSW, **không phải R-tree**; tìm gần đúng | Không |
| Cột tọa độ + chỉ mục không gian (SQLite R\*Tree) | Chỉ mục nằm trong CSDL | SQLite R\*Tree tối đa 5 chiều | Dự phòng nếu PCA còn 5 chiều |

---

## 6. Đường đi của một truy vấn — kèm kết quả trung gian

Ví dụ: người dùng đưa vào một đoạn cello 5.84 s (số liệu minh họa).

| # | Bước | Kết quả trung gian (hệ thống in ra) | Lý thuyết |
|---|---|---|---|
| 1 | Kiểm tra file | Đọc được; 0.3 s ≤ thời lượng ≤ 60 s | [12](12_DIGITAL_AUDIO.md) |
| 2 | Tiền xử lý | Mono, 22 050 Hz, lọc 25 Hz, chuẩn hóa đỉnh | [12](12_DIGITAL_AUDIO.md) §7 |
| 3 | Tách nốt | Dạng sóng + vạch ranh giới: **6 đoạn** | [17](17_ONSET_SEGMENTATION.md) |
| 4 | Đặc trưng từng đoạn | Bảng: F0 (146.8 Hz → D3), centroid, RMS-CV, ZCR, MFCC 1–3 | [15](15_AUDIO_FEATURES.md) |
| 5 | So với prototype | Mỗi đoạn: prototype gần nhất (ví dụ "cello-2", w = 0.71) và **nốt REF gần nhất** (ví dụ `cello_D3_1_forte_arco-normal.mp3`) | [18](18_FEATURE_VECTOR.md) §4 |
| 6 | Vector file | **h gộp theo nhạc cụ:** cello 62% · viola 21% · double bass 12% · violin 4% · guitar 1% | [18](18_FEATURE_VECTOR.md) §5 |
| 7 | Chuẩn hóa + PCA | u (8 số): [−1.74, 0.62, 0.05, …] | [19](19_DISTANCE_SIMILARITY.md), [20](20_PCA.md) |
| 8 | R-tree lọc | k' = 20 → 40; 40/500 ứng viên; 2 vòng | [21](21_R_TREE.md) §5.3 |
| 9 | Tinh chỉnh 52 chiều | Top-5: hạng, file, nhạc cụ, d (52 chiều), d (8 chiều), similarity | [19](19_DISTANCE_SIMILARITY.md) §7 |
| 10 | Hình không gian | PC1 – PC2 của CSDL, tô truy vấn và Top-5 | [20](20_PCA.md) §6 |

Bảng đầy đủ những gì phải in: [INTERMEDIATE_RESULTS](../05_PART_2/04_QUERY/INTERMEDIATE_RESULTS.md).

---

## 7. Đánh giá trung thực

| Điều cần làm | Vì sao |
|---|---|
| So Top-5 của R-tree với quét toàn bộ (phải trùng 100%) | Chứng minh lọc – tinh chỉnh **chính xác** ([21](21_R_TREE.md) §5.3) |
| Báo cáo P@5, MRR **theo từng nhạc cụ** và ma trận nhầm lẫn | Con số chung có thể che một nhạc cụ kém ([19](19_DISTANCE_SIMILARITY.md) §8) |
| Chọn tham số trên tập dev, chạy tập truy vấn **một lần** | Chống rò rỉ ([16](16_DATASET_MODEL.md) §7) |
| Báo cáo riêng truy vấn **khác nguồn thu** | Đặc trưng hiện tại gần như không "chuyển" sang nguồn thu khác (1-NN 29–53%, [15](15_AUDIO_FEATURES.md) §16.1). Nếu chỉ đánh giá trên tập trộn nguồn, kết quả sẽ **lạc quan** (mục chờ P12) |
| Báo cáo truy vấn phrase (nhạc thật) và unseen (banjo, mandolin) | Đo hạn chế của sequence ghép và hành vi khi không có đáp án ([10](10_BANJO_MANDOLIN.md) §4) |
| Nói rõ R-tree không nhanh hơn quét toàn bộ ở 500 điểm | Giá trị của R-tree ở đây là minh họa cơ chế ([21](21_R_TREE.md) §7) |

---

## 8. Toàn bộ chuỗi, từ nhạc cụ tới kết quả

```
Nhạc cụ (thân đàn, dây)                         [04]–[10]
   ↓ người chơi chọn dây, nốt, cách chơi        [05]–[11]
Âm thanh trong không khí (F0, harmonic, âm sắc) [01]–[03]
   ↓ micro, lấy mẫu                              [12]
File âm thanh (dãy mẫu)                          [12]
   ↓ dạng sóng, phổ                              [13], [14]
Đoạn ≈ nốt                                       [17]
   ↓ 32 đặc trưng mỗi đoạn                       [15]
Vector file 52 chiều (h ‖ μ)                     [18]
   ↓ chuẩn hóa, cân bằng khối                    [19]
8 chiều (PCA)                                    [20]
   ↓ R-tree lọc, 52 chiều tinh chỉnh             [21]
Top-5 file nghe giống nhất + kết quả trung gian  [22]
```
