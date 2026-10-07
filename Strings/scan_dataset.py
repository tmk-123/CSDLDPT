import csv
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

# Thư mục chứa 7 thư mục nhạc cụ
DATA_DIR = Path(r"D:\Ki1_4\HCSDLDPT\Strings")
OUTPUT_FILE = DATA_DIR / "metadata_strings.csv"


def read_metadata(file_path):
    """Dùng ffprobe đọc thông tin âm thanh."""
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries",
        "format=duration:stream=sample_rate,channels",
        "-of", "json",
        str(file_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "ffprobe không đọc được file"
        )

    info = json.loads(result.stdout)
    streams = info.get("streams", [])

    if not streams:
        raise ValueError("Không tìm thấy luồng âm thanh")

    stream = streams[0]
    duration = info.get("format", {}).get("duration")

    return {
        "duration_sec": float(duration) if duration else "",
        "sample_rate_hz": stream.get("sample_rate", ""),
        "channels": stream.get("channels", ""),
    }


def main():
    if not DATA_DIR.is_dir():
        print(f"Không tìm thấy thư mục: {DATA_DIR}")
        return

    if shutil.which("ffprobe") is None:
        print("Không tìm thấy ffprobe. Hãy đóng và mở lại VS Code.")
        return

    files = sorted(
        path for path in DATA_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() == ".mp3"
    )

    if not files:
        print("Không tìm thấy file MP3.")
        return

    columns = [
        "file_name",
        "instrument",
        "note",
        "duration_label",
        "dynamics",
        "technique",
        "duration_sec",
        "sample_rate_hz",
        "channels",
        "size_bytes",
        "status",
        "error",
        "relative_path",
    ]

    instrument_counts = Counter()
    status_counts = Counter()

    # utf-8-sig giúp Excel đọc tiếng Việt.
    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8-sig"
    ) as output:
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()

        for index, file_path in enumerate(files, start=1):
            print(f"[{index}/{len(files)}] {file_path.name}")

            # Chia tối đa thành 5 phần, giữ nguyên tên kỹ thuật.
            parts = file_path.stem.split("_", 4)
            valid_name = len(parts) == 5
            parts += [""] * (5 - len(parts))

            row = {
                "file_name": file_path.name,
                "instrument": parts[0],
                "note": parts[1],
                "duration_label": parts[2],
                "dynamics": parts[3],
                "technique": parts[4],
                "duration_sec": "",
                "sample_rate_hz": "",
                "channels": "",
                "size_bytes": "",
                "status": "OK",
                "error": "",
                "relative_path": file_path.relative_to(
                    DATA_DIR
                ).as_posix(),
            }

            flags = []

            if not valid_name:
                flags.append("TEN_KHONG_DUNG_MAU")

            try:
                row["size_bytes"] = file_path.stat().st_size
                row.update(read_metadata(file_path))

                if row["duration_sec"] == "":
                    flags.append("THIEU_THOI_LUONG")
                elif row["duration_sec"] <= 0:
                    flags.append("THOI_LUONG_KHONG_HOP_LE")

            except Exception as error:
                flags.append("LOI_DOC_THONG_TIN")
                row["error"] = str(error)

            row["status"] = ";".join(flags) if flags else "OK"

            writer.writerow(row)
            instrument_counts[row["instrument"]] += 1
            status_counts[row["status"]] += 1

    print("\n===== HOÀN THÀNH =====")
    print(f"Tổng số file: {len(files)}")
    print(f"Kết quả: {OUTPUT_FILE}")

    print("\nSố file theo nhạc cụ:")
    for instrument, count in sorted(instrument_counts.items()):
        print(f"  {instrument}: {count}")

    print("\nTrạng thái:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()