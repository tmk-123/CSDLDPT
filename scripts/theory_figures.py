"""Hình minh họa và số liệu đo thật cho phần lý thuyết (docs/01_THEORY/).

Đầu vào : data/catalog.csv, file âm thanh trong data/ (chạy sau p01_3_build_catalog.py)
Đầu ra  : reports/theory/*.png   (hình minh họa, dùng trong docs/01_THEORY)
          reports/theory/*.csv   (số liệu đo, để docs trích dẫn đúng con số)

    .venv/Scripts/python scripts/theory_figures.py            # đo đặc trưng (≈ 3 phút lần đầu) + vẽ
    .venv/Scripts/python scripts/theory_figures.py --redo     # đo lại đặc trưng từ đầu

Mọi đặc trưng đo theo đúng cách của project (docs/04_PART_1/02_AUDIO_ANALYSIS/PREPROCESSING.md):
mono 22 050 Hz, chuẩn hóa đỉnh, cắt lặng, lấy tối đa 1.5 s đầu, frame 2048 / hop 512, chỉ tính frame có âm.
"""
import argparse
import csv
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import librosa
import matplotlib
import matplotlib.ticker
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from scipy.signal import butter, sosfiltfilt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "theory"
CATALOG = ROOT / "data" / "catalog.csv"
SR, N_FFT, HOP = 22050, 2048, 512

INSTRUMENTS = ["violin", "viola", "cello", "double-bass", "guitar"]
VI = {"violin": "Violin", "viola": "Viola", "cello": "Cello", "double-bass": "Double bass", "guitar": "Guitar"}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Bảng màu tham chiếu (skill dataviz; đã chạy validate_palette.js: 5 màu đạt, có cảnh báo tương phản
# ⇒ biểu đồ nhiều đường luôn có nhãn trực tiếp + bảng số liệu trong docs)
SURFACE, INK, INK_2, MUTED, GRID, BASELINE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INST_COLOR = dict(zip(INSTRUMENTS, SLOTS))
BLUE_RAMP = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SPEC_CMAP = LinearSegmentedColormap.from_list("blue_seq", BLUE_RAMP)


def midi_name(m):
    return f"{NAMES[int(m) % 12]}{int(m) // 12 - 1}"


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ───────────────────────── đo đặc trưng một nốt ─────────────────────────
HP_SOS = butter(4, 25, btype="highpass", fs=SR, output="sos")   # D27: bỏ tiếng ù hạ âm < 25 Hz


def highpass(y):
    return sosfiltfilt(HP_SOS, y).astype(np.float32) if len(y) > 64 else y


def load_note(path, seconds=1.5):
    y, _ = librosa.load(path, sr=SR, mono=True)
    if len(y) == 0:
        return None
    y = highpass(y)
    y = 0.95 * y / (np.abs(y).max() + 1e-12)
    y, _ = librosa.effects.trim(y, top_db=40)
    return y[: int(seconds * SR)]


def note_features(path):
    try:
        y = load_note(path)
        if y is None or len(y) < N_FFT:
            return None
        S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP, window="hann"))
        rms = librosa.feature.rms(S=S, frame_length=N_FFT)[0]
        active = 20 * np.log10(rms / (rms.max() + 1e-12) + 1e-12) > -40
        zcr = librosa.feature.zero_crossing_rate(y, frame_length=N_FFT, hop_length=HOP)[0][: len(rms)]
        cen = librosa.feature.spectral_centroid(S=S, sr=SR)[0]
        bw = librosa.feature.spectral_bandwidth(S=S, sr=SR)[0]
        ro = librosa.feature.spectral_rolloff(S=S, sr=SR, roll_percent=0.85)[0]
        fl = librosa.feature.spectral_flatness(S=S)[0]
        # MFCC như FEATURE_SET: 128 dải Mel, 14 hệ số, bỏ c0 (chỉ đo độ to) → c1..c13
        mel = librosa.feature.melspectrogram(S=S ** 2, sr=SR, n_mels=128)
        mf = librosa.feature.mfcc(S=librosa.power_to_db(mel), n_mfcc=14)[1:, active]
        r = rms[active]
        out = {"centroid_hz": float(cen[active].mean()), "bandwidth_hz": float(bw[active].mean()),
               "rolloff_hz": float(ro[active].mean()), "zcr": float(zcr[active].mean()),
               "flatness": float(fl[active].mean()), "rms_cv": float(r.std() / (r.mean() + 1e-12)),
               "seconds_used": round(len(y) / SR, 3)}
        out.update({f"mfcc{i + 1}": float(mf[i].mean()) for i in range(13)})
        out.update({f"mfcc_std{i + 1}": float(mf[i].std()) for i in range(13)})   # biến đổi theo thời gian
        return out
    except Exception as e:  # file hỏng hiếm gặp: bỏ qua, không làm dừng cả lần chạy
        return {"error": str(e)[:80]}


def measure_all(rows, redo):
    cache = OUT / "note_features.csv"
    if cache.exists() and not redo:
        with cache.open(encoding="utf-8") as f:
            return list(csv.DictReader(f))
    targets = [r for r in rows if r["status"] == "OK" and (
        r["path"].startswith("data/notes/") or r["path"].startswith("data/queries/unseen/")
        or (r["instrument"] in ("violin", "cello") and r["reason"] == "technique"))]
    print(f"Đo đặc trưng {len(targets)} nốt ...", flush=True)
    with ProcessPoolExecutor(6) as ex:
        feats = list(ex.map(note_features, [str(ROOT / r["path"]) for r in targets], chunksize=16))
    out = []
    keep = ["recording_id", "source", "instrument", "note", "midi", "dynamics", "technique",
            "technique_family", "split", "file"]
    for r, f in zip(targets, feats):
        if f and "error" not in f:
            out.append({**{k: r[k] for k in keep}, **{k: (round(v, 4) if isinstance(v, float) else v)
                                                       for k, v in f.items()}})
    with cache.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    return out


# ───────────────────────── trình bày ─────────────────────────
def style(ax, grid_axis="y"):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelcolor=INK_2, labelsize=8, length=0)
    if grid_axis:
        ax.grid(True, axis=grid_axis, color=GRID, lw=0.8)
        ax.set_axisbelow(True)


def plain_log_ticks(ax, axis, values):
    """Trục log ghi số thường (300, 1.000…) thay cho dạng 3×10²."""
    labels = [f"{v:,}".replace(",", ".") for v in values]
    target = ax.yaxis if axis == "y" else ax.xaxis
    (ax.set_yticks if axis == "y" else ax.set_xticks)(values, labels)
    target.set_minor_formatter(matplotlib.ticker.NullFormatter())


def low_band_fraction(path):
    """Tỷ lệ năng lượng 25–80 Hz (sau lọc 25 Hz): cao nghĩa là bản thu lẫn tiếng ù tần số thấp."""
    y, _ = librosa.load(path, sr=SR, mono=True)
    y = highpass(y)[: int(3 * SR)]
    s = np.abs(np.fft.rfft(y * np.hanning(len(y)))) ** 2
    f = np.fft.rfftfreq(len(y), 1 / SR)
    return float(s[(f >= 25) & (f < 80)].sum() / (s.sum() + 1e-20))


def title(fig, text, sub=None, x=0.06):
    fig.text(x, 0.965, text, color=INK, fontsize=12, weight="semibold", va="top")
    if sub:
        fig.text(x, 0.915, sub, color=INK_2, fontsize=9, va="top")


def save(fig, name):
    fig.savefig(OUT / name, facecolor=SURFACE, dpi=150)
    plt.close(fig)
    print("  ✓", name)


