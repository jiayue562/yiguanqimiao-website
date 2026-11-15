# -*- coding: utf-8 -*-
"""同名目录融合执行器：复制（不移动、不覆盖）+ 冲突两版并存互链

  python _apply_fusion.py            # 预演
  python _apply_fusion.py --apply    # 执行
  python _apply_fusion.py --verify   # 验证
  python _apply_fusion.py --rollback <manifest目录>  # 把新增文件移回归档（不删除）

零数据丢失保证：
  - 原副库/研学库文件全部保留不动；
  - 主库既有文件一篇不覆盖、不修改；
  - 961 个同名但内容不同的文件，副库版另存到 99-并入冲突存档/ 并链接回主库版。
"""
import argparse
import csv
import hashlib
import json
import shutil
import stat
import time
from pathlib import Path

BASE = Path(r"D:\以观其妙书院知识库")
MAIN = BASE / "以观其妙书院"
IDX = MAIN / "00-索引与导航" / "AI统一索引"
ARCHIVE = MAIN / "99-并入冲突存档"
BACKUP_ROOT = BASE / "备份"
FB, FE = "<!-- FUSION-LINK-BEGIN -->", "<!-- FUSION-LINK-END -->"


def detect(raw):
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def enc_back(text, enc):
    if enc == "utf-8-sig":
        return b"\xef\xbb\xbf" + text.encode("utf-8")
    if enc == "gb18030":
        return text.encode("gb18030", errors="replace")
    return text.encode("utf-8")


def read_csv(name):
    with (IDX / name).open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def append_link(p: Path, rel: str):
    raw = p.read_bytes()
    text, enc = detect(raw)
    crlf = "\r\n" in text
    norm = text.replace("\r\n", "\n")
    wiki = rel[:-3] if rel.endswith(".md") else rel
    block = "\n".join([
        FB, "## 🔗 同名版本对照（融合时生成）", "",
        "> 本文件是副库/研学库版本；主库另有同名现行版本，**两版内容不同，均未覆盖**。",
        f"- 主库现行版本：[[{wiki}|主库现行版本]]", "", FE])
    if FB in norm:
        import re
        norm = re.sub(re.escape(FB) + r".*?" + re.escape(FE),
                      lambda _m: block, norm, flags=re.S)
    else:
        norm = norm.rstrip("\n") + "\n\n" + block + "\n"
    new = norm.replace("\n", "\r\n") if crlf else norm
    mode0 = p.stat().st_mode
    ro = not (mode0 & stat.S_IWRITE)
    if ro:
        p.chmod(mode0 | stat.S_IWRITE)
    try:
        p.write_bytes(enc_back(new, enc))
    finally:
        if ro:
            p.chmod(p.stat().st_mode & ~stat.S_IWRITE)


def apply(do_write):
    direct = read_csv("AI-融合直迁清单.csv")
    conflict = read_csv("AI-融合冲突清单.csv")
    print(f"直迁 {len(direct):,} 篇 / 冲突存档 {len(conflict):,} 篇")
    if not do_write:
        print("DRY-RUN：未复制任何文件。确认后加 --apply。")
        return
    ts = time.strftime("%Y%m%d_%H%M%S")
    man_dir = BACKUP_ROOT / f"AI融合_manifest_{ts}"
    man_dir.mkdir(parents=True, exist_ok=False)
    created = []
    errors = []

    for r in direct:
        src, dst = Path(r["源路径"]), Path(r["目标路径(主库)"])
        if dst.exists():
            errors.append((str(dst), "目标已存在，跳过（不覆盖）"))
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        created.append(str(dst))

    for r in conflict:
        rel = r["相对路径"]
        src, dst = Path(r["副库文件(不动)"]), ARCHIVE / rel
        if dst.exists():
            errors.append((str(dst), "存档目标已存在，跳过"))
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        try:
            append_link(dst, rel)
        except Exception as e:
            errors.append((str(dst), "追加对照链接失败：" + str(e)))
        created.append(str(dst))

    (man_dir / "manifest.json").write_text(json.dumps({
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": "同名目录融合 · 本次新建文件清单（回滚时移走，不删除）",
        "direct": len(direct), "conflict": len(conflict),
        "created_files": created, "errors": errors}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(f"新建文件 {len(created):,} 个；异常 {len(errors):,} 个")
    for e in errors[:10]:
        print("  ", e)
    print(f"回滚：python _apply_fusion.py --rollback \"{man_dir}\"")
    return {"created": len(created), "errors": len(errors), "manifest": str(man_dir)}


def verify():
    direct = read_csv("AI-融合直迁清单.csv")
    conflict = read_csv("AI-融合冲突清单.csv")
    ok1 = sum(1 for r in direct if Path(r["目标路径(主库)"]).exists())
    ok2 = sum(1 for r in conflict if (ARCHIVE / r["相对路径"]).exists())
    linked = sum(1 for r in conflict
                 if (ARCHIVE / r["相对路径"]).exists() and
                 FB in detect((ARCHIVE / r["相对路径"]).read_bytes())[0])
    print(json.dumps({"直迁就位": f"{ok1}/{len(direct)}",
                      "冲突存档就位": f"{ok2}/{len(conflict)}",
                      "含对照链接": linked}, ensure_ascii=False, indent=2))


def rollback(man_dir: Path):
    data = json.loads((man_dir / "manifest.json").read_text(encoding="utf-8"))
    ts = time.strftime("%Y%m%d_%H%M%S")
    dest = BACKUP_ROOT / f"AI融合_回滚_{ts}"
    n = 0
    for s in data["created_files"]:
        p = Path(s)
        if not p.exists():
            continue
        target = dest / p.relative_to(MAIN)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(target))
        n += 1
    print(f"已把 {n:,} 个新增文件移回 {dest}（原副库/研学库文件从未变动）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--rollback", default="")
    a = ap.parse_args()
    if a.rollback:
        rollback(Path(a.rollback))
    elif a.verify:
        verify()
    else:
        apply(a.apply)


if __name__ == "__main__":
    main()
