# -*- coding: utf-8 -*-
"""Obsidian 知识库 · 统一索引生成器（只新建索引文件，绝不修改任何原有笔记）

产物落在 <主库>/00-索引与导航/AI统一索引/
  README.md              索引使用说明（AI 如何检索引用）
  AI-总索引.md           人类可读总索引（分层 + 目录导航）
  ai-index.json          机器可读全量索引（唯一真相源）
  ai-index.jsonl         逐行扁平索引（便于流式检索）
  AI-断链清单.csv / .md  现有 wikilink 断链（区分目录型/真断链）
  AI-重名清单.csv        重名歧义清单
  AI-孤立笔记清单.csv    零入链零出链笔记
  AI-补链接计划.json     dry-run：拟补的双向链接（不写入正文）
  AI-补链接计划预览.md   计划样例
"""
import csv
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(r"D:\以观其妙书院知识库")
MAIN = BASE / "以观其妙书院"
OUT = MAIN / "00-索引与导航" / "AI统一索引"
# 2026-11-14 同名目录融合后：全部内容都在主 vault 内。
# 原副库/研学库文件保留为磁盘存档，不再重复进索引（避免同一内容计数两次）。
VAULTS = {"主库": MAIN}
EXCLUDE_PARTS = {
    ".git", ".obsidian", ".trash", ".smart-env", ".claude", ".codebuddy",
    ".cursor", ".github", ".workbuddy", "node_modules", "__pycache__",
    "site-packages", "binaries", "venv", ".venv", "dist", "build",
    "99-归档", "备份", ".backup", "backup", "AI统一索引",
}
EXCLUDE_PREFIX_HINTS = (
    "backup_", "备份_", "_archive", "archive-", "WorkBuddy知识备份体系",
    "skills-marketplace", "connectors-marketplace", "plugins",
)
LINK_RE = re.compile(r"\[\[([^\[\]|#\n]+?)(?:[#|][^\[\]\n]*?)?\]\]")
FM_RE = re.compile(r"\A\ufeff?---\s*\n(.*?)\n---\s*\n", re.S)
STOP = set("的了是在和与及或对于中的一个这那有为以从把被将由等值不也无之而其若则即于关于如何进行可以能够通过以及我们你们他们它们此该各每并并且但但是就都也很更最一二三四五六七八九十第章节版本文件目录内容说明介绍概述总结相关关联使用实现方法系统数据信息")


def read_text(p: Path):
    try:
        raw = p.read_bytes()
    except Exception:
        return None
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def is_excluded(rel: Path) -> bool:
    parts = {p.lower() for p in rel.parts}
    # 统一索引目录：总入口与说明本身必须可被引为笔记，其余清单/预览排除
    if "ai统一索引" in parts:
        return rel.name not in ("AI-总索引.md", "README.md")
    if parts & {s.lower() for s in EXCLUDE_PARTS}:
        return True
    return any(any(p.lower().startswith(h.lower()) for h in EXCLUDE_PREFIX_HINTS)
               for p in rel.parts)


def layer_of(vname: str, rel: Path) -> str:
    p0 = rel.parts[0] if rel.parts else ""
    # 顶层目录两轮编号规范化后，按「去掉编号后的名称」判定层级，
    # 新旧目录名都兼容（99-/XX-并入冲突存档、11-E盘资料库、Raw原文、Wiki成书）。
    body = p0.split("-", 1)[1] if re.match(r"^\d{1,3}-", p0) else p0
    if body == "并入冲突存档":
        return "L4-冲突存档·副库版本"
    if body in ("Raw原文", "Wiki成书"):
        return "L3-研学·Raw原文" if body == "Raw原文" else "L3-研学·Wiki成书"
    if body == "E盘资料库":
        return "L2-素材·原文抽取"
    return "L1-正式知识笔记"


def parse_fm(txt: str):
    m = FM_RE.match(txt)
    if not m:
        return {}, txt
    body = txt[m.end():]
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"\'')
    return fm, body


def first_title(body: str, stem: str) -> str:
    m = re.search(r"^#\s+(.+)$", body, re.M)
    if m:
        return re.sub(r"[#*`\[\]]", "", m.group(1)).strip()[:120]
    return stem


