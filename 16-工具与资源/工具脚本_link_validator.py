#!/usr/bin/env python3
"""
知识库链接验证工具
验证 Obsidian 知识库中双向链接的完整性和正确性
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# 配置
VAULT_PATH = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院"
OUTPUT_PATH = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\00-索引与导航\🔍 链接验证报告.md"

class LinkValidator:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.links = defaultdict(set)  # 文件 -> 链接到的文件
        self.backlinks = defaultdict(set)  # 文件 -> 链接到的文件（反向）
        self.files = set()  # 所有 md 文件
        self.broken_links = []  # 破损链接
        self.orphaned_files = []  # 孤立文件
        
    def scan_vault(self):
        """扫描整个知识库"""
        print(f"📂 扫描知识库: {self.vault_path}")
        
        for md_file in self.vault_path.rglob("*.md"):
            # 跳过隐藏文件夹
            if any(part.startswith('.') for part in md_file.parts):
                continue
                
            rel_path = md_file.relative_to(self.vault_path)
            self.files.add(str(rel_path))
            self._parse_file(md_file, rel_path)
        
        print(f"✅ 扫描完成: {len(self.files)} 个文件")
    
    def _parse_file(self, file_path, rel_path):
        """解析单个文件中的链接"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 匹配 [[链接]] 格式
            wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            
            for link in wiki_links:
                # 移除锚点
                link = link.split('#')[0]
                if not link:
                    continue
                    
                # 尝试匹配文件
                matched = self._resolve_link(link, rel_path)
                
                if matched:
                    self.links[str(rel_path)].add(matched)
                    self.backlinks[matched].add(str(rel_path))
                else:
                    self.broken_links.append({
                        'source': str(rel_path),
                        'target': link,
                        'type': 'wiki'
                    })
                    
        except Exception as e:
            print(f"⚠️ 解析错误 {file_path}: {e}")
    
    def _resolve_link(self, link, source_file):
        """解析链接到实际文件"""
        # 尝试不同扩展名
        candidates = [
            f"{link}.md",
            f"{link}/index.md",
            link
        ]
        
        for candidate in candidates:
            if candidate in self.files:
                return candidate
            
            # 尝试在同目录
            source_dir = Path(source_file).parent
            full_path = source_dir / candidate
            rel_path = str(full_path.relative_to(self.vault_path))
            if rel_path in self.files:
                return rel_path
        
        return None
    
    def analyze(self):
        """分析链接关系"""
        # 找出孤立文件（没有任何链接）
        for f in self.files:
            if not self.links.get(f) and not self.backlinks.get(f):
                self.orphaned_files.append(f)
        
        # 计算统计数据
        total_links = sum(len(v) for v in self.links.values())
        bidirectional = 0
        
        for source, targets in self.links.items():
            for target in targets:
                if source in self.backlinks.get(target, set()):
                    bidirectional += 1
        
        return {
            'total_files': len(self.files),
            'total_links': total_links,
            'broken_links': len(self.broken_links),
            'orphaned_files': len(self.orphaned_files),
            'bidirectional_links': bidirectional,
            'bidirectional_rate': bidirectional / total_links if total_links > 0 else 0
        }
    
    def generate_report(self):
        """生成验证报告"""
        stats = self.analyze()
        
        report = f"""---
title: "🔍 链接验证报告"
type: report
tags: [链接, 验证, 报告]
created: {datetime.now().strftime('%Y-%m-%d')}
version: 1.0
---

# 🔍 知识库链接验证报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 统计概览

| 指标 | 数值 | 状态 |
|------|------|------|
| 总文件数 | {stats['total_files']} | {'✅' if stats['total_files'] > 0 else '❌'} |
| 总链接数 | {stats['total_links']} | {'✅' if stats['total_links'] > 0 else '❌'} |
| 双向链接数 | {stats['bidirectional_links']} | {'✅' if stats['bidirectional_rate'] > 0.5 else '⚠️'} |
| 双向链接率 | {stats['bidirectional_rate']:.1%} | {'✅' if stats['bidirectional_rate'] > 0.5 else '⚠️'} |
| 破损链接 | {stats['broken_links']} | {'✅' if stats['broken_links'] == 0 else '❌'} |
| 孤立文件 | {stats['orphaned_files']} | {'✅' if stats['orphaned_files'] == 0 else '⚠️'} |

---

## 🔧 详细分析

### 链接密度

"""
        
        # 计算各文件的链接数
        file_link_counts = []
        for f in self.files:
            out_links = len(self.links.get(f, set()))
            in_links = len(self.backlinks.get(f, set()))
            file_link_counts.append((f, out_links, in_links))
        
        # 按总链接数排序
        file_link_counts.sort(key=lambda x: x[1] + x[2], reverse=True)
        
        report += "#### 链接最多的文件 (Top 10)\n\n"
        report += "| 文件 | 出链 | 入链 | 总计 |\n"
        report += "|------|------|------|------|\n"
        
        for f, out_links, in_links in file_link_counts[:10]:
            report += f"| {f} | {out_links} | {in_links} | {out_links + in_links} |\n"
        
        # 破损链接详情
        if stats['broken_links'] > 0:
            report += f"\n## ⚠️ 破损链接\n\n"
            report += f"发现 {stats['broken_links']} 个破损链接:\n\n"
            
            for link in self.broken_links[:20]:
                report += f"- [[{link['target']}]] (来自 {link['source']})\n"
            
            if len(self.broken_links) > 20:
                report += f"\n... 还有 {len(self.broken_links) - 20} 个\n"
        
        # 孤立文件
        if stats['orphaned_files'] > 0:
            report += f"\n## ⚠️ 孤立文件\n\n"
            report += f"发现 {stats['orphaned_files']} 个孤立文件（没有任何链接）:\n\n"
            
            for f in self.orphaned_files[:20]:
                report += f"- {f}\n"
            
            if len(self.orphaned_files) > 20:
                report += f"\n... 还有 {len(self.orphaned_files) - 20} 个\n"
        
        # 修复建议
        report += f"\n## 💡 修复建议\n\n"
        
        if stats['bidirectional_rate'] < 0.5:
            report += "- 提高双向链接比例，建议核心文档相互链接\n"
        
        if stats['broken_links'] > 0:
            report += "- 修复破损链接，删除或修正无效链接\n"
        
        if stats['orphaned_files'] > 0:
            report += f"- 为 {stats['orphaned_files']} 个孤立文件添加链接\n"
        
        report += """
---

## 🔗 关联文档

- [[📚 知识库总索引]]
- [[📋 文档标准化模板]]
- [[🔗 双向链接规范]]

---

*报告自动生成 | 最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        return report
    
    def save_report(self):
        """保存报告"""
        report = self.generate_report()
        
        output_path = Path(OUTPUT_PATH)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        
        print(f"✅ 报告已保存: {output_path}")

def main():
    validator = LinkValidator(VAULT_PATH)
    validator.scan_vault()
    validator.save_report()
    
    stats = validator.analyze()
    print("\n📊 验证结果:")
    print(f"  文件总数: {stats['total_files']}")
    print(f"  链接总数: {stats['total_links']}")
    print(f"  双向链接率: {stats['bidirectional_rate']:.1%}")
    print(f"  破损链接: {stats['broken_links']}")
    print(f"  孤立文件: {stats['orphaned_files']}")

if __name__ == "__main__":
    main()
