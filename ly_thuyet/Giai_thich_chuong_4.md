# Giải thích dễ hiểu Chương 4 – Bộ đặc trưng âm thanh

Tài liệu này giải thích nội dung trong báo cáo Chương 4 bằng lời dễ hiểu hơn. Trọng tâm là: vì sao có **3 bộ tổng hợp nhưng 6 loại đặc trưng**, 58 chiều được tạo ra thế nào, mỗi đặc trưng đo điều gì, và đọc các bảng so sánh ra sao.

## 1. Chương 4 đang giải quyết việc gì?

Mỗi tệp WAV chứa rất nhiều mẫu âm thanh nối tiếp theo thời gian. Máy tính không thể so sánh hai tệp chỉ bằng cách nhìn tên tệp hoặc nghe như con người. Ta cần chuyển mỗi đoạn âm thanh thành một dãy số cố định, gọi là **vector đặc trưng**.

Trong báo cáo, mỗi tệp được biểu diễn bằng một vector có **58 số thực**. Các số này tóm tắt một số dấu hiệu của âm thanh như:

- hình dạng phổ và âm sắc;
- mức năng lượng cùng sự thay đổi của năng lượng;
- độ sáng phổ;
- phân bố các lớp cao độ.

Khi hai vector gần nhau, ta nói hai tệp giống nhau hơn **theo những đặc trưng đã chọn**. Điều đó không đồng nghĩa chúng chắc chắn do cùng một nhạc cụ phát ra; cao độ, cách chơi, người chơi và thiết bị thu cũng có thể làm vector thay đổi.

## 2. Vì sao có 3 bộ đặc trưng nhưng 6 loại đặc trưng?

Đây là hai cấp gọi tên khác nhau:

- **Loại đặc trưng** là từng phép đo cụ thể, gồm MFCC, Spectral Roll-off, RMS Energy, Zero-Crossing Rate, Spectral Centroid và Chroma STFT: tổng cộng **6 loại**.
- **Bộ đặc trưng** là cách báo cáo gom các loại có vai trò gần nhau thành các nhóm lớn để tiện trình bày và so sánh: tổng cộng **3 bộ**.

Ba bộ trong báo cáo được chia như sau:

| Bộ tổng hợp                                  | Gồm những loại nào?                     |   Số chiều | Nói đơn giản, bộ này mô tả gì?                                                        |
| ----------------------------------------------- | ------------------------------------------- | -----------: | ---------------------------------------------------------------------------------------------- |
| A – Âm sắc và phổ                          | MFCC (26) + Spectral Roll-off (2)           |           28 | Hình dạng phổ âm và phổ trải tới vùng tần số nào                                   |
| B – Năng lượng và biến thiên dạng sóng | RMS Energy (2) + Zero-Crossing Rate (2)     |            4 | Âm mạnh yếu ra sao và dạng sóng đổi dấu nhiều hay ít                                |
| C – Độ sáng phổ và lớp cao độ          | Spectral Centroid (2) + Chroma STFT (24)    |           26 | Trọng tâm phổ nghiêng về vùng tần số nào và năng lượng thuộc các lớp nốt nào |
| **Tổng**                                 | **6 loại đặc trưng thành phần** | **58** | **Vector cố định dùng để lưu trữ, so sánh**                                     |

Ba bộ A, B, C là **cách tổ chức của báo cáo**, không phải ba thuật toán phân loại. Sáu loại đặc trưng vẫn được tính riêng; khi cần so sánh, có thể xem từng loại, từng bộ, hoặc ghép cả 58 chiều.

## 3. Âm thanh được biến thành 58 số như thế nào?

### 3.1. Chia âm thanh thành các khung ngắn

Âm thanh được lấy mẫu ở 22.050 mẫu/giây. Mỗi khung dùng 2.048 mẫu, tương đương khoảng **92,9 mili giây**. Khung kế tiếp bắt đầu sau mỗi 512 mẫu, tương đương khoảng **23,2 mili giây**. Các khung chồng lấn lên nhau để theo dõi âm thanh biến đổi liên tục.

Với đoạn dài khoảng 3 giây, có xấp xỉ 130 khung. Tệp 2,8 giây và 3,2 giây sẽ có số khung khác nhau. Vì vậy, đặc trưng tính theo từng khung ban đầu là một chuỗi hoặc một ma trận có độ dài thay đổi theo tệp.

### 3.2. Temporal Pooling: tóm tắt theo thời gian

Để mọi tệp đều có vector cùng kích thước, báo cáo dùng hai thống kê cho mỗi chuỗi đặc trưng:

