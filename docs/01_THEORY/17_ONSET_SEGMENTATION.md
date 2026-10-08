# 17. Tách nốt — onset và segmentation

> **Đọc xong file này bạn sẽ biết:** vì sao phải chia một file nhiều nốt thành từng đoạn; onset là gì; ba cách tìm onset (năng lượng, spectral flux, SuperFlux) và vì sao vibrato của nhạc cụ kéo vĩ làm cách đơn giản thất bại; cách chọn đỉnh; thuật toán của project; bài học thật khi cắt nốt bộ Iowa; đánh giá kết quả tách nốt.
> **Cần biết trước:** [13](13_WAVEFORM.md) (RMS, đường bao), [14](14_FFT_STFT_SPECTRUM.md) (spectrogram, Mel).
> **Đọc tiếp:** [18 Vector đặc trưng](18_FEATURE_VECTOR.md).

---

## 1. Vì sao phải tách nốt

CSDL của project chứa các file **nhiều nốt** (sequence 4–8 nốt, đoạn phrase). Nhưng "thư viện tham chiếu" để biết mỗi nhạc cụ trông thế nào lại là các **nốt đơn** (tập REF, [16](16_DATASET_MODEL.md) §3). Muốn so được hai thứ đó, phải chia file nhiều nốt thành các **đoạn (segment) xấp xỉ một nốt**.

```
File nhiều nốt:  |──── D3 ────|── F3 ──|──────── A3 ────────|── C4 ──|
                 ↓ tìm các điểm bắt đầu nốt (onset)
Segment:         [   seg 1   ][ seg 2 ][      seg 3        ][ seg 4 ]
                 ↓ mỗi segment → 32 đặc trưng ([15])
```
**Mục tiêu không phải là phiên âm chính xác** (biết đúng từng nốt). Chỉ cần mỗi đoạn **chủ yếu chứa một nốt**. Vector của file ([18](18_FEATURE_VECTOR.md)) được thiết kế để chịu được khi chia thừa hoặc gộp sót.

---

## 2. Các khái niệm

| Thuật ngữ | Là gì | Ví dụ |
|---|---|---|
| **Onset** | Thời điểm một nốt **bắt đầu** (đầu pha attack, [13](13_WAVEFORM.md) §4) | 0.72 s |
| **Offset** | Thời điểm nốt **kết thúc** | 1.38 s |
| **Segment** | Đoạn tín hiệu giữa hai mốc liên tiếp | [0.72, 1.41) |
| **IOI** (*inter-onset interval*) | Khoảng cách giữa hai onset liên tiếp | 0.69 s |
| **ODF** (*onset detection function*) | Một đường theo thời gian, có **đỉnh** tại các onset | Đường flux ở §4 |

**Khung chung của mọi cách tìm onset:**
```
tín hiệu → ODF (đường "độ mạnh khởi đầu nốt") → chọn đỉnh (peak picking) → danh sách onset
```

---

## 3. Cách 1 — dựa vào năng lượng

**Ý tưởng.** Nốt mới bắt đầu thì âm **to lên đột ngột**. ODF = mức tăng của RMS ([13](13_WAVEFORM.md) §5) giữa hai frame liên tiếp.

**Tốt khi:** giữa các nốt có **khoảng lặng**, hoặc nốt gảy (bật lên rất nhanh).

**Thất bại khi:**
- **Legato** (nối liền): nốt sau bắt đầu khi nốt trước chưa tắt, năng lượng gần như không đổi.
- **Kéo vĩ**: người chơi tự điều chỉnh độ to trong lúc giữ nốt, tạo ra các "đỉnh năng lượng" không phải nốt mới.
- **Guitar**: nốt trước còn ngân, nốt sau gảy cùng dây làm nốt trước tắt đột ngột.

**Bài học thật của project.** Lần đầu cắt bộ guitar Iowa (353 nốt dự kiến) bằng ngưỡng năng lượng, thuật toán tìm ra **743 đoạn**, tức là cứ mỗi nốt bị chia thành khoảng 2 mảnh. Năng lượng đơn thuần **không đủ**.

---

## 4. Cách 2 — spectral flux: nhìn vào phổ

