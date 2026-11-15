# -*- coding: utf-8 -*-
"""
知识库增量备份管理器
功能:
  - 文件哈希比对，只备份变更文件
  - 保存备份历史记录
  - 支持版本回滚
  - 三库同步状态记录
"""
import os, sys, json, hashlib, shutil, argparse
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\以观其妙书院知识库\以观其妙书院")
BACKUP_ROOT = VAULT / "_backups"
HISTORY_FILE = BACKUP_ROOT / "_history.json"
EXCLUDE_DIRS = {".trash", ".git", ".obsidian", ".workbuddy", "_backups",
                "node_modules", "__pycache__", ".claude", ".codebuddy", ".cursor"}

def ensure_dirs():
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

def file_hash(path):
    """计算文件 MD5"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_history():
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"backups": [], "file_hashes": {}}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def do_backup(label=""):
    """执行增量备份"""
    ensure_dirs()
    history = load_history()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / f"backup_{timestamp}"
    old_hashes = history.get("file_hashes", {})
    new_hashes = {}
    changed = []
    unchanged = 0

    print(f"\n{'='*60}")
    print(f"  增量备份: {timestamp}")
    print(f"  Label: {label or '(无)'}")
    print(f"{'='*60}\n")

    for p in VAULT.rglob("*"):
        if any(e in p.parts for e in EXCLUDE_DIRS):
            continue
        if p.is_file():
            rel = str(p.relative_to(VAULT))
            h = file_hash(p)
            new_hashes[rel] = h

            if rel not in old_hashes or old_hashes[rel] != h:
                changed.append(rel)
                dest = backup_dir / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
            else:
                unchanged += 1

    # 记录
    record = {
        "timestamp": timestamp,
        "label": label,
        "changed": len(changed),
        "unchanged": unchanged,
        "total": len(new_hashes),
        "changed_files": changed[:100],  # 只记录前 100 个
    }
    history["backups"].append(record)
    history["file_hashes"] = new_hashes
    save_history(history)

    print(f"  变更文件: {len(changed)}")
    print(f"  未变更:   {unchanged}")
    print(f"  总计:     {len(new_hashes)}")
    print(f"  备份目录: {backup_dir}")
    print(f"\n  变更文件列表 (前 20):")
    for f in changed[:20]:
        print(f"    + {f}")
    if len(changed) > 20:
        print(f"    ... 还有 {len(changed) - 20} 个")

    return record

def list_backups():
    """列出所有备份"""
    history = load_history()
    print(f"\n{'='*60}")
    print(f"  备份历史")
    print(f"{'='*60}\n")
    print(f"{'时间':<20} {'标签':<20} {'变更':<8} {'总计':<8}")
    print("-" * 60)
    for b in reversed(history.get("backups", [])):
        print(f"{b['timestamp']:<20} {b.get('label',''):<20} {b['changed']:<8} {b['total']:<8}")

def rollback(timestamp):
    """回滚到指定版本"""
    backup_dir = BACKUP_ROOT / f"backup_{timestamp}"
    if not backup_dir.exists():
        print(f"\n❌ 备份不存在: {backup_dir}")
        return False

    print(f"\n{'='*60}")
    print(f"  回滚到: {timestamp}")
    print(f"{'='*60}\n")
    print(f"⚠️  警告: 将恢复 {backup_dir} 中的文件到 {VAULT}")
    print(f"  当前文件将被覆盖！")
    confirm = input("  确认回滚? (yes/no): ")
    if confirm.lower() != "yes":
        print("  已取消")
        return False

    restored = 0
    for p in backup_dir.rglob("*"):
        if p.is_file():
            rel = p.relative_to(backup_dir)
            dest = VAULT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
            restored += 1

    print(f"\n  已恢复 {restored} 个文件")
    return True

def show_status():
    """显示备份状态"""
    history = load_history()
    backups = history.get("backups", [])
    print(f"\n{'='*60}")
    print(f"  备份状态")
    print(f"{'='*60}")
    print(f"  总备份数: {len(backups)}")
    print(f"  总文件数: {len(history.get('file_hashes', {}))}")
    if backups:
        last = backups[-1]
        print(f"  最近备份: {last['timestamp']} ({last['changed']} changed)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="知识库增量备份管理器")
    parser.add_argument("--backup", "-b", action="store_true", help="执行增量备份")
    parser.add_argument("--list", "-l", action="store_true", help="列出备份历史")
    parser.add_argument("--status", "-s", action="store_true", help="显示备份状态")
    parser.add_argument("--rollback", "-r", type=str, help="回滚到指定版本 (timestamp)")
    parser.add_argument("--label", type=str, default="", help="备份标签")
    args = parser.parse_args()

    if args.backup:
        do_backup(args.label)
    elif args.list:
        list_backups()
    elif args.rollback:
        rollback(args.rollback)
    elif args.status:
        show_status()
    else:
        parser.print_help()
