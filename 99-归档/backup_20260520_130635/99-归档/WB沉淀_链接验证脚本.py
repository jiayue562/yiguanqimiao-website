# -*- coding: utf-8 -*-
"""
双向链接验证脚本
功能：
1. 扫描所有Markdown文件
2. 提取所有 [[链接]]
3. 验证双向链接完整性
4. 生成验证报告
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

class LinkValidator:
    def __init__(self, base_path):
        self.base_path = base_path
        self.links = defaultdict(set)  # file -> set of linked files
        self.backlinks = defaultdict(set)  # file -> set of files linking to it
        
    def extract_links(self, file_path):
        """提取文件中的所有 [[链接]]"""
        links = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 匹配 [[链接]] 格式
                pattern = r'\[\[([^\]]+)\]\]'
                matches = re.findall(pattern, content)
                for match in matches:
                    # 处理相对路径
                    link = match.strip()
                    links.add(link)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return links
    
    def normalize_link(self, link, current_file):
        """规范化链接，转换为文件路径"""
        # 移除锚点
        if '#' in link:
            link = link.split('#')[0]
        # 如果是相对路径，转换为绝对路径
        if not link.endswith('.md'):
            link = link + '.md'
        return link
    
    def scan_directory(self):
        """扫描目录下的所有Markdown文件"""
        print("=" * 60)
        print("双向链接验证工具")
        print("=" * 60)
        print(f"\n扫描目录: {self.base_path}\n")
        
        md_files = list(Path(self.base_path).rglob("*.md"))
        print(f"找到 {len(md_files)} 个 Markdown 文件\n")
        
        for md_file in md_files:
            rel_path = md_file.relative_to(self.base_path)
            links = self.extract_links(md_file)
            self.links[str(rel_path)] = links
            
            for link in links:
                normalized = self.normalize_link(link, str(rel_path))
                self.backlinks[normalized].add(str(rel_path))
        
        return len(md_files)
    
    def validate_links(self):
        """验证链接完整性"""
        print("\n" + "=" * 60)
        print("链接验证结果")
        print("=" * 60)
        
        issues = []
        orphans = []  # 没有反向链接的文件
        total_links = 0
        bidirectional = 0
        
        for file, links in self.links.items():
            file_total = len(links)
            file_bidirectional = 0
            
            for link in links:
                total_links += 1
                normalized = self.normalize_link(link, file)
                # 检查是否有反向链接
                if file in self.backlinks.get(normalized, set()):
                    file_bidirectional += 1
                else:
                    # 检查目标文件是否存在
                    target_exists = any(
                        str(p).endswith(normalized) or 
                        str(p).replace('.md', '') == normalized.replace('.md', '')
                        for p in Path(self.base_path).rglob("*.md")
                    )
                    if not target_exists:
                        issues.append({
                            'source': file,
                            'target': link,
                            'issue': '目标文件不存在'
                        })
            
            bidirectional += file_bidirectional
            
            # 检查孤立文件（没有反向链接）
            if not self.backlinks.get(file.replace('.md', ''), set()) and not links:
                orphans.append(file)
        
        # 统计
        print(f"\n📊 统计信息:")
        print(f"   总文件数: {len(self.links)}")
        print(f"   总链接数: {total_links}")
        print(f"   双向链接数: {bidirectional}")
        print(f"   链接完整率: {bidirectional/total_links*100:.1f}%" if total_links > 0 else "   N/A")
        print(f"   孤立文件数: {len(orphans)}")
        print(f"   链接问题数: {len(issues)}")
        
        # 报告问题
        if issues:
            print(f"\n⚠️ 链接问题 ({len(issues)} 项):")
            for i, issue in enumerate(issues[:10], 1):
                print(f"   {i}. [{issue['source']}]")
                print(f"      -> {issue['target']}")
                print(f"      问题: {issue['issue']}")
            if len(issues) > 10:
                print(f"   ... 还有 {len(issues) - 10} 项问题")
        
        if orphans:
            print(f"\n📄 孤立文件 ({len(orphans)} 个):")
            for orphan in orphans[:10]:
                print(f"   - {orphan}")
            if len(orphans) > 10:
                print(f"   ... 还有 {len(orphans) - 10} 个孤立文件")
        
        # 生成建议
        print(f"\n💡 优化建议:")
        if orphans:
            print(f"   1. 为孤立文件添加链接，建立知识网络")
        if issues:
            print(f"   2. 修复损坏的链接")
        if bidirectional/total_links < 0.5 if total_links > 0 else False:
            print(f"   3. 增加双向链接密度")
        
        return {
            'total_files': len(self.links),
            'total_links': total_links,
            'bidirectional': bidirectional,
            'orphans': orphans,
            'issues': issues
        }
    
    def generate_report(self, output_path):
        """生成验证报告"""
        report = {
            'timestamp': str(Path().stat().st_mtime),
            'base_path': self.base_path,
            **self.validate_links()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 报告已保存: {output_path}")

def main():
    # 配置路径
    base_path = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\WorkBuddy知识沉淀"
    output_path = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\WorkBuddy知识沉淀\08-WB-验证工具\验证报告.json"
    
    validator = LinkValidator(base_path)
    validator.scan_directory()
    validator.validate_links()
    validator.generate_report(output_path)

if __name__ == "__main__":
    main()
