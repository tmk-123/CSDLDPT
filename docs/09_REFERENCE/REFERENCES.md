# REFERENCES

## Slide môn học (`MMDB slides/`)
| Lecture | Dùng cho |
|---|---|
| 1 – Introduction | Precision/Recall |
| 2 – Multimedia data | Lấy mẫu, lượng tử hóa |
| 4 – MMDS Architecture | Lưu trữ hỗn hợp |
| 5 – MM data model | Mô hình dữ liệu |
| 6 – Multidimensional data structures | k-d tree, Quadtree, **R-tree** |
| 7 – Vector database and Clustering | Không gian vector, khoảng cách, K-means, k-NN |
| 8 – Text documents and Boolean | Bag-of-words (ý tưởng cho bag-of-prototypes) |
| 9 – Multimedia metadata | Phân loại metadata |
| 10 – Indexing and Retrieval for Audio | CBAR, frame, STFT, MFCC, centroid, ZCR, RMS |

## Bài báo và tài liệu kỹ thuật
- S. Böck, G. Widmer. *Maximum Filter Vibrato Suppression for Onset Detection.* DAFx 2013. (SuperFlux)
- M. Mauch, S. Dixon. *pYIN: A Fundamental Frequency Estimator Using Probabilistic Threshold Distributions.* ICASSP 2014.
- A. Guttman. *R-trees: A Dynamic Index Structure for Spatial Searching.* SIGMOD 1984.
- N. Beckmann et al. *The R\*-tree: An Efficient and Robust Access Method for Points and Rectangles.* SIGMOD 1990.
- C. Faloutsos et al. *Fast Subsequence Matching in Time-Series Databases* (khung GEMINI, lower bounding). SIGMOD 1994.
- T. Seidl, H.-P. Kriegel. *Optimal Multi-Step k-Nearest Neighbor Search.* SIGMOD 1998.

## Thư viện
librosa · scikit-learn · rtree (libspatialindex) · SQLite · FFmpeg.

## Dataset
- `Strings/`: **Philharmonia Orchestra Sound Samples**, https://philharmonia.co.uk/resources/sound-samples/ (người dùng xác nhận ngày 07/10/2026). Điều khoản trên trang: "You are free to use these samples as you wish, including releasing them as part of a commercial work", với **một hạn chế**: samples "must not be sold or made available 'as is' (i.e. as samples or as a sampler instrument)". Không bắt buộc ghi nguồn, nhưng báo cáo vẫn nên ghi.
  - ⚠️ Hệ quả: **không được công khai nguyên file mẫu**, ví dụ để `Strings/` trong repo GitHub public. Dùng trong project, ghép thành sequence, trích đặc trưng thì đều được.
- **University of Iowa Musical Instrument Samples (MIS)**: https://theremin.music.uiowa.edu/MIS.html. Theo trang này, các bản thu "may be downloaded and used for any projects, without restrictions". Bản pre-2012: 16-bit, 44.1 kHz, mono; thu trong phòng tiêu âm. *(Ghi ngày tải, số file, dung lượng sau khi tải.)*

| Nhạc cụ | Trang | Ngày tải | Số file | Ghi chú |
|---|---|---|---|---|
| guitar | MISguitar.html | **2026-10-07** | **45** file `.aif` (từ `Guitar.mono.1644.1.zip`, 119 980 148 byte, MD5 `7add3d0272bd3ad301fc8fb5dca5300d`) | Đàn Raimundo 118, nhạc công Brian Penkrot, thu 11/12/2011, phòng tiêu âm, micro Earthworks QTC40. Lưu tại `External/iowa_mis/guitar/` (zip gốc ở `_download/`) |
| violin | MISviolin.html | | | 56 file (33 arco, 23 pizz) |
| viola | | | | |
| cello | | | | |
| double bass | | | | |

- Đã xem xét nhưng **không dùng**: NSynth (CC BY 4.0, nhưng 16 kHz); IDMT-SMT-Guitar (Zenodo 7544110, CC BY-NC-ND 4.0); GuitarSet (Zenodo 3371780, CC BY 4.0) là lựa chọn phụ cho query guitar nhạc thật.
