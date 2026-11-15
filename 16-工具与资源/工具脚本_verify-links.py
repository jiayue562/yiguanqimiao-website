#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【双向链接验证脚本】verify-links.py
功能：验证Obsidian知识库中双向链接的完整性
版本：v1.0 | 创建：2026-04-03 | 龙龟神将

使用方法：
    python verify-links.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# ============================================
# 配置区
# ============================================

VAULT_ROOT = Path(r"D:\以观其妙书院知识库\观其妙书院")

# 排除的目录
EXCLUDE_DIRS = {".obsidian", "node_modules", ".git", "__pycache__"}

# 支持的链接格式
LINK_PATTERN = re.compile(r'\[\[([^\]]+)\]\]')


class LinkVerifier:
    """双向链接验证器"""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.all_links: Dict[Path, Set[str]] = {}  # 文件 -> 它引用的链接
        self.backlinks: Dict[str, Set[Path]] = defaultdict(set)  # 被链接的文件 -> 链接它的文件
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def scan_vault(self):
        """扫描整个知识库"""
        print("📂 扫描知识库...")
        md_files = list(self.vault_root.rglob("*.md"))

        for md_file in md_files:
            # 跳过排除目录
            if any(excluded in md_file.parts for excluded in EXCLUDE_DIRS):
                continue

            self._process_file(md_file)

        print(f"✅ 扫描完成：{len(self.all_links)} 个文件，{len(self.backlinks)} 个被链接目标")
        return len(self.all_links) > 0

    def _process_file(self, file_path: Path):
        """处理单个文件"""
        try:
            content = file_path.read_text(encoding="utf-8")
            links = LINK_PATTERN.findall(content)

            # 转换为相对路径格式
            normalized_links = set()
            for link in links:
                # 处理链接中的 | 别名
                link_target = link.split("|")[0].strip()
                normalized_links.add(link_target)

            self.all_links[file_path] = normalized_links

            # 记录反向链接
            for link_target in normalized_links:
                self.backlinks[link_target].add(file_path)

        except Exception as e:
            self.errors.append(f"读取失败 {file_path}: {e}")

    def verify_links(self) -> Tuple[int, int, int]:
        """验证所有链接"""
        print("\n🔍 验证双向链接...")

        valid_count = 0
        broken_count = 0
        missing_backlink_count = 0

        # 创建文件路径映射（支持多种扩展名）
        def find_target(link_target: str) -> Path:
            """查找链接目标文件"""
            # 移除目录前缀如果存在
            if "/" in link_target:
                parts = link_target.split("/")
                for i in range(len(parts)):
                    candidate = Path(*parts[i:])
                    for ext in ["", ".md"]:
                        full_path = self.vault_root / (str(candidate).replace("/", os.sep) + ext)
                        if full_path.exists():
                            return full_path
            else:
                # 直接文件名
                for ext in ["", ".md"]:
                    full_path = self.vault_root / (link_target + ext)
                    if full_path.exists():
                        return full_path
            return None

        # 检查每个链接
        for file_path, links in self.all_links.items():
            for link in links:
                target = find_target(link)
                if target is None:
                    self.warnings.append(f"⚠️  断链: {file_path.name} -> [[{link}]]")
                    broken_count += 1
                else:
                    # 检查是否有反向链接
                    if link not in self.backlinks or len(self.backlinks[link]) <= 1:
                        # 只有一个链接（自己到自己）或没有链接
                        pass  # 这是正常的，不算错误
                    valid_count += 1

        # 检查孤立文件（没有任何文件链接它，也没有链接其他文件）
        for file_path, links in self.all_links.items():
            if len(links) == 0 and file_path.name != "__init__.md":
                # 检查是否有反向链接
                file_key = file_path.stem  # 无扩展名的文件名
                has_backlink = any(
                    file_key in str(backlink) or file_path.name in str(backlink)
                    for backlink_set in self.backlinks.values()
                    for backlink in backlink_set
                )
                if not has_backlink:
                    self.warnings.append(f"⚠️  孤立文件: {file_path.name}")

        return valid_count, broken_count, missing_backlink_count

    def generate_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("=" * 60)
        report.append("📊 双向链接验证报告")
        report.append("=" * 60)
        report.append(f"知识库: {self.vault_root}")
        report.append(f"扫描文件: {len(self.all_links)}")
        report.append(f"被链接目标: {len(self.backlinks)}")
        report.append("")

        if self.errors:
            report.append("❌ 错误:")
            for error in self.errors[:10]:
                report.append(f"   {error}")
            if len(self.errors) > 10:
                report.append(f"   ... 还有 {len(self.errors) - 10} 个错误")
            report.append("")

        if self.warnings:
            report.append("⚠️  警告/断链:")
            for warning in self.warnings[:20]:
                report.append(f"   {warning}")
            if len(self.warnings) > 20:
                report.append(f"   ... 还有 {len(self.warnings) - 20} 个警告")
            report.append("")

        # 统计信息
        total_links = sum(len(links) for links in self.all_links.values())
        report.append("📈 统计:")
        report.append(f"   总链接数: {total_links}")
        report.append(f"   平均每文件链接: {total_links / len(self.all_links):.2f}")

        # 链接最多的文件
        if self.all_links:
            top_linked = sorted(
                self.all_links.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:5]
            report.append("")
            report.append("🔗 链接最多的文件:")
            for file_path, links in top_linked:
                report.append(f"   {file_path.name}: {len(links)} 个链接")

        # 被链接最多的文件
        if self.backlinks:
            top_backlinked = sorted(
                self.backlinks.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:5]
            report.append("")
            report.append("🔗 被链接最多的文件:")
            for target, files in top_backlinked:
                report.append(f"   [[{target}]]: {len(files)} 个反向链接")

        report.append("")
        report.append("=" * 60)
        report.append("验证完成")
        report.append("=" * 60)

        return "\n".join(report)


def main():
    """主函数"""
    print("=" * 60)
    print("🔗 观其妙书院知识库 · 双向链接验证")
    print("=" * 60)
    print()

    if not VAULT_ROOT.exists():
        print(f"❌ 错误：路径不存在 {VAULT_ROOT}")
        return

    verifier = LinkVerifier(VAULT_ROOT)

    if verifier.scan_vault():
        valid, broken, missing = verifier.verify_links()
        report = verifier.generate_report()
        print(report)

        # 保存报告
        report_file = VAULT_ROOT / "08-工具与脚本" / "链接验证报告.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report, encoding="utf-8")
        print(f"\n📄 报告已保存: {report_file}")

        if broken > 0:
            print(f"\n⚠️  发现 {broken} 个断链，请检查")
        else:
            print("\n✅ 所有链接验证通过！")
    else:
        print("❌ 扫描失败")


if __name__ == "__main__":
    main()
