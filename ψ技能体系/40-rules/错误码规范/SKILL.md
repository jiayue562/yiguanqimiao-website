---
name: 错误码规范
parent_skill: ai-os
description: 五段式错误码——AI OS统一错误码体系
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 错误码规范 v1.0

### 五段式格式
ERR-XXXXX-YY-ZZZ

| 段位 | 长度 | 说明 | 示例 |
|------|------|------|------|
| ERR | 3 | 固定前缀 | ERR |
| XXXXX | 5 | 模块编号 | DIAGN(诊断) |
| YY | 2 | 错误类型 | 01(输入) 02(处理) 03(输出) |
| ZZZ | 3 | 具体错误 | 001 |

### 常用错误码
| 错误码 | 说明 |
|--------|------|
| ERR-DIAGN-01-001 | 诊断输入数据格式错误 |
| ERR-DIAGN-02-001 | 诊断处理超时 |
| ERR-DISP-01-001 | 分派目标不存在 |
| ERR-GOV-03-001 | Agent未注册 |
| ERR-GOV-01-001 | 越权操作被拒绝 |
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙脑OS升级包：思维模型/龙脑动态组方引擎-开发文档]] — 龙脑动态组方引擎 · 开发文档
- [[01-核心体系/龙心OS_龙心OS-知行合一-五行人格OS整合方案v1.0]] — 龙心OS · 知行合一 · 五行人格OS 三大系统整合方案 v1.0
- [[01-核心体系/龙心OS_📖Harness-Engineering记忆层]] — Harness Engineering记忆层
- [[03-知识地基层/记忆系统_ERRORS]] — ERRORS.md - 错误记录与规避
- [[09-技能库/Harness-Engineering/references/memory-layer]] — Harness Engineering · 记忆层

<!-- AI-LINKS-END -->
