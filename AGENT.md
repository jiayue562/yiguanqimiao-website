# Obsidian Knowledge Base — Agent Instructions

This is an agent-managed Obsidian vault. You (the AI agent) operate this vault via the `obsidian-agent` CLI.

## Quick Start

```bash
# Read a note
obsidian-agent read "my-project"
obsidian-agent read "my-project" --section "TODO"

# Check what's in the vault
obsidian-agent list
obsidian-agent recent                    # last 7 days
obsidian-agent stats                     # vault overview

# Create
obsidian-agent journal                   # today's journal
obsidian-agent note "Title" project --tags "backend,api"
obsidian-agent capture "Quick idea text"

# Search & discover
obsidian-agent search "keyword"          # full-text search
obsidian-agent backlinks "note-name"     # what links here?
obsidian-agent orphans                   # unlinked notes

# Edit existing notes
obsidian-agent patch "note" --heading "TODO" --append "- [ ] New task"
obsidian-agent update "note" --status active --summary "Updated"
obsidian-agent archive "old-note"
obsidian-agent delete "obsolete-note"

# Tags
obsidian-agent tag list
obsidian-agent tag rename "old" "new"

# Rename / Move / Merge
obsidian-agent rename "note" "New Title"  # rename + update refs
obsidian-agent move "note" project        # change type/directory
obsidian-agent merge "source" "target"    # combine two notes

# Batch operations
obsidian-agent batch tag --type idea --add "review"
obsidian-agent batch archive --tag "deprecated"
obsidian-agent batch update --type project --set-status active

# Export / Import
obsidian-agent export backup.json
obsidian-agent import notes.json

# Reviews
obsidian-agent review                    # weekly
obsidian-agent review monthly

# Smart linking & quality
obsidian-agent link --dry-run            # preview missing links
obsidian-agent link                      # auto-link related notes
obsidian-agent validate                  # check frontmatter issues
obsidian-agent relink --dry-run          # preview broken link fixes
obsidian-agent relink                    # auto-fix broken links
obsidian-agent timeline --days 7         # recent activity feed

# Pin favorites
obsidian-agent pin "important-note"
obsidian-agent pin list
obsidian-agent unpin "important-note"

# Graph & discovery
obsidian-agent neighbors "note" --depth 3 # connected notes
obsidian-agent random 3                  # serendipitous review
obsidian-agent focus                     # what to work on next

# Stats & reporting
obsidian-agent count                     # word/line statistics
obsidian-agent agenda                    # pending TODOs
obsidian-agent changelog --days 14       # recent changes
obsidian-agent daily                     # daily dashboard
obsidian-agent suggest                   # improvement suggestions

# Smart & semantic search (v1.3+)
obsidian-agent smart-search "API design" # BM25 ranked search
obsidian-agent embed-search "how to..."  # semantic via Ollama/OpenAI
obsidian-agent embed-status              # check embedding providers

# Canvas & Bases (v1.3+)
obsidian-agent canvas create "board"     # create .canvas file
obsidian-agent canvas add-node "board" --type text --text "Note"
obsidian-agent canvas add-edge "board" --from id1 --to id2
obsidian-agent canvas read "board"
obsidian-agent base create "tracker"     # create .base file
obsidian-agent base query "tracker"      # query notes with filters
obsidian-agent base read "tracker"

# Maintenance
obsidian-agent sync                      # rebuild indices
obsidian-agent health                    # vault health score
obsidian-agent graph                     # Mermaid knowledge graph
obsidian-agent broken-links              # find broken [[00-索引与导航/AI统一索引/AI-总索引|links]]
obsidian-agent duplicates                # find similar notes
obsidian-agent search "pattern" --regex  # regex search
obsidian-agent bridge-status             # Obsidian CLI bridge info
```

All commands support `--json` for machine-readable output.

## Navigation

- `_index.md` — Vault index
- `_tags.md` — Tag index (find notes by tag)
- `_graph.md` — Knowledge graph (relationships between notes)
- `CONVENTIONS.md` — Writing rules (**read before manual edits**)
- `templates/` — Note templates (`{{}}` placeholders)

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `areas/` | Long-term focus areas |
| `projects/` | Concrete projects with goals |
| `resources/` | Reference materials |
| `journal/` | Daily logs and weekly reviews |
| `ideas/` | Draft ideas to explore |

## Rules for Manual Edits

If you edit files directly instead of using the CLI:

1. **Read `CONVENTIONS.md` first**
2. **Include complete frontmatter** in new notes
3. **Update `updated` field** when modifying
4. **Update indices**: `_tags.md`, `_graph.md`, directory `_index.md`
5. **Build bidirectional links** via the `related` field
6. **File names**: lowercase with hyphens
7. **Internal links**: `[[filename]]` (no `.md` extension)

## Environment Variables

