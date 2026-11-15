# 上下文工程实践指南

## 典型场景

### 场景1：长会话优化
会话超过 30 轮时，使用 summarizer 生成摘要，prioritizer 决定保留哪些上下文。

### 场景2：跨 Skills 调用
agent-memory-systems -> 上下文工程 -> LLM Wiki，协议统一传递。

### 场景3：质量门禁
每次上下文变更后，通过 scorer 评分，低于 60 分自动触发优化。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[05-五行人格心理学/理论基石/系统配置_规则四_上下文压缩工程]] — 规则四：上下文压缩工程
- [[09-技能库/上下文工程.skills/references/practice-guide]] — 上下文工程 · 实操指南
- [[09-技能库/上下文工程.skills/references/references/sop]] — 上下文工程标准操作流程
- [[ψ技能体系/99-archive/上下文工程.skills/cross-skill-context/protocol]] — 跨 Skills 上下文统一协议 v1.0
- [[ψ技能体系/99-archive/上下文工程.skills/references/practice-guide]] — 上下文工程实践指南
- [[ψ技能体系/99-archive/上下文工程.skills/references/sop]] — 上下文工程标准操作流程

<!-- AI-LINKS-END -->
