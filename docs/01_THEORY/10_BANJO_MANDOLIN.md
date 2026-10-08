# 10. Banjo và mandolin — hai nhạc cụ gảy **ngoài** CSDL

> **Đọc xong file này bạn sẽ biết:** vì sao project giữ hai nhạc cụ không có trong CSDL; banjo và mandolin cấu tạo, lên dây, phát âm ra sao; vì sao banjo "tắt nhanh" nhất và mandolin vê (tremolo) lại giống nhạc cụ kéo vĩ; dự đoán hệ thống sẽ trả lời gì khi truy vấn bằng hai nhạc cụ này.
> **Cần biết trước:** [09 Guitar](09_GUITAR.md).
> **Đọc tiếp:** [11 Cách chơi](11_PLAYING_TECHNIQUES.md).

---

## 1. Vì sao có hai nhạc cụ "thừa"?

CSDL của project chỉ chứa 5 nhạc cụ. Nhưng ngoài đời, người dùng có thể gửi tiếng của **một nhạc cụ khác**. Hệ thống tìm kiếm theo nội dung **luôn trả về k kết quả gần nhất**, dù không có kết quả nào thật sự "đúng". Câu hỏi cần kiểm tra là: **khi đó hệ thống trả về gì, và có hợp lý không?**

Banjo và mandolin rất hợp cho việc này:
- Cùng là **nhạc cụ dây** (cùng "thế giới" âm thanh với CSDL), nhưng **không có** trong CSDL.
- Cùng là nhạc cụ **gảy** như guitar, nhưng âm sắc khác guitar rõ rệt.
- Có sẵn trong bộ Philharmonia, cùng điều kiện thu với phần lớn CSDL.

Trong dataset, cả hai được gắn tập **UNSEEN** và để riêng ở `data/queries/unseen/`. Có test kiểm tra chúng **không bao giờ** lọt vào `data/notes/` (`test_unseen_instruments_stay_out_of_database`).

---

## 2. Banjo

### 2.1. Họ, cấu tạo, cơ chế
- **Họ:** nhạc cụ dây, có cần đàn, **gảy** (giống guitar).
- **Điểm đặc biệt: thân đàn là một mặt trống.** Thay vì hộp gỗ, banjo có một **màng căng** (như mặt trống) trên khung tròn. Ngựa đàn đứng trên màng.
- **Hệ quả:** màng mỏng, nhẹ và căng nên rung rất dễ, phát âm **rất hiệu quả**: to, sáng, "đanh". Nhưng nó cũng **tiêu hao năng lượng rất nhanh**, nên nốt **tắt rất nhanh**.
- Dây kim loại, có phím đàn, thường gảy bằng móng gảy đeo ở ngón tay.

### 2.2. Dây và lên dây
Loại phổ biến nhất là **banjo 5 dây**, lên dây kiểu "Sol mở" (gảy tất cả dây buông thì ra hợp âm Sol trưởng):
```
Banjo 5 dây
 ├── Dây 5 · g (ngắn, bắt đầu từ phím 5)  → G4 → 392.00 Hz   ← dây CAO NHẤT lại nằm sát dây trầm nhất
 ├── Dây 4 · D                             → D3 → 146.83 Hz
 ├── Dây 3 · G                             → G3 → 196.00 Hz
 ├── Dây 2 · B                             → B3 → 246.94 Hz
 └── Dây 1 · D                             → D4 → 293.66 Hz
```
- **Lên dây "đảo":** dây 5 ngắn hơn các dây khác, được lên **cao nhất** (G4), dù nằm ở phía dây trầm. Người chơi dùng ngón cái gảy dây này liên tục làm **âm nền**.
- Bảng nốt theo phím (12 phím đầu):

| Phím | Dây 5 · g | Dây 4 · D | Dây 3 · G | Dây 2 · B | Dây 1 · D |
|---|---|---|---|---|---|
| **buông** | **G4 · 392.00** | **D3 · 146.83** | **G3 · 196.00** | **B3 · 246.94** | **D4 · 293.66** |
| 2 | A4 · 440.00 | E3 · 164.81 | A3 · 220.00 | C♯4 · 277.18 | E4 · 329.63 |
| 4 | B4 · 493.88 | F♯3 · 185.00 | B3 · 246.94 | D♯4 · 311.13 | F♯4 · 369.99 |
| 5 | C5 · 523.25 | G3 · 196.00 | C4 · 261.63 | E4 · 329.63 | G4 · 392.00 |
| 7 | D5 · 587.33 | A3 · 220.00 | D4 · 293.66 | F♯4 · 369.99 | A4 · 440.00 |
| 12 | G5 · 783.99 | D4 · 293.66 | G4 · 392.00 | B4 · 493.88 | D5 · 587.33 |

