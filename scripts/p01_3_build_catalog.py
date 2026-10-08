"""Bước 1.3–1.5: catalog hợp nhất, lọc, chia tập, rồi sắp xếp file theo nhạc cụ.

Đầu vào (chỉ đọc):
  raw/philharmonia/<instrument>/*.mp3                 nốt đơn + phrase Philharmonia
  data/interim/iowa_notes/notes.csv + <instrument>/   nốt đơn cắt từ Iowa (scripts/p01_2_slice_iowa.py)

Đầu ra (tạo lại hoàn toàn mỗi lần chạy):
  data/catalog.csv                         mỗi file một dòng: nguồn, nhạc cụ, cao độ, status, split, selected
  data/notes/<instrument>/<source>/        nốt đơn dùng được của 5 nhạc cụ trong CSDL
  data/queries/unseen/<instrument>/        banjo, mandolin: truy vấn nhạc cụ ngoài CSDL
  data/queries/phrases/<instrument>/       đoạn phrase thật: truy vấn nhạc thật
  data/excluded/<reason>/<instrument>/     không dùng (corrupt, duplicate, too_short, technique)

Quy tắc: docs/04_PART_1/01_DATASET/DATASET_COLLECTION_AND_FILTERING.md và SPLIT_AND_LEAKAGE.md
"""
import csv
import hashlib
import random
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfiltfilt

ROOT = Path(__file__).resolve().parents[1]
RAW_PHIL = ROOT / "raw" / "philharmonia"
IOWA_NOTES = ROOT / "data" / "interim" / "iowa_notes"
DATA = ROOT / "data"

SR = 22050
HOP = 512
ACTIVE_DB = -40          # phần có âm: RMS > −40 dB so với đỉnh
MIN_ACTIVE_SEC = 0.35    # D22
SEED = 42

IN_DATABASE = ["violin", "viola", "cello", "double-bass", "guitar"]
UNSEEN = ["banjo", "mandolin"]
ALLOWED_FAMILY = {"guitar": {"pluck", "harmonic"}}   # bộ kéo vĩ: chỉ arco (D20)
CAPS = {"REF": 150, "DB_POOL": 200, "QUERY_POOL": 60}  # D23: số nốt được chọn tối đa / nhạc cụ
# D27: lọc thông cao 25 Hz (Butterworth bậc 4, không lệch pha) bỏ tiếng ù hạ âm có trong nhiều bản thu
# (Iowa guitar: 93% năng lượng dưới 20 Hz). Nốt thấp nhất của 5 nhạc cụ là C1 = 32.7 Hz → chỉ giảm ~1 dB.
HP_SOS = butter(4, 25, btype="highpass", fs=SR, output="sos")


def highpass(y):
    return sosfiltfilt(HP_SOS, y).astype(np.float32) if len(y) > 64 else y

PC = {"C": 0, "Cs": 1, "D": 2, "Ds": 3, "E": 4, "F": 5, "Fs": 6, "G": 7, "Gs": 8, "A": 9, "As": 10, "B": 11}


def note_to_midi(note):
    return 12 * (int(note[-1]) + 1) + PC[note[:-1]]


def technique_family(instrument, technique):
    if instrument in ("guitar", "banjo", "mandolin"):
        return "harmonic" if "harmonic" in technique else "pluck"
    if technique in ("arco-normal", "molto-vibrato", "non-vibrato"):
        return "arco"
    if technique == "pizz-normal":
        return "pizz"
    return "special"


