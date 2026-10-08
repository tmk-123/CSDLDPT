# 09. Guitar (tây ban cầm)

> **Đọc xong file này bạn sẽ biết:** guitar khác 4 nhạc cụ kéo vĩ ở đâu (gảy, có phím đàn, 6 dây); 6 dây với nốt, quãng tám, tần số; phím đàn chia dây theo đúng công thức nửa cung ra sao; vì sao dây Sol–Si lệch khỏi quy luật; vị trí gảy làm đổi âm sắc thế nào; vì sao guitar là nhạc cụ "tối" nhất và "tắt dần" nhất; guitar trong dataset.
> **Cần biết trước:** [04](04_HOW_STRING_INSTRUMENTS_WORK.md) (đặc biệt §4 phím đàn, §6.2 gảy).
> **Đọc tiếp:** [10 Banjo và mandolin](10_BANJO_MANDOLIN.md), hai nhạc cụ gảy **không có** trong CSDL, dùng để thử hệ thống.

---

## 1. Guitar là gì, thuộc họ nào

```
Nhạc cụ dây → có cần đàn → GẢY:  GUITAR · banjo · mandolin
```
- Guitar là nhạc cụ dây **gảy** (bằng ngón tay, móng tay hoặc miếng gảy), có **6 dây** và **phím đàn** trên cần.
- Có nhiều loại: guitar **cổ điển** (dây nylon), guitar **acoustic dây sắt**, guitar **điện**. Bộ Iowa dùng đàn **Raimundo 118**, một cây guitar cổ điển dây nylon ([REFERENCES](../09_REFERENCE/REFERENCES.md)). Bộ Philharmonia **không ghi** loại đàn.
- **Khác 4 nhạc cụ kia ở 3 điểm lớn:**
  1. **Gảy** chứ không kéo vĩ → âm **tắt dần**, không giữ được ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6.2).
  2. **Có phím đàn** → cao độ "đóng khung" đúng từng nửa cung.
  3. **6 dây** và lên dây **không đều** (§4).

---

## 2. Cấu tạo

| Bộ phận | Ở guitar cổ điển | Ảnh hưởng tới âm thanh |
|---|---|---|
| **Thân đàn** | Hình số 8, mặt gỗ vân sam hoặc tuyết tùng, lưng và hông gỗ cứng; **mỏng và rộng** hơn họ violin | Cộng hưởng chính ở khoảng **100 Hz** (khối khí) và **200 Hz** (mặt đàn), tức vùng nốt trầm |
| **Lỗ thoát âm** | **Một lỗ tròn** giữa mặt đàn | Cho khối khí "thở" → cộng hưởng khí |
| **Dây** | 3 dây trầm: lõi sợi nylon quấn đồng mạ bạc; 3 dây cao: **nylon** trơn. Phần dây rung dài **650 mm** | Nylon mềm, tiêu hao năng lượng nhanh → harmonic cao tắt rất nhanh → âm **tròn, ấm** |
| **Phím đàn (fret)** | Các thanh kim loại gắn ngang cần, thường **19 phím** | Mỗi phím = 1 nửa cung, cố định |
| **Ngựa đàn** | Thanh gỗ **dán** trên mặt đàn, dây buộc vào đó | Truyền rung động; khác họ violin (ngựa đứng, dây vắt qua) |
| **Không có** | Hồn đàn, vĩ | — |

---

## 3. Cơ chế tạo âm: gảy

```
Ngón tay kéo dây lệch sang một bên rồi THẢ
          ↓  lúc thả, dây có hình tam giác (đỉnh ở chỗ gảy)
Dây rung tự do: là tổng của các harmonic, độ mạnh do VỊ TRÍ GẢY quyết định
          ↓  qua ngựa đàn
Mặt đàn + khối khí rung → không khí → tai / micro
          ↓  KHÔNG có gì bơm thêm năng lượng
Âm tắt dần; harmonic cao tắt trước, harmonic thấp tắt sau
```

### Vị trí gảy quyết định harmonic nào mạnh
**Là gì.** Gảy ở các điểm khác nhau trên dây cho ra âm sắc khác nhau, dù cùng nốt.

**Hình dung.** Nếu gảy đúng tại một **điểm nút** của harmonic thứ k (điểm dây đứng yên khi rung theo kiểu thứ k), harmonic đó **không được kích thích**. Ví dụ, giữa dây là nút của h2, h4, h6…, nên gảy ở giữa dây thì mọi harmonic chẵn **biến mất**.