**Trong dataset:** banjo Philharmonia có 74 nốt, từ **C3 → E6** (41 cao độ), gảy thường, 2 cường độ (*forte* 39, *piano* 35). Nốt thấp nhất C3 **thấp hơn** D3 của banjo 5 dây chuẩn. Vậy cây đàn được thu có lẽ là loại **4 dây** (loại *tenor* hoặc *plectrum*, dây thấp nhất là C3) hoặc được lên dây khác. Philharmonia không ghi loại đàn.

### 2.3. Âm sắc, phổ, đặc trưng
**Mô tả:** sáng, đanh, "lanh canh", tắt rất nhanh.

| Đặc trưng (trung vị, 74 nốt) | Banjo | Guitar (để so) |
|---|---|---|
| Centroid | 1 142 Hz | 781 Hz |
| Rolloff | 1 797 Hz | 1 021 Hz |
| ZCR | 0.054 | 0.031 |
| **RMS-CV** | **1.60** (cao nhất trong 7 nhạc cụ) | 0.88 |

RMS-CV 1.60 cho thấy năng lượng **sụt rất nhanh** sau lúc gảy, nhanh hơn hẳn guitar. Đây đúng là hệ quả của thân màng (§2.1).

---

## 3. Mandolin

### 3.1. Họ, cấu tạo, cơ chế
- **Họ:** nhạc cụ dây, có cần đàn, **gảy**, thường gảy bằng **miếng gảy** (phím gảy).
- Thân gỗ nhỏ (hình giọt nước hoặc dẹt), dây **thép**, có phím đàn. Phần dây rung dài khoảng 35 cm, gần bằng violin.
- **Điểm đặc biệt: 8 dây chia thành 4 cặp.** Hai dây trong một cặp lên **cùng nốt** và luôn được gảy cùng lúc. Hai dây không bao giờ khớp nhau hoàn toàn, lệch vài cent, nên âm có tiếng "lấp lánh" rất nhẹ (hai tần số gần nhau tạo ra tiếng đập).

### 3.2. Dây và lên dây — **giống hệt violin**
```
Mandolin (4 cặp dây)
 ├── Cặp G → G3 → 196.00 Hz
 ├── Cặp D → D4 → 293.66 Hz
 ├── Cặp A → A4 → 440.00 Hz
 └── Cặp E → E5 → 659.26 Hz
```
Cùng nốt, cùng tần số với 4 dây violin ([05](05_VIOLIN.md) §4), nên bảng nốt theo phím **giống hệt bảng violin** ([05](05_VIOLIN.md) §5), chỉ khác là mandolin có **phím đàn** cố định.

Đây là một điểm thú vị cho bài toán: **mandolin và violin chơi cùng những nốt trên cùng những dây**. Hai nhạc cụ chỉ khác nhau ở **cách tạo âm** (gảy và kéo vĩ) và **thân đàn**. Nếu hệ thống phân biệt được hai nhạc cụ này, thì đó là nhờ âm sắc, không phải nhờ cao độ.

### 3.3. Hai cách chơi trong dataset
| Kỹ thuật · số nốt | Người chơi làm gì | Âm thanh |
|---|---|---|
| **Gảy thường** (`normal`) · 39 | Gảy một lần | Bật rồi tắt dần, như guitar nhưng sáng hơn (dây thép, miếng gảy cứng) |
| **Vê** (`tremolo`) · 41 | Gảy **lên xuống rất nhanh và liên tục** cùng một nốt | Nốt được **kéo dài** như kéo vĩ, có độ "rung" nhanh |

**Trong dataset:** 80 nốt, **G3 → A6** (39 cao độ mỗi kỹ thuật), chủ yếu *piano*.

### 3.4. Âm sắc, phổ, đặc trưng — và một bất ngờ

| Đặc trưng (trung vị) | Mandolin gảy (39) | Mandolin vê (41) | Violin (để so) | Guitar (để so) |
|---|---|---|---|---|
| Centroid | 1 299 Hz | **2 035 Hz** | 2 299 Hz | 781 Hz |
| Rolloff | 2 071 Hz | 3 905 Hz | 4 063 Hz | 1 021 Hz |
| ZCR | 0.064 | 0.088 | 0.115 | 0.031 |
| **RMS-CV** | 1.38 | **0.66** | **0.65** | 0.88 |

