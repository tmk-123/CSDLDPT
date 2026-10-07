# DATASET ROLES — File nào dùng để làm gì

## 1. Năm vai trò

| Vai trò | Nguồn | Số lượng (dự kiến) | Dùng để | Vào R-tree? |
|---|---|---|---|---|
| **REF** (reference single-note) | Nốt đơn của 5 nhạc cụ thuộc nhóm cao độ REF | ~1 360 | Fit `scaler_seg`, học 20 prototype | Không |
| **DB sequences** | Ghép từ nốt **DB_POOL** | **500** (100/nhạc cụ) | **Là CSDL được tìm kiếm** | **Có** |
| **QUERY sequences** | Ghép từ nốt **QUERY_POOL** | 100 (20/nhạc cụ) | Truy vấn kiểm thử chính thức | Không |
| **PHRASE** | 446 file `phrase` thật (violin, viola, cello, double-bass) | 446 | Truy vấn "nhạc thật" | Không |
| **UNSEEN** | Banjo 74 + mandolin 80 | 154 | Truy vấn "nhạc cụ ngoài CSDL" (đề mục 4). Không dùng để học hay ghép CSDL, nên chỉ cần vài chục file | Không |

## 2. Tại sao cần single-note (REF)
- Nhãn **chắc chắn** (nhạc cụ, cao độ, kỹ thuật), mỗi file **đúng một sự kiện âm thanh**, nên là mẫu "sạch" nhất để học "âm sắc của từng nhạc cụ trông thế nào trong không gian đặc trưng".
- Đơn vị của REF là "một nốt", và segmentation biến multi-note thành các đơn vị "xấp xỉ một nốt". **Hai phía cùng đơn vị nên so sánh được.**

## 3. Tại sao cần multi-note
- Là đối tượng thực tế được lưu và tìm kiếm: âm nhạc thường là chuỗi nốt, không phải từng nốt rời.
- Cho phép xây file đủ dài (3–8 s) chứa nhiều âm vực của cùng một nhạc cụ, đúng yêu cầu "đủ dài để nhận diện".

## 4. Tại sao 500 multi-note phải **ghép**
Dataset **không có** 500 file multi-note của 5 nhạc cụ: guitar có 0 phrase; phrase violin phần lớn chỉ dài khoảng 1 s; phrase không có nhãn nốt. Đề cho phép "xây dựng/sưu tầm". Ghép từ nốt thu âm thật có hai lợi ích: **ground truth ranh giới nốt** (để đo segmentation) và **cân bằng 100 file/nhạc cụ**. Hạn chế (chuyển nốt không tự nhiên) được đo bằng tập PHRASE.

## 5. Một file nốt đơn cũng là "file hợp lệ"
Pipeline xem nốt đơn là file có n = 1 segment. Vì vậy người dùng có thể truy vấn bằng một nốt, và phương án dự phòng (CSDL = nốt đơn) dùng chung toàn bộ code.