**Công thức** (dây lý tưởng, gảy tại vị trí `p`, tính bằng phần của chiều dài dây kể từ ngựa đàn):
```
biên độ harmonic thứ k  ∝  sin(k · π · p) / k²
```
| Thành phần | Ý nghĩa |
|---|---|
| `sin(k·π·p)` | Bằng 0 khi chỗ gảy trùng nút của harmonic k → harmonic đó mất |
| `1 / k²` | Dây gảy có hình tam giác (có góc nhọn) → harmonic yếu đi nhanh hơn sóng răng cưa của vĩ (1/k) |

**Ví dụ tính** (dB so với h1):

| Gảy ở đâu | h2 | h3 | h4 | h5 | h6 | Nghe thế nào |
|---|---|---|---|---|---|---|
| Sát ngựa đàn (p = 1/10, cách ngựa 65 mm) | −6.5 | −10.7 | −14.3 | −17.8 | −21.4 | Nhiều harmonic cao → **sáng, "kim loại"** (*ponticello*) |
| Chỗ gảy thường, gần lỗ thoát âm (p = 1/5, cách ngựa 130 mm) | −7.9 | −14.9 | −24.1 | **mất** | −31.1 | Cân bằng, ấm |
| Giữa dây, trên phím 12 (p = 1/2) | **mất** | −19.1 | **mất** | −28.0 | **mất** | Chỉ còn harmonic lẻ → **tròn, rỗng, mềm** (*tasto, dolce*) |

So với 1/k của kéo vĩ, 1/k² làm harmonic tụt nhanh gấp đôi (tính theo dB). Đây là một lý do âm guitar **tối** hơn các nhạc cụ kéo vĩ, ngay từ lúc vừa gảy.

---

## 4. Sáu dây và cách lên dây chuẩn

Dây được đánh số **từ dây mảnh nhất**: dây 1 là dây cao nhất, dây 6 là dây trầm nhất.
```
Guitar
 ├── Dây 6 · Mi trầm (lowE)  → E2 → 82.41 Hz
 ├── Dây 5 · La (A)          → A2 → 110.00 Hz
 ├── Dây 4 · Rê (D)          → D3 → 146.83 Hz
 ├── Dây 3 · Sol (G)         → G3 → 196.00 Hz
 ├── Dây 2 · Si (B)          → B3 → 246.94 Hz
 └── Dây 1 · Mi cao (highE)  → E4 → 329.63 Hz
```
- **Quãng tám:** E2, A2 ở quãng tám 2; D3, G3, B3 ở quãng tám 3; E4 ở quãng tám 4.
- **Hai dây cùng tên "Mi"** nhưng cách nhau đúng **2 quãng tám** (82.41 × 4 = 329.63 Hz). Trong dataset, project đặt nhãn **`lowE`** và **`highE`** để phân biệt (Iowa ghi `sulE` và `sul_E`).
- **Khoảng cách giữa các dây không đều:**
```
E2 ──+5 nửa cung (quãng 4, ×1.3348)──→ A2 ──+5──→ D3 ──+5──→ G3 ──+4 (quãng 3 trưởng, ×1.2599)──→ B3 ──+5──→ E4
                                                                 ↑ chỗ duy nhất cách 4 nửa cung
```
- **Vì sao Sol–Si chỉ cách 4?** Tổng 5 + 5 + 5 + 4 + 5 = **24 nửa cung = đúng 2 quãng tám**, nên hai dây Mi trùng tên. Khoảng 4 nửa cung ở giữa cũng giúp các thế bấm hợp âm phổ biến vừa với bàn tay.
- **So với double bass:** 4 dây trầm của guitar (E2 A2 D3 G3) cao hơn đúng **1 quãng tám** so với 4 dây của double bass (E1 A1 D2 G2).

### Guitar cũng là nhạc cụ "chuyển giọng"
Bản nhạc guitar được viết **cao hơn âm thật 1 quãng tám** (như double bass, [08](08_DOUBLE_BASS.md) §4). Dataset dùng **âm thật**: file `guitar_A3_very-long_piano_normal.mp3` đo được F0 = **222.6 Hz**, đúng A3 = 220 Hz.

---

## 5. Phím đàn: bấm phím nào, ra nốt nào

**Phím đàn là gì.** Các thanh kim loại gắn ngang cần đàn. Ấn dây ngay sau một phím, dây chạm vào thanh kim loại, và phần dây rung chỉ còn **từ phím đó tới ngựa đàn**. Mỗi phím làm nốt cao lên **đúng 1 nửa cung**.

