# data/ — Bộ dữ liệu đã dọn dẹp và sắp xếp

> **Tóm tắt:** thư mục này chứa dataset **đã lọc, gắn nhãn và sắp xếp theo nhạc cụ**, được script tạo ra từ dữ liệu gốc trong [`raw/`](../raw/README.md). File chỉ được **chép** sang, bản gốc trong `raw/` giữ nguyên.
>
> - **Không có trong git** (trừ file README này): vì chứa file mẫu Philharmonia (giấy phép cấm công khai nguyên dạng) và vì tạo lại được.
> - **Không sửa tay** bất cứ thứ gì ở đây: lần chạy script sau sẽ ghi đè.
> - Xóa `data/` (trừ README) rồi chạy lại các script là có lại y hệt (seed cố định).

## 1. Dữ liệu chảy qua đây như thế nào

```
raw/ (dữ liệu gốc tải về)
 │
 ├─ raw/iowa_mis/: 188 file, MỖI FILE NHIỀU NỐT ──► interim/iowa_notes/   (cắt ra 1 429 nốt đơn)
 │                                                        │
 └─ raw/philharmonia/: 4 477 file mp3 ───────────────────┤
                                                          ▼
                                              catalog.csv   ← "sổ quản lý": mỗi file 1 dòng, gắn nhãn
                                                          │   dựa vào nhãn, chép file vào đúng 1 trong 3 ngăn:
                       ┌──────────────────────────────────┼──────────────────────────────────┐
                       ▼                                  ▼                                  ▼
                    notes/                            queries/                           excluded/
             4 653 nốt DÙNG ĐƯỢC                 599 file để THỬ TÌM KIẾM          654 file KHÔNG DÙNG
```

Script tạo ra từng phần:

| Phần | Script | Thời gian chạy |
|---|---|---|
| `interim/iowa_notes/` | `scripts/p01_2_slice_iowa.py` | ≈ 16 phút (chạy tiếp được nếu bị dừng) |
| `catalog.csv`, `notes/`, `queries/`, `excluded/` | `scripts/p01_3_build_catalog.py` | ≈ 4 phút |

## 2. Cấu trúc và số lượng (đo ngày 08/10/2026)

```
data/
├── README.md                       file này (có trong git)
├── catalog.csv                     5 906 dòng = 5 906 file
├── notes/<nhạc cụ>/<nguồn>/        4 653 nốt đơn dùng được (646 MB)
│   ├── violin/       philharmonia 897 · iowa 244
│   ├── viola/        philharmonia 728 · iowa 262
│   ├── cello/        philharmonia 759 · iowa 288
│   ├── double-bass/  philharmonia 751 · iowa 279
│   └── guitar/       philharmonia 106 · iowa 339
├── queries/                        599 file truy vấn (35 MB)
│   ├── phrases/<nhạc cụ>/          445 đoạn nhạc thật: violin 252 · viola 55 · cello 64 · double-bass 74
│   └── unseen/<nhạc cụ>/           154 file nhạc cụ ngoài CSDL: banjo 74 · mandolin 80
├── excluded/<lý do>/<nhạc cụ>/     654 file không dùng (13 MB)
│   ├── technique/   573  kỹ thuật đặc biệt hoặc pizz (gảy) ở nhạc cụ kéo vĩ
│   ├── too_short/    76  phần có âm < 0.35 s (đo sau khi lọc tiếng ù 25 Hz)
│   ├── duplicate/     4  trùng nội dung với file khác (2 cặp, mỗi cặp mang nhãn 2 nhạc cụ khác nhau)
│   └── corrupt/       1  hỏng, không giải mã được
└── interim/iowa_notes/             kết quả trung gian của bước cắt nốt Iowa (587 MB)
    ├── <nhạc cụ>/*.wav             1 429 nốt vừa cắt
    ├── notes.csv                   mỗi nốt đã cắt một dòng
    ├── slice_report.csv            mỗi file Iowa gốc một dòng: dự kiến bao nhiêu nốt, cắt được bao nhiêu
    ├── _cache/                     kết quả cắt của từng file gốc (để chạy tiếp được)
    └── slice.log, slice.err        nhật ký lần chạy gần nhất
```

