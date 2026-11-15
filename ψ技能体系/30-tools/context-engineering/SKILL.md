---
name: context-engineering
parent_skill: ai-os
description: 上下文工程引擎 - 管理 AI 对话上下文的优化、摘要、注入、评估全生命周期。实现会话上下文管理、Prompt 上下文工程、跨 Skills 上下文协同和质量评估四大核心功能，确保每次对话都有高质量上下文支持。
allowed-tools: read, write, edit, memory_search, memory_get, sessions_list, sessions_history
metadata:
  version: 1.0
  created: 2026-04-16
  based_on: 上下文工程最佳实践 + Skill Builder 5 阶 20 步
 协同 skills:
    - agent-memory-systems
    - llm-wiki-knowledge-base
    - knowledge-base-manager
    - self-learning
    - super-save
    - super-search
---

# Context Engineering - 上下文工程引擎

> "上下文质量决定 AI 对话质量——好的上下文工程让 AI 更懂你。" — 基于上下文工程最佳实践

**版本**: v1.0  
**创建**: 2026-04-16  
**标签**: #上下文工程 #会话管理 #Prompt 优化 #质量评估

---

## 📋 核心定义

**一句话定义**: 上下文工程引擎是管理 AI 对话上下文优化、摘要、注入、评估全生命周期的核心系统，确保每次对话都有高质量上下文支持。

**三行问题陈述**:
- **What**: 解决上下文碎片化、质量不可控、跨 Skills 协同困难的问题
- **Why**: 上下文质量直接决定 AI 对话质量，需要系统化管理
- **How**: 四大核心功能（会话管理 + Prompt 工程 + 跨 Skills 协同 + 质量评估）

---

## 🎯 核心能力

### 能力 1: 会话上下文管理
- 上下文优化器：压缩冗余，保留关键信息
- 上下文摘要：自动生成会话摘要
- 上下文优先级：智能排序上下文重要性

### 能力 2: Prompt 上下文工程
- Prompt 模板库：标准化 Prompt 模板
- 上下文注入：智能注入相关上下文
- A/B 测试：Prompt 效果对比测试

### 能力 3: 跨 Skills 上下文协同
- 统一协议：标准化上下文协议
- 共享存储：跨 Skills 上下文共享
- 依赖追踪：上下文依赖关系管理

### 能力 4: 质量评估
- 质量评分：上下文质量量化评估
- 健康检查：定期上下文健康扫描
- 优化建议：自动生成优化方案

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│              Context Engineering 架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  会话上下文管理层                                            │
│  ├── optimizer.py: 上下文优化器                             │
│  ├── summarizer.py: 上下文摘要                              │
│  └── prioritizer.py: 上下文优先级                           │
│                                                             │
│  Prompt 上下文工程层                                          │
│  ├── templates/: Prompt 模板库                               │
│  ├── injector.py: 上下文注入                                │
│  └── ab-test.py: A/B 测试                                   │
│                                                             │
│  跨 Skills 上下文协同层                                       │
│  ├── protocol.md: 统一协议                                  │
│  ├── shared-store.py: 共享存储                              │
│  └── dependency-tracker.py: 依赖追踪                        │
│                                                             │
│  质量评估层                                                  │
│  ├── scorer.py: 质量评分                                    │
│  ├── checker.py: 健康检查                                   │
│  └── optimizer.py: 优化建议                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 核心工作流程

### 流程 1: 会话上下文优化

```
会话开始 → 加载上下文 → 优先级排序 → 压缩摘要 → 注入对话
    ↓           ↓           ↓           ↓           ↓
初始化    从记忆系统    按重要性    去除冗余    优化 Prompt
```

**详细步骤**:
1. **加载上下文**: 从 agent-memory-systems 加载相关记忆
2. **优先级排序**: 使用 prioritizer 评估上下文重要性
3. **压缩摘要**: 使用 summarizer 生成简洁摘要
4. **优化处理**: 使用 optimizer 去除冗余信息
5. **注入对话**: 将优化后的上下文注入当前对话

---

### 流程 2: Prompt 上下文注入

```
用户请求 → 分析需求 → 检索上下文 → 选择模板 → 注入上下文 → 生成 Prompt
    ↓           ↓           ↓           ↓           ↓           ↓
输入    理解意图    从 Wiki/记忆    匹配模板    智能注入    优化输出
```