**Bất ngờ:** mandolin **vê** có RMS-CV **0.66**, gần như bằng violin (0.65), và centroid gần với violin. Lý do là vê liên tục đã **giữ nốt kéo dài**, nên về mặt đường bao năng lượng, nó trông giống kéo vĩ chứ không giống gảy. Các đặc trưng **trung bình theo thời gian** không còn thấy "gảy" nữa, vì mỗi cú gảy nhỏ quá ngắn.

**Bài học:** "gảy hay kéo vĩ" không phải lúc nào cũng thấy rõ trong RMS-CV. Kỹ thuật chơi có thể làm một nhạc cụ gảy **mang đường bao** của nhạc cụ kéo vĩ.

---

## 4. Hệ thống sẽ trả lời gì? Dự đoán và số đo sơ bộ

**Số đo sơ bộ ở mức nốt:** mỗi nốt banjo hoặc mandolin tìm **5 nốt gần nhất** trong 4 653 nốt của 5 nhạc cụ trong CSDL, bằng vector 32 chiều đã chuẩn hóa ([15](15_AUDIO_FEATURES.md) §14), bỏ qua nốt cùng cao độ (`reports/theory/plucked_queries_nn.csv`). Kết quả chính thức ở mức file (sequence) sẽ đo ở Phần 2.

| Truy vấn | Dự đoán ban đầu (từ lý thuyết) | Số đo: nốt gần nhất thuộc nhạc cụ… | Dự đoán đúng không? |
|---|---|---|---|
| Banjo gảy (74 nốt) | **Guitar**: cùng gảy, tắt dần | guitar **47%** · violin 22% · double bass 19% · viola 8% · cello 4% | Đúng một nửa |
| Mandolin gảy (39 nốt) | **Guitar** | guitar **46%** · double bass 23% · viola 18% · violin 13% | Đúng một nửa |
| Mandolin vê (41 nốt) | **Violin** hoặc viola: vê giữ âm như kéo vĩ | **double bass 44%** · violin 32% · cello 15% · viola 7% · guitar **2%** | Đúng là **không** ra guitar; nhưng ra double bass nhiều hơn violin (chưa rõ vì sao) |

**Đọc kết quả:**
- "Âm gảy lạ → guitar" chỉ đúng khoảng **một nửa**: hệ thống không chỉ nhìn "gảy hay kéo vĩ", mà nhìn cả hình dạng phổ và âm vực.
- Mandolin **vê** gần như không bao giờ ra guitar: đúng như §3.4, vê đã biến âm gảy thành âm giữ đều.
- **Cẩn thận khi đọc:** banjo và mandolin đều thu ở Philharmonia, mà bộ kéo vĩ trong CSDL phần lớn cũng thu ở Philharmonia, còn guitar **76% thu ở Iowa**. Vì đặc trưng nhạy với nguồn thu ([15](15_AUDIO_FEATURES.md) §16.1), một phần các kết quả "ra violin, double bass" có thể do **cùng phòng thu** chứ không do giống âm sắc.

**Cách dùng kết quả:** nếu khoảng cách tới kết quả gần nhất của các truy vấn UNSEEN **lớn hơn hẳn** khoảng cách thường gặp của truy vấn nhạc cụ có trong CSDL, hệ thống có thể dùng một **ngưỡng** để báo "không tìm thấy nhạc cụ tương tự" ([19](19_DISTANCE_SIMILARITY.md), [22](22_MULTIMEDIA_DATABASE.md)).

---

## 5. CSDL chỉ có MỘT nhạc cụ gảy (4 kéo vĩ, 1 gảy): ảnh hưởng gì?

### 5.1. Những gì KHÔNG bị ảnh hưởng
- **Yêu cầu đề bài:** đề chỉ yêu cầu "nhạc cụ bộ dây", không yêu cầu cân bằng giữa gảy và kéo vĩ.
- **Cách chấm điểm:** CSDL cân bằng theo **nhạc cụ** (100 sequence mỗi nhạc cụ, guitar cũng 100), và "kết quả đúng" là **cùng nhạc cụ** ([19](19_DISTANCE_SIMILARITY.md) §8). Guitar chiếm đúng 1/5 CSDL như mọi nhạc cụ khác, không bị lép vế.

### 5.2. Những gì CÓ bị ảnh hưởng

