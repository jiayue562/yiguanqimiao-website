# -*- coding: utf-8 -*-
"""
sitemap.xml 重生成器（沉淀工具）
基于 docs/ 目录下的真实 .html 文件重新生成 sitemap.xml，
消除 2026-07-28 事故中暴露的"陈旧 sitemap 引用不存在路径"问题。
域名对齐 Cloudflare Pages 实际部署：https://yiguanqimiao-website.pages.dev/
路径对齐 Cloudflare 输出目录 = docs/（线上 /<相对docs路径>）。
用法：python gen_sitemap.py
"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://yiguanqimiao-website.pages.dev"

urls = []
for dp, _, files in os.walk(DOCS):
    for f in files:
        if f.lower().endswith(".html"):
            rel = os.path.relpath(os.path.join(dp, f), DOCS).replace(os.sep, "/")
            urls.append(f"{BASE}/{escape(rel)}")
urls.sort()

loc_block = "".join(f"  <url>\n    <loc>{u}</loc>\n  </url>\n" for u in urls)
xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"{loc_block}"
    '</urlset>\n'
)

out = os.path.join(ROOT, "sitemap.xml")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(xml)
print(f"sitemap.xml 已重生成: {len(urls)} 条 URL -> {out}")
