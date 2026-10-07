# MASTER WORKFLOW

## 1. Sơ đồ toàn hệ thống
```mermaid
flowchart TB
    subgraph P1["PHẦN 1 - Dataset tới vector 52D"]
        A["Strings/ 4477 mp3"] --> B["Catalog: parse tên, ffprobe, MD5, status"]
        B --> C{"Split theo cao độ mod 5"}
        C -->|REF| D["Nốt đơn REF"]
        C -->|DB_POOL| E["Ghép 500 sequence DB"]
        C -->|QUERY_POOL| F["Ghép 100 sequence query"]
        B -->|phrase| G["446 phrase thật"]
        B -->|banjo, mandolin| H["154 unseen"]
        D --> D1["Feature 32D"]
        D1 --> D2["scaler_seg + K-means: 20 prototype, tau"]
        E --> AV["audio_to_vector: segmentation, feature 32D, soft matching, h 20D + mu 32D"]
        F --> AV
        D2 -.-> AV
        AV --> V["v 52D cho mọi file"]
    end
    subgraph P2["PHẦN 2 - CSDL, chỉ mục, tìm kiếm"]
        V --> N["scaler_file + chia khối: v' 52D"]
        N --> PCA["PCA 8D: u"]
        PCA --> RT[("R*-tree 8D, 500 điểm")]
        N --> DB[("SQLite")]
        PCA --> DB
        Q["query.wav"] --> QA["audio_to_vector"]
        QA --> QN["transform: v' và u"]
        QN --> S1["R-tree nearest k' ứng viên"]
        S1 --> S2["Refine Euclid 52D"]
        S2 --> S3{"d5 <= r8 ?"}
        S3 -->|không, k' x 2| S1
        S3 -->|có| TOP["Top-5 + kết quả trung gian"]
        RT -.-> S1
        DB -.-> S2
    end
```

## 2. Khối chức năng và vào/ra (đề mục 4a)

| Khối | Chức năng | Vào | Ra | Phần |
|---|---|---|---|---|
| Catalog | Kiểm kê, lọc lỗi, chia tập | `Strings/*.mp3` | `catalog.csv` | 1 |
| Synthesizer | Ghép multi-note | Nốt DB_POOL/QUERY_POOL | WAV + ground truth JSON | 1 |
| Preprocessor | Chuẩn hóa tín hiệu | File audio | y | 1 |
| Feature extractor | Đặc trưng segment | y, (start, end) | s 32D | 1 |
| Reference builder | Học prototype | s của REF | 20 prototype, τ | 1 |
| Segmenter | Tách nốt | y | Danh sách segment | 1 |
| Vectorizer | Gộp thành vector file | Segment, prototype | v 52D | 1 |
| Normalizer + PCA | Chuẩn hóa, giảm chiều | v | v' 52D, u 8D | 2 |
| Database | Lưu metadata + vector | Tất cả ở trên | `mmdb.sqlite` | 2 |
| Spatial index | R\*-tree | u của 500 DB | `rtree_v1` | 2 |
| Search engine | k-NN chính xác | v'_q, u_q | Top-5 | 2 |
| Query interface | CLI | File query | Top-5 + kết quả trung gian | 2 |

Chi tiết: [PART_1_WORKFLOW](PART_1_WORKFLOW.md), [PART_2_WORKFLOW](PART_2_WORKFLOW.md), [DATA_FLOW](DATA_FLOW.md).
