# Phương pháp đánh giá giá trị thông tin của các đặc trưng

## Mục tiêu và dữ liệu

Phân tích dùng 600 tệp WAV thuộc sáu nhãn nhạc cụ, mỗi nhãn có 100 tệp. Mục tiêu là kiểm tra hai điều: các vector có đặt tệp cùng nhãn gần nhau hơn không; và khi truy vấn, các tệp cùng nhãn có xuất hiện gần đầu danh sách không.

Nhãn được dùng để chia cặp, tính Fisher/MI hoặc chấm kết quả sau khi xếp hạng. Nhãn không tham gia vào phép tính vector và khoảng cách. Dữ liệu hiện không có nhãn kỹ thuật chơi, vì vậy không thể kết luận về khả năng tìm tệp cùng kỹ thuật diễn tấu.

## 1. Ý nghĩa âm học – đánh giá định tính

- **MFCC:** tóm tắt hình dạng phổ log-Mel, thường dùng để mô tả màu âm. Hệ số MFCC không đo trực tiếp loại gỗ, kích thước đàn hay từng formant.
- **Spectral Centroid và Spectral Roll-off:** tóm tắt vị trí và phạm vi năng lượng trong phổ, gợi ý độ sáng và độ trải phổ của bản ghi.
- **RMS:** tóm tắt mức năng lượng hiệu dụng và độ biến thiên giữa các khung; chịu ảnh hưởng của âm lượng thu và cường độ diễn tấu.
- **Zero-Crossing Rate:** tóm tắt mức đổi dấu của dạng sóng; không thể tự nó kết luận tiếng bị méo hay do một kỹ thuật chơi.
- **Chroma:** tóm tắt phân bố năng lượng theo 12 lớp cao độ; hữu ích cho nội dung nốt nhưng phụ thuộc nốt đang chơi.

Phần này giải thích lý do các đặc trưng có thể bổ sung cho nhau. Đây là căn cứ định tính, không phải kết quả độ chính xác hay bằng chứng quan hệ nhân quả với cấu tạo nhạc cụ.

## 2. Khoảng cách cùng nhãn và khác nhãn

Chuẩn hóa mỗi chiều bằng Z-score. Với hai tệp `a`, `b` trên `k` chiều:

`RMSD(a,b) = sqrt[ sum((z(a,j) - z(b,j))^2, j=1..k) / k ]`

RMSD là khoảng cách Euclid chia cho căn bậc hai số chiều. Tính khoảng cách cho từng cặp không lặp, sau đó lấy trung vị riêng cho cặp cùng nhãn và khác nhãn. Có `6 × C(100,2) = 29.700` cặp cùng nhãn và `C(6,2) × 100 × 100 = 150.000` cặp khác nhãn.

Tỷ số được tính là `trung vị khác nhãn / trung vị cùng nhãn`. Tỷ số trên 1 có nghĩa trung vị khác nhãn lớn hơn trung vị cùng nhãn; nó không chứng minh mọi cặp khác nhãn đều xa hơn mọi cặp cùng nhãn.

### Kết quả theo sáu loại đặc trưng

| Đặc trưng | Bộ | Số chiều | Cùng nhãn | Khác nhãn | Tỷ số khác/cùng |
|---|---:|---:|---:|---:|---:|
| MFCC | A | 26 | 0,886 | 1,325 | 1,50 |
| Spectral Roll-off | A | 2 | 0,458 | 1,277 | 2,79 |
| RMS Energy | B | 2 | 0,859 | 1,250 | 1,46 |
| Zero-Crossing Rate | B | 2 | 0,432 | 0,926 | 2,14 |
| Spectral Centroid | C | 2 | 0,494 | 1,276 | 2,58 |
| Chroma STFT | C | 24 | 1,272 | 1,394 | 1,10 |

Roll-off có tỷ số lớn nhất (2,79), tiếp theo là Centroid (2,58); Chroma thấp nhất (1,10). Đây là so sánh giữa các trung vị trên tập này, không phải độ chính xác truy vấn.

### Kết quả theo ba bộ tổng hợp

| Bộ | Số chiều | Cùng nhãn | Khác nhãn | Tỷ số khác/cùng |
|---|---:|---:|---:|---:|
| A – Âm sắc và phổ | 28 | 0,870 | 1,346 | 1,55 |
| B – Năng lượng và dạng sóng | 4 | 0,786 | 1,272 | 1,62 |
| C – Độ sáng phổ và lớp cao độ | 26 | 1,245 | 1,402 | 1,13 |

Bộ B có tỷ số trung vị cao nhất nhưng không đứng đầu trong kiểm tra truy vấn. Điều này cho thấy trung vị khoảng cách không thay thế được phép thử xếp hạng. Trên vector 58 chiều, trung vị Euclid là 8,235 với cặp cùng nhãn và 10,650 với cặp khác nhãn; đây là Euclid không chia cho căn bậc hai số chiều, nên không so trực tiếp với các giá trị RMSD.

## 3. Fisher F và Mutual Information

Hai phép đo xét từng chiều với nhãn nhạc cụ.

- `F = MS_between / MS_within`. F cao cho biết trung bình của chiều đó khác nhau giữa các nhãn tương đối nhiều so với độ biến thiên bên trong nhãn. F không phải xác suất hay độ chính xác; nếu không báo cáo p-value thì không kết luận ý nghĩa thống kê chỉ từ F.
- `I(X;Y) = H(Y) - H(Y|X)`. MI đo mức liên hệ thông tin giữa giá trị một chiều `X` và nhãn `Y`. Ước lượng trong bảng dùng đơn vị nat, `n_neighbors=3`, `random_state=42`; MI không phải tỷ lệ dự đoán đúng.