def pick(rows, instrument, note, techniques, dynamics_pref=("forte", "mezzo-forte", "fortissimo", "piano")):
    cands = [r for r in rows if r["instrument"] == instrument and r["note"] == note and r["status"] == "OK"
             and r["source"] == "philharmonia" and r["technique"] in techniques and r["duration_label"] != "phrase"]
    for d in dynamics_pref:
        c = [r for r in cands if r["dynamics"] == d]
        if c:
            return max(c, key=lambda r: float(r["active_sec"]))
    return max(cands, key=lambda r: float(r["active_sec"])) if cands else None


def write_rows(name, header, body):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(body)


# ───────────────────────── các hình ─────────────────────────
def fig_sine():
    t = np.linspace(0, 0.010, 2000)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3), facecolor=SURFACE)
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.17, top=0.78, wspace=0.28)
    ax = axes[0]
    style(ax)
    ax.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 220 * t), color=SLOTS[0], lw=2)
    T = 1000 / 220
    p1 = 1000 / 880
    ax.annotate("", xy=(p1 + T, 0.92), xytext=(p1, 0.92), arrowprops=dict(arrowstyle="<->", color=INK_2, lw=1))
    ax.text(p1 + T / 2, 0.97, f"chu kỳ T = 1/220 s ≈ {T:.2f} ms", ha="center", va="bottom", color=INK, fontsize=8)
    ax.annotate("", xy=(p1, 0.8), xytext=(p1, 0), arrowprops=dict(arrowstyle="<->", color=INK_2, lw=1))
    ax.text(p1 + 0.15, 0.4, "biên độ A = 0.8", color=INK, fontsize=8, va="center")
    ax.set_ylim(-1.05, 1.25)
    ax.set_title("(a) Một sóng sin 220 Hz", color=INK_2, fontsize=9, loc="left")
    ax = axes[1]
    style(ax)
    ax.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 220 * t), color=SLOTS[0], lw=2, label="220 Hz (A3)")
    ax.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 440 * t), color=SLOTS[1], lw=2, label="440 Hz (A4)")
    ax.set_ylim(-1.05, 1.25)
    ax.legend(loc="upper right", frameon=False, fontsize=8, labelcolor=INK_2, ncol=2)
    ax.set_title("(b) Tần số gấp đôi → dao động nhanh gấp đôi", color=INK_2, fontsize=9, loc="left")
    ax = axes[2]
    style(ax)
    ax.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 220 * t), color=SLOTS[0], lw=2, label="pha 0°")
    ax.plot(t * 1000, 0.8 * np.sin(2 * np.pi * 220 * t + np.pi / 2), color=SLOTS[1], lw=2, label="pha 90°")
    ax.set_ylim(-1.05, 1.25)
    ax.legend(loc="upper right", frameon=False, fontsize=8, labelcolor=INK_2, ncol=2)
    ax.set_title("(c) Cùng tần số, lệch pha 1/4 chu kỳ", color=INK_2, fontsize=9, loc="left")
    for ax in axes:
        ax.set_xlabel("thời gian (ms)", color=INK_2, fontsize=8)
    axes[0].set_ylabel("áp suất / biên độ", color=INK_2, fontsize=8)
    title(fig, "Ba thông số của một sóng sin: tần số, biên độ, pha")
    save(fig, "01_sine_frequency_amplitude_phase.png")


def fig_harmonic_recipes():
    f0, k = 220, np.arange(1, 9)
    recipes = {"Công thức A — bồi âm giảm đều (giống kéo vĩ)": 1 / k,
               "Công thức B — bồi âm lẻ mạnh, chẵn yếu": np.where(k % 2 == 1, 1 / k, 0.08 / k)}
    t = np.linspace(0, 3 / f0, 1500)
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.2), facecolor=SURFACE,
                             gridspec_kw=dict(height_ratios=[1, 1.15]))
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.1, top=0.84, hspace=0.55, wspace=0.22)
    for j, (name, amp) in enumerate(recipes.items()):
        ax = axes[0, j]
        style(ax)
        ax.bar(k * f0, amp, width=70, color=SLOTS[0])
        ax.set_xticks(k * f0, [f"{int(x)}" for x in k * f0], fontsize=7)
        ax.set_ylim(0, 1.1)
        ax.set_title(name, color=INK_2, fontsize=9, loc="left")
        ax.set_xlabel("tần số (Hz) = 1×, 2×, 3× … F0", color=INK_2, fontsize=8)
        ax.set_ylabel("biên độ", color=INK_2, fontsize=8)
        wave = sum(a * np.sin(2 * np.pi * kk * f0 * t) for kk, a in zip(k, amp))
        ax = axes[1, j]
        style(ax)
        ax.plot(t * 1000, wave / np.abs(wave).max(), color=SLOTS[0], lw=2)
        ax.set_xlabel("thời gian (ms) — 3 chu kỳ, cùng chu kỳ 4.55 ms", color=INK_2, fontsize=8)
        ax.set_ylabel("dạng sóng", color=INK_2, fontsize=8)
    title(fig, "Cùng F0 = 220 Hz, khác “công thức” bồi âm → khác dạng sóng → khác âm sắc",
          "Hàng trên: biên độ từng bồi âm (phổ). Hàng dưới: sóng thu được khi cộng các bồi âm lại.")
    save(fig, "02_same_f0_different_harmonics.png")


def harmonic_profile(y, f0_guess, n_harm=15):
    # Phân tích 0.3 s ngay sau lúc nốt mạnh nhất (không lấy vị trí cố định: một số bản thu có tiếng động
    # nhỏ trước khi gảy, khiến đoạn cố định rơi vào trước nốt).
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    peak = int(np.argmax(rms[: int(1.0 * SR / 256)])) * 256
    start = peak + int(0.05 * SR)
    seg = y[start: start + int(0.3 * SR)]
    if len(seg) < int(0.2 * SR):
        seg = y[: int(0.3 * SR)]
    f0s, vo, _ = librosa.pyin(seg, fmin=60, fmax=1000, sr=SR, frame_length=4096)
    f0 = float(np.nanmedian(f0s[vo])) if np.any(vo) else f0_guess
    f0 = f0 * 2 ** round(np.log2(f0_guess / f0))      # pYIN có thể nhầm quãng tám: đưa về quãng tám của nốt
    n = 1 << 16
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n))
    freqs = np.fft.rfftfreq(n, 1 / SR)
    amps = []
    for h in range(1, n_harm + 1):
        band = (freqs > h * f0 * 0.975) & (freqs < h * f0 * 1.025)
        amps.append(spec[band].max() if band.any() else 1e-9)
    amps = np.array(amps)
    return f0, 20 * np.log10(amps / amps.max()), seg


