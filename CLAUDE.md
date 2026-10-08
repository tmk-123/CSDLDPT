### Yêu cầu về phần lý thuyết

Mục tiêu của phần lý thuyết **không phải chỉ liệt kê các thuật ngữ hoặc định nghĩa**, mà phải giúp người thực hiện **thực sự hiểu bản chất của âm thanh, âm nhạc và cách các nhạc cụ tạo ra âm thanh**, đồng thời hiểu được mối quan hệ giữa các khái niệm để biết:

* Dữ liệu âm thanh cần thu thập là gì và tại sao cần thu thập như vậy.
* Một file âm thanh chứa những thông tin gì.
* Một nốt nhạc liên quan như thế nào đến tần số.
* Tần số, cao độ, nốt nhạc, F0, harmonic và timbre khác nhau như thế nào.
* Đặc điểm âm thanh của từng nhạc cụ khác nhau ở đâu.
* Tại sao cùng một nốt nhưng hai nhạc cụ khác nhau vẫn tạo ra âm thanh khác nhau.
* Tại sao cần thu thập cùng một nhạc cụ ở nhiều nốt và nhiều cách chơi khác nhau.
* Tại sao lựa chọn một đặc trưng âm thanh cụ thể để biểu diễn dữ liệu.
* Các đặc trưng đó có ý nghĩa gì đối với bài toán phân biệt/tìm kiếm âm thanh.

**Người thực hiện hiện chưa có nhiều kiến thức nền tảng về âm thanh, âm nhạc và các loại nhạc cụ.** Vì vậy, tài liệu phải được viết theo hướng **giảng giải từ cơ bản đến nâng cao**, không được mặc định rằng người đọc đã biết các khái niệm về âm nhạc hoặc xử lý tín hiệu âm thanh.

Khi xuất hiện một thuật ngữ mới, cần:

1. Giải thích thuật ngữ đó là gì.
2. Giải thích bản chất một cách trực quan.
3. Nếu có công thức, giải thích từng thành phần của công thức.
4. Cho ví dụ cụ thể.
5. Giải thích mối quan hệ của nó với các khái niệm trước đó.
6. Giải thích tại sao khái niệm đó quan trọng đối với project.
7. Nếu có thể, minh họa bằng chính 5 nhạc cụ của project:

   * Violin
   * Viola
   * Cello
   * Double Bass
   * Guitar

### Không được bỏ qua kiến thức về nhạc cụ

Phải nghiên cứu và giải thích **riêng từng nhạc cụ**, không chỉ đưa ra một bảng thông số tổng hợp.

Với mỗi nhạc cụ cần trình bày:

* Nhạc cụ thuộc họ nào.
* Cấu tạo cơ bản.
* Cơ chế tạo âm thanh.
* Các dây.
* Cách lên dây chuẩn.
* Tên note của từng dây buông.
* Octave của từng dây.
* Frequency tương ứng.
* Khoảng cao độ/range.
* Các note có thể chơi trên từng dây.
* Mối quan hệ giữa dây, note và frequency.
* Các cách chơi phổ biến.
* Cách mỗi kỹ thuật chơi làm thay đổi âm thanh.
* Đặc điểm timbre.
* Đặc điểm spectrum/harmonics.
* Những đặc trưng âm thanh có khả năng giúp phân biệt nhạc cụ.

### Phải giải thích từng note và frequency

Không chỉ nói:

> Violin có 4 dây: G-D-A-E.

Mà phải giải thích:

```text
Violin
 ├── G string → G3 → 196.00 Hz
 ├── D string → D4 → 293.66 Hz
 ├── A string → A4 → 440.00 Hz
 └── E string → E5 → 659.25 Hz
```

Sau đó giải thích cách các note thay đổi khi người chơi bấm dây:

```text
Dây buông
   ↓
Tăng 1 semitone
   ↓
Tăng 2 semitone
   ↓
Tăng 3 semitone
   ↓
...
```

Cần làm rõ:

