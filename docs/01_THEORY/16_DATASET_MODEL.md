# 16. Mô hình dữ liệu — từ lý thuyết tới cách tổ chức dataset

> **Đọc xong file này bạn sẽ biết:** dataset của project được phân cấp như thế nào (Nhạc cụ → Dây → Nốt → … → Vector đặc trưng) và **mỗi tầng mang ý nghĩa gì**; tầng nào là nhãn (metadata), tầng nào là đặc tính của tín hiệu, tầng nào là đặc trưng trích xuất; **dữ liệu cần thu thập là gì và vì sao**, mỗi yêu cầu được rút ra từ lý thuyết nào; vì sao chia tập theo `midi mod 5`.
> **Cần biết trước:** các file [02](02_PITCH_NOTE_OCTAVE_SEMITONE.md)–[15](15_AUDIO_FEATURES.md). File này tổng hợp chúng.
> **Đọc tiếp:** [17 Tách nốt](17_ONSET_SEGMENTATION.md).

---

## 1. Cây phân cấp của dữ liệu

```
Instrument            violin                                  ┐
   ↓                                                           │
String                dây A                                    │  NHÃN ÂM NHẠC (metadata)
   ↓                                                           │  con người đặt, đọc từ tên file
Note                  A4                                       │
   ↓                                                           │
Octave                4                                        │
   ↓                                                           ┘
Frequency / F0        440 Hz (danh nghĩa, từ tên nốt)          ← cầu nối: nhãn ↔ vật lý
   ↓
Playing Technique     arco-normal                              ← metadata
   ↓
Audio File            violin_A4_mezzo-forte_arco-normal_A_A4B4.wav   ← đối tượng lưu trữ (1 file = 1 bản ghi)
   ↓                                                           ┐
Waveform              ~1.5 s × 22 050 mẫu/s                    │  ĐẶC TÍNH CỦA TÍN HIỆU
   ↓                                                           │  có sẵn trong âm thanh, vật lý quyết định
Spectrum/Spectrogram  1 025 bin × 65 frame                     ┘
   ↓
Extracted Features    centroid, MFCC, RMS-CV, F0 đo được…      ← ĐẶC TRƯNG TRÍCH XUẤT (project tính)
   ↓
Feature Vector        32 số / đoạn → 52 số / file → 8 số trong R-tree
```

---

## 2. Mỗi tầng mang ý nghĩa gì

| Tầng | Ý nghĩa | Loại thông tin | Trong project | Vì sao cần tầng này |
|---|---|---|---|---|
| **Instrument** | Nhạc cụ nào | Metadata | Cột `instrument` | Là **đáp án** của bài toán: dùng để chấm kết quả tìm kiếm, chia dữ liệu cân bằng |
| **String** | Chơi trên dây nào | Metadata | Cột `string`: chỉ bộ Iowa ghi (`G`, `D`, `A`, `E`, `C`; guitar `lowE`…`highE`); Philharmonia để trống | Cùng nốt, khác dây → khác âm sắc ([05](05_VIOLIN.md) §6, [09](09_GUITAR.md) §6). Kiểm tra dataset phủ đủ dây |
| **Note** | Tên cao độ | Metadata | Cột `note` (`A4`, `As4`) | Gọi tên nốt; cơ sở chia tập |
| **Octave** | Thuộc quãng tám nào | Metadata (suy ra từ nốt) | Chữ số cuối của `note` | Âm sắc đổi mạnh theo quãng tám (§3, yêu cầu 1) |
| **Frequency / F0** | Tần số cơ bản | **Cầu nối**: F0 danh nghĩa tính từ nốt; F0 thật đo từ tín hiệu | Cột `midi` (danh nghĩa); đặc trưng `median log2 F0` (đo bằng pYIN) | Nối nhãn với vật lý. Hai giá trị có thể lệch (lên dây lệch vài cent, pYIN sai quãng tám) |
| **Playing Technique** | Chơi kiểu gì | Metadata | Cột `technique`, `technique_family` | Kỹ thuật đổi âm sắc mạnh ([11](11_PLAYING_TECHNIQUES.md)) → quyết định nốt nào vào CSDL (D20) |
| **Audio File** | Một bản thu | Đối tượng lưu trữ | Một dòng `catalog.csv`; một bản ghi `audio_file` trong CSDL | Đơn vị được lưu, tìm kiếm và trả về |
| **Waveform** | Áp suất theo thời gian | Đặc tính tín hiệu | Dãy mẫu sau tiền xử lý ([12](12_DIGITAL_AUDIO.md) §7) | Nguồn của mọi thứ phía dưới; cho RMS, ZCR, F0 |
| **Spectrum / Spectrogram** | Tần số nào mạnh, lúc nào | Đặc tính tín hiệu | STFT 2 048 / 512 / Hann ([14](14_FFT_STFT_SPECTRUM.md)) | Cho thấy công thức harmonic và cộng hưởng thân đàn |
| **Extracted Features** | Các con số tóm tắt âm sắc | Đặc trưng trích xuất | 32 số mỗi đoạn ([15](15_AUDIO_FEATURES.md), [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md)) | So sánh được giữa các file (bất biến pha, độ dài, độ to) |
| **Feature Vector** | Một điểm trong không gian nhiều chiều | Đặc trưng trích xuất | 52 số mỗi file → 8 số cho R-tree ([18](18_FEATURE_VECTOR.md), [20](20_PCA.md)) | Đơn vị để tính khoảng cách và đánh chỉ mục |

