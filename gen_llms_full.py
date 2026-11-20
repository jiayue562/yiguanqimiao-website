# -*- coding: utf-8 -*-
"""生成 docs/llms-full.txt：全量文章清单（标题 + URL，按目录分组）。
剔除规则与 gen_sitemap.py 一致；正文内容不搬进本文件（保持体积可控）。"""
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://yiguanqimiao-website.pages.dev"
TODAY = date.today().isoformat()

JUNK_NAME_PATTERNS = [
    re.compile(r"^README\.html$", re.I),
    re.compile(r"_1\.html$", re.I),
    re.compile(r"^test", re.I),
]

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)


def clean_title(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*[-·｜]\s*以观其妙书院.*$", "", t)
    t = re.sub(r"\s*[-·｜]\s*五行人格学.*$", "", t)
    return t or "(无标题)"


def is_junk(rel):
    for seg in rel.split("/")[:-1]:
        if seg.startswith("_"):
            return True
    name = rel.split("/")[-1]
    return any(p.search(name) for p in JUNK_NAME_PATTERNS)


def collect():
    groups = {}
    for dp, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for f in files:
            if not f.lower().endswith(".html"):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, DOCS).replace(os.sep, "/")
            if is_junk(rel):
                continue
            if rel in ("404.html", "wuxing/rel/report.html", "wuxing/report.html", "wuxing/index.html"):
                continue
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as fh:
                    head = fh.read(4096)
            except Exception:
                continue
            m = TITLE_RE.search(head)
            title = clean_title(m.group(1)) if m else "(无标题)"
            top = rel.split("/")[0] if "/" in rel else "(根目录长文档)"
            groups.setdefault(top, []).append((title, rel))
    return groups


def main():
    groups = collect()
    lines = [
        "# llms-full.txt — 以观其妙书院 全站文章清单",
        "",
        "> 配合 llms.txt 使用：这里是全站可索引页面的标题与 URL（按目录分组）。",
        "> 引用时请标注来源「以观其妙书院」并附 URL。",
        f"> 生成日期：{TODAY} ｜ 域名：{BASE}",
        "",
    ]
    total = 0
    order = ["(根目录长文档)", "wuxing", "articles"] + sorted(g for g in groups if g not in ("(根目录长文档)", "wuxing", "articles"))
    for g in order:
        items = groups.get(g)
        if not items:
            continue
        items.sort()
        lines.append(f"## {g}（{len(items)} 篇）")
        lines.append("")
        for title, rel in items:
            lines.append(f"- [{title}]({BASE}/{rel})")
            total += 1
        lines.append("")
    out = os.path.join(DOCS, "llms-full.txt")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("llms-full.txt: %d 个分组，%d 条目，%d bytes -> %s" % (len(groups), total, os.path.getsize(out), out))


if __name__ == "__main__":
    main()