def fig_same_note(rows):
    """Chọn bản thu A3 sạch nhất của mỗi nhạc cụ: một số bản thu guitar lẫn tiếng ù 25–80 Hz (ghi trong
    RESULTS_REPORT), dùng chúng sẽ làm sai hình. Ưu tiên Philharmonia, forte, rồi bản ít ù nhất."""
    picks = {}
    pref = ["forte", "mezzo-forte", "fortissimo", "piano", "mezzo-piano", "pianissimo"]
    for ins in INSTRUMENTS:
        techs = ("normal",) if ins == "guitar" else ("arco-normal",)
        cands = [r for r in rows if r["instrument"] == ins and r["note"] == "A3" and r["status"] == "OK"
                 and r["technique"] in techs and r["duration_label"] != "phrase"
                 and r["split"] in ("REF", "DB_POOL", "QUERY_POOL")]
        scored = []
        for r in cands:
            lb = low_band_fraction(str(ROOT / r["path"]))
            f0, _, _ = harmonic_profile(load_note(str(ROOT / r["path"]), seconds=1.0), 220.0)
            bad_f0 = abs(f0 / 220.0 - 1) > 0.03            # F0 đo được phải khớp nốt A3: loại bản thu bị nhiễu
            dyn = pref.index(r["dynamics"]) if r["dynamics"] in pref else 9
            scored.append((bad_f0, lb > 0.10, r["source"] != "philharmonia", dyn, lb, r))
        picks[ins] = sorted(scored, key=lambda t: t[:5])[0][5]
    fig, axes = plt.subplots(5, 2, figsize=(10.5, 9.6), facecolor=SURFACE,
                             gridspec_kw=dict(width_ratios=[1.15, 1]))
    fig.subplots_adjust(left=0.1, right=0.98, bottom=0.06, top=0.86, hspace=0.75, wspace=0.18)
    table = []
    for i, ins in enumerate(INSTRUMENTS):
        r = picks[ins]
        y = load_note(str(ROOT / r["path"]), seconds=1.0)
        f0, hdb, seg = harmonic_profile(y, 220.0)
        table.append([ins, r["file"], round(f0, 1)] + [round(float(v), 1) for v in hdb])
        ax = axes[i, 0]
        style(ax, grid_axis=None)
        start = int(0.05 * SR)
        z = np.where((seg[start:-1] <= 0) & (seg[start + 1:] > 0))[0]
        s0 = start + (z[0] if len(z) else 0)
        n = int(4 * SR / f0)
        w = seg[s0: s0 + n]
        ax.plot(np.arange(len(w)) / SR * 1000, w / (np.abs(w).max() + 1e-9), color=SLOTS[0], lw=1.6)
        ax.set_ylim(-1.15, 1.15)
        ax.set_yticks([])
        src = "Philharmonia" if r["source"] == "philharmonia" else "Iowa"
        ax.set_title(f"{VI[ins]} — 4 chu kỳ, F0 đo được {f0:.1f} Hz ({src}, {r['dynamics']})",
                     color=INK, fontsize=9, loc="left")
        ax = axes[i, 1]
        style(ax)
        ax.bar(np.arange(1, 16), hdb + 60, bottom=-60, width=0.62, color=SLOTS[0])
        ax.set_ylim(-60, 3)
        ax.set_xticks(range(1, 16), [str(k) for k in range(1, 16)], fontsize=7)
        ax.set_title("độ mạnh bồi âm thứ 1 … 15 (dB, so với bồi âm mạnh nhất)", color=INK_2, fontsize=8, loc="left")
    axes[-1, 0].set_xlabel("thời gian (ms)", color=INK_2, fontsize=8)
    axes[-1, 1].set_xlabel("bồi âm thứ k (tần số = k × F0)", color=INK_2, fontsize=8)
    title(fig, "Cùng nốt A3 (F0 ≈ 220 Hz) trên 5 nhạc cụ: cùng chu kỳ, khác dạng sóng, khác phổ bồi âm",
          "Kéo vĩ thường / guitar gảy thường, mỗi nhạc cụ chọn bản thu sạch nhất. "
          "Sự khác nhau về dạng sóng và phổ chính là khác nhau về âm sắc (timbre).", x=0.1)
    save(fig, "03_same_note_A3_five_instruments.png")
    write_rows("harmonics_A3.csv", ["instrument", "file", "f0_hz"] + [f"h{k}_db" for k in range(1, 16)], table)
    return picks


def rms_db_curve(path, seconds=3.0):
    y, _ = librosa.load(path, sr=SR, mono=True)
    y = highpass(y)
    y = y / (np.abs(y).max() + 1e-12)
    y, _ = librosa.effects.trim(y, top_db=60)
    y = y[: int(seconds * SR)]
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    return np.arange(len(rms)) * 256 / SR, 20 * np.log10(rms / rms.max() + 1e-6)


def fig_envelope(rows):
    def longest(ins, tech):
        c = [r for r in rows if r["instrument"] == ins and r["note"] == "A4" and r["technique"] == tech
             and r["status"] == "OK" and r["source"] == "philharmonia" and r["duration_label"] != "phrase"
             and r["dynamics"] in ("forte", "mezzo-forte", "fortissimo")]
        return max(c, key=lambda r: float(r["active_sec"]))
    v, g = longest("violin", "arco-normal"), longest("guitar", "normal")
    fig, ax = plt.subplots(figsize=(9, 3.6), facecolor=SURFACE)
    fig.subplots_adjust(left=0.08, right=0.8, bottom=0.16, top=0.8)
    style(ax)
    for r, c, lab, lim in ((v, SLOTS[0], "Violin — kéo vĩ (arco)", -15), (g, SLOTS[1], "Guitar — gảy", -50)):
        t, db = rms_db_curve(str(ROOT / r["path"]))
        ax.plot(t, db, color=c, lw=2, label=lab)
        # violin: gắn nhãn ở cuối đoạn giữ âm (trước khi nhấc vĩ); guitar: ở cuối đường
        k = np.where(db > lim)[0][-1]
        ax.text(t[k] + 0.04, db[k] + 2, lab, color=INK, fontsize=8, va="bottom")
    ax.legend(loc="lower left", frameon=False, fontsize=8, labelcolor=INK_2)
    ax.set_ylim(-62, 3)
    ax.set_xlabel("thời gian (s)", color=INK_2, fontsize=8)
    ax.set_ylabel("độ to (dB so với đỉnh)", color=INK_2, fontsize=8)
    title(fig, "Đường bao năng lượng: kéo vĩ giữ âm đều, gảy thì tắt dần",
          f"Cùng nốt A4 (440 Hz). Violin: {v['file']}. Guitar: {g['file']}.")
    save(fig, "04_envelope_bowed_vs_plucked.png")
    return v, g


def fig_spectrograms(v, g):
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), facecolor=SURFACE)
    fig.subplots_adjust(left=0.07, right=0.9, bottom=0.15, top=0.78, wspace=0.18)
    for ax, r, lab in ((axes[0], v, "Violin A4 — kéo vĩ"), (axes[1], g, "Guitar A4 — gảy")):
        y, _ = librosa.load(str(ROOT / r["path"]), sr=SR, mono=True)
        y = highpass(y)
        y, _ = librosa.effects.trim(y / (np.abs(y).max() + 1e-12), top_db=60)
        y = y[: int(2.5 * SR)]
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=2048, hop_length=256)), ref=np.max)
        t = np.arange(D.shape[1]) * 256 / SR
        f = np.linspace(0, SR / 2, D.shape[0])
        m = ax.pcolormesh(t, f, D, cmap=SPEC_CMAP, vmin=-80, vmax=0, shading="auto")
        ax.set_ylim(0, 5000)
        style(ax, grid_axis=None)
        ax.set_title(lab, color=INK, fontsize=9, loc="left")
        ax.set_xlabel("thời gian (s)", color=INK_2, fontsize=8)
        ks = [k for k in range(1, 12) if k * 440 < 5000]
        ax.set_yticks([k * 440 for k in ks], [f"{k}× · {k * 440}" for k in ks], fontsize=6.5)
    axes[0].set_ylabel("bồi âm thứ k · tần số (Hz)", color=INK_2, fontsize=8)
    cax = fig.add_axes([0.915, 0.15, 0.012, 0.63])
    cb = fig.colorbar(m, cax=cax)
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=7, colors=INK_2, length=0)
    fig.text(0.905, 0.81, "dB", color=INK_2, fontsize=8)
    title(fig, "Spectrogram: mỗi vạch ngang là một bồi âm (k × 440 Hz)",
          "Violin: các vạch kéo dài suốt nốt và hơi gợn sóng (vibrato). Guitar: vạch sáng lúc gảy rồi mờ dần, "
          "bồi âm cao tắt trước.")
    save(fig, "05_spectrogram_violin_vs_guitar.png")


