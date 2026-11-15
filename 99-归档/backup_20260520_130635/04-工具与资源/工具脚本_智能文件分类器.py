#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【智能文件分类器】smart-classifier.py
功能：基于文件名和内容自动分类知识库文件
版本：v1.0 | 创建：2026-04-03 | 龙龟神将

使用方法：
    python smart-classifier.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from datetime import datetime

# ============================================
# 配置区
# ============================================

VAULT_ROOT = Path(r"D:\以观其妙书院知识库\观其妙书院")

# 分类规则
CLASSIFICATION_RULES = {
    "Skills文档": {
        "patterns": [r"Skills\.md$", r"skill", r"skill\.md"],
        "category": "01-核心独创Skills",
        "emoji": "🧠"
    },
    "对话记录": {
        "patterns": [r"对话记录", r"chat", r"dialogue", r"聊天"],
        "category": "07-学习档案/对话记录",
        "emoji": "💬"
    },
    "方法论": {
        "patterns": [r"方法论", r"method", r"principle", r"模型"],
        "category": "02-方法论库",
        "emoji": "📜"
    },
    "五行人格": {
        "patterns": [r"五行", r"木行", r"火行", r"土行", r"金行", r"水行"],
        "category": "04-专业领域/五行人格心理学",
        "emoji": "🔮"
    },
    "心文化": {
        "patterns": [r"心文化", r"大圆满", r"修行", r"佛法"],
        "category": "05-修行文化/心文化体系",
        "emoji": "🙏"
    },
    "企业咨询": {
        "patterns": [r"企业", r"管理", r"文化", r"咨询"],
        "category": "04-专业领域/企业文化体系",
        "emoji": "🏢"
    },
    "知识图谱": {
        "patterns": [r"知识图谱", r"图谱", r"graph", r"可视"],
        "category": "00-索引与导航/知识图谱",
        "emoji": "📊"
    },
    "索引文件": {
        "patterns": [r"索引", r"index", r"导航", r"总览"],
        "category": "00-索引与导航",
        "emoji": "📚"
    },
    "学习笔记": {
        "patterns": [r"学习", r"笔记", r"note", r"笔记"],
        "category": "03-学习笔记",
        "emoji": "📝"
    },
    "脚本工具": {
        "patterns": [r"\.py$", r"\.ps1$", r"\.sh$", r"脚本", r"tool"],
        "category": "08-工具与脚本",
        "emoji": "⚙️"
    },
    "模板文件": {
        "patterns": [r"模板", r"template", r"template\.md"],
        "category": "00-索引与导航",
        "emoji": "📋"
    },
    "关系与共生": {
        "patterns": [r"共生", r"关系", r"relationship", r"木火"],
        "category": "03-关系与共生",
        "emoji": "💚"
    },
}

# 特殊文件映射
SPECIAL_FILES = {
    "Dragon OS": "01-核心独创Skills",
    "龙心OS": "01-核心独创Skills",
    "象思维": "01-核心独创Skills",
    "五色光": "01-核心独创Skills",
    "人机协同": "01-核心独创Skills",
    "知行合一": "01-核心独创Skills",
    "知识学习": "01-核心独创Skills",
    "木火共生": "03-关系与共生",
}