* Note là gì.
* Frequency của note là gì.
* Octave là gì.
* Semitone là gì.
* Vì sao cùng một note có thể xuất hiện ở nhiều dây/vị trí.
* Vì sao cùng một frequency/note nhưng âm thanh từ các nhạc cụ khác nhau vẫn khác nhau.

### Phải phân biệt rõ các khái niệm dễ nhầm

Đặc biệt phải giải thích bằng ví dụ:

```text
Frequency
    ≠
Pitch
    ≠
Note
    ≠
F0
    ≠
Harmonic
    ≠
Timbre
```

Không được viết theo kiểu định nghĩa ngắn gọn rồi chuyển sang phần tiếp theo. Phải giải thích **mối quan hệ giữa chúng**.

Ví dụ cần hiểu được chuỗi:

```text
Nhạc cụ
   ↓
Dây
   ↓
Note
   ↓
Pitch
   ↓
F0
   ↓
Harmonics
   ↓
Waveform
   ↓
Spectrum
   ↓
Timbre
   ↓
Audio Features
```

### Phải giải thích đặc trưng âm thanh theo ý nghĩa thực tế

Không chỉ liệt kê:

```text
RMS
ZCR
MFCC
Spectral Centroid
...
```

Mà với từng đặc trưng phải trả lời:

* Nó đo cái gì?
* Nó được tính từ đâu?
* Nó có ý nghĩa vật lý/cảm nhận gì?
* Nó thay đổi như thế nào khi note thay đổi?
* Nó thay đổi như thế nào khi nhạc cụ thay đổi?
* Nó thay đổi như thế nào khi cách chơi thay đổi?
* Nó có bị ảnh hưởng bởi microphone/recording không?
* Nó có hữu ích cho bài toán phân biệt các nhạc cụ không?
* Có nên đưa nó vào feature vector của project không?

### Phải liên kết lý thuyết với dataset

Mục tiêu cuối cùng của phần lý thuyết là giúp xây dựng được mô hình dữ liệu hợp lý:

```text
Instrument
    ↓
String
    ↓
Note
    ↓
Octave
    ↓
Frequency / F0
    ↓
Playing Technique
    ↓
Audio File
    ↓
Waveform
    ↓
Spectrum / Spectrogram
    ↓
Extracted Features
    ↓
Feature Vector
```

Phải giải thích tại sao dataset cần được phân cấp như vậy và **mỗi tầng mang ý nghĩa gì**.

Ví dụ:

```text
Violin
 └── A String
      └── A4
           ├── Arco
           ├── Pizzicato
           ├── Tremolo
           └── Vibrato
```

Từ đó phải giải thích:

* `Instrument`, `String`, `Note`, `Technique` là **metadata/nhãn âm nhạc**.
* `F0`, spectrum, harmonics, envelope là **đặc tính của tín hiệu âm thanh**.
* `RMS`, `ZCR`, spectral features, MFCC... là **các feature được trích xuất từ tín hiệu**.

### Yêu cầu về cách trình bày

Tài liệu phải đi theo trình tự:

```text
Âm thanh cơ bản
        ↓
Frequency / Amplitude / Phase
        ↓
Pitch
        ↓
Note / Octave / Semitone
        ↓
F0
        ↓
Harmonics / Overtones
        ↓
Timbre
        ↓
Nhạc cụ
        ↓
Dây / Note / Frequency
        ↓
Cách chơi
        ↓
Digital Audio
        ↓
Waveform
        ↓
FFT / STFT
        ↓
Spectrum / Spectrogram
        ↓
Audio Features
        ↓
Dataset
        ↓
Feature Vector
        ↓
CSDL đa phương tiện / Similarity Search / R-tree
```

**Ưu tiên giải thích bằng ví dụ cụ thể thay vì chỉ đưa ra định nghĩa.**

Nếu một khái niệm khó, phải giải thích theo kiểu:

> Khái niệm này là gì → hình dung trực quan → ví dụ → công thức → áp dụng vào Violin/Viola/Cello/Double Bass/Guitar → liên hệ với dataset của project.

Không được giả định người đọc đã học qua lý thuyết âm nhạc hoặc xử lý tín hiệu số.
