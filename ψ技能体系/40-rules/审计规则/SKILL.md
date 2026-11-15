---
name: 审计规则
parent_skill: ai-os
description: 操作/决策/合规三维审计——确保AI OS所有操作可追溯
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 审计规则 v1.0

### 三维审计

**1. 操作审计**
- 记录所有Agent的每次操作
- 记录操作的输入、输出、耗时
- 记录操作所属的红绿灯区域

**2. 决策审计**
- 记录每次AI决策的依据和理由
- 记录人类确认/修改/驳回的决策
- 记录决策的最终结果和执行情况

**3. 合规审计**
- 检查Agent是否越权操作
- 检查数据访问是否在授权范围内
- 定期生成审计报告

### 审计日志格式
JSONL格式存储于 ~/.aios/audit_log.jsonl
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/04-Knowledge/六大OS_SKILL审计报告]] — 六大OS·SKILL全面审计报告
- [[13-WorkBuddy-Sync/05-味藏AI应用/味藏智能体总包_SKILL审计报告_第七步]] — 味藏智能体总包·SKILL全面审计报告
- [[13-WorkBuddy-Sync/06-工作记录与复盘/MEMORY]] — MEMORY.md - 龙龟神将长期记忆
- [[01-核心体系/agents_安全智能体模块]] — 安全智能体模块
- [[03-知识地基层/记忆系统_obsidian-skill-security-audit]] — 🔍 安全审计报告
- [[05-五行人格心理学/应用场景/企业管理/企业管理_分身理论应用]] — 分身理论应用

<!-- AI-LINKS-END -->
