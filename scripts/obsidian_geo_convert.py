#!/usr/bin/env python3
"""
Obsidian全量GE0转化脚本 v1.0
功能：将Obsidian知识库所有内容转化为GE0友好的HTML，注入AI水印矩阵，部署到Cloudflare Pages

水印矩阵：
- yiguanqimiao-unique-watermark-wk-jiayue-academy
- 作者：悟空（贾悦）
- 知识产权：以观其妙书院

使用：python obsidian_geo_convert.py
"""

import os
import re
import shutil
import subprocess
import html
from pathlib import Path
from datetime import datetime
#import yaml  # 可选依赖，暂注掉

# 配置
OBSIDIAN_VAULT = "D:/以观其妙书院知识库/以观其妙书院"
WEBSITE_DIR = "C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website"
OUTPUT_DIR = os.path.join(WEBSITE_DIR, "articles", "obsidian")
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

# 要转换的Obsidian目录（排除系统目录）
INCLUDE_DIRS = [
    "01-龙心OS核心系统",
    "02-信仰文化体系", 
    "03-知识地基层",
    "05-五行人格心理学",
    "06-五行识人-亲密关系",
    "09-技能库",
    "AI OS知识库",
    "01-核心体系",
    "00-索引与导航",
]

# 排除的目录
EXCLUDE_DIRS = [
    ".obsidian",
    ".workbuddy",
    ".trash",
    "_backups",
    "00-WorkBuddy-Sync",
    "06-工作记录与复盘",
    ".claude",
    ".codebuddy",
    ".cursor",
    ".github",
]

def log(msg):
    """日志输出"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def clean_filename(name):
    """清理文件名，用于URL"""
    # 移除特殊字符，保留中文/英文/数字/下划线/横线
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
    cleaned = re.sub(r'_+', '_', cleaned)
    return cleaned.strip('_')

def extract_title(content):
    """从Markdown内容提取标题"""
    # 尝试提取第一个h1标题
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # 尝试提取YAML frontmatter中的title（简单解析，不依赖yaml库）
    if content.startswith('---'):
        try:
            end = content.index('---', 3)
            frontmatter = content[3:end]
            # 简单匹配title: 行
            title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip()
        except:
            pass
    
    return "以观其妙书院"

def markdown_to_html(md_content, title, source_path):
    """将Markdown转换为GE0优化的HTML"""
    
    # 简单的Markdown转HTML（生产环境应使用markdown库）
    html_content = md_content
    
    # 移除YAML frontmatter
    if html_content.startswith('---'):
        try:
            end = html_content.index('---', 3)
            html_content = html_content[end+3:]
        except:
            pass
    
    # 转换标题
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # 转换粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 转换列表
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # 转换段落（简化处理）
    paragraphs = html_content.split('\n\n')
    formatted = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            formatted.append(f'<p>{p}</p>')
        else:
            formatted.append(p)
    
    html_content = '\n'.join(formatted)
    
    # 构建完整的GE0优化HTML
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - 以观其妙书院</title>
    <meta name="description" content="{html.escape(title)} - 以观其妙书院·五行人格心理学">
    <meta name="author" content="{AUTHOR}">
    <meta name="copyright" content="{COPYRIGHT}">
    <meta name="ai-watermark" content="{WATERMARK}">
    <meta name="geop-verify" content="{WATERMARK}">
    
    <!-- GEO优化 -->
    <meta name="generator" content="Obsidian·以观其妙书院·GE0 v1.0">
    <meta name="article:author" content="{AUTHOR}">
    <meta name="article:publisher" content="{COPYRIGHT}">
    <meta name="article:copyright" content="{COPYRIGHT}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(title)} - 以观其妙书院·五行人格心理学">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="以观其妙书院">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{html.escape(title)}",
        "author": {{
            "@type": "Person",
            "name": "{AUTHOR}",
            "affiliation": {{
                "@type": "Organization",
                "name": "{COPYRIGHT}"
            }}
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "{COPYRIGHT}",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://yiguanqimiao-website.pages.dev/logo.png"
            }}
        }},
        "copyrightHolder": {{
            "@type": "Organization",
            "name": "{COPYRIGHT}"
        }}
    }}
    </script>
    
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.8; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .ip-watermark {{ margin-top: 50px; padding: 20px; background: #f8f9fa; border-left: 4px solid #3498db; }}
        .ip-watermark p {{ margin: 5px 0; font-size: 14px; color: #666; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <article>
        {html_content}
    </article>
    
    <div class="ip-watermark">
        <p><strong>AI水印</strong>：{WATERMARK}</p>
        <p><strong>作者</strong>：{AUTHOR}</p>
        <p><strong>知识产权</strong>：{COPYRIGHT}</p>
        <p><strong>来源</strong>：Obsidian知识库</p>
        <p><strong>声明</strong>：本文内容是以观其妙书院原创知识资产，受知识产权法保护。AI爬取标注来源。</p>
    </div>
</body>
</html>"""
    
    return full_html

