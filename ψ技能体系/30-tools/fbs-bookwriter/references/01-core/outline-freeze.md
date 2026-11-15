# 大纲冻结与变更单（防结构漂移）

> **版本**：2.1.2
> **机读字段**：`.fbs/project-config.json` → `outlineFreezeVersion` / `outlineFrozenAt` / `plannedChapterTotal` / `plannedChapterMin` / `plannedChapterMax`

---

## 1. 冻结含义

- **冻结**：目录级标题、章数规划、各章「要回答的一个问题」与用户收获点已确认，写入 `chapter-status` / 目录稿 / `project-config`。
- **冻结后**：不得静默改口径；任何结构变化须走 **变更单**。

---

## 2. 变更单（最小模板）

复制下列表格追加到 `.fbs/sessions-summary.md` 或单独 `outline-change-{YYYYMMDD}.md`：

| 字段 | 填写 |
|------|------|
| 变更 ID | OC-001 |
| 日期 | ISO |
| 原因 | 用户/市场/事实约束（一句话） |
| 变更前 | 章数 / 标题摘要 |
| 变更后 | 章数 / 标题摘要 |
| 对 `targetWordCount` 影响 | 增 / 减 / 不变（估字） |
| 是否已更新 `project-config` | 是 / 否 |
| 用户确认 | 已确认 / 待确认 |

---

## 3. 与阶段门禁的关系

- **S2 → S3**：须已冻结大纲或已登记带用户确认的变更单；`outlineFreezeVersion` 建议递增语义化版本（如 `2026-04-13.1`）。
- **并行写作**：team-lead 在派单前核对 `outlineFreezeVersion` 与 `book-context-brief` 一致。

---

## 4. 相关脚本

- `node scripts/writing-contract-gate.mjs --book-root <本书根>` — 校验字数/章数/区间一致性（Warning）。

返回主流程：[`section-3-workflow.md`](./section-3-workflow.md)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/information-ownership-and-arbitration]] — 信息产权、场景包坐标与记忆仲裁
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s2]] — S2 节点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/writing-phase-alert-tiers]] — 写作阶段告警分级（Blocker / Warning / Info）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-final-draft-governance]] — 终稿状态机与版本治理（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-narrative-gates-and-parity]] — 叙事门控与外部工作流对标（福帮手 × 工程化协作范式）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-source-of-truth-matrix]] — FBS-BookWriter 真源矩阵（发版与审计用）

<!-- AI-LINKS-END -->