**Ranh giới quan trọng nhất** nằm giữa nửa trên (metadata) và nửa dưới (tín hiệu, đặc trưng):
- **Hệ thống tìm kiếm chỉ được nhìn nửa dưới.** File truy vấn của người dùng không có nhãn ([12](12_DIGITAL_AUDIO.md) §6).
- **Metadata chỉ dùng để:** chia tập dữ liệu, cân bằng, chấm điểm kết quả, và giải thích.

---

## 3. Dữ liệu cần thu thập là gì, và vì sao

Mỗi yêu cầu dưới đây được **rút ra từ một điều lý thuyết** đã chứng minh bằng số đo:

| # | Yêu cầu | Vì sao (lý thuyết + số đo) | Dataset đáp ứng ra sao |
|---|---|---|---|
| 1 | **Mỗi nhạc cụ ở nhiều nốt, phủ hết âm vực** | Âm sắc đổi mạnh theo cao độ: centroid ÷ F0 của violin giảm từ 6.0 (quãng tám 3) xuống 1.3 (quãng tám 7) ([05](05_VIOLIN.md) §10). Chỉ thu vài nốt thì hệ thống chỉ biết "một vùng" của nhạc cụ | 40–52 cao độ khác nhau mỗi (nhạc cụ, nguồn); bảng §5 |
| 2 | **Nhiều cường độ** cho mỗi nốt | Nốt to sáng hơn nốt nhỏ 10–18% ([11](11_PLAYING_TECHNIQUES.md) §3.3) | Philharmonia 6–7 mức; Iowa 3 mức (pp, mf, ff) |
| 3 | **Nhiều dây** cho cùng nốt | Cùng nốt trên dây khác → âm sắc khác ([05](05_VIOLIN.md) §6) | Iowa ghi dây; ví dụ E4 guitar có trên cả 5 dây ([09](09_GUITAR.md) §6) |
| 4 | **Nhiều cách chơi** | Để **đo** biến thiên trong cùng nhạc cụ, và biết đặc trưng nào bền ([11](11_PLAYING_TECHNIQUES.md) §5) | Philharmonia có 14 kỹ thuật cho violin. CSDL chỉ giữ arco (D20); phần còn lại để riêng |
| 5 | **Nhiều nơi thu** | Phòng và micro làm đặc trưng lệch tới 60% (cello). Nếu mỗi nhạc cụ chỉ có một nguồn, hệ thống sẽ "nhận phòng thu" thay vì nhận nhạc cụ ([07](07_CELLO.md) §9.1) | 2 nguồn (Philharmonia, Iowa) **cho cả 5 nhạc cụ** (D21), trộn trong mọi tập; có test kiểm tra |
| 6 | **Nốt đơn có nhãn chắc chắn** | Để học "mỗi nhạc cụ trông thế nào" từ mẫu sạch: một file = một nốt = một nhãn | Tập REF ([18](18_FEATURE_VECTOR.md)) |
| 7 | **File nhiều nốt** | Đối tượng thật cần lưu và tìm là đoạn nhạc, không phải một nốt | 500 sequence ghép từ nốt thật + 445 đoạn phrase thật ([SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md)) |
| 8 | **Nhạc cụ ngoài CSDL** | Kiểm tra hệ thống làm gì khi không có đáp án đúng | Banjo, mandolin: tập UNSEEN ([10](10_BANJO_MANDOLIN.md)) |
| 9 | **Kiểm soát chất lượng** | File hỏng, trùng (có cả trùng mà khác nhãn), quá ngắn, bị cắt đỉnh, tiếng ù hạ âm đều làm sai số đo | Cột `status`, `flags`, `clipped`; lọc thông cao 25 Hz (D27); §6 |

