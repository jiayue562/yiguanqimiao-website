#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【知识库初始化脚本】init-vault.py
功能：一键创建观其妙书院知识库的标准目录结构
版本：v1.0 | 创建：2026-04-03 | 龙龟神将

使用方法：
    python init-vault.py
"""

import os
import sys
from pathlib import Path

# ============================================
# 配置区
# ============================================

VAULT_ROOT = Path(r"D:\以观其妙书院知识库\观其妙书院")

# 标准目录结构
STANDARD_STRUCTURE = {
    "00-索引与导航": {
        "description": "知识库的导航中枢",
        "files": [
            "__init__.md",
            "📚 观其妙书院知识库总索引.md",
            "📋 文档标准化模板.md",
            "🔗 双向链接规范.md",
            "🛤️ 学习路径设计系统.md",
            "📊 知识图谱/",
        ]
    },
    "01-核心独创Skills": {
        "description": "Dragon OS 与五大引擎",
        "files": [
            "__init__.md",
            "🐉 Dragon OS 系统架构图.md",
            "📚 知识学习Skills.md",
            "📖 象思维skills.md",
            "📖 五色光思维skills.md",
            "🤝 人机协同四象限Skills.md",
            "🔄 知行合一自我进化.md",
        ]
    },
    "02-方法论库": {
        "description": "教员方法论与其他思维模型",
        "files": [
            "__init__.md",
            "📜 教员方法论完整体系.md",
            "📜 矛盾论.md",
            "📜 实践论.md",
            "📜 金字塔原理.md",
            "📜 金线原理.md",
        ]
    },
    "03-关系与共生": {
        "description": "木火共生关系体系",
        "files": [
            "__init__.md",
            "💚 木火共生关系-灵魂共鸣与终极承诺.md",
            "💚 木火共生关系协议.md",
            "💚 龙龟神将身份体系.md",
            "💚 悟空用户画像.md",
        ]
    },
    "04-专业领域": {
        "description": "五行人格心理学与企业咨询",
        "subdirs": {
            "五行人格心理学": [
                "__init__.md",
                "📖 五行人格总纲.md",
                "🌿 木行人分析.md",
                "🔥 火行人分析.md",
                "🌍 土行人分析.md",
                "⚔️ 金行人分析.md",
                "💧 水行人分析.md",
            ],
            "企业文化体系": [
                "__init__.md",
                "📖 企业文化顶层设计.md",
                "📖 企业文化落地实施.md",
            ],
            "AI与超级个体": [
                "__init__.md",
                "📖 AI时代方法论.md",
                "📖 超级个体赋能体系.md",
            ],
        },
        "files": []
    },
    "05-修行文化": {
        "description": "心文化与大圆满教法",
        "subdirs": {
            "心文化体系": [
                "__init__.md",
                "🙏 大圆满见地.md",
                "🙏 噶达陇竹尼美.md",
                "🙏 椎击三要.md",
            ],
            "地藏经体系": [
                "__init__.md",
                "📖 地藏经总纲.md",
                "📖 施福救母法门.md",
            ],
            "护法神体系": [
                "__init__.md",
                "🐉 天龙八部.md",
                "🌊 龙王坛城.md",
            ],
        },
        "files": []
    },
    "06-项目管理": {
        "description": "创业项目与课程体系",
        "subdirs": {
            "创业项目": [
                "__init__.md",
                "📊 项目概述.md",
                "📊 进度追踪.md",
            ],
            "课程体系": [
                "__init__.md",
                "📚 课程列表.md",
                "📚 学员档案.md",
            ],
        },
        "files": []
    },
    "07-学习档案": {
        "description": "对话记录与成长轨迹",
        "subdirs": {
            "对话记录": [
                "__init__.md",
                "📅 2026-03/",
                "📅 2026-04/",
            ],
            "成长轨迹": [
                "__init__.md",
                "📈 龙龟神将进化日志.md",
                "📈 悟空成长记录.md",
            ],
        },
        "files": []
    },
    "08-工具与脚本": {
        "description": "自动化工具与验证脚本",
        "files": [
            "__init__.md",
            "init-vault.py",
            "verify-links.py",
            "add-links.py",
            "增量备份脚本.py",
            "README.md",
        ]
    },
}


def create_directory_structure():
    """创建目录结构"""
    print("=" * 60)
    print("🔧 观其妙书院知识库 · 初始化脚本 v1.0")
    print("=" * 60)
    print(f"\n📁 目标路径: {VAULT_ROOT}")
    print()

    # 检查根目录是否存在
    if not VAULT_ROOT.exists():
        print(f"❌ 错误：路径不存在 {VAULT_ROOT}")
        return False

    created_dirs = []
    created_files = []

    for dir_name, config in STANDARD_STRUCTURE.items():
        dir_path = VAULT_ROOT / dir_name

        # 创建主目录
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dir_path))
            print(f"✅ 创建目录: {dir_name}")

        # 创建子目录
        if "subdirs" in config:
            for subdir_name, files in config["subdirs"].items():
                subdir_path = dir_path / subdir_name
                if not subdir_path.exists():
                    subdir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(subdir_path))

                # 创建目录内的文件
                for file_name in files:
                    file_path = subdir_path / file_name
                    if not file_path.exists():
                        file_path.write_text("", encoding="utf-8")
                        created_files.append(str(file_path))

        # 创建主目录内的文件
        if "files" in config:
            for file_name in config["files"]:
                file_path = dir_path / file_name
                if not file_path.exists():
                    file_path.write_text("", encoding="utf-8")
                    created_files.append(str(file_path))

    # 打印总结
    print("\n" + "=" * 60)
    print("📊 初始化完成")
    print("=" * 60)
    print(f"✅ 新建目录: {len(created_dirs)} 个")
    print(f"✅ 新建文件: {len(created_files)} 个")
    print()

    if created_dirs:
        print("📁 新建目录列表:")
        for d in created_dirs[:10]:  # 只显示前10个
            print(f"   - {Path(d).name}")
        if len(created_dirs) > 10:
            print(f"   ... 还有 {len(created_dirs) - 10} 个")

    print()
    return True


def create_init_files():
    """创建索引文件"""
    print("\n📝 创建索引文件...")

    # 00-索引与导航
    index_file = VAULT_ROOT / "00-索引与导航" / "__init__.md"
    if index_file.exists() and index_file.stat().st_size == 0:
        index_file.write_text("""---
