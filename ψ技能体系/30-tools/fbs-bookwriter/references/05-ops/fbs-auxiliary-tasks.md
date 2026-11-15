# 辅助模型适用任务（P2 C3）

当宿主提供**轻量/快速**模型通道时，建议将下列任务与「正文写作主模型」分离：

| 任务 | 输入 | 输出 | 说明 |
|------|------|------|------|
| 章前摘要 | 已读章节路径列表 | ≤500 字要点 | 降低主模型重复读全文 |
| 术语对齐表 | GLOSSARY + 当前章草稿 | 冲突列表 | 不直接改稿，只列问题 |
| 格式/结构检查 | 单章 Markdown | 问题清单 | 与 `quality-auditor-lite` 互补 |

未配置辅助模型时：**全部任务由主模型完成**，并遵守 `anti-stall` 与单轮文件修改上限。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workbuddy-agent-briefings]] — 宿主平台多智能体委托话术（S3 / S5）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/cross-chapter-consistency]] — 跨章一致性（全书 CX · 手册级）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/writing-phase-alert-tiers]] — 写作阶段告警分级（Blocker / Warning / Info）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-context-compression]] — 上下文压缩策略（P1 B1）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-optimization-roadmap-spec]] — FBS 优化路线图规格（P0–P2）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/multi-agent-horizontal-sync]] — 多智能体横向协同（架构模式 · 磁盘协议）

<!-- AI-LINKS-END -->
