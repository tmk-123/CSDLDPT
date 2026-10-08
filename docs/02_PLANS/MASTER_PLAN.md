# MASTER PLAN — Project làm gì, theo thứ tự nào, và vì sao

> **Đây là "hợp đồng thiết kế".** Mọi thuật toán, tham số, số lượng dữ liệu dưới đây là phương án **đã chốt**. Muốn đổi bất kỳ điều gì, phải ghi vào [DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md) trước.
>
> **Ba loại tài liệu, ba câu hỏi khác nhau:**
> | Tài liệu | Trả lời |
> |---|---|
> | **MASTER_PLAN** (file này) | Project **làm gì** ở từng bước, theo thứ tự nào, **vì sao** |
> | [IMPLEMENTATION](../03_WORKFLOWS/IMPLEMENTATION.md) | **Hàm nào** được gọi, ở **file nào**, **tham số** gì, ra **kết quả** gì |
> | [01_THEORY](../01_THEORY/README.md) | **Bản chất**, công thức, cách hoạt động của từng khái niệm và thuật toán |
>
> File này cố ý **không** đi sâu vào công thức hay thư viện; mỗi bước có link tới bài lý thuyết tương ứng.

---

## 0. Bức tranh toàn cảnh

**Bài toán.** Người dùng đưa vào **một file âm thanh** của một nhạc cụ dây. Hệ thống trả về **5 file trong CSDL nghe giống nhất** (Top-5). Hệ thống phải tự "nghe" nội dung âm thanh, vì file của người dùng không có nhãn ([22_MULTIMEDIA_DATABASE](../01_THEORY/22_MULTIMEDIA_DATABASE.md) §1).

**Ý tưởng chính.** Biến mỗi file âm thanh thành **một dãy số cố định** (vector). Hai file nghe giống nhau thì hai vector **gần nhau**. Tìm kiếm trở thành "tìm 5 vector gần nhất".

```
RAW AUDIO            dữ liệu gốc tải về
  → FILTERING          lọc file hỏng/trùng/quá ngắn, chọn nốt, chia tập             Bước 1 ✅
  → PREPROCESSING      đưa mọi file về cùng một dạng tín hiệu                      Bước 2
  → (TẠO AUDIO CSDL)   ghép nốt đơn thành 500 + 100 đoạn nhạc có đáp án            Bước 5
  → SEGMENTATION       chia đoạn nhạc thành các đoạn ngắn ≈ từng nốt                Bước 6
  → FEATURE EXTRACTION mỗi đoạn → 32 con số mô tả âm sắc                           Bước 3
  → REFERENCE PROTOTYPES  học 20 "kiểu âm mẫu" (4 cho mỗi nhạc cụ) từ nốt đơn      Bước 4
  → REFERENCE MATCHING mỗi đoạn giống từng kiểu âm mẫu bao nhiêu                   Bước 7
  → FIXED-LENGTH VECTOR cả file → đúng 52 con số                                   Bước 7
  → DATABASE           lưu vector + thông tin mô tả vào SQLite                     Bước 8
  → NORMALIZATION      đưa 52 con số về cùng thang đo                              Bước 9
  → PCA                rút gọn 52 → 8 con số để đánh chỉ mục                       Bước 9
  → R-TREE             xếp 500 điểm 8 chiều vào cây để tìm nhanh                   Bước 10
  → SIMILARITY SEARCH  tìm Top-5: lọc bằng R-tree, xếp hạng chính xác bằng 52 số   Bước 10–11
  → EVALUATION         đo hệ thống đúng tới đâu                                    sau Phần 1, 2
```
Cột "Bước" là **thứ tự viết code** trong [PART_1_PLAN](PART_1_PLAN.md) và [PART_2_PLAN](PART_2_PLAN.md). Nó hơi khác thứ tự đọc ở trên: ví dụ hàm tính đặc trưng (Bước 3) được viết trước hàm chia đoạn (Bước 6), vì việc học kiểu âm mẫu (Bước 4) chỉ cần nốt đơn, chưa cần chia đoạn.

**Ba loại "dữ liệu" xuất hiện xuyên suốt** (chi tiết: [16_DATASET_MODEL](../01_THEORY/16_DATASET_MODEL.md)):
- **Nốt đơn**: file chỉ chứa **một** nốt nhạc, nhãn chắc chắn (nhạc cụ, nốt, cường độ, cách chơi). Là nguyên liệu.
- **Sequence** (đoạn nhạc): file chứa **4–8 nốt** liên tiếp của **một** nhạc cụ, project tự ghép từ nốt đơn. 500 sequence là **nội dung CSDL**; 100 sequence khác là **truy vấn thử**.
- **Segment** (đoạn ngắn): một phần của sequence, xấp xỉ **một nốt**, do bước chia đoạn tìm ra.

---

## 1. RAW AUDIO → FILTERING: chuẩn bị dữ liệu (Bước 1, ✅ đã xong)

**Mục tiêu.** Từ các bộ dữ liệu tải về, có được một **danh sách nốt đơn sạch, có nhãn đúng**, chia sẵn vào các tập dùng cho những việc khác nhau, sao cho **không rò rỉ** (không có chuyện cùng một nốt vừa dùng để xây CSDL vừa dùng để thử).

**INPUT.**
- **4 477 file MP3** của Philharmonia (7 nhạc cụ: violin, viola, cello, double bass, guitar, banjo, mandolin).
- **188 file AIFF** của Iowa MIS (5 nhạc cụ trong CSDL), mỗi file chứa một dãy nốt liên tiếp. Bổ sung theo D21 vì guitar Philharmonia chỉ có 106 nốt.

**Làm gì, theo thứ tự:**
```
4 477 MP3 (Philharmonia) + 188 AIFF (Iowa)
 → [Iowa] cắt mỗi file nhiều nốt thành từng nốt đơn                 ý nghĩa: Iowa ghi liền nhiều nốt; cần tách ra để
                                                                   cùng đơn vị "một nốt" với Philharmonia → 1 429 nốt
 → đọc TÊN FILE để lấy nhãn: nhạc cụ, nốt, cường độ, cách chơi,     ý nghĩa: file âm thanh không tự chứa nhãn; nhãn chỉ
   độ dài danh nghĩa (Philharmonia); thêm dây đàn (Iowa)             có trong tên file ([12] §6)
 → đổi tên nốt ra số MIDI (A4 = 69)                                  ý nghĩa: dùng một con số để tính toán và chia tập
 → GIẢI MÃ từng file (ffmpeg) về mono 22 050 Hz                      ý nghĩa: kiểm tra file đọc được không; lấy tín hiệu
                                                                   để đo
 → lọc tiếng ù hạ âm 25 Hz rồi ĐO: thời lượng, phần có âm            ý nghĩa: biết file có đủ âm thanh để dùng không;
   (năng lượng > −40 dB so với đỉnh), đỉnh, số mẫu bị cắt đỉnh       tiếng ù làm đo sai nên phải lọc trước (D27)
 → tính MD5 (dấu vân tay nội dung) của từng file                     ý nghĩa: hai file cùng MD5 là giống hệt nhau
 → GẮN TRẠNG THÁI: CORRUPT (không đọc được) → DUPLICATE (trùng MD5)  ý nghĩa: loại file hỏng, file trùng (có cặp trùng
   → TOO_SHORT (phần có âm < 0.35 s) → còn lại OK                     mang nhãn hai nhạc cụ khác nhau), nốt quá ngắn
 → GẮN VAI TRÒ (split):                                              ý nghĩa: mỗi file chỉ làm một việc
     banjo, mandolin → UNSEEN (truy vấn "nhạc cụ ngoài CSDL")
     đoạn nhạc thật nhiều nốt (phrase) → PHRASE (truy vấn nhạc thật)
     cách chơi không dùng (bộ kéo vĩ chỉ giữ arco; guitar giữ gảy thường + harmonic, D20) → NONE
     còn lại chia THEO CAO ĐỘ: midi mod 5 = 0, 1 → REF; = 2, 3 → DB_POOL; = 4 → QUERY_POOL   (D24)
 → CHỌN trong giới hạn: mỗi nhạc cụ tối đa REF 150, DB_POOL 200, QUERY_POOL 60,
   trải đều theo (nguồn, cao độ, cường độ) (D23)                     ý nghĩa: các nhạc cụ được đối xử ngang nhau
 → chép file vào thư mục theo nhạc cụ, ghi bảng catalog
```
**Vì sao chia theo cao độ (`midi mod 5`).** Cùng một nốt của cùng nhạc cụ thì âm rất giống nhau, kể cả khác cường độ. Nếu nốt A4 của violin vừa nằm trong CSDL vừa nằm trong truy vấn, hệ thống sẽ "tìm thấy chính nó" và kết quả đẹp giả tạo. Chia theo cao độ đảm bảo mọi bản thu của một cao độ đi chung một tập. Chia xen kẽ (mod 5) giúp tập nào cũng phủ đủ vùng trầm, giữa, cao ([16_DATASET_MODEL](../01_THEORY/16_DATASET_MODEL.md) §7).

