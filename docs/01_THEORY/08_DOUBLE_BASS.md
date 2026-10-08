# 08. Double bass (contrabass, đại hồ cầm)

> **Đọc xong file này bạn sẽ biết:** double bass thuộc họ nào (và vì sao nó "lai" giữa hai họ); 4 dây với nốt, quãng tám, tần số; vì sao dây cách nhau quãng 4 chứ không phải quãng 5; vì sao ta vẫn nghe ra nốt thấp dù thân đàn gần như không phát ra F0; các cách chơi; phổ, âm sắc, đặc trưng nhận dạng; double bass trong dataset.
> **Cần biết trước:** [04](04_HOW_STRING_INSTRUMENTS_WORK.md), [07 Cello](07_CELLO.md).
> **Đọc tiếp:** [09 Guitar](09_GUITAR.md).

---

## 1. Double bass là gì, thuộc họ nào

```
Nhạc cụ dây → có cần đàn → kéo vĩ (và gảy)
   ├── HỌ VIOLIN: violin · viola · cello
   └── HỌ VIOL (cổ, thế kỷ 15–17) ─── violone ──→ DOUBLE BASS ngày nay (mang nét của cả hai họ)
```
- Double bass là nhạc cụ **lớn nhất và trầm nhất** trong 5 nhạc cụ của project. Trong dàn nhạc nó ngồi cùng nhóm với họ violin và chơi bè **trầm nhất**, thường gấp đôi bè cello thấp hơn 1 quãng tám. Tên "double bass" có nguồn gốc từ việc này.
- **Vì sao nói "lai":** nhiều cây double bass giữ nét của **họ viol**: vai đàn **dốc** (dễ với tay xuống thấp), lưng thường **phẳng**, và lên dây cách nhau **quãng 4** (§4). Nhưng nó có lỗ chữ f, 4 dây và cách kéo vĩ như họ violin.
- **Tư thế:** người chơi **đứng**, hoặc ngồi ghế cao; đàn đứng trên cọc chống.
- **Hai cách chơi chính:** kéo vĩ (*arco*, phổ biến trong nhạc cổ điển) và **gảy** (*pizzicato*, gần như là cách chơi chính trong nhạc jazz, pop).

---

## 2. Cấu tạo

| | Cello | Double bass (cỡ "3/4", phổ biến nhất trong dàn nhạc) |
|---|---|---|
| Chiều cao cả đàn | khoảng 1.2 m | khoảng **1.8 m** (cao hơn nhiều người chơi) |
| Phần dây rung | khoảng 69 cm | khoảng **104–106 cm** |
| Dây | dày | **rất dày và nặng**, lõi thép quấn kim loại |
| Vai đàn | tròn | thường **dốc** (nét của họ viol) |
| Khóa lên dây | chốt gỗ | **bánh răng kim loại** (dây căng tới mức chốt gỗ không giữ nổi) |

Một số cây double bass có **phần nối dài** ở đầu cần (hạ dây E xuống **C1 = 32.70 Hz**) hoặc có **dây thứ 5** (thường là B0 = 30.87 Hz). Bộ Philharmonia có nốt tới C1, nên cây đàn được thu có một trong hai thứ này.

---

## 3. Cơ chế tạo âm và vấn đề "thân đàn quá nhỏ"

Cơ chế kéo vĩ giống cello ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6.1). Khi gảy thì giống guitar ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §6.2), nhưng dây dài và nặng nên **ngân lâu hơn** guitar rất nhiều.

### Vì sao double bass gần như không phát ra F0 ở các nốt thấp nhất
**Hình dung.** Một vật phát âm muốn đẩy không khí hiệu quả ở một tần số thì kích thước của nó phải **không quá nhỏ so với bước sóng** của tần số đó. Bước sóng = tốc độ âm / tần số ([01](01_SOUND_BASICS.md) §3):
```
E1 = 41.20 Hz  →  bước sóng = 343 / 41.2 ≈ 8.3 m
Thân double bass dài khoảng 1.1 m  →  nhỏ hơn bước sóng khoảng 7–8 lần
```
Thân đàn vì thế đẩy không khí **rất kém** ở F0 của các nốt thấp nhất. Nhưng các harmonic h2, h3, h4… (82, 124, 165… Hz) có bước sóng ngắn hơn nên được phát ra tốt hơn nhiều.