**Phím được đặt theo đúng công thức nửa cung** ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §4): phím thứ n cách đầu cần `650 × (1 − 2^(−n/12))` mm.

**Ví dụ trên dây Mi trầm:**
```
Dây Mi trầm buông ...... E2    82.41 Hz      dây rung dài 650 mm
   ↓ phím 1 (cách đầu cần 36.5 mm)
F2 ..................... 87.31 Hz
   ↓ phím 2 (70.9 mm)
F♯2 .................... 92.50 Hz
   ↓ phím 3 (103.4 mm)
G2 ..................... 98.00 Hz      ← bằng dây G buông của cello, dây G buông của double bass
   ↓ phím 4 (134.1 mm)
G♯2 .................... 103.83 Hz
   ↓ phím 5 (163.1 mm)
A2 ..................... 110.00 Hz     ← trùng dây La buông
   ↓ phím 6 (190.4 mm)
A♯2 .................... 116.54 Hz
   ↓ phím 7 (216.2 mm)
B2 ..................... 123.47 Hz
   ↓ … mỗi phím nhân 1.0595 …
   ↓ phím 12 (325 mm, đúng giữa dây)
E3 ..................... 164.81 Hz     ← gấp đôi 82.41: lên 1 quãng tám
   ↓ … tới phím 19 (433.1 mm)
B3 ..................... 246.94 Hz     ← nốt cao nhất trên dây này
```
Các phím **sát nhau dần** khi lên cao: khoảng phím 1–2 rộng 34.4 mm, khoảng phím 18–19 chỉ còn 12.9 mm.

**Bảng đầy đủ: 6 dây × 12 phím đầu** (tên nốt · tần số Hz):

| Phím | Dây 6 · lowE | Dây 5 · A | Dây 4 · D | Dây 3 · G | Dây 2 · B | Dây 1 · highE |
|---|---|---|---|---|---|---|
| **buông (0)** | **E2 · 82.41** | **A2 · 110.00** | **D3 · 146.83** | **G3 · 196.00** | **B3 · 246.94** | **E4 · 329.63** |
| 1 | F2 · 87.31 | A♯2 · 116.54 | D♯3 · 155.56 | G♯3 · 207.65 | C4 · 261.63 | F4 · 349.23 |
| 2 | F♯2 · 92.50 | B2 · 123.47 | E3 · 164.81 | A3 · 220.00 | C♯4 · 277.18 | F♯4 · 369.99 |
| 3 | G2 · 98.00 | C3 · 130.81 | F3 · 174.61 | A♯3 · 233.08 | D4 · 293.66 | G4 · 392.00 |
| 4 | G♯2 · 103.83 | C♯3 · 138.59 | F♯3 · 185.00 | B3 · 246.94 | D♯4 · 311.13 | G♯4 · 415.30 |
| 5 | A2 · 110.00 | D3 · 146.83 | G3 · 196.00 | C4 · 261.63 | E4 · 329.63 | A4 · 440.00 |
| 6 | A♯2 · 116.54 | D♯3 · 155.56 | G♯3 · 207.65 | C♯4 · 277.18 | F4 · 349.23 | A♯4 · 466.16 |
| 7 | B2 · 123.47 | E3 · 164.81 | A3 · 220.00 | D4 · 293.66 | F♯4 · 369.99 | B4 · 493.88 |
| 8 | C3 · 130.81 | F3 · 174.61 | A♯3 · 233.08 | D♯4 · 311.13 | G4 · 392.00 | C5 · 523.25 |
| 9 | C♯3 · 138.59 | F♯3 · 185.00 | B3 · 246.94 | E4 · 329.63 | G♯4 · 415.30 | C♯5 · 554.37 |
| 10 | D3 · 146.83 | G3 · 196.00 | C4 · 261.63 | F4 · 349.23 | A4 · 440.00 | D5 · 587.33 |
| 11 | D♯3 · 155.56 | G♯3 · 207.65 | C♯4 · 277.18 | F♯4 · 369.99 | A♯4 · 466.16 | D♯5 · 622.25 |
| **12 (1 quãng tám)** | **E3 · 164.81** | **A3 · 220.00** | **D4 · 293.66** | **G4 · 392.00** | **B4 · 493.88** | **E5 · 659.26** |

