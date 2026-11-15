# 上下文快照

**会话 ID**: {{session_id}}
**快照时间**: {{timestamp}}
**质量评分**: {{quality_score}}

## 上下文项
{% for item in context_items %}
- [{{item.priority}}] {{item.key}}: {{item.value[:100]}}...
{% endfor %}

## 摘要
{{summary}}

## 优化建议
{% for issue in issues %}
- {{issue}}
{% endfor %}

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[05-五行人格心理学/理论基石/系统配置_规则四_上下文压缩工程]] — 规则四：上下文压缩工程
- [[09-技能库/resources_snapshot-template]] — 上下文快照模板 v1
- [[09-技能库/上下文工程.skills/references/references/prompts]] — 上下文工程提示词模板
- [[09-技能库/上下文工程.skills/references/references/sop]] — 上下文工程标准操作流程
- [[09-技能库/上下文工程.skills/templates/context-snapshot]] — 上下文快照 · {项目名称}
- [[ψ技能体系/99-archive/上下文工程/templates/output-snapshot]] — 上下文快照: {{project_name}}

<!-- AI-LINKS-END -->