- **Mean (trung bình)**: mức điển hình của đặc trưng trong toàn đoạn.
- **Std (độ lệch chuẩn)**: mức đặc trưng thay đổi giữa các khung. Std thấp thường biểu thị giá trị khá ổn định; std cao biểu thị giá trị thay đổi nhiều hơn.

Với một chuỗi có M khung và giá trị ở khung m là x(m), hai phép tính có thể viết như sau:

    Mean = (x(1) + x(2) + ... + x(M)) / M

    Std = căn bậc hai của trung bình các bình phương sai lệch so với Mean

Mean và Std **không giữ lại chính xác thứ tự thời gian**. Chúng tóm tắt mức trung bình và mức dao động, chứ không ghi rằng âm nào xảy ra trước hay sau.

Ví dụ: nếu một đặc trưng có 13 chuỗi giá trị theo thời gian, ta lưu 13 Mean và 13 Std, tổng cộng 26 số. Nếu đặc trưng chỉ tạo một chuỗi, ta lưu 1 Mean và 1 Std, tổng cộng 2 số.

### 3.3. Phép cộng tạo nên 58 chiều

| Thành phần       |  Số giá trị theo mỗi khung | Thống kê lưu cho mỗi giá trị | Số chiều sau khi gộp |
| ------------------ | -----------------------------: | ---------------------------------: | ----------------------: |
| MFCC               |                     13 hệ số |                       Mean và Std |            13 × 2 = 26 |
| Spectral Roll-off  |                              1 |                       Mean và Std |              1 × 2 = 2 |
| RMS Energy         |                              1 |                       Mean và Std |              1 × 2 = 2 |
| Zero-Crossing Rate |                              1 |                       Mean và Std |              1 × 2 = 2 |
| Spectral Centroid  |                              1 |                       Mean và Std |              1 × 2 = 2 |
| Chroma STFT        |               12 lớp cao độ |                       Mean và Std |            12 × 2 = 24 |
| **Tổng**    | **29 chuỗi theo khung** | **2 thống kê mỗi chuỗi** |  **29 × 2 = 58** |

Tính theo ba bộ:

- Bộ A: 26 + 2 = **28 chiều**.
- Bộ B: 2 + 2 = **4 chiều**.
- Bộ C: 2 + 24 = **26 chiều**.
- Toàn bộ: 28 + 4 + 26 = **58 chiều**.

## 4. Giải thích từng loại đặc trưng

### 4.1. MFCC – 26 chiều, thuộc Bộ A

Ở mỗi khung, MFCC tạo 13 hệ số: c₀ đến c₁₂. Có thể hiểu đơn giản, các hệ số này nén hình dạng phổ âm thành một nhóm số ngắn. Chúng thường được dùng để so sánh **màu âm** và **dạng bao phổ**.

Mỗi hệ số có một Mean và một Std:

- 13 Mean tóm tắt hình dạng phổ log-Mel điển hình của đoạn.
- 13 Std tóm tắt mỗi hệ số thay đổi ra sao giữa các khung.
- Vì thế MFCC có 13 × 2 = **26 chiều**.

Hai tệp có các giá trị MFCC gần nhau sau chuẩn hóa thường gần nhau hơn về hình dạng phổ mà MFCC mô tả. MFCC không phải phép đo trực tiếp loại gỗ, kích thước đàn hay một họa âm cụ thể; kết quả còn chịu ảnh hưởng của nốt, kỹ thuật chơi và thiết bị thu.

Trong Bảng 4.3, MFCC có RMSD trung vị **0,886** cho các cặp cùng nhãn và **1,325** cho các cặp khác nhãn. Theo cách đo này, các cặp khác nhãn thường xa nhau hơn, nên MFCC có dấu hiệu hữu ích để phân biệt trên tập dữ liệu đã khảo sát. Chênh lệch này không có nghĩa mọi cặp khác nhãn đều xa hơn mọi cặp cùng nhãn.

### 4.2. Spectral Roll-off – 2 chiều, thuộc Bộ A

Ở từng khung, Roll-off 85% tìm tần số mà phía dưới nó đã tích lũy ít nhất 85% tổng độ lớn phổ. Nói dễ hiểu, nó tóm tắt **phổ trải tới vùng tần số nào**. Giá trị được đo bằng Hz.

Sau đó lấy:

- rolloff_mean: ngưỡng tần số điển hình trong đoạn;
- rolloff_std: ngưỡng này thay đổi nhiều hay ít giữa các khung.

