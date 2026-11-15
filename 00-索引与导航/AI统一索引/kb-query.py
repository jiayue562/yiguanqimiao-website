# -*- coding: utf-8 -*-
"""
KB-QUERY · AI 调用本知识库的唯一入口（index-first-v1 + merge-v1）

硬约束（由本脚本强制，不靠口头约定）：
  1. 定位文章必须先经 kb-index.jsonl / code-map.json；
  2. 裸编码（001 / 01 ...）一律返回 AMBIGUOUS 候选表，绝不随机命中单篇；
  3. search 阶段只读索引，不扫描磁盘、不逐篇读取文章；
  4. 只有 uid 或唯一规范码才能取正文；取回的正文带 via=index 溯源；
  5. context 同时返回文章内的关联（outlinks / inlinks），答案须基于此生成；
  6. 字节完全相同的副本在索引层折叠：不单独命中，取正文时自动改为主本并标注；
  7. L5 归档快照默认不进常规检索；显式查询必须标注「归档快照·非现行版本」，
     不得作为现行结论的依据。

命令：
  python kb-query.py search "关键词" [--limit 10] [--layer L1] [--include-archive]
  python kb-query.py resolve <uid|规范码|裸编码>
  python kb-query.py get <uid|规范码> [--body] [--body-chars 4000]
  python kb-query.py context <uid|规范码> [--depth 1] [--max-related 8] [--body]
  python kb-query.py archive "关键词" [--limit 10] [--body]
  python kb-query.py groups
  python kb-query.py stats
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
VAULT = OUT.parents[1]
KB_JSONL = OUT / "kb-index.jsonl"
CODE_MAP = OUT / "code-map.json"
MERGE_FILE = OUT / "kb-merge.json"
ARCHIVE_FILE = OUT / "kb-archive.jsonl"

CONTRACT = (
    "AI 只能使用本输出中的 uid/path 读取原文；"
    "禁止按裸编码定位、禁止绕过索引逐篇遍历库内文件；"
    "答案须基于 context 返回的文章正文及其关联信息生成；"
    "字节相同副本已折叠，不得另行引用 duplicate_of 指向的主本以外的副本；"
    "L5 归档快照默认不进常规检索，显式查询时必须标注「归档快照·非现行版本」，"
    "且不得作为现行结论依据。"
)

MERGE = {}
ARCHIVE = None


def load_merge():
    global MERGE
    MERGE = json.loads(MERGE_FILE.read_text(encoding="utf-8")) if MERGE_FILE.exists() else {}
    return MERGE


def load_archive():
    global ARCHIVE
    if ARCHIVE is None:
        ARCHIVE = []
        if ARCHIVE_FILE.exists():
            with ARCHIVE_FILE.open(encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        ARCHIVE.append(json.loads(line))
    return ARCHIVE


def envelope(command, ok, result, **extra):
    out = {
        "protocol": "index-first-v1 + merge-v1" if MERGE else "index-first-v1",
        "entry": "kb-query.py",
        "index": KB_JSONL.name,
        "command": command,
        "ok": ok,
        "result": result,
        "contract": CONTRACT,
    }
    if MERGE:
        out["merge_policy"] = {
            "duplicate_folding": MERGE.get("policy", {}).get("duplicate_folding", ""),
            "archive": MERGE.get("archive_layer", {}).get("policy", ""),
        }
    out.update(extra)
    return out


def load_index():
    if not KB_JSONL.exists():
        raise SystemExit("规范索引不存在，请先运行：python kb-reindex.py")
    rows = []
    with KB_JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_codes():
    if not CODE_MAP.exists():
        raise SystemExit("编码映射不存在，请先运行：python kb-reindex.py")
    return json.loads(CODE_MAP.read_text(encoding="utf-8"))


def brief(r):
    b = {k: r.get(k) for k in (
        "uid", "code", "legacy_code", "path", "rel", "title", "layer",
        "namespace", "summary", "related")}
    dup = MERGE.get("duplicate_of", {})
    if r.get("rel") in dup:
        b["duplicate_of"] = dup[r["rel"]]
    return b


def canonicalize(r, rows):
    """副本 → 主本。返回 (row, folding_meta|None)。"""
    dup = MERGE.get("duplicate_of", {})
    target = dup.get(r.get("rel"))
    if not target:
        return r, None
    cand = next((x for x in rows if x["rel"] == target), None)
    if not cand:
        return r, None
    return cand, {"folded_from": r["uid"], "folded_from_rel": r["rel"],
                  "canonical": target,
                  "reason": "字节完全相同的副本，按 merge-v1 折叠到主本，避免重复引用"}


def resolve_token(token, rows, codes):
    """返回 (kind, payload)。kind: single / ambiguous / not_found"""
    by_uid = {r["uid"]: r for r in rows}
    unique = codes.get("unique", {})
    ambiguous = codes.get("ambiguous", {})

    if token in by_uid:
        return "single", by_uid[token]
    if token in unique:
        r = by_uid.get(unique[token])
        if r:
            return "single", r
    if token in ambiguous:
        cands = [brief(by_uid[u]) for u in ambiguous[token] if u in by_uid]
        return "ambiguous", cands
    return "not_found", None


def cmd_resolve(args, rows, codes):
    kind, payload = resolve_token(args.token, rows, codes)
    if kind == "single":
        canon, fold = canonicalize(payload, rows)
        return envelope("resolve", True, {
            "status": "UNIQUE", "match": brief(payload),
            "folding": fold,
            "hint": ("该条目为副本，请使用 canonical 再调用 get / context" if fold
                     else "可用 get / context 继续取正文与关联")}, resolved_uid=payload["uid"])
    if kind == "ambiguous":
        return envelope("resolve", True, {
            "status": "AMBIGUOUS",
            "reject_single": True,
            "reason": f"裸编码 {args.token!r} 对应 {len(payload)} 篇文章，禁止单篇命中",
            "candidates": payload,
            "hint": "请改用候选中的 code（唯一规范码）或 uid 再调用 resolve"},
            resolved_uid=None)
    return envelope("resolve", False, {
        "status": "NOT_FOUND", "token": args.token,
        "hint": "索引中无此 uid / 规范码；请用 search 先定位"}, resolved_uid=None)


def score(r, q):
    s = 0
    title = (r.get("title") or "").lower()
    code = (r.get("code") or "").lower()
    summary = (r.get("summary") or "").lower()
    rel = (r.get("rel") or "").lower()
    ns = (r.get("namespace") or "").lower()
    tags = " ".join(r.get("tags") or []).lower()
    if q == code:
        s += 100
    if q in title:
        s += 30
    if q in code:
        s += 25
    if q in tags:
        s += 15
    if q in ns:
        s += 8
    if q in rel:
        s += 6
    if q in summary:
        s += 4
    return s


def cmd_search(args, rows, codes):
    q = args.query.strip().lower()
    if not q:
        return envelope("search", False, {"status": "EMPTY_QUERY"})
    dup = MERGE.get("duplicate_of", {})
    copies = {g["canonical"]: g["copies"]
              for g in MERGE.get("duplicate_groups", [])}
    hits, folded = [], 0
    for r in rows:
        if r["rel"] in dup:
            folded += 1
            continue
        if args.layer and not (r.get("layer") or "").startswith(args.layer):
            continue
        s = score(r, q)
        if s > 0:
            b = brief(r)
            b["score"] = s
            b["related_count"] = len(r.get("related") or [])
            if r["rel"] in copies:
                b["copies"] = len(copies[r["rel"]])
            hits.append(b)
    hits.sort(key=lambda x: (-x["score"], x["rel"]))

    archive_hits = []
    if args.include_archive:
        for a in load_archive():
            if q in a["rel"].lower():
                archive_hits.append({
                    "rel": a["rel"], "layer": "L5-归档快照·非现行版本",
                    "score": 0, "archive_only": True,
                    "current_twin": a.get("current_twin"),
                    "version_note": "归档快照·非现行版本，不得作为现行结论依据"})
    # 归档结果单独给配额，不与常规命中争抢 limit；否则显式查询也可能返回 0 条
    return envelope("search", True, {
        "status": "OK", "query": args.query, "total_hits": len(hits),
        "returned": len(hits[:args.limit]), "hits": hits[:args.limit],
        "folded_duplicates": folded,
        "archive_layer": ({"included": args.include_archive,
                           "count": len(load_archive()),
                           "returned": len(archive_hits[:args.limit]),
                           "hits": archive_hits[:args.limit],
                           "version_note": "归档快照·非现行版本，不得作为现行结论依据"}
                          if args.include_archive else
                          {"included": False, "count": len(load_archive()),
                           "hint": "显式 --include-archive 或 archive 子命令才可查归档快照"}),
        "note": "本阶段仅检索索引，未读取任何文章正文"},
        resolved_uid=None)


def read_body(r, limit):
    p = Path(r["path"])
    if not p.exists():
        return {"available": False, "reason": "索引指向的文件不存在"}
    try:
        txt = p.read_bytes().decode("utf-8-sig", errors="replace")
    except OSError as e:
        return {"available": False, "reason": str(e)}
    truncated = len(txt) > limit
    return {"available": True, "chars_total": len(txt), "truncated": truncated,
            "text": txt[:limit], "via": "index", "source_uid": r.get("uid")}


def cmd_get(args, rows, codes):
    kind, payload = resolve_token(args.token, rows, codes)
    if kind != "single":
        return envelope("get", False, {
            "status": "REJECTED",
            "reason": "get 只接受 uid 或唯一规范码；裸编码请先 resolve 查看候选",
            "resolve_status": kind})
    canon, fold = canonicalize(payload, rows)
    out = brief(canon)
    if args.body:
        out["body"] = read_body(canon, args.body_chars)
    return envelope("get", True, {
        "status": "OK", "article": out, "folding": fold,
        "hint": "若 folding 非空，正文来自主本；请勿另行引用副本"},
        resolved_uid=canon["uid"])


def cmd_context(args, rows, codes):
    kind, payload = resolve_token(args.token, rows, codes)
    if kind != "single":
        return envelope("context", False, {
            "status": "REJECTED",
            "reason": "context 只接受 uid 或唯一规范码；裸编码请先 resolve 查看候选",
            "resolve_status": kind})
    canon, fold = canonicalize(payload, rows)
    by_uid = {r["uid"]: r for r in rows}
    main = canon
    outs = set(main.get("outlinks") or [])
    ins = set(main.get("inlinks") or [])
    rel_ids = list(dict.fromkeys(list(outs) + list(ins)))[:args.max_related]

    main_art = {k: v for k, v in brief(main).items() if k != "related"}
    main_art["relation"] = "main"
    articles, seen_uid, rel_arts, folded_related = [main_art], {main["uid"]}, [], 0
    for u in rel_ids:
        r = by_uid.get(u)
        if not r:
            continue
        r2, f2 = canonicalize(r, rows)
        if f2:
            folded_related += 1
        if r2["uid"] in seen_uid:
            continue
        seen_uid.add(r2["uid"])
        a = {k: v for k, v in brief(r2).items() if k != "related"}
        a["relation"] = "both" if (u in outs and u in ins) else (
            "outlink" if u in outs else "inlink")
        articles.append(a)
        rel_arts.append((a, r2))

    if args.body:
        main_art["body"] = read_body(main, args.body_chars)
        for a, r2 in rel_arts:
            a["body"] = read_body(r2, min(args.body_chars, 2500))

    return envelope("context", True, {
        "status": "OK",
        "main": brief(main),
        "folding": fold,
        "folded_related_duplicates": folded_related,
        "relation_counts": {"outlinks": len(outs), "inlinks": len(ins),
                            "returned_related": len(rel_arts)},
        "articles": articles,
        "answer_rule": "答案须基于 articles 中的正文与 relation 字段组织；"
                       "不得引用未出现在 articles 中的文章，不得另行遍历库内文件；"
                       "不得把折叠掉的副本当作独立证据。",
    }, resolved_uid=main["uid"])


def cmd_archive(args, rows, codes):
    """L5 归档快照显式查询：必须标注版本性质，不得作为现行结论依据。"""
    q = args.query.strip().lower()
    if not q:
        return envelope("archive", False, {"status": "EMPTY_QUERY"})
    all_items = [a for a in load_archive() if q in a["rel"].lower()]
    items = []
    for a in all_items[:args.limit]:
        item = dict(a)
        item["version_note"] = "归档快照·非现行版本，不得作为现行结论依据"
        if args.body:
            item["body"] = read_body(
                {"path": str(VAULT / a["rel"]), "uid": "ARCHIVE/" + a["rel"]},
                args.body_chars)
        items.append(item)
    return envelope("archive", True, {
        "status": "OK", "query": args.query,
        "total_hits": len(all_items), "returned": len(items), "items": items,
        "answer_rule": "这些是排除在常规检索之外的历史快照；"
                       "若 current_twin 非空，应优先以该现行版本为依据；"
                       "引用时必须显式标注「归档快照·非现行版本」。",
    }, resolved_uid=None)


def cmd_groups(args, rows, codes):
    return envelope("groups", True, {
        "status": "OK",
        "directory_groups": MERGE.get("directory_groups", {}),
        "unnumbered_tops": MERGE.get("unnumbered_tops", []),
        "merged_pairs": MERGE.get("merged_pairs", []),
        "root_navigation": MERGE.get("root_navigation", []),
        "archive_layer": MERGE.get("archive_layer", {}),
        "duplicate_groups_count": len(MERGE.get("duplicate_groups", [])),
        "hint": "语义同类目录仅为名称相近，实测文件交集为 0；按主题一次找全即可，勿据此物理合并",
    }, resolved_uid=None)


def cmd_stats(args, rows, codes):
    layers = {}
    for r in rows:
        layers[r.get("layer", "")] = layers.get(r.get("layer", ""), 0) + 1
    return envelope("stats", True, {
        "notes": len(rows),
        "unique_codes": len(codes.get("unique", {})),
        "ambiguous_legacy_codes": len(codes.get("ambiguous", {})),
        "physical_normalized": sum(1 for r in rows if r.get("physical_normalized")),
        "layers": layers,
        "duplicate_groups": len(MERGE.get("duplicate_groups", [])),
        "folded_copies": len(MERGE.get("duplicate_of", {})),
        "archive_snapshots": len(load_archive()),
        "path_migrations": len(MERGE.get("path_migrations", [])),
        "uid_inheritance": len(MERGE.get("uid_inheritance", [])),
        "generated": codes.get("generated", ""),
    })


def main():
    ap = argparse.ArgumentParser(description="AI 调用知识库的唯一入口")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--layer", default="")
    p.add_argument("--include-archive", action="store_true")

    p = sub.add_parser("resolve")
    p.add_argument("token")

    p = sub.add_parser("get")
    p.add_argument("token")
    p.add_argument("--body", action="store_true")
    p.add_argument("--body-chars", type=int, default=4000)

    p = sub.add_parser("context")
    p.add_argument("token")
    p.add_argument("--depth", type=int, default=1)
    p.add_argument("--max-related", type=int, default=8)
    p.add_argument("--body", action="store_true")
    p.add_argument("--body-chars", type=int, default=4000)

    p = sub.add_parser("archive")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--body", action="store_true")
    p.add_argument("--body-chars", type=int, default=2000)

    sub.add_parser("groups")
    sub.add_parser("stats")

    args = ap.parse_args()
    load_merge()
    rows = load_index()
    codes = load_codes()
    fn = {"search": cmd_search, "resolve": cmd_resolve, "get": cmd_get,
          "context": cmd_context, "archive": cmd_archive,
          "groups": cmd_groups, "stats": cmd_stats}[args.cmd]
    print(json.dumps(fn(args, rows, codes), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