**Ba tập nốt đơn và việc của chúng:**
| Tập | Dùng để | Không bao giờ dùng để |
|---|---|---|
| **REF** (tham chiếu) | Học "kiểu âm mẫu" của từng nhạc cụ (§5) | Ghép sequence |
| **DB_POOL** | Ghép 500 sequence của CSDL (§3) | Ghép truy vấn |
| **QUERY_POOL** | Ghép 100 sequence truy vấn (§3) | Học hay chỉnh bất kỳ tham số nào |

**OUTPUT.**
- `data/catalog.csv`: **5 906 dòng**, mỗi file một dòng (nguồn, nhạc cụ, dây, nốt, MIDI, cường độ, cách chơi, phần có âm, MD5, trạng thái, tập, được chọn hay không, đường dẫn).
- **4 653 nốt dùng được** của 5 nhạc cụ, gom trong `data/notes/<nhạc cụ>/<nguồn>/`; 445 phrase và 154 file banjo/mandolin trong `data/queries/`; 654 file không dùng trong `data/excluded/<lý do>/`.
- Kiểm tra tự động: `tests/test_catalog.py` 12/12 đạt.

**Dùng ở bước sau.** REF → học kiểu âm mẫu (§5). DB_POOL, QUERY_POOL → ghép sequence (§3). PHRASE, UNSEEN → truy vấn khi đánh giá (§13).

**Vì sao cần.** Hệ thống chỉ tốt bằng dữ liệu của nó: nhãn sai, file hỏng hay rò rỉ giữa các tập đều làm kết quả sai hoặc đẹp giả. Chi tiết và số liệu: [RESULTS_REPORT](../00_PROJECT/RESULTS_REPORT.md), [DATASET_COLLECTION_AND_FILTERING](../04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md), [SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md).

---

## 2. PREPROCESSING: đưa mọi file về cùng một dạng (Bước 2)

**Mục tiêu.** Mọi file, dù là MP3 hay AIFF hay file của người dùng, đều được biến thành **cùng một dạng tín hiệu**, để các con số tính sau này so sánh được với nhau.

**INPUT.** Một file âm thanh bất kỳ (nốt đơn, sequence, phrase, hay truy vấn của người dùng).

**Làm gì, theo thứ tự:**
```
File audio (mp3 / wav / aiff / …)
 → DECODE: giải nén thành dãy mẫu                      ý nghĩa: máy chỉ tính toán được trên dãy số ([12] §1)
 → MONO: trung bình các kênh (nếu file stereo)          ý nghĩa: mọi file có đúng một dãy số
 → RESAMPLE về 22 050 Hz (22 050 mẫu mỗi giây)          ý nghĩa: mọi file cùng "độ phân giải thời gian". Giữ được
                                                        mọi tần số dưới 11 025 Hz, đủ cho 5 nhạc cụ; nhanh gấp 2
                                                        so với 44 100 Hz ([12] §3; D04)
 → LỌC THÔNG CAO 25 Hz                                  ý nghĩa: bỏ tiếng ù hạ âm (tai không nghe được) có trong
                                                        nhiều bản thu (D27)
 → PEAK-NORMALIZE về 0.95: nhân cả dãy để mẫu lớn nhất  ý nghĩa: micro đặt gần hay xa không phải đặc điểm của nhạc
   có độ lớn đúng 0.95                                  cụ; bỏ khác biệt đó đi (D05)
 → [chỉ với nốt đơn] TRIM: cắt khoảng lặng đầu và cuối  ý nghĩa: khoảng lặng làm sai các giá trị trung bình
   (phần nhỏ hơn đỉnh 40 dB)
 → [chỉ với nốt REF] giữ tối đa 1.5 giây đầu            ý nghĩa: để nốt REF giống các đoạn trong sequence (dài
                                                        0.35–1.2 s)
 → y: dãy số thực float32 trong [−1, 1]
```
> **Ký hiệu `y`**: tín hiệu âm thanh sau tiền xử lý, tức là **dãy mẫu** (mỗi mẫu là độ lớn của áp suất âm tại một thời điểm, cách nhau 1/22 050 giây). Một file 5 giây có `y` gồm 110 250 con số.

**Phương pháp và tham số đã chốt:** 22 050 Hz · mono · lọc thông cao 25 Hz · peak-normalize 0.95 · trim −40 dB (chỉ nốt đơn) · REF ≤ 1.5 s · **không** pre-emphasis (độ dốc của phổ chính là thông tin âm sắc).

**OUTPUT.** `y` (float32).

**Dùng ở bước sau.** Mọi bước còn lại: ghép sequence (§3), chia đoạn (§4), tính đặc trưng (§5).

**Vì sao cần.** Nếu file CSDL ở 44 100 Hz còn truy vấn ở 22 050 Hz, hay một file to gấp đôi file kia, các con số tính ra sẽ khác nhau **dù âm thanh giống nhau**. Một hàm tiền xử lý duy nhất cho mọi file loại bỏ các khác biệt không liên quan tới nhạc cụ. Lý thuyết: [12_DIGITAL_AUDIO](../01_THEORY/12_DIGITAL_AUDIO.md) §7; thiết kế: [PREPROCESSING](../04_PART_1/02_AUDIO_ANALYSIS/PREPROCESSING.md).

---

## 3. TẠO AUDIO CHO CSDL VÀ TRUY VẤN: ghép sequence (Bước 5)

**Mục tiêu.** Có **500 file đoạn nhạc** cho CSDL và **100 file** để truy vấn thử, mỗi file chỉ một nhạc cụ, **biết chính xác** mỗi nốt bắt đầu và kết thúc lúc nào.

**Vì sao phải ghép.** Không bộ dữ liệu nào có sẵn 500 đoạn nhạc nhiều nốt của 5 nhạc cụ kèm vị trí từng nốt. Ghép từ nốt thu âm thật cho ra **đáp án** (để chấm bước chia đoạn) và **cân bằng** 100 file cho mỗi nhạc cụ ([DATASET_ROLES](../04_PART_1/01_DATASET/DATASET_ROLES.md) §4).

**INPUT.** Nốt **DB_POOL** đã chọn (để ghép CSDL) và nốt **QUERY_POOL** đã chọn (để ghép truy vấn), qua tiền xử lý §2.

