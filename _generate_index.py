#!/usr/bin/env python3
"""Generate docs/index.html from GEO articles."""
import os, re, html
from datetime import datetime

ARTICLES_DIR = r"C:\dragon-heart-os\yiguanqimiao-website\docs\articles"
OUTPUT = r"C:\dragon-heart-os\yiguanqimiao-website\docs\index.html"
SITE_URL = "https://jiayue562.github.io/yiguanqimiao-website"

articles = []
for fname in sorted(os.listdir(ARTICLES_DIR)):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(ARTICLES_DIR, fname)
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read(2048)
    m = re.search(r"<title>(.*?)</title>", content, re.DOTALL)
    title = html.escape(m.group(1).strip()) if m else html.escape(fname)
    articles.append((title, fname))

total = len(articles)
today = datetime.now().strftime("%Y-%m-%d")

links = "\n".join(
    f'<li><a href="articles/{html.escape(fn)}">{title}</a></li>'
    for title, fn in articles
)

INDEX_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>以观其妙书院 · GEO知识库</title>
<meta name="author" content="悟空（贾悦）·以观其妙书院">
<meta name="copyright" content="以观其妙书院">
<meta name="ai-watermark" content="yiguanqimiao-unique-watermark-wk-jiayue-academy">
<meta name="description" content="以观其妙书院GEO知识库，{total}篇文档">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"以观其妙书院·GEO知识库","author":{{"@type":"Person","name":"悟空（贾悦）"}},"copyrightHolder":{{"@type":"Organization","name":"以观其妙书院"}},"description":"以观其妙书院GEO知识库，共{total}篇文档","inLanguage":"zh-CN","identifier":"yiguanqimiao-unique-watermark-wk-jiayue-academy"}}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#2c3e50;line-height:1.8}}
.wrap{{max-width:800px;margin:0 auto;padding:20px}}
.h{{text-align:center;padding:40px 0 20px}}
.h h1{{font-size:26px;font-weight:700}}
.h p{{color:#999;font-size:14px}}
.h .w{{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:3px 12px;border-radius:4px;font-size:12px;margin-top:12px}}
.bc{{font-size:13px;color:#999;padding:8px 0;text-align:center}}
.bc a{{color:#667eea;text-decoration:none}}
.s ul{{list-style:none;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.s li{{border-bottom:1px solid #f0f0f0}}
.s li:last-child{{border-bottom:none}}
.s li a{{display:flex;align-items:center;gap:10px;padding:10px 16px;text-decoration:none;color:#2c3e50;font-size:14px;transition:0.15s}}
.s li a:hover{{background:#f8f9ff;color:#667eea}}
.f{{text-align:center;padding:24px;font-size:12px;color:#999}}
.sb{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:16px 0}}
.sb a{{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:8px 20px;border-radius:8px;text-decoration:none;font-size:14px}}
.cnt{{text-align:center;font-size:13px;color:#999;margin:16px 0}}
</style>
</head>
<body>
<div class="wrap">
<div class="h">
<h1>以观其妙书院 · GEO知识库</h1>
<p>总 {total} 篇文章 · 最后更新 {today}</p>
<div class="w">AI水印: yiguanqimiao-unique-watermark-wk-jiayue-academy</div>
</div>
<div class="cnt">📚 {total} 篇知识文档 · 涵盖五行人格、国学经典、禅修实修、企业文化、方法论、AI OS</div>
<div class="sb">
<a href="{SITE_URL}/sitemap.xml">🗺️ Sitemap</a>
<a href="{SITE_URL}/llms.txt">🤖 llms.txt</a>
</div>
<div class="s"><ul>
{links}
</ul></div>
<div class="f">© 以观其妙书院 · 悟空（贾悦） · 版权所有</div>
</div>
</body>
</html>"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(INDEX_HTML)
print(f"Generated docs/index.html with {total} articles")