Một giá trị theo khung nhân với hai thống kê tạo **2 chiều**. Con số 85% là ngưỡng quy ước của phép tính, không phải giới hạn tần số cố định của một nhạc cụ.

Bảng 4.3 ghi **0,458** cho cặp cùng nhãn và **1,277** cho cặp khác nhãn. Hai số này cách nhau khá rõ, nên nhận xét “Tách phạm vi phổ khá rõ” có nghĩa là đặc trưng Roll-off tạo ra khoảng cách nhỏ hơn ở các cặp cùng nhạc cụ và lớn hơn ở các cặp khác nhạc cụ trong phép đo này.

### 4.3. RMS Energy – 2 chiều, thuộc Bộ B

RMS là căn bậc hai của trung bình bình phương các mẫu trong một khung. Có thể hình dung nó như mức năng lượng hiệu dụng, gần với việc tóm tắt âm thanh đang mạnh hay yếu trong khung đó.

- rms_mean: mức năng lượng điển hình của cả đoạn.
- rms_std: mức năng lượng dao động giữa các khung.
- Một chuỗi RMS tạo 1 Mean và 1 Std, tổng cộng **2 chiều**.

Nếu rms_std lớn, năng lượng biến đổi nhiều hơn trong đoạn; nếu nhỏ, năng lượng ổn định hơn. Đây có thể là dấu hiệu hỗ trợ nhận biết âm duy trì đều hoặc âm mạnh lúc đầu rồi suy giảm. Tuy nhiên, âm lượng thu, cường độ người chơi và việc chuẩn hóa âm lượng cũng làm RMS thay đổi.

Trong Bảng 4.3, RMS có **0,859** ở cặp cùng nhãn và **1,250** ở cặp khác nhãn. Đây là dấu hiệu năng lượng có đóng góp, nhưng không nên dùng riêng RMS để kết luận một âm thanh thuộc nhạc cụ nào.

### 4.4. Zero-Crossing Rate – 2 chiều, thuộc Bộ B

Zero-Crossing Rate (ZCR) đo tỷ lệ các cặp mẫu liên tiếp đổi dấu, tức tín hiệu chuyển từ phía âm sang phía dương hoặc ngược lại. Đây là dấu hiệu lấy trực tiếp từ dạng sóng.

- zcr_mean: tỷ lệ đổi dấu điển hình qua các khung.
- zcr_std: mức tỷ lệ đổi dấu biến thiên ra sao.
- Một chuỗi ZCR tạo 1 Mean và 1 Std, tổng cộng **2 chiều**.

ZCR bổ sung một góc nhìn khác với các đặc trưng dựa trên phổ. Nó có thể phản ánh độ nhám hoặc thành phần thay đổi nhanh, nhưng ZCR cao **không tự động có nghĩa** âm thanh bị méo hay clipping.

Trong Bảng 4.3, khoảng cách trung vị là **0,432** cho cùng nhãn và **0,926** cho khác nhãn. Nhận xét “Bổ sung dấu hiệu biến thiên dạng sóng” nghĩa là ZCR thêm thông tin từ số lần dạng sóng đổi dấu; nó bổ trợ cho các đặc trưng khác chứ không mô tả toàn bộ âm thanh.

### 4.5. Spectral Centroid – 2 chiều, thuộc Bộ C

Spectral Centroid là trung bình có trọng số của các tần số trong phổ. Có thể hình dung nó như **trọng tâm của phổ**:

- centroid cao thường có nghĩa phổ có tương đối nhiều năng lượng ở các tần số cao;
- centroid thấp thường có nghĩa trọng tâm phổ nằm về phía tần số thấp hơn.

Đây là cách diễn giải về phổ của bản ghi, không phải phép đo trực tiếp kích thước thùng đàn hay chất liệu nhạc cụ.

- centroid_mean: vị trí trọng tâm phổ điển hình, đơn vị Hz.
- centroid_std: mức trọng tâm phổ thay đổi theo thời gian.
- Một chuỗi centroid tạo **2 chiều**.

Bảng 4.3 có **0,494** cho cùng nhãn và **1,276** cho khác nhãn, cho thấy centroid có dấu hiệu phân biệt trên tập đang xét. Bảng 4.4 cũng cho thấy centroid_mean có MI cao nhất trong các chiều được liệt kê: **0,813 nat**.

### 4.6. Chroma STFT – 24 chiều, thuộc Bộ C

