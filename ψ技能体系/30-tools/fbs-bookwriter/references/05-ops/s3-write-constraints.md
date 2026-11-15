# S3 写作阶段写入约束（规范真值）

> 与根目录 [`fbs-runtime-hints.json`](../../fbs-runtime-hints.json) 中 `s3` 字段一致。

| 约束 | 值 | 说明 |
|------|-----|------|
| 每轮最多修改文件数 | `maxFilesModifiedPerTurn`（默认 2） | 与 SKILL 速查表一致 |
| 串行修改 | `serialEdits: true` | 完成其一再处理下一文件 |
| 修改前可见性 | `visibilityBeforeEdit: true` | 先说明改哪些文件与范围 |

宿主或模型应优先遵守 `fbs-runtime-hints.json`；本文件为可读说明，**非**运行时强制引擎。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/runtime-mandatory-contract]] — 运行时强制契约（主 Agent / 宿主对齐）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-refinement-phase]] — S3.7 精修阶段（扩写后的润色与事实收口）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/writing-phase-alert-tiers]] — 写作阶段告警分级（Blocker / Warning / Info）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/anti-stall-guide]] — 防卡顿执行指南
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-context-compression]] — 上下文压缩策略（P1 B1）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-subtask-contract]] — 长任务 / 辅助子任务机读契约（FBS）

<!-- AI-LINKS-END -->
