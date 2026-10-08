# DATASET COLLECTION & FILTERING — Thu thập và lọc dữ liệu

> **Đây là việc trọng tâm hiện tại.** File này trả lời ba câu hỏi: (1) dữ liệu đang có lọc ra còn bao nhiêu; (2) còn thiếu gì so với thiết kế; (3) lấy thêm ở đâu và làm theo các bước nào.
> Số liệu §1 được đo ngày 07/10/2026 bằng cách **giải mã toàn bộ 4 477 file** (ffmpeg → mono 22 050 Hz), đo phần có âm (RMS > −40 dB so với đỉnh), đỉnh biên độ, số mẫu clipping và MD5.

## 1. Kết quả lọc dữ liệu hiện có (`raw/philharmonia/`)

### 1.1. Chất lượng kỹ thuật
| Kiểm tra | Kết quả |
|---|---|
| Giải mã lỗi | **1** file: `viola/viola_D6_05_piano_arco-normal.mp3` |
| Trùng MD5 | **2 cặp** (4 file): `cello_Cs6_1_mezzo-forte_arco-harmonic` = `violin_Ds5_phrase_forte_arco-spiccato`; `cello_Ds5_05_forte_arco-normal` = `viola_G6_05_fortissimo_arco-normal` |
| Clipping | Chỉ **1** file (một phrase double-bass); nốt đơn không có file nào |
| Rất nhỏ (đỉnh < 0.01) | 3 file (violin/viola pianissimo cao, trong đó 1 là file hỏng) |
| Phần có âm < 0.35 s | **55** nốt đơn (violin 10, viola 29, cello 11, double-bass 5), phần lớn có nhãn `025` |

⇒ **Chất lượng tốt.** Vấn đề chính không nằm ở chất lượng mà ở **phân bố** (§1.3).

### 1.2. Thời lượng phần có âm (nốt đơn)
| Nhạc cụ | Median | 10% ngắn nhất dưới |
|---|---|---|
| violin | 0.88 s | 0.51 s |
| viola | 1.00 s | 0.46 s |
| cello | 0.88 s | 0.51 s |
| double-bass | 1.07 s | 0.49 s |
| guitar | 3.59 s | 2.81 s |
| banjo | 1.99 s | 1.90 s |
| mandolin | 1.92 s | 1.65 s |

Nốt bộ kéo vĩ ngắn (khoảng 1 s). Guitar, banjo và mandolin dài hơn vì âm gảy có đuôi tắt dần.

### 1.3. Số nốt **dùng được** sau lọc
Điều kiện: không lỗi, không trùng, không phải phrase, phần có âm ≥ 0.35 s, kỹ thuật cơ bản.

| Nhạc cụ | arco / normal | vibrato¹ | pizz | harmonics | **Tổng** | Số cao độ |
|---|---|---|---|---|---|---|
| violin | 842 | 69 | 48 | — | **959** | 49 |
| viola | 679 | 42 | 38 | — | **759** | 51 |
| cello | 731 | 25 | **0** | — | **756** | 49 |
| double-bass | 751 | — | **12** | — | **763** | 44 |
| guitar | 71 | — | — | 35 | **106** | 42 |

¹ molto-vibrato + non-vibrato.

### 1.4. Những gì phải sửa trong thiết kế do số liệu thật
1. **Pizz quá hiếm:** cello 0, double-bass 12. Quy tắc cũ "20% sequence pizz" không làm được ⇒ **bộ kéo vĩ chỉ dùng arco** (gồm cả vibrato/non-vibrato) trong v1. Nốt pizz giữ trong catalog và có thể dùng làm query phụ. (Đã ghi D20.)
2. **Guitar thiếu nghiêm trọng:** 106 nốt so với khoảng 760–960 của bộ kéo vĩ. Chia 40/40/20 thì DB_POOL guitar chỉ có khoảng 42 nốt, mỗi nốt bị dùng lại khoảng 14 lần ⇒ **phải bổ sung dữ liệu guitar** (§3).

## 2. Yêu cầu dữ liệu tối thiểu (suy ra từ thiết kế)

