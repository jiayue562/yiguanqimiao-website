# 上下文工程标准操作流程

## SOP-01：上下文优化
1. 接收输入（session_id, context_items, max_tokens）
2. prioritizer 按优先级排序
3. summarizer 生成摘要
4. optimizer 执行裁剪
5. scorer 质量评分
6. 输出优化后的上下文

## SOP-02：跨 Skills 上下文传递
1. 发起方调用 shared-store.set(namespace, data)
2. dependency-tracker 记录依赖关系
3. 接收方调用 shared-store.get(namespace)
4. 协议验证（protocol.md）
5. 注入到接收方 Prompt

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/上下文工程.skills/references/references/practice-guide]] — 上下文工程实践指南
- [[09-技能库/上下文工程.skills/references/references/prompts]] — 上下文工程提示词模板
- [[09-技能库/上下文工程.skills/references/references/sop]] — 上下文工程标准操作流程
- [[09-技能库/上下文工程.skills/references/references/theory]] — 上下文工程理论
- [[ψ技能体系/99-archive/上下文工程.skills/cross-skill-context/protocol]] — 跨 Skills 上下文统一协议 v1.0
- [[ψ技能体系/99-archive/上下文工程.skills/prompt-context/templates/README]] — Prompt 模板库
- [[ψ技能体系/99-archive/上下文工程.skills/references/practice-guide]] — 上下文工程实践指南
- [[ψ技能体系/99-archive/上下文工程.skills/references/prompts]] — 上下文工程提示词模板

<!-- AI-LINKS-END -->