Chroma gom năng lượng phổ vào 12 lớp cao độ: C (Đô), C♯ (Đô thăng), D (Rê), D♯ (Rê thăng), E (Mi), F (Fa), F♯ (Fa thăng), G (Sol), G♯ (Sol thăng), A (La), A♯ (La thăng) và B (Si). Ký hiệu ♯ đọc là “thăng”, nghĩa là cao hơn nốt tự nhiên liền trước một nửa cung; vì vậy C♯ là Đô thăng, nằm giữa C (Đô) và D (Rê). Các nốt cùng tên ở những quãng tám khác nhau được gom vào cùng một lớp. Vì vậy, Chroma tập trung vào **lớp cao độ**, không giữ nguyên thông tin quãng tám như tần số gốc.

Với mỗi lớp trong 12 lớp, ta lưu:

- Mean của lớp đó qua các khung;
- Std của lớp đó qua các khung.

Do đó, Chroma có 12 × 2 = **24 chiều**. Ví dụ chroma_0_mean tóm tắt đáp ứng trung bình của lớp C; chroma_0_std tóm tắt đáp ứng lớp C thay đổi giữa các khung thế nào. Các chỉ số 1 đến 11 lần lượt ứng với C♯ đến B.

Chroma hữu ích khi muốn biết hai đoạn có các lớp nốt hoặc phân bố nốt tương tự không. Nhưng nó phụ thuộc nhiều vào nốt hay hợp âm đang chơi. Hai nhạc cụ khác loại chơi cùng một nốt có thể có Chroma gần nhau, dù âm sắc khác nhau.

Trong Bảng 4.3, Chroma có **1,272** cho cùng nhãn và **1,394** cho khác nhãn. Hai giá trị khá gần nhau, nên riêng phép đo này cho thấy Chroma phân biệt nhãn nhạc cụ yếu hơn các loại đặc trưng khác. Điều đó không có nghĩa Chroma vô dụng: nó bổ sung thông tin về nội dung cao độ.

## 5. Bảng 4.2: hiểu 58 tọa độ cụ thể

Mỗi dòng của Bảng 4.2 là **một số** trong vector 58 chiều. Tên trường cho biết số đó thuộc đặc trưng nào và là thống kê nào:

- hậu tố _mean: giá trị trung bình qua các khung;
- hậu tố _std: độ lệch chuẩn qua các khung;
- mfcc_i: hệ số MFCC thứ i;
- chroma_i: lớp cao độ thứ i, với chỉ số 0–11 ứng với C đến B.

Thứ tự lưu trong báo cáo là:

1. Hai chiều RMS: rms_mean, rms_std.
2. Hai chiều ZCR: zcr_mean, zcr_std.
3. Hai chiều Centroid: centroid_mean, centroid_std.
4. Hai chiều Roll-off: rolloff_mean, rolloff_std.
5. Hai chiều cho từng hệ số MFCC từ 0 đến 12: mfcc_0_mean, mfcc_0_std, ... mfcc_12_mean, mfcc_12_std.
6. Hai chiều cho từng lớp Chroma từ 0 đến 11: chroma_0_mean, chroma_0_std, ... chroma_11_mean, chroma_11_std.

Vì vậy, thứ tự các dòng Bảng 4.2 không xếp lần lượt theo Bộ A, B, C. Cột “Bộ” mới cho biết từng tọa độ thuộc nhóm tổng hợp nào. Khi đọc hoặc lưu vector, cần giữ nguyên thứ tự tọa độ để không gán nhầm giá trị cho đặc trưng.

## 6. Chuẩn hóa: vì sao cần Z-score?

Các đặc trưng có đơn vị và cỡ giá trị khác nhau. Centroid và Roll-off tính bằng Hz; ZCR và Chroma có thang khác; RMS phụ thuộc mức biên độ. Nếu tính khoảng cách trực tiếp, những chiều có trị số lớn có thể chi phối phép đo chỉ vì đơn vị lớn.

Z-score đưa từng chiều về một thang so sánh chung:

    z = (x - trung bình của chiều đó) / độ lệch chuẩn của chiều đó

Trong đó x là giá trị ban đầu. Sau chuẩn hóa, z cho biết giá trị đó cách trung bình của chiều bao nhiêu độ lệch chuẩn. Các tham số trung bình và độ lệch chuẩn phải được tính từ tập tham chiếu rồi giữ cố định khi chuẩn hóa tệp truy vấn mới.

## 7. “Cùng nhạc cụ” và “Khác nhạc cụ” nghĩa là gì?

Trong các bảng, hai cụm này được xác định theo **nhãn đã gán trong bộ dữ liệu**:

