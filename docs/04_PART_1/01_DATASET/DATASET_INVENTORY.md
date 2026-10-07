# DATASET INVENTORY

> Số liệu chi tiết và cách đo: [AUDIT_REPORT](../../00_PROJECT/AUDIT_REPORT.md). File này mô tả **dữ liệu gốc dùng thế nào** trong project.

## 1. Nguồn
Thư viện mẫu nốt nhạc đơn của các nhạc cụ dây, có quy ước tên kiểu Philharmonia Orchestra Sound Samples (theo docs cũ). Định dạng MP3, 44.1 kHz, mono. **Nguồn và giấy phép phải được xác nhận lại trước khi viết báo cáo** ([REFERENCES](../../09_REFERENCE/REFERENCES.md)).

## 2. Quy ước tên file
```
<instrument>_<note>_<duration-label>_<dynamics>_<technique>.mp3
cello_As2_05_forte_arco-normal.mp3
```

| Trường | Ví dụ | Ý nghĩa | Dùng trong project |
|---|---|---|---|
| instrument | `cello`, `double-bass` | Nhạc cụ | Nhãn chính (ground truth) |
| note | `As2` | Tên nốt + quãng tám; `s` = thăng | → `midi`, dùng để **chia tập** |
| duration-label | `025`, `05`, `1`, `15`, `long`, `very-long`, `phrase` | Nhãn độ dài **danh nghĩa** | Chỉ để nhận biết `phrase`; thời lượng thật lấy từ ffprobe |
| dynamics | `pianissimo` … `fortissimo` | Cường độ (định tính) | Metadata; không dùng làm đặc trưng |
| technique | `arco-normal`, `pizz-normal`, `harmonics`, … | Kỹ thuật chơi | → `technique_family`, dùng để lọc và ghép |

Đổi nốt sang MIDI: `midi = 12·(octave + 1) + pc`, với pc: C = 0, Cs = 1, D = 2, Ds = 3, E = 4, F = 5, Fs = 6, G = 7, Gs = 8, A = 9, As = 10, B = 11. Ví dụ `A4` → 69, `E1` → 28.

## 3. Nhóm kỹ thuật (`technique_family`)

| Family | Gồm | Dùng ở v1? |
|---|---|---|
| `arco` | arco-normal, molto-vibrato, non-vibrato | Có |
| `pizz` | pizz-normal | Có |
| `pluck` | normal (guitar) | Có |
| `harmonic` | harmonics (guitar), natural-harmonic, artificial-harmonic, arco-harmonic | Chỉ guitar `harmonics` |
| `special` | col-legno, sul-ponticello, sul-tasto, tremolo, trill, glissando, spiccato, staccato, con-sord, … | **Không** (giữ trong catalog, split = NONE) |

## 4. Trạng thái file (`status`)
| Status | Điều kiện | Số lượng dự kiến |
|---|---|---|
| CORRUPT | ffprobe/decode lỗi | 1 |
| DUPLICATE | MD5 trùng với file khác (đánh dấu **cả hai**) | 4 |
| TOO_SHORT | < 0.2 s sau khi cắt lặng | đo ở Bước 1–2 |
| OK | còn lại | |

## 5. Vai trò từng nhóm
Xem [DATASET_ROLES](DATASET_ROLES.md) và [SPLIT_AND_LEAKAGE](SPLIT_AND_LEAKAGE.md).