---

## 4. Ví dụ cây dữ liệu bằng file thật

Ví dụ trong CLAUDE.md, điền bằng dữ liệu có thật của project:
```
Violin
 └── Dây A
      └── A4  (MIDI 69 · F0 = 440 Hz · 69 mod 5 = 4 → QUERY_POOL)
           ├── Arco (arco-normal)
           │    ├── violin_A4_mezzo-forte_arco-normal_A_A4B4.wav     Iowa, dây A buông
           │    └── violin_A4_1_fortissimo_arco-normal.mp3           Philharmonia (không ghi dây)
           ├── Pizzicato        — không có bản thu A4 nào (pizz violin có ở 48 cao độ khác, G3 → A6)
           ├── Tremolo
           │    └── violin_A4_phrase_fortissimo_arco-tremolo.mp3     đoạn phrase (truy vấn nhạc thật)
           └── Vibrato
                └── (molto-vibrato có ở 45 nốt khác, không có ở A4)
```
Ngoài dây A, nốt A4 còn được thu trên **dây D** (`violin_A4_fortissimo_arco-normal_D_D4B4.wav`) và **dây G** (`violin_A4_pianissimo_arco-normal_G_A4Gb5.wav`).

**Nhận xét:** cây "đầy đủ" (mọi nhạc cụ × mọi dây × mọi nốt × mọi kỹ thuật) **không tồn tại** trong bất kỳ bộ dữ liệu công khai nào. Ô nào cũng đủ thì cần hàng chục nghìn bản thu. Thiết kế của project là: **phủ dày** những tầng quan trọng nhất cho nhận dạng nhạc cụ (nốt, cường độ, nguồn thu), và **phủ vừa đủ** các tầng còn lại (dây: chỉ Iowa; kỹ thuật: chỉ arco trong CSDL).

---

## 5. Dataset hiện có, theo từng tầng

**Số nốt dùng được** (đạt chất lượng, đúng kỹ thuật cho CSDL) theo quãng tám:

| Nhạc cụ | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Tổng | Philharmonia + Iowa |
|---|---|---|---|---|---|---|---|---|---|
| Violin | | | 116 | 291 | 328 | 257 | 149 | **1 141** | 897 + 244 |
| Viola | | | 240 | 292 | 263 | 176 | 19 | **990** | 728 + 262 |
| Cello | | 253 | 287 | 279 | 213 | 15 | | **1 047** | 759 + 288 |
| Double bass | 200 | 330 | 329 | 171 | | | | **1 030** | 751 + 279 |
| Guitar | | 49 | 147 | 168 | 78 | 3 | | **445** | 106 + 339 |

(Q = quãng tám.) Sự phân bố khớp với âm vực của từng nhạc cụ ([02](02_PITCH_NOTE_OCTAVE_SEMITONE.md) §8). Guitar ít nốt nhất. Hình phủ cao độ: [`reports/dataset/pitch_coverage.png`](../../reports/dataset/pitch_coverage.png).

**Tầng dây** (chỉ Iowa, số nốt dùng được):

| Nhạc cụ | Các dây |
|---|---|
| Violin | G 63 · D 53 · A 54 · E 74 |
| Viola | C 65 · G 69 · D 66 · A 62 |
| Cello | C 74 · G 73 · D 70 · A 71 |
| Double bass | E 66 · A 74 · D 73 · G 66 |
| Guitar | lowE 58 · A 59 · D 57 · G 54 · B 57 · highE 54 |

---

## 6. Từ "bản ghi gốc" tới "tập dữ liệu": các bước lọc

