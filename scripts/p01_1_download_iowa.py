"""Bước 1.1: tải file arco (16-bit, 44.1 kHz, mono) của Iowa MIS cho 4 nhạc cụ kéo vĩ.

Nguồn: https://theremin.music.uiowa.edu/MIS.html (bản pre-2012).
Kết quả: raw/iowa_mis/<instrument>/*.aiff và raw/iowa_mis/<instrument>/_download/manifest.csv
Chạy lại an toàn: file đã tải đủ dung lượng sẽ được bỏ qua.

    python scripts/p01_1_download_iowa.py            # tải
    python scripts/p01_1_download_iowa.py --dry-run  # chỉ liệt kê, không tải
"""
import argparse
import csv
import hashlib
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://theremin.music.uiowa.edu/"
PAGES = {
    "violin": "MISviolin.html",
    "viola": "MISviola.html",
    "cello": "MIScello.html",
    "double-bass": "MISdoublebass.html",
}
ROOT = Path(__file__).resolve().parents[1] / "raw" / "iowa_mis"


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception as e:  # mạng chập chờn: thử lại
            if attempt == retries - 1:
                raise
            print(f"   thử lại ({e})")
            time.sleep(3)


def remote_size(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers.get("Content-Length", -1))


def arco_links(page):
    html = fetch(BASE + page).decode("utf-8", errors="replace")
    links = re.findall(r'href="([^"]+\.aiff?)"', html, flags=re.I)
    return [l for l in links if ".arco." in l.lower()]


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # terminal Windows mặc định cp1252, không in được tiếng Việt
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    for instrument, page in PAGES.items():
        links = arco_links(page)
        out_dir = ROOT / instrument
        print(f"== {instrument}: {len(links)} file arco")
        if args.dry_run:
            for l in links:
                print("   ", l.split("/")[-1])
            continue
        (out_dir / "_download").mkdir(parents=True, exist_ok=True)
        rows = []
        for i, link in enumerate(links, 1):
            url = BASE + urllib.parse.quote(link)
            dest = out_dir / link.split("/")[-1]
            if dest.exists() and dest.stat().st_size == remote_size(url):
                data = dest.read_bytes()
                status = "skip"
            else:
                data = fetch(url)
                tmp = dest.with_suffix(dest.suffix + ".part")  # tải dở không bao giờ mang tên thật
                tmp.write_bytes(data)
                tmp.replace(dest)
                status = "ok"
            rows.append({"file": dest.name, "url": url, "bytes": len(data),
                         "md5": hashlib.md5(data).hexdigest()})
            total += len(data)
            print(f"   [{i}/{len(links)}] {status} {dest.name} ({len(data) / 1e6:.1f} MB)")
        with (out_dir / "_download" / "manifest.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["file", "url", "bytes", "md5"])
            w.writeheader()
            w.writerows(rows)
    print(f"DONE total {total / 1e6:.0f} MB")


if __name__ == "__main__":
    sys.exit(main())
