# 03. F0, harmonic, timbre — vì sao cùng một nốt mà khác nhạc cụ vẫn nghe khác

> **Đọc xong file này bạn sẽ hiểu:** F0 là gì và khác pitch ra sao; vì sao một dây đàn tạo ra **nhiều** tần số cùng lúc (harmonic); âm sắc (timbre) được tạo nên từ đâu; và phân biệt rõ 6 khái niệm hay bị nhầm.
> **Cần biết trước:** [01](01_SOUND_BASICS.md) (sóng sin, tần số), [02](02_PITCH_NOTE_OCTAVE_SEMITONE.md) (nốt, quãng tám).
> **Đọc tiếp:** [04 Nhạc cụ dây hoạt động thế nào](04_HOW_STRING_INSTRUMENTS_WORK.md).

---

## 1. F0 — tần số cơ bản (fundamental frequency)

**Là gì.** F0 là **tần số lặp lại của dạng sóng**: nếu dạng sóng (dù phức tạp tới đâu) cứ sau `T` giây lại lặp lại y hệt, thì F0 = 1/T.

**Hình dung.** Nhìn panel trái của hình dưới: dạng sóng của violin chơi nốt A3 rất gồ ghề, nhưng **cứ 4.55 ms lại lặp lại đúng hình đó**. Vậy F0 = 1 / 0.00455 s ≈ **220 Hz**.

**F0 và pitch.** Với âm của nhạc cụ có cao độ, pitch ta nghe ≈ F0. Nhưng:
- **F0 là vật lý** (đo được bằng máy, đơn vị Hz).
- **Pitch là cảm nhận** (đo bằng tai, gọi bằng tên nốt).
- Hai thứ khớp nhau gần như hoàn toàn với âm tuần hoàn, nên trong thực tế người ta hay dùng F0 để "đo" pitch.

**Một điều bất ngờ (đo được trong dataset).** F0 **không nhất thiết là thành phần mạnh nhất** của âm thanh, thậm chí có thể rất yếu, mà tai vẫn nghe ra đúng nốt. Ví dụ violin chơi A3 (bảng ở §4): thành phần 220 Hz yếu hơn thành phần 440 Hz tới **19.4 dB** (yếu hơn khoảng 9 lần về biên độ), nhưng ta vẫn nghe ra A3 chứ không phải A4. Lý do: **dạng sóng vẫn lặp lại mỗi 4.55 ms**, và não cảm nhận nhịp lặp đó. Hiện tượng này gọi là **"F0 bị thiếu/yếu" (missing fundamental)**, rất hay gặp ở các nốt thấp của violin và double bass (xem [04](04_HOW_STRING_INSTRUMENTS_WORK.md) §7).

**Vì sao quan trọng với project.** Project **đo F0** bằng thuật toán pYIN (tìm chu kỳ lặp, không tìm đỉnh phổ mạnh nhất — chính vì F0 có thể yếu). F0 dùng để:
- kiểm tra nốt khi cắt file Iowa,
- làm một chiều trong vector đặc trưng (median log2 F0: cho biết âm vực).

---

## 2. Harmonic (bồi âm) — một dây, nhiều tần số cùng lúc

**Là gì.** Âm của một nhạc cụ có cao độ là **tổng của nhiều sóng sin** có tần số **gấp 1, 2, 3, 4… lần F0**. Mỗi sóng sin thành phần là **một harmonic (bồi âm, họa âm)**. Harmonic thứ `k` có tần số:
```
f_k = k × F0        (k = 1, 2, 3, …)
```
Harmonic thứ 1 chính là F0.

**Vì sao dây đàn tạo ra harmonic? (bản chất vật lý)**
Một dây bị giữ chặt **hai đầu** (đầu ngựa đàn và đầu bấm/đầu cần) chỉ có thể rung theo những "kiểu" mà hai đầu đứng yên:
```
Kiểu 1:  ⌒⌒⌒⌒⌒⌒⌒⌒        cả dây cong một múi        → tần số F0
Kiểu 2:  ⌒⌒⌒⌒ ⌣⌣⌣⌣        hai múi, giữa dây đứng yên  → 2 × F0
Kiểu 3:  ⌒⌒⌒ ⌣⌣⌣ ⌒⌒⌒     ba múi                      → 3 × F0
...
```
Mỗi kiểu là một **sóng đứng**, rung với tần số gấp `k` lần kiểu đầu tiên (vì múi ngắn hơn `k` lần). Khi kéo vĩ hay gảy, dây **rung theo tất cả các kiểu cùng lúc**, mỗi kiểu một độ mạnh khác nhau. Âm ta nghe là tổng của chúng.

