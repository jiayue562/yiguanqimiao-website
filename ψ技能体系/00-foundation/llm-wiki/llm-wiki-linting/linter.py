#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM Wiki Linting 引擎
自动检测知识库质量问题

版本：v1.0
创建：2026-04-17
"""

import sys
import io

# Windows 编码兼容性
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """问题严重度"""
    HIGH = "🔴 高"
    MEDIUM = "🟡 中"
    LOW = "🟢 低"


@dataclass
class LintIssue:
    """Linting 问题"""
    file: str
    line: Optional[int]
    severity: Severity
    category: str
    message: str
    suggestion: str
    auto_fixable: bool = False


class WikiLinter:
    """Wiki Linting 引擎"""
    
    def __init__(self, wiki_dir: str):
        """
        初始化 Linter
        
        Args:
            wiki_dir: Wiki 知识库目录
        """
        self.wiki_dir = Path(wiki_dir)
        self.issues: List[LintIssue] = []
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'files_with_issues': 0
        }
        
    def scan(self, file_pattern: str = "*.md") -> int:
        """
        扫描知识库文件
        
        Args:
            file_pattern: 文件匹配模式
            
        Returns:
            扫描的文件数量
        """
        print(f"🔍 扫描知识库：{self.wiki_dir}")
        
        files = list(self.wiki_dir.rglob(file_pattern))
        self.stats['total_files'] = len(files)
        
        for file_path in files:
            # 跳过缓存和临时文件
            if file_path.name.startswith('.') or 'node_modules' in str(file_path):
                continue
                
            self._scan_file(file_path)
            self.stats['total_size'] += file_path.stat().st_size
            
        print(f"✅ 扫描完成：{len(files)} 个文件，发现 {len(self.issues)} 个问题")
        return len(files)
        
    def _scan_file(self, file_path: Path):
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # 执行所有检查
            self._check_empty_content(file_path, content)
            self._check_format_errors(file_path, content, lines)
            self._check_freshness(file_path)
            self._check_broken_links(file_path, content)
            self._check_structure(file_path, content)
            
        except Exception as e:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.HIGH,
                category="读取错误",
                message=f"无法读取文件：{e}",
                suggestion="检查文件编码和权限",
                auto_fixable=False
            ))
            
    def _check_empty_content(self, file_path: Path, content: str):
        """检查空内容"""
        if len(content.strip()) < 50:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.HIGH,
                category="内容质量",
                message="文件内容为空或过短",
                suggestion="添加内容或删除文件",
                auto_fixable=False
            ))
            
    def _check_format_errors(self, file_path: Path, content: str, lines: List[str]):
        """检查格式错误"""
        # 检查未闭合的代码块
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.MEDIUM,
                category="格式错误",
                message="未闭合的代码块（``` 数量为奇数）",
                suggestion="检查代码块是否正确闭合",
                auto_fixable=False
            ))
            
        # 检查过长的行
        for i, line in enumerate(lines, 1):
            if len(line) > 200 and not line.startswith('```'):
                self.issues.append(LintIssue(
                    file=str(file_path),
                    line=i,
                    severity=Severity.LOW,
                    category="格式错误",
                    message=f"行过长（{len(line)} 字符）",
                    suggestion="考虑换行或格式化",
                    auto_fixable=False
                ))
                
    def _check_freshness(self, file_path: Path):
        """检查时效性"""
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        days_old = (datetime.now() - mtime).days
        
        if days_old > 90:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.MEDIUM,
                category="时效性",
                message=f"文件超过 {days_old} 天未更新",
                suggestion="检查内容是否过时，考虑更新或标记",
                auto_fixable=False
            ))
            
    def _check_broken_links(self, file_path: Path, content: str):
        """检查失效链接"""
        # 提取所有 markdown 链接
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # 检查内部链接
            if not link_url.startswith(('http://', 'https://', 'mailto:')):
                # 内部链接检查
                linked_file = self.wiki_dir / link_url.split('#')[0]
                if not linked_file.exists():
                    self.issues.append(LintIssue(
                        file=str(file_path),
                        line=None,
                        severity=Severity.HIGH,
                        category="一致性",
                        message=f"内部链接失效：{link_url}",
                        suggestion=f"检查文件是否存在：{linked_file}",
                        auto_fixable=False
                    ))
                    
    def _check_structure(self, file_path: Path, content: str):
        """检查结构完整性"""
        lines = content.split('\n')
        
        # 检查是否有标题
        has_title = any(line.startswith('#') for line in lines[:10])
        if not has_title:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.LOW,
                category="完整性",
                message="文件缺少标题",
                suggestion="在文件开头添加标题（# 标题）",
                auto_fixable=False
            ))
            
        # 检查是否有内容（至少 3 行）
        if len([l for l in lines if l.strip()]) < 3:
            self.issues.append(LintIssue(
                file=str(file_path),
                line=None,
                severity=Severity.LOW,
                category="完整性",
                message="文件内容过少（少于 3 行）",
                suggestion="添加更多内容或考虑删除",
                auto_fixable=False
            ))
            
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """
        生成 Linting 报告
        
        Args:
            output_file: 输出文件路径（可选）
            
        Returns:
            报告内容
        """
        # 统计
        high_count = sum(1 for i in self.issues if i.severity == Severity.HIGH)
        medium_count = sum(1 for i in self.issues if i.severity == Severity.MEDIUM)
        low_count = sum(1 for i in self.issues if i.severity == Severity.LOW)
        
        # 计算评分
        score = max(0, 100 - (high_count * 10) - (medium_count * 5) - (low_count * 2))
        grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
        
        # 生成报告
        report = f"""# LLM Wiki Linting 报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**扫描范围**: {self.wiki_dir}  
