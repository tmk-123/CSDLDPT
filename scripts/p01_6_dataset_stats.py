"""Bước 1.6: thống kê và mô tả dataset (số liệu cho đề mục 1 và cho báo cáo).

Đầu vào : data/catalog.csv, data/interim/iowa_notes/slice_report.csv
Đầu ra  : reports/dataset/dataset_stats.md          (bảng markdown tự sinh — ĐỪNG sửa tay)
          reports/dataset/*.csv                      (cùng số liệu, dạng bảng)
          reports/dataset/notes_by_instrument.png    (số nốt dùng được theo nhạc cụ × nguồn)
          reports/dataset/pitch_coverage.png         (số nốt theo nhạc cụ × cao độ)

    .venv/Scripts/python scripts/p01_6_dataset_stats.py
"""
import csv
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import BoundaryNorm, ListedColormap  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog.csv"
SLICE_REPORT = ROOT / "data" / "interim" / "iowa_notes" / "slice_report.csv"
OUT = ROOT / "reports" / "dataset"

INSTRUMENTS = ["violin", "viola", "cello", "double-bass", "guitar"]
SOURCES = ["philharmonia", "iowa"]
SPLITS = ["REF", "DB_POOL", "QUERY_POOL"]
MIN_NEEDED = 360                      # mức tối thiểu mỗi nhạc cụ (DATASET_COLLECTION_AND_FILTERING §2)
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Màu và mực theo bảng tham chiếu của skill dataviz (đã kiểm tra bằng validate_palette.js)
SURFACE, INK, INK_2, MUTED, GRID, BASELINE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SERIES = {"philharmonia": "#2a78d6", "iowa": "#eb6834"}          # slot 1 xanh, slot 2 cam
EMPTY = "#f0efec"                                                 # ô 0 nốt: xám trung tính
RAMP = ["#b7d3f6", "#86b6ef", "#3987e5", "#256abf", "#104281"]   # thang tuần tự xanh, nhạt → đậm
BINS = [1, 3, 6, 11, 21, 31]       # 1–2, 3–5, 6–10, 11–20, 21+ (giá trị > 30 được kẹp về 30 khi vẽ)


def midi_name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def load():
    with CATALOG.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["midi"] = int(r["midi"])
        r["selected"] = int(r["selected"])
        r["active_sec"] = float(r["active_sec"])
    with SLICE_REPORT.open(encoding="utf-8") as f:
        slices = list(csv.DictReader(f))
    return rows, slices


def md_table(header, body):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in body]
    return "\n".join(lines)


def write_csv(name, header, body):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(body)


def style_axes(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelcolor=INK_2, length=0)


