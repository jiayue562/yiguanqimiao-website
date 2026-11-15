---
name: agent-memory-systems
parent_skill: ai-os
description: AI 智能体跨会话长期记忆系统。实现语义记忆 + 情景记忆 + 工作记忆三层架构，支持记忆编码、存储、检索、更新、遗忘全生命周期管理。
allowed-tools: read, write, edit, memory_search, memory_get
metadata:
  version: 2.0
  created: 2026-04-16
  enhanced: true
---

# Agent Memory Systems

> "记忆是智能体的基石——没有记忆，每次交互都从零开始。" — 基于 AI 记忆系统架构研究

**版本**: v2.0 (增强版)  
**创建**: 2026-04-16  
**标签**: #记忆系统 #长期记忆 #语义记忆 #情景记忆

---

## 📋 核心定义

**一句话定义**: AI 智能体跨会话长期记忆系统，实现语义记忆 + 情景记忆 + 工作记忆三层架构，支持记忆编码、存储、检索、更新、遗忘全生命周期管理。

**三行问题陈述**:
- **What**: 解决 AI 智能体会话间失忆、经验无法沉淀、知识无法复用的问题
- **Why**: 记忆是智能体的基石，没有记忆每次交互都从零开始
- **How**: 三层记忆架构 + 全生命周期管理 + 与 Skills 协同

---

## 🧠 三层记忆架构

```
┌─────────────────────────────────────────────────────────────┐
│                  AI 智能体记忆系统架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L2 长期记忆 (Long-Term Memory)                              │
│  ├── 语义记忆 (Semantic): 模式/规则/概念                     │
│  ├── 情景记忆 (Episodic): 经历/事件/日志                     │
│  └── 程序记忆 (Procedural): 技能/流程/方法                   │
│                                                             │
│  L1 会话记忆 (Session Memory)                                │
│  ├── SESSION.md: 当前会话上下文                              │
│  └── memory/YYYY-MM-DD.md: 日常记忆                          │
│                                                             │
│  L0 工作记忆 (Working Memory)                                │
│  ├── 当前任务状态                                            │
│  └── 短期缓存                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 记忆存储结构

### L2 长期记忆

**位置**: `memory/` + `MEMORY.md`

**语义记忆** (`memory/semantic/`):
```
memory/semantic/
├── patterns.json        # 模式库
├── rules.json           # 规则库
└── concepts.json        # 概念库
```

**情景记忆** (`memory/episodic/`):
```
memory/episodic/
├── learning-logs/       # 学习日志
├── project-logs/        # 项目日志
└── interaction-logs/    # 交互日志
```

**程序记忆** (`skills/`):
```
skills/
├── self-learning/       # 学习技能
├── self-improving/      # 优化技能
└── domain-skills/       # 领域技能
```

---

### L1 会话记忆

**位置**: `memory/YYYY-MM-DD.md` + `SESSION.md`

**日常记忆**:
```
memory/
├── 2026-04-13.md        # 第 1 天
├── 2026-04-15.md        # 第 2 天
├── 2026-04-16.md        # 第 3 天
└── ...
```

**会话上下文**:
```
SESSION.md               # 当前会话状态
```

---

### L0 工作记忆

**位置**: 内存缓存 + `memory/working/`

**当前任务**:
```
memory/working/
├── current-task.json    # 当前任务状态
├── short-term-cache/    # 短期缓存
└── context-window/      # 上下文窗口
```

---

## 🔄 记忆生命周期

### 编码 (Encoding)

**从经验到记忆**:
```
经历 → 提取关键信息 → 分类 (语义/情景/程序) → 编码存储
```

**编码规则**:
- 语义记忆：抽象为模式/规则
- 情景记忆：保留时间/地点/情感
- 程序记忆：记录步骤/条件/结果

---

### 存储 (Storage)

**存储策略**:
```
高频访问 → L0 工作记忆 (快速访问)
中频访问 → L1 会话记忆 (会话内访问)
低频访问 → L2 长期记忆 (持久存储)
```

**存储格式**:
- 语义记忆：JSON (结构化)
- 情景记忆：Markdown (可读性)
- 程序记忆：Skill 包 (可执行)

---

### 检索 (Retrieval)

**检索方式**:
```
语义检索 → memory_search (语义搜索)
精确检索 → memory_get (精确获取)
上下文检索 → SESSION.md (会话历史)
```

**检索优化**:
- 索引建立：关键词/标签/时间
- 缓存策略：高频内容缓存
- 关联检索：相关记忆联动

---

### 更新 (Update)

**更新触发**:
- 新经验积累
- 旧记忆修正
- 模式优化

**更新策略**:
```
增量更新：添加新内容
覆盖更新：替换旧内容
合并更新：整合多个来源
```

---

### 遗忘 (Forgetting)

**遗忘策略**:
```
自然遗忘：长期未访问 → 归档
主动遗忘：错误/过时 → 删除
选择性遗忘：低价值 → 压缩
```

**遗忘规则**:
- 90 天未访问 → 归档
- 确认错误 → 立即删除
- 低价值内容 → 压缩摘要

---

## 🎯 记忆操作 API

### 保存记忆

```
动作：save_memory
参数:
  - type: semantic|episodic|procedural
  - content: 记忆内容
  - tags: [标签列表]
  - priority: high|medium|low
