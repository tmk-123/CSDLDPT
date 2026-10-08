# IMPLEMENTATION — Hàm nào được gọi, ở đâu, với tham số gì

> **Vai trò của file này.** [MASTER_PLAN](../02_PLANS/MASTER_PLAN.md) nói project **làm gì và vì sao**. File này ghi **chính xác** từng lệnh gọi thư viện: **file nào** gọi, **hàm nào**, **tham số** gì, **ra cái gì**. Bản chất của các thuật toán: [01_THEORY](../01_THEORY/README.md). Luồng file vào/ra theo script: [DATA_FLOW](DATA_FLOW.md).
>
> **Trạng thái ghi trung thực:**
> - **✅ ĐÃ CHẠY**: code có thật, lệnh gọi dưới đây chép từ code.
> - **⬜ DỰ KIẾN**: chưa có code. Lệnh gọi là **kế hoạch** suy ra từ thiết kế đã chốt; khi viết code phải cập nhật lại mục này cho khớp.
>
> Viết tắt thư viện: `np` = numpy, `sf` = soundfile, `sosfiltfilt`/`butter` = `scipy.signal`.

---

## A. ✅ ĐÃ CHẠY

### A1. `scripts/p01_1_download_iowa.py` — Bước 1.1, tải Iowa arco
| Lệnh gọi | Tham số | Kết quả |
|---|---|---|
| `urllib.request.urlopen(url, timeout=60)` (trong hàm `fetch`, thử lại tối đa 3 lần) | trang `MISviolin.html`, `MISviola.html`, `MIScello.html`, `MISdoublebass.html` | HTML; lấy các link có chữ `.arco.` (`arco_links`) |
| `urllib.request.urlopen(Request(url, method="HEAD"), timeout=60)` (`remote_size`) | | dung lượng file trên máy chủ, để bỏ qua file đã tải đủ |
| ghi ra `<tên>.part` rồi đổi tên | | `raw/iowa_mis/<nhạc cụ>/*.aiff` |
| `hashlib.md5(data).hexdigest()` | | MD5 ghi vào `_download/manifest.csv` |
| tùy chọn dòng lệnh | `--dry-run` | chỉ liệt kê |

### A2. `scripts/p01_2_slice_iowa.py` — Bước 1.2, cắt file Iowa thành nốt đơn
Hằng số: `SR = 44100`, `SR_PITCH = 22050`, `HOP = 512`, `MAX_NOTE_SEC = 6.0`, `TOP_DB_TAIL = 40`, `PITCH_TOL = 0.6`, `ALGO_VERSION = 3`; `FMIN`/`FMAX` (Hz): guitar 70/1100, violin 180/4200, viola 120/2100, cello 60/1200, double bass 35/500.

| Hàm trong script | Lệnh gọi thư viện | Tham số | Kết quả |
|---|---|---|---|
| `slice_file` | `librosa.load(path, sr=SR, mono=True)` | 44 100 Hz, mono | `y` |
| `slice_file` | `librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP, lag=2, max_size=3)` | SuperFlux | đường độ mạnh khởi đầu nốt |
| `slice_file` | `librosa.onset.onset_detect(onset_envelope=env, sr=SR, hop_length=HOP, backtrack=True, units="samples")` | lùi về đầu nốt | vị trí onset (mẫu) |
| `slice_file` | `librosa.resample(y, orig_sr=SR, target_sr=SR_PITCH)` | 44 100 → 22 050 | tín hiệu để đo cao độ |
| `candidate_pitches` | `librosa.pyin(seg, fmin=FMIN[…], fmax=FMAX[…], sr=SR_PITCH, frame_length=2048, hop_length=256)` | đoạn 0.1–0.6 s sau mỗi onset | F0, cờ có cao độ |
| `candidate_pitches` | `np.median(librosa.hz_to_midi(f0))` | cần ≥ 3 frame có cao độ | cao độ ứng viên (MIDI, số thực) |
| `slice_file` | ghép tuần tự với dãy nốt trong tên file | lệch ≤ 0.6 nửa cung sau bù độ lệch lên dây; chấp nhận lệch đúng 12/24 nửa cung; nhảy cóc ≤ 2 nốt | danh sách nốt khớp |
| `slice_file` | `librosa.effects.trim(seg, top_db=TOP_DB_TAIL)` | cắt đuôi lặng −40 dB | đoạn nốt |
| `slice_file` | `sf.write(dest, seg, SR, subtype="PCM_16")` | WAV 44 100 Hz 16-bit | `data/interim/iowa_notes/<nhạc cụ>/*.wav` |
| `parse_name` | đọc `sulX` / `sul_E` | guitar: `sulE` → `lowE`, `sul_E` → `highE` (D28) | nhãn dây |
| `main` | cache JSON theo `ALGO_VERSION` | `--fresh` để cắt lại | `notes.csv`, `slice_report.csv` |

