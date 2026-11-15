# -*- coding: utf-8 -*-
"""阶段 B 统一执行器：备份 → 链接规范化 → 追加双向链接区块 → 校验 → 回滚能力

默认 DRY-RUN。只有 --apply 才写入。
  python _apply_all.py                     # 预演
  python _apply_all.py --apply            # 执行（已获悟空授权）
  python _apply_all.py --verify           # 验证写入结果
  python _apply_all.py --rollback <目录>   # 从逐字节备份还原
"""
import argparse
import hashlib
import json
import re
import shutil
import stat
import time
from pathlib import Path

MAIN = Path(r"D:\以观其妙书院知识库\以观其妙书院")
IDX = MAIN / "00-索引与导航" / "AI统一索引"
PLAN = IDX / "AI-补链接计划.json"
RELINK = Path(r"C:\Users\jia'yue\WorkBuddy\2026-11-14-02-54-34\relink_map.json")
BACKUP_ROOT = Path(r"D:\以观其妙书院知识库\备份")
WORK = Path(r"C:\Users\jia'yue\WorkBuddy\2026-11-14-02-54-34")
BEGIN, END = "<!-- AI-LINKS-BEGIN -->", "<!-- AI-LINKS-END -->"
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
BATCH = 10


def detect(raw: bytes):
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def enc_back(text: str, enc: str) -> bytes:
    if enc == "utf-8-sig":
        return b"\xef\xbb\xbf" + text.encode("utf-8")
    if enc == "gb18030":
        return text.encode("gb18030", errors="replace")
    return text.encode("utf-8")


def strip_noise(s: str) -> str:
    s = BLOCK_RE.sub("", s)
    s = re.sub(r"\[\[[^\]]*\]\]", "", s)
    return re.sub(r"\s+", "", s)


def load():
    plandata = json.loads(PLAN.read_text(encoding="utf-8"))
    if "DRY-RUN" not in plandata.get("status", ""):
        raise RuntimeError("计划状态不是 DRY-RUN，拒绝执行")
    index = json.loads((IDX / "ai-index.json").read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in index["notes"]}
    rel = json.loads(RELINK.read_text(encoding="utf-8"))["map"]
    # 本轮只处理主库：副库/研学库的链接要等合并进同一 vault 后重写才有意义
    rel = {k: v for k, v in rel.items() if k.startswith("主库/")}
    return plandata["plan"], by_id, rel


def make_block(nid, targets, by_id, date):
    lines = [BEGIN, f"## 🔗 AI 关联笔记（统一索引生成 · {date}）", "",
             "> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。", ""]
    for t in targets[:10]:
        if t in by_id:
            lines.append(f"- [[{by_id[t]['wikilink']}]] — {by_id[t]['title']}")
    lines += ["", END]
    return "\n".join(lines)


def relink_text(text: str, mapping: dict):
    n = 0
    for old, new in mapping.items():
        pat = re.compile(r"\[\[\s*" + re.escape(old) +
                         r"\s*(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
        text, k = pat.subn(lambda _m, v=new: v, text)
        n += k
    return text, n


def affected_items(plan, relink, by_id):
    ids = set(plan) | set(relink)
    items, skip = [], []
    for nid in sorted(ids):
        n = by_id.get(nid)
        if not n:
            skip.append((nid, "索引中无此条目"))
            continue
        p = Path(n["path"])
        if not p.exists():
            skip.append((nid, "文件不存在"))
            continue
        items.append((nid, p))
    return items, skip


def backup(items, bdir: Path):
    man = []
    fdir = bdir / "files"
    fdir.mkdir(parents=True, exist_ok=True)
    for nid, p in items:
        # 用 id 哈希做备份文件名，规避超长路径 / 特殊字符 / 跨库相对路径问题
        dst = fdir / (hashlib.sha256(nid.encode("utf-8")).hexdigest()[:20] + ".orig")
        shutil.copy2(p, dst)
        raw = p.read_bytes()
        man.append({"id": nid, "path": str(p), "backup": str(dst),
                    "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    (bdir / "manifest.json").write_text(json.dumps({
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "purpose": "阶段B：补双向链接 + 目录型链接规范化 · 逐字节原样备份",
        "files": man}, ensure_ascii=False, indent=1), encoding="utf-8")
    return man


