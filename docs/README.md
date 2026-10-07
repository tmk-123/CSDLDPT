# docs/ — Bản đồ tài liệu

> Theo `CLAUDE.md`, `docs/` là **nguồn thiết kế chính**. Trước khi code một module: đọc tài liệu liên quan → xác định requirement → cập nhật design nếu cần → mới code.

**Trọng tâm hiện tại: PHẦN 1 và PHẦN 2.** Thư mục 06, 07 mới chỉ giữ chỗ.

| Thư mục | Trả lời câu hỏi | Bắt đầu từ |
|---|---|---|
| [00_PROJECT/](00_PROJECT/) | Đề bài là gì, phạm vi tới đâu, hiện đang ở đâu? | [PROJECT_OVERVIEW.md](00_PROJECT/PROJECT_OVERVIEW.md) |
| [01_THEORY/](01_THEORY/) | **Nó là gì?** Kiến thức chung, không chứa tham số của project | [01_AUDIO_FUNDAMENTALS.md](01_THEORY/01_AUDIO_FUNDAMENTALS.md) |
| [02_PLANS/](02_PLANS/) | **Phải làm gì, theo thứ tự nào?** | ⭐ [PART_1_PLAN.md](02_PLANS/PART_1_PLAN.md) |
| [03_WORKFLOWS/](03_WORKFLOWS/) | Dữ liệu chảy qua các bước ra sao? | [MASTER_WORKFLOW.md](03_WORKFLOWS/MASTER_WORKFLOW.md) |
| [04_PART_1/](04_PART_1/) | **Project dùng nó thế nào?** Từ dataset tới vector đặc trưng | [DATASET_INVENTORY.md](04_PART_1/01_DATASET/DATASET_INVENTORY.md) |
| [05_PART_2/](05_PART_2/) | **Project dùng nó thế nào?** CSDL, chỉ mục R-tree, tìm kiếm, truy vấn | [SCHEMA.md](05_PART_2/01_DATABASE/SCHEMA.md) |
| [06_SYSTEM/](06_SYSTEM/) | (để sau) Kiến trúc tổng, demo, cài đặt | — |
| [07_EVALUATION/](07_EVALUATION/) | (để sau) Đánh giá | — |
| [08_AI_CONTEXT/](08_AI_CONTEXT/) | Tóm tắt ngắn cho người hoặc AI mới vào project; nhật ký quyết định | [DESIGN_DECISIONS.md](08_AI_CONTEXT/DESIGN_DECISIONS.md) |
| [09_REFERENCE/](09_REFERENCE/) | Thuật ngữ, công thức, nguồn tham khảo | [GLOSSARY.md](09_REFERENCE/GLOSSARY.md) |
| [_archive/](_archive/) | Bộ docs cũ (00–17). **Chỉ để tham khảo**, nhiều chỗ đã lỗi thời | — |

## Quy tắc tránh trùng lặp
1. `01_THEORY` giải thích **khái niệm**. Không ghi tham số cụ thể như "2048", "32D", "20 prototype".
2. `04_PART_1` và `05_PART_2` ghi **quyết định và tham số của project**, rồi link ngược về THEORY.
3. **Lý do** của mỗi lựa chọn chỉ ghi ở một nơi: [08_AI_CONTEXT/DESIGN_DECISIONS.md](08_AI_CONTEXT/DESIGN_DECISIONS.md). Các file khác chỉ link tới đó.
4. Mỗi con số chỉ có **một nguồn**. Nếu thay đổi (ví dụ đổi PCA 8D → 6D), sửa ở file PART tương ứng và thêm một dòng vào DESIGN_DECISIONS.

## Bảo đảm nội dung `_archive/17_IMPLEMENTATION_ROADMAP.md` không bị mất
Toàn bộ nội dung của file đó đã được tách vào cấu trúc mới:

| §17 | Nơi mới |
|---|---|
| §0.1, §1 | 09_REFERENCE/GLOSSARY.md, 00_PROJECT/PROJECT_OVERVIEW.md |
| §2 | 00_PROJECT/AUDIT_REPORT.md |
| §3, §16 | 04_PART_1/01_DATASET/* |
| §4 | 04_PART_1/02_AUDIO_ANALYSIS/PREPROCESSING.md |
| §5 | 04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md |
| §6 | 04_PART_1/04_FEATURE_EXTRACTION/SEGMENTATION.md |
| §7, §8 | 04_PART_1/03_FEATURE_DESIGN/REFERENCE_PROTOTYPES.md, FILE_LEVEL_VECTOR.md |
| §9, §10 | 05_PART_2/02_INDEX/NORMALIZATION_PCA.md |
| §11, §12 | 05_PART_2/02_INDEX/RTREE_INDEX.md, 03_SEARCH/KNN_SEARCH.md |
| §13 | 05_PART_2/01_DATABASE/SCHEMA.md |
| §14 | 05_PART_2/04_QUERY/QUERY_PIPELINE.md |
| §15 | 07_EVALUATION/README.md |
| §17 | 00_PROJECT/PROJECT_SCOPE.md (bảng rủi ro) |
| §18, §19, A–D | 02_PLANS/*, 03_WORKFLOWS/MASTER_WORKFLOW.md |