**Làm gì, theo thứ tự (cho mỗi file cần ghép):**
```
Chọn 1 nhạc cụ, 1 nhóm cách chơi                          bộ kéo vĩ: 100% arco; guitar: khoảng 70% gảy thường, 30% harmonic
 → chọn ngẫu nhiên n nốt, n từ 4 tới 8                    nốt sau cách nốt trước tối đa 7 nửa cung; ưu tiên nốt ít được dùng
 → mỗi nốt: cắt lặng đầu, lấy đoạn đầu dài L giây,        giữ phần mở đầu nốt (giàu thông tin âm sắc); âm gảy tới 1.5 s
   L ngẫu nhiên trong 0.35–1.2 s
 → làm nhỏ dần 20 ms cuối (fade-out)                       tránh tiếng "tách" khi nối
 → nhân độ to ngẫu nhiên trong −6…0 dB                     giả lập nốt to nhỏ khác nhau
 → nối các nốt: 50% chèn khoảng lặng 0–150 ms;             giả lập lối chơi ngắt và lối chơi liền (legato)
   50% chồng đuôi lên nhau 10–40 ms
 → peak-normalize cả đoạn; ghi WAV 22 050 Hz mono 16-bit   tổng dài khoảng 3–8 s
 → ghi file đáp án (JSON): nhạc cụ, và từng nốt đã dùng:   đây là ground truth
   mã bản ghi gốc, tên nốt, thời điểm bắt đầu, kết thúc
```
**Tham số đã chốt:** 100 file CSDL + 20 file truy vấn cho **mỗi** nhạc cụ → **500 DB + 100 query**; seed cố định (chạy lại ra y hệt).

**OUTPUT.** `data/sequences/db/seq_<nhạc cụ>_<số>.wav` (500), `data/sequences/query/q_<nhạc cụ>_<số>.wav` (100), mỗi file kèm một JSON đáp án.

**Dùng ở bước sau.** 500 file DB → chia đoạn, tính vector, lưu CSDL (§4–§8). 100 file truy vấn → tìm kiếm và đánh giá (§12–§13). Thời điểm bắt đầu nốt trong JSON → chấm bước chia đoạn (§4, §13).

**Vì sao cần.** CSDL phải chứa **đoạn nhạc** (đối tượng thật người ta tìm), không chỉ nốt rời; và phải có đáp án để chứng minh hệ thống đúng. Chi tiết: [SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md).

---

## 4. SEGMENTATION: chia đoạn nhạc thành các đoạn ≈ từng nốt (Bước 6)

**Mục tiêu.** Biết trong một file có những nốt nào, mỗi nốt nằm từ giây nào tới giây nào, **mà không dùng đáp án** (vì file của người dùng không có đáp án).

**INPUT.** `y` của một file nhiều nốt (sequence, phrase, hoặc truy vấn).

**Làm gì, theo thứ tự:**
```
y
 → tìm VÙNG CÓ ÂM: chỗ nào năng lượng > −40 dB so với đỉnh;          bỏ khoảng lặng
   nối vùng cách nhau < 50 ms, bỏ vùng < 120 ms
 → tính đường "độ mạnh khởi đầu nốt" bằng SUPERFLUX:                 ý nghĩa: nốt mới làm xuất hiện các tần số mới.
   so phổ của từng thời điểm với phổ 2 bước trước,                   SuperFlux "nới" phổ cũ sang tần số bên cạnh nên
   chỉ cộng phần tần số MỚI mạnh lên                                  không nhầm VIBRATO (rung ngón tay) là nốt mới
 → CHỌN ĐỈNH của đường đó làm điểm bắt đầu nốt (onset), nếu:          ý nghĩa: chỉ giữ đỉnh thật, bỏ dao động nhỏ
   lớn nhất trong ±70 ms · vượt trung bình xung quanh một ngưỡng δ ≈ 0.1 · cách onset trước ≥ 100 ms
 → LÙI mỗi onset về chỗ năng lượng thấp nhất ngay trước nó            ý nghĩa: cắt đúng lúc nốt bắt đầu, giữ trọn phần
                                                                     mở đầu nốt
 → ranh giới = đầu mỗi vùng có âm + các onset → các đoạn
 → hậu xử lý: đoạn < 120 ms gộp vào đoạn trước; đoạn > 2 s chặt       ý nghĩa: đoạn quá ngắn không đủ để tính đặc
   thành các khúc ≤ 1 s; đoạn quá nhỏ (< −35 dB) bỏ đi                 trưng; đoạn quá dài có thể chứa nhiều nốt
```
**Tham số đã chốt:** khung phân tích 2 048 mẫu (≈ 93 ms), bước nhảy 512 mẫu (≈ 23 ms), 128 dải Mel, SuperFlux lag 2 và cửa sổ max 3 dải; δ chọn lại ở Bước 6 (mục chờ P03).

**OUTPUT.** Danh sách **n** đoạn: [(bắt đầu, kết thúc), …]. **n** là số đoạn tìm được, **khác nhau giữa các file** (file 4 nốt thường cho khoảng 4 đoạn, file 8 nốt khoảng 8 đoạn).

**Dùng ở bước sau.** Mỗi đoạn → tính 32 đặc trưng (§5). Độ dài mỗi đoạn → trọng số khi gộp (§8).

**Vì sao cần.** "Kiểu âm mẫu" được học từ **nốt đơn** (§6). Muốn so một đoạn nhạc với chúng, phải chia đoạn nhạc thành các đơn vị **cùng loại**: xấp xỉ một nốt. Chia sai một chút vẫn chấp nhận được, vì bước gộp (§8) được thiết kế để chịu lỗi. Lý thuyết: [17_ONSET_SEGMENTATION](../01_THEORY/17_ONSET_SEGMENTATION.md); thiết kế: [SEGMENTATION](../04_PART_1/04_FEATURE_EXTRACTION/SEGMENTATION.md).

---

## 5. FEATURE EXTRACTION: mỗi đoạn → 32 con số mô tả âm sắc (Bước 3)

**Mục tiêu.** Tóm tắt một đoạn âm thanh (hàng chục nghìn mẫu) thành **32 con số** sao cho: cùng nhạc cụ thì các con số gần nhau, khác nhạc cụ thì xa nhau, và các con số **không phụ thuộc** vào việc file to hay nhỏ, dài hay ngắn.

**INPUT.** `y` và một đoạn (bắt đầu, kết thúc). Với nốt REF thì cả nốt là một đoạn.

