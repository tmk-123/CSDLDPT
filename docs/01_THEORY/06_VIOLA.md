# 06. Viola (vĩ cầm trầm, alto)

> **Đọc xong file này bạn sẽ biết:** viola khác violin ở đâu (kích thước, dây C, âm sắc); 4 dây với nốt, quãng tám, tần số; bấm dây làm nốt đổi ra sao; vì sao viola "quá nhỏ so với âm vực của nó" và điều đó làm âm sắc khác thế nào; các cách chơi; phổ, đặc trưng nhận dạng; viola trong dataset.
> **Cần biết trước:** [05 Violin](05_VIOLIN.md). Viola giống violin ở rất nhiều điểm, nên file này tập trung vào **chỗ khác nhau**.
> **Đọc tiếp:** [07 Cello](07_CELLO.md).

---

## 1. Viola là gì, thuộc họ nào

```
Nhạc cụ dây → có cần đàn → kéo vĩ → HỌ VIOLIN:  violin · VIOLA · cello
```
- Viola là thành viên **thứ hai** của họ violin, giữ **bè giữa** (giọng alto) trong dàn nhạc: thấp hơn violin, cao hơn cello.
- **Cầm giống violin:** kẹp giữa cằm và vai trái. Điều này giới hạn kích thước của viola (§3).
- Người mới thường nhầm viola với violin vì hai đàn trông gần như giống hệt nhau. Cách nhận nhanh: viola **to hơn một chút**, và dây trầm nhất là dây **C** chứ không phải G.

---

## 2. Cấu tạo — giống violin, chỉ to hơn

Các bộ phận giống hệt violin ([05](05_VIOLIN.md) §2): thân gỗ, 4 dây, bàn phím không có phím, ngựa đàn, hồn đàn, thanh đỡ trầm, 2 lỗ chữ f, cây vĩ. Khác biệt:

| | Violin | Viola |
|---|---|---|
| Chiều dài thân | khoảng 35.5 cm (gần như chuẩn hóa) | khoảng **38–43 cm** (không có cỡ chuẩn, tùy người chơi) |
| Phần dây rung | khoảng 32.8 cm | khoảng **37 cm** |
| Dây | mảnh hơn | **dày hơn** (để rung chậm hơn, xem [04](04_HOW_STRING_INSTRUMENTS_WORK.md) §3) |
| Cây vĩ | khoảng 75 cm, nhẹ hơn | ngắn hơn chút, **nặng hơn** |

---

## 3. Cơ chế tạo âm — và chuyện "viola quá nhỏ"

Cơ chế giống violin: kéo vĩ (dính – trượt) → sóng răng cưa giàu harmonic → ngựa đàn → thân đàn cộng hưởng ([05](05_VIOLIN.md) §3).

**Điều đặc biệt: thân viola "quá nhỏ" so với âm vực của nó.**
- Viola lên dây thấp hơn violin **một quãng 5** (tần số chia 1.5).
- Nếu muốn viola cộng hưởng "giống violin, chỉ thấp hơn 1 quãng 5", thì mọi kích thước phải **lớn hơn 1.5 lần**. Thân đàn sẽ dài khoảng 35.5 × 1.5 ≈ **53 cm**, quá to để kẹp dưới cằm.
- Viola thật chỉ dài khoảng 40 cm, nên là một **thỏa hiệp**: các cộng hưởng của thân nằm **cao hơn** so với các nốt viola chơi. Cộng hưởng khí của viola ở khoảng **230 Hz** (violin khoảng 270–290 Hz).

**Hệ quả lên âm thanh:**
- Các nốt **dây C** (131–185 Hz) nằm dưới cộng hưởng khí, nên F0 được khuếch đại ít. Âm dây C "đặc, hơi khàn", không vang mạnh như cello cùng nốt.
- Toàn bộ âm sắc viola **tối và "che" hơn** violin, đôi khi được tả là hơi "giọng mũi". Đây chính là âm sắc riêng mà người nghe nhận ra là viola.

