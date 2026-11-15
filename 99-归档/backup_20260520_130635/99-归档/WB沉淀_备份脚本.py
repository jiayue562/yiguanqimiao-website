# -*- coding: utf-8 -*-
"""
增量备份脚本
功能：
1. 计算文件哈希值
2. 比对变更文件
3. 只备份变更内容
4. 保存备份历史
5. 支持版本回滚
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

class IncrementalBackup:
    def __init__(self, source_path, backup_path):
        self.source_path = source_path
        self.backup_path = backup_path
        self.hash_file = os.path.join(backup_path, '.backup_hashes.json')
        self.history_file = os.path.join(backup_path, '.backup_history.json')
        
    def calculate_hash(self, file_path):
        """计算文件MD5哈希"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return None
    
    def load_hashes(self):
        """加载已保存的哈希记录"""
        if os.path.exists(self.hash_file):
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_hashes(self, hashes):
        """保存哈希记录"""
        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(hashes, f, ensure_ascii=False, indent=2)
    
    def load_history(self):
        """加载备份历史"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_history(self, history):
        """保存备份历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def scan_changes(self):
        """扫描变更文件"""
        print("=" * 60)
        print("增量备份工具")
        print("=" * 60)
        print(f"\n源目录: {self.source_path}")
        print(f"备份目录: {self.backup_path}")
        
        old_hashes = self.load_hashes()
        new_hashes = {}
        changes = {
            'added': [],
            'modified': [],
            'deleted': []
        }
        
        # 扫描源目录
        for root, dirs, files in os.walk(self.source_path):
            # 跳过隐藏文件夹
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.source_path)
                new_hash = self.calculate_hash(file_path)
                
                if new_hash:
                    new_hashes[rel_path] = new_hash
                    
                    if rel_path not in old_hashes:
                        changes['added'].append(rel_path)
                    elif old_hashes[rel_path] != new_hash:
                        changes['modified'].append(rel_path)
        
        # 检查删除的文件
        for rel_path in old_hashes:
            if rel_path not in new_hashes:
                changes['deleted'].append(rel_path)
        
        return changes, new_hashes
    
    def backup_files(self, changes):
        """备份变更文件"""
        total = len(changes['added']) + len(changes['modified'])
        
        print(f"\n📊 变更统计:")
        print(f"   新增文件: {len(changes['added'])}")
        print(f"   修改文件: {len(changes['modified'])}")
        print(f"   删除文件: {len(changes['deleted'])}")
        print(f"   总计备份: {total} 个文件")
        
        if total == 0:
            print("\n✅ 没有需要备份的文件")
            return []
        
        # 创建备份
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_subdir = os.path.join(self.backup_path, f'backup_{timestamp}')
        os.makedirs(backup_subdir, exist_ok=True)
        
        backed_up = []
        
        # 备份新增和修改的文件
        for rel_path in changes['added'] + changes['modified']:
            src = os.path.join(self.source_path, rel_path)
            dst = os.path.join(backup_subdir, rel_path)
            dst_dir = os.path.dirname(dst)
            
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src, dst)
            backed_up.append(rel_path)
            print(f"   📄 {rel_path}")
        
        # 记录删除的文件
        for rel_path in changes['deleted']:
            print(f"   🗑️ {rel_path} (已删除)")
        
        # 保存历史记录
        history = self.load_history()
        history.append({
            'timestamp': timestamp,
            'date': datetime.now().isoformat(),
            'changes': {
                'added': len(changes['added']),
                'modified': len(changes['modified']),
                'deleted': len(changes['deleted'])
            },
            'files': backed_up
        })
        self.save_history(history)
        
        print(f"\n✅ 备份完成!")
        print(f"   备份位置: {backup_subdir}")
        
        return backed_up
    
    def restore(self, timestamp=None):
        """恢复备份"""
        history = self.load_history()
        
        if not history:
            print("❌ 没有备份记录")
            return
        
        if timestamp is None:
            # 使用最新备份
            latest = history[-1]
        else:
            latest = next((h for h in history if h['timestamp'] == timestamp), None)
            if not latest:
                print(f"❌ 未找到备份: {timestamp}")
                return
        
        print(f"\n🔄 恢复备份: {latest['date']}")
        print(f"   文件数: {len(latest['files'])}")
        
        backup_dir = os.path.join(self.backup_path, f"backup_{latest['timestamp']}")
        
        for rel_path in latest['files']:
            src = os.path.join(backup_dir, rel_path)
            dst = os.path.join(self.source_path, rel_path)
            
            if os.path.exists(src):
                dst_dir = os.path.dirname(dst)
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"   ✅ {rel_path}")
        
        print(f"\n✅ 恢复完成!")

def main():
    # 配置路径
    source_path = r"C:\Users\jia'yue\.qclaw\workspace"
    backup_path = r"C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\WorkBuddy知识沉淀\08-WB-验证工具\备份历史"
    
    backup = IncrementalBackup(source_path, backup_path)
    changes, new_hashes = backup.scan_changes()
    backup.backup_files(changes)
    backup.save_hashes(new_hashes)

if __name__ == "__main__":
    main()