**详细步骤**:
1. **分析需求**: 理解用户请求的核心意图
2. **检索上下文**: 从 LLM Wiki 和记忆系统检索相关知识
3. **选择模板**: 从模板库选择最匹配的 Prompt 模板
4. **注入上下文**: 使用 injector 智能注入相关上下文
5. **生成 Prompt**: 生成优化的最终 Prompt

---

### 流程 3: 跨 Skills 上下文协同

```
Skill A 请求 → 检查协议 → 访问共享存储 → 获取上下文 → 返回结果
    ↓           ↓           ↓           ↓           ↓
请求    验证权限    查询存储    提取数据    响应
```

**详细步骤**:
1. **请求验证**: 检查请求 Skill 的权限
2. **协议检查**: 验证符合统一协议规范
3. **共享访问**: 访问 shared-store 获取上下文
4. **依赖追踪**: 记录上下文依赖关系
5. **返回结果**: 返回所需的上下文数据

---

### 流程 4: 质量评估与优化

```
定期扫描 → 质量评分 → 健康检查 → 生成报告 → 优化建议
    ↓           ↓           ↓           ↓           ↓
触发    量化评估    问题检测    可视化    改进方案
```

**详细步骤**:
1. **定期扫描**: 定时触发上下文质量检查
2. **质量评分**: 使用 scorer 量化评估上下文质量
3. **健康检查**: 使用 checker 检测问题
4. **生成报告**: 生成可视化质量报告
5. **优化建议**: 自动生成改进方案

---

## 📁 目录结构

```
context-engineering/
├── SKILL.md                          # 本技能定义
│
├── session-context/                  # 会话上下文管理
│   ├── optimizer.py                  # 上下文优化器
│   ├── summarizer.py                 # 上下文摘要
│   └── prioritizer.py                # 上下文优先级
│
├── prompt-context/                   # Prompt 上下文工程
│   ├── templates/                    # Prompt 模板库
│   │   ├── analysis-template.md      # 分析类 Prompt
│   │   ├── creation-template.md      # 创作类 Prompt
│   │   └── optimization-template.md  # 优化类 Prompt
│   ├── injector.py                   # 上下文注入
│   └── ab-test.py                    # A/B 测试
│
├── cross-skill-context/              # 跨 Skills 上下文协同
│   ├── protocol.md                   # 统一协议规范
│   ├── shared-store.py               # 共享存储
│   └── dependency-tracker.py         # 依赖追踪
│
├── quality-assessment/               # 质量评估
│   ├── scorer.py                     # 质量评分
│   ├── checker.py                    # 健康检查
│   └── optimizer.py                  # 优化建议
│
├── scripts/
│   ├── context-health-check.py       # 上下文健康检查
│   └── context-report.py             # 上下文报告
│
├── references/                       # 参考资料
│   ├── theory.md                     # 上下文工程理论
│   ├── practice-guide.md             # 实操指南
│   └── best-practices.md             # 最佳实践
│
├── templates/                        # 模板库
│   ├── input-template.md             # 输入模板
│   ├── output-template.md            # 输出模板
│   └── workflow-template.md          # 流程模板
│
└── triggers/                         # 触发配置
    ├── trigger-rules.yaml            # 触发规则
    ├── skill-routes.yaml             # Skills 协同路由
    └── auto-activate.json            # 自动触发配置
```

---

## 🎯 触发条件

### P0 直接触发（权重 5）
```
- 上下文优化
- 优化当前对话
- 上下文管理
- 上下文质量检查
- 上下文健康检查
- 生成上下文报告
```

### P1 场景触发（权重 4）
```
- "对话质量不高，优化一下"
- "上下文太长了，压缩一下"
- "帮我整理当前对话上下文"
- "检查上下文是否有问题"
- "如何改进 Prompt 效果"
```

### P2 信号触发（权重 3）
```
- "感觉 AI 不理解我"
- "对话有点混乱"
- "需要更好的上下文管理"
- "Prompt 效果不好"
```

---

## 🔗 与现有 Skills 协同

| Skill | 协同方式 | 说明 |
|-------|----------|------|
| **agent-memory-systems** | 上下文存储 | 使用记忆系统存储和管理上下文 |
| **llm-wiki-knowledge-base** | 知识上下文 | 从 Wiki 获取知识上下文 |
| **knowledge-base-manager** | 三库同步 | 同步三库上下文 |
| **self-learning** | 学习优化 | 学习上下文优化策略 |
| **super-save** | 快速保存 | 保存重要上下文 |
| **super-search** | 快速检索 | 检索历史上下文 |

