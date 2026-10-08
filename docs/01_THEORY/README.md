# 01_THEORY — Lý thuyết từ cơ bản đến nâng cao

> **Viết cho ai:** người **chưa học** âm nhạc, chưa học xử lý tín hiệu, chưa biết các nhạc cụ dây.
> **Mục tiêu:** không chỉ biết định nghĩa, mà **hiểu bản chất** của âm thanh, âm nhạc và cách nhạc cụ tạo ra âm thanh; hiểu các khái niệm **nối với nhau thế nào**; và từ đó hiểu **vì sao** project thu thập dữ liệu như vậy và chọn đặc trưng như vậy.
>
> Mọi hình minh họa và con số đo đều lấy từ **dataset thật của project**, sinh bởi `scripts/theory_figures.py` (hình và bảng trong [`reports/theory/`](../../reports/theory/)). Tra nhanh thuật ngữ: [GLOSSARY](../09_REFERENCE/GLOSSARY.md).

## 1. Lộ trình đọc (đọc theo thứ tự)

```
Phần A — ÂM THANH VÀ ÂM NHẠC
 01 Âm thanh cơ bản ............ dao động, sóng, tần số, biên độ, pha
 02 Pitch, note, octave, semitone  cao độ là gì, tên nốt, công thức nốt → tần số
 03 F0, harmonic, timbre ........ vì sao cùng nốt mà khác nhạc cụ vẫn nghe khác

Phần B — NHẠC CỤ
 04 Nhạc cụ dây hoạt động thế nào  dây, thân đàn, kéo vĩ và gảy, bấm dây
 05 Violin   06 Viola   07 Cello   08 Double bass   09 Guitar
 10 Banjo và mandolin (nhạc cụ ngoài CSDL, dùng để thử)
 11 Cách chơi (kỹ thuật) ........ mỗi kỹ thuật làm âm thanh thay đổi ra sao

Phần C — TỪ ÂM THANH THẬT TỚI CON SỐ
 12 Âm thanh số ................ lấy mẫu, file âm thanh chứa gì
 13 Dạng sóng (waveform)
 14 FFT, STFT, phổ, spectrogram
 15 Đặc trưng âm thanh .......... mỗi đặc trưng đo gì, có nên dùng không
 16 Mô hình dữ liệu (dataset) ... vì sao dataset được tổ chức như vậy

Phần D — TỪ CON SỐ TỚI TÌM KIẾM
 17 Tách nốt (onset, segmentation)
 18 Vector đặc trưng của một file
 19 Khoảng cách và độ tương đồng
 20 PCA (giảm số chiều)
 21 R-tree
 22 CSDL đa phương tiện và tìm kiếm theo nội dung
```

## 2. Bản đồ khái niệm: mọi thứ nối với nhau thế nào

```
Nhạc cụ ─(có)→ Dây ─(bấm ở vị trí nào)→ Note ─(người nghe cảm nhận)→ Pitch
                                         │
                                         └─(đo bằng vật lý)→ F0 ─(dây rung theo nhiều kiểu cùng lúc)→ Harmonics
                                                                                          │
     ┌──────────────────── cộng các harmonic lại ────────────────────────────────────────┘
     ▼
 Waveform (dạng sóng: áp suất theo thời gian) ─(FFT)→ Spectrum (độ mạnh từng tần số)
     │                                                     │
     └──────────── cả hai cùng quyết định ─────────────────┴──→ Timbre (âm sắc: "tiếng violin")
                                                                    │
                                                    (đo bằng công thức)
                                                                    ▼
                                                  Audio features (RMS, MFCC, centroid…)
                                                                    │
                                                                    ▼
                                       Feature vector → CSDL → R-tree → tìm Top-5 file giống nhất
```

Ba loại thông tin **không được trộn lẫn** (chi tiết ở [16_DATASET_MODEL](16_DATASET_MODEL.md)):

| Loại | Ví dụ | Từ đâu ra |
|---|---|---|
| **Nhãn âm nhạc (metadata)** | nhạc cụ = violin, dây = A, nốt = A4, kỹ thuật = arco | Ghi trong tên file / catalog; con người đặt |
| **Đặc tính của tín hiệu** | F0 = 440 Hz, các harmonic, đường bao năng lượng, phổ | Có sẵn trong âm thanh; vật lý quyết định |
| **Đặc trưng trích xuất (feature)** | RMS-CV = 0.65, centroid = 2 299 Hz, 13 hệ số MFCC | Project **tính** từ tín hiệu bằng công thức |

Hệ thống tìm kiếm **chỉ được nhìn đặc trưng trích xuất** (vì file truy vấn mới không có nhãn). Nhãn chỉ dùng để **chia dữ liệu và chấm điểm**.

## 3. Mỗi câu hỏi được trả lời ở đâu