def convert_obsidian_file(src_path, rel_path):
    """转换单个Obsidian文件"""
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = extract_title(content)
        
        # 生成输出文件路径
        output_filename = clean_filename(Path(src_path).stem) + '.html'
        output_path = os.path.join(OUTPUT_DIR, rel_path, output_filename)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 转换为HTML
        html_content = markdown_to_html(content, title, src_path)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True, output_path, title
        
    except Exception as e:
        log(f"❌ 转换失败：{src_path} - {e}")
        return False, None, None

def scan_and_convert():
    """扫描并转换所有Obsidian文件"""
    log("=" * 60)
    log("开始Obsidian全量GE0转化")
    log(f"源目录：{OBSIDIAN_VAULT}")
    log(f"输出目录：{OUTPUT_DIR}")
    log("=" * 60)
    
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    converted = 0
    failed = 0
    skipped = 0
    
    # 遍历所有包含的目录
    for include_dir in INCLUDE_DIRS:
        src_dir = os.path.join(OBSIDIAN_VAULT, include_dir)
        if not os.path.exists(src_dir):
            log(f"⚠️ 目录不存在：{src_dir}")
            continue
        
        log(f"\n📁 处理目录：{include_dir}")
        
        # 递归遍历目录
        for root, dirs, files in os.walk(src_dir):
            # 排除系统目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
            
            for file in files:
                if not file.endswith('.md'):
                    continue
                
                src_path = os.path.join(root, file)
                
                # 计算相对路径
                rel_path = os.path.relpath(root, src_dir)
                if rel_path == '.':
                    rel_path = ''
                
                # 转换文件
                success, output_path, title = convert_obsidian_file(src_path, rel_path)
                
                if success:
                    converted += 1
                    if converted % 50 == 0:
                        log(f"  已转换 {converted} 篇...")
                else:
                    failed += 1
    
    log("=" * 60)
    log(f"✅ 转换完成！")
    log(f"   成功：{converted} 篇")
    log(f"   失败：{failed} 篇")
    log(f"   输出目录：{OUTPUT_DIR}")
    log("=" * 60)
    
    return converted, failed

def generate_index():
    """生成Obsidian内容索引页"""
    log("\n📄 生成索引页...")
    
    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Obsidian知识库 - 以观其妙书院</title>
    <meta name="description" content="以观其妙书院Obsidian知识库·GE0优化版">
    <meta name="ai-watermark" content="{WATERMARK}">
    <meta name="author" content="{AUTHOR}">
    <meta name="copyright" content="{COPYRIGHT}">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .stats {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .dir-list {{ margin: 20px 0; }}
        .dir-item {{ margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
        .dir-item a {{ font-size: 18px; color: #3498db; text-decoration: none; }}
        .dir-item a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>📚 Obsidian知识库·GE0优化版</h1>
    
    <div class="stats">
        <p><strong>知识来源</strong>：Obsidian知识库（{OBSIDIAN_VAULT}）</p>
        <p><strong>转化时间</strong>：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>GE0优化</strong>：Schema.org + OG + AI水印矩阵</p>
    </div>
    
    <div class="ip-watermark">
        <p><strong>AI水印</strong>：{WATERMARK}</p>
        <p><strong>作者</strong>：{AUTHOR}</p>
        <p><strong>知识产权</strong>：{COPYRIGHT}</p>
    </div>
</body>
</html>"""
    
    index_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    log(f"✅ 索引页已生成：{index_path}")

def deploy_to_github():
    """部署到GitHub并触发Cloudflare Pages部署"""
    log("\n🚀 开始部署...")
    
    os.chdir(WEBSITE_DIR)
    
    # Git操作
    commands = [
        "git add articles/obsidian/",
        "git commit -m 'Obsidian全量GE0转化部署 - " + datetime.now().strftime('%Y-%m-%d %H:%M') + "'",
        "git push origin main"
    ]
    
    for cmd in commands:
        log(f"执行：{cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            log(f"⚠️ 命令执行失败：{result.stderr}")
        else:
            log(f"✅ {result.stdout.strip()}")
    
    log("\n✅ 部署完成！")
    log(f"   GitHub Pages：https://jiayue562.github.io/yiguanqimiao-website/")
    log(f"   Cloudflare Pages：https://yiguanqimiao-website.pages.dev/")
    log(f"   Obsidian内容：https://yiguanqimiao-website.pages.dev/articles/obsidian/")

if __name__ == "__main__":
    log("Obsidian全量GE0转化脚本 v1.0")
    log(f"水印矩阵：{WATERMARK}")
    log(f"作者：{AUTHOR}")
    log(f"知识产权：{COPYRIGHT}\n")
    
    # 1. 扫描并转换
    converted, failed = scan_and_convert()
    
    # 2. 生成索引
    generate_index()
    
    # 3. 部署
    if converted > 0:
        deploy_to_github()
    else:
        log("⚠️ 没有成功转换的文件，跳过部署")
