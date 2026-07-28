# -*- coding: utf-8 -*-
"""
六向同步·AI印记全链路 v2.0 —— 第三步 GitHub/Cloudflare/pages.dev
将龙脑OS系列10篇 Markdown 转换为带完整SEO的 HTML，部署到 yiguanqimiao-website/docs/articles/longnao-os/
"""
import os, re, html, json

SRC_DIR = r"C:/Users/jia'yue/WorkBuddy/Claw/龙脑OS系列公众号文章"
OUT_DIR = r"C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/docs/articles/longnao-os"
SITE = "https://jiayue562.github.io/yiguanqimiao-website"
PAGES = "https://yiguanqimiao-website.pages.dev"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"

ARTICLES = [
    "01-龙脑OS-AI原生时代的思维操作系统.md",
    "02-象思维-中国传统文化最本质的思维模式.md",
    "03-思维模型-西方理性思维的武器库.md",
    "04-思维模型组合-人的长项与AI的盲区.md",
    "05-象思维与思维模型的会通-东西方思维的融合.md",
    "06-理论层-龙脑OS的科学支撑与可信度锚.md",
    "07-龙心调度龙脑-R5R8路由协议与思维编排.md",
    "08-龙脑OS实操框架-从思维到行动的工程化落地.md",
    "09-龙脑OS前瞻-AI原生时代的思维操作系统演化.md",
    "10-龙脑OS的局限与演化-边界谦卑与自我超越.md",
]

def strip_frontmatter(md):
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            return md[end+4:].lstrip("\n")
    return md

def get_title(md):
    m = re.match(r"^---\n(.*?)\n---", md, re.DOTALL)
    if m:
        tm = re.search(r"^title:\s*(.+)$", m.group(1), re.MULTILINE)
        if tm:
            return tm.group(1).strip()
    hm = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return hm.group(1).strip() if hm else "龙脑OS文章"