Phím 5 của một dây = dây buông bên cạnh. **Ngoại lệ:** dây Sol thì phím **4** mới bằng dây Si buông (§4).

**Mỗi dây chơi được tới đâu** (bộ Iowa, có ghi dây): nghệ sĩ chơi **mọi dây từ dây buông lên khoảng phím 18–19**:

| Dây | Dây buông | Nốt cao nhất trong dataset Iowa | Số phím |
|---|---|---|---|
| lowE (6) | E2 · 82.41 Hz | B3 · 246.94 Hz | 19 |
| A (5) | A2 · 110.00 Hz | E4 · 329.63 Hz | 19 |
| D (4) | D3 · 146.83 Hz | G♯4 · 415.30 Hz | 18 |
| G (3) | G3 · 196.00 Hz | C♯5 · 554.37 Hz | 18 |
| B (2) | B3 · 246.94 Hz | F♯5 · 739.99 Hz | 19 |
| highE (1) | E4 · 329.63 Hz | B5 · 987.77 Hz | 19 |

---

## 6. Cùng một nốt, nhiều vị trí trên cần đàn

Vì 6 dây cách nhau ít (4–5 nửa cung) mà mỗi dây có 19 phím, **một nốt có thể có tới 5 vị trí**. Nốt **E4 = 329.63 Hz**:
```
Dây 1 (highE) buông   → E4   dây nylon mảnh, buông: sáng, ngân lâu nhất
Dây 2 (B), phím 5     → E4
Dây 3 (G), phím 9     → E4   dây nylon dày hơn: tròn, ấm hơn
Dây 4 (D), phím 14    → E4   dây quấn kim loại: dày, hơi "đục"
Dây 5 (A), phím 19    → E4   phần dây rung rất ngắn: tối, ngân ngắn
```
**Bộ Iowa có thật cả 5 cách**, mỗi cách ở 3 cường độ, ví dụ ở cường độ *mezzo-forte*:
`guitar_E4_mezzo-forte_normal_highE_E4B4.wav` · `…_B_C4B4.wav` · `…_G_C4B4.wav` · `…_D_C4Ab4.wav` · `…_A_C4E4.wav`

Nốt **A2 = 110 Hz** có 2 cách: dây La buông (`guitar_A2_mezzo-forte_normal_A_A2B2.wav`) và dây Mi trầm phím 5 (`guitar_A2_mezzo-forte_normal_lowE_E2B2.wav`).

**Chỉ có trên dây Mi trầm:** 5 nốt **E2 → G♯2** (82.41 → 103.83 Hz).

**Vì sao điều này quan trọng với dataset:** cùng tên nốt, cùng F0, nhưng 5 âm sắc khác nhau. Nếu chỉ thu guitar trên một dây, hệ thống sẽ chỉ biết "một kiểu" tiếng guitar. Đó là lý do tầng **String** trong mô hình dữ liệu ([16](16_DATASET_MODEL.md)) có ý nghĩa, và lý do project sửa lỗi gộp nhãn hai dây Mi (test `test_iowa_string_labels_match_physics`).

---

## 7. Âm vực

- **Thấp nhất: E2 = 82.41 Hz** (dây Mi trầm buông).
- **Cao nhất:** **B5 = 987.77 Hz** (dây Mi cao, phím 19). Đàn có 20 phím thì lên tới C6 = 1 046.50 Hz, như cây đàn Philharmonia. Dùng harmonic thì cao hơn nữa (§8).
- **Trong dataset:** Philharmonia gảy thường **E2 → C6** (38 cao độ), harmonic **E3 → E6** (1 318.51 Hz, 20 cao độ); Iowa **E2 → B5** (44 cao độ).
- **Chồng lấn:** E2 → G4 chung với double bass; E2 → C6 với cello; C3 → C6 với viola; G3 → C6 với violin. Âm vực guitar **không có vùng riêng**: mọi nốt guitar đều có ít nhất một nhạc cụ kéo vĩ chơi được.

---

## 8. Các cách chơi

