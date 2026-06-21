#!/usr/bin/env python
"""将docs/下所有中文名的.html文件重命名为英文名（解决Cloudflare无法处理中文文件名的问题）
保留index.html不变。"""
import os
import re
import hashlib
from pathlib import Path
import html

DOCS_DIR = Path("C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/docs")

def has_chinese(text):
    """检查字符串是否包含中文字符"""
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f':
            return True
    return False

def make_slug(text, max_len=60):
    """将中文名转换为ASCII安全的名字（用拼音或简单命名规则）"""
    # 移除.html后缀
    name = text
    if name.endswith('.html'):
        name = name[:-5]
    
    # 使用MD5哈希前8位作为唯一标识符
    hash_part = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    
    # 提取英文单词部分（如果有）
    ascii_parts = []
    chinese_parts = []
    current = ""
    for ch in name:
        if ord(ch) < 128:
            current += ch
        else:
            if current:
                ascii_parts.append(current)
                current = ""
            chinese_parts.append(ch)
    if current:
        ascii_parts.append(current)
    
    # 组合：取英文前30字符 + 哈希
    ascii_prefix = ""
    if ascii_parts:
        combined = "".join(ascii_parts)
        # 清理特殊字符
        combined = re.sub(r'[^a-zA-Z0-9_-]', '_', combined)
        if len(combined) > 40:
            combined = combined[:40]
        ascii_prefix = combined + "-"
    
    slug = f"{ascii_prefix}{hash_part}"
    return slug.strip('-')

def get_new_name(filepath):
    """获取新文件名"""
    name = filepath.stem  # 不含扩展名
    ext = filepath.suffix  # .html或空
    
    if not has_chinese(name):
        return None  # 不需要重命名
    
    # 获取父目录中所有文件
    parent = filepath.parent
    
    # 生成新文件名
    new_name = make_slug(str(filepath.relative_to(DOCS_DIR)))
    
    # 检查同目录下是否有同名文件（排除原文件）
    # 先尝试直接使用生成的slug
    new_file = parent / f"{new_name}{ext}"
    
    # 如果存在，追加数字后缀
    counter = 1
    while new_file.exists() and new_file.name != filepath.name:
        new_file = parent / f"{new_name}_{counter}{ext}"
        counter += 1
    
    return new_file

def main():
    print(f"{'='*60}")
    print(f"扫描docs/下所有需要重命名的中文名文件...")
    print(f"{'='*60}")
    
    rename_map = {}  # old -> new
    total_files = 0
    chinese_files = 0
    
    # 第一遍：收集所有需要重命名的文件
    for html_path in DOCS_DIR.rglob('*.html'):
        if html_path.name == 'index.html':
            continue
        
        total_files += 1
        if has_chinese(html_path.stem):
            chinese_files += 1
            new_path = get_new_name(html_path)
            if new_path:
                rename_map[html_path] = new_path
    
    print(f"总HTML文件: {total_files}")
    print(f"含中文文件: {chinese_files}")
    print(f"需要重命名: {len(rename_map)}")
    print()
    
    if not rename_map:
        print("✅ 没有需要重命名的文件")
        return
    
    # 第二遍：执行重命名（先重命名.html文件）
    print("正在重命名.html文件...")
    renamed_html = 0
    for old_path, new_path in sorted(rename_map.items(), key=lambda x: str(x[0])):
        try:
            old_path.rename(new_path)
            renamed_html += 1
        except Exception as e:
            print(f"  ❌ {old_path.stem} -> {new_path.stem}: {e}")
    
    print(f"  ✅ 重命名.html文件: {renamed_html} 个")
    print()
    
    # 第三遍：处理无扩展名的副本（如果有同名的）
    print("正在重命名无扩展名副本...")
    renamed_copy = 0
    for old_html, new_html in rename_map.items():
        old_copy = old_html.with_suffix('')  # 无.html
        new_copy = new_html.with_suffix('')  # 无.html
        
        if not old_copy.exists():
            continue
        
        try:
            old_copy.rename(new_copy)
            renamed_copy += 1
        except Exception as e:
            print(f"  ❌ {old_copy.stem} -> {new_copy.stem}: {e}")
    
    print(f"  ✅ 重命名副本: {renamed_copy} 个")
    print()
    
    # 第四遍：重新生成索引页面
    print("正在重新生成索引页面...")
    from generate_indexes import main as gen_indexes
    gen_indexes()
    
    print(f"\n{'='*60}")
    print(f"🎉 完成！")
    print(f"  重命名.html文件: {renamed_html}")
    print(f"  重命名副本: {renamed_copy}")
    print(f"  索引页面已重新生成")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
