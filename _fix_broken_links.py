#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 2026-07-28 六向同步后产生的坏链与渲染问题"""
import os, glob, re

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")

# ---- 1. 删除无扩展名重复文件（会造成路由冲突） ----
removed = []
for f in glob.glob(os.path.join(DOCS, "articles", "longnao-os", "articles_longnao-os_*")):
    if not f.endswith(".html"):
        os.remove(f)
        removed.append(os.path.relpath(f, ROOT))
dup_ai = os.path.join(DOCS, "ai-native-org-complete-book")
if os.path.exists(dup_ai) and not dup_ai.endswith(".html"):
    os.remove(dup_ai)
    removed.append(os.path.relpath(dup_ai, ROOT))
print(f"[1] 删除无扩展名重复文件: {len(removed)} 个")
for r in removed[:5]: print("  -", r)
if len(removed) > 5: print(f"  ... 共 {len(removed)} 个")

# ---- 2. 修复 ai-native-org-complete-book.html 的 CDATA 包裹 ----
book = os.path.join(DOCS, "ai-native-org-complete-book.html")
if os.path.exists(book):
    text = open(book, encoding="utf-8").read()
    if text.startswith("<![CDATA["):
        text = text[len("<![CDATA["):]
    if text.rstrip().endswith("]]>"):
        text = text.rstrip()[:-3]
    text = text.lstrip()
    open(book, encoding="utf-8", mode="w").write(text)
    print(f"[2] 已剥离 CDATA: {os.path.relpath(book, ROOT)}")
else:
    print("[2] 未找到 ai-native-org-complete-book.html")

# ---- 3. 更新 index.html 中的坏链 ----
idx = os.path.join(DOCS, "index.html")
html = open(idx, encoding="utf-8").read()

# 3a AI原生组织卡片显式指向 .html
html = html.replace('href="/ai-native-org-complete-book"', 'href="/ai-native-org-complete-book.html"')

# 3b 龙脑OS 链接改为实际存在的 ASCII 文件名（显示文本保持中文）
mapping = {
    "01-龙脑OS-AI原生时代的思维操作系统.html": "articles_longnao-os_01-OS-AI-255f76fb.html",
    "02-象思维-中国传统文化最本质的思维模式.html": "articles_longnao-os_02---f033c3eb.html",
    "03-思维模型-西方理性思维的武器库.html": "articles_longnao-os_03---498d776f.html",
    "04-思维模型组合-人的长项与AI的盲区.html": "articles_longnao-os_04--AI-a7515bb9.html",
    "05-象思维与思维模型的会通-东西方思维的融合.html": "articles_longnao-os_05---39f1d0b3.html",
    "06-理论层-龙脑OS的科学支撑与可信度锚.html": "articles_longnao-os_06--OS-044e46c8.html",
    "07-龙心调度龙脑-R5R8路由协议与思维编排.html": "articles_longnao-os_07--R5R8-05bb052d.html",
    "08-龙脑OS实操框架-从思维到行动的工程化落地.html": "articles_longnao-os_08-OS--8e9c0b03.html",
    "09-龙脑OS前瞻-AI原生时代的思维操作系统演化.html": "articles_longnao-os_09-OS-AI-b9525812.html",
    "10-龙脑OS的局限与演化-边界谦卑与自我超越.html": "articles_longnao-os_10-OS--d6e92638.html",
}
for old_name, new_name in mapping.items():
    html = html.replace(f"articles/longnao-os/{old_name}", f"articles/longnao-os/{new_name}")
open(idx, encoding="utf-8", mode="w").write(html)
print("[3] 已更新 index.html 中的坏链")

# ---- 4. 同步修复 sitemap.xml 与 llms.txt ----
for fname in ["sitemap.xml", "llms.txt"]:
    path = os.path.join(DOCS, fname)
    if not os.path.exists(path):
        continue
    text = open(path, encoding="utf-8").read()
    # 把 /docs/articles/longnao-os/ 前缀也统一为 /articles/longnao-os/
    text = text.replace("/docs/articles/longnao-os/", "/articles/longnao-os/")
    for old_name, new_name in mapping.items():
        text = text.replace(old_name, new_name)
    open(path, encoding="utf-8", mode="w").write(text)
    print(f"[4] 已更新 {fname}")

# ---- 5. 验证 ----
print("\n[5] 验证关键文件存在:")
for new_name in mapping.values():
    p = os.path.join(DOCS, "articles", "longnao-os", new_name)
    print("  ✓" if os.path.exists(p) else "  ✗", os.path.relpath(p, DOCS))
book_ok = os.path.exists(book) and not open(book, encoding="utf-8").read().startswith("<![CDATA[")
print("  ✓ ai-native-org-complete-book.html CDATA 已剥离" if book_ok else "  ✗ 仍含 CDATA")
print("\n修复完成。请提交并推送。")