**Bằng chứng trong dataset:** cùng nốt A3 (220 Hz), nằm ngay cạnh cộng hưởng khí 230 Hz của viola, harmonic h1 của viola **mạnh nhất** (0 dB). Với violin, cộng hưởng khí ở 270–290 Hz cách xa 220 Hz, nên h1 yếu hơn h2 tới 19.4 dB (§9).

---

## 4. Bốn dây và cách lên dây chuẩn

```
Viola
 ├── Dây C (Đô, dày nhất)  → C3 → 130.81 Hz      ← dây riêng của viola (violin không có)
 ├── Dây G (Sol)           → G3 → 196.00 Hz      ← giống dây G violin
 ├── Dây D (Rê)            → D4 → 293.66 Hz      ← giống dây D violin
 └── Dây A (La, mảnh nhất) → A4 → 440.00 Hz      ← giống dây A violin
```
- **Quãng tám:** C3 và G3 thuộc quãng tám 3 (dưới C4 = 261.63 Hz); D4 và A4 thuộc quãng tám 4.
- **Cách nhau quãng 5** (nhân 1.4983), như violin: 130.81 × 1.4983 = 196.00 → × 1.4983 = 293.66 → × 1.4983 = 440.00.
- **So với violin:** viola = violin **bỏ dây E, thêm dây C** ở dưới. Ba dây G, D, A **cùng nốt, cùng tần số** với violin. Vì vậy khi hai đàn chơi cùng nốt trên cùng dây buông (ví dụ A4), **chỉ còn âm sắc** để phân biệt.

---

## 5. Bấm dây: từ dây buông lên từng nửa cung

**Ví dụ trên dây C**, dây riêng của viola:
```
Dây C buông ....... C3    130.81 Hz
   ↓ +1 nửa cung
C♯3 ............... 138.59 Hz
   ↓ +1
D3 ................ 146.83 Hz
   ↓ +1
D♯3 ............... 155.56 Hz
   ↓ +1
E3 ................ 164.81 Hz
   ↓ +1
F3 ................ 174.61 Hz
   ↓ +1
F♯3 ............... 185.00 Hz
   ↓ +1
G3 ................ 196.00 Hz   ← +7: trùng dây G buông
   ↓ … mỗi bước nhân 1.0595 …
   ↓ +12 (bấm giữa dây)
C4 ................ 261.63 Hz   ← gấp đôi 130.81: lên 1 quãng tám
```

**Bảng đầy đủ** (tên nốt · tần số Hz):

| Bấm thêm | Dây C | Dây G | Dây D | Dây A |
|---|---|---|---|---|
| **dây buông (0)** | **C3 · 130.81** | **G3 · 196.00** | **D4 · 293.66** | **A4 · 440.00** |
| +1 | C♯3 · 138.59 | G♯3 · 207.65 | D♯4 · 311.13 | A♯4 · 466.16 |
| +2 | D3 · 146.83 | A3 · 220.00 | E4 · 329.63 | B4 · 493.88 |
| +3 | D♯3 · 155.56 | A♯3 · 233.08 | F4 · 349.23 | C5 · 523.25 |
| +4 | E3 · 164.81 | B3 · 246.94 | F♯4 · 369.99 | C♯5 · 554.37 |
| +5 | F3 · 174.61 | C4 · 261.63 | G4 · 392.00 | D5 · 587.33 |
| +6 | F♯3 · 185.00 | C♯4 · 277.18 | G♯4 · 415.30 | D♯5 · 622.25 |
| +7 | G3 · 196.00 | D4 · 293.66 | A4 · 440.00 | E5 · 659.26 |
| +8 | G♯3 · 207.65 | D♯4 · 311.13 | A♯4 · 466.16 | F5 · 698.46 |
| +9 | A3 · 220.00 | E4 · 329.63 | B4 · 493.88 | F♯5 · 739.99 |
| +10 | A♯3 · 233.08 | F4 · 349.23 | C5 · 523.25 | G5 · 783.99 |
| +11 | B3 · 246.94 | F♯4 · 369.99 | C♯5 · 554.37 | G♯5 · 830.61 |
| **+12 (1 quãng tám)** | **C4 · 261.63** | **G4 · 392.00** | **D5 · 587.33** | **A5 · 880.00** |

