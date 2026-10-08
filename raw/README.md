# raw/ — Dữ liệu gốc (chỉ đọc)

> **Tóm tắt:** thư mục này chứa dữ liệu âm thanh **đúng như khi tải về**, chưa xử lý gì. Mọi xử lý (cắt nốt, lọc, sắp xếp) đều tạo kết quả trong [`data/`](../data/README.md); **không sửa, đổi tên hay xóa** file trong `raw/`.
>
> **Không có trong git** (trừ file README này): giấy phép Philharmonia **cấm công khai nguyên dạng file mẫu**, và dữ liệu khá nặng (≈ 1.3 GB). Muốn có lại dữ liệu, làm theo mục 3.

## 1. Có gì trong đây

```
raw/
├── README.md                    file này (có trong git)
├── philharmonia/                4 477 file mp3 · 189 MB · 7 nhạc cụ
│   ├── banjo/          74   (+ banjo.zip)
│   ├── cello/         889   (+ cello.zip)
│   ├── double bass/   852   (+ double bass.zip, _notes/dwsync.xml là file rác của trang web gốc)
│   ├── guitar/        106   (+ guitar.zip)
│   ├── mandolin/       80   (+ mandolin.zip)
│   ├── viola/         974   (+ viola.zip)
│   └── violin/      1 502   (+ violin.zip)
└── iowa_mis/                    188 file AIFF · ≈ 920 MB · 5 nhạc cụ
    ├── guitar/        45 .aif   (+ _download/Guitar.mono.1644.1.zip)
    ├── violin/        35 .aiff  (+ _download/manifest.csv)
    ├── viola/         32 .aiff  (+ _download/manifest.csv)
    ├── cello/         41 .aiff  (+ _download/manifest.csv)
    └── double-bass/   35 .aiff  (+ _download/manifest.csv)
```

| | Philharmonia | Iowa MIS |
|---|---|---|
| Mỗi file chứa | **Một nốt** (trừ 446 file `phrase` là đoạn nhạc ngắn) | **Nhiều nốt** liên tiếp trên một dây, đi lên từng nửa cung |
| Định dạng | MP3, 44.1 kHz, mono | AIFF PCM 16-bit, 44.1 kHz, mono |
| Thu âm | Phòng thu của dàn nhạc Philharmonia (London) | Phòng tiêu âm (không vang) của Đại học Iowa |
| Có ghi dây đàn? | Không | Có (`sulG`, `sulE`…) |
| Dùng trong project | Nguồn chính cho cả 7 nhạc cụ | Bổ sung guitar (thiếu dữ liệu) và trộn nguồn thu cho 4 nhạc cụ kéo vĩ |

## 2. Nguồn và giấy phép

| Nguồn | Trang tải | Điều khoản | Hệ quả |
|---|---|---|---|
| **Philharmonia Orchestra Sound Samples** | https://philharmonia.co.uk/resources/sound-samples/ | Được dùng tự do, kể cả thương mại; **cấm bán hoặc công khai nguyên dạng file mẫu** | Không đưa `raw/philharmonia/` (và `data/`) lên git |
| **University of Iowa Musical Instrument Samples** | https://theremin.music.uiowa.edu/MIS.html | Dùng cho mọi dự án, không hạn chế | — |

Chi tiết (ngày tải, MD5…): [docs/09_REFERENCE/REFERENCES.md](../docs/09_REFERENCE/REFERENCES.md).

## 3. Cách lấy lại dữ liệu

1. **Philharmonia**: vào trang tải, tải file zip phần **Strings** của từng nhạc cụ (banjo, cello, double bass, guitar, mandolin, viola, violin). Giải nén mỗi zip vào `raw/philharmonia/<tên nhạc cụ>/`. Giữ tên thư mục giống bảng trên, kể cả `double bass` có dấu cách.
2. **Iowa guitar**: trên trang https://theremin.music.uiowa.edu/MISguitar.html, tải `Guitar.mono.1644.1.zip` (mục *Mono – zipped*). Giải nén **chỉ các file `.aif`** (bỏ thư mục `__MACOSX`) vào `raw/iowa_mis/guitar/`; đặt file zip vào `raw/iowa_mis/guitar/_download/`.
3. **Iowa violin, viola, cello, double bass** (chỉ arco): chạy
   ```powershell
   .venv\Scripts\python scripts\p01_1_download_iowa.py
   ```
   Script tự tìm và tải 143 file arco; file đã tải đủ dung lượng sẽ được bỏ qua.
4. **Kiểm tra**: phải có 4 477 file `.mp3` trong `philharmonia/`, 45 file `.aif` và 143 file `.aiff` trong `iowa_mis/`.

Lỗi đã biết trong dữ liệu gốc (không phải do tải lỗi): 1 file hỏng (`viola/viola_D6_05_piano_arco-normal.mp3`) và 2 cặp file trùng nội dung. Script catalog tự đánh dấu và loại chúng.

## 4. Quy ước tên file

**Philharmonia:** `<nhạc cụ>_<nốt>_<nhãn độ dài>_<cường độ>_<kỹ thuật>.mp3`
```
cello_As2_05_forte_arco-normal.mp3
  cello        nhạc cụ
  As2          nốt La thăng (A♯), quãng tám 2 (s = thăng)
  05           nhãn độ dài danh nghĩa (không phải số giây thật); "phrase" = đoạn nhạc nhiều nốt
  forte        cường độ (to)
  arco-normal  kỹ thuật: kéo vĩ bình thường
```

**Iowa:** `<Nhạc cụ>.<kỹ thuật>.<cường độ>.<dây>.<khoảng nốt>[.mono].aif(f)` (viola đặt dây trước cường độ)
```
Violin.arco.mf.sulG.G3B3.aiff     violin · kéo vĩ · mf (hơi to) · trên dây G · các nốt G3, G♯3, A3, A♯3, B3
Guitar.ff.sulE.E2B2.aif           guitar · ff (rất to) · trên dây Mi trầm · 8 nốt E2 … B2
```
Giải thích thuật ngữ (arco, mf, sul…): [docs/09_REFERENCE/GLOSSARY.md](../docs/09_REFERENCE/GLOSSARY.md).
