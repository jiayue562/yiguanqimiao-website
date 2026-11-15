---
name: 部署规范
parent_skill: ai-os
description: 本地/云端/自动化+灰度——AI OS部署标准
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 部署规范 v1.0

### 部署环境

**本地开发**
- 路径：~/.agents/skills/
- opencode.json本地配置
- 直接修改+重启验证

**生产部署**
- 从WorkBuddy同步到opencode
- 灰度发布（先1台→再全部）
- 回滚预案准备

### 部署流程
1. 代码/配置变更
2. 本地测试（冒烟+单元+集成）
3. 灰度部署（1个Agent）
4. 验证通过
5. 全量部署
6. 回归测试
7. 文档同步

### 版本标签
部署时在opencode.json中添加version注释
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[03-知识地基层/记忆系统_browser-automation-solution]] — 🔧 Browser-Automation技能链接问题解决方案报告
- [[03-知识地基层/记忆系统_obsidian-backup-system]] — 🚀 WorkBuddy ↔ Obsidian 知识备份系统
- [[03-知识地基层/记忆系统_skills-sync-summary]] — Skills文档同步检查报告
- [[03-知识地基层/记忆系统_对话总结-2026-03-30-0942]] — 对话总结：WorkBuddy-Obsidian备份任务分析（2026-03-30 09:42）
- [[05-五行人格心理学/理论基石/系统配置_Obsidian知识库同步机制]] — 🔄 Obsidian知识库同步机制
- [[09-技能库/岗位智能体/v2.0/学习笔记]] — 岗位智能体 v1.0 → v2.0 改造清单 · 深度学习笔记

<!-- AI-LINKS-END -->