**Bằng chứng trong dataset.** Tỉ lệ centroid ÷ F0 (trung vị trên 1 030 nốt double bass dùng được):

| Quãng tám | 1 (33–62 Hz) | 2 (65–123 Hz) | 3 (131–247 Hz) | 4 (262–392 Hz) |
|---|---|---|---|---|
| Centroid | 498 Hz | 611 Hz | 1 043 Hz | 1 166 Hz |
| Centroid ÷ F0 | **9.9** | 6.9 | 5.9 | 3.6 |

Ở quãng tám 1, "trọng tâm" năng lượng nằm quanh **harmonic thứ 10**. Đây là tỉ lệ cao nhất trong 5 nhạc cụ (cello quãng tám thấp nhất: 7.0; violin: 6.0).

### Vậy vì sao ta vẫn nghe ra nốt E1?
Vì **cao độ khớp với F0, không phải với tần số mạnh nhất** ([03](03_F0_HARMONICS_TIMBRE.md) §5). Các harmonic 82.4, 123.6, 164.8, 206.0… Hz cách đều nhau đúng **41.2 Hz**, và não người suy ra nhịp lặp chung đó, tức là nghe ra nốt E1, **kể cả khi gần như không có năng lượng ở 41.2 Hz**. Hiện tượng này gọi là **"F0 vắng mặt"** (missing fundamental).

**Hệ quả cho project:**
- Thuật toán đo F0 (pYIN) cũng phải "suy ra" F0 từ nhịp lặp của dạng sóng, không tìm đỉnh phổ mạnh nhất. Nếu tìm đỉnh mạnh nhất, nó sẽ báo nhầm lên 1–2 quãng tám. Khi cắt nốt Iowa, project đã gặp đúng lỗi này và phải cho phép lệch **đúng 12 hoặc 24 nửa cung** ([17](17_ONSET_SEGMENTATION.md)).
- Bộ lọc thông cao 25 Hz (D27), dùng để bỏ tiếng ù hạ âm, chỉ làm nốt thấp nhất C1 = 32.70 Hz yếu đi khoảng 1 dB, nên không làm mất nốt.

---

## 4. Bốn dây và cách lên dây chuẩn

```
Double bass
 ├── Dây E (Mi, dày nhất)  → E1 → 41.20 Hz      ← nốt thấp nhất của 5 nhạc cụ (không tính phần nối dài)
 ├── Dây A (La)            → A1 → 55.00 Hz
 ├── Dây D (Rê)            → D2 → 73.42 Hz
 └── Dây G (Sol, mảnh nhất) → G2 → 98.00 Hz
```
- **Quãng tám:** E1, A1 thuộc quãng tám 1; D2, G2 thuộc quãng tám 2.
- **Cách nhau quãng 4 = 5 nửa cung = nhân 1.3348** (không phải quãng 5 như họ violin):
```
E1  41.20 Hz × 1.3348 = 55.00 Hz (A1)
A1  55.00 Hz × 1.3348 = 73.42 Hz (D2)
D2  73.42 Hz × 1.3348 = 98.00 Hz (G2)
```
- **Vì sao quãng 4?** Dây quá dài nên mỗi nửa cung cách nhau rất xa (§5). Nếu lên dây quãng 5 (7 nửa cung giữa hai dây), bàn tay phải dời chỗ liên tục để đi hết khoảng giữa hai dây. Quãng 4 (5 nửa cung) giảm bớt quãng đường đó.
- **Giống 4 dây trầm của guitar** (E2-A2-D3-G3), nhưng **thấp hơn đúng 1 quãng tám**.

### Double bass là nhạc cụ "chuyển giọng"
Bản nhạc cho double bass được **viết cao hơn âm thật 1 quãng tám**, để nốt nằm gọn trong khuông nhạc. Ví dụ, người chơi đọc nốt "E2" nhưng âm phát ra là **E1** (41.20 Hz). Guitar cũng vậy ([09](09_GUITAR.md)).

