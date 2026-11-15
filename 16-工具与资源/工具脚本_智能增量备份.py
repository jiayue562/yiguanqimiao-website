#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【增量备份脚本】smart-backup.py
功能：智能增量备份，只备份变更文件，支持版本回滚
版本：v1.0 | 创建：2026-04-03 | 龙龟神将

使用方法：
    python smart-backup.py          # 执行增量备份
    python smart-backup.py --list   # 列出备份历史
    python smart-backup.py --restore <version>  # 恢复到指定版本
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================
# 配置区
# ============================================

VAULT_ROOT = Path(r"D:\以观其妙书院知识库\观其妙书院")
BACKUP_ROOT = Path(r"D:\以观其妙书院知识库\备份")
HASH_FILE = BACKUP_ROOT / "file_hashes.json"
BACKUP_HISTORY = BACKUP_ROOT / "backup_history.json"

# 备份保留策略
MAX_FULL_BACKUPS = 10  # 最多保留10个完整备份
MAX_INCREMENTAL = 50   # 最多保留50个增量备份

# 排除的目录/文件
EXCLUDE_PATTERNS = [
    ".obsidian",
    ".git",
    "node_modules",
    "__pycache__",
    "*.tmp",
    "*.bak",
    "备份",
]


class SmartBackup:
    """智能增量备份系统"""

    def __init__(self, vault_root: Path, backup_root: Path):
        self.vault_root = vault_root
        self.backup_root = backup_root
        self.hash_file = HASH_FILE
        self.history_file = BACKUP_HISTORY

        # 确保备份目录存在
        self.backup_root.mkdir(parents=True, exist_ok=True)

        # 加载历史数据
        self.file_hashes: Dict[str, str] = self._load_json(self.hash_file, {})
        self.backup_history: List[Dict] = self._load_json(self.history_file, [])

    def _load_json(self, file_path: Path, default: any) -> any:
        """加载JSON文件"""
        if file_path.exists():
            try:
                return json.loads(file_path.read_text(encoding="utf-8"))
            except:
                return default
        return default

    def _save_json(self, file_path: Path, data: any):
        """保存JSON文件"""
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _get_file_hash(self, file_path: Path) -> str:
        """计算文件哈希"""
        hasher = hashlib.sha256()
        try:
            hasher.update(file_path.read_bytes())
            return hasher.hexdigest()
        except:
            return ""

    def _should_exclude(self, path: Path) -> bool:
        """检查是否应该排除"""
        path_str = str(path)
        for pattern in EXCLUDE_PATTERNS:
            if pattern.startswith("*"):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False

    def scan_changes(self) -> Tuple[List[Path], List[Path], List[Path]]:
        """扫描变更文件"""
        changed = []
        added = []
        deleted = []

        # 扫描当前文件
        current_files = set()
        for file_path in self.vault_root.rglob("*"):
            if file_path.is_file() and not self._should_exclude(file_path):
                rel_path = str(file_path.relative_to(self.vault_root))
                current_files.add(rel_path)

                # 检查是否新增或变更
                current_hash = self._get_file_hash(file_path)
                old_hash = self.file_hashes.get(rel_path, "")

                if old_hash == "":
                    added.append(file_path)
                elif current_hash != old_hash:
                    changed.append(file_path)

        # 检查删除的文件
        for rel_path in self.file_hashes.keys():
            if rel_path not in current_files:
                deleted.append(Path(rel_path))

        return changed, added, deleted

    def create_backup(self, backup_type: str = "incremental") -> bool:
        """创建备份"""
        print("=" * 60)
        print("📦 观其妙书院知识库 · 智能增量备份")
        print("=" * 60)
        print()

        # 扫描变更
        changed, added, deleted = self.scan_changes()

        if not changed and not added and not deleted:
            print("✅ 没有检测到变更，无需备份")
            return True

        # 创建备份目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_root / timestamp

        # 决定是否需要完整备份
        needs_full = (len(changed) + len(added)) > 100 or backup_type == "full"

        if needs_full:
            backup_type = "full"
            backup_dir = self.backup_root / f"FULL_{timestamp}"

        backup_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 备份类型: {backup_type.upper()}")
        print(f"📍 备份位置: {backup_dir}")
        print()
        print(f"📊 变更统计:")
        print(f"   修改: {len(changed)} 个文件")
        print(f"   新增: {len(added)} 个文件")
        print(f"   删除: {len(deleted)} 个文件")
        print()

        # 备份文件
        copied_count = 0
        for file_path in changed + added:
            rel_path = file_path.relative_to(self.vault_root)
            dest_path = backup_dir / rel_path

            # 创建目标目录
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # 复制文件
            shutil.copy2(file_path, dest_path)
            copied_count += 1

            # 更新哈希
            self.file_hashes[str(rel_path)] = self._get_file_hash(file_path)

        # 保存变更记录
        for rel_path in deleted:
            if rel_path in self.file_hashes:
                del self.file_hashes[str(rel_path)]

        # 保存哈希文件
        self._save_json(self.hash_file, self.file_hashes)

        # 记录备份历史
        history_entry = {
            "timestamp": timestamp,
            "type": backup_type,
            "backup_dir": str(backup_dir),
            "changed": len(changed),
            "added": len(added),
            "deleted": len(deleted),
            "total_files": copied_count,
        }
        self.backup_history.append(history_entry)
        self._save_json(self.history_file, self.backup_history)

        # 清理过期备份
        self._cleanup_old_backups()

        print(f"✅ 备份完成！共备份 {copied_count} 个文件")
        print(f"📄 备份记录已保存")
        return True

    def _cleanup_old_backups(self):
        """清理过期备份"""
        full_backups = []
        incremental_backups = []

        for entry in self.backup_history:
            backup_dir = Path(entry["backup_dir"])
            if "FULL_" in backup_dir.name:
                full_backups.append(backup_dir)
            else:
                incremental_backups.append(backup_dir)

        # 清理多余完整备份
        if len(full_backups) > MAX_FULL_BACKUPS:
            to_delete = full_backups[:-MAX_FULL_BACKUPS]
            for backup_dir in to_delete:
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                    print(f"🗑️  删除过期完整备份: {backup_dir.name}")

        # 清理多余增量备份
        if len(incremental_backups) > MAX_INCREMENTAL:
            to_delete = incremental_backups[:-MAX_INCREMENTAL]
            for backup_dir in to_delete:
                if backup_dir.exists():
                    shutil.rmtree(backup_dir)
                    print(f"🗑️  删除过期增量备份: {backup_dir.name}")

    def list_backups(self):
        """列出备份历史"""
        print("=" * 60)
        print("📜 备份历史记录")
        print("=" * 60)
        print()

        if not self.backup_history:
            print("暂无备份记录")
            return

        for i, entry in enumerate(reversed(self.backup_history[-20:]), 1):
            print(f"{i}. [{entry['type'].upper()}] {entry['timestamp']}")
            print(f"   位置: {entry['backup_dir']}")
            print(f"   文件: 修改{entry['changed']} | 新增{entry['added']} | 删除{entry['deleted']}")
            print()

    def restore_backup(self, version: str) -> bool:
        """恢复到指定版本"""
        print("=" * 60)
        print("🔄 恢复备份")
        print("=" * 60)
        print()

        # 查找目标备份
        target_backup = None
        for entry in self.backup_history:
            if version in entry["timestamp"] or version in entry["backup_dir"]:
                target_backup = entry
                break

        if not target_backup:
            print(f"❌ 未找到备份: {version}")
            return False

        backup_dir = Path(target_backup["backup_dir"])
        if not backup_dir.exists():
            print(f"❌ 备份目录不存在: {backup_dir}")
            return False

        # 确认操作
        print(f"⚠️  即将恢复到: {target_backup['timestamp']}")
        print(f"📍 备份位置: {backup_dir}")
        print(f"⚠️  这将覆盖当前文件！")
        print()
        confirm = input("确认恢复？(y/N): ")
        if confirm.lower() != "y":
            print("取消恢复")
            return False

        # 创建回滚点
        rollback_dir = self.backup_root / f"ROLLBACK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        rollback_dir.mkdir(parents=True, exist_ok=True)

        print("📦 创建回滚点...")
        for file_path in self.vault_root.rglob("*"):
            if file_path.is_file() and not self._should_exclude(file_path):
                rel_path = file_path.relative_to(self.vault_root)
                dest_path = rollback_dir / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_path)

        print(f"✅ 回滚点已创建: {rollback_dir}")

        # 恢复文件
        print("📦 恢复文件...")
        for file_path in backup_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(backup_dir)
                dest_path = self.vault_root / rel_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_path)

        # 更新哈希
        self.file_hashes = {}
        for file_path in backup_dir.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(backup_dir))
                self.file_hashes[rel_path] = self._get_file_hash(file_path)
        self._save_json(self.hash_file, self.file_hashes)

        print("✅ 恢复完成！")
        print(f"💡 如需回滚，可使用: {rollback_dir}")
        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能增量备份工具")
    parser.add_argument("--list", action="store_true", help="列出备份历史")
    parser.add_argument("--restore", metavar="VERSION", help="恢复到指定版本")
    parser.add_argument("--full", action="store_true", help="执行完整备份")

    args = parser.parse_args()

    if not VAULT_ROOT.exists():
        print(f"❌ 错误：知识库路径不存在 {VAULT_ROOT}")
        return

    backup = SmartBackup(VAULT_ROOT, BACKUP_ROOT)

    if args.list:
        backup.list_backups()
    elif args.restore:
        backup.restore_backup(args.restore)
    else:
        backup_type = "full" if args.full else "incremental"
        backup.create_backup(backup_type)


if __name__ == "__main__":
    main()