- “Cùng nhạc cụ”: chọn hai tệp có cùng nhãn, ví dụ cả hai cùng mang nhãn Violin.
- “Khác nhạc cụ”: chọn hai tệp mang hai nhãn khác nhau, ví dụ một tệp Violin và một tệp Cello.

Đây là cách chia các cặp để kiểm tra khoảng cách đặc trưng. Nó không nói rằng hai tệp cùng nhãn có cùng nốt, người chơi hoặc cách diễn tấu. Tương tự, hai tệp khác nhãn vẫn có thể chơi cùng một nốt hoặc có âm thanh gần nhau.

## 8. Bảng 4.3: khoảng cách Euclid RMSD và cột “Nhận xét”

### 8.1. Cột “Cùng nhạc cụ” và “Khác nhạc cụ” là con số gì?

Trước tiên, mỗi tệp được biểu diễn bằng các chiều đặc trưng đã chuẩn hóa Z-score. Với hai tệp a và b, báo cáo tính căn trung bình bình phương sai khác trên k chiều:

    RMSD(a,b) = căn bậc hai của [tổng bình phương (z_a,j - z_b,j), với j từ 1 đến k, chia cho k]

Đây là khoảng cách Euclid L2 đã chia cho căn bậc hai số chiều. Nó **không phải Manhattan**. Chia cho căn bậc hai số chiều giúp so sánh các nhóm có số chiều khác nhau, ví dụ MFCC 26 chiều với RMS 2 chiều.

Sau khi tính khoảng cách cho mọi cặp, lấy **trung vị** riêng cho cặp cùng nhãn và cặp khác nhãn. Trung vị là giá trị ở giữa khi các khoảng cách được sắp xếp; đây không phải khoảng cách của một tệp cụ thể.

Trên dữ liệu báo cáo có 600 tệp, sáu nhãn và 100 tệp mỗi nhãn:

- Có 6 × C(100, 2) = **29.700 cặp cùng nhãn**.
- Có C(6, 2) × 100 × 100 = **150.000 cặp khác nhãn**.

### 8.2. Đọc một dòng mẫu

Với MFCC, Bảng 4.3 ghi:

Hiểu đơn giản: khi so sánh 26 chiều MFCC, khoảng cách ở giữa các cặp khác nhãn lớn hơn khoảng cách ở giữa các cặp cùng nhãn. Đây là xu hướng có lợi cho việc phân biệt nhãn bằng MFCC trên tập dữ liệu này. Tuy vậy, hai nhóm khoảng cách vẫn có thể chồng lấn: có cặp khác nhãn rất gần nhau và có cặp cùng nhãn khá xa nhau.

### 8.3. Giải nghĩa nhận xét cho từng dòng

| Đặc trưng       | Cùng / khác | Ý của nhận xét trong bảng                                                                                                                                                                                                   |
| ------------------ | ------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MFCC               | 0,886 / 1,325 | Các hệ số MFCC tóm tắt dạng phổ. Cặp cùng nhãn gần nhau hơn ở trung vị, còn cặp khác nhãn xa hơn; vì vậy MFCC cung cấp dấu hiệu về màu âm và dạng bao phổ.                                         |
| Spectral Roll-off  | 0,458 / 1,277 | Cặp cùng nhãn gần nhau khá rõ so với cặp khác nhãn. Roll-off tóm tắt ngưỡng tần số chứa phần lớn độ lớn phổ, nên nhận xét nói đặc trưng này giúp tách các phạm vi phổ trong tập đang xét. |
| RMS Energy         | 0,859 / 1,250 | Mức năng lượng và biến động năng lượng khác nhau phần nào giữa các nhãn. RMS bổ sung dấu hiệu về đường bao năng lượng, nhưng cũng chịu ảnh hưởng của âm lượng và cách thu.                |
| Zero-Crossing Rate | 0,432 / 0,926 | Tỷ lệ đổi dấu của dạng sóng có khác biệt giữa các cặp theo nhãn. Đây là dấu hiệu bổ sung từ dạng sóng, không phải bằng chứng riêng rằng âm thanh bị méo.                                        |
| Spectral Centroid  | 0,494 / 1,276 | Trọng tâm phổ của các cặp khác nhãn xa hơn ở trung vị. Vì vậy, độ sáng phổ có khả năng đóng góp cho phân biệt nhãn trong tập này.                                                                    |
| Chroma STFT        | 1,272 / 1,394 | Hai khoảng cách khá sát nhau. Chroma ở phép đo này phân biệt nhãn nhạc cụ yếu hơn; vai trò chính là bổ sung thông tin về các lớp cao độ đang xuất hiện.                                              |

