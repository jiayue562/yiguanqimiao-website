# -*- coding: utf-8 -*-
"""每日知识蒸馏 - 将 SESSION/对话精华写入 MEMORY.md"""
import os, datetime, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.expanduser("~")
MEMORY_PATH = os.path.join(BASE, ".workbuddy", "knowledge", "memory", "MEMORY.md")

def distill():
    today = datetime.date.today().isoformat()
    summary = sys.argv[1] if len(sys.argv) > 1 else "本次对话未有明确学习内容记录"
    entry = "\n### %s 学习摘要\n\n%s\n" % (today, summary)
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            current = f.read()
        marker = "## 学习沉淀日志"
        if marker in current:
            idx = current.index(marker)
            current = current[:idx + len(marker)] + entry + current[idx + len(marker):]
        else:
            current += "\n## 学习沉淀日志\n" + entry
    else:
        current = "# MEMORY.md - 长期记忆\n\n## 学习沉淀日志\n" + entry
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        f.write(current)
    print("蒸馏完成：" + today)

if __name__ == "__main__":
    distill()