**文件总数**: {self.stats['total_files']}  
**总大小**: {self.stats['total_size'] / 1024:.1f} KB  
**问题总数**: {len(self.issues)}  

## 质量评分：{grade} ({score}/100)

| 严重度 | 数量 | 扣分 |
|--------|------|------|
| 🔴 高 | {high_count} | -{high_count * 10} |
| 🟡 中 | {medium_count} | -{medium_count * 5} |
| 🟢 低 | {low_count} | -{low_count * 2} |

---

## 🔴 高严重度问题 ({high_count})

"""
        
        # 添加高严重度问题
        high_issues = [i for i in self.issues if i.severity == Severity.HIGH]
        for i, issue in enumerate(high_issues[:10], 1):  # 最多显示 10 个
            report += f"""### {i}. {issue.category}

- **文件**: `{issue.file}`
- **问题**: {issue.message}
- **建议**: {issue.suggestion}
- **自动修复**: {"✅ 可用" if issue.auto_fixable else "❌ 需人工"}

"""
            
        if high_count > 10:
            report += f"\n... 还有 {high_count - 10} 个高严重度问题\n"
            
        # 添加中严重度问题（摘要）
        if medium_count > 0:
            report += f"\n## 🟡 中严重度问题 ({medium_count})\n\n"
            for i, issue in enumerate(high_issues[:5], 1):
                report += f"- {issue.file}: {issue.message}\n"
                
        # 添加低严重度问题（摘要）
        if low_count > 0:
            report += f"\n## 🟢 低严重度问题 ({low_count})\n\n"
            for i, issue in enumerate(high_issues[:5], 1):
                report += f"- {issue.file}: {issue.message}\n"
                
        # 修复建议
        report += f"""
---

## 修复建议

### 立即修复（{high_count} 个）
{chr(10).join(f'- {i.file}: {i.message}' for i in high_issues[:5])}

### 本周修复（{medium_count} 个）
建议本周内完成中严重度问题修复

### 后续优化（{low_count} 个）
可在空闲时优化低严重度问题

---

_LLM Wiki Linting 报告 · {datetime.now().strftime('%Y-%m-%d')} · 龙心 OS_
"""
        
        # 输出报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 报告已保存：{output_file}")
            
        return report


def main():
    """主函数 - 测试 Linting"""
    # 配置
    wiki_dirs = [
        Path.home() / ".OpcClaw 知识库",
        Path.home() / ".openclaw" / "workspace",
    ]
    
    for wiki_dir in wiki_dirs:
        if wiki_dir.exists():
            print(f"\n{'='*60}")
            print(f"检查：{wiki_dir}")
            print('='*60)
            
            linter = WikiLinter(str(wiki_dir))
            linter.scan()
            
            # 生成报告
            report_file = wiki_dir.parent / f"lint-report-{datetime.now().strftime('%Y-%m-%d')}.md"
            linter.generate_report(str(report_file))


if __name__ == "__main__":
    main()
