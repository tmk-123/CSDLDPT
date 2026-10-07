# PART 2 WORKFLOW

## 1. Luồng build (offline)
```
[p08_load_db]        catalog, sequences, ground truth, vectors, models ─► data/mmdb.sqlite
[p09_fit_reduction]  V (500 DB) ─► scaler_file.npz, pca.npz ─► file_vector.v_norm, u_pca (mọi file)
[p10_build_index]    u của 500 DB ─► data/index/rtree_v1.{dat,idx}
```

## 2. Luồng truy vấn (online)
```
query.wav
 │ validate + audio_to_vector          (Phần 1)
 ▼
v (52D)
 │ scaler_file.transform, chia khối
 ▼
v' (52D) ───────────────────────────────┐
 │ pca.transform                         │
 ▼                                       │
u (8D)                                   │
 │ rtree.nearest(u, k')                  │
 ▼                                       ▼
C = {k' audio_id}  ──── đọc v_norm ───► D(x) = ‖v' − v'_x‖ (52D)
                                         │ d₅ ≤ r8 ?  không → k' ← 2k', quay lại
                                         ▼ có
                                   Top-5 → JOIN metadata → in kết quả + trung gian
```

## 3. Đồng bộ phiên bản
`model_version` (v1) phải giống nhau ở: `data/models/v1/`, `file_vector.model_version`, `rtree_v1`. Khi đổi tham số thì tạo v2 và build lại Bước 7 → 10.
