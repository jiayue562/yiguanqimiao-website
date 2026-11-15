---
type: context-snapshot
project: "{{project_name}}"
timestamp: "{{timestamp}}"
status: "{{status}}"
---

# 上下文快照: {{project_name}}

## 项目信息
- **名称**: {{project_name}}
- **类型**: {{project_type}}
- **优先级**: {{priority}}

## 已完成事项
{{completed_items}}
累计进度: {{progress}}%

## 关键决策记录
| 决策 | 依据 | 时间 | 文件 |
{{decision_rows}}

## 待办事项
### 高优先级
{{high_todos}}
### 中优先级
{{medium_todos}}
### 低优先级
{{low_todos}}

## 关键上下文
- **核心概念**: {{core_concepts}}
- **重要数据**: {{key_data}}
- **相关文件**: {{related_files}}

## AI记忆状态
- **加载Skills**: {{loaded_skills}}
- **激活引擎**: {{active_engines}}
- **知识库引用**: {{kb_refs}}

## 风险提示
{{risk_rows}}

## 会话摘要
- **核心产出**: {{core_output}}
- **下一步**: {{next_suggestion}}
- **需确认**: {{pending_confirms}}

## 接力说明
- **恢复方式**: 加载本快照到上下文
- **相关快照**: {{related_snapshots}}

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[16-工具与资源/templates_weekly-review]] — Weekly Review {{WEEK}}
- [[08-龙心OS核心系统/记忆系统/SESSION]] — SESSION.md - 会话上下文
- [[09-技能库/resources_snapshot-template]] — 上下文快照模板 v1
- [[09-技能库/上下文工程.skills/templates/context-snapshot]] — 上下文快照 · {项目名称}
- [[09-技能库/上下文工程/上下文工程]] — 上下文工程 Skill
- [[ψ技能体系/99-archive/上下文工程.skills/templates/output-snapshot]] — 上下文快照
- [[ψ技能体系/99-archive/上下文工程/references/prompts]] — 提示词模板
- [[ψ技能体系/99-archive/上下文工程/references/sop]] — SOP

<!-- AI-LINKS-END -->
