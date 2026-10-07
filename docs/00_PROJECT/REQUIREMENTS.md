# REQUIREMENTS — Ánh xạ đề bài → thiết kế → trạng thái

Trạng thái: ⬜ chưa làm · 📝 đã thiết kế (chưa code) · ✅ xong và đã kiểm tra.

| ID | Yêu cầu (đề bài) | Phần | Đáp ứng bằng | Tài liệu | Trạng thái |
|---|---|---|---|---|---|
| R1.1 | ≥ 500 file âm thanh nhạc cụ dây | P1 | 500 sequence DB ghép từ nốt đơn thật (tổng hệ thống > 600 file) | [SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md) | 📝 |
| R1.2 | Mỗi file chỉ một nhạc cụ | P1 | Quy tắc ghép: mỗi sequence một nhạc cụ | như trên | 📝 |
| R1.3 | Độ dài đủ nhận diện | P1 | Sequence dài 3–8 s, 4–8 nốt | như trên | 📝 |
| R1.4 | Mô tả giống và khác giữa các nhạc cụ | P1 | Lý thuyết + **số liệu đo thật** (f0, centroid… theo nhạc cụ) | [INSTRUMENT_CHARACTERISTICS](../04_PART_1/02_AUDIO_ANALYSIS/INSTRUMENT_CHARACTERISTICS.md) | 📝 |
| R2.1 | Bộ đặc trưng tìm tương đồng và khác biệt | P1 | 32D/segment, 52D/file | [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md) | 📝 |
| R2.2 | Giá trị thông tin của từng đặc trưng | P1 | Bảng "đo gì, phân biệt gì" + đo thực nghiệm (tương quan, khả năng tách lớp) | như trên | 📝 |
| R3.1 | Triển khai trích rút đặc trưng | P1 | `features.py`, `segmentation.py`, `representation.py` | [EXTRACTION_PIPELINE](../04_PART_1/04_FEATURE_EXTRACTION/EXTRACTION_PIPELINE.md) | 📝 |
| R3.2 | Hệ CSDL quản trị đặc trưng | P2 | SQLite, 8 bảng, vector dạng BLOB | [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md) | 📝 |
| R4.1 | Input: file mới (nhạc cụ đã có hoặc chưa có) | P2 | Query pipeline; banjo/mandolin làm "chưa có" | [QUERY_PIPELINE](../05_PART_2/04_QUERY/QUERY_PIPELINE.md) | 📝 |
| R4.2 | Output: Top-5 giảm dần độ tương đồng | P2 | R-tree + multi-step exact k-NN | [KNN_SEARCH](../05_PART_2/03_SEARCH/KNN_SEARCH.md) | 📝 |
| R4a | Sơ đồ khối, vào/ra từng khối | P1+P2 | Workflow docs | [MASTER_WORKFLOW](../03_WORKFLOWS/MASTER_WORKFLOW.md) | 📝 |
| R4b | Kết quả trung gian | P2 | Segment, W, h, u 8D, ứng viên, bảng khoảng cách | [INTERMEDIATE_RESULTS](../05_PART_2/04_QUERY/INTERMEDIATE_RESULTS.md) | 📝 |
| R4c | Đánh giá | sau | P@5, Top-1, MRR… | [07_EVALUATION](../07_EVALUATION/README.md) | ⬜ |
| R5 | Demo | sau | Streamlit | [06_SYSTEM](../06_SYSTEM/README.md) | ⬜ |

## Yêu cầu ngầm của môn học (không ghi trong đề nhưng phải có)
| ID | Yêu cầu | Đáp ứng |
|---|---|---|
| C1 | Có **chỉ mục không gian** (R-tree) | [RTREE_INDEX](../05_PART_2/02_INDEX/RTREE_INDEX.md), bắt buộc, không phải "nâng cao" |
| C2 | Không coi frame là record | 1 file = 1 record; frame chỉ tồn tại trong RAM |
| C3 | Query xử lý bằng **cùng pipeline** với DB | Một hàm duy nhất `audio_to_vector()` |
