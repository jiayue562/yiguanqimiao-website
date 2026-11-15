# 质量规则

> 龙心 OS · LLM Wiki Schema 配置层

---

## 编译质量

| 规则 | 说明 | 检查方式 |
|------|------|---------|
| 原始完整性 | 原始资料不可删减修改 | 哈希校验 |
| 概念准确性 | 提取概念需精确反映原文语义 | LLM 自检 |
| 链接充分性 | 每页面最少 3 个双向链接 | lint 检查 |
| 版本标注 | 标注来源 URL 和归档时间 | 元数据检查 |

## 页面质量

| 指标 | 标准 | 检查频率 |
|------|------|---------|
| 内容准确性 | 定义无冲突、引用源可追溯 | 每次编译 |
| 结构清晰性 | 使用标准模板、标题层级合理 | 每周 |
| 链接有效性 | 所有 [[链接]] 可导航到目标页 | 每日 |
| 更新时效性 | 超过 90 天未更新需复审 | 每月 |

## 健康评分公式

```
健康分 = 链接率×40% + (1-孤立率)×30% + min(平均链接数/3,1)×30%
优秀 ≥ 85, 良好 ≥ 70, 需改进 ≥ 55, 关注 < 55
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/agents_LLM Wiki 知识库激活完成报告]] — LLM Wiki 知识库激活完成报告
- [[02-信仰文化体系/项目实践_02-03-经验总结]] — 02-03-经验总结
- [[16-工具与资源/工具脚本_知识库验证系统]] — 🤖 知识库验证系统
- [[05-五行人格心理学/00-入口/附录A-Obsidian标准模板]] — 附录A：Obsidian知识文档标准模板
- [[08-龙心OS核心系统/AI-OS知识库/🧠 龙脑OS·知识地基层/wiki·概念页/LLMification]] — LLMification（知识编译方法论）
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/lint-config]] — Linting 配置
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/reference/practice-guide]] — LLM Wiki 实操指南
- [[ψ技能体系/30-tools/knowledge-site-creator/references/seo-best-practices]] — SEO 最佳实践 - 知识网站优化指南

<!-- AI-LINKS-END -->
