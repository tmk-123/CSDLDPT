# PROJECT OVERVIEW

## 1. Đề bài (nguyên văn tóm tắt từ `yeu_cau.txt`)
**Xây dựng hệ CSDL lưu trữ và tìm kiếm tiếng nhạc cụ bộ dây.**
1. Xây dựng/sưu tầm **≥ 500 file** âm thanh của các nhạc cụ bộ dây. Mỗi file chỉ chứa tiếng **một nhạc cụ**, đủ dài để nhận diện. Mô tả điểm giống và khác nhau giữa tiếng các nhạc cụ.
2. Xây dựng bộ đặc trưng nhận diện âm thanh nhạc cụ; trình bày các đặc trưng và **giá trị thông tin** của chúng.
3. Triển khai thuật toán trích rút đặc trưng; xây dựng **hệ CSDL** quản trị đặc trưng của mọi file.
4. Hệ thống tìm kiếm: đầu vào là một file âm thanh mới (nhạc cụ **đã có hoặc chưa có** trong dữ liệu), đầu ra là **5 file giống nhất**, xếp giảm dần theo độ tương đồng.
   a. Sơ đồ khối, chức năng và vào/ra của từng khối; quy trình thực hiện.
   b. Minh họa **kết quả trung gian** (giá trị đặc trưng, tính độ tương đồng).
   c. Đánh giá kết quả.
5. Demo.

## 2. Hệ thống đang xây dựng (một đoạn)
Một hệ **CBAR** (Content-Based Audio Retrieval). CSDL chứa **500 file multi-note** của 5 nhạc cụ: violin, viola, cello, double bass, guitar. Mỗi file được biến thành **một vector 52 chiều**. Vector này gồm hai phần: (a) mức độ giống với 20 "prototype âm sắc" học từ thư viện nốt đơn; (b) âm sắc trung bình. Vector được giảm xuống **8D bằng PCA** và đánh chỉ mục bằng **R\*-tree**. File truy vấn đi qua **đúng pipeline đó**; R-tree lọc ứng viên, rồi khoảng cách Euclid 52D xếp hạng ra **Top-5 chính xác**.

### 2.1. Nhạc cụ sử dụng
Project dùng **7 nhạc cụ dây**: 5 nhạc cụ **trong CSDL** (được lưu và tìm kiếm) và 2 nhạc cụ **ngoài CSDL** (chỉ dùng làm file truy vấn, để thử khi nhạc cụ "chưa có trong dữ liệu" như đề bài mục 4 yêu cầu).

| Nhạc cụ | Vai trò | Cách tạo âm | Cách chơi được dùng | Nốt dùng được (Philharmonia + Iowa) | Lý thuyết |
|---|---|---|---|---|---|
| Violin | Trong CSDL | Kéo vĩ | arco: thường, vibrato mạnh, không vibrato | 1 141 (897 + 244) | [05_VIOLIN](../01_THEORY/05_VIOLIN.md) |
| Viola | Trong CSDL | Kéo vĩ | arco | 990 (728 + 262) | [06_VIOLA](../01_THEORY/06_VIOLA.md) |
| Cello | Trong CSDL | Kéo vĩ | arco | 1 047 (759 + 288) | [07_CELLO](../01_THEORY/07_CELLO.md) |
| Double bass | Trong CSDL | Kéo vĩ | arco | 1 030 (751 + 279) | [08_DOUBLE_BASS](../01_THEORY/08_DOUBLE_BASS.md) |
| Guitar | Trong CSDL | Gảy | gảy thường, harmonic | 445 (106 + 339) | [09_GUITAR](../01_THEORY/09_GUITAR.md) |
| Banjo | Truy vấn ngoài CSDL | Gảy | gảy thường | 74 file (chỉ Philharmonia) | [10_BANJO_MANDOLIN](../01_THEORY/10_BANJO_MANDOLIN.md) |
| Mandolin | Truy vấn ngoài CSDL | Gảy | gảy thường, vê (tremolo) | 80 file (chỉ Philharmonia) | [10_BANJO_MANDOLIN](../01_THEORY/10_BANJO_MANDOLIN.md) |

- **Vì sao chọn bộ này:** có cả hai cách tạo âm (kéo vĩ và gảy); có sẵn nhạc cụ ngoài CSDL để thử; đủ dữ liệu sau khi bổ sung guitar ([RESULTS_REPORT](RESULTS_REPORT.md) §3.1; quyết định D01).
- **Hai nguồn thu:** Philharmonia (MP3) cho cả 7 nhạc cụ; University of Iowa MIS (AIFF) cho 5 nhạc cụ trong CSDL. Lý do: guitar Philharmonia chỉ có 106 nốt (cần ≥ 360), và mọi nhạc cụ cần ≥ 2 nguồn để hệ thống không "nhận phòng thu" thay vì nhận nhạc cụ (D21).
- **Cách chơi khác** (pizzicato, col legno, ponticello, harmonic của bộ kéo vĩ…): 573 nốt **không bị xóa**, mà để riêng trong `data/excluded/technique/` (D20; lý do ở [11_PLAYING_TECHNIQUES](../01_THEORY/11_PLAYING_TECHNIQUES.md) §5).
- **Giới hạn đã biết:** CSDL có 4 nhạc cụ kéo vĩ nhưng **chỉ 1 nhạc cụ gảy** (guitar), và 76% nốt guitar đến từ Iowa. Cách chấm điểm không bị lệch (CSDL cân bằng theo nhạc cụ), nhưng "gảy" và "guitar" trùng nhau, nên truy vấn gảy của nhạc cụ khác hay bị xếp gần guitar. Phân tích, số đo và phương án: [10_BANJO_MANDOLIN](../01_THEORY/10_BANJO_MANDOLIN.md) §5; mục chờ **P13**.
- Tổng: **4 653 nốt dùng được** của 5 nhạc cụ trong CSDL; 445 đoạn phrase thật (violin, viola, cello, double bass) dùng làm truy vấn nhạc thật. Số liệu chi tiết: [RESULTS_REPORT](RESULTS_REPORT.md) §0, §7.

