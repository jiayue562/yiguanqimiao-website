# -*- coding: utf-8 -*-
"""
KB-INDEX · 规范索引构建器 / 增量演化入口

在 ai-index.json（统一索引）之上构建「AI 检索唯一入口」：
  - 全库每篇分配稳定 UID（改名/移动/新增都不漂移）
  - 每篇编号文章生成全局唯一的规范编码 code
  - 裸编码（001 / 01 ...）一律进歧义表，不作为定位键
  - 关联（outlinks / inlinks）映射为 UID，供「基于文章内关联生成答案」

用法：
  python kb-reindex.py            重建统一索引 + 规范索引（新增文章/关联后跑这一条）
  python kb-reindex.py --check    只读：检测新增 md 与编码冲突，不写任何文件
  python kb-reindex.py --no-base  跳过统一索引重建，仅按现有 ai-index.json 重建规范索引
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

VAULT = Path(r"D:\以观其妙书院知识库\以观其妙书院")
OUT = VAULT / "00-索引与导航" / "AI统一索引"
BASE = OUT / "ai-index.json"
WORK = Path(os.environ.get("USERPROFILE", "")) / "WorkBuddy" / "2026-11-14-02-54-34"

UID_MAP = OUT / "uid-map.json"
CODE_MAP = OUT / "code-map.json"
KB_JSONL = OUT / "kb-index.jsonl"
KB_JSON = OUT / "kb-index.json"
REWRITE_MAP = OUT / "AI检索-引用改写映射.json"
REL_BASELINE = OUT / "AI检索-关联基线.json"

# 已物理规范化的命名：<NS>-<1~3位原始编号>[-<4位去冲突后缀>]-<标题>.md
# 第二轮纳入了 1 位 / 2 位编号文章（74 + 1360 篇），必须放宽到 \d{1,3}，
# 否则重建时这些文章会被判成「无编码」，规范码与 UID 继承链同时断掉。
# 115 篇带 -XXXX 后缀的码不能用正则猜：提取到短码会与另一篇撞码，
# 因此 code_fields 改用「按段拼候选 + physical_codes 白名单」精确判定。
NORM_RE = re.compile(r"^([A-Z][A-Z0-9]*-\d{1,3}(?:-[0-9A-F]{4})?)-")
# 未物理规范化的编号文章：<1~3位数字>-<标题>.md
RAW_CODE_RE = re.compile(r"^(\d{1,3})-")

NS_CODE = {
    "07-得到大脑同步/_发芽报告/2026-10": "FY2610",
    "07-得到大脑同步/_发芽报告/2026-11": "FY2611",
    "07-得到大脑同步/企业文化": "QYW",
    "07-得到大脑同步/回魏餐饮": "HWCY",
    "07-得到大脑同步/悟空": "WK",
    "07-得到大脑同步/AI 原生组织": "AIO",
    "05-五行人格心理学/公众号100讲/81-100讲": "WX81",
}


def ns_code(ns: str) -> str:
    if ns in NS_CODE:
        return NS_CODE[ns]
    return "NS" + hashlib.sha1(ns.encode("utf-8")).hexdigest()[:5].upper()


def sha_file(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return ""


def load_json(p: Path, default):
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def code_fields(rel: str, name: str, physical_codes: set):
    """返回 (规范码, 裸编码, 是否已物理规范化)；非编号文章返回 (None, None, False)。

    物理规范化文件名形如 <NS>-<编号>-<标题>.md 或 <NS>-<编号>-<4位HEX>-<标题>.md。
    用「前 3 段 / 前 2 段」拼候选再查白名单，而不是用正则截取：
    115 篇去冲突码带后缀，正则只截到 <NS>-<编号> 会与同命名空间的另一篇撞码。
    """
    ns = str(Path(rel).parent).replace("\\", "/")
    stem = name[:-3] if name.endswith(".md") else name
    parts = stem.split("-")
    for k in (3, 2):
        if len(parts) >= k:
            cand = "-".join(parts[:k])
            if cand in physical_codes:
                return cand, parts[1], True
    m = RAW_CODE_RE.match(name)
    if m:
        raw = m.group(1)
        # 保留原始位数：1 / 01 / 001 是不同体系，补齐成三位会人为制造冲突
        return f"{ns_code(ns)}-{raw}", raw, False
    return None, None, False


def build():
    base = load_json(BASE, None)
    if not base or "notes" not in base:
        raise SystemExit(f"统一索引不可用：{BASE}（请先跑 _build_ai_index.py）")
    notes = base["notes"]

    uid_map = load_json(UID_MAP, {"seq": 0, "by_id": {}, "by_code": {}, "by_sha": {}})
    by_id = uid_map.setdefault("by_id", {})
    by_code = uid_map.setdefault("by_code", {})
    by_sha = uid_map.setdefault("by_sha", {})
    seq = int(uid_map.get("seq", 0))
    used_uid = set(by_id.values())

    # 目录合并等路径迁移会让 ai-index 的 id、文件名规范码、正文 sha 三者同时失效，
    # 仅靠 by_id/by_code/by_sha 继承会把同一篇文章误判为新文章并重发 UID。
    # kb-merge.json 的 uid_inheritance 保存「迁移前 rel → 原 UID」，此处优先继承。
    merge = load_json(OUT / "kb-merge.json", {})
    inherited_by_rel = {x["to"]: x["uid"]
                        for x in merge.get("uid_inheritance", []) if x.get("uid")}

    physical_codes = {r["norm_code"] for r in
                      load_json(WORK / "_kb_normalize_plan.json", {}).get("renames", [])}
    if REWRITE_MAP.exists():
        physical_codes |= {r["norm_code"] for r in
                           load_json(REWRITE_MAP, {}).get("renames", [])}

    # 物理规范化的码来自文件名，固定不可变，先预留；其余编号文章的码遇到冲突加确定性后缀
    used_codes = set(physical_codes)
    collisions = []

    rows = []
    for n in notes:
        nid = n["id"]
        rel = n["rel"]
        name = Path(rel).name
        code, legacy, normalized = code_fields(rel, name, physical_codes)
        if code and not normalized:
            if code in used_codes:
                base = code
                code = f"{base}-{hashlib.sha1(rel.encode('utf-8')).hexdigest()[:4].upper()}"
                collisions.append({"rel": rel, "conflicted": base, "resolved": code})
            used_codes.add(code)
        elif code:
            used_codes.add(code)
        sha = sha_file(Path(n["path"]))

        uid = inherited_by_rel.get(rel) or by_id.get(nid)
        if not uid and code and code in by_code:
            uid = by_code[code]                      # 改名后按规范码继承
        if not uid and sha and sha in by_sha:
            uid = by_sha[sha]                        # 移动后按正文继承
        # 迁移继承的 UID 本就在 by_id.values() 里，不能被「已占用」判定误伤
        if not uid or (uid in used_uid and uid != by_id.get(nid)
                       and rel not in inherited_by_rel):
            seq += 1
            uid = f"KB-{seq:06d}"
            while uid in used_uid:
                seq += 1
                uid = f"KB-{seq:06d}"
        used_uid.add(uid)
        by_id[nid] = uid
        if code:
            by_code[code] = uid
        if sha and sha not in by_sha:
            by_sha[sha] = uid

        rows.append({
            "uid": uid, "code": code, "legacy_code": legacy,
            "physical_normalized": normalized,
            "path": n["path"], "rel": rel, "title": n.get("title", ""),
            "summary": n.get("summary", ""), "tags": n.get("tags", []),
            "layer": n.get("layer", ""), "top": n.get("top", ""),
            "namespace": str(Path(rel).parent).replace("\\", "/"),
            "wikilink": n.get("wikilink", ""), "updated": n.get("updated", ""),
            "chars": n.get("chars", 0), "sha256": sha,
            "_out": n.get("outlinks", []), "_in": n.get("inlinks", []),
            "_base_id": nid,
        })

    uid_by_base = {r["_base_id"]: r["uid"] for r in rows}
    unique, ambiguous = {}, defaultdict(list)
    for r in rows:
        if r["code"]:
            unique[r["code"]] = r["uid"]
        if r["legacy_code"]:
            ambiguous[r["legacy_code"]].append(r["uid"])

    for r in rows:
        r["outlinks"] = [uid_by_base[x] for x in r.pop("_out") if x in uid_by_base]
        r["inlinks"] = [uid_by_base[x] for x in r.pop("_in") if x in uid_by_base]
        r["related"] = sorted(set(r["outlinks"]) | set(r["inlinks"]))
        r.pop("_base_id", None)
        r["legacy_ambiguous"] = bool(r["legacy_code"] and len(ambiguous[r["legacy_code"]]) > 1)

    # ---- 写产物 ----
    OUT.mkdir(parents=True, exist_ok=True)
    with KB_JSONL.open("w", encoding="utf-8") as fh:
        for r in rows:
            flat = {k: r[k] for k in (
                "uid", "code", "legacy_code", "legacy_ambiguous", "physical_normalized",
                "path", "rel", "title", "summary", "tags", "layer", "top", "namespace",
                "wikilink", "updated", "chars", "sha256", "outlinks", "inlinks", "related")}
            fh.write(json.dumps(flat, ensure_ascii=False) + "\n")

    KB_JSON.write_text(json.dumps({
        "protocol": "index-first-v1",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vault": str(VAULT), "note_count": len(rows),
        "source_index": "ai-index.json",
        "notes": rows,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    CODE_MAP.write_text(json.dumps({
        "protocol": "index-first-v1",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rule": "唯一入口只接受 uid 或 unique.code；ambiguous 中的裸编码禁止单篇命中",
        "unique": unique,
        "ambiguous": {k: v for k, v in sorted(ambiguous.items())},
        "stats": {"unique_codes": len(unique), "ambiguous_legacy_codes": len(ambiguous),
                  "duplicate_legacy_groups": sum(1 for v in ambiguous.values() if len(v) >= 2),
                  "single_member_legacy_groups": sum(1 for v in ambiguous.values() if len(v) == 1),
                  "physical_normalized": sum(1 for r in rows if r["physical_normalized"]),
                  "collisions_resolved": len(collisions)},
        "collisions_resolved": collisions,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    UID_MAP.write_text(json.dumps(
        {"seq": seq, "by_id": by_id, "by_code": by_code, "by_sha": by_sha},
        ensure_ascii=False), encoding="utf-8")

    # 引用映射是「已物理规范化清单」的唯一真相源。
    # 第二轮会把它从 166 条扩为 1600 条；此处只允许在文件缺失时初始化，
    # 绝不能用工作区的第一轮旧计划覆盖，否则 1434 篇会失去规范码。
    plan = WORK / "_kb_normalize_plan.json"
    if plan.exists() and not REWRITE_MAP.exists():
        p = load_json(plan, {})
        REWRITE_MAP.write_text(json.dumps({
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "renames": [{"old_rel": r["old_rel"], "new_rel": r["new_rel"],
                         "old_wiki": r["old_wiki"], "new_wiki": r["new_wiki"],
                         "sha256_before": r["sha256_before"],
                         "norm_code": r["norm_code"]} for r in p.get("renames", [])],
            "rewrites": [{"rel": w["rel"], "changes": w["changes"],
                          "sha256_before": w["sha256_before"],
                          "encoding": w["encoding"], "bom": w["bom"]}
                         for w in p.get("rewrites", [])],
        }, ensure_ascii=False), encoding="utf-8")
    audit = WORK / "_kb_audit.json"
    if audit.exists() and not REL_BASELINE.exists():
        a = load_json(audit, {})
        REL_BASELINE.write_text(json.dumps({
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scope": "三位数字连载（规范化前基线）",
            "baseline": [{"legacy_code": f["code"], "rel": f["rel"],
                          "outlinks_count": f["outlinks_count"],
                          "inlinks_count": f["inlinks_count"]}
                         for f in a.get("files", []) if re.match(r"^\d{3}-", f["filename"])],
        }, ensure_ascii=False), encoding="utf-8")

    return {
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "收录笔记": len(rows),
        "分配 UID": len(used_uid),
        "唯一规范编码": len(unique),
        "歧义裸编码组": len(ambiguous),
        "物理规范化文件": sum(1 for r in rows if r["physical_normalized"]),
        "自动消解的编码冲突": len(collisions),
        "剩余规范编码冲突": sum(1 for r in rows if r["code"]) - len(unique),
        "产物": [KB_JSONL.name, KB_JSON.name, CODE_MAP.name, UID_MAP.name],
    }


def check():
    """只读：按统一索引的同一排除口径扫描磁盘，检测尚未进索引的新增 md。"""
    import importlib.util
    base = load_json(BASE, None)
    indexed = {n["rel"] for n in base["notes"]} if base else set()
    try:
        spec = importlib.util.spec_from_file_location("_kb_base_rules",
                                                     OUT / "_build_ai_index.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        is_excluded = mod.is_excluded
    except Exception:
        skip = {".obsidian", ".git", "99-归档", "WorkBuddy知识备份体系",
                ".trash", "node_modules", "AI统一索引"}
        is_excluded = lambda rel: any(part in skip for part in rel.parts)
    on_disk = set()
    for p in VAULT.rglob("*.md"):
        relp = p.relative_to(VAULT)
        if is_excluded(relp):
            continue
        on_disk.add(relp.as_posix())
    cmap = load_json(CODE_MAP, {"unique": {}})
    new_files = sorted(on_disk - indexed)
    renamed_candidates = [r for r in new_files if NORM_RE.match(Path(r).name)]
    print(json.dumps({
        "status": "CHECK · 只读",
        "磁盘 md（扫描口径）": len(on_disk),
        "统一索引收录": len(indexed),
        "尚未进索引的新增 md": len(new_files),
        "其中已带规范编码": len(renamed_candidates),
        "新增样例": new_files[:10],
        "当前唯一规范码数": len(cmap.get("unique", {})),
        "建议": "有新增时运行 python kb-reindex.py 完成演化",
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-base", action="store_true")
    a = ap.parse_args()
    if a.check:
        check()
        return
    if not a.no_base:
        script = OUT / "_build_ai_index.py"
        if not script.exists():
            raise SystemExit(f"缺少统一索引重建脚本：{script}")
        subprocess.run([sys.executable, str(script)], check=True)
    print(json.dumps(build(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
