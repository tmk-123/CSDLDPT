"""Kiểm tra data/catalog.csv và các thư mục data/notes, data/queries, data/excluded (Bước 1.3–1.5).

Chạy:  .venv/Scripts/python tests/test_catalog.py      (hoặc pytest tests/ nếu đã cài pytest)
Yêu cầu: đã chạy scripts/p01_3_build_catalog.py.
"""
import csv
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPLITS = {"REF", "DB_POOL", "QUERY_POOL"}
CAPS = {"REF": 150, "DB_POOL": 200, "QUERY_POOL": 60}           # D23
RULE = {0: "REF", 1: "REF", 2: "DB_POOL", 3: "DB_POOL", 4: "QUERY_POOL"}  # D24: midi mod 5


def load():
    with (ROOT / "data" / "catalog.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


ROWS = load()


def test_every_file_has_exactly_one_row():
    on_disk = sum(len(fs) for d in ("notes", "queries", "excluded") for _, _, fs in os.walk(ROOT / "data" / d))
    assert on_disk == len(ROWS), f"{on_disk} file trên đĩa nhưng {len(ROWS)} dòng catalog"
    missing = [r["path"] for r in ROWS if not (ROOT / r["path"]).exists()]
    assert not missing, f"thiếu file: {missing[:5]}"


def test_known_problem_files():
    status = Counter(r["status"] for r in ROWS)
    assert status["CORRUPT"] == 1, status              # viola_D6_05_piano_arco-normal.mp3
    assert status["DUPLICATE"] == 4, status            # 2 cặp, đánh dấu cả hai file


def test_too_short_follows_rule():
    # Kiểm tra QUY TẮC thay vì một con số cố định: con số đổi khi đổi cách đo (vd thêm lọc thông cao, D27)
    bad_short = [r["file"] for r in ROWS if r["status"] == "TOO_SHORT" and float(r["active_sec"]) >= 0.35]
    bad_ok = [r["file"] for r in ROWS if r["status"] == "OK" and float(r["active_sec"]) < 0.35]
    assert not bad_short, f"TOO_SHORT nhưng phần có âm ≥ 0.35 s: {bad_short[:5]}"
    assert not bad_ok, f"OK nhưng phần có âm < 0.35 s: {bad_ok[:5]}"


def test_one_pitch_one_split():
    splits = defaultdict(set)
    for r in ROWS:
        if r["split"] in SPLITS:
            splits[(r["instrument"], r["midi"])].add(r["split"])
    leaked = {k: v for k, v in splits.items() if len(v) > 1}
    assert not leaked, f"cùng cao độ ở nhiều tập (rò rỉ): {list(leaked)[:5]}"


def test_split_follows_midi_mod_5():
    wrong = [r["file"] for r in ROWS if r["split"] in SPLITS and RULE[int(r["midi"]) % 5] != r["split"]]
    assert not wrong, wrong[:5]


def test_selection_within_caps():
    sel = Counter((r["instrument"], r["split"]) for r in ROWS if r["selected"] == "1")
    over = {k: v for k, v in sel.items() if v > CAPS[k[1]]}
    assert not over, over


def test_selected_uses_both_sources():
    sources = defaultdict(set)
    for r in ROWS:
        if r["split"] in SPLITS and r["selected"] == "1":
            sources[(r["instrument"], r["split"])].add(r["source"])
    single = [k for k, v in sources.items() if len(v) < 2]
    assert not single, f"chỉ có một nguồn (nguy cơ học nhầm nguồn thu): {single}"


def test_unseen_instruments_stay_out_of_database():
    leak = [r["file"] for r in ROWS if r["instrument"] in ("banjo", "mandolin")
            and r["path"].startswith("data/notes/")]
    assert not leak, leak[:5]


def test_bad_files_only_in_excluded():
    bad = [r["path"] for r in ROWS if r["status"] != "OK" and not r["path"].startswith("data/excluded/")]
    assert not bad, bad[:5]


def test_techniques_in_notes():
    def allowed(r):
        if r["instrument"] == "guitar":
            return r["technique_family"] in ("pluck", "harmonic")
        return r["technique_family"] == "arco"           # D20
    bad = [r["file"] for r in ROWS if r["path"].startswith("data/notes/") and not allowed(r)]
    assert not bad, bad[:5]


OPEN_STRINGS = {   # nhãn dây → MIDI của dây buông (docs/01_THEORY/05–09)
    "violin": {"G": 55, "D": 62, "A": 69, "E": 76},
    "viola": {"C": 48, "G": 55, "D": 62, "A": 69},
    "cello": {"C": 36, "G": 43, "D": 50, "A": 57},
    "double-bass": {"E": 28, "A": 33, "D": 38, "G": 43},
    "guitar": {"lowE": 40, "A": 45, "D": 50, "G": 55, "B": 59, "highE": 64},
}


def test_iowa_string_labels_match_physics():
    # Nhãn dây phải là một dây có thật của nhạc cụ, và nốt không thể thấp hơn dây buông
    # (bấm dây chỉ làm nốt CAO lên). Bắt lỗi kiểu gộp hai dây Mi của guitar thành một nhãn "E".
    iowa = [r for r in ROWS if r["source"] == "iowa"]
    unknown = [r["file"] for r in iowa if r["string"] not in OPEN_STRINGS[r["instrument"]]]
    below = [r["file"] for r in iowa if r["string"] in OPEN_STRINGS[r["instrument"]]
             and int(r["midi"]) < OPEN_STRINGS[r["instrument"]][r["string"]]]
    assert not unknown, f"nhãn dây không có trên nhạc cụ: {unknown[:5]}"
    assert not below, f"nốt thấp hơn dây buông: {below[:5]}"


def test_enough_notes_per_instrument():
    usable = Counter(r["instrument"] for r in ROWS if r["split"] in SPLITS)
    short = {i: n for i, n in usable.items() if n < 360}
    assert not short, f"dưới mức cần 360 nốt: {short}"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    failed = 0
    for name, fn in sorted((k, v) for k, v in globals().items() if k.startswith("test_")):
        try:
            fn()
            print(f"ĐẠT   {name}")
        except AssertionError as e:
            failed += 1
            print(f"LỖI   {name}: {e}")
    print(f"\n{len([k for k in globals() if k.startswith('test_')]) - failed} đạt, {failed} lỗi")
    sys.exit(1 if failed else 0)