### 协同流程图

```
用户请求
    ↓
context-engineering (主协调)
    ↓
┌───────────────────────────────────────┐
│           协同 Skills                  │
├───────────────────────────────────────┤
│ agent-memory-systems ← 加载记忆上下文  │
│ llm-wiki-knowledge-base ← 获取知识    │
│ knowledge-base-manager ← 同步三库     │
│ super-search ← 检索历史上下文         │
└───────────────────────────────────────┘
    ↓
上下文优化处理
    ↓
返回优化结果
```

---

## ⚠️ 使用边界

### ✅ 适用场景
- 需要优化对话上下文质量
- 需要管理长会话上下文
- 需要跨 Skills 上下文协同
- 需要评估上下文质量
- 需要 Prompt 优化

### ❌ 不适用场景
- 简单问答（无需上下文优化）
- 纯记忆操作（直接用 agent-memory-systems）
- 纯知识库查询（直接用 LLM Wiki）
- 纯知识同步（直接用 knowledge-base-manager）

---

## 📊 质量评估指标

### 上下文质量评分

| 指标 | 计算方式 | 健康范围 |
|------|----------|----------|
| **相关性** | 相关上下文/总上下文 | >80% |
| **完整性** | 关键信息完整度 | >90% |
| **简洁性** | 冗余信息比例 | <20% |
| **时效性** | 最新上下文占比 | >50% |
| **一致性** | 无冲突上下文比例 | 100% |

### 综合评分公式

```
综合评分 = 相关性×0.3 + 完整性×0.25 + 简洁性×0.2 + 时效性×0.15 + 一致性×0.1

评分等级:
- 90-100: 优秀
- 75-89: 良好
- 60-74: 需改进
- <60: 需关注
```

---

## 🎯 应用场景

### 场景 1: 长会话上下文优化

```
用户："我们已经聊了很多，帮我优化一下当前上下文"

流程:
1. 加载当前会话所有上下文
2. 优先级排序（保留关键信息）
3. 生成会话摘要
4. 去除冗余信息
5. 返回优化后的上下文

输出:
✓ 上下文优化完成
✓ 原始上下文：5000 tokens
✓ 优化后：1500 tokens (压缩 70%)
✓ 保留关键信息：100%
```

---

### 场景 2: Prompt 质量提升

```
用户："这个 Prompt 效果不好，帮我优化"

流程:
1. 分析当前 Prompt 问题
2. 从模板库选择最佳模板
3. 注入相关上下文
4. 生成优化版 Prompt
5. A/B 测试建议

输出:
✓ Prompt 优化完成
✓ 问题诊断：缺少上下文、结构混乱
✓ 优化方案：注入知识上下文、使用标准模板
✓ 预期提升：30-50%
```

---

### 场景 3: 跨 Skills 上下文协同

```
用户："需要结合记忆和知识库回答问题"

流程:
1. 从 agent-memory 加载记忆上下文
2. 从 LLM Wiki 获取知识上下文
3. 统一协议整合
4. 去重和优先级排序
5. 注入到当前对话

输出:
✓ 上下文协同完成
✓ 记忆上下文：5 条
✓ 知识上下文：3 条
✓ 整合后：7 条（去重 1 条）
```

---

### 场景 4: 上下文健康检查

```
用户："检查上下文健康状态"

流程:
1. 运行健康检查脚本
2. 评估各项质量指标
3. 生成质量报告
4. 提供优化建议

输出:
上下文健康检查报告
- 相关性：85% ✅
- 完整性：92% ✅
- 简洁性：75% ⚠️ (冗余 25%)
- 时效性：60% ⚠️ (旧上下文过多)
- 一致性：100% ✅

综合评分：82/100 (良好)

优化建议:
1. 清理过期上下文
2. 压缩冗余信息
3. 更新老旧上下文
```

---

## 🔧 核心工具

### 工具 1: 上下文优化器 (optimizer.py)

**功能**:
- 去除冗余信息
- 保留关键内容
- 压缩上下文体积