**Ví dụ — chuỗi harmonic của nốt A3 (F0 = 220 Hz):**

| k | Tần số | Gần nốt nào | Lệch so với nốt đó |
|---|---|---|---|
| 1 | 220 Hz | A3 | 0 cent (chính là nốt) |
| 2 | 440 Hz | A4 | 0 (cao hơn đúng 1 quãng tám) |
| 3 | 660 Hz | E5 (659.26) | +2 cent |
| 4 | 880 Hz | A5 | 0 (2 quãng tám) |
| 5 | 1 100 Hz | C♯6 (1 108.73) | −14 cent |
| 6 | 1 320 Hz | E6 (1 318.51) | +2 cent |
| 7 | 1 540 Hz | G6 (1 567.98) | −31 cent |
| 8 | 1 760 Hz | A6 | 0 (3 quãng tám) |

Nhận xét: harmonic 2, 4, 8 là **cùng tên nốt** (A) ở các quãng tám cao hơn — đây chính là lý do hai âm cách quãng tám nghe "giống nhau" ([02](02_PITCH_NOTE_OCTAVE_SEMITONE.md) §2).

**Thuật ngữ hay gặp:**
| Từ | Nghĩa | Quan hệ |
|---|---|---|
| Harmonic | Thành phần có tần số đúng k × F0 | Harmonic 1 = F0 |
| Overtone (âm bội) | Mọi thành phần **phía trên** F0 | Overtone thứ 1 = harmonic 2 (dễ nhầm!) |
| Partial (thành phần) | Mọi thành phần, kể cả loại không đúng k × F0 | Dây đàn thật hơi cứng nên partial cao bị lệch nhẹ khỏi k × F0 |

**Vì sao quan trọng với project.** **Độ mạnh của từng harmonic** chính là thứ phân biệt các nhạc cụ (§4). Mọi đặc trưng phổ của project (centroid, rolloff, MFCC) đều là những cách **tóm tắt** "harmonic nào mạnh, harmonic nào yếu".

---

## 3. Từ harmonic tới dạng sóng: "công thức" quyết định hình dạng

Cùng một F0, nếu **trộn các harmonic theo tỉ lệ khác nhau**, ta được dạng sóng khác nhau:

![Cùng F0 khác công thức harmonic](../../reports/theory/02_same_f0_different_harmonics.png)

- **Công thức A** (harmonic giảm đều 1, 1/2, 1/3…) → sóng răng cưa. Đây gần đúng với dao động của dây khi **kéo vĩ**.
- **Công thức B** (chỉ harmonic lẻ mạnh) → sóng gần vuông.
- **Cả hai lặp lại sau cùng 4.55 ms** → cùng F0 = 220 Hz → **cùng nốt A3**. Nhưng hình dạng khác nhau → **nghe khác nhau**. Sự khác biệt đó gọi là **âm sắc**.

> **"Công thức" harmonic** (danh sách độ mạnh của từng harmonic) được gọi là **phổ (spectrum)** của âm. Cách tính phổ từ dạng sóng (FFT) ở [14](14_FFT_STFT_SPECTRUM.md).

---

## 4. Timbre (âm sắc) — "màu" của âm thanh

**Là gì.** Âm sắc là thuộc tính giúp ta **phân biệt hai âm có cùng cao độ và cùng độ to**. Nói cách khác: âm sắc là **tất cả những gì còn lại** sau khi bỏ cao độ và độ to.

**Âm sắc được tạo nên từ đâu?** Không phải một thứ duy nhất, mà từ nhiều thứ cùng lúc:

| Yếu tố | Nghĩa | Ví dụ |
|---|---|---|
| 1. **Phổ harmonic** | Harmonic nào mạnh, harmonic nào yếu | Violin nhiều harmonic cao → sáng; cello harmonic thấp trội → tối, tròn |
| 2. **Cộng hưởng thân đàn** | Thân đàn khuếch đại một số vùng tần số **cố định**, bất kể chơi nốt nào | "Chất gỗ" riêng của mỗi cây đàn ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §7) |
| 3. **Đường bao thời gian** | Âm bắt đầu, giữ, tắt ra sao | Gảy: bật nhanh rồi tắt dần; kéo vĩ: giữ đều |
| 4. **Thành phần nhiễu** | Âm không có cao độ đi kèm | Tiếng vĩ cọ dây, tiếng móng gảy |
| 5. **Biến đổi theo thời gian** | Các thành phần thay đổi khi nốt đang vang | Vibrato; harmonic cao của guitar tắt trước |

**Dữ liệu thật: cùng nốt A3 trên 5 nhạc cụ**