- `OA_VAULT` — Vault path (so you don't need `--vault` every time)
- `OA_TIMEZONE` — Timezone for dates (default: UTC)
- `OA_NO_OFFICIAL_CLI` — Disable Obsidian CLI bridge (set to 1)
- `OA_OPENAI_KEY` — OpenAI API key for embedding search

## 本库实际配置（2026-11-14 · 龙龟神将修复后补记）

> 上文 Directory Structure 的 PARA 五目录是工具默认值；**本库不是这个结构**，请以本节为准。

- **Vault**：`D:\以观其妙书院知识库\以观其妙书院`（融合后单一 vault，全部内容都在此）
- `.obsidian-agent.json`：登记了 46 个实际顶层目录（排除 `99-归档` 与软件副本目录），CLI 才扫得到笔记；删掉它会退回默认五目录、统计变 0
- `OA_VAULT` 已设为用户级环境变量指向上述 vault；三个 shim 另带 `OA_VAULT_FALLBACK` 兜底（仅在变量未设置时生效），WorkBuddy 会话内新起的进程也能用
- 覆盖 vault 时 `--vault <path>` **必须放在命令之后**，例如 `obsidian-agent stats --vault "D:\..."`；放在最前会被当成命令名，报 `Unknown command: --vault`
- 只读命令可放心用：`stats` / `search` / `smart-search` / `backlinks` / `orphans` / `broken-links` / `graph` / `validate` / `list` / `read`
- ⚠️ **不要在整理后的库上跑写命令**：`sync` / `link` / `relink` / `note` / `capture` / `patch` / `batch` / `rename` / `move` 会改写 `_index.md`、`_tags.md`、`_graph.md` 与 frontmatter，与 `00-索引与导航/AI统一索引` 口径冲突
- Windows PowerShell 5.1 下先执行 `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`，否则中文输出乱码
- AI 检索入口仍以 `00-索引与导航/AI统一索引/ai-index.jsonl` 为准（含 path / layer / summary）；本库里 CLI 的 `type` 字段会退化成目录名
- ⚠️ `stats --json` 的 `total` 是 **13,721**，统一索引是 **14,250**，差 529 **不是数据丢失**：CLI 会跳过 `_` 开头子目录（主要是 `07-得到大脑同步/_历史归档_20261104` 328 篇与 `_发芽报告` 128 篇）、扫不到根目录散落的 21 篇 md，且 `type` 取值口径不同。**判定「收录与否」一律以统一索引为准**，CLI 统计只作只读辅助

## 索引优先检索协议（index-first-v1 · 2026-11-14 起强制）

> **本节优先级高于上文所有 Quick Start 示例**。任何 AI 调用本库内容时以本节为准。

- **唯一入口**：`00-索引与导航/AI统一索引/kb-query.py`；唯一索引 `kb-index.jsonl` + `code-map.json`。`ai-index.jsonl` 与本文件的 Quick Start 降级为底层清单/历史示例，不再作为检索入口。
- **五条硬约束**：① 必须先 `search` / `resolve` 拿到 UID 或唯一规范码才允许读正文；② 裸编码 `001` / `01` / `1` 一律返回 AMBIGUOUS 候选表，禁止猜一篇、取第一篇或取最像的一篇；③ 禁止 `rglob` / 递归遍历 / 文件名模糊匹配找文章；④ 只有 `get` / `context` 返回的 `path` 才可读，且带 `via=index` 溯源；⑤ 答案只基于 `context` 返回的 `articles` 正文与 `relation` 生成，不得引用未命中的文章。
- **标准流程**：`python kb-query.py search "关键词"` → `python kb-query.py resolve <code|uid>` → `python kb-query.py context <uid> --body` → 基于 articles 作答并标注所用 uid。
- **编码规范（两轮已字面零重复）**：顶层目录编号重复 **0 组**（`00-索引与导航` 固定，12 个重复目录重编为 `12–23`，无编号目录不加号，`99-归档` 独占 99）；索引内 **1,600 篇**编号文章文件名全部带唯一规范码（如 `FY2610-001-xxx.md`、`NS7AA7E-01-xxx.md`），知识库口径下纯数字编号文件 **0 个**；232 组裸编码（126 组重复 + 106 组单成员）全部登记，**无论对应几篇都禁止单篇命中**；裸编码保留为 `legacy_code`，不再是定位键。详见 `AI检索-验证报告.md` 第四节。
- **持续演化**：新增文章或改动双链后跑 `python kb-reindex.py`；`--check` 只读体检；`python kb-verify.py` 独立复验。索引重建不改任何笔记正文。
- 完整协议见 `00-索引与导航/AI统一索引/AI-调用约束.md`；验证结果见 `AI检索-验证报告.md`。
- **合并同类项（merge-v1）**：`kb-merge.json` 为归并规则真相源。字节完全相同的 33 组 / 38 份副本**只在索引层折叠**（`search` 不单列；传副本 uid 取正文自动改为主本并带 `folding` 标注），**不物理删除**——它们多是 `SKILL.md` / `README.md` / `api.md` 等技能包功能构件，删掉会让技能包失效。2,722 篇 L5 归档快照**默认不进常规检索**，须用 `archive` 子命令或 `--include-archive` 显式查询，答案必须标注「归档快照·非现行版本」；`groups` 子命令返回目录归并对照。详见 `AI-目录归并对照.md` 第九节与 `AI检索-验证报告.md` 第五节。
- **目录合并已收口**：`19-系统配置 → 10-系统配置`、`22-工作记录与复盘 → 20-工作记录与复盘`；113 个文件迁移、873 处双链同步改写、112 条 UID 路径迁移继承，验证器 V1–V12 全 PASS。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[16-工具与资源/templates_area]] — {{TITLE}}
- [[16-工具与资源/templates_idea]] — {{TITLE}}
- [[16-工具与资源/templates_monthly-review]] — Monthly Review {{YEAR}}-{{MONTH}}
- [[16-工具与资源/templates_project]] — {{TITLE}}
- [[16-工具与资源/templates_weekly-review]] — Weekly Review {{WEEK}}
- [[09-技能库/obsidian/SKILL]] — Obsidian
- [[09-技能库/self-improving/heartbeat-rules]] — Heartbeat Rules
- [[09-技能库/self-improving/operations]] — Memory Operations
- [[CONVENTIONS]] — Writing & Agent Conventions
- [[_graph]] — Knowledge Graph

<!-- AI-LINKS-END -->
