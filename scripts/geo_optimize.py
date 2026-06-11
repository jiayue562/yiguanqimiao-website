#!/usr/bin/env python3
"""
GEO优化脚本 - 批量处理公众号文章，生成优化后的HTML和索引
用于 yiguanqimiao-website 自动部署
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

# 路径配置
CLAW_DIR = Path(r"C:\Users\jia'yue\WorkBuddy\Claw")
WEBSITE_DIR = Path(r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website")
ARTICLES_OUT_DIR = WEBSITE_DIR / "articles"

# 文章来源
SOURCES = [
    CLAW_DIR,  # Claw 根目录的主要文章
    CLAW_DIR / "wechat-articles",  # wechat-articles 目录
]

# 全局索引
all_articles = []

def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    meta = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_lines = parts[1].strip().split('\n')
            for line in yaml_lines:
                if ':' in line:
                    key, _, value = line.partition(':')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    meta[key] = value
    return meta

def extract_description(content: str, max_chars=200) -> str:
    """提取文章描述（前200字）"""
    # 移除 frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        body = parts[2] if len(parts) >= 3 else content
    else:
        body = content
    
    # 清理 markdown 标记
    cleaned = re.sub(r'[#*\[\]`>|]', '', body)
    cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', cleaned)
    cleaned = re.sub(r'\[([^\]]*)\]\(.*?\)', r'\1', cleaned)
    cleaned = cleaned.strip()
    
    # 跳过空行取前 max_chars 字
    lines = [l.strip() for l in cleaned.split('\n') if l.strip()]
    desc = ''.join(lines)[:max_chars].strip()
    return desc

def extract_keywords(meta: dict, content: str) -> str:
    """提取关键词"""
    if 'tags' in meta:
        tags = meta['tags']
        if isinstance(tags, list):
            return ', '.join(tags)
        return tags
    
    # 自动从内容提取关键词（简单版）
    keywords = ['五行人格', '以观其妙书院', '龙龟神将']
    title = meta.get('title', '')
    if '五行' in title:
        keywords.insert(0, '五行人格心理学')
    if 'AI' in title or 'AI' in content[:500]:
        keywords.append('人工智能')
    if '龙心' in title:
        keywords.append('龙心OS')
    return ', '.join(keywords[:8])

def markdown_to_html(markdown: str) -> str:
    """基础 Markdown → HTML 转换"""
    html = markdown
    
    # 移除 frontmatter
    if html.startswith('---'):
        parts = html.split('---', 2)
        html = parts[2] if len(parts) >= 3 else html
    
    # 标题转换
    html = re.sub(r'^#### (.*)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 加粗
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # 图片
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', html)
    
    # 代码块
    html = re.sub(r'```(.*?)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # 水平线
    html = re.sub(r'^---$', '<hr>', html, flags=re.MULTILINE)
    
    # 引用
    html = re.sub(r'^> (.*)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 无序列表
    html = re.sub(r'^[\-\*] (.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 段落（用双换行分割）
    blocks = html.split('\n\n')
    processed = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith('<'):
            processed.append(block)
        else:
            processed.append(f'<p>{block}</p>')
    
    return '\n\n'.join(processed)

def generate_article_html(meta: dict, content: str, filename: str) -> str:
    """为单篇文章生成 GEO 优化的 HTML"""
    title = meta.get('title', filename.replace('.md', '').replace('-', ' ').title())
    description = meta.get('description', extract_description(content))
    author = meta.get('author', '以观其妙书院')
    date = meta.get('date', datetime.now().strftime('%Y-%m-%d'))
    keywords = extract_keywords(meta, content)
    
    body_html = markdown_to_html(content)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 以观其妙书院</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{author}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://jiayue562.github.io/yiguanqimiao-website/articles/{filename.replace('.md', '.html')}">
    <meta property="og:site_name" content="以观其妙书院">
    <meta name="twitter:card" content="summary">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://jiayue562.github.io/yiguanqimiao-website/articles/{filename.replace('.md', '.html')}">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{description}",
      "author": {{"@type": "Person", "name": "{author}"}},
      "datePublished": "{date}",
      "publisher": {{"@type": "Organization", "name": "以观其妙书院"}}
    }}
    </script>
    <style>
        :root {{ --max-width: 800px; --font-size: 18px; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            font-size: var(--font-size);
            line-height: 1.8;
            color: #2c3e50;
            background: #fafafa;
            padding: 0;
        }}
        .container {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 40px 20px;
            background: white;
            min-height: 100vh;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }}
        header {{
            text-align: center;
            padding: 40px 0 20px;
            border-bottom: 2px solid #eee;
            margin-bottom: 40px;
        }}
        header h1 {{
            font-size: 2em;
            color: #1a1a1a;
            margin-bottom: 10px;
            line-height: 1.3;
        }}
        header .meta {{
            color: #888;
            font-size: 0.9em;
        }}
        header .meta span {{ margin: 0 10px; }}
        nav {{
            text-align: center;
            margin-bottom: 30px;
        }}
        nav a {{
            color: #2c3e50;
            text-decoration: none;
            margin: 0 15px;
            font-size: 0.95em;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background 0.2s;
        }}
        nav a:hover {{ background: #f0f0f0; }}
        article h1 {{ font-size: 1.8em; margin: 30px 0 15px; color: #1a1a1a; }}
        article h2 {{ font-size: 1.5em; margin: 25px 0 12px; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
        article h3 {{ font-size: 1.3em; margin: 20px 0 10px; color: #444; }}
        article h4 {{ font-size: 1.1em; margin: 15px 0 8px; color: #555; }}
        article p {{ margin: 12px 0; text-align: justify; }}
        article blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            color: #555;
            font-style: italic;
        }}
        article pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        article code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
        article pre code {{ background: none; padding: 0; }}
        article img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
        article hr {{ border: none; border-top: 1px solid #eee; margin: 30px 0; }}
        article ul, article ol {{ margin: 15px 0; padding-left: 25px; }}
        article li {{ margin: 8px 0; }}
        article strong {{ color: #1a1a1a; }}
        article a {{ color: #3498db; text-decoration: none; }}
        article a:hover {{ text-decoration: underline; }}
        .breadcrumb {{
            margin-bottom: 30px;
            color: #888;
            font-size: 0.9em;
        }}
        .breadcrumb a {{ color: #3498db; }}
        footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #888;
            font-size: 0.9em;
        }}
        footer a {{ color: #3498db; }}
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/yiguanqimiao-website/">首页</a>
            <a href="/yiguanqimiao-website/articles/">文章列表</a>
            <a href="/yiguanqimiao-website/llms.txt" target="_blank">GEO索引</a>
        </nav>
        
        <header>
            <h1>{title}</h1>
            <div class="meta">
                <span>📅 {date}</span>
                <span>✍️ {author}</span>
            </div>
        </header>
        
        <div class="breadcrumb">
            <a href="/yiguanqimiao-website/">首页</a> &raquo; 
            <a href="/yiguanqimiao-website/articles/">文章列表</a> &raquo; 
            {title[:30]}...
        </div>
        
        <article>
{body_html}
        </article>
        
        <footer>
            <p>&copy; 2024-2026 以观其妙书院 | 五行人格心理学</p>
            <p>
                <a href="https://github.com/jiayue562/yiguanqimiao-website">GitHub</a> | 
                <a href="/yiguanqimiao-website/llms.txt">llms.txt</a>
            </p>
        </footer>
    </div>
</body>
</html>"""
    return html

