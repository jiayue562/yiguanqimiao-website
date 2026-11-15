# 福帮手持续改进与进化门控（P0–P2 总览）

> 与 `fbs-runtime-hints.json` 中 `evolutionGate` / `trace` 对齐；发版前与 `pack:skill-gates` 同级执行 `evolution-gate`。

## 轨迹（A2）

- 事件写入：`bookRoot/.fbs/audit/trace-YYYY-MM-DD.jsonl`
- Schema：`references/05-ops/fbs-trace-events.schema.json`
- 覆盖入口：`intake-router`、`session-exit`、`record-search-preflight`

## 书稿索引（A1）

- 全局登记：`~/.workbuddy/fbs-book-projects.json`（`session-exit` 成功时）
- 本书关键词：`bookRoot/.fbs/index/book-snippet.json`（`intake` / `session-exit` 维护）
- 统一检索：`intake-router --search` → `searchUnifiedBookRoots`

## 进化门控（A3）

- 清单：`scripts/generated/scripts-manifest.json`（`node scripts/generate-scripts-manifest.mjs`）
- 门禁：`node scripts/evolution-gate.mjs`（打包前由 `pack-skill-gates` 调用）
- 严格模式：`FBS_STRICT_EVOLUTION=1` 时若 `references/` 有未提交变更则失败

## 提案（C1）

- `node scripts/evolution-propose.mjs --book-root <书稿根>` → `.fbs/evolution/proposal-*.md` 草稿，**须人工审核**后再改仓库规范。

## 实验（C2）

- 影子规则建议目录：`bookRoot/.fbs/experiments/`（文件名自说明，不自动晋升）

## 辅助模型（C3）

- 任务列表见 `fbs-auxiliary-tasks.md`；路由由宿主实现，技能侧只约定用途边界。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/runtime-mandatory-contract]] — 运行时强制契约（主 Agent / 宿主对齐）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-cli-bridge-matrix]] — Skill ↔ 脚本 ↔ CLI 联动矩阵（非 MCP）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/03-product/NS08213-07-ux-design]] — UX 设计规范（对话层防卡顿 · 流畅度设计）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-performance-ux]] — 体验与防卡顿专项（性能 / 价值显性化）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-source-of-truth-matrix]] — FBS-BookWriter 真源矩阵（发版与审计用）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/host-qc-and-fbs-reports]] — 宿主侧质检脚本与 FBS 报告落盘约定
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/lexicon-governance]] — 词表与质检规则演进治理（策略 C）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/release-checklist]] — 发版与主包策略核对清单
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/windows-host-cli]] — Windows / PowerShell 宿主与 Node 脚本输出
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/workbuddy-integration-checklist]] — WorkBuddy 审核 / 集成检查清单（FBS-BookWriter v2.1.2）

<!-- AI-LINKS-END -->