Nói ngắn gọn về cột “Nhận xét”: đây là câu tóm tắt **đặc trưng mô tả điều gì** và **hai số trong dòng gợi ý điều gì**. Cột này không khẳng định độ chính xác phân loại.

### 8.4. Kết quả khi ghép theo ba bộ

Trên toàn bộ các chiều của từng bộ, các trung vị cùng nhãn / khác nhãn trong báo cáo là:

| Bộ | Cùng nhãn | Khác nhãn | Cách đọc                                                                                                      |
| --- | ----------: | ----------: | ---------------------------------------------------------------------------------------------------------------- |
| A   |       0,870 |       1,346 | Khoảng cách cặp khác nhãn cao hơn khá rõ so với cặp cùng nhãn.                                       |
| B   |       0,786 |       1,272 | Bộ năng lượng và dạng sóng cũng cho chênh lệch trung vị rõ trên tập khảo sát.                    |
| C   |       1,245 |       1,402 | Chênh lệch nhỏ hơn A và B; trong bộ C, thông tin cao độ có thể làm các nhãn giao nhau nhiều hơn. |

Các số này được tính trực tiếp trên tất cả các chiều của từng bộ. Không thể lấy trung bình các ô MFCC, Roll-off... trong Bảng 4.3 để thay cho phép tính của cả bộ, vì khoảng cách của một vector ghép được tính đồng thời trên các chiều của vector đó.

## 9. Bảng 4.4: Fisher F và Mutual Information (MI)

Bảng 4.4 xem xét **từng chiều riêng lẻ** để tìm chiều nào có quan hệ với nhãn nhạc cụ trong tập dữ liệu.

### Fisher F

Fisher F so sánh mức khác nhau giữa trung bình các nhãn với mức dao động bên trong từng nhãn:

- F lớn: trung bình của chiều đó ở các nhãn khác nhau rõ so với độ dao động trong từng nhãn.
- F nhỏ: khác biệt giữa các trung bình nhãn không nổi bật so với độ dao động trong nhãn.

Ví dụ, mfcc_1_mean có F = 385,08. Có thể hiểu là giá trị trung bình của chiều này khác nhau đáng kể giữa các nhãn so với mức biến động bên trong mỗi nhãn theo phép đo ANOVA. **385,08 không phải 385,08% và cũng không phải độ chính xác.**

### Mutual Information

MI đo mức độ biết giá trị của một chiều giúp giảm sự không chắc chắn về nhãn đến đâu:

- MI lớn hơn thường cho thấy chiều đó mang nhiều thông tin hơn về nhãn theo phép đo này.
- MI = 0,813 nat không phải 81,3% và cũng không phải xác suất nhận diện đúng.
- “Nat” là đơn vị của MI khi dùng logarit tự nhiên.

Trong công thức của báo cáo, ký hiệu đã được ghi rõ là:

    MI(X;Y) = I(X;Y) = E[ln(p(X,Y) / (p(X)p(Y)))]

Ở đây, X là giá trị của một chiều đặc trưng, Y là nhãn nhạc cụ, còn I(X;Y) là ký hiệu toán học thường dùng cho Mutual Information. Vì vậy, cột MI trong Bảng 4.4 chính là giá trị của đại lượng được ký hiệu trong công thức trên.

Ví dụ, centroid_mean có MI = 0,813 nat trong bảng. Điều này cho thấy giá trị centroid_mean có quan hệ thông tin với nhãn trong phân tích đang làm; nó không chứng minh centroid là nguyên nhân làm nên loại nhạc cụ.

Bảng 4.4 liệt kê hợp các chiều xếp hạng cao theo hai phép đo. Có 11 dòng vì danh sách 10 chiều theo Fisher và 10 chiều theo MI có một số chiều trùng nhau. F và MI có thang đo khác nhau, nên không so sánh trực tiếp số F với số MI.

## 10. Bảng 4.5: đo chất lượng danh sách truy vấn

Bảng 4.5 trả lời câu hỏi trực tiếp hơn Bảng 4.3: khi tìm các tệp gần một tệp truy vấn, những kết quả đầu có cùng nhạc cụ với truy vấn không?