**Ý tưởng.** Nốt mới làm **xuất hiện các harmonic mới** (vạch mới trên spectrogram, [14](14_FFT_STFT_SPECTRUM.md) §4), kể cả khi độ to không đổi. ODF = tổng **mức tăng** của phổ giữa hai frame:
```
flux[t] = Σ_f  max( 0,  M[f, t] − M[f, t−1] )
```
| Thành phần | Ý nghĩa |
|---|---|
| `M[f, t]` | Phổ (log, thang Mel) ở dải tần f, frame t |
| `M[f, t] − M[f, t−1]` | Dải f mạnh lên hay yếu đi so với frame trước |
| `max(0, …)` | Chỉ đếm phần **mạnh lên** (nốt mới), bỏ phần yếu đi (nốt cũ tắt) |
| `Σ_f` | Cộng trên mọi dải tần |

**Thất bại với vibrato.** Vibrato làm các harmonic **trượt lên xuống** liên tục ([05](05_VIOLIN.md) §8.1). Khi một harmonic trượt sang dải bên cạnh, dải mới "mạnh lên" và flux dương, dù **không có nốt mới**. Thực tế, một nốt kéo vĩ có vibrato cho ra **3–5 onset giả**.

---

## 5. Cách 3 — SuperFlux: spectral flux "chịu được" vibrato

**Ý tưởng** (Böck & Widmer, 2013). Trước khi so với frame trước, **làm "phình" frame trước theo trục tần số**: mỗi dải lấy giá trị lớn nhất của chính nó và các dải kề bên. Nếu một harmonic chỉ trượt sang **dải bên cạnh** (vibrato), frame trước đã "phủ" sẵn dải đó, nên phép trừ không còn dương. Còn nốt mới thật sự thì harmonic xuất hiện ở chỗ **hoàn toàn mới**, nên vẫn dương.

**Công thức:**
```
SF[t] = Σ_f  max( 0,  M[f, t] − max_{f' ∈ {f−1, f, f+1}} M[f', t − μ] )
```
| Thành phần | Ý nghĩa |
|---|---|
| `max_{f'∈{f−1,f,f+1}} M[f', t−μ]` | Frame trước đã được "phình" sang dải kề (bộ lọc max theo tần số, cỡ 3) |
| `μ` | So với frame cách đó μ frame (project: μ = 2, khoảng 46 ms) để onset chậm của kéo vĩ vẫn kịp nổi lên |

**Ví dụ.** Harmonic h3 của nốt A4 vibrato dao động giữa dải Mel 41 và 42:
- **Flux thường:** frame t có năng lượng ở dải 42, frame t−1 ở dải 41 → dải 42 "mới mạnh lên" → **onset giả**.
- **SuperFlux:** frame t−2 sau khi phình đã có năng lượng ở cả 40, 41, 42 → dải 42 không mới → **không có onset**.
- **Nốt mới C5:** các harmonic nhảy sang dải 47, 52… cách xa → SuperFlux vẫn **dương lớn** → onset thật.

Trong thư viện librosa: `librosa.onset.onset_strength(..., lag=2, max_size=3)`.

---

## 6. Chọn đỉnh (peak picking) và lùi về đầu nốt

ODF có đỉnh lớn ở onset thật nhưng cũng có nhiều đỉnh nhỏ do nhiễu. Frame t được nhận là onset khi **cả ba điều kiện** đúng:
1. **Đỉnh cục bộ:** ODF[t] lớn nhất trong cửa sổ ±3 frame (±70 ms).
2. **Vượt ngưỡng thích nghi:** ODF[t] ≥ trung bình ODF trong ±10 frame + δ. "Thích nghi" nghĩa là ngưỡng **tự nâng lên** ở đoạn nhạc ồn ào và hạ xuống ở đoạn yên.
3. **Không quá sát onset trước:** cách onset trước ≥ 100 ms.

**Lùi về đầu nốt (backtrack).** Đỉnh ODF nằm ở giữa pha attack. Lùi onset về **điểm năng lượng thấp nhất ngay trước đỉnh** thì mốc cắt trùng với lúc nốt thật sự bắt đầu, và đoạn được giữ nguyên phần attack (phần chứa nhiều thông tin âm sắc).

---

## 7. Thuật toán của project

Chi tiết và tham số: [SEGMENTATION](../04_PART_1/04_FEATURE_EXTRACTION/SEGMENTATION.md). Tóm tắt:
```
1. Vùng có âm: RMS > −40 dB so với đỉnh; nối vùng cách nhau < 50 ms; bỏ vùng < 120 ms
2. SuperFlux trên log-Mel 128 dải (frame 2 048, hop 512, lag 2, max 3)
3. Chọn đỉnh như §6 (δ ≈ 0.1, chọn lại ở Bước 6), lùi về đầu nốt
4. Mốc cắt = đầu mỗi vùng có âm ∪ các onset trong vùng
5. Hậu xử lý: đoạn < 120 ms gộp vào đoạn trước; đoạn > 2 s chặt thành khúc ≤ 1 s;
   đoạn có RMS trung bình < −35 dB bỏ đi
```

