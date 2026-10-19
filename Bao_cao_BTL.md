# BÁO CÁO BÀI TẬP LỚN HỆ CƠ SỞ DỮ LIỆU ĐA PHƯƠNG TIỆN

**HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG**
**KHOA CÔNG NGHỆ THÔNG TIN**
———————————

## ĐỀ TÀI: XÂY DỰNG HỆ CSDL LƯU TRỮ VÀ TÌM KIẾM TIẾNG NHẠC CỤ BỘ DÂY DỰA TRÊN NỘI DUNG (CBAR)

- **Học phần:** Hệ cơ sở dữ liệu đa phương tiện
- **Sinh viên thực hiện:** Trần Mạnh Khiêm
- **Nhiệm vụ báo cáo:**
  - Nhiệm vụ 1: Xây dựng bộ dữ liệu âm thanh nhạc cụ bộ dây và phân tích đặc điểm giống, khác nhau.
  - Nhiệm vụ 2: Xây dựng bộ đặc trưng nhận diện và thiết kế mô hình tính độ tương đồng cho hệ thống CBAR.
- **Hà Nội – 2026**

---

## MỤC LỤC

1. [CHƯƠNG 1: TỔNG QUAN VỀ BÀI TOÁN VÀ CƠ SỞ KỸ THUẬT](#chương-1-tổng-quan-về-bài-toán-và-cơ-sở-kỹ-thuật)
   - 1.1. [Bài toán tìm kiếm âm thanh theo nội dung (CBAR) và phân biệt với phân loại nhạc cụ](#11-bài-toán-tìm-kiếm-âm-thanh-theo-nội-dung-cbar-và-phân-biệt-với-phân-loại-nhạc-cụ)
   - 1.2. [Đặc điểm và nguyên lý tạo âm của nhạc cụ bộ dây](#12-đặc-điểm-và-nguyên-lý-tạo-âm-của-nhạc-cụ-bộ-dây)
   - 1.3. [Nền tảng xử lý tín hiệu âm thanh số](#13-nền-tảng-xử-lý-tín-hiệu-âm-thanh-số)
2. [CHƯƠNG 2: NHIỆM VỤ 1 - XÂY DỰNG BỘ DỮ LIỆU ÂM THANH](#chương-2-nhiệm-vụ-1---xây-dựng-bộ-dữ-liệu-âm-thanh)
   - 2.1. [Yêu cầu đề bài và tiêu chí kỹ thuật của bộ dữ liệu](#21-yêu-cầu-đề-bài-và-tiêu-chí-kỹ-thuật-của-bộ-dữ-liệu)
   - 2.2. [Lựa chọn nhạc cụ và giới thiệu từng nhạc cụ](#22-lựa-chọn-nhạc-cụ-và-giới-thiệu-từng-nhạc-cụ)
   - 2.3. [Các bộ dữ liệu được sử dụng, cấu trúc dữ liệu thô và phạm vi nhãn](#23-các-bộ-dữ-liệu-được-sử-dụng-cấu-trúc-dữ-liệu-thô-và-phạm-vi-nhãn)
   - 2.4. [Quy trình tiền xử lý và lọc dữ liệu 11 bước](#24-quy-trình-tiền-xử-lý-và-lọc-dữ-liệu-11-bước)
   - 2.5. [Kết quả bộ dữ liệu 600 file hoàn chỉnh](#25-kết-quả-bộ-dữ-liệu-600-file-hoàn-chỉnh)
3. [CHƯƠNG 3: NHIỆM VỤ 1 - PHÂN TÍCH ĐIỂM GIỐNG VÀ KHÁC NHAU CỦA TIẾNG CÁC NHẠC CỤ](#chương-3-nhiệm-vụ-1---phân-tích-điểm-giống-và-khác-nhau-của-tiếng-các-nhạc-cụ)
   - 3.1. [Phương diện 1: Phân tích dựa trên lý thuyết và đặc tính vật lý của nhạc cụ](#31-phương-diện-1-phân-tích-dựa-trên-lý-thuyết-và-đặc-tính-vật-lý-của-nhạc-cụ)
   - 3.2. [Phương diện 2: Phân tích thực nghiệm dựa trên phương pháp âm học và số liệu đo đạc](#32-phương-diện-2-phân-tích-thực-nghiệm-dựa-trên-phương-pháp-âm-học-và-số-liệu-đo-đạc)
   - 3.3. [Bảng tổng hợp đối chiếu song song giữa lý thuyết và thực nghiệm](#33-bảng-tổng-hợp-đối-chiếu-song-song-giữa-lý-thuyết-và-thực-nghiệm)
   - 3.4. [Các trường hợp ngoại lệ và hạn chế của bộ dữ liệu](#34-các-trường-hợp-ngoại-lệ-và-hạn-chế-của-bộ-dữ-liệu)
   - 3.5. [Ý nghĩa chuyển tiếp sang Nhiệm vụ 2](#35-ý-nghĩa-chuyển-tiếp-sang-nhiệm-vụ-2)
4. [CHƯƠNG 4: NHIỆM VỤ 2 - XÂY DỰNG BỘ ĐẶC TRƯNG VÀ THIẾT KẾ ĐỘ TƯƠNG ĐỒNG CHO CBAR](#chương-4-nhiệm-vụ-2---xây-dựng-bộ-đặc-trưng-và-thiết-kế-độ-tương-đồng-cho-cbar)
   - 4.1. [Mục tiêu và kiến trúc bộ đặc trưng tìm kiếm](#41-mục-tiêu-và-kiến-trúc-bộ-đặc-trưng-tìm-kiếm)
   - 4.2. [Chi tiết ba bộ đặc trưng: Từ cơ sở lý thuyết đến ứng dụng CBAR](#42-chi-tiết-ba-bộ-đặc-trưng-từ-cơ-sở-lý-thuyết-đến-ứng-dụng-cbar)
   - 4.3. [Tổng hợp vector đặc trưng qua Temporal Pooling và phân tích 58 chiều](#43-tổng-hợp-vector-đặc-trưng-qua-temporal-pooling-và-phân-tích-58-chiều)
   - 4.4. [Chuẩn hóa đặc trưng Z-score và nguyên tắc chống rò rỉ dữ liệu](#44-chuẩn-hóa-đặc-trưng-z-score-và-nguyên-tắc-chống-rò-rỉ-dữ-liệu)
   - 4.5. [Độ đo khoảng cách chuẩn hóa và cơ chế xếp hạng Top-5 file giống nhất](#45-độ-đo-khoảng-cách-chuẩn-hóa-và-cơ-chế-xếp-hạng-top-5-file-giống-nhất)
   - 4.6. [Đề xuất phương pháp luận đánh giá hệ thống tìm kiếm cho Nhiệm vụ 4](#46-đề-xuất-phương-pháp-luận-đánh-giá-hệ-thống-tìm-kiếm-cho-nhiệm-vụ-4)
5. [CHƯƠNG 5: KẾT LUẬN VÀ KẾ HOẠCH TRIỂN KHAI TIẾP THEO](#chương-5-kết-luận-và-kế-hoạch-triển-khai-tiếp-theo)
   - 5.1. [Tổng kết kết quả Nhiệm vụ 1 và Nhiệm vụ 2](#51-tổng-kết-kết-quả-nhiệm-vụ-1-và-nhiệm-vụ-2)
   - 5.2. [Các hạn chế thực tế của hệ thống](#52-các-hạn-chế-thực-tế-của-hệ-thống)
   - 5.3. [Kế hoạch thực hiện Nhiệm vụ 3 và Nhiệm vụ 4](#53-kế-hoạch-thực-hiện-nhiệm-vụ-3-và-nhiệm-vụ-4)
6. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## CHƯƠNG 1: TỔNG QUAN VỀ BÀI TOÁN VÀ CƠ SỞ KỸ THUẬT

### 1.1. Bài toán tìm kiếm âm thanh theo nội dung (CBAR) và phân biệt với phân loại nhạc cụ

#### 1.1.1. Khái niệm bài toán CBAR

Khác với phương thức tìm kiếm âm thanh truyền thống dựa trên siêu dữ liệu văn bản (như tên bài hát, nghệ sĩ, thể loại), **tìm kiếm âm thanh dựa trên nội dung (Content-Based Audio Retrieval – CBAR)** khai thác trực tiếp các đặc tính âm học nội tại của tín hiệu sóng âm. Hệ thống hoạt động theo mô hình truy vấn bằng âm thanh mẫu (Query-by-Example): người dùng cung cấp một đoạn âm thanh mẫu (Query), hệ thống trích xuất vector đặc trưng biểu diễn nội dung âm học của mẫu đó, tính toán khoảng cách hoặc độ tương đồng với các vector trong cơ sở dữ liệu (Gallery), sau đó xếp hạng và trả về danh sách $K$ tệp tương đồng nhất (Top-$K$).

#### 1.1.2. Phân biệt CBAR và Phân loại nhạc cụ (Instrument Classification)

Cần phân biệt rõ ràng hai bài toán xử lý thông tin âm thanh này:

- **Bài toán Phân loại nhạc cụ (Classification):** Là bài toán học có giám sát (Supervised Learning). Mục tiêu là ánh xạ một đoạn âm thanh đầu vào thành một nhãn rời rạc thuộc tập nhãn cố định định trước $\mathcal{C} = \{c_1, c_2, \dots, c_K\}$ (ví dụ: gán nhãn chính xác "Violin" hay "Guitar"). Mô hình phân loại tối ưu hóa ranh giới quyết định (decision boundary) để tách biệt các lớp nhãn.
- **Bài toán Truy xuất âm thanh dựa trên nội dung (CBAR):** Là bài toán truy hồi thông tin (Information Retrieval / Metric Learning). Mục tiêu không phải là gán nhãn cứng cho tệp, mà là lượng hóa mức độ tương đồng liên tục giữa các đối tượng âm thanh trong một không gian đặc trưng chung. Hệ thống CBAR có tính linh hoạt cao hơn: nếu đưa vào một tệp truy vấn thuộc nhạc cụ chưa từng có trong cơ sở dữ liệu (Out-of-Distribution) hoặc tệp chứa kỹ thuật diễn tấu đặc thù, hệ thống vẫn có thể tìm và xếp hạng các tệp có âm sắc, cao độ hoặc phong cách kích âm gần gũi nhất.

#### 1.1.3. Mục tiêu và phạm vi của bài tập lớn

Đề tài đặt mục tiêu xây dựng hệ thống CBAR cho **tiếng nhạc cụ bộ dây**, bao gồm 4 nhiệm vụ tuần tự:

1. **Nhiệm vụ 1:** Thu thập, tiền xử lý và xây dựng bộ dữ liệu âm thanh gồm ít nhất 500 file độc tấu đơn nhạc cụ bộ dây; chuẩn hóa định dạng và phân tích, đối chiếu các đặc điểm giống, khác nhau của tiếng các nhạc cụ.
2. **Nhiệm vụ 2:** Xây dựng hệ thống các bộ đặc trưng âm thanh giúp biểu diễn sự tương đồng và phân biệt giữa các nhạc cụ; giải thích rõ cơ sở toán học và giá trị thông tin của từng đặc trưng.
3. **Nhiệm vụ 3:** Triển khai công cụ trích rút đặc trưng tự động và thiết kế hệ CSDL đa phương tiện để quản lý các vector đặc trưng.
4. **Nhiệm vụ 4:** Xây dựng hệ thống tìm kiếm: nhận một tệp âm thanh truy vấn mới, tính khoảng cách tương đồng, xếp hạng và trả về danh sách 5 tệp giống nhất (Top-5) trong cơ sở dữ liệu.

Báo cáo này tập trung nghiệm thu đầy đủ nội dung kỹ thuật của **Nhiệm vụ 1** và **Nhiệm vụ 2**, đồng thời thiết lập khung phương pháp luận cho Nhiệm vụ 3 và 4.

---

### 1.2. Đặc điểm và nguyên lý tạo âm của nhạc cụ bộ dây

#### 1.2.1. Cấu tạo và đường truyền âm thanh

Nhạc cụ bộ dây (chordophone) tạo ra âm thanh từ sự dao động cơ học của một hoặc nhiều sợi dây đàn được căng giữa hai điểm cố định. Quá trình bức xạ sóng âm ra môi trường diễn ra qua chuỗi truyền động:

$$
\text{Tác động kích âm (kéo vĩ / gảy ngón)} \longrightarrow \text{Dây đàn rung} \longrightarrow \text{Ngựa đàn truyền lực} \longrightarrow \text{Thùng đàn cộng hưởng / Pickup} \longrightarrow \text{Sóng âm}
$$

- Do tiết diện sợi dây rất nhỏ, dây đàn rung tự do trong không khí chỉ bức xạ một năng lượng âm học không đáng kể.
- Ngựa đàn (bridge) đóng vai trò biến đổi dao động ngang của dây thành dao động uốn truyền xuống bản mặt thùng đàn.
- Thùng đàn bằng gỗ có khoang rỗng hoạt động như một hệ cộng hưởng âm học phức tạp, khuếch đại biên độ và tạo nên các đỉnh cộng hưởng formant đặc thù cho từng loại đàn.
- Đối với guitar điện, dao động của dây kim loại được cuộn cảm biến từ tính (pickup) biến đổi trực tiếp thành tín hiệu dòng điện xoay chiều tương tự, sau đó chuyển qua mạch tiền khuếch đại, bộ hiệu ứng xử lý tín hiệu và amply công suất.

#### 1.2.2. Dao động của dây và cơ chế tạo cao độ

Với một sợi dây lý tưởng có chiều dài rung $L$, lực căng $T$ và khối lượng trên một đơn vị chiều dài $\mu$, tần số dao động cơ bản $f_0$ (nốt cơ bản) được xác định xấp xỉ theo công thức Mersenne–Taylor:

$$
f_0 \approx \frac{1}{2L} \sqrt{\frac{T}{\mu}}
$$

Khi dây rung, sóng phản xạ tại hai đầu cố định tạo thành hệ sóng dừng với các tần số họa âm (harmonics) xuất hiện tại các bội số nguyên:

$$
f_n \approx n \cdot f_0 \quad (n = 1, 2, 3, \dots)
$$

- $f_0$ ($n = 1$) quy định **cao độ danh định** của nốt nhạc.
- Sự phân bố năng lượng tương đối giữa các họa âm $f_n$ kết hợp với đáp ứng tần số của thùng cộng hưởng tạo nên **âm sắc (timbre)** của nhạc cụ.
- Dây có chiều dài rung lớn, khối lượng nặng và lực căng thấp sẽ phát ra âm thanh trầm; dây ngắn, nhẹ và căng sẽ phát ra âm thanh bổng.

#### 1.2.3. Hai cơ chế kích âm cơ bản: Kéo vĩ và Gảy dây

Phương thức truyền năng lượng cơ học vào dây tạo ra sự phân hóa sâu sắc về hình thái tín hiệu âm thanh:

- **Kéo vĩ (như Violin, Viola, Cello, Double Bass):** Dựa trên hiện tượng dính - trượt (stick-slip friction) giữa lông vĩ bôi nhựa thông và dây đàn. Năng lượng được nạp liên tục vào dây trong suốt hành trình kéo vĩ. Do đó, tín hiệu có giai đoạn duy trì năng lượng (Sustain) kéo dài và tương đối ổn định về biên độ.
- **Gảy dây (như Acoustic Guitar, Electric Guitar):** Dây đàn bị kéo lệch khỏi vị trí cân bằng rồi buông tự do. Toàn bộ cơ năng chỉ được truyền vào dây tại thời điểm gảy ban đầu (tạo đỉnh xung kích biên độ cao trong thời gian ngắn - Attack), sau đó năng lượng tiêu hao dần do ma sát nội và ma sát không khí, khiến biên độ dao động suy giảm nhanh theo hàm mũ (Decay).

---

### 1.3. Nền tảng xử lý tín hiệu âm thanh số

Để máy tính có thể phân tích và trích xuất đặc trưng, sóng âm tương tự liên tục phải được số hóa thông qua các bước kỹ thuật cơ bản:

#### 1.3.1. Lấy mẫu tín hiệu và định lý Nyquist–Shannon

Tín hiệu âm thanh liên tục $x(t)$ được rời rạc hóa theo thời gian với chu kỳ lấy mẫu $T_s$, tương ứng tần số lấy mẫu $f_s = 1/T_s$:

$$
x[n] = x(n T_s)
$$

Theo định lý lấy mẫu Nyquist–Shannon, để có thể khôi phục hoàn toàn và chính xác một tín hiệu liên tục có dải thông hữu hạn từ các mẫu rời rạc mà không bị hiện tượng chồng phổ (aliasing), tần số lấy mẫu $f_s$ phải lớn hơn hai lần tần số cao nhất $f_{\max}$ có trong phổ tín hiệu:

$$
f_s > 2 f_{\max} \iff f_{\text{Nyquist}} = \frac{f_s}{2} > f_{\max}
$$

Trong thực tế, tín hiệu cần được giới hạn băng tần trước khi lấy mẫu để hạn chế hiện tượng chồng phổ ( *aliasing* ). Do đó, việc chọn tần số lấy mẫu không chỉ phụ thuộc vào cao độ cơ bản của nhạc cụ mà còn phụ thuộc vào các họa âm và thành phần tần số cao có ý nghĩa đối với bài toán.

Trong báo cáo này, dữ liệu được chuẩn hóa về tần số lấy mẫu (f_s=22,050\text{ Hz}), tương ứng tần số Nyquist (f_N=11,025\text{ Hz}). Mức lấy mẫu này giúp giảm dung lượng dữ liệu và chi phí tính toán so với chuẩn 44,1 kHz, đồng thời vẫn giữ lại phần lớn thông tin phổ trong dải tần đến 11,025 kHz.

#### 1.3.2. Cấu hình kênh đơn (Mono) và lượng tử hóa PCM 16-bit

Âm thanh stereo gồm hai kênh trái và phải, có thể chứa cả thông tin về vị trí không gian, mức âm lượng và khác biệt giữa hai kênh thu. Đối với bài toán tìm kiếm âm thanh theo nội dung, việc chuyển về mono giúp thống nhất đầu vào và giảm chi phí lưu trữ, xử lý. Tuy nhiên, thao tác này cũng có thể làm mất một phần thông tin không gian hoặc gây suy giảm một số thành phần âm thanh nếu hai kênh có sự khác biệt về pha.

Nếu hai kênh stereo được gộp bằng phép lấy trung bình cộng, tín hiệu mono được tính như sau:

- $$
  x_{\text{mono}}[n] = \frac{x_L[n] + x_R[n]}{2}
  $$

Dữ liệu được lưu ở định dạng WAV sử dụng PCM 16-bit. Với cách biểu diễn PCM có dấu 16-bit thông thường, mỗi mẫu có thể biểu diễn các giá trị nguyên từ (-32,768) đến (32,767). PCM là phương pháp mã hóa mẫu âm thanh không mất dữ liệu so với chính các mẫu PCM đã được tạo ra; tuy nhiên, quá trình chuyển đổi từ nguồn âm thanh ban đầu sang PCM 16-bit vẫn có thể làm thay đổi dữ liệu do lượng tử hóa, chuyển đổi tần số lấy mẫu hoặc các bước tiền xử lý khác

#### 1.3.3. Phân biệt ba cấp độ biểu diễn dữ liệu trong hệ thống

Để tránh nhầm lẫn trong quá trình xử lý, hệ thống phân định rõ ràng 3 cấp độ biểu diễn dữ liệu:

1. **Dữ liệu âm thanh thô (Raw Audio):** Các tệp âm thanh gốc thu thập từ nhiều nguồn, có độ dài không đồng đều, tần số lấy mẫu khác nhau ($44{,}1\text{ kHz}$ hoặc $48\text{ kHz}$), có thể ở định dạng stereo hoặc chứa khoảng lặng dài.
2. **Tín hiệu tiền xử lý chuẩn hóa (Preprocessed Audio):** Dạng sóng số $x[n]$ đã được đưa về mono, chuẩn hóa tần số lấy mẫu $22\,050\text{ Hz}$, cắt đoạn có độ dài chuẩn quanh $3\text{ s}$ theo ranh giới nốt nhạc và chuẩn hóa biên độ đỉnh.
3. **Vector đặc trưng truy hồi (Feature Vector):** Vector số thực cố định $\mathbf{v} \in \mathbb{R}^{58}$ được trích xuất từ tín hiệu sau tiền xử lý qua các phép biến đổi toán học và tổng hợp thống kê, đại diện cho tệp âm thanh trong cơ sở dữ liệu CBAR.

#### 1.3.4. Chia khung (Framing) và Bước nhảy (Hop Size)

Do tín hiệu âm thanh có tính chất biến đổi phi dừng theo thời gian, kỹ thuật chia khung (Framing) được áp dụng để coi tín hiệu là dừng trong từng đoạn ngắn:

- **Độ dài khung ($N$):** Chọn $N = 2048$ mẫu (khoảng $92{,}88\text{ ms}$ tại $f_s = 22\,050\text{ Hz}$).
- **Bước nhảy ($H$):** Chọn $H = 512$ mẫu (khoảng $23{,}22\text{ ms}$).
- **Độ gối khung (Overlap):** Đạt $(2048 - 512) / 2048 = 75\%$, giúp duy trì tính liên tục và giảm thiểu mất mát thông tin tại biên khung.
- Độ phân giải tần số: $\Delta f = f_s / N = 22\,050 / 2048 \approx 10{,}77\text{ Hz}$, đủ mịn để tách bạch các họa âm ở dải trầm.

#### 1.3.5. Năng lượng hiệu dụng RMS và mức Decibel (dB)

- **Năng lượng hiệu dụng RMS:** Đo mức biên độ hiệu dụng trong khung thời gian thứ $m$:

  $$
  \operatorname{RMS}(m) = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x_m[n]^2}
  $$

  RMS phản ánh mức năng lượng vật lý của tín hiệu sóng, khác với độ to cảm nhận (Loudness) của thính giác người do tai người có độ nhạy biến thiên phi tuyến theo tần số (mô tả qua các đường cong đẳng âm ISO 226).
- **Mức Decibel tương đối:** Biểu diễn mức năng lượng theo thang logarit so với giá trị đỉnh của tệp:

  $$
  L_{\text{dB}}(m) = 20 \log_{10} \left( \frac{\operatorname{RMS}(m)}{\max_{k} \operatorname{RMS}(k) + 10^{-9}} \right)
  $$

#### 1.3.6. Biến đổi Fourier thời gian ngắn (STFT) và Spectrogram

Biến đổi Fourier thời gian ngắn (Short-Time Fourier Transform – STFT) phân tích nội dung tần số của từng khung sau khi nhân với cửa sổ làm mịn Hann $w[n]$:

$$
X(m, k) = \sum_{n=0}^{N-1} x_m[n] \cdot w[n] \cdot e^{-j 2\pi k n / N}, \quad k = 0, 1, \dots, N/2
$$

Phổ công suất tương ứng là $P(m, k) = |X(m, k)|^2$. Biểu đồ Spectrogram ghép các phổ công suất theo trục thời gian, cung cấp hình ảnh trực quan về sự phân bố năng lượng theo thời gian và tần số.

---

## CHƯƠNG 2: NHIỆM VỤ 1 - XÂY DỰNG BỘ DỮ LIỆU ÂM THANH

### 2.1. Yêu cầu đề bài và tiêu chí kỹ thuật của bộ dữ liệu

Để đáp ứng đầy đủ yêu cầu của bài tập lớn, các tiêu chí kỹ thuật cụ thể được xác lập như sau:

| Yêu cầu đề bài                    | Tiêu chí kỹ thuật cụ thể                                                                                                                          | Giải pháp thực hiện trong đề tài                                                                                                                                                                                                                          |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Số lượng $\ge 500$ file** | Đạt số lượng quy định, phân bổ cân bằng giữa các lớp để tránh lệch dữ liệu                                                          | Xây dựng chuẩn xác **600 file WAV**, chia đều cho **6 lớp nhạc cụ** (mỗi nhạc cụ đúng 100 file).                                                                                                                                       |
| **Nhạc cụ bộ dây**           | Đại diện đủ các cơ chế kích âm (kéo vĩ, gảy) và các dải âm vực                                                                        | Chọn **4 nhạc cụ kéo vĩ** (*Violin, Viola, Cello, Double Bass*) và **2 nhạc cụ gảy** (*Acoustic Guitar, Electric Guitar*).                                                                                                              |
| **Mỗi file chỉ 1 nhạc cụ**   | Ưu tiên các bản thu độc tấu riêng từng nhạc cụ; kiểm tra để hạn chế tiếng nhạc cụ khác, tiếng nói và tạp âm không mong muốn. | Ưu tiên các track riêng từ những bộ dữ liệu phù hợp. Ghi lại nguồn, track gốc và phương pháp trích đoạn của từng file; kiểm tra thủ công hoặc bằng công cụ phân tích đối với các đoạn nghi ngờ có âm thanh chồng lấn. |
| **Độ dài phù hợp**          | Chứa trọn vẹn đặc trưng nhận diện của nốt nhạc, không bị ngắt cụt giữa chừng                                                           | Cắt đoạn tự động theo ranh giới nốt nhạc (Onset) với độ dài mục tiêu **3,0 giây** (dao động $2{,}5 - 3{,}5\text{ s}$); tỷ lệ có tiếng $\ge 90\%$; fade mép 50 ms.                                                               |
| **Định dạng lưu trữ**       | Chất lượng âm thanh đồng nhất, không nén mất dữ liệu                                                                                        | Lưu dạng **WAV mono, 22 050 Hz, PCM 16-bit**; kèm bảng siêu dữ liệu `metadata.csv` lưu vết nguồn gốc chi tiết.                                                                                                                               |

---

### 2.2. Lựa chọn nhạc cụ và giới thiệu từng nhạc cụ

#### 2.2.1. Lý do chọn nhạc cụ bộ dây

Nhạc cụ bộ dây (chordophone) là nhóm nhạc cụ phát âm từ sự dao động của dây căng – cơ chế đơn giản nhất nhưng tạo ra sự đa dạng âm sắc rất phong phú tùy theo kích thước, vật liệu, cách chơi và hệ thống khuếch đại. Đây là nhóm nhạc cụ lý tưởng để nghiên cứu bài toán CBAR vì:

- Đủ đa dạng để thử thách hệ thống: Có cả nhạc cụ kéo vĩ (âm ngân dài, đều đặn) và gảy dây (âm tắt nhanh), âm vực từ siêu trầm đến rất cao.
- Có các cặp nhạc cụ giống nhau về cấu tạo nhưng khác nhau về kích thước: Violin–Viola–Cello–Double bass là  cùng họ, giúp kiểm tra khả năng phân biệt tinh tế của bộ đặc trưng.
- Tiếng đơn nhạc cụ phổ biến và dễ thu thập từ các bộ dữ liệu học thuật lớn có sẵn.

#### 2.2.2. Tiêu chí lựa chọn 6 nhạc cụ cụ thể

Từ nhóm nhạc cụ bộ dây, 6 nhạc cụ được chọn dựa trên các tiêu chí:

1. **Bao quát cơ chế kích âm:** 4 nhạc cụ kéo vĩ (Violin, Viola, Cello, Double Bass) và 2 nhạc cụ gảy dây (Acoustic Guitar, Electric Guitar).
2. **Bao quát toàn dải âm vực:** Từ nốt thấp nhất của Double Bass ($E_1 \approx 41{,}2\text{ Hz}$) đến dải cao của Violin ($E_7 \approx 2637\text{ Hz}$).
3. **Thiết lập các cặp đối chứng :** Cặp Violin–Viola (tương đồng cấu tạo thùng, chênh lệch một quãng 5); cặp Acoustic Guitar–Electric Guitar (cùng 6 dây và âm vực, khác biệt về cơ chế cộng hưởng cơ học và hiệu ứng khuếch đại điện tử).
4. **Đảm bảo nguồn gốc học thuật có thể kiểm chứng:** Dữ liệu được trích xuất từ 4 bộ dữ liệu nghiên cứu chuẩn: URMP, GuitarSet, Medley-solos-DB và PHENICX-Anechoic.

#### 2.2.3. Giới thiệu tổng quan từng nhạc cụ

| Nhạc cụ                 | Cơ chế kích âm   | Dây buông thấp nhất | Tần số thấp nhất lý thuyết | Đặc điểm âm học nổi bật                                                                            |
| :------------------------ | :------------------- | :---------------------: | :------------------------------: | :--------------------------------------------------------------------------------------------------------- |
| **Violin**          | Kéo vĩ liên tục  |           G3           |             196,0 Hz             | Thùng đàn nhỏ nhất họ vĩ, âm vực cao nhất, âm sắc thanh mảnh và sáng.                       |
| **Viola**           | Kéo vĩ liên tục  |           C3           |             130,8 Hz             | Thùng lớn hơn violin khoảng 15%, âm vực trầm hơn đúng một quãng 5, âm sắc ấm và đượm.   |
| **Cello**           | Kéo vĩ / Pizzicato |           C2           |             65,4 Hz             | Thùng đàn lớn đặt sàn, âm vực trung-trầm ấm áp; chứa cả lối chơi kéo vĩ và gảy ngón.  |
| **Double Bass**     | Kéo vĩ liên tục  |           E1           |             41,2 Hz             | Lớn nhất và trầm nhất họ vĩ, dải năng lượng dồn sâu về vùng hạ âm làm bè đáy.         |
| **Acoustic Guitar** | Gảy buông          |           E2           |             82,4 Hz             | Thùng gỗ rỗng cộng hưởng tự nhiên, âm vang mộc, năng lượng tắt dốc sau khi gảy.            |
| **Electric Guitar** | Gảy + Méo tiếng   |           E2           |             82,4 Hz             | Thân đặc, thu qua pickup và tầng khuếch đại bão hòa (distortion), sinh nhiều họa âm dải cao. |

---

### 2.3. Các bộ dữ liệu được sử dụng, cấu trúc dữ liệu thô và phạm vi nhãn

Hệ thống tích hợp dữ liệu từ 4 bộ dữ liệu học thuật mở:

1. **URMP (University of Rochester Multi-Modal Music Performance):** Tập hợp các tác phẩm thính phòng cổ điển được thu âm riêng rẽ từng nhạc công (isolated stems) với micro chuyên dụng ở định dạng 48 kHz mono: Violin (`vn`), Viola (`va`), Cello (`vc`), Double Bass (`db`).
2. **PHENICX-Anechoic:** Thu âm các tác phẩm giao hưởng trong phòng tiêu âm (anechoic chamber) cách âm tuyệt đối không tiếng vang dội, cung cấp các track riêng lẻ của từng bè nhạc cụ (44,1 kHz). Hệ thống sử dụng track `doublebass.wav`.
3. **GuitarSet:** Bộ dữ liệu ghi âm độc tấu guitar acoustic chuyên nghiệp với 360 đoạn biểu diễn đa dạng phong cách. Hệ thống sử dụng bản thu micro tự nhiên (`*_mic.wav`, 44,1 kHz).
4. **Medley-solos-DB:** Bộ dữ liệu trích từ MedleyDB, gồm các đoạn 3 giây được gán nhãn nhạc cụ độc tấu (distorted electric guitar, 44,1 kHz).

```text
data/raw/
├── violin/            34 track URMP (48 kHz mono)
├── viola/             13 track URMP (48 kHz mono)
├── cello/             11 track URMP (48 kHz mono)
├── double_bass/        3 track URMP (48 kHz) + 4 track PHENICX (44.1 kHz)
├── guitar_acoustic/  360 file GuitarSet (44.1 kHz mono)
└── guitar_electric/  213 clip Medley-solos-DB (44.1 kHz mono)
```

| Nhạc cụ                 | Nguồn thu thập | Số file gốc | Tổng thời lượng gốc | Dải độ dài file gốc | Tần số lấy mẫu gốc |
| :------------------------ | :--------------- | :-----------: | :----------------------: | :----------------------: | :---------------------: |
| **Violin**          | URMP             |   34 track   |        63,4 phút        |     40 – 214 giây     |        48 000 Hz        |
| **Viola**           | URMP             |   13 track   |        28,1 phút        |     58 – 214 giây     |        48 000 Hz        |
| **Cello**           | URMP             |   11 track   |        24,0 phút        |     83 – 214 giây     |        48 000 Hz        |
| **Double Bass**     | URMP + PHENICX   |  3 + 4 track  |     6,1 + 10,6 phút     |     87 – 227 giây     |   48 000 / 44 100 Hz   |
| **Guitar acoustic** | GuitarSet        |   360 track   |       182,8 phút       |      14 – 46 giây      |        44 100 Hz        |
| **Guitar electric** | Medley-solos-DB  |   213 clip   |        10,6 phút        |        2,97 giây        |        44 100 Hz        |

---

### 2.4. Quy trình tiền xử lý và lọc dữ liệu 11 bước

Quy trình tự động hóa chuyển đổi từ dữ liệu thô sang 600 file WAV được triển khai trong kịch bản `src/tao_bo_du_lieu.py`:

![Sơ đồ 11 bước](hinh/0_so_do_quy_trinh.png)

*Hình 2.1: Sơ đồ 11 bước tiền xử lý và lọc dữ liệu từ nguồn thô đến 600 file WAV.*

- **Bước 1: Đọc tín hiệu, trộn kênh Mono và chuẩn hóa tần số lấy mẫu về 22 050 Hz:** Sử dụng hàm `librosa.load(..., sr=22050, mono=True)` kết hợp bộ lọc chống chồng phổ chất lượng cao `soxr_hq`.
- **Bước 2: Phân đoạn khung có tiếng (ngưỡng RMS −25 dB):**

  $$
  L_{\text{dB}}(m) = 20 \log_{10} \left( \frac{\operatorname{RMS}(m)}{\max \operatorname{RMS} + 10^{-9}} \right) > -25\text{ dB}
  $$

  *Thực nghiệm chọn ngưỡng:* Khi thử nghiệm với ngưỡng $-30\text{ dB}$, tạp âm phòng thu ở giây thứ 2 của track violin *Jupiter* (mức $-28{,}9\text{ dB}$) bị nhận nhầm là tiếng đàn dù nghệ sĩ chưa chơi. Nâng ngưỡng lên $-25\text{ dB}$ giúp phân tách chuẩn xác các đoạn nghỉ và khoảng lặng.

![Ngưỡng có tiếng](hinh/q1_nguong_co_tieng.png)*Hình 2.2: Phân biệt khung có tín hiệu nhạc cụ và khung khoảng lặng/nhiễu nền.*

- **Bước 3: Dò tìm ranh giới nốt nhạc (Onset Detection) bằng Spectral Flux:**
  Đo mức biến thiên phổ tần số Mel giữa hai khung liên tiếp:

  $$
  \operatorname{SF}(m) = \frac{1}{M} \sum_{i=0}^{M-1} \max\big(0, S_{\text{Mel}}(m, i) - S_{\text{Mel}}(m-1, i)\big)
  $$

  Áp dụng kỹ thuật lùi vết (**Backtracking**): lùi thời điểm onset về cực tiểu cục bộ năng lượng ngay trước đó (khoảng 40–70 ms) để bảo toàn trọn vẹn pha kích âm ban đầu (Attack).
- **Bước 4: Cắt đoạn âm thanh theo ranh giới nốt (2,5 – 3,5 giây):** Chọn điểm cắt gần mốc 3,0 giây nhất và kiểm tra tỷ lệ khung có tiếng $\ge 90\%$ để loại bỏ các đoạn chứa nhiều khoảng ngắt.

![Cắt theo nốt](hinh/q2_cat_theo_not.png)*Hình 2.3: Các điểm cắt đoạn tự động bám theo ranh giới chuyển nốt nhạc.*

- **Bước 5: Loại bỏ các bản thu trùng lặp bằng hệ số tương quan Pearson ($r > 0{,}99$):**
  Trong tập URMP, một số bản nhạc được nhóm tác giả phối cho nhiều đội hình khác nhau và sử dụng lại cùng một track thu âm gốc (ví dụ bài *Rondeau* các bản 35, 36, 37). Thuật toán so khớp tương quan tín hiệu thời gian giữa các cặp track có độ dài chênh lệch dưới 1 giây đã phát hiện và loại bỏ chính xác **18 track trùng lặp** (`reports/track_trung_bi_bo.csv`).
- **Bước 6: Loại bỏ các đoạn trùng lặp âm nhạc bằng dấu vân tay Mel (Mel-Fingerprint):**
  Để tránh hiện tượng chọn lặp các câu nhạc điệp khúc hoặc mẫu riff guitar giống hệt nhau trong cùng một bài, mỗi đoạn được tóm tắt thành vector vân tay 2048 chiều ($64\text{ dải Mel} \times 32\text{ cột thời gian}$), chuẩn hóa $\ell_2$. Nếu độ tương đồng Cosine giữa hai đoạn trong cùng một lớp vượt quá **$0{,}95$**, chỉ giữ lại một đoạn đại diện.
- **Bước 7: Loại trừ các đoạn liền kề:** Không chọn hai đoạn nối tiếp trực tiếp trên cùng một track nguồn nhằm tăng tính đa dạng âm nhạc. (Riêng Double Bass do số lượng track gốc hạn chế nên cho phép ngoại lệ để bảo đảm đủ 100 mẫu).
- **Bước 8: Chọn mẫu rải đều theo cơ chế Round-Robin:** Lần lượt lấy mỗi track nguồn một đoạn với `random.seed(42)`, bảo đảm các mẫu được phân tán đồng đều qua nhiều nghệ sĩ và bản nhạc khác nhau.
- **Bước 9: Chuẩn hóa biên độ đỉnh (Peak Normalization về 0,9):**

  $$
  y_{\text{norm}}[n] = 0{,}9 \times \frac{y[n]}{\max |y| + 10^{-9}}
  $$

  Đưa giá trị cực đại của tín hiệu về mức 0,9 để tối ưu dải động lượng tử hóa 16-bit và tránh hiện tượng méo cắt đỉnh (clipping).
- **Bước 10: Làm mềm hai mép tín hiệu (Fade 50 ms):** Áp dụng cửa sổ tăng dần ở 50 ms đầu và giảm dần ở 50 ms cuối:

  $$
  y[n] \leftarrow y[n] \cdot w_{\text{fade}}[n]
  $$

  *Mục đích kỹ thuật:* Làm suy giảm biên độ về 0 tại hai đầu mút của đoạn âm thanh nhằm giảm thiểu sự gián đoạn dạng sóng (waveform discontinuity), qua đó hạn chế tiếng lách tách (click artifact) và giảm rò rỉ phổ do mép cắt đột ngột. Kỹ thuật này chỉ tác động tại mép cắt 50 ms, không thể loại bỏ tạp âm bên trong thân bản ghi.

![Fade mép](hinh/q3_fade.png)*Hình 2.4: Dạng sóng tại mép cắt trước và sau khi làm mềm 50 ms.*

- **Bước 11: Lưu tệp WAV và xuất bảng siêu dữ liệu:** Ghi các tệp vào `data/wav/<nhạc_cụ>/` và tạo tệp `data/metadata.csv` lưu trữ đầy đủ thông tin: định danh tệp, nhạc cụ, track gốc, thời điểm bắt đầu và thời lượng.

---

### 2.5. Kết quả bộ dữ liệu 600 file hoàn chỉnh

Thống kê số lượng qua từng bước xử lý dữ liệu (`reports/thong_ke_loc_du_lieu.csv`):

| Nhạc cụ                 |  Track gốc  | Track trùng bị loại | Track sử dụng | Đoạn hợp lệ | Bỏ vì liền kề | Bỏ vì tương đồng ($\cos > 0{,}95$) | Số file chọn chính thức |
| :------------------------ | :-----------: | :--------------------: | :-------------: | :-------------: | :----------------: | :----------------------------------------: | :-------------------------: |
| **Violin**          |      34      |           11           |       23       |       515       |         31         |                     0                     |        **100**        |
| **Viola**           |      13      |           5           |        8        |       209       |         91         |                     0                     |        **100**        |
| **Cello**           |      11      |           1           |       10       |       221       |         60         |                     1                     |        **100**        |
| **Double Bass**     |       7       |           1           |        6        |       128       | 0 *(ngoại lệ)* |                     21                     |        **100**        |
| **Guitar acoustic** |      360      |           0           |       360       |      2 281      |         0         |                     0                     |        **100**        |
| **Guitar electric** |    11 bài    |           0           |     11 bài     |       213       |         0         |                     39                     |        **100**        |
| **TỔNG CỘNG**     | **436** |      **18**      |  **418**  | **3 567** |   **182**   |                **61**                |        **600**        |

Sau quá trình xây dựng và tiền xử lý, bộ dữ liệu được tổ chức thành 600 file WAV, phân bổ dự kiến 100 file cho mỗi nhạc cụ trong sáu lớp: Violin, Viola, Cello, Double bass, Guitar acoustic và Guitar electric. Các file được chuẩn hóa về mono, tần số lấy mẫu 22.050 Hz và PCM 16-bit để thuận tiện cho việc xử lý thống nhất.Số lượng file giữa các lớp được cân bằng nhằm hạn chế tình trạng một lớp chiếm ưu thế về số lượng trong quá trình đánh giá.

---

## CHƯƠNG 3: PHÂN TÍCH ĐIỂM GIỐNG VÀ KHÁC NHAU CỦA TIẾNG CÁC NHẠC CỤ

Nội dung phân tích được triển khai trên hai phương diện bổ trợ nhau:

1. **Phương diện lý thuyết & vật lý nhạc cụ:** Giải thích dựa trên cấu tạo, kích thước thùng đàn và cơ chế phát âm tự nhiên.
2. **Phương diện thực nghiệm âm học:** Đo đạc và xử lý tín hiệu trực tiếp trên toàn bộ 600 tệp âm thanh

### 3.1.Phân tích dựa trên lý thuyết và đặc tính vật lý của nhạc cụ

#### 3.1.1. Các điểm tương đồng theo lý thuyết

- **Chung nguyên lý phát âm từ dao động dây:** Toàn bộ 6 nhạc cụ đều phát âm từ sóng dừng trên dây căng, tạo ra âm thanh có cao độ xác định gồm nốt cơ bản và chuỗi họa âm tuần hoàn.
- **Bắt buộc có bộ phận khuếch đại:** Do diện tích dây nhỏ, dao động cơ học bắt buộc phải được truyền qua ngựa đàn tới thùng cộng hưởng (đối với violin, viola, cello, double bass, guitar acoustic) hoặc cuộn cảm ứng pickup (đối với guitar điện) để bức xạ ra ngoài.
- **Tính đồng dạng trong từng phân họ:**
  - Nhóm 4 nhạc cụ họ vĩ (Violin, Viola, Cello, Double Bass) có cùng kết cấu thùng gỗ hình số 8, cùng sử dụng vĩ kéo bằng lông ngựa bôi nhựa thông và hoạt động theo nguyên lý ma sát dính - trượt.
  - Nhóm 2 nhạc cụ guitar cùng sử dụng 6 dây với cách lên dây chuẩn E-A-D-G-B-E, cùng kích âm bằng ngón tay hoặc móng gảy.

#### 3.1.2. Các điểm khác biệt theo lý thuyết

- **Kích thước thùng đàn và dải âm vực:**
  - Theo công thức $f_0 \approx \frac{1}{2L}\sqrt{T/\mu}$, dây càng dài và nặng thì nốt càng trầm.
  - Violin có kích thước nhỏ nhất nên phát âm ở dải cao nhất; Viola lớn hơn 15% nên âm vực thấp hơn một quãng 5; Cello có thùng lớn đặt sàn, âm vực trầm ấm; Double Bass có kích thước lớn nhất, dây dài và dày, phát âm ở dải siêu trầm.
  - Hai loại guitar có âm vực nằm ở khoảng trung-trầm (dây buông thấp nhất $E_2 \approx 82{,}4\text{ Hz}$).
- **Hình thái đường bao năng lượng (Kéo vĩ vs Gảy dây):**
  - Kéo vĩ nạp năng lượng liên tục, tạo ra đường bao biên độ duy trì đều đặn (Sustain dài).
  - Gảy dây chỉ nạp năng lượng tức thời tại thời điểm buông ngón, tạo đỉnh nhọn Attack rồi suy giảm nhanh (Decay nhanh).
- **Cơ chế cộng hưởng và xử lý tín hiệu:**
  - Guitar acoustic sử dụng thùng gỗ rỗng phẳng có lỗ thoát âm tròn, âm thanh mang tính mộc tự nhiên.
  - Guitar electric thân gỗ đặc, tín hiệu được pickup từ tính chuyển đổi thành dòng điện và đưa qua bộ khuếch đại có hiệu ứng méo tiếng (distortion). Hiệu ứng này nén biên độ và sinh ra nhiều họa âm dải cao, làm âm thanh đanh dày và có độ ngân nhân tạo kéo dài.
- **Hình thức diễn tấu Đơn âm (Monophonic) vs Đa âm (Polyphonic):**
  - 4 nhạc cụ họ vĩ chủ yếu diễn tấu các giai điệu đơn âm (monophonic - mỗi thời điểm bấm và kéo một nốt đơn).
  - Hai loại guitar thường xuyên được dùng để đệm hợp âm đa âm (polyphonic - quạt hoặc rải đồng thời nhiều dây).

---

### 3.2. Phương diện 2: Phân tích thực nghiệm dựa trên phương pháp âm học và số liệu đo đạc

Bốn phép phân tích xử lý tín hiệu được thực hiện trên 600 file :

1. **Dạng sóng thời gian và Spectrogram:** Khảo sát trực quan hình thái biên độ và các vạch họa âm trên tệp đại diện thứ 11 của mỗi lớp .
2. **Khảo sát âm vực bằng thuật toán pYIN:** Ước lượng cao độ cơ bản $f_0$ từng khung bằng thuật toán pYIN, tính trung vị $f_0$ của mỗi tệp, sau đó xác định phân vị 10% ($p_{10}$), trung vị ($p_{50}$) và phân vị 90% ($p_{90}$) cho từng nhạc cụ.
3. **Phổ công suất trung bình và tần số trung vị năng lượng $f_{50}$:** Tính trung bình phổ công suất qua 100 tệp của từng nhạc cụ; xác định mốc tần số $f_{50}$ (tần số mà $50\%$ tổng năng lượng phổ tích lũy nằm phía dưới nó).
4. **Đường bao năng lượng sau Onset và mức suy giảm $D_{0{,}4}$:** Đo mức giảm biên độ RMS tại thời điểm 0,4 giây sau đỉnh nốt trên các nốt ngân dài $\ge 0{,}5\text{ s}$ ($D_{0{,}4} = L_{\text{dB}}(0{,}4\text{ s}) - L_{\text{dB}}(0\text{ s})$ tính bằng dB).

#### 3.2.1. Bảng số liệu đo đạc thực nghiệm trên 600 file

Bảng kết quả trích xuất từ tệp `reports/mo_ta_du_lieu.csv`:

| Nhạc cụ                 | Âm vực $f_0$ $p_{10}$ (Hz) | Âm vực $f_0$ Trung vị (Hz) | Âm vực $f_0$ $p_{90}$ (Hz) | Nốt trung vị tương đương | Tần số trung vị năng lượng $f_{50}$ (Hz) | Mức giảm năng lượng sau 0,4s $D_{0{,}4}$ (dB) |
| :------------------------ | :------------------------------: | :-----------------------------: | :------------------------------: | :-----------------------------: | :----------------------------------------------: | :--------------------------------------------------: |
| **Violin**          |              329,7              |         **501,3**         |              780,7              |         $\approx$ B4         |                 **506,0**                 |                    **0,0**                    |
| **Viola**           |              197,1              |         **290,4**         |              365,9              |         $\approx$ D4         |                 **355,3**                 |                   **−1,6**                   |
| **Cello**           |               98,0               |         **157,4**         |              197,2              |         $\approx$ D#3         |                 **193,8**                 |                   **−7,0**                   |
| **Double Bass**     |               72,1               |         **92,3**         |              131,6              |         $\approx$ F#2         |                 **107,7**                 |                   **−1,6**                   |
| **Guitar acoustic** |               58,9               |         **117,6**         |              351,6              |         $\approx$ A#2         |                 **236,9**                 |                   **−7,1**                   |
| **Guitar electric** |               47,0               |         **130,9**         |              331,7              |         $\approx$ C3         |                 **549,1**                 |                   **−1,0**                   |

#### 3.2.2. Kết quả Dạng sóng thời gian và Spectrogram

![Dạng sóng và Spectrogram](hinh/1_song_va_spectrogram.png)*Hình 3.1: Dạng sóng biên độ (trên) và Spectrogram (dưới) của 6 tệp đại diện.*

- **Violin:** Các vạch họa âm song song nằm ở vùng tần số cao ($600 - 8000\text{ Hz}$), năng lượng trải đều, dạng sóng biên độ biến thiên mượt mà liên tục.
- **Viola, Cello, Double Bass:** Các vạch họa âm dịch chuyển dần xuống dải tần thấp; khoảng cách giữa các vạch hẹp dần theo tỷ lệ nghịch với chiều dài dây. Double Bass dồn gần như toàn bộ năng lượng dưới $300\text{ Hz}$.
- **Guitar acoustic:** Xuất hiện các **vạch sáng dựng đứng** tại thời điểm gảy dây (năng lượng bật to tức thời trên dải tần rộng do xung gảy), ngay sau đó các vạch ngang mờ dần rất nhanh theo quy luật suy giảm tự do.
- **Guitar electric:** Spectrogram sáng đặc từ $100\text{ Hz}$ đến tận $8\text{ kHz}$. Khoảng trống giữa các họa âm bị lấp kín bởi các thành phần sóng méo do mạch khuếch đại bão hòa (distortion). Biên độ dạng sóng bị nén phẳng ở các mức đỉnh.

#### 3.2.3. Kết quả khảo sát Âm vực $f_0$ bằng thuật toán pYIN

![Biểu đồ âm vực](hinh/2_am_vuc_f0.png)*Hình 3.2: Biểu đồ hộp (Boxplot) cao độ trung vị $f_0$ (đường nét đứt: nốt dây buông thấp nhất theo lý thuyết).*

- **Trật tự âm vực họ vĩ giảm dần rõ rệt:** Violin ($501{,}3\text{ Hz}$) > Viola ($290{,}4\text{ Hz}$) > Cello ($157{,}4\text{ Hz}$) > Double Bass ($92{,}3\text{ Hz}$).
- Toàn bộ các hộp giá trị của họ vĩ đều nằm trên nốt thấp nhất lý thuyết (G3 của violin, C3 của viola, C2 của cello, E1 của double bass).
- **Hiện tượng chồng lấn âm vực:** Viola và Cello chồng lấn dải cao độ trong khoảng $190 - 200\text{ Hz}$; Guitar acoustic và Cello cùng phân bố trong khoảng $100 - 200\text{ Hz}$. Điều này chứng minh rằng cao độ $f_0$ đơn lẻ không đủ để nhận diện phân loại nhạc cụ.
- *Lỗi sub-harmonic của thuật toán pYIN:* Phân vị $p_{10}$ của Guitar acoustic ($58{,}9\text{ Hz}$) và Guitar electric ($47{,}0\text{ Hz}$) thấp hơn dây buông thấp nhất $E_2$ ($82{,}4\text{ Hz}$). Đây là hiện tượng thường gặp khi thuật toán dò cao độ đơn âm xử lý các đoạn chơi hợp âm đa âm (sự giao thoa giữa các nốt tạo ra chu kỳ lặp biểu kiến dài hơn thực tế).

#### 3.2.4. Kết quả Phổ công suất trung bình và Tần số trung vị $f_{50}$

![Phổ trung bình](hinh/3_pho_trung_binh.png)*Hình 3.3: Phổ công suất trung bình và tần số trung vị năng lượng $f_{50}$.*

- **Nhóm tập trung năng lượng dải trầm:** Double Bass có $f_{50} = 107{,}7\text{ Hz}$ (thấp nhất), Cello đạt $193{,}8\text{ Hz}$, Guitar acoustic đạt $236{,}9\text{ Hz}$. Năng lượng phổ suy giảm nhanh sau $1\text{ kHz}$.
- **Nhóm tập trung dải cao:** Violin đạt $f_{50} = 506{,}0\text{ Hz}$.
- **Nghịch lý âm học ở Guitar electric ($f_{50} = 549{,}1\text{ Hz}$):** Mặc dù nốt cơ bản của Guitar electric thuộc dải trung-trầm ($130{,}9\text{ Hz}$, tương đương Cello), hiệu ứng méo tiếng (distortion) sinh ra nhiều thành phần họa âm bậc cao và thành phần phi điều hòa, đẩy năng lượng lên dải cao khiến tần số trung vị năng lượng $f_{50}$ đạt mức cao nhất trong 6 nhạc cụ ($549{,}1\text{ Hz}$).

#### 3.2.5. Kết quả Đường bao năng lượng và Mức giảm $D_{0{,}4}$

![Đường bao năng lượng](hinh/4_duong_bao_sau_onset.png)*Hình 3.4: Đường bao năng lượng trung vị của các nốt ngân dài $\ge 0{,}5$ giây.*

- **Nhóm kéo vĩ duy trì năng lượng ổn định:** Sau 0,4 giây kể từ đỉnh, Violin giữ nguyên mức đỉnh ($D_{0{,}4} = 0{,}0\text{ dB}$); Viola và Double Bass chỉ giảm $-1{,}6\text{ dB}$.
- **Nhóm gảy dây suy giảm nhanh:** Guitar acoustic sụt giảm rất mạnh, đạt **$-7{,}1\text{ dB}$** sau 0,4 giây (biên độ giảm còn dưới $44\%$ mức đỉnh). Cello cũng ghi nhận mức giảm **$-7{,}0\text{ dB}$** do trong các bản thu thính phòng URMP, bè cello có nhiều đoạn nghệ sĩ diễn tấu kỹ thuật gảy ngón (pizzicato).
- **Guitar electric chỉ giảm $-1{,}0\text{ dB}$:** Bộ khuếch đại nén biên độ (compressor/limiter) giữ cho mức tín hiệu sau đỉnh không bị tụt nhanh, tạo độ ngân nhân tạo kéo dài.

---

### 3.3. Bảng tổng hợp đối chiếu song song giữa lý thuyết và thực nghiệm

| Nhạc cụ                 | Phương diện 1: Lý thuyết & Đặc tính vật lý                                                                                         | Phương diện 2: Thực nghiệm đo đạc âm học trên 600 file                                                                                                                                                           |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Violin**          | Cỡ nhỏ nhất họ vĩ, dây ngắn và căng; dùng vĩ kéo liên tục; nốt thấp nhất G3 (196 Hz); âm sắc thanh sáng.                 | $f_0$ trung vị đạt **501,3 Hz**; $f_{50} = \mathbf{506,0\text{ Hz}}$; $D_{0{,}4} = \mathbf{0,0\text{ dB}}$ (giữ nguyên năng lượng đỉnh); năng lượng giảm rất mạnh dưới 196 Hz.                |
| **Viola**           | Cấu tạo giống violin nhưng thùng đàn lớn hơn 15%, dây trầm hơn một quãng 5; nốt thấp nhất C3 (130,8 Hz); âm sắc ấm hơn. | $f_0$ trung vị đạt **290,4 Hz**; $f_{50} = \mathbf{355,3\text{ Hz}}$; $D_{0{,}4} = \mathbf{-1,6\text{ dB}}$ (duy trì đều); năng lượng sụt giảm mạnh dưới 130 Hz.                                  |
| **Cello**           | Thùng lớn đặt sàn, dây dài và dày; nốt thấp nhất C2 (65,4 Hz); âm vực trầm ấm; diễn tấu cả kéo vĩ và pizzicato.        | $f_0$ trung vị đạt **157,4 Hz**; $f_{50} = \mathbf{193,8\text{ Hz}}$; $D_{0{,}4} = \mathbf{-7,0\text{ dB}}$ (suy giảm nhanh do chứa nhiều đoạn chơi kỹ thuật pizzicato).                             |
| **Double Bass**     | Nhạc cụ khổng lồ đứng chơi, dây rất dài và nặng; nốt thấp nhất E1 (41,2 Hz); âm vực siêu trầm làm bè đáy.             | $f_0$ trung vị đạt **92,3 Hz**; $f_{50} = \mathbf{107,7\text{ Hz}}$ (thấp nhất); $D_{0{,}4} = \mathbf{-1,6\text{ dB}}$ (kéo vĩ giữ đều); năng lượng dồn chủ yếu dưới 300 Hz.                  |
| **Guitar acoustic** | 6 dây gảy buông, thùng gỗ rỗng cộng hưởng; nốt thấp nhất E2 (82,4 Hz); âm vang mộc, tắt nhanh; thường đệm hợp âm.       | $f_0$ trung vị đạt **117,6 Hz**; $f_{50} = \mathbf{236,9\text{ Hz}}$; $D_{0{,}4} = \mathbf{-7,1\text{ dB}}$ (tắt dốc nhanh); spectrogram xuất hiện vạch dọc xung kích tại lúc gảy.                 |
| **Guitar electric** | 6 dây kim loại thân đặc, thu qua pickup và tầng khuếch đại bão hòa (distortion); nốt thấp nhất E2; tiếng dày, ngân dài.   | $f_0$ trung vị đạt **130,9 Hz**; $f_{50} = \mathbf{549,1\text{ Hz}}$ (cao nhất do họa âm méo tiếng); $D_{0{,}4} = \mathbf{-1,0\text{ dB}}$ (ngân nhân tạo); phổ trải đặc từ 100 Hz đến 8 kHz. |

---

### 3.4. Các trường hợp ngoại lệ và hạn chế của bộ dữ liệu

1. **Hiện tượng Cello suy giảm năng lượng tương đương Guitar:** Mức giảm $D_{0{,}4} = -7{,}0\text{ dB}$ của Cello phản ánh kỹ thuật diễn tấu thực tế: trong các bản nhạc thính phòng URMP, nghệ sĩ cello sử dụng kỹ thuật gảy ngón **pizzicato** ở nhiều phân đoạn. Điều này cho thấy đường bao năng lượng phụ thuộc vào kỹ thuật chơi chứ không chỉ phụ thuộc loại nhạc cụ.
2. **Hiện tượng nhận diện sai cao độ ở Guitar:** Lỗi sub-harmonic của thuật toán pYIN khi phân tích tín hiệu đa âm khiến $p_{10}$ của guitar ghi nhận giá trị dưới $82{,}4\text{ Hz}$.
3. **Số lượng track gốc hạn chế ở Double Bass:** 100 file double bass được trích xuất từ 6 track gốc (2 URMP và 4 PHENICX), do đó phải cho phép chọn các đoạn liền kề để bảo đảm đủ quy mô mẫu.
4. **Độ dài cố định của Guitar electric:** Dữ liệu Medley-solos-DB được cắt sẵn ở độ dài $2{,}97\text{ s}$ nên không được cắt theo ranh giới nốt Onset như các nhạc cụ còn lại.
5. **Nhiễu ù tần số thấp:** Các bản thu URMP có một lượng nhỏ tạp âm ù điện tần số thấp (dưới $60\text{ Hz}$) từ nguồn điện phòng thu.
6. **Mức độ kiểm chứng thủ công:** Quy trình tiền xử lý 11 bước đã áp dụng các bộ lọc tự động theo ngưỡng biên độ, Onset và hệ số tương quan để lọc nhiễu và loại bản thu trùng; tuy nhiên việc nghe kiểm âm thủ công toàn bộ 600 tệp chưa được thực hiện toàn diện. Vì vậy, một số tệp (nhất là các đoạn guitar điện từ Medley-solos-DB) vẫn có thể còn rò rỉ âm thanh nhỏ từ phòng thu hoặc mạch khuếch đại.

---

### 3.5. Ý nghĩa

Từ các kết quả phân tích lý thuyết và thực nghiệm:

- Không thể sử dụng một đặc trưng đơn lẻ nào để nhận diện hoặc truy hồi âm thanh nhạc cụ: cao độ $f_0$ bị chồng lấn âm vực; đường bao năng lượng bị biến động theo kỹ thuật kéo/gảy; phổ tần số bị tác động bởi hiệu ứng khuếch đại điện tử.
- Các chỉ số đo đạc ở Chương 3 ($f_0$ pYIN, $f_{50}$, $D_{0{,}4}$) đòi hỏi các điều kiện ngặt nghèo (phải có nốt ngân đơn lẻ $\ge 0{,}5\text{ s}$, phải là giai điệu đơn âm). Trong hệ thống CBAR thực tế, đoạn âm thanh truy vấn của người dùng có thể là bất kỳ đoạn nhạc phức tạp nào.

Do đó,  cần thiết kế một **không gian vector đặc trưng đa chiều cố định**, kết hợp cả 3 khía cạnh: **Màu âm bao phổ (MFCC, Spectral Roll-off)**, **Động học năng lượng thời gian (RMS, ZCR)** và **Cấu trúc cao độ hòa âm (Spectral Centroid, Chroma STFT)**.

---

## CHƯƠNG 4: NHIỆM VỤ 2 - XÂY DỰNG BỘ ĐẶC TRƯNG VÀ THIẾT KẾ ĐỘ TƯƠNG ĐỒNG CHO CBAR

### 4.1. Mục tiêu và kiến trúc bộ đặc trưng tìm kiếm

#### 4.1.1. Thách thức kỹ thuật và mục tiêu bài toán

Dữ liệu âm thanh đầu vào là chuỗi tín hiệu thời gian $x[n]$ phi cấu trúc và có độ dài biến thiên ($2{,}5\text{ s}$ đến $3{,}5\text{ s}$, tương ứng $55\,125$ đến $77\,175$ mẫu). Máy tính không thể tính khoảng cách trực tiếp giữa hai chuỗi có kích thước khác nhau.

Mục tiêu của Nhiệm vụ 2 :

1. **Rút gọn chiều dữ liệu (Dimensionality Reduction):** Chuyển đổi mỗi đoạn âm thanh thành một vector số thực cố định $\mathbf{v} \in \mathbb{R}^D$ có kích thước nhỏ gọn, thuận tiện cho việc lưu trữ trong CSDL và tối ưu hóa tốc độ tính khoảng cách truy vấn.
2. **Bảo đảm hai yêu cầu đối nghịch nhưng bổ trợ của hệ thống CBAR:**
   - **Tìm kiếm sự tương đồng (Similarity Search):** Các tệp có cùng loại nhạc cụ, cùng cơ chế kích âm hoặc cùng màu sắc âm học phải có khoảng cách vector nhỏ trong không gian đặc trưng.
   - **Phân biệt sự khác biệt (Instrument Discrimination):** Các tệp thuộc các lớp nhạc cụ khác nhau phải có khoảng cách đủ xa, ngay cả khi chúng có dải cao độ trùng lặp (như Viola và Cello ở $190 - 200\text{ Hz}$) hoặc có mức suy giảm năng lượng tương đương (như Acoustic Guitar và Cello pizzicato ở $D_{0{,}4} \approx -7\text{ dB}$).

#### 4.1.2. Kiến trúc 3 bộ đặc trưng đa góc nhìn

Hệ thống thiết kế cấu trúc phân tầng gồm **3 bộ đặc trưng (6 nhóm toán học)**, bao quát 3 trục phân hóa âm học cơ bản:

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           HỆ THỐNG ĐẶC TRƯNG TRUY HỒI CBAR (58 CHIỀU)                   │
├─────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│   BỘ A: ÂM SẮC / BAO PHỔ    │     BỘ B: NĂNG LƯỢNG /      │    BỘ C: TRỌNG TÂM PHỔ      │
│      (Spectral Timbre)      │     ĐỘNG HỌC THỜI GIAN      │      / HÒA ÂM CAO ĐỘ        │
│          [28 chiều]         │          [4 chiều]          │         [26 chiều]          │
├─────────────────────────────┼─────────────────────────────┼─────────────────────────────┤
│ 1. MFCC (13 hệ số × 2)      │ 3. RMS Energy (1 GT × 2)    │ 5. Spectral Centroid        │
│    - Bản chất: Mô hình      │    - Bản chất: Năng lượng   │    (1 GT × 2)               │
│      nguồn - bộ lọc; bóc    │      hiệu dụng khung; đường │    - Bản chất: Momen phổ    │
│      tách bao phổ âm sắc   │      bao biên độ ADSR       │      bậc 1; cảm nhận trực   │
│    - Vai trò: Tách nhạc cụ  │    - Vai trò: Tách Kéo vĩ   │      giác về "độ sáng/tối"  │
│      mộc và guitar điện;    │      (bền vững) vs Gảy dây  │    - Vai trò: Phân tầng kích│
│      nhận diện màu âm       │      (suy giảm dốc nhanh)   │      thước thùng họ vĩ      │
│ 2. Spectral Roll-off        │ 4. Zero-Crossing Rate (ZCR) │ 6. Chroma STFT              │
│    (1 GT × 2)               │    (1 GT × 2)               │    (12 lớp cao độ × 2)      │
│    - Bản chất: Tần số giới  │    - Bản chất: Tần suất đổi │    - Bản chất: Gập phổ về   │
│      hạn chứa 85% năng      │      dấu sóng; độ nhám và   │      12 nửa cung chuẩn nhạc │
│      lượng phổ STFT         │      méo tín hiệu           │      lý độc lập quãng tám   │
│    - Vai trò: Tách nhạc cụ  │    - Vai trò: Nhận diện méo │    - Vai trò: Xu hướng phân │
│      siêu trầm (Double Bass)│      tiếng distortion guitar│      bố năng lượng nốt nhạc │
│      khỏi dải cao           │      điện; bắt xước vĩ      │      và vòng hòa âm         │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

### 4.2. Chi tiết ba bộ đặc trưng: Từ cơ sở lý thuyết đến ứng dụng CBAR

#### 4.2.1. Bộ A: Âm sắc và hình dạng bao phổ (Spectral Timbre & Spectral Envelope)

##### 1. Hệ số Cepstral thang Mel (Mel-Frequency Cepstral Coefficients - MFCC)

- **Cơ sở lý thuyết và bản chất toán học:**
  - *Mô hình Nguồn - Bộ lọc (Source-Filter Model):* Tín hiệu âm thanh nhạc cụ bộ dây được mô hình hóa qua phép chập giữa tín hiệu nguồn dao động dây $e(t)$ (chuỗi xung tuần hoàn với tần số cơ bản $f_0$ và các họa âm) và đáp ứng xung của thùng đàn $h(t)$ (bộ lọc âm học định hình các đỉnh formant): $s(t) = e(t) * h(t) \iff |S(f)| = |E(f)| \cdot |H(f)|$.
  - *Ngân hàng bộ lọc Mel (Mel Filter Bank):* Mô phỏng cơ chế cảm thụ phi tuyến của màng đáy ốc tai người qua thang tần số Mel:

    $$
    m(f) = 2595 \log_{10} \left(1 + \frac{f}{700}\right)
    $$

    Phổ công suất $P(m, k) = |X(m, k)|^2$ được gom qua ngân hàng $M = 40$ bộ lọc tam giác Mel gối nhau:

    $$
    E_{\text{Mel}}(m, i) = \sum_{k=0}^{N/2} P(m, k) \cdot H_i(k), \quad i = 0, 1, \dots, M-1
    $$
  - *Nén Logarit và biến đổi Cosine rời rạc (DCT-II):* Lấy logarit biến tích thành tổng: $\log E_{\text{Mel}} \approx \log |E_{\text{Mel}}| + \log |H_{\text{Mel}}|$. Biến đổi DCT-II sau đó giải tương quan và chuyển đổi về miền quefrency:

    $$
    c_q(m) = \sqrt{\frac{2}{M}} \sum_{i=0}^{M-1} \log\big(E_{\text{Mel}}(m, i) + 10^{-9}\big) \cos\left[ \frac{\pi q}{M} \left(i + \frac{1}{2}\right) \right], \quad q = 0, 1, \dots, 12
    $$
  - *Giá trị thông tin của 13 hệ số đầu ($c_0 - c_{12}$):* Các biến thiên chậm của phổ (đường bao phổ $|H(f)|$ phản ánh màu âm thùng đàn) tập trung ở các hệ số thấp; các biến thiên nhanh (các đỉnh nhọn họa âm nốt nhạc) nằm ở các hệ số cao và bị lược bỏ. Hệ số $c_0$ tỷ lệ với năng lượng logarit trung bình.
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* So khớp các tệp có cùng dạng đường bao phổ formant của thùng đàn, bất kể nốt nhạc cụ thể đang chơi.
  - *Tìm sự khác biệt:* Tách biệt Guitar điện (đường bao phổ bị xén phẳng do méo tiếng) khỏi 5 nhạc cụ mộc; hỗ trợ phân biệt xu hướng đường bao phổ giữa các nhạc cụ họ vĩ.
  - *Giới hạn:* MFCC mô tả hình thái đường bao phổ trên thang Mel, phản ánh âm sắc tổng thể nhưng không thể dùng để suy ngược chính xác kích thước hình học cụ thể hay thể tích thùng đàn. MFCC cũng không đủ để phân biệt mọi cặp nhạc cụ (ví dụ giữa các nhạc cụ cùng họ chơi ở cùng cao độ), cần kết hợp với các đặc trưng động học và cao độ.

##### 2. Tần số cuộn phổ (Spectral Roll-off)

- **Cơ sở lý thuyết và bản chất toán học:**
  - Tần số cuộn phổ $R_{0{,}85}(m)$ là tần số ngưỡng mà $85\%$ tổng năng lượng của phổ công suất trong khung $m$ tập trung phía dưới nó:
    $$
    R_{0{,}85}(m) = \min \left\{ f_r \in \left[0, \frac{f_s}{2}\right] : \sum_{k: f_k \le f_r} P(m, k) \ge 0{,}85 \sum_{k=0}^{N/2} P(m, k) \right\}
    $$
  - Phản ánh độ dốc suy giảm phổ (Spectral Decay / Tilt) và giới hạn trên của dải tần số phát xạ âm thanh hiệu dụng.
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* Nhóm các tệp có cùng giới hạn dải tần phát xạ hiệu dụng.
  - *Tìm sự khác biệt:* Tách biệt Double Bass (năng lượng dồn dưới $300\text{ Hz}$, $R_{0{,}85} < 1000\text{ Hz}$) với các nhạc cụ dải cao như Violin ($R_{0{,}85} > 3000\text{ Hz}$); ghi nhận dải họa âm mở rộng của Guitar điện ($R_{0{,}85} > 4000\text{ Hz}$).

---

#### 4.2.2. Bộ B: Năng lượng và động học thời gian (Energy Dynamics & Temporal Envelope)

##### 3. Năng lượng hiệu dụng biên độ (RMS Energy)

- **Cơ sở lý thuyết và bản chất toán học:**
  - Căn bậc hai trung bình bình phương biên độ khung: $\operatorname{RMS}(m) = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x_m[n]^2}$.
  - Chuỗi $\operatorname{RMS}(m)$ theo thời gian phản ánh đường bao biên độ (Amplitude Envelope) qua mô hình ADSR (Attack - Decay - Sustain - Release).
  - Dao động cưỡng bức liên tục (kéo vĩ) tạo ra pha Sustain ổn định, độ biến thiên RMS thấp; dao động tự do (gảy buông) tạo đỉnh nhọn Attack rồi suy giảm dốc, độ biến thiên RMS cao.
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* Nhóm các tệp có cùng mật độ năng lượng và phong cách diễn tấu (ngân nga legato hay ngắt rời staccato).
  - *Tìm sự khác biệt:* Là chỉ số quan trọng phân biệt cơ chế Kéo vĩ (độ lệch chuẩn $\sigma_{\text{RMS}}$ nhỏ, $D_{0{,}4} \approx 0\text{ dB}$) và Gảy dây (độ lệch chuẩn $\sigma_{\text{RMS}}$ lớn, $D_{0{,}4} = -7{,}1\text{ dB}$ ở Acoustic Guitar); nhận diện kỹ thuật gảy ngón pizzicato ở Cello.

##### 4. Tốc độ qua điểm không (Zero-Crossing Rate - ZCR)

- **Cơ sở lý thuyết và bản chất toán học:**
  - Tỷ lệ số lần tín hiệu đổi dấu giữa hai mẫu kế tiếp:
    $$
    \operatorname{ZCR}(m) = \frac{1}{2(N-1)} \sum_{n=1}^{N-1} \big| \operatorname{sgn}(x_m[n]) - \operatorname{sgn}(x_m[n-1]) \big|
    $$
  - Với sóng sin thuần túy, $\operatorname{ZCR} \approx 2 f_0 / f_s$. Với tín hiệu nhạc cụ thực tế, ZCR nhạy bén với các thành phần dao động ký sinh tần số cao, tiếng ồn ma sát cơ học (tiếng rít nhựa thông lông vĩ) và hiện tượng méo cắt đỉnh biên độ (clipping).
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* Nhận diện các bản ghi có cùng độ nhám hoặc độ mịn của dạng sóng.
  - *Tìm sự khác biệt:* Tách biệt Guitar điện distortion (sóng bị xén vuông hóa làm ZCR tăng vọt) khỏi các nhạc cụ mộc; ghi nhận giá trị ZCR rất thấp ở các nhạc cụ siêu trầm như Double Bass và Cello.
  - *Giới hạn:* ZCR là một chỉ báo phụ trợ, không thể dùng làm tiêu chí duy nhất để kết luận nhãn nhạc cụ.

---

#### 4.2.3. Bộ C: Trọng tâm phổ và phân bố cao độ (Spectral Centroid & Chroma STFT)

##### 5. Trọng tâm phổ (Spectral Centroid)

- **Cơ sở lý thuyết và bản chất toán học:**
  - Momen bậc 1 của phổ tần số (tâm khối hình học phổ):
    $$
    C(m) = \frac{\sum_{k=0}^{N/2} f_k \cdot P(m, k)}{\sum_{k=0}^{N/2} P(m, k) + 10^{-9}}
    $$
  - Trong tâm lý thính giác (Psychoacoustics), Spectral Centroid tương quan thuận chặt chẽ với cảm nhận trực giác của con người về **"độ sáng" (Brightness)** của âm thanh.
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* Nhóm các âm thanh có cùng cảm nhận về độ sáng/độ tối vào gần nhau.
  - *Tìm sự khác biệt:* Phản ánh xu hướng phân cấp độ sáng phổ giữa các nhạc cụ họ vĩ ($\text{Double Bass} < \text{Cello} < \text{Viola} < \text{Violin}$); vạch rõ sự khác biệt giữa cao độ cơ bản $f_0$ và độ sáng phổ ở Guitar điện.

##### 6. Đặc trưng Chroma (Pitch Class Profile - 12 lớp cao độ)

- **Cơ sở lý thuyết và bản chất toán học:**
  - Hệ âm nhạc bình quân chia quãng tám thành 12 nửa cung: $\text{C, C\#, D, D\#, E, F, F\#, G, G\#, A, A\#, B}$.
  - Dựa trên hiện tượng tương đương quãng tám (Octave Equivalence), toàn bộ các bin tần số $k$ trong STFT được ánh xạ sang nốt MIDI $p(k) = \operatorname{round}(12 \log_2 (f_k/440)) + 69$, sau đó lấy modulo 12 để gập về 12 nửa cung:

    $$
    \operatorname{Chr}(m, c) = \sum_{k: p(k) \bmod 12 = c} P(m, k), \quad c \in \{0, 1, \dots, 11\}
    $$

    Vector được chuẩn hóa $\ell_1$: $\widehat{\operatorname{Chr}}(m, c) = \operatorname{Chr}(m, c) / (\sum_{j=0}^{11} \operatorname{Chr}(m, j) + 10^{-9})$.
- **Ứng dụng vào bài toán CBAR:**
  - *Tìm sự tương đồng:* Tìm kiếm các đoạn nhạc có cùng vòng hòa âm hoặc cùng giai điệu độc lập với quãng tám.
  - *Tìm sự khác biệt:* Hỗ trợ phân biệt lối chơi giai điệu đơn âm (họ vĩ có năng lượng Chroma tập trung nhọn) với lối đệm hợp âm đa âm (guitar có năng lượng Chroma phân tán đều ra nhiều bin); tháo gỡ hiện tượng chồng lấn âm vực giữa Viola và Cello.
  - *Giới hạn:* Chroma không phải là công cụ độc lập để kết luận chắc chắn tín hiệu là đơn âm hay đa âm. Khi một nhạc cụ chơi đơn âm, các họa âm bậc cao (như họa âm bậc 3, 5) vẫn có thể rơi vào các bin chroma khác với nốt cơ bản (ví dụ nốt C có họa âm bậc 3 rơi vào bin G và bậc 5 rơi vào bin E), khiến vector Chroma có năng lượng ở nhiều bin.

---

### 4.3. Tổng hợp vector đặc trưng qua Temporal Pooling và phân tích 58 chiều

#### 4.3.1. Kỹ thuật tổng hợp thống kê qua thời gian (Temporal Pooling)

Do số khung $M$ của các file dao động từ 108 đến 151 khung, kỹ thuật Temporal Pooling được áp dụng để rút gọn chuỗi khung thành một vector cố định thông qua hai đại lượng thống kê:

1. **Giá trị trung bình ($\mu_j$):**

   $$
   \mu_j = \frac{1}{M} \sum_{m=1}^M g_j(m)
   $$

   Đại diện cho đặc tính nền, trạng thái tĩnh của âm sắc và độ sáng chủ đạo trong suốt đoạn âm thanh.
2. **Độ lệch chuẩn ($\sigma_j$):**

   $$
   \sigma_j = \sqrt{\frac{1}{M} \sum_{m=1}^M \big(g_j(m) - \mu_j\big)^2}
   $$

   Đại diện cho động thái thời gian (Temporal Dynamics): $\sigma_{\text{RMS}}$ phản ánh độ biến thiên biên độ (kéo vĩ phẳng vs gảy tắt dốc); $\sigma_{\text{MFCC}}$ và $\sigma_{\text{Centroid}}$ phản ánh kỹ thuật rung ngón (vibrato) và sự thay đổi sắc thái; $\sigma_{\text{Chroma}}$ phản ánh tốc độ chuyển dịch nốt nhạc.

*Đánh giá hạn chế:* Việc lấy trung bình và độ lệch chuẩn giúp cố định số chiều biểu diễn, nhưng **làm mất mát thông tin về thứ tự diễn biến thời gian (temporal sequence)**. Hệ thống không phân biệt được đoạn nhạc tăng dần âm lượng (crescendo) với đoạn giảm dần âm lượng (decrescendo).

#### 4.3.2. Cấu trúc chi tiết của không gian vector 58 chiều

- **Bộ A: Âm sắc & Bao phổ (28 chiều):** 13 MFCC $\times 2$ + 1 Roll-off $\times 2$ = 28 chiều.
- **Bộ B: Năng lượng & Động học (4 chiều):** 1 RMS $\times 2$ + 1 ZCR $\times 2$ = 4 chiều.
- **Bộ C: Trọng tâm phổ & Cao độ (26 chiều):** 1 Centroid $\times 2$ + 12 Chroma $\times 2$ = 26 chiều.

$$
\mathbf{v}_{\text{total}} = [\mathbf{v}_A, \mathbf{v}_B, \mathbf{v}_C] \in \mathbb{R}^{28 + 4 + 26} = \mathbb{R}^{58}
$$

| Bộ đặc trưng                                        | Nhóm đặc trưng                 | Số chiều khung | Số chiều sau pooling $(\mu, \sigma)$ | Cơ sở lý thuyết toán học / âm học                                                                                         | Vai trò tìm kiếm tương đồng (Similarity)                                                                   | Vai trò phân biệt nhạc cụ (Discrimination)                                                                                                                                                                                           |
| :------------------------------------------------------ | :--------------------------------- | :--------------: | :--------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bộ A: Âm sắc / Bao phổ** (28 chiều)        | **MFCC**                     |        13        |  **26 chiều** ($c_0 - c_{12}$)  | Mô hình nguồn - bộ lọc; ngân hàng 40 bộ lọc tam giác Mel; biến đổi DCT-II bóc tách đường bao phổ thùng đàn. | Gom các file có cùng cấu trúc đỉnh formant của thùng đàn; nhận diện âm sắc độc lập nốt nhạc.  | Tách Guitar điện (thân đặc, méo tiếng) khỏi 5 nhạc cụ thùng gỗ; hỗ trợ phân biệt sự khác biệt về đường bao phổ giữa các nhạc cụ họ vĩ.                                                                     |
|                                                         | **Spectral Roll-off**        |        1        |            **2 chiều**            | Tần số ngưỡng tích lũy $85\%$ năng lượng phổ STFT; đo độ dốc suy giảm năng lượng dải cao.                    | Nhóm các file có cùng giới hạn dải tần số phát xạ âm thanh hiệu dụng.                               | Tách Double Bass ($< 1000\text{ Hz}$) khỏi các nhạc cụ dải cao; ghi nhận dải họa âm mở rộng của Guitar điện ($> 4000\text{ Hz}$).                                                                                      |
| **Bộ B: Năng lượng / Động học** (4 chiều) | **RMS Energy**               |        1        |            **2 chiều**            | Căn bậc hai trung bình bình phương biên độ; mô hình hóa đường bao ADSR miền thời gian.                           | Nhóm các file có cùng mật độ năng lượng và phong cách diễn tấu (ngân nga hay dồn dập).           | **Phân biệt Kéo vĩ vs Gảy dây:** $\sigma_{\text{RMS}}$ của Kéo vĩ nhỏ (giữ đều); $\sigma_{\text{RMS}}$ của Gảy dây lớn (tắt dốc); nhận diện Cello pizzicato.                                               |
|                                                         | **Zero-Crossing Rate (ZCR)** |        1        |            **2 chiều**            | Tần suất đổi dấu giữa các mẫu biên độ kế tiếp; đo lường độ nhám, độ nhiễu và độ méo sóng.              | Tìm các file có cùng độ mịn sạch hoặc cùng độ thô ráp cơ học của dạng sóng.                    | Ghi nhận tiếng méo bão hòa của Guitar điện (ZCR cao nhất); phân biệt nốt trầm trơn nhẵn (Double Bass, Cello ZCR rất thấp).                                                                                               |
| **Bộ C: Trọng tâm / Cao độ** (26 chiều)     | **Spectral Centroid**        |        1        |            **2 chiều**            | Momen bậc 1 của phổ; đại lượng đo lường cảm nhận thính giác trực giác về "độ sáng" của âm thanh.            | Xếp hạng các âm thanh có cùng cảm nhận độ sáng - tối vào gần nhau trong không gian truy hồi.      | Phân tầng độ sáng phổ giữa các nhạc cụ họ vĩ; hỗ trợ nhận diện Guitar điện (hiệu ứng méo tiếng đẩy năng lượng lên dải cao, tương tự xu hướng $f_{50} = 549{,}1\text{ Hz}$ đo được ở Chương 3). |
|                                                         | **Chroma STFT**              |        12        |           **24 chiều**           | Gập phổ về 12 nửa cung chuẩn nhạc lý phương Tây; tính tương đương quãng tám; chuẩn hóa $\ell_1$.            | Tìm kiếm các đoạn nhạc có cùng hòa âm, điệu thức hoặc chủ đề giai điệu độc lập quãng tám. | Ghi nhận xu hướng phân tán năng lượng: họ vĩ chơi đơn âm (Chroma nhọn); guitar chơi hợp âm (Chroma phân tán); tháo gỡ chồng lấn Viola - Cello.                                                                    |

#### 4.3.3. Ma trận tương hỗ: Cơ chế giải quyết các cặp nhạc cụ thách thức

| Cặp nhạc cụ thách thức                      | Điểm giống nhau gây nhầm lẫn                                                                                                                  |          Bộ đặc trưng đóng vai trò nòng cốt          | Cơ chế giải quyết cụ thể                                                                                                                                                                                                                                                                                                                                                                                                      |
| :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Violin vs. Viola**                    | Cùng thuộc họ vĩ, dáng đàn số 8, cùng kéo vĩ liên tục ($D_{0{,}4}$ đều gần $0\text{ dB}$, $\sigma_{\text{RMS}}$ đều thấp). |      **Bộ C (Centroid)** & **Bộ A (MFCC)**      | Violin có âm vực cao và kích thước nhỏ hơn Viola, do đó năng lượng phổ và Spectral Centroid của Violin dịch về dải tần cao hơn (ở Chương 3, tần số trung vị năng lượng $f_{50}$ của Violin đạt $506{,}0\text{ Hz}$ so với $355{,}3\text{ Hz}$ của Viola). Đồng thời, các hệ số MFCC đầu ghi nhận sự khác biệt về hình thái đường bao phổ giữa hai loại thùng đàn. |
| **2. Viola vs. Cello**                     | Chồng lấn dải cao độ ở vùng $190 - 200\text{ Hz}$ (nốt G3 - G#3 đều có thể chơi trên cả hai đàn).                                |  **Bộ A (MFCC)** & **Bộ C (Centroid, Chroma)**  | Thùng Cello lớn hơn nhiều so với Viola, năng lượng phổ tập trung chủ yếu ở dải trầm (thể hiện qua tần số trung vị năng lượng $f_{50} = 193{,}8\text{ Hz}$ so với $355{,}3\text{ Hz}$ của Viola), kéo Spectral Centroid của Cello xuống thấp hơn. Phân bố Chroma cũng phản ánh sự khác biệt về các nốt dây buông (C2–G2–D3–A3 của Cello vs C3–G3–D4–A4 của Viola).            |
| **3. Cello vs. Double Bass**               | Cùng đảm nhận dải âm trầm của dàn nhạc, âm sắc tối ấm, cùng chơi kéo vĩ.                                                          |    **Bộ A (Roll-off)** & **Bộ C (Centroid)**    | Double Bass tập trung phần lớn năng lượng ở dải siêu trầm (tần số trung vị năng lượng $f_{50} = 107{,}7\text{ Hz}$, $85\%$ năng lượng tập trung dưới $1000\text{ Hz}$), dẫn đến giá trị Spectral Centroid và Roll-off đều rất thấp; trong khi Cello có năng lượng trải rộng hơn ($f_{50} = 193{,}8\text{ Hz}$), giúp hai đặc trưng này phân tách rõ hai nhạc cụ.           |
| **4. Guitar Acoustic vs. Cello Pizzicato** | Cùng có mức suy giảm năng lượng sau $0{,}4\text{ s}$ tương đương nhau ($D_{0{,}4} \approx -7\text{ dB}$).                           |       **Bộ C (Chroma)** & **Bộ A (MFCC)**       | Cello dù gảy ngón (pizzicato) vẫn chủ yếu diễn tấu đơn nốt nên năng lượng Chroma có xu hướng tập trung cục bộ hơn; trong khi Guitar acoustic thường chơi hợp âm hoặc rải ngón nhiều dây, phân tán năng lượng qua nhiều bin Chroma. Ngoài ra, MFCC phản ánh sự khác biệt về đường bao phổ giữa thùng đàn vĩ và guitar.                                                        |
| **5. Guitar Acoustic vs. Guitar Electric** | Cùng có 6 dây kim loại, cùng dùng ngón hoặc móng gảy để kích âm.                                                                      | **Bộ B (RMS, ZCR)** & **Bộ A (Roll-off, MFCC)** | Guitar điện có mạch nén biên độ ($D_{0{,}4} = -1{,}0\text{ dB}$, $\sigma_{\text{RMS}}$ nhỏ) và hiệu ứng distortion làm ZCR có xu hướng cao hơn; Roll-off vươn tới $> 4000\text{ Hz}$. Ngược lại, Guitar acoustic tắt nhanh ($D_{0{,}4} = -7{,}1\text{ dB}$), ZCR thấp và Roll-off suy giảm sớm.                                                                                                 |

---

### 4.4. Chuẩn hóa đặc trưng Z-score và nguyên tắc chống rò rỉ dữ liệu

Các thành phần trong vector 58 chiều có đơn vị và thang đo chênh lệch rất lớn (Roll-off, Centroid lên tới hàng nghìn Hz; MFCC từ $-50$ đến $+100$; RMS, ZCR, Chroma trong khoảng 0 đến 1). Nếu không chuẩn hóa, các đặc trưng có thang đo lớn sẽ chi phối hoàn toàn hàm khoảng cách.

Hệ thống áp dụng chuẩn hóa **Z-score Standard Normalization**:

$$
z_j = \frac{v_j - \mu_j^{(\text{gallery})}}{\sigma_j^{(\text{gallery})} + 10^{-9}}, \quad j = 1, 2, \dots, 58
$$

Trong đó đại lượng $\epsilon = 10^{-9}$ được cộng vào mẫu số để xử lý trường hợp đặc trưng có độ lệch chuẩn bằng 0 (tránh lỗi chia cho 0).

**Nguyên tắc chống rò rỉ dữ liệu (Data Leakage):**
Tham số chuẩn hóa $\mu_j^{(\text{gallery})}$ và $\sigma_j^{(\text{gallery})}$ **chỉ được tính toán một lần trên tập dữ liệu cơ sở (Gallery)**. Khi tiếp nhận một tệp truy vấn mới (Query), vector đặc trưng của tệp truy vấn phải được chuẩn hóa bằng chính các tham số $\mu^{(\text{gallery})}, \sigma^{(\text{gallery})}$ đã lưu sẵn; không tính gộp tệp truy vấn vào tập dữ liệu để tính lại giá trị trung bình và độ lệch chuẩn, nhằm tránh hiện tượng rò rỉ dữ liệu (Data Leakage).

---

### 4.5. Độ đo khoảng cách chuẩn hóa và cơ chế xếp hạng Top-5 file giống nhất

#### 4.5.1. Xử lý nguy cơ mất cân bằng số chiều giữa các nhóm (Dimensional Dominance)

Nếu tính khoảng cách Euclidean trực tiếp trên từng nhóm:

- Nhóm A có $\dim_A = 28$ chiều.
- Nhóm B có $\dim_B = 4$ chiều.
- Nhóm C có $\dim_C = 26$ chiều.

Về mặt xác suất, kỳ vọng độ lớn khoảng cách Euclidean của một nhóm tỷ lệ thuận với căn bậc hai số chiều: $\mathbb{E}[d_k] \propto \sqrt{\dim_k}$. Do đó, khoảng cách của nhóm A tự nhiên sẽ lớn hơn khoảng cách của nhóm B khoảng $\sqrt{28/4} \approx 2{,}65$ lần. Nếu gộp trực tiếp có trọng số, nhóm 28 chiều sẽ lấn át nhóm 4 chiều bất kể vai trò vật lý của nhóm B rất quan trọng.

Để khắc phục hiện tượng này, hệ thống áp dụng **khoảng cách Euclidean chuẩn hóa theo số chiều (Root-Mean-Square Distance - RMSD)** cho từng nhóm:

$$
d_k^*(\mathbf{q}_k, \mathbf{x}_k) = \sqrt{\frac{1}{\dim_k} \sum_{j=1}^{\dim_k} (q_{k,j} - x_{k,j})^2}, \quad k \in \{A, B, C\}
$$

Phép chia cho $\dim_k$ đưa khoảng cách trung bình trên mỗi chiều của cả 3 nhóm về cùng một bậc thang đo, bảo đảm tính công bằng.

#### 4.5.2. Khoảng cách tổng hợp có trọng số

Khoảng cách tổng hợp giữa vector truy vấn $\mathbf{q}$ và vector ứng viên $\mathbf{x}$ trong CSDL là:

$$
d_{\text{total}}(\mathbf{q}, \mathbf{x}) = \lambda_1 d_A^*(\mathbf{q}_A, \mathbf{x}_A) + \lambda_2 d_B^*(\mathbf{q}_B, \mathbf{x}_B) + \lambda_3 d_C^*(\mathbf{q}_C, \mathbf{x}_C)
$$

với điều kiện ràng buộc:

$$
\lambda_1 + \lambda_2 + \lambda_3 = 1, \quad \lambda_i \ge 0
$$

- $\lambda_1$: Trọng số nhóm Âm sắc & Bao phổ (Bộ A).
- $\lambda_2$: Trọng số nhóm Năng lượng & Động học thời gian (Bộ B).
- $\lambda_3$: Trọng số nhóm Trọng tâm phổ & Cao độ hòa âm (Bộ C).

*Nguyên tắc xác định trọng số:* Không có bộ trọng số nào là tối ưu tiên nghiệm cho mọi bài toán. Các giá trị trọng số $\boldsymbol{\lambda}$ cần được khảo sát và tinh chỉnh bằng thực nghiệm trên tập kiểm thực (Validation Set), không được tự ý kết luận khi chưa có số liệu đánh giá.

#### 4.5.3. Quy trình tìm kiếm Top-5 và xử lý truy vấn

Quy trình thực thi khi tiếp nhận một tệp âm thanh truy vấn mới:

1. Nhận tệp âm thanh truy vấn $x_{\text{query}}(t)$.
2. Tiền xử lý: chuyển mono, đổi tần số mẫu về $22\,050\text{ Hz}$, chuẩn hóa biên độ đỉnh về 0,9.
3. Trích xuất vector 58 chiều $\mathbf{q} \in \mathbb{R}^{58}$ theo cùng thuật toán trích xuất đặc trưng.
4. Chuẩn hóa Z-score vector $\mathbf{q}$ bằng bộ tham số $\mu^{(\text{gallery})}, \sigma^{(\text{gallery})}$.
5. Tính khoảng cách có trọng số $d_{\text{total}}(\mathbf{q}, \mathbf{x}^{(i)})$ tới từng tệp trong cơ sở dữ liệu.
6. **Xử lý tệp truy vấn nằm trong CSDL (Leave-One-Out):** Nếu tệp truy vấn chính là một tệp đã có trong CSDL (khoảng cách $d = 0$), tệp này phải được loại bỏ khỏi danh sách trước khi xếp hạng để tránh kết quả tầm thường.
7. Sắp xếp danh sách tệp còn lại theo khoảng cách tăng dần:
   $$
   d_{(1)} \le d_{(2)} \le d_{(3)} \le d_{(4)} \le d_{(5)} \le \dots
   $$
8. Trả về **Top-5** tệp có khoảng cách nhỏ nhất (tương đồng nhất theo độ đo).

*Lưu ý khoa học:* Năm tệp trả về là 5 tệp có khoảng cách vector nhỏ nhất theo không gian đặc trưng đã thiết kế, không đồng nghĩa chắc chắn rằng đó là 5 tệp hoàn toàn chính xác về mặt ngữ nghĩa hoặc cùng loại nhạc cụ trong mọi trường hợp.

---

### 4.6. Đề xuất phương pháp luận đánh giá hệ thống tìm kiếm cho Nhiệm vụ 4

Do đề tài hiện tại mới hoàn thành Nhiệm vụ 1 và Nhiệm vụ 2, phần đánh giá hệ thống dưới đây được xây dựng dưới dạng **đề xuất phương pháp luận và khung thử nghiệm chuẩn mực** để triển khai trong Nhiệm vụ 4:

#### 4.6.1. Chiến lược phân chia dữ liệu chống rò rỉ nguồn (Source-wise Splitting)

Trong bộ dữ liệu 600 tệp, nhiều tệp được cắt từ cùng một track nguồn gốc (ví dụ các đoạn cắt từ cùng một tác phẩm của URMP). Nếu chia tập ngẫu nhiên theo từng tệp (File-wise Random Splitting), một đoạn của track có thể nằm ở tập Gallery và một đoạn khác của chính track đó nằm ở tập Query. Khi đó, hệ thống sẽ nhận diện lại bản nhạc/nghệ sĩ cụ thể thay vì đánh giá khả năng nhận diện âm thanh nhạc cụ nói chung, gây ra hiện tượng rò rỉ thông tin bản thu (Track Bleed / Source Leakage).

$\to$ **Giải pháp:** Phải phân chia dữ liệu theo **bản ghi nguồn độc lập (Source-wise Splitting)**:

- Tập Gallery (Tham chiếu): Chiếm khoảng $70\% - 80\%$ số track gốc của mỗi nhạc cụ.
- Tập Query (Kiểm thử): Chiếm khoảng $20\% - 30\%$ số track gốc còn lại, bảo đảm hoàn toàn độc lập về bản thu và nghệ sĩ diễn tấu.

#### 4.6.2. Tiêu chí xác định độ liên quan (Relevance Criterion)

Một tệp trong danh sách trả về được coi là liên quan (Relevant) với tệp truy vấn nếu:

- **Tiêu chí nghiêm ngặt (Strict Relevance):** Tệp trả về có cùng nhãn nhạc cụ với tệp truy vấn (ví dụ: Query là Violin thì chỉ các tệp Violin mới được tính là đúng).
- **Tiêu chí mở rộng (Family Relevance):** Tệp trả về cùng phân họ kích âm (kéo vĩ hoặc gảy dây) hoặc cùng dải âm vực gần gũi.

#### 4.6.3. Các chỉ số đánh giá truy hồi đề xuất

1. **Độ chính xác Top-5 (Precision@5):**

   $$
   \text{Precision@5} = \frac{\text{Số tệp liên quan trong Top-5}}{5}
   $$

   Chỉ số trung bình $\text{Mean Precision@5}$ được tính qua toàn bộ các tệp truy vấn trong tập kiểm thử.
2. **Mean Average Precision (MAP@5):**
   Đánh giá cả thứ tự xếp hạng của các kết quả đúng (kết quả đúng xuất hiện ở vị trí Top-1 được tính điểm cao hơn Top-5):

   $$
   \text{AP@5} = \frac{1}{\min(R, 5)} \sum_{k=1}^5 P(k) \cdot \operatorname{rel}(k)
   $$

   trong đó $P(k)$ là độ chính xác tại vị trí cắt $k$, $\operatorname{rel}(k) \in \{0, 1\}$ là chỉ thị tính liên quan của tệp thứ $k$, và $R$ là tổng số tệp liên quan có trong cơ sở dữ liệu.

---

## CHƯƠNG 5: KẾT LUẬN VÀ KẾ HOẠCH TRIỂN KHAI TIẾP THEO

### 5.1. Tổng kết kết quả Nhiệm vụ 1 và Nhiệm vụ 2

1. **Về Nhiệm vụ 1 (Xây dựng dữ liệu và phân tích đặc điểm):**
   - Đã thu thập và chuẩn hóa thành công bộ dữ liệu chuẩn gồm **600 tệp âm thanh WAV** (22 050 Hz, mono, PCM 16-bit), phân bổ cân bằng 100 tệp/lớp cho 6 nhạc cụ bộ dây (Violin, Viola, Cello, Double Bass, Acoustic Guitar, Electric Guitar), vượt quy mô tối thiểu đề bài yêu cầu ($\ge 500$ tệp).
   - Thiết lập quy trình 11 bước xử lý tự động: cắt nốt bằng spectral flux kết hợp backtracking, lọc bỏ 18 track trùng lặp bằng tương quan Pearson, loại bỏ các đoạn trùng lặp âm nhạc bằng dấu vân tay Mel và fade mép 50 ms khử click.
   - Phân tích toàn diện điểm giống và khác nhau của tiếng 6 nhạc cụ trên cả phương diện lý thuyết vật lý và số liệu đo đạc thực nghiệm ($f_0$ pYIN, $f_{50}$, $D_{0{,}4}$, Spectrogram).
2. **Về Nhiệm vụ 2 (Thiết kế bộ đặc trưng và mô hình tương đồng):**
   - Thiết kế hệ thống 3 bộ đặc trưng (gồm 6 nhóm toán học: MFCC, Spectral Roll-off, RMS Energy, ZCR, Spectral Centroid, Chroma STFT) bao quát 3 trục phân hóa âm học cơ bản.
   - Xây dựng giải pháp biểu diễn cố định **58 chiều** thông qua kỹ thuật Temporal Pooling (giá trị trung bình và độ lệch chuẩn).
   - Xây dựng công thức khoảng cách Euclidean chuẩn hóa theo số chiều (RMSD) kết hợp trọng số và chuẩn hóa Z-score chống rò rỉ dữ liệu, đề xuất quy trình xếp hạng Top-5 và khung phương pháp luận đánh giá hiệu năng truy hồi cho Nhiệm vụ 4.

---

### 5.2. Các hạn chế thực tế của hệ thống

Báo cáo thẳng thắn chỉ ra các hạn chế kỹ thuật thực tế cần lưu ý:

1. **Hạn chế về tính đa dạng của nguồn dữ liệu:** Nhạc cụ Double Bass có số lượng track gốc hạn chế (chỉ 6 track) nên phải cho phép chọn các đoạn liền kề; dữ liệu Guitar electric cắt sẵn từ Medley-solos-DB có thể tồn tại rò rỉ âm thanh nhẹ từ dàn nhạc nền.
2. **Hạn chế của vector thống kê tĩnh:** Việc tổng hợp chuỗi khung qua $(\mu, \sigma)$ làm mất mát thông tin về trật tự thời gian và cấu trúc câu nhạc.
3. **Độ nhạy cảm của hàm khoảng cách:** Kết quả truy hồi Top-5 phụ thuộc vào việc lựa chọn bộ trọng số $\boldsymbol{\lambda}$. Trọng số này cần được tối ưu hóa bằng thực nghiệm thay vì gán giá trị cố định.
4. **Khả năng tổng quát hóa:** Hệ thống được thiết kế và kiểm thử trên 6 lớp nhạc cụ bộ dây cụ thể; hiệu năng khi tiếp nhận các nhạc cụ ngoài tập danh mục (Out-of-Distribution) cần được kiểm chứng thêm.
5. **Chưa kiểm âm thủ công toàn diện:** Bộ dữ liệu được xây dựng hoàn toàn bằng quy trình lọc tự động; việc xác minh thủ công bằng tai nghe trên toàn bộ 600 tệp chưa được thực hiện toàn diện.

---

### 5.3. Kế hoạch thực hiện Nhiệm vụ 3 và Nhiệm vụ 4

Các công việc tiếp theo để hoàn thiện toàn bộ bài tập lớn:

- **Nhiệm vụ 3:**
  - Viết kịch bản Python tự động trích xuất vector 58 chiều cho toàn bộ 600 tệp trong cơ sở dữ liệu.
  - Thiết kế bảng cơ sở dữ liệu quan hệ (SQLite) hoặc sử dụng thư viện chỉ mục vector chuyên dụng (như FAISS) để quản lý vector đặc trưng và siêu dữ liệu tệp, tối ưu hóa tốc độ tìm kiếm.
- **Nhiệm vụ 4:**
  - Xây dựng module tìm kiếm tương đồng Top-5 theo công thức khoảng cách chuẩn hóa có trọng số.
  - Phân chia tập dữ liệu theo track nguồn độc lập (Source-wise Splitting) và tiến hành thực nghiệm đo đạc các chỉ số đánh giá $\text{Precision@5}$ và $\text{MAP@5}$.
  - Xây dựng giao diện demo tương tác trực quan (Web UI bằng Streamlit hoặc Gradio) cho phép người dùng tải lên tệp âm thanh mẫu, nghe thử kết quả truy xuất và xem biểu đồ khoảng cách tương đồng.

---

## Tài liệu tham khảo

1. **B. Li, X. Liu, K. Dinesh, Z. Duan, G. Sharma**, *"Creating a multitrack classical music performance dataset for multimodal music analysis: Challenges, insights, and applications"*, IEEE Transactions on Multimedia, vol. 21, no. 2, pp. 522–535, 2019. (Bộ dữ liệu URMP, DOI: [10.1109/TMM.2018.2856094](https://doi.org/10.1109/TMM.2018.2856094)).
2. **M. Miron, J. Carabias-Orti, J. Bosch, E. Gómez, J. Janer**, *"Score-informed source separation for multichannel orchestral recordings"*, Journal of Electrical and Computer Engineering, vol. 2016, Article ID 8363507, 2016. (Bộ dữ liệu PHENICX-Anechoic, DOI: [10.1155/2016/8363507](https://doi.org/10.1155/2016/8363507)).
3. **J. Pätynen, V. Pulkki, T. Lokki**, *"Anechoic recording system for symphony orchestra"*, Acta Acustica united with Acustica, vol. 94, no. 6, pp. 856–865, 2008. (DOI: [10.3813/AAA.918108](https://doi.org/10.3813/AAA.918108)).
4. **Q. Xi, R. Bittner, J. Pauwels, X. Ye, J. P. Bello**, *"GuitarSet: A dataset for guitar transcription"*, in Proc. of the 19th International Society for Music Information Retrieval Conference (ISMIR), Paris, France, pp. 453–460, 2018.
5. **V. Lostanlen, C.-E. Cella**, *"Deep convolutional networks on the pitch spiral for musical instrument recognition"*, in Proc. of the 17th International Society for Music Information Retrieval Conference (ISMIR), New York, USA, pp. 612–618, 2016. (Bộ dữ liệu Medley-solos-DB).
6. **J. J. Bosch, J. Janer, F. Fuhrmann, P. Herrera**, *"A comparison of sound segregation techniques for predominant instrument recognition in musical audio signals"*, in Proc. of the 13th International Society for Music Information Retrieval Conference (ISMIR), Porto, Portugal, pp. 559–564, 2012. (Bộ dữ liệu IRMAS).
7. **A. de Cheveigné, H. Kawahara**, *"YIN, a fundamental frequency estimator for speech and music"*, Journal of the Acoustical Society of America, vol. 111, no. 4, pp. 1917–1930, 2002. (DOI: [10.1121/1.1458024](https://doi.org/10.1121/1.1458024)).
8. **M. Mauch, S. Dixon**, *"pYIN: A fundamental frequency estimator using probabilistic threshold distributions"*, in Proc. of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Florence, Italy, pp. 659–663, 2014. (DOI: [10.1109/ICASSP.2014.6853678](https://doi.org/10.1109/ICASSP.2014.6853678)).
9. **S. Böck, F. Krebs, M. Schedl**, *"Evaluating the online capabilities of onset detection methods"*, in Proc. of the 13th International Society for Music Information Retrieval Conference (ISMIR), Porto, Portugal, pp. 49–54, 2012.
10. **B. McFee, C. Raffel, D. Liang, D. P. Ellis, M. McVicar, E. Battenberg, O. Nieto**, *"librosa: Audio and music signal analysis in Python"*, in Proc. of the 14th Python in Science Conference (SciPy), Austin, Texas, pp. 18–25, 2015. (DOI: [10.25080/Majora-7b98e3ed-003](https://doi.org/10.25080/Majora-7b98e3ed-003)).
11. **M. Müller**, *"Fundamentals of Music Processing: Audio, Analysis, Algorithms, Applications"*, Springer International Publishing, Cham, Switzerland, 2015. (ISBN: 978-3-319-21944-8).
