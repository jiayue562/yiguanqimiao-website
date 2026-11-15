# 宿主侧质检脚本与 FBS 报告落盘约定

> **背景**：部分宿主工作区会出现会话级 `qc-*.js` 等脚本，与 FBS 仓库内 `quality-auditor`、`run-p0-audits` 并行存在。为避免**两套口径互相打架**，约定如下。

## 1. FBS 权威输出（书稿根内）

| 产物 | 说明 |
|------|------|
| `.fbs/p0-audit-report.json` | `run-p0-audits.mjs` 结构化报告 |
| `.fbs/reports/` | **建议**宿主或会话质检将**摘要**写入此目录（若目录不存在可由 Agent 创建） |
| `.fbs/audit/*.jsonl` | 追溯轨迹，见 `fbs-continuous-improvement.md` |

## 2. 宿主会话 `qc-*` 脚本

若 WorkBuddy 工作区生成 `qc-ai-strict.js` 等文件：

- **不要**与 FBS「七锁 / S 层」定义冲突时仍声称「官方质检」；应在汇报中说明来源（会话工具 vs FBS 脚本）。
- 若需对用户展示单一结论：以 **`run-p0-audits` + quality 系列脚本** 为发版与复盘权威；宿主 qc 可作为补充。

## 3. 推荐文件名

- `qc-host-summary-<date>.md`（放在 `.fbs/reports/`）
- 内容至少含：执行时间、书稿根、结论摘要、与 `p0-audit-report` 是否一致

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/docs/history/SMART-MEMORY-ARCHITECTURE-v2.0.2]] — 智能记忆架构说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/memory-layer-matrix]] — 记忆分层与写入矩阵（策略 A / B / C 总览）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/qc-agent-briefing-template]] — 质检子智能体任务模板
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/quality-check]] — 去AI味审校体系与评分模型
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-continuous-improvement]] — 福帮手持续改进与进化门控（P0–P2 总览）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/lexicon-governance]] — 词表与质检规则演进治理（策略 C）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/teams-inbox-mapping]] — Teams 收件箱与福帮手编排对齐（策略 B）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/windows-host-cli]] — Windows / PowerShell 宿主与 Node 脚本输出
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/workbuddy-integration-checklist]] — WorkBuddy 审核 / 集成检查清单（FBS-BookWriter v2.1.2）

<!-- AI-LINKS-END -->