def inline(text):
    text = html.escape(text, quote=True)
    # code
    text = re.sub(r"`([^`]+)`", lambda m: "<code>"+m.group(1)+"</code>", text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # italic
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    # links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text

def md_to_html(md):
    md = strip_frontmatter(md)
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # code fence
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append("<pre><code>"+html.escape("\n".join(buf), quote=False)+"</code></pre>")
            continue
        # blank
        if not line.strip():
            i += 1
            continue
        # heading
        hm = re.match(r"^(#{1,4})\s+(.*)$", line)
        if hm:
            lvl = len(hm.group(1))
            out.append(f"<h{lvl}>{inline(hm.group(2))}</h{lvl}>")
            i += 1
            continue
        # hr
        if re.match(r"^---+$", line.strip()):
            out.append("<hr>")
            i += 1
            continue
        # blockquote
        if line.lstrip().startswith(">"):
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>"+inline(" ".join(buf))+"</blockquote>")
            continue
        # unordered list
        if re.match(r"^[-*]\s+", line):
            buf = []
            while i < n and re.match(r"^[-*]\s+", lines[i]):
                buf.append(re.sub(r"^[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>"+"".join(f"<li>{inline(x)}</li>" for x in buf)+"</ul>")
            continue
        # ordered list
        if re.match(r"^\d+\.\s+", line):
            buf = []
            while i < n and re.match(r"^\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>"+"".join(f"<li>{inline(x)}</li>" for x in buf)+"</ol>")
            continue
        # paragraph (collect consecutive non-special lines)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|[-*]\s|\d+\.\s|```|>|---+$)", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append("<p>"+inline(" ".join(buf))+"</p>")
    return "\n".join(out)

def plain_text(md):
    md = strip_frontmatter(md)
    md = re.sub(r"```.*?```", "", md, flags=re.DOTALL)
    md = re.sub(r"^---\n.*?\n---", "", md, flags=re.DOTALL)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[#>*`]", "", md)
    md = re.sub(r"\*\*", "", md)
    md = re.sub(r"\s+", " ", md).strip()
    return md

def gen_html(title, body, url_github, url_pages, desc_raw):
    desc = desc_raw[:120]
    kw = "龙脑OS, 五行人格, 以观其妙书院, 龙龟神将, AI操作系统, 思维模型, 象思维, 思维操作系统"
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Person", "name": "以观其妙书院"},
        "datePublished": "2026-07-28",
        "publisher": {"@type": "Organization", "name": "以观其妙书院"},
        "identifier": WATERMARK
    }
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} - 以观其妙书院</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{kw}">
<meta name="author" content="以观其妙书院">
<meta name="ai-watermark" content="{WATERMARK}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url_github}">
<meta property="og:site_name" content="以观其妙书院">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url_github}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=6)}
</script>
<style>
:root {{ --max-width: 800px; --font-size: 18px; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif; font-size: var(--font-size); line-height: 1.9; color: #2c3e50; background: #fafafa; }}
.container {{ max-width: var(--max-width); margin: 0 auto; padding: 40px 20px 80px; background: white; min-height: 100vh; box-shadow: 0 0 24px rgba(0,0,0,0.04); }}
h1 {{ font-size: 30px; line-height: 1.4; margin: 24px 0 12px; color: #1a2233; }}
h2 {{ font-size: 24px; margin: 36px 0 12px; color: #22304a; border-left: 4px solid #667eea; padding-left: 12px; }}
h3 {{ font-size: 20px; margin: 28px 0 10px; color: #2c3e50; }}
h4 {{ font-size: 17px; margin: 22px 0 8px; color: #445; }}
p {{ margin: 14px 0; }}
ul, ol {{ margin: 14px 0; padding-left: 28px; }}
li {{ margin: 6px 0; }}
blockquote {{ margin: 18px 0; padding: 12px 18px; background: #f4f6fb; border-left: 4px solid #9aa7d8; color: #455; border-radius: 6px; }}
pre {{ margin: 16px 0; padding: 16px; background: #1e293b; color: #e2e8f0; border-radius: 8px; overflow-x: auto; font-size: 14px; }}
code {{ font-family: "SFMono-Regular", Consolas, monospace; }}
:not(pre) > code {{ background: #eef1f7; color: #c0392b; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
hr {{ border: none; border-top: 1px solid #e2e6ee; margin: 32px 0; }}
a {{ color: #667eea; text-decoration: none; }}
.wm {{ margin-top: 48px; padding-top: 16px; border-top: 1px dashed #cdd; font-size: 13px; color: #98a; text-align: center; }}
</style>
</head>
<body>
<div class="container">
{body}
<div class="wm">*以观其妙书院 · 悟空(贾悦) &amp; 龙龟神将 · AI印记: {WATERMARK}*</div>
</div>
</body>
</html>"""

os.makedirs(OUT_DIR, exist_ok=True)
generated = []
for fn in ARTICLES:
    src = os.path.join(SRC_DIR, fn)
    md = open(src, encoding="utf-8").read()
    title = get_title(md)
    body = md_to_html(md)
    desc_raw = plain_text(md)
    base = os.path.splitext(fn)[0]
    out_fn = base + ".html"
    url_g = f"{SITE}/articles/longnao-os/{out_fn}"
    url_p = f"{PAGES}/docs/articles/longnao-os/{out_fn}"
    html_out = gen_html(title, body, url_g, url_p, desc_raw)
    with open(os.path.join(OUT_DIR, out_fn), "w", encoding="utf-8") as f:
        f.write(html_out)
    generated.append((base, title, url_g, url_p))
    print(f"✅ 生成: {out_fn}")

# 写出映射，供后续更新索引/站点图
with open(os.path.join(os.path.dirname(OUT_DIR), "_longnao_map.json"), "w", encoding="utf-8") as f:
    json.dump(generated, f, ensure_ascii=False, indent=2)
print(f"\n共生成 {len(generated)} 篇 HTML -> {OUT_DIR}")
