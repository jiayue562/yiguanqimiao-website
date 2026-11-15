---
name: 数据备份规则
parent_skill: ai-os
description: 六向同步+三级备份——AI OS数据安全保障
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 数据备份规则 v1.0

### 六向同步
- WorkBuddy ↔ Obsidian ↔ IMA ↔ GitHub ↔ Cloudflare Pages ↔ pages.dev

### 三级备份
**L1 日常备份（每日）**
- 配置文件备份
- SKILL.md变更备份
- 审计日志备份

**L2 周备份（每周）**
- 全量SKILL目录备份
- opencode.json配置备份
- 状态文件备份

**L3 月备份（每月）**
- 全量系统状态快照
- 跨平台一致性校验
- 归档至冷存储

### 备份位置
~/.aios/backups/
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-27]] — 2026-06-27 工作日志
- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[03-知识地基层/记忆系统_obsidian-backup-system]] — 🚀 WorkBuddy ↔ Obsidian 知识备份系统
- [[20-工作记录与复盘/01-每日归档/2026-04-08_每日备份报告]] — 2026-04-08 每日备份报告
- [[20-工作记录与复盘/02-每日日志/2026-04-14]] — 2026-04-14 每日日志
- [[20-工作记录与复盘/2026-08/三日沟通汇总-0825-0827]] — 以观其妙书院 · 三日沟通汇总（2026-08-25 ~ 08-27）

<!-- AI-LINKS-END -->