**Trong dataset:** tên file dùng **âm thật**, không phải nốt viết. Kiểm chứng: file `double-bass_A3_15_forte_arco-normal.mp3` đo được F0 = **221.4 Hz**, đúng A3 = 220 Hz. Nếu tên file dùng nốt viết thì F0 phải là 110 Hz.

---

## 5. Bấm dây: từ dây buông lên từng nửa cung

**Ví dụ trên dây E** (dây rung dài khoảng 1 050 mm):
```
Dây E buông ........ E1    41.20 Hz     dây rung dài 1 050 mm
   ↓ +1 nửa cung (ngón tay cách đầu cần 58.9 mm)
F1 ................. 43.65 Hz
   ↓ +2 (114.6 mm)
F♯1 ................ 46.25 Hz
   ↓ +3 (167.1 mm)
G1 ................. 49.00 Hz
   ↓ +4 (216.6 mm)
G♯1 ................ 51.91 Hz
   ↓ +5 (263.4 mm)
A1 ................. 55.00 Hz     ← trùng dây A buông (quãng 4)
   ↓ … mỗi bước nhân 1.0595 …
   ↓ +12 (525 mm, giữa dây)
E2 ................. 82.41 Hz     ← gấp đôi 41.20; bằng dây Mi trầm của guitar
```
**Mỗi nửa cung cách nhau khoảng 59 mm**, gấp hơn 3 lần violin (18 mm). Bàn tay chỉ phủ được khoảng **2 nửa cung** ở vùng thấp (người chơi dùng ngón 1, 2 và 4 cho 3 nửa cung liên tiếp). Đây là lý do cần lên dây quãng 4 (§4).

**Bảng đầy đủ** (tên nốt · tần số Hz):

| Bấm thêm | Dây E | Dây A | Dây D | Dây G |
|---|---|---|---|---|
| **dây buông (0)** | **E1 · 41.20** | **A1 · 55.00** | **D2 · 73.42** | **G2 · 98.00** |
| +1 | F1 · 43.65 | A♯1 · 58.27 | D♯2 · 77.78 | G♯2 · 103.83 |
| +2 | F♯1 · 46.25 | B1 · 61.74 | E2 · 82.41 | A2 · 110.00 |
| +3 | G1 · 49.00 | C2 · 65.41 | F2 · 87.31 | A♯2 · 116.54 |
| +4 | G♯1 · 51.91 | C♯2 · 69.30 | F♯2 · 92.50 | B2 · 123.47 |
| +5 | A1 · 55.00 | D2 · 73.42 | G2 · 98.00 | C3 · 130.81 |
| +6 | A♯1 · 58.27 | D♯2 · 77.78 | G♯2 · 103.83 | C♯3 · 138.59 |
| +7 | B1 · 61.74 | E2 · 82.41 | A2 · 110.00 | D3 · 146.83 |
| +8 | C2 · 65.41 | F2 · 87.31 | A♯2 · 116.54 | D♯3 · 155.56 |
| +9 | C♯2 · 69.30 | F♯2 · 92.50 | B2 · 123.47 | E3 · 164.81 |
| +10 | D2 · 73.42 | G2 · 98.00 | C3 · 130.81 | F3 · 174.61 |
| +11 | D♯2 · 77.78 | G♯2 · 103.83 | C♯3 · 138.59 | F♯3 · 185.00 |
| **+12 (1 quãng tám)** | **E2 · 82.41** | **A2 · 110.00** | **D3 · 146.83** | **G3 · 196.00** |

Với double bass, hàng **+5** của một dây trùng hàng 0 của dây bên phải (quãng 4). Ở violin, viola, cello là hàng +7 (quãng 5).

**Mỗi dây chơi được tới đâu** (bộ Iowa, có ghi dây):

| Dây | Dây buông | Nốt cao nhất trong dataset Iowa | Số nửa cung |
|---|---|---|---|
| E | E1 · 41.20 Hz | D3 · 146.83 Hz | 22 |
| A | A1 · 55.00 Hz | A3 · 220.00 Hz | 24 |
| D | D2 · 73.42 Hz | D4 · 293.66 Hz | 24 |
| G | G2 · 98.00 Hz | G4 · 392.00 Hz | 24 |