def fig_ranges():
    data = {  # (thấp nhất, cao nhất thường dùng, [dây buông])
        "violin": (55, 105, [55, 62, 69, 76]),
        "viola": (48, 88, [48, 55, 62, 69]),
        "cello": (36, 81, [36, 43, 50, 57]),
        "double-bass": (28, 67, [28, 33, 38, 43]),
        "guitar": (40, 83, [40, 45, 50, 55, 59, 64]),
    }
    fig, ax = plt.subplots(figsize=(11, 3.9), facecolor=SURFACE)
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.2, top=0.8)
    style(ax, grid_axis="x")
    for i, ins in enumerate(INSTRUMENTS):
        lo, hi, opens = data[ins]
        ax.plot([lo, hi], [i, i], color="#b7d3f6", lw=10, solid_capstyle="round")
        for m in opens:
            ax.plot(m, i, "o", ms=7, color=SLOTS[0], mec=SURFACE, mew=1.5)
            ax.text(m, i - 0.32, midi_name(m), color=INK_2, fontsize=7, ha="center", va="bottom")
        ax.text(hi + 0.8, i, f"≈ {midi_name(hi)}", color=MUTED, fontsize=7, va="center")
    cs = list(range(24, 109, 12))
    ax.set_xticks(cs, [f"{midi_name(m)}\n{hz(m):.0f} Hz" for m in cs], fontsize=7)
    ax.set_yticks(range(len(INSTRUMENTS)), [VI[i] for i in INSTRUMENTS], fontsize=9)
    ax.set_ylim(len(INSTRUMENTS) - 0.5, -1)
    ax.set_xlim(22, 110)
    title(fig, "Âm vực 5 nhạc cụ: chấm = dây buông, thanh = khoảng cao độ thường chơi",
          "Mỗi vạch dọc cách nhau 1 quãng tám (tần số gấp đôi). Nốt chuẩn A4 = 440 Hz là dây A của violin và viola. "
          "Vùng G3–G4 cả 5 nhạc cụ đều chơi được.")
    save(fig, "06_instrument_ranges_open_strings.png")


def feature_summary(feats):
    groups = defaultdict(list)
    for f in feats:
        if f["path_kind"] == "notes":
            groups[f["instrument"]].append(f)
    body = []
    for ins in INSTRUMENTS:
        g = groups[ins]
        row = [ins, len(g)]
        for k in ("centroid_hz", "bandwidth_hz", "rolloff_hz", "zcr", "rms_cv", "flatness"):
            v = np.array([float(x[k]) for x in g])
            row += [round(float(np.median(v)), 4), round(float(np.percentile(v, 25)), 4),
                    round(float(np.percentile(v, 75)), 4)]
        body.append(row)
    hdr = ["instrument", "n"]
    for k in ("centroid_hz", "bandwidth_hz", "rolloff_hz", "zcr", "rms_cv", "flatness"):
        hdr += [f"{k}_median", f"{k}_q25", f"{k}_q75"]
    write_rows("feature_summary_by_instrument.csv", hdr, body)
    return groups


def fig_features_by_instrument(groups):
    keys = [("centroid_hz", "Spectral centroid (Hz) — độ sáng", True),
            ("rms_cv", "RMS-CV — năng lượng dao động bao nhiêu", False),
            ("zcr", "ZCR — tỷ lệ đổi dấu / mẫu", False)]
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.9), facecolor=SURFACE)
    fig.subplots_adjust(left=0.06, right=0.99, bottom=0.17, top=0.78, wspace=0.28)
    rng = np.random.default_rng(0)
    for ax, (k, lab, logy) in zip(axes, keys):
        style(ax)
        for i, ins in enumerate(INSTRUMENTS):
            v = np.array([float(x[k]) for x in groups[ins]])
            ax.scatter(i + rng.uniform(-0.28, 0.28, len(v)), v, s=4, color=SLOTS[0], alpha=0.18, lw=0)
            q1, med, q3 = np.percentile(v, [25, 50, 75])
            ax.plot([i - 0.32, i + 0.32], [med, med], color=INK, lw=2)
            ax.plot([i, i], [q1, q3], color=INK, lw=1)
        if logy:
            ax.set_yscale("log")
            plain_log_ticks(ax, "y", [300, 500, 1000, 2000, 4000])
        ax.set_xticks(range(5), [VI[i] for i in INSTRUMENTS], fontsize=7)
        ax.set_title(lab, color=INK_2, fontsize=9, loc="left")
    n = sum(len(groups[i]) for i in INSTRUMENTS)
    title(fig, f"Ba đặc trưng đo trên {n:,} nốt đơn của dataset, theo nhạc cụ".replace(",", "."),
          "Mỗi chấm là một nốt; vạch đen ngang = trung vị, vạch đứng = khoảng 25%–75%.")
    save(fig, "07_features_by_instrument.png")


def fig_centroid_vs_pitch(groups):
    fig, ax = plt.subplots(figsize=(10, 4.4), facecolor=SURFACE)
    fig.subplots_adjust(left=0.08, right=0.86, bottom=0.17, top=0.8)
    style(ax)
    body = []
    for ins in INSTRUMENTS:
        by = defaultdict(list)
        for x in groups[ins]:
            by[int(x["midi"])].append(float(x["centroid_hz"]))
        ms = sorted(m for m in by if len(by[m]) >= 3)
        med = np.array([np.median(by[m]) for m in ms])
        sm = np.convolve(med, np.ones(3) / 3, mode="same")
        sm[0], sm[-1] = med[0], med[-1]
        ax.plot(ms, sm, color=INST_COLOR[ins], lw=2)
        ax.plot(ms[-1], sm[-1], "o", ms=6, color=INST_COLOR[ins], mec=SURFACE, mew=1.5)
        ax.text(ms[-1] + 1, sm[-1], VI[ins], color=INK, fontsize=8, va="center")
        for m, c in zip(ms, med):
            body.append([ins, m, midi_name(m), round(float(c), 1), len(by[m])])
    ax.plot([40, 100], [hz(40), hz(100)], color=MUTED, lw=1)
    ax.text(58, hz(58) * 0.8, "đường F0 (nếu centroid = F0)", color=MUTED, fontsize=7, va="top", rotation=17)
    ax.set_yscale("log")
    plain_log_ticks(ax, "y", [100, 200, 500, 1000, 2000, 4000])
    cs = list(range(24, 109, 12))
    ax.set_xticks(cs, [midi_name(m) for m in cs], fontsize=8)
    ax.set_xlabel("nốt được chơi", color=INK_2, fontsize=8)
    ax.set_ylabel("centroid (Hz, thang log)", color=INK_2, fontsize=8)
    title(fig, "Centroid tăng khi nốt cao lên, nhưng ở CÙNG một nốt, mỗi nhạc cụ một mức khác nhau",
          "Trung vị centroid của các nốt cùng cao độ (làm mượt 3 nốt). Khoảng cách tới đường F0 cho biết bồi âm cao mạnh tới đâu.")
    save(fig, "08_centroid_vs_pitch.png")
    write_rows("centroid_by_pitch.csv", ["instrument", "midi", "note", "centroid_median_hz", "n_notes"], body)