def process_article(filepath: Path, source_dir: Path) -> dict:
    """处理单篇文章"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        meta = parse_frontmatter(content)
        
        # 生成相对路径
        rel_path = filepath.relative_to(source_dir)
        out_name = str(rel_path).replace('\\', '/').replace('.md', '.html')
        
        # 生成输出路径
        out_path = ARTICLES_OUT_DIR / out_name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成 HTML
        html = generate_article_html(meta, content, filepath.name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        title = meta.get('title', filepath.stem.replace('-', ' ').title())
        description = meta.get('description', extract_description(content))
        date = meta.get('date', '')
        
        return {
            'title': title,
            'url': out_name,
            'description': description,
            'date': date,
            'source': str(filepath),
            'author': meta.get('author', '以观其妙书院')
        }
    except Exception as e:
        print(f"  ⚠️ 处理失败: {filepath} - {e}")
        return None

def collect_articles() -> list:
    """收集所有公众号文章"""
    articles = []
    
    for source_dir in SOURCES:
        if not source_dir.exists():
            continue
        
        search_dir = source_dir
        for filepath in search_dir.rglob("*.md"):
            # 跳过非公众号文章
            name = filepath.name
            rel = str(filepath.relative_to(source_dir))
            
            # 识别公众号文章的条件
            is_wechat = (
                '公众号' in name or 
                'wechat' in name.lower() or
                'wuxing' in name.lower() or
                '.xhs-' not in rel  # 排除小红书文章
            )
            
            # 排除某些非文章文件
            exclude_patterns = ['style', '规范', '分析', '建议', 'template', 'test', 'demo']
            should_exclude = any(p in name for p in exclude_patterns)
            
            if is_wechat and not should_exclude:
                result = process_article(filepath, search_dir)
                if result:
                    articles.append(result)
                    print(f"  ✅ {result['title'][:40]}...")
    
    return articles

def generate_index(articles: list):
    """生成文章索引页面"""
    sorted_articles = sorted(articles, key=lambda a: a.get('date', ''), reverse=True)
    
    list_items = []
    for a in sorted_articles:
        date_str = f" ({a['date']})" if a['date'] else ''
        list_items.append(f"""<li class="article-item">
            <a href="{a['url']}" class="article-title">{a['title']}</a>
            <span class="article-date">{date_str}</span>
            <p class="article-desc">{a['description'][:100]}...</p>
        </li>""")
    
    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章列表 - 以观其妙书院</title>
    <meta name="description" content="以观其妙书院全部公众号文章 - 五行人格心理学、AI智能体、东方智慧">
    <meta name="keywords" content="五行人格,以观其妙书院,公众号文章,AI智能体,东方智慧">
    <meta property="og:title" content="以观其妙书院文章列表">
    <meta property="og:description" content="共{len(sorted_articles)}篇深度文章">
    <style>
        :root {{ --max-width: 800px; --font-size: 16px; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            font-size: var(--font-size);
            line-height: 1.8;
            color: #2c3e50;
            background: #fafafa;
        }}
        .container {{ max-width: var(--max-width); margin: 0 auto; padding: 40px 20px; background: white; min-height: 100vh; box-shadow: 0 0 20px rgba(0,0,0,0.05); }}
        nav {{ text-align: center; margin-bottom: 30px; }}
        nav a {{ color: #2c3e50; text-decoration: none; margin: 0 15px; }}
        header {{ text-align: center; padding: 40px 0 20px; border-bottom: 2px solid #eee; margin-bottom: 40px; }}
        header h1 {{ font-size: 2em; color: #1a1a1a; }}
        header p {{ color: #888; margin-top: 10px; }}
        .article-item {{ padding: 20px; border-bottom: 1px solid #f0f0f0; list-style: none; }}
        .article-item:hover {{ background: #fafafa; }}
        .article-title {{ font-size: 1.2em; color: #2c3e50; text-decoration: none; font-weight: bold; }}
        .article-title:hover {{ color: #3498db; }}
        .article-date {{ color: #888; font-size: 0.85em; margin-left: 10px; }}
        .article-desc {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        footer {{ margin-top: 60px; padding: 40px 0; text-align: center; color: #888; border-top: 2px solid #eee; }}
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/yiguanqimiao-website/">首页</a>
            <a href="/yiguanqimiao-website/articles/">文章列表</a>
            <a href="/yiguanqimiao-website/llms.txt">GEO索引</a>
        </nav>
        <header>
            <h1>📚 文章列表</h1>
            <p>共 {len(sorted_articles)} 篇文章 | 每日更新</p>
        </header>
        <ul>
            {''.join(list_items)}
        </ul>
        <footer>
            <p>&copy; 2024-2026 以观其妙书院 | <a href="/yiguanqimiao-website/llms.txt">llms.txt</a></p>
        </footer>
    </div>
</body>
</html>"""
    
    (ARTICLES_OUT_DIR / "index.html").write_text(index_html, encoding='utf-8')
    print(f"\n📄 索引页已生成: {len(sorted_articles)} 篇文章")

