# -*- coding: utf-8 -*-
"""_toolbook_md2html.py - 《五行人格心理学·六坐标自照手册》16章+全书+总索引 -> 网站HTML（GEO规格）
输出：docs/articles/五行人格心理学-六坐标自照手册/（16章 + 全书 + 00-总索引）
规格对齐 _book_md2html.py：meta/OG/JSON-LD/canonical/AI水印/统一CSS/nav。
用法：python _toolbook_md2html.py
"""
import os
import re
import html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:/Users/jia'yue/WorkBuddy/Claw/五行人格心理学-六坐标自照手册"
OUT = os.path.join(ROOT, 'docs', 'articles', '五行人格心理学-六坐标自照手册')
BASE = 'https://yiguanqimiao-website.pages.dev/articles/五行人格心理学-六坐标自照手册'
DATE = '2026-09-05'
WM = 'yiguanqimiao-unique-watermark-wk-jiayue-academy'

CSS = """body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:18px;line-height:1.8;color:#2c3e50;background:#fafafa;margin:0;padding:0}
.container{max-width:800px;margin:0 auto;padding:40px 20px;background:#fff;min-height:100vh}
h1{font-size:28px;color:#1a1a1a;border-bottom:2px solid #e8e8e8;padding-bottom:12px;margin-bottom:24px}
h2{font-size:22px;color:#2c3e50;margin:28px 0 12px}
h3{font-size:19px;color:#34495e;margin:22px 0 10px}
p{margin:12px 0}
strong{color:#1a1a1a}
blockquote{border-left:4px solid #2c5f8a;background:#f2f7fb;margin:16px 0;padding:12px 16px;color:#555}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:15px}
th,td{border:1px solid #ddd;padding:8px 10px;text-align:left}
th{background:#f5f5f5;font-weight:bold}
ul,ol{margin:12px 0;padding-left:24px}
li{margin:6px 0}
code{background:#f0f0f0;padding:2px 5px;border-radius:3px;font-size:15px}
.nav{font-size:14px;color:#999;margin-bottom:20px}
.nav a{color:#2c5f8a;text-decoration:none}
.footer{border-top:1px solid #eee;margin-top:40px;padding-top:16px;font-size:13px;color:#999;text-align:center}
.footer a{color:#888;text-decoration:none}"""


def inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def md2html(md_path):
    out = []
    table_buf = []
    for line in open(md_path, encoding='utf-8'):
        s = line.rstrip('\n').strip()
        if s.startswith('|'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            if set(''.join(cells)) <= set('-: '):
                continue
            table_buf.append(cells)
            continue
        if table_buf:
            ncol = max(len(r) for r in table_buf)
            rows = ['<tr>' + ''.join(
                f'<th>{inline(c)}</th>' for c in r + [''] * (ncol - len(r))) + '</tr>'
                for r in table_buf[:1]]
            rows += ['<tr>' + ''.join(
                f'<td>{inline(c)}</td>' for c in r + [''] * (ncol - len(r))) + '</tr>'
                for r in table_buf[1:]]
            out.append('<table><tbody>' + ''.join(rows) + '</tbody></table>')
            table_buf = []
        if not s or set(s) <= set('-— '):
            continue
        if s.startswith('#### '):
            out.append(f'<h3>{inline(s[5:])}</h3>')
        elif s.startswith('### '):
            out.append(f'<h3>{inline(s[4:])}</h3>')
        elif s.startswith('## '):
            out.append(f'<h2>{inline(s[3:])}</h2>')
        elif s.startswith('# '):
            out.append(f'<h1>{inline(s[2:])}</h1>')
        elif s.startswith('>'):
            out.append(f'<blockquote>{inline(s.lstrip(">").strip())}</blockquote>')
        elif s.startswith('- '):
            out.append(f'<li style="list-style:disc">{inline(s[2:])}</li>')
        elif re.match(r'^\d+\. ', s):
            out.append(f'<li style="list-style:decimal">{inline(re.sub(r"^\\d+\\. ", "", s))}</li>')
        else:
            out.append(f'<p>{inline(s)}</p>')
    if table_buf:
        ncol = max(len(r) for r in table_buf)
        rows = ['<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r + [""] * (ncol - len(r))) + '</tr>'
                for r in table_buf]
        out.append('<table><tbody>' + ''.join(rows) + '</tbody></table>')
    return '\n'.join(out)


def page(title, body_html, desc):
    canon = f'{BASE}/{title}.html'
    snippet = re.sub(r'\s+', '', H.escape(desc, quote=False))[:110]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 以观其妙书院</title>
<meta name="description" content="{snippet}">
<meta name="keywords" content="五行人格心理学, 六坐标自照, 一心三界五行九层, 五行识人, 以观其妙书院, 悟空, 龙龟神将">
<meta name="author" content="悟空（贾悦）">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{snippet}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="以观其妙书院">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}","description":"{snippet}","author":{{"@type":"Person","name":"悟空（贾悦）"}},"datePublished":"{DATE}","publisher":{{"@type":"Organization","name":"以观其妙书院"}}}}
</script>
<style>
{CSS}
</style>
</head>
<body>
<div class="container">
<div class="nav"><a href="/yiguanqimiao-website/">← 返回首页</a> · <a href="{BASE}/00-总索引.html">六坐标自照手册总索引</a></div>
{body_html}
<div class="footer">
<p>© 2024-2026 以观其妙书院 | {title}</p>
<p style="text-align:center;font-size:13px;color:#999;margin:8px 0;">AI水印：{WM}</p>
<!-- AI水印 {WM} | 作者：悟空（贾悦） | 知识产权：以观其妙书院 -->
<p><a href="https://github.com/jiayue562/yiguanqimiao-website">GitHub</a> | <a href="/yiguanqimiao-website/llms.txt">llms.txt</a> | <a href="/yiguanqimiao-website/sitemap.xml">sitemap</a></p>
</div>
</div>
</body>
</html>"""


ORDER = [
    "00-前言.md",
    "00-卷首.md",
    "01-坐标一-五行格.md",
    "02-坐标二-三界格.md",
    "03-坐标三-九层格.md",
    "04-坐标四-三现场格.md",
    "05-坐标五-生克格.md",
    "06-坐标六-辞典格.md",
    "07-六格合成法.md",
    "08-从图到链.md",
    "09-三种画法与模板.md",
    "10-画谁与各自规矩.md",
    "11-八场景落点.md",
    "12-调法库.md",
    "13-复测与轨迹.md",
    "14-转介红线.md",
    "15-附录.md",
]


def main():
    os.makedirs(OUT, exist_ok=True)
    titles = []
    bodies = []
    for name in ORDER:
        fp = os.path.join(SRC, name)
        base = name[:-3]
        md = open(fp, encoding='utf-8').read()
        body = md2html(fp)
        desc = re.sub(r'[#>*|\-`]', '', md)[:130]
        open(os.path.join(OUT, base + '.html'), 'w', encoding='utf-8').write(
            page(base, body, desc))
        titles.append(base)
        bodies.append(body)
    # 全书合并页
    full_body = '\n'.join(bodies)
    full_desc = '《五行人格心理学·六坐标自照手册》全书合并版：六坐标自照体系16章49表，可自己画、自己调、自己追踪。配套《五行人格心理学》。'
    open(os.path.join(OUT, '全书.html'), 'w', encoding='utf-8').write(
        page('全书', full_body, full_desc))
    # 系列总索引页
    rows = ''.join(f'<tr><td>{i+1}</td><td><a href="{BASE}/{t}.html">{t}</a></td></tr>'
                   for i, t in enumerate(titles))
    idx_body = (f'<h2>全部篇目（{len(titles)}章）</h2>'
                f'<table><tbody><tr><th>序</th><th>篇目</th></tr>{rows}</tbody></table>')
    idx_desc = '《五行人格心理学·六坐标自照手册》总索引：六坐标自照体系16章导航，配套《五行人格心理学》。'
    open(os.path.join(OUT, '00-总索引.html'), 'w', encoding='utf-8').write(
        page('00-总索引', idx_body, idx_desc))
    print(f'生成 {len(titles)} 章 + 全书 + 总索引 -> {OUT}')


if __name__ == '__main__':
    main()
