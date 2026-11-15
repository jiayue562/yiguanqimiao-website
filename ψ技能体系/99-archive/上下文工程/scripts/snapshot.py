# -*- coding: utf-8 -*-
"""上下文快照生成器"""
import os, sys
from pathlib import Path
from datetime import datetime

BASE = Path.home() / ".agents" / "skills" / "上下文工程"
SNAPSHOT_DIR = BASE / "snapshots"
INDEX_FILE = SNAPSHOT_DIR / "_snapshot-index.md"

def ensure_dirs():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def generate_snapshot(project, completed, decisions, todos, context_items):
    """生成上下文快照"""
    ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"context-{ts}.md"
    p = SNAPSHOT_DIR / fn
    cm = "\n".join(f"- [x] {i}" for i in (completed or ["无"]))
    tm = "\n".join(f"- [ ] {i}" for i in (todos or ["无"]))
    dm = "\n".join(f"- {d}" for d in (decisions or ["无"]))
    cxm = "\n".join(f"- {c}" for c in (context_items or ["无"]))
    # build content safely
    cl = ["---", f"type: context-snapshot", f'project: "{project}"', f"timestamp: {datetime.now().isoformat()}", "---", "", f"# 上下文快照: {project}", "", "## 已完成事项", cm, "", "## 关键决策", dm, "", "## 待办事项", tm, "", "## 关键上下文", cxm, "", "---", ""]
    content = "\n".join(cl)
    dts = datetime.now().strftime('%Y-%m-%d %H:%M')
    content += "_\u751f\u6210: " + dts + "_\n"
    p.write_text(content, encoding="utf-8")
    print(f"[OK] {fn}")
    update_index(project, fn, ts)
    return p

def update_index(project, fn, ts):
    ensure_dirs()
    e = f"| {ts} | {project} | [[{fn}]] | \u8fdb\u884c\u4e2d |\n"
    c = ""
    if INDEX_FILE.exists():
        c = INDEX_FILE.read_text(encoding="utf-8")
    else:
        h = "# \u4e0a\u4e0b\u6587\u5feb\u7167\u7d22\u5f15"
        h += "\n\n| \u65f6\u95f4 | \u9879\u76ee | \u6587\u4ef6 | \u72b6\u6001 |"
        h += "\n|------|------|------|------|\n"
        c = h
    c += e
    INDEX_FILE.write_text(c, encoding="utf-8")

def list_snapshots(project=None):
    ensure_dirs()
    ss = sorted(SNAPSHOT_DIR.glob("context-*.md"), reverse=True)
    if project:
        ss = [s for s in ss if project.lower() in s.read_text(encoding="utf-8").lower()]
    return ss

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        for s in list_snapshots():
            print(f"  {s.name}")
    elif cmd == "generate" and len(sys.argv) > 2:
        generate_snapshot(sys.argv[2], [], [], [], [])