| Ảnh hưởng | Vì sao | Số đo |
|---|---|---|
| **"Gảy" và "guitar" trùng nhau trong CSDL.** Không thể biết hệ thống nhận ra guitar nhờ **âm sắc của guitar** hay chỉ nhờ "**đây là âm gảy**" | Mọi mẫu gảy trong CSDL đều là guitar | Âm gảy của nhạc cụ khác bị xếp gần guitar khá nhiều: banjo 47%, mandolin 46%, violin pizzicato 24% (§4) |
| **Không phân biệt được các âm gảy với nhau** | Không có mẫu gảy nào khác để so | Truy vấn banjo, mandolin, double bass gảy (jazz) đều chỉ có thể rơi về guitar hoặc về một nhạc cụ kéo vĩ |
| Guitar là nhạc cụ "khác loại" duy nhất nên **dễ nhận**; cái khó thật nằm ở 4 nhạc cụ kéo vĩ | Violin – viola, cello – double bass giống nhau hơn nhiều so với guitar – bất kỳ | Nốt guitar tìm thấy guitar 87%, violin tìm thấy violin 96%; các cặp kéo vĩ là nơi nhầm nhiều ([15](15_AUDIO_FEATURES.md) §13) |
| **Guitar ít dữ liệu nhất** | Philharmonia chỉ có 106 nốt guitar | 445 nốt (các nhạc cụ khác khoảng 1 000); DB_POOL 181 < 200 nên nốt guitar được dùng lại nhiều hơn một chút khi ghép |
| **Guitar gần như đến từ MỘT nguồn thu** — ảnh hưởng đáng lo nhất | 76% nốt guitar từ Iowa, trong khi bộ kéo vĩ chỉ 21–28% từ Iowa. Mà đặc trưng lại nhạy với nguồn thu | Nốt guitar Iowa tìm trong Philharmonia chỉ ra guitar **29%** (`source_transfer_1nn.csv`). Hệ thống có thể đang nhận guitar một phần nhờ "nghe như thu ở Iowa" |

**Một kết quả bất ngờ:** violin **gảy** (pizzicato, 67 nốt) vẫn được xếp gần **violin** nhiều nhất (58%), chỉ 24% gần guitar. Nghĩa là "dấu vân tay" của violin (thân đàn, âm vực) vẫn còn khi đổi từ kéo sang gảy. Tuy vậy, violin pizzicato và phần lớn nốt violin trong CSDL cùng thu ở Philharmonia, nên một phần con số 58% có thể đến từ **cùng phòng thu**.

### 5.3. Có nên thêm nhạc cụ gảy?

| Cách | Ưu | Nhược |
|---|---|---|
| **A. Giữ nguyên**, ghi rõ giới hạn, đo thêm truy vấn bằng âm gảy (banjo, mandolin, pizzicato của bộ kéo vĩ đang để ở `data/excluded/technique/`) | Không tốn thêm dữ liệu; đề bài vẫn đạt; bài toán chính (phân biệt 4 nhạc cụ kéo vĩ) không đổi | Vẫn còn trùng "gảy = guitar" |
| **B. Thêm pizzicato của 4 nhạc cụ kéo vĩ từ Iowa MIS.** Trang Iowa có sẵn 140 file pizz (violin 36, viola 30, cello 38, double bass 36), cùng định dạng với file arco đã dùng; lúc tải ta chỉ lấy arco | "Gảy" không còn chỉ là guitar; hệ thống buộc phải nhận nhạc cụ qua nhiều cách chơi. Pizz Iowa cùng nguồn với guitar Iowa, nên cũng giảm trùng "guitar = Iowa" | Phải đổi D20; bài toán khó hơn (violin gảy phải được coi là "giống" violin kéo vĩ); phải tải, cắt, lọc thêm |
| C. Đưa banjo, mandolin vào CSDL | Thêm 2 nhạc cụ gảy | Chỉ 74 và 80 nốt (cần ≥ 360); mất nhạc cụ "ngoài CSDL" mà đề bài cần để thử |
| D. Tìm nguồn mới cho nhạc cụ gảy khác | — | Tốn thời gian, phải kiểm tra giấy phép, và thêm một nguồn thu nữa (càng làm nặng vấn đề nguồn thu) |

**Đề xuất:** làm **A** ngay (không tốn gì); cân nhắc **B** như phần mở rộng nếu còn thời gian. Đây là mục chờ quyết định **P13** trong [DESIGN_DECISIONS](../08_AI_CONTEXT/DESIGN_DECISIONS.md), nên quyết trước khi ghép sequence (Bước 5).
