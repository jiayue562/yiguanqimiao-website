---
name: llm-wiki-manager
parent_skill: ai-os
description: |
  LLM Wiki 知识库管理工具 - 实现 Karpathy 的 LLMification 方法论。
  将知识管理从"人类编写、机器检索"转变为"机器编译、人类审核"。
  支持原始资料层/Wiki 本体层/Schema 配置层三层架构。
metadata:
  openclaw:
    emoji: '🧠'
    requires: { }
---

# LLM Wiki Manager - Karpathy 知识库构建方法

## 核心定位
机器编译、人类审核 · 构建具有持久记忆与自我进化能力的第二大脑

---

## 📋 功能概述

### What（这是什么）
LLM Wiki 知识库管理工具，实现 Karpathy 的 LLMification 方法论。

### Why（为什么需要）
- 传统 RAG 系统存在"失忆"缺陷：每次对话从零开始，会话结束即记忆清空
- PDF-to-text 简单转换导致结构化与语义信息丢失
- 知识无法积累与复利增长

### How（怎么用）
```
1. 原始资料 → raw/（只读）
2. LLM 编译 → Wiki/（结构化知识）
3. Schema 配置 → AGENTS.md（行为准则）
```

---

## 🏛️ 三层架构设计

### 2.1 原始资料层（Raw Sources）

**功能定位**: 系统的"原材料库"，只读的事实来源

**目录结构**:
```
raw/
├── articles/        # 文章
├── papers/          # 论文
├── code/            # 代码库
├── datasets/        # 数据集
└── images/          # 图片（本地化）
```

**数据摄取**:
- 使用 Obsidian Web Clipper 快速保存网页为 Markdown
- 图片本地化，解决 LLM 引用路径问题
- 保留原始格式，确保事实来源不可篡改

### 2.2 Wiki 本体层（The Wiki）

**功能定位**: 系统核心，由 LLM 生成并维护的结构化 Markdown 文件集合

**内容类型**:
| 类型 | 说明 | 示例 |
|------|------|------|
| 摘要页 | 每篇资料的精简摘要 | `summary-xxx.md` |
| 实体页 | 人物、组织、产品等 | `entity-xxx.md` |
| 概念页 | 核心概念与定义 | `concept-xxx.md` |
| 对比页 | 多个实体的对比分析 | `compare-a-vs-b.md` |
| 综合页 | 跨资料的综合结论 | `synthesis-xxx.md` |

**知识表示**:
- 叙述性内容 → 保留样式的 Markdown
- 数学公式 → LaTeX 格式封装
- 图表 → 独立文件 + 引用链接
- 表格 → 结构化 Markdown 表格

### 2.3 Schema 配置层（The Schema）

**功能定位**: 通过配置文件定义 Wiki 的结构规范与维护规则

**核心文件**:
| 文件 | 功能 |
|------|------|
| `AGENTS.md` | LLM 操作规则与行为准则 |
| `CLAUDE.md` | Claude 特定配置 |
| `wiki-schema.yaml` | Wiki 结构规范 |
| `maintenance-rules.md` | 维护规则 |

---

## 🔄 核心操作流程

### 3.1 录入（Ingest）- 增量编译与知识融合

**流程**:
```
1. 新资料放入 raw/
2. LLM 启动"编译"程序
3. 阅读资料，提取关键信息
4. 整合进现有 Wiki
5. 更新实体页面
6. 修正过时观点
7. 标注新旧矛盾
8. 维护索引文件
```

**人机协同**:
- 人类筛选：决定哪些资料值得入库
- 机器整理：LLM 负责结构化与索引
- 用户审核：确认摘要与更新内容

### 3.2 查询（Query）- 从"检索"到"调用"

**Karpathy 的反直觉发现**:
> 在中等规模下，LLM 依靠自建的索引文件和摘要即可高效完成检索，无需复杂的向量数据库 RAG。

**流程**:
```
1. 用户提问
2. LLM 搜索 Wiki 页面
3. 交叉验证多个来源
4. 生成综合答案
5. 高质量问答归档回 Wiki（复利效应）
```

### 3.3 检查（Lint）- 自我修复与进化

**健康检查机制**:

| 检查项 | 说明 | 处理 |
|--------|------|------|
| 一致性校验 | 发现并修复矛盾数据 | 标注矛盾，让用户决定 |
| 完整性补全 | 识别孤立页面与缺失引用 | 建议补链接 |
| 过时检测 | 识别超过 90 天未更新的内容 | 建议更新或归档 |
| 方向建议 | 基于现有知识结构建议下一步 | 提供研究方向 |

---

## 📁 目录结构

### 完整 Wiki 结构

```
LLM Wiki/
├── raw/                    # 原始资料层（只读）
│   ├── articles/          # 文章
│   ├── papers/            # 论文
│   ├── code/              # 代码库
│   ├── datasets/          # 数据集
│   └── images/            # 图片
│
├── wiki/                   # Wiki 本体层（LLM 维护）
│   ├── index.md           # 全局索引
│   ├── log.md             # 时间线日志
│   ├── summaries/         # 摘要页
│   ├── entities/          # 实体页
│   ├── concepts/          # 概念页
│   ├── comparisons/       # 对比页
│   └── syntheses/         # 综合页
│
└── schema/                 # Schema 配置层
    ├── AGENTS.md          # 操作规则
    ├── CLAUDE.md          # Claude 配置
    ├── wiki-schema.yaml   # 结构规范
    └── maintenance-rules.md # 维护规则
```

### 与龙心 OS 知识库的映射

| LLM Wiki | 龙心 OS | 说明 |
|----------|---------|------|
| raw/ | Notes/ | 统一入口，待处理内容 |
| wiki/ | Knowledge/ + 01-05/ | 结构化知识沉淀 |
| schema/ | AGENTS.md + rules/ | 操作规则配置 |

