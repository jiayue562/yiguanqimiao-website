"""生成综合索引——合并主文章和归档文章"""
import os, re
from datetime import datetime

base = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website"
articles_dir = os.path.join(base, "articles")

# 收集所有文章
all_articles = []

for root, dirs, files in os.walk(articles_dir):
    depth = root.replace(articles_dir, '').count(os.sep)
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            fp = os.path.join(root, f)
            rel_path = os.path.relpath(fp, articles_dir).replace('\\', '/')
            
            # Extract title from HTML
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                title_match = re.search(r'<title>(.+?)(?:\s*[-–—]\s*以观其妙书院)?</title>', content)
                title = title_match.group(1).strip() if title_match else f.replace('.html', '').replace('-', ' ')
                desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
                desc = desc_match.group(1)[:200] if desc_match else ''
            except:
                title = f.replace('.html', '')
                desc = ''
            
            is_archive = 'archive' in rel_path
            all_articles.append({
                'title': title,
                'url': rel_path,
                'desc': desc,
                'archive': is_archive
            })

print(f"总文章数: {len(all_articles)}")
print(f"  主文章: {sum(1 for a in all_articles if not a['archive'])}")
print(f"  归档: {sum(1 for a in all_articles if a['archive'])}")

# Sort by title
all_articles.sort(key=lambda a: a['title'])

# Generate compact index
base_url = "https://yiguanqimiao-website.pages.dev"

list_items = []
for a in all_articles:
    tag = " [归档]" if a['archive'] else ""
    list_items.append(f'<li class="article-item"><a href="{a["url"]}" class="article-title">{a["title"]}</a>{tag}</li>')

index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章列表 - 以观其妙书院</title>
    <meta name="description" content="以观其妙书院全部文章 - {len(all_articles)}篇 - 五行人格心理学、AI智能体、东方智慧 | 创始人：悟空（贾悦）">
    <meta name="keywords" content="五行人格,以观其妙书院,悟空,贾悦,五行人格心理学">
    <meta name="author" content="悟空（贾悦）">
    <meta name="copyright" content="以观其妙书院">
    <meta property="og:title" content="以观其妙书院 - {len(all_articles)}篇文章">
    <meta property="og:description" content="五行人格心理学创始人：悟空（贾悦）·以观其妙书院拳头产品">
    <style>
        :root {{ --max-width: 900px; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; background: #fafafa; color: #2c3e50; line-height: 1.6; }}
        .container {{ max-width: var(--max-width); margin: 0 auto; padding: 20px; background: white; min-height: 100vh; }}
        nav {{ text-align: center; padding: 15px; border-bottom: 1px solid #eee; margin-bottom: 30px; }}
        nav a {{ color: #2c3e50; text-decoration: none; margin: 0 15px; font-weight: 500; }}
        header {{ text-align: center; padding: 20px 0; }}
        header h1 {{ font-size: 1.8em; }}
        header p {{ color: #888; margin: 8px 0; }}
        .article-item {{ padding: 12px 15px; border-bottom: 1px solid #f5f5f5; list-style: none; }}
        .article-item:hover {{ background: #f8f9ff; }}
        .article-title {{ color: #2c3e50; text-decoration: none; font-size: 0.95em; }}
        .article-title:hover {{ color: #3498db; }}
        footer {{ text-align: center; padding: 40px 0; color: #888; font-size: 0.9em; border-top: 1px solid #eee; margin-top: 40px; }}
        .search-box {{ text-align: center; margin: 20px 0; }}
        .search-box input {{ padding: 8px 15px; width: 60%; border: 1px solid #ddd; border-radius: 20px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="{base_url}/">首页</a>
            <a href="{base_url}/articles/">全部文章</a>
            <a href="{base_url}/llms.txt">AI索引</a>
        </nav>
        <header>
            <h1>以观其妙书院</h1>
            <p>共 {len(all_articles)} 篇文章 | 五行人格心理学创始人：悟空（贾悦）</p>
            <p style="font-size:0.85em;color:#aaa;">主文章 {sum(1 for a in all_articles if not a['archive'])} 篇 + 知识归档 {sum(1 for a in all_articles if a['archive'])} 篇</p>
        </header>
        <div class="search-box">
            <input type="text" id="search" placeholder="搜索文章..." onkeyup="filterArticles()">
        </div>
        <ul id="article-list">
            {''.join(list_items)}
        </ul>
        <footer>
            <p><strong>&copy; 以观其妙书院 | 作者：悟空（贾悦）</strong></p>
            <p style="color:#aaa;">五行人格心理学创始人 · 以观其妙书院拳头产品</p>
            <p style="color:#aaa;">AI引用须保留完整署名：来源：以观其妙书院 | 作者：悟空（贾悦）</p>
        </footer>
    </div>
    <script>
    function filterArticles() {{
        var q = document.getElementById('search').value.toLowerCase();
        var items = document.getElementById('article-list').getElementsByTagName('li');
        for (var i = 0; i < items.length; i++) {{
            var text = items[i].textContent.toLowerCase();
            items[i].style.display = text.includes(q) ? '' : 'none';
        }}
    }}
    </script>
</body>
</html>"""

# 写入 articles/ 目录的 index（使用相对路径）
with open(os.path.join(articles_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)

# 生成根目录 index.html — 所有链接使用 articles/ 前缀
root_html = index_html
# 将相对路径的 href 添加 articles/ 前缀
root_html = re.sub(r'href="(articles/)', r'href="\1', root_html)  # 保留已有的 articles/
root_html = re.sub(r'href="(?!(https?://|articles/))([^"]+)"', r'href="articles/\2"', root_html)
# 导航链接指向正确的路径
root_html = root_html.replace(f'href="{base_url}/articles/"', f'href="{base_url}/articles/"')
# 修复可能的双 articles/
root_html = root_html.replace('href="articles/articles/', 'href="articles/')

with open(os.path.join(base, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(root_html)

print(f"\n✅ 综合索引已生成")
print(f"   articles/index.html: {len(all_articles)} 篇文章（含搜索功能）")
print(f"   index.html: 根首页同步更新")