| Kỹ thuật | Trong dataset? | Người chơi làm gì | Âm thanh đổi ra sao |
|---|---|---|---|
| **Gảy thường** (`normal`) | Philharmonia 71, Iowa 341 | Gảy bằng ngón/móng tay ở gần lỗ thoát âm | Mốc so sánh |
| **Harmonic** (`harmonics`) | Philharmonia 35 | Chạm nhẹ lên dây **ngay trên** phím 12, 7 hoặc 5 rồi gảy và nhấc tay | Chỉ còn harmonic có nút tại đó: phím 12 → h2 (cao 1 quãng tám); phím 7 → h3; phím 5 → h4 (cao 2 quãng tám). Âm trong như chuông |
| Gảy sát ngựa (*ponticello*) | không | Gảy gần ngựa đàn | Sáng, "kim loại" (§3) |
| Gảy trên phím (*tasto*, *dolce*) | không | Gảy gần giữa dây | Tròn, mềm, ít harmonic chẵn (§3) |
| Rung ngón (vibrato) | không | Lắc ngón tay trái dọc dây | Cao độ dao động **rất nhỏ** (phím đàn giữ cao độ) |
| Tắt tiếng bằng lòng bàn tay (*pizzicato*) | không | Đặt cạnh bàn tay phải lên dây gần ngựa đàn | Âm ngắn, đục |
| Quạt chả (*rasgueado*), vê (*tremolo*) | không | Quạt nhiều dây liên tiếp / gảy lặp nhanh một nốt | Nhiều nốt chồng lên nhau |

**Đo được:** harmonic so với gảy thường ở **cùng cao độ** (Philharmonia, 29 cặp): centroid ×0.98 (gần như không đổi), RMS-CV −0.30 (đều hơn), flatness ×2.0. Cả hai kỹ thuật đều là **gảy**, nên CSDL giữ cả hai (họ kỹ thuật `pluck` và `harmonic`).

### 8.1. Cường độ, và một cái bẫy đo đạc
Gảy mạnh hơn → dây lệch xa hơn, góc tam giác nhọn hơn → **nhiều harmonic cao hơn** → sáng hơn. Bộ Philharmonia khớp với điều này: so cặp cùng cao độ, *forte* sáng hơn *piano* **×1.14** (33 cặp).

**Nhưng bộ Iowa cho kết quả ngược lại:** *fortissimo* "tối" hơn *pianissimo* (centroid ×0.78, 116 cặp). Kiểm tra kỹ trên 42 cặp nốt cùng cao độ (*pp* và *ff*):

| Đo trên đoạn nào | *ff* so với *pp* |
|---|---|
| 0.3 s ngay sau lúc gảy | **×1.43**: gảy mạnh **sáng hơn**, đúng vật lý |
| Cả 1.5 s | ×0.99: không còn khác |
| Vùng trên 4 kHz, lúc gảy so với cuối nốt | *ff*: 37.3 dB · *pp*: chỉ **11.5 dB** |

**Giải thích.** Gảy rất nhỏ (*pp*) thì tín hiệu yếu, chỉ cao hơn **tiếng ồn nền** (tiếng xì của micro, phòng) khoảng 11 dB ở vùng tần số cao. Khi nốt tắt dần, vùng cao tần **chìm vào tiếng ồn**. Tiếng ồn có nhiều tần số cao, nên kéo centroid lên. Kết quả là đo trên cả đoạn dài, nốt *pp* trông "sáng" hơn, dù thực ra người chơi gảy nó tối hơn.

**Bài học cho project:** đặc trưng phổ đo trên **phần đuôi đang tắt** của nhạc cụ gảy dễ bị **tiếng ồn nền** làm sai. Đây là một điểm thiết kế cần xử lý ở bước trích đặc trưng (ghi trong [DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md), mục chờ quyết định).

---

## 9. Âm sắc và phổ của guitar

**Mô tả bằng lời:** tròn, ấm, mềm (dây nylon); lúc gảy có tiếng "tách" sáng rất ngắn, sau đó âm tối dần và tắt.

**Đường bao** ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6.3): bật lên trong vài mili-giây rồi tắt dần, khoảng −20 dB sau 1 giây.

**Ví dụ nốt A3 (220 Hz)** (`guitar_A3_very-long_piano_normal`):
```
h1 (220 Hz)    0.0 dB   ← F0 mạnh nhất
h2 (440 Hz)  −13.8 dB
h3 (660 Hz)  −21.5 dB
h4 (880 Hz)  −43.9 dB
h5 (1100 Hz) −37.1 dB
h6 (1320 Hz) −28.2 dB
```
F0 trội hẳn, harmonic yếu đi rất nhanh: phần lớn thời gian nốt vang, guitar **gần như một sóng sin**.

**Phổ theo quãng tám** (trung vị trên 445 nốt guitar dùng được):