---

## 8. Bài học thật: cắt 1 552 nốt của bộ Iowa

Mỗi file Iowa là **một dãy nốt** chơi lần lượt trên một dây (ví dụ `Guitar.mf.sulA.C3B3.aif` = C3, C♯3, … B3). Project phải cắt chúng thành nốt đơn ([`scripts/p01_2_slice_iowa.py`](../../scripts/p01_2_slice_iowa.py)). Ba phiên bản thuật toán:

| Phiên bản | Cách làm | Kết quả |
|---|---|---|
| 1 | Ngưỡng năng lượng | Guitar: **743 đoạn** cho 353 nốt (chia thừa khoảng 2 lần) |
| 2 | SuperFlux + pYIN đo cao độ mỗi đoạn + ghép tuần tự với dãy nốt dự kiến (lấy từ tên file); **mọi** cao độ đo được đều được "gập" về quãng tám gần nhất | Chỉ ghép đúng 76%: gập quãng tám làm nhận nhầm cả harmonic khác thành nốt |
| 3 | Như trên, nhưng chỉ chấp nhận sai **đúng 12 hoặc 24 nửa cung** (lỗi quãng tám của pYIN) và lệch tối đa **60 cent** sau khi bù độ lệch lên dây của cả file | **1 429 / 1 552 nốt (92%)** |

Theo nhạc cụ: double bass 279/286 (98%), guitar 341/353 (97%), cello 291/309 (94%), viola 267/292 (91%), violin 251/312 (80%). Violin thấp nhất vì có nhiều nốt rất cao trên dây E (tới B7, 3 951 Hz), nơi pYIN dễ đo sai.

**Bài học rút ra cho thiết kế:**
1. **Vibrato là kẻ thù số một** của tìm onset trên nhạc cụ kéo vĩ → phải dùng SuperFlux.
2. **pYIN hay sai đúng 1–2 quãng tám** ở nốt rất thấp (F0 yếu, [08](08_DOUBLE_BASS.md) §3) và nốt rất cao → không tin tuyệt đối vào F0 đo được. Đặc trưng F0 dùng **trung vị** trên các frame để giảm ảnh hưởng ([15](15_AUDIO_FEATURES.md)).
3. Một chút **độ lệch lên dây** của cả file (vài chục cent) là bình thường ([05](05_VIOLIN.md) §4); phải bù trước khi so cao độ.

---

## 9. Áp dụng cho 5 nhạc cụ

| Nhạc cụ | Đầu nốt trông thế nào | Khó khăn khi tách |
|---|---|---|
| Guitar | Bật rất nhanh, rõ (vạch dọc trên spectrogram) | Dễ nhất. Chỉ khó khi nốt trước còn ngân |
| Violin, viola | Mềm (vĩ "vào dây" từ từ), có vibrato | Onset giả do vibrato → cần SuperFlux; legato rất khó |
| Cello | Như trên, cộng nốt sói ([07](07_CELLO.md) §3) làm năng lượng dao động | Onset giả do dao động năng lượng |
| Double bass | Attack chậm, F0 yếu | Onset muộn; pYIN sai quãng tám |

---

## 10. Đánh giá kết quả tách nốt

Với sequence **ghép** ([SEQUENCE_SYNTHESIS](../04_PART_1/01_DATASET/SEQUENCE_SYNTHESIS.md)), project **biết chính xác** mỗi nốt bắt đầu lúc nào (cột `start_sec` trong file JSON đi kèm), nên đo được:
```
Một onset dự đoán là ĐÚNG nếu cách một onset thật ≤ 50 ms (mỗi onset thật chỉ khớp một lần)
Precision = số onset đúng / số onset dự đoán        (có bao nhiêu % onset tìm ra là thật)
Recall    = số onset đúng / số onset thật           (tìm ra được bao nhiêu % onset thật)
F         = 2 × P × R / (P + R)                      (mục tiêu F ≥ 0.80)
```
**Ví dụ.** Sequence có 6 nốt thật; thuật toán tìm ra 7 onset, trong đó 5 cái khớp: P = 5/7 = 0.71; R = 5/6 = 0.83; F = 0.77.

Ngưỡng δ được chọn trên sequence của CSDL, rồi kết quả cuối được báo cáo trên sequence truy vấn. Không chọn tham số trên chính tập dùng để báo cáo, để tránh "rò rỉ" ([16](16_DATASET_MODEL.md) §7).