---

## 6. Một nốt trên nhiều dây

- **G2 = 98 Hz** có 4 cách: dây G buông · dây D +5 · dây A +10 · dây E +15.
- **Chỉ có trên dây E:** 5 nốt **E1 → G♯1** (41.20 → 51.91 Hz).
- Vì dây cách nhau ít (5 nửa cung), **rất nhiều nốt** của double bass chơi được trên 3–4 dây.

---

## 7. Âm vực

- **Thấp nhất: E1 = 41.20 Hz** (đàn 4 dây chuẩn); C1 = 32.70 Hz nếu có phần nối dài.
- **Cao nhất:** nhạc giao hưởng thường viết tới khoảng **G4 = 392 Hz**; nghệ sĩ độc tấu dùng harmonic để lên cao hơn nhiều.
- **Trong dataset:** Philharmonia **C1 → G4** (32.70 → 392.00 Hz, 44 cao độ); Iowa **E1 → G4** (41.20 → 392.00 Hz, 40 cao độ).
- **Chồng lấn:** C2 → G4 chung với cello; E2 → G4 chung với guitar; C3 → G4 với viola; G3 → G4 với violin. Vùng **C1 → B1** (32.7 → 61.7 Hz) **chỉ double bass có**.

---

## 8. Các cách chơi

| Kỹ thuật (tên trong dataset) · số nốt | Người chơi làm gì | Âm thanh đổi ra sao |
|---|---|---|
| **Arco thường** · 756 | Kéo vĩ. Có hai kiểu cầm vĩ: kiểu Pháp (úp tay, như cello) và kiểu Đức (nắm tay, như cầm cưa) | Âm giữ đều, nhiều harmonic, có tiếng vĩ "rè" rõ ở dây thấp |
| **Pizzicato** · 12 | Gảy bằng mặt ngón tay | Bật rồi ngân dài, âm tròn, ấm (cách chơi chính trong jazz) |
| **Col legno battuto** · 10 | Gõ dây bằng gỗ vĩ | Tiếng gõ ngắn, cao độ mờ |

CSDL chỉ giữ **arco** (D20). Pizzicato bị loại tuy rất phổ biến ngoài đời. Lý do: cả bộ dữ liệu chỉ có 12 nốt gảy, quá ít để làm một "nhóm" riêng, mà trộn vào arco thì làm phân tán đặc trưng của double bass. Hệ quả: **truy vấn bằng tiếng double bass gảy (jazz) có thể bị nhận nhầm sang guitar**, vì cùng là gảy. Đây là một giới hạn cần ghi trong báo cáo.

**Cường độ.** Philharmonia có 7 mức, thêm `molto-pianissimo` (cực nhỏ). So cặp cùng cao độ, cùng độ dài nốt, nốt to sáng hơn nốt nhỏ: centroid ×1.10 (Philharmonia, 264 cặp), ×1.06 (Iowa, 97 cặp).

---

## 9. Âm sắc và phổ của double bass

**Mô tả bằng lời:** sâu, dày, "rền"; ở dây thấp có tiếng vĩ rè rõ; vùng cao (dây G bấm cao) căng và hơi gắt.

**Ví dụ nốt A3 (220 Hz) — vùng cao của double bass** (`double-bass_A3_15_forte_arco-normal`; Philharmonia không ghi dây, nhiều khả năng là dây G bấm lên 14 nửa cung):
```
h1 (220 Hz)   −0.5 dB
h2 (440 Hz)    0.0 dB   ← mạnh nhất
h3 (660 Hz)  −16.4 dB
h4 (880 Hz)   −1.1 dB   ← gần bằng h2
h5 (1100 Hz) −17.6 dB
h6 (1320 Hz) −20.7 dB
h7 (1540 Hz) −14.1 dB   … h8, h9, h10 vẫn chỉ yếu hơn khoảng 18–19 dB
```
**Rất nhiều harmonic mạnh**: âm căng, "gắt". A3 nằm gần đỉnh âm vực double bass. Để chơi nốt này phải bấm rất cao, phần dây rung ngắn mà dây lại rất dày, cộng thêm kéo vĩ mạnh, nên sinh nhiều harmonic. Ở cùng nốt A3, double bass sáng hơn cả cello (centroid 1 217 so với 1 042 Hz, [03](03_F0_HARMONICS_TIMBRE.md) §6). Điều này trái với trực giác "nhạc cụ to thì tối hơn".