```
5 906 bản ghi  (Philharmonia 4 477 file mp3 + 1 429 nốt cắt từ 188 file aiff của Iowa)
   │  1. Giải mã được không?        → CORRUPT 1 file
   │  2. Nội dung có trùng không?   → DUPLICATE 4 file (2 cặp MD5 trùng; cả hai cặp mang nhãn hai nhạc cụ khác nhau)
   │  3. Phần có âm ≥ 0.35 s?       → TOO_SHORT 76 nốt (đo sau lọc thông cao 25 Hz)
   │  4. Nhạc cụ có trong CSDL?     → không: UNSEEN (banjo 74, mandolin 80)
   │  5. Là đoạn nhiều nốt?         → PHRASE 445
   │  6. Kỹ thuật hợp lệ (D20)?     → không: để riêng 573 nốt
   ▼
4 653 nốt dùng được → chia theo midi mod 5 (§7) → chọn tối đa REF 150 / DB_POOL 200 / QUERY_POOL 60 mỗi nhạc cụ (D23)
```
Chi tiết, bảng số và lý do: [DATASET_COLLECTION_AND_FILTERING](../04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md), [`data/README.md`](../../data/README.md).

---

## 7. Vì sao chia tập theo `midi mod 5`

**Vấn đề — rò rỉ dữ liệu.** Nếu cùng một **cao độ** của cùng nhạc cụ xuất hiện ở cả tập dùng để xây CSDL lẫn tập truy vấn (dù khác cường độ, khác nguồn), thì truy vấn gần như "tìm thấy chính mình", vì cùng nốt, cùng nhạc cụ thì âm sắc rất giống. Kết quả đánh giá sẽ **đẹp giả tạo**.

**Quy tắc:**
```
r = midi mod 5
r = 0 hoặc 1 → REF          (học "mỗi nhạc cụ trông thế nào")
r = 2 hoặc 3 → DB_POOL      (ghép 500 sequence của CSDL)
r = 4        → QUERY_POOL   (ghép 100 sequence truy vấn)
```
**Ví dụ:** A4 = 69 → 69 mod 5 = 4 → mọi bản thu A4 (mọi nhạc cụ, mọi cường độ, cả hai nguồn) chỉ nằm trong QUERY_POOL. C4 = 60 → 0 → REF. D4 = 62 → 2 → DB_POOL.

**Vì sao "mod 5" mà không chia theo dải (ví dụ: nốt thấp làm REF, nốt cao làm truy vấn)?** Năm nửa cung liền nhau rơi vào đủ 3 tập, nên **tập nào cũng phủ đủ âm vực** thấp, giữa, cao. Điều này cần thiết vì âm sắc đổi theo cao độ (yêu cầu 1). Hai nốt cách nhau nửa cung vẫn giống nhau phần nào, nhưng đó là **tổng quát hóa hợp lệ**: hệ thống phải nhận ra violin ở một nốt nó chưa từng thấy.

Chi tiết: [SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md). Có test tự động: `test_one_pitch_one_split`, `test_split_follows_midi_mod_5`.

---

## 8. Mô hình dữ liệu trong CSDL

Cây phân cấp ở §1 trở thành các bảng quan hệ ([22](22_MULTIMEDIA_DATABASE.md), [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md)):

| Tầng | Bảng / cột trong CSDL |
|---|---|
| Instrument | bảng `instrument` (tên, kéo vĩ hay gảy, có trong CSDL không) |
| String, Note, Octave, F0 danh nghĩa, Technique, nguồn | **thuộc tính** của bảng `source_note` (một dòng = một nốt đơn gốc) |
| Audio File | bảng `audio_file` (một dòng = một đối tượng tìm kiếm: sequence, phrase, truy vấn) |
| Waveform, Spectrum | **không lưu** trong CSDL: file âm thanh nằm trên đĩa, CSDL lưu đường dẫn; phổ tính lại khi cần |
| Extracted Features (theo đoạn) | bảng `segment` (cột `feat`: 32 số) |
| Feature Vector (theo file) | bảng `file_vector` (52 số và 8 số) + chỉ mục R-tree |

Vì sao String, Note, Technique là **cột** chứ không phải **bảng riêng**: chúng là thuộc tính mô tả một bản thu, không có thông tin đi kèm nào cần lưu riêng. Vì sao **không có bảng frame**: frame chỉ là đơn vị tính toán trung gian (hàng trăm frame mỗi file), không phải đối tượng người dùng tìm kiếm.
