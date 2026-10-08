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
| D22 | 2026-10-07 | Ngưỡng `TOO_SHORT` = phần có âm < **0.35 s** (thay cho 0.2 s) | Khớp với độ dài đoạn tối thiểu khi ghép sequence; chỉ loại 54 nốt Philharmonia (sau D27 đo lại: 76 nốt = 59 Philharmonia + 17 Iowa) | 0.2 s |
| D23 | 2026-10-08 | **Giới hạn số nốt được chọn** mỗi nhạc cụ: REF 150, DB_POOL 200, QUERY_POOL 60, chọn trải đều theo (nguồn, cao độ, cường độ). Phần dư giữ cùng split với cột `selected = 0` (dự trữ) | Cân bằng giữa các nhạc cụ: nhạc cụ nhiều nốt không được ghép đa dạng hơn nhạc cụ ít nốt. Giữ dự trữ cùng split để không phát sinh rò rỉ | Dùng hết mọi nốt; xóa nốt thừa |
| D24 | 2026-10-08 | Chia tập theo **`midi mod 5`** (thay cho "thứ tự cao độ mod 5"), cùng một quy tắc cho cả hai nguồn | Cùng một nốt (vd A4) luôn nằm cùng một tập ở cả Philharmonia và Iowa ⇒ chống rò rỉ chặt hơn; đơn giản, dễ giải thích | Chia riêng theo thứ tự cao độ trong từng nguồn (D21 cũ) |
| D25 | 2026-10-08 | Bố cục thư mục: `raw/` (dữ liệu gốc tải về, chỉ đọc: `philharmonia/` = Strings cũ, `iowa_mis/` = External cũ); `data/` (sinh ra bằng script: `interim/`, `notes/<nhạc cụ>/<nguồn>/`, `queries/`, `excluded/<lý do>/`, `catalog.csv`) | Tách "gốc" và "đã xử lý"; gom nốt dùng được theo nhạc cụ; tách riêng file không dùng; mọi thứ trong `data/` tạo lại được | Giữ `Strings/` + `External/`; xóa file không dùng |
| D26 | 2026-10-08 | Bước con của Bước 1 đánh số **1.1–1.6** (thay cho D1–D6) | D1–D6 dễ nhầm với mã quyết định D01–D25 | — |
| D27 | 2026-10-08 | **Lọc thông cao 25 Hz** (Butterworth bậc 4, không lệch pha `sosfiltfilt`) ngay sau khi giải mã, trước mọi phép đo năng lượng và đặc trưng. Đã dùng trong `p01_3_build_catalog.py` và `theory_figures.py`; cần thêm vào `load_audio` ([PREPROCESSING](../04_PART_1/02_AUDIO_ANALYSIS/PREPROCESSING.md)) | Tiếng ù hạ âm (dưới 20 Hz, tai không nghe được) chiếm trung vị 92.8% năng lượng nốt guitar Iowa; làm `active_sec` lệch > 0.5 s ở 41–56% nốt Iowa của cello, double bass, guitar, viola; 28 file đổi trạng thái sau khi lọc. Nốt thấp nhất C1 = 32.7 Hz chỉ yếu đi khoảng 1 dB | Không lọc; lọc 40 Hz (làm yếu C1–D♯1); lọc thích nghi theo cao độ (để P07) |
| D28 | 2026-10-08 | Nhãn dây guitar trong cột `string`: **`lowE`** (Iowa `sulE`, dây 6, E2) và **`highE`** (Iowa `sul_E`, dây 1, E4); các dây khác giữ chữ cái (`A`, `D`, `G`, `B`) | Trước đó cả hai dây Mi cùng nhãn `E`, làm tầng String sai (một "dây" phủ E2 → B5). Test `test_iowa_string_labels_match_physics` kiểm tra nhãn có thật trên nhạc cụ và nốt không thấp hơn dây buông | Giữ `E` cho cả hai; số dây 1–6 (lệch quy ước của 4 nhạc cụ kia); chữ thường `e` (Windows không phân biệt hoa thường trong tên file) |

## Chờ quyết định sau khi có số liệu
> Các mục P07–P12 đến từ số đo sơ bộ trong [`01_THEORY`](../01_THEORY/README.md) (script `scripts/theory_figures.py`, bảng ở `reports/theory/`), chưa phải pipeline chính thức của Bước 3.

| ID | Câu hỏi | Quyết định ở |
|---|---|---|
| P01 | Có bỏ chiều nào do tương quan > 0.95? | Bước 3 |
| P02 | k ∈ {3..6} cho prototype? | Bước 4 |
| P03 | δ của peak-picking | Bước 6 |
| P04 | PCA 8D hay 5–6D (theo số ứng viên)? | Bước 10 |
| P05 | ~~Có bổ sung dữ liệu guitar? Nguồn nào?~~ D21 (Iowa MIS) — ✅ đã tải 07/10 | Bước 1.1 |
| P06 | ~~Số nốt guitar thực tế thu được từ Iowa có đủ khoảng 250 không?~~ ✅ Đủ: cắt được 341, dùng được 339 (tổng guitar 445 nốt) | Sau Bước 1.2 |
| P07 | Khoảng 48 file guitar còn tiếng ù 25–80 Hz sau D27. Có cần lọc thông cao **thích nghi theo cao độ** (cắt dưới khoảng 0.7 × F0 của nốt)? | Bước 2–3 |
| P08 | pYIN `fmin = 40 Hz` ([FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md)) không đo được **18 nốt double bass dưới 40 Hz** (C1 → D♯1, 15 nốt đã được chọn). Hạ xuống khoảng **30 Hz**? | Bước 3, trước khi trích đặc trưng |
| P09 | Giữ, giảm hay bỏ **13 chiều MFCC std**? Đo sơ bộ từng chiều: nhạc cụ giải thích ≤ 13% phương sai, nguồn thu giải thích 11–22% (nhiều hơn nhạc cụ ở cả 13 chiều) ([15](../01_THEORY/15_AUDIO_FEATURES.md) §9) | Bước 3–5: thử bỏ trên tập dev |
| P10 | **RMS-CV phụ thuộc độ dài nốt khi thu** (violin Philharmonia nốt 0.25 s: 0.88; nốt 1.5 s: 0.48), làm mờ ranh giới gảy – kéo vĩ. Đo đường bao trên cửa sổ cố định tính từ đầu nốt, hoặc đo độ dốc tắt dần sau đỉnh? | Bước 3 |
| P11 | **Tiếng ồn nền** trên phần đuôi nốt gảy nhỏ làm đặc trưng phổ sai (guitar Iowa *pp* "sáng" hơn *ff* trên 1.5 s, dù 0.3 s đầu thì ngược lại). Dùng ngưỡng frame chặt hơn (−30 dB) cho đặc trưng phổ, hoặc trung bình có trọng số năng lượng? | Bước 3 |
| P12 | Đặc trưng gần như **không chuyển sang nguồn thu khác**: láng giềng gần nhất đúng nhạc cụ 94–98% khi cùng nguồn, 29–53% khi khác nguồn ([15](../01_THEORY/15_AUDIO_FEATURES.md) §16.1). Thêm phép đánh giá khác nguồn vào Phần 2? Bỏ đặc trưng nhạy với nguồn (MFCC std, c2, c6)? Thêm nguồn thứ ba? | Bước 3–5 và đánh giá Phần 2 |
