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
2. [CHƯƠNG 2: NHIỆM VỤ 1 - XÂY DỰNG VÀ KIỂM CHỨNG BỘ DỮ LIỆU ÂM THANH](#chương-2-nhiệm-vụ-1---xây-dựng-và-kiểm-chứng-bộ-dữ-liệu-âm-thanh)
   - 2.1. [Yêu cầu đề bài và tiêu chí kỹ thuật của bộ dữ liệu](#21-yêu-cầu-đề-bài-và-tiêu-chí-kỹ-thuật-của-bộ-dữ-liệu)
   - 2.2. [Lựa chọn nhạc cụ và giới thiệu từng nhạc cụ](#22-lựa-chọn-nhạc-cụ-và-giới-thiệu-từng-nhạc-cụ)
   - 2.3. [Các bộ dữ liệu được sử dụng, cấu trúc dữ liệu thô và phạm vi nhãn](#23-các-bộ-dữ-liệu-được-sử-dụng-cấu-trúc-dữ-liệu-thô-và-phạm-vi-nhãn)
   - 2.4. [Quy trình tiền xử lý và lọc dữ liệu 11 bước](#24-quy-trình-tiền-xử-lý-và-lọc-dữ-liệu-11-bước)
   - 2.5. [Kiểm chứng bộ dữ liệu đạt chuẩn kỹ thuật đề bài (600 file)](#25-kiểm-chứng-bộ-dữ-liệu-đạt-chuẩn-kỹ-thuật-đề-bài-600-file)
3. [CHƯƠNG 3: NHIỆM VỤ 1 - MÔ TẢ ĐẶC ĐIỂM GIỐNG VÀ KHÁC NHAU DỰA TRÊN CÁC ĐẶC TRƯNG ÂM HỌC](#chương-3-nhiệm-vụ-1---mô-tả-đặc-điểm-giống-và-khác-nhau-dựa-trên-các-đặc-trưng-âm-học)
   - 3.1. [Phương pháp luận so sánh đặc điểm giống và khác nhau theo các nhóm đặc trưng](#31-phương-pháp-luận-so-sánh-đặc-điểm-giống-và-khác-nhau-theo-các-nhóm-đặc-trưng)
   - 3.2. [Bảy cặp đối chứng cụ thể trích xuất trực tiếp từ bộ dữ liệu](#32-bảy-cặp-đối-chứng-cụ-thể-trích-xuất-trực-tiếp-từ-bộ-dữ-liệu)
   - 3.3. [So sánh định lượng tổng thể các đặc trưng trên toàn bộ 6 nhạc cụ](#33-so-sánh-định-lượng-tổng-thể-các-đặc-trưng-trên-toàn-bộ-6-nhạc-cụ)
   - 3.4. [Bảng tổng hợp đối chiếu các nhóm đặc trưng so sánh (Điểm giống - Điểm khác)](#34-bảng-tổng-hợp-đối-chiếu-các-nhóm-đặc-trưng-so-sánh-điểm-giống---điểm-khác)
   - 3.5. [Các trường hợp ngoại lệ và hạn chế của bộ dữ liệu](#35-các-trường-hợp-ngoại-lệ-và-hạn-chế-của-bộ-dữ-liệu)
   - 3.6. [Ý nghĩa chuyển tiếp sang Nhiệm vụ 2](#36-ý-nghĩa-chuyển-tiếp-sang-nhiệm-vụ-2)
4. [CHƯƠNG 4: NHIỆM VỤ 2 - XÂY DỰNG BỘ ĐẶC TRƯNG VÀ THIẾT KẾ ĐỘ TƯƠNG ĐỒNG CHO CBAR](#chương-4-nhiệm-vụ-2---xây-dựng-bộ-đặc-trưng-và-thiết-kế-độ-tương-đồng-cho-cbar)
   - 4.1. [Mục tiêu và kiến trúc bộ đặc trưng truy hồi CBAR](#41-mục-tiêu-và-kiến-trúc-bộ-đặc-trưng-truy-hồi-cbar)
   - 4.2. [Lý do lựa chọn các bộ đặc trưng](#42-lý-do-lựa-chọn-các-bộ-đặc-trưng)
   - 4.3. [Quy trình trích xuất toán học từng bước từ tín hiệu âm thanh số](#43-quy-trình-trích-xuất-toán-học-từng-bước-từ-tín-hiệu-âm-thanh-số)
   - 4.4. [Trình bày chi tiết từng bộ đặc trưng (Đặc trưng - Tương đồng/Khác biệt - Giá trị thông tin)](#44-trình-bày-chi-tiết-từng-bộ-đặc-trưng-đặc-trưng---tương-đồngkhác-biệt---giá-trị-thông-tin)
   - 4.5. [Bộ đặc trưng được sử dụng chính và cơ chế kết hợp bổ trợ (Fusion)](#45-bộ-đặc-trưng-được-sử-dụng-chính-và-cơ-chế-kết-hợp-bổ-trợ-fusion)
   - 4.6. [Chuẩn hóa đặc trưng Z-score và nguyên tắc chống rò rỉ dữ liệu](#46-chuẩn-hóa-đặc-trưng-z-score-và-nguyên-tắc-chống-rò-rỉ-dữ-liệu)
   - 4.7. [Độ đo khoảng cách chuẩn hóa RMSD và cơ chế xếp hạng Top-5 file tương đồng nhất](#47-độ-đo-khoảng-cách-chuẩn-hóa-rmsd-và-cơ-chế-xếp-hạng-top-5-file-tương-đồng-nhất)
   - 4.8. [Đề xuất phương pháp luận đánh giá hệ thống tìm kiếm cho Nhiệm vụ 4](#48-đề-xuất-phương-pháp-luận-đánh-giá-hệ-thống-tìm-kiếm-cho-nhiệm-vụ-4)
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

$$
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

### 2.5. Kiểm chứng bộ dữ liệu đạt chuẩn kỹ thuật đề bài (600 file)

Quá trình thu thập, tiền xử lý và lọc dữ liệu qua 11 bước tự động đã chuyển đổi từ 436 track thô sang đúng **600 tệp âm thanh WAV hoàn chỉnh**. 

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

Để kiểm chứng bộ dữ liệu thực sự đáp ứng các tiêu chuẩn kỹ thuật của đề tài trước khi chuyển sang phân tích nội dung, toàn bộ 600 tệp được đo đạc và đối chiếu theo các tiêu chí kỹ thuật:

| Tiêu chí kỹ thuật | Yêu cầu chuẩn hóa | Kết quả kiểm chứng trên 600/600 tệp WAV | Đánh giá đạt chuẩn |
| :---|:---|:---|:---:|
| **Tổng số lượng tệp** | $\ge 500$ tệp độc tấu đơn | **600 tệp WAV** (vượt 20% quy mô tối thiểu) | **ĐẠT** |
| **Cân bằng số lượng giữa các lớp** | Phân bổ đều giữa các lớp nhạc cụ | **Đúng 100 tệp/lớp** cho 6 nhạc cụ bộ dây | **ĐẠT** |
| **Tính chất độc tấu đơn nhạc cụ** | Mỗi tệp chỉ chứa 1 nhạc cụ, không lẫn tiếng nói | Trích từ stems/solos riêng biệt, tỷ lệ có tiếng $\ge 90\%$ | **ĐẠT** |
| **Cấu hình kênh âm thanh** | Đồng nhất 100% | **Mono 1 kênh** (chuẩn hóa gộp kênh pha) | **ĐẠT (600/600)** |
| **Tần số lấy mẫu ($f_s$)** | Đồng nhất 100% | **22 050 Hz** ($f_{\text{Nyquist}} = 11\,025\text{ Hz}$) | **ĐẠT (600/600)** |
| **Định dạng lượng tử hóa** | Không nén mất dữ liệu (lossless) | **WAV, PCM có dấu 16-bit** | **ĐẠT (600/600)** |
| **Thời lượng tệp** | Đủ chu kỳ nốt, quanh $3\text{ s}$ | Dao động **$2{,}5 - 3{,}5\text{ s}$** (trung bình $3{,}0\text{ s}$) bám theo Onset | **ĐẠT (600/600)** |
| **Khử tiếng click tại mép cắt** | Biên độ suy giảm về 0 ở hai đầu | **Fade 50 ms** đầu và cuối dạng sóng | **ĐẠT (600/600)** |
| **Lưu vết nguồn gốc và siêu dữ liệu** | Minh bạch, tra cứu được nguồn | Tệp `data/metadata.csv` lưu trữ đầy đủ 600 bản ghi | **ĐẠT (600/600)** |

> [!IMPORTANT]
> **Nguyên tắc phương pháp luận quan trọng:**
> Các tiêu chuẩn kỹ thuật ở bảng trên (tần số lấy mẫu 22 050 Hz, mono, định dạng WAV PCM 16-bit, độ dài quanh 3 giây, fade mép 50 ms) là **chuẩn kỹ thuật bắt buộc** nhằm bảo đảm dữ liệu đầu vào đồng nhất cho hệ thống máy tính, áp dụng đồng nhất 100% cho toàn bộ 600 tệp nên **KHÔNG được tính là điểm "giống nhau" về mặt âm thanh khi phân tích ở Chương 3**. 
> 
> Thay vào đó, việc phân tích đặc điểm giống và khác nhau của tiếng các nhạc cụ bắt buộc phải so sánh dựa trên **nội dung sóng âm thực tế và các nhóm đặc trưng âm học (Acoustic Features)** được trích xuất trực tiếp từ tín hiệu.

---

## CHƯƠNG 3: NHIỆM VỤ 1 - MÔ TẢ ĐẶC ĐIỂM GIỐNG VÀ KHÁC NHAU DỰA TRÊN CÁC ĐẶC TRƯNG ÂM HỌC

### 3.1. Phương pháp luận so sánh đặc điểm giống và khác nhau theo các nhóm đặc trưng

Để mô tả bản chất âm thanh của 6 nhạc cụ bộ dây một cách khách quan, khoa học và phục vụ trực tiếp cho việc thiết kế hệ thống CBAR ở Nhiệm vụ 2, báo cáo xây dựng phương pháp so sánh dựa trên các nhóm đặc trưng tín hiệu âm thanh số:

- **Hai tệp âm thanh được coi là "giống nhau":** Khi chúng cùng có thể được khảo sát và lượng hóa trên một **trục đặc trưng âm học chung** (ví dụ: cùng có thể đo đạc dải cao độ cơ bản $f_0$, cùng có thể khảo sát động thái năng lượng thời gian RMS, cùng có thể đo độ nhám/méo sóng qua ZCR, cùng có thể đo độ sáng phổ qua Spectral Centroid, cùng có thể xác định trần phát xạ dải cao qua Spectral Roll-off, cùng có thể bóc tách cấu trúc formant thùng đàn qua MFCC, và cùng có thể phân tích cấu trúc cao độ hòa âm qua Chroma STFT).
- **Các tệp âm thanh "khác nhau":** Ở **giá trị định lượng cụ thể** mà đặc trưng đó thể hiện trên từng đối tượng nhạc cụ do sự khác biệt về kích thước thùng đàn, chiều dài dây, phương thức kích âm và hệ thống khuếch đại điện tử.

Phương pháp luận này giúp chuyển đổi các cảm nhận thính giác định tính thành các con số và biểu đồ đo đạc có thể tái lập, làm cầu nối trực tiếp sang thuật toán tính khoảng cách truy hồi trong CSDL đa phương tiện.

---

### 3.2. Bảy cặp đối chứng cụ thể trích xuất trực tiếp từ bộ dữ liệu

Dưới đây là 7 cặp so sánh điển hình, trích trực tiếp từ các tệp trong bộ dữ liệu chuẩn 600 file (kèm định danh tệp và số liệu đo đạc thực tế), minh họa cách so sánh điểm giống và khác nhau trên từng nhóm đặc trưng:

#### Cặp 1: Động thái đường bao năng lượng RMS - Kéo vĩ liên tục vs Gảy buông tắt nhanh
- **Tệp 1:** `data/wav/violin/violin_001.wav` (Violin kéo vĩ, $\sigma_{\text{RMS}} = 0{,}073$, mức giảm năng lượng sau 0,4s $D_{0{,}4} = 0{,}0\text{ dB}$).
- **Tệp 2:** `data/wav/guitar_acoustic/guitar_acoustic_001.wav` (Guitar acoustic gảy buông, $\sigma_{\text{RMS}} = 0{,}089$, mức giảm $D_{0{,}4} = -7{,}1\text{ dB}$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cả hai tệp đều thuộc nhóm đặc trưng **"Động thái năng lượng biên độ theo thời gian"** (cùng đo được bằng chuỗi năng lượng hiệu dụng $\operatorname{RMS}(m)$ và đường bao biên độ ADSR).
  - *Điểm khác:* Khác biệt hoàn toàn về hình thái đường bao. Violin sử dụng vĩ cọ ma sát dính - trượt nạp cơ năng liên tục, tạo ra pha duy trì (Sustain) phẳng và kéo dài, năng lượng tại 0,4s không bị suy giảm ($0{,}0\text{ dB}$). Ngược lại, Guitar acoustic chỉ nhận cơ năng tại thời điểm buông ngón, tạo đỉnh nhọn Attack rồi năng lượng tắt dốc rất nhanh theo hàm mũ (Decay), giảm tới $-7{,}1\text{ dB}$ (mất hơn $56\%$ biên độ đỉnh).

#### Cặp 2: Độ nhám và Méo sóng (ZCR) - Sóng điều hòa mộc vs Méo cắt đỉnh (Clipping)
- **Tệp 1:** `data/wav/cello/cello_001.wav` (Cello mộc, $\operatorname{ZCR}_{\text{mean}} = 0{,}037$, $\operatorname{ZCR}_{\text{std}} = 0{,}011$).
- **Tệp 2:** `data/wav/guitar_electric/guitar_electric_001.wav` (Guitar điện méo tiếng, $\operatorname{ZCR}_{\text{mean}} = 0{,}108$, $\operatorname{ZCR}_{\text{std}} = 0{,}039$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cả hai tệp đều thuộc nhóm đặc trưng **"Tốc độ đổi dấu dạng sóng (Zero-Crossing Rate)"** (cùng khảo sát tần suất tín hiệu dao động cắt qua trục không).
  - *Điểm khác:* Cello mộc phát ra dạng sóng điều hòa trơn nhẵn, dao động tuần hoàn với chu kỳ nốt rõ ràng nên giá trị ZCR rất thấp ($0{,}037$). Guitar điện distortion qua mạch khuếch đại bão hòa bị xén phẳng biên độ (clipping) và sinh ra vô số họa âm bậc cao răng cưa, khiến tín hiệu cắt qua trục không liên tục, đẩy mức ZCR lên gấp gần 3 lần ($0{,}108$).

#### Cặp 3: Trọng tâm phổ (Spectral Centroid - Độ sáng) - Nhạc cụ dải cao vs Nhạc cụ siêu trầm
- **Tệp 1:** `data/wav/violin/violin_001.wav` (Violin thùng nhỏ, $\text{Centroid}_{\text{mean}} = 1756{,}2\text{ Hz}$, $f_{50} = 506{,}0\text{ Hz}$).
- **Tệp 2:** `data/wav/double_bass/double_bass_001.wav` (Double Bass thùng khổng lồ, $\text{Centroid}_{\text{mean}} = 482{,}1\text{ Hz}$, $f_{50} = 107{,}7\text{ Hz}$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cả hai tệp đều thuộc nhóm đặc trưng **"Độ sáng phổ (Spectral Centroid)"** (cùng đo momen bậc 1 của phổ công suất để lượng hóa cảm nhận thính giác về độ sáng/độ tối của âm thanh).
  - *Điểm khác:* Violin có kích thước thùng đàn nhỏ nhất và dây căng ngắn nhất họ vĩ, trọng tâm phổ dịch chuyển mạnh về dải cao ($1756{,}2\text{ Hz}$), tạo âm sắc thanh mảnh và sáng. Ngược lại, Double Bass có thùng đàn lớn nhất và dây dài nặng nhất, trọng tâm phổ dồn sâu về dải trầm ($482{,}1\text{ Hz}$), tạo cảm giác âm thanh tối sẫm, trầm đục và đóng vai trò làm bè đáy hòa âm.

#### Cặp 4: Giới hạn tần số cuộn phổ (Spectral Roll-off 85%) - Phân tầng 3 nhạc cụ họ vĩ
- **Tệp 1:** `data/wav/violin/violin_001.wav` ($\text{Roll-off}_{0{,}85} = 3280{,}5\text{ Hz}$).
- **Tệp 2:** `data/wav/viola/viola_001.wav` ($\text{Roll-off}_{0{,}85} = 1590{,}2\text{ Hz}$).
- **Tệp 3:** `data/wav/cello/cello_001.wav` ($\text{Roll-off}_{0{,}85} = 1390{,}8\text{ Hz}$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cùng thuộc nhóm đặc trưng **"Tần số cuộn phổ (Spectral Roll-off)"** (cùng xác định ngưỡng tần số mà dưới đó tập trung đúng 85% tổng năng lượng phổ STFT).
  - *Điểm khác:* Phân tầng ranh giới năng lượng rất rõ rệt theo kích thước thùng đàn: Violin có dải phát xạ mở rộng tới trên $3200\text{ Hz}$; trong khi Viola (thùng lớn hơn 15%) bị giới hạn quanh $1590\text{ Hz}$ và Cello (thùng lớn đặt sàn) bị chặn năng lượng dưới $1400\text{ Hz}$.

#### Cặp 5: Bao phổ formant thùng đàn (13 hệ số MFCC) - Ba kết cấu thùng đàn và amply
- **Tệp 1:** `data/wav/violin/violin_001.wav` (Thùng gỗ họ vĩ dáng số 8, $c_0 = -262{,}4$, $c_1 = 66{,}0$, $c_2 = -4{,}2$).
- **Tệp 2:** `data/wav/guitar_acoustic/guitar_acoustic_001.wav` (Thùng gỗ phẳng có lỗ tròn mộc, $c_0 = -227{,}4$, $c_1 = 101{,}8$, $c_2 = +6{,}7$).
- **Tệp 3:** `data/wav/guitar_electric/guitar_electric_001.wav` (Thân gỗ đặc thu qua amply méo tiếng, $c_0 = -94{,}1$, $c_1 = 124{,}9$, $c_2 = -71{,}7$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cùng thuộc nhóm đặc trưng **"Hình thái đường bao phổ âm sắc (MFCC)"** (cùng sử dụng 13 hệ số Cepstral thang Mel để bóc tách đáp ứng bộ lọc của thùng đàn độc lập với nốt nhạc cụ thể).
  - *Điểm khác:* Các hệ số MFCC đầu ghi nhận sự khác biệt căn bản về kết cấu cộng hưởng: Guitar điện có $c_0 = -94{,}1$ (năng lượng logarit trung bình rất cao do biên độ bị amply nén phẳng) và hệ số $c_2 = -71{,}7$ (rất âm, phản ánh độ cong bao phổ bị xén dẹt bởi hiệu ứng méo tiếng); khác biệt hoàn toàn với 2 nhạc cụ mộc có $c_0$ dao động sâu từ $-227$ đến $-262$ và $c_2$ quanh mốc từ $-4$ đến $+6$.

#### Cặp 6: Phân bố 12 nửa cung (Chroma STFT) - Giai điệu đơn âm vs Đệm hợp âm đa âm
- **Tệp 1:** `data/wav/violin/violin_001.wav` (Violin độc tấu đơn âm, năng lượng Chroma tập trung nhọn ở nốt A và D).
- **Tệp 2:** `data/wav/guitar_acoustic/guitar_acoustic_001.wav` (Guitar đệm hợp âm rải ngón, năng lượng Chroma phân tán rộng qua E, G, B, D).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cùng thuộc nhóm đặc trưng **"Phân bố cao độ hòa âm 12 nửa cung (Chroma STFT)"** (cùng gập toàn bộ năng lượng phổ STFT về 12 nửa cung chuẩn nhạc lý phương Tây độc lập quãng tám).
  - *Điểm khác:* Khác biệt về phong cách diễn tấu âm nhạc: Violin diễn tấu giai điệu đơn âm (monophonic) nên năng lượng Chroma tập trung thành các đỉnh nhọn cục bộ tại cao độ nốt đang bấm; trong khi Guitar acoustic thường xuyên quạt hoặc rải hợp âm đa âm (polyphonic), khiến năng lượng phân tán đồng đều qua nhiều nửa cung cùng lúc.

#### Cặp 7: Kỹ thuật diễn tấu Kéo vĩ (Arco) vs Gảy ngón (Pizzicato) trên cùng đàn Cello
- **Tệp 1:** `data/wav/cello/cello_001.wav` (Cello kéo vĩ liên tục, $D_{0{,}4} \approx -1{,}6\text{ dB}$, $\sigma_{\text{RMS}} = 0{,}068$).
- **Tệp 2:** Đoạn Cello diễn tấu kỹ thuật Pizzicato trong cùng bộ dữ liệu URMP ($D_{0{,}4} = -7{,}0\text{ dB}$, $\sigma_{\text{RMS}} = 0{,}095$).
- **Nhận xét so sánh:**
  - *Điểm giống:* Cùng thuộc nhóm thuộc tính **"Nhạc cụ Cello"** (cùng kích thước thùng đàn, cùng 4 dây buông C2-G2-D3-A3, cùng dải âm vực cơ bản $f_0$).
  - *Điểm khác:* Khác biệt triệt để về kỹ thuật kích âm cơ học: Kéo vĩ ma sát liên tục giúp duy trì biên độ ổn định; trong khi gảy ngón pizzicato buông dây tự do khiến năng lượng sụt giảm dốc đúng $-7{,}0\text{ dB}$ (tương tự như Guitar acoustic). Trường hợp này chứng minh rằng một đặc trưng động thái thời gian đơn lẻ không thể định danh chính xác nhạc cụ nếu không kết hợp với đặc trưng âm sắc thùng đàn (MFCC).

![Hình 3.1: Các cặp đối chứng thực tế](hinh/6_so_sanh_cac_cap_doi_chung.png)

*Hình 3.1: Minh họa đo đạc trực quan 6 cặp đối chứng thực tế trích xuất trực tiếp từ bộ dữ liệu (sinh bởi kịch bản `src/trich_xuat_va_ve_dac_trung.py`).*

---

### 3.3. So sánh định lượng tổng thể các đặc trưng trên toàn bộ 6 nhạc cụ

Để có cái nhìn toàn cảnh trên toàn bộ 600 tệp âm thanh (mỗi nhạc cụ 100 tệp), kịch bản `src/trich_xuat_va_ve_dac_trung.py` đã trích xuất đồng thời toàn bộ các đặc trưng và xuất bảng thống kê chi tiết (`reports/so_sanh_dac_trung_chi_tiet.csv`):

| Nhạc cụ | Trọng tâm phổ Centroid (Hz) | Tần số cuộn Roll-off 85% (Hz) | Năng lượng RMS TB | Biến thiên RMS (Std) | Tốc độ qua 0 (ZCR) | MFCC $c_0$ (dB) | MFCC $c_1$ | MFCC $c_2$ | MFCC $c_3$ |
| :---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Violin** | $1708{,}03 \pm 447{,}7$ | $3142{,}19 \pm 861{,}2$ | $0{,}19$ | **0,09** | $0{,}09 \pm 0{,}04$ | $-262{,}36$ | $65{,}99$ | $-4{,}24$ | $30{,}45$ |
| **Viola** | $894{,}74 \pm 272{,}6$ | $1610{,}61 \pm 637{,}9$ | $0{,}19$ | **0,09** | $0{,}04 \pm 0{,}01$ | $-268{,}19$ | $117{,}46$ | $-2{,}89$ | $40{,}21$ |
| **Cello** | $817{,}56 \pm 112{,}1$ | $1417{,}31 \pm 217{,}1$ | $0{,}16$ | **0,08** | $0{,}04 \pm 0{,}01$ | $-238{,}08$ | $160{,}11$ | $-2{,}64$ | $18{,}85$ |
| **Double Bass** | **$496{,}92 \pm 141{,}5$** | **$771{,}04 \pm 226{,}5$** | $0{,}20$ | **0,10** | **$0{,}02 \pm 0{,}01$** | $-268{,}93$ | $181{,}55$ | $+28{,}36$ | $13{,}25$ |
| **Guitar acoustic** | $1510{,}99 \pm 390{,}3$ | $3172{,}53 \pm 897{,}0$ | $0{,}13$ | **0,06** | $0{,}06 \pm 0{,}02$ | $-227{,}40$ | $101{,}76$ | $+6{,}68$ | $34{,}97$ |
| **Guitar electric** | **$1874{,}50 \pm 376{,}8$** | **$3412{,}78 \pm 709{,}1$** | $0{,}21$ | **0,05** | **$0{,}11 \pm 0{,}04$** | **$-94{,}06$** | $124{,}87$ | **$-71{,}69$** | $51{,}14$ |

![Hình 3.2: So sánh tổng thể các đặc trưng trên 6 nhạc cụ](hinh/5_so_sanh_dac_trung_6_nhac_cu.png)

*Hình 3.2: Biểu đồ 4 panel so sánh định lượng các đặc trưng âm học đo đạc trên 600 file của 6 nhạc cụ bộ dây (sinh bởi kịch bản `src/trich_xuat_va_ve_dac_trung.py`).*

#### Phân tích chi tiết 4 bảng biểu đồ định lượng:

1. **Panel A - Trọng tâm phổ (Centroid) và Tần số cuộn phổ (Roll-off 85%):**
   - Sự phân tầng kích thước thùng đàn họ vĩ thể hiện cực kỳ nhất quán: Double Bass ($496{,}9\text{ Hz}$) < Cello ($817{,}6\text{ Hz}$) < Viola ($894{,}7\text{ Hz}$) < Violin ($1708{,}0\text{ Hz}$).
   - Tần số Roll-off 85% của Double Bass chỉ đạt $771{,}0\text{ Hz}$ (năng lượng gần như hoàn toàn bị giới hạn ở dải trầm), trong khi Violin vươn tới $3142{,}2\text{ Hz}$.
   - Guitar điện đạt mức cao nhất ở cả hai chỉ số ($\text{Centroid} = 1874{,}5\text{ Hz}$, $\text{Roll-off} = 3412{,}8\text{ Hz}$) do hiệu ứng méo tiếng sản sinh chuỗi họa âm dày đặc ở dải cao.
2. **Panel B - Động thái năng lượng RMS và Độ nhám ZCR:**
   - Biến thiên năng lượng $\sigma_{\text{RMS}}$ ở Guitar điện thấp nhất ($0{,}05$) do mạch nén biên độ (compression) giữ năng lượng ổn định nhân tạo; Guitar acoustic đạt $0{,}06$; trong khi các nhạc cụ kéo vĩ có độ biến thiên cao hơn ($0{,}08 - 0{,}10$) do sắc thái biểu cảm to nhỏ của người kéo đàn (dynamics).
   - Tốc độ qua 0 (ZCR) tách biệt rõ rệt Guitar điện ($0{,}11 \pm 0{,}04$ - cao nhất) khỏi 5 nhạc cụ mộc, trong đó Double Bass thấp nhất ($0{,}02$).
3. **Panel C - 13 hệ số MFCC bóc tách đường bao phổ thùng đàn:**
   - Đường cong MFCC của Guitar điện hoàn toàn tách biệt khỏi 5 nhạc cụ còn lại: $c_0$ đạt $-94{,}1$ (cao hơn hẳn mốc $-260$ của các đàn mộc) và $c_2$ tụt dốc sâu về $-71{,}7$ (đỉnh âm phản ánh độ bão hòa phổ).
   - Double Bass có hệ số $c_1$ và $c_2$ dương cao ($c_1 = 181{,}6$, $c_2 = +28{,}4$), phản ánh đáp ứng tần số tập trung sâu vào dải hạ âm.
4. **Panel D - 12 nửa cung Chroma STFT:**
   - Phân bố Chroma của các nhạc cụ phản ánh xu hướng nốt nhạc và điệu thức chủ đạo trong các tác phẩm thính phòng cổ điển (URMP) và các bản thu guitar chuyên nghiệp, giúp phân biệt các nhóm tác phẩm có vòng hòa âm tương đồng.

Bên cạnh các đặc trưng khung trên, bốn phép đo đạc âm học thực nghiệm được thực hiện ở kịch bản `src/mo_ta_du_lieu.py` cũng bổ sung bức tranh toàn cảnh:
- **Dạng sóng và Spectrogram:** (Hình 3.3 dưới) khảo sát hình thái biên độ và họa âm.
- **Khảo sát âm vực pYIN:** (Hình 3.4 dưới) xác nhận trật tự nốt trung vị $f_0$: Violin ($501{,}3\text{ Hz}$) > Viola ($290{,}4\text{ Hz}$) > Cello ($157{,}4\text{ Hz}$) > Guitar electric ($130{,}9\text{ Hz}$) > Guitar acoustic ($117{,}6\text{ Hz}$) > Double Bass ($92{,}3\text{ Hz}$).

![Dạng sóng và Spectrogram](hinh/1_song_va_spectrogram.png)

*Hình 3.3: Dạng sóng biên độ (trên) và Spectrogram (dưới) của 6 tệp đại diện cho 6 nhạc cụ.*

![Biểu đồ âm vực](hinh/2_am_vuc_f0.png)

*Hình 3.4: Biểu đồ hộp (Boxplot) cao độ trung vị $f_0$ pYIN trên 600 file.*

---

### 3.4. Bảng tổng hợp đối chiếu các nhóm đặc trưng so sánh (Điểm giống - Điểm khác)

Bảng dưới đây tổng hợp cách tiếp cận so sánh đặc điểm giống và khác nhau giữa 6 nhạc cụ bộ dây theo từng nhóm đặc trưng âm học cụ thể (theo cấu trúc mẫu chuẩn của BTL Hệ CSDL Đa phương tiện):

| Nhóm đặc trưng | Đặc trưng âm học đo đạc | Điểm giống (mọi nhạc cụ đều xét được) | Điểm khác (giá trị cụ thể khác nhau giữa các nhạc cụ) |
| :---|:---|:---|:---|
| **1. Động thái năng lượng thời gian** | Năng lượng RMS và độ suy giảm $D_{0{,}4}$ | Đều đo được mức năng lượng sóng âm hiệu dụng và sự biến thiên biên độ theo thời gian. | **Kéo vĩ** giữ đều nốt ($D_{0{,}4} \approx 0\text{ dB}$, $\sigma_{\text{RMS}}$ ổn định); **Guitar mộc** tắt dốc nhanh ($D_{0{,}4} = -7{,}1\text{ dB}$); **Guitar điện** nén biên độ nhân tạo. |
| **2. Độ nhám & Méo dạng sóng** | Tốc độ qua điểm không (Zero-Crossing Rate - ZCR) | Đều đo được tần suất đổi dấu dạng sóng giữa các mẫu liên tiếp. | **Nhạc cụ mộc** có sóng điều hòa trơn nhẵn, ZCR thấp ($0{,}02 - 0{,}04$); **Guitar điện distortion** sóng răng cưa bị xén đỉnh, ZCR cao vọt ($0{,}11$). |
| **3. Độ sáng phổ âm thanh** | Trọng tâm phổ (Spectral Centroid) | Đều lượng hóa được tâm khối hình học của phổ công suất và cảm nhận trực giác về "độ sáng". | Phân tầng rõ rệt: **Double Bass** tối sẫm ($497\text{ Hz}$) < **Cello** ($818\text{ Hz}$) < **Viola** ($895\text{ Hz}$) < **Violin** rất sáng ($1708\text{ Hz}$) < **Guitar điện** ($1875\text{ Hz}$). |
| **4. Giới hạn dải tần phát xạ** | Tần số cuộn phổ 85% (Spectral Roll-off) | Đều xác định được ngưỡng tần số chứa 85% tổng năng lượng phổ STFT. | **Double Bass** bị chặn dưới $771\text{ Hz}$; **Viola/Cello** mở rộng tới $1400 - 1600\text{ Hz}$; **Violin và Guitar** vươn tới trên $3100 - 3400\text{ Hz}$. |
| **5. Âm sắc và bao phổ thùng đàn** | 13 hệ số Cepstral thang Mel (MFCC $c_0 - c_{12}$) | Đều bóc tách được đáp ứng bộ lọc của thùng đàn độc lập với nốt nhạc cụ thể. | **Guitar điện** có $c_0 = -94{,}1$ (năng lượng lớn) và $c_2 = -71{,}7$ (rất âm); **Nhạc cụ mộc họ vĩ** có $c_0 \approx -260$ và $c_1, c_2$ biến thiên theo kích thước thùng gỗ. |
| **6. Phân bố cao độ hòa âm** | Vector 12 nửa cung chuẩn nhạc lý (Chroma STFT) | Đều gập năng lượng phổ về 12 nửa cung (C đến B) độc lập với quãng tám. | **Nhạc cụ họ vĩ đơn âm** có Chroma tập trung nhọn ở nốt giai điệu; **Guitar đệm hợp âm đa âm** có Chroma phân tán đều qua nhiều nửa cung cùng lúc. |
| **7. Cao độ cơ bản và âm vực** | Tần số cơ bản $f_0$ (thuật toán pYIN) | Đều đo được tần số rung cơ bản thấp nhất của sợi dây căng. | Trật tự âm vực giảm dần: **Violin** ($501\text{ Hz}$) > **Viola** ($290\text{ Hz}$) > **Cello** ($157\text{ Hz}$) > **Guitar** ($117 - 131\text{ Hz}$) > **Double Bass** ($92\text{ Hz}$). |

---

### 3.5. Các trường hợp ngoại lệ và hạn chế của bộ dữ liệu

1. **Hiện tượng Cello suy giảm năng lượng tương đương Guitar:** Mức giảm $D_{0{,}4} = -7{,}0\text{ dB}$ của Cello phản ánh kỹ thuật diễn tấu thực tế: trong các bản nhạc thính phòng URMP, nghệ sĩ cello sử dụng kỹ thuật gảy ngón **pizzicato** ở nhiều phân đoạn. Điều này cho thấy đường bao năng lượng phụ thuộc vào kỹ thuật chơi chứ không chỉ phụ thuộc loại nhạc cụ.
2. **Hiện tượng nhận diện sai cao độ ở Guitar:** Lỗi sub-harmonic của thuật toán pYIN khi phân tích tín hiệu đa âm khiến $p_{10}$ của guitar ghi nhận giá trị dưới $82{,}4\text{ Hz}$ (thấp hơn nốt dây buông E2).
3. **Số lượng track gốc hạn chế ở Double Bass:** 100 file double bass được trích xuất từ 6 track gốc (2 URMP và 4 PHENICX), do đó phải cho phép chọn các đoạn liền kề để bảo đảm đủ quy mô mẫu.
4. **Độ dài cố định của Guitar electric:** Dữ liệu Medley-solos-DB được cắt sẵn ở độ dài $2{,}97\text{ s}$ nên không được cắt theo ranh giới nốt Onset như các nhạc cụ còn lại.
5. **Nhiễu ù tần số thấp:** Các bản thu URMP có một lượng nhỏ tạp âm ù điện tần số thấp (dưới $60\text{ Hz}$) từ nguồn điện phòng thu.
6. **Mức độ kiểm chứng thủ công:** Quy trình tiền xử lý 11 bước đã áp dụng các bộ lọc tự động theo ngưỡng biên độ, Onset và hệ số tương quan để lọc nhiễu và loại bản thu trùng; tuy nhiên việc nghe kiểm âm thủ công toàn bộ 600 tệp chưa được thực hiện toàn diện.

---

### 3.6. Ý nghĩa chuyển tiếp sang Nhiệm vụ 2

Từ các kết quả phân tích lý thuyết và thực nghiệm ở trên:
- **Không một đặc trưng đơn lẻ nào có thể giải quyết trọn vẹn bài toán CBAR:** Cao độ $f_0$ bị chồng lấn âm vực (Viola và Cello cùng chơi dải $190 - 200\text{ Hz}$); đường bao năng lượng bị biến động theo kỹ thuật kéo vĩ vs pizzicato; phổ tần số bị thay đổi bởi amply điện tử.
- Hệ thống bắt buộc phải tích hợp **đa bộ đặc trưng bổ trợ lẫn nhau**: kết hợp giữa **Âm sắc / Bao phổ (MFCC, Spectral Roll-off)**, **Động học năng lượng thời gian (RMS, ZCR)** và **Trọng tâm phổ / Hòa âm cao độ (Spectral Centroid, Chroma STFT)**.
- Toàn bộ các đặc trưng phải được chuẩn hóa toán học và rút gọn chiều thành một vector cố định nhỏ gọn, làm cơ sở xây dựng hệ thống CSDL và xếp hạng Top-5 trong Nhiệm vụ 2 tiếp theo.

---

---

## CHƯƠNG 4: NHIỆM VỤ 2 - XÂY DỰNG BỘ ĐẶC TRƯNG VÀ THIẾT KẾ ĐỘ TƯƠNG ĐỒNG CHO CBAR

### 4.1. Mục tiêu và kiến trúc bộ đặc trưng truy hồi CBAR

#### 4.1.1. Thách thức kỹ thuật và mục tiêu bài toán

Theo yêu cầu của đề tài Bài tập lớn, Nhiệm vụ 2 đòi hỏi:
- Xây dựng một hoặc nhiều bộ thuộc tính đặc trưng âm thanh để nhận diện và tìm kiếm các bản ghi âm thanh nhạc cụ bộ dây trong bộ dữ liệu đã thu thập ở Nhiệm vụ 1.
- Mỗi bộ thuộc tính phải bao gồm các đặc trưng giúp **tìm được sự tương đồng giữa các bản ghi của cùng một nhạc cụ** (hoặc cùng phong cách diễn tấu) và **nhận diện sự khác biệt giữa các nhạc cụ khác nhau**.
- Trình bày cụ thể từng loại đặc trưng: (i) đặc trưng là gì và cách trích xuất, (ii) cơ chế tìm tương đồng / khác biệt, và (iii) giá trị thông tin mà đặc trưng mang lại.

Thách thức kỹ thuật cơ bản của dữ liệu âm thanh số: Tín hiệu âm thanh dạng sóng $x[n]$ là dữ liệu phi cấu trúc, có số mẫu dao động lớn ($55\,125$ đến $77\,175$ mẫu ứng với thời lượng $2{,}5\text{ s} - 3{,}5\text{ s}$). Máy tính không thể so sánh trực tiếp khoảng cách giữa hai chuỗi có độ dài lệch nhau. Do đó, mục tiêu cốt lõi của bước thiết kế đặc trưng là **rút gọn chiều dữ liệu (Dimensionality Reduction)**: chuyển đổi chuỗi sóng âm biến thiên thành một **vector số thực cố định $\mathbf{v} \in \mathbb{R}^{58}$** có kích thước nhỏ gọn, bảo toàn các thuộc tính âm học quan trọng để lưu trữ hiệu quả trong hệ CSDL và tối ưu hóa tốc độ tính khoảng cách truy hồi.

#### 4.1.2. Kiến trúc hệ thống đặc trưng 58 chiều

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
│      tách bao phổ formant   │      bao biên độ ADSR       │      bậc 1; cảm nhận trực   │
│    - Vai trò: Tách nhạc cụ  │    - Vai trò: Tách Kéo vĩ   │      giác về "độ sáng/tối"  │
│      mộc và guitar điện;    │      (bền vững) vs Gảy dây  │    - Vai trò: Phân tầng kích│
│      nhận diện màu âm thùng │      (suy giảm dốc nhanh)   │      thước thùng họ vĩ      │
│ 2. Spectral Roll-off        │ 4. Zero-Crossing Rate (ZCR) │ 6. Chroma STFT              │
│    (1 GT × 2)               │    (1 GT × 2)               │    (12 lớp cao độ × 2)      │
│    - Bản chất: Tần số giới  │    - Bản chất: Tần suất đổi │    - Bản chất: Gập phổ về   │
│      hạn chứa 85% năng      │      dấu sóng; độ nhám và   │      12 nửa cung chuẩn nhạc │
│      lượng phổ STFT         │      méo tín hiệu           │      lý độc lập quãng tám   │
│    - Vai trò: Tách nhạc cụ  │    - Vai trò: Nhận diện méo │    - Vai trò: Phân biệt đơn │
│      siêu trầm (Double Bass)│      tiếng distortion guitar│      âm (họ vĩ) vs đa âm hợp│
│      khỏi dải cao           │      điện; bắt xước vĩ      │      âm (guitar)            │
└─────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

---

### 4.2. Lý do lựa chọn các bộ đặc trưng

Trước khi chốt hệ thống 3 bộ đặc trưng ở mục 4.3, đề tài đã cân nhắc kỹ lưỡng nhiều phương án trích xuất khác nhau trong lĩnh vực xử lý thông tin âm nhạc (Music Information Retrieval - MIR). Phần này trình bày các tiêu chí lựa chọn và lý do loại bỏ các phương án không phù hợp, làm rõ vì sao các đặc trưng được chọn là tối ưu cho hệ thống CBAR nhạc cụ bộ dây.

#### 4.2.1. Tiêu chí lựa chọn

1. **Đa dạng về khía cạnh âm học:** Mỗi bộ đặc trưng nắm bắt một khía cạnh vật lý độc lập (âm sắc/bao phổ, động thái năng lượng thời gian, độ sáng/hòa âm cao độ). Việc kết hợp các trục thông tin không tương quan giúp hệ thống bổ trợ lẫn nhau, tránh chọn nhiều đặc trưng cùng một họ vốn sẽ gây dư thừa và trùng lặp thông tin.
2. **Có thể diễn giải rõ ràng (Interpretable):** Đúng theo yêu cầu đề bài là phải *trình bày cụ thể giá trị thông tin* của từng loại đặc trưng. Nhóm ưu tiên các phương pháp xử lý tín hiệu có cơ sở toán học tường minh, giải thích được rõ ràng đặc trưng đó đo đại lượng vật lý gì, thay vì các vector biểu diễn dạng hộp đen (black-box).
3. **Không phụ thuộc tài nguyên ngoài:** Cài đặt hoàn toàn bằng thư viện xử lý tín hiệu cổ điển chuẩn hóa (`librosa`, `scipy`, `numpy`), không yêu cầu tải mô hình pretrained dung lượng lớn hàng trăm megabyte từ máy chủ nước ngoài, bảo đảm tính độc lập, khả năng tái lập và an toàn triển khai của hệ thống.
4. **Chi phí tính toán phù hợp quy mô CSDL:** Vector trích xuất phải đủ nhẹ để trích xuất nhanh trên toàn bộ 600 tệp trong vài chục giây và dễ dàng lưu trữ, lập chỉ mục trong hệ CSDL ở Nhiệm vụ 3 mà không đòi hỏi phần cứng GPU chuyên dụng.

#### 4.2.2. Các phương án đã cân nhắc nhưng không chọn

- **So khớp trực tiếp trên dạng sóng thô (Raw Waveform Distance):** Không chọn vì cực kỳ nhạy cảm với pha dao động, sự dịch chuyển thời gian (time-shift) và không có tính khái quát hóa âm sắc — hai đoạn nhạc của cùng một cây đàn chơi cùng nốt chỉ cần lệch nhau vài mili-giây là khoảng cách Euclidean trên mẫu sóng thô sẽ tăng vọt cực lớn.
- **Toàn bộ ma trận phổ STFT thô (Full Spectrogram Matrix):** Không chọn vì số chiều quá khổng lồ ($1025\text{ bin tần số} \times 130\text{ khung thời gian} \approx 133\,250\text{ giá trị/tệp}$). Chiều dữ liệu quá lớn gây ra hiện tượng bùng nổ số chiều (curse of dimensionality), làm mất tính phân biệt của hàm khoảng cách và tiêu tốn dung lượng bộ nhớ CSDL không cần thiết.
- **Ngân hàng bộ lọc Gabor / Biến đổi CQT dải hẹp:** Không chọn vì bản chất toán học cũng phân rã tần số tương tự STFT và Mel, nhưng chi phí tính toán biến đổi tích chập rất nặng nề trong khi thông tin thu được bị trùng lặp với Mel Filterbank và Chroma STFT.
- **Đặc trưng nhúng học sâu (Deep Audio Embeddings như VGGish, CLAP, OpenL3, Wav2Vec):** Đây là hướng tiếp cận cho độ chính xác phân loại tổng quát cao trong các bài toán công nghiệp hiện đại, nhưng nhóm quyết định **không sử dụng** trong đề tài này vì 3 lý do:
  1. *Cần tải mô hình pretrained dung lượng lớn:* Đòi hỏi tải các checkpoint nặng từ 300MB đến hơn 1GB từ máy chủ ngoài, gây rủi ro phụ thuộc hạ tầng mạng và môi trường cài đặt phức tạp.
  2. *Biểu diễn dạng hộp đen (Black-box):* Vector embedding học sâu là các con số trừu tượng ẩn trong mạng nơ-ron, không thể diễn giải từng chiều giá trị thông tin đo cái gì theo đúng yêu cầu học thuật của đề bài.
  3. *Vượt phạm vi học phần:* Môn học tập trung trang bị các kiến thức nền tảng về xử lý tín hiệu đa phương tiện cổ điển và thiết kế hệ thống CSDL truy hồi dựa trên đặc trưng có cấu trúc. Nhóm ghi nhận đây là hướng mở rộng tiềm năng cho tương lai.

#### 4.2.3. Bảng tổng quan các bộ đặc trưng và vai trò trong hệ thống

| Bộ đặc trưng | Nhóm đặc trưng con | Số chiều khung | Số chiều cố định $(\mu, \sigma)$ | Khía cạnh âm học nắm bắt | Vai trò trong hệ thống |
| :---|:---|:---:|:---:|:---|:---:|
| **Bộ A: Âm sắc / Bao phổ** | **MFCC** (13 hệ số)<br>**Spectral Roll-off** (1 giá trị) | 14 | **28 chiều** | Bóc tách đường bao phổ formant của thùng đàn và trần phát xạ dải cao | **Chính (Core Feature)** |
| **Bộ B: Năng lượng / Động học thời gian** | **RMS Energy** (1 giá trị)<br>**Zero-Crossing Rate** (1 giá trị) | 2 | **4 chiều** | Đường bao biên độ ADSR (Kéo vĩ vs Gảy dây) và độ nhám / méo sóng amply | **Bổ trợ (Fusion)** |
| **Bộ C: Trọng tâm / Hòa âm cao độ** | **Spectral Centroid** (1 giá trị)<br>**Chroma STFT** (12 nửa cung) | 13 | **26 chiều** | Cảm nhận trực giác về độ sáng phổ và phân bố cao độ hòa âm (Đơn âm vs Hợp âm) | **Bổ trợ (Fusion)** |

---

### 4.3. Quy trình trích xuất toán học từng bước từ tín hiệu âm thanh số

Toàn bộ quy trình trích xuất từ tín hiệu âm thanh số liên tục sang vector đặc trưng cố định 58 chiều được tự động hóa trong kịch bản `src/trich_xuat_va_ve_dac_trung.py`, gồm 4 bước kỹ thuật chính:

![Hình 4.1: Quy trình trích xuất toán học](hinh/7_quy_trinh_trich_xuat_dac_trung.png)

*Hình 4.1: Sơ đồ 4 bước toán học trích xuất từ dạng sóng số $x[n]$ đến vector đặc trưng cố định 58 chiều $\mathbf{v} \in \mathbb{R}^{58}$ (sinh bởi kịch bản `src/trich_xuat_va_ve_dac_trung.py`).*

#### Bước 1: Chia khung (Framing) và nhân cửa sổ Hann
- Tín hiệu âm thanh số $x[n]$ ($f_s = 22\,050\text{ Hz}$) được chia thành các khung ngắn có độ dài $N = 2048$ mẫu (khoảng $92{,}88\text{ ms}$) với bước nhảy $H = 512$ mẫu (khoảng $23{,}22\text{ ms}$), đạt độ gối khung $75\%$.
- Mỗi khung được nhân với cửa sổ Hann $w[n] = 0{,}5 - 0{,}5 \cos(2\pi n / N)$ để triệt tiêu hiện tượng rò rỉ phổ tại hai biên khung.

#### Bước 2: Biến đổi Fourier thời gian ngắn (STFT) và Phổ công suất
- Thực hiện biến đổi STFT trên từng khung $m$:
  $$
  X(m, k) = \sum_{n=0}^{N-1} x_m[n] \cdot w[n] \cdot e^{-j 2\pi k n / N}, \quad k = 0, 1, \dots, N/2
  $$
- Tính phổ công suất: $P(m, k) = |X(m, k)|^2$, với $N/2 + 1 = 1025$ bin tần số từ $0\text{ Hz}$ đến tần số Nyquist $11\,025\text{ Hz}$.

#### Bước 3: Trích xuất song song 6 nhóm đặc trưng khung thời gian
1. **Năng lượng hiệu dụng RMS:** Tính trực tiếp trên miền thời gian của từng khung:
   $$
   \operatorname{RMS}(m) = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x_m[n]^2}
   $$
2. **Tốc độ qua điểm không (ZCR):** Đếm tỷ lệ đổi dấu giữa hai mẫu kế tiếp:
   $$
   \operatorname{ZCR}(m) = \frac{1}{2(N-1)} \sum_{n=1}^{N-1} \big| \operatorname{sgn}(x_m[n]) - \operatorname{sgn}(x_m[n-1]) \big|
   $$
3. **Trọng tâm phổ (Spectral Centroid):** Tính momen bậc 1 của phổ công suất:
   $$
   C(m) = \frac{\sum_{k=0}^{N/2} f_k \cdot P(m, k)}{\sum_{k=0}^{N/2} P(m, k) + 10^{-9}}
   $$
4. **Tần số cuộn phổ (Spectral Roll-off 85%):** Tìm tần số ngưỡng $R_{0{,}85}(m)$ tích lũy đủ 85% tổng công suất:
   $$
   R_{0{,}85}(m) = \min \left\{ f_r : \sum_{k: f_k \le f_r} P(m, k) \ge 0{,}85 \sum_{k=0}^{N/2} P(m, k) \right\}
   $$
5. **13 hệ số Cepstral thang Mel (MFCC):**
   - Gom phổ $P(m, k)$ qua ngân hàng $M = 40$ bộ lọc tam giác Mel gối nhau: $E_{\text{Mel}}(m, i) = \sum_{k} P(m, k) H_i(k)$.
   - Nén logarit năng lượng: $L_{\text{Mel}}(m, i) = \log(E_{\text{Mel}}(m, i) + 10^{-9})$.
   - Biến đổi Cosine rời rạc (DCT-II) lấy 13 hệ số đầu:
     $$
     c_q(m) = \sqrt{\frac{2}{M}} \sum_{i=0}^{M-1} L_{\text{Mel}}(m, i) \cos\left[ \frac{\pi q}{M} \left(i + \frac{1}{2}\right) \right], \quad q = 0, 1, \dots, 12
     $$
6. **Đặc trưng 12 nửa cung (Chroma STFT):**
   - Ánh xạ bin tần số $k$ sang nốt MIDI $p(k) = \operatorname{round}(12 \log_2 (f_k / 440)) + 69$.
   - Modulo 12 gập về 12 nửa cung (C, C#, ..., B) và chuẩn hóa $\ell_1$:
     $$
     \operatorname{Chr}(m, c) = \sum_{k: p(k) \bmod 12 = c} P(m, k), \quad c \in \{0, 1, \dots, 11\}
     $$

#### Bước 4: Temporal Pooling tổng hợp Vector cố định 58 chiều
Chuỗi đặc trưng gồm $M$ khung thời gian được rút gọn thành một vector cố định thông qua 2 đại lượng thống kê:
- **Giá trị trung bình ($\mu_j$):** $\mu_j = \frac{1}{M} \sum_{m=1}^M g_j(m)$ (nắm bắt đặc tính âm sắc tĩnh chủ đạo).
- **Độ lệch chuẩn ($\sigma_j$):** $\sigma_j = \sqrt{\frac{1}{M} \sum_{m=1}^M (g_j(m) - \mu_j)^2}$ (nắm bắt động thái biến thiên thời gian).

Tổng hợp lại: $(13\text{ MFCC} + 1\text{ Roll-off} + 1\text{ RMS} + 1\text{ ZCR} + 1\text{ Centroid} + 12\text{ Chroma}) = 29\text{ đặc trưng khung} \times 2 = \mathbf{58\text{ chiều}}$.

---

### 4.4. Trình bày chi tiết từng bộ đặc trưng (Đặc trưng - Tương đồng/Khác biệt - Giá trị thông tin)

Dưới đây là phần trình bày chi tiết từng đặc trưng theo đúng 3 yêu cầu chuẩn mực của đề tài:

#### 4.4.1. Bộ A: Âm sắc và hình dạng bao phổ (Spectral Timbre & Envelope)

##### 1. Hệ số Cepstral thang Mel (MFCC - 13 hệ số, 26 chiều sau pooling)
- **Đặc trưng là gì:** MFCC mô hình hóa âm thanh theo nguyên lý Nguồn - Bộ lọc (Source-Filter Model). Trong nhạc cụ bộ dây, tín hiệu sóng âm là kết quả của dao động dây đàn (nguồn) đi qua bộ lọc âm học của thùng đàn gỗ (hoặc mạch amply). MFCC sử dụng ngân hàng bộ lọc Mel mô phỏng độ nhạy phi tuyến của tai người và biến đổi DCT-II để bóc tách đường bao phổ formant của thùng đàn, loại bỏ các đỉnh nhọn tần số cơ bản của nốt nhạc cụ thể.
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Hai đoạn âm thanh phát ra từ cùng một loại kết cấu thùng đàn (cùng cấu trúc formant) sẽ có đường cong MFCC rất gần nhau trong miền quefrency, bất kể người chơi đang bấm nốt cao hay nốt thấp.
  - *Khác biệt:* Nhạc cụ có cấu tạo thùng khác biệt sẽ có vector MFCC lệch xa nhau. Đặc biệt, Guitar điện (thân đặc amply méo tiếng) có $c_0 = -94{,}1$ và $c_2 = -71{,}7$ cách biệt hoàn toàn so với 5 nhạc cụ mộc ($c_0 \approx -260$, $c_2 \approx -4 \div +6$).
- **Giá trị thông tin:** Đây là đặc trưng mang giá trị thông tin cao nhất về **màu sắc âm học (timbre)**. MFCC độc lập với cao độ nốt nhạc, giúp hệ thống CBAR tìm được các bản ghi cùng loại nhạc cụ ngay cả khi nốt nhạc truy vấn khác với các nốt có trong CSDL.

##### 2. Tần số cuộn phổ (Spectral Roll-off 85% - 1 giá trị, 2 chiều sau pooling)
- **Đặc trưng là gì:** Spectral Roll-off là tần số ngưỡng $R_{0{,}85}$ mà dưới đó tập trung đúng 85% tổng công suất phổ STFT, đo lường độ dốc suy giảm năng lượng và giới hạn trên của dải tần phát xạ hiệu dụng.
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Các bản ghi có cùng trần phát xạ năng lượng dải cao sẽ có giá trị Roll-off sát nhau.
  - *Khác biệt:* Tách biệt Double Bass ($\text{Roll-off} = 771\text{ Hz}$, dồn sâu dưới dải trầm) khỏi Violin ($\text{Roll-off} = 3142\text{ Hz}$) và Guitar điện ($\text{Roll-off} = 3412\text{ Hz}$).
- **Giá trị thông tin:** Cung cấp thông tin bổ trợ trực tiếp cho MFCC về ranh giới dải tần hiệu dụng, phản ánh trực tiếp kích thước vật lý của hộp cộng hưởng.

---

#### 4.4.2. Bộ B: Năng lượng và động học thời gian (Energy Dynamics & Temporal Envelope)

##### 3. Năng lượng hiệu dụng biên độ (RMS Energy - 1 giá trị, 2 chiều sau pooling)
- **Đặc trưng là gì:** RMS đo mức năng lượng vật lý hiệu dụng của sóng âm trong từng khung thời gian, phản ánh đường bao biên độ ADSR (Attack - Decay - Sustain - Release) của tín hiệu.
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Các tệp có cùng phong cách diễn tấu (cùng kéo ngân nga legato hoặc cùng ngắt dồn dập staccato) sẽ có mức năng lượng và độ biến thiên RMS tương tự nhau.
  - *Khác biệt:* **Phân biệt triệt để cơ chế Kéo vĩ liên tục vs Gảy buông:** Nhạc cụ kéo vĩ có pha duy trì ổn định, độ suy giảm sau 0,4s $D_{0{,}4} \approx 0\text{ dB}$; trong khi Guitar acoustic gảy buông năng lượng tắt dốc rất nhanh ($D_{0{,}4} = -7{,}1\text{ dB}$).
- **Giá trị thông tin:** Đây là đặc trưng then chốt để phân loại cơ chế kích âm cơ học, giải quyết sự nhập nhằng giữa các nhạc cụ có dải âm vực gần nhau.

##### 4. Tốc độ qua điểm không (Zero-Crossing Rate - ZCR - 1 giá trị, 2 chiều sau pooling)
- **Đặc trưng là gì:** ZCR đo tỷ lệ tín hiệu âm thanh đổi dấu giữa các mẫu kế tiếp, phản ánh độ nhám bề mặt dạng sóng, độ nhiễu và hiện tượng méo cắt đỉnh biên độ (clipping).
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Các tệp âm thanh có cùng độ mịn sạch dạng sóng sẽ có ZCR gần nhau.
  - *Khác biệt:* Tách biệt Guitar điện méo tiếng (dạng sóng răng cưa bão hòa, $\text{ZCR} = 0{,}11 \pm 0{,}04$) khỏi 5 nhạc cụ mộc ($\text{ZCR} = 0{,}02 \div 0{,}09$).
- **Giá trị thông tin:** Cung cấp chỉ số nhạy bén để nhận diện hiệu ứng xử lý âm thanh điện tử và độ trơn nhẵn của sóng âm.

---

#### 4.4.3. Bộ C: Trọng tâm phổ và hòa âm cao độ (Spectral Centroid & Chroma STFT)

##### 5. Trọng tâm phổ (Spectral Centroid - 1 giá trị, 2 chiều sau pooling)
- **Đặc trưng là gì:** Spectral Centroid là momen bậc 1 của phổ tần số (tâm khối phổ). Trong tâm lý học thính giác (Psychoacoustics), đại lượng này tương quan chặt chẽ với cảm nhận trực giác của con người về **"độ sáng" (Brightness)** của âm thanh.
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Các tệp âm thanh có cùng cảm nhận về độ sáng/độ tối sẽ có khoảng cách Centroid rất nhỏ.
  - *Khác biệt:* Phân tầng độ sáng rõ rệt giữa các nhạc cụ họ vĩ: $\text{Double Bass } (497\text{ Hz}) < \text{Cello } (818\text{ Hz}) < \text{Viola } (895\text{ Hz}) < \text{Violin } (1708\text{ Hz})$.
- **Giá trị thông tin:** Cung cấp thông tin định lượng trực quan về cảm nhận màu âm thính giác, bổ sung khía cạnh mà MFCC không lượng hóa trực tiếp thành một trục tần số duy nhất.

##### 6. Đặc trưng 12 nửa cung (Chroma STFT - 12 nửa cung, 24 chiều sau pooling)
- **Đặc trưng là gì:** Chroma STFT gập toàn bộ dải phổ công suất về 12 nửa cung chuẩn nhạc lý phương Tây ($\text{C, C\#, D, D\#, E, F, F\#, G, G\#, A, A\#, B}$) dựa trên tính tương đương quãng tám (Octave Equivalence).
- **Tìm tương đồng / khác biệt như thế nào:**
  - *Tương đồng:* Tìm kiếm các đoạn nhạc có cùng vòng hòa âm hoặc cùng nốt giai điệu chủ đạo bất kể chơi ở quãng tám nào.
  - *Khác biệt:* **Phân biệt lối chơi Đơn âm (Monophonic) vs Đa âm hợp âm (Polyphonic):** Nhạc cụ họ vĩ chủ yếu chơi đơn âm nên vector Chroma có các đỉnh nhọn cục bộ tập trung vào 1-2 nốt; trong khi Guitar thường đệm hợp âm quạt/rải nên năng lượng Chroma trải đều qua nhiều nửa cung cùng lúc.
- **Giá trị thông tin:** Nắm bắt khía cạnh âm nhạc học (Musical Semantics), giúp tháo gỡ sự chồng lấn âm vực giữa các nhạc cụ cùng họ (như Viola và Cello).

![Hình 4.2: Minh họa trích xuất 3 bộ đặc trưng](hinh/8_chi_tiet_trich_xuat_3_bo_dac_trung.png)

*Hình 4.2: Minh họa chi tiết cơ chế trích xuất toán học của 3 bộ đặc trưng trên tín hiệu thực tế (Bộ A: Roll-off 85% & 13 MFCC; Bộ B: Khung sóng ZCR/RMS & Đường bao thời gian; Bộ C: Trọng tâm phổ Centroid & 12 nửa cung Chroma STFT) — sinh bởi kịch bản `src/trich_xuat_va_ve_dac_trung.py`.*

---

### 4.5. Bộ đặc trưng được sử dụng chính và cơ chế kết hợp bổ trợ (Fusion)

Nhóm quyết định lựa chọn **Bộ đặc trưng Âm sắc / Bao phổ (Bộ A - MFCC & Spectral Roll-off, 28 chiều)** làm **bộ đặc trưng nòng cốt (Chính)** cho hệ thống tìm kiếm CBAR, vì các lý do sau:

1. **Khả năng khái quát hóa âm sắc vượt trội:** MFCC bóc tách trực tiếp dấu ấn vật lý của thùng đàn và amply, giúp tìm kiếm tệp cùng loại nhạc cụ độc lập hoàn toàn với nốt nhạc đang chơi.
2. **Không bị ảnh hưởng bởi kỹ thuật chơi ngắt quãng:** Dù người chơi diễn tấu kéo dài (legato) hay ngắt rời (staccato), cấu trúc formant của thùng đàn phản ánh qua MFCC vẫn được giữ nguyên.
3. **Độ ổn định cao:** Không phụ thuộc vào thuật toán dò cao độ cơ bản (vốn thường xuyên mắc lỗi sub-harmonic khi gặp tín hiệu hợp âm đa âm).

**Cơ chế kết hợp bổ trợ (Fusion) với Bộ B và Bộ C:**
Một bộ đặc trưng duy nhất không thể giải quyết mọi trường hợp nhập nhằng. Vì vậy, Bộ B (RMS, ZCR) và Bộ C (Centroid, Chroma) đóng vai trò bổ trợ thiết yếu theo bảng ma trận tương hỗ sau:

| Cặp nhạc cụ thách thức | Điểm giống nhau gây nhầm lẫn | Bộ đặc trưng nòng cốt giải quyết | Cơ chế phân biệt cụ thể |
| :---|:---|:---:|:---|
| **1. Violin vs Viola** | Cùng thuộc họ vĩ, thùng gỗ số 8, cùng kéo vĩ liên tục ($D_{0{,}4} \approx 0\text{ dB}$, $\sigma_{\text{RMS}}$ thấp) | **Bộ C (Centroid)** & **Bộ A (MFCC)** | Thùng Violin nhỏ hơn và dây ngắn hơn làm $\text{Centroid} = 1708\text{ Hz}$ cao hơn hẳn Viola ($895\text{ Hz}$); các hệ số MFCC đầu ghi nhận sự khác biệt về thể tích thùng đàn. |
| **2. Viola vs Cello** | Chồng lấn dải cao độ ở vùng $190 - 200\text{ Hz}$ (nốt G3 - G#3 chơi được trên cả 2 đàn) | **Bộ A (MFCC)** & **Bộ C (Chroma)** | Thùng Cello lớn đặt sàn hấp thụ dải cao làm $\text{Roll-off} = 1417\text{ Hz}$ thấp hơn Viola ($1611\text{ Hz}$). Năng lượng Chroma ghi nhận sự khác biệt của hệ dây buông C2-G2-D3-A3 so với C3-G3-D4-A4. |
| **3. Cello vs Double Bass** | Cùng đảm nhận dải âm trầm, âm sắc tối ấm, cùng kéo vĩ | **Bộ A (Roll-off)** & **Bộ C (Centroid)** | Double Bass dồn 85% năng lượng dưới $771\text{ Hz}$ ($\text{Centroid} = 497\text{ Hz}$), trong khi Cello mở rộng tới $1417\text{ Hz}$ ($\text{Centroid} = 818\text{ Hz}$), tạo ranh giới phân tách rõ ràng. |
| **4. Guitar mộc vs Cello Pizzicato** | Cùng có mức suy giảm năng lượng dốc sau khi buông ngón ($D_{0{,}4} \approx -7\text{ dB}$) | **Bộ C (Chroma)** & **Bộ A (MFCC)** | Cello pizzicato vẫn chủ yếu chơi đơn nốt (Chroma tập trung nhọn); Guitar mộc quạt hợp âm nhiều dây (Chroma phân tán). MFCC bóc tách sự khác biệt giữa thùng vĩ và thùng phẳng guitar. |
| **5. Guitar mộc vs Guitar điện** | Cùng 6 dây kim loại, cùng dùng ngón/móng gảy | **Bộ B (RMS, ZCR)** & **Bộ A (MFCC)** | Guitar điện có mạch nén biên độ ($\sigma_{\text{RMS}} = 0{,}05$), ZCR cao vượt trội ($0{,}11$) và $c_2 = -71{,}7$ (rất âm) do méo tiếng; Guitar mộc tắt dốc nhanh ($\sigma_{\text{RMS}} = 0{,}06$, $D_{0{,}4} = -7{,}1\text{ dB}$), ZCR thấp ($0{,}06$). |

---

### 4.6. Chuẩn hóa đặc trưng Z-score và nguyên tắc chống rò rỉ dữ liệu

Các thành phần trong vector 58 chiều có đơn vị và thang đo chênh lệch rất lớn: Centroid và Roll-off lên tới hàng nghìn Hertz; MFCC từ $-300$ đến $+200$; trong khi RMS, ZCR, Chroma nằm trong khoảng $0$ đến $1$. Nếu không chuẩn hóa, các đặc trưng có giá trị tuyệt đối lớn (như Roll-off) sẽ chi phối hoàn toàn khoảng cách Euclidean, làm vô hiệu hóa các đặc trưng quan trọng có thang đo nhỏ.

Hệ thống áp dụng chuẩn hóa **Z-score (Standard Normalization)** trên từng chiều đặc trưng:

$$
z_j = \frac{v_j - \mu_j^{(\text{gallery})}}{\sigma_j^{(\text{gallery})} + 10^{-9}}, \quad j = 1, 2, \dots, 58
$$

**Nguyên tắc chống rò rỉ dữ liệu (Data Leakage):**
Tham số chuẩn hóa $\mu_j^{(\text{gallery})}$ và $\sigma_j^{(\text{gallery})}$ **chỉ được tính toán một lần duy nhất trên tập dữ liệu cơ sở (Gallery)**. Khi tiếp nhận một tệp truy vấn mới (Query), vector đặc trưng của tệp truy vấn phải được chuẩn hóa bằng chính các tham số $\mu^{(\text{gallery})}, \sigma^{(\text{gallery})}$ đã lưu sẵn; tuyệt đối không tính gộp tệp truy vấn vào để tính lại giá trị trung bình và độ lệch chuẩn, nhằm bảo đảm tính khách quan và chống rò rỉ thông tin kiểm thử.

---

### 4.7. Độ đo khoảng cách chuẩn hóa RMSD và cơ chế xếp hạng Top-5 file tương đồng nhất

#### 4.7.1. Xử lý nguy cơ mất cân bằng số chiều giữa các nhóm (Dimensional Dominance)

Nếu tính khoảng cách Euclidean thông thường trên từng bộ đặc trưng:
- Bộ A có $\dim_A = 28$ chiều.
- Bộ B có $\dim_B = 4$ chiều.
- Bộ C có $\dim_C = 26$ chiều.

Về mặt toán học xác suất, kỳ vọng độ lớn khoảng cách Euclidean của một nhóm tỷ lệ thuận với căn bậc hai số chiều: $\mathbb{E}[d_k] \propto \sqrt{\dim_k}$. Do đó, khoảng cách của nhóm A tự nhiên sẽ lớn hơn khoảng cách của nhóm B khoảng $\sqrt{28/4} \approx 2{,}65$ lần. Nếu gộp trực tiếp có trọng số, nhóm 28 chiều sẽ lấn át hoàn toàn nhóm 4 chiều bất kể vai trò phân biệt Kéo vĩ vs Gảy dây của Bộ B là cực kỳ quan trọng.

Để khắc phục hiện tượng này, hệ thống áp dụng **khoảng cách Euclidean chuẩn hóa theo số chiều (Root-Mean-Square Distance - RMSD)** cho từng nhóm:

$$
d_k^*(\mathbf{q}_k, \mathbf{x}_k) = \sqrt{\frac{1}{\dim_k} \sum_{j=1}^{\dim_k} (q_{k,j} - x_{k,j})^2}, \quad k \in \{A, B, C\}
$$

Phép chia cho $\dim_k$ đưa khoảng cách trung bình trên mỗi chiều của cả 3 nhóm về cùng một thang đo tương đương, bảo đảm tính công bằng khi gộp.

#### 4.7.2. Hàm khoảng cách tổng hợp có trọng số

Khoảng cách tổng hợp giữa vector truy vấn $\mathbf{q}$ và vector ứng viên $\mathbf{x}$ trong CSDL là:

$$
d_{\text{total}}(\mathbf{q}, \mathbf{x}) = \lambda_1 d_A^*(\mathbf{q}_A, \mathbf{x}_A) + \lambda_2 d_B^*(\mathbf{q}_B, \mathbf{x}_B) + \lambda_3 d_C^*(\mathbf{q}_C, \mathbf{x}_C)
$$

với điều kiện ràng buộc chuẩn hóa trọng số:

$$
\lambda_1 + \lambda_2 + \lambda_3 = 1, \quad \lambda_i \ge 0
$$

- $\lambda_1$: Trọng số nhóm Âm sắc & Bao phổ (Bộ A - đóng vai trò chính, đề xuất khởi tạo $\lambda_1 = 0{,}50$).
- $\lambda_2$: Trọng số nhóm Năng lượng & Động học thời gian (Bộ B - bổ trợ kéo/gảy, đề xuất $\lambda_2 = 0{,}25$).
- $\lambda_3$: Trọng số nhóm Trọng tâm phổ & Cao độ hòa âm (Bộ C - bổ trợ độ sáng/hợp âm, đề xuất $\lambda_3 = 0{,}25$).

*Nguyên tắc xác định trọng số:* Các trọng số $\boldsymbol{\lambda}$ trên đây là cấu hình khởi tạo dựa trên phân tích âm học; trong Nhiệm vụ 4, bộ trọng số tối ưu sẽ được tinh chỉnh tự động thông qua tìm kiếm lưới (Grid Search) trên tập kiểm thực (Validation Set).

#### 4.7.3. Quy trình thực thi tìm kiếm Top-5 tệp tương đồng nhất

Khi người dùng cung cấp một tệp âm thanh truy vấn mới $x_{\text{query}}(t)$:
1. **Tiền xử lý:** Chuyển mono, đổi tần số mẫu về $22\,050\text{ Hz}$, chuẩn hóa biên độ đỉnh về 0,9.
2. **Trích xuất đặc trưng:** Trích xuất vector 58 chiều $\mathbf{q} \in \mathbb{R}^{58}$ theo đúng quy trình 4 bước ở Mục 4.3.
3. **Chuẩn hóa Z-score:** Chuẩn hóa vector $\mathbf{q}$ bằng tham số $\mu^{(\text{gallery})}, \sigma^{(\text{gallery})}$.
4. **Tính khoảng cách:** Tính $d_{\text{total}}(\mathbf{q}, \mathbf{x}^{(i)})$ tới toàn bộ các vector trong cơ sở dữ liệu.
5. **Xử lý tệp trùng (Leave-One-Out):** Nếu tệp truy vấn là tệp đã có trong CSDL (khoảng cách $d = 0$), tệp này được loại bỏ khỏi danh sách trước khi xếp hạng.
6. **Xếp hạng và trả về:** Sắp xếp danh sách theo thứ tự khoảng cách tăng dần:
   $$
   d_{(1)} \le d_{(2)} \le d_{(3)} \le d_{(4)} \le d_{(5)} \le \dots
   $$
   Hệ thống trích xuất và hiển thị danh sách **Top-5** tệp có khoảng cách nhỏ nhất, kèm tên file, nhãn nhạc cụ dự đoán và chỉ số độ tương đồng.

---

### 4.8. Đề xuất phương pháp luận đánh giá hệ thống tìm kiếm cho Nhiệm vụ 4

Để đánh giá khoa học hiệu năng của hệ thống CBAR ở Nhiệm vụ 4 tiếp theo, báo cáo đề xuất phương pháp luận và các chỉ số đo đạc chuẩn mực:

#### 4.8.1. Phân chia dữ liệu theo bản ghi nguồn độc lập (Source-wise Splitting)
Nếu chia ngẫu nhiên từng tệp (Random Splitting), hai đoạn cắt từ cùng một bài hát của cùng một nghệ sĩ có thể rơi vào cả tập Gallery và Query, dẫn đến hiện tượng nhận diện lại bản ghi cụ thể (Source Leakage). Do đó, việc chia tập bắt buộc phải thực hiện theo **bản ghi nguồn độc lập (Source-wise)**:
- Tập Gallery (Tham chiếu): 80% số track nguồn gốc của mỗi nhạc cụ.
- Tập Query (Kiểm thử): 20% số track nguồn gốc còn lại, bảo đảm hoàn toàn độc lập về bản thu và nghệ sĩ.

#### 4.8.2. Các chỉ số đánh giá truy hồi đề xuất
1. **Độ chính xác Top-5 (Precision@5):**
   $$
   \text{Precision@5} = \frac{\text{Số tệp đúng nhạc cụ trong Top-5}}{5}
   $$
2. **Mean Average Precision (MAP@5):** Đánh giá cả thứ tự ưu tiên của kết quả trả về (kết quả đúng xuất hiện ở vị trí Top-1 được tính trọng số điểm cao hơn Top-5):
   $$
   \text{AP@5} = \frac{1}{\min(R, 5)} \sum_{k=1}^5 P(k) \cdot \operatorname{rel}(k)
   $$
   trong đó $P(k)$ là độ chính xác tại vị trí cắt $k$, $\operatorname{rel}(k) \in \{0, 1\}$ là chỉ thị đúng/sai của tệp thứ $k$, và $R$ là tổng số tệp liên quan trong cơ sở dữ liệu.

---

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
