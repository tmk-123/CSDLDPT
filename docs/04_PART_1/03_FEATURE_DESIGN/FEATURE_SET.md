# FEATURE SET — Bộ đặc trưng 32D cho mỗi segment (đề mục 2)

> Lý thuyết từng đặc trưng: [15_AUDIO_FEATURES](../../01_THEORY/15_AUDIO_FEATURES.md). Lý do chọn/loại: [DESIGN_DECISIONS](../../08_AI_CONTEXT/DESIGN_DECISIONS.md) D07, D08.

## 1. Phân tích và giá trị thông tin

| Feature | Đo gì | Phân biệt được gì | Theo frame? | Aggregate | Dư thừa với |
|---|---|---|---|---|---|
| **MFCC c1–c13** | Hình bao phổ (âm sắc, cộng hưởng thân đàn) | Violin/viola/cello (cùng kỹ thuật, khác thân đàn); kéo/gảy | Có | **Mean + Std**; **bỏ c0** (chỉ đo độ to) | Thấp (DCT đã giải tương quan) |
| **Spectral Centroid** | Trọng tâm phổ: độ sáng | Violin sáng ↔ bass tối | Có | Mean của log10 | Rolloff, bandwidth, MFCC c1 |
| **Spectral Bandwidth** | Độ trải phổ quanh centroid | Âm giàu/nghèo bồi âm | Có | Mean của log10 | Centroid |
| **Spectral Rolloff 85%** | Tần số dưới đó có 85% năng lượng | Giới hạn trên của phổ | Có | Mean của log10 | Centroid (mạnh) |
| **ZCR** | Tần suất đổi dấu | Tạp âm vĩ, nhiễu cao tần | Có | Mean | Centroid |
| **RMS** | Năng lượng/frame | Đường bao: gảy tắt dần ↔ kéo ổn định | Có | **CV = std/mean** (bất biến độ to); **không** dùng mean | Thấp |
| **f₀ (pYIN)** | Tần số cơ bản | Âm vực: bass ↔ violin; bổ trợ viola ↔ cello | Có | **Median** log2(f₀) trên frame voiced | Centroid (vừa) |
| ~~Chroma~~ | 12 lớp cao độ | **Giai điệu**, không phải nhạc cụ | — | **LOẠI** | — |

**Về các phép thống kê:**
- **Mean:** giá trị điển hình.
- **Std:** dùng cho MFCC, vì bắt được vibrato và độ tắt dần.
- **Median:** chỉ dùng cho f₀, vì pYIN hay nhảy quãng tám.
- Các thống kê khác không dùng, để tránh phình số chiều.

## 2. Vì sao loại Chroma
Chroma trả lời câu hỏi "nốt nào đang vang". Hai file violin chơi giai điệu khác nhau có chroma khác nhau; một file violin và một file cello chơi cùng giai điệu có chroma gần trùng. Đề bài tìm **"tiếng nhạc cụ"** tương đồng, nên Chroma sẽ kéo kết quả sai hướng.

## 3. CHỐT: vector segment s ∈ ℝ³² (thứ tự cố định)

| Chỉ số (0-based) | Đặc trưng | Số chiều |
|---|---|---|
| 0–12 | Mean MFCC c1..c13 | 13 |
| 13–25 | Std MFCC c1..c13 | 13 |
| 26 | Mean log10(centroid) | 1 |
| 27 | Mean log10(bandwidth) | 1 |
| 28 | Mean log10(rolloff 85%) | 1 |
| 29 | Mean ZCR | 1 |
| 30 | RMS-CV = std(RMS)/mean(RMS) | 1 |
| 31 | Median log2(f₀) trên frame voiced. Nếu < 20% frame voiced: gán mean REF và bật cờ `f0_missing` | 1 |

Tham số: SR 22 050; n_fft 2048; hop 512; Hann; 128 Mel band; 14 MFCC (bỏ c0); rolloff 0.85; pYIN fmin = 40 Hz, fmax = 4 200 Hz. Chỉ tính trên **frame active** (RMS > −40 dB so với đỉnh file).

> ⚠️ **Đang chờ xem lại** (số đo sơ bộ ở [15_AUDIO_FEATURES](../../01_THEORY/15_AUDIO_FEATURES.md) §16): **P08** fmin = 40 Hz bỏ sót 18 nốt double bass C1 → D♯1 (đề xuất 30 Hz); **P09** giá trị của 13 chiều MFCC std; **P10** RMS-CV phụ thuộc độ dài nốt; **P11** tiếng ồn nền trên đuôi nốt gảy; **P12** đặc trưng không chuyển sang nguồn thu khác. Chưa đổi tham số nào ở đây cho tới khi có quyết định trong [DESIGN_DECISIONS](../../08_AI_CONTEXT/DESIGN_DECISIONS.md).

## 4. Kiểm chứng giá trị thông tin (làm ở Bước 3–4)
1. **Tương quan 32×32 trên REF:** cặp nào có |r| > 0.95 thì bỏ một chiều và ghi vào DESIGN_DECISIONS. Ứng viên bị bỏ nhiều khả năng nhất: rolloff.
2. **Boxplot theo nhạc cụ** cho centroid, f₀, RMS-CV: chứng minh từng đặc trưng tách được nhóm nào.
3. **Độ tách lớp** (tùy chọn): tỉ số Fisher = phương sai giữa lớp / phương sai trong lớp cho từng chiều. Xếp hạng 32 chiều theo tỉ số này. Đây là bảng "giá trị thông tin" định lượng cho báo cáo.
