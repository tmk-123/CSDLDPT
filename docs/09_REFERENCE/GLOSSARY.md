# GLOSSARY — Từ điển thuật ngữ

> Viết cho người **chưa học nhạc** và **chưa học xử lý âm thanh**. Gặp từ lạ trong docs thì tra ở đây. Thiếu từ nào thì bổ sung vào đúng mục.

**Mục lục:**
1. [Âm nhạc cơ bản](#1-âm-nhạc-cơ-bản)
2. [Cách chơi nhạc cụ dây (kỹ thuật)](#2-cách-chơi-nhạc-cụ-dây-kỹ-thuật)
3. [Cường độ (dynamics)](#3-cường-độ-dynamics)
4. [Đọc tên file trong dataset](#4-đọc-tên-file-trong-dataset)
5. [File âm thanh và thu âm](#5-file-âm-thanh-và-thu-âm)
6. [Dataset và chia tập](#6-dataset-và-chia-tập)
7. [Tám khái niệm phải phân biệt trong pipeline](#7-tám-khái-niệm-phải-phân-biệt-trong-pipeline)
8. [Xử lý tín hiệu và đặc trưng](#8-xử-lý-tín-hiệu-và-đặc-trưng)
9. [CSDL và tìm kiếm](#9-csdl-và-tìm-kiếm)
10. [Ký hiệu riêng của project](#10-ký-hiệu-riêng-của-project)

---

## 1. Âm nhạc cơ bản

| Thuật ngữ | Giải thích dễ hiểu | Ví dụ |
|---|---|---|
| **Nốt (note)** | Một âm có cao độ xác định, phát ra một lần | Đánh một phím đàn piano là một nốt |
| **Cao độ (pitch)** | Âm nghe "cao" hay "trầm" | Tiếng sáo cao, tiếng trống bass trầm |
| **Tần số cơ bản (f₀)** | Con số đo cao độ: dây đàn rung bao nhiêu lần mỗi giây (Hz) | Nốt La (A4) = 440 Hz |
| **Tên nốt** | 7 nốt C D E F G A B = Đô Rê Mi Fa Sol La Si | C = Đô, A = La |
| **Quãng tám (octave)** | Khoảng từ một nốt tới nốt cùng tên cao hơn liền kề; tần số **gấp đôi** | A3 = 220 Hz, A4 = 440 Hz, A5 = 880 Hz |
| **Số sau tên nốt** | Cho biết nốt nằm ở quãng tám thứ mấy; số càng lớn càng cao | `C4` là Đô giữa đàn piano |
| **Nửa cung (semitone)** | Bước cao độ nhỏ nhất. Một quãng tám có 12 nửa cung | C → C♯ là nửa cung |
| **Dấu thăng (♯, sharp)** | Nâng nốt lên nửa cung. **Trong tên file viết là `s`** | `As4` = A♯4 (La thăng) |
| **Dấu giáng (♭, flat)** | Hạ nốt xuống nửa cung. Trong tên file Iowa viết là `b` | `Ab4` = A♭4 = G♯4 (cùng một phím) |
| **Âm vực (range)** | Từ nốt thấp nhất tới nốt cao nhất mà nhạc cụ chơi được | Violin: G3 → khoảng E7 |
| **MIDI number** | Đánh số mỗi nốt bằng một số nguyên, tăng 1 sau mỗi nửa cung | A4 = 69, C4 = 60 |
| **Âm sắc (timbre)** | "Màu" của âm thanh: giúp phân biệt hai nhạc cụ khi chơi **cùng nốt, cùng độ to**. **Đây chính là thứ project cần nhận ra** | Violin và sáo cùng thổi/kéo nốt A4 vẫn nghe khác nhau |
| **Bồi âm (harmonics, overtones)** | Một nốt thật không chỉ có f₀ mà còn có các tần số 2f₀, 3f₀, 4f₀… vang kèm. Độ mạnh yếu của chúng tạo nên âm sắc | A4: 440, 880, 1320, … Hz |
| **Monophonic / đơn âm** | Tại mỗi lúc chỉ vang **một** nốt | Giai điệu hát một mình |
| **Polyphonic / đa âm** | Nhiều nốt vang cùng lúc | Hợp âm guitar |
| **Hợp âm (chord)** | Nhiều nốt chơi cùng lúc | Quét cả 6 dây guitar |
| **Thang âm chromatic** | Đi lần lượt **từng nửa cung** | C, C♯, D, D♯, E, … |
| **Đường bao âm (envelope, ADSR)** | Độ to của một nốt thay đổi theo thời gian: **A**ttack (bật lên) → **D**ecay (giảm) → **S**ustain (giữ) → **R**elease (tắt) | Guitar: bật mạnh rồi tắt dần, không có sustain. Violin kéo vĩ: sustain dài |
| **Attack** | Khoảnh khắc đầu tiên của nốt, khi âm vừa bật lên | Tiếng "tưng" lúc gảy dây |

## 2. Cách chơi nhạc cụ dây (kỹ thuật)

### 2.1. Nhóm nhạc cụ
| Thuật ngữ | Giải thích | Nhạc cụ |
|---|---|---|
| **Bộ dây (chordophone)** | Nhạc cụ phát âm nhờ **dây rung** | Tất cả nhạc cụ trong project |
| **Nhạc cụ kéo vĩ (bowed)** | Dây được làm rung bằng **cây vĩ** kéo qua | Violin, viola, cello, double bass |
| **Nhạc cụ gảy (plucked)** | Dây được làm rung bằng **ngón tay hoặc miếng gảy** | Guitar, banjo, mandolin |
| **Vĩ (bow)** | Cây cung gỗ căng lông đuôi ngựa, dùng để kéo qua dây | — |
| **Violin** | Vĩ cầm: nhỏ nhất, cao nhất trong bộ kéo vĩ, đặt trên vai | Âm vực G3 trở lên |
| **Viola** | Lớn hơn violin một chút, trầm hơn khoảng 5 nốt, âm ấm hơn | Âm vực C3 trở lên |
| **Cello** | Đại hồ cầm: đặt giữa hai chân khi chơi | Âm vực C2 trở lên |
| **Double bass** | Công-trơ-bát: lớn nhất, trầm nhất, đứng chơi | Âm vực E1/C1 trở lên |
| **Dây buông (open string)** | Dây được chơi mà không bấm ngón | Dây Mi trầm của guitar = E2 |
| **`sul` + tên dây** | "Trên dây …". Trong tên file Iowa, `sulG` nghĩa là chơi trên dây G | `Violin.arco.mf.sulG…` = kéo vĩ trên dây Sol |

### 2.2. Kỹ thuật chơi (cột `technique` trong tên file)
| Thuật ngữ | Giải thích dễ hiểu | Project dùng? |
|---|---|---|
| **Arco** | (tiếng Ý: "dùng vĩ") Chơi bằng cách **kéo vĩ** qua dây. Âm liền, ngân dài. Cách chơi chính của violin, viola, cello, double bass | ✅ **Có** (D20) |
| **arco-normal** | Kéo vĩ bình thường, không kỹ thuật đặc biệt | ✅ Có |
| **Pizzicato (pizz)** | **Gảy dây bằng ngón tay** thay vì kéo vĩ. Âm ngắn, "tưng", nghe khá giống guitar | ❌ Không (quá ít mẫu: cello 0, double bass 12) |
| **Vibrato** | Ngón tay **rung nhẹ** trên dây, làm cao độ dao động lên xuống liên tục, tạo âm "ấm, sống" | ✅ Có (`molto-vibrato` = rung nhiều) |
| **Non-vibrato** | Cố ý **không rung**, âm "thẳng, lạnh" | ✅ Có |
| **Tremolo** | Kéo vĩ qua lại **rất nhanh** trên cùng một nốt, nghe như "rrrrr" | ❌ Không (đặc biệt) |
| **Trill** | **Láy nhanh** qua lại giữa hai nốt cạnh nhau (`major-trill`: cách 1 cung, `minor-trill`: cách nửa cung) | ❌ Không |
| **Legato** | Chơi các nốt **nối liền**, không ngắt quãng | ❌ (chỉ có trong phrase) |
| **Staccato** | Chơi nốt **ngắn, ngắt rời** | ❌ |
| **Spiccato** | Vĩ **nảy** trên dây, nốt ngắn và nhẹ | ❌ |
| **Détaché** | Mỗi nốt một lần kéo vĩ, tách rời nhưng không ngắn như staccato | ❌ |
| **Martelé** | Nốt nhấn mạnh như "búa gõ", có điểm bắt đầu rõ | ❌ |
| **Col legno** | Dùng **phần gỗ** của vĩ gõ (`battuto`) hoặc kéo (`tratto`) lên dây. Âm khô, lách cách | ❌ |
| **Sul ponticello** | Kéo vĩ **sát ngựa đàn**, âm chói, "rít" | ❌ |
| **Sul tasto** | Kéo vĩ **trên phím đàn**, âm mờ, nhẹ như sáo | ❌ |
| **Con sordino (con-sord)** | Gắn **cái chặn tiếng** lên ngựa đàn, âm nhỏ và tối hơn | ❌ |
| **Glissando** | **Trượt** liên tục từ nốt này sang nốt khác (nghe "vút") | ❌ |
| **Harmonics (bồi âm kỹ thuật)** | Chạm **nhẹ** ngón tay lên dây (không bấm hẳn) để nghe một bồi âm cao, trong, "như chuông". `natural-harmonic` dùng dây buông; `artificial-harmonic` bấm thêm một ngón | ✅ Chỉ với guitar (`harmonics`) |
| **Snap pizz** | Kéo dây lên rồi thả cho **đập vào phím đàn**, kêu "bốp" | ❌ |
| **Au talon / punta d'arco** | Kéo vĩ ở phần **gốc** / **đầu mũi** cây vĩ | ❌ |
| **normal (guitar)** | Gảy guitar bình thường | ✅ Có |
| **Phrase** | Không phải kỹ thuật mà là **một đoạn nhạc ngắn nhiều nốt** | Dùng làm truy vấn nhạc thật |

> **"Kỹ thuật đặc biệt" (`special`)** trong docs là tất cả những kỹ thuật đánh ❌ ở trên. Chúng được giữ trong catalog nhưng không dùng ở v1, vì quá ít mẫu và làm âm sắc lệch khỏi "tiếng bình thường" của nhạc cụ.

## 3. Cường độ (dynamics)
Ký hiệu độ to khi chơi, từ nhỏ đến to:

| Tên đầy đủ | Viết tắt | Nghĩa |
|---|---|---|
| molto pianissimo | ppp | Cực nhỏ |
| pianissimo | pp | Rất nhỏ |
| piano | p | Nhỏ |
| mezzo-piano | mp | Hơi nhỏ |
| mezzo-forte | mf | Hơi to |
| forte | f | To |
| fortissimo | ff | Rất to |
| crescendo / decrescendo | cresc. / decresc. | To dần / nhỏ dần |
| cresc-decresc | — | To dần rồi nhỏ dần |

Chơi to không chỉ tăng âm lượng mà còn làm âm **sáng hơn**, vì bồi âm cao mạnh lên. Vì vậy cường độ ảnh hưởng nhẹ tới âm sắc.

## 4. Đọc tên file trong dataset

**`Strings/` (Philharmonia):** `<nhạc cụ>_<nốt>_<độ dài>_<cường độ>_<kỹ thuật>.mp3`
```
cello_As2_05_forte_arco-normal.mp3
  cello        → nhạc cụ: cello
  As2          → nốt La thăng (A♯), quãng tám 2  (≈ 116.5 Hz)
  05           → nhãn độ dài danh nghĩa "0.5" (KHÔNG phải số giây thật)
  forte        → chơi to
  arco-normal  → kéo vĩ bình thường
```
Nhãn độ dài có các giá trị `025`, `05`, `1`, `15`, `long`, `very-long`, `phrase`.

**Iowa MIS:** `<Nhạc cụ>.<kỹ thuật>.<cường độ>.<dây>.<khoảng nốt>.<mono/stereo>.aif`
```
Violin.arco.mf.sulG.G3B3.aiff
  Violin  → nhạc cụ        arco → kéo vĩ          mf → hơi to
  sulG    → chơi trên dây G
  G3B3    → file chứa các nốt liên tiếp từ G3 tới B3 (G3, G♯3, A3, A♯3, B3 = 5 nốt)
Guitar.ff.sulE.E2B2.mono.aif   → guitar, rất to, dây Mi trầm, các nốt E2…B2 (8 nốt), mono
```

## 5. File âm thanh và thu âm

| Thuật ngữ | Giải thích |
|---|---|
| **Sample rate (tần số lấy mẫu)** | Số lần đo biên độ âm thanh mỗi giây. 44 100 Hz = 44 100 lần/giây. Chỉ ghi được âm có tần số **dưới một nửa** con số này |
| **Bit depth** | Độ chính xác mỗi lần đo. 16-bit = 65 536 mức |
| **Mono / Stereo** | 1 kênh / 2 kênh (trái, phải). ⚠️ **Không liên quan tới số nốt**: file mono và file stereo cùng tên chứa cùng một nội dung. Số nốt xem ở phần khoảng nốt trong tên file (ví dụ `E2B2` = 8 nốt, `B3` = 1 nốt). Project dùng **mono** |
| **MP3** | Định dạng **nén mất mát**: bỏ bớt phần tai khó nghe để file nhỏ |
| **WAV, AIFF** | Định dạng **không nén**: giữ nguyên chất lượng. AIFF là định dạng của Apple, tương tự WAV |
| **Clipping** | Âm to quá mức tối đa nên bị "cắt đỉnh", gây méo tiếng |
| **Khoảng lặng (silence)** | Đoạn không có âm (hoặc chỉ có nhiễu rất nhỏ) |
| **dB (decibel)** | Đơn vị đo độ to tương đối. "−40 dB so với đỉnh" = nhỏ hơn đoạn to nhất khoảng 100 lần về biên độ |
| **Phòng tiêu âm (anechoic chamber)** | Phòng có tường hút hết âm, **không có tiếng vang**. Iowa MIS thu ở đây |
| **Tiếng vang (reverb)** | Âm phản xạ từ tường phòng, kéo dài sau khi nốt đã dừng |
| **Micro (microphone)** | Thiết bị thu âm. Micro và phòng khác nhau làm âm thu được hơi khác nhau dù cùng nhạc cụ |
| **MD5** | "Dấu vân tay" của file. Hai file có MD5 giống nhau nghĩa là **giống hệt nhau từng byte** |

## 6. Dataset và chia tập

| Thuật ngữ | Giải thích |
|---|---|
| **Dataset** | Bộ dữ liệu âm thanh dùng cho project |
| **Nguồn (source)** | Nơi dữ liệu xuất phát: `philharmonia` (thư mục `Strings/`) hoặc `iowa` (Iowa MIS) |
| **Philharmonia** | Thư viện mẫu âm thanh của dàn nhạc Philharmonia (London). Quy ước tên file trong `Strings/` giống thư viện này |
| **Iowa MIS** | University of Iowa Musical Instrument Samples: thư viện mẫu nhạc cụ miễn phí của Đại học Iowa (Mỹ), thu trong phòng tiêu âm |
| **Single-note / nốt đơn** | File chỉ chứa **một** nốt |
| **Multi-note / sequence** | File chứa **nhiều** nốt nối tiếp. Trong project, phần lớn được **ghép** từ nốt đơn |
| **Ghép (synthesize)** | Nối nhiều nốt đơn thật thành một file multi-note. Không phải tạo âm thanh giả |
| **Catalog** | Bảng liệt kê **mọi file**, mỗi file một dòng, kèm thông tin và nhãn `status`, `split`. **Lọc = điền nhãn vào catalog, không xóa file** |
| **status** | File dùng được không: `OK`, `CORRUPT` (hỏng), `DUPLICATE` (trùng), `TOO_SHORT` (quá ngắn), `PITCH_MISMATCH` (cao độ không khớp tên) |
| **split** | File được dùng vào việc gì (các dòng dưới) |
| **REF** | Nốt đơn **tham chiếu**, dùng để học prototype |
| **DB_POOL** | Nốt đơn dùng để **ghép 500 file CSDL** |
| **QUERY_POOL** | Nốt đơn dùng để **ghép file truy vấn** kiểm thử |
| **SPARE** | Nốt **dư**, để dự trữ (truy vấn nốt đơn, thay thế nốt lỗi) |
| **PHRASE** | 446 đoạn nhạc thật nhiều nốt có sẵn trong `Strings/`, dùng làm truy vấn |
| **UNSEEN / nhạc cụ ngoài CSDL** | Banjo, mandolin: **cố ý không đưa vào CSDL**, chỉ dùng làm truy vấn, để kiểm tra yêu cầu "nhạc cụ không có trong dữ liệu" của đề bài |
| **NONE** | Không dùng (file lỗi hoặc kỹ thuật đặc biệt) |
| **Ground truth** | "Đáp án đúng" đã biết trước, dùng để chấm. Ví dụ: file này là cello; nốt thứ 2 bắt đầu ở giây 0.88 |
| **Data leakage (rò rỉ dữ liệu)** | Dữ liệu dùng để **kiểm tra** lại lọt vào phần **xây dựng**, làm kết quả cao ảo. Giống như học tủ đúng đề thi |
| **Source confound (nhiễu nguồn)** | Hệ thống học nhầm đặc điểm **nguồn thu** (phòng, micro) thay vì **nhạc cụ**. Ví dụ: nếu mọi file guitar đều thu ở Iowa, hệ thống có thể chỉ nhận ra "tiếng phòng Iowa" |
| **Cân bằng (balanced)** | Mỗi nhạc cụ có số file như nhau trong CSDL (100), để kết quả không nghiêng về nhạc cụ nhiều file |
| **Giấy phép (license)** | Điều khoản cho phép dùng dữ liệu. CC BY = được dùng nếu ghi nguồn; NC = không thương mại; ND = không được chỉnh sửa |

## 7. Tám khái niệm phải phân biệt trong pipeline

| Khái niệm | Là gì | Kích thước | Lưu trong CSDL? |
|---|---|---|---|
| **Raw audio** | Chuỗi mẫu PCM sau giải mã (mono, 22 050 Hz) | ~22 050 số/giây | Không; chỉ lưu đường dẫn |
| **Frame** | Cửa sổ 2048 mẫu (≈ 93 ms), hop 512 | ~43 frame/giây | **Không bao giờ** |
| **Segment** | Đoạn liên tục, *xấp xỉ* một nốt, do segmentation tìm ra | 0.12–2 s | Có (bảng `segment`) |
| **Segment feature vector** s | Âm sắc của một segment | 32D | Có (`segment.feat`) |
| **Reference prototype** P_j | Tâm cụm K-means của nốt REF thuộc một nhạc cụ | 20 × 32D | Có (`prototype`) |
| **File-level vector** v | MỘT vector cho cả file = [h ‖ μ] | 52D | Có (`file_vector.v_raw`) |
| **Indexed vector** u | v sau chuẩn hóa + PCA; là điểm trong R-tree | 8D | Có (`file_vector.u_pca`) + file R-tree |
| **Database record** | Một dòng `audio_file` + `file_vector` + một entry R-tree. **1 file = 1 record** | — | Có |

> frame → segment → (so với prototype) → v 52D → v' 52D → u 8D → điểm trong R-tree → record.

## 8. Xử lý tín hiệu và đặc trưng

| Thuật ngữ | Giải thích |
|---|---|
| FFT | Biến đổi tín hiệu theo thời gian thành **phổ**: mỗi tần số mạnh bao nhiêu |
| STFT | Làm FFT trên từng frame, cho biết phổ thay đổi theo thời gian |
| Spectrogram | Ảnh của STFT: trục ngang là thời gian, trục dọc là tần số, màu là độ mạnh |
| Window (Hann) | Hàm "làm mềm" hai đầu frame trước khi FFT, giảm méo phổ |
| Mel | Thang tần số mô phỏng tai người (tai nhạy với khác biệt ở tần thấp hơn ở tần cao) |
| MFCC | Bộ số mô tả **hình dạng phổ**, tức âm sắc. Đặc trưng chính của project |
| RMS | Năng lượng (độ to) của một frame |
| ZCR | Số lần tín hiệu đổi dấu trong một frame; cao nghĩa là nhiều nhiễu hoặc tần cao |
| Spectral centroid | "Trọng tâm" phổ, cho biết âm **sáng** hay **tối** |
| Spectral bandwidth | Phổ trải rộng hay tập trung |
| Spectral rolloff | Tần số mà dưới nó chứa 85% năng lượng |
| Chroma | Năng lượng của 12 tên nốt; đo giai điệu, **không dùng** trong project |
| pYIN | Thuật toán đo f₀ (cao độ) của từng frame |
| Onset / Offset | Thời điểm một nốt **bắt đầu** / **kết thúc** |
| Segmentation | Chia file nhiều nốt thành các đoạn, mỗi đoạn xấp xỉ một nốt |
| Spectral flux / SuperFlux | Cách phát hiện onset dựa trên mức tăng của phổ; SuperFlux chống báo nhầm do vibrato |
| Peak-normalize | Phóng/thu biên độ sao cho đỉnh lớn nhất bằng một mức cố định (0.95) |
| Trim | Cắt khoảng lặng ở đầu và cuối file |
| Pre-emphasis | Bộ lọc làm nổi tần cao (thường dùng cho tiếng nói); project **không dùng** |
| Mean / Std / Median | Trung bình / độ lệch chuẩn (mức dao động) / trung vị (giá trị ở giữa) |

## 9. CSDL và tìm kiếm

| Thuật ngữ | Giải thích |
|---|---|
| CBAR | Content-Based Audio Retrieval: tìm âm thanh theo **nội dung âm thanh**, không theo tên hay từ khóa |
| Query-by-Example | Truy vấn bằng cách đưa vào **một file mẫu** |
| Feature vector | Dãy số mô tả một đối tượng; mỗi file trở thành một **điểm** trong không gian nhiều chiều |
| Z-score | Chuẩn hóa: (x − trung bình)/độ lệch chuẩn, để mọi đặc trưng cùng thang đo |
| PCA | Giảm số chiều nhưng giữ lại nhiều thông tin nhất |
| Euclid distance | Khoảng cách "đường thẳng" giữa hai điểm |
| Cosine similarity | Đo góc giữa hai vector (bỏ qua độ dài) |
| k-NN | Tìm k điểm gần nhất (project: k = 5) |
| R-tree / R\*-tree | Cây chỉ mục nhóm các điểm gần nhau vào các **hộp (MBR)** để tìm nhanh |
| MBR | Hộp chữ nhật nhỏ nhất bao trọn một nhóm điểm |
| MINDIST | Khoảng cách ngắn nhất từ điểm truy vấn tới một hộp |
| Lower bound (cận dưới) | Khoảng cách sau PCA **không bao giờ lớn hơn** khoảng cách thật |
| Filter-and-refine / GEMINI | Lọc nhanh ứng viên ở số chiều thấp, rồi tính chính xác ở số chiều cao |
| Brute force | Tính khoảng cách tới **tất cả** các file (chậm nhưng chắc chắn đúng); dùng để kiểm tra R-tree |
| Curse of dimensionality | Càng nhiều chiều, chỉ mục càng kém hiệu quả |
| Hybrid storage | File âm thanh nằm trên đĩa; CSDL chỉ lưu đường dẫn, metadata và vector |
| BLOB | Dữ liệu nhị phân lưu trong CSDL (ở đây là vector số thực) |
| P@5 | Trong 5 kết quả trả về, có bao nhiêu phần đúng nhạc cụ |
| Top-1 / Hit@5 / MRR | Kết quả đầu tiên có đúng không / có ít nhất một kết quả đúng trong 5 không / kết quả đúng đầu tiên nằm ở hạng mấy |
| Semantic gap | Khoảng cách giữa con số máy tính tính được và ý nghĩa con người cảm nhận |

## 10. Ký hiệu riêng của project

| Ký hiệu | Nghĩa |
|---|---|
| technique_family | Nhóm kỹ thuật: `arco` / `pizz` / `pluck` (guitar gảy thường) / `harmonic` / `special` |
| h | Histogram mềm 20D: file giống mỗi prototype bao nhiêu % |
| μ | Trung bình có trọng số của các vector segment (32D) |
| α_i | Trọng số thời lượng của segment i (segment dài thì đóng góp nhiều) |
| τ | "Nhiệt độ" của softmax: quyết định phân bố mềm hay gắt |
| r8 | Khoảng cách 8D tới ứng viên xa nhất trong tập ứng viên |
| model_version | Nhãn đồng bộ model, vector và index (v1, v2, …) |
| D01…D22 | Mã quyết định thiết kế ([DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md)) |
| B0…B11, D1…D6 | Mã bước trong kế hoạch ([PART_1_PLAN](../02_PLANS/PART_1_PLAN.md)) |
