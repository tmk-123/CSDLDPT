# AUDIT REPORT — Dữ liệu và project thực tế

> Đo trực tiếp ngày 07/10/2026 bằng script trên `raw/philharmonia/`. Bản audit cũ hơn nằm ở `_archive/00_PROJECT_AUDIT_REPORT.md`. Bản cũ **bỏ sót các file phrase**.

## 1. Dataset
- **4 477 file `.mp3`**, 100% tên đúng mẫu `instrument_note_durationLabel_dynamics_technique.mp3`.
- Kèm 7 file `.zip` (chưa mở; theo tên có vẻ là bản nén gốc) và file rác `double bass/_notes/dwsync.xml`.
- 100% là 44 100 Hz, mono (đo bằng ffprobe trong audit cũ).
- Lỗi đã biết: 1 file hỏng (`viola_D6_05_piano_arco-normal.mp3`); 2 cặp trùng MD5 (`cello_Cs6_1_mezzo-forte_arco-harmonic` = `violin_Ds5_phrase_forte_arco-spiccato`; `cello_Ds5_05_forte_arco-normal` = `viola_G6_05_fortissimo_arco-normal`).
- Thư mục `double bass` có dấu cách, nhưng tên file dùng `double-bass`. **Lấy tên nhạc cụ từ tên file.**

| Nhạc cụ | Tổng | Nốt đơn | `phrase` | Nốt đơn kỹ thuật cơ bản¹ | Số cao độ |
|---|---|---|---|---|---|
| violin | 1 502 | 1 249 | 253 | 969 | 49 |
| viola | 974 | 919 | 55 | 789 | 51 |
| cello | 889 | 825 | 64 | 768 | 49 |
| double-bass | 852 | 778 | 74 | 768 | 44 |
| guitar | 106 | 106 | 0 | 106 | 42 |
| banjo | 74 | 74 | 0 | — | 41 |
| mandolin | 80 | 80 | 0 | — | 39 |

¹ `arco-normal`, `molto-vibrato`, `non-vibrato`, `pizz-normal` (bộ kéo vĩ); `normal`, `harmonics` (guitar).

## 2. Single-note hay multi-note?
- **4 031 file là nốt đơn.**
- **446 file `phrase` là đoạn nhiều sự kiện.** Đếm onset thử (spectral flux thô, 25 file mẫu mỗi nhóm):

| Nhóm | Median số onset |
|---|---|
| `phrase` | ≈ 10 |
| Nốt đơn `_1_` (kéo vĩ) | ≈ 3 (**onset giả** do vibrato và tiếng vĩ) |
| Guitar | ≈ 1 |

- Thời lượng phrase: cello median 12.2 s; double-bass 9.4 s; viola 8.3 s; violin chỉ 1.0 s (trill, tremolo, spiccato).
- **Hệ quả:** (1) không có sẵn 500 file multi-note, phải ghép; (2) onset detection thô không dùng được cho bộ kéo vĩ, phải dùng SuperFlux.

## 3. Metadata hiện có

| Thông tin | Có? | Nguồn |
|---|---|---|
| Nhạc cụ | Có | Tên file |
| Cao độ (note) | Có (nốt đơn); phrase chỉ có nhãn đại diện | Tên file |
| Cường độ (dynamics) | Có, định tính | Tên file |
| Kỹ thuật | Có, phân bố rất lệch | Tên file |
| Nhãn độ dài (`025`, `05`, `1`, `15`, `long`, `very-long`, `phrase`) | Có, **danh nghĩa**, không phải thời lượng thật | Tên file |
| Duration / sample rate / channels | Có | ffprobe |
| Ranh giới nốt trong phrase | **Không** | — |
| Người chơi, cây đàn, phòng thu | **Không** | — |

## 4. Project
- Code: chỉ có `scan_dataset.py` (sai đường dẫn; nay ở `scripts/legacy/`).
- Thư viện có sẵn: numpy, scipy, matplotlib, fastapi, ffmpeg. **Chưa có:** librosa, soundfile, scikit-learn, rtree.
- Chưa có CSDL, đặc trưng, index hay giao diện.

## 5. Những điểm docs cũ (`_archive/`) không còn đúng
| Docs cũ | Thiết kế hiện tại |
|---|---|
| README ghi "✅ Hoàn thành" | Chưa có code |
| Toàn bộ là single-note | Có 446 phrase |
| CSDL = 4 476 nốt đơn, 7 nhạc cụ | CSDL = 500 multi-note, 5 nhạc cụ; banjo/mandolin là truy vấn "nhạc cụ ngoài CSDL" |
| Vector 35D mức file | 32D/segment → 52D/file |
| Có MFCC c0, Silence Ratio | Bỏ |
| 44.1 kHz | 22.05 kHz |
| Cosine + quét tuyến tính; R-tree "low priority" | Euclid + R-tree bắt buộc |
| Không có split | Split theo cao độ, chống rò rỉ |
