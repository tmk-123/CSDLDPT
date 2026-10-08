# PART 2 PLAN — CSDL, chỉ mục R-tree, tìm kiếm, truy vấn (Bước 8 → 11)

> **Đầu vào của Phần 2:** sản phẩm bàn giao của Phần 1 ([PART_1_OUTPUT_SPEC](../04_PART_1/05_OUTPUT/PART_1_OUTPUT_SPEC.md)).
> **Kết quả cuối:** lệnh `python scripts/p11_query.py <file>` in ra Top-5 kèm kết quả trung gian, và Top-5 đó **trùng 100% với brute force**.

```
Vector 52D (Phần 1) ─► 8 SQLite ─► 9 Chuẩn hóa + PCA 8D ─► 10 R-tree + k-NN chính xác ─► 11 Query CLI
```

---

## Bước 8 — CSDL SQLite
**Đọc trước:** [01_THEORY/22_MULTIMEDIA_DATABASE](../01_THEORY/22_MULTIMEDIA_DATABASE.md), [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md)

**Mục tiêu:** một file `data/mmdb.sqlite` chứa catalog, sequence, ground truth, segment, prototype và vector.

**Việc cần làm** (`src/strings_mmdb/db.py` + `scripts/p08_load_db.py`):
- [ ] Viết DDL đúng SCHEMA (8 bảng), bật `PRAGMA foreign_keys = ON`.
- [ ] Hàm tiện ích: `vec_to_blob(v) = v.astype('<f4').tobytes()`, `blob_to_vec(b) = np.frombuffer(b, '<f4')`.
- [ ] Nạp: `instrument` (7 dòng) → `source_note` (từ catalog) → `audio_file` (600 sequence; tùy chọn thêm phrase/unseen) → `sequence_note` → `segment` → `prototype` → `model`.
- [ ] Script phải **xóa và tạo lại** toàn bộ CSDL bằng một lệnh (idempotent).

**Kiểm tra:**
- [ ] Đếm số dòng: instrument = 7, source_note = 4 477, audio_file ≥ 600, prototype = 20.
- [ ] Đọc BLOB ra so với vector gốc: sai số = 0.
- [ ] Chạy thử 3 truy vấn SQL mẫu (xem SCHEMA §4).

**Xong khi:** CSDL tạo lại được bằng một lệnh và các truy vấn mẫu đúng.

---

## Bước 9 — Chuẩn hóa + PCA
**Đọc trước:** [01_THEORY/19_DISTANCE_SIMILARITY](../01_THEORY/19_DISTANCE_SIMILARITY.md), [01_THEORY/20_PCA](../01_THEORY/20_PCA.md), [NORMALIZATION_PCA](../05_PART_2/02_INDEX/NORMALIZATION_PCA.md)

**Mục tiêu:** v (52D) → v' (52D, đã chuẩn hóa) → u (8D) cho mọi file.

**Việc cần làm** (`src/strings_mmdb/reduction.py` + `scripts/p09_fit_reduction.py`):
- [ ] Fit `scaler_file` **chỉ trên 500 vector DB**.
- [ ] Cân bằng khối: chia 20 cột đầu cho √20, 32 cột sau cho √32.
- [ ] Fit `PCA(n_components=8, whiten=False)` **chỉ trên DB**.
- [ ] Hàm `transform(v) → (v', u)`, dùng chung cho DB và query.
- [ ] Ghi `file_vector.v_raw` (v), `file_vector.v_norm` (v') và `file_vector.u_pca` (u) cho mọi file; lưu `scaler_file.npz` và `pca.npz`.
- [ ] Ghi lại explained variance (từng thành phần và cộng dồn).

**Kiểm tra** (`tests/test_lower_bound.py`):
- [ ] Trên DB sau scaler: mean ≈ 0, std ≈ 1 ở từng cột.
- [ ] **Cận dưới:** 10 000 cặp ngẫu nhiên đều thỏa ‖u_a − u_b‖ ≤ ‖v'_a − v'_b‖ + 1e-6.
- [ ] Query chỉ gọi `transform`, không gọi `fit` (kiểm tra bằng code review).

**Xong khi:** vector đã ghi vào CSDL và test cận dưới qua.

---

## Bước 10 — R-tree + tìm k-NN chính xác
**Đọc trước:** [01_THEORY/21_R_TREE](../01_THEORY/21_R_TREE.md), [RTREE_INDEX](../05_PART_2/02_INDEX/RTREE_INDEX.md), [KNN_SEARCH](../05_PART_2/03_SEARCH/KNN_SEARCH.md)

**Mục tiêu:** R\*-tree 8D trên 500 điểm DB + hàm `search(v'_q, u_q, k=5)` cho kết quả chính xác.

**Việc cần làm** (`src/strings_mmdb/index_rtree.py`, `src/strings_mmdb/search.py`, `scripts/p10_build_index.py`):
- [ ] `index.Property(dimension=8, leaf_capacity=10, index_capacity=10, variant=RT_Star)`; lưu ra file `data/index/rtree_v1`.
- [ ] Chèn 500 điểm (hộp suy biến: min = max = u), id = `audio_id`.
- [ ] `brute_force(v'_q, k)`: quét toàn bộ 500 vector (dùng để đối chiếu).
- [ ] `search(v'_q, u_q, k)`: thuật toán multi-step (k' = 20, gấp đôi cho tới khi d₅ ≤ r8). Trả về Top-5, số ứng viên, số vòng lặp.

**Kiểm tra** (`tests/test_search_exact.py`):
- [ ] Index chứa đúng 500 entry; mở lại từ file được.
- [ ] Với 100 sequence query: Top-5 của `search` **== Top-5 của `brute_force`** (cùng id, cùng thứ tự) ở 100% query.
- [ ] Ghi số ứng viên trung bình / 500 và thời gian trung bình.

**Xong khi:** test chính xác qua 100%.

---

## Bước 11 — Truy vấn (CLI)
**Đọc trước:** [QUERY_PIPELINE](../05_PART_2/04_QUERY/QUERY_PIPELINE.md), [INTERMEDIATE_RESULTS](../05_PART_2/04_QUERY/INTERMEDIATE_RESULTS.md)

**Mục tiêu:** `python scripts/p11_query.py path/to/file.wav` in ra kết quả trung gian và Top-5.

**Việc cần làm** (`scripts/p11_query.py`, dùng `representation.audio_to_vector` + `reduction.transform` + `search.search`):
- [ ] Validate (đọc được, 0.3–60 s, không lặng).
- [ ] In: danh sách segment, bảng đặc trưng rút gọn, h gộp theo nhạc cụ (%), u (8D), số ứng viên, Top-5 (hạng, file, nhạc cụ, d, similarity).
- [ ] Tùy chọn `--save-figs`: lưu waveform + segment, heatmap W, biểu đồ h.

**Kiểm tra:**
- [ ] Query bằng chính một file DB: hạng 1 là chính nó, d ≈ 0.
- [ ] Query một nốt đơn guitar (QUERY_POOL): chạy được (n = 1).
- [ ] Query file stereo 44.1 kHz: chạy được.
- [ ] Query một file banjo: chạy được, in ra phân bố nhạc cụ của Top-5.
- [ ] File lặng: báo lỗi rõ ràng, không crash.

**Xong khi:** 5 kiểm tra trên qua. **PHẦN 2 HOÀN THÀNH.**
