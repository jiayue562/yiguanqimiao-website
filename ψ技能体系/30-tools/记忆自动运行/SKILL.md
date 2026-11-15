---
name: 记忆自动运行系统
parent_skill: ai-os
description: 自主学习记忆全自动运行 — instinct 定时维护 + 会话生命周期 hook + 模式自动升级
version: 2.0
created: 2026-05-29
tags:
  - 记忆系统
  - instinct
  - 自动化
  - 自主学习
  - WorkBuddy
trigger: session-start, task-complete, session-end, scheduled-maintenance
---

# 记忆自动运行系统

> "每次对话都在积累智慧，每次错误都在训练模型。"
> 三层全自动记忆管道：后台定时维护 → 会话生命周期 hook → 模式自动升级

---

## 系统架构

```
┌──────────────────────────────────────────────────────────────────┐
│                     记忆自动运行系统 v2.0                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Layer 1      │    │  Layer 2      │    │  Layer 3      │       │
│  │  Windows      │    │  opencode     │    │  instinct     │       │
│  │  计划任务     │◄──►│  AGENTS.md    │◄──►│  模式引擎     │       │
│  │  (每 2h)      │    │  (每次会话)   │    │  (实时)        │       │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘       │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              memory-auto.ps1 统一维护脚本               │       │
│  │  consolidate → gc → backup → log                     │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                  │
│  WorkBuddy 记忆工具 ← (已自动运行)                                │
│  workbuddy_memory read/append + workbuddy_kb_search             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 三层自动运行机制

### Layer 1: 后台定时维护（Windows 计划任务）

| 任务名 | 触发 | 执行内容 | 状态 |
|--------|------|----------|------|
| InstinctMemoryAuto | 每 2 小时 | consolidate → gc → backup | 已注册 |
| InstinctMemoryAutoBackup | 每天 03:00 | 数据库备份 | 已注册 |

调用脚本：`~/.agents/scripts/memory-auto.ps1`

### Layer 2: AGENTS.md 会话生命周期 hook

| 时机 | 操作 | 说明 |
|------|------|------|
| 会话开始 | instinct session-summary | 查看昨日模式总结 |
| 会话开始 | instinct suggest | 获取成熟模式建议 |
| 任务完成 | instinct observe | 记录本次任务的模式 |
| 任务完成 | instinct consolidate | 触发模式自动升级 |
| 遇到错误 | instinct observe --cat fix_pattern | 记录修复方案 |
| 会话结束 | instinct consolidate | 确保模式升级 |
| 会话结束 | instinct gc | 垃圾回收 + 衰减 |

### Layer 3: instinct 模式引擎

#### 模式生命周期

```
observe (raw, conf=1)
  -> 重复 observe (confidence +1)
  -> threshold_mature=3 -> 升 mature
  -> threshold_rule=6 -> 升 rule (可导出)
  -> consolidate 自动触发升级
```

#### 置信度阈值（已优化）

| 参数 | 旧值 | 新值 | 效果 |
|------|------|------|------|
| threshold_mature | 5 | 3 | 观察 3 次即成熟 |
| threshold_rule | 10 | 6 | 观察 6 次成规则 |
| decay_days | 90 | 30 | 30 天不出现开始衰减 |
| hard_delete_days | 无 | 90 | 90 天不出现彻底删除 |

#### 模式分类

| 分类前缀 | --cat 值 | 用途 |
|----------|----------|------|
| task:* | sequence | 任务记录 |
| style:* | preference | 编码风格 |
| fix:* | fix_pattern | 修复方案 |
| seq:* | sequence | 操作序列 |
| pref:* | preference | 偏好选择 |
| error:* | fix_pattern | 错误处理 |

---

## 安装清单（检查用）

- [x] `~/.instinct/config.toml` -- 已优化阈值
- [x] `~/.agents/scripts/memory-auto.ps1` -- 统一维护脚本
- [x] Windows 计划任务 InstinctMemoryAuto -- 每 2 小时
- [x] Windows 计划任务 InstinctMemoryAutoBackup -- 每天 03:00
- [x] `~/.config/opencode/AGENTS.md` -- 已添加 instinct 自动调用规则
- [x] instinct MCP -- 已配置自动启动
- [x] WorkBuddy 记忆工具 -- 已自动运行

---

## 手动维护命令

```powershell
# 查看记忆系统状态
& "$env:USERPROFILE\.agents\scripts\memory-auto.ps1" -Mode status

# 执行完整维护
& "$env:USERPROFILE\.agents\scripts\memory-auto.ps1" -Mode full

# 仅 consolidate + gc
& "$env:USERPROFILE\.agents\scripts\memory-auto.ps1" -Mode quick

# 仅备份
& "$env:USERPROFILE\.agents\scripts\memory-auto.ps1" -Mode backup
```

---

## 故障排查

| 症状 | 排查步骤 |
|------|----------|
| instinct 命令找不到 | 检查 Get-Command instinct，重装 instinct |
| 计划任务不执行 | 检查任务状态：schtasks /Query /TN "InstinctMemoryAuto" |
| 模式不自动升级 | 运行 instinct consolidate 手动触发 |
| MCP 工具不显示 | 检查 opencode.json 中 memory MCP 是否 enabled: true |

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/MEMORY]] — MEMORY.md - 龙龟神将长期记忆
- [[01-核心体系/agents_龙心 OS 自主学习系统指令手册]] — 龙心 OS 自主学习系统 - 完整指令手册
- [[03-知识地基层/记忆系统_LEARNINGS]] — LEARNINGS.md - 学习积累与知识沉淀
- [[03-知识地基层/记忆系统_MEMORY]] — MEMORY.md - 记忆系统架构 v2.1
- [[03-知识地基层/记忆系统_记忆系统安装完成报告-v3.0]] — 记忆系统安装完成报告 v3.0
- [[21-学习档案/内容创作系统_CLAUDE]] — CLAUDE.md · 内容创作AI自动化配置

<!-- AI-LINKS-END -->