**Làm gì, theo thứ tự:**
```
Đoạn âm thanh
 → CHIA THÀNH FRAME: các khung ngắn 2 048 mẫu (≈ 93 ms), khung sau     ý nghĩa: âm thanh thay đổi theo thời gian;
   bắt đầu sau 512 mẫu (≈ 23 ms), mỗi khung nhân cửa sổ Hann           trong 93 ms có thể coi là "đứng yên"
 → chỉ giữ các frame CÓ ÂM (năng lượng > −40 dB so với đỉnh)           bỏ lặng
 → STFT: chuyển từng frame từ miền THỜI GIAN sang miền TẦN SỐ           ý nghĩa: thấy được tần số nào mạnh bao nhiêu,
   → được PHỔ của từng frame (1 025 tần số, cách nhau 10.8 Hz)          tức là "công thức" harmonic và vùng cộng
                                                                       hưởng thân đàn ([14])
 → từ PHỔ, tính các đặc trưng phổ:
     • MFCC c1–c13: 13 số mô tả HÌNH DẠNG đường bao của phổ             = "dấu vân tay" âm sắc: thân đàn khuếch đại
       (gom phổ theo 128 dải Mel giống tai người → lấy log → DCT;        vùng tần số nào. Bỏ c0 vì c0 chỉ đo độ to
       giữ 14 hệ số, bỏ c0)
     • spectral centroid: "trọng tâm" của phổ                           = âm SÁNG hay TỐI
     • spectral bandwidth: phổ trải RỘNG hay HẸP quanh trọng tâm        = âm giàu harmonic hay nghèo
     • spectral rolloff 85%: tần số mà 85% năng lượng nằm bên dưới      = "giới hạn trên" của âm
 → từ DẠNG SÓNG, tính:
     • ZCR: tỉ lệ số lần tín hiệu đổi dấu (cắt trục 0)                  = lượng tần số cao và tiếng xì (tiếng vĩ)
     • RMS: năng lượng của từng frame → RMS-CV = độ lệch chuẩn ÷        = âm GIỮ ĐỀU (kéo vĩ) hay TẮT DẦN (gảy).
       trung bình                                                        Dùng tỉ số để không phụ thuộc độ to
     • F0: tần số cơ bản, ước lượng bằng pYIN (tìm chu kỳ lặp lại)      = CAO ĐỘ: nhạc cụ đang chơi ở vùng âm nào
 → GỘP theo thời gian (vì mỗi frame cho một giá trị):
     MFCC: trung bình (13) + độ lệch chuẩn (13) theo thời gian           trung bình = âm sắc điển hình; độ lệch chuẩn
     centroid, bandwidth, rolloff: trung bình của log10                  = âm sắc thay đổi nhiều không (vibrato, tắt dần)
     ZCR: trung bình · RMS-CV: một số cho cả đoạn
     F0: trung vị của log2(F0) trên các frame có cao độ                  trung vị: bền khi pYIN thỉnh thoảng sai quãng tám
 → GHÉP thành vector 32 chiều s
```
> **Ký hiệu `s`**: vector đặc trưng của **một đoạn**, gồm 32 con số theo thứ tự cố định: 13 MFCC trung bình · 13 MFCC độ lệch chuẩn · log centroid · log bandwidth · log rolloff · ZCR · RMS-CV · log2 F0. Viết `s ∈ ℝ³²` nghĩa là "s là một dãy 32 số thực".

**Vì sao ghép thành 32 chiều.** Không đặc trưng nào **một mình** tách được 5 nhạc cụ: tốt nhất chỉ giải thích khoảng một nửa khác biệt giữa các nhạc cụ, còn cặp violin – viola thì không đặc trưng nào tách quá 19% ([15_AUDIO_FEATURES](../01_THEORY/15_AUDIO_FEATURES.md) §13). Mỗi nhóm đặc trưng nhìn một khía cạnh khác: MFCC nhìn **thân đàn**, centroid/rolloff nhìn **độ sáng**, RMS-CV nhìn **gảy hay kéo**, F0 nhìn **âm vực**. Gộp lại thì đủ để phân biệt. **Không** dùng chroma (đo giai điệu, không đo nhạc cụ, D08).

**Tham số đã chốt:** 22 050 Hz · frame 2 048, bước nhảy 512, cửa sổ Hann · 128 dải Mel · 14 MFCC, bỏ c0 · rolloff 85% · pYIN fmin 40 Hz, fmax 4 200 Hz · nếu dưới 20% frame có cao độ: F0 lấy giá trị trung bình của REF và bật cờ `f0_missing`. *(Đang có các mục chờ xem lại P08–P11 từ số đo sơ bộ; chưa đổi tham số nào.)*

**OUTPUT.** `s` (32 số) cho mỗi đoạn; một file có n đoạn thì có n vector `s_1 … s_n`.

**Dùng ở bước sau.** Nốt REF → học kiểu âm mẫu (§6). Đoạn của sequence/truy vấn → so với kiểu âm mẫu (§7) và gộp thành vector file (§8).

**Vì sao cần.** Không thể so hai âm thanh bằng cách so từng mẫu: chỉ lệch nhau vài mili-giây là các mẫu khác hẳn dù âm giống hệt ([13_WAVEFORM](../01_THEORY/13_WAVEFORM.md) §3). Đặc trưng là cách mô tả âm thanh bằng những con số **có nghĩa** và **so sánh được**. Thiết kế: [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md).

---

## 6. REFERENCE PROTOTYPES: học 20 "kiểu âm mẫu" (Bước 4)

**Mục tiêu.** Từ nốt đơn có nhãn chắc chắn, học xem **mỗi nhạc cụ có những "kiểu âm" điển hình nào**, để sau này mô tả một đoạn nhạc bằng câu "nó giống kiểu âm nào bao nhiêu".

**Vì sao cần prototype.** Một nhạc cụ **không phải một điểm** trong không gian 32 chiều, mà là một **đám mây** trải rộng: violin dây G (trầm, dày) trông rất khác violin dây E vùng cao (mảnh, sáng); bản thu to khác bản thu nhỏ; phòng thu này khác phòng thu kia. Mô tả đám mây đó bằng **vài điểm đại diện** thì chính xác hơn một điểm trung bình. Mỗi điểm đại diện gọi là một **prototype** ("kiểu âm mẫu").

**INPUT.** 150 nốt REF đã chọn của mỗi nhạc cụ (tổng **750**), mỗi nốt đã thành một vector `s` (§5).

**Làm gì, theo thứ tự:**
```
750 vector s của nốt REF
 → CHUẨN HÓA từng chiều: z = (s − μ_seg) ÷ σ_seg                      ý nghĩa: các chiều có đơn vị rất khác nhau
                                                                     (centroid hàng nghìn Hz, ZCR nhỏ hơn 1); đưa về
                                                                     cùng thang để chiều nào cũng có tiếng nói
 → với TỪNG nhạc cụ riêng: K-means chia các nốt của nhạc cụ đó        ý nghĩa: tự tìm 4 nhóm âm giống nhau trong một
   thành 4 nhóm; tâm của mỗi nhóm là một prototype                    nhạc cụ, ví dụ vùng trầm, vùng giữa, vùng cao,
                                                                     hoặc theo nguồn thu
 → gộp: violin P1–P4 · viola P5–P8 · cello P9–P12 ·
   double bass P13–P16 · guitar P17–P20  →  20 prototype có nhãn
 → tính τ = trung vị của (bình phương khoảng cách từ mỗi nốt REF      ý nghĩa: một "khoảng cách điển hình", dùng ở §7
   tới prototype gần nhất của nó)                                     để chia trọng số
```
> **Ký hiệu:**
> - `μ_seg`, `σ_seg`: trung bình và độ lệch chuẩn của **từng chiều** trong 32 chiều, tính **một lần** trên 750 nốt REF (bộ chuẩn hóa này gọi là `scaler_seg`). Sau đó dùng nguyên vẹn cho mọi file khác.
> - `z`: vector `s` sau chuẩn hóa (vẫn 32 số). `z = 0` ở một chiều nghĩa là bằng trung bình; `z = +1` là cao hơn trung bình một độ lệch chuẩn.
> - `P_j`: prototype thứ j (j = 1…20), cũng là một vector 32 số trong cùng không gian với `z`.
> - `τ` (tau): một con số, "độ mềm" của phép gán ở §7.

**K-means gom nhóm thế nào** (lý thuyết: [18_FEATURE_VECTOR](../01_THEORY/18_FEATURE_VECTOR.md) §2): đặt 4 tâm ban đầu → mỗi nốt về tâm gần nhất → dời mỗi tâm tới giữa các nốt của nó → lặp tới khi không nốt nào đổi nhóm. "Mỗi nhạc cụ có 4 prototype" nghĩa là K-means chạy **riêng** trên nốt của từng nhạc cụ với **k = 4**, nên prototype nào cũng biết mình thuộc nhạc cụ nào.

**Vì sao không làm prototype theo từng nốt** ("violin-A4", "violin-B4"…): khi đó vector sẽ mã hóa **giai điệu** thay vì nhạc cụ; hai đoạn violin chơi hai giai điệu khác nhau sẽ trông khác nhau như violin so với cello ([REFERENCE_PROTOTYPES](../04_PART_1/03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md) §1).

