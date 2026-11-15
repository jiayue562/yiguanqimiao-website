# 工作流设计（结构化入口，问题导向）

> 说明：原 `section-3-workflow.md` 体量过大（>200KB），已做结构化瘦身，避免单文件读取失败。
> 
> 全量历史内容已保留至：[`section-3-workflow.full.md`](./section-3-workflow.full.md)

---

## 快速导航（按执行阶段）

- **S0 前置调研与检索基线**：参见 [`intake-and-routing.md`](./intake-and-routing.md)、[`../05-ops/search-policy.json`](../05-ops/search-policy.json)
- **S1 主题与边界确认**：参见 [`intake-and-routing.md`](./intake-and-routing.md)
- **S2 目录与章节规划**：参见 [`intake-and-routing.md`](./intake-and-routing.md)、[`session-protocols.md`](./session-protocols.md)
- **S2.5 风险核销与启动准备**：参见 [`../05-ops/multi-agent-horizontal-sync.md`](../05-ops/multi-agent-horizontal-sync.md)
- **S3 并行写作与门禁**：参见 [`../05-ops/multi-agent-horizontal-sync.md`](../05-ops/multi-agent-horizontal-sync.md)、[`../05-ops/platform-ops-brief.md`](../05-ops/platform-ops-brief.md)
- **S4 构建与排版**：参见 [`../05-ops/delivery-guide.md`](../05-ops/delivery-guide.md)、[`../03-product/06-typography.md`](../03-product/06-typography.md)
- **S5 终审与一致性**：参见 [`../02-quality/quality-check.md`](../02-quality/quality-check.md)、[`../02-quality/cross-chapter-consistency.md`](../02-quality/cross-chapter-consistency.md)
- **S6 转化与发布准备**：参见 [`section-s6-transformation.md`](./section-s6-transformation.md)

---

## 守卫链与审计入口（推荐）

- `npm run guard:s3:full -- --skill-root <技能根> --book-root <本书根>`
- `npm run audit:all -- --skill-root <技能根> --book-root <本书根> --strict`
- `npm run audit:broken-links`

> `audit:all` 默认包含断链强校验；紧急情况下可加 `--no-broken-links`。

---

## 为什么这样调整

1. 降低单文件上下文体积，避免工具读取超限。
2. 将“阶段入口”与“执行命令”前置，提升定位效率。
3. 全量历史内容不丢失，保留可追溯性。
4. 建议在每次里程碑后执行一次 `audit:all --strict`，及时暴露风险。

---

## 分卷阅读（推荐）

- [`workflow-volumes/workflow-s0.md`](./workflow-volumes/workflow-s0.md)
- [`workflow-volumes/workflow-s1.md`](./workflow-volumes/workflow-s1.md)
- [`workflow-volumes/workflow-s2.md`](./workflow-volumes/workflow-s2.md)
- [`workflow-volumes/workflow-s2.5.md`](./workflow-volumes/workflow-s2.5.md)
- [`workflow-volumes/workflow-s3.md`](./workflow-volumes/workflow-s3.md)
- [`workflow-volumes/workflow-s4.md`](./workflow-volumes/workflow-s4.md)
- [`workflow-volumes/workflow-s5.md`](./workflow-volumes/workflow-s5.md)
- [`workflow-volumes/workflow-s6.md`](./workflow-volumes/workflow-s6.md)

## 全量内容（保留）

- [`section-3-workflow.full.md`](./section-3-workflow.full.md)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/documentation-layers]] — 文档分层说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-refinement-phase]] — S3.7 精修阶段（扩写后的润色与事实收口）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-3-workflow.full]] — FBS-BookWriter 第 3 节（完整版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-nlu]] — NLU 指令系统（可执行版，问题导向）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-index]] — FBS-BookWriter 文档索引
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workbuddy-agent-briefings]] — 宿主平台多智能体委托话术（S3 / S5）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s2.5]] — S2.5 节点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-closure]] — S3 节点 — 收口规则
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s5]] — S5 节点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/cross-chapter-consistency]] — 跨章一致性（全书 CX · 手册级）

<!-- AI-LINKS-END -->
