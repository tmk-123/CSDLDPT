# PROJECT CONTEXT (đọc đầu tiên khi mới vào project)

**Tóm tắt 10 dòng** (dùng để trình bày với giảng viên):
1. Hệ CBAR: CSDL **500 file multi-note** của 5 nhạc cụ dây (violin, viola, cello, double bass, guitar); trả về Top-5 file có tiếng nhạc cụ gần nhất với file truy vấn.
2. Dữ liệu gốc là thư viện **nốt đơn** thu âm thật (4 477 file). 500 file multi-note được **ghép** từ nốt đơn, kèm ranh giới nốt làm ground truth.
3. Nốt đơn được chia **theo cao độ** thành REF / DB_POOL / QUERY_POOL không giao nhau, nên không rò rỉ dữ liệu.
4. Mỗi nốt REF thành vector âm sắc 32D; K-means lấy **4 prototype/nhạc cụ, tổng 20**.
5. File multi-note được **segmentation** (energy + SuperFlux, chống vibrato) thành các đoạn xấp xỉ nốt.
6. Mỗi segment thành 32D, so với 20 prototype, ra phân bố mềm (softmax khoảng cách).
7. Gộp có trọng số thời lượng: **histogram 20D ‖ trung bình 32D = vector 52D cố định** cho mọi file.
8. Z-score, rồi **PCA 8D**; 500 điểm 8D được đánh chỉ mục bằng **R\*-tree**.
9. Query đi qua **cùng hàm**; R-tree lọc ứng viên (khoảng cách 8D là cận dưới), refine Euclid 52D, cho **Top-5 chính xác tuyệt đối**.
10. Đánh giá: P@5, Top-1, MRR (relevant = cùng nhạc cụ) trên query giữ riêng, phrase thật và banjo/mandolin (nhạc cụ ngoài CSDL).

**Trạng thái:** xem [CURRENT_STATUS](../00_PROJECT/CURRENT_STATUS.md). **Việc tiếp theo:** xem [TODO](TODO.md).

**Quy tắc làm việc:**
- Đọc docs của bước trước khi code (`CLAUDE.md`).
- Chỉ đánh ✅ khi đã có code chạy được và đã kiểm tra.
- Mọi thay đổi thiết kế phải ghi vào [DESIGN_DECISIONS](DESIGN_DECISIONS.md).
- `Strings/` chỉ đọc.
