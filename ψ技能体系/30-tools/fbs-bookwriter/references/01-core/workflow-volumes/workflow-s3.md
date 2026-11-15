# S3 节点 — 导航入口

> 本文件为 S3 阶段总索引。内容已拆分为三个子卷，请按需加载，避免一次性加载全部内容。

## 子卷导航

| 子卷 | 内容 | 何时加载 |
|------|------|---------|
| [`workflow-s3-core.md`](./workflow-s3-core.md) | 入口条件 · 联网超时处理 · Auto-Run 断点机制 · 骨架检测 · 台账实测 · 单章写稿流程 | **必读**，开始 S3 前加载 |
| [`workflow-s3-writing-guide.md`](./workflow-s3-writing-guide.md) | 写稿规范 · Chapter Brief / Report Brief 格式 · 单章清单 · 评分流程 · 进度汇报格式 | 进入正式写稿时加载 |
| [`workflow-s3-closure.md`](./workflow-s3-closure.md) | 收口工件清单 · 骨架汇总 · S3→S4 进入条件 | S3 全部章节写完时加载 |

> **防卡顿原则**：每次只加载当前阶段所需子卷；禁止一次性 `read_file` 全量加载三个子卷。

## S3.5 扩写（初稿后的加厚迭代）

若用户要求 **扩写 / 加厚 / 提高字数**：必读 [`../s3-expansion-phase.md`](../s3-expansion-phase.md)（计划门禁、并行≤2、`expansion-word-verify` 实测字数、扩写后质检）。

## S3.7 精修（扩写后的润色与事实收口）

若用户要求 **精修 / 润色 / 收口事实**：必读 [`../s3-refinement-phase.md`](../s3-refinement-phase.md)。

## 关联文档

- [`workflow-s0.md`](./workflow-s0.md) — 原料激活与联网查证
- [`workflow-s2.md`](./workflow-s2.md) — 目录规划
- [`workflow-s2.5.md`](./workflow-s2.5.md) — 节点确认
- [`workflow-s4.md`](./workflow-s4.md) — 排版构建
- [`../05-ops/large-scale-book-strategy.md`](../../05-ops/large-scale-book-strategy.md) — 大规模书稿策略（M1/M2/M3）

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-expansion-phase]] — S3.5 内容扩写阶段（初稿后的迭代扩写）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-refinement-phase]] — S3.7 精修阶段（扩写后的润色与事实收口）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s2]] — S2 节点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-closure]] — S3 节点 — 收口规则
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-core]] — S3 节点 — 核心执行机制
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-writing-guide]] — S3 节点 — 写稿规范与 Brief 模板

<!-- AI-LINKS-END -->