def chart_notes_by_instrument(usable):
    """Thanh ngang xếp chồng: số nốt dùng được theo nhạc cụ, tách theo nguồn."""
    dpi, fig_w, fig_h = 150, 9.0, 3.2
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi, facecolor=SURFACE)
    left, bottom, width, height = 0.14, 0.17, 0.80, 0.62
    ax = fig.add_axes([left, bottom, width, height])
    style_axes(ax)
    n = len(INSTRUMENTS)
    xmax = max(sum(usable[(i, s)] for s in SOURCES) for i in INSTRUMENTS) * 1.12
    ax.set_xlim(0, xmax)
    ax.set_ylim(n - 0.5, -0.5)
    px_x = xmax / (fig_w * width * dpi)          # 1 pixel ảnh = bao nhiêu đơn vị trục x
    px_y = n / (fig_h * height * dpi)
    bar_h = 22 * px_y * dpi / 100                 # dày ~22px (≤ 24px)
    gap, r = 2 * px_x * dpi / 100, 4 * px_x * dpi / 100
    for y, ins in enumerate(INSTRUMENTS):
        x = 0.0
        parts = [(s, usable[(ins, s)]) for s in SOURCES if usable[(ins, s)] > 0]
        for k, (src, v) in enumerate(parts):
            x0, x1 = x + (gap if k else 0), x + v
            last = k == len(parts) - 1
            if last and x1 - x0 > 2 * r:          # đầu thanh bo tròn 4px, gốc vuông
                ax.add_patch(Rectangle((x0, y - bar_h / 2), x1 - x0 - r, bar_h, color=SERIES[src], lw=0))
                ax.add_patch(FancyBboxPatch((x1 - 2 * r, y - bar_h / 2), 2 * r, bar_h,
                                            boxstyle=f"round,pad=0,rounding_size={r}",
                                            mutation_aspect=(px_y / px_x), color=SERIES[src], lw=0))
            else:
                ax.add_patch(Rectangle((x0, y - bar_h / 2), x1 - x0, bar_h, color=SERIES[src], lw=0))
            x = x1
        ax.text(x + 8 * px_x * dpi / 100, y, f"{int(x):,}".replace(",", "."), va="center",
                ha="left", color=INK, fontsize=9)
    ax.axvline(MIN_NEEDED, color=INK_2, lw=1)
    ax.text(MIN_NEEDED, -0.5, f" mức cần: {MIN_NEEDED}", color=INK_2, fontsize=8, va="bottom", ha="left")
    ax.set_yticks(range(n), INSTRUMENTS)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", ".")))
    ax.xaxis.grid(True, color=GRID, lw=1)
    ax.set_axisbelow(True)
    ax.set_xlabel("Số nốt đơn dùng được", color=INK_2, fontsize=9)
    fig.text(left, 0.93, "Nốt đơn dùng được theo nhạc cụ và nguồn", color=INK, fontsize=11, weight="semibold")
    handles = [Rectangle((0, 0), 1, 1, color=SERIES[s]) for s in SOURCES]
    fig.legend(handles, ["Philharmonia", "Iowa MIS"], loc="upper right", bbox_to_anchor=(0.94, 0.97),
               ncol=2, frameon=False, labelcolor=INK_2, fontsize=9, handlelength=1, handleheight=1)
    fig.savefig(OUT / "notes_by_instrument.png", facecolor=SURFACE)
    plt.close(fig)