class SmartClassifier:
    """智能文件分类器"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.classification_results: Dict[str, List[Tuple[Path, str]]] = defaultdict(list)
        self.unclassified: List[Path] = []
        self.mismatched: List[Tuple[Path, str]] = []

    def classify_file(self, file_path: Path) -> str:
        """分类单个文件"""
        filename = file_path.stem  # 无扩展名
        full_path = str(file_path)
        current_dir = file_path.parent.name

        # 1. 检查特殊文件映射
        for keyword, category in SPECIAL_FILES.items():
            if keyword in filename or keyword in full_path:
                return category

        # 2. 检查文件名模式
        for category_name, rule in CLASSIFICATION_RULES.items():
            for pattern in rule["patterns"]:
                if re.search(pattern, filename, re.IGNORECASE):
                    # 检查是否已在正确目录
                    if current_dir in rule["category"]:
                        return rule["category"]
                    else:
                        return rule["category"]

        # 3. 检查当前目录
        if "Skills" in current_dir:
            return "01-核心独创Skills"
        elif "对话" in current_dir or "归档" in current_dir:
            return "07-学习档案/对话记录"
        elif "方法" in current_dir or "思维" in current_dir:
            return "02-方法论库"
        elif "五行" in current_dir or "人格" in current_dir:
            return "04-专业领域/五行人格心理学"
        elif "修行" in current_dir or "文化" in current_dir or "心文化" in current_dir:
            return "05-修行文化"
        elif "企业" in current_dir or "管理" in current_dir:
            return "04-专业领域/企业文化体系"
        elif "索引" in current_dir or "导航" in current_dir or "00" in current_dir:
            return "00-索引与导航"
        elif "工具" in current_dir or "脚本" in current_dir or "08" in current_dir:
            return "08-工具与脚本"
        elif "关系" in current_dir or "共生" in current_dir or "03" in current_dir:
            return "03-关系与共生"
        elif "项目" in current_dir or "课程" in current_dir or "06" in current_dir:
            return "06-项目管理"
        elif "学习" in current_dir or "07" in current_dir:
            return "07-学习档案"

        # 4. 无法分类
        return None

    def scan_and_classify(self):
        """扫描并分类所有文件"""
        print("📂 扫描知识库...")
        md_files = list(self.vault_root.rglob("*.md"))
        py_files = list(self.vault_root.rglob("*.py"))

        all_files = md_files + py_files

        for file_path in all_files:
            # 跳过排除目录
            if any(excluded in file_path.parts for excluded in [".obsidian", "node_modules", ".git"]):
                continue

            category = self.classify_file(file_path)
            if category:
                self.classification_results[category].append((file_path, ""))
            else:
                self.unclassified.append(file_path)

        return len(all_files)

    def generate_report(self) -> str:
        """生成分类报告"""
        report = []
        report.append("=" * 60)
        report.append("📊 智能文件分类报告")
        report.append("=" * 60)
        report.append(f"知识库: {self.vault_root}")
        report.append(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # 统计
        total_classified = sum(len(files) for files in self.classification_results.values())
        total_unclassified = len(self.unclassified)

        report.append(f"📈 统计:")
        report.append(f"   已分类: {total_classified} 个文件")
        report.append(f"   未分类: {total_unclassified} 个文件")
        report.append("")

        # 各类别详情
        report.append("📁 分类详情:")
        for category, files in sorted(self.classification_results.items()):
            emoji = "📂"
            for cat_name, rule in CLASSIFICATION_RULES.items():
                if rule["category"] == category:
                    emoji = rule["emoji"]
                    break
            report.append(f"\n   {emoji} {category} ({len(files)} 个文件):")

            # 显示前5个文件
            for file_path, _ in files[:5]:
                rel_path = file_path.relative_to(self.vault_root)
                report.append(f"      - {rel_path}")
            if len(files) > 5:
                report.append(f"      ... 还有 {len(files) - 5} 个文件")

        # 未分类文件
        if self.unclassified:
            report.append("\n❓ 未分类文件:")
            for file_path in self.unclassified[:10]:
                rel_path = file_path.relative_to(self.vault_root)
                report.append(f"   - {rel_path}")
            if len(self.unclassified) > 10:
                report.append(f"   ... 还有 {len(self.unclassified) - 10} 个文件")

        report.append("")
        report.append("=" * 60)
        report.append("分类完成")
        report.append("=" * 60)

        return "\n".join(report)

    def generate_move_recommendations(self) -> Dict[str, List[str]]:
        """生成移动建议"""
        recommendations = defaultdict(list)

        for file_path in self.unclassified:
            category = self.classify_file(file_path)
            if category:
                rel_path = str(file_path.relative_to(self.vault_root))
                recommendations[category].append(rel_path)

        return recommendations


def main():
    """主函数"""
    print("=" * 60)
    print("🧠 观其妙书院知识库 · 智能文件分类器")
    print("=" * 60)
    print()

    if not VAULT_ROOT.exists():
        print(f"❌ 错误：路径不存在 {VAULT_ROOT}")
        return

    classifier = SmartClassifier(VAULT_ROOT)

    total_files = classifier.scan_and_classify()
    report = classifier.generate_report()
    print(report)

    # 保存报告
    report_file = VAULT_ROOT / "08-工具与脚本" / "文件分类报告.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(report, encoding="utf-8")
    print(f"\n📄 报告已保存: {report_file}")

    # 生成移动建议
    recommendations = classifier.generate_move_recommendations()
    if recommendations:
        print("\n📋 移动建议:")
        for category, files in recommendations.items():
            print(f"   → {category}: {len(files)} 个文件待移动")


if __name__ == "__main__":
    main()