**Đặc trưng toàn bộ** (trung vị, 1 030 nốt): centroid **790 Hz** · rolloff 1 289 Hz · ZCR **0.017** (thấp nhất trong 5 nhạc cụ) · RMS-CV 0.59 · bandwidth 1 484 Hz.

**ZCR thấp nhất**: dạng sóng dao động chậm (F0 thấp), nên đổi dấu ít lần mỗi giây. ZCR ([15](15_AUDIO_FEATURES.md)) là manh mối mạnh để nhận ra double bass.

**Cẩn thận với RMS-CV của double bass.** Trung vị ở Philharmonia là 0.69 nhưng ở Iowa chỉ 0.26. Nguyên nhân chủ yếu là **độ dài nốt khi thu**, không phải nhạc cụ: Philharmonia có nhiều nốt ngắn 0.25–1 s (RMS-CV 0.69–0.79), còn nốt 1.5 s chỉ 0.43; Iowa thu nốt dài. RMS-CV đo "năng lượng dao động bao nhiêu trong cửa sổ phân tích", nên nốt ngắn (kết thúc sớm trong cửa sổ) cho RMS-CV cao. Chi tiết và hệ quả cho thiết kế: [15](15_AUDIO_FEATURES.md).

---

## 10. Đặc trưng nào giúp nhận ra double bass

| Manh mối | Đặc trưng | Mạnh / yếu |
|---|---|---|
| Nốt **dưới C2** (65.41 Hz) chỉ double bass có | median log2 F0 | **Rất mạnh**: khoảng 1/5 số nốt double bass trong dataset (quãng tám 1: 200 / 1 030) nằm ở đó |
| Dạng sóng dao động chậm | **ZCR** thấp nhất | Mạnh, nhưng ZCR bị phòng thu ảnh hưởng |
| Năng lượng dồn lên harmonic cao (F0 yếu) | MFCC mean, tỉ lệ centroid/F0 (gián tiếp) | Phân biệt với cello ở cùng nốt |
| Kéo vĩ: âm giữ đều | RMS-CV | Tách khỏi guitar, nhưng **phụ thuộc độ dài nốt** (§9) |

**Cặp dễ nhầm:**
- **Double bass ↔ cello** (chung C2 → G4): cùng kéo vĩ, độ sáng ở cùng nốt lúc cao lúc thấp hơn nhau.
- **Double bass ↔ guitar** (chung E2 → G4): centroid trung vị gần như bằng nhau (790 so với 781 Hz)! Tách nhau chủ yếu nhờ **đường bao** (kéo vĩ giữ đều, gảy tắt dần) và ZCR.

---

## 11. Double bass trong dataset của project

| | Philharmonia | Iowa MIS |
|---|---|---|
| File gốc | 852 file = **778 nốt đơn** + 74 đoạn phrase | 35 file aiff (mỗi file một dãy nốt trên một dây) |
| Sau khi xử lý | 5 nốt quá ngắn; 22 nốt kỹ thuật khác arco (12 pizz, 10 col legno; để riêng) | Cắt được **279 nốt** (dự kiến 286, tỉ lệ 98%, cao nhất trong 5 nhạc cụ), không nốt nào quá ngắn |
| Nốt dùng được | **751** (toàn bộ arco thường) · C1 → G4 | **279** · E1 → G4 · dây E 66, A 74, D 73, G 66 |

**Tổng: 1 030 nốt double bass dùng được**; project chọn 410 (REF 150, DB_POOL 200, QUERY_POOL 60).

Iowa cắt double bass tốt nhất vì nốt ngân dài và đều, tách rõ từng nốt. Khó khăn duy nhất là pYIN hay báo **cao hơn 1 quãng tám** ở các nốt thấp, do F0 yếu (§3). Thuật toán cắt đã tính tới lỗi này.
