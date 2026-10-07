# INSTRUMENT CHARACTERISTICS — Điểm giống và khác giữa các nhạc cụ (đề mục 1)

> Phần lý thuyết dưới đây lấy từ `_archive/03_AUDIO_CHARACTERISTICS.md` (đã rút gọn). **Phần §5 phải được điền bằng số liệu đo thật ở Bước 3.** Đây là điểm khiến phần trả lời đề mục 1 có giá trị, thay vì chỉ trích lý thuyết.

## 1. Phân nhóm
| Nhóm | Nhạc cụ | Vai trò trong project |
|---|---|---|
| Kéo vĩ (bowed) | Violin, Viola, Cello, Double Bass | Trong CSDL |
| Gảy (plucked) | Guitar | Trong CSDL |
| Gảy (plucked) | Banjo, Mandolin | **Query "chưa có trong CSDL"** |

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
| Double Bass | E1 | ≈ 41 – 260 Hz (cao hơn khi chơi harmonic) | Rất tối |
| Cello | C2 | ≈ 65 – 1 050 Hz | Tối – trung |
| Viola | C3 | ≈ 131 – 1 320 Hz | Trung |
| Violin | G3 | ≈ 196 – 3 500 Hz (dataset tới A♯7) | Sáng |
| Guitar | E2 | ≈ 82 – 990 Hz | Trung, tắt nhanh |
| Banjo | ~C3/G3 | ≈ 130 – 1 050 Hz | Đanh, sáng ở attack |
| Mandolin | G3 | ≈ 196 – 2 350 Hz | Rất sáng, dây kép |

Các dải **chồng lấn** (ví dụ viola và violin trùng nhau ở G3–E6) ⇒ chỉ dùng f₀ thì không đủ, cần âm sắc (MFCC).

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
