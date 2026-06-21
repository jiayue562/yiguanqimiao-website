#!/usr/bin/env python
"""为所有.html文件创建"无扩展名"副本（解决Cloudflare Clean URL 308问题）
并在docs/_headers中设置正确的Content-Type"""
import os
from pathlib import Path

DOCS_DIR = Path("C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/docs")

def main():
    # 1. 创建_headers文件，设置Content-Type
    headers_content = """# Cloudflare Pages Headers
# 为所有无扩展名的HTML文件设置正确的Content-Type
/articles/*
  Content-Type: text/html
  X-Content-Type-Options: nosniff
"""
    with open(DOCS_DIR / '_headers', 'w', encoding='utf-8') as f:
        f.write(headers_content)
    print("✅ 创建 _headers (Content-Type: text/html)")
    
    # 2. 遍历所有.html文件，为每个文件创建"无扩展名"的副本
    created_count = 0
    skip_count = 0
    error_count = 0
    
    for html_path in DOCS_DIR.rglob('*.html'):
        # 跳过index.html（目录入口，不需要创建副本）
        if html_path.name == 'index.html':
            skip_count += 1
            continue
        
        # 副本路径：移除.html后缀
        copy_path = html_path.with_suffix('')
        
        # 如果副本已存在，跳过
        if copy_path.exists():
            skip_count += 1
            continue
        
        try:
            # 读取原文件内容并写入副本
            content = html_path.read_bytes()
            copy_path.write_bytes(content)
            created_count += 1
            
            # 每100个文件报告一次进度
            if created_count % 200 == 0:
                print(f"  ... 已创建 {created_count} 个副本")
        except Exception as e:
            error_count += 1
            print(f"❌ 错误: {html_path.name} - {e}")
    
    print(f"\n{'='*50}")
    print(f"✅ 完成!")
    print(f"  📋 创建副本: {created_count} 个文件")
    print(f"  ⏭️  跳过: {skip_count} 个文件 (index.html)")
    print(f"  ❌ 错误: {error_count} 个文件")
    print(f"📝 _headers 已创建 (Content-Type: text/html)")

if __name__ == '__main__':
    main()
