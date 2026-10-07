# INTERMEDIATE RESULTS — Kết quả trung gian (đề mục 4b)

> Đề yêu cầu "minh họa kết quả trung gian (giá trị đặc trưng, tính toán độ tương đồng)". Bảng dưới đây là **những gì CLI (Bước 11) phải in hoặc vẽ**.

| # | Kết quả trung gian | Dạng | Ý nghĩa khi trình bày |
|---|---|---|---|
| 1 | Waveform + vạch ranh giới segment | Hình | Segmentation đã tìm được bao nhiêu nốt |
| 2 | Bảng segment: start, end, f₀ (Hz, tên nốt gần nhất) | Bảng | Từng "nốt" được phát hiện |
| 3 | Bảng đặc trưng rút gọn của từng segment (centroid, f₀, RMS-CV, ZCR, MFCC1–3) | Bảng | Giá trị đặc trưng (đề yêu cầu) |
| 4 | Prototype top-1 + w + nốt REF gần nhất cho từng segment | Bảng | Liên hệ single-note ↔ multi-note |
| 5 | Heatmap W (n × 20) | Hình | Phân bố mềm của từng segment |
| 6 | h gộp theo nhạc cụ (%) | Biểu đồ cột | "Query giống cello 62%, viola 25%, …" |
| 7 | u (8D) | Dòng số | Tọa độ trong không gian chỉ mục |
| 8 | Thống kê R-tree: k', số ứng viên, số vòng | Dòng số | Cơ chế lọc-tinh chỉnh |
| 9 | Bảng Top-5: hạng, file, nhạc cụ, d (52D), d₈ (8D), similarity | Bảng | Tính độ tương đồng (đề yêu cầu) |
| 10 | Scatter PC1–PC2 của DB, tô query và Top-5 | Hình | Trực quan không gian đặc trưng |

## Mẫu in ra (minh họa, số giả định)
```
Query: q_cello_0007.wav  (5.84 s)
Segments: 6   [0.00–0.88] [0.88–1.64] [1.64–2.71] ...
Seg  f0(Hz)  note  top-proto        w     nearest REF                          d
 1   146.8   D3    P10 (cello-2)   0.71  cello_D3_1_forte_arco-normal.mp3     1.21
 ...
Profile h: cello 62% | viola 21% | double-bass 12% | violin 4% | guitar 1%
u(8D): [-1.74, 0.62, 0.05, ...]
R-tree: k'=20 → 40, candidates=40/500, rounds=2, 0.8 ms
Rank  File                 Instr        d      d8     sim
 1    seq_cello_0042.wav   cello        1.873  1.412  0.348
 2    seq_cello_0013.wav   cello        1.951  1.380  0.339
 ...
```
