# Thư viện sử dụng và vai trò

Ngôn ngữ: **Python 3.13**. Danh sách phiên bản chính xác nằm trong `requirements-python.txt`.

| Thư viện | Phiên bản | Vai trò trong hệ thống | Hàm chính sẽ dùng |
|---|---|---|---|
| **librosa** | 1.0.0 | Xử lý và phân tích âm thanh: đọc file, đổi tần số mẫu, STFT, trích đặc trưng | `load`, `stft`, `feature.mfcc`, `feature.spectral_centroid`, `feature.spectral_bandwidth`, `feature.spectral_rolloff`, `feature.zero_crossing_rate`, `feature.rms`, `pyin` |
| **numpy** | 2.5.4 | Tính toán trên mảng. Tín hiệu âm thanh và vector đặc trưng đều là mảng numpy | `mean`, `std`, `fft.rfft`, `linalg.norm` |
| **soundfile** | 0.14.0 | Đọc thông tin file và ghi file WAV đã chuẩn hóa | `info`, `write` |
| **scipy** | 1.18.1 | Xử lý tín hiệu cấp thấp (librosa dùng bên dưới), lọc, thống kê | `signal`, `stats` |
| **pandas** | 3.0.6 | Quản lý bảng metadata (file, nhạc cụ, nốt, độ dài) và bảng đặc trưng | `DataFrame`, `read_csv`, `groupby` |
| **matplotlib** | 3.11.2 | Vẽ dạng sóng, phổ, spectrogram, biểu đồ so sánh đặc trưng cho báo cáo | `pyplot`, `librosa.display.specshow` |
| **FFmpeg** (công cụ ngoài) | 9.0.2 | Giải mã các định dạng nén (MP3…) khi gom dữ liệu | dòng lệnh `ffmpeg` |

## Nếu thầy hỏi

**Vì sao chọn librosa?**
Đây là thư viện mã nguồn mở chuẩn trong lĩnh vực truy xuất thông tin âm nhạc (Music Information Retrieval). Nó có sẵn và đã được kiểm chứng các đặc trưng mà đề bài cần (MFCC, các đặc trưng phổ, năng lượng, cao độ), nên không phải tự cài đặt lại công thức. Nhờ vậy kết quả cũng đáng tin cậy và so sánh được với các nghiên cứu khác.

**librosa đọc file xong thì được gì?**
Một mảng numpy 1 chiều chứa các giá trị biên độ (số thực trong khoảng −1…1), kèm tần số mẫu. Gọi `librosa.load(file, sr=22050, mono=True)` thì file được trộn về mono và đổi tần số mẫu về 22 050 Hz.

**Vì sao dùng numpy mà không dùng list của Python?**
numpy tính trên cả mảng cùng lúc bằng code C đã biên dịch, nhanh hơn vòng lặp Python hàng chục đến hàng trăm lần. Một file 3 giây ở 22 050 Hz đã có khoảng 66 000 mẫu.

**Vì sao cần soundfile khi đã có librosa?**
librosa thiên về phân tích. soundfile đọc nhanh thông tin gốc của file (tần số mẫu, số kênh, độ sâu bit) mà không phải giải mã cả file, và dùng để ghi file WAV sau khi chuẩn hóa.
