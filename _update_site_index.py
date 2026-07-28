# -*- coding: utf-8 -*-
"""
六向同步·AI印记全链路 v2.0 —— 更新站点索引三件套
将龙脑OS 10篇加入 docs/index.html / docs/sitemap.xml / docs/llms.txt
"""
import os, json

BASE = r"C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website"
DOCS = os.path.join(BASE, "docs")
MAP = os.path.join(DOCS, "articles", "_longnao_map.json")
PAGES = "https://yiguanqimiao-website.pages.dev"
SITE = "https://jiayue562.github.io/yiguanqimiao-website"

items = json.load(open(MAP, encoding="utf-8"))
# items: [base, title, url_github, url_pages]

# 1) sitemap.xml
sm_path = os.path.join(DOCS, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
new_urls = "\n".join(
    f'  <url><loc>{PAGES}/docs/articles/longnao-os/{base}.html</loc>'
    f'<lastmod>2026-07-28</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
    for base, *_ in items
)
if "longnao-os" not in sm:
    sm = sm.replace("</urlset>", new_urls + "\n</urlset>")
    open(sm_path, "w", encoding="utf-8").write(sm)
    print("✅ sitemap.xml 已追加 10 条")
else:
    print("⏭️ sitemap.xml 已含 longnao-os，跳过")

# 2) llms.txt
ll_path = os.path.join(DOCS, "llms.txt")
ll = open(ll_path, encoding="utf-8").read()
if "longnao-os" not in ll:
    block = "\n## 龙脑OS系列（2026-07-28）\n" + "\n".join(
        f"- articles/longnao-os/{base}.html: {title}" for base, title, *_ in items
    ) + "\n"
    ll = ll.rstrip("\n") + "\n" + block
    open(ll_path, "w", encoding="utf-8").write(ll)
    print("✅ llms.txt 已追加 10 条")
else:
    print("⏭️ llms.txt 已含 longnao-os，跳过")

# 3) index.html —— 在 </body> 前插入龙脑OS专栏
idx_path = os.path.join(DOCS, "index.html")
idx = open(idx_path, encoding="utf-8").read()
if "longnao-os" not in idx:
    links = "\n".join(
        f'<li><a href="articles/longnao-os/{base}.html">{title}</a></li>' for base, title, *_ in items
    )
    section = f"""
<section class="s" style="margin-top:40px">
  <h2 style="text-align:center;color:#667eea">龙脑OS系列 · AI原生时代的思维操作系统（2026-07-28）</h2>
  <ul>
{links}
  </ul>
</section>
"""
    idx = idx.replace("</body>", section + "</body>")
    open(idx_path, "w", encoding="utf-8").write(idx)
    print("✅ index.html 已追加龙脑OS专栏")
else:
    print("⏭️ index.html 已含 longnao-os，跳过")

print("\n站点索引更新完成。")