def fig_technique_dynamics(feats):
    tech = defaultdict(list)
    dyn = defaultdict(list)
    for f in feats:
        if f["instrument"] == "violin" and f["source"] == "philharmonia":   # 1 nguồn: không lẫn hiệu ứng phòng thu
            tech[f["technique"]].append(f)
            if f["technique"] == "arco-normal":
                dyn[f["dynamics"]].append(f)
    techs = sorted([t for t in tech if len(tech[t]) >= 10], key=lambda t: np.median([float(x["centroid_hz"]) for x in tech[t]]))
    dyns = [d for d in ("pianissimo", "piano", "mezzo-piano", "mezzo-forte", "forte", "fortissimo") if len(dyn[d]) >= 10]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), facecolor=SURFACE, gridspec_kw=dict(width_ratios=[1.5, 1]))
    fig.subplots_adjust(left=0.2, right=0.98, bottom=0.12, top=0.8, wspace=0.55)
    body = []
    for ax, groups, order, lab in ((axes[0], tech, techs, "Kỹ thuật chơi (violin)"),
                                   (axes[1], dyn, dyns, "Cường độ (violin, kéo vĩ thường)")):
        style(ax, grid_axis="x")
        for i, key in enumerate(order):
            v = np.array([float(x["centroid_hz"]) for x in groups[key]])
            q1, med, q3 = np.percentile(v, [25, 50, 75])
            ax.plot([q1, q3], [i, i], color=SLOTS[0], lw=2)
            ax.plot(med, i, "o", ms=7, color=SLOTS[0], mec=SURFACE, mew=1.5)
            rc = np.median([float(x["rms_cv"]) for x in groups[key]])
            body.append([lab, key, len(v), round(float(med), 1), round(float(q1), 1), round(float(q3), 1), round(float(rc), 3)])
        ax.set_yticks(range(len(order)), [f"{k} (n={len(groups[k])})" for k in order], fontsize=8)
        ax.set_xscale("log")
        plain_log_ticks(ax, "x", [1000, 1500, 2000, 3000, 4000])
        ax.set_xlabel("spectral centroid (Hz, thang log)", color=INK_2, fontsize=8)
        ax.set_title(lab, color=INK_2, fontsize=9, loc="left")
    title(fig, "Cách chơi và độ to đều làm thay đổi độ sáng (centroid) của cùng một nhạc cụ",
          "Chấm = trung vị, thanh = khoảng 25%–75% trên mọi nốt đơn violin (Philharmonia) có kỹ thuật/cường độ đó.", x=0.03)
    save(fig, "09_violin_technique_and_dynamics.png")
    write_rows("violin_technique_dynamics.csv", ["group", "value", "n", "centroid_median_hz", "centroid_q25", "centroid_q75",
                                                 "rms_cv_median"], body)


def fig_source_effect(feats):
    by = defaultdict(lambda: defaultdict(list))
    for f in feats:
        if f["path_kind"] == "notes":
            by[f["instrument"]][(f["source"], int(f["midi"]))].append(float(f["centroid_hz"]))
    fig, ax = plt.subplots(figsize=(9, 3.6), facecolor=SURFACE)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.17, top=0.78)
    style(ax, grid_axis="x")
    body = []
    for i, ins in enumerate(INSTRUMENTS):
        common = {m for (s, m) in by[ins] if s == "iowa"} & {m for (s, m) in by[ins] if s == "philharmonia"}
        vals = {}
        for s in ("philharmonia", "iowa"):
            vals[s] = float(np.median([c for (src, m), cs in by[ins].items() if src == s and m in common for c in cs]))
        ax.plot([vals["philharmonia"], vals["iowa"]], [i, i], color=BASELINE, lw=2)
        ax.plot(vals["philharmonia"], i, "o", ms=8, color=SLOTS[0], mec=SURFACE, mew=1.5)
        ax.plot(vals["iowa"], i, "o", ms=8, color=SLOTS[1], mec=SURFACE, mew=1.5)
        body.append([ins, len(common), round(vals["philharmonia"], 1), round(vals["iowa"], 1),
                     round(100 * (vals["iowa"] / vals["philharmonia"] - 1), 1)])
    ax.set_yticks(range(5), [VI[i] for i in INSTRUMENTS], fontsize=9)
    ax.set_ylim(4.6, -0.6)
    ax.set_xscale("log")
    plain_log_ticks(ax, "x", [500, 700, 1000, 1500, 2000, 2500])
    ax.set_xlabel("trung vị centroid (Hz, thang log), chỉ so các cao độ có ở cả hai nguồn", color=INK_2, fontsize=8)
    ax.plot([], [], "o", color=SLOTS[0], label="Philharmonia (phòng thu dàn nhạc)")
    ax.plot([], [], "o", color=SLOTS[1], label="Iowa (phòng tiêu âm)")
    ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=INK_2)
    title(fig, "Cùng nhạc cụ, cùng cao độ, khác phòng thu và micro → centroid cũng lệch",
          "Vì vậy project trộn cả hai nguồn vào mọi tập: để hệ thống học nhạc cụ, không học phòng thu.")
    save(fig, "10_recording_source_effect.png")
    write_rows("source_effect_centroid.csv", ["instrument", "n_common_pitches", "philharmonia_median_hz",
                                              "iowa_median_hz", "iowa_vs_phil_percent"], body)


def feature_sensitivity(feats):
    """Đặc trưng thay đổi thế nào khi đổi NỐT / NHẠC CỤ / NGUỒN THU — số liệu cho docs/01_THEORY/15_AUDIO_FEATURES.md.
    - rho_pitch_<nhạc cụ>: hệ số tương quan hạng Spearman giữa đặc trưng và số MIDI (+1: nốt càng cao giá trị càng lớn).
    - spread_instruments: trung vị lớn nhất / nhỏ nhất giữa 5 nhạc cụ (càng lớn càng phân biệt nhạc cụ tốt).
    - source_shift_pct: trung vị lệch của (Iowa / Philharmonia − 1) trên 5 nhạc cụ, chỉ so các cao độ chung."""
    from scipy.stats import spearmanr
    keys = ["centroid_hz", "bandwidth_hz", "rolloff_hz", "zcr", "rms_cv", "flatness"]
    notes = [f for f in feats if f["path_kind"] == "notes"]
    body = []
    for k in keys:
        row = [k]
        meds = []
        for ins in INSTRUMENTS:
            g = [f for f in notes if f["instrument"] == ins]
            rho = spearmanr([int(f["midi"]) for f in g], [float(f[k]) for f in g]).statistic
            row.append(round(float(rho), 2))
            meds.append(float(np.median([float(f[k]) for f in g])))
        row.append(round(max(meds) / min(meds), 2))
        shifts = []
        for ins in INSTRUMENTS:
            by = defaultdict(list)
            for f in notes:
                if f["instrument"] == ins:
                    by[(f["source"], int(f["midi"]))].append(float(f[k]))
            common = {m for (s, m) in by if s == "iowa"} & {m for (s, m) in by if s == "philharmonia"}
            mp = np.median([v for (s, m), vs in by.items() if s == "philharmonia" and m in common for v in vs])
            mi = np.median([v for (s, m), vs in by.items() if s == "iowa" and m in common for v in vs])
            shifts.append(100 * (mi / mp - 1))
        row.append(round(float(np.median(np.abs(shifts))), 1))
        body.append(row)
    write_rows("feature_sensitivity.csv", ["feature"] + [f"rho_pitch_{i}" for i in INSTRUMENTS]
               + ["spread_instruments", "source_shift_pct_median_abs"], body)
    unseen = [["instrument", "n"] + [f"{k}_median" for k in keys]]
    for ins in ("banjo", "mandolin"):
        g = [f for f in feats if f["instrument"] == ins]
        if g:
            unseen.append([ins, len(g)] + [round(float(np.median([float(f[k]) for f in g])), 4) for k in keys])
    write_rows("unseen_feature_summary.csv", unseen[0], unseen[1:])


INFO_FEATURES = [   # (cột trong note_features, nhãn, biến đổi giống FEATURE_SET)
    ("log2_f0", "log2 F0 (danh nghĩa)", None),
    ("centroid_hz", "log10 centroid", np.log10),
    ("bandwidth_hz", "log10 bandwidth", np.log10),
    ("rolloff_hz", "log10 rolloff", np.log10),
    ("zcr", "ZCR", None),
    ("rms_cv", "RMS-CV", None),
    ("flatness", "log10 flatness", np.log10),
] + [(f"mfcc{i}", f"MFCC c{i} mean", None) for i in range(1, 14)] + [
    (f"mfcc_std{i}", f"MFCC c{i} std", None) for i in range(1, 14)]


