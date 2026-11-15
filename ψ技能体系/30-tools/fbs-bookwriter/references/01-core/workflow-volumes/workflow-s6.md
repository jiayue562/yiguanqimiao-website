# S6 分卷说明

> 本分卷面向 S6 阶段。目标不是把作品丢出书房，而是把书稿从**虚拟书房的完成区**推进到**虚拟书房的转化区**，并在需要时继续推进到**发布区**，形成可传播、可产品化、可外部使用且可回流修订的成果。

## S6 目标

- 明确本轮转化目标。
- 沉淀可复用的转化资产，并在需要时关联 S5 交付物。
- 把转化结果映射回资产面板。
- 在发布区记录外部使用状态与反馈闭环。
- 给出下一步执行动作。

## 必备输入

- 已完成的章节状态台账。
- 已通过的质量检查结果。
- 当前版本的发布范围说明。

## 必备输出

- `[S6]-content-units.md`：内容单元清单。
- `[S6]-product-roadmap.md`：产品化路线图。
- `story-bank.md`：故事库归档状态更新。
- `sessions-summary.md`：追加 S6 决策记录与后续动作。
- `[S6]-release-map.md`：发布映射内部台账（按需，但进入发布区时必须生成）。
- `releases/<chapterId>-release.json`：发布区初始清单，记录待发布状态、交付物引用与渠道信息。

## 执行顺序

1. 读取 `chapter-status.md` 与 `.fbs/chapter-status.md`。
2. 核对完成度、风险项、未闭环事项。
3. 生成内容单元与路线图草案。
4. 更新 `story-bank.md` 归档状态，并向 `sessions-summary.md` 追加本轮 S6 决策摘要。
5. 复核后将内部转化记录落盘到 `.fbs/`，将对外交付物保持在 `deliverables/`。
6. 若存在可外用成果，补做发布映射，并同步写入 `releases/` 的发布区初始状态。
7. 发生真实外部使用后，按 `待发布 → 已发布 → 反馈中 → 回流修改` 四态更新发布区记录。

## 通过标准

- 状态结论清晰。
- 输出文件齐全。
- 发布状态可追踪。
- 风险与后续动作可执行。
- 若发生反馈回流，能明确回到转化区或写作区的后续动作。

## 关联文档

- `references/01-core/section-s6-transformation.md`
- `references/05-ops/search-policy.json`
- `references/02-quality/quality-check.md`

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[02-信仰文化体系/项目实践_02-03-经验总结]] — 02-03-经验总结
- [[03-知识地基层/建设完成报告]] — 03-知识地基层建设完成报告
- [[05-五行人格心理学/理论基石/系统配置_Skills技能系统架构]] — 🛠️ Skills技能系统完整架构
- [[09-技能库/五行人格心理学/五行人格总智能体/金行人分智能体/references/拔阴取阳-金行人专用-知识学习成果]] — 金行人拔阴取阳体系 · 知识学习成果
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-8-onboarding]] — 新手引导体系（§8 完整版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-s6-transformation]] — S6 知识产品转化执行规范

<!-- AI-LINKS-END -->
