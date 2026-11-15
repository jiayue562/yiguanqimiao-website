# 跨 Skills 上下文统一协议 v1.0

## 协议格式
```json
{
  "protocol_version": "1.0",
  "source_skill": "str",
  "target_skill": "str",
  "context": {
    "session_id": "str",
    "items": [{"key": "str", "value": "str", "priority": 1-5}]
  }
}
```

## 传输规则
1. 发起方调用 shared-store.set(namespace, data)
2. dependency-tracker 记录调用链
3. 接收方通过 shared-store.get(namespace) 读取

## 当前注册的 Skills
| Skill | namespace | 版本 |
|-------|-----------|------|
| 上下文工程 | context-engineering | v1.0 |
| agent-memory-systems | agent-memory | v1.0 |
| LLM Wiki 知识库 | llm-wiki | v2.0 |
| knowledge-base-manager | kb-manager | v1.0 |

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[03-知识地基层/记忆系统_AGENTS]] — AGENTS.md - 智能体配置
- [[08-龙心OS核心系统/记忆系统/TOOLS]] — TOOLS.md - 可用的工具与技能（龙龟神将工具库）
- [[09-技能库/llmification-knowledge-builder/references/theory]] — Theory.md - LLMification 理论依据
- [[09-技能库/上下文工程.skills/references/references/practice-guide]] — 上下文工程实践指南
- [[09-技能库/上下文工程.skills/references/references/sop]] — 上下文工程标准操作流程
- [[ψ技能体系/99-archive/上下文工程.skills/references/sop]] — 上下文工程标准操作流程

<!-- AI-LINKS-END -->