## 3. Chia phần làm việc

| Phần | Nội dung | Ứng với đề | Trạng thái |
|---|---|---|---|
| **PHẦN 1** | Dataset → tiền xử lý → đặc trưng → segmentation → prototype → **vector 52D cho mỗi file** | Mục 1, 2, trích rút của mục 3 | **Đang làm** |
| **PHẦN 2** | CSDL SQLite → chuẩn hóa + PCA → **R-tree** → tìm k-NN → truy vấn Top-5 | CSDL của mục 3; mục 4, 4a, 4b | **Đang làm** |
| Phần sau | Đánh giá, kiến trúc tổng, demo | Mục 4c, 5 | Để sau |

Ranh giới giữa hai phần được định nghĩa trong [PART_1_OUTPUT_SPEC.md](../04_PART_1/05_OUTPUT/PART_1_OUTPUT_SPEC.md).

## 4. Trả lời nhanh 16 câu hỏi cốt lõi

| # | Câu hỏi | Trả lời ngắn | Chi tiết |
|---|---|---|---|
| 1 | Đang xây cái gì? | CBAR: 500 file multi-note, vector cố định, R-tree, Top-5 | §2 ở trên |
| 2 | Tại sao thu thập single-note? | Mẫu "sạch", nhãn chắc chắn, mỗi file đúng một sự kiện. Đây là nguyên liệu tốt nhất để học "một nốt violin/cello trông thế nào" trong không gian đặc trưng | [DATASET_ROLES](../04_PART_1/01_DATASET/DATASET_ROLES.md) |
| 3 | Single-note dùng làm gì? | (a) Tập REF học 20 prototype; (b) tập DB-POOL / QUERY-POOL là nguyên liệu ghép multi-note. Các tập không giao nhau | [SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md) |
| 4 | Multi-note dùng làm gì? | Là 500 record được lưu và tìm kiếm; cũng là dạng của file truy vấn | [SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md) |
| 5 | File thành vector thế nào? | Segmentation → mỗi segment 32D → so với 20 prototype → histogram mềm 20D ‖ trung bình 32D = 52D | [FILE_LEVEL_VECTOR](../04_PART_1/03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md) |
| 6 | Tại sao segmentation? | Đơn vị của REF là "một nốt", nên phía multi-note cũng cần đơn vị "một nốt" để so sánh | [SEGMENTATION](../04_PART_1/04_FEATURE_EXTRACTION/SEGMENTATION.md) |
| 7 | Segmentation bằng gì? | Energy gating + SuperFlux onset + peak-picking + hậu xử lý | như trên |
| 8 | Feature extraction bằng gì? | STFT → MFCC c1–13 mean/std, log centroid/bandwidth/rolloff, ZCR, RMS-CV, median log2 f0 | [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md) |
| 9 | Single-note liên hệ với multi-note thế nào? | Qua **prototype**: mỗi segment được đo khoảng cách tới 20 prototype học từ REF | [REFERENCE_PROTOTYPES](../04_PART_1/03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md) |
| 10 | Vector tạo chính xác thế nào? | `h_j = Σ α_i·w_ij`, `μ = Σ α_i·z_i`, `v = [h‖μ]` | [FILE_LEVEL_VECTOR](../04_PART_1/03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md) |
| 11 | Tại sao cùng số chiều? | Khoảng cách, PCA và R-tree chỉ định nghĩa được trong cùng một không gian ℝ^d | như trên |
| 12 | R-tree ở đâu? | Sau PCA. Index 500 **điểm 8D**, không phải audio | [RTREE_INDEX](../05_PART_2/02_INDEX/RTREE_INDEX.md) |
| 13 | Query đi qua gì? | **Đúng hàm `audio_to_vector()`**, dùng tham số đã fit, rồi k-NN | [QUERY_PIPELINE](../05_PART_2/04_QUERY/QUERY_PIPELINE.md) |
| 14 | Similarity tính thế nào? | Euclid 52D; hiển thị `sim = 1/(1+d)` | [KNN_SEARCH](../05_PART_2/03_SEARCH/KNN_SEARCH.md) |
| 15 | Lấy Top-5 thế nào? | Multi-step k-NN: R-tree 8D (cận dưới) → refine 52D → dừng sớm vẫn đúng tuyệt đối | như trên |
| 16 | Đánh giá thế nào? | P@5, Top-1, MRR (relevant = cùng nhạc cụ); onset F-measure; R-tree == brute force | [07_EVALUATION](../07_EVALUATION/README.md) |
