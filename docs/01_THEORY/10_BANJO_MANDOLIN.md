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

## 4. Dự đoán: hệ thống sẽ trả lời gì?

Đây là **giả thuyết** để kiểm tra ở Phần 2 (đánh giá truy vấn), **chưa phải kết quả**:

| Truy vấn | Dự đoán kết quả gần nhất | Lý do |
|---|---|---|
| Banjo gảy | **Guitar** | Cùng gảy, tắt dần (RMS-CV cao); nhưng banjo sáng hơn guitar nhiều, nên khoảng cách sẽ **xa hơn** truy vấn guitar thật |
| Mandolin gảy | **Guitar** (hoặc violin ở nốt cao) | Gảy, tắt dần; độ sáng (1 299 Hz) nằm giữa cello và viola, sáng hơn guitar nhiều |
| Mandolin vê | **Violin** (hoặc viola) | Đường bao giữ đều, độ sáng gần violin, cùng âm vực G3 → A6 |

**Cách dùng kết quả:** nếu khoảng cách tới kết quả gần nhất của các truy vấn UNSEEN **lớn hơn hẳn** khoảng cách thường gặp của truy vấn nhạc cụ có trong CSDL, hệ thống có thể dùng một **ngưỡng** để báo "không tìm thấy nhạc cụ tương tự" ([19](19_DISTANCE_SIMILARITY.md), [22](22_MULTIMEDIA_DATABASE.md)).
