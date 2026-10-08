"""Bước 1.2: cắt file Iowa MIS (mỗi file = nhiều nốt chromatic tăng dần) thành từng nốt đơn.

Thuật toán (docs/04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md, Bước 1.2):
  1. Ứng viên onset: SuperFlux (librosa onset_strength lag=2, max_size=3) + backtrack.
  2. Đo cao độ (pYIN) trong 0.1–0.6 s sau mỗi ứng viên; bỏ ứng viên không có cao độ rõ.
  3. Ước lượng độ lệch lên dây của cả file (median phần lẻ nửa cung), làm tròn về MIDI.
  4. Ghép tuần tự với dãy nốt dự kiến lấy từ tên file (vd E2B2 → E2..B2);
     ứng viên trùng cao độ với nốt vừa ghép bị bỏ (dao động trong đuôi ngân).
  5. Cắt nốt từ onset tới onset kế tiếp (tối đa MAX_NOTE_SEC), bỏ đuôi lặng.

Đầu vào : raw/iowa_mis/<instrument>/*.aif(f)
Đầu ra  : data/interim/iowa_notes/<instrument>/<instrument>_<note>_<dynamics>_<technique>_<string>_<range>.wav
          data/interim/iowa_notes/notes.csv         (mỗi nốt một dòng)
          data/interim/iowa_notes/slice_report.csv  (mỗi file gốc một dòng)

    .venv/Scripts/python scripts/p01_2_slice_iowa.py [--fresh]
"""
import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "raw" / "iowa_mis"
OUT = ROOT / "data" / "interim" / "iowa_notes"

SR = 44100            # giữ nguyên chất lượng gốc; load_audio sẽ đổi về 22 050 Hz sau
SR_PITCH = 22050      # chỉ dùng để đo cao độ (nhanh hơn)
ALGO_VERSION = 3      # tăng khi đổi thuật toán ⇒ cache cũ bị bỏ, file được cắt lại
HOP = 512
MAX_NOTE_SEC = 6.0    # project chỉ dùng tối đa 1.5 s mỗi nốt; 6 s là dư
TOP_DB_TAIL = 40      # cắt đuôi lặng: −40 dB so với đỉnh của nốt
PITCH_TOL = 0.6       # nửa cung, sau khi đã bù độ lệch lên dây

PC = {"C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "Gb": 6, "G": 7,
      "Ab": 8, "A": 9, "Bb": 10, "B": 11}
NAMES = ["C", "Cs", "D", "Ds", "E", "F", "Fs", "G", "Gs", "A", "As", "B"]  # quy ước tên file Strings/
DYN = {"pp": "pianissimo", "mf": "mezzo-forte", "ff": "fortissimo"}
FMIN = {"guitar": 70, "violin": 180, "viola": 120, "cello": 60, "double-bass": 35}
FMAX = {"guitar": 1100, "violin": 4200, "viola": 2100, "cello": 1200, "double-bass": 500}


def note_to_midi(n):
    m = re.fullmatch(r"([A-G]b?)(\d)", n)
    return 12 * (int(m.group(2)) + 1) + PC[m.group(1)]


def midi_to_name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def parse_name(path, instrument):
    """Iowa: Violin.arco.pp.sulG.G3B3.aiff · Viola.arco.sulC.pp.C3B3.aiff · Guitar.pp.sulE.E2B2.aif"""
    tokens = path.stem.split(".")
    dyn = next(t for t in tokens if t in DYN)
    sul = next(t for t in tokens if t.lower().startswith("sul"))
    string = sul.replace("sul_", "sul").replace("sul", "")
    if instrument == "guitar" and string == "E":   # guitar có hai dây Mi: Iowa ghi "sulE" = Mi trầm (dây 6, E2)
        string = "highE" if sul.startswith("sul_") else "lowE"   # và "sul_E" = Mi cao (dây 1, E4)
    rng = next(t for t in reversed(tokens) if re.fullmatch(r"([A-G]b?\d){1,2}", t))
    notes = re.findall(r"[A-G]b?\d", rng)
    lo, hi = note_to_midi(notes[0]), note_to_midi(notes[-1])
    technique = "normal" if instrument == "guitar" else "arco-normal"
    return {"dyn": DYN[dyn], "string": string, "expected": list(range(lo, hi + 1)),
            "technique": technique, "range": rng}


