# 10. INTERMEDIATE RESULTS SPECIFICATION

> **TRẠNG THÁI HIỆN TẠI TRONG PROJECT**: **CHƯA CÓ TRONG CODEBASE GỐC / CẦN TRIỂN KHAI**  
> *(Ghi nhận trung thực: Mã nguồn gốc hiện tại mới chỉ có file `Strings/scan_dataset.py` quét thông tin thời lượng/kênh qua ffprobe, chưa có module trích xuất đặc trưng trung gian và chưa có bảng kết quả ranking thực tế).*

Tài liệu này đặc tả quy chuẩn các **kết quả trung gian** bắt buộc phải trình diễn trong báo cáo và bản demo theo yêu cầu 4b của đề bài: *"Minh họa các kết quả trung gian (các giá trị đặc trưng, tính toán độ tương đồng) của quá trình truy vấn âm thanh"*.

---

## 1. Các Kết Quả Trung Gian Cần Minh Họa

Khi một file âm thanh truy vấn được đưa vào hệ thống, các kết quả trung gian sau đây sẽ được hệ thống tính toán và hiển thị từng bước:

### 1.1. Kết Quả Tiền Xử Lý (Preprocessed Audio Visualization)
* **Waveform trước và sau cắt khoảng lặng**:
  * Đồ thị sóng âm nguyên bản (Raw Waveform) hiển thị các đoạn im lặng ở đầu và đuôi.
  * Đồ thị sóng âm sau khi Trimmed & Peak Normalized về mức $[-0.95, +0.95]$.
* **Phổ tần số thời gian (Spectrogram)**:
  * Biểu đồ nhiệt 2D thời gian $\times$ tần số hiển thị các đường vân sóng hài (Harmonic bands) sắc nét của nhạc cụ bộ dây.

### 1.2. Bảng Giá Trị Đặc Trưng Trung Gian Của File Truy Vấn (Extracted Feature Values)
Bảng minh họa các giá trị vật lý cụ thể trước khi chuẩn hóa:

| Nhóm đặc trưng | Tên đặc trưng cụ thể | Giá trị đo được (Query Sample) | Ý nghĩa thính giác |
| :--- | :--- | :---: | :--- |
| **Năng lượng** | RMS Mean | $0.1245$ | Cường độ âm thanh vừa phải |
| | RMS Std | $0.0210$ | Biên độ khá ổn định trong pha kéo |
| **Tần số thời gian** | ZCR Mean | $0.0782$ | Tần số đổi dấu trung bình cao |
| | ZCR Std | $0.0094$ | Không có xung gõ bất thường |
| **Cấu trúc thời gian** | Silence Ratio | $0.0450$ ($4.5\%$) | Âm thanh liên tục, ít khoảng lặng |
| **Độ sáng phổ** | Spectral Centroid Mean | $2,845.2 \text{ Hz}$ | Âm thanh khá sáng (nhóm vĩ cầm cỡ nhỏ) |
| | Spectral Centroid Std | $340.5 \text{ Hz}$ | Độ sáng dao động nhẹ |
| **Độ lan tỏa phổ** | Spectral Bandwidth Mean | $1,920.4 \text{ Hz}$ | Bồi âm phân bố trong dải $\approx 2\text{ kHz}$ |
| | Spectral Bandwidth Std | $215.1 \text{ Hz}$ | Dải phổ ổn định |
| **Cuộn phổ** | Spectral Rolloff 85% | $5,120.0 \text{ Hz}$ | $85\%$ năng lượng nằm dưới $5.1\text{ kHz}$ |
| **Âm sắc Mel** | MFCC 0 (Log Energy) | $-195.4$ | Năng lượng tổng thể |
| | MFCC 1 | $+82.1$ | Tỷ lệ năng lượng trầm/bổng |
| | MFCC 2 đến MFCC 12 | $[\dots]$ | Chi tiết cấu trúc Formant hộp đàn |

### 1.3. Vector Đặc Trưng Số Học Đầy Đủ (Feature Vector Representation)
* **Raw Vector (35 chiều)**: Mảng 35 số thực gốc chưa chuẩn hóa.
* **Z-Score Vector**: Mảng 35 số thực sau khi trừ kỳ vọng $\mu$ và chia độ lệch chuẩn $\sigma$ của toàn bộ CSDL.
* **L2 Normalized Vector ($q_{\text{norm}}$)**: Mảng 35 số thực có tổng bình phương bằng 1 ($\|q_{\text{norm}}\|_2 = 1.0$).

### 1.4. Các Bước Tính Toán Độ Tương Đồng (Step-by-Step Similarity Computation)
Hiển thị quá trình so khớp vector truy vấn $q_{\text{norm}}$ với các vector ứng viên trong CSDL:
1. **Phép nhân ma trận vector**:
   $$\text{Scores} = V_{\text{norm}} \cdot q_{\text{norm}}$$
2. **So sánh điểm số mẫu giữa các nhóm nhạc cụ**:
   * File cùng nhóm (ví dụ: Violin truy vấn vs Cello trong DB): Cosine Sim $\approx 0.72 - 0.85$ (tương đồng về tính chất kéo vĩ nhưng khác biệt về trọng tâm phổ).
   * File khác nhóm (ví dụ: Violin truy vấn vs Banjo trong DB): Cosine Sim $\approx 0.35 - 0.50$ (khác biệt lớn về Envelope và ZCR).
   * File cùng nhạc cụ, cùng kỹ thuật (Violin truy vấn vs Violin khác): Cosine Sim $\approx 0.94 - 0.99$.

### 1.5. Kết Quả Xếp Hạng Cuối Cùng (Ranked Top-5 Results)
Bảng kết quả trả về cho người dùng với đầy đủ thông tin:

| Hạng (Rank) | Tên file kết quả | Nhạc cụ | Nốt | Kỹ thuật | Cường độ | Điểm tương đồng (Cosine Sim) | Khoảng cách Euclid ($L_2$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | `violin_Gs4_1_forte_arco-normal.mp3` | Violin | G#4 | arco-normal | forte | $\mathbf{0.9982}$ | $0.060$ |
| **#2** | `violin_A4_1_forte_arco-normal.mp3` | Violin | A4 | arco-normal | forte | $\mathbf{0.9875}$ | $0.158$ |
| **#3** | `violin_G4_1_mezzo-forte_arco-normal.mp3` | Violin | G4 | arco-normal | mezzo-forte | $\mathbf{0.9760}$ | $0.219$ |
| **#4** | `viola_E5_1_forte_arco-normal.mp3` | Viola | E5 | arco-normal | forte | $\mathbf{0.9412}$ | $0.343$ |
| **#5** | `violin_B4_1_forte_arco-normal.mp3` | Violin | B4 | arco-normal | forte | $\mathbf{0.9380}$ | $0.352$ |

---

## 2. Kế Hoạch Triển Khai Cho Bản Demo
Khi bước vào giai đoạn code, chúng ta sẽ xây dựng:
1. Giao diện trực quan cho phép người dùng click vào từng bước để xem đồ thị Spectrogram và biểu đồ so sánh vector hình mạng nhện (Radar Chart) hoặc biểu đồ thanh ngang giữa file Query và file Top-1.
2. Nút bấm xuất file JSON báo cáo chi tiết toàn bộ các kết quả trung gian này.
