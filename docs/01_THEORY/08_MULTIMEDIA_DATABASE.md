# 08. MULTIMEDIA DATABASE

## 1. CBAR / Query-by-Example
Hệ **tìm kiếm âm thanh theo nội dung** (Content-Based Audio Retrieval): người dùng đưa một **mẫu** (file audio), hệ thống trả về các đối tượng có **đặc trưng nội dung** gần nhất, không dựa vào từ khóa (Lecture 10).

Quy trình chuẩn:
```
Offline: đối tượng → trích đặc trưng → vector → lưu + đánh chỉ mục
Online : query → CÙNG phép trích đặc trưng → vector → tìm k-NN qua chỉ mục → xếp hạng
```

## 2. Lưu trữ hỗn hợp (Hybrid storage)
- **Dữ liệu lớn** (file audio, BLOB media) nằm trên hệ thống file hoặc object store.
- **CSDL** lưu metadata, đường dẫn và vector đặc trưng (Lecture 4).
- Lợi ích: CSDL nhỏ, truy vấn nhanh, file media phục vụ trực tiếp.

## 3. Metadata (Lecture 9)
| Loại | Ví dụ trong bài |
|---|---|
| Kỹ thuật | Sample rate, kênh, thời lượng, định dạng |
| Mô tả | Nhạc cụ, cao độ, cường độ, kỹ thuật chơi |
| Cấu trúc | Danh sách segment, sequence gồm những nốt nào |
| Quản trị | Nguồn, MD5, trạng thái, phiên bản model |

## 4. Lưu vector
| Cách | Ưu | Nhược |
|---|---|---|
| BLOB nhị phân | Gọn, nhanh, chính xác | Không đọc được bằng mắt |
| JSON/TEXT | Dễ đọc | Chậm, tốn chỗ |
| Kiểu mảng (PostgreSQL `real[]`) | Truy vấn được từng phần tử | Cần PostgreSQL |
| Vector extension (pgvector) | Có index ANN | Index là HNSW/IVF, không phải R-tree |
| Cột tọa độ + spatial index (SQLite R\*Tree, PostGIS, cube/GiST) | Index nằm trong DBMS | Giới hạn số chiều (SQLite ≤ 5) |

## 5. Mô hình dữ liệu
Quan hệ (relational) cho metadata; vector là thuộc tính của đối tượng; chỉ mục không gian là cấu trúc phụ trên vector (Lecture 5). **Một đối tượng media = một record**; các đơn vị phân tích nhỏ hơn (frame) không phải record.