**Tham số đã chốt:** K-means **k = 4 mỗi nhạc cụ**, 20 lần khởi tạo, seed 42 → **20 prototype**. Kiểm tra: mỗi nhóm ≥ 10 nốt; gán mỗi nốt REF vào prototype gần nhất rồi lấy nhạc cụ của prototype đó, đúng > 70%. *(k = 3…6 được thử lại ở Bước 4, mục chờ P02.)*

**OUTPUT.** `μ_seg`, `σ_seg` (32 + 32 số) · 20 prototype `P_1 … P_20` (20 × 32 số, kèm nhãn nhạc cụ) · `τ`.

**Dùng ở bước sau.** Chuẩn hóa và so sánh mọi đoạn của mọi file (§7). Ngoài ra, cho mỗi đoạn tìm **nốt REF gần nhất** để minh họa ("đoạn này giống nốt `cello_D3_1_forte` nhất"), không đưa vào vector.

---

## 7. REFERENCE MATCHING: mỗi đoạn giống từng kiểu âm mẫu bao nhiêu (Bước 7, phần 1)

**Mục tiêu.** Diễn tả mỗi đoạn của một file bằng **20 trọng số**: đoạn này giống prototype 1 bao nhiêu, prototype 2 bao nhiêu… tổng bằng 1.

**INPUT.** Các vector `s_1 … s_n` của n đoạn trong một file (§5); `μ_seg`, `σ_seg`, 20 prototype, `τ` (§6).

**Làm gì, theo thứ tự (cho mỗi đoạn i):**
```
s_i
 → chuẩn hóa: z_i = (s_i − μ_seg) ÷ σ_seg          dùng ĐÚNG bộ chuẩn hóa của REF, không tính lại
 → đo khoảng cách Euclid d_ij từ z_i tới từng       ý nghĩa: d nhỏ = đoạn i nghe giống kiểu âm j
   prototype P_j (j = 1…20)                         ("khoảng cách" = căn của tổng bình phương chênh lệch 32 chiều)
 → đổi 20 khoảng cách thành 20 trọng số bằng SOFTMAX:
     w_ij = exp(−d_ij² ÷ τ) ÷ (tổng của exp(−d_ij'² ÷ τ) trên cả 20 prototype)
   ý nghĩa: prototype càng gần thì trọng số càng lớn; 20 trọng số luôn dương và cộng lại bằng 1
 → xếp trọng số của n đoạn thành bảng W gồm n hàng × 20 cột
```
> **Ký hiệu:**
> - `d_ij`: khoảng cách từ đoạn i tới prototype j.
> - `w_ij`: trọng số "đoạn i giống prototype j bao nhiêu phần", từ 0 tới 1.
> - `W` (n×20): bảng gồm **n hàng** (mỗi hàng một đoạn) và **20 cột** (mỗi cột một prototype). Mỗi hàng cộng lại bằng 1.

**Ví dụ.** Một đoạn cello có khoảng cách nhỏ nhất tới prototype "cello-2" và hơi gần "double bass-1": hàng của nó trong W có thể là 0.71 ở cột cello-2, 0.20 ở cột double bass-1, và các cột còn lại gần 0.

**Vì sao dùng trọng số "mềm" thay vì chỉ chọn prototype gần nhất.** Nếu một đoạn nằm **sát biên** giữa hai prototype (khoảng cách 1.01 và 1.00), chọn cứng sẽ nhảy qua lại giữa hai prototype chỉ vì một chút nhiễu. Trọng số mềm cho khoảng 0.49 và 0.51, nên kết quả **ổn định** ([18_FEATURE_VECTOR](../01_THEORY/18_FEATURE_VECTOR.md) §4; D11).

**Vì sao biến mỗi đoạn thành 20 trọng số.** 20 trọng số nói đoạn này "nghe giống kiểu âm nào của nhạc cụ nào", một cách mô tả **dễ diễn giải** và cùng một số chiều cho mọi đoạn. Đây là cầu nối giữa **nốt đơn có nhãn** (thư viện REF) và **đoạn nhạc không nhãn**.

**OUTPUT.** `W` (n × 20) và các `z_1 … z_n`.

**Dùng ở bước sau.** Gộp thành vector cố định của file (§8).

---

## 8. FIXED-LENGTH VECTOR: cả file → đúng 52 con số (Bước 7, phần 2)

**Mục tiêu.** Biến một file có **n đoạn** (n khác nhau giữa các file) thành **một vector có đúng 52 số**, giống nhau về cấu trúc cho mọi file.

**Vì sao số đoạn mỗi file khác nhau.** File dài hơn, nhiều nốt hơn thì có nhiều đoạn hơn; bước chia đoạn cũng có thể chia thừa hay gộp sót.

**Vì sao cần vector cố định.** Để **đo khoảng cách** giữa hai file và **đặt file vào R-tree**, mỗi file phải là **một điểm** trong một không gian có **số chiều cố định**. Không thể đo khoảng cách giữa một bảng 4×32 và một bảng 7×32.

**INPUT.** `W` (n × 20), `z_1 … z_n` (§7) và độ dài từng đoạn.

**Làm gì, theo thứ tự:**
```
n đoạn của một file
 → trọng số theo độ dài: α_i = độ dài đoạn i ÷ tổng độ dài các đoạn       đoạn dài đóng góp nhiều hơn; các α cộng lại = 1
 → h = tổng theo các đoạn của (α_i × hàng i của W)        → 20 số          ý nghĩa: cả file giống từng kiểu âm bao nhiêu %
 → μ = tổng theo các đoạn của (α_i × z_i)                  → 32 số          ý nghĩa: "âm sắc trung bình" của cả file
 → v = [h ‖ μ]: viết 20 số của h rồi nối tiếp 32 số của μ   → 52 số
```
> **Ký hiệu:**
> - `α_i` (alpha): tỉ lệ thời lượng của đoạn i trong file.
> - `h`: "hồ sơ giống nhau" 20 số, cộng lại bằng 1. Ví dụ: cộng 4 số của violin được 0.50, của viola 0.33, của cello 0.17 → "file này nghe 50% giống violin, 33% giống viola, 17% giống cello".
> - `μ` (mu): trung bình có trọng số của các `z_i`, 32 số, cùng ý nghĩa từng chiều như `s`. *Khác với `μ_seg` ở §6: `μ_seg` là trung bình của REF, dùng để chuẩn hóa.*
> - `‖`: phép **nối** hai dãy số.
> - `v`: **vector của file**, đúng **52 = 20 + 32** số. Không có thành phần nào khác.

**Vì sao cần cả h lẫn μ.** `h` nói file gần **các kiểu âm đã biết** nào, dễ diễn giải. Nhưng với nhạc cụ **ngoài CSDL** (banjo), mọi prototype đều xa, mà `h` vẫn cộng lại bằng 1 nên trông "bình thường". `μ` là âm sắc **tuyệt đối**, cho thấy file thật sự nằm ở đâu.

**Vì sao chịu được lỗi chia đoạn.** Chia một nốt thành 3 mảnh thì 3 mảnh vẫn chỉ đóng góp đúng thời lượng của nốt đó (nhờ α), và các mảnh giống nhau nên trọng số gần nhau. Thứ tự nốt không ảnh hưởng, vì ta tìm theo âm sắc chứ không theo giai điệu. File chỉ có 1 nốt (n = 1) vẫn hợp lệ.

**OUTPUT.** `v` (52 số) cho mỗi file, kèm thông tin trung gian (các đoạn, `W`, `h`) để hiển thị. Đây là **sản phẩm bàn giao của Phần 1** ([PART_1_OUTPUT_SPEC](../04_PART_1/05_OUTPUT/PART_1_OUTPUT_SPEC.md)).

**Dùng ở bước sau.** Lưu vào CSDL (§9), chuẩn hóa (§10).

