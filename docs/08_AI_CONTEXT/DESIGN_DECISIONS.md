# DESIGN DECISIONS — Nhật ký quyết định

> **Nguồn duy nhất cho câu hỏi "TẠI SAO chọn".** Mỗi quyết định có ID; các file khác chỉ trích ID.
> Đổi quyết định ⇒ **không xóa**: đánh dấu "Thay bởi Dxx" và thêm dòng mới.

| ID | Ngày | Quyết định | Lý do | Phương án bị loại |
|---|---|---|---|---|
| D01 | 2026-10-07 | CSDL = **500 sequence multi-note ghép** từ nốt đơn (100/nhạc cụ × 5). Banjo/mandolin là truy vấn "nhạc cụ ngoài CSDL" | Dataset không có 500 multi-note; ghép cho ground truth và cân bằng lớp; đề yêu cầu có trường hợp nhạc cụ chưa có | CSDL = 4 476 nốt đơn của 7 nhạc cụ (docs cũ) |
| D02 | 2026-10-07 | Split **theo cao độ, xen kẽ mod 5**: REF {0,1}, DB_POOL {2,3}, QUERY_POOL {4} | Chống rò rỉ bản ghi gần trùng (cùng cao độ, khác dynamics), vẫn phủ đủ âm vực | Split ngẫu nhiên theo file |
| D03 | 2026-10-07 | ~~v1 chỉ dùng technique family arco, pizz, pluck, harmonic (guitar)~~ **Thay bởi D20** | Kỹ thuật đặc biệt quá ít mẫu, gây nhiễu | Dùng mọi kỹ thuật |
| D04 | 2026-10-07 | Sample rate **22 050 Hz** cho mọi file | Đủ cho Mel/MFCC; nhanh gấp 2; điều quan trọng là thống nhất giữa DB và query | Giữ 44.1 kHz |
| D05 | 2026-10-07 | Peak-normalize 0.95; trim −40 dB với nốt đơn; **không pre-emphasis**; REF lấy 1.5 s đầu | Loại ảnh hưởng mức thu; độ dốc phổ là thông tin âm sắc; khớp phân phối với segment | Pre-emphasis 0.97 |
| D06 | 2026-10-07 | Frame 2048, hop 512, Hann | ≥ 3 chu kỳ của E1 (41 Hz); hop 23 ms đủ cho dung sai ±50 ms | 1024/256 |
| D07 | 2026-10-07 | Đặc trưng segment **32D**: MFCC c1–13 mean+std, log centroid/bandwidth/rolloff, ZCR, RMS-CV, median log2 f₀. **Bỏ MFCC c0, Silence Ratio** | c0 chỉ đo độ to; Silence Ratio phụ thuộc cách ghép chứ không phụ thuộc nhạc cụ | Vector 35D mức file (docs cũ) |
| D08 | 2026-10-07 | **Loại Chroma** khỏi vector | Đo giai điệu chứ không đo nhạc cụ | Đưa Chroma vào |
| D09 | 2026-10-07 | Segmentation = energy gating + **SuperFlux** + peak-picking + hậu xử lý (120 ms, 2 s) | Spectral flux thô cho 3–5 onset giả trên một nốt kéo vĩ (đo ngày 07/10); SuperFlux khử vibrato | Spectral flux thô; HPSS; chỉ energy |
| D10 | 2026-10-07 | Prototype = **K-means k = 4 trong từng nhạc cụ** (20 prototype), không gắn cao độ | Prototype theo cao độ làm vector mã hóa giai điệu và rất thưa | Prototype "G4 violin arco"…; histogram 5 lớp |
| D11 | 2026-10-07 | **Gán mềm** (softmax −d²/τ) + **trọng số thời lượng** α | Ổn định ở biên giữa cụm; bền với lỗi chia thừa | Hard assignment; đếm không trọng số |
| D12 | 2026-10-07 | Vector file **v = [h (20) ‖ μ (32)] = 52D** | h dùng reference và diễn giải được; μ giữ âm sắc tuyệt đối (cho nhạc cụ lạ) | Concatenate; VLAD (640D); DTW |
| D13 | 2026-10-07 | Z-score: scaler_seg (fit REF) + scaler_file (fit DB); cân bằng khối √20, √32 | Các chiều cùng thang; hai khối đóng góp ngang nhau | Min-Max; L2-normalize |
| D14 | 2026-10-07 | **PCA 8D**, fit trên DB, `whiten=False` | R-tree cần số chiều thấp; không whitening để giữ cận dưới | Không giảm chiều; whitening |
| D15 | 2026-10-07 | Độ đo **Euclid L2**; hiển thị sim = 1/(1+d) | Tương thích MINDIST của R-tree và cận dưới PCA | Cosine (docs cũ) |
| D16 | 2026-10-07 | **R\*-tree** (`rtree`/libspatialindex), 8D, capacity 10 | Hỗ trợ đủ 8D và nearest; capacity 10 để cây có chiều sâu minh họa | SQLite R\*Tree (≤ 5D); pgvector (không phải R-tree) |
| D17 | 2026-10-07 | Top-K bằng **multi-step exact k-NN** (filter 8D → refine 52D) | Kết quả chính xác như brute force, vẫn dùng R-tree thật | Chỉ lấy k-NN trong 8D (sai số); quét tuyến tính |
| D18 | 2026-10-07 | **SQLite**, vector dạng BLOB float32; R-tree file riêng đồng bộ bằng `model_version` | Không cần server; dễ demo trên Windows | PostgreSQL; JSON |
| D19 | 2026-10-07 | Sequence lưu **WAV 22 050 Hz mono 16-bit** | Không mất mát, tránh nén MP3 lần hai | MP3 |
| D20 | 2026-10-07 | Bộ kéo vĩ **chỉ dùng arco** (arco-normal, molto-vibrato, non-vibrato) trong sequence v1; guitar dùng normal + harmonics. Pizz giữ trong catalog, không ghép | Quét thật: pizz dùng được của cello = 0, double-bass = 12, nên không thể ghép đủ sequence pizz | 20% sequence pizz (thiết kế cũ) |
| D21 | 2026-10-07 | Bổ sung **University of Iowa MIS** (pre-2012, 44.1 kHz mono) cho **cả 5 nhạc cụ**; thêm cột `source`; chia tập theo (nhạc cụ, nguồn) | Guitar chỉ có 106 nốt (cần ≥ 360). Iowa không hạn chế sử dụng, cùng định dạng. Tải cho cả 5 nhạc cụ để tránh hệ thống học "nguồn thu" thay vì nhạc cụ | NSynth (16 kHz, nhiễu nguồn); IDMT-SMT-Guitar (CC BY-NC-ND); chỉ bổ sung riêng guitar |
| D22 | 2026-10-07 | Ngưỡng `TOO_SHORT` = phần có âm < **0.35 s** (thay cho 0.2 s) | Khớp với độ dài đoạn tối thiểu khi ghép sequence; chỉ loại 55 nốt | 0.2 s |

## Chờ quyết định sau khi có số liệu
| ID | Câu hỏi | Quyết định ở |
|---|---|---|
| P01 | Có bỏ chiều nào do tương quan > 0.95? | Bước 3 |
| P02 | k ∈ {3..6} cho prototype? | Bước 4 |
| P03 | δ của peak-picking | Bước 6 |
| P04 | PCA 8D hay 5–6D (theo số ứng viên)? | Bước 10 |
| P05 | ~~Có bổ sung dữ liệu guitar? Nguồn nào?~~ Đã đề xuất D21 (Iowa MIS). **Chờ người dùng duyệt và tải** | Bước D1 |
| P06 | Số nốt guitar thực tế thu được từ Iowa có đủ khoảng 250 không? Nếu thiếu: tự thu âm hay giảm số sequence guitar? | Sau Bước D2 |