def auto_summary(fm: dict, body: str) -> str:
    if fm.get("summary"):
        return fm["summary"][:200]
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if not p or p.startswith(("#", ">", "|", "```", "---", "-", "*", "!")):
            continue
        p = re.sub(r"\s+", " ", p)
        if len(p) >= 12:
            return p[:160]
    return ""


def tokens(text: str, limit: int = 160):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+|[^\u4e00-\u9fffA-Za-z0-9]+", " ", text)
    out = []
    for seg in text.split():
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]{2,}$", seg):
            out.append(seg.lower())
        else:
            for i in range(len(seg) - 1):
                bg = seg[i:i + 2]
                if bg not in STOP:
                    out.append(bg)
    seen, res = set(), []
    for t in out:
        if t not in seen:
            seen.add(t)
            res.append(t)
        if len(res) >= limit:
            break
    return res


def norm_target(raw: str) -> str:
    t = raw.strip().split("/")[-1].split("#")[0].split("|")[0].strip()
    return t[:-3] if t.endswith(".md") else t


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    notes, basename_map = [], defaultdict(list)
    corpus = {}
    dirset = set()

    for vname, vroot in VAULTS.items():
        if not vroot.exists():
            continue
        for d in vroot.rglob("*"):
            if d.is_dir():
                dirset.add(d.name)
        for f in sorted(vroot.rglob("*.md")):
            rel = f.relative_to(vroot)
            if is_excluded(rel):
                continue
            txt = read_text(f)
            if txt is None:
                continue
            fm, body = parse_fm(txt)
            relposix = rel.as_posix()
            stem = f.stem
            links = [l.strip() for l in LINK_RE.findall(txt)]
            n = {
                "id": f"{vname}/{relposix}",
                "vault": vname,
                "path": str(f),
                "rel": relposix,
                "layer": layer_of(vname, rel),
                "top": rel.parts[0] if len(rel.parts) > 1 else "(根目录)",
                "title": (fm.get("title") or first_title(body, stem)).strip().strip('"\''),
                "type": fm.get("type", ""),
                "tags": re.findall(r"[\w\u4e00-\u9fff/-]+", fm.get("tags", "")),
                "summary": auto_summary(fm, body),
                "created": fm.get("created", ""),
                "updated": fm.get("updated", ""),
                "chars": len(txt),
                "has_fm": bool(FM_RE.match(txt)),
                "outlinks_raw": links,
                "wikilink": relposix[:-3],
            }
            notes.append(n)
            corpus[n["id"]] = (n["title"] + " " + " ".join(n["tags"]) + " " + body[:1500])
            basename_map[stem].append(n["id"])

    by_id = {n["id"]: n for n in notes}
    id_by_stem = defaultdict(list)
    for n in notes:
        id_by_stem[Path(n["rel"]).stem].append(n["id"])

    # 链接图（仅同 vault 内 wikilink 有效）；带路径链接优先精确匹配
    wiki_by_vault = defaultdict(dict)
    for n0 in notes:
        wiki_by_vault[n0["vault"]][n0["wikilink"]] = n0["id"]
    inlinks = defaultdict(set)
    broken_rows = []
    for n in notes:
        n["outlinks"] = []
        n["broken"] = []
        for raw in n["outlinks_raw"]:
            full = raw.strip().split("#")[0].split("|")[0].strip()
            if full.endswith(".md"):
                full = full[:-3]
            exact = wiki_by_vault[n["vault"]].get(full)
            if exact and exact != n["id"]:
                n["outlinks"].append(exact)
                inlinks[exact].add(n["id"])
                continue
            t = norm_target(raw)
            targets = id_by_stem.get(t, [])
            same = [x for x in targets if x.startswith(n["vault"] + "/")]
            if len(same) == 1:
                n["outlinks"].append(same[0])
                inlinks[same[0]].add(n["id"])
            elif len(same) > 1:
                # 同名歧义：优先同目录
                pref = [x for x in same if "/".join(x.split("/")[1:-1]) ==
                        "/".join(n["id"].split("/")[1:-1])]
                pick = pref[0] if len(pref) == 1 else None
                if pick:
                    n["outlinks"].append(pick)
                    inlinks[pick].add(n["id"])
                else:
                    n["ambiguous"] = n.get("ambiguous", []) + [raw]
            else:
                kind = "目录型链接(非文件)" if t in dirset or re.match(r"^\d{2}-", t) else "真断链"
                n["broken"].append({"raw": raw, "kind": kind})
                broken_rows.append((n["id"], raw, kind))

    for n in notes:
        n["inlinks"] = sorted(inlinks.get(n["id"], []))
        n["in_degree"] = len(n["inlinks"])
        n["duplicate_group"] = len(id_by_stem[Path(n["rel"]).stem]) > 1

    isolated = [n for n in notes if n["in_degree"] == 0 and not n["outlinks"]]
    dups = {k: v for k, v in id_by_stem.items() if len(v) > 1}

    # ---------- 写索引 ----------
    (OUT / "ai-index.json").write_text(
        json.dumps({"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "vault_root": str(MAIN),
                    "note_count": len(notes),
                    "notes": notes}, ensure_ascii=False, indent=1), encoding="utf-8")
    with (OUT / "ai-index.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
        for n in notes:
            fh.write(json.dumps({k: n[k] for k in
                                 ("id", "vault", "path", "layer", "top", "title",
                                  "type", "tags", "summary", "updated", "chars",
                                  "in_degree", "wikilink")}, ensure_ascii=False) + "\n")

    def wcsv(name, header, rows):
        with (OUT / name).open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)

    wcsv("AI-断链清单.csv", ["来源笔记", "链接原文", "类型"], broken_rows)
    wcsv("AI-重名清单.csv", ["笔记名", "份数", "全部路径"],
         [[k, len(v), " | ".join(v)] for k, v in sorted(dups.items(), key=lambda x: -len(x[1]))])
    wcsv("AI-孤立笔记清单.csv", ["笔记ID", "层级", "标题", "字数"],
         [[n["id"], n["layer"], n["title"], n["chars"]] for n in isolated])

    # ---------- 人类可读总索引 ----------
    layers = Counter((n["vault"], n["layer"]) for n in notes)
    tops = Counter((n["vault"], n["layer"], n["top"]) for n in notes)
    L = ["---", "title: AI 统一索引 · 总入口", "type: index",
         f"updated: {time.strftime('%Y-%m-%d')}",
         "tags: [索引, AI检索, 统一入口]", "---", "",
         "# 📚 以观其妙书院 · AI 统一索引", "",
         "> 本目录是**唯一索引真相源**。旧版多份总索引（v2.0/v4.0/知识地图等）保留为历史存档，不再作为检索入口。",
         "> 生成方式：运行本目录 `_build_ai_index.py`；本索引只新增文件，不改动任何原有笔记。", "",
         f"生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}　|　收录笔记：**{len(notes):,}** 篇（已排除软件副本与归档）", "",
         "## 一、给 AI 的检索方式", "",
         "1. 读 `ai-index.jsonl`（逐行一条，最省上下文）或 `ai-index.json`（含完整链接图）。",
         "2. 按 `title` / `summary` / `tags` / `top` 过滤，命中后取 `path` 字段直接读取原文。",
         "3. 融合后全部笔记都在同一个 vault，Obsidian 双链全局有效；跨系统引用请用 `path`。",
         "4. `layer`：L1 正式笔记＝补双向链接；L2 素材抽取＝只登记；L3 研学＝独立体系；L4 冲突存档＝副库异文版本（两版并存，不覆盖）。", "",
         "## 二、分层统计", "", "| 库 | 层 | 笔记数 |", "|---|---|---:|"]
    for (v, l), c in sorted(layers.items()):
        L.append(f"| {v} | {l} | {c:,} |")
    L += ["", "## 三、目录导航（按笔记数排序）", "", "| 库 / 层 | 目录 | 笔记数 |", "|---|---|---:|"]
    for (v, l, t), c in tops.most_common(80):
        L.append(f"| {v} · {l} | {t} | {c:,} |")
    L += ["", "## 四、质量快照", "",
          f"- 现有 wikilink：{sum(len(n['outlinks_raw']) for n in notes):,} 条",
          f"- 断链：{len(broken_rows):,} 条（其中真断链 {sum(1 for r in broken_rows if r[2]=='真断链'):,} 条）",
          f"- 孤立笔记（零入链零出链）：{len(isolated):,} 篇",
          f"- 重名笔记名：{len(dups):,} 组 / {sum(len(v) for v in dups.values()):,} 篇",
          f"- 有自动摘要可用：{sum(1 for n in notes if n['summary']):,} 篇", "",
          "## 五、配套清单与方案", "",
          "- `AI-断链清单.csv` — 全量断链，含目录型/真断链分类",
          "- `AI-重名清单.csv` — 链接歧义裁决依据",
          "- `AI-孤立笔记清单.csv` — 待补链接的重点对象",
          "- `AI-补链接计划.json` / `AI-补链接计划预览.md` — **dry-run 方案，尚未写入任何正文**", ""]
    (OUT / "AI-总索引.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------- dry-run 补链接计划（仅主库 L1） ----------
    pool = [n for n in notes if n["vault"] == "主库" and n["layer"] == "L1-正式知识笔记"]
    pool_ids = {n["id"] for n in pool}
    N = max(1, len(pool))

    # 词项 → 倒排（用标题+标签+正文前 1500 字），IDF 抑制通用词
    inv, toks = defaultdict(list), {}
    for n in pool:
        toks[n["id"]] = set(tokens(corpus[n["id"]], 140))
    for nid, ts in toks.items():
        for t in ts:
            inv[t].append(nid)
    usable = {t for t, v in inv.items() if len(v) <= max(40, int(N * 0.12))}
    idf = {t: math.log(1 + N / (1 + len(v))) for t, v in inv.items()}

    tag_index, dir_index = defaultdict(list), defaultdict(list)
    for n in pool:
        for tg in n["tags"][:8]:
            tag_index[tg].append(n["id"])
        dir_index["/".join(n["rel"].split("/")[:2])].append(n["id"])

    score, hits = defaultdict(Counter), defaultdict(Counter)
    for nid, ts in toks.items():
        for t in ts & usable:
            for cand in inv[t][:80]:
                if cand != nid:
                    score[nid][cand] += idf[t]
                    hits[nid][cand] += 1
    for n in pool:
        nid = n["id"]
        for tg in n["tags"][:8]:
            for cand in tag_index[tg][:60]:
                if cand != nid:
                    score[nid][cand] += 0.6
        for cand in dir_index["/".join(n["rel"].split("/")[:2])][:60]:
            if cand != nid:
                score[nid][cand] += 0.3
        for cand in n["outlinks"]:
            if cand in pool_ids:
                score[nid][cand] += 3.0

    # 粗选 + 枢纽惩罚：任何笔记被过多来源选为目标时降权，避免全局热门节点污染
    rough = {}
    hub = Counter()
    for nid in pool_ids:
        cand = [c for c, s in score[nid].most_common(40)
                if c in pool_ids and (hits[nid][c] >= 2 or s >= 3.0)][:12]
        rough[nid] = cand
        for c in cand:
            hub[c] += 1
    HUB_LIMIT = max(25, int(N * 0.015))
    hubs = {c for c, k in hub.items() if k > HUB_LIMIT}

    def is_nav(c):
        stem = Path(by_id[c]["rel"]).stem
        return (stem.startswith("_") or stem.lower() in {"readme", "skill", "index"}
                or any(k in stem for k in ("总索引", "快速导航", "知识图谱", "使用指南", "导航")))

    proposed = defaultdict(list)
    for n in pool:
        nid = n["id"]
        existing = set(n["outlinks"]) | set(n["inlinks"])
        ordered = [c for c in rough[nid] if c not in existing and c not in hubs]
        ordered.sort(key=lambda c: (is_nav(c), -score[nid][c]))
        picks = ordered[:6]
        for c in picks:
            proposed[nid].append(c)
            proposed[c].append(nid)   # 双向对称回指

    plan = {nid: sorted(set(v))[:10] for nid, v in proposed.items()}
    print(f"[质量] 候选池 {N:,} 篇 / 枢纽剔除 {len(hubs)} 个 / 高频目标 "
          f"{hub.most_common(3)}")
    (OUT / "AI-补链接计划.json").write_text(
        json.dumps({"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "scope": "主库 L1-正式知识笔记（Obsidian 同 vault 内链接才有效）",
                    "status": "DRY-RUN · 未写入任何笔记正文",
                    "note_count": len(pool), "linked_notes": len(plan),
                    "pairs": sum(len(v) for v in plan.values()),
                    "plan": plan}, ensure_ascii=False, indent=1), encoding="utf-8")

    pv = ["# AI 补链接计划 · 预览（DRY-RUN，未写入正文）", "",
          f"- 范围：主库 L1 正式知识笔记 {len(pool):,} 篇",
          f"- 将被补齐的笔记：{len(plan):,} 篇；拟新增双向链接：{sum(len(v) for v in plan.values()):,} 条",
          "- 链接形式：`[[目录/文件名]]`（带完整路径，规避 2,488 组重名歧义）",
          "- 质量处理：已用 IDF 抑制通用词、剔除全局枢纽节点、导航/索引类目标降权",
          "- 写入方式：在笔记末尾追加带标记的「🔗 AI 关联笔记」区块，可识别、可回滚、重复运行不叠加",
          "- 跨库（副库 / 研学库）不做 `[[]]`，只在统一索引里以 path 关联", "",
          "## 样例", ""]
    for nid in list(plan)[:12]:
        src = by_id[nid]
        pv += [f"### {src['title']}", f"`{nid}`", ""]
        for t in plan[nid][:5]:
            pv.append(f"- → [[{by_id[t]['wikilink']}]]　`{by_id[t]['title']}`")
        pv.append("")
    (OUT / "AI-补链接计划预览.md").write_text("\n".join(pv) + "\n", encoding="utf-8")

    # 断链清单 md（聚合）
    agg = Counter((r[2], r[1]) for r in broken_rows)
    md = ["# 断链清单（只读诊断）", "",
          f"共 {len(broken_rows):,} 条。分类：**目录型链接**是索引文件里写 `[[01-核心体系]]` 指向文件夹，",
          "Obsidian 无法解析但语义是导航；**真断链**才是目标笔记不存在或已改名。", "",
          "## 高频断链目标（前 60）", "", "| 类型 | 链接原文 | 次数 |", "|---|---|---:|"]
    for (kind, raw), c in agg.most_common(60):
        md.append(f"| {kind} | `{raw}` | {c:,} |")
    (OUT / "AI-断链清单.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    (OUT / "README.md").write_text("\n".join([
        "# AI 统一索引 · 使用说明", "",
        "## 这是什么", "把散落在三个库、多个版本总索引里的内容，收敛成**一份**可复现、机器可读的索引。",
        "本目录由脚本生成，**只新增文件，不修改、不删除任何原有笔记**。", "",
        "## 当前状态（2026-11-14）", "",
        "- 阶段 B + 融合后累计：主库 **6,281 篇**含可回滚的「🔗 AI 关联笔记」区块；目录型链接累计规范化 **2,292 处**。",
        "- `AI-补链接计划.json` 现为**下一轮增量建议**；本轮已执行计划留存在 `AI-补链接计划-已执行.json`。",
        "- 备份位置、回滚命令与验证结果见 `AI-补链接执行报告.md`。",
        "- 2026-11-14 已完成同名目录融合：1,179 篇直迁同名目录；961 篇内容不同的异文另存 `99-并入冲突存档/` 并互链回主库现行版。",
        "- 原副库/研学库文件全部保留不动；现在只有一个索引口径，`[[]]` 全局有效。", "",
        "## 文件用途", "",
        "| 文件 | 用途 |", "|---|---|",
        "| `AI-总索引.md` | 人类入口：分层统计 + 目录导航 |",
        "| `ai-index.json` | 唯一真相源：全量字段 + 链接图（含 inlinks/outlinks/broken） |",
        "| `ai-index.jsonl` | 逐行扁平版，AI 检索时最省 token |",
        f"| `AI-断链清单.csv/.md` | {len(broken_rows):,} 条断链，按目录型/真断链分类 |",
        f"| `AI-重名清单.csv` | {len(dups):,} 组重名，补链接前必须规避 |",
        f"| `AI-孤立笔记清单.csv` | {len(isolated):,} 篇零链接笔记（同 vault 严格口径） |",
        "| `AI-补链接计划.json/.md` | dry-run 方案，尚未写入正文 |",
        "| `_build_ai_index.py` | 重建脚本；内容更新后重跑即可 |", "",
        "## AI 检索引用三步", "",
        "1. 查 `ai-index.jsonl`，按 title/summary/tags/top 过滤；",
        "2. 取命中条目的 `path` 直接读原文（跨库必须用 path）；",
        "3. 引用时：主库内部用 Obsidian 双链；跨库/给外部用 `path`。", "",
        "## 分层口径", "",
        "- **L1 正式知识笔记**：可补双向链接、可进图谱；",
        "- **L2 素材·原文抽取**（11-E盘资料库 6,899 篇）：老 .doc 抽取件，只登记不补链；",
        "- **L3 研学**：Raw 原文 + Wiki 成书，独立体系；",
        "- **L4 冲突存档**：961 篇副库异文版本，两版并存、不覆盖、不补链；",
        "- 软件副本 / 99-归档 / 备份：不进索引。", "",
        "## 已知限制（诚实说明）", "",
        "- 961 个同名但内容不同的文件**未做内容合并**，采用「两版并存 + 互链」；哪版为准需人工裁决（见 `AI-融合冲突清单.csv`）。",
        "- L2 素材层（6,899 篇老 .doc 抽取件）与 L4 冲突存档按分层口径不补链接。",
        "- 13,000+ 条真缺失断链多为旧索引示例链接与历史改名文件，保留在 `AI-断链清单.csv` 待人工裁决。",
        "- `obsidian-agent stats` 报 13,721 篇，本索引 14,250 篇，差 529 属**扫描口径差异而非缺文件**：CLI 跳过 `_` 开头子目录（456 篇）与根目录散落 md（21 篇），其余为 `type` 字段与排除规则差异。**全量口径以本索引为准**。", "",
        "## 索引优先检索（AI 必读）", "",
        "- **唯一入口**：`kb-query.py` + `kb-index.jsonl` + `code-map.json`；本文件与 `ai-index.jsonl` 降级为底层清单，不再是检索入口。",
        "- 硬约束与四步调用流程见 `AI-调用约束.md`；验证结果见 `AI检索-验证报告.md`。",
        "- 新增文章或改动双链后跑 `python kb-reindex.py`；独立复验 `python kb-verify.py`。",
        "- 14,250 篇各有稳定 UID；1,600 个规范编码全局唯一；232 组裸编码（126 组重复 + 106 组单成员）全部登记，禁止单篇命中。",
        "- 顶层目录与文章文件名两层编号均已字面零重复（`00-索引与导航` 固定，`99-归档` 独占 99）；详见 `AI检索-验证报告.md` 第四节。",
        "- 合并同类项（merge-v1）：`kb-merge.json` 折叠 33 组字节相同副本（不物理删除技能包构件）、登记 2,722 篇 L5 归档快照（默认不检索、须显式查询并标注版本）；`groups` 子命令返回目录对照；详见 `AI-目录归并对照.md`。",
        "- 独立复验 `python kb-verify.py` 现为 V1–V12，含折叠/归档/目录迁移/UID 继承一致性检查。", "",
        f"生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}", "",
    ]) + "\n", encoding="utf-8")

    # 复现脚本随索引一起归档
    (OUT / "_build_ai_index.py").write_text(
        Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")

    print(json.dumps({
        "索引目录": str(OUT),
        "收录笔记": len(notes),
        "分层": dict(Counter(n["layer"] for n in notes)),
        "断链": len(broken_rows),
        "真断链": sum(1 for r in broken_rows if r[2] == "真断链"),
        "重名组": len(dups),
        "孤立": len(isolated),
        "补链接候选笔记": len(pool),
        "拟补双向链接": sum(len(v) for v in plan.values()),
        "耗时秒": round(time.time() - t0, 1),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