Ba cột G, D, A **giống hệt** ba cột đầu của bảng violin ([05](05_VIOLIN.md) §5).

**Mỗi dây chơi được tới đâu** (bộ Iowa, có ghi dây):

| Dây | Dây buông | Nốt cao nhất trong dataset Iowa | Số nửa cung |
|---|---|---|---|
| C | C3 · 130.81 Hz | C5 · 523.25 Hz | 24 |
| G | G3 · 196.00 Hz | G♯5 · 830.61 Hz | 25 |
| D | D4 · 293.66 Hz | D♯6 · 1 244.51 Hz | 25 |
| A | A4 · 440.00 Hz | A6 · 1 760.00 Hz | 24 |

---

## 6. Một nốt trên nhiều dây

- **A4 = 440 Hz** có tới 4 cách: dây A buông · dây D +7 · dây G +14 · dây C +21.
- **Nốt chỉ có trên dây C:** 7 nốt **C3 → F♯3** (130.81 → 185.00 Hz). Các nốt này **violin không chơi được** (violin thấp nhất là G3). Trong bài toán phân biệt violin ↔ viola, một nốt dưới G3 là manh mối chắc chắn rằng **không phải violin**.
- Dây C có âm sắc rất riêng: dày, tối, hơi "khàn". Nhiều nhà soạn nhạc dùng dây C để tạo màu u buồn.

---

## 7. Âm vực

- **Thấp nhất: C3 = 130.81 Hz** (dây C buông).
- **Cao nhất:** nhạc giao hưởng thường viết tới khoảng **E6 = 1 318.51 Hz**, có thể cao hơn.
- **Trong dataset:** Philharmonia **C3 → D7** (130.81 → 2 349.32 Hz, 51 cao độ). Iowa **C3 → A6** (130.81 → 1 760.00 Hz, 46 cao độ).
- **Chồng lấn:** gần như **toàn bộ** âm vực viola trùng với nhạc cụ khác. G3 → A6 chung với violin; C3 → C6 chung với cello; C3 → B5 chung với guitar; C3 → G4 chung với double bass.

---

## 8. Các cách chơi

Viola dùng **cùng bộ kỹ thuật** với violin ([05](05_VIOLIN.md) §8): arco, vibrato, pizzicato, ponticello, tasto, con sordino, harmonic… Các kỹ thuật có trong dataset (nốt đơn Philharmonia):

| Kỹ thuật · số nốt | Người chơi làm gì | Âm thanh đổi ra sao | Đo được (so cặp cùng nốt, cùng độ dài) |
|---|---|---|---|
| Arco thường · 708 | Kéo vĩ bình thường | Mốc so sánh | — |
| Vibrato mạnh · 21 | Rung ngón tay mạnh | Cao độ dao động, phổ "quét" theo thời gian | centroid ×1.12 · RMS-CV −0.21 |
| Không vibrato · 21 | Ngón tay đứng yên | Âm phẳng, đứng | centroid ×0.95 · RMS-CV −0.18 |
| Pizzicato · 39 | Gảy | Bật rồi tắt dần | chưa đo riêng cho viola (với violin: centroid ×0.68, RMS-CV +0.59) |
| Snap pizz · 11 | Gảy cho dây đập bàn phím | Thêm tiếng "tách" | chưa đo riêng |
| Láy (trill) `arco-major-trill` · 20, `arco-minor-trill` · 21 | Đổi rất nhanh qua lại giữa nốt chính và nốt cao hơn 2 nửa cung (*major*) hoặc 1 nửa cung (*minor*) | Cao độ **nhảy liên tục** giữa 2 nốt → F0 không đứng yên | chưa đo riêng (với cello: centroid ×1.2, flatness ×3) |
| Vuốt (glissando) `arco-glissando` · 20 | Trượt ngón tay khi đang kéo vĩ | Cao độ **trượt liên tục** | chưa đo riêng |
| Harmonic tự nhiên · 20, nhân tạo · 30 | Chạm nhẹ vào điểm nút | Âm trong, gần sóng sin | chưa đo riêng (với violin: centroid ×0.79–0.91) |
| Glissando gảy · 8 | Gảy rồi trượt | Cao độ trượt, tắt dần | chưa đo riêng |