```

**示例**:
```
保存语义记忆:
{
  "type": "semantic",
  "content": "五行分类规则",
  "tags": ["五行", "分类", "知识管理"],
  "priority": "high"
}
```

---

### 检索记忆

```
动作：search_memory
参数:
  - query: 搜索查询
  - type: semantic|episodic|procedural
  - limit: 结果数量
  - min_score: 最低相似度
```

**示例**:
```
搜索记忆:
{
  "query": "五行分类",
  "type": "semantic",
  "limit": 5,
  "min_score": 0.7
}
```

---

### 更新记忆

```
动作：update_memory
参数:
  - id: 记忆 ID
  - content: 新内容
  - merge_strategy: replace|merge|append
```

**示例**:
```
更新记忆:
{
  "id": "wuxing-classification-001",
  "content": "更新后的五行分类规则",
  "merge_strategy": "merge"
}
```

---

### 删除记忆

```
动作：delete_memory
参数:
  - id: 记忆 ID
  - reason: 删除原因
  - archive: true|false
```

**示例**:
```
删除记忆:
{
  "id": "outdated-rule-001",
  "reason": "规则已过时",
  "archive": true
}
```

---

## 🔗 与 Skills 协同

### self-learning 协同

**协同方式**:
```
self-learning 学习新技术
    ↓
创建技能 + 学习日志
    ↓
agent-memory-systems 归档
    ↓
语义记忆 + 情景记忆
```

**触发条件**: self-learning 完成学习

---

### self-improving-agent 协同

**协同方式**:
```
self-improving-agent 优化经验
    ↓
提取模式/规则
    ↓
agent-memory-systems 存储
    ↓
语义记忆更新
```

**触发条件**: self-improving 完成优化

---

### LLM Wiki 协同

**协同方式**:
```
LLM Wiki 编译知识
    ↓
三层架构 (原始/Wiki/Schema)
    ↓
agent-memory-systems 映射
    ↓
语义/情景/程序记忆
```

**触发条件**: LLM Wiki 完成编译

---

## 📊 记忆健康检查

### 检查指标

| 指标 | 计算方式 | 健康范围 |
|------|----------|----------|
| 记忆总量 | 总记忆条数 | 100-1000 条 |
| 检索成功率 | 成功检索/总检索 | >90% |
| 记忆更新率 | 月更新/总记忆 | 5-20% |
| 遗忘率 | 月遗忘/总记忆 | 2-10% |
| 重复率 | 重复记忆/总记忆 | <5% |

---

### 检查脚本

```powershell
# 记忆健康检查脚本
param(
    [string]$MemoryPath = "memory/",
    [int]$DaysThreshold = 90
)