def eta_squared(values, labels):
    """Tỉ lệ phương sai giải thích được bởi nhóm: SS_giữa_nhóm / SS_tổng (0 = vô dụng, 1 = tách hoàn toàn)."""
    v, lab = np.asarray(values, float), np.asarray(labels)
    ss_tot = ((v - v.mean()) ** 2).sum()
    ss_b = sum((lab == c).sum() * (v[lab == c].mean() - v.mean()) ** 2 for c in np.unique(lab))
    return float(ss_b / ss_tot) if ss_tot > 0 else 0.0


def feature_information(feats):
    """Giá trị thông tin SƠ BỘ của từng đặc trưng (đo trên nốt đơn bằng script minh họa, chưa phải pipeline Bước 3):
    - eta2_instrument: nhạc cụ giải thích bao nhiêu % phương sai (càng cao càng phân biệt tốt);
    - eta2_violin_viola, eta2_cello_bass: như trên nhưng chỉ cho cặp khó;
    - abs_rho_pitch: trung vị |Spearman ρ| với số MIDI trên 5 nhạc cụ (đặc trưng đổi theo nốt nhiều hay ít);
    - eta2_source_within: trong cùng nhạc cụ và cùng các cao độ chung, nguồn thu giải thích bao nhiêu % phương sai
      (càng thấp càng ít bị phòng thu / micro ảnh hưởng)."""
    from scipy.stats import spearmanr
    notes = [f for f in feats if f["path_kind"] == "notes"]
    for f in notes:
        f["log2_f0"] = np.log2(hz(int(f["midi"])))
    body = []
    for key, label, tf in INFO_FEATURES:
        def val(f):
            x = float(f[key])
            return float(tf(max(x, 1e-6))) if tf else x
        vals = np.array([val(f) for f in notes])
        inst = np.array([f["instrument"] for f in notes])
        e_all = eta_squared(vals, inst)
        pair = lambda a, b: eta_squared(vals[(inst == a) | (inst == b)], inst[(inst == a) | (inst == b)])
        rhos = [abs(spearmanr([int(f["midi"]) for f in notes if f["instrument"] == i],
                              vals[inst == i]).statistic) for i in INSTRUMENTS]
        ss_w = ss_src = 0.0
        for i in INSTRUMENTS:
            g = [f for f in notes if f["instrument"] == i]
            common = ({int(f["midi"]) for f in g if f["source"] == "iowa"}
                      & {int(f["midi"]) for f in g if f["source"] == "philharmonia"})
            g = [f for f in g if int(f["midi"]) in common]
            v = np.array([val(f) for f in g])
            src = np.array([f["source"] for f in g])
            ss_w += ((v - v.mean()) ** 2).sum()
            ss_src += sum((src == s).sum() * (v[src == s].mean() - v.mean()) ** 2 for s in np.unique(src))
        plucked = np.where(inst == "guitar", "gảy", "kéo vĩ")
        body.append([label, round(e_all, 3), round(pair("violin", "viola"), 3), round(pair("cello", "double-bass"), 3),
                     round(float(np.median(rhos)), 2), round(ss_src / ss_w, 3), round(eta_squared(vals, plucked), 3)])
    write_rows("feature_information.csv", ["feature", "eta2_instrument", "eta2_violin_viola", "eta2_cello_bass",
                                           "abs_rho_pitch", "eta2_source_within", "eta2_guitar_vs_bowed"], body)
    return body


def fig_feature_information(body):
    """Thanh ngang: % phương sai do NHẠC CỤ (muốn cao) và do NGUỒN THU trong cùng nhạc cụ (muốn thấp)."""
    rows = sorted(body, key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(9.5, 1.8 + 0.27 * len(rows)), facecolor=SURFACE)
    fig.subplots_adjust(left=0.22, right=0.97, bottom=0.05, top=0.91)
    style(ax, grid_axis="x")
    y = np.arange(len(rows))
    h = 0.38
    ax.barh(y + h / 2, [100 * r[1] for r in rows], height=h - 0.04, color=SLOTS[0], label="do nhạc cụ (càng dài càng tốt)")
    ax.barh(y - h / 2, [100 * r[5] for r in rows], height=h - 0.04, color=SLOTS[1], label="do nguồn thu, trong cùng nhạc cụ (càng ngắn càng tốt)")
    for yi, r in zip(y, rows):
        ax.text(100 * r[1] + 0.8, yi + h / 2, f"{100 * r[1]:.0f}%", va="center", fontsize=7, color=INK_2)
        ax.text(100 * r[5] + 0.8, yi - h / 2, f"{100 * r[5]:.0f}%", va="center", fontsize=7, color=MUTED)
    ax.set_yticks(y, [r[0] for r in rows], fontsize=8, color=INK)
    ax.set_xlim(0, 60)
    ax.set_xlabel("% phương sai của đặc trưng (η²)", color=INK_2, fontsize=8)
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    title(fig, "Mỗi đặc trưng mang bao nhiêu thông tin về nhạc cụ?",
          "Đo sơ bộ trên 4 653 nốt đơn (script minh họa, chưa phải pipeline Bước 3). η² = tỉ lệ phương sai giải thích được.")
    save(fig, "15_feature_information.png")


VEC32 = (["mfcc%d" % i for i in range(1, 14)] + ["mfcc_std%d" % i for i in range(1, 14)]
         + ["centroid_hz", "bandwidth_hz", "rolloff_hz", "zcr", "rms_cv", "log2_f0"])   # thứ tự như FEATURE_SET


def pca_demo(feats):
    """Minh họa PCA trên vector 32D của từng NỐT ĐƠN (cùng bộ đặc trưng FEATURE_SET; F0 lấy theo tên nốt).
    Project thật làm PCA trên vector 52D của 500 sequence (Bước 9–10); đây chỉ để thấy PCA làm gì với dữ liệu thật."""
    notes = [f for f in feats if f["path_kind"] == "notes"]
    def val(f, k):
        x = float(f[k]) if k != "log2_f0" else np.log2(hz(int(f["midi"])))
        return np.log10(max(x, 1e-6)) if k in ("centroid_hz", "bandwidth_hz", "rolloff_hz") else x
    X = np.array([[val(f, k) for k in VEC32] for f in notes])
    Z = (X - X.mean(0)) / X.std(0)
    _, s, vt = np.linalg.svd(Z, full_matrices=False)
    ratio = s ** 2 / (s ** 2).sum()
    cum = np.cumsum(ratio)
    write_rows("pca_notes_explained.csv", ["component", "explained_ratio", "cumulative"],
               [[i + 1, round(float(r), 4), round(float(c), 4)] for i, (r, c) in enumerate(zip(ratio, cum))])
    load = [[VEC32[j], round(float(vt[0, j]), 3), round(float(vt[1, j]), 3)] for j in np.argsort(-np.abs(vt[0]))[:8]]
    write_rows("pca_notes_top_loadings.csv", ["feature", "pc1_loading", "pc2_loading"], load)
    # cận dưới: ‖W(a−b)‖ ≤ ‖a−b‖ trên 10 000 cặp ngẫu nhiên, với 8 thành phần
    rng = np.random.default_rng(0)
    i, j = rng.integers(0, len(Z), 10000), rng.integers(0, len(Z), 10000)
    full = np.linalg.norm(Z[i] - Z[j], axis=1)
    low = np.linalg.norm((Z[i] - Z[j]) @ vt[:8].T, axis=1)
    ok = full > 0
    write_rows("pca_lower_bound_check.csv", ["pairs", "max_ratio_8d_over_32d", "median_ratio", "violations"],
               [[int(ok.sum()), round(float((low[ok] / full[ok]).max()), 6), round(float(np.median(low[ok] / full[ok])), 3),
                 int((low[ok] > full[ok] + 1e-9).sum())]])
    P = Z @ vt[:2].T
    fig, ax = plt.subplots(figsize=(8.5, 6.2), facecolor=SURFACE)
    fig.subplots_adjust(left=0.09, right=0.97, bottom=0.1, top=0.84)
    style(ax, grid_axis=None)
    inst = np.array([f["instrument"] for f in notes])
    for k in INSTRUMENTS:
        m = inst == k
        ax.scatter(P[m, 0], P[m, 1], s=6, color=INST_COLOR[k], alpha=0.45, lw=0, label=VI[k])
    for k in INSTRUMENTS:   # nhãn trực tiếp ở trung vị mỗi đám
        m = inst == k
        cx, cy = np.median(P[m, 0]), np.median(P[m, 1])
        ax.text(cx, cy, VI[k], fontsize=9, weight="semibold", color=INK, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc=SURFACE, ec=INST_COLOR[k], lw=1.5))
    ax.axhline(0, color=GRID, lw=0.8, zorder=0)
    ax.axvline(0, color=GRID, lw=0.8, zorder=0)
    ax.set_xlabel(f"PC1 ({100 * ratio[0]:.0f}% phương sai)", color=INK_2, fontsize=8)
    ax.set_ylabel(f"PC2 ({100 * ratio[1]:.0f}% phương sai)", color=INK_2, fontsize=8)
    leg = ax.legend(loc="upper right", frameon=False, fontsize=8, markerscale=2.5)
    for h in leg.legend_handles:
        h.set_alpha(1)
    n_txt = f"{len(notes):,}".replace(",", " ")
    title(fig, "PCA: 32 đặc trưng của mỗi nốt, chiếu xuống 2 trục chính",
          f"{n_txt} nốt đơn (minh họa; project làm PCA trên vector 52D của sequence). "
          f"2 trục giữ {100 * cum[1]:.0f}%, 8 trục giữ {100 * cum[7]:.0f}% phương sai.")
    save(fig, "16_pca_notes_2d.png")
    src = np.array([f["source"] for f in notes])
    write_rows("pca_notes_axes_eta2.csv", ["component", "eta2_instrument", "eta2_source"],
               [[c + 1, round(eta_squared(Z @ vt[c], inst), 3), round(eta_squared(Z @ vt[c], src), 3)] for c in range(4)])
    return Z, notes


