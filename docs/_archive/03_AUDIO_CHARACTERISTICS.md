# 03. AUDIO CHARACTERISTICS OF STRING INSTRUMENTS

## 1. Giới Thiệu Nhóm Nhạc Cụ Bộ Dây (Chordophones)
Dataset của chúng ta bao gồm 7 loại nhạc cụ thuộc bộ dây, có thể chia thành hai nhóm chính dựa trên phương thức kích thích dây đàn (Excitation Mechanism):
1. **Nhóm dây kéo vĩ (Bowed Strings - Dòng vĩ cầm)**: `Violin`, `Viola`, `Cello`, `Double Bass`.
2. **Nhóm dây gảy (Plucked Strings)**: `Guitar`, `Banjo`, `Mandolin`.

---

## 2. Đặc Điểm Âm Học Giống Nhau Của Các Nhạc Cụ Bộ Dây
Dựa trên lý thuyết tín hiệu âm thanh đa phương tiện ([Lecture 2](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%202%20-%20Multimedia%20data.pdf) và [Lecture 10](file:///D:/Ki1_4/HCSDLDPT/BTL/MMDB%20slides/Lecture%2010%20-%20Indexing%20and%20Retrieval%20for%20Audio.pdf)), các nhạc cụ bộ dây chia sẻ các đặc tính cốt lõi:
1. **Tính điều hòa phổ cực cao (Strong Harmonicity)**:
   * Âm thanh được tạo ra bởi sự dao động tuần hoàn của dây đàn có hai đầu cố định. Do đó, phổ tần số chứa các đỉnh bồi âm (harmonics / overtones) tại các bội số nguyên của tần số cơ bản:
     $$f_k = k \cdot f_0 \quad (k = 1, 2, 3, \dots)$$
   * So với tiếng nói (speech) hay tiếng ồn (noise), âm thanh nhạc cụ bộ dây có cấu trúc các đường kẻ ngang sắc nét (horizontal bands) trên Spectrogram (xem slide 22-24, Lecture 10).
2. **Dải tần số âm thanh rộng (Wide Bandwidth)**:
   * Trải rộng từ vài chục Hz lên tới hơn 15,000 – 20,000 Hz, vượt xa giới hạn của tiếng nói (vốn chỉ từ 300 Hz đến 3,400 Hz hoặc 7,000 Hz).
3. **Cộng hưởng thùng đàn (Acoustic Body Resonance)**:
   * Thùng đàn bằng gỗ (Soundboard) khuếch đại dao động dây và tạo ra một bộ lọc formant tự nhiên (Formant Filter), định hình âm sắc đặc trưng (timbre) cho từng nhạc cụ.

---

## 3. Đặc Điểm Khác Biệt Giữa Các Nhạc Cụ Trong Dataset

### 3.1. Phân Biệt Theo Phương Thức Kích Thích (Attack - Decay Envelope)
* **Dây kéo vĩ (Bowed Strings - Violin, Viola, Cello, Double Bass)**:
  * Cơ chế dính - trượt (Stick-slip / Helmholtz motion) giữa lông vĩ và dây đàn.
  * Tín hiệu có pha duy trì liên tục (Sustain phase) kéo dài, năng lượng trung bình ổn định (RMS Energy phẳng), Zero-Crossing Rate biến thiên mượt mà.
* **Dây gảy (Plucked Strings - Guitar, Banjo, Mandolin)**:
  * Tín hiệu có giai đoạn tấn công cực nhanh (Sharp Attack Transient, $\approx 5 - 20\text{ ms}$), sau đó năng lượng suy hao hàm mũ tự nhiên (Exponential Decay).
  * Không có pha Sustain nhân tạo của vĩ kéo. Mandolin giải quyết việc duy trì âm thanh bằng kỹ thuật **tremolo** (gảy liên tục, xuất hiện trong 41/80 file Mandolin).

### 3.2. Phân Biệt Theo Dải Tần Số Cơ Bản (Fundamental Frequency Range - $f_0$)
Kích thước hộp cộng hưởng và chiều dài dây quyết định trực tiếp cao độ $f_0$:

| Nhạc cụ | Kích thước | Nốt thấp nhất (Dây buông) | Nốt cao nhất (Thực tế) | Dải tần số $f_0$ ước tính | Vị trí trọng tâm phổ (Spectral Centroid) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Double Bass** | Rất lớn ($\approx 1.8\text{ m}$) | E1 (hoặc C1) | G4 / C5 | $\approx 41.2 \text{ Hz} - 261.6 \text{ Hz}$ | Rất thấp ($< 1,000\text{ Hz}$) |
| **Cello** | Lớn ($\approx 1.2\text{ m}$) | C2 | C6 | $\approx 65.4 \text{ Hz} - 1,046.5 \text{ Hz}$ | Trung bình thấp ($800 - 2,500\text{ Hz}$) |
| **Viola** | Trung bình ($\approx 67\text{ cm}$) | C3 | E6 | $\approx 130.8 \text{ Hz} - 1,318.5 \text{ Hz}$ | Trung bình ($1,500 - 3,500\text{ Hz}$) |
| **Violin** | Nhỏ ($\approx 60\text{ cm}$) | G3 | E7 (hoặc G7) | $\approx 196.0 \text{ Hz} - 2,637.0 \text{ Hz}$ | Cao, sáng ($2,500 - 5,000+\text{ Hz}$) |
| **Guitar (Acoustic)** | Trung bình | E2 | B5 | $\approx 82.4 \text{ Hz} - 987.8 \text{ Hz}$ | Trung bình thấp |
| **Banjo** | Mặt trống màng da | C3 (hoặc G3) | C6 | $\approx 130.8 \text{ Hz} - 1,046.5 \text{ Hz}$ | Sáng chói, đanh kim loại |
| **Mandolin** | Rất nhỏ, dây kép | G3 | D7 | $\approx 196.0 \text{ Hz} - 2,349.3 \text{ Hz}$ | Rất sáng, đanh, rung kép |

### 3.3. Đặc Tính Âm Sắc Riêng Biệt (Timbre Nuances)
* **Banjo**: Có cấu tạo mặt cộng hưởng bằng màng da (membrane) thay vì gỗ đặc. Tiếng gảy tạo ra sóng hài kim loại đanh, tắt nhanh (percussive decay), Spectral Centroid cao đột biến ở pha attack.
* **Mandolin**: Sử dụng dây kim loại kép (pairs of strings). Khi gảy, hai dây dao động với độ lệch pha vi mô tạo ra hiệu ứng âm thanh đặc thù (chorus effect / detuned harmonics), rất dễ phân biệt với Violin dù cùng dải cao độ.
* **Violin vs Viola**:
  * Cùng kỹ thuật kéo vĩ nhưng Viola có thân đàn lớn hơn và âm thanh dày, ấm, tối hơn (lower Spectral Centroid, nhiều năng lượng ở vùng 200–800 Hz).
  * Violin có âm thanh thanh thoát, chói sáng (brilliant / piercing timbre, Spectral Centroid dịch chuyển mạnh về phía 2,500–4,000 Hz).

---

## 4. Ý Nghĩa Đối Với Bài Toán Nhận Diện Và Tìm Kiếm Tương Đồng
1. **Nhận diện họ nhạc cụ (Bowed vs Plucked)**: Dựa vào Envelope thời gian, RMS Decay Rate, Silence Ratio và ZCR variance.
2. **Nhận diện kích thước / cao độ (Double Bass vs Cello vs Violin)**: Dựa vào Fundamental Frequency $f_0$, Spectral Centroid (độ sáng của âm) và Spectral Rolloff.
3. **Nhận diện bản sắc âm thanh (Acoustic fingerprinting / Timbre)**: Dựa vào các hệ số Mel-Frequency Cepstral Coefficients (MFCCs). MFCC mô tả chính xác hình bao phổ (Spectral Envelope) do thùng đàn tạo nên, loại bỏ ảnh hưởng của cao độ riêng biệt.
