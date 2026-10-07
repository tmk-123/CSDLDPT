# 01. AUDIO FUNDAMENTALS

## 1. Âm thanh số
- **Lấy mẫu (sampling):** đo biên độ sóng âm f_s lần mỗi giây. **Định lý Nyquist:** chỉ biểu diễn được tần số < f_s/2. Ví dụ 22 050 Hz biểu diễn được tới 11 025 Hz.
- **Lượng tử hóa:** mỗi mẫu được lưu bằng b bit (16 bit ⇒ 65 536 mức).
- **Kênh:** mono (1) hay stereo (2). Đưa về mono bằng cách lấy trung bình các kênh.
- **Nén:** MP3 là nén mất mát (bỏ thành phần tai khó nghe); WAV/PCM là không nén.

## 2. Âm nhạc cụ
- **Cao độ (pitch)** ↔ **tần số cơ bản f₀**. Nốt nhạc theo MIDI: f₀ = 440 · 2^((midi − 69)/12). Ví dụ A4 = 69 → 440 Hz; E1 = 28 → 41.2 Hz.
- **Bồi âm (harmonics):** f_k = k·f₀. Tỷ lệ biên độ giữa các bồi âm tạo nên **âm sắc (timbre)**.
- **Đường bao ADSR:** Attack – Decay – Sustain – Release. Âm gảy không có sustain; âm kéo vĩ có sustain dài.

## 3. Phân tích theo thời gian ngắn
Tín hiệu âm nhạc thay đổi theo thời gian, nên phải phân tích từng đoạn ngắn coi như "tĩnh":
- **Frame:** đoạn N mẫu liên tiếp.
- **Hop:** bước nhảy giữa hai frame (overlap = 1 − hop/N).
- **Window:** nhân frame với hàm cửa sổ (Hann: w[n] = 0.5 − 0.5·cos(2πn/(N−1))) để giảm **rò rỉ phổ** do cắt đột ngột ở hai đầu.

Đánh đổi: frame dài cho độ phân giải tần số tốt (Δf = f_s/N) nhưng độ phân giải thời gian kém.

## 4. FFT và STFT
- **DFT/FFT** của một frame: X[k] = Σₙ x[n]·w[n]·e^(−j2πkn/N); bin k ứng với tần số k·f_s/N.
- **STFT:** FFT trên mọi frame, cho ra ma trận |X[k, t]| (tần số × thời gian).
- **Spectrogram:** hình ảnh của |X|² (thường lấy log/dB).
- **Thang Mel:** m = 2595·log10(1 + f/700), mô phỏng tai người (nhạy ở tần thấp hơn ở tần cao). **Mel spectrogram** = STFT đi qua một dãy bộ lọc tam giác trên thang Mel.

## 5. Năng lượng và lặng
- **RMS** của frame: √(mean(x²)). Tính theo dB tương đối: 20·log10(RMS/RMS_max).
- **Silence trimming:** cắt các frame có dB dưới một ngưỡng (ví dụ −40 dB so với đỉnh).
- **Peak normalization:** y ← a·y / max|y|.
- **Pre-emphasis:** y[n] − 0.97·y[n−1], làm nổi tần cao. Quy ước của xử lý tiếng nói.
