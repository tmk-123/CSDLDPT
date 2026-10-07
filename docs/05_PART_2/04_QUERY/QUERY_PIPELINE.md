# QUERY PIPELINE

## 1. Các bước

| # | Bước | Input | Xử lý | Output | Module |
|---|---|---|---|---|---|
| 1 | Nhận file | Đường dẫn (CLI) hoặc upload | — | path | `p11_query.py` |
| 2 | Validate | path | ffprobe đọc được; 0.3 s ≤ thời lượng ≤ 60 s (dài hơn thì lấy 30 s đầu); không lặng hoàn toàn | path hợp lệ hoặc thông báo lỗi | `audio_io` |
| 3 | Preprocess | path | Decode → mono → 22 050 Hz → peak-normalize | y | `audio_io` |
| 4 | Segmentation | y | SuperFlux + energy | n segment | `segmentation` |
| 5 | Feature | y, segments | 32D/segment | S (n×32) | `features` |
| 6 | Matching | S | scaler_seg, softmax tới 20 prototype; nốt REF gần nhất | W (n×20) | `representation` |
| 7 | File vector | W, S, dur | h ‖ μ | v (52D) | `representation` |
| 8 | Chuẩn hóa | v | scaler_file.transform + chia khối | v' (52D) | `reduction` |
| 9 | PCA | v' | pca.transform | u (8D) | `reduction` |
| 10 | R-tree | u | nearest(u, k') | Tập ứng viên C | `index_rtree` |
| 11 | Refine | v', C | Đọc `v_norm` của C từ CSDL, tính L2 | D | `search` |
| 12 | Dừng/sắp xếp | D, r8 | Điều kiện d₅ ≤ r8 | Top-5 chính xác | `search` |
| 13 | Trả kết quả | Top-5 ids | JOIN audio_file + instrument | Bảng kết quả + đường dẫn audio | `db` |

**Bước 3–7 là đúng hàm `audio_to_vector()` đã dùng để xây CSDL. Bước 8–9 là đúng hàm `transform()` đã dùng cho DB.** Không có code riêng cho query.

## 2. Truy vấn thuộc nhạc cụ chưa có (banjo, mandolin)
Pipeline giống hệt. Hệ thống vẫn trả 5 file **gần nhất về âm sắc**. Kết quả trung gian h cho biết query "giống nhạc cụ nào bao nhiêu %". Kỳ vọng hợp lý: banjo và mandolin là nhạc cụ gảy, nên Top-5 nghiêng về guitar và các sequence pizz.

## 3. Lỗi và xử lý
| Tình huống | Hành vi |
|---|---|
| Không decode được | Báo "Không đọc được file" + lý do từ ffprobe |
| < 0.3 s | Báo "File quá ngắn" |
| 0 segment (lặng) | Báo "Không phát hiện âm thanh" |
| > 60 s | Cảnh báo, chỉ dùng 30 s đầu |
| Model/index khác version | Từ chối, yêu cầu build lại |