def source_transfer(Z, notes):
    """Láng giềng gần nhất (bỏ mọi nốt cùng cao độ, như quy tắc chia tập) có cùng nhạc cụ không,
    khi tìm TRONG cùng nguồn thu và khi tìm SANG nguồn kia. Đo cho 32D và cho 19D (bỏ 13 chiều MFCC std)."""
    inst = np.array([f["instrument"] for f in notes])
    src = np.array([f["source"] for f in notes])
    midi = np.array([int(f["midi"]) for f in notes])
    body = []
    for name, idx in (("32D", list(range(32))), ("19D (bỏ MFCC std)", list(range(13)) + list(range(26, 32)))):
        Zs = Z[:, idx]
        for qs, ds in (("iowa", "iowa"), ("iowa", "philharmonia"), ("philharmonia", "philharmonia"), ("philharmonia", "iowa")):
            q, d = np.where(src == qs)[0], np.where(src == ds)[0]
            D = (Zs[q] ** 2).sum(1)[:, None] + (Zs[d] ** 2).sum(1)[None, :] - 2 * Zs[q] @ Zs[d].T
            D[midi[q][:, None] == midi[d][None, :]] = np.inf
            ok = inst[d[D.argmin(1)]] == inst[q]
            body.append([name, qs, ds, len(q), round(float(ok.mean()), 3)]
                        + [round(float(ok[inst[q] == k].mean()), 2) for k in INSTRUMENTS])
    write_rows("source_transfer_1nn.csv", ["vector", "query_source", "db_source", "n_query", "accuracy"]
               + [f"acc_{k}" for k in INSTRUMENTS], body)


def fig_sampling():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.4), facecolor=SURFACE)
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.17, top=0.78, wspace=0.2)
    t = np.linspace(0, 0.002, 4000)
    fs = 8000
    ts = np.arange(0, 0.002, 1 / fs)
    ax = axes[0]
    style(ax)
    ax.plot(t * 1000, np.sin(2 * np.pi * 1000 * t), color=SLOTS[0], lw=2)
    ax.plot(ts * 1000, np.sin(2 * np.pi * 1000 * ts), "o", ms=6, color=INK, mec=SURFACE, mew=1.5)
    ax.set_title("(a) Sóng 1 000 Hz, lấy mẫu 8 000 lần/s: vẽ lại đúng", color=INK_2, fontsize=9, loc="left")
    ax = axes[1]
    style(ax)
    ax.plot(t * 1000, np.sin(2 * np.pi * 7000 * t), color=SLOTS[0], lw=1.2)
    ax.plot(t * 1000, -np.sin(2 * np.pi * 1000 * t), color=SLOTS[1], lw=2)
    ax.plot(ts * 1000, np.sin(2 * np.pi * 7000 * ts), "o", ms=6, color=INK, mec=SURFACE, mew=1.5)
    ax.text(0.02, -1.3, "các mẫu (chấm đen) nằm đúng trên một sóng 1 000 Hz “giả” (cam)", color=INK_2, fontsize=8)
    ax.set_ylim(-1.45, 1.2)
    ax.set_title("(b) Sóng 7 000 Hz, cũng 8 000 lần/s: thiếu mẫu → nhầm thành 1 000 Hz",
                 color=INK_2, fontsize=9, loc="left")
    for ax in axes:
        ax.set_xlabel("thời gian (ms)", color=INK_2, fontsize=8)
    title(fig, "Lấy mẫu (sampling) và giới hạn Nyquist: chỉ ghi đúng được tần số < một nửa tần số lấy mẫu")
    save(fig, "11_sampling_and_aliasing.png")


def fig_frames_spectrum(v):
    y = load_note(str(ROOT / v["path"]), seconds=1.0)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.7), facecolor=SURFACE, gridspec_kw=dict(width_ratios=[1.1, 1]))
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.17, top=0.78, wspace=0.18)
    ax = axes[0]
    style(ax, grid_axis=None)
    t = np.arange(len(y)) / SR
    ax.plot(t, y, color=SLOTS[0], lw=0.6)
    # frame k bắt đầu ở mẫu k·HOP; frame 10, 14, 18 nằm sát nhau (cách 4 bước nhảy = 2048 mẫu).
    # Các frame ở giữa (11, 12, 13…) chồng lên chúng 75% nên không tô, để hình dễ đọc.
    for j, c in enumerate((SLOTS[1], SLOTS[2], SLOTS[3])):
        k = 10 + j * 4
        s = k * HOP
        ax.axvspan(s / SR, (s + N_FFT) / SR, color=c, alpha=0.18, lw=0)
        ax.text((s + N_FFT / 2) / SR, 1.02 + 0.09 * j, f"frame {k}", color=INK_2, fontsize=7, ha="center")
    ax.set_ylim(-1.05, 1.3)
    ax.set_xlabel("thời gian (s)", color=INK_2, fontsize=8)
    ax.set_title("(a) Frame dài 2048 mẫu (≈ 93 ms); frame sau bắt đầu sau 512 mẫu (≈ 23 ms),\n"
                 "nên các frame chồng nhau 75%. Hình chỉ tô frame 10, 14, 18", color=INK_2, fontsize=9, loc="left")
    ax = axes[1]
    style(ax)
    s = 14 * HOP
    frame = y[s: s + N_FFT] * np.hanning(N_FFT)
    mag = np.abs(np.fft.rfft(frame))
    f = np.fft.rfftfreq(N_FFT, 1 / SR)
    db = 20 * np.log10(mag / mag.max() + 1e-6)
    ax.plot(f, db, color=SLOTS[0], lw=1.4)
    for k in range(1, 9):
        ax.text(k * 440, 4, f"{k}×", color=INK_2, fontsize=7, ha="center")
    ax.set_xlim(0, 4000)
    ax.set_ylim(-80, 10)
    ax.set_xlabel("tần số (Hz)", color=INK_2, fontsize=8)
    ax.set_ylabel("dB", color=INK_2, fontsize=8)
    ax.set_title("(b) FFT của frame 14: các đỉnh nằm ở 1×, 2×, 3× … 440 Hz", color=INK_2, fontsize=9, loc="left")
    title(fig, f"Từ dạng sóng tới phổ: {v['file']}")
    save(fig, "12_frames_and_spectrum.png")