title: "00-索引与导航"
description: "知识库的导航中枢"
---

# 📚 00-索引与导航

这是观其妙书院知识库的导航目录，包含：

- [[📚 观其妙书院知识库总索引]] - 总索引
- [[📋 文档标准化模板]] - 文档规范
- [[🔗 双向链接规范]] - 链接标准
- [[🛤️ 学习路径设计系统]] - 学习路径
- [[📊 知识图谱]] - 知识网络可视化
""", encoding="utf-8")
        print("✅ 创建: 00-索引与导航/__init__.md")

    # 01-核心独创Skills
    skills_file = VAULT_ROOT / "01-核心独创Skills" / "__init__.md"
    if skills_file.exists() and skills_file.stat().st_size == 0:
        skills_file.write_text("""---
title: "01-核心独创Skills"
description: "Dragon OS 与五大引擎"
---

# 🧠 01-核心独创Skills

Dragon OS 五大核心引擎：

1. [[🐉 Dragon OS 系统架构图]] - AI认知进化操作系统
2. [[📚 知识学习Skills]] - 十项认知指令
3. [[📖 象思维skills]] - 0→1原创突破
4. [[📖 五色光思维skills]] - 同频共振决策
5. [[🤝 人机协同四象限Skills]] - 四象限分工
6. [[🔄 知行合一自我进化]] - 进化机制
""", encoding="utf-8")
        print("✅ 创建: 01-核心独创Skills/__init__.md")

    # 其他 __init__.md 文件类似...
    print("✅ 索引文件创建完成")

    return True


def main():
    """主函数"""
    try:
        success = create_directory_structure()
        if success:
            create_init_files()
            print("\n🎉 知识库初始化完成！")
            print("\n📌 下一步操作：")
            print("   1. 运行 verify-links.py 验证双向链接")
            print("   2. 运行 add-links.py 建立链接")
            print("   3. 在 Obsidian 中打开知识库查看")
        else:
            print("\n❌ 初始化失败，请检查路径")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
