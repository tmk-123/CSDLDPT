# PROJECT SCOPE — Phạm vi, ràng buộc, rủi ro

## 1. Trong phạm vi hiện tại
- **Phần 1:** catalog dataset, chia tập, ghép sequence, tiền xử lý, đặc trưng 32D, segmentation, prototype, vector 52D.
- **Phần 2:** CSDL SQLite, chuẩn hóa + PCA, R-tree, tìm k-NN chính xác, truy vấn CLI có kết quả trung gian.

## 2. Ngoài phạm vi hiện tại (làm sau)
Đánh giá đầy đủ (ngoài các kiểm tra trong từng bước), giao diện demo, kiến trúc triển khai, báo cáo cuối.

## 3. Bắt buộc vs nâng cao (trong Phần 1, 2)

| Bắt buộc | Nâng cao (chỉ làm nếu dư thời gian) |
|---|---|
| Catalog + lọc lỗi + split theo cao độ | Pitch-split cho legato |
| 500 sequence DB + 100 query + ground truth | Bổ sung dữ liệu guitar từ nguồn mở |
| Đặc trưng 32D + kiểm tra tương quan | Augmentation (nhiễu, reverb) |
| Segmentation SuperFlux + đo F-measure | Tune λ cân bằng khối |
| 20 prototype + soft BoP + mean pooling | Tự cài đặt R-tree (insert/split) để trình bày |
| SQLite theo schema | R-tree 2D để vẽ MBR |
| Scaler + PCA 8D | PostgreSQL cube/GiST |
| R-tree + multi-step exact k-NN, kiểm chứng với brute force | |
| CLI truy vấn kèm kết quả trung gian | |

## 4. Ràng buộc
| Ràng buộc | Hệ quả |
|---|---|
| Máy Windows 10, Python 3.13.9; ffmpeg/ffprobe đã có | Nếu thư viện chưa có wheel cho 3.13, dùng venv 3.12 |
| Chưa cài: librosa, soundfile, scikit-learn, rtree | Bước 0 phải cài |
| `raw/philharmonia/` là dữ liệu gốc | **Không sửa, không di chuyển**; mọi thứ sinh ra nằm trong `data/` |
| Không giả định metadata không có | Phrase không có nhãn từng nốt, nên không đo segmentation trên phrase |
| Người làm là sinh viên, cần giải thích được với giảng viên | Ưu tiên thuật toán đơn giản, diễn giải được |

## 5. Rủi ro (Phần 1, 2)

| # | Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|---|
| 1 | Legato | Gộp nốt | Chặt segment > 2 s; pooling chịu lỗi |
| 2 | Đa âm (double-stop, hợp âm guitar) | f0 sai | Median f0; âm sắc vẫn đúng nhạc cụ |
| 3 | Nhiễu | Segment rác | Bỏ segment < −35 dB |
| 4 | Khoảng lặng | Lệch thống kê | Energy gating, chỉ dùng frame active |
| 5 | Vang (reverb) | Mờ onset | Giới hạn segment 2 s; ghi là giới hạn |
| 6 | Điều kiện thu khác | Query ngoài kém hơn | Bỏ MFCC c0, peak-normalize, dùng log |
| 7 | Độ to khác nhau | Vector đo "độ to" thay vì nhạc cụ | Peak-normalize, bỏ c0, RMS dùng CV |
| 8 | Tempo khác nhau | Số segment khác | Trọng số thời lượng α |
| 9 | Cao độ khác nhau | Âm sắc đổi theo âm vực | k = 4 prototype mỗi nhạc cụ; f0 là một chiều |
| 10 | Kỹ thuật khác (pizz vs arco) | Pizz violin giống guitar | Chấp nhận (đúng về âm học); ghi trong phân tích |
| 11 | Nốt chồng | Segment hai nốt | Như #2 |
| 12 | Segmentation sai | Vector lệch | Soft assignment + α; mục tiêu F ≥ 0.8 |
| 13 | Metadata thiếu | Không đo được segmentation trên phrase | Chỉ đo trên sequence ghép |
| 14 | Số chiều cao | R-tree vô dụng | 52D → PCA 8D |
| 15 | Curse of dimensionality | Chồng lấn MBR, nhiều ứng viên | R\*-tree, M = 10; kết quả vẫn chính xác |
| 16 | Guitar ít dữ liệu (106 bản ghi) | P@5 guitar cao giả | Cắt đoạn khác nhau mỗi lần dùng; báo cáo riêng theo nhạc cụ |
| 17 | Thiếu thư viện | Không chạy được | Bước 0 |
| 18 | pYIN chậm | Build lâu | Cache đặc trưng |

**Phương án dự phòng:** nếu không kịp làm segmentation hoặc sequence, cho CSDL = nốt đơn (mỗi file 1 segment). Mọi module phía sau giữ nguyên.