def fig_mfcc_steps(v):
    y = load_note(str(ROOT / v["path"]), seconds=1.0)
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP)) ** 2
    frame = S[:, 14]
    mel_fb = librosa.filters.mel(sr=SR, n_fft=N_FFT, n_mels=40)
    mel = mel_fb @ frame
    logmel = 10 * np.log10(mel + 1e-10)
    import scipy.fftpack
    mfcc = scipy.fftpack.dct(logmel, type=2, norm="ortho")[:14]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7), facecolor=SURFACE)
    fig.subplots_adjust(left=0.05, right=0.99, bottom=0.17, top=0.76, wspace=0.28)
    ax = axes[0]
    style(ax)
    f = np.fft.rfftfreq(N_FFT, 1 / SR)
    ax.plot(f, 10 * np.log10(frame / frame.max() + 1e-10), color=SLOTS[0], lw=1)
    for b in range(0, 40, 6):
        on = mel_fb[b] > 0                                   # chỉ vẽ phần tam giác, bỏ đường nền bằng 0
        ax.plot(f[on], -78 + 18 * mel_fb[b][on] / mel_fb[b].max(), color=SLOTS[1], lw=1)
    ax.set_xlim(0, 8000)
    ax.set_ylim(-80, 5)
    ax.set_xlabel("tần số (Hz)", color=INK_2, fontsize=8)
    ax.set_title("(1) Phổ công suất + vài bộ lọc Mel (tam giác)", color=INK_2, fontsize=9, loc="left")
    ax = axes[1]
    style(ax)
    ax.bar(range(40), logmel - logmel.min(), color=SLOTS[0], width=0.7)
    ax.set_xlabel("dải Mel thứ … (thấp → cao)", color=INK_2, fontsize=8)
    ax.set_title("(2) Năng lượng 40 dải Mel, lấy log", color=INK_2, fontsize=9, loc="left")
    ax = axes[2]
    style(ax)
    ax.bar(range(1, 14), mfcc[1:], color=SLOTS[0], width=0.6)
    ax.axhline(0, color=BASELINE, lw=1)
    ax.set_xticks(range(1, 14), [f"c{k}" for k in range(1, 14)], fontsize=7)
    ax.set_title("(3) DCT → 13 hệ số MFCC (bỏ c0)", color=INK_2, fontsize=9, loc="left")
    title(fig, "MFCC tính như thế nào (một frame của nốt violin A4)",
          "Phổ → gom thành dải theo thang Mel (giống tai) → log (giống cảm nhận độ to) → DCT (tóm tắt hình dáng) → vài con số.")
    save(fig, "13_mfcc_steps.png")


def fig_vibrato(rows):
    def find(tech):
        c = [r for r in rows if r["instrument"] == "violin" and r["technique"] == tech and r["status"] == "OK"
             and r["duration_label"] != "phrase" and r["source"] == "philharmonia"]
        return c
    vib, non = find("molto-vibrato"), find("non-vibrato")
    common = sorted({r["midi"] for r in vib} & {r["midi"] for r in non}, key=int)
    if not common:
        note = None
    else:                                      # ưu tiên A4 cho thống nhất với các hình khác, nếu không có thì nốt giữa
        mid = "69" if "69" in common else common[len(common) // 2]
        note = next(r["note"] for r in vib if r["midi"] == mid)
    rv = max([r for r in vib if r["note"] == note], key=lambda r: float(r["active_sec"])) if note else vib[0]
    rn = max([r for r in non if r["note"] == note], key=lambda r: float(r["active_sec"])) if note else non[0]
    fig, ax = plt.subplots(figsize=(9, 3.6), facecolor=SURFACE)
    fig.subplots_adjust(left=0.09, right=0.8, bottom=0.17, top=0.78)
    style(ax)
    body = []
    for r, c, lab in ((rv, SLOTS[0], "molto vibrato"), (rn, SLOTS[1], "non vibrato")):
        y = load_note(str(ROOT / r["path"]), seconds=2.0)
        # Độ phân giải mặc định của pYIN (10 cent): thử 2 cent cho kết quả sai quãng tám, nên giữ mặc định
        # và chỉ làm mượt khi vẽ (trung bình trượt 5 frame ≈ 58 ms, ngắn hơn nhiều so với 1 chu kỳ vibrato).
        f0, vo, _ = librosa.pyin(y, fmin=150, fmax=2500, sr=SR, frame_length=2048, hop_length=256)
        tt = np.arange(len(f0)) * 256 / SR
        ref = hz(int(r["midi"]))
        cents = 1200 * np.log2(f0 / ref)
        ok = vo & np.isfinite(cents) & (tt > 0.2)        # bỏ 0.2 s đầu: lúc bắt đầu kéo vĩ cao độ chưa ổn định
        smooth = np.convolve(cents[ok], np.ones(5) / 5, mode="same")
        ax.plot(tt[ok][2:-2], smooth[2:-2], color=c, lw=1.8, label=lab)
        body.append([lab, r["file"], round(float(np.nanstd(cents[ok])), 1),
                     round(float(np.nanpercentile(cents[ok], 95) - np.nanpercentile(cents[ok], 5)), 1)])
    ax.axhline(0, color=BASELINE, lw=1)
    ax.set_ylim(-60, 60)
    ax.legend(loc="lower right", frameon=False, fontsize=8, labelcolor=INK_2)
    ax.set_ylabel("lệch so với nốt chuẩn (cent; 100 cent = 1 nửa cung)", color=INK_2, fontsize=8)
    ax.set_xlabel("thời gian (s)", color=INK_2, fontsize=8)
    title(fig, f"Vibrato: cao độ dao động quanh nốt chuẩn (violin {note})",
          f"{rv['file']}  vs  {rn['file']}")
    save(fig, "14_violin_vibrato_pitch.png")
    write_rows("vibrato.csv", ["technique", "file", "cents_std", "cents_range_p5_p95"], body)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--redo", action="store_true", help="đo lại đặc trưng (bỏ cache note_features.csv)")
    args = ap.parse_args()
    plt.rcParams["font.family"] = ["Segoe UI", "DejaVu Sans"]
    OUT.mkdir(parents=True, exist_ok=True)
    with CATALOG.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    feats = measure_all(rows, args.redo)
    for f in feats:
        f["path_kind"] = "notes" if f["split"] in ("REF", "DB_POOL", "QUERY_POOL") else "other"
    print("Vẽ hình ...")
    fig_sine()
    fig_harmonic_recipes()
    fig_same_note(rows)
    v, g = fig_envelope(rows)
    fig_spectrograms(v, g)
    fig_ranges()
    groups = feature_summary(feats)
    fig_features_by_instrument(groups)
    fig_centroid_vs_pitch(groups)
    fig_technique_dynamics(feats)
    fig_source_effect(feats)
    feature_sensitivity(feats)
    fig_feature_information(feature_information(feats))
    source_transfer(*pca_demo(feats))
    fig_sampling()
    fig_frames_spectrum(v)
    fig_mfcc_steps(v)
    fig_vibrato(rows)
    print(f"Đã ghi {OUT}")


if __name__ == "__main__":
    main()
