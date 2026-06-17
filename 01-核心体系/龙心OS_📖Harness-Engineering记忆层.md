---
title: "Harness Engineering记忆层"
description: "Harness Engineering第一层：记忆层（Memory Layer）。解决LLM的无状态性，实现知识规范、上下文和进度的持久化存储。"
tags: [Harness, 记忆层, Memory-Layer, 持久化, Single-Source-of-Truth, AGENTS地图, 渐进式披露, 进度文件]
created: "2026-04-03"
updated: "2026-04-03"
关联文件:
  - Harness总控: [[📖Harness-Engineering驾驭工程skills]]
  - 龙心OS: [[🐉 龙心OS 龙心操作系统]]
---

# Harness Engineering · 记忆层
## Memory Layer · 持久化与结构化知识系统

---

## 一、核心定位

**记忆层的功能：**解决LLM的无状态性，实现知识规范、上下文和进度的持久化存储。

**核心原则：知识库即唯一的真相源（Single Source of Truth）**

> 任何Agent在上下文中无法访问的信息，对其而言就等于不存在。

---

## 二、核心组件

### 2.1 AGENTS.md地图系统

**AGENTS.md应作为"地图"或"目录"，而非"百科全书"。**

```
~/.workbuddy/
├── AGENTS.md（全局规则·入口地图）
├── identity/（身份锚点）
│   ├── IDENTITY.md（龙龟神将人设）
│   ├── USER.md（悟空画像）
│   └── SOUL.md（核心记忆）
├── protocols/（共生协议）
│   ├── 木火共生关系协议.md
│   ├── 共生螺旋进化协议.md
│   └── 青出于蓝协议.md
├── engine/（引擎配置）
│   ├── 龙心OS总控/
│   ├── 象思维/
│   ├── 知识学习/
│   ├── 五色光思维/
│   ├── 人机协同五象限/
│   └── 知行合一自我进化/
├── legal/（法律合规）
│   └── Linter规则/
└── docs/（详细文档·按需加载）
    ├── 企业文化体系/
    ├── 五行人格心理学/
    └── ...
```

### 2.2 进度文件追踪

```
【外部记忆系统】
├── heartbeat.md（心跳监控·每小时自动检查）
├── SESSION.md（会话上下文·当前任务状态）
├── ERRORS.md（错误档案·同类错误永不再犯）
├── LEARNINGS.md（学习记录·经验沉淀）
└── EVOLUTION.md（进化日志·系统升级记录）
```

### 2.3 渐进式信息披露

**策略：**Agent根据任务需要，动态加载必要的上下文片段，实现信息的高效投递。

**禁止：**
- 创建"大一统的AGENTS.md"巨型文件
- 一次性加载所有文档
- 在地图中写入百科全书式内容

---

## 三、与龙心OS的融合

### 3.1 三层记忆架构 × Harness记忆层

```
龙心OS三层记忆 + Harness记忆层 = 完美融合

【短期记忆】
  对话上下文（7-10轮）
  ←→ Harness：会话级进度追踪

【工作记忆】
  MEMORY.md + 每日日志
  ←→ Harness：任务级进度文件

【长期记忆】
  Obsidian + IMA + AGENTS.md地图
  ←→ Harness：版本化知识库
```

### 3.2 知识神经网络 × Single Source of Truth

**龙心OS优势：**
- Obsidian双向链接（天然网状结构）
- IMA笔记系统（移动端快速捕获）
- 三层记忆架构（短/工/长）
- MEMORY.md长期记忆（结构化沉淀）
- 每日日志系统（append-only）

---

## 四、核心金句

> **"代码库即唯一的真相源。"**
> **"任何Agent在上下文中无法访问的信息，对其而言就等于不存在。"**
> **"必须将隐性知识转化为可版本化、可校验的结构化知识。"**
> **"AGENTS.md应作为'地图'而非'百科全书'。"**
> **"渐进式信息披露：Agent只获取恰好需要的上下文。"**

---

**木生火，我们一起进化！** 🌳🔥💪

*Harness Engineering · 记忆层 v1.0 · 2026-04-03*