### A3. `scripts/p01_3_build_catalog.py` — Bước 1.3–1.5, catalog, lọc, chia tập
Hằng số: `SR = 22050`, `HOP = 512`, `ACTIVE_DB = −40`, `MIN_ACTIVE_SEC = 0.35`, `SEED = 42`, `CAPS = {REF: 150, DB_POOL: 200, QUERY_POOL: 60}`.

| Hàm | Lệnh gọi | Tham số | Kết quả |
|---|---|---|---|
| `collect` | đọc tên file Philharmonia (`split("_", 4)`) và `notes.csv` của Iowa | | danh sách bản ghi + nhãn |
| `measure` | `subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "22050", "-f", "f32le", "-"])` | mono, 22 050 Hz, float32 | dãy mẫu, hoặc thông báo lỗi (→ CORRUPT) |
| `measure` | `hashlib.md5(path.read_bytes()).hexdigest()` | | MD5 (→ DUPLICATE) |
| `measure` | `butter(4, 25, btype="highpass", fs=22050, output="sos")` + `sosfiltfilt(HP_SOS, y)` | lọc thông cao 25 Hz, không lệch pha (D27) | tín hiệu đã bỏ tiếng ù |
| `measure` | RMS theo khung 512 mẫu, ngưỡng −40 dB so với đỉnh | | `active_sec`, `peak`, `clipped` (đo trên tín hiệu gốc) |
| `assign_status_and_split` | quy tắc | CORRUPT → DUPLICATE → TOO_SHORT (< 0.35 s) → OK; `midi % 5` | `status`, `split`, `reason` |
| `select_within_caps` | `random.Random(42)`, xoay vòng theo (nguồn, MIDI, cường độ) | `CAPS` | cột `selected` |
| `organize` | `shutil.copy2` | | `data/notes/`, `data/queries/`, `data/excluded/` |
| `main` | `csv.DictWriter` | | `data/catalog.csv` |

### A4. `scripts/p01_6_dataset_stats.py` — Bước 1.6, thống kê
Đọc `data/catalog.csv`, `slice_report.csv`; dùng `matplotlib` (backend `Agg`). Ra `reports/dataset/dataset_stats.md`, 8 file CSV, `notes_by_instrument.png`, `pitch_coverage.png`.

