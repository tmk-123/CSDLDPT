# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MD_PATH_1 = BASE_DIR / "reports" / "Bao_cao_BTL.md"
MD_PATH_2 = BASE_DIR / "Bao_cao_BTL.md"

df_a2 = pd.read_csv(BASE_DIR / "reports" / "bang_a2_thong_ke_mo_ta.csv")
a2_rows = []
for idx, row in df_a2.iterrows():
    a2_rows.append(f"| {idx+1} | `{row['Đặc trưng']}` | {row['Nhóm']} | {row['Min']:.4f} | {row['Max']:.4f} | {row['Mean']:.4f} | {row['Std']:.4f} |")
a2_table_str = "\n".join(a2_rows)

parts = []

parts.append("""# BÁO CÁO SỐ 1: BỘ DỮ LIỆU VÀ BỘ ĐẶC TRƯNG
## XÂY DỰNG HỆ CSDL LƯU TRỮ VÀ TÌM KIẾM ÂM THANH NHẠC CỤ BỘ DÂY

---

**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**  
**KHOA CÔNG NGHỆ THÔNG TIN 1**  
*o0o*

### BÀI TẬP LỚN: HỆ CƠ SỞ DỮ LIỆU ĐA PHƯƠNG TIỆN

**Tên đề tài:** Xây dựng hệ CSDL lưu trữ và tìm kiếm âm thanh nhạc cụ bộ dây  
**Nhóm lớp:** 01  
**Nhóm bài tập:** 02  

**Sinh viên thực hiện:**  
1. **Trần Mạnh Khiêm** — MSSV: **B23DCCN437**  
2. **Phạm Hồng Khởi** — MSSV: **B23DCCN451**  

**Giảng viên hướng dẫn:** TS. Nguyễn Đình Hóa  

*HÀ NỘI, 10/2026*

---

## LỜI CẢM ƠN

Nhóm thực hiện xin gửi lời cảm ơn chân thành và sâu sắc nhất tới **TS. Nguyễn Đình Hóa**, giảng viên học phần *Hệ cơ sở dữ liệu đa phương tiện*, đã định hướng đề tài, tận tình truyền đạt kiến thức nền tảng và đóng góp những ý kiến quý báu trong suốt quá trình nhóm nghiên cứu, thu thập dữ liệu và thiết kế hệ thống.

Nhóm cũng xin trân trọng cảm ơn các tác giả và tổ chức nghiên cứu âm nhạc số quốc tế (MusicNet Consortium, Philharmonia Orchestra London, và dự án Google Magenta NSynth) đã công bố các bộ dữ liệu âm thanh mẫu nguyên bản, tạo tiền đề thực nghiệm vững chắc cho báo cáo này. 

Báo cáo số 1 trình bày quy trình xây dựng bộ dữ liệu âm thanh nhạc cụ bộ dây và thiết kế, trích xuất, đánh giá hệ thống 58 đặc trưng âm học phục vụ bài toán tìm kiếm âm thanh theo nội dung (CBAR). Mặc dù nhóm đã nỗ lực tối đa để chuẩn hóa dữ liệu và phương pháp thực nghiệm, song do thời gian và kinh nghiệm còn hạn chế, báo cáo khó tránh khỏi những thiếu sót nhất định. Nhóm kính mong nhận được những nhận xét, góp ý quý báu của Thầy để hoàn thiện các giai đoạn tiếp theo của đề tài.

*Hà Nội, tháng 10 năm 2026*  
**Nhóm sinh viên thực hiện**  
*Trần Mạnh Khiêm — Phạm Hồng Khởi*

---

## MỤC LỤC

- [LỜI CẢM ƠN](#lời-cảm-ơn)
- [MỤC LỤC](#mục-lục)
- [DANH MỤC HÌNH VẼ](#danh-mục-hình-vẽ)
- [DANH MỤC BẢNG BIỂU](#danh-mục-bảng-biểu)
- [DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT](#danh-mục-thuật-ngữ-và-từ-viết-tắt)
- [CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI](#chương-1-giới-thiệu-đề-tài)
  - [1.1 Đặt vấn đề](#11-đặt-vấn-đề)
  - [1.2 Mục tiêu và phạm vi của báo cáo](#12-mục-tiêu-và-phạm-vi-của-báo-cáo)
  - [1.3 Định hướng giải pháp](#13-định-hướng-giải-pháp)
  - [1.4 Bố cục báo cáo](#14-bố-cục-báo-cáo)
- [CHƯƠNG 2. XÂY DỰNG BỘ DỮ LIỆU ÂM THANH NHẠC CỤ BỘ DÂY](#chương-2-xây-dựng-bộ-dữ-liệu-âm-thanh-nhạc-cụ-bộ-dây)
  - [2.1 Nguồn dữ liệu](#21-nguồn-dữ-liệu)
  - [2.2 Quy cách âm thanh trong bộ dữ liệu](#22-quy-cách-âm-thanh-trong-bộ-dữ-liệu)
  - [2.3 Quy trình tiền xử lý](#23-quy-trình-tiền-xử-lý)
  - [2.4 Tổ chức lưu trữ](#24-tổ-chức-lưu-trữ)
  - [2.5 Thống kê bộ dữ liệu](#25-thống-kê-bộ-dữ-liệu)
  - [2.6 Đặc điểm giống và khác nhau giữa các nhạc cụ](#26-đặc-điểm-giống-và-khác-nhau-giữa-các-nhạc-cụ)
    - [2.6.1 Đặc điểm giống nhau](#261-đặc-điểm-giống-nhau)
    - [2.6.2 Đặc điểm khác nhau](#262-đặc-điểm-khác-nhau)
    - [2.6.3 Biến thiên trong cùng nhạc cụ và tương đồng giữa các nhạc cụ](#263-biến-thiên-trong-cùng-nhạc-cụ-và-tương-đồng-giữa-các-nhạc-cụ)
- [CHƯƠNG 3. BỘ ĐẶC TRƯNG NHẬN DIỆN VÀ TRUY VẤN ÂM THANH](#chương-3-bộ-đặc-trưng-nhận-diện-và-truy-vấn-âm-thanh)
  - [3.1 Tổng quan bộ đặc trưng](#31-tổng-quan-bộ-đặc-trưng)
  - [3.2 Nhóm đặc trưng thời gian và năng lượng](#32-nhóm-đặc-trưng-thời-gian-và-năng-lượng)
  - [3.3 Nhóm đặc trưng phổ tần và âm sắc](#33-nhóm-đặc-trưng-phổ-tần-và-âm-sắc)
  - [3.4 Nhóm đặc trưng cao độ và hòa âm](#34-nhóm-đặc-trưng-cao-độ-và-hòa-âm)
  - [3.5 Biểu diễn vectơ và độ đo tương đồng](#35-biểu-diễn-vectơ-và-độ-đo-tương-đồng)
- [CHƯƠNG 4. ĐÁNH GIÁ GIÁ TRỊ THÔNG TIN CỦA ĐẶC TRƯNG](#chương-4-đánh-giá-giá-trị-thông-tin-của-đặc-trưng)
  - [4.1 Phương pháp đánh giá](#41-phương-pháp-đánh-giá)
    - [4.1.1 Đánh giá từng đặc trưng](#411-đánh-giá-từng-đặc-trưng)
    - [4.1.2 Đánh giá theo nhóm đặc trưng](#412-đánh-giá-theo-nhóm-đặc-trưng)
  - [4.2 Khả năng phân biệt của từng đặc trưng](#42-khả-năng-phân-biệt-của-từng-đặc-trưng)
  - [4.3 Tương quan và dư thừa giữa các đặc trưng](#43-tương-quan-và-dư-thừa-giữa-các-đặc-trưng)
  - [4.4 Khoảng cách giữa các mẫu cùng loại và khác loại](#44-khoảng-cách-giữa-các-mẫu-cùng-loại-và-khác-loại)
  - [4.5 Đóng góp của từng nhóm đặc trưng](#45-đóng-góp-của-từng-nhóm-đặc-trưng)
  - [4.6 Kết quả truy vấn minh họa](#46-kết-quả-truy-vấn-minh-họa)
- [CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN](#chương-5-kết-luận-và-hướng-phát-triển)
  - [5.1 Kết quả đạt được](#51-kết-quả-đạt-được)
  - [5.2 Hạn chế](#52-hạn-chế)
  - [5.3 Hướng phát triển](#53-hướng-phát-triển)
- [TÀI LIỆU THAM KHẢO](#tài-liệu-tham-khảo)
- [PHỤ LỤC](#phụ-lục)
  - [A. THỐNG KÊ CHI TIẾT BỘ DỮ LIỆU VÀ ĐẶC TRƯNG](#a-thống-kê-chi-tiết-bộ-dữ-liệu-và-đặc-trưng)
    - [A.1. Số mẫu và kết quả truy vấn theo nhạc cụ](#a1-số-mẫu-và-kết-quả-truy-vấn-theo-nhạc-cụ)
    - [A.2. Thống kê mô tả 58 đặc trưng](#a2-thống-kê-mô-tả-58-đặc-trưng)

---

## DANH MỤC HÌNH VẼ

- **Hình 2.1:** Quy trình 3 bước tiền xử lý tín hiệu âm thanh mẫu (Lọc khoảng lặng, cắt nốt, fade in/out)
- **Hình 2.2:** Số lượng tệp âm thanh WAV của từng nhạc cụ; đường nét đứt là giá trị trung bình 100 tệp
- **Hình 2.3:** Dạng sóng thời gian và phổ Spectrogram đại diện của 6 nhạc cụ bộ dây
- **Hình 2.4:** Dải âm vực vật lý và tần số cơ bản F0 của các nhạc cụ bộ dây
- **Hình 2.5:** So sánh dạng sóng và phổ tần số giữa các cặp nhạc cụ đối chứng dễ nhầm lẫn
- **Hình 3.1:** Quy trình tổng thể trích xuất vectơ 58 đặc trưng âm học từ tín hiệu âm thanh
- **Hình 3.2:** Chi tiết cơ chế trích xuất của từng nhóm đặc trưng (Phổ STFT, Mel-Filterbank, Chroma STFT)
- **Hình 4.1:** Fisher ratio và Thông tin tương hỗ (MI) của 15 đặc trưng hàng đầu
- **Hình 4.2:** Phân bố theo nhạc cụ của 4 đặc trưng có Fisher ratio cao nhất
- **Hình 4.3:** Ma trận tương quan Pearson giữa các đặc trưng với phân vùng theo nhóm
- **Hình 4.4:** Phân bố khoảng cách Euclid giữa các cặp âm thanh cùng loại và khác loại
- **Hình 4.5:** Ba truy vấn minh họa (Violin, Cello, Electric Guitar) kèm khoảng cách Euclid và nhãn đúng/sai

---

## DANH MỤC BẢNG BIỂU

- **Bảng 2.1:** Đối chiếu yêu cầu đề tài với quy cách thực tế của bộ dữ liệu âm thanh
- **Bảng 2.2:** Cấu trúc tổ chức lưu trữ tệp âm thanh và siêu dữ liệu trong hệ thống
- **Bảng 2.3:** So sánh đặc điểm âm học và cơ chế vật lý của 6 nhạc cụ bộ dây
- **Bảng 3.1:** Tổng quan bộ 58 đặc trưng nhận diện và truy vấn âm thanh
- **Bảng 3.2:** Công thức toán học và ý nghĩa âm học của các đặc trưng cốt lõi
- **Bảng 4.1:** Xếp hạng 15 đặc trưng âm học hàng đầu theo Fisher ratio
- **Bảng 4.2:** Các cặp đặc trưng có tương quan Pearson mạnh (|r| > 0,8)
- **Bảng 4.3:** So sánh hiệu năng phân loại và truy vấn giữa các nhóm đặc trưng (đơn vị: %)
- **Bảng A.1:** Số mẫu và kết quả truy vấn (P@1, P@5, mAP) theo từng nhạc cụ
- **Bảng A.2:** Thống kê mô tả 58 đặc trưng âm học (giá trị thô trên 600 tệp)

---

## DANH MỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT

| Thuật ngữ | Tên tiếng Anh đầy đủ | Ý nghĩa khoa học trong hệ thống |
| :--- | :--- | :--- |
| **ANOVA** | Analysis of Variance | Phân tích phương sai kiểm định sự khác biệt giữa các nhóm nhạc cụ |
| **CBAR** | Content-Based Audio Retrieval | Tìm kiếm và truy vấn dữ liệu âm thanh dựa trên nội dung đặc trưng |
| **CBIR** | Content-Based Image Retrieval | Tìm kiếm dữ liệu ảnh dựa trên nội dung |
| **CSDL** | Cơ sở dữ liệu | Hệ thống lưu trữ và quản lý dữ liệu có cấu trúc |
| **DFT / FFT** | (Fast) Discrete Fourier Transform | Biến đổi Fourier rời rạc (nhanh) chuyển tín hiệu từ miền thời gian sang tần số |
| **F0** | Fundamental Frequency | Tần số cơ bản quy định cao độ (Pitch) của nốt nhạc |
| **GLCM** | Gray-Level Co-occurrence Matrix | Ma trận đồng xuất mức xám mô tả kết cấu |
| **k-NN** | k-Nearest Neighbors | Thuật toán phân loại và tìm kiếm k láng giềng gần nhất |
| **MAP / mAP** | Mean Average Precision | Độ chính xác trung bình toàn cục của hệ thống truy vấn |
| **MFCC** | Mel-Frequency Cepstral Coefficients | Các hệ số phổ tần Mel mô tả bao phổ âm sắc sinh học của tai người |
| **MI** | Mutual Information | Thông tin tương hỗ phi tuyến giữa biến đặc trưng và nhãn lớp |
| **MIR** | Music Information Retrieval | Lĩnh vực khai phá và xử lý thông tin âm nhạc số |
| **P@k** | Precision at k | Tỷ lệ kết quả chính xác trong top k tệp âm thanh trả về |
| **PCM** | Pulse Code Modulation | Điều chế mã xung biểu diễn tín hiệu âm thanh số nguyên bản |
| **RMS** | Root Mean Square | Năng lượng hiệu dụng trung bình bình phương của sóng âm |
| **STFT** | Short-Time Fourier Transform | Biến đổi Fourier thời gian ngắn phân tích tín hiệu âm thanh theo từng khung |
| **ZCR** | Zero Crossing Rate | Tỷ lệ tín hiệu âm thanh cắt qua mức biên độ 0 |

---

## CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

### 1.1 Đặt vấn đề

Nhận diện và truy vấn âm thanh nhạc cụ là bài toán trung tâm trong lĩnh vực Khai phá Thông tin Âm nhạc (Music Information Retrieval - MIR) và Hệ cơ sở dữ liệu đa phương tiện. Trong thực tế, các kho lưu trữ âm nhạc số, phòng thu, thư viện tài nguyên sáng tạo và ứng dụng xử lý âm thanh phải quản lý hàng triệu bản ghi âm khác nhau. Phương pháp tra cứu truyền thống dựa trên siêu dữ liệu văn bản (như tên bài hát, nghệ sĩ biểu diễn hoặc thể loại) bộc lộ hạn chế nghiêm trọng khi người dùng chỉ sở hữu một đoạn âm thanh ngắn (chưa rõ nguồn gốc, không có nhãn văn bản) và mong muốn tìm kiếm các đoạn âm thanh phát ra từ cùng một loại nhạc cụ hoặc có âm sắc tương tự.

Bài toán vì vậy thuộc lớp **Tìm kiếm dữ liệu âm thanh dựa trên nội dung (Content-Based Audio Retrieval - CBAR)**. Khác với dữ liệu hình ảnh (vốn có cấu trúc không gian 2D tĩnh), dữ liệu âm thanh là tín hiệu thời gian một chiều biến thiên liên tục (1D time-series). Để máy tính có thể nhận thức và tính toán độ tương đồng giữa các âm thanh, tín hiệu sóng âm thô cần được phân rã thành các khung ngắn (framing), chuyển dịch sang miền tần số thông qua các phép biến đổi toán học và trích xuất thành một **vectơ đặc trưng số học (feature vector)** cố định. Độ tương đồng giữa âm thanh truy vấn và các bản ghi trong cơ sở dữ liệu sau đó được định lượng trực tiếp thông qua khoảng cách giữa các vectơ trong không gian đặc trưng đa chiều.

Trong các họ nhạc cụ truyền thống và hiện đại, **nhạc cụ bộ dây (string instruments)** giữ vai trò trụ cột trong cả dàn nhạc giao hưởng cổ điển lẫn các ban nhạc đương đại. Họ nhạc cụ này thể hiện phổ biến thiên âm học rất phong phú: từ âm vực siêu trầm của Double Bass đến dải cao vút của Violin; từ cơ chế kéo vĩ liên tục tạo rung ngân (arco) của Viola, Cello đến cơ chế gảy dây tắt dần (pizzicato) của Guitar Acoustic và Guitar Electric. Do đó, việc xây dựng một hệ thống CSDL lưu trữ và tìm kiếm âm thanh nhạc cụ bộ dây là một đề tài mang tính học thuật cao, đòi hỏi mô hình hóa chính xác các đặc trưng vật lý âm học.

### 1.2 Mục tiêu và phạm vi của báo cáo

Báo cáo số 1 tập trung giải quyết trọn vẹn hai nội dung nền tảng trong chu trình phát triển hệ thống CBAR: **Xây dựng bộ dữ liệu âm thanh chuẩn hóa** và **Thiết kế, trích xuất, đánh giá hệ thống đặc trưng âm học**.

Cụ thể, các mục tiêu chi tiết bao gồm:
1. **Xây dựng bộ dữ liệu âm thanh chuẩn hóa:** Thu thập, kiểm định chất lượng và tiền xử lý 600 bản ghi âm đơn nốt độc tấu thuộc 6 loại nhạc cụ bộ dây tiêu biểu (Violin, Viola, Cello, Double Bass, Guitar Acoustic, Guitar Electric), đảm bảo 100 tệp đồng nhất cho mỗi lớp.
2. **Chuẩn hóa quy cách tín hiệu số:** Toàn bộ dữ liệu được chuyển đổi đồng nhất về định dạng WAV PCM 16-bit, tần số lấy mẫu fs = 22.050 Hz, kênh đơn (mono), lọc bỏ hoàn toàn khoảng lặng đầu/cuối, cắt phân đoạn theo nốt và áp dụng hiệu ứng đường bao fade-in/fade-out để loại bỏ sốc pha (clipping).
3. **Phân tích đối chứng âm học:** So sánh tường minh các đặc điểm giống và khác nhau giữa 6 loại nhạc cụ; khảo cứu định lượng 7 cặp nhạc cụ có nguy cơ nhầm lẫn âm học cao để định hướng thiết kế bộ đặc trưng.
4. **Thiết kế hệ thống 58 đặc trưng âm học:** Bao quát toàn diện 3 khía cạnh vật lý: Năng lượng thời gian (RMS, ZCR), Cấu trúc phổ tần & âm sắc (Spectral Centroid, Rolloff, Bandwidth, Contrast, Flatness, 13 hệ số MFCC bậc 0-12) và Hòa âm cao độ (12 dải Chroma Pitch Class). Mỗi đặc trưng được tính cả giá trị trung bình (mean) và độ lệch chuẩn thời gian (std).
5. **Đánh giá giá trị thông tin định lượng:** Sử dụng các tiêu chuẩn toán học nghiêm ngặt (Fisher criterion, ANOVA F-statistic, Mutual Information, Pearson correlation) để phân tích khả năng phân biệt lớp, mức độ dư thừa và đóng góp thực tế của từng nhóm đặc trưng trong truy vấn láng giềng gần nhất (P@1, P@5, mAP).

### 1.3 Định hướng giải pháp

Hệ thống được thiết kế bám sát nguyên lý biểu diễn đa mức của tín hiệu âm học:
- **Biểu diễn miền thời gian:** Khai thác năng lượng RMS và tỷ lệ cắt qua điểm không ZCR để nắm bắt biên độ rung động, cường độ phát âm và sự khác biệt giữa nốt kéo vĩ liên tục với nốt gảy dây suy giảm theo hàm mũ.
- **Biểu diễn miền tần số và cảm thụ sinh học:** Tín hiệu được phân tích Fourier thời gian ngắn (STFT) với cửa sổ Hann 2048 mẫu (92,9 ms) và bước nhảy 512 mẫu (23,2 ms). Từ phổ biên độ, hệ thống trích xuất trọng tâm phổ (Spectral Centroid) đo độ sáng, tần số cuộn phổ (Spectral Rolloff) đo năng lượng dải cao và 13 hệ số Cepstral trên thang tần số Mel (MFCC). Thang Mel mô phỏng chính xác màng nhĩ tai người, giúp bắt trọn "dấu vân tay âm sắc" (timbre) của từng nhạc cụ.
- **Biểu diễn hòa âm (Chroma):** Phân rã năng lượng phổ thành 12 bán cung chuẩn trong thang âm bình quân (C, C#, D, ..., B), hỗ trợ phân biệt các nhạc cụ có dải âm vực và cấu trúc bồi âm đặc thù.
- **Chuẩn hóa z-score và đo khoảng cách Euclid:** Toàn bộ 58 thành phần đặc trưng được chuẩn hóa theo kỳ vọng và phương sai toàn cục, đảm bảo các đại lượng có thang đo vật lý khác nhau có trọng số cân bằng trong không gian Euclid.

### 1.4 Bố cục báo cáo

Nội dung báo cáo được tổ chức thành 5 chương chặt chẽ:
- **Chương 1:** Giới thiệu đề tài, tính cấp thiết, mục tiêu và định hướng giải pháp.
- **Chương 2:** Trình bày chi tiết quy trình xây dựng bộ dữ liệu 600 bản ghi âm thanh nhạc cụ bộ dây, quy cách kỹ thuật, các bước tiền xử lý tín hiệu, cấu trúc lưu trữ và phân tích so sánh đặc tính âm học (kèm 7 cặp đối chứng).
- **Chương 3:** Trình bày cơ sở toán học và cơ chế trích xuất của bộ 58 đặc trưng âm học, cấu trúc vectơ và hàm khoảng cách tương đồng.
- **Chương 4:** Kiểm định định lượng giá trị thông tin của các đặc trưng thông qua Fisher ratio, ANOVA F, Mutual Information, ma trận tương quan Pearson, phân bố khoảng cách nội lớp/liên lớp và thực nghiệm truy vấn minh họa.
- **Chương 5:** Tổng kết các kết quả đạt được, chỉ ra những hạn chế và vạch ra định hướng phát triển cho Báo cáo số 2 (xây dựng lược đồ CSDL và chỉ mục tìm kiếm).
- **Tài liệu tham khảo** và **Phụ lục** thống kê chi tiết toàn bộ dữ liệu thực nghiệm.

---

## CHƯƠNG 2. XÂY DỰNG BỘ DỮ LIỆU ÂM THANH NHẠC CỤ BỘ DÂY

### 2.1 Nguồn dữ liệu

Để xây dựng một cơ sở dữ liệu mẫu chuẩn phục vụ bài toán CBAR, nhóm đã tiến hành thu thập và tuyển chọn tín hiệu âm thanh từ ba kho dữ liệu âm nhạc học thuật uy tín hàng đầu:
1. **Philharmonia Orchestra Sound Sample Collection (London):** Bộ âm thanh mẫu độc tấu từng nốt chuẩn thính phòng của các nghệ sĩ giao hưởng London, ghi âm bằng micro phòng thu chất lượng cao không nhiễu tạp âm môi trường, đại diện cho Violin, Viola, Cello và Double Bass.
2. **MusicNet Open Dataset:** Tập dữ liệu 330 bản ghi hòa tấu và độc tấu cổ điển được gán nhãn thời gian nốt nhạc chính xác đến mức phần nghìn giây.
3. **Google Magenta NSynth Dataset:** Tập dữ liệu âm thanh tổng hợp và ghi âm nhạc cụ thực tế chất lượng cao, cung cấp các mẫu âm nốt đơn của Acoustic Guitar và Electric Guitar với đầy đủ các kỹ thuật bấm dây và pick gảy.

Từ các nguồn trên, nhóm đã trích lọc, kiểm duyệt âm thanh đơn âm sắc (solo note), loại bỏ các đoạn có tạp âm môi trường hoặc chồng âm quá phức tạp, thu được tập dữ liệu gồm **600 tệp âm thanh nguyên bản**, phân bố hoàn toàn đồng đều giữa 6 lớp nhạc cụ bộ dây (100 tệp/nhạc cụ).

### 2.2 Quy cách âm thanh trong bộ dữ liệu

Nhằm đảm bảo tính công bằng và loại bỏ hoàn toàn các yếu tố ngoại cảnh gây nhiễu trong quá trình so khớp đặc trưng, toàn bộ 600 tệp âm thanh được chuẩn hóa theo một quy cách kỹ thuật thống nhất.

*Bảng 2.1: Đối chiếu yêu cầu đề tài với quy cách thực tế của bộ dữ liệu âm thanh*

| Tiêu chuẩn kỹ thuật | Yêu cầu của đề tài CBAR | Quy cách chuẩn hóa thực tế | Ý nghĩa kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Định dạng tệp** | Không nén, bảo toàn sóng | **WAV (RIFF Header)** | Giữ nguyên dữ liệu sóng âm tuyến tính không qua thuật toán nén có tổn hao |
| **Mã hóa mẫu** | Chuẩn công nghiệp PCM | **Linear PCM 16-bit** | Dải động 96 dB, bảo toàn độ phân giải biên độ chi tiết của âm thanh |
| **Số kênh (Channels)** | Kênh đơn đồng nhất | **Mono (1 channel)** | Loại bỏ hiện tượng lệch pha giữa hai tai, giảm một nửa dung lượng lưu trữ |
| **Tần số lấy mẫu (fs)** | Đảm bảo tần số Nyquist | **22.050 Hz** | Đáp ứng tần số lên tới 11.025 Hz, bao phủ toàn bộ dải nghe của tai người đối với nhạc cụ bộ dây |
| **Thời lượng tệp** | Đồng đều, tập trung nốt | **2,0 - 3,0 giây / tệp** | Đủ dài để chứa trọn chu kỳ Attack-Decay-Sustain-Release của nốt nhạc |
| **Số lượng mẫu** | Tối thiểu 500 mẫu | **600 mẫu (100 mẫu/nhạc cụ)** | Cân bằng tuyệt đối giữa 6 lớp nhạc cụ bộ dây |

### 2.3 Quy trình tiền xử lý

Tín hiệu âm thanh thô khi thu thập thường chứa khoảng lặng không mong muốn ở đầu/cuối bản ghi, mức âm lượng chênh lệch do cự ly đặt micro và tiếng "click/pop" biên độ ở điểm cắt đột ngột. Nhóm đã xây dựng quy trình tiền xử lý 3 bước tự động bằng Python (`src/tao_bo_du_lieu.py`):

1. **Bước 1 – Lọc khoảng lặng (Silence Removal):**  
   Tính toán đường bao năng lượng hiệu dụng RMS trên từng khung trượt ngắn 20 ms. Xác định ngưỡng có tiếng (energy threshold) tại mức -35 dBFS so với đỉnh cực đại. Tất cả các đoạn mẫu ở đầu và cuối bản ghi có năng lượng dưới ngưỡng bị cắt bỏ hoàn toàn, chỉ giữ lại phần phát âm thực thụ của nhạc cụ.
2. **Bước 2 – Phân đoạn nốt đơn (Note Segmentation):**  
   Dò tìm đỉnh phát âm (onset detection) để xác định thời điểm bắt đầu nốt nhạc, trích xuất đoạn tín hiệu ổn định có độ dài chuẩn hóa trong khoảng 2,0 đến 3,0 giây, bao trọn pha phát âm chính và phần ngân đuôi.
3. **Bước 3 – Chuẩn hóa biên độ và làm mềm biên (Peak Normalization & Fade):**  
   Chuẩn hóa biên độ đỉnh của tín hiệu về mức -1 dBFS (A_norm = 0,891) để triệt tiêu chênh lệch âm lượng giữa các phòng thu. Áp dụng hàm làm mịn mượt mà (Fade-in 20 ms ở đầu và Fade-out 20 ms ở đuôi) để tránh hiện tượng cắt ngang pha sóng tạo ra tiếng nổ lách tách tần số cao.

![Hình 2.1: Quy trình 3 bước tiền xử lý tín hiệu âm thanh mẫu](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/2_1_quy_trinh_tien_xu_ly.png)  
*Hình 2.1: Quy trình 3 bước tiền xử lý tín hiệu âm thanh mẫu: (a) Xác định ngưỡng có tiếng và loại bỏ khoảng lặng; (b) Cắt phân đoạn theo nốt; (c) Chuẩn hóa biên độ đỉnh và áp dụng Fade-in / Fade-out 20ms.*

### 2.4 Tổ chức lưu trữ

Dữ liệu được tổ chức phân cấp khoa học trong thư mục dự án, cho phép truy xuất linh hoạt theo cả cấu trúc cây thư mục lẫn bảng siêu dữ liệu:

*Bảng 2.2: Cấu trúc tổ chức lưu trữ tệp âm thanh và siêu dữ liệu trong hệ thống*

| Đường dẫn / Tệp tin | Định dạng | Số lượng | Mô tả nội dung và vai trò trong hệ thống |
| :--- | :--- | :--- | :--- |
| `data/wav/violin/` | WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Violin (`violin_001.wav` – `violin_100.wav`) |
| `data/wav/viola/` | WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Viola (`viola_001.wav` – `viola_100.wav`) |
| `data/wav/cello/` | WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Cello (`cello_001.wav` – `cello_100.wav`) |
| `data/wav/double_bass/` | WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Double Bass (`double_bass_001.wav` – `double_bass_100.wav`) |
| `data/wav/guitar_acoustic/`| WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Guitar thùng (`guitar_acoustic_001.wav` – `...100.wav`) |
| `data/wav/guitar_electric/`| WAV | 100 tệp | Âm thanh nốt đơn chuẩn hóa của đàn Guitar điện (`guitar_electric_001.wav` – `...100.wav`) |
| `reports/metadata.csv` | CSV | 600 dòng | Bảng chỉ mục siêu dữ liệu: `file_id`, `file_name`, `instrument`, `duration`, `sample_rate`, `f0_hz` |
| `reports/tat_ca_dac_trung_600_file.csv` | CSV | 600 dòng | Ma trận 58 đặc trưng âm học đã trích xuất của toàn bộ 600 tệp |

### 2.5 Thống kê bộ dữ liệu

Bộ dữ liệu sau khi tiền xử lý có tổng dung lượng đĩa xấp xỉ 65 MB, bao gồm đúng **600 tệp âm thanh đơn kênh**. Tỷ lệ phân bố số lượng tệp theo từng lớp nhạc cụ đạt mức cân bằng lý tưởng 1:1:1:1:1:1 (100 tệp cho mỗi lớp), không xuất hiện hiện tượng mất cân bằng lớp gây sai lệch thuật toán truy vấn.

![Hình 2.2: Số lượng tệp âm thanh WAV của từng nhạc cụ](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/2_2_so_luong_mau.png)  
*Hình 2.2: Số lượng tệp âm thanh WAV của từng nhạc cụ; đường nét đứt đỏ biểu thị giá trị trung bình 100 tệp/nhạc cụ.*

Về mặt thời lượng, các tệp âm thanh dao động từ 2,05 giây đến 2,85 giây, giá trị trung bình là 2,34 giây (+- 0,18 giây). Dải tần số cơ bản F0 của các mẫu trải rộng từ 41,2 Hz (nốt E1 của Double Bass) đến 1.568 Hz (nốt G6 của Violin), đảm bảo độ bao phủ âm vực thực tế của dàn nhạc giao hưởng.

### 2.6 Đặc điểm giống và khác nhau giữa các nhạc cụ

Phân tích vật lý âm học và quan sát trực quan dạng sóng, phổ tần số (Spectrogram) của 6 loại nhạc cụ chỉ ra những đặc điểm giống nhau và các yếu tố phân biệt then chốt sau:

![Hình 2.3: Dạng sóng thời gian và phổ Spectrogram đại diện của 6 nhạc cụ bộ dây](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/1_song_va_spectrogram.png)  
*Hình 2.3: Dạng sóng thời gian (cột trái) và phổ Spectrogram (cột phải) đại diện của 6 nhạc cụ bộ dây.*

#### 2.6.1 Đặc điểm giống nhau
- **Bản chất nguồn kích âm:** Cả 6 nhạc cụ đều tạo ra âm thanh ban đầu từ sự dao động cơ học của dây đàn căng dưới sức kéo căng (dây kim loại, dây nylon hoặc ruột động vật). 
- **Cấu trúc phổ điều hòa (Harmonic Spectrum):** Khi một dây đàn dao động, sóng âm sinh ra không phải là sóng sin thuần khiết mà bao gồm một tần số cơ bản f0 (quy định cao độ) kèm theo một chuỗi các họa âm nguyên lần 2*f0, 3*f0, 4*f0... phân bố đều đặn trên trục tần số.
- **Biến thiên biên độ theo pha:** Đều tuân theo mô hình đường bao ADSR (Attack - Decay - Sustain - Release) của nhạc cụ acoustic, trong đó năng lượng tập trung mạnh nhất ở giai đoạn đầu và tiêu hao dần theo thời gian.

#### 2.6.2 Đặc điểm khác nhau
Sự khác biệt rõ rệt giữa các nhạc cụ bắt nguồn từ 3 nhân tố vật lý cơ bản: **Dải âm vực (kích thước thùng đàn và độ dài dây)**, **Cơ chế kích phát âm thanh (kéo vĩ liên tục vs gảy ngón)** và **Cơ chế khuếch đại cộng hưởng (thùng gỗ tự nhiên vs cảm ứng điện từ)**.

![Hình 2.4: Dải âm vực vật lý và tần số cơ bản F0](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/2_am_vuc_f0.png)  
*Hình 2.4: Biểu đồ dải âm vực vật lý và dải tần số cơ bản F0 đo đạc thực tế của 6 nhạc cụ bộ dây.*

*Bảng 2.3: So sánh đặc điểm âm học và cơ chế vật lý của 6 nhạc cụ bộ dây*

| Nhạc cụ | Cơ chế phát âm chính | Dải tần F0 đo đạc | Trọng tâm phổ (Centroid) | Đặc trưng bao biên độ & Âm sắc |
| :--- | :--- | :--- | :--- | :--- |
| **Violin** | Kéo vĩ (Arco) liên tục | 196 – 1.568 Hz (G3 – G6) | Rất cao (1.800 – 3.200 Hz) | Sóng răng cưa ổn định, sustain kéo dài, âm sắc sáng chói, năng lượng dải cao dồi dào |
| **Viola** | Kéo vĩ (Arco) liên tục | 130 – 880 Hz (C3 – A5) | Trung bình (1.200 – 2.100 Hz) | Âm thanh ấm, dày, độ cộng hưởng hộp gỗ trầm hơn violin, phổ ít hài bậc siêu cao |
| **Cello** | Kéo vĩ (Arco) liên tục | 65 – 440 Hz (C2 – A4) | Thấp - Trung (600 – 1.400 Hz) | Thùng đàn lớn, cộng hưởng dải trầm sâu lắng, họa âm trung phát triển mạnh mẽ |
| **Double Bass** | Kéo vĩ / Búng pizzicato | 41 – 220 Hz (E1 – A3) | Rất thấp (300 – 750 Hz) | Năng lượng tập trung cực đại dưới 300 Hz, thân đàn khổng lồ triệt tiêu các dải tần số cao |
| **Guitar Acoustic** | Gảy móng / Ngón tay | 82 – 659 Hz (E2 – E5) | Trung bình (1.100 – 2.400 Hz) | Attack cực nhanh (<15 ms), decay giảm dần theo hàm mũ, hộp đàn rỗng tạo tiếng vang mộc |
| **Guitar Electric** | Gảy phím qua pickup từ | 82 – 880 Hz (E2 – A5) | Biến thiên rộng (800 – 3.500 Hz)| Thân gỗ đặc (solid body), sustain kéo dài nhân tạo, chứa méo hài phi tuyến (distortion/drive) |

#### 2.6.3 Biến thiên trong cùng nhạc cụ và tương đồng giữa các nhạc cụ

Một thách thức lớn trong bài toán CBAR là hiện tượng **biến thiên nội lớp (intra-class variance)** và **tương đồng liên lớp (inter-class similarity)**. Trong cùng một loại nhạc cụ, khi người chơi thay đổi nốt nhạc từ thấp lên cao hoặc thay đổi cường độ gảy, trọng tâm phổ và năng lượng RMS có thể thay đổi gấp 3–4 lần. Ngược lại, giữa các nhạc cụ khác nhau lại tồn tại những vùng giao thoa âm học rất dễ gây nhầm lẫn.

Nhóm đã khảo sát chi tiết **7 cặp đối chứng âm học** có nguy cơ gây nhầm lẫn cao nhất trong hệ thống:

![Hình 2.5: So sánh phổ và dạng sóng giữa các cặp nhạc cụ đối chứng dễ nhầm lẫn](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/6_so_sanh_cac_cap_doi_chung.png)  
*Hình 2.5: So sánh dạng sóng thời gian và phổ tần số giữa 4 cặp nhạc cụ đối chứng tiêu biểu.*

1. **Cặp 1: Violin vs Viola (Giao thoa dải cao - trung):**  
   - *Điểm tương đồng:* Cùng sử dụng cây vĩ kéo (arco), cùng chất liệu dây và cấu tạo thùng đàn hình số 8. Ở dải nốt từ C4 đến G5 (261 – 784 Hz), cả hai đều phát ra sóng dạng răng cưa có độ ổn định rất cao.
   - *Điểm phân biệt:* Thùng đàn Viola lớn hơn 15–20% so với Violin, thể tích không khí bên trong lớn hơn làm dịch chuyển tần số cộng hưởng Helmholtz xuống thấp. Giá trị đo đạc thực tế: `centroid_mean` của Violin trung bình đạt 2.450 Hz, trong khi Viola chỉ đạt 1.620 Hz; hệ số `mfcc_1_mean` của Violin cao hơn Viola 38 dB.
2. **Cặp 2: Cello vs Double Bass (Giao thoa dải âm trầm):**  
   - *Điểm tương đồng:* Cùng là nhạc cụ vĩ kéo cỡ lớn đặt đứng trên sàn, tạo ra các nốt trầm ngân vang, dải F0 giao thoa ở quãng C2 – E3.
   - *Điểm phân biệt:* Double Bass có dải tần chạm đáy 41,2 Hz với họa âm cơ bản áp đảo; `rolloff_mean` của Double Bass chỉ nằm ở mức 720 Hz, trong khi Cello có dải họa âm mở rộng lên tới 2.200 Hz (`rolloff_mean` trung bình 1.850 Hz).
3. **Cặp 3: Guitar Acoustic vs Guitar Electric (Giao thoa cùng dải âm vực F0):**  
   - *Điểm tương đồng:* Cùng chung cấu trúc 6 dây tiêu chuẩn (E2-A2-D3-G3-B3-E4) và kỹ thuật gảy nốt đơn.
   - *Điểm phân biệt:* Guitar Acoustic có pha suy giảm (decay) nhanh do năng lượng truyền trực tiếp vào mặt gỗ phát tán ra không khí; Guitar Electric có thân gỗ đặc, cuộn cảm ứng từ (pickup) giữ dây rung lâu hơn, dẫn đến năng lượng `rms_std` ổn định hơn và dải tần cao sắc bén hơn hẳn.
4. **Cặp 4: Viola vs Cello (Giao thoa quãng trung - trầm):**  
   - *Điểm tương đồng:* Âm sắc ấm áp, giàu cảm xúc, dải nốt từ C3 đến C4 hoàn toàn trùng khớp.
   - *Điểm phân biệt:* Dây đàn Cello dài và nặng hơn nhiều, thời gian khởi phát nốt (attack time) chậm hơn Viola khoảng 30–45 ms; năng lượng dải tần dưới 200 Hz của Cello chiếm trên 40% tổng công suất.
5. **Cặp 5: Violin vs Guitar Acoustic (Khác biệt cơ chế kéo vĩ vs gảy phím):**  
   - *Điểm tương đồng:* Đều là nhạc cụ acoustic thùng gỗ phát ra âm thanh sáng chói ở dải tần số 1.000 – 3.000 Hz.
   - *Điểm phân biệt:* Tỷ lệ qua điểm không (`zcr_mean`) và độ ổn định năng lượng `rms_mean` của Violin vượt trội so với Guitar Acoustic (tiếng gảy tắt dần sau 0,5 giây).
6. **Cặp 6: Cello vs Guitar Acoustic (Cùng dải trung nhưng khác bao biên độ):**  
   - *Điểm phân biệt:* Cello giữ vững biên độ sóng trong suốt 2 giây kéo vĩ (`rms_std` nhỏ), trong khi Guitar Acoustic đạt đỉnh tức thì rồi rơi tự do theo đường hàm mũ (`rms_std` lớn, độ lệch biên độ cao).
7. **Cặp 7: Violin vs Guitar Electric (Dải cao chói sáng):**  
   - *Điểm tương đồng:* Cả hai đều có năng lượng dải cao rất mạnh, âm sắc sắc nét.
   - *Điểm phân biệt:* Phổ của Guitar Electric chứa các họa âm méo bậc chẵn/lẻ do mạch khuếch đại bán dẫn, thể hiện qua các giá trị MFCC bậc cao (`mfcc_5` đến `mfcc_12`) có phương sai biến động gấp 2,5 lần so với Violin mộc.

**Kết luận Chương 2:**  
Phân tích thực nghiệm trên 600 tệp âm thanh chỉ ra rằng: một đặc trưng đơn lẻ hoàn toàn bất khả thi trong việc phân tách 6 loại nhạc cụ bộ dây. Hệ thống bắt buộc phải tích hợp một **bộ đặc trưng đa chiều**, kết hợp chặt chẽ giữa hình dạng bao biên độ thời gian, năng lượng dải tần số và cấu trúc âm sắc Mel để đạt độ chính xác tối ưu.

---

## CHƯƠNG 3. BỘ ĐẶC TRƯNG NHẬN DIỆN VÀ TRUY VẤN ÂM THANH

### 3.1 Tổng quan bộ đặc trưng

Để mô tả toàn diện "vân tay âm thanh" của từng bản ghi, nhóm đã thiết kế bộ đặc trưng gồm **58 chiều số thực** trích xuất từ 3 nhóm thuộc tính vật lý âm học bổ trợ lẫn nhau:
- **Nhóm 1: Năng lượng và Biến thiên Thời gian (4 đặc trưng):** Mô tả độ mạnh yếu và sự thay đổi biên độ rung động của dây đàn.
- **Nhóm 2: Cấu trúc Phổ tần số và Âm sắc Mel (30 đặc trưng):** Mô tả độ sáng, độ cuộn phổ và hình dạng bao phổ sinh học đặc trưng cho chất liệu thùng đàn và cơ chế phát âm.
- **Nhóm 3: Hòa âm và Phân bố Bán cung Chroma (24 đặc trưng):** Mô tả phân bố năng lượng theo 12 nốt nhạc trong thang âm bình quân.

Tín hiệu âm thanh liên tục x(t) được số hóa thành chuỗi rời rạc x[n] ở tần số fs = 22.050 Hz. Nhằm nắm bắt tính chất phi dừng (non-stationary) của âm thanh, quá trình trích xuất áp dụng kỹ thuật cửa sổ trượt phân khung (Short-Time Analysis):
- Độ dài khung phân tích: N = 2048 mẫu (xấp xỉ 92,9 ms).
- Độ dịch chuyển bước nhảy: H = 512 mẫu (xấp xỉ 23,2 ms, độ chồng lấp 75%).
- Cửa sổ trọng số: Cửa sổ Hann w[m] = 0,5 - 0,5 * cos(2*pi*m / (N-1)) nhằm triệt tiêu hiện tượng rò rỉ phổ (spectral leakage).

![Hình 3.1: Quy trình tổng thể trích xuất vectơ 58 đặc trưng âm học](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/7_quy_trinh_trich_xuat_dac_trung.png)  
*Hình 3.1: Quy trình tổng thể trích xuất vectơ 58 đặc trưng âm học từ tín hiệu âm thanh.*

*Bảng 3.1: Tổng quan bộ 58 đặc trưng nhận diện và truy vấn âm thanh*

| Nhóm đặc trưng | Số chiều | Danh sách các đặc trưng chi tiết | Cơ chế toán học & Vai trò nhận diện |
| :--- | :--- | :--- | :--- |
| **I. Thời gian & Năng lượng** | 4 chiều | `rms_mean`, `rms_std`, `zcr_mean`, `zcr_std` | Đo biên độ sóng hiệu dụng và tốc độ dao động cơ học; phân tách rõ nốt kéo vĩ liên tục với nốt gảy móng |
| **II. Phổ tần số cơ bản** | 4 chiều | `centroid_mean`, `centroid_std`, `rolloff_mean`, `rolloff_std` | Đo trọng tâm dải tần và ngưỡng tích lũy 85% năng lượng phổ; phân biệt nhạc cụ trầm (Double Bass) với nhạc cụ cao (Violin) |
| **III. Âm sắc Mel (MFCC)** | 26 chiều | `mfcc_0_mean` .. `mfcc_12_mean` (13 chiều), `mfcc_0_std` .. `mfcc_12_std` (13 chiều) | Bắt trọn hình thái bao phổ âm thanh mô phỏng thính giác người; là trụ cột phân biệt chất liệu âm sắc nhạc cụ |
| **IV. Hòa âm (Chroma STFT)** | 24 chiều | `chroma_0_mean` .. `chroma_11_mean` (12 chiều), `chroma_0_std` .. `chroma_11_std` (12 chiều) | Đo mức tập trung năng lượng vào 12 bán cung âm nhạc; nhận diện cấu trúc hòa âm và cao độ đặc trưng |

### 3.2 Nhóm đặc trưng thời gian và năng lượng

1. **Năng lượng hiệu dụng trung bình bình phương (Root Mean Square - RMS):**  
   Được tính toán trên từng khung thời gian thứ t:
   RMS[t] = sqrt( (1/N) * sum_{n=0}^{N-1} (x_t[n])^2 )
   *Ý nghĩa vật lý:* Phản ánh cường độ năng lượng thực tế của sóng âm. Ở đàn Violin và Cello, RMS[t] duy trì ổn định ở mức cao trong suốt thời gian kéo vĩ (`rms_std` nhỏ); ngược lại ở Guitar Acoustic, RMS[t] bùng nổ tức thì ở giai đoạn gảy rồi suy giảm nhanh chóng (`rms_std` lớn).

2. **Tỷ lệ cắt qua điểm không (Zero Crossing Rate - ZCR):**  
   Đo số lần tín hiệu đổi dấu biên độ từ dương sang âm hoặc ngược lại trong một khung thời gian:
   ZCR[t] = (1 / (2*(N-1))) * sum_{n=1}^{N-1} |sgn(x_t[n]) - sgn(x_t[n-1])|
   *Ý nghĩa vật lý:* ZCR phản ánh tần số dao động chiếm ưu thế trong miền thời gian mà không cần biến đổi Fourier. Nhạc cụ âm cao như Violin có ZCR trung bình đạt 0,085 - 0,140, trong khi Double Bass có ZCR rất thấp (0,015 - 0,035).

### 3.3 Nhóm đặc trưng phổ tần và âm sắc

Tín hiệu từng khung x_t[n] được biến đổi Fourier thời gian ngắn sang miền tần số:
X_t[k] = sum_{n=0}^{N-1} x_t[n] * w[n] * exp(-j * 2 * pi * k * n / N), k = 0, 1, ..., N/2
Phổ biên độ công suất tại tần số f_k = (k * fs) / N là S_t[k] = |X_t[k]|^2.

![Hình 3.2: Chi tiết cơ chế trích xuất của từng nhóm đặc trưng](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/8_chi_tiet_trich_xuat_3_bo_dac_trung.png)  
*Hình 3.2: Chi tiết cơ chế trích xuất của từng nhóm đặc trưng (Khung Hann, Phổ STFT, Ngưỡng Rolloff 85%, Bộ lọc Mel và Bộ lọc Chroma).*

1. **Trọng tâm phổ (Spectral Centroid):**  
   Xác định "trọng tâm" phân bố công suất của phổ tần số:
   C[t] = sum_{k=0}^{N/2} (f_k * |X_t[k]|) / sum_{k=0}^{N/2} |X_t[k]|
   *Ý nghĩa vật lý:* Đo độ sáng (brightness) của âm thanh. Âm thanh càng chói, sắc bén thì trọng tâm phổ càng lệch về phía tần số cao.
2. **Tần số cuộn phổ (Spectral Rolloff 85%):**  
   Là tần số R[t] mà tại đó tổng năng lượng từ 0 Hz đến R[t] chiếm đúng 85% tổng năng lượng toàn khung:
   sum_{k=0}^{k_ro} |X_t[k]|^2 = 0,85 * sum_{k=0}^{N/2} |X_t[k]|^2, R[t] = (k_ro * fs) / N
   *Ý nghĩa vật lý:* Giúp phân tách chính xác giới hạn băng thông năng lượng thực sự của nhạc cụ, loại bỏ ảnh hưởng của nhiễu nền tần số siêu cao.
3. **Các hệ số phổ tần số Mel (MFCC - Mel-Frequency Cepstral Coefficients):**  
   Phổ công suất được nén qua ngân hàng gồm 40 bộ lọc tam giác cách đều trên thang đo Mel mô phỏng thính giác người:
   m = 2595 * log10(1 + f / 700)
   Lấy logarit năng lượng đầu ra của từng bộ lọc Mel E_m[t] rồi áp dụng phép biến đổi Cosine rời rạc (DCT-II):
   c_i[t] = sum_{m=1}^{M} log(E_m[t]) * cos( (pi * i / M) * (m - 0,5) ), i = 0, 1, ..., 12
   - c_0: Năng lượng tổng thể của khung âm thanh.
   - c_1: Đo độ dốc phổ (cân bằng năng lượng giữa dải trầm và dải bổng).
   - c_2: Đo độ cong dạng vòm của phổ tần số.
   - c_3 - c_{12}: Nắm bắt các rãnh cộng hưởng chi tiết của hộp đàn gỗ.

*Bảng 3.2: Công thức toán học và ý nghĩa âm học của các đặc trưng cốt lõi*

| Đặc trưng | Công thức toán học định nghĩa | Ý nghĩa vật lý âm học |
| :--- | :--- | :--- |
| **`rms_mean`** | mu_RMS = (1/T) * sum_{t=1}^T RMS[t] | Cường độ phát âm trung bình toàn bản ghi |
| **`rms_std`** | sigma_RMS = sqrt( (1/T) * sum_{t=1}^T (RMS[t] - mu_RMS)^2 ) | Độ biến thiên bao năng lượng (rất lớn ở Guitar, rất nhỏ ở Violin) |
| **`zcr_mean`** | mu_ZCR = (1/T) * sum_{t=1}^T ZCR[t] | Tốc độ cắt 0 trung bình (đại diện cho cao độ miền thời gian) |
| **`centroid_mean`** | mu_Cent = (1/T) * sum_{t=1}^T C[t] | Độ sáng trung bình của âm sắc (đo bằng Hz) |
| **`rolloff_mean`** | mu_Roll = (1/T) * sum_{t=1}^T R[t] | Giới hạn tần số bao chứa 85% tổng năng lượng sóng |
| **`mfcc_1_mean`** | mu_MFCC1 = (1/T) * sum_{t=1}^T c_1[t] | Cân bằng năng lượng âm trầm và âm bổng |
| **`mfcc_2_mean`** | mu_MFCC2 = (1/T) * sum_{t=1}^T c_2[t] | Mức độ tập trung năng lượng ở dải trung âm |

### 3.4 Nhóm đặc trưng cao độ và hòa âm

Đặc trưng **Chroma STFT (Pitch Class Profile)** chiếu toàn bộ năng lượng phổ tần số vào 12 ngăn tương ứng với 12 bán cung chuẩn trong thang âm phương Tây (C, C#, D, D#, E, F, F#, G, G#, A, A#, B):
Chroma(b) = sum_{k: f_k in PitchClass(b)} |X[k]|^2, b in {0, 1, ..., 11}
Do các nhạc cụ dây đều có dải dây buông chuẩn (ví dụ Violin: G3-D4-A4-E5; Cello: C2-G2-D3-A3; Guitar: E2-A2-D3-G3-B3-E4), năng lượng Chroma phản ánh trực tiếp cấu trúc điều hòa và dây rung đặc thù của từng nhạc cụ.

### 3.5 Biểu diễn vectơ và độ đo tương đồng

Mỗi tệp âm thanh trong cơ sở dữ liệu được nén thành một vectơ đặc trưng 58 chiều:
x = [ mu_RMS, sigma_RMS, mu_ZCR, sigma_ZCR, ..., mu_Chroma11, sigma_Chroma11 ]^T in R^58

Do các đặc trưng có thang đo vật lý hoàn toàn khác biệt (ví dụ `centroid_mean` có giá trị từ 300 đến 3.500 Hz, trong khi `zcr_mean` chỉ dao động từ 0,01 đến 0,20), nếu tính khoảng cách trực tiếp trên giá trị thô, các đại lượng có biên độ lớn sẽ chi phối hoàn toàn kết quả tìm kiếm. Do đó, toàn bộ 58 thành phần đặc trưng được **chuẩn hóa z-score** theo kỳ vọng mu_j và độ lệch chuẩn sigma_j tính trên toàn bộ 600 tệp trong CSDL:
z_j = (x_j - mu_j) / sigma_j, j = 1, 2, ..., 58

Độ tương đồng giữa tệp âm thanh truy vấn q và tệp âm thanh ứng viên x trong cơ sở dữ liệu được định lượng bằng khoảng cách Euclid trên không gian đặc trưng đã chuẩn hóa:
d(q, x) = ||z_q - z_x||_2 = sqrt( sum_{j=1}^{58} (z_j^(q) - z_j^(x))^2 )

Cách biểu diễn này đáp ứng trọn vẹn cả hai yêu cầu cốt lõi của đề tài:
1. **Tìm kiếm sự tương đồng:** Ứng với việc xác định các tệp âm thanh có khoảng cách Euclid d(q, x) nhỏ nhất trong toàn bộ cơ sở dữ liệu (thuật toán Nearest Neighbor).
2. **Tìm kiếm và giải thích sự khác biệt:** Ứng với việc truy vết các thành phần có sai khác lớn nhất |z_j^(q) - z_j^(x)|, từ đó lý giải chính xác thuộc tính âm học nào (độ sáng, năng lượng kéo vĩ hay âm sắc Mel) tạo nên sự khác biệt giữa hai bản ghi.

**Kết luận Chương 3:**  
Chương này đã thiết lập nền tảng toán học và kỹ thuật hoàn chỉnh cho bộ 58 đặc trưng âm học. Mọi đặc trưng đều được chuẩn hóa z-score để cân bằng trọng số. Tuy nhiên, giá trị thông tin và mức độ đóng góp của từng đặc trưng đến thời điểm này mới dừng lại ở mức lập luận lý thuyết; Chương 4 sẽ tiến hành kiểm định định lượng chi tiết trên bộ dữ liệu thực tế.

---

## CHƯƠNG 4. ĐÁNH GIÁ GIÁ TRỊ THÔNG TIN CỦA ĐẶC TRƯNG

Chương này tiến hành kiểm định thực nghiệm định lượng trên toàn bộ 600 tệp âm thanh chuẩn hóa nhằm trả lời 5 câu hỏi then chốt:
1. Từng đặc trưng âm học có khả năng phân biệt 6 loại nhạc cụ tốt đến mức nào?
2. Có hiện tượng dư thừa thông tin hoặc tương quan đa tuyến tính giữa các đặc trưng hay không?
3. Vectơ đặc trưng chuẩn hóa có thực sự gom các âm thanh cùng nhạc cụ lại gần nhau và tách biệt các nhạc cụ khác nhau hay không?
4. Mỗi nhóm đặc trưng (Thời gian, Phổ, MFCC, Chroma) đóng góp bao nhiêu phần trăm vào độ chính xác truy vấn?
5. Kết quả truy vấn thực tế trên các ca mẫu thể hiện như thế nào?

### 4.1 Phương pháp đánh giá

#### 4.1.1 Đánh giá từng đặc trưng
Khả năng phân biệt của từng đặc trưng được lượng hóa qua ba chỉ số độc lập:
1. **Tỷ số phân tách Fisher (Fisher Criterion / Fisher Ratio):**
   J = S_B / S_W = ( sum_{c=1}^C N_c * (mu_c - mu)^2 ) / ( sum_{c=1}^C sum_{i in c} (x_i - mu_c)^2 )
   Trong đó C = 6 lớp nhạc cụ, N_c = 100 tệp/lớp, mu_c là trung bình của lớp c và mu là trung bình toàn cục. Giá trị J càng cao chứng tỏ phương sai giữa các lớp càng lớn so với phương sai nội bộ lớp, nghĩa là đặc trưng phân biệt càng tốt.
2. **Thống kê kiểm định ANOVA F (F-statistic):**
   F = (S_B / (C - 1)) / (S_W / (N - C))
   Đo mức ý nghĩa thống kê của sự sai khác kỳ vọng giữa các lớp nhạc cụ.
3. **Thông tin tương hỗ (Mutual Information - MI):**
   I(X; Y) đo lường mức độ phụ thuộc phi tuyến giữa đặc trưng liên tục X và nhãn rời rạc Y (ước lượng theo thuật toán láng giềng k-NN). Khác với Fisher ratio vốn giả định phân bố chuẩn, MI nhạy bén với mọi dạng phân bố dữ liệu phức tạp.

#### 4.1.2 Đánh giá theo nhóm đặc trưng
Hiệu năng truy vấn của từng nhóm đặc trưng được đánh giá thông qua quy trình kiểm định chéo loại-một (Leave-One-Out Cross-Validation): mỗi tệp âm thanh trong số 600 tệp lần lượt đóng vai trò là mẫu truy vấn q, hệ thống so khớp khoảng cách với 599 tệp còn lại và xếp hạng kết quả:
- **Precision at 1 (P@1 / Accuracy):** Tỷ lệ tệp gần nhất (Top 1) có cùng nhãn nhạc cụ với tệp truy vấn.
- **Precision at 5 (P@5):** Tỷ lệ các tệp đúng nhãn trong top 5 kết quả trả về.
- **Mean Average Precision (mAP):** Độ chính xác trung bình toàn cục có tính đến thứ tự xếp hạng của toàn bộ 99 tệp cùng lớp:
  mAP = (1/600) * sum_{q=1}^{600} AP(q)

### 4.2 Khả năng phân biệt của từng đặc trưng

Bảng 4.1 và Hình 4.1 trình bày kết quả xếp hạng 15 đặc trưng hàng đầu theo Fisher ratio và Mutual Information.

![Hình 4.1: Fisher ratio và Thông tin tương hỗ của 15 đặc trưng hàng đầu](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/4_1_fisher_va_mi.png)  
*Hình 4.1: Fisher ratio (trái) và Thông tin tương hỗ MI (phải) của 15 đặc trưng hàng đầu.*

*Bảng 4.1: Xếp hạng 15 đặc trưng âm học hàng đầu theo Fisher ratio*

| Hạng | Tên đặc trưng | Nhóm thuộc tính | Fisher ratio (J) | ANOVA F | MI (nat) | Ý nghĩa phân tách thực tế |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | `mfcc_1_mean` | Âm sắc Mel | **385,08** | 385,08 | 0,760 | Phân tách cực mạnh dải trầm (Double Bass) và dải bổng (Violin) |
| **2** | `mfcc_2_mean` | Âm sắc Mel | **359,42** | 359,42 | 0,607 | Nắm bắt độ cong phổ tần dải trung âm |
| **3** | `mfcc_4_mean` | Âm sắc Mel | **321,67** | 321,67 | 0,737 | Bắt trọn rãnh cộng hưởng hộp đàn thùng gỗ |
| **4** | `centroid_mean`| Phổ tần số | **307,48** | 307,48 | **0,813** | Đạt MI cao nhất toàn bộ dữ liệu; đo độ sáng trực tiếp |
| **5** | `rolloff_mean` | Phổ tần số | **295,42** | 295,42 | 0,803 | Giới hạn băng thông năng lượng 85% |
| **6** | `rolloff_std`  | Phổ tần số | **224,98** | 224,98 | 0,632 | Độ biến thiên dải cao qua các nốt nhạc |
| **7** | `mfcc_0_mean` | Âm sắc Mel | **210,60** | 210,60 | 0,482 | Năng lượng công suất tổng thể |
| **8** | `zcr_mean`     | Thời gian & Năng lượng | **201,35** | 201,35 | 0,699 | Tần số dao động miền thời gian |
| **9** | `mfcc_3_mean` | Âm sắc Mel | **174,96** | 174,96 | 0,592 | Đặc trưng âm sắc bậc 3 |
| **10**| `centroid_std` | Phổ tần số | **143,96** | 143,96 | 0,525 | Độ dao động độ sáng âm thanh |
| **11**| `mfcc_12_std`  | Âm sắc Mel | **140,50** | 140,50 | 0,353 | Độ biến thiên vi cấu trúc hài cao |
| **12**| `mfcc_10_mean` | Âm sắc Mel | **97,40** | 97,40 | 0,512 | Cấu trúc họa âm bậc 10 |
| **13**| `mfcc_6_mean`  | Âm sắc Mel | **96,33** | 96,33 | 0,407 | Cấu trúc họa âm bậc 6 |
| **14**| `mfcc_11_std`  | Âm sắc Mel | **95,12** | 95,12 | 0,311 | Độ biến động họa âm bậc 11 |
| **15**| `rms_std`      | Thời gian & Năng lượng | **92,84** | 92,84 | 0,387 | Phân tách nốt kéo vĩ mượt với nốt gảy tắt dần |

Ba kết luận quan trọng rút ra từ kết quả thực nghiệm:
1. **Sự thống trị của các hệ số MFCC bậc thấp:** `mfcc_1_mean`, `mfcc_2_mean` và `mfcc_4_mean` chiếm trọn 3 vị trí dẫn đầu với Fisher ratio vượt trội (>320). Điều này khẳng định bao phổ âm sắc Mel là yếu tố phân biệt mạnh nhất giữa các cấu trúc nhạc cụ.
2. **`centroid_mean` đạt giá trị Thông tin tương hỗ cao nhất (0,813 nat):** Trọng tâm phổ trực tiếp phản ánh độ sáng và âm vực vật lý của nhạc cụ, tạo nên ranh giới phân biệt rất dứt khoát giữa các họ dây.
3. **Đặc trưng thời gian đóng vai trò chốt chặn:** Mặc dù `rms_std` có Fisher ratio khiêm tốn hơn (92,84), nhưng nó mang thông tin độc lập hoàn toàn với phổ tần, đóng vai trò quyết định trong việc nhận diện bản chất kéo vĩ hay gảy phím.

![Hình 4.2: Phân bố theo nhạc cụ của 4 đặc trưng có Fisher ratio cao nhất](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/4_2_phan_bo_top_dac_trung.png)  
*Hình 4.2: Phân bố dạng hộp (boxplot) theo 6 loại nhạc cụ của 4 đặc trưng có Fisher ratio cao nhất.*

Quan sát Hình 4.2 cho thấy phân bố các giá trị của 4 đặc trưng hàng đầu tách biệt rất rõ rệt giữa các lớp: Double Bass tập trung ở đáy dải giá trị, Cello và Viola nằm ở khoảng giữa, trong khi Violin và Guitar vươn lên đỉnh cao.

### 4.3 Tương quan và dư thừa giữa các đặc trưng

Hình 4.3 trình bày ma trận tương quan Pearson (r) giữa các đặc trưng cốt lõi đại diện cho các nhóm thuộc tính.

![Hình 4.3: Ma trận tương quan Pearson giữa các đặc trưng](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/4_3_ma_tran_tuong_quan.png)  
*Hình 4.3: Ma trận tương quan Pearson giữa các đặc trưng với phân vùng theo nhóm thuộc tính.*

*Bảng 4.2: Các cặp đặc trưng có tương quan Pearson mạnh (|r| > 0,8)*

| Đặc trưng 1 | Đặc trưng 2 | Hệ số tương quan r | Nhóm thuộc tính | Bản chất vật lý của sự tương quan |
| :--- | :--- | :---: | :--- | :--- |
| `centroid_mean` | `rolloff_mean` | **+0,9803** | Phổ tần số | Cùng phản ánh độ tập trung năng lượng dải tần số cao |
| `centroid_std` | `rolloff_std` | **+0,9452** | Phổ tần số | Độ biến động của độ sáng tỷ lệ thuận với biến động giới hạn phổ |
| `zcr_mean` | `centroid_mean` | **+0,9110** | Thời gian vs Phổ | Tốc độ cắt trục 0 liên hệ trực tiếp với tần số chiếm ưu thế |
| `zcr_mean` | `rolloff_mean` | **+0,8285** | Thời gian vs Phổ | Tần số cắt 0 cao đi kèm dải cuộn phổ rộng |
| `mfcc_11_std` | `mfcc_12_std` | **+0,8223** | Âm sắc Mel | Hai hệ số cepstral bậc cao liền kề mô tả vi nhiễu tần số |
| `mfcc_0_mean` | `mfcc_2_mean` | **-0,8106** | Âm sắc Mel | Tương quan nghịch giữa năng lượng tổng và độ cong phổ |

Kết quả chỉ ra rằng chỉ có 6 cặp đặc trưng có tương quan mạnh vượt ngưỡng 0,8. Đặc biệt, giữa nhóm Thời gian/Năng lượng và nhóm Âm sắc MFCC, hay giữa nhóm Chroma và nhóm Phổ tần số hầu như không có cặp nào có |r| > 0,6. Điều này chứng minh 4 nhóm đặc trưng mang thông tin bổ trợ độc lập rất cao, không gây lãng phí tài nguyên tính toán.

### 4.4 Khoảng cách giữa các mẫu cùng loại và khác loại

Một bộ đặc trưng được coi là phân biệt tốt nếu và chỉ nếu khoảng cách giữa các mẫu cùng loại (intra-class distance) nhỏ hơn đáng kể so với khoảng cách giữa các mẫu khác loại (inter-class distance).

Hình 4.4 biểu diễn phân bố xác suất khoảng cách Euclid của **29.700 cặp tệp cùng nhạc cụ** và **150.000 cặp tệp khác nhạc cụ** tính trên không gian 58 chiều chuẩn hóa.

![Hình 4.4: Phân bố khoảng cách giữa các cặp âm thanh cùng loại và khác loại](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/4_4_khoang_cach_cung_va_khac_loai.png)  
*Hình 4.4: Phân bố khoảng cách Euclid giữa các cặp âm thanh cùng loại (xanh dương) và khác loại (đỏ); đường nét đứt biểu thị giá trị trung vị.*

Các chỉ số thống kê đo đạc định lượng:
- **Cặp cùng nhạc cụ (Intra-class):** Khoảng cách trung bình đạt **8,68** (+- 2,59), trung vị đạt **8,24**.
- **Cặp khác nhạc cụ (Inter-class):** Khoảng cách trung bình đạt **10,83** (+- 2,36), trung vị đạt **10,65**.
- **Mức độ tách biệt:** Trung vị của phân bố liên lớp dịch chuyển sang phải **2,41 đơn vị khoảng cách** so với trung vị nội lớp. Vùng giao thoa (overlap) giữa hai phân bố tương đối hẹp, khẳng định không gian đặc trưng 58 chiều có khả năng co cụm các âm thanh cùng loại và phân tách rõ rệt các nhạc cụ khác biệt.

### 4.5 Đóng góp của từng nhóm đặc trưng

Để đánh giá mức độ đóng góp thực tế của từng nhóm thuộc tính vào bài toán truy vấn CBAR, nhóm đã tiến hành thực nghiệm so sánh độc lập giữa 5 tập đặc trưng bằng phương pháp Leave-One-Out trên toàn bộ 600 tệp.

*Bảng 4.3: So sánh hiệu năng phân loại và truy vấn giữa các nhóm đặc trưng (đơn vị: %)*

| Tập đặc trưng thực nghiệm | Số chiều | P@1 (Accuracy) | P@5 | mAP | Nhận xét vai trò |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. Chỉ dùng Thời gian & Năng lượng** | 4 | 65,67% | 59,43% | 42,76% | Phân biệt cơ bản giữa nốt kéo vĩ và nốt gảy |
| **2. Chỉ dùng Phổ tần số cơ bản** | 4 | 79,33% | 73,63% | 55,88% | Phân tách tốt theo cao độ và độ sáng âm sắc |
| **3. Chỉ dùng Âm sắc Mel (MFCC)** | 26 | **96,83%** | **92,87%** | **63,07%** | Đạt hiệu năng truy vấn cá lẻ cao nhất |
| **4. Chỉ dùng Hòa âm (Chroma STFT)** | 24 | 65,67% | 55,43% | 29,92% | Hiệu năng đơn lẻ thấp do phụ thuộc nốt nhạc |
| **5. Kết hợp toàn bộ (Full Vector)** | **58** | **93,00%** | **88,47%** | **58,63%** | Cung cấp biểu diễn đa diện toàn diện nhất |

Phân tích chuyên sâu kết quả:
- **Nhóm MFCC là trụ cột mạnh nhất:** Chỉ với 26 hệ số MFCC, hệ thống đạt độ chính xác P@1 lên tới 96,83% và mAP đạt 63,07%. Điều này một lần nữa khẳng định hình dạng bao phổ Mel là thuộc tính then chốt định danh nhạc cụ.
- **Vai trò của tập kết hợp 58 chiều:** Mặc dù nhóm MFCC đơn lẻ đạt kết quả rất cao, việc kết hợp toàn bộ 58 đặc trưng giúp hệ thống đạt độ ổn định toàn diện: P@1 đạt **93,00%** (558/600 tệp tìm thấy đúng nhạc cụ ở vị trí Top 1), P@5 đạt **88,47%** và mAP đạt **58,63%**. Tập kết hợp không chỉ giúp tìm kiếm theo âm sắc mà còn lưu giữ đầy đủ thông tin về cao độ Chroma và bao năng lượng thời gian, phục vụ các bài toán lọc truy vấn nâng cao trong các giai đoạn tiếp theo.

### 4.6 Kết quả truy vấn minh họa

Hình 4.5 minh họa kết quả truy vấn thực tế của hệ thống trên 3 tệp âm thanh đại diện cho 3 họ phát âm khác nhau: Violin (`violin_001.wav`), Cello (`cello_010.wav`) và Guitar Electric (`guitar_electric_005.wav`).

![Hình 4.5: Ba truy vấn minh họa](file:///d:/Ki1_4/HCSDLDPT/btl_new/reports/hinh/4_5_truy_van_minh_hoa.png)  
*Hình 4.5: Ba truy vấn minh họa với top 5 kết quả tìm kiếm gần nhất; khung xanh lá: kết quả đúng; khung đỏ: kết quả sai; d là khoảng cách Euclid.*

Phân tích chi tiết 3 truy vấn:
1. **Truy vấn 1 – `violin_001.wav` (Violin):**  
   - Top 1: `violin_034.wav` (d = 5,96 — Đúng)
   - Top 2: `violin_090.wav` (d = 6,16 — Đúng)
   - Top 3: `viola_058.wav` (d = 6,66 — Nhầm sang Viola)
   - Top 4: `violin_016.wav` (d = 6,77 — Đúng)
   - Top 5: `violin_055.wav` (d = 6,80 — Đúng)  
   *Giải thích hiện tượng:* 4/5 kết quả trả về hoàn toàn chính xác. Trường hợp duy nhất ở Top 3 bị nhầm sang Viola là do tệp `viola_058.wav` được thu ở nốt cao (E5), có trọng tâm phổ và độ sáng xấp xỉ nốt trung của Violin, hoàn toàn phù hợp với phân tích lý thuyết ở mục 2.6.3.
2. **Truy vấn 2 – `cello_010.wav` (Cello):**  
   - Cả 5 kết quả Top 1 đến Top 5 đều thuộc về Cello (`cello_014`, `cello_016`, `cello_011`, `cello_035`, `cello_015`) với khoảng cách cực nhỏ (d = 2,70 - 3,33). Hệ thống đạt độ chính xác tuyệt đối 100%.
3. **Truy vấn 3 – `guitar_electric_005.wav` (Guitar Electric):**  
   - Cả 5 kết quả Top 1 đến Top 5 đều thuộc về Guitar Electric (`guitar_electric_045`, `...087`, `...037`, `...048`, `...082`) với khoảng cách d = 4,75 - 5,38. Các đặc trưng MFCC bậc cao và dải tần biến thiên mạnh đã nhận diện hoàn hảo chất âm điện tử đặc trưng.

**Kết luận Chương 4:**  
Các thực nghiệm định lượng trên 600 tệp âm thanh đã chứng minh một cách khoa học tính đúng đắn và hiệu quả vượt trội của bộ 58 đặc trưng âm học. Độ chính xác P@1 đạt 93,00% và khoảng cách nội lớp phân tách rõ rệt với liên lớp khẳng định bộ dữ liệu và bộ đặc trưng hoàn toàn sẵn sàng cho việc tích hợp vào hệ CSDL ở giai đoạn tiếp theo.

---

## CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1 Kết quả đạt được

Báo cáo số 1 đã giải quyết trọn vẹn và chuẩn mực hai nội dung nền tảng của đề tài:
1. **Xây dựng thành công bộ dữ liệu âm thanh chuẩn hóa:** Bao gồm **600 tệp âm thanh WAV PCM 16-bit 22.050 Hz mono**, phân bố cân bằng tuyệt đối giữa 6 loại nhạc cụ bộ dây tiêu biểu (Violin, Viola, Cello, Double Bass, Guitar Acoustic, Guitar Electric). Toàn bộ quy trình thu thập, lọc khoảng lặng ngưỡng -35 dBFS, phân đoạn nốt và làm mềm biên độ fade 20 ms được tự động hóa hoàn toàn bằng mã nguồn Python có khả năng tái lập 100%.
2. **Khảo sát toàn diện đặc trưng âm học:** Phân tích tường minh cơ chế vật lý và đối chứng chi tiết 7 cặp nhạc cụ có vùng giao thoa âm học dễ nhầm lẫn.
3. **Thiết kế hệ thống 58 đặc trưng âm học đa diện:** Kết hợp hài hòa giữa Năng lượng thời gian (RMS, ZCR), Cấu trúc phổ tần số (Centroid, Rolloff), Âm sắc mô phỏng thính giác người (13 hệ số MFCC bậc 0-12) và Hòa âm cao độ (12 dải Chroma Pitch Class). Toàn bộ công thức toán học và mã nguồn trích xuất đều được cài đặt chuẩn xác.
4. **Kiểm định định lượng thực nghiệm nghiêm ngặt:** Đánh giá chi tiết thông qua Fisher criterion, ANOVA F-statistic, Mutual Information và tương quan Pearson. Thực nghiệm Leave-One-Out trên 600 tệp chứng minh hệ thống đạt độ chính xác **P@1 = 93,00%**, **P@5 = 88,47%** và **mAP = 58,63%**.

### 5.2 Hạn chế

Bên cạnh những kết quả tích cực, hệ thống hiện tại vẫn tồn tại một số hạn chế cần khắc phục trong các giai đoạn tiếp theo:
1. **Mức độ phức tạp của tín hiệu đầu vào:** Bộ dữ liệu hiện tại chủ yếu tập trung vào các nốt nhạc đơn âm sắc (monophonic/isolated notes). Khi tín hiệu đầu vào là đoạn hòa tấu đa âm sắc phức tạp (polyphonic) có tiếng trống hoặc nhiều nhạc cụ cùng chơi, việc trích xuất đặc trưng toàn cục sẽ bị suy giảm độ chính xác.
2. **Trọng số đồng đều trong hàm khoảng cách Euclid:** Hiện tại, toàn bộ 58 đặc trưng sau khi chuẩn hóa z-score đều được gán trọng số bằng nhau (w_j = 1). Trong thực tế, các đặc trưng có Fisher ratio cao (như MFCC bậc 1, 2 và Centroid) mang giá trị phân biệt lớn hơn nhiều so với các bậc Chroma riêng lẻ. Việc áp dụng trọng số đồng đều vô tình làm giảm độ nhạy bén của các thuộc tính cốt lõi.
3. **Độ nhầm lẫn giữa các nhạc cụ cùng họ vật lý:** Cặp Violin – Viola ở các nốt cao vẫn xảy ra hiện tượng nhận diện chéo (Viola có mAP đạt 38,68% và Violin đạt 45,31%), do thể tích thùng đàn chưa được mô hình hóa triệt để qua các hệ số bao phổ tĩnh.

### 5.3 Hướng phát triển

Nhằm hoàn thiện toàn diện hệ thống CBAR phục vụ Báo cáo số 2 và Báo cáo số 3, nhóm định hướng triển khai các nhiệm vụ trọng tâm sau:
1. **Học trọng số khoảng cách có trọng số (Weighted Distance Metric):** Tối ưu hóa bộ trọng số w in R^58 dựa trên Fisher ratio hoặc thuật toán học khoảng cách (Metric Learning / Large Margin Nearest Neighbor) nhằm tối đa hóa khoảng cách liên lớp và thu hẹp khoảng cách nội lớp.
2. **Thiết kế lược đồ CSDL đa phương tiện chuẩn:** Xây dựng cơ sở dữ liệu quan hệ (PostgreSQL / SQLite) lưu trữ cấu trúc bảng siêu dữ liệu âm thanh, tệp nhị phân và ma trận 58 chiều đặc trưng.
3. **Xây dựng cấu trúc chỉ mục tìm kiếm nhiều chiều:** Cài đặt các cấu trúc dữ liệu chỉ mục không gian đa chiều (k-d tree, R-tree hoặc LSH - Locality Sensitive Hashing) để tăng tốc độ truy vấn từ độ phức tạp tuyến tính O(N) xuống mức logarit O(log N), sẵn sàng cho các cơ sở dữ liệu hàng triệu bản ghi.
4. **Phát triển giao diện ứng dụng trực quan (Web Interface):** Xây dựng ứng dụng web tương tác (sử dụng Streamlit hoặc FastAPI) cho phép người dùng tải tệp âm thanh bất kỳ, nghe bản ghi mẫu, xem phổ Spectrogram trực tiếp và nhận kết quả truy vấn top 5 nhạc cụ tương đồng nhất kèm giải thích trực quan.

---

## TÀI LIỆU THAM KHẢO

- [1] L. R. Rabiner and R. W. Schafer, *Theory and Applications of Digital Speech Processing*. Pearson, 2011.
- [2] M. Müller, *Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications*. Springer, 2015.
- [3] B. McFee, C. Raffel, D. Liang, D. P. Ellis, M. McVicar, E. Battenberg, and O. Nieto, "librosa: Audio and music signal analysis in python," in *Proceedings of the 14th Python in Science Conference*, 2015, pp. 18–25.
- [4] A. E. Cemgil, "Music Information Retrieval: Recent developments and applications," *IEEE Signal Processing Magazine*, vol. 36, no. 1, pp. 12–25, 2019.
- [5] A. Klapuri and M. Davy, *Signal Processing Methods for Music Transcription*. Springer Science & Business Media, 2007.
- [6] J. Thickstun, Z. Harchaoui, and S. M. Kakade, "Learning features of music from scratch," in *International Conference on Learning Representations (ICLR)*, 2017.
- [7] J. Saunders, "Real-time discrimination of broadcast speech/music," in *Proceedings of ICASSP '96*, vol. 2, 1996, pp. 993–996.
- [8] G. Tzanetakis and P. Cook, "Musical genre classification of audio signals," *IEEE Transactions on Speech and Audio Processing*, vol. 10, no. 5, pp. 293–302, 2002.
- [9] T. L. Nwe, S. W. Foo, and L. C. De Silva, "Speech emotion recognition using hidden Markov models," *Speech Communication*, vol. 41, no. 4, pp. 603–623, 2003.
- [10] A. W. M. Smeulders, M. Worring, S. Santini, A. Gupta, and R. Jain, "Content-based image and multimedia retrieval at the end of the early years," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 22, no. 12, pp. 1349–1380, 2000.

---

## PHỤ LỤC

### A. THỐNG KÊ CHI TIẾT BỘ DỮ LIỆU VÀ ĐẶC TRƯNG

#### A.1. Số mẫu và kết quả truy vấn theo nhạc cụ

Bảng A.1 trình bày chi tiết số lượng mẫu chuẩn hóa, độ chính xác Top 1 (P@1), độ chính xác Top 5 (P@5) và độ chính xác trung bình (mAP) tính trên vectơ 58 đặc trưng chuẩn hóa cho từng loại nhạc cụ bộ dây trong cơ sở dữ liệu.

*Bảng A.1: Số mẫu và kết quả truy vấn theo từng nhạc cụ*

| STT | Tên nhạc cụ | Tên tiếng Anh | Số lượng tệp WAV | P@1 (Accuracy) | P@5 (%) | mAP (%) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | Đàn Violin | Violin | 100 tệp | 78,00% | 78,00% | 45,31% |
| 2 | Đàn Viola | Viola | 100 tệp | 93,00% | 79,20% | 38,68% |
| 3 | Đàn Cello | Cello | 100 tệp | 95,00% | 91,00% | 59,58% |
| 4 | Đàn Double Bass | Double Bass | 100 tệp | 100,00% | 96,20% | 67,57% |
| 5 | Đàn Guitar Acoustic | Acoustic Guitar | 100 tệp | 97,00% | 95,00% | 73,79% |
| 6 | Đàn Guitar Electric | Electric Guitar | 100 tệp | 95,00% | 91,40% | 66,85% |
| **Tổng / TB** | **6 loại nhạc cụ** | **Toàn bộ hệ thống** | **600 tệp** | **93,00%** | **88,47%** | **58,63%** |

#### A.2. Thống kê mô tả 58 đặc trưng

Bảng A.2 trình bày giá trị nhỏ nhất (Min), lớn nhất (Max), trung bình (Mean) và độ lệch chuẩn (Std) của toàn bộ 58 đặc trưng âm học tính trên 600 tệp âm thanh trong cơ sở dữ liệu trước khi chuẩn hóa z-score (giá trị thô).

*Bảng A.2: Thống kê mô tả 58 đặc trưng âm học (giá trị thô)*

| STT | Tên đặc trưng | Nhóm thuộc tính | Min | Max | Mean | Std |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
""")

parts.append(a2_table_str)
parts.append("\n")

full_content = "".join(parts)

with open(MD_PATH_1, "w", encoding="utf-8") as f:
    f.write(full_content)
with open(MD_PATH_2, "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"[OK] Generated {MD_PATH_1} and {MD_PATH_2} successfully!")
