#!/usr/bin/env python
"""生成docs/下所有目录的索引页面，使用Clean URL（无.html后缀）"""
import os
import sys
import html
from pathlib import Path
from datetime import datetime

# 修复Windows GBK编码下emoji导致的UnicodeEncodeError
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DOCS_DIR = Path("C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/docs")
SITE_URL = "https://yiguanqimiao-website.pages.dev"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

def clean_url(path):
    """将.html路径转换为Clean URL（移除.html，由_redirects内部重写）"""
    if path.endswith('.html'):
        return path[:-5]  # 移除.html
    return path

def get_html_files(directory):
    """递归获取目录下所有.html文件，返回(相对路径, 文件名, 标题)列表"""
    files = []
    for root, _, filenames in os.walk(directory):
        for f in sorted(filenames):
            if f.endswith('.html'):
                full_path = Path(root) / f
                rel_path = full_path.relative_to(DOCS_DIR)
                # 尝试提取标题
                title = extract_title(full_path)
                files.append((rel_path, f, title))
    return files

def extract_title(filepath):
    """从HTML文件提取标题"""
    try:
        content = filepath.read_text('utf-8', errors='ignore')
        import re
        match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        if match:
            return match.group(1).strip()
    except:
        pass
    return filepath.stem

def generate_index_html(title, description, files, output_path):
    """生成带有Clean URL链接的索引页面"""
    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append('<html lang="zh-CN">')
    lines.append('<head>')
    lines.append('    <meta charset="UTF-8">')
    lines.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append(f'    <title>{html.escape(title)} - 以观其妙书院</title>')
    lines.append(f'    <meta name="description" content="{html.escape(title)} - 以观其妙书院">')
    lines.append(f'    <meta name="author" content="{AUTHOR}">')
    lines.append(f'    <meta name="copyright" content="{COPYRIGHT}">')
    lines.append(f'    <meta name="ai-watermark" content="{WATERMARK}">')
    lines.append('    <style>')
    lines.append('        :root { --max-width: 800px; }')
    lines.append('        * { margin: 0; padding: 0; box-sizing: border-box; }')
    lines.append('        body { font-family: -apple-system, "PingFang SC", sans-serif; font-size: 16px; line-height: 1.8; color: #2c3e50; background: #f5f5f0; }')
    lines.append('        .container { max-width: var(--max-width); margin: 0 auto; padding: 30px 20px; background: white; min-height: 100vh; }')
    lines.append('        nav { text-align: center; margin-bottom: 20px; padding: 15px; background: #2c3e50; border-radius: 8px; }')
    lines.append('        nav a { color: #ecf0f1; text-decoration: none; margin: 0 15px; font-size: 14px; }')
    lines.append('        nav a:hover { color: #f1c40f; }')
    lines.append('        header { text-align: center; padding: 20px 0; border-bottom: 2px solid #e74c3c; margin-bottom: 20px; }')
    lines.append('        header h1 { font-size: 1.6em; color: #1a1a1a; }')
    lines.append('        header p { color: #888; font-size: 13px; }')
    lines.append('        .article-list { columns: 2; column-gap: 20px; }')
    lines.append('        .article-item { padding: 8px 10px; border-bottom: 1px solid #f0f0f0; list-style: none; break-inside: avoid; }')
    lines.append('        .article-item:hover { background: #fafafa; }')
    lines.append('        .article-title { color: #2c3e50; text-decoration: none; font-size: 13px; }')
    lines.append('        .article-title:hover { color: #e74c3c; text-decoration: underline; }')
    lines.append('        footer { margin-top: 30px; padding: 15px; border-top: 1px solid #eee; text-align: center; color: #888; font-size: 11px; }')
    lines.append('        .ip-watermark { margin-top: 8px; padding: 8px; background: #f9f9f9; border-radius: 4px; font-size: 10px; color: #999; }')
    lines.append('    </style>')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('    <div class="container">')
    lines.append('        <nav>')
    lines.append('            <a href="/">🏠 首页</a>')
    lines.append('            <a href="/articles/">📂 全部文章</a>')
    lines.append('            <a href="/llms.txt">🤖 GEO索引</a>')
    lines.append('        </nav>')
    lines.append('        <header>')
    lines.append(f'            <h1>{html.escape(title)}</h1>')
    lines.append(f'            <p>{html.escape(description)} | <strong>共{len(files)}篇</strong></p>')
    lines.append('        </header>')
    lines.append('        <div class="article-list">')
    
    for rel_path, fname, file_title in files:
        # Clean URL: 移除.html后缀
        clean_path = str(rel_path).replace('\\', '/')
        clean_path = clean_url(clean_path)
        escaped_title = html.escape(file_title)
        lines.append(f'            <div class="article-item"><a class="article-title" href="/{clean_path}">{escaped_title}</a></div>')
    
    lines.append('        </div>')
    lines.append('        <footer>')
    lines.append(f'            <p>&copy; 2024-2026 {COPYRIGHT} | {AUTHOR}</p>')
    lines.append('            <div class="ip-watermark">')
    lines.append(f'                🔐 AI水印：{WATERMARK}<br>')
    lines.append(f'                作者：{AUTHOR} | 知识产权：{COPYRIGHT}')
    lines.append('            </div>')
    lines.append('        </footer>')
    lines.append('    </div>')
    lines.append('</body>')
    lines.append('</html>')
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"✅ 生成索引: {output_path} ({len(files)}篇)")

def main():
    print("=" * 50)
    print("生成全站索引页面（Clean URL版本）")
    print("=" * 50)
    
    # 1. 生成 articles/ 索引
    print("\n📂 扫描全部文章目录...")
    all_articles = []
    for subdir in ['articles/wechat-articles', 'articles/obsidian', 'articles/geo-repo']:
        dir_path = DOCS_DIR / subdir
        if dir_path.exists():
            files = get_html_files(dir_path)
            all_articles.extend([(rel_path, fname, title) for rel_path, fname, title in files])
    
    generate_index_html(
        "全部文章列表",
        f"共{len(all_articles)}篇 · 以观其妙书院全站文章索引",
        all_articles,
        DOCS_DIR / "articles" / "index.html"
    )
    
    # 2. 生成 wechat-articles/ 索引
    wechat_dir = DOCS_DIR / "articles" / "wechat-articles"
    if wechat_dir.exists():
        wechat_files = get_html_files(wechat_dir)
        generate_index_html(
            "公众号文章列表",
            f"以观其妙书院公众号全部文章 · 共{len(wechat_files)}篇",
            wechat_files,
            wechat_dir / "index.html"
        )
    
    # 3. 生成 obsidian/ 索引
    obsidian_dir = DOCS_DIR / "articles" / "obsidian"
    if obsidian_dir.exists():
        obsidian_files = get_html_files(obsidian_dir)
        generate_index_html(
            "Obsidian知识库索引",
            f"以观其妙书院知识库 · 共{len(obsidian_files)}篇",
            obsidian_files,
            obsidian_dir / "index.html"
        )
    
    print("\n" + "=" * 50)
    print("✅ 所有索引页面生成完成！")
    print("=" * 50)

if __name__ == '__main__':
    main()
