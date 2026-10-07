# SEQUENCE SYNTHESIS — Ghép file multi-note

## 1. Quy tắc ghép một sequence

| Tham số | Giá trị |
|---|---|
| Nhạc cụ | **Một** nhạc cụ duy nhất (đề yêu cầu) |
| Technique family | Một family/sequence. Bộ kéo vĩ: 80% `arco`, 20% `pizz`. Guitar: 70% `pluck`, 30% `harmonic` |
| Số nốt n | Ngẫu nhiên đều trong {4, …, 8} |
| Chọn nốt | Nốt tiếp theo cách nốt trước ±7 semitone (nếu có); ưu tiên bản ghi **ít được dùng** |
| Đoạn cắt mỗi nốt | Cắt lặng đầu, rồi lấy L ~ U(0.35, 1.2) s từ đầu (giữ phần attack). Âm gảy: tới 1.5 s. Guitar dùng lại: offset ngẫu nhiên |
| Fade-out | 20 ms (tránh tiếng "click") |
| Gain mỗi nốt | U(−6, 0) dB |
| Nối nốt | 50%: khoảng lặng U(0, 150) ms · 50%: crossfade chồng 10–40 ms (giả lập legato và vang) |
| Tổng thời lượng | Khoảng 3–8 s |
| Định dạng | WAV, 22 050 Hz, mono, PCM 16-bit (lossless) |
| Ngẫu nhiên | Seed cố định ⇒ tái lập được |

Số lượng: **100 DB + 20 query cho mỗi nhạc cụ** ⇒ 500 DB + 100 query.

## 2. Tên file
```
data/sequences/db/seq_<instrument>_<0001..0100>.wav
data/sequences/query/q_<instrument>_<0001..0020>.wav
```

## 3. Ground truth (JSON, một file cho mỗi sequence)
```json
{
  "file": "seq_cello_0007.wav",
  "instrument": "cello",
  "technique_family": "arco",
  "sr": 22050,
  "duration_sec": 5.84,
  "notes": [
    {"position": 0, "recording_id": 1532, "source": "cello/cello_D3_1_forte_arco-normal.mp3",
     "note": "D3", "midi": 50, "start_sec": 0.000, "end_sec": 0.912, "gain_db": -2.1},
    {"position": 1, "recording_id": 1607, "note": "F3", "midi": 53, "start_sec": 0.880, "end_sec": 1.640, "gain_db": -0.4}
  ]
}
```
`start_sec` của nốt sau có thể nhỏ hơn `end_sec` của nốt trước (crossfade). **Onset đúng** là `start_sec` của mỗi nốt.

## 4. Pseudocode
```
for instrument in INSTRUMENTS:
  for kind, pool, count in [(db, DB_POOL, 100), (query, QUERY_POOL, 20)]:
    usage = {rec: 0 for rec in pool(instrument)}
    for k in 1..count:
      fam   = chọn family theo tỷ lệ
      n     = randint(4, 8)
      notes = chọn n bản ghi thuộc fam, ưu tiên usage nhỏ, bước cao độ ≤ 7
      y, t  = [], 0
      for rec in notes:
        x = load_audio(rec, trim=True)[offset : offset + L]·gain, fade-out 20 ms
        nếu random < 0.5: chèn lặng g, t += g
        nếu không:        chồng x lên cuối y (crossfade c), t -= c
        ghi (rec, start=t, end=t+len(x)); t += len(x); usage[rec] += 1
      peak-normalize y, ghi WAV + JSON
```

## 5. Phải nêu trong báo cáo
500 file DB được **xây dựng** bằng cách ghép nốt đơn thu âm thật, nhằm có ground truth và cân bằng giữa các nhạc cụ. Hạn chế là thiếu chuyển nốt tự nhiên (legato thật, portamento); tập PHRASE dùng để đo hạn chế này.
