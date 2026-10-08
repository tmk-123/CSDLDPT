# INSTRUMENT CHARACTERISTICS — Điểm giống và khác giữa các nhạc cụ (đề mục 1)

> Phần lý thuyết dưới đây lấy từ `_archive/03_AUDIO_CHARACTERISTICS.md` (đã rút gọn). Giải thích đầy đủ từng nhạc cụ (dây, nốt, tần số, kỹ thuật, phổ, số đo): [01_THEORY/04–10](../../01_THEORY/04_HOW_STRING_INSTRUMENTS_WORK.md). **Phần §5 phải được điền bằng số liệu đo thật ở Bước 3**; hiện đã có số **sơ bộ** từ phần lý thuyết.

## 1. Phân nhóm
| Nhóm | Nhạc cụ | Vai trò trong project |
|---|---|---|
| Kéo vĩ (bowed) | Violin, Viola, Cello, Double Bass | Trong CSDL |
| Gảy (plucked) | Guitar | Trong CSDL |
| Gảy (plucked) | Banjo, Mandolin | **Truy vấn "nhạc cụ ngoài CSDL"** |

## 2. Điểm giống nhau
1. **Tính điều hòa mạnh:** dây hai đầu cố định nên phổ có các bồi âm tại f_k = k·f₀. Trên spectrogram thấy các vạch ngang rõ.
2. **Dải tần rộng:** từ vài chục Hz tới trên 10 kHz.
3. **Cộng hưởng thùng đàn:** thân đàn đóng vai trò bộ lọc formant, quyết định âm sắc. Đây là thứ mà MFCC đo.

## 3. Điểm khác nhau
### 3.1. Cơ chế kích thích (đường bao thời gian)
- **Kéo vĩ:** chuyển động stick-slip (Helmholtz), năng lượng được duy trì liên tục nên RMS khá phẳng trong pha sustain. Có vibrato và tiếng vĩ cọ.
- **Gảy:** attack rất nhanh (5–20 ms), sau đó tắt dần theo hàm mũ; không có sustain. Mandolin dùng tremolo để kéo dài âm.
- **Đặc trưng đo được:** RMS-CV (gảy > kéo), std của MFCC.

### 3.2. Âm vực (f₀)
| Nhạc cụ | Nốt thấp (dây buông) | Dải f₀ ước tính | Độ sáng (centroid) |
|---|---|---|---|
| Double Bass | E1 (C1 nếu có phần nối dài) | Dataset: C1 – G4 (32.7 – 392 Hz) | Tối (centroid trung vị 790 Hz) |
| Cello | C2 | Dataset: C2 – C6 (65 – 1 047 Hz) | Tối – trung (1 172 Hz) |
| Viola | C3 | Dataset: C3 – D7 (131 – 2 349 Hz) | Trung (1 712 Hz) |
| Violin | G3 | Dataset: G3 – B7 (196 – 3 951 Hz) | Sáng nhất (2 299 Hz) |
| Guitar | E2 | Dataset: E2 – C6 (gảy), tới E6 (harmonic) | **Tối nhất** (781 Hz), tắt dần |
| Banjo | C3 trong dataset | Dataset: C3 – E6 (131 – 1 319 Hz) | Đanh, tắt rất nhanh (1 142 Hz) |
| Mandolin | G3 | Dataset: G3 – A6 (196 – 1 760 Hz) | Sáng, dây kép (1 590 Hz) |

Các dải **chồng lấn** (ví dụ viola và violin trùng nhau ở G3–A6) ⇒ chỉ dùng f₀ thì không đủ, cần âm sắc (MFCC).

### 3.3. Sắc thái âm sắc
- **Violin và viola:** cùng kỹ thuật; viola thân lớn hơn nên âm dày và tối hơn. Đây là cặp **dễ nhầm nhất**.
- **Cello và double bass:** tương tự ở âm vực thấp.
- **Pizz của bộ kéo vĩ** có đường bao giống âm gảy ⇒ có thể gần guitar. Đây là hiện tượng âm học đúng, không phải lỗi.
- **Banjo:** mặt cộng hưởng bằng màng da, âm đanh, tắt nhanh. **Mandolin:** dây kép lệch nhẹ nên có hiệu ứng chorus.

## 4. Hệ quả cho bộ đặc trưng
| Câu hỏi phân biệt | Đặc trưng chính |
|---|---|
| Kéo hay gảy? | RMS-CV, std MFCC |
| Lớn hay nhỏ (âm vực)? | f₀, centroid, rolloff |
| Cùng âm vực, khác thân đàn? | MFCC mean (hình bao phổ) |

## 5. Số liệu đo thật (ĐIỀN Ở BƯỚC 3)
Trên tập REF, theo nhạc cụ: median và IQR của centroid (Hz), median f₀ (Hz), RMS-CV, ZCR. Kèm boxplot `reports/figures/features_by_instrument.png`.

| Nhạc cụ | Centroid median (Hz) | f₀ median (Hz) | RMS-CV median | ZCR median |
|---|---|---|---|---|
| violin | | | | |
| viola | | | | |
| cello | | | | |
| double-bass | | | | |
| guitar | | | | |
| banjo (tham khảo) | | | | |
| mandolin (tham khảo) | | | | |

**Số sơ bộ (đã có, từ phần lý thuyết):** đo bằng `scripts/theory_figures.py` trên **mọi nốt dùng được** (không chỉ REF), 1.5 s đầu, frame có âm; F0 là cao độ danh nghĩa theo tên nốt. Chi tiết: [01_THEORY/15](../../01_THEORY/15_AUDIO_FEATURES.md), `reports/theory/feature_summary_by_instrument.csv`.

| Nhạc cụ | Số nốt | Centroid median (IQR) | F0 danh nghĩa median | RMS-CV median | ZCR median |
|---|---|---|---|---|---|
| violin | 1 141 | 2 299 Hz (1 585 – 2 929) | 740 Hz | 0.65 | 0.115 |
| viola | 990 | 1 712 Hz (1 277 – 2 171) | 466 Hz | 0.52 | 0.089 |
| cello | 1 047 | 1 172 Hz (705 – 1 604) | 247 Hz | 0.55 | 0.050 |
| double-bass | 1 030 | 790 Hz (547 – 1 076) | 123 Hz | 0.59 | 0.017 |
| guitar | 445 | 781 Hz (595 – 1 076) | 277 Hz | 0.88 | 0.031 |
| banjo (tham khảo) | 74 | 1 142 Hz (791 – 1 333) | 370 Hz | 1.60 | 0.054 |
| mandolin (tham khảo) | 80 | 1 590 Hz (1 209 – 2 035) | 571 Hz | 0.93 | 0.077 |
