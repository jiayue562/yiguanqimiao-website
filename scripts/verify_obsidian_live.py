import urllib.request, urllib.parse, re, sys, hashlib, os

BASE = "https://yiguanqimiao-website.pages.dev"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}

def make_ascii_name(text):
    name = text[:-5] if text.endswith('.html') else text
    h = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    parts = []; cur = ""
    for ch in name:
        if ord(ch) < 128:
            cur += ch
        else:
            if cur:
                parts.append(cur); cur = ""
    if cur:
        parts.append(cur)
    pre = ""
    if parts:
        c = "".join(parts); c = re.sub(r'[^a-zA-Z0-9_-]', '_', c)
        if len(c) > 40:
            c = c[:40]
        pre = c + "-"
    return (pre + h).strip('-')

WM = "yiguanqimiao-unique-watermark-wk-jiayue-academy"

def test(path, label=""):
    url = BASE + "/" + urllib.parse.quote(path)
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=25)
        body = r.read().decode('utf-8', 'ignore')
        spa = "3552篇" in body
        wm = WM in body
        title = re.search(r'<title>(.*?)</title>', body)
        real = (not spa) and wm
        print(f"  {label}{path[:50]:52} code={r.getcode()} spa={str(spa):5} wm={str(wm):5} real={str(real):5} title={(title.group(1)[:28] if title else 'NONE')!r}", flush=True)
        return real
    except Exception as e:
        print(f"  {label}{path[:50]:52} ERR {str(e)[:45]}", flush=True)
        return False

print("=== Verification start ===", flush=True)

# 1) obsidian index
ok1 = test("articles/obsidian/index.html", "IDX ")

# 2) sample ASCII note derived from a known obsidian note
rel = "articles/obsidian/05-五行人格心理学/00-入口/2026-04-05-系统竣工报告.html"
ascii_name = make_ascii_name(rel) + ".html"
print(f"  Computed ASCII note: {ascii_name}", flush=True)
ok2 = test("articles/obsidian/" + ascii_name, "NOTE")

# 3) a couple more sample notes from different top-level dirs (verify on disk first)
import glob
DOC_OBS = os.path.join(os.path.dirname(__file__), "..", "docs", "articles", "obsidian")
candidates = []
for root, dirs, files in os.walk(DOC_OBS):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            candidates.append(os.path.relpath(os.path.join(root, f), DOC_OBS).replace(os.sep, '/'))
    if len(candidates) >= 6:
        break
print(f"  Found {len(candidates)} sample notes on disk", flush=True)
oks = [ok1, ok2]
for c in candidates[:4]:
    oks.append(test("articles/obsidian/" + c, "SMP "))

print("\n=== SUMMARY ===", flush=True)
print(f"  index real={ok1}  sample note real={ok2}", flush=True)
print(f"  all sample checks passed: {all(oks)}", flush=True)
if all(oks):
    print("✅ OBSIDIAN ASCII LIVE!", flush=True)
else:
    print("❌ NOT FULLY LIVE YET", flush=True)
