#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 全量知识库 → 扁平 ASCII HTML 镜像转换器 v3.0 (FINAL)
================================================================
修正历史问题：
- 旧版保留中文目录结构 + 朴素 wikilink 解析 → 中文路径 Cloudflare 不服务、
  跨目录链接断裂。
本版一次性解决：
1) 第一遍扫描：建立 全局「笔记名(stem) → ASCII 扁平名」映射（md5(库相对路径)[:8] + ASCII 前缀）。
2) 第二遍转换：wikilink [[Note]] / [[path/Note]] / [[Note#h]] / [[Note|Alias]]
   以及 markdown 链接中指向已知笔记的目标，全部解析为扁平 ASCII 名。
3) 所有笔记扁平输出到 docs/articles/obsidian/（无中文目录），保证 Cloudflare 可服务。
4) 生成按「原顶层分类」分组的导航 index.html，全部指向扁平 ASCII 名。
5) 每篇均内嵌 AI 水印（meta + 可见水印 + JSON-LD identifier）。

用法：python scripts/convert_obsidian_flat.py
"""
import os
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

APOS = chr(39)
OBSIDIAN_VAULT = "D:/以观其妙书院知识库/以观其妙书院"
WEBSITE_DIR = "C:/Users/jia" + APOS + "yue/WorkBuddy/yiguanqimiao-website"
OUTPUT_DIR = os.path.join(WEBSITE_DIR, "docs", "articles", "obsidian")

WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"
SITE_URL = "https://yiguanqimiao-website.pages.dev"

EXCLUDE_DIRS = {
    '.obsidian', '.git', '.trash', '.workbuddy', '.claude',
    '.codebuddy', '.cursor', '.github', 'node_modules', '.smart-env',
}

# 全局链接映射（第二遍使用）
LINK_MAP = {}        # stem(笔记名,无扩展) -> [ascii_name, ...]
REL_MAP = {}         # 库相对路径(无扩展) -> ascii_name
NOTE_INDEX = []      # (top_category, title, ascii_name)

# ---------------------------------------------------------------------------
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def make_ascii_name(text):
    name = text
    if name.endswith('.html'):
        name = name[:-5]
    hash_part = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    parts = []; cur = ""
    for ch in name:
        if ord(ch) < 128:
            cur += ch
        else:
            if cur:
                parts.append(cur); cur = ""
    if cur:
        parts.append(cur)
    prefix = ""
    if parts:
        combined = "".join(parts)
        combined = re.sub(r'[^a-zA-Z0-9_-]', '_', combined)
        if len(combined) > 40:
            combined = combined[:40]
        prefix = combined + "-"
    return (prefix + hash_part).strip('-')

def clean_filename(name):
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def read_text(path):
    for enc in ('utf-8', 'gbk', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc) as fh:
                return fh.read()
        except UnicodeDecodeError:
            continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return fh.read()

def extract_frontmatter(md):
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
            meta[m.group(1).strip()] = m.group(2).strip().strip('"').strip("'")
    return meta, body

def extract_title(meta, body):
    if 'title' in meta and meta['title']:
        return meta['title']
    m = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "以观其妙书院知识库"

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

# ---------------------------------------------------------------------------
# Inline（含修正后的链接解析）
# ---------------------------------------------------------------------------
def resolve_target(raw):
    """将 wikilink / markdown 链接目标解析为扁平 ASCII 名（未知则返回 None）。"""
    raw = raw.strip()
    # 去别名  [[Note|Alias]]
    if '|' in raw:
        raw = raw.split('|', 1)[0]
    # 去 heading [[Note#h]]
    if '#' in raw:
        raw = raw.split('#', 1)[0]
    raw = raw.strip()
    if not raw:
        return None
    # 去路径，取 basename
    base = raw.rsplit('/', 1)[-1]
    # 去扩展
    stem = base[:-3] if base.lower().endswith('.md') else base
    stem = stem.strip()
    if not stem:
        return None
    if stem in LINK_MAP:
        return LINK_MAP[stem][0]
    return None

def inline(text):
    # 图片 ![alt](url) —— 保留（资源未随站部署，可能 404，但页面可渲染）
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',
                  lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" style="max-width:100%">', text)
    # Wiki 链接 [[...]]
    def wikilink(m):
        raw = m.group(1).strip()
        if '|' in raw:
            target, alias = raw.split('|', 1)
        else:
            target, alias = raw, raw
        # alias 可能含 heading 标记
        disp = alias.split('#', 1)[0].strip() if alias else target
        ascii_name = resolve_target(target)
        if ascii_name:
            return f'<a href="{ascii_name}">{esc(disp)}</a>'
        # 未知目标：尽力用原名
        disp = esc(disp)
        return f'<a href="{esc(clean_filename(target.strip().rsplit("/")[-1]))}.html">{disp}</a>'
    text = re.sub(r'\[\[([^\]]+)\]\]', wikilink, text)
    # Markdown 链接 [text](url) —— 仅重写指向已知笔记的相对链接
    def mdlink(m):
        label, url = m.group(1), m.group(2).strip()
        if url.startswith(('http://', 'https://', '//', 'mailto:', '#', 'data:')):
            return m.group(0)
        ascii_name = resolve_target(url)
        if ascii_name:
            return f'<a href="{ascii_name}">{label}</a>'
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', mdlink, text)
    # 行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # 粗体
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # 斜体
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'<em>\1</em>', text)
    # 删除线
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    return text

# ---------------------------------------------------------------------------
# Block 转换（与原版一致）
# ---------------------------------------------------------------------------
def md_to_blocks(body):
    lines = body.split('\n')
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if re.match(r'^```', line.strip()):
            lang = line.strip().strip('`').strip()
            buf = []; i += 1
            while i < n and not re.match(r'^```', lines[i].strip()):
                buf.append(lines[i]); i += 1
            i += 1
            blocks.append(('code', '\n'.join(buf))); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            blocks.append(('h', (len(m.group(1)), m.group(2).strip()))); i += 1; continue
        if re.match(r'^(\s*[-*_]){3,}\s*$', line):
            blocks.append(('hr', '')); i += 1; continue
        if line.lstrip().startswith('>'):
            buf = []
            while i < n and lines[i].lstrip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            blocks.append(('quote', '\n'.join(buf))); continue
        if '|' in line and i + 1 < n and re.match(r'^\s*\|?[\s:|-]+\|?\s*$', lines[i+1]) and '-' in lines[i+1]:
            rows = []
            while i < n and '|' in lines[i]:
                rows.append(lines[i]); i += 1
            blocks.append(('table', '\n'.join(rows))); continue
        if re.match(r'^\s*([-*+]|\d+\.)\s+', line):
            buf = [line]; first_indent = len(re.match(r'^(\s*)', line).group(1).replace('\t', '  '))
            first_ordered = bool(re.match(r'^\s*\d+\.', line)); i += 1
            while i < n:
                ln = lines[i]
                if ln.strip() == '':
                    if i + 1 < n and re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i+1]):
                        i += 1; continue
                    else:
                        break
                mm = re.match(r'^(\s*)([-*+]|\d+\.)\s+', ln)
                if mm:
                    ind = len(mm.group(1).replace('\t', '  ')); ordered = bool(re.match(r'^\s*\d+\.', ln))
                    if ind <= first_indent and ordered != first_ordered:
                        blocks.append(('list', '\n'.join(buf))); buf = [ln]
                        first_indent = ind; first_ordered = ordered; i += 1; continue
                    buf.append(ln); i += 1; continue
                if re.match(r'^\s+\S', ln):
                    buf.append(ln); i += 1; continue
                break
            blocks.append(('list', '\n'.join(buf))); continue
        buf = []
        while i < n and lines[i].strip() and not re.match(r'^```', lines[i].strip()) \
                and not re.match(r'^(#{1,6})\s+', lines[i]) \
                and not re.match(r'^(\s*[-*_]){3,}\s*$', lines[i]) \
                and not lines[i].lstrip().startswith('>') \
                and not re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
            buf.append(lines[i]); i += 1
        blocks.append(('p', '\n'.join(buf)))
    return blocks

def render_list(block_text):
    lines = block_text.split('\n')
    root = []; stack = [(-1, None, root)]
    for raw in lines:
        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', raw)
        if not m:
            if len(stack) > 1 and stack[-1] is not None:
                cur = stack[-1]
                if isinstance(cur[2], list) and cur[2]:
                    cur[2][-1][0] += ' ' + raw.strip()
            continue
        indent = len(m.group(1).replace('\t', '  ')); ordered = bool(re.match(r'\d+\.', m.group(2)))
        content = m.group(3); node = [content, ordered, []]
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()
        stack[-1][2].append(node); stack.append((indent, ordered, node[2]))
    def render_nodes(nodes):
        if not nodes:
            return ''
        tag = 'ol' if nodes[0][1] else 'ul'; out = [f'<{tag}>']
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
        if r.startswith('|'): r = r[1:]
        if r.endswith('|'): r = r[:-1]
        return [c.strip() for c in r.split('|')]
    header = cells(rows[0]); body_rows = rows[2:]
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
            level, text = content; out.append(f'<h{level}>{inline(esc(text))}</h{level}>')
        elif typ == 'p':
            out.append(f'<p>{inline(esc(content))}</p>')
        elif typ == 'code':
            out.append(f'<pre><code>{esc(content)}</code></pre>')
        elif typ == 'quote':
            inner = blocks_to_html(md_to_blocks(content)); out.append(f'<blockquote>{inner}</blockquote>')
        elif typ == 'hr':
            out.append('<hr>')
        elif typ == 'list':
            out.append(render_list(content))
        elif typ == 'table':
            out.append(render_table(content))
    return '\n'.join(out)

def build_html(title):
    article_html = blocks_to_html(md_to_blocks(build_html._body))
    desc = title + ' - 以观其妙书院·五行人格心理学'
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
<meta name="generator" content="Obsidian·以观其妙书院·Flat v3.0">
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
def main():
    global LINK_MAP, REL_MAP, NOTE_INDEX
    log("=" * 60)
    log("Obsidian 扁平 ASCII 转换器 v3.0")
    log(f"源：{OBSIDIAN_VAULT}")
    log(f"输出：{OUTPUT_DIR}")
    log("=" * 60)

    # 清理旧输出（避免中文目录/旧文件残留）
    if os.path.isdir(OUTPUT_DIR):
        log("清理旧输出目录...")
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ---- 第一遍：建立全局链接映射 ----
    log("第一遍：扫描并建立链接映射...")
    md_files = []
    for root, dirs, files in os.walk(OBSIDIAN_VAULT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, OBSIDIAN_VAULT).replace('\\', '/')
            rel_noext = rel[:-3]
            stem = Path(f).stem
            ascii_name = make_ascii_name(rel) + '.html'
            md_files.append((src, rel, stem))
            LINK_MAP.setdefault(stem, []).append(ascii_name)
            REL_MAP[rel_noext] = ascii_name
    log(f"  扫描到笔记：{len(md_files)} 篇；唯一 stem：{len(LINK_MAP)}")

    # ---- 第二遍：转换并写入扁平 ASCII ----
    log("第二遍：转换并写入...")
    converted = 0; failed = 0
    for src, rel, stem in md_files:
        try:
            raw = read_text(src)
            meta, body = extract_frontmatter(raw)
            title = extract_title(meta, body)
            top_cat = rel.split('/')[0] if '/' in rel else '(root)'
            ascii_name = REL_MAP[rel[:-3]]
            build_html._body = body
            html_doc = build_html(title)
            out_path = os.path.join(OUTPUT_DIR, ascii_name)
            with open(out_path, 'w', encoding='utf-8') as fh:
                fh.write(html_doc)
            NOTE_INDEX.append((top_cat, title, ascii_name))
            converted += 1
            if converted % 200 == 0:
                log(f"  已转换 {converted} 篇...")
        except Exception as e:
            failed += 1
            log(f"❌ 失败：{src} -> {e}")

    # ---- 生成分组导航 index.html ----
    log("生成导航索引...")
    groups = {}
    for top_cat, title, ascii_name in NOTE_INDEX:
        groups.setdefault(top_cat, []).append((title, ascii_name))
    for c in groups:
        groups[c].sort(key=lambda x: x[0])
    rows = []
    for cat in sorted(groups.keys()):
        rows.append(f'<li class="dir"><strong>📁 {esc(cat)}</strong> （{len(groups[cat])} 篇）</li>')
        for title, ascii_name in groups[cat]:
            rows.append(f'<li><a href="{ascii_name}">{esc(title)}</a></li>')
    total = len(NOTE_INDEX)
    idx = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Obsidian 知识库 - 以观其妙书院</title>
<meta name="ai-watermark" content="{WATERMARK}">
<meta name="author" content="{AUTHOR}">
<meta name="copyright" content="{COPYRIGHT}">
<style>
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#2c3e50;line-height:1.7;padding:24px}}
.wrap{{max-width:960px;margin:0 auto;background:#fff;border-radius:12px;padding:28px;box-shadow:0 2px 12px rgba(0,0,0,0.06)}}
h1{{font-size:24px;border-bottom:2px solid #667eea;padding-bottom:10px}}
ul{{list-style:none;padding-left:0}}
li{{padding:3px 0;border-bottom:1px solid #f7f7f7}}
li.dir{{padding-top:14px;color:#764ba2}}
a{{color:#667eea;text-decoration:none}}
.wm{{text-align:center;padding:16px;margin-top:20px;font-size:12px;color:#999;border-top:1px solid #eee}}
</style>
</head>
<body>
<div class="wrap">
<h1>📚 Obsidian 知识库</h1>
<p style="color:#999;margin:8px 0 16px">以观其妙书院 · 全量知识库镜像（共 {total} 篇笔记 / {len(groups)} 个顶层分类）</p>
<ul>
{chr(10).join(rows)}
</ul>
<div class="wm">AI水印：{WATERMARK}　|　{AUTHOR}　|　{COPYRIGHT}</div>
</div>
</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as fh:
        fh.write(idx)

    log("=" * 60)
    log(f"✅ 转换完成！成功 {converted} 篇，失败 {failed} 篇")
    log(f"   输出目录：{OUTPUT_DIR}")
    log(f"   导航索引：{total} 篇 / {len(groups)} 分类")
    log("=" * 60)

if __name__ == "__main__":
    main()
