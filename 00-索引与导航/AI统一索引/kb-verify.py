# -*- coding: utf-8 -*-
"""
KB-VERIFY v3 · 「索引优先 + 两层编号字面零重复 + 合并同类项」独立验证器

只读、可重复运行。产出：
  AI检索-验证结果.json   机器可读
  AI检索-验证报告.md     人类可读

v2 相对 v1：V5 正向重建、V6 Obsidian 解析口径、V8 关联字段完备性、V10/V11、UID 锚点。
v3 相对 v2（合并同类项 B 档后）：
  - 历史复验基线不再被钉死在旧路径：V4/V5/V6 通过 kb-merge.json 的 path_migrations
    把第二轮 rel 映射到当前路径；V5 追加「本轮链接改写」第二阶段正向重建；
  - V6 判定链接目标时同时接受迁移后的目标，避免把「已随目录迁移的链接」误报断链；
  - V11 同时校验两代备份与回滚脚本；
  - 新增 V12：重复组折叠、L5 归档层默认/显式行为、目录合并落位、UID 继承一致性。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

OUT = Path(__file__).resolve().parent
VAULT = OUT.parent.parent
KB_JSONL = OUT / "kb-index.jsonl"
CODE_MAP = OUT / "code-map.json"
REWRITE_MAP = OUT / "AI检索-引用改写映射.json"
MERGE_FILE = OUT / "kb-merge.json"
MERGE_REWRITE = OUT / "AI检索-合并同类项-改写映射.json"
ARCHIVE_FILE = OUT / "kb-archive.jsonl"
KB_QUERY = OUT / "kb-query.py"
REPORT_MD = OUT / "AI检索-验证报告.md"
REPORT_JSON = OUT / "AI检索-验证结果.json"
BODY_CHECK = OUT / "AI检索-正文校验.json"
BACKUP_ROOT = VAULT.parent / "备份"

WIKI_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
CODE_RE = re.compile(r"^(\d{1,3})-")
UID_ANCHOR = ("FY2610-001", "KB-002587")   # 第一轮确立、跨多轮演化不得漂移
EXCLUDED_ARCHIVES = {"99-归档", "WorkBuddy知识备份体系", "备份",
                     ".obsidian", ".git", ".trash", ".smart-env", ".claude",
                     ".codebuddy", ".cursor", ".github", ".workbuddy",
                     "node_modules", "__pycache__"}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def load_optional(p: Path, default):
    return load(p) if p.exists() else default


def rows():
    out = []
    with KB_JSONL.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
    return out


def run_query(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(KB_QUERY), *args],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        return {"_error": r.stderr[-500:]}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"_error": "输出非 JSON", "_raw": r.stdout[-300:]}


def find_backup():
    """取最近一个正文校验 PASS 的全量规范化备份，作为 V5 的原始字节来源。"""
    if not BACKUP_ROOT.exists():
        return None
    for d in sorted(BACKUP_ROOT.glob("索引优先_全量规范化_*"), reverse=True):
        log = d / "apply_log.json"
        if log.exists() and (d / "manifest.json").exists():
            try:
                if load(log).get("正文还原校验") == "PASS":
                    return d
            except (json.JSONDecodeError, OSError):
                continue
    return None


def find_merge_backup():
    """本轮合并同类项的 PASS 备份（含 rollback.py）。"""
    if not BACKUP_ROOT.exists():
        return None
    for d in sorted(BACKUP_ROOT.glob("合并同类项_物理整理_*"), reverse=True):
        log = d / "apply_log.json"
        if log.exists() and (d / "rollback.py").exists() and (d / "manifest.json").exists():
            try:
                if not load(log).get("stats", {}).get("errors"):
                    return d
            except (json.JSONDecodeError, OSError):
                continue
    return None


def main():
    R = rows()
    CM = load(CODE_MAP)
    MP = load_optional(REWRITE_MAP, {"renames": [], "rewrites": []})
    MG = load_optional(MERGE_FILE, {})
    MR = load_optional(MERGE_REWRITE, {})
    checks = []

    def add(name, ok, detail, critical=True):
        checks.append({"检查项": name, "结果": "PASS" if ok else "FAIL",
                       "关键": critical, "明细": detail})

    md_paths = [p for p in VAULT.rglob("*.md")]
    disk_stems = {p.stem for p in md_paths}
    disk_rels = {p.relative_to(VAULT).with_suffix("").as_posix() for p in md_paths}
    top_dirs = {p.name for p in VAULT.iterdir() if p.is_dir()}
    by_rel_rows = {r["rel"]: r for r in R}

    # ---- 迁移映射：让第二轮历史基线能在当前磁盘上复验 ----
    migrations = MG.get("path_migrations", [])
    MIG = {m["from"]: m["to"] for m in migrations}

    def current_path(rel):
        return MIG.get(rel, rel)

    EXACT_LINK = {}
    for m in migrations:
        a = m["from"][:-3] if m["from"].endswith(".md") else m["from"]
        b = m["to"][:-3] if m["to"].endswith(".md") else m["to"]
        if a != b:
            EXACT_LINK[a] = b
    PREFIX_LINK = {p["from"] + "/": p["to"] + "/"
                   for p in MG.get("merged_pairs", []) if p.get("from") and p.get("to")}

    def current_link(t):
        tt = t[:-3] if t.endswith(".md") else t
        tt = tt.replace("\\", "/")
        if tt in EXACT_LINK:
            return EXACT_LINK[tt]
        for a, b in PREFIX_LINK.items():
            if tt.startswith(a):
                return b + tt[len(a):]
        return tt

    SECOND = {w["rel"]: w for w in MR.get("rewrites", [])}

    # V1 规范编码全局唯一
    coded = [r for r in R if r.get("code")]
    all_codes = [r["code"] for r in coded]
    dup = len(all_codes) - len(set(all_codes))
    dup_sample = [c for c, n in Counter(all_codes).items() if n > 1][:10]
    add("V1 规范编码全局唯一", dup == 0,
        {"带规范码文章": len(coded), "唯一规范码": len(set(all_codes)),
         "重复码数": dup, "重复样例": dup_sample})

    # V2 code-map 的 unique 表与索引完全一致
    unique = CM.get("unique", {})
    bad = [r["code"] for r in coded if unique.get(r["code"]) != r["uid"]][:10]
    add("V2 规范码 → UID 映射一致", len(bad) == 0 and len(unique) == len(set(all_codes)),
        {"unique 表条目": len(unique), "索引唯一码": len(set(all_codes)), "不一致样例": bad})

    # V3 裸编码一律歧义，绝不单篇命中
    amb = CM.get("ambiguous", {})
    single_groups = sum(1 for v in amb.values() if len(v) == 1)
    bad_amb = {k: v for k, v in amb.items() if k in unique}
    add("V3 裸编码全部登记且不可单篇命中", len(bad_amb) == 0,
        {"裸编码组": len(amb), "重复组": len(amb) - single_groups,
         "单成员组(仍非定位键)": single_groups, "误入唯一码表": len(bad_amb),
         "示例": {"001": len(amb.get("001", [])), "01": len(amb.get("01", []))}})

    # V4 物理改名落位（允许按 path_migrations 定位到当前路径）
    renames = MP.get("renames", [])
    located = sum(1 for r in renames
                  if (VAULT / current_path(r["new_rel"])).exists()
                  and not (VAULT / r["old_rel"]).exists())
    add("V4 物理规范化落位（新路径存在 / 旧路径消失）", located == len(renames),
        {"应落位": len(renames), "已落位": located,
         "按迁移映射复验": len(migrations)})

    # V5 正文完整性：备份原始字节 → 第二轮 changes → 本轮 changes 两阶段正向重建
    bdir = find_backup()
    mani = load(bdir / "manifest.json") if bdir else {}
    bak_by_old = {f["rel"]: bdir / f["backup"] for f in mani.get("md_files", [])}
    inverse_rel = {v: k for k, v in mani.get("rel_map", {}).items()}
    GENERATED = {"AI-总索引.md", "AI-补链接计划预览.md", "AI-断链清单.md", "README.md"}
    POST_EDITED = {"AGENT.md"}
    bad_body, checked_body, no_bak, gen_skipped, post_checked, second_phase = [], 0, 0, 0, 0, 0
    for w in MP.get("rewrites", []):
        orig_final = w["rel"]
        final = current_path(orig_final)
        if Path(orig_final).name in GENERATED and "AI统一索引" in orig_final:
            gen_skipped += 1
            continue
        if Path(orig_final).name in POST_EDITED:
            cur = VAULT / final
            if not cur.exists():
                bad_body.append({"rel": final, "reason": "受控编辑后文件缺失"})
                continue
            txt = cur.read_text(encoding="utf-8", errors="replace")
            lost = []
            for c in w["changes"]:
                new = c["new"]
                if "[[" + new + "]]" in txt:
                    continue
                head = new.split("|")[0].split("#")[0]
                tail = new[len(head):]
                if "[[" + current_link(head) + tail + "]]" in txt:
                    continue
                lost.append(new)
            post_checked += 1
            if lost:
                bad_body.append({"rel": final, "reason": "受控编辑丢失了已改写链接",
                                 "样例": lost[:3]})
            continue
        old = inverse_rel.get(orig_final, orig_final)
        bak, cur = bak_by_old.get(old), VAULT / final
        if not cur.exists() or not bak or not bak.exists():
            no_bak += 1
            continue
        ob, cb = bak.read_bytes(), cur.read_bytes()
        bom = ob.startswith(b"\xef\xbb\xbf")
        enc = w.get("encoding", "utf-8")
        if hashlib.sha256(ob).hexdigest() != w["sha256_before"]:
            bad_body.append({"rel": final, "reason": "备份与计划基线不一致"})
            continue
        ot = (ob[3:] if bom else ob).decode(enc, errors="replace")
        cmap = {c["old"]: c["new"] for c in w["changes"]}

        def rebuild(mm):
            inner = mm.group(1)
            return "[[" + cmap[inner] + "]]" if inner in cmap else mm.group(0)

        txt = WIKI_RE.sub(rebuild, ot)
        s = SECOND.get(final)
        if s:
            cmap2 = {c["old"]: c["new"] for c in s["changes"]}

            def rebuild2(mm):
                inner = mm.group(1)
                return "[[" + cmap2[inner] + "]]" if inner in cmap2 else mm.group(0)

            txt = WIKI_RE.sub(rebuild2, txt)
            second_phase += 1
        data = txt.encode(enc, errors="replace")
        if bom:
            data = b"\xef\xbb\xbf" + data
        checked_body += 1
        if hashlib.sha256(data).hexdigest() != hashlib.sha256(cb).hexdigest():
            bad_body.append({"rel": final, "reason": "两阶段正向重建与落盘字节不一致"})
    body_check = load(BODY_CHECK) if BODY_CHECK.exists() else {}
    add("V5 正文未被改动（仅链接目标同步改写）",
        len(bad_body) == 0 and no_bak == 0 and body_check.get("result") == "PASS",
        {"校验文件": checked_body, "不一致": len(bad_body), "缺备份": no_bak,
         "第二阶段(本轮改写)重建": second_phase,
         "生成器动态产物跳过": gen_skipped,
         "交付期受控编辑文件(已校验链接完整)": post_checked,
         "apply 自检": body_check.get("result"), "异常样例": bad_body[:5]})

    # V6 关联完整性：按 Obsidian 口径判定，且接受随目录迁移后的目标
    def resolvable(t):
        tt = t[:-3] if t.endswith(".md") else t
        tt = tt.replace("\\", "/")
        if (VAULT / (tt + ".md")).exists() or tt in top_dirs or tt in disk_rels:
            return True
        return "/" not in tt and tt in disk_stems

    total_links, broken_targets = 0, []
    for w in MP.get("rewrites", []):
        for ch in w["changes"]:
            total_links += 1
            t = ch["new"].split("|")[0].split("#")[0].strip()
            if not resolvable(t) and not resolvable(current_link(t)):
                broken_targets.append(t)
    # 本轮 873 处改写目标也必须可解析
    merge_links, merge_broken = 0, []
    for w in MR.get("rewrites", []):
        for ch in w["changes"]:
            merge_links += 1
            t = ch["new"].split("|")[0].split("#")[0].strip()
            if not resolvable(t):
                merge_broken.append(t)
    add("V6 文章间关联未断裂（改写目标均可解析）",
        len(broken_targets) == 0 and len(merge_broken) == 0,
        {"第二轮改写链接处数": total_links, "第二轮失效目标": len(broken_targets),
         "本轮改写链接处数": merge_links, "本轮失效目标": len(merge_broken),
         "失效样例": list(dict.fromkeys(broken_targets + merge_broken))[:5]})

    # V7 索引与磁盘一致
    missing = [r["uid"] for r in R if not Path(r["path"]).exists()]
    add("V7 索引条目与磁盘文件一致", len(missing) == 0,
        {"索引条目": len(R), "磁盘缺失": len(missing), "缺失样例": missing[:5]})

    # V8 关联信息可查询（孤立笔记 related 允许为空）
    normalized_rows = [r for r in R if r.get("physical_normalized")]
    has_field = sum(1 for r in normalized_rows if isinstance(r.get("related"), list))
    with_rel = sum(1 for r in normalized_rows if r.get("related"))
    add("V8 规范化文章关联信息可查询", has_field == len(normalized_rows),
        {"规范化文章": len(normalized_rows), "关联字段完备": has_field,
         "其中含关联": with_rel, "本来孤立": len(normalized_rows) - with_rel}, critical=False)

    # V9 端到端：唯一检索入口 + UID 稳定性锚点
    e2e = {}
    q1 = run_query("resolve", "001")
    e2e["resolve 001"] = (q1.get("result", {}).get("status"),
                          q1.get("result", {}).get("reject_single"))
    q2 = run_query("resolve", UID_ANCHOR[0])
    e2e["resolve FY2610-001"] = q2.get("result", {}).get("status")
    e2e["UID 稳定性锚点"] = q2.get("resolved_uid")
    uid = q2.get("resolved_uid") or ""
    q3 = run_query("get", uid, "--body", "--body-chars", "200") if uid else {}
    e2e["get body"] = q3.get("result", {}).get("article", {}).get("body", {}).get("available")
    q4 = run_query("context", uid, "--max-related", "3") if uid else {}
    e2e["context articles"] = len(q4.get("result", {}).get("articles", []))
    q5 = run_query("search", "五行到坐标", "--limit", "3")
    e2e["search hits"] = q5.get("result", {}).get("total_hits", 0)
    q6 = run_query("resolve", "016")
    e2e["resolve 016(单成员裸编码)"] = q6.get("result", {}).get("status")
    e2e_ok = (e2e["resolve 001"] == ("AMBIGUOUS", True)
              and e2e["resolve FY2610-001"] == "UNIQUE"
              and e2e["UID 稳定性锚点"] == UID_ANCHOR[1]
              and e2e["get body"] is True
              and e2e["context articles"] >= 2
              and e2e["search hits"] >= 1
              and e2e["resolve 016(单成员裸编码)"] == "AMBIGUOUS")
    add("V9 唯一检索入口端到端行为 + UID 不漂移", e2e_ok, e2e)

    # V10 两层编号字面零重复
    dir_codes = [CODE_RE.match(d).group(1) for d in top_dirs if CODE_RE.match(d)]
    dir_dup = {k: v for k, v in Counter(dir_codes).items() if v > 1}

    def in_archive(p):
        return any(part in EXCLUDED_ARCHIVES for part in p.relative_to(VAULT).parts)

    visible_numeric = [p.name for p in md_paths
                       if CODE_RE.match(p.name) and not in_archive(p)]
    archived_numeric = [p.name for p in md_paths
                        if CODE_RE.match(p.name) and in_archive(p)]
    add("V10 顶层目录 / 文章文件名编号字面零重复",
        not dir_dup and not visible_numeric,
        {"顶层目录编号重复组": dir_dup, "知识库口径数字编号文件": len(visible_numeric),
         "样例": visible_numeric[:5],
         "排除存档内数字编号文件(声明边界)": len(archived_numeric),
         "排除目录": sorted(EXCLUDED_ARCHIVES)})

    # V11 两代备份与回滚
    mdir = find_merge_backup()
    add("V11 逐字节备份与一键回滚可用",
        bool(bdir) and (bdir / "rollback.py").exists()
        and bool(mdir) and (mdir / "rollback.py").exists()
        and (mdir / "AI统一索引").exists(),
        {"第二轮备份": str(bdir) if bdir else None,
         "第二轮rollback.py": bool(bdir and (bdir / "rollback.py").exists()),
         "本轮备份": str(mdir) if mdir else None,
         "本轮rollback.py": bool(mdir and (mdir / "rollback.py").exists()),
         "本轮索引全量副本": bool(mdir and (mdir / "AI统一索引").exists())}, critical=False)

    # V12 合并同类项一致性
    dup_groups = MG.get("duplicate_groups", [])
    dup_ok = all((VAULT / g["canonical"]).exists()
                 and all((VAULT / c).exists() for c in g["copies"]) for g in dup_groups)
    fold_ok = True
    fold_sample = None
    if dup_groups:
        g0 = dup_groups[0]
        cr, dr = by_rel_rows.get(g0["canonical"]), by_rel_rows.get(g0["copies"][0])
        if cr and dr:
            qq = run_query("get", dr["uid"])
            fold_ok = (qq.get("resolved_uid") == cr["uid"]
                       and bool(qq.get("result", {}).get("folding")))
            fold_sample = f"{g0['copies'][0]} → {g0['canonical']}"
        else:
            fold_ok = False
    arch_rows = []
    if ARCHIVE_FILE.exists():
        with ARCHIVE_FILE.open(encoding="utf-8") as fh:
            arch_rows = [json.loads(l) for l in fh if l.strip()]
    arch_default = run_query("search", "每日备份报告", "--limit", "3")
    arch_explicit = run_query("archive", "每日备份报告", "--limit", "2")
    inc = run_query("search", "每日备份报告", "--limit", "2", "--include-archive")
    arch_ok = (
        len(arch_rows) == MG.get("archive_layer", {}).get("count", 0)
        and arch_default.get("result", {}).get("archive_layer", {}).get("included") is False
        and arch_explicit.get("result", {}).get("total_hits", 0) > 0
        and all("归档快照" in x.get("version_note", "")
                for x in arch_explicit.get("result", {}).get("items", []))
        and inc.get("result", {}).get("archive_layer", {}).get("returned", 0) > 0
        and all(a["rel"] not in by_rel_rows for a in arch_rows))
    pairs = MG.get("merged_pairs", [])
    pair_ok = all(not (VAULT / p["from"]).exists() and (VAULT / p["to"]).exists()
                  for p in pairs)
    mig_ok = all((VAULT / m["to"]).exists() and not (VAULT / m["from"]).exists()
                 for m in migrations)
    inh = MG.get("uid_inheritance", [])
    inh_ok = all(by_rel_rows.get(x["to"], {}).get("uid") == x["uid"] for x in inh)
    v12_ok = dup_ok and fold_ok and arch_ok and pair_ok and mig_ok and inh_ok
    add("V12 合并同类项一致性（折叠/归档/迁移/UID继承）", v12_ok,
        {"字节相同重复组": len(dup_groups), "重复组文件齐全": dup_ok,
         "副本折叠到主本": fold_ok, "折叠样例": fold_sample,
         "L5归档快照": len(arch_rows), "归档显式可查且标版本": arch_ok,
         "已合并目录对": len(pairs), "源目录已消失": pair_ok,
         "路径迁移落位": len(migrations), "迁移全部落位": mig_ok,
         "UID继承": len(inh), "继承逐条一致": inh_ok})

    critical_fail = [c for c in checks if c["关键"] and c["结果"] == "FAIL"]
    overall = "PASS" if not critical_fail else "FAIL"

    result = {
        "protocol": "index-first-v1 + merge-v1",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vault": str(VAULT),
        "overall": overall,
        "checks": checks,
        "summary": {
            "索引条目": len(R),
            "唯一规范编码": len(set(all_codes)),
            "歧义裸编码组": len(amb),
            "物理规范化文章": len(normalized_rows),
            "第二轮同步改写链接": total_links,
            "本轮同步改写链接": merge_links,
            "顶层目录编号重复组": len(dir_dup),
            "知识库口径数字编号文件": len(visible_numeric),
            "重复组折叠": len(dup_groups),
            "L5归档快照": len(arch_rows),
            "路径迁移": len(migrations),
            "UID继承": len(inh),
            "关键检查失败数": len(critical_fail),
        },
    }
    REPORT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# AI 检索验证报告 · 索引优先 / 字面零重复 / 合并同类项", "",
        f"> 生成：{result['generated']}　|　协议：`index-first-v1 + merge-v1`　|　**总体：{overall}**", "",
        "复跑命令：`python kb-verify.py`　|　机器可读结果：`AI检索-验证结果.json`", "",
        "## 一、验证结果", "",
        "| # | 检查项 | 结果 | 关键明细 |", "|---|---|---|---|",
    ]
    for i, c in enumerate(checks, 1):
        d = c["明细"]
        brief = "；".join(f"{k}={v}" for k, v in list(d.items())[:4])
        md.append(f"| V{i} | {c['检查项']} | **{c['结果']}** | {brief} |")
    md += [
        "", "## 二、核心结论", "",
        f"- 全库 **{len(R):,}** 篇笔记各有稳定 UID；**{len(set(all_codes)):,}** 个规范编码全局唯一，重复 **{dup}** 个。",
        f"- **{len(amb)}** 组裸编码（`001` / `01` / `1` …）全部登记在歧义表；`resolve 001` 返回 "
        f"**{len(amb.get('001', []))}** 个候选且 `reject_single=true`，**绝不随机命中单篇**。",
        f"- 两轮合并物理规范化 **{len(renames):,}** 篇；顶层目录 **{len(dir_dup)}** 组编号重复、"
        f"知识库口径 **{len(visible_numeric)}** 个数字编号文件，均为字面零重复。",
        f"- 正文两阶段正向重建逐字节比对 **{checked_body:,}** 个文件（其中本轮改写第二阶段 {second_phase} 个）、"
        f"不一致 **{len(bad_body)}** 个；第二轮改写 **{total_links:,}** 处、本轮 **{merge_links:,}** 处，"
        f"不可解析目标 **{len(broken_targets) + len(merge_broken)}** 个。",
        f"- UID 稳定性锚点 `{UID_ANCHOR[0]}` → `{e2e.get('UID 稳定性锚点')}`（多轮演化未漂移）；"
        f"本轮目录合并的 **{len(inh)}** 条路径迁移逐条继承原 UID，无重发。",
        "- 定位路径已收敛为：`kb-query.py → kb-index.jsonl/code-map.json → uid/path → 正文 + 关联 → 答案`。", "",
        "## 三、交付物", "",
        "| 文件 | 作用 |", "|---|---|",
        "| `kb-index.jsonl` / `kb-index.json` | 规范索引（唯一检索入口的数据源） |",
        "| `code-map.json` | 唯一规范码表 + 裸编码歧义表 |",
        "| `uid-map.json` | UID 持久化，改名/移动/新增不漂移 |",
        "| `kb-query.py` | AI 唯一检索入口（含副本折叠与 L5 归档显式查询） |",
        "| `kb-reindex.py` | 新增文章/关联后一键演化（含路径迁移 UID 继承） |",
        "| `kb-merge.json` | 归并规则真相源（重复组/目录组/归档层/路径迁移/UID 继承） |",
        "| `kb-archive.jsonl` | L5 归档快照清单，默认不进常规检索 |",
        "| `AI-目录归并对照.md` | 人类可读的目录与重复内容对照表 |",
        "| `AI检索-合并同类项-改写映射.json` | 本轮 873 处双链改写的第二阶段复验基线 |",
        "| `kb-verify.py` | 本验证器（v3） |",
        "| `AI-调用约束.md` | 硬性调用协议 |",
        f"| `AI检索-重命名清单.csv` | {len(renames):,} 条两轮合并改名对照 |",
        "| `AI检索-引用改写映射.json` / `AI检索-正文校验.json` | 第二轮可复验基线与正文校验 |", "",
        "## 四、两层规范化口径", "",
        "- **顶层目录**：`00-索引与导航` 固定不动；`05-五行人格心理学` / `07-得到大脑同步` "
        "因命名空间短码受保护不动；无编号目录一律不加号；已唯一的编号一律不动；"
        "`99-归档` 独占 99，`99-并入冲突存档` 让位为 `23-并入冲突存档`。共改 12 个。",
        "- **文章文件名**：索引内 1,434 篇 + 索引外归档快照 3 篇，共 1,437 篇加命名空间短码前缀；"
        "115 处同命名空间撞码加确定性 4 位后缀。",
        "- **目录型双链** 8 处同步映射；**真歧义裸链接** 932 处改为「同目录优先 + 带路径」。", "",
        "## 五、本轮合并同类项", "",
        "- 只读盘点：磁盘 17,017 篇 md、索引 14,250 篇、**真遗漏 0 篇**；"
        "2,722 篇为归档/备份快照（明确排除），38 篇为工具配置，7 篇为索引产物。",
        f"- **不物理去重**：字节完全相同的 {len(dup_groups)} 组 / {len(MG.get('duplicate_of', {}))} 份副本"
        "几乎全是技能包功能构件（SKILL/README/api），物理删除会使技能包失效；"
        "改为索引层折叠，副本不单独命中、取正文自动改为主本并标注。",
        "- **不自动裁决同名**：2,373 组同名异文中绝大多数是 `SKILL.md`(1,164) / `README.md`(228) / "
        "`test-cases.md`(133) 等技能包标准构件，分属不同技能、各有语义，不是同一文章的多个版本。",
        "- **语义目录只登记不合并**：书稿 5 目录、AI 原生组织 4 目录等两两文件交集为 0，"
        "合并只改善外观、不减少冗余，却需重算命名空间短码与全量双链。",
        f"- **已物理整理**：`19-系统配置 → 10-系统配置`、`22-工作记录与复盘 → 20-工作记录与复盘`，"
        f"共 {len(migrations)} 个文件迁移、{merge_links} 处双链改写；"
        "1 处同名异文 `MEMORY备份.md` 加 `-来自22` 后缀零覆盖保留两版。",
        "- **归档策略**：2,722 篇 L5 快照默认不进常规检索，须显式 `archive` 子命令或 "
        "`--include-archive` 查询，且答案必须标注「归档快照·非现行版本」。", "",
        "## 六、边界（诚实说明）", "",
        f"- 排除存档内仍有 **{len(archived_numeric):,}** 个数字编号文件"
        "（`99-归档` / `WorkBuddy知识备份体系` 等），不参与 AI 检索与编码定位，V10 单列声明。",
        "- `AI-总索引.md` / `AI-补链接计划预览.md` / `AI-断链清单.md` / `README.md` 由 "
        "`_build_ai_index.py` 每次重建重新生成，属可再生成产物，不参与 V5 静态正文比对。",
        "- `AGENT.md` 在交付阶段做过受控编辑，不参与 V5 逐字节比对；已单独校验其已改写链接仍完整。",
        "- 历史存档中仍有 **57 处**双链带旧目录名前缀，独立诊断确认全部是规范化前即存在的"
        "历史断链 / 示例链接，**真实关联断裂 0 处**，故未做无意义改写。",
        "- 库外引用（IMA / 网站 / 公众号草稿 / 桌面合稿 / 手工记录的路径）不会自动跟随新路径，需人工按需更新。",
        "- `scripts`（4 个脚本）与 `微信公众号草稿库`（约 180 个草稿 HTML）含大量非 md 资产，"
        "虽无 md 但不是空目录，本轮**未移动**。",
        "- 23 个无编号遗留顶层目录保持原位；是否收编进编号体系属于组织裁决，尚未执行。",
        f"- 回滚：第二轮 `python \"{bdir / 'rollback.py' if bdir else '（见备份目录）/rollback.py'}\"`；"
        f"本轮 `python \"{mdir / 'rollback.py' if mdir else '（见备份目录）/rollback.py'}\"`；"
        "回滚后需再跑 `python kb-reindex.py` 同步索引。", "",
    ]
    REPORT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print("overall =", overall)
    for c in checks:
        print(f"  {c['结果']:<4} {c['检查项']}")


if __name__ == "__main__":
    main()
