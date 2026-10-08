# Thống kê dataset (tự sinh)

> File này do `scripts/p01_6_dataset_stats.py` sinh ra từ `data/catalog.csv`. **Đừng sửa tay**; chạy lại script để cập nhật.

## 1. Tổng quan: số file theo nguồn và trạng thái

| Nguồn | Tổng file | OK | CORRUPT | DUPLICATE | TOO_SHORT |
|---|---|---|---|---|---|
| philharmonia | 4477 | 4413 | 1 | 4 | 59 |
| iowa | 1429 | 1412 | 0 | 0 | 17 |
| **tổng** | 5906 | 5825 | 1 | 4 | 76 |

## 2. Phân bổ file theo split

REF/DB_POOL/QUERY_POOL: nốt đơn dùng được (chia theo `midi mod 5`). PHRASE, UNSEEN: chỉ làm truy vấn. NONE: không dùng (xem mục 5).

| Nhạc cụ | REF | DB_POOL | QUERY_POOL | PHRASE | UNSEEN | NONE | Tổng |
|---|---|---|---|---|---|---|---|
| violin | 493 | 457 | 191 | 252 | 0 | 360 | 1753 |
| viola | 400 | 384 | 206 | 55 | 0 | 196 | 1241 |
| cello | 410 | 423 | 214 | 64 | 0 | 69 | 1180 |
| double-bass | 412 | 412 | 206 | 74 | 0 | 27 | 1131 |
| guitar | 177 | 181 | 87 | 0 | 0 | 2 | 447 |
| banjo | 0 | 0 | 0 | 0 | 74 | 0 | 74 |
| mandolin | 0 | 0 | 0 | 0 | 80 | 0 | 80 |

## 3. Nốt đơn dùng được và số được chọn

Giới hạn chọn mỗi nhạc cụ (D23): REF 150, DB_POOL 200, QUERY_POOL 60. Phần dư là dự trữ (`selected = 0`), vẫn thuộc cùng split.

| Nhạc cụ | Philharmonia | Iowa | Tổng dùng được | REF (chọn / có) | DB_POOL (chọn / có) | QUERY_POOL (chọn / có) | ≥ 360? |
|---|---|---|---|---|---|---|---|
| violin | 897 | 244 | 1141 | 150 / 493 | 200 / 457 | 60 / 191 | ✅ |
| viola | 728 | 262 | 990 | 150 / 400 | 200 / 384 | 60 / 206 | ✅ |
| cello | 759 | 288 | 1047 | 150 / 410 | 200 / 423 | 60 / 214 | ✅ |
| double-bass | 751 | 279 | 1030 | 150 / 412 | 200 / 412 | 60 / 206 | ✅ |
| guitar | 106 | 339 | 445 | 150 / 177 | 181 / 181 | 60 / 87 | ✅ |

![Nốt đơn dùng được theo nhạc cụ](notes_by_instrument.png)

## 4. Độ phủ cao độ

| Nhạc cụ | Âm vực | Số nửa cung | Số cao độ có nốt | Nốt / cao độ (trung vị) | Cao độ bị trống trong âm vực |
|---|---|---|---|---|---|
| violin | G3 – B7 | 53 | 53 | 23 | — |
| viola | C3 – D7 | 51 | 51 | 21 | — |
| cello | C2 – C6 | 49 | 49 | 22 | — |
| double-bass | C1 – G4 | 44 | 44 | 24.5 | — |
| guitar | E2 – E6 | 49 | 46 | 10.0 | C#6 D6 D#6 |

![Độ phủ cao độ](pitch_coverage.png)

## 5. File không dùng (`data/excluded/<lý do>/`)

| Nhạc cụ | corrupt | duplicate | too_short | technique | Tổng |
|---|---|---|---|---|---|
| violin | 0 | 1 | 32 | 327 | 360 |
| viola | 1 | 1 | 26 | 168 | 196 |
| cello | 0 | 2 | 11 | 56 | 69 |
| double-bass | 0 | 0 | 5 | 22 | 27 |
| guitar | 0 | 0 | 2 | 0 | 2 |
| banjo | 0 | 0 | 0 | 0 | 0 |
| mandolin | 0 | 0 | 0 | 0 | 0 |

Kỹ thuật bị loại nhiều nhất: `pizz-normal` (98), `arco-col-legno-battuto` (72), `natural-harmonic` (54), `artificial-harmonic` (50), `con-sord` (44), `arco-sul-ponticello` (39), `arco-major-trill` (33), `arco-minor-trill` (31).

## 6. File dùng làm truy vấn (`data/queries/`)

| Nhạc cụ | PHRASE (đoạn nhạc thật) | UNSEEN (nhạc cụ ngoài CSDL) |
|---|---|---|
| violin | 252 | 0 |
| viola | 55 | 0 |
| cello | 64 | 0 |
| double-bass | 74 | 0 |
| guitar | 0 | 0 |
| banjo | 0 | 74 |
| mandolin | 0 | 80 |

## 7. Cắt nốt Iowa (bước 1.2)

| Nhạc cụ | File Iowa | Nốt dự kiến (theo tên file) | Nốt cắt được | Tỷ lệ |
|---|---|---|---|---|
| violin | 35 | 312 | 251 | 80% |
| viola | 32 | 292 | 267 | 91% |
| cello | 41 | 309 | 291 | 94% |
| double-bass | 35 | 286 | 279 | 98% |
| guitar | 45 | 353 | 341 | 97% |
| **tổng** | 188 | 1552 | 1429 | 92% |

File cắt được ít nhất:

| File gốc | Dự kiến | Cắt được | Nốt thiếu |
|---|---|---|---|
| Cello.arco.pp.sulA.Ab5.aiff | 1 | 0 | Gs5 |
| Guitar.pp.sulB.B3.aif | 1 | 0 | B3 |
| Violin.arco.pp.sulD.D4Bb4.aiff | 9 | 1 | Ds4 E4 F4 Fs4 G4 Gs4 A4 As4 |
| Cello.arco.mf.sulC.C4Gb4.aiff | 7 | 2 | D4 Ds4 E4 F4 Fs4 |
| Violin.arco.ff.sulA.D6G6.aiff | 6 | 2 | D6 Ds6 F6 G6 |
| Violin.arco.pp.sulA.Bb5Ab6.aiff | 11 | 6 | B5 E6 Fs6 G6 Gs6 |
| Guitar.pp.sul_E.E4B4.aif | 8 | 5 | E4 F4 As4 |
| Viola.arco.sulA.pp.C6G6.aiff | 8 | 5 | D6 E6 Fs6 |

## 8. Thời lượng phần có âm của nốt dùng được

| Nhạc cụ | Philharmonia (trung vị) | Iowa (trung vị) |
|---|---|---|
| violin | 0.91 s | 5.65 s |
| viola | 1.02 s | 2.64 s |
| cello | 0.88 s | 2.50 s |
| double-bass | 1.09 s | 3.90 s |
| guitar | 3.59 s | 5.32 s |

Nốt Iowa dài hơn vì được thu ngân hết; project chỉ dùng tối đa 1.5 s đầu mỗi nốt.