| Câu hỏi | Đọc |
|---|---|
| Dữ liệu âm thanh cần thu thập là gì, vì sao như vậy? | [16 Mô hình dữ liệu](16_DATASET_MODEL.md) §3–4 |
| Một file âm thanh chứa những thông tin gì? | [12 Âm thanh số](12_DIGITAL_AUDIO.md) §6 |
| Một nốt nhạc liên quan thế nào tới tần số? | [02 Pitch, note…](02_PITCH_NOTE_OCTAVE_SEMITONE.md) §5–6 |
| Frequency, pitch, note, F0, harmonic, timbre khác nhau thế nào? | [03 F0, harmonic, timbre](03_F0_HARMONICS_TIMBRE.md) §5 |
| Âm thanh từng nhạc cụ khác nhau ở đâu? | [05](05_VIOLIN.md)–[09](09_GUITAR.md), tổng kết ở [04](04_HOW_STRING_INSTRUMENTS_WORK.md) §9 |
| Vì sao cùng một nốt mà hai nhạc cụ nghe vẫn khác? | [03](03_F0_HARMONICS_TIMBRE.md) §6, [04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6–7 |
| Vì sao cần thu một nhạc cụ ở nhiều nốt và nhiều cách chơi? | [16](16_DATASET_MODEL.md) §3, [11](11_PLAYING_TECHNIQUES.md) |
| Vì sao chọn một đặc trưng cụ thể? Nó có ý nghĩa gì với bài toán? | [15 Đặc trưng](15_AUDIO_FEATURES.md) |

## 4. Danh sách hình minh họa (tất cả từ dữ liệu thật hoặc mô phỏng có ghi rõ)

| Hình | Nội dung | Dùng ở |
|---|---|---|
| `01_sine_frequency_amplitude_phase.png` | Tần số, biên độ, pha của sóng sin (mô phỏng) | 01 |
| `02_same_f0_different_harmonics.png` | Cùng F0, khác "công thức" harmonic → khác dạng sóng (mô phỏng) | 03 |
| `03_same_note_A3_five_instruments.png` | Nốt A3 trên 5 nhạc cụ: dạng sóng và phổ harmonic (dữ liệu thật) | 03, 05–09 |
| `04_envelope_bowed_vs_plucked.png` | Đường bao năng lượng: kéo vĩ và gảy | 04, 13 |
| `05_spectrogram_violin_vs_guitar.png` | Spectrogram violin và guitar cùng nốt A4 | 04, 14 |
| `06_instrument_ranges_open_strings.png` | Âm vực và dây buông của 5 nhạc cụ | 02, 04–09 |
| `07_features_by_instrument.png` | Centroid, RMS-CV, ZCR theo nhạc cụ (4 653 nốt) | 15 |
| `08_centroid_vs_pitch.png` | Centroid theo cao độ của 5 nhạc cụ | 03, 15 |
| `09_violin_technique_and_dynamics.png` | Kỹ thuật chơi và cường độ làm đổi centroid (violin) | 05, 11 |
| `10_recording_source_effect.png` | Cùng nhạc cụ, khác phòng thu → đặc trưng lệch | 15, 16 |
| `11_sampling_and_aliasing.png` | Lấy mẫu và giới hạn Nyquist (mô phỏng) | 12 |
| `12_frames_and_spectrum.png` | Cắt frame và FFT một frame | 14 |
| `13_mfcc_steps.png` | Các bước tính MFCC | 15 |
| `14_violin_vibrato_pitch.png` | Vibrato: cao độ dao động theo thời gian | 05, 11 |
| `15_feature_information.png` | Mỗi đặc trưng mang bao nhiêu thông tin về nhạc cụ, bao nhiêu về phòng thu (η²) | 15 |
| `16_pca_notes_2d.png` | PCA của 4 653 nốt: trục 1 là sáng – tối, trục 2 chủ yếu là nguồn thu | 20 |

Bảng số liệu đi kèm (cùng thư mục): `note_features.csv` (đặc trưng của 5 190 nốt), `feature_information.csv`, `feature_sensitivity.csv`, `source_transfer_1nn.csv`, `plucked_queries_nn.csv`, `pca_notes_*.csv`, `harmonics_A3.csv`, `centroid_by_pitch.csv`, `source_effect_centroid.csv`, `violin_technique_dynamics.csv`, `vibrato.csv`, `unseen_feature_summary.csv`.

## 5. Những điều số đo trên dataset cho thấy (tóm tắt)

| Phát hiện | Ở đâu |
|---|---|
| Cùng nốt A3, 5 nhạc cụ có 5 "công thức" harmonic khác hẳn nhau; violin có h1 yếu hơn h2 tới 19 dB | [03](03_F0_HARMONICS_TIMBRE.md) §4, [05](05_VIOLIN.md) §10 |
| Âm sắc đổi mạnh theo cao độ: centroid ÷ F0 của violin giảm từ 6.0 (quãng tám 3) xuống 1.3 (quãng tám 7) | [05](05_VIOLIN.md) §10 |
| Ở quãng tám 4, centroid trung vị của violin và viola **bằng nhau** (1 526 và 1 527 Hz) | [06](06_VIOLA.md) §9 |
| Double bass ở quãng tám 1 có "trọng tâm" phổ quanh harmonic thứ 10: F0 gần như không được phát ra | [08](08_DOUBLE_BASS.md) §3 |
| Kỹ thuật đổi cơ chế tạo âm (gảy, gõ) làm âm đổi mạnh hơn khoảng cách violin – viola | [11](11_PLAYING_TECHNIQUES.md) §5 |
| RMS-CV phụ thuộc độ dài nốt khi thu; guitar Iowa gảy nhỏ trông "sáng" hơn vì tiếng ồn nền | [15](15_AUDIO_FEATURES.md) §4, [09](09_GUITAR.md) §8.1 |
| MFCC c4, c5 là đặc trưng mang nhiều thông tin nhất (51%, 49%); 13 chiều MFCC std mang rất ít | [15](15_AUDIO_FEATURES.md) §9 |
| **Đặc trưng nhận ra nhạc cụ trong cùng nguồn thu (94–98%) nhưng gần như không chuyển sang nguồn khác (29–53%)** | [15](15_AUDIO_FEATURES.md) §16.1, [20](20_PCA.md) §6 |
| CSDL chỉ có 1 nhạc cụ gảy: âm gảy lạ (banjo, mandolin) bị xếp gần guitar khoảng một nửa số lần; violin gảy vẫn gần violin hơn (58%) | [10](10_BANJO_MANDOLIN.md) §4–5 |