# 1. 统计记忆总量
$totalMemories = (Get-ChildItem $MemoryPath -Recurse -File).Count

# 2. 检查未访问记忆
$oldMemories = Get-ChildItem $MemoryPath -Recurse -File | 
    Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$DaysThreshold) }

# 3. 检查重复记忆
# ...

# 4. 生成报告
Write-Host "记忆健康检查报告"
Write-Host "总记忆数：$totalMemories"
Write-Host "过期记忆：$($oldMemories.Count)"
```

---

## 🎯 应用场景

### 场景 1: 跨会话学习

```
会话 1: 学习 React Query
    ↓
保存语义记忆 (React Query 模式)
保存情景记忆 (学习日志)
    ↓
会话 2: 使用 React Query
    ↓
检索语义记忆 (应用模式)
参考情景记忆 (避免错误)
```

---

### 场景 2: 经验沉淀

```
项目完成
    ↓
提取经验教训
    ↓
保存语义记忆 (模式/规则)
保存情景记忆 (项目日志)
    ↓
未来项目参考
```

---

### 场景 3: 技能进化

```
技能使用
    ↓
收集反馈
    ↓
self-improving 优化
    ↓
agent-memory 存储新模式
    ↓
技能自动进化
```

---

## ⚠️ 关键规则

### 记忆质量规则

1. **准确性**: 记忆内容必须准确，定期验证
2. **时效性**: 标注时间戳，过时记忆标记
3. **可检索**: 建立索引，支持语义搜索
4. **去重**: 避免重复存储，合并相似记忆

### 记忆安全规则

5. **隐私保护**: 敏感信息加密存储
6. **权限控制**: 分级访问权限
7. **备份机制**: 定期备份记忆数据
8. **恢复能力**: 支持记忆恢复

---

## 📈 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 记忆检索速度 | <1 秒 | 平均检索时间 |
| 记忆准确率 | >95% | 检索结果准确率 |
| 跨会话复用率 | >50% | 记忆被复用比例 |
| 记忆更新及时性 | <24 小时 | 经验到记忆延迟 |
| 用户满意度 | >4/5 | 用户评分 |

---

## 🔄 版本迭代

| 版本 | 日期 | 改动 |
|------|------|------|
| v1.0 | 2026-04-13 | 初始版本，基础记忆架构 |
| v2.0 | 2026-04-16 | 增强版：三层架构 + 全生命周期 + Skills 协同 |

---

## 🔗 双向链接

### 向上链接
- [[00-索引与导航/AI统一索引/AI-总索引|01-龙心 OS 核心系统]] - 核心系统
- [[知识学习 Skill]] - 知识学习

### 平行链接
- [[09-技能库/self-improving-agent/README|self-improving-agent]] - 自我优化
- [[00-索引与导航/AI统一索引/AI-总索引|self-learning]] - 自主学习
- [[00-索引与导航/AI统一索引/AI-总索引|LLM Wiki 知识库管理]] - 知识编译
- [[00-索引与导航/AI统一索引/AI-总索引|super-save]] - 记忆保存
- [[00-索引与导航/AI统一索引/AI-总索引|super-search]] - 记忆搜索

### 向下链接
- [[记忆编码规范]] - 编码方法
- [[记忆检索指南]] - 检索方法

---

_创建：2026-04-16 · 基于 AI 记忆系统架构研究 v2.0_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/agents_龙心 OS 记忆系统架构]] — 龙心 OS 记忆系统架构
- [[03-知识地基层/五行分类/五行分类图谱全息阐释]] — 五行分类图谱全息阐释
- [[03-知识地基层/五行分类/五行系统总览]] — 五行系统总览
- [[03-知识地基层/五行分类/生克制化关系]] — 生克制化关系详解
- [[03-知识地基层/记忆系统_MEMORY]] — MEMORY.md - 记忆系统架构 v2.1
- [[03-知识地基层/象思维/核心方法]] — 象思维核心方法

<!-- AI-LINKS-END -->
