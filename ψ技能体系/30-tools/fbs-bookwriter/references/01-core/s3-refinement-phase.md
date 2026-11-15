# S3.7 精修阶段（扩写后的润色与事实收口）

> **版本**：2.1.2  
> **定位**：位于 **S3.5 扩写** 之后、**S4 排版构建** 之前；与 S3.5 共用 `expansion-word-verify` 字数逻辑与 `iterationPhase: refinement`。

---

## 1. 何时进入 S3.7

- 扩写已达标，但需 **统一文风、压缩重复、补 MAT、对齐术语**；或用户明确说「精修 / 润色 / 收口事实」。

---

## 2. 门禁

| 门禁 | 要求 |
|------|------|
| **输入** | S3.5 已达标章节 + `book-context-brief.md` + `术语锁定记录.md` |
| **ESM** | `.fbs/esm-state.md` 中 `iterationPhase: refinement`；`refinementRound` 每轮精修 +1 |
| **并行** | 与 S3.5 相同：**写作类 ≤2 章** |
| **字数** | 精修后若变更幅度大，仍可用 `expansion-word-verify` 对「不低于 Brief 期望」做抽检 |

---

## 3. 质检

最低 **S + P**；涉及事实增删时 **+ C**；跨章重复抽检 **B**（相邻章）。

---

## 4. 台账

每轮精修结束更新 `chapter-status.md`；中断时记录 `lastInterruptAt` / `lastInterruptReason`。

---

## 5. 与 S4 的衔接

进入 S4 前：`iterationPhase` 可置回 `none`，或保留 `refinement` 直至全书精修完毕（由 team-lead 与用户对齐）。

返回：[`s3-expansion-phase.md`](./s3-expansion-phase.md) · [`workflow-s3-closure.md`](./workflow-volumes/workflow-s3-closure.md)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/expansion-fact-tagging]] — 扩写与精修中的事实标注（MAT / 待证实）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s0-material-phase-guard]] — S0 素材阶段 · 阶段守护与强制推进（防「无限 S0」）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-expansion-phase]] — S3.5 内容扩写阶段（初稿后的迭代扩写）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-3-workflow]] — 工作流设计（结构化入口，问题导向）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-4-commands]] — 短指令完整清单（§4 扩展版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-closure]] — S3 节点 — 收口规则
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-core]] — S3 节点 — 核心执行机制
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-writing-guide]] — S3 节点 — 写稿规范与 Brief 模板
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3]] — S3 节点 — 导航入口
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/book-level-consistency]] — 全书级一致性（C0 · 汇编门禁）

<!-- AI-LINKS-END -->
