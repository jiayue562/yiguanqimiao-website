---
name: 版本管理规则
parent_skill: ai-os
description: Semantic Versioning三轨制——SKILL版本管理规范
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 版本管理规则 v1.0

### 三轨制版本号
格式：MAJOR.MINOR.PATCH (如 v2.1.3)

- MAJOR：重大重构、不兼容变更（架构升级）
- MINOR：新增功能、兼容性增强（新引擎/新域）
- PATCH：Bug修复、文档更新、性能优化

### 版本文件
- SKILL.md 头部 version 字段
- CHANGELOG.md 记录每次变更

### 版本流转
开发版 → 内部评审 → RC版 → 正式发布 → 归档
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[12-AIOS经验卡/EXP-20260909-03]] — 改版本号前先 grep changelog 头部
- [[01-核心体系/AI智能体_01-AI与智能体]] — 01-AI与智能体
- [[03-知识地基层/记忆系统_ERRORS]] — ERRORS.md - 错误记录与规避
- [[21-学习档案/内容创作系统_迭代日志]] — 迭代日志 · 方法论进化记录
- [[09-技能库/AI-OS六层架构智能体/triggers/auto-trigger]] — AI-OS六层架构智能体 · 自动触发规则
- [[ψ技能体系/30-tools/fbs-bookwriter/CHANGELOG]] — 变更日志

<!-- AI-LINKS-END -->
