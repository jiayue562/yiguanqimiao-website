# -*- coding: utf-8 -*-
"""
sitemap 生成器 v2（2026-11-16 SEO 升级）

变更要点：
  1. sitemap.xml 由 urlset 改为 sitemapindex，指向三张子图（对外地址不变，已提交的 URL 不断链）
     - sitemap-core.xml      核心页：门户、五行频道、关系测评六页、clean URL
     - sitemap-articles.xml  文章页：剔除内部页/副本后的可索引文章
     - sitemap-books.xml     长文档（整本书 / 手册 / 白皮书单页 HTML）
  2. 剔除规则：README、`_1` 副本、下划线目录（_temp/_ai_org_build/_thinking_models_build 等）、
     test 页、无扩展名重复文件对应的 .html 孪生
  3. lastmod 用文件真实 mtime（不再全站写今天），让搜索引擎只重抓真正变过的页
  4. 每张子图 ≤ 45000 条，超限自动切片

用法：python gen_sitemap.py
输出：docs/sitemap.xml（index）+ docs/sitemap-*.xml
"""
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
BASE = "https://yiguanqimiao-website.pages.dev"
TODAY = date.today().isoformat()
MAX_PER_MAP = 45000

# ── 核心页（clean URL，与各页 canonical 严格一致）──────────────────────────
CORE = [
    ("",                    "1.0", "daily"),
    ("wuxing/rel/",         "1.0", "weekly"),
    ("wuxing/rel/baike",    "0.9", "weekly"),
    ("wuxing/rel/types",    "0.9", "weekly"),
    ("wuxing/rel/camp",     "0.9", "weekly"),
    ("wuxing/rel/contact",  "0.7", "monthly"),
    # quiz / report 为 noindex 页，不进 sitemap（避免与页面级 noindex 冲突）
    # wuxing/ 已改为跳转页（noindex, follow → wuxing/rel/），不进 sitemap
]

# 这些 .html 已由上面的 clean URL 代表，或本身 noindex，不进子图
CORE_EXCLUDE_HTML = {
    "index.html",
    "wuxing/index.html",
    "wuxing/quiz.html",
    "wuxing/report.html",
    "wuxing/rel/index.html",
    "wuxing/rel/quiz.html",
    "wuxing/rel/report.html",
    "wuxing/rel/baike.html",
    "wuxing/rel/types.html",
    "wuxing/rel/camp.html",
    "wuxing/rel/contact.html",
    "wuxing/rel/method.html",
    "404.html",
}

# ── 文章层剔除规则 ────────────────────────────────────────────────────────
JUNK_DIR_PREFIX = ("_",)          # _temp / _ai_org_build / _thinking_models_build ...
JUNK_NAME_PATTERNS = [
    re.compile(r"^README\.html$", re.I),
    re.compile(r"_1\.html$", re.I),          # 同名副本
    re.compile(r"^test", re.I),
    re.compile(r"^index\.html$", re.I),      # 目录索引页（低质导航页）
]

# ── 长文档（docs 根部的大单页）─────────────────────────────────────────────
BOOK_MIN_BYTES = 150_000


def rel_of(path):
    return os.path.relpath(path, DOCS).replace(os.sep, "/")


def lastmod_of(path):
    import datetime
    return datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()


def is_junk(rel):
    parts = rel.split("/")
    for seg in parts[:-1]:
        if seg.startswith(JUNK_DIR_PREFIX):
            return True
    name = parts[-1]
    return any(p.search(name) for p in JUNK_NAME_PATTERNS)


def url_entry(loc, lastmod, priority, changefreq):
    return (
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def write_urlset(filename, entries):
    """entries: [(loc, lastmod, priority, changefreq)]，超过 MAX_PER_MAP 自动切片"""
    chunks = [entries[i:i + MAX_PER_MAP] for i in range(0, len(entries), MAX_PER_MAP)] or [[]]
    names = []
    for idx, chunk in enumerate(chunks, 1):
        name = filename if len(chunks) == 1 else filename.replace(".xml", "-%d.xml" % idx)
        body = "".join(url_entry(*e) for e in chunk)
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body +
            "</urlset>\n"
        )
        with open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(xml)
        names.append(name)
        print("  %-26s %5d 条" % (name, len(chunk)))
    return names


def main():
    core, articles, books = [], [], []

    # 核心页
    for path, prio, freq in CORE:
        core.append(("%s/%s" % (BASE, path) if path else BASE + "/", TODAY, prio, freq))

    for dp, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for f in files:
            if not f.lower().endswith(".html"):
                continue
            full = os.path.join(dp, f)
            rel = rel_of(full)
            if rel in CORE_EXCLUDE_HTML:
                continue
            if is_junk(rel):
                continue
            size = os.path.getsize(full)
            loc = "%s/%s" % (BASE, rel)
            if rel.startswith("articles/"):
                articles.append((loc, lastmod_of(full), "0.6", "monthly"))
            elif "/" not in rel and size >= BOOK_MIN_BYTES:
                books.append((loc, lastmod_of(full), "0.8", "yearly"))
            else:
                # 其他散页（archive 等）按文章级处理
                articles.append((loc, lastmod_of(full), "0.5", "monthly"))

    core.sort()
    articles.sort()
    books.sort()

    print("生成子图：")
    names = []
    names += write_urlset("sitemap-core.xml", core)
    names += write_urlset("sitemap-articles.xml", articles)
    names += write_urlset("sitemap-books.xml", books)

    index = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(
            "  <sitemap>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n  </sitemap>\n"
            % (BASE, n, TODAY) for n in names
        )
        + "</sitemapindex>\n"
    )
    with open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(index)

    total = len(core) + len(articles) + len(books)
    print("sitemap.xml（index）-> %d 张子图，合计 %d 条 URL" % (len(names), total))


if __name__ == "__main__":
    main()