![Nốt A3 trên 5 nhạc cụ](../../reports/theory/03_same_note_A3_five_instruments.png)

Độ mạnh 6 harmonic đầu (dB so với harmonic mạnh nhất; số liệu: `reports/theory/harmonics_A3.csv`):

| Nhạc cụ (file) | h1 (220) | h2 (440) | h3 (660) | h4 (880) | h5 (1 100) | h6 (1 320) | Đọc phổ |
|---|---|---|---|---|---|---|---|
| Violin (`violin_A3_15_forte`) | −19.4 | **0** | −15.2 | −5.2 | −16.3 | −15.9 | F0 rất yếu, h2 và h4 mạnh, nhiều harmonic cao → sáng |
| Viola (`viola_A3_1_forte`) | **0** | −7.8 | −7.3 | −10.6 | −29.9 | −32.8 | 4 harmonic đầu đều mạnh, sau đó tụt hẳn → ấm, đầy |
| Cello (`cello_A3_025_forte`) | **0** | −9.1 | −46.6 | −29.7 | −32.5 | −39.3 | Gần như chỉ có h1 và h2 → tròn, tối |
| Double bass (`double-bass_A3_15_forte`) | −0.5 | **0** | −16.4 | −1.1 | −17.6 | −20.7 | Nhiều harmonic mạnh (A3 là vùng cao của bass) → căng, "gắt" |
| Guitar (`guitar_A3_very-long_piano_normal`) | **0** | −13.8 | −21.5 | −43.9 | −37.1 | −28.2 | F0 trội, harmonic yếu dần nhanh → gần như sóng sin, tròn |

**Cùng một nốt, cùng F0 ≈ 220 Hz, mà 5 "công thức" harmonic hoàn toàn khác nhau.** Đây là câu trả lời bằng số cho câu hỏi "vì sao cùng nốt mà khác nhạc cụ vẫn nghe khác".

> **Lưu ý trung thực:** mỗi dòng trên là **một** bản thu. Cùng một nhạc cụ, phổ còn đổi theo nốt, cường độ, cách chơi, dây và phòng thu. Vì vậy project không dựa vào một nốt, mà dùng **hàng nghìn nốt** và các đặc trưng thống kê ([15](15_AUDIO_FEATURES.md)).

---

## 5. Phân biệt 6 khái niệm hay nhầm: Frequency ≠ Pitch ≠ Note ≠ F0 ≠ Harmonic ≠ Timbre

**Ví dụ xuyên suốt:** một nghệ sĩ kéo vĩ dây A buông của **violin** (nốt A4).

| Khái niệm | Thuộc loại | Trong ví dụ là gì | Câu hỏi nó trả lời |
|---|---|---|---|
| **Frequency** (tần số) | Vật lý — khái niệm chung | **Bất kỳ** tần số nào có trong âm: 440, 880, 1 320, 1 760 Hz… và cả dải tần số rộng của tiếng vĩ cọ dây | "Có dao động nào ở tần số f không, mạnh bao nhiêu?" |
| **F0** | Vật lý — một tần số đặc biệt | **440 Hz**: dạng sóng lặp lại mỗi 2.27 ms | "Âm này lặp lại nhanh tới đâu?" |
| **Harmonic** | Vật lý — các thành phần của âm | h1 = 440, **h2 = 880**, h3 = 1 320 Hz… (k × F0) | "Âm này gồm những thành phần nào?" |
| **Pitch** (cao độ) | Cảm nhận của tai | Người nghe thấy "**nốt La giữa**" | "Nghe cao hay thấp?" |
| **Note** (nốt) | Nhãn, ký hiệu | Chữ "**A4**" trên bản nhạc, trong tên file | "Gọi tên cao độ này là gì?" |
| **Timbre** (âm sắc) | Cảm nhận, quyết định bởi phổ + đường bao + nhiễu | "**Đây là tiếng violin**, sáng, có tiếng vĩ" | "Nhạc cụ nào, chơi kiểu gì?" |

**Chúng nối với nhau thế nào** (chuỗi CLAUDE.md yêu cầu hiểu):
```
Nhạc cụ (violin)
   ↓  có 4 dây; người chơi chọn dây A
Dây (dây A, buông)
   ↓  dây dài và căng tới mức rung 440 lần/s
Note (A4)                 ← tên con người đặt cho cao độ đó
   ↓  tai cảm nhận
Pitch ("La giữa")
   ↓  tương ứng với nhịp lặp vật lý
F0 (440 Hz)
   ↓  dây rung theo nhiều kiểu cùng lúc
Harmonics (440, 880, 1 320 … với độ mạnh do cách kéo vĩ và thân đàn quyết định)
   ↓  cộng tất cả lại theo thời gian
Waveform (dạng sóng: áp suất theo thời gian)          → [13]
   ↓  phân tích thành các tần số (FFT)
Spectrum (độ mạnh của từng tần số)                    → [14]
   ↓  phổ + đường bao + nhiễu cùng tạo nên
Timbre (âm sắc: "tiếng violin")
   ↓  project đo bằng công thức
Audio features (centroid, MFCC, RMS-CV, F0…)          → [15]
```

