# DATABASE SCHEMA — SQLite

> Lý thuyết: [08_MULTIMEDIA_DATABASE](../../01_THEORY/08_MULTIMEDIA_DATABASE.md). Quyết định: D18.

## 1. Chọn công nghệ
| Lựa chọn | Ưu | Nhược | Kết luận |
|---|---|---|---|
| **SQLite + vector BLOB float32 + R-tree file (`rtree`)** | Không cần server, một file, dễ demo; BLOB gọn (52·4 = 208 byte); R-tree đủ 8D, có `nearest` | Index nằm ngoài DBMS, phải đồng bộ bằng `model_version` | **CHỌN** |
| SQLite R\*Tree module | Index nằm trong DBMS | Tối đa 5 chiều; chỉ có range query | Dự phòng (PCA = 5D) |
| PostgreSQL + cube + GiST | GiST là R-tree-like, có k-NN `<->` | Cần cài server | Nâng cao |
| PostgreSQL + pgvector | Tiện | Index là HNSW/IVFFlat, **không phải R-tree** ⇒ mất phần R-tree của môn | **Không** |
| Vector dạng JSON | Dễ đọc | Chậm, tốn chỗ, mất độ chính xác | Chỉ dùng khi export |

**Nguyên lý lưu trữ hỗn hợp:** file audio nằm trên đĩa (`Strings/`, `data/sequences/`); CSDL lưu **đường dẫn + metadata + vector**.

## 2. DDL
```sql
PRAGMA foreign_keys = ON;

CREATE TABLE instrument (
  instrument_id INTEGER PRIMARY KEY,
  name          TEXT UNIQUE NOT NULL,          -- violin, viola, cello, double-bass, guitar, banjo, mandolin
  excitation    TEXT NOT NULL CHECK (excitation IN ('bowed','plucked')),
  in_database   INTEGER NOT NULL               -- 1: có trong CSDL tìm kiếm; 0: unseen
);

CREATE TABLE source_note (                     -- bản ghi GỐC trong Strings/ (= catalog.csv)
  recording_id     INTEGER PRIMARY KEY,
  rel_path         TEXT UNIQUE NOT NULL,
  instrument_id    INTEGER NOT NULL REFERENCES instrument,
  note TEXT, midi INTEGER, duration_label TEXT, dynamics TEXT,
  technique TEXT, technique_family TEXT,
  duration_sec REAL, sample_rate INTEGER, channels INTEGER, md5 TEXT,
  status TEXT NOT NULL,                        -- OK|CORRUPT|DUPLICATE|TOO_SHORT
  split  TEXT NOT NULL                         -- REF|DB_POOL|QUERY_POOL|PHRASE|UNSEEN|NONE
);

CREATE TABLE audio_file (                      -- ĐỐI TƯỢNG được tìm kiếm/truy vấn: 1 file = 1 record
  audio_id         INTEGER PRIMARY KEY,
  rel_path         TEXT UNIQUE NOT NULL,
  kind             TEXT NOT NULL,              -- db_sequence|query_sequence|phrase|unseen|user_query
  instrument_id    INTEGER REFERENCES instrument,
  technique_family TEXT,
  duration_sec REAL, sample_rate INTEGER,
  n_notes_true     INTEGER,                    -- chỉ có với sequence ghép
  n_segments       INTEGER,
  in_index         INTEGER NOT NULL DEFAULT 0  -- 1 = nằm trong R-tree
);

CREATE TABLE sequence_note (                   -- ground truth
  audio_id INTEGER REFERENCES audio_file, position INTEGER,
  recording_id INTEGER REFERENCES source_note,
  start_sec REAL, end_sec REAL,
  PRIMARY KEY (audio_id, position)
);

CREATE TABLE segment (                         -- kết quả segmentation (minh họa)
  audio_id INTEGER REFERENCES audio_file, idx INTEGER,
  start_sec REAL, end_sec REAL, f0_hz REAL,
  feat BLOB,                                   -- 32 × float32
  top_proto_id INTEGER REFERENCES prototype, top_proto_w REAL,
  nearest_ref_id INTEGER REFERENCES source_note, nearest_ref_dist REAL,
  PRIMARY KEY (audio_id, idx)
);

CREATE TABLE prototype (
  proto_id INTEGER PRIMARY KEY,                -- 1..20
  instrument_id INTEGER REFERENCES instrument,
  k_index INTEGER, centroid BLOB,              -- 32 × float32 (không gian z)
  n_members INTEGER, model_version TEXT REFERENCES model
);

CREATE TABLE file_vector (
  audio_id INTEGER PRIMARY KEY REFERENCES audio_file,
  v_raw    BLOB NOT NULL,                      -- 52 × float32, output Phần 1 (h ‖ μ)
  v_norm   BLOB NOT NULL,                      -- 52 × float32, sau scaler_file + chia khối  → khoảng cách thật
  u_pca    BLOB NOT NULL,                      -- 8 × float32  → điểm trong R-tree
  model_version TEXT NOT NULL REFERENCES model
);

CREATE TABLE model (
  model_version TEXT PRIMARY KEY,              -- 'v1'
  params TEXT,                                 -- JSON
  artifacts_dir TEXT,                          -- data/models/v1/
  created_at TEXT
);
```

## 3. Quan hệ
```
instrument 1─n source_note        instrument 1─n audio_file      instrument 1─n prototype
audio_file 1─n segment            audio_file 1─1 file_vector
audio_file(db/query_sequence) 1─n sequence_note n─1 source_note
```
- **Không có bảng frame.** Frame không phải record.
- Pitch và technique là **thuộc tính** của `source_note`. Không tách bảng riêng vì chúng không có thuộc tính đi kèm cần chuẩn hóa.
- R-tree: file `data/index/rtree_v1.{dat,idx}`, khóa = `audio_id`. Chỉ những `audio_file` có `in_index = 1` (500 sequence DB).

## 4. Truy vấn mẫu (dùng để kiểm tra ở Bước 8)
```sql
-- 1. Số file trong index theo nhạc cụ (kỳ vọng mỗi nhạc cụ 100)
SELECT i.name, COUNT(*) FROM audio_file a JOIN instrument i USING(instrument_id)
WHERE a.in_index = 1 GROUP BY i.name;

-- 2. Các sequence cello có ≥ 6 nốt
SELECT rel_path, n_notes_true FROM audio_file a JOIN instrument i USING(instrument_id)
WHERE i.name = 'cello' AND a.kind = 'db_sequence' AND n_notes_true >= 6;

-- 3. Kiểm tra rò rỉ: bản ghi nốt dùng ở cả DB và query (kỳ vọng 0 dòng)
SELECT sn.recording_id FROM sequence_note sn JOIN audio_file a USING(audio_id)
GROUP BY sn.recording_id HAVING COUNT(DISTINCT a.kind) > 1;
```

## 5. BLOB ↔ numpy
```python
blob = v.astype('<f4').tobytes()        # ghi
v    = np.frombuffer(blob, dtype='<f4') # đọc
```
