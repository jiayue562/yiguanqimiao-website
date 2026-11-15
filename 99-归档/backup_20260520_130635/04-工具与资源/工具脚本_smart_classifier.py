#!/usr/bin/env python3
"""
智能文件分类工具
基于文件扩展名、文件名模式、内容关键词进行自动分类
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# 配置
VAULT_PATH = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院"
OUTPUT_FILE = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\00-索引与导航\📈 文件分类统计.md"

class SmartClassifier:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.files = []
        
        # 分类规则
        self.extension_rules = {
            '.md': 'Markdown文档',
            '.py': 'Python脚本',
            '.json': 'JSON配置',
            '.yaml': 'YAML配置',
            '.yml': 'YAML配置',
            '.sh': 'Shell脚本',
            '.ps1': 'PowerShell脚本',
            '.bat': '批处理文件',
            '.txt': '文本文件',
            '.html': 'HTML网页',
            '.css': '样式表',
            '.js': 'JavaScript',
            '.docx': 'Word文档',
            '.xlsx': 'Excel表格',
            '.pptx': 'PPT演示'
        }
        
        self.filename_patterns = {
            r'^SKILL\.md$': '技能定义',
            r'^README\.md$': '说明文档',
            r'^TODO\.md$': '待办事项',
            r'^CHANGELOG.*': '变更日志',
            r'.*skills.*': '技能相关',
            .*模板.*': '模板文件',
            .*index.*': '索引文件',
            .*导航.*': '导航文件',
            .*学习.*': '学习资料',
            .*笔记.*': '笔记文档'
        }
        
        self.content_keywords = {
            '思维模型': ['思维', '模型', '框架', '方法论'],
            '五行': ['五行', '木行人', '火行人', '土行人', '金行人', '水行人'],
            '象思维': ['象思维', '观物取象', '意象', '原象'],
            '五色光': ['五色光', '白光', '红光', '黄光', '绿光', '蓝光'],
            '人机协同': ['人机协同', '四象限', '高效助理', '共创伙伴'],
            'DragonOS': ['Dragon OS', '龙脑操作系统', '五大引擎'],
            '知识学习': ['知识学习', '深度学习', '十项认知'],
            '知行合一': ['知行合一', '表示空间', '压缩', '泛化'],
            '对话记录': ['对话', '问答', '问答记录'],
            '记忆系统': ['记忆', 'SOUL', 'USER', 'TOOLS', 'SESSION'],
            '大圆满': ['大圆满', '明觉', '本自圆满', '本来清净'],
            '地藏经': ['地藏经', '地藏菩萨', '因果'],
            '企业文化': ['企业文化', '使命', '愿景', '价值观'],
            'AI应用': ['AI', '人工智能', '智能体', 'Agent'],
            'Obsidian': ['Obsidian', '双向链接', '知识图谱']
        }
    
    def scan_vault(self):
        """扫描知识库"""
        print(f"📂 扫描知识库: {self.vault_path}")
        
        for file_path in self.vault_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            # 跳过隐藏文件夹
            if any(part.startswith('.') for part in file_path.parts):
                continue
            
            rel_path = str(file_path.relative_to(self.vault_path))
            self.files.append({
                'path': rel_path,
                'name': file_path.name,
                'stem': file_path.stem,
                'suffix': file_path.suffix,
                'size': file_path.stat().st_size,
                'mtime': datetime.fromtimestamp(file_path.stat().st_mtime)
            })
        
        print(f"✅ 扫描完成: {len(self.files)} 个文件")
    
    def classify_by_extension(self):
        """按扩展名分类"""
        result = defaultdict(list)
        
        for f in self.files:
            ext = f['suffix'].lower()
            category = self.extension_rules.get(ext, '其他文件')
            result[category].append(f)
        
        return dict(result)
    
    def classify_by_pattern(self):
        """按文件名模式分类"""
        result = defaultdict(list)
        
        for f in self.files:
            name = f['name']
            
            for pattern, category in self.filename_patterns.items():
                try:
                    if re.search(pattern, name, re.IGNORECASE):
                        result[category].append(f)
                        break
                except re.error:
                    pass
        
        return dict(result)
    
    def classify_by_content(self):
        """按内容关键词分类"""
        result = defaultdict(list)
        
        for f in self.files:
            if f['suffix'] != '.md':
                continue
            
            try:
                file_path = self.vault_path / f['path']
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                for category, keywords in self.content_keywords.items():
                    if any(kw in content for kw in keywords):
                        result[category].append(f)
            except Exception:
                pass
        
        return dict(result)
    
    def analyze(self):
        """综合分析"""
        # 扩展名统计
        ext_stats = Counter(f['suffix'].lower() for f in self.files)
        
        # 目录统计
        dir_stats = Counter(Path(f['path']).parts[0] if f['path'] else '' for f in self.files)
        
        # 文件大小统计
        total_size = sum(f['size'] for f in self.files)
        avg_size = total_size / len(self.files) if self.files else 0
        
        return {
            'extension_stats': dict(ext_stats),
            'directory_stats': dict(dir_stats),
            'total_files': len(self.files),
            'total_size_mb': total_size / (1024 * 1024),
            'average_size_kb': avg_size / 1024
        }
    
    def generate_report(self):
        """生成分类报告"""
        ext_class = self.classify_by_extension()
        pattern_class = self.classify_by_pattern()
        content_class = self.classify_by_content()
        stats = self.analyze()
        
        report = f"""---