Bảng là hợp của 10 chiều đầu theo từng phép đo, có 11 chiều riêng biệt vì một số chiều trùng nhau.

| Chiều đặc trưng | Bộ | Fisher F | MI (nat) |
|---|---:|---:|---:|
| mfcc_1_mean | A | 385,08 | 0,760 |
| mfcc_2_mean | A | 359,42 | 0,607 |
| mfcc_4_mean | A | 321,67 | 0,737 |
| centroid_mean | C | 307,48 | 0,813 |
| rolloff_mean | A | 295,42 | 0,803 |
| rolloff_std | A | 224,98 | 0,632 |
| mfcc_0_mean | A | 210,60 | 0,482 |
| zcr_mean | B | 201,35 | 0,699 |
| mfcc_3_mean | A | 174,96 | 0,592 |
| centroid_std | C | 143,96 | 0,525 |
| mfcc_10_mean | A | 97,40 | 0,512 |

`mfcc_1_mean` có F cao nhất trong danh sách; `centroid_mean` có MI cao nhất. Không gán ý nghĩa vật lý trực tiếp như formant hoặc bộ phận đàn cho từng chỉ số MFCC.

## 4. Precision@k và MAP@5 cho truy vấn

Đây là phép đánh giá gần nhất với mục tiêu CBAR. Mỗi tệp lần lượt làm truy vấn; tệp đó được bỏ khỏi gallery còn 599 tệp. Với từng truy vấn, Z-score được ước lượng trên 599 tệp gallery rồi áp dụng cho cả gallery và query. Các chiều trong cấu hình được nối thành vector và xếp hạng bằng RMSD. Kết quả được tính là liên quan nếu nhãn nhạc cụ trùng với truy vấn.

- `Precision@k = số tệp cùng nhãn trong Top-k / k`.
- `AP@5(q) = sum(Precision@k(q) × rel_q(k), k=1..5) / 5`.
- `MAP@5 = trung bình AP@5 trên 600 truy vấn`.

Mỗi truy vấn có 99 tệp cùng nhãn còn lại trong gallery, nên mẫu số AP@5 là 5. Các số dưới đây là trung bình trên 600 truy vấn.

| Cấu hình | Số chiều | Precision@1 | Precision@5 | Precision@10 | MAP@5 |
|---|---:|---:|---:|---:|---:|
| A | 28 | 96,83% | 93,50% | 91,33% | 92,46% |
| B | 4 | 65,67% | 59,43% | 56,47% | 52,45% |
| C | 26 | 77,00% | 65,00% | 58,93% | 58,84% |
| A+B | 32 | 97,00% | 92,90% | 90,88% | 91,86% |
| A+C | 54 | 93,67% | 87,23% | 83,05% | 84,96% |
| B+C | 30 | 82,00% | 70,43% | 65,33% | 65,13% |
| A+B+C | 58 | 93,00% | 88,47% | 83,77% | 86,09% |

Bộ A đạt MAP@5 cao nhất (92,46%) và Precision@5 cao nhất (93,50%). A+B tăng Precision@1 nhẹ từ 96,83% lên 97,00%, nhưng giảm Precision@5 xuống 92,90% và MAP@5 xuống 91,86%. Các cấu hình A+C, B+C và A+B+C cũng không vượt Bộ A theo MAP@5. Theo cách nối các chiều và chuẩn hóa đang dùng, các tổ hợp chưa cải thiện tìm kiếm Top 5 trên bộ 600 tệp. Đây là leave-one-out trên các tệp hiện có; “liên quan” được xác định theo cùng nhãn nhạc cụ.

## 5. Tương quan Pearson và khả năng chồng lấn

Tính Pearson giữa mọi cặp trong 58 chiều, tổng cộng `C(58,2)=1.653` cặp. Bảng liệt kê các cặp có `|r| > 0,8`. Pearson cho biết hai chiều biến thiên cùng nhau đến đâu; nó không đo trực tiếp khả năng phân biệt nhãn.

| Chiều thứ nhất | Chiều thứ hai | Pearson r |
|---|---|---:|
| centroid_mean | rolloff_mean | 0,980 |
| centroid_std | rolloff_std | 0,945 |
| zcr_mean | centroid_mean | 0,911 |
| zcr_mean | rolloff_mean | 0,829 |
| mfcc_11_std | mfcc_12_std | 0,822 |
| mfcc_0_mean | mfcc_2_mean | −0,811 |

Cặp mạnh nhất là `centroid_mean` với `rolloff_mean`. Tương quan cao chỉ gợi ý có thể chồng lấn một phần; muốn quyết định bỏ chiều cần bỏ thử và đo lại MAP@5/Precision@5.

## Kết luận

Các phép đo cho kết quả bổ sung nhau: khoảng cách cặp mô tả xu hướng gom/tách theo nhãn; Fisher F và MI xếp hạng từng chiều; Precision@k/MAP@5 kiểm tra chất lượng danh sách truy vấn; Pearson rà soát khả năng chồng lấn. Trên dữ liệu hiện tại, Roll-off và Centroid tạo chênh lệch khoảng cách rõ nhất trong sáu loại đặc trưng, `centroid_mean` có MI cao nhất và Bộ A đạt truy vấn tốt nhất. Các kết luận chỉ áp dụng cho bộ 600 tệp và tiêu chí liên quan cùng nhãn đang dùng.