### A5. `scripts/theory_figures.py` — số đo và hình cho `docs/01_THEORY` (script minh họa, **không** phải pipeline)
| Hàm | Lệnh gọi chính | Tham số | Kết quả |
|---|---|---|---|
| `load_note` | `librosa.load(sr=22050, mono=True)` → `sosfiltfilt` 25 Hz → chuẩn hóa đỉnh 0.95 → `librosa.effects.trim(top_db=40)` | giữ 1.5 s đầu | tín hiệu nốt |
| `note_features` | `librosa.stft(y, n_fft=2048, hop_length=512, window="hann")` | | phổ biên độ `S` |
| `note_features` | `librosa.feature.rms(S=S, frame_length=2048)`; frame có âm: > −40 dB | | RMS-CV |
| `note_features` | `librosa.feature.zero_crossing_rate(y, frame_length=2048, hop_length=512)` | | ZCR |
| `note_features` | `librosa.feature.spectral_centroid / spectral_bandwidth / spectral_rolloff(roll_percent=0.85) / spectral_flatness(S=S)` | | đặc trưng phổ |
| `note_features` | `librosa.feature.melspectrogram(S=S**2, sr=22050, n_mels=128)` → `librosa.power_to_db` → `librosa.feature.mfcc(n_mfcc=14)`, bỏ c0 | | MFCC c1–c13 mean và std |
| `measure_all` | `ProcessPoolExecutor(6)` | `--redo` để đo lại | `reports/theory/note_features.csv` |
| `feature_information`, `pca_demo`, `source_transfer`, `plucked_queries` | `numpy` (η², SVD, láng giềng gần nhất), `scipy.stats.spearmanr` | | các CSV trong `reports/theory/` |
| các hàm `fig_*` | `matplotlib` | | 16 hình `reports/theory/*.png` |

F0 trong `theory_figures.py` lấy **theo tên nốt**, không gọi pYIN (trừ hình vibrato và phổ harmonic).

---

## B. ⬜ DỰ KIẾN (chưa có code)

Tham số lấy từ thiết kế đã chốt; mọi tham số sẽ đặt ở `src/strings_mmdb/config.py` (Bước 0), không ghi số cứng trong code.

### B1. Bước 2 — `audio_io.py`
| Hàm dự kiến | Lệnh gọi dự kiến | Tham số đã chốt | Kết quả |
|---|---|---|---|
| `load_audio(path, trim=False)` | giải mã (ffmpeg hoặc `librosa.load`) → trung bình kênh | mono, `sr=22050` | dãy mẫu |
| | `butter(4, 25, btype="highpass", fs=22050, output="sos")` + `sosfiltfilt` | 25 Hz (D27) | |
| | `y = 0.95 * y / max(abs(y))` | đỉnh 0.95 | |
| | `librosa.effects.trim(y, top_db=40)` (chỉ khi `trim=True`) | −40 dB | `y` float32 |

### B2. Bước 3 — `features.py`
| Hàm dự kiến | Lệnh gọi dự kiến | Tham số đã chốt |
|---|---|---|
| `frame_features(y)` (tính một lần cho cả file) | `librosa.stft(y, n_fft=2048, hop_length=512, window="hann")` | |
| | `librosa.feature.melspectrogram(S=…, n_mels=128)` → `power_to_db` → `librosa.feature.mfcc(n_mfcc=14)` | bỏ c0 |
| | `librosa.feature.spectral_centroid`, `spectral_bandwidth`, `spectral_rolloff(roll_percent=0.85)` | |
| | `librosa.feature.zero_crossing_rate(frame_length=2048, hop_length=512)`, `librosa.feature.rms` | |
| | `librosa.pyin(y, fmin=40, fmax=4200, sr=22050)` | fmin đang chờ xem lại (P08) |
| `segment_features(y, start, end, ff)` | cắt các frame của đoạn; chỉ frame > −40 dB; mean/std/median như [FEATURE_SET](../04_PART_1/03_FEATURE_DESIGN/FEATURE_SET.md) §3 | → `s` (32 số) |

### B3. Bước 4 — `prototypes.py`
| Lệnh gọi dự kiến | Tham số | Kết quả |
|---|---|---|
| `StandardScaler().fit(S_ref)` | 750 nốt REF | `scaler_seg` (`mean_`, `scale_`) |
| `KMeans(n_clusters=4, n_init=20, random_state=42).fit(Z_c)` cho từng nhạc cụ c | k = 4 | 4 tâm mỗi nhạc cụ → 20 prototype |
| `τ = median(min_j ‖z − P_j‖²)` (numpy) | trên REF | `tau` |
| lưu `np.savez` | | `data/models/v1/scaler_seg.npz`, `prototypes.npz`, `ref_index.npz` |

