#!/usr/bin/env python
"""重命名所有.html文件，移除.html后缀（解决Cloudflare Clean URL的308重定向问题）
并在docs/_headers中设置正确的Content-Type"""
import os
from pathlib import Path

DOCS_DIR = Path("C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/docs")

def main():
    # 1. 删除旧的_redirects和_headers（如果有的话）
    for f in ['_redirects', '_headers']:
        path = DOCS_DIR / f
        if path.exists():
            path.unlink()
            print(f"✅ 删除 {f}")
    
    # 2. 创建_headers，为所有无扩展名的HTML文件设置Content-Type
    headers_content = """# Cloudflare Pages Headers
# 为articles/目录下的所有文件设置正确的Content-Type
/articles/*
  Content-Type: text/html
  X-Content-Type-Options: nosniff
"""
    with open(DOCS_DIR / '_headers', 'w', encoding='utf-8') as f:
        f.write(headers_content)
    print("✅ 创建 _headers (Content-Type: text/html)")
    
    # 3. 遍历所有.html文件，重命名为无.html后缀
    renamed_count = 0
    skip_count = 0
    error_count = 0
    
    for html_path in DOCS_DIR.rglob('*.html'):
        # 跳过index.html文件（保留为.html，因为是目录入口）
        if html_path.name == 'index.html':
            skip_count += 1
            continue
        
        # 新路径：移除.html后缀
        new_path = html_path.with_suffix('')
        
        # 检查新路径是否已存在（冲突）
        if new_path.exists():
            skip_count += 1
            print(f"⚠️ 跳过（已存在）: {html_path.name}")
            continue
        
        try:
            html_path.rename(new_path)
            renamed_count += 1
        except Exception as e:
            error_count += 1
            print(f"❌ 重命名失败: {html_path.name} - {e}")
    
    print(f"\n{'='*50}")
    print(f"重命名结果:")
    print(f"  ✅ 重命名: {renamed_count} 个文件")
    print(f"  ⏭️  跳过: {skip_count} 个文件 (index.html)")
    print(f"  ❌ 错误: {error_count} 个文件")
    print(f"📝 _headers 已创建 (Content-Type: text/html)")

if __name__ == '__main__':
    main()