def measure(path):
    """Giải mã → mono 22 050 Hz; đo thời lượng, phần có âm, đỉnh, số mẫu clipping, MD5."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR),
                        "-f", "f32le", "-"], capture_output=True)
    y = np.frombuffer(r.stdout, dtype=np.float32)
    out = {"md5": hashlib.md5(path.read_bytes()).hexdigest(), "decode_error": ""}
    if len(y) == 0:
        # chỉ giữ dòng đầu (CSV một dòng / file, mở bằng Excel không vỡ dòng) và bỏ tiền tố
        # "[in#0 @ 000002f7…]" của ffmpeg: địa chỉ bộ nhớ đổi mỗi lần chạy → catalog không ổn định
        first = (r.stderr.decode(errors="replace").strip().splitlines() or ["empty"])[0]
        out.update(duration_sec=0.0, active_sec=0.0, peak=0.0, clipped=0,
                   decode_error=re.sub(r"^\[[^\]]*@ [0-9a-fA-Fx]+\]\s*", "", first)[:100])
        return out
    clipped = int((np.abs(y) >= 0.999).sum())          # clipping đo trên tín hiệu gốc
    y = highpass(y)                                     # phần có âm, đỉnh: đo sau khi bỏ tiếng ù hạ âm (D27)
    n = max(len(y) // HOP, 1)
    rms = np.sqrt((y[: n * HOP].reshape(n, -1) ** 2).mean(1) + 1e-12) if len(y) >= HOP else np.array([1.0])
    active = np.where(20 * np.log10(rms / rms.max()) > ACTIVE_DB)[0]
    out.update(duration_sec=round(len(y) / SR, 3),
               active_sec=round((active[-1] - active[0] + 1) * HOP / SR, 3) if len(active) else 0.0,
               peak=round(float(np.abs(y).max()), 4),
               clipped=clipped)
    return out


def collect():
    rows = []
    for p in sorted(RAW_PHIL.rglob("*.mp3")):
        instrument, note, dur_label, dynamics, technique = p.stem.split("_", 4)
        rows.append({"source": "philharmonia", "raw_path": p.relative_to(ROOT).as_posix(),
                     "file": p.name, "instrument": instrument, "note": note, "midi": note_to_midi(note),
                     "duration_label": dur_label, "dynamics": dynamics, "technique": technique,
                     "string": "", "parent_file": ""})
    with (IOWA_NOTES / "notes.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            p = IOWA_NOTES / r["instrument"] / r["file"]
            rows.append({"source": "iowa", "raw_path": p.relative_to(ROOT).as_posix(),
                         "file": r["file"], "instrument": r["instrument"], "note": r["note"],
                         "midi": int(r["midi"]), "duration_label": "", "dynamics": r["dynamics"],
                         "technique": r["technique"], "string": r["string"], "parent_file": r["parent_file"]})
    return rows


def assign_status_and_split(rows):
    md5_count = Counter(r["md5"] for r in rows)
    for r in rows:
        r["technique_family"] = technique_family(r["instrument"], r["technique"])
        if r["decode_error"]:
            r["status"] = "CORRUPT"
        elif md5_count[r["md5"]] > 1:
            r["status"] = "DUPLICATE"
        elif r["active_sec"] < MIN_ACTIVE_SEC:
            r["status"] = "TOO_SHORT"
        else:
            r["status"] = "OK"
        r["flags"] = ";".join(f for f, on in (("LOW_LEVEL", r["peak"] < 0.01), ("CLIPPED", r["clipped"] > 0)) if on)

        allowed = ALLOWED_FAMILY.get(r["instrument"], {"arco"})
        if r["status"] != "OK":
            r["split"], r["reason"] = "NONE", r["status"].lower()
        elif r["instrument"] in UNSEEN:
            r["split"], r["reason"] = "UNSEEN", ""
        elif r["duration_label"] == "phrase":
            r["split"], r["reason"] = "PHRASE", ""
        elif r["technique_family"] not in allowed:
            r["split"], r["reason"] = "NONE", "technique"
        else:
            g = r["midi"] % 5     # chia theo cao độ, xen kẽ (D02, D24)
            r["split"] = "REF" if g in (0, 1) else "DB_POOL" if g in (2, 3) else "QUERY_POOL"
            r["reason"] = ""
        r["selected"] = 0


def select_within_caps(rows):
    """D23: mỗi (nhạc cụ, split) chọn tối đa CAPS nốt, trải đều theo (nguồn, cao độ, cường độ);
    phần còn lại là dự trữ (selected = 0), vẫn cùng split nên không gây rò rỉ."""
    rng = random.Random(SEED)
    groups = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["split"] in CAPS:
            groups[(r["instrument"], r["split"])][(r["source"], r["midi"], r["dynamics"])].append(r)
    for (instrument, split), buckets in groups.items():
        keys = sorted(buckets)
        rng.shuffle(keys)
        for k in keys:
            rng.shuffle(buckets[k])
        chosen, cap = 0, CAPS[split]
        while chosen < cap and any(buckets[k] for k in keys):
            for k in keys:                     # round-robin: mỗi nhóm lấy 1 nốt mỗi vòng
                if buckets[k] and chosen < cap:
                    buckets[k].pop()["selected"] = 1
                    chosen += 1


def organize(rows):
    for sub in ("notes", "queries", "excluded"):
        shutil.rmtree(DATA / sub, ignore_errors=True)
    for r in rows:
        if r["split"] in CAPS:
            dest = DATA / "notes" / r["instrument"] / r["source"]
        elif r["split"] == "UNSEEN":
            dest = DATA / "queries" / "unseen" / r["instrument"]
        elif r["split"] == "PHRASE":
            dest = DATA / "queries" / "phrases" / r["instrument"]
        else:
            dest = DATA / "excluded" / r["reason"] / r["instrument"]
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / r["raw_path"], dest / r["file"])
        r["path"] = (dest / r["file"]).relative_to(ROOT).as_posix()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rows = collect()
    print(f"Đo {len(rows)} file ...")
    with ThreadPoolExecutor(8) as ex:
        for r, m in zip(rows, ex.map(lambda r: measure(ROOT / r["raw_path"]), rows)):
            r.update(m)
    assign_status_and_split(rows)
    select_within_caps(rows)
    organize(rows)

    for i, r in enumerate(rows, 1):
        r["recording_id"] = i
    fields = ["recording_id", "source", "instrument", "note", "midi", "dynamics", "technique",
              "technique_family", "string", "duration_label", "duration_sec", "active_sec", "peak",
              "clipped", "md5", "status", "flags", "split", "selected", "reason", "path", "raw_path",
              "parent_file", "file", "decode_error"]
    with (DATA / "catalog.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print("\nStatus:", dict(Counter(r["status"] for r in rows)))
    print("Loại vì kỹ thuật:", sum(r["reason"] == "technique" for r in rows))
    print(f"\n{'nhạc cụ':12s} {'nguồn':13s} " + " ".join(f"{s:>10s}" for s in ("REF", "DB_POOL", "QUERY_POOL")) + "   (chọn/có)")
    for ins in IN_DATABASE:
        for src in ("philharmonia", "iowa", "*"):
            cells = []
            for s in ("REF", "DB_POOL", "QUERY_POOL"):
                sub = [r for r in rows if r["instrument"] == ins and r["split"] == s and (src == "*" or r["source"] == src)]
                cells.append(f"{sum(r['selected'] for r in sub):>4d}/{len(sub):<5d}")
            print(f"{ins:12s} {('TỔNG' if src == '*' else src):13s} " + " ".join(cells))
    print("\nUNSEEN:", dict(Counter(r["instrument"] for r in rows if r["split"] == "UNSEEN")),
          " PHRASE:", dict(Counter(r["instrument"] for r in rows if r["split"] == "PHRASE")))
    print(f"\nĐã ghi {DATA / 'catalog.csv'}")


if __name__ == "__main__":
    main()