| Quãng tám | 2 (82–123 Hz) | 3 (131–247 Hz) | 4 (262–494 Hz) | 5 (523–988 Hz) |
|---|---|---|---|---|
| Centroid | 520 Hz | 652 Hz | 838 Hz | 1 271 Hz |
| Centroid ÷ F0 | 4.8 | **3.3** | 2.3 | 1.9 |

Ở **mọi quãng tám**, tỉ lệ centroid ÷ F0 của guitar **thấp nhất** trong 5 nhạc cụ. Ví dụ quãng tám 3: guitar 3.3; cello 4.9; double bass 5.9; violin 6.0; viola 6.2. Guitar có **ít harmonic mạnh nhất**, vì:
1. Gảy cho harmonic tụt theo 1/k² (§3), nhanh hơn 1/k của kéo vĩ.
2. Dây nylon mềm, tiêu hao năng lượng ở tần số cao rất nhanh.
3. Không có vĩ bơm lại năng lượng: sau tiếng "tách" lúc gảy, chỉ còn vài harmonic thấp.

**Đặc trưng toàn bộ** (trung vị, 445 nốt):

| Đặc trưng | Guitar | Thứ hạng trong 5 nhạc cụ |
|---|---|---|
| Centroid | **781 Hz** | thấp nhất (gần bằng double bass 790 Hz) |
| Rolloff | **1 021 Hz** | thấp nhất |
| ZCR | 0.031 | thấp thứ hai (sau double bass 0.017) |
| **RMS-CV** | **0.88** | **cao nhất**: tắt dần (kéo vĩ: 0.52–0.65) |

**Ảnh hưởng của phòng thu:** centroid của Iowa cao hơn Philharmonia 4.9% ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §8.2), nhỏ.

---

## 10. Đặc trưng nào giúp nhận ra guitar

| Manh mối | Đặc trưng | Mạnh / yếu |
|---|---|---|
| **Tắt dần** (gảy) | **RMS-CV**, MFCC std | **Mạnh nhất**: tách guitar khỏi cả 4 nhạc cụ kéo vĩ |
| Phổ thay đổi theo thời gian (harmonic cao tắt trước) | MFCC std | Mạnh |
| Tối nhất, ít harmonic | centroid, rolloff | Tốt với violin, viola; **yếu với double bass** (781 so với 790 Hz) |
| Âm vực E2 → B5 | median log2 F0 | Yếu: không có vùng riêng (§7) |

**Cặp dễ nhầm:**
- **Guitar ↔ double bass** về **độ sáng** (gần như bằng nhau), tách nhau nhờ **đường bao** và ZCR.
- **Guitar ↔ các nhạc cụ gảy khác:** double bass gảy, violin pizzicato (bị loại khỏi CSDL, D20), banjo, mandolin. Khi người dùng truy vấn bằng tiếng **gảy** của nhạc cụ khác, hệ thống nhiều khả năng trả về guitar, vì trong CSDL **chỉ guitar** là nhạc cụ gảy. Đây là hành vi đúng với thiết kế: hệ thống tìm "âm thanh giống nhất", và trong CSDL thì âm gảy giống nhất là guitar. Xem thử nghiệm với banjo, mandolin ở [10](10_BANJO_MANDOLIN.md).

---

## 11. Guitar trong dataset của project

| | Philharmonia | Iowa MIS |
|---|---|---|
| File gốc | **106 nốt đơn** (đều là nốt dài `very-long`), không có phrase | 45 file aiff (mỗi file một dãy nốt trên một dây) |
| Sau khi xử lý | Dùng được cả 106 | Cắt được **341 nốt** (dự kiến 353, tỉ lệ 97%), 2 nốt quá ngắn |
| Nốt dùng được | **106** (gảy thường 71: E2 → C6; harmonic 35: E3 → E6) | **339** · E2 → B5 · lowE 58, A 59, D 57, G 54, B 57, highE 54 |

**Tổng: 445 nốt guitar dùng được**, ít nhất trong 5 nhạc cụ (các nhạc cụ khác khoảng 1 000). Project chọn 391: REF 150, DB_POOL **181** (thiếu so với mức 200 của các nhạc cụ khác), QUERY_POOL 60.

**Vì sao phải thêm bộ Iowa cho guitar:** Philharmonia chỉ có 106 nốt guitar, dưới mức tối thiểu **360 nốt mỗi nhạc cụ** mà thiết kế yêu cầu (quyết định D21). Bộ Iowa còn mang lại **thông tin dây**: tầng String của guitar trong dataset hoàn toàn đến từ Iowa.
