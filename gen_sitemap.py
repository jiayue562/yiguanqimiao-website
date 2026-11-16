# -*- coding: utf-8 -*-
"""
sitemap.xml 重生成器（沉淀工具）
基于 docs/ 目录下的真实 .html 文件重新生成 sitemap.xml，
消除 2026-07-28 事故中暴露的"陈旧 sitemap 引用不存在路径"问题。
域名对齐 Cloudflare Pages 实际部署：https://yiguanqimiao-website.pages.dev/
路径对齐 Cloudflare 输出目录 = docs/（线上 /<相对docs路径>）。

2026-11-16 升级：
  - 新增 EXCLUDE：跳过 noindex 页（method.html 跳转页）与被 clean URL 代表的 index 页
  - 新增 EXTRA：五行人格测评模块的 clean URL（/wuxing/ /wuxing/rel/ 等）带 priority + lastmod
用法：python gen_sitemap.py
"""
import os
from datetime import date
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://yiguanqimiao-website.pages.dev"
TODAY = date.today().isoformat()

# 不进 sitemap 的页面：
#   - noindex 页（跳转页）与报告页（个性化输出，无可索引内容）
#   - 已由 EXTRA clean URL 代表的 .html 变体（页面 canonical 已声明规范地址，避免双收录）
EXCLUDE = {
    "wuxing/rel/method.html",   # 跳转页 → baike.html#method（noindex）
    "wuxing/rel/report.html",   # 动态报告页（无作答数据时为空壳）
    "wuxing/report.html",       # 同上（单人报告页）
    "wuxing/index.html",
    "wuxing/quiz.html",
    "wuxing/rel/index.html",
    "wuxing/rel/quiz.html",
    "wuxing/rel/baike.html",
    "wuxing/rel/types.html",
    "wuxing/rel/camp.html",
}

# 五行人格测评模块 clean URL（canonical 与 sitemap 对齐）
EXTRA = [
    ("wuxing/",             "1.0"),
    ("wuxing/rel/",         "1.0"),
    ("wuxing/rel/baike",    "0.9"),
    ("wuxing/rel/types",    "0.9"),
    ("wuxing/rel/camp",     "0.9"),
    ("wuxing/rel/quiz",     "0.8"),
    ("wuxing/quiz",         "0.8"),
]

urls = []
for dp, _, files in os.walk(DOCS):
    for f in files:
        if f.lower().endswith(".html"):
            rel = os.path.relpath(os.path.join(dp, f), DOCS).replace(os.sep, "/")
            if rel.replace("\\", "/") in EXCLUDE:
                continue
            urls.append(f"{BASE}/{escape(rel)}")
urls.sort()

loc_block = "".join(f"  <url>\n    <loc>{u}</loc>\n  </url>\n" for u in urls)
extra_block = "".join(
    f"  <url>\n    <loc>{BASE}/{escape(path)}</loc>\n"
    f"    <lastmod>{TODAY}</lastmod>\n"
    f"    <priority>{prio}</priority>\n  </url>\n"
    for path, prio in EXTRA
)
xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"{extra_block}"
    f"{loc_block}"
    '</urlset>\n'
)

out = os.path.join(ROOT, "sitemap.xml")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(xml)
print(f"sitemap.xml 已重生成: {len(urls)} 条常规 + {len(EXTRA)} 条五行模块 clean URL -> {out}")
