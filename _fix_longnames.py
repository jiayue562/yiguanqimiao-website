#!/usr/bin/env python3
"""Truncate filenames > 200 UTF-8 bytes to prevent Linux checkout failures."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ARTICLES_DIR = r"C:\dragon-heart-os\yiguanqimiao-website\docs\articles"
MAX_BYTES = 200

fixed = []
for f in sorted(os.listdir(ARTICLES_DIR)):
    if not f.endswith(".html"):
        continue
    b = len(f.encode("utf-8"))
    if b <= MAX_BYTES:
        continue
    base = f[:-5]
    while len(base.encode("utf-8")) > MAX_BYTES - 10:
        base = base[:-1]
    new_name = base + ".html"
    src = os.path.join(ARTICLES_DIR, f)
    dst = os.path.join(ARTICLES_DIR, new_name)
    if os.path.exists(dst):
        for i in range(1, 100):
            dst2 = os.path.join(ARTICLES_DIR, f"{base}_{i}.html")
            if not os.path.exists(dst2):
                dst = dst2
                break
    os.rename(src, dst)
    new_b = len(os.path.basename(dst).encode("utf-8"))
    fixed.append((f, os.path.basename(dst), b, new_b))
    print(f"{b}B -> {new_b}B: {os.path.basename(dst)[:60]}")
print(f"Done. Fixed {len(fixed)} filenames")