**Quan trọng:** §2 → §8 gói trong **một hàm duy nhất** `audio_to_vector()`, dùng cho **cả** file CSDL **lẫn** file truy vấn. Thiết kế: [FILE_LEVEL_VECTOR](../04_PART_1/03_FEATURE_DESIGN/FILE_LEVEL_VECTOR.md).

---

## 9. DATABASE: lưu vector và thông tin mô tả (Bước 8)

**Mục tiêu.** Lưu mọi thứ cần cho tìm kiếm và giải thích kết quả vào **một CSDL quan hệ**, mỗi file âm thanh là **một bản ghi**.

**INPUT.** 500 vector `v` của CSDL (§8), catalog (§1), đáp án các sequence (§3), các đoạn và trọng số (§4–§7), prototype (§6).

**Làm gì:**
```
 → bảng instrument: 7 nhạc cụ, kéo vĩ hay gảy, có trong CSDL không
 → bảng source_note: mỗi nốt đơn gốc một dòng (nguồn, nhạc cụ, dây, nốt, cường độ, cách chơi, trạng thái, tập)
 → bảng audio_file: mỗi file tìm kiếm/truy vấn một dòng (đường dẫn, loại, nhạc cụ, thời lượng, có trong chỉ mục không)
 → bảng sequence_note: sequence gồm những nốt gốc nào, bắt đầu/kết thúc lúc nào (đáp án)
 → bảng segment: các đoạn tìm được và 32 đặc trưng của từng đoạn (để giải thích)
 → bảng prototype, model: 20 prototype, phiên bản mô hình
 → bảng file_vector: v (52 số), và sau §10–§11 thêm v' (52 số) và u (8 số), lưu dạng nhị phân float32
```
**Phương pháp đã chốt:** SQLite (một file, không cần máy chủ); vector lưu dạng **BLOB float32** (52 × 4 = 208 byte); **file âm thanh nằm trên đĩa**, CSDL chỉ lưu **đường dẫn** + thông tin mô tả + vector (lưu trữ hỗn hợp). **Không** có bảng frame: frame chỉ là bước tính trung gian, không phải đối tượng người dùng tìm.

**OUTPUT.** `mmdb.sqlite`. **Dùng ở bước sau.** Chuẩn hóa, PCA, R-tree đọc vector từ đây; bước trả kết quả đọc đường dẫn và nhãn từ đây.

**Vì sao cần.** Đề bài yêu cầu một **hệ CSDL** quản trị đặc trưng của mọi file; CSDL quan hệ cho phép truy vấn bằng SQL, kiểm tra rò rỉ, và nối kết quả tìm kiếm với nhãn. Thiết kế: [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md); lý thuyết: [22](../01_THEORY/22_MULTIMEDIA_DATABASE.md) §3–5.

---

## 10. NORMALIZATION: đưa 52 con số về cùng thang đo (Bước 9, phần 1)

**Mục tiêu.** Làm cho mỗi chiều của vector file đóng góp **công bằng** vào khoảng cách.

**Vì sao phải chuẩn hóa.** Khoảng cách Euclid cộng bình phương chênh lệch của mọi chiều. Chiều nào có giá trị lớn sẽ **lấn át** các chiều còn lại. Ví dụ thật với 3 nốt A4: chênh centroid 278 Hz, chênh ZCR 0.03, chênh RMS-CV 0.32. Không chuẩn hóa thì centroid chiếm **99.9999%** khoảng cách, ZCR và RMS-CV coi như vô hình ([19_DISTANCE_SIMILARITY](../01_THEORY/19_DISTANCE_SIMILARITY.md) §3).

**INPUT.** 500 vector `v` của CSDL.

**Làm gì, theo thứ tự:**
```
v (52 số)
 → x = (v − trung bình) ÷ độ lệch chuẩn, tính TỪNG chiều        bộ chuẩn hóa này (scaler_file) được FIT một lần
                                                                trên 500 vector của CSDL
 → cân bằng hai khối:                                            ý nghĩa: sau bước trên mỗi chiều "nặng" như nhau,
     20 chiều đầu (khối h) chia cho √20                          nên khối 32 chiều sẽ chiếm 62% khoảng cách chỉ vì
     32 chiều sau (khối μ) chia cho √32                          nhiều chiều hơn. Chia cho căn số chiều làm mỗi khối
                                                                đóng góp đúng 50%
 → v' (52 số)
```
> **Ký hiệu:**
> - `x`: vector `v` sau chuẩn hóa từng chiều.
> - `v'` (đọc "v phẩy"): vector sau khi cân bằng khối. **Khoảng cách thật giữa hai file được tính trên `v'`.**

**Bộ chuẩn hóa được fit ở đâu.** Có **hai** bộ chuẩn hóa, không được nhầm:
| Bộ | Cho vector nào | Fit trên |
|---|---|---|
| `scaler_seg` | `s` (32 số, của đoạn) | 750 nốt REF (§6) |
| `scaler_file` | `v` (52 số, của file) | 500 vector của CSDL (bước này) |

Truy vấn **chỉ dùng lại** bộ đã fit, không bao giờ tính lại. Tính lại cho truy vấn sẽ cho ra một hệ tọa độ khác, không còn so được với CSDL.

**Tham số đã chốt:** z-score; cân bằng khối √20 và √32 (D13). **OUTPUT.** `v'` của 500 file; tham số của `scaler_file`. **Dùng ở bước sau.** PCA (§11) và khoảng cách cuối cùng (§13). Thiết kế: [NORMALIZATION_PCA](../05_PART_2/02_INDEX/NORMALIZATION_PCA.md).

---

## 11. PCA: rút gọn 52 → 8 con số để đánh chỉ mục (Bước 9, phần 2)

**Mục tiêu.** Có một bản **8 chiều** của mỗi vector để đặt vào R-tree, sao cho mất ít thông tin nhất và **không làm sai** kết quả tìm kiếm.

**Vector 52D là gì.** `v'` (§10): 20 số "giống kiểu âm nào" + 32 số "âm sắc trung bình", đã chuẩn hóa. Mỗi file là một điểm trong không gian 52 chiều.

**Vì sao giảm xuống 8D.** R-tree chia không gian bằng các hộp chữ nhật; ở 52 chiều các hộp chồng lên nhau gần hết và mọi điểm cách truy vấn gần như bằng nhau, nên R-tree phải mở gần hết cây, **không nhanh hơn** quét toàn bộ. R-tree chỉ hiệu quả ở khoảng dưới 10 chiều ([21_R_TREE](../01_THEORY/21_R_TREE.md) §6).

**INPUT.** 500 vector `v'`.

**Làm gì, theo thứ tự:**
```
500 vector v' (52 số)
 → tìm các HƯỚNG mà 500 điểm trải rộng nhất (thành phần chính),      ý nghĩa: hướng trải rộng = nơi các file khác nhau
   xếp từ rộng nhất tới hẹp nhất                                     nhiều nhất = nhiều thông tin nhất
 → giữ 8 hướng đầu
 → chiếu mỗi v' lên 8 hướng đó → u (8 số)
```
> **Ký hiệu `u`**: tọa độ của file trên 8 hướng chính, 8 số. (Ma trận chứa 8 hướng gọi là ma trận chiếu PCA; **không** nhầm với bảng trọng số `W` ở §7.)

**PCA giữ lại thông tin nào.** Phần **khác biệt lớn nhất** giữa các file (phương sai lớn nhất). Với dữ liệu thật của project, hướng lớn nhất là "sáng – tối / cao – trầm"; thử trên nốt đơn, 8 hướng giữ khoảng 71% phương sai ([20_PCA](../01_THEORY/20_PCA.md) §6). Phần còn lại không mất: nó vẫn nằm trong `v'`.

