# 上下文工程理论

## 核心命题
上下文工程是管理AI跨会话任务连续性的专业智能体。大模型如同操作系统，上下文窗口充当内存，上下文工程就是"内存管理器"。

## 四大失效模式
- 污染: 幻觉进入上下文
- 干扰: 模型降智
- 混淆: 冗余偏离期望
- 冲突: 信息互相矛盾

## LLM-aware分块
不是简单切割，而是语义切割+压缩+精确索引检索。

## GraphRAG三层匹配
1. 精确匹配 -> 2. LLM相似度 -> 3. 新建实体

## 自进化机制
"AI解决长尾 + 规则覆盖高频 + 二次深度分类与规则学习"闭环

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/AI-OS六层架构智能体/references/上下文工程层]] — 上下文工程层 v1.0
- [[09-技能库/LLM-Wiki/references/theory]] — LLM Wiki · 卡帕西体系完整理论 v1.0
- [[09-技能库/llmification-knowledge-builder/references/theory]] — Theory.md - LLMification 理论依据
- [[09-技能库/上下文工程.skills/references/theory]] — 上下文工程 · 理论基础
- [[09-技能库/上下文工程/上下文工程]] — 上下文工程 Skill
- [[09-技能库/知识学习Skills/references/llm-wiki-architecture]] — LLM Wiki三层知识流水线架构详解
- [[ψ技能体系/99-archive/上下文工程/SKILL]] — 上下文工程

<!-- AI-LINKS-END -->