title: "📈 文件分类统计报告"
type: report
tags: [统计, 分类, 文件分析]
created: {datetime.now().strftime('%Y-%m-%d')}
version: 1.0
---

# 📈 观其妙书院文件分类统计

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 总体统计

| 指标 | 数值 |
|------|------|
| 总文件数 | {stats['total_files']} |
| 总大小 | {stats['total_size_mb']:.2f} MB |
| 平均大小 | {stats['average_size_kb']:.2f} KB |

---

## 📁 按扩展名分类

| 扩展名 | 文件数 | 占比 |
|--------|--------|------|
"""
        
        for ext, count in sorted(stats['extension_stats'].items(), key=lambda x: -x[1]):
            pct = count / stats['total_files'] * 100
            report += f"| {ext} | {count} | {pct:.1f}% |\n"
        
        report += f"""
---

## 📂 按目录分类

| 目录 | 文件数 |
|------|--------|
"""
        
        for dir_name, count in sorted(stats['directory_stats'].items(), key=lambda x: -x[1])[:20]:
            if dir_name:
                report += f"| {dir_name} | {count} |\n"
        
        # 按内容分类
        report += f"""
---

## 🏷️ 按内容关键词分类

| 关键词类别 | 文件数 |
|------------|--------|
"""
        
        for category, files in sorted(content_class.items(), key=lambda x: -len(x[1])):
            if files:
                report += f"| {category} | {len(files)} |\n"
        
        # 按文件名模式分类
        report += f"""
---

## 🔤 按文件名模式分类

| 模式类型 | 文件数 |
|----------|--------|
"""
        
        for pattern, files in sorted(pattern_class.items(), key=lambda x: -len(x[1])):
            if files:
                report += f"| {pattern} | {len(files)} |\n"
        
        # 分类规则说明
        report += f"""
---

## 📋 分类规则说明

### 扩展名规则
"""
        
        for ext, desc in sorted(self.extension_rules.items()):
            report += f"- `{ext}`: {desc}\n"
        
        report += """
---

## 🔗 关联文档

- [[📚 知识库总索引]]
- [[📊 知识图谱]]
- [[🔗 双向链接规范]]

---

*报告自动生成 | 最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        return report
    
    def save_report(self):
        """保存报告"""
        report = self.generate_report()
        
        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        
        print(f"✅ 报告已保存: {output_path}")

def main():
    classifier = SmartClassifier(VAULT_PATH)
    classifier.scan_vault()
    classifier.save_report()
    
    stats = classifier.analyze()
    print("\n📊 分类结果:")
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总大小: {stats['total_size_mb']:.2f} MB")

if __name__ == "__main__":
    main()