def chart_pitch_coverage(counts, lo, hi):
    """Lưới nhạc cụ × cao độ: số nốt dùng được ở mỗi cao độ (thang tuần tự một màu)."""
    import numpy as np
    grid = np.zeros((len(INSTRUMENTS), hi - lo + 1))
    for (ins, m), c in counts.items():
        grid[INSTRUMENTS.index(ins), m - lo] = c
    fig = plt.figure(figsize=(11, 3.0), dpi=150, facecolor=SURFACE)
    ax = fig.add_axes([0.10, 0.22, 0.78, 0.60])
    style_axes(ax)
    ax.spines["bottom"].set_visible(False)
    cmap = ListedColormap(RAMP)
    cmap.set_under(EMPTY)
    norm = BoundaryNorm(BINS, cmap.N)
    shown = np.where(grid == 0, 0.5, np.minimum(grid, BINS[-1] - 1))   # 0 → màu "under"; >30 → khoảng 21+
    mesh = ax.pcolormesh(np.arange(lo, hi + 2) - 0.5, np.arange(len(INSTRUMENTS) + 1) - 0.5,
                         shown, cmap=cmap, norm=norm,
                         edgecolors=SURFACE, linewidth=1.0)          # khe màu nền giữa các ô
    ax.set_ylim(len(INSTRUMENTS) - 0.5, -0.5)
    ax.set_yticks(range(len(INSTRUMENTS)), INSTRUMENTS)
    cs = [m for m in range(lo, hi + 1) if m % 12 == 0]
    ax.set_xticks(cs, [midi_name(m) for m in cs])
    ax.set_xlabel("Cao độ (mỗi ô = 1 nửa cung)", color=INK_2, fontsize=9)
    fig.text(0.10, 0.92, "Độ phủ cao độ: số nốt dùng được ở mỗi cao độ", color=INK, fontsize=11,
             weight="semibold")
    cax = fig.add_axes([0.90, 0.22, 0.012, 0.60])
    cb = fig.colorbar(mesh, cax=cax, spacing="uniform",
                      ticks=[(a + b) / 2 for a, b in zip(BINS, BINS[1:])])     # nhãn ở giữa mỗi khoảng
    cb.ax.set_yticklabels(["1–2", "3–5", "6–10", "11–20", "21+"], color=INK_2, fontsize=8)
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0)
    fig.text(0.90, 0.85, "số nốt", color=INK_2, fontsize=8)
    fig.text(0.10, 0.06, "Ô xám nhạt = không có nốt nào ở cao độ đó.", color=MUTED, fontsize=8)
    fig.savefig(OUT / "pitch_coverage.png", facecolor=SURFACE)
    plt.close(fig)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]
    OUT.mkdir(parents=True, exist_ok=True)
    rows, slices = load()
    md = ["# Thống kê dataset (tự sinh)", "",
          "> File này do `scripts/p01_6_dataset_stats.py` sinh ra từ `data/catalog.csv`. **Đừng sửa tay**; "
          "chạy lại script để cập nhật.", ""]

    # 1. Tổng quan theo nguồn × status
    status_list = ["OK", "CORRUPT", "DUPLICATE", "TOO_SHORT"]
    body = []
    for src in SOURCES:
        c = Counter(r["status"] for r in rows if r["source"] == src)
        body.append([src, sum(c.values())] + [c.get(s, 0) for s in status_list])
    body.append(["**tổng**", len(rows)] + [sum(1 for r in rows if r["status"] == s) for s in status_list])
    header = ["Nguồn", "Tổng file", *status_list]
    md += ["## 1. Tổng quan: số file theo nguồn và trạng thái", "", md_table(header, body), ""]
    write_csv("status_by_source.csv", header, body)

    # 2. Nơi mỗi file được đặt (split)
    split_order = ["REF", "DB_POOL", "QUERY_POOL", "PHRASE", "UNSEEN", "NONE"]
    body = []
    for ins in INSTRUMENTS + ["banjo", "mandolin"]:
        c = Counter(r["split"] for r in rows if r["instrument"] == ins)
        body.append([ins] + [c.get(s, 0) for s in split_order] + [sum(c.values())])
    header = ["Nhạc cụ", *split_order, "Tổng"]
    md += ["## 2. Phân bổ file theo split", "",
           "REF/DB_POOL/QUERY_POOL: nốt đơn dùng được (chia theo `midi mod 5`). PHRASE, UNSEEN: chỉ làm truy vấn. "
           "NONE: không dùng (xem mục 5).", "", md_table(header, body), ""]
    write_csv("split_by_instrument.csv", header, body)

    # 3. Nốt dùng được theo nhạc cụ × nguồn, và số được chọn trong giới hạn (D23)
    usable = Counter((r["instrument"], r["source"]) for r in rows if r["split"] in SPLITS)
    body = []
    for ins in INSTRUMENTS:
        sub = [r for r in rows if r["instrument"] == ins and r["split"] in SPLITS]
        cells = []
        for s in SPLITS:
            ss = [r for r in sub if r["split"] == s]
            cells.append(f"{sum(r['selected'] for r in ss)} / {len(ss)}")
        total = len(sub)
        body.append([ins, usable[(ins, "philharmonia")], usable[(ins, "iowa")], total, *cells,
                     "✅" if total >= MIN_NEEDED else "❌"])
    header = ["Nhạc cụ", "Philharmonia", "Iowa", "Tổng dùng được", "REF (chọn / có)", "DB_POOL (chọn / có)",
              "QUERY_POOL (chọn / có)", f"≥ {MIN_NEEDED}?"]
    md += ["## 3. Nốt đơn dùng được và số được chọn", "",
           "Giới hạn chọn mỗi nhạc cụ (D23): REF 150, DB_POOL 200, QUERY_POOL 60. Phần dư là dự trữ "
           "(`selected = 0`), vẫn thuộc cùng split.", "",
           md_table(header, body), "", "![Nốt đơn dùng được theo nhạc cụ](notes_by_instrument.png)", ""]
    write_csv("usable_by_instrument.csv", header, body)

    # 4. Độ phủ cao độ
    counts = Counter((r["instrument"], r["midi"]) for r in rows if r["split"] in SPLITS)
    body = []
    for ins in INSTRUMENTS:
        ms = sorted({m for (i, m) in counts if i == ins})
        missing = [midi_name(m) for m in range(ms[0], ms[-1] + 1) if (ins, m) not in counts]
        per_pitch = [counts[(ins, m)] for m in ms]
        body.append([ins, f"{midi_name(ms[0])} – {midi_name(ms[-1])}", ms[-1] - ms[0] + 1, len(ms),
                     statistics.median(per_pitch), " ".join(missing) if missing else "—"])
    header = ["Nhạc cụ", "Âm vực", "Số nửa cung", "Số cao độ có nốt", "Nốt / cao độ (trung vị)",
              "Cao độ bị trống trong âm vực"]
    lo = min(m for (_, m) in counts)
    hi = max(m for (_, m) in counts)
    md += ["## 4. Độ phủ cao độ", "", md_table(header, body), "",
           "![Độ phủ cao độ](pitch_coverage.png)", ""]
    write_csv("pitch_coverage.csv", header, body)

    # 5. File không dùng, theo lý do
    reasons = ["corrupt", "duplicate", "too_short", "technique"]
    body = []
    for ins in INSTRUMENTS + ["banjo", "mandolin"]:
        c = Counter(r["reason"] for r in rows if r["instrument"] == ins and r["split"] == "NONE")
        body.append([ins] + [c.get(x, 0) for x in reasons] + [sum(c.values())])
    header = ["Nhạc cụ", *reasons, "Tổng"]
    tech = Counter(r["technique"] for r in rows if r["reason"] == "technique")
    md += ["## 5. File không dùng (`data/excluded/<lý do>/`)", "", md_table(header, body), "",
           "Kỹ thuật bị loại nhiều nhất: " + ", ".join(f"`{t}` ({n})" for t, n in tech.most_common(8)) + ".", ""]
    write_csv("excluded_by_reason.csv", header, body)

    # 6. Truy vấn
    body = [[ins, sum(1 for r in rows if r["instrument"] == ins and r["split"] == "PHRASE"),
             sum(1 for r in rows if r["instrument"] == ins and r["split"] == "UNSEEN")]
            for ins in INSTRUMENTS + ["banjo", "mandolin"]]
    header = ["Nhạc cụ", "PHRASE (đoạn nhạc thật)", "UNSEEN (nhạc cụ ngoài CSDL)"]
    md += ["## 6. File dùng làm truy vấn (`data/queries/`)", "", md_table(header, body), ""]
    write_csv("queries.csv", header, body)

    # 7. Cắt nốt Iowa
    agg = defaultdict(lambda: [0, 0, 0])
    for s in slices:
        a = agg[s["instrument"]]
        a[0] += 1
        a[1] += int(s["expected"])
        a[2] += int(s["matched"])
    body = [[ins, agg[ins][0], agg[ins][1], agg[ins][2], f"{agg[ins][2] / agg[ins][1]:.0%}"]
            for ins in INSTRUMENTS if ins in agg]
    tot = [sum(agg[i][k] for i in agg) for k in range(3)]
    body.append(["**tổng**", tot[0], tot[1], tot[2], f"{tot[2] / tot[1]:.0%}"])
    header = ["Nhạc cụ", "File Iowa", "Nốt dự kiến (theo tên file)", "Nốt cắt được", "Tỷ lệ"]
    worst = sorted(slices, key=lambda s: int(s["matched"]) / int(s["expected"]))[:8]
    md += ["## 7. Cắt nốt Iowa (bước 1.2)", "", md_table(header, body), "",
           "File cắt được ít nhất:", "",
           md_table(["File gốc", "Dự kiến", "Cắt được", "Nốt thiếu"],
                    [[s["parent_file"], s["expected"], s["matched"], s["missing"] or "—"] for s in worst]), ""]
    write_csv("iowa_slicing.csv", header, body)

    # 8. Thời lượng phần có âm
    body = []
    for ins in INSTRUMENTS:
        cells = []
        for src in SOURCES:
            d = [r["active_sec"] for r in rows if r["instrument"] == ins and r["source"] == src
                 and r["split"] in SPLITS]
            cells.append(f"{statistics.median(d):.2f} s" if d else "—")
        body.append([ins, *cells])
    header = ["Nhạc cụ", "Philharmonia (trung vị)", "Iowa (trung vị)"]
    md += ["## 8. Thời lượng phần có âm của nốt dùng được", "", md_table(header, body), "",
           "Nốt Iowa dài hơn vì được thu ngân hết; project chỉ dùng tối đa 1.5 s đầu mỗi nốt.", ""]
    write_csv("active_duration.csv", header, body)

    chart_notes_by_instrument(usable)
    chart_pitch_coverage(counts, lo, hi)
    (OUT / "dataset_stats.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    print(f"\nĐã ghi {OUT}")


if __name__ == "__main__":
    main()