**Câu dễ nhầm, viết đúng:**
- ❌ "Nốt A4 có tần số 440 Hz" → ✅ "Nốt A4 có **F0** = 440 Hz; âm của nó chứa **nhiều tần số**: 440, 880, 1 320…"
- ❌ "Violin và cello chơi cùng tần số nên giống nhau" → ✅ "Cùng **F0** nhưng khác **độ mạnh các harmonic** và **đường bao**, nên khác **âm sắc**."
- ❌ "Pitch = tần số" → ✅ "Pitch là cảm nhận; với âm tuần hoàn nó khớp với **F0**, không phải với tần số mạnh nhất."

---

## 6. Vì sao cùng một nốt mà hai nhạc cụ vẫn nghe khác nhau? — trả lời đầy đủ

1. **Khác công thức harmonic** (bảng §4): cách tạo âm (kéo vĩ hay gảy, kéo ở đâu trên dây) và độ cứng, độ nặng của dây quyết định harmonic nào được kích thích mạnh.
2. **Khác thân đàn**: thân to/nhỏ, gỗ, hình dạng khác nhau thì khuếch đại các vùng tần số khác nhau ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §7). Violin có thân nhỏ, cộng hưởng mạnh ở vùng cao; cello thân lớn, cộng hưởng ở vùng thấp.
3. **Khác đường bao thời gian**: guitar tắt dần, bộ kéo vĩ giữ đều (hình ở [04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6).
4. **Khác thành phần nhiễu**: tiếng vĩ cọ dây (bộ kéo vĩ), tiếng móng/ngón chạm dây (guitar).
5. **Khác vị trí của nốt trong âm vực**: A3 là nốt **thấp** với violin (gần dây buông thấp nhất) nhưng là nốt **cao** với double bass. Cùng nốt, nhưng mỗi nhạc cụ đang ở một "vùng" khác của mình → âm sắc khác.

**Đo bằng một con số: "độ sáng" (spectral centroid) ở cùng một nốt** (trung vị trên nhiều bản thu; `reports/theory/centroid_by_pitch.csv`):

| Nốt | Violin | Viola | Cello | Double bass | Guitar |
|---|---|---|---|---|---|
| G3 (196 Hz) | 1 263 Hz | 1 087 Hz | 951 Hz | 861 Hz | 647 Hz |
| A3 (220 Hz) | 1 285 Hz | 1 081 Hz | 1 042 Hz | 1 217 Hz | 723 Hz |
| C4 (262 Hz) | 1 288 Hz | 1 085 Hz | 1 199 Hz | 983 Hz | 704 Hz |
| G4 (392 Hz) | 1 753 Hz | 1 696 Hz | 1 502 Hz | 1 199 Hz | 854 Hz |

![Centroid theo cao độ](../../reports/theory/08_centroid_vs_pitch.png)

Đọc hình: ở **cùng một nốt** (cùng vị trí trên trục ngang), các đường nằm ở **độ cao khác nhau**: violin thường sáng nhất, guitar tối nhất. Nhưng các đường **sát nhau và có chỗ cắt nhau** (violin–viola, cello–double bass) → **một đặc trưng là không đủ**; project dùng 32 đặc trưng cùng lúc.

---

## 7. Vì sao quan trọng với project

- Bài toán của project là **tìm tiếng nhạc cụ giống nhau**, tức là so **âm sắc**, không phải so nốt. Vì vậy:
  - Các đặc trưng chính đo **phổ harmonic và hình bao phổ** (MFCC, centroid, rolloff, bandwidth) và **đường bao thời gian** (RMS-CV).
  - F0 chỉ là **một** trong 32 chiều, để biết âm vực.
  - **Không** dùng chroma (chỉ đo tên nốt).
- Vì âm sắc **thay đổi theo nốt** (centroid tăng mạnh khi nốt cao lên, hình trên), dataset phải có **mỗi nhạc cụ ở rất nhiều nốt** để hệ thống học được "violin ở mọi âm vực trông thế nào" ([16](16_DATASET_MODEL.md)).
