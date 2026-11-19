# -*- coding: utf-8 -*-
"""extract-book.py — 构建期从出版合稿 docx 提取纯文本→中间 md
输入：D:/悟空核心资料/五行人格心理学-出版合稿.docx
输出：scripts/.build/book.md（供 build-knowledge.js 统一切块）
纯 Python，不依赖 WorkBuddy；书稿更新重跑即可。
"""
import os, re
from docx import Document

SRC = r"D:\悟空核心资料\五行人格心理学-出版合稿.docx"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".build", "book.md")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

doc = Document(SRC)
lines = []
for p in doc.paragraphs:
    t = p.text.strip()
    if not t:
        continue
    style = (p.style.name or "").lower()
    if "heading" in style or "标题" in style:
        # 推断层级
        m = re.search(r"(\d+)", style)
        lvl = min(int(m.group(1)) if m else 1, 4)
        lines.append("#" * lvl + " " + t)
    else:
        lines.append(t)

text = "\n\n".join(lines)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print("EXTRACT OK", len(text), "chars ->", OUT)
print("HEADINGS", text.count("\n#"), "approx")
