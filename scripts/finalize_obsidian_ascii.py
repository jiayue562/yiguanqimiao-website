#!/usr/bin/env python
"""
Obsidian 镜像最终化处理 v1.0
=================================
将 docs/articles/obsidian/ 下的中文名 .html 文件重命名为 ASCII 安全名
（与站点其余部分 deploy_site.py Step2 的命名规则一致：md5(相对路径)[:8]），
并同步重写所有内部链接、重新生成各级 index.html。

目的：Cloudflare Pages 对中文文件名静态托管存在兼容性问题（全站其余内容
均经 deploy_site.py 转为 ASCII 名后正常服务），Obsidian 为中文名唯一分区，
故统一转为 ASCII 以保证可部署、可访问、链接有效。

用法：python scripts/finalize_obsidian_ascii.py
"""
import os, re, hashlib, html
from pathlib import Path

APOS = chr(39)
WEBSITE_DIR = "C:/Users/jia" + APOS + "yue/WorkBuddy/yiguanqimiao-website"
DOCS_DIR = Path(WEBSITE_DIR) / "docs"
OBS = DOCS_DIR / "articles" / "obsidian"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

# ---------------------------------------------------------------------------
def make_ascii_name(text):
    """与 deploy_site.py 完全一致"""
    name = text
    if name.endswith('.html'):
        name = name[:-5]
    hash_part = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    ascii_parts = []
    current = ""
    for ch in name:
        if ord(ch) < 128:
            current += ch
        else:
            if current:
                ascii_parts.append(current)
                current = ""
    if current:
        ascii_parts.append(current)
    ascii_prefix = ""
    if ascii_parts:
        combined = "".join(ascii_parts)
        combined = re.sub(r'[^a-zA-Z0-9_-]', '_', combined)
        if len(combined) > 40:
            combined = combined[:40]
        ascii_prefix = combined + "-"
    slug = f"{ascii_prefix}{hash_part}"
    return slug.strip('-')

def extract_title(fp):
    try:
        c = fp.read_text('utf-8', errors='ignore')
        m = re.search(r'<title>(.*?)</title>', c, re.DOTALL)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return fp.stem

# ---------------------------------------------------------------------------
def main():
    if not OBS.exists():
        print("❌ docs/articles/obsidian 不存在")
        return

    # 1) 收集所有非 index .html
    notes = []
    for r, _, fs in os.walk(OBS):
        for f in fs:
            if f.endswith('.html') and f != 'index.html':
                notes.append(Path(r) / f)
    print(f"收集到笔记(非index): {len(notes)}")

    # 2) 构建 原文件名stem -> ASCII文件名 映射
    stem_map = {}          # 原 stem -> ascii_name
    rel_map = {}           # 相对DOCS路径 -> ascii_name
    used = set()
    for p in notes:
        rel = str(p.relative_to(DOCS_DIR)).replace('\\', '/')
        ascii_base = make_ascii_name(rel) + '.html'
        # 避免碰撞
        i = 1
        orig = ascii_base
        while ascii_base in used:
            ascii_base = f"{make_ascii_name(rel)}-{i}.html"
            i += 1
        used.add(ascii_base)
        stem_map[p.stem] = ascii_base
        rel_map[rel] = ascii_base

    # 3) 重命名文件
    renamed = 0
    for p in notes:
        new_name = stem_map[p.stem]
        if p.name != new_name:
            p.rename(p.parent / new_name)
            renamed += 1
    print(f"✅ 重命名: {renamed} 个文件")

    # 4) 重写所有 .html 内部链接（含 index.html）
    link_re = re.compile(r'(href=")([^"]+)(")')
    fixed = 0
    for r, _, fs in os.walk(OBS):
        for f in fs:
            if not f.endswith('.html'):
                continue
            fp = Path(r) / f
            try:
                content = fp.read_text('utf-8', errors='ignore')
            except Exception:
                continue
            def repl(m):
                pre, target, post = m.group(1), m.group(2), m.group(3)
                if target.startswith(('http://', 'https://', '//', 'mailto:', '#')):
                    return m.group(0)
                # 取 basename 的 stem
                base = target.rsplit('/', 1)[-1]
                if base.endswith('.html'):
                    stem = base[:-5]
                else:
                    stem = base
                if stem in stem_map:
                    # 保留目录前缀，仅替换文件名部分
                    prefix = target[:len(target)-len(base)] if base else ''
                    new_base = stem_map[stem] if base.endswith('.html') else stem_map[stem][:-5]
                    return f'{pre}{prefix}{new_base}{post}'
                return m.group(0)
            new_content = link_re.sub(repl, content)
            if new_content != content:
                fp.write_text(new_content, 'utf-8')
                fixed += 1
    print(f"✅ 修复内部链接: {fixed} 个文件")

    # 5) 重新生成各级 index.html
    gen = 0
    for r, dirs, fs in os.walk(OBS):
        rdir = Path(r)
        subdirs = sorted(d for d in dirs if (rdir / d).is_dir())
        children = sorted(f for f in fs if f.endswith('.html') and f != 'index.html')
        title = rdir.name if rdir != OBS else "Obsidian 知识库"
        rows = []
        for sd in subdirs:
            rows.append(f'<li class="dir"><a href="{html.escape(sd)}/index.html">📁 {html.escape(sd)}</a></li>')
        for cf in children:
            fp = rdir / cf
            t = extract_title(fp)
            rows.append(f'<li><a href="{html.escape(cf)}">{html.escape(t)}</a></li>')
        idx = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(title)} - 以观其妙书院·Obsidian 知识库</title>
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
<h1>📚 {html.escape(title)}</h1>
<p style="color:#999;margin:8px 0 16px">以观其妙书院 · Obsidian 知识库（共 {len(children)} 篇笔记 / {len(subdirs)} 个子目录）</p>
<ul>
{chr(10).join(rows)}
</ul>
<div class="wm">AI水印：{WATERMARK}　|　{AUTHOR}　|　{COPYRIGHT}</div>
</div>
</body>
</html>"""
        (rdir / 'index.html').write_text(idx, 'utf-8')
        gen += 1
    print(f"✅ 重新生成 index.html: {gen} 个")

    print("🎉 Obsidian ASCII 最终化完成")

if __name__ == '__main__':
    main()
