# Linting 配置

> 龙心 OS · LLM Wiki Schema 配置层

---

## 检查项目

| 类别 | 检查项 | 严重度 | 自动修复 |
|------|--------|--------|---------|
| 一致性 | 概念定义是否冲突 | 高 | 否(需审核) |
| 一致性 | 链接是否有效 | 中 | 是 |
| 一致性 | 引用是否准确 | 中 | 否(需审核) |
| 完整性 | 缺失的概念页面 | 中 | 是(生成骨架) |
| 完整性 | 未建立的链接 | 低 | 是(推荐链接) |
| 完整性 | 过时信息(>90天) | 低 | 否(标记待审) |
| 质量 | 页面可读性 | 低 | 否(需人工) |
| 质量 | 链接密度 | 中 | 是(推荐补充) |
| 质量 | 更新频率 | 低 | 否(统计报告) |

## 修复策略

1. **自动修复**：链接失效 → 删/补；格式错误 → 修正；缺失骨架 → 生成
2. **人工审核**：定义冲突 → 标记+通知；引证错误 → 标记；过时信息 → 标记

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[01-核心体系/agents_LLM Wiki 知识库激活完成报告]] — LLM Wiki 知识库激活完成报告
- [[16-工具与资源/工具脚本_README]] — 验证工具目录
- [[16-工具与资源/工具脚本_知识库验证系统]] — 🤖 知识库验证系统
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/quality-rules]] — 质量规则
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/triggers]] — 触发规则
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-linting/SKILL]] — LLM Wiki Linting Skill
- [[ψ技能体系/40-rules/质量门禁规则/SKILL]] — SKILL

<!-- AI-LINKS-END -->
