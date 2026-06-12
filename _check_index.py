#!/usr/bin/env python3
"""Check if merged index.html has 4415 count."""
import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

f = open(r"C:\dragon-heart-os\yiguanqimiao-website\index.html", "r", encoding="utf-8").read()
m = re.search(r"总 (\d+) 篇", f)
print(f"Count: {m.group(1) if m else 'NOT FOUND'}")
secs = re.findall(r"<h2>(.*?)</h2>", f)
print(f"Sections: {len(secs)}")
for s in secs:
    print(f"  {s[:50]}")