## 3. Ý nghĩa từng ngăn

| Ngăn | Là gì | Dùng ở bước nào |
|---|---|---|
| **`notes/`** | Nốt đơn sạch của 5 nhạc cụ trong CSDL. Gom theo `nhạc cụ/nguồn/` để dễ nghe thử và dễ đếm | Bước 3–4: học "thư viện âm sắc" (prototype) từ nốt **REF**. Bước 5: **ghép 500 file đoạn nhạc** cho CSDL từ nốt **DB_POOL** và 100 file truy vấn từ nốt **QUERY_POOL** |
| **`queries/`** | File chỉ dùng để **hỏi** hệ thống, không bao giờ nằm trong CSDL. `phrases/` là nhạc thật nhiều nốt; `unseen/` là nhạc cụ không có trong CSDL (đề bài mục 4 yêu cầu) | Bước 11–12: thử tìm kiếm và đánh giá |
| **`excluded/`** | File không dùng, **để riêng theo lý do thay vì xóa**: biết rõ đã loại gì, vì sao, và đổi quy tắc thì chạy lại là xong | Không dùng |
| **`interim/`** | "Bàn làm việc" của bước cắt nốt Iowa. Nốt dùng được đã được chép sang `notes/` | Bình thường không cần mở |

**Vì sao `notes/` không chia thư mục con REF / DB_POOL / QUERY_POOL?** Việc nốt nào thuộc tập nào là một **quy tắc** (chia theo cao độ, `midi mod 5`) và có thể còn chỉnh. Quy tắc được ghi trong cột `split` và `selected` của `catalog.csv`, nên đổi quy tắc chỉ cần chạy lại script, không phải xáo trộn hàng nghìn file.

## 4. `catalog.csv` — từ điển các cột

| Cột | Ý nghĩa | Ví dụ |
|---|---|---|
| `recording_id` | Số thứ tự duy nhất của file | `1` |
| `source` | Nguồn gốc: `philharmonia` hoặc `iowa` | `iowa` |
| `instrument` | Nhạc cụ | `guitar` |
| `note` | Tên nốt theo quy ước tên file (`s` = thăng) | `Ds5` (= D♯5) |
| `midi` | Số MIDI của nốt (mỗi nửa cung +1; A4 = 69) | `75` |
| `dynamics` | Cường độ khi chơi | `fortissimo` |
| `technique` | Kỹ thuật chơi ghi trong tên file | `arco-normal` |
| `technique_family` | Nhóm kỹ thuật: `arco` (kéo vĩ), `pizz` (gảy ngón ở nhạc cụ kéo vĩ), `pluck` (gảy guitar/banjo/mandolin), `harmonic`, `special` | `arco` |
| `string` | Dây đàn chơi nốt đó (chỉ nguồn Iowa có thông tin này). Bộ kéo vĩ: `G`, `D`, `A`, `E`, `C`. Guitar: `lowE` (dây 6, Mi trầm), `A`, `D`, `G`, `B`, `highE` (dây 1, Mi cao) (D28) | `lowE` |
| `duration_label` | Nhãn độ dài danh nghĩa trong tên file Philharmonia (`025`, `05`, `1`, `15`, `long`, `very-long`, `phrase`). **Không phải số giây thật** | `025` |
| `duration_sec` | Thời lượng thật của file (giây) | `1.183` |
| `active_sec` | Độ dài **phần có âm** (năng lượng > −40 dB so với đỉnh), đo **sau** khi lọc thông cao 25 Hz để bỏ tiếng ù hạ âm (D27) | `0.766` |
| `peak` | Biên độ lớn nhất (1.0 = mức tối đa) | `0.5058` |
| `clipped` | Số mẫu bị "cắt đỉnh" (méo do quá to) | `0` |
| `md5` | Dấu vân tay nội dung file; hai file cùng MD5 là giống hệt | `176854b2…` |
| `status` | File dùng được không: `OK`, `CORRUPT`, `DUPLICATE`, `TOO_SHORT` | `OK` |
| `flags` | Cờ cần nghe lại: `LOW_LEVEL` (quá nhỏ), `CLIPPED` | (trống) |
| `split` | File dùng vào việc gì: `REF`, `DB_POOL`, `QUERY_POOL`, `PHRASE`, `UNSEEN`, `NONE` | `QUERY_POOL` |
| `selected` | `1` = được chọn cho bước sau; `0` = dự trữ (vượt giới hạn chọn) hoặc không thuộc 3 tập trên | `1` |
| `reason` | Lý do không dùng (khi `split = NONE`): `corrupt`, `duplicate`, `too_short`, `technique` | `technique` |
| `path` | Đường dẫn file trong `data/` | `data/notes/violin/philharmonia/…` |
| `raw_path` | Đường dẫn file gốc | `raw/philharmonia/violin/…` |
| `parent_file` | (Iowa) file gốc nhiều nốt mà nốt này được cắt ra | `Guitar.mf.sulE.E2B2.aif` |
| `file` | Tên file | `violin_A4_025_forte_arco-normal.mp3` |
| `decode_error` | Thông báo lỗi khi giải mã (chỉ file hỏng); đã bỏ phần địa chỉ bộ nhớ của ffmpeg để catalog giống hệt giữa các lần chạy | `Failed to find two consecutive MPEG audio frames.` |