def candidate_pitches(y_pitch, onsets, instrument):
    """Median f0 (MIDI, số thực) trong 0.1–0.6 s sau mỗi onset; NaN nếu không có cao độ rõ.
    Đo trên bản 22 050 Hz (nhanh gấp ~2 lần, đủ cho f0 ≤ 4.2 kHz); onsets tính theo mẫu 44.1 kHz."""
    ratio = SR_PITCH / SR
    out = []
    for s in onsets:
        a = int(s * ratio)
        seg = y_pitch[a + int(0.1 * SR_PITCH): a + int(0.6 * SR_PITCH)]
        if len(seg) < int(0.2 * SR_PITCH):
            out.append(np.nan)
            continue
        f0, voiced, _ = librosa.pyin(seg, fmin=FMIN[instrument], fmax=FMAX[instrument],
                                     sr=SR_PITCH, frame_length=2048, hop_length=256)
        f0 = f0[voiced]
        out.append(float(np.median(librosa.hz_to_midi(f0))) if len(f0) >= 3 else np.nan)
    return np.array(out)


def slice_file(path, instrument):
    meta = parse_name(path, instrument)
    y, _ = librosa.load(path, sr=SR, mono=True)
    env = librosa.onset.onset_strength(y=y, sr=SR, hop_length=HOP, lag=2, max_size=3)
    onsets = librosa.onset.onset_detect(onset_envelope=env, sr=SR, hop_length=HOP,
                                        backtrack=True, units="samples")
    pitches = candidate_pitches(librosa.resample(y, orig_sr=SR, target_sr=SR_PITCH), onsets, instrument)
    valid = ~np.isnan(pitches)
    frac = pitches[valid] - np.round(pitches[valid])
    tuning = float(np.median(frac)) if valid.any() else 0.0

    # ghép tuần tự với dãy nốt dự kiến
    matched, k, last_midi = [], 0, None
    for s, p in zip(onsets, pitches):
        if np.isnan(p) or k >= len(meta["expected"]):
            continue
        m = int(np.round(p - tuning))
        if m == last_midi:
            continue                                  # vẫn là nốt trước (đuôi ngân / vĩ đổi chiều)
        target = meta["expected"][k]
        dev = p - tuning - target
        # pYIN hay sai đúng một/hai quãng tám ở âm vực cao/thấp; tên file cho quãng tám thật.
        # Chỉ chấp nhận khi lệch ĐÚNG bội của 12 so với target, để không nhận nhầm bồi âm khác.
        octave_err = abs(m - target) in (12, 24) and abs(dev - np.round(dev / 12) * 12) <= PITCH_TOL
        if abs(dev) <= PITCH_TOL or octave_err:
            matched.append((s, target, p, dev - np.round(dev / 12) * 12))
            last_midi, k = target, k + 1
        elif m in meta["expected"][k + 1:k + 3]:      # nhảy cóc tối đa 2 nốt: thiếu nốt target
            k = meta["expected"].index(m, k)
            matched.append((s, m, p, p - tuning - m))
            last_midi, k = m, k + 1

    rows = []
    for i, (s, midi, p, dev) in enumerate(matched):
        end = matched[i + 1][0] if i + 1 < len(matched) else len(y)
        end = min(end, s + int(MAX_NOTE_SEC * SR))
        seg = y[s:end]
        _, (_, tail) = librosa.effects.trim(seg, top_db=TOP_DB_TAIL)
        seg = seg[:tail]
        # luôn kèm khoảng nốt của file gốc ⇒ tên duy nhất và cố định giữa các lần chạy
        # (cùng một nốt có thể xuất hiện ở hai file có khoảng chồng nhau, vd C2Gb2 và Gb2D3)
        name = f"{instrument}_{midi_to_name(midi)}_{meta['dyn']}_{meta['technique']}_{meta['string']}_{meta['range']}.wav"
        dest = OUT / instrument / name
        sf.write(dest, seg, SR, subtype="PCM_16")
        rows.append({"file": dest.name, "parent_file": path.name, "instrument": instrument,
                     "note": midi_to_name(midi), "midi": midi, "dynamics": meta["dyn"],
                     "technique": meta["technique"], "string": meta["string"],
                     "onset_sec": round(s / SR, 3), "duration_sec": round(len(seg) / SR, 3),
                     "pitch_dev_semitone": round(float(dev), 2)})
    found = {r["midi"] for r in rows}
    missing = [midi_to_name(m) for m in meta["expected"] if m not in found]
    report = {"parent_file": path.name, "instrument": instrument, "expected": len(meta["expected"]),
              "candidates": len(onsets), "matched": len(rows), "missing": " ".join(missing),
              "tuning_offset": round(tuning, 2)}
    return rows, report


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # terminal Windows mặc định cp1252, không in được tiếng Việt
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", action="store_true", help="bỏ cache, cắt lại mọi file từ đầu")
    args = ap.parse_args()
    instruments = sorted(d.name for d in SRC.iterdir() if d.is_dir())
    if args.fresh:
        shutil.rmtree(OUT / "_cache", ignore_errors=True)

    # Chạy tiếp được: mỗi file gốc cắt xong được lưu vào _cache/<instrument>/<file>.json;
    # lần chạy sau bỏ qua file đã có cache cùng ALGO_VERSION (máy tắt giữa chừng không mất công).
    all_rows, reports = [], []
    for instrument in instruments:
        (OUT / instrument).mkdir(parents=True, exist_ok=True)
        cache_dir = OUT / "_cache" / instrument
        cache_dir.mkdir(parents=True, exist_ok=True)
        files = sorted(p for p in (SRC / instrument).iterdir() if p.suffix.lower() in (".aif", ".aiff"))
        kept = set()
        for path in files:
            cache = cache_dir / (path.stem + ".json")
            data = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else None
            if data and data["algo_version"] == ALGO_VERSION and all(
                    (OUT / instrument / r["file"]).exists() for r in data["rows"]):
                rows, rep, tag = data["rows"], data["report"], "(cache)"
            else:
                rows, rep = slice_file(path, instrument)
                cache.write_text(json.dumps({"algo_version": ALGO_VERSION, "rows": rows, "report": rep},
                                            ensure_ascii=False), encoding="utf-8")
                tag = ""
            all_rows += rows
            reports.append(rep)
            kept |= {r["file"] for r in rows}
            flag = "" if rep["matched"] == rep["expected"] else f"  thiếu: {rep['missing']}"
            print(f"{instrument:12s} {path.name:34s} dự kiến {rep['expected']:2d}  cắt được {rep['matched']:2d}{flag} {tag}",
                  flush=True)
        for stale in (OUT / instrument).glob("*.wav"):   # file của lần chạy cũ không còn khớp
            if stale.name not in kept:
                stale.unlink()

    for name, data in (("notes.csv", all_rows), ("slice_report.csv", reports)):
        if not data:
            continue
        mode_path = OUT / name
        with mode_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            w.writeheader()
            w.writerows(data)
    exp = sum(r["expected"] for r in reports)
    got = sum(r["matched"] for r in reports)
    print(f"TỔNG: dự kiến {exp} nốt, cắt được {got} ({got / max(exp, 1):.0%})")


if __name__ == "__main__":
    main()