**使用方式**:
```python
from session-context.optimizer import optimize_context

optimized = optimize_context(
    context=current_context,
    target_length=1500,  # 目标长度
    preserve_key_info=True  # 保留关键信息
)
```

---

### 工具 2: 上下文摘要器 (summarizer.py)

**功能**:
- 自动生成会话摘要
- 提取核心要点
- 保持语义完整

**使用方式**:
```python
from session-context.summarizer import summarize

summary = summarize(
    conversation=session_history,
    max_length=500,  # 最大长度
    style="bullet"   # 摘要风格
)
```

---

### 工具 3: 上下文优先级 (prioritizer.py)

**功能**:
- 评估上下文重要性
- 智能排序
- 动态调整权重

**使用方式**:
```python
from session-context.prioritizer import prioritize

ranked = prioritize(
    contexts=context_list,
    criteria=["relevance", "recency", "importance"]
)
```

---

### 工具 4: 上下文注入器 (injector.py)

**功能**:
- 智能注入相关上下文
- 保持上下文连贯性
- 避免信息过载

**使用方式**:
```python
from prompt-context.injector import inject_context

prompt = inject_context(
    base_prompt=base,
    contexts=relevant_contexts,
    max_tokens=1000
)
```

---

### 工具 5: 质量评分器 (scorer.py)

**功能**:
- 量化评估上下文质量
- 多维度评分
- 生成改进建议

**使用方式**:
```python
from quality-assessment.scorer import score_context

score = score_context(
    context=current_context,
    dimensions=["relevance", "completeness", "conciseness"]
)
```

---

## ⚠️ 关键规则

### 上下文管理规则

1. **最小必要原则**: 只保留必要的上下文信息
2. **优先级排序**: 重要上下文优先保留
3. **定期清理**: 定期清理过期上下文
4. **版本管理**: 保留上下文版本历史

### 质量保障规则

5. **相关性检查**: 确保上下文与当前任务相关
6. **完整性验证**: 确保关键信息完整
7. **一致性校验**: 确保上下文无冲突
8. **时效性评估**: 优先使用最新上下文

### 协同规则

9. **协议优先**: 遵循统一上下文协议
10. **权限控制**: 验证跨 Skills 访问权限
11. **依赖追踪**: 记录上下文依赖关系
12. **日志记录**: 记录所有上下文操作

---

## 📈 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 上下文压缩率 | >50% | 优化后体积减少 |
| 关键信息保留率 | 100% | 关键信息不丢失 |
| Prompt 效果提升 | >30% | 优化后效果提升 |
| 质量评分 | >80/100 | 综合质量评分 |
| 用户满意度 | >4/5 | 用户评分 |

---

## 🔄 版本迭代

| 版本 | 日期 | 改动 |
|------|------|------|
| v1.0 | 2026-04-16 | 初始版本，完整四大核心功能 |

---

## 🔗 双向链接

### 向上链接
- [[00-索引与导航/AI统一索引/AI-总索引|01-龙心 OS 核心系统]] - 核心系统
- [[00-索引与导航/AI统一索引/AI-总索引|01-五大引擎]] - 五大引擎之一

### 平行链接
- [[00-索引与导航/AI统一索引/AI-总索引|agent-memory-systems]] - 记忆存储
- [[00-索引与导航/AI统一索引/AI-总索引|llm-wiki-knowledge-base]] - 知识上下文
- [[00-索引与导航/AI统一索引/AI-总索引|knowledge-base-manager]] - 三库同步
- [[00-索引与导航/AI统一索引/AI-总索引|self-learning]] - 学习优化

### 向下链接
- [[上下文工程理论]] - 理论基础
- [[上下文管理 SOP]] - 操作流程
- [[Prompt 模板库]] - 模板资源

---

_创建：2026-04-16 · 基于上下文工程最佳实践 v1.0_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[03-知识地基层/五行分类/五行分类图谱全息阐释]] — 五行分类图谱全息阐释
- [[03-知识地基层/五行分类/五行系统总览]] — 五行系统总览
- [[03-知识地基层/五行分类/生克制化关系]] — 生克制化关系详解
- [[03-知识地基层/象思维/核心方法]] — 象思维核心方法
- [[03-知识地基层/象思维/核心概念]] — 象思维核心概念
- [[09-技能库/上下文工程.skills/references/references/sop]] — 上下文工程标准操作流程

<!-- AI-LINKS-END -->
