---
name: 日志规范
parent_skill: ai-os
description: 操作/决策/错误/进化四类日志——AI OS日志统一规范
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 日志规范 v1.0

### 四类日志

**1. 操作日志**
记录Agent每次操作的详细信息
格式：[timestamp] [agent_id] [action] [input_summary] [output_summary] [zone] [status]

**2. 决策日志**
记录AI决策过程和人类反馈
格式：[timestamp] [decision_id] [issue] [ai_proposal] [human_decision] [reason]

**3. 错误日志**
记录系统和Agent的运行异常
格式：[timestamp] [error_code] [module] [message] [traceback]

**4. 进化日志**
记录AI OS的迭代和升级
格式：[timestamp] [version] [change_type] [description] [author]

### 日志存储
~/.aios/logs/
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙脑OS升级包：思维模型/龙脑动态组方引擎-开发文档]] — 龙脑动态组方引擎 · 开发文档
- [[01-核心体系/龙心OS_📖Harness-Engineering执行层]] — Harness Engineering执行层
- [[01-核心体系/龙心OS_📖Harness-Engineering编排层]] — Harness Engineering编排层
- [[09-技能库/ghost-scan-deps/agents/analyze/template-finding]] — SCA Finding: <vuln_id> in <package_name>
- [[09-技能库/resources_evolution-log]] — 龙心OS · 系统进化日志规范
- [[ψ技能体系/30-tools/mcp-builder/reference/mcp_best_practices]] — MCP Server Best Practices

<!-- AI-LINKS-END -->