**8D dùng cho R-tree thế nào, và vì sao cuối cùng vẫn dùng Euclid 52D.** Phép chiếu PCA **không bao giờ làm dài** khoảng cách: khoảng cách giữa hai file trong 8D **luôn ≤** khoảng cách thật trong 52D (tính chất **cận dưới**). Nên 8D dùng để **lọc nhanh** ứng viên trong R-tree, còn **xếp hạng cuối cùng** dùng khoảng cách thật 52D trên số ít ứng viên. Nhờ cận dưới, cách làm này cho kết quả **giống hệt** quét toàn bộ (§13).

**Tham số đã chốt:** **PCA 8D**, fit trên 500 vector CSDL, **không whitening** (whitening chia mỗi hướng cho độ trải của nó, có thể làm dài khoảng cách và phá tính chất cận dưới) (D14). *(8D hay 5–6D xem lại theo số ứng viên, mục chờ P04.)*

**OUTPUT.** `u` của 500 file; tham số PCA. **Dùng ở bước sau.** R-tree (§12); truy vấn cũng được chiếu bằng đúng tham số này.

---

## 12. R-TREE: xếp 500 điểm 8 chiều vào cây để tìm nhanh (Bước 10, phần 1)

**Mục tiêu.** Sắp xếp trước 500 điểm `u` sao cho khi có truy vấn, chỉ cần xem **một phần nhỏ** các điểm mà vẫn chắc chắn tìm đúng các điểm gần nhất.

**R-tree lưu các vector 8D để làm gì.** Mỗi sequence của CSDL là **một điểm** 8 chiều (khóa là mã file `audio_id`). R-tree **không** lưu file âm thanh, frame hay đoạn: chỉ lưu điểm `u` của từng file.

**INPUT.** 500 điểm `u` (§11).

**Làm gì:**
```
500 điểm u
 → gom các điểm GẦN NHAU vào một HỘP chữ nhật nhỏ nhất bao trọn chúng (MBR)
 → gom các hộp gần nhau vào hộp lớn hơn … tới một hộp gốc → cây nhiều tầng
 → mỗi hộp chứa tối đa M = 10 mục (điểm hoặc hộp con)
```
**M = 10 nghĩa là gì.** Mỗi nút của cây chứa tối đa **10 mục**. Với 500 điểm: khoảng 50 hộp lá, cây cao 3 tầng. (Mặc định của thư viện là 100, khi đó 500 điểm chỉ thành 5 lá và không thấy được cơ chế cắt tỉa.)

**R-tree giúp tìm nhanh thế nào.** Với mỗi hộp, tính khoảng cách **nhỏ nhất có thể** từ truy vấn tới hộp (MINDIST). Nếu ngay cả khoảng cách đó đã lớn hơn kết quả đang có, **bỏ qua cả hộp** mà không cần xem điểm nào bên trong ([21_R_TREE](../01_THEORY/21_R_TREE.md) §5).

**Vì sao không dùng R-tree trực tiếp trên 52D.** Lời nguyền số chiều (§11): ở 52 chiều không hộp nào bị bỏ qua được.

**Tham số đã chốt:** biến thể **R\*-tree** (ít chồng lấn hộp hơn), 8 chiều, **M = 10** (D16). **Nói thẳng:** với 500 điểm, quét toàn bộ mất dưới 1 ms và thường nhanh hơn; R-tree ở đây để **minh họa** chỉ mục nhiều chiều và cơ chế lọc – tinh chỉnh, sẽ báo cáo số ứng viên phải xem.

**OUTPUT.** File chỉ mục `data/index/rtree_v1`. **Dùng ở bước sau.** Lọc ứng viên khi tìm kiếm (§13). Thiết kế: [RTREE_INDEX](../05_PART_2/02_INDEX/RTREE_INDEX.md).

---

## 13. SIMILARITY SEARCH + TOP-5: trả lời truy vấn (Bước 10–11)

**Mục tiêu.** Với một file truy vấn, trả về **5 file CSDL gần nhất**, đúng y hệt như khi so với cả 500 file.

**INPUT.** Một file âm thanh truy vấn bất kỳ.

**Làm gì, theo thứ tự:**
```
File truy vấn
 → audio_to_vector(): ĐÚNG các bước §2 → §8 như file CSDL      → v_q (52 số)      [_q = "của truy vấn"]
 → scaler_file + cân bằng khối (đã fit, không tính lại)        → v'_q (52 số)
 → chiếu bằng PCA đã fit                                       → u_q (8 số)
 → LỌC (tìm ứng viên): hỏi R-tree k' = 20 điểm gần u_q nhất theo khoảng cách 8D
 → TINH CHỈNH (xếp hạng chính xác): tính khoảng cách THẬT 52D
     d = khoảng cách Euclid giữa v'_q và v' của từng ứng viên; giữ 5 ứng viên có d nhỏ nhất
 → KIỂM TRA DỪNG: gọi r8 là khoảng cách 8D tới ứng viên xa nhất vừa lấy.
     nếu d của kết quả thứ 5 ≤ r8 → DỪNG: chắc chắn đúng
     nếu không → gấp đôi k' (40, 80, …) và làm lại
 → Top-5: hạng, file, nhạc cụ, d, điểm hiển thị similarity = 1 ÷ (1 + d)
```
**Vì sao dừng như vậy là chắc chắn đúng.** Mọi file **chưa** được xét đều có khoảng cách 8D ≥ r8. Theo tính chất cận dưới (§11), khoảng cách thật 52D của chúng còn ≥ r8 ≥ khoảng cách của kết quả thứ 5. Vậy không file nào bị bỏ sót.

**Vì sao cần hai bước lọc và tinh chỉnh.** Chỉ dùng 8D thì nhanh nhưng **có thể sai thứ tự** (8D chỉ giữ một phần thông tin). Chỉ dùng 52D thì đúng nhưng phải tính với **mọi** file. Lọc bằng 8D rồi tinh chỉnh bằng 52D cho cả hai ưu điểm: chỉ tính chính xác trên vài chục ứng viên, mà kết quả **giống hệt** quét toàn bộ. Đây là khung GEMINI của CSDL đa phương tiện.

**Vì sao dùng Euclid, không dùng cosine.** R-tree cắt tỉa bằng khoảng cách Euclid; tính chất cận dưới qua PCA đúng với Euclid; và trong không gian đã chuẩn hóa, "độ lớn" của vector có nghĩa (D15; [19](../01_THEORY/19_DISTANCE_SIMILARITY.md) §5).