- Mỗi trong 600 tệp lần lượt làm truy vấn. Tệp đang truy vấn bị loại khỏi danh sách so sánh; 599 tệp còn lại được xếp hạng theo khoảng cách.
- Trước khi tính khoảng cách, các chiều được chuẩn hóa Z-score theo 599 tệp trong gallery.
- Một kết quả được chấm là **liên quan/đúng theo tiêu chí phép thử** nếu nhãn nhạc cụ trùng với nhãn của truy vấn. Ví dụ truy vấn Violin thì tệp Violin được tính là liên quan; tệp Cello hoặc Guitar thì không.
- Nhãn không được dùng để tính khoảng cách hoặc xếp hạng. Nhãn chỉ được dùng sau đó để chấm danh sách kết quả.

### Precision@5 và Precision@10

Precision@5 là tỷ lệ tệp cùng nhãn trong 5 kết quả đầu. Nếu truy vấn là Violin và 4/5 tệp đầu cũng mang nhãn Violin, Precision@5 của truy vấn đó bằng 4/5 = 80%. Precision@10 tính tương tự trên 10 tệp đầu. Các giá trị trong Bảng 4.5 là trung bình trên cả 600 truy vấn; vì thế Precision@5 = 93,50% có nghĩa là trung bình khoảng 4,675 trong 5 kết quả đầu cùng nhãn với truy vấn, chứ không có nghĩa mọi truy vấn đều đạt 93,50%.

### MAP@5

AP@5 chấm thứ tự của 5 kết quả đầu: một tệp cùng nhãn xuất hiện ở vị trí càng sớm thì càng có lợi cho điểm. MAP@5 là AP@5 trung bình của 600 truy vấn. Do mỗi nhạc cụ có 100 tệp và tệp truy vấn đã bị loại khỏi gallery, mỗi truy vấn còn 99 tệp cùng nhãn; vì vậy công thức AP@5 chia cho 5. **MAP@5 cũng là điểm truy hồi, không phải tỷ lệ phân loại đúng trên dữ liệu mới.**

### Kết quả cần rút ra

| Cấu hình                             | Số chiều | Precision@5 | Precision@10 |  MAP@5 |
| -------------------------------------- | ---------: | ----------: | -----------: | -----: |
| Bộ A – âm sắc và phổ             |         28 |      93,50% |       91,33% | 92,46% |
| Bộ B – năng lượng và dạng sóng |          4 |      59,43% |       56,47% | 52,45% |
| Bộ C – độ sáng phổ và cao độ  |         26 |      65,00% |       58,93% | 58,84% |
| Toàn bộ vector                       |         58 |      88,47% |       83,77% | 86,09% |

Trong phép thử này, **Bộ A đạt kết quả cao nhất**: MAP@5 là 92,46%. Vector 58 chiều đạt 86,09%, thấp hơn Bộ A 6,37 điểm phần trăm. Vì vậy, với cách chuẩn hóa và khoảng cách đang dùng, ghép đủ ba bộ chưa cải thiện việc tìm tệp cùng nhạc cụ so với chỉ dùng Bộ A. Đây là kết quả trên 600 tệp hiện có; chưa thể khẳng định kết quả sẽ giống vậy trên các bản ghi mới. Khi dùng RMSD trực tiếp trên vector 58 chiều, mỗi chiều có trọng số bằng nhau; do Bộ A và C có nhiều chiều hơn Bộ B nên tổng ảnh hưởng của ba bộ không ngang nhau.

## 11. Mục 4.10 và Bảng 4.6: tương quan giữa các chiều

Bảng 4.6 trả lời một câu hỏi khác với Fisher F/MI: **hai chiều đặc trưng có cùng biến thiên hay không?** Fisher F và MI so một chiều với nhãn nhạc cụ; Pearson so hai chiều đặc trưng với nhau.

Hệ số Pearson r nằm từ −1 đến 1:

- r dương, gần 1: hai chiều thường tăng hoặc giảm cùng nhau.
- r âm, gần −1: khi một chiều tăng thì chiều kia thường giảm.
- r gần 0: không thấy quan hệ tuyến tính rõ trong các dữ liệu đang xét.

Bảng được tính trên 58 chiều của 600 tệp, tạo ra 1.653 cặp khác nhau. Để bảng gọn và tập trung vào cặp nổi bật, báo cáo chỉ liệt kê 6 cặp có |r| > 0,8:

| Cặp chiều                   | Pearson r | Cách hiểu                                                                    |
| ----------------------------- | --------: | ------------------------------------------------------------------------------ |
| centroid_mean – rolloff_mean |     0,980 | Hai số đo phổ tăng giảm gần như cùng nhau trong tập này.             |
| centroid_std – rolloff_std   |     0,945 | Độ biến thiên của hai số đo phổ cũng có quan hệ cùng chiều mạnh. |
| zcr_mean – centroid_mean     |     0,911 | ZCR trung bình và độ sáng phổ thường cùng biến thiên.               |
| zcr_mean – rolloff_mean      |     0,829 | ZCR trung bình và phạm vi phổ thường cùng biến thiên.                 |
| mfcc_11_std – mfcc_12_std    |     0,822 | Độ biến thiên của hai hệ số MFCC có liên hệ cùng chiều.            |
| mfcc_0_mean – mfcc_2_mean    |   −0,811 | Hai chiều thường biến thiên ngược chiều nhau.                          |

Ví dụ, **r = 0,980 không có nghĩa là độ chính xác 98%**. Nó cho biết centroid_mean và rolloff_mean có quan hệ tuyến tính dương rất mạnh trong 600 tệp đang xét. Hai chiều đó có thể chứa một phần thông tin chồng lấn, nhưng chưa thể kết luận một chiều là thừa hoặc nên xóa.

Các hệ số tính gộp trên cả sáu nhãn nhạc cụ nên khác biệt giữa các nhạc cụ cũng có thể góp phần làm tương quan cao. Bảng này là bước rà soát ban đầu về khả năng trùng lặp; để biết bỏ một chiều có làm tìm kiếm tốt hơn hay không, cần bỏ thử chiều đó rồi so sánh lại Precision@5/MAP@5.

## 12. “Giá trị thông tin” trong báo cáo nên được hiểu thế nào?

Chương 4 có ba mức bằng chứng khác nhau:

1. **Bảng 4.3 – khoảng cách cặp:** xem khoảng cách giữa các cặp cùng nhãn và khác nhãn có xu hướng khác nhau không. Đây mới là xu hướng tổng quát, chưa cho biết Top-5 sẽ có bao nhiêu kết quả cùng nhạc cụ.
2. **Bảng 4.4 – Fisher F và MI:** xem từng chiều đặc trưng có liên hệ với nhãn như thế nào; không phải độ chính xác truy vấn.
3. **Bảng 4.5 – Precision@k và MAP@5:** kiểm tra trực tiếp danh sách được xếp hạng có đưa tệp cùng nhãn lên đầu hay không. Đây là phép đánh giá truy vấn leave-one-out trên chính 600 tệp, không phải kiểm thử độc lập trên bản thu mới.
4. **Bảng 4.6 – Pearson:** tìm các cặp chiều biến thiên cùng nhau mạnh để nhận biết khả năng chồng lấn thông tin; hệ số tương quan cao tự nó chưa đủ để loại chiều.

Vì vậy, có thể nói các đặc trưng cho kết quả hữu ích **trong phép thử đang báo cáo**. Không nên từ đó kết luận hệ thống sẽ đạt cùng mức trên mọi tệp âm thanh hoặc trên dữ liệu thu thập khác.

## 13. Hai hình trong Chương 4

- **Hình 4.1 – cấu trúc phân tầng**: cho thấy vector 58 chiều chia thành ba bộ A, B, C; mỗi bộ lại gồm hai loại đặc trưng. Hình này giải đáp trực quan vì sao báo cáo nói 3 bộ nhưng có 6 loại.
- **Hình 4.2 – quy trình trích xuất và so sánh**: minh họa thứ tự từ tệp WAV, chia khung, tính đặc trưng, gộp Mean/Std, tạo vector, chuẩn hóa rồi tính khoảng cách để tìm các tệp gần nhau.

## 14. Tóm tắt nhanh

- Có **6 loại đặc trưng**; chúng được gom thành **3 bộ tổng hợp** để trình bày.
- Mean và Std tóm tắt chuỗi theo thời gian thành số chiều cố định.
- Số chiều: Bộ A 28, Bộ B 4, Bộ C 26; tổng cộng **58**.
- “Cùng nhạc cụ” và “Khác nhạc cụ” được xác định theo nhãn của các tệp dùng trong phân tích.
- Bảng 4.3 dùng RMSD, một dạng khoảng cách Euclid đã chuẩn hóa theo số chiều; các ô là trung vị của nhiều cặp tệp.
- Bảng 4.4 dùng Fisher F và MI để xem từng chiều liên hệ với nhãn ra sao; Bảng 4.5 đo chất lượng truy vấn; Bảng 4.6 rà soát tương quan giữa các chiều.
- Các kết quả mô tả xu hướng trên bộ dữ liệu đang có, không đảm bảo mọi tệp mới đều phân biệt được.