| Mục đích | Cần cho mỗi nhạc cụ | Lý do |
|---|---|---|
| REF (học prototype) | ≥ 100 nốt, phủ đủ âm vực | K-means 4 cụm × ≥ 10 thành viên, có dư |
| DB_POOL | ≥ 200 nốt | 100 sequence × ~6 nốt = 600 lượt ⇒ dùng lại ≤ 3 lần |
| QUERY_POOL | ≥ 60 nốt | 20 sequence × ~6 nốt = 120 lượt ⇒ dùng lại ≤ 2 lần |
| **Tổng** | **≥ 360 nốt dùng được** | |

| Nhạc cụ | Có | Cần | Thiếu |
|---|---|---|---|
| violin, viola, cello, double-bass | 756–959 | 360 | Không thiếu |
| **guitar** | **106** | 360 | **≈ 250** |
| banjo, mandolin (truy vấn "nhạc cụ ngoài CSDL") | 74, 80 | Chỉ cần vài chục | Không thiếu |

## 3. Nguồn bổ sung (đã kiểm tra ngày 07/10/2026)

| Nguồn | Nội dung | Định dạng | Giấy phép | Đánh giá |
|---|---|---|---|---|
| **University of Iowa MIS** (theremin.music.uiowa.edu/MIS.html) | Violin, viola, cello, double bass, **guitar**; thu trong phòng tiêu âm. Mỗi file chứa **nhiều nốt liên tiếp** trên một dây trong một khoảng cao độ, ở 3 mức pp/mf/ff. Trang guitar có 72 file (gồm bản mono và stereo) | AIFF 16-bit 44.1 kHz mono (bản pre-2012) | "Dùng cho mọi dự án, không hạn chế" | **ĐỀ XUẤT CHÍNH** |
| GuitarSet (Zenodo 3371780) | 360 đoạn guitar acoustic khoảng 30 s (comping + solo), có chú thích nốt | Mic mono khoảng 657 MB | CC BY 4.0 | Phụ: làm **query nhạc thật** cho guitar (phần solo); không cần cho Phần 1 |
| IDMT-SMT-Guitar (Zenodo 7544110) | Khoảng 4 700 nốt guitar điện + acoustic, nhiều kỹ thuật | WAV 44.1 kHz | **CC BY-NC-ND 4.0** (cấm tác phẩm phái sinh) | Không chọn: điều khoản ND không hợp với việc cắt và ghép |
| NSynth | Hàng trăm nghìn nốt, có guitar acoustic | **16 kHz**, 4 s | CC BY 4.0 | **Loại**: 16 kHz không có nội dung trên 8 kHz ⇒ hệ thống sẽ "nhận ra nguồn" thay vì nhận ra nhạc cụ |

### 3.1. Vì sao chọn Iowa MIS, và tải cho **cả 5 nhạc cụ**
- Cùng 44.1 kHz, mono, nốt rời của nhạc công thật, nên **cùng bản chất** với dữ liệu hiện có.
- Không hạn chế sử dụng.
- **Rủi ro nhiễu nguồn (source confound):** nếu chỉ guitar có thêm dữ liệu Iowa (phòng tiêu âm), hệ thống có thể học đặc điểm "phòng thu Iowa" và gán cho guitar. Cách tránh: **tải Iowa cho cả 5 nhạc cụ**, và chia mọi tập theo cả nhạc cụ lẫn nguồn ⇒ mỗi nhạc cụ đều có hai nguồn ở mọi tập.
- **Lợi ích thêm:** file Iowa gốc là **bản thu multi-note thật** (nhiều nốt liên tiếp), nên dùng được làm tập query "khác điều kiện thu" để kiểm tra tổng quát hóa.

### 3.2. Những điều CHƯA biết, phải kiểm tra sau khi tải
- Số nốt thực tế trong mỗi file Iowa guitar, và chúng có phải là các nốt chromatic tăng dần đúng như khoảng ghi trong tên file (ví dụ `E2B2`) hay không.
- Khoảng lặng giữa các nốt đủ để cắt tự động chưa.
- Số nốt guitar thu được thực tế.

### 3.3. Iowa guitar: ước tính từ danh sách file (xem trang ngày 07/10/2026)
Đàn Raimundo 118, thu ngày 11/12/2011 trong phòng tiêu âm, micro Earthworks QTC40. Có bản mono 16-bit/44.1 kHz (tải gọn: `Guitar.mono.1644.1.zip`). Có 45 file mono = 6 dây × 3 mức (pp/mf/ff) × 2–3 khoảng cao độ:

| Dây | Các khoảng (tên file) | Số nốt / mức |
|---|---|---|
| E trầm (`sulE`) | E2B2, C3B3 | 8 + 12 = 20 |
| A (`sulA`) | A2B2, C3B3, C4E4 | 3 + 12 + 5 = 20 |
| D (`sulD`) | D3B3, C4Ab4 | 10 + 9 = 19 |
| G (`sulG`) | G3B3, C4B4, C5Db5 | 5 + 12 + 2 = 19 |
| B (`sulB`) | B3, C4B4, C5Gb5 | 1 + 12 + 7 = 20 |
| E cao (`sul_E`) | E4B4, C5B5 (ff: C5Bb5) | 8 + 12 = 20 (ff: 19) |

⇒ **Khoảng 353 nốt** (118 + 118 + 117), âm vực E2–B5, **mỗi nốt có ghi rõ dây**. *(Ngày 07/10 đã tải đủ 45 file; khảo sát cho thấy các nốt đúng là đi lên từng nửa cung như tên file, xem Bước 1.2.)* Cộng 106 nốt của `raw/philharmonia/` ⇒ khoảng **459 nốt guitar**, vượt mức cần 360. Con số này suy ra từ tên file; phải xác nhận ở Bước 1.2 (số đoạn cắt được trong mỗi file).

Nếu Iowa guitar không đủ khoảng 250 nốt: lựa chọn tiếp theo là tự thu âm guitar (ghi rõ trong báo cáo), hoặc chấp nhận ít sequence guitar hơn và báo cáo rõ.

## 4. Quy trình thu thập và lọc (các việc phải làm)

### Bước 1.1 — Tải dữ liệu Iowa MIS
- **Guitar (bắt buộc):** `Guitar.mono.1644.1.zip` (45 file mono 16-bit 44.1 kHz) trên trang MISguitar.html.
- **Violin, viola, cello, double bass (khuyến nghị, để trộn đều hai nguồn):** chỉ file **arco**, bản 16-bit 44.1 kHz mono.
- Lưu nguyên trạng vào `raw/iowa_mis/<instrument>/` (chỉ đọc, giống `raw/philharmonia/`).
- Ghi vào [REFERENCES](../../09_REFERENCE/REFERENCES.md): URL, ngày tải, số file, dung lượng.
- **Xong khi:** đủ file cho 5 nhạc cụ, đã ghi nguồn.

### Bước 1.2 — Cắt file Iowa thành nốt đơn
**Cấu trúc thật của file Iowa guitar** (khảo sát ngày 07/10 trên cả 45 file):
- Các nốt **đi lên từng nửa cung** đúng như khoảng trong tên file. Ví dụ `A2B2`: 3 cú gảy ở giây 0.07, 12.5, 23.6 với cao độ A2 → A♯2 → B2.
- Mỗi nốt **ngân khoảng 10–13 s**, và nốt sau được gảy khi nốt trước còn vang ⇒ **KHÔNG có khoảng lặng giữa các nốt**.
- Đuôi ngân dao động nhỏ (−25 đến −40 dB so với đỉnh). Vì vậy cắt theo khoảng lặng (energy gating) **không dùng được**: thử nghiệm cho ra 743 đoạn so với 353 nốt thật.
- Cao độ đo được thấp hơn tên nốt khoảng 0.2–0.4 nửa cung (đàn lên dây hơi thấp), nên dung sai kiểm tra cao độ cần khoảng **0.6 nửa cung**.

