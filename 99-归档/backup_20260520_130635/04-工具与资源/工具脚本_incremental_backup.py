#!/usr/bin/env python3
"""
知识库增量备份工具
使用文件哈希比对，只备份变更文件
支持备份历史记录和版本回滚
"""

import os
import json
import shutil
import hashlib
import datetime
from pathlib import Path

# 配置
VAULT_PATH = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院"
BACKUP_ROOT = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\备份"
HASH_FILE = "file_hashes.json"
HISTORY_FILE = "backup_history.json"

class IncrementalBackup:
    def __init__(self, vault_path, backup_root):
        self.vault_path = Path(vault_path)
        self.backup_root = Path(backup_root)
        self.hash_file = self.backup_root / HASH_FILE
        self.history_file = self.backup_root / HISTORY_FILE
        
        # 确保备份目录存在
        self.backup_root.mkdir(parents=True, exist_ok=True)
    
    def compute_file_hash(self, file_path):
        """计算文件的 SHA256 哈希"""
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            print(f"⚠️ 计算哈希失败 {file_path}: {e}")
            return None
    
    def load_hashes(self):
        """加载上次保存的文件哈希"""
        if self.hash_file.exists():
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_hashes(self, hashes):
        """保存文件哈希"""
        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(hashes, f, indent=2, ensure_ascii=False)
    
    def load_history(self):
        """加载备份历史"""
        if self.history_file.exists():
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self, history):
        """保存备份历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def scan_vault(self):
        """扫描知识库文件"""
        files = {}
        for file_path in self.vault_path.rglob("*"):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                rel_path = str(file_path.relative_to(self.vault_path))
                files[rel_path] = self.compute_file_hash(file_path)
        return files
    
    def run_backup(self):
        """执行增量备份"""
        print(f"🔄 开始增量备份...")
        print(f"   知识库: {self.vault_path}")
        print(f"   备份目录: {self.backup_root}")
        
        # 加载上次的哈希
        old_hashes = self.load_hashes()
        
        # 扫描当前文件
        current_files = self.scan_vault()
        
        # 创建备份目录（按日期）
        backup_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.backup_root / backup_date
        backup_dir.mkdir(exist_ok=True)
        
        # 统计
        stats = {
            'added': [],
            'modified': [],
            'deleted': [],
            'unchanged': []
        }
        
        # 检查新增和修改的文件
        for rel_path, file_hash in current_files.items():
            old_hash = old_hashes.get(rel_path)
            
            if old_hash is None:
                # 新增文件
                stats['added'].append(rel_path)
                self._backup_file(rel_path, backup_dir)
            elif old_hash != file_hash:
                # 修改的文件
                stats['modified'].append(rel_path)
                self._backup_file(rel_path, backup_dir)
            else:
                # 未变化
                stats['unchanged'].append(rel_path)
        
        # 检查删除的文件
        for rel_path in old_hashes:
            if rel_path not in current_files:
                stats['deleted'].append(rel_path)
        
        # 保存当前哈希
        self.save_hashes(current_files)
        
        # 记录历史
        history = self.load_history()
        history.append({
            'timestamp': backup_date,
            'stats': {k: len(v) for k, v in stats.items()},
            'backup_dir': str(backup_dir)
        })
        
        # 只保留最近30个备份
        if len(history) > 30:
            history = history[-30:]
        
        self.save_history(history)
        
        # 输出结果
        print(f"\n✅ 备份完成!")
        print(f"   新增: {len(stats['added'])} 个文件")
        print(f"   修改: {len(stats['modified'])} 个文件")
        print(f"   删除: {len(stats['deleted'])} 个文件")
        print(f"   未变: {len(stats['unchanged'])} 个文件")
        print(f"   备份位置: {backup_dir}")
        
        return stats, backup_dir
    
    def _backup_file(self, rel_path, backup_dir):
        """备份单个文件"""
        source = self.vault_path / rel_path
        target = backup_dir / rel_path
        
        # 确保目标目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件
        shutil.copy2(source, target)
    
    def restore_backup(self, backup_date=None):
        """恢复备份"""
        history = self.load_history()
        
        if not history:
            print("❌ 没有备份历史")
            return
        
        # 选择要恢复的备份
        if backup_date is None:
            # 恢复最近的备份
            backup_info = history[-1]
        else:
            # 查找指定日期的备份
            backup_info = None
            for h in history:
                if h['timestamp'] == backup_date:
                    backup_info = h
                    break
            
            if backup_info is None:
                print(f"❌ 找不到日期为 {backup_date} 的备份")
                return
        
        backup_dir = Path(backup_info['backup_dir'])
        
        if not backup_dir.exists():
            print(f"❌ 备份目录不存在: {backup_dir}")
            return
        
        print(f"🔄 正在恢复备份: {backup_info['timestamp']}")
        
        # 复制文件
        restored_count = 0
        for file_path in backup_dir.rglob("*"):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(backup_dir))
                target = self.vault_path / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, target)
                restored_count += 1
        
        print(f"✅ 已恢复 {restored_count} 个文件")
    
    def list_backups(self):
        """列出所有备份"""
        history = self.load_history()
        
        if not history:
            print("📭 没有备份记录")
            return
        
        print(f"\n📜 备份历史 (共 {len(history)} 个备份):\n")
        print(f"{'日期':<20} | {'新增':<6} | {'修改':<6} | {'删除':<6}")
        print("-" * 55)
        
        for h in reversed(history):
            stats = h['stats']
            print(f"{h['timestamp']:<20} | {stats['added']:<6} | {stats['modified']:<6} | {stats['deleted']:<6}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库增量备份工具')
    parser.add_argument('command', choices=['backup', 'restore', 'list'],
                        help='命令: backup(备份), restore(恢复), list(列表)')
    parser.add_argument('--date', help='恢复指定日期的备份 (格式: YYYYMMDD_HHMMSS)')
    
    args = parser.parse_args()
    
    backup = IncrementalBackup(VAULT_PATH, BACKUP_ROOT)
    
    if args.command == 'backup':
        backup.run_backup()
    elif args.command == 'restore':
        backup.restore_backup(args.date)
    elif args.command == 'list':
        backup.list_backups()

if __name__ == "__main__":
    main()
