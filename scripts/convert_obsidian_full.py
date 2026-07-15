#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 全量知识库 → HTML 镜像转换器 v2.0
===========================================
将整个 Obsidian 知识库（排除系统目录）转换为 GEO 优化 + AI 水印的 HTML，
完整保留目录结构输出到 articles/obsidian/，并为每个目录生成 index.html 导航页。

水印矩阵：
- yiguanqimiao-unique-watermark-wk-jiayue-academy
- 作者：悟空（贾悦）
- 知识产权：以观其妙书院
"""
import os
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

APOS = chr(39)
OBSIDIAN_VAULT = "D:/以观其妙书院知识库/以观其妙书院"
WEBSITE_DIR = "C:/Users/jia" + APOS + "yue/WorkBuddy/yiguanqimiao-website"
# 2026-07-15 架构调整：docs/ 为唯一权威部署源，转换结果直接写入 docs/articles/obsidian/
OUTPUT_DIR = os.path.join(WEBSITE_DIR, "docs", "articles", "obsidian")

WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"
SITE_URL = "https://yiguanqimiao-website.pages.dev"

# 排除的纯系统/工具目录（不属知识库内容）
EXCLUDE_DIRS = {
    '.obsidian', '.git', '.trash', '.workbuddy', '.claude',
    '.codebuddy', '.cursor', '.github', 'node_modules', '.smart-env',
}

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def clean_filename(name):
    """生成安全的文件名（保留中文/英文/数字/下划线/横线）。"""
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def safe_url(path_str):
    """将含中文的路径转为可用 URL（目录/文件名分别编码）。"""
    parts = path_str.split('/')
    return '/'.join(quote(p, safe='') for p in parts)

def extract_frontmatter(md):
    """解析 YAML frontmatter（不依赖 yaml 库），返回 (meta_dict, body)。"""
    if not md.startswith('---'):
        return {}, md
    try:
        end = md.index('\n---', 3)
    except ValueError:
        return {}, md
    fm_text = md[3:end].strip('\n')
    body = md[end+4:]
    meta = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^([A-Za-z0-9_\-]+):\s*(.*)$', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
            meta[key] = val
    return meta, body

def extract_title(meta, body):
    if 'title' in meta and meta['title']:
        return meta['title']
    m = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "以观其妙书院知识库"

# ---------------------------------------------------------------------------
# Inline 转换
# ---------------------------------------------------------------------------
def inline(text):
    """处理行内格式。输入应为已转义的文本。"""
    # 图片 ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
                  lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" style="max-width:100%">', text)
    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    # Wiki 链接 [[Note]] 或 [[Note|Alias]]
    def wikilink(m):
        raw = m.group(1).strip()
        if '|' in raw:
            target, alias = raw.split('|', 1)
        else:
            target, alias = raw, raw
        fn = clean_filename(target.strip()) + '.html'
        return f'<a href="{fn}">{alias.strip()}</a>'
    text = re.sub(r'\[\[([^\]]+)\]\]', wikilink, text)
    # 行内代码 `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 粗体 **text** 或 __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # 斜体 *text*（仅星号，避免误伤 snake_case 下划线）
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'<em>\1</em>', text)
    # 删除线 ~~text~~
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    return text

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------------------------------------------------------------------
# Block 转换（基于行的状态机）
# ---------------------------------------------------------------------------
def md_to_blocks(body):
    lines = body.split('\n')
    blocks = []          # list of (type, content)
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # 空行
        if not line.strip():
            i += 1
            continue
        # 代码块
        if re.match(r'^```', line.strip()):
            lang = line.strip().strip('`').strip()
            buf = []
            i += 1
            while i < n and not re.match(r'^```', lines[i].strip()):
                buf.append(lines[i])
                i += 1
            i += 1  # 跳过结束 ```
            blocks.append(('code', '\n'.join(buf)))
            continue
        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            blocks.append(('h', (level, m.group(2).strip())))
            i += 1
            continue
        # 分隔线
        if re.match(r'^(\s*[-*_]){3,}\s*$', line):
            blocks.append(('hr', ''))
            i += 1
            continue
        # 引用
        if line.lstrip().startswith('>'):
            buf = []
            while i < n and lines[i].lstrip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            blocks.append(('quote', '\n'.join(buf)))
            continue
        # 表格
        if '|' in line and i + 1 < n and re.match(r'^\s*\|?[\s:|-]+\|?\s*$', lines[i+1]) and '-' in lines[i+1]:
            rows = []
            while i < n and '|' in lines[i]:
                rows.append(lines[i])
                i += 1
            blocks.append(('table', '\n'.join(rows)))
            continue
        # 列表（有序/无序，含嵌套）；同级切换标记类型时拆分为独立列表块
        if re.match(r'^\s*([-*+]|\d+\.)\s+', line):
            buf = [line]
            first_indent = len(re.match(r'^(\s*)', line).group(1).replace('\t', '  '))
            first_ordered = bool(re.match(r'^\s*\d+\.', line))
            i += 1
            while i < n:
                ln = lines[i]
                if ln.strip() == '':
                    if i + 1 < n and re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i+1]):
                        i += 1
                        continue
                    else:
                        break
                mm = re.match(r'^(\s*)([-*+]|\d+\.)\s+', ln)
                if mm:
                    ind = len(mm.group(1).replace('\t', '  '))
                    ordered = bool(re.match(r'^\s*\d+\.', ln))
                    if ind <= first_indent and ordered != first_ordered:
                        blocks.append(('list', '\n'.join(buf)))
                        buf = [ln]
                        first_indent = ind
                        first_ordered = ordered
                        i += 1
                        continue
                    buf.append(ln)
                    i += 1
                    continue
                if re.match(r'^\s+\S', ln):
                    buf.append(ln)
                    i += 1
                    continue
                break
            blocks.append(('list', '\n'.join(buf)))
            continue
        # 段落（连续非空行）
        buf = []
        while i < n and lines[i].strip() and not re.match(r'^```', lines[i].strip()) \
                and not re.match(r'^(#{1,6})\s+', lines[i]) \
                and not re.match(r'^(\s*[-*_]){3,}\s*$', lines[i]) \
                and not lines[i].lstrip().startswith('>') \
                and not re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
            buf.append(lines[i])
            i += 1
        blocks.append(('p', '\n'.join(buf)))
    return blocks

def render_list(block_text):
    """将列表块（含嵌套）渲染为正确嵌套的 <ul>/<ol>。"""
    lines = block_text.split('\n')
    # 解析为树：每个节点 = [content, ordered_flag, children]
    root = []
    stack = [(-1, None, root)]  # (indent, ordered, children_list)
    for raw in lines:
        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', raw)
        if not m:
            # 列表项的续行（缩进的非标记文本），并入当前项内容
            if len(stack) > 1 and stack[-1] is not None:
                cur = stack[-1]
                if isinstance(cur[2], list) and cur[2]:
                    cur[2][-1][0] += ' ' + raw.strip()
            continue
        indent = len(m.group(1).replace('\t', '  '))
        ordered = bool(re.match(r'\d+\.', m.group(2)))
        content = m.group(3)
        node = [content, ordered, []]
        # 找到缩进更小的父级
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        parent_children = stack[-1][2]
        parent_children.append(node)
        stack.append((indent, ordered, node[2]))

    def render_nodes(nodes):
        if not nodes:
            return ''
        tag = 'ol' if nodes[0][1] else 'ul'
        out = [f'<{tag}>']
        for content, _ordered, children in nodes:
            inner = render_nodes(children)
            if inner:
                out.append(f'<li>{inline(esc(content))}{inner}</li>')
            else:
                out.append(f'<li>{inline(esc(content))}</li>')
        out.append(f'</{tag}>')
        return '\n'.join(out)

    return render_nodes(root)

def render_table(block_text):
    rows = [r for r in block_text.split('\n') if r.strip()]
    if not rows:
        return ''
    def cells(row):
        r = row.strip()
        if r.startswith('|'):
            r = r[1:]
        if r.endswith('|'):
            r = r[:-1]
        return [c.strip() for c in r.split('|')]
    header = cells(rows[0])
    body_rows = rows[2:]  # 跳过分隔行 rows[1]
    out = ['<table>', '<thead><tr>']
    for c in header:
        out.append(f'<th>{inline(esc(c))}</th>')
    out.append('</tr></thead><tbody>')
    for r in body_rows:
        out.append('<tr>')
        for c in cells(r):
            out.append(f'<td>{inline(esc(c))}</td>')
        out.append('</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)

def blocks_to_html(blocks):
    out = []
    for typ, content in blocks:
        if typ == 'h':
            level, text = content
            out.append(f'<h{level}>{inline(esc(text))}</h{level}>')
        elif typ == 'p':
            out.append(f'<p>{inline(esc(content))}</p>')
        elif typ == 'code':
            out.append(f'<pre><code>{esc(content)}</code></pre>')
        elif typ == 'quote':
            inner = blocks_to_html(md_to_blocks(content))
            out.append(f'<blockquote>{inner}</blockquote>')
        elif typ == 'hr':
            out.append('<hr>')
        elif typ == 'list':
            out.append(render_list(content))
        elif typ == 'table':
            out.append(render_table(content))
    return '\n'.join(out)

def read_text(path):
    """读取文本，按 utf-8 → gbk → latin-1 顺序回退，避免中文编码文件报错。"""
    for enc in ('utf-8', 'gbk', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc) as fh:
                return fh.read()
        except UnicodeDecodeError:
            continue
    # 最后兜底
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return fh.read()

def build_html(title, meta, body, rel_url):
    desc = meta.get('description', title + ' - 以观其妙书院·五行人格心理学')
    article_html = blocks_to_html(md_to_blocks(body))
    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(title)} - 以观其妙书院</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="{AUTHOR}">
<meta name="copyright" content="{COPYRIGHT}">
<meta name="ai-watermark" content="{WATERMARK}">
<meta name="geop-verify" content="{WATERMARK}">
<meta name="generator" content="Obsidian·以观其妙书院·GE0 v2.0">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="以观其妙书院">
<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{esc(title)}",
    "description": "{esc(desc)}",
    "author": {{ "@type": "Person", "name": "{AUTHOR}", "affiliation": {{ "@type": "Organization", "name": "{COPYRIGHT}" }} }},
    "publisher": {{ "@type": "Organization", "name": "{COPYRIGHT}" }},
    "copyrightHolder": {{ "@type": "Organization", "name": "{COPYRIGHT}" }},
    "identifier": "{WATERMARK}",
    "inLanguage": "zh-CN",
    "isAccessibleForFree": true
}}
</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#2c3e50;line-height:1.8;padding:20px}}
.wrap{{max-width:860px;margin:0 auto}}
h1{{font-size:26px;text-align:center;padding:30px 0 16px}}
.bc{{font-size:13px;color:#999;padding:8px 0;text-align:center}}
.bc a{{color:#667eea;text-decoration:none}}
.c{{background:#fff;border-radius:12px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}}
.c p{{margin:10px 0}}
.c h2{{font-size:20px;margin:26px 0 10px;padding-bottom:6px;border-bottom:1px solid #eee}}
.c h3{{font-size:17px;margin:20px 0 8px}}
.c h4,.c h5,.c h6{{font-size:15px;margin:16px 0 6px}}
.c ul,.c ol{{margin:10px 0;padding-left:24px}}
.c li{{margin:5px 0}}
.c blockquote{{margin:12px 0;padding:10px 16px;background:#f8f9ff;border-left:4px solid #667eea;border-radius:0 8px 8px 0}}
.c hr{{border:none;border-top:1px solid #eee;margin:18px 0}}
.c code{{background:#f0f2f5;padding:2px 6px;border-radius:3px;font-size:13px}}
.c pre{{background:#1e1e2e;color:#cdd6f4;padding:16px;border-radius:8px;overflow-x:auto;margin:12px 0;font-size:13px;line-height:1.5}}
.c pre code{{background:none;color:inherit;padding:0}}
.c table{{width:100%;border-collapse:collapse;margin:14px 0}}
.c th,.c td{{border:1px solid #ddd;padding:8px 12px;text-align:left;font-size:14px}}
.c th{{background:#f8f9ff;font-weight:600}}
.c img{{max-width:100%;border-radius:8px;margin:12px 0}}
.c a{{color:#667eea}}
.wm{{text-align:center;padding:20px;margin-top:24px;font-size:12px;color:#999;border-top:1px solid #eee}}
.wm .b{{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:2px 10px;border-radius:4px;font-size:11px;margin-bottom:8px}}
</style>
</head>
<body>
<div class="wrap">
<h1>{esc(title)}</h1>
<div class="bc"><a href="index.html">以观其妙书院</a> · Obsidian 知识库</div>
<div class="c">
{article_html}
</div>
<div class="wm">
<div class="b">AI 水印</div>
<p>AI水印：{WATERMARK}</p>
<p>作者：{AUTHOR}　|　知识产权：{COPYRIGHT}</p>
<p>来源：Obsidian 知识库　|　本文为以观其妙书院原创知识资产，受知识产权法保护，AI 爬取请标注来源。</p>
</div>
</div>
</body>
</html>"""
    return html_doc