---

## 🔧 工具链配置

### 4.1 前端 IDE

**Obsidian**:
- 图谱视图直观展示知识关联
- 实时查看 LLM 的编辑结果
- 双向链接自动维护

### 4.2 输出多样化

**LLM 生成的知识不仅限于文本**:
- Marp 幻灯片
- Matplotlib 图表
- Mermaid 流程图
- 数据可视化

---

## 🚀 进阶路径：微调与内化

### Karpathy 的未来展望

> 随着 Wiki 数据的日益纯净，未来的方向是利用合成数据生成与微调技术，将 Markdown 知识库中的知识"内化"进模型权重。

**路径**:
```
Markdown 知识库
    ↓
高质量问答对
    ↓
SFT（监督微调）数据
    ↓
强化学习环境
    ↓
领域专才模型
```

**效果**:
- 从"通过上下文窗口记忆" → "通过权重掌握知识"
- 从通用模型 → 领域专才模型

---

## 📊 与龙心 OS 知识库的整合

### 整合方案

| 维度 | LLM Wiki | 龙心 OS | 整合方式 |
|------|----------|---------|----------|
| 架构 | 三层 | 五层 | LLM Wiki 作为 Knowledge/的子集 |
| 录入 | 增量编译 | Ingest | 合并流程 |
| 查询 | Wiki 搜索 | Query | 统一接口 |
| 检查 | Linting | Lint | 合并检查 |

### 整合后的结构

```
workspace/
├── Notes/                    # 输入层（统一入口）
│   ├── raw/                 # LLM Wiki 原始资料
│   ├── Clippings/           # 网页剪藏
│   ├── Inbox/               # 碎片想法
│   └── Conversation/        # AI 对话沉淀
│
├── wiki/                     # LLM Wiki 本体层
│   ├── index.md
│   ├── log.md
│   ├── summaries/
│   ├── entities/
│   ├── concepts/
│   └── ...
│
├── Knowledge/                # 知识层（龙心 OS）
│   ├── 方法论/
│   └── 读书笔记/
│
└── schema/                   # Schema 配置层
    ├── AGENTS.md
    └── wiki-schema.yaml
```

---

## ⚠️ 边界条件与异常

| 异常情况 | 处理方式 |
|----------|----------|
| 资料格式不支持 | 转为 Markdown 后入库 |
| 图片无法本地化 | 保留原链接，标注可能失效 |
| 新旧知识矛盾 | 标注矛盾，让用户决定 |
| Wiki 规模过大 | 分主题建立多个 Wiki |

---

## 📌 使用示例

### 场景 1: 录入新资料

**输入**:
```
把这篇论文加入 Wiki
文件：raw/papers/attention-is-all-you-need.pdf
```

**处理**:
1. 读取论文内容
2. 提取关键信息（摘要、方法、实验、结论）
3. 创建 `summaries/attention-is-all-you-need.md`
4. 提取实体（Transformer、Attention 等）
5. 创建/更新 `entities/transformer.md`
6. 更新 `index.md` 索引
7. 记录到 `log.md`

**输出**:
```
## 录入完成

### 新建文件
- summaries/attention-is-all-you-need.md
- entities/transformer.md（更新）

### 提取实体
- Transformer
- Self-Attention
- Positional Encoding

### 更新索引
- index.md 已添加新条目
- log.md 已记录

请审核摘要内容。
```

### 场景 2: 查询 Wiki

**输入**:
```
Transformer 的核心创新是什么？
```

**处理**:
1. 搜索 `entities/transformer.md`
2. 搜索相关 summaries
3. 交叉验证多个来源
4. 生成综合答案

**输出**:
```
## Transformer 核心创新

### 1. Self-Attention 机制
[详细说明]

### 2. Positional Encoding
[详细说明]

### 3. 并行计算优势
[详细说明]

## 来源
- [[attention-is-all-you-need]]
- [[transformer 详解]]
```

### 场景 3: Lint 检查

**输入**:
```
运行 Wiki 健康检查
```

**处理**:
1. 检查一致性（矛盾数据）
2. 检查完整性（孤立页面）
3. 检查时效性（过时内容）
4. 生成报告

**输出**:
```
## Wiki 健康报告

### 一致性检查 ✅
- 未发现矛盾数据

### 完整性检查 ⚠️
- 3 个孤立页面（无入链）
- 5 处缺失交叉引用

### 时效性检查 ⚠️
- 2 篇摘要超过 90 天未更新

### 方向建议 💡
- 建议补充：XXX 相关研究
- 建议更新：XXX 已过时
```

---

## 📊 版本迭代

| 版本 | 时间 | 改动点 |
|------|------|--------|
| v1.0 | 2026-04-13 | 初始版本，三层架构 + 三大操作 |

---

_龙心 OS LLM Wiki Manager v1.0 · 基于 Karpathy 方法论 · 最后更新：2026-04-13_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/agents_LLM Wiki 知识库激活完成报告]] — LLM Wiki 知识库激活完成报告
- [[01-核心体系/龙心OS_📚 知识库建设Skill]] — 📚 知识库建设 · 三层架构设计与实施指南
- [[08-龙心OS核心系统/AI-OS知识库/🧠 龙脑OS·知识地基层/wiki·概念页/LLMification]] — LLMification（知识编译方法论）
- [[09-技能库/知识学习Skills/references/llm-wiki-architecture]] — LLM Wiki三层知识流水线架构详解
- [[09-技能库/知识库建设/references/llm-wiki-theory]] — LLM Wiki 理论完整版
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer1-raw/🧠 龙脑OS·知识地基层/wiki·概念页/LLMification]] — LLMification（知识编译方法论）

<!-- AI-LINKS-END -->