*"Chưa đo riêng":* các nốt này bị loại khỏi CSDL theo D20 (chỉ giữ arco), và bước đo cho tài liệu lý thuyết chỉ đo kỹ thuật bị loại của violin và cello. Hiệu ứng **vật lý** giống violin, nên số đo của violin là ước lượng hợp lý.

**Láy và vuốt là hai kỹ thuật làm F0 không còn là "một số".** Với cả hai, cao độ thay đổi trong lúc nốt đang vang. Đặc trưng "median log2 F0" của project chỉ lấy **trung vị**, nên với nốt láy nó cho ra nốt chính hoặc nốt láy, còn với nốt vuốt nó cho ra một nốt ở giữa. Đây là một lý do nữa để CSDL chỉ giữ nốt arco ổn định.

**Cường độ:** so cặp cùng cao độ, cùng độ dài nốt, nốt to sáng hơn nốt nhỏ: centroid ×1.10 (Philharmonia, 256 cặp), ×1.02 (Iowa, 84 cặp).

---

## 9. Âm sắc và phổ của viola

**Mô tả bằng lời:** ấm, tối và "che" hơn violin, đôi khi hơi khàn hoặc "giọng mũi"; dây C dày và u buồn.

**Ví dụ nốt A3 (220 Hz)** (`viola_A3_1_forte_arco-normal`; dB so với harmonic mạnh nhất):
```
h1 (220 Hz)    0.0 dB   ← F0 MẠNH NHẤT (khác hẳn violin: −19.4 dB)
h2 (440 Hz)   −7.8 dB
h3 (660 Hz)   −7.3 dB
h4 (880 Hz)  −10.6 dB
h5 (1100 Hz) −29.9 dB   ← tụt mạnh từ h5
h6 (1320 Hz) −32.8 dB
```
Bốn harmonic đầu đều mạnh, sau đó tụt hẳn: âm **đầy ở vùng thấp, ít "chói"**. So với violin cùng nốt, năng lượng dồn về các harmonic thấp, nên viola **tối hơn**.

**Phổ theo quãng tám** (trung vị trên 990 nốt viola dùng được), đặt cạnh violin:

| Quãng tám | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| Centroid viola | 1 093 Hz | **1 527 Hz** | 1 963 Hz | 2 381 Hz | 2 520 Hz |
| Centroid violin | 1 250 Hz | **1 526 Hz** | 2 314 Hz | 2 931 Hz | 3 269 Hz |
| Viola ÷ violin | 0.87 | **1.00** | 0.85 | 0.81 | 0.77 |
| Centroid ÷ F0 (viola) | 6.2 | 4.1 | 2.8 | 1.7 | 1.2 |

Hai điều đáng chú ý:
1. Ở **quãng tám 4**, trung vị centroid của viola và violin **bằng nhau** (1 527 so với 1 526 Hz). Đây chính là vùng hai nhạc cụ chơi nhiều nhất (dây D, dây A). Một đặc trưng "độ sáng" đơn lẻ **không phân biệt được** hai nhạc cụ ở vùng này.
2. Ở các quãng tám khác, viola tối hơn violin 13–23%. Khoảng cách tăng ở vùng cao: vùng cao của viola gần giới hạn trên của nó, nên dây và thân phải "gắng" hơn violin.