**Tham số đã chốt:** **Top-5**; k' bắt đầu 20, gấp đôi tới khi đủ điều kiện dừng; khoảng cách Euclid trên `v'` 52D; `similarity = 1/(1+d)` chỉ để hiển thị (D15, D17).

**OUTPUT.** 5 mã file + khoảng cách + nhạc cụ + đường dẫn, cùng **kết quả trung gian**: dạng sóng và ranh giới các đoạn, bảng đặc trưng từng đoạn, prototype và nốt REF gần nhất, hồ sơ `h` theo nhạc cụ, số ứng viên và số vòng ([INTERMEDIATE_RESULTS](../05_PART_2/04_QUERY/INTERMEDIATE_RESULTS.md)).

**Kiểm tra bắt buộc.** Với 100 truy vấn, Top-5 của R-tree phải **trùng 100%** với quét toàn bộ (cùng file, cùng thứ tự). Thiết kế: [KNN_SEARCH](../05_PART_2/03_SEARCH/KNN_SEARCH.md), [QUERY_PIPELINE](../05_PART_2/04_QUERY/QUERY_PIPELINE.md).

---

## 14. EVALUATION: hệ thống đúng tới đâu (sau Phần 1, 2)

**Mục tiêu.** Đo bằng số hệ thống tìm đúng tới đâu, chỗ nào hay nhầm, và giới hạn ở đâu.

**INPUT.** Các bộ truy vấn: **100 sequence truy vấn** (con số chính thức, chạy **một lần**), **445 phrase** thật, **154 file nhạc cụ ngoài CSDL** (banjo, mandolin).

**Làm gì và đo gì:**
| Độ đo | Ý nghĩa |
|---|---|
| **P@5** (chỉ số chính) | Trong 5 kết quả, bao nhiêu % **cùng nhạc cụ** với truy vấn |
| **Top-1** | Kết quả đầu tiên có đúng nhạc cụ không |
| **MRR** | Trung bình của 1 ÷ (hạng của kết quả đúng đầu tiên): đúng ở hạng 1 được 1, hạng 2 được 0.5… |
| **Onset F** | Bước chia đoạn tìm đúng điểm bắt đầu nốt tới đâu (so với đáp án, sai lệch cho phép ±50 ms; mục tiêu ≥ 0.80) |
| Ma trận nhầm lẫn | Nhạc cụ nào hay bị nhầm thành nhạc cụ nào |
| R-tree == quét toàn bộ | Phải 100% |

**Quy tắc.** Mọi tham số được chọn trên **tập dev** (lấy từng file CSDL làm truy vấn, sau khi bỏ các file dùng chung nốt gốc với nó); tập truy vấn chính thức chỉ chạy **một lần** để lấy số cuối, tránh "học thuộc" tập thử. Kết quả báo cáo **theo từng nhạc cụ**. *(Các phép đánh giá bổ sung đang chờ quyết định: khác nguồn thu P12, âm gảy không phải guitar P13.)*

**OUTPUT.** Bảng số liệu và nhận xét cho báo cáo. Thiết kế: [07_EVALUATION](../07_EVALUATION/README.md).

---

## 15. Bảng tóm tắt các bước

| # | Bước | INPUT | OUTPUT | Dùng ở |
|---|---|---|---|---|
| 1 | Filtering (Bước 1 ✅) | 4 477 MP3 + 188 AIFF | catalog 5 906 dòng; 4 653 nốt dùng được, chia REF / DB_POOL / QUERY_POOL | 3, 6 |
| 2 | Preprocessing (Bước 2) | file audio | `y` (22 050 Hz, mono, đỉnh 0.95) | mọi bước |
| 3 | Ghép sequence (Bước 5) | nốt DB_POOL, QUERY_POOL | 500 DB + 100 query WAV + đáp án | 4, 13, 14 |
| 4 | Segmentation (Bước 6) | `y` | n đoạn | 5, 8 |
| 5 | Feature extraction (Bước 3) | đoạn | `s` (32 số) mỗi đoạn | 6, 7 |
| 6 | Reference prototypes (Bước 4) | 750 nốt REF | `μ_seg`, `σ_seg`, 20 prototype, `τ` | 7 |
| 7 | Reference matching (Bước 7) | `s_1…s_n` | `W` (n × 20), `z_1…z_n` | 8 |
| 8 | Fixed-length vector (Bước 7) | `W`, `z`, độ dài | `v` = [h ‖ μ] (52 số) | 9, 10 |
| 9 | Database (Bước 8) | `v` + nhãn | `mmdb.sqlite` | 10–13 |
| 10 | Normalization (Bước 9) | 500 `v` | `v'` (52 số), `scaler_file` | 11, 13 |
| 11 | PCA (Bước 9) | 500 `v'` | `u` (8 số), tham số PCA | 12, 13 |
| 12 | R-tree (Bước 10) | 500 `u` | chỉ mục R\*-tree, M = 10 | 13 |
| 13 | Similarity + Top-5 (Bước 10–11) | file truy vấn | 5 file + khoảng cách + kết quả trung gian | 14 |
| 14 | Evaluation | các bộ truy vấn | P@5, Top-1, MRR, onset F | báo cáo |

## 16. Bảng ký hiệu (tra nhanh)

| Ký hiệu | Đọc là | Là gì | Số lượng số | Xuất hiện ở |
|---|---|---|---|---|
| `y` | tín hiệu | Dãy mẫu âm thanh sau tiền xử lý | dài tùy file | §2 |
| `s` | vector đoạn | 32 đặc trưng của một đoạn | 32 | §5 |
| `μ_seg`, `σ_seg` | | Trung bình, độ lệch chuẩn của 32 đặc trưng trên nốt REF | 32 + 32 | §6 |
| `z` | | `s` sau chuẩn hóa bằng `μ_seg`, `σ_seg` | 32 | §6, §7 |
| `P_j` | prototype j | Một trong 20 kiểu âm mẫu | 32 mỗi cái | §6 |
| `τ` | tau | Độ mềm của phép gán trọng số | 1 | §6, §7 |
| `d_ij` | | Khoảng cách từ đoạn i tới prototype j | 1 | §7 |
| `w_ij` | | Đoạn i giống prototype j bao nhiêu phần | 1 | §7 |
| `W` | | Bảng trọng số: n hàng (đoạn) × 20 cột (prototype) | n × 20 | §7 |
| `α_i` | alpha | Tỉ lệ thời lượng của đoạn i | 1 | §8 |
| `h` | | Cả file giống từng prototype bao nhiêu (tổng = 1) | 20 | §8 |
| `μ` | mu | Âm sắc trung bình của file (trung bình có trọng số của `z`) | 32 | §8 |
| `v` | vector file | `[h ‖ μ]` | 52 | §8 |
| `v'` | v phẩy | `v` sau chuẩn hóa + cân bằng khối; dùng để tính khoảng cách thật | 52 | §10 |
| `u` | | `v'` chiếu xuống 8 hướng chính; dùng trong R-tree | 8 | §11 |
| `_q` | | "của truy vấn", ví dụ `v'_q`, `u_q` | | §13 |
| `k'` | | Số ứng viên lấy từ R-tree trong một vòng | 1 | §13 |
| `r8` | | Khoảng cách 8D tới ứng viên xa nhất trong vòng | 1 | §13 |
| `d` | | Khoảng cách Euclid 52D giữa truy vấn và một file | 1 | §13 |

---

## 17. Công nghệ và cấu trúc code dự kiến

Python · numpy/scipy · **librosa** (STFT, Mel, MFCC, pYIN, onset) · **scikit-learn** (chuẩn hóa, K-means, PCA) · **rtree** (R\*-tree) · **sqlite3** (có sẵn) · ffmpeg. Demo sau này dùng Streamlit. Hàm cụ thể, tham số và file gọi: [IMPLEMENTATION](../03_WORKFLOWS/IMPLEMENTATION.md).

```
BTL/
├── requirements.txt
├── src/strings_mmdb/
│   ├── config.py               # Bước 0: mọi tham số ở một chỗ
│   ├── catalog.py              # Bước 1
│   ├── audio_io.py             # Bước 2
│   ├── features.py             # Bước 3
│   ├── prototypes.py           # Bước 4
│   ├── synth.py                # Bước 5
│   ├── segmentation.py         # Bước 6
│   ├── representation.py       # Bước 7  ← audio_to_vector(): HÀM DUY NHẤT cho CSDL và truy vấn
│   ├── db.py                   # Bước 8
│   ├── reduction.py            # Bước 9
│   ├── index_rtree.py          # Bước 10
│   └── search.py               # Bước 10–11
├── scripts/p01_… → p11_…       # mỗi bước một script (Bước 1 hiện nằm ở scripts/p01_1 … p01_6)
├── tests/                      # mỗi module một file test
└── data/                       # mọi thứ sinh ra (xóa đi tạo lại được)
```

## 18. Kế hoạch chi tiết
- [PART_1_PLAN.md](PART_1_PLAN.md): Bước 0 → 7 (checklist, tiêu chí xong).
- [PART_2_PLAN.md](PART_2_PLAN.md): Bước 8 → 11.
- [MILESTONES.md](MILESTONES.md): mốc và checklist.
