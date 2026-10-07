# GLOSSARY

## 1. Tám khái niệm phải phân biệt trong project

| Khái niệm | Là gì | Kích thước | Lưu trong CSDL? |
|---|---|---|---|
| **Raw audio** | Chuỗi mẫu PCM sau giải mã (mono, 22 050 Hz) | ~22 050 số/giây | Không; chỉ lưu đường dẫn |
| **Frame** | Cửa sổ 2048 mẫu (≈ 93 ms), hop 512 | ~43 frame/giây | **Không bao giờ** |
| **Segment** | Đoạn liên tục, *xấp xỉ* một nốt, do segmentation tìm ra | 0.12–2 s | Có (bảng `segment`) |
| **Segment feature vector** s | Âm sắc của một segment | 32D | Có (`segment.feat`) |
| **Reference prototype** P_j | Tâm cụm K-means của nốt REF thuộc một nhạc cụ | 20 × 32D | Có (`prototype`) |
| **File-level vector** v | MỘT vector cho cả file = [h ‖ μ] | 52D | Có (`file_vector.v_raw`) |
| **Indexed vector** u | v sau chuẩn hóa + PCA; là điểm trong R-tree | 8D | Có (`file_vector.u_pca`) + file R-tree |
| **Database record** | Một dòng `audio_file` + `file_vector` + một entry R-tree. **1 file = 1 record** | — | Có |

> frame → segment → (so với prototype) → v 52D → v' 52D → u 8D → điểm trong R-tree → record.

## 2. Thuật ngữ project
| Thuật ngữ | Nghĩa |
|---|---|
| REF / DB_POOL / QUERY_POOL | Ba tập nốt đơn không giao nhau ([SPLIT_AND_LEAKAGE](../04_PART_1/01_DATASET/SPLIT_AND_LEAKAGE.md)) |
| Sequence | File multi-note ghép từ nốt đơn |
| PHRASE | 446 file `phrase` thật trong dataset |
| UNSEEN | Banjo, mandolin: nhạc cụ không có trong CSDL |
| technique_family | arco / pizz / pluck / harmonic / special |
| h | Histogram mềm 20D theo prototype |
| μ | Trung bình có trọng số của z (32D) |
| α_i | Trọng số thời lượng của segment i |
| τ | Nhiệt độ softmax |
| r8 | Khoảng cách 8D tới ứng viên xa nhất trong tập ứng viên |
| model_version | Nhãn đồng bộ model, vector, index (v1, v2, …) |

## 3. Âm thanh và xử lý tín hiệu
| Thuật ngữ | Nghĩa |
|---|---|
| Timbre (âm sắc) | Thuộc tính giúp phân biệt hai nhạc cụ chơi cùng nốt, cùng độ to |
| f₀ | Tần số cơ bản, quyết định cao độ |
| Harmonics (bồi âm) | Thành phần tần số k·f₀ |
| FFT / STFT | Biến đổi sang miền tần số / theo từng frame |
| Spectrogram | Ảnh thời gian × tần số của năng lượng |
| Mel | Thang tần số mô phỏng tai người |
| MFCC | Hệ số cepstrum trên thang Mel: mô tả hình bao phổ |
| RMS, ZCR, Centroid, Bandwidth, Rolloff | Xem [02_AUDIO_FEATURES](../01_THEORY/02_AUDIO_FEATURES.md) |
| pYIN | Thuật toán ước lượng f₀ có xác suất voiced |
| Onset / Offset | Thời điểm bắt đầu / kết thúc nốt |
| Spectral flux / SuperFlux | Hàm phát hiện onset; SuperFlux chống vibrato |
| Arco / Pizz | Kéo vĩ / gảy bằng ngón trên nhạc cụ kéo vĩ |
| Legato | Chơi nối, không ngắt giữa các nốt |
| Vibrato / Tremolo / Trill | Rung cao độ / lặp nhanh một nốt / láy hai nốt |

## 4. CSDL và tìm kiếm
| Thuật ngữ | Nghĩa |
|---|---|
| CBAR | Content-Based Audio Retrieval |
| Query-by-Example | Truy vấn bằng một mẫu media |
| Feature vector | Vector số mô tả đối tượng |
| Z-score | (x − μ)/σ |
| PCA | Phân tích thành phần chính, giảm chiều |
| Lower bound (cận dưới) | d_index ≤ d_thật |
| k-NN | k láng giềng gần nhất |
| R-tree / R\*-tree | Cây chỉ mục bằng MBR / biến thể giảm chồng lấn |
| MBR | Hộp bao nhỏ nhất song song trục |
| MINDIST | Khoảng cách nhỏ nhất từ điểm tới MBR |
| Filter-and-refine / GEMINI | Lọc ở không gian chỉ mục rồi tinh chỉnh bằng khoảng cách thật |
| Curse of dimensionality | Chỉ mục kém hiệu quả khi số chiều cao |
| Hybrid storage | File media trên đĩa, metadata + vector trong CSDL |
| BLOB | Dữ liệu nhị phân trong CSDL |
| Data leakage | Thông tin của tập kiểm thử lọt vào quá trình xây dựng/tune |
| P@K, Hit@K, MRR | Xem [07_EVALUATION](../07_EVALUATION/README.md) |
| Semantic gap | Khoảng cách giữa đặc trưng mức thấp và khái niệm con người |
