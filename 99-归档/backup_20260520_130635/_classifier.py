# -*- coding: utf-8 -*-
"""
智能文件分类器
功能:
  - 按扩展名分类
  - 按文件名模式分类
  - 按内容关键词分类
  - 生成分类报告
"""
import os, re, json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\以观其妙书院知识库\以观其妙书院")

# 分类规则
EXT_RULES = {
    ".md": "文档",
    ".py": "Python 脚本",
    ".json": "JSON 数据",
    ".yaml": "YAML 配置",
    ".yml": "YAML 配置",
    ".css": "CSS 样式",
    ".js": "JavaScript",
    ".html": "HTML",
    ".ps1": "PowerShell 脚本",
    ".bat": "批处理",
    ".txt": "文本",
    ".docx": "Word 文档",
    ".toml": "TOML 配置",
    ".gitignore": "Git 配置",
}

NAME_RULES = [
    (r"^SKILL\.md$", "Skill 定义"),
    (r"^README\.md$", "说明文档"),
    (r"^_index\.md$", "索引文件"),
    (r"^_graph\.md$", "图谱数据"),
    (r"^_tags\.md$", "标签索引"),
    (r"^CONVENTIONS\.md$", "规范文件"),
    (r"^AGENT.*\.md$", "智能体配置"),
    (r"^.*总索引.*\.md$", "总索引"),
    (r"^.*知识图谱.*\.md$", "知识图谱"),
    (r"^.*模板.*\.md$", "模板文件"),
    (r"^journal_.*", "日志记录"),
    (r"^reports_.*", "报告文件"),
    (r"^WorkBuddySync_.*", "同步镜像"),
    (r"^龙心OS_.*", "龙心 OS"),
    (r"^agents_.*", "智能体"),
]

CONTENT_RULES = [
    ("象思维", "象思维"),
    ("五行", "五行体系"),
    ("知行合一", "知行合一"),
    ("双向链接", "链接规范"),
    ("人机协同", "人机协同"),
    ("五色光", "五色光思维"),
    ("LLMification", "LLM Wiki"),
    ("知识编译", "知识编译"),
    ("记忆系统", "记忆系统"),
    ("龙心OS", "龙心OS"),
    ("WorkBuddy", "WorkBuddy"),
    ("对话归档", "对话记录"),
    ("备份", "备份"),
    ("复盘", "复盘"),
]

def classify_by_ext(path):
    return EXT_RULES.get(path.suffix.lower(), "其他")

def classify_by_name(path):
    name = path.name
    for pattern, label in NAME_RULES:
        if re.match(pattern, name):
            return label
    return None

def classify_by_content(path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        matches = []
        for keyword, label in CONTENT_RULES:
            if keyword in content:
                matches.append(label)
        return matches[:3] if matches else None
    except:
        return None

def scan():
    """执行分类扫描"""
    print(f"\n{'='*60}")
    print("  智能文件分类扫描")
    print(f"{'='*60}\n")

    by_ext = defaultdict(int)
    by_name = defaultdict(int)
    by_content = defaultdict(int)
    total = 0

    for p in VAULT.rglob("*"):
        if ".trash" in p.parts or ".git" in p.parts:
            continue
        if not p.is_file():
            continue

        total += 1
        ext = classify_by_ext(p)
        by_ext[ext] += 1

        name_class = classify_by_name(p)
        if name_class:
            by_name[name_class] += 1

        content_classes = classify_by_content(p)
        if content_classes:
            for c in content_classes:
                by_content[c] += 1

    # 输出报告
    print(f"总文件数: {total}\n")

    print("1. 按扩展名分类:")
    print("-" * 40)
    for cat, count in sorted(by_ext.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print(f"\n2. 按文件名模式分类:")
    print("-" * 40)
    for cat, count in sorted(by_name.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    print(f"\n3. 按内容关键词分类:")
    print("-" * 40)
    for cat, count in sorted(by_content.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "by_ext": dict(by_ext),
        "by_name": dict(by_name),
        "by_content": dict(by_content),
    }
    report_path = VAULT / "00-索引与导航" / "知识图谱" / "classification.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")

if __name__ == "__main__":
    scan()