def apply(plan, by_id, relink, do_write, keep_blocks=False):
    items, skip = affected_items(plan, relink, by_id)
    print(f"受影响文件 {len(items):,} 个（补链接 {len(plan):,} + 链接规范化 {len(relink):,} 去重后）"
          f"；跳过 {len(skip):,}")
    if not do_write:
        print("DRY-RUN：未写入任何文件。确认后加 --apply。")
        return
    ts = time.strftime("%Y%m%d_%H%M%S")
    bdir = BACKUP_ROOT / f"AI整理_全量_{ts}"
    bdir.mkdir(parents=True, exist_ok=False)
    man = backup(items, bdir)
    print(f"备份完成：{bdir}（{len(man):,} 个文件，逐字节 + sha256）")

    date = time.strftime("%Y-%m-%d")
    changed = relinked = 0
    failed = []
    for start in range(0, len(items), BATCH):
        for nid, p in items[start:start + BATCH]:
            try:
                raw = p.read_bytes()
                text, enc = detect(raw)
                crlf = "\r\n" in text
                norm = text.replace("\r\n", "\n")
                before_noise = strip_noise(norm)
                norm_orig = norm
                if nid in relink:
                    norm, k = relink_text(norm, relink[nid])
                    relinked += k
                if nid in plan and plan[nid]:
                    if keep_blocks and BEGIN in norm:
                        pass  # 增量模式：保留第一轮已写好的区块，不替换
                    else:
                        block = make_block(nid, plan[nid], by_id, date)
                        norm = (BLOCK_RE.sub(lambda _m: block, norm)
                                if BLOCK_RE.search(norm)
                                else norm.rstrip("\n") + "\n\n" + block + "\n")
                if norm == norm_orig:
                    continue  # 无任何变化，不触碰文件 mtime
                if strip_noise(norm) != before_noise:
                    raise RuntimeError("非链接正文发生变化，拒绝写入")
                if nid in plan and plan[nid] and norm.count(BEGIN) != 1:
                    raise RuntimeError("AI 区块标记异常")
                new = norm.replace("\n", "\r\n") if crlf else norm
                # 味藏 references 下 8 个文件被设为只读：临时解除写入后立即恢复保护属性
                mode0 = p.stat().st_mode
                was_ro = not (mode0 & stat.S_IWRITE)
                if was_ro:
                    p.chmod(mode0 | stat.S_IWRITE)
                try:
                    p.write_bytes(enc_back(new, enc))
                finally:
                    if was_ro:
                        p.chmod(p.stat().st_mode & ~stat.S_IWRITE)
                # 回读校验
                back = detect(p.read_bytes())[0].replace("\r\n", "\n")
                if strip_noise(back) != before_noise:
                    raise RuntimeError("回读校验失败")
                changed += 1
            except Exception as e:
                failed.append((nid, str(e)))
        if failed:
            print(f"第 {start // BATCH + 1} 批出错，立即停止。失败 {len(failed)} 个")
            break
        if (start // BATCH) % 100 == 0:
            print(f"  进度 {min(start + BATCH, len(items)):,}/{len(items):,}")
    (bdir / "apply_log.json").write_text(json.dumps({
        "changed": changed, "relink_replacements": relinked,
        "failed": failed, "backup_dir": str(bdir)}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    print(f"\n完成：写入 {changed:,} 个文件；链接替换 {relinked:,} 处；失败 {len(failed):,}")
    for f in failed[:10]:
        print("  失败：", f)
    print(f"回滚：python _apply_all.py --rollback \"{bdir}\"")
    return {"changed": changed, "relinked": relinked, "failed": len(failed),
            "backup": str(bdir), "ts": time.strftime("%Y-%m-%d %H:%M:%S")}


def verify(plan, by_id):
    ok = miss = extra = 0
    for nid, n in by_id.items():
        p = Path(n["path"])
        if not p.exists():
            continue
        has = BEGIN in detect(p.read_bytes())[0]
        if has:
            ok += 1
        if nid in plan and plan[nid] and not has:
            miss += 1
        if nid not in plan and has:
            extra += 1
    print(json.dumps({"含AI区块": ok, "计划内缺失": miss, "计划外写入": extra},
                     ensure_ascii=False, indent=2))


def rollback(bdir: Path):
    man = json.loads((bdir / "manifest.json").read_text(encoding="utf-8"))
    ok = 0
    for f in man["files"]:
        src, dst = Path(f["backup"]), Path(f["path"])
        if not src.exists():
            print("备份缺失：", f["path"])
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if hashlib.sha256(dst.read_bytes()).hexdigest() == f["sha256"]:
            ok += 1
        else:
            print("sha256 不一致：", f["path"])
    print(f"已还原 {ok:,}/{len(man['files']):,} 个文件")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--rollback", default="")
    ap.add_argument("--keep-blocks", action="store_true",
                    help="保留已有 AI 区块，只给尚无区块的笔记补链（增量模式）")
    a = ap.parse_args()
    if a.rollback:
        rollback(Path(a.rollback))
        return
    plan, by_id, relink = load()
    if a.verify:
        verify(plan, by_id)
        return
    result = apply(plan, by_id, relink, a.apply, a.keep_blocks)
    if result and result.get("changed") and not a.keep_blocks:
        (IDX / "AI-补链接执行报告.md").write_text("\n".join([
            "# AI 补链接 · 执行报告", "",
            f"- 执行时间：{result['ts']}",
            f"- 写入文件：**{result['changed']:,}** 篇（主库 L1 正式知识笔记）",
            f"- 新增双向链接区块：对应 `AI-补链接计划.json` 中 {len(plan):,} 篇计划",
            f"- 目录型链接规范化替换：**{result['relinked']:,}** 处（2,410 条目录型链接）",
            f"- 失败：{result['failed']:,} 个",
            f"- 逐字节备份：`{result['backup']}`（含 manifest.json + sha256）",
            f"- 回滚：`python _apply_all.py --rollback \"{result['backup']}\"`", "",
            "## 改动范围说明", "",
            "- 仅在文末追加/替换 `<!-- AI-LINKS-BEGIN/END -->` 区块；正文与 frontmatter 未被改动。",
            "- 链接替换仅针对已判定为「目录型」的 `[[目录名]]`，改为指向目录索引页或统一总索引。",
            "- 13,962 条真缺失（多为旧索引示例链接与历史改名文件）与 344 条跨库目标**未改动**，"
            "保留在 `AI-断链清单.csv` 等待人工裁决 / 合并后重写。",
            "- 副库与研学库文件未移动、未修改。", "",
            "## 验证", "", "运行 `python _apply_all.py --verify` 检查区块覆盖率与越界写入。", "",
        ]) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