def generate_llms_txt(articles: list):
    """生成 GEO 优化的 llms.txt"""
    sorted_articles = sorted(articles, key=lambda a: a.get('date', ''), reverse=True)
    
    lines = [
        "# llms.txt - 以观其妙书院",
        "",
        "> 本文件帮助 AI 模型理解和索引网站内容",
        "> 遵循 GEO (Generative Engine Optimization) 最佳实践",
        "",
        "## 网站信息",
        f"- 名称: 以观其妙书院",
        f"- 网址: https://jiayue562.github.io/yiguanqimiao-website/",
        f"- 简介: 传播五行人格心理学与东方智慧，探索 AI 时代的人文觉醒",
        f"- 语言: 中文（简体）",
        f"- 文章总数: {len(sorted_articles)}",
        f"- 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 核心主题",
        "- 五行人格心理学: 木火土金水五行人格分析与转化",
        "- AI 智能体: 龙龟共生OS、龙心OS、味藏智能体系统",
        "- 东方智慧: 象思维、大圆满、身语意",
        "- 组织进化: AI原生组织、人机协同、心文化",
        "- 个人成长: 拔阴取阳、化克为生、阴阳转化",
        "",
        "## 全部文章",
    ]
    
    for a in sorted_articles:
        date_str = f" ({a['date']})" if a.get('date') else ''
        desc = a.get('description', '')[:80]
        lines.append(f"- [{a['title']}](articles/{a['url']}){date_str} - {desc}")
    
    lines.extend([
        "",
        "## 系列文章",
        "### 五行人格系列 (9篇)",
    ])
    
    wuxing_patterns = ['wuxing-1', 'wuxing-2', 'wuxing-3', 'wuxing-4', 'wuxing-5', 'wuxing-6', 'wuxing-7', 'wuxing-8', 'wuxing-9']
    for a in sorted_articles:
        for p in wuxing_patterns:
            if p in a.get('url', ''):
                lines.append(f"- [{a['title']}](articles/{a['url']})")
                break
    
    lines.extend([
        "",
        "### AI OS 系列",
    ])
    
    for a in sorted_articles:
        if 'AI' in a.get('title', '') or '龙心' in a.get('title', '') or '智能体' in a.get('title', ''):
            lines.append(f"- [{a['title']}](articles/{a['url']})")
    
    lines.extend([
        "",
        "## 网站结构",
        "- /articles/ - 全部文章",
        "- /articles/index.html - 文章列表",
        "- /llms.txt - 本文件 (GEO 优化)",
        "- /yiguanqimiao/ - 龙龟神将备份资料",
        "- /wukong/ - 悟空日志",
        "",
        "## SEO 元数据",
        "- og:site_name: 以观其妙书院",
        "- Schema.org: Article (含 headline/description/author/datePublished)",
        "- robots: index, follow",
        "- canonical: 已设置",
    ])
    
    (WEBSITE_DIR / "llms.txt").write_text('\n'.join(lines), encoding='utf-8')
    print(f"📄 llms.txt 已更新: {len(sorted_articles)} 篇文章索引")

def main():
    print("🚀 开始 GEO 优化...\n")
    print("📁 收集公众号文章...\n")
    
    # 清空旧的 articles 目录
    if ARTICLES_OUT_DIR.exists():
        shutil.rmtree(ARTICLES_OUT_DIR)
    ARTICLES_OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 收集并处理文章
    articles = collect_articles()
    
    print(f"\n📊 共处理 {len(articles)} 篇文章\n")
    
    # 生成索引
    generate_index(articles)
    
    # 生成 llms.txt
    generate_llms_txt(articles)
    
    print(f"\n✅ GEO 优化完成！")
    print(f"   文章目录: {ARTICLES_OUT_DIR}")
    print(f"   文章总数: {len(articles)}")
    print(f"   llms.txt: {WEBSITE_DIR / 'llms.txt'}")

if __name__ == "__main__":
    main()