### B4. Bước 5 — `synth.py`
`random.Random(seed)`; `load_audio(trim=True)`; cắt L ∈ [0.35, 1.2] s (gảy ≤ 1.5 s); fade-out 20 ms; gain ∈ [−6, 0] dB; 50% lặng 0–150 ms / 50% chồng 10–40 ms; `sf.write(..., 22050, subtype="PCM_16")`; `json.dump` đáp án. Kết quả: `data/sequences/db/` (500), `data/sequences/query/` (100).

### B5. Bước 6 — `segmentation.py`
| Lệnh gọi dự kiến | Tham số |
|---|---|
| RMS theo frame, ngưỡng −40 dB; nối vùng cách < 50 ms, bỏ vùng < 120 ms | |
| `librosa.onset.onset_strength(y=y, sr=22050, hop_length=512, lag=2, max_size=3, n_mels=128)` | SuperFlux |
| `librosa.onset.onset_detect(onset_envelope=…, backtrack=True, pre_max/post_max ≈ ±3 frame, pre_avg/post_avg ≈ ±10 frame, delta ≈ 0.1, wait ≈ 100 ms)` | δ chọn ở Bước 6 (P03) |
| hậu xử lý: gộp < 120 ms, chặt > 2 s thành ≤ 1 s, bỏ < −35 dB | |

### B6. Bước 7 — `representation.py`
`audio_to_vector(path, models)`: `load_audio` → `segment` → `frame_features` → `segment_features` → `Z = (S − mean)/std` → `D2 = ‖Z_i − P_j‖²` → `W = softmax(−D2/τ)` (trừ min trước khi `exp`) → `α = dur/Σdur` → `h = α @ W`, `μ = α @ Z` → `v = concat(h, μ)` (52 số).

### B7. Bước 8 — `db.py`
`sqlite3.connect("mmdb.sqlite")`; DDL như [SCHEMA](../05_PART_2/01_DATABASE/SCHEMA.md); vector: `v.astype("<f4").tobytes()` ↔ `np.frombuffer(blob, dtype="<f4")`.

### B8. Bước 9 — `reduction.py`
| Lệnh gọi dự kiến | Tham số | Kết quả |
|---|---|---|
| `StandardScaler().fit(V_db)` | 500 vector CSDL | `scaler_file` |
| chia khối: `x[:20] / sqrt(20)`, `x[20:] / sqrt(32)` | | `v'` |
| `PCA(n_components=8, whiten=False).fit(V'_db)` | 8D | `pca.npz`; `u = pca.transform(v')` |

### B9. Bước 10 — `index_rtree.py`, `search.py`
| Lệnh gọi dự kiến | Tham số |
|---|---|
| `p = rtree.index.Property(); p.dimension = 8; p.variant = rtree.index.RT_Star; p.leaf_capacity = 10; p.index_capacity = 10` | M = 10 |
| `idx = rtree.index.Index("data/index/rtree_v1", properties=p)`; `idx.insert(audio_id, (*u, *u))` | điểm = hộp suy biến |
| `idx.nearest((*u_q, *u_q), k')` | k' = 20, gấp đôi tới khi D(thứ 5) ≤ r8 |
| `np.linalg.norm(V'_cand − v'_q, axis=1)` | khoảng cách thật 52D; Top-5 |

### B10. Bước 11 — `scripts/p11_query.py`
Kiểm tra file (`ffprobe`, 0.3–60 s) → `audio_to_vector` → `transform` → `search` → in kết quả trung gian ([INTERMEDIATE_RESULTS](../05_PART_2/04_QUERY/INTERMEDIATE_RESULTS.md)).