**Cách cắt (đã chỉnh theo cấu trúc trên):**
1. Tìm **ứng viên onset**: năng lượng tăng mạnh (> 12 dB trong 60 ms) hoặc dùng SuperFlux.
2. Đo cao độ (pYIN) ở đoạn 0.15–0.5 s sau mỗi ứng viên. **Bỏ** ứng viên không có cao độ rõ (đó là dao động trong đuôi ngân).
3. **Gộp** các ứng viên liên tiếp có cùng cao độ, chỉ giữ cái đầu tiên.
4. **Kiểm tra bằng tên file:** chuỗi cao độ còn lại phải là dãy chromatic tăng dần đúng khoảng (`E2B2` ⇒ E2, F2, …, B2: 8 nốt). Nốt nào thiếu hoặc lệch quá 0.6 nửa cung thì đánh dấu `SLICE_MISMATCH`/`PITCH_MISMATCH` và loại.
5. Mỗi nốt được cắt từ onset của nó tới onset nốt kế tiếp (hoặc tới khi tắt hẳn); có thể **giới hạn 4 s đầu** cho gọn, vì project chỉ dùng tối đa 1.5 s mỗi nốt.
- Ghi ra `data/interim/iowa_notes/<instrument>/<instrument>_<note>_<dynamics>_<technique>_<string>_<range>.wav` (vd `violin_C5_mezzo-forte_arco-normal_A_C5C6.wav`; `<range>` là khoảng nốt của file gốc, giúp tên không trùng khi hai file có khoảng chồng nhau). Script chạy tiếp được: mỗi file gốc cắt xong được lưu vào `_cache/`.
- **Xong khi:** có bảng "file gốc → số nốt cắt được → số nốt qua kiểm tra pitch".

### Bước 1.3 — Catalog hợp nhất
Một catalog cho cả hai nguồn, **thêm cột `source`** (`philharmonia` | `iowa`) và `parent_file` (file Iowa gốc).

### Bước 1.4 — Áp quy tắc lọc

| Mã | Điều kiện | Status |
|---|---|---|
| F1 | Không giải mã được | `CORRUPT` |
| F2 | MD5 trùng (đánh dấu cả hai file) | `DUPLICATE` |
| F3 | Phần có âm < 0.35 s | `TOO_SHORT` |
| F4 | Lệch cao độ > 0.5 semitone (chỉ áp dụng cho nốt cắt từ Iowa) | `PITCH_MISMATCH` |
| F5 | Kỹ thuật không thuộc {arco, vibrato/non-vibrato, guitar normal/harmonics} | `OK` nhưng `split = NONE` |
| F6 | Đỉnh < 0.01 hoặc có clipping | Giữ, bật cờ `LOW_LEVEL` / `CLIPPED` để nghe lại |

### Bước 1.5 — Chia tập
Theo [SPLIT_AND_LEAKAGE](SPLIT_AND_LEAKAGE.md) §2: `midi mod 5`, **cùng một quy tắc cho cả hai nguồn** (D24), rồi chọn trong giới hạn (D23). Đã kiểm tra: mọi tập được chọn đều có cả hai nguồn.

### Bước 1.6 — Báo cáo dataset (đề mục 1)
- Bảng số lượng cuối cùng: nhạc cụ × nguồn × split.
- Biểu đồ phân bố cao độ theo nhạc cụ.
- Mô tả điểm giống và khác ([INSTRUMENT_CHARACTERISTICS](../02_AUDIO_ANALYSIS/INSTRUMENT_CHARACTERISTICS.md)).

## 5. Kết quả sau khi thu thập và lọc (đo ngày 08/10/2026, sau khi lọc tiếng ù 25 Hz — D27)
Nốt dùng được = `status = OK`, kỹ thuật đúng D20 (bộ kéo vĩ chỉ arco, nên Philharmonia giảm so với §1.3 vì đã bỏ pizz). Ô REF/DB_POOL/QUERY_POOL ghi **được chọn / có** (D23).

| Nhạc cụ | Philharmonia | Iowa | Tổng dùng được | REF | DB_POOL | QUERY_POOL |
|---|---|---|---|---|---|---|
| violin | 897 | 244 | **1 141** | 150 / 493 | 200 / 457 | 60 / 191 |
| viola | 728 | 262 | **990** | 150 / 400 | 200 / 384 | 60 / 206 |
| cello | 759 | 288 | **1 047** | 150 / 410 | 200 / 423 | 60 / 214 |
| double-bass | 751 | 279 | **1 030** | 150 / 412 | 200 / 412 | 60 / 206 |
| guitar | 106 | 339 | **445** | 150 / 177 | 181 / 181 | 60 / 87 |

Chi tiết và biểu đồ: [RESULTS_REPORT](../../00_PROJECT/RESULTS_REPORT.md) §6–7, [reports/dataset/dataset_stats.md](../../../reports/dataset/dataset_stats.md).