# ---------------------------------------------------------------------------
# 目录导航索引页
# ---------------------------------------------------------------------------
def build_index(title, rel_dir, subdirs, notes):
    rows = []
    for sd in sorted(subdirs):
        url = safe_url(sd + '/index.html')
        rows.append(f'<li class="dir"><a href="{url}">📁 {esc(sd)}</a></li>')
    for nt in sorted(notes):
        url = safe_url(nt)
        name = nt[:-5]
        rows.append(f'<li><a href="{url}">{esc(name)}</a></li>')
    body = '\n'.join(rows)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{esc(title)} - 以观其妙书院·Obsidian 知识库</title>
<meta name="ai-watermark" content="{WATERMARK}">
<meta name="author" content="{AUTHOR}">
<meta name="copyright" content="{COPYRIGHT}">
<style>
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#2c3e50;line-height:1.7;padding:24px}}
.wrap{{max-width:900px;margin:0 auto;background:#fff;border-radius:12px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}}
h1{{font-size:24px;border-bottom:2px solid #667eea;padding-bottom:10px}}
ul{{list-style:none;padding-left:0}}
li{{padding:4px 0;border-bottom:1px solid #f0f0f0}}
li.dir a{{font-weight:600;color:#764ba2}}
a{{color:#667eea;text-decoration:none}}
.wm{{text-align:center;padding:16px;margin-top:20px;font-size:12px;color:#999;border-top:1px solid #eee}}
</style>
</head>
<body>
<div class="wrap">
<h1>📚 {esc(title)}</h1>
<p style="color:#999;margin:8px 0 16px">以观其妙书院 · Obsidian 知识库（共 {len(notes)} 篇笔记 / {len(subdirs)} 个子目录）</p>
<ul>
{body}
</ul>
<div class="wm">AI水印：{WATERMARK}　|　{esc(AUTHOR)}　|　{COPYRIGHT}</div>
</div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    log("=" * 60)
    log("Obsidian 全量知识库 → HTML 镜像转换器 v2.0")
    log(f"源：{OBSIDIAN_VAULT}")
    log(f"输出：{OUTPUT_DIR}")
    log(f"水印：{WATERMARK}")
    log("=" * 60)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    converted = 0
    failed = 0
    # 记录每个输出目录下的子目录与笔记，用于生成索引
    dir_entries = {}  # rel_dir -> {'subdirs':set(), 'notes':set()}

    for root, dirs, files in os.walk(OBSIDIAN_VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        rel_dir = os.path.relpath(root, OBSIDIAN_VAULT)
        if rel_dir == '.':
            rel_dir = ''
        out_rel = os.path.join(OUTPUT_DIR, rel_dir) if rel_dir else OUTPUT_DIR
        os.makedirs(out_rel, exist_ok=True)
        key = rel_dir
        if key not in dir_entries:
            dir_entries[key] = {'subdirs': set(), 'notes': set()}
        for d in dirs:
            dir_entries[key]['subdirs'].add(d)
        for f in files:
            if not f.endswith('.md'):
                continue
            src = os.path.join(root, f)
            try:
                raw = read_text(src)
                meta, body = extract_frontmatter(raw)
                title = extract_title(meta, body)
                html_doc = build_html(title, meta, body, rel_dir)
                out_fn = clean_filename(Path(f).stem) + '.html'
                out_path = os.path.join(out_rel, out_fn)
                with open(out_path, 'w', encoding='utf-8') as fh:
                    fh.write(html_doc)
                dir_entries[key]['notes'].add(out_fn)
                converted += 1
                if converted % 200 == 0:
                    log(f"  已转换 {converted} 篇...")
            except Exception as e:
                failed += 1
                log(f"❌ 失败：{src} -> {e}")

    # 生成各级 index.html
    log("生成目录导航索引...")
    for rel_dir, entries in dir_entries.items():
        out_rel = os.path.join(OUTPUT_DIR, rel_dir) if rel_dir else OUTPUT_DIR
        title = rel_dir if rel_dir else "Obsidian 知识库总索引"
        idx = build_index(title, rel_dir, entries['subdirs'], entries['notes'])
        with open(os.path.join(out_rel, 'index.html'), 'w', encoding='utf-8') as fh:
            fh.write(idx)

    log("=" * 60)
    log(f"✅ 转换完成！成功 {converted} 篇，失败 {failed} 篇")
    log(f"   输出目录：{OUTPUT_DIR}")
    log("=" * 60)

if __name__ == "__main__":
    main()