**Đặc trưng toàn bộ** (trung vị, 990 nốt): centroid **1 712 Hz** · rolloff 2 934 Hz · ZCR 0.089 · RMS-CV 0.52. Centroid, rolloff và ZCR đều nằm **giữa violin và cello**, đúng với vị trí "giọng giữa" của viola. RMS-CV thì thấp nhất trong 5 nhạc cụ (âm giữ đều nhất), nhưng chênh lệch với violin (0.65) và cello (0.55) nhỏ.

**Ảnh hưởng của phòng thu:** centroid của bản thu Iowa chỉ cao hơn Philharmonia **1.1%**, ít nhất trong 5 nhạc cụ ([04](04_HOW_STRING_INSTRUMENTS_WORK.md) §8.2).

---

## 10. Đặc trưng nào giúp nhận ra viola

| Manh mối | Đặc trưng | Mạnh / yếu |
|---|---|---|
| Nốt **dưới G3** (dây C) → không phải violin | median log2 F0 | Chắc chắn với violin, nhưng chỉ 125 trong 990 nốt viola dùng được (13%) nằm ở đó |
| Tối hơn violin, sáng hơn cello | centroid, rolloff | **Yếu ở quãng tám 4** (bằng violin) |
| Hình phổ "4 harmonic đầu mạnh rồi tụt" | **MFCC mean** | Manh mối chính: MFCC tả **hình dạng** phổ, không chỉ "trọng tâm" |
| Kéo vĩ, âm giữ đều | RMS-CV, MFCC std | Tách khỏi guitar, không tách khỏi violin, cello |

**Kết luận cho project:** viola là nhạc cụ **khó nhận nhất** trong 5 nhạc cụ, vì nó nằm giữa violin và cello về mọi mặt. Khi đánh giá kết quả tìm kiếm, cần xem riêng **độ nhầm viola ↔ violin** và **viola ↔ cello**, không chỉ độ chính xác chung.

---

## 11. Viola trong dataset của project

| | Philharmonia | Iowa MIS |
|---|---|---|
| File gốc | 974 file = **919 nốt đơn** + 55 đoạn phrase | 32 file aiff (mỗi file một dãy nốt trên **một dây**) |
| Sau khi xử lý | 21 nốt quá ngắn; 168 nốt kỹ thuật khác arco (để riêng); **1 file hỏng** (`viola_D6_05_piano_arco-normal.mp3`, không giải mã được); **1 file trùng** (§11.1) | Cắt được **267 nốt** (dự kiến 292), 5 nốt quá ngắn |
| Nốt dùng được | **728** (arco thường 686, vibrato mạnh 21, không vibrato 21) · C3 → D7 | **262** · C3 → A6 · dây C 65, G 69, D 66, A 62 |

**Tổng: 990 nốt viola dùng được**; project chọn 410 (REF 150, DB_POOL 200, QUERY_POOL 60).

### 11.1. Một bài học về chất lượng nguồn dữ liệu
File `viola_G6_05_fortissimo_arco-normal.mp3` có nội dung **giống hệt từng byte** (cùng mã MD5) với file `cello_Ds5_05_forte_arco-normal.mp3`: **cùng một bản thu mà mang nhãn hai nhạc cụ khác nhau, và hai nốt khác nhau** (G6 = 1 568 Hz so với D♯5 = 622 Hz). Không biết nhãn nào đúng, nên project loại **cả hai** (status DUPLICATE). Bài học: **nhãn trong dataset công khai cũng có thể sai**. Đó là lý do bước lọc dữ liệu kiểm tra MD5 thay vì tin tên file ([16](16_DATASET_MODEL.md) §6). Cặp trùng thứ hai: [07](07_CELLO.md) §11.1.