### Quy tắc gắn `split`
1. `status ≠ OK` → `NONE` (lý do = status).
2. Banjo, mandolin → `UNSEEN`.
3. File `phrase` → `PHRASE`.
4. Kỹ thuật không dùng (bộ kéo vĩ không phải arco; guitar không phải pluck/harmonic) → `NONE` (lý do `technique`).
5. Còn lại: `midi mod 5` = 0, 1 → `REF`; = 2, 3 → `DB_POOL`; = 4 → `QUERY_POOL`. Ví dụ A4: 69 mod 5 = 4 → `QUERY_POOL`.

Mỗi nhạc cụ chọn tối đa REF 150, DB_POOL 200, QUERY_POOL 60 nốt, trải đều theo nguồn, cao độ và cường độ (`selected = 1`). Lý do của từng quy tắc: [SPLIT_AND_LEAKAGE](../docs/04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md), [DESIGN_DECISIONS](../docs/08_AI_CONTEXT/DESIGN_DECISIONS.md) D20–D24.

## 5. Quy ước tên file

| Nguồn | Mẫu | Ví dụ |
|---|---|---|
| Philharmonia | `<nhạc cụ>_<nốt>_<nhãn độ dài>_<cường độ>_<kỹ thuật>.mp3` | `cello_As2_05_forte_arco-normal.mp3` |
| Iowa (sau khi cắt) | `<nhạc cụ>_<nốt>_<cường độ>_<kỹ thuật>_<dây>_<khoảng nốt của file gốc>.wav` | `guitar_A2_mezzo-forte_normal_lowE_E2B2.wav` (nốt A2, chơi trên dây Mi trầm, cắt từ file chứa các nốt E2…B2) |

## 6. Ví dụ hành trình của một nốt
1. `raw/iowa_mis/guitar/Guitar.mf.sulE.E2B2.aif` là một bản thu 8 nốt E2 → B2 trên dây Mi trầm.
2. `p01_2_slice_iowa.py` cắt ra `interim/iowa_notes/guitar/guitar_A2_mezzo-forte_normal_lowE_E2B2.wav`.
3. `p01_3_build_catalog.py` đo file, `status = OK`; A2 có MIDI 45, 45 mod 5 = 0 → `split = REF`.
4. File được chép vào `notes/guitar/iowa/`.

Cùng thư mục còn có `guitar_A2_…_A_A2B2.wav`: **cùng nốt A2 nhưng chơi trên dây La**. Cùng một cao độ, chơi trên hai dây khác nhau cho âm sắc hơi khác. Đó là lý do dữ liệu guitar cần phủ đủ 6 dây (xem [docs/01_THEORY](../docs/01_THEORY/README.md)).

## 7. Kiểm tra
```powershell
.venv\Scripts\python tests\test_catalog.py     # phải ra "12 đạt, 0 lỗi"
```
Thống kê đầy đủ và biểu đồ: [reports/dataset/dataset_stats.md](../reports/dataset/dataset_stats.md).
