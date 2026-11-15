# -*- coding: utf-8 -*-
"""AI 双向链接补写执行器 —— 默认 DRY-RUN，只有显式 --apply 才写入。

用法：
  python _apply_ai_links.py                 # 预演：只报告将改哪些文件
  python _apply_ai_links.py --apply        # 备份 + 写入（需人工确认后执行）
  python _apply_ai_links.py --verify       # 只验证已写入的区块
  python _apply_ai_links.py --rollback <备份目录>   # 从备份完整还原

安全设计：
  1. 写入前把每个待改文件的原始字节逐字节备份到 备份/AI整理_<时间戳>/
  2. 只在文末追加/替换带标记的区块，绝不改动正文前缀与 frontmatter
  3. 保留原编码（UTF-8 BOM / UTF-8 / GB18030）与换行风格
  4. 幂等：重复运行只替换标记区块，不叠加
  5. 每批 10 个文件，批后校验「原文前缀未变 + 区块存在」
  6. 任何异常立即停止，备份保留，可用 --rollback 还原
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from pathlib import Path

MAIN = Path(r"D:\以观其妙书院知识库\以观其妙书院")
IDX = MAIN / "00-索引与导航" / "AI统一索引"
PLAN = IDX / "AI-补链接计划.json"
BACKUP_ROOT = Path(r"D:\以观其妙书院知识库\备份")
BEGIN = "<!-- AI-LINKS-BEGIN -->"
END = "<!-- AI-LINKS-END -->"
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
BATCH = 10


def detect_decode(raw: bytes):
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def encode_back(text: str, enc: str) -> bytes:
    if enc == "utf-8-sig":
        return b"\xef\xbb\xbf" + text.encode("utf-8")
    if enc == "gb18030":
        return text.encode("gb18030", errors="replace")
    return text.encode("utf-8")


def load_plan():
    data = json.loads(PLAN.read_text(encoding="utf-8"))
    if "DRY-RUN" not in data.get("status", ""):
        raise RuntimeError("计划文件状态不是 DRY-RUN，拒绝执行")
    index = json.loads((IDX / "ai-index.json").read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in index["notes"]}
    return data["plan"], by_id


def make_block(nid: str, targets, by_id, date: str) -> str:
    lines = [BEGIN, f"## 🔗 AI 关联笔记（统一索引生成 · {date}）", "",
             "> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可回滚。", ""]
    for t in targets[:10]:
        if t not in by_id:
            continue
        tn = by_id[t]
        lines.append(f"- [[{tn['wikilink']}]] — {tn['title']}")
    lines += ["", END]
    return "\n".join(lines)


def targets_for(plan, nid):
    return plan.get(nid, [])


def backup_files(items, backup_dir: Path):
    manifest = []
    for nid, p in items:
        rel = p.relative_to(MAIN)
        dst = backup_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        raw = p.read_bytes()
        manifest.append({"id": nid, "path": str(p), "backup": str(dst),
                         "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    (backup_dir / "manifest.json").write_text(
        json.dumps({"created": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "purpose": "AI双向链接补写·逐字节原样备份",
                    "files": manifest}, ensure_ascii=False, indent=1), encoding="utf-8")
    return manifest


def apply(plan, by_id, do_write: bool):
    date = time.strftime("%Y-%m-%d")
    items = []
    skipped = []
    for nid in plan:
        n = by_id.get(nid)
        if not n or not targets_for(plan, nid):
            continue
        p = Path(n["path"])
        if not p.exists():
            skipped.append((nid, "文件不存在"))
            continue
        items.append((nid, p))
    print(f"待处理 {len(items):,} 篇；跳过 {len(skipped):,} 篇")
    if not do_write:
        for nid, p in items[:15]:
            print(f"  [预演] {p.relative_to(MAIN)} → {len(plan[nid])} 条链接")
        print("\nDRY-RUN 结束，未写入任何文件。确认后加 --apply 执行。")
        return

    ts = time.strftime("%Y%m%d_%H%M%S")
    backup_dir = BACKUP_ROOT / f"AI整理_{ts}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    print(f"备份目录：{backup_dir}")
    manifest = backup_files(items, backup_dir)
    print(f"已逐字节备份 {len(manifest):,} 个文件")

    changed, failed = 0, []
    for start in range(0, len(items), BATCH):
        batch = items[start:start + BATCH]
        for nid, p in batch:
            try:
                raw = p.read_bytes()
                text, enc = detect_decode(raw)
                crlf = "\r\n" in text
                norm = text.replace("\r\n", "\n")
                block = make_block(nid, plan[nid], by_id, date)
                if BLOCK_RE.search(norm):
                    new = BLOCK_RE.sub(lambda _m: block, norm)
                else:
                    new = norm.rstrip("\n") + "\n\n" + block + "\n"
                if crlf:
                    new = new.replace("\n", "\r\n")
                out = encode_back(new, enc)
                # 校验：原正文（去掉旧区块后）必须完整保留
                old_body = BLOCK_RE.sub("", norm).rstrip("\n")
                new_body = BLOCK_RE.sub("", new.replace("\r\n", "\n")).rstrip("\n")
                if old_body != new_body:
                    raise RuntimeError("正文前缀校验失败，已中止该文件")
                if BEGIN not in new:
                    raise RuntimeError("区块写入校验失败")
                p.write_bytes(out)
                changed += 1
            except Exception as e:
                failed.append((nid, str(e)))
        if failed:
            print(f"第 {start//BATCH+1} 批出现错误，立即停止。失败 {len(failed)} 篇")
            break
        if (start // BATCH) % 50 == 0:
            print(f"  进度 {min(start+BATCH, len(items)):,}/{len(items):,}")
    (backup_dir / "apply_log.json").write_text(
        json.dumps({"changed": changed, "failed": failed,
                    "backup_dir": str(backup_dir)}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(f"\n完成：已写入 {changed:,} 篇，失败 {len(failed):,} 篇")
    if failed:
        for f in failed[:10]:
            print("  失败：", f)
    print(f"回滚命令：python _apply_ai_links.py --rollback \"{backup_dir}\"")


def verify(plan, by_id):
    ok, missing, extra = 0, [], []
    for nid, n in by_id.items():
        p = Path(n["path"])
        if not p.exists():
            continue
        text = detect_decode(p.read_bytes())[0]
        has = BEGIN in text
        if has:
            ok += 1
        if nid in plan and not has:
            missing.append(nid)
        if nid not in plan and has:
            extra.append(nid)
    print(json.dumps({"含AI区块": ok, "计划内缺失": len(missing),
                      "计划外写入": len(extra)}, ensure_ascii=False, indent=2))
    print("提示：计划外写入数应为 0，否则说明有其他来源写入了同标记区块。")


def rollback(backup_dir: Path):
    man = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
    restored = 0
    for f in man["files"]:
        src, dst = Path(f["backup"]), Path(f["path"])
        if not src.exists():
            print("备份缺失，跳过：", f["path"])
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if hashlib.sha256(dst.read_bytes()).hexdigest() == f["sha256"]:
            restored += 1
        else:
            print("校验不一致：", f["path"])
    print(f"已还原 {restored:,}/{len(man['files']):,} 个文件（与备份 sha256 一致）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正写入（默认只预演）")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--rollback", type=str, default="")
    args = ap.parse_args()
    if args.rollback:
        rollback(Path(args.rollback))
        return
    plan, by_id = load_plan()
    if args.verify:
        verify(plan, by_id)
    else:
        apply(plan, by_id, args.apply)


if __name__ == "__main__":
    main()
