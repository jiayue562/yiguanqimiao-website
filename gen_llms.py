# -*- coding: utf-8 -*-
"""
llms.txt 重建器（沉淀工具 · 待确认运行）
基于 docs/ 真实 .html 文件重建 llms.txt，链接对齐真实文件名（哈希名），
描述取各页 <title>，消除"文件名哈希化但 llms.txt 仍用中文名"导致的坏链。
运行前自动备份原 llms.txt -> llms.txt.bak（git 亦可恢复）。
用法：python gen_llms.py
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

entries = []
for dp, _, files in os.walk(DOCS):
    for f in files:
        if not f.lower().endswith(".html"):
            continue
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
        # 链接用相对站点根的形式（对应 Cloudflare 输出 docs/ -> 线上 /articles/...）
        link = rel[len("docs/"):] if rel.startswith("docs/") else rel
        try:
            data = open(full, encoding="utf-8", errors="replace").read()
        except Exception:
            data = ""
        m = re.search(r"<title[^>]*>(.*?)</title>", data, re.I | re.S)
        title = (m.group(1).strip() if m else os.path.splitext(f)[0])
        title = re.sub(r"\s+", " ", title)
        entries.append((link, title))
entries.sort()

lines = [
    "# 以观其妙书院 网站索引 (llms.txt)",
    "",
    "> 自动重建：链接对齐 docs/ 真实文件，描述取各页 <title>。",
    "",
]
for link, title in entries:
    lines.append(f"- [{title}]({link})")

out = os.path.join(ROOT, "llms.txt")
if os.path.exists(out):
    shutil.copy2(out, out + ".bak")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print(f"llms.txt 已重建: {len(entries)} 条 (原文件备份 -> llms.txt.bak) -> {out}")
