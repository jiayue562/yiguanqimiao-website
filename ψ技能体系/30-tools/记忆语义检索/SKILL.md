---
name: 记忆语义检索
parent_skill: ai-os
description: 基于embedding相似度的智能语义记忆检索 - 超越关键词匹配，实现语义理解与跨语言检索
---

# 记忆语义检索增强 Skill

> 🧠 基于 embedding 相似度的智能记忆检索 · 龙心 OS 记忆系统增强

**版本**: v1.0  
**创建**: 2026-04-17  
**标签**: #语义检索 #embedding #记忆增强

---

## 📋 核心定义

**一句话定义**: 使用 embedding 向量相似度进行智能记忆检索，超越关键词匹配，实现语义理解。

**三行问题陈述**:
- **What**: 解决传统关键词检索无法理解语义的问题
- **Why**: 人类记忆是关联式的，不是关键词式的
- **How**: embedding 向量 + 余弦相似度 + 语义聚类

---

## 🎯 与 v1.0 的增强对比

| 维度 | v1.0 (关键词检索) | v2.0 (语义检索) |
|------|------------------|-----------------|
| **检索方式** | 关键词匹配 | embedding 相似度 |
| **召回率** | 60-70% | 85-95% |
| **语义理解** | ❌ 无 | ✅ 强 |
| **同义词识别** | ❌ 需要手动配置 | ✅ 自动识别 |
| **跨语言检索** | ❌ 不支持 | ✅ 支持 |

---

## 🔄 语义检索流程

```
用户查询
    ↓
1. 查询 embedding 编码
    ↓
2. 与记忆库 embedding 计算余弦相似度
    ↓
3. 排序 + 过滤（相似度阈值 > 0.75）
    ↓
4. 返回 Top-K 最相关记忆
    ↓
5. 可选：语义聚类 + 摘要
```

---

## 🛠️ 实现方案

### 方案 A: 使用现有 API（推荐）

**优点**: 快速实现，无需训练  
**缺点**: 依赖外部 API

```python
# 使用 OpenAI/SentenceTransformers embedding
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 编码记忆
memory_embeddings = model.encode(memory_texts)

# 编码查询
query_embedding = model.encode(query)

# 计算余弦相似度
similarities = cosine_similarity([query_embedding], memory_embeddings)
```

### 方案 B: 本地轻量模型

**优点**: 离线可用，隐私保护  
**缺点**: 需要本地部署

```bash
# 安装
pip install sentence-transformers

# 模型选择
- paraphrase-multilingual-MiniLM-L12-v2 (推荐，支持中文)
- text2vec-base-chinese (中文专用)
- bge-small-zh-v1.5 (中文优化)
```

---

## 📁 文件结构

```
semantic-memory-search/
├── SKILL.md                          # 技能定义
├── semantic_search.py                # 核心检索逻辑
├── embedding_cache.json              # embedding 缓存
├── requirements.txt                  # Python 依赖
└── scripts/
    ├── build_embeddings.ps1         # 构建记忆 embedding
    └── search.ps1                   # 语义搜索入口
```

---

## 🎯 触发条件

### P0 直接触发
```
语义搜索、相似记忆、相关记忆、
embedding 搜索、智能检索、
"帮我找类似的记忆"、"这个我记得说过"
```

### P1 场景触发
```
"我记得之前讨论过类似的..."
"这个和之前的项目有什么关系？"
"找出所有关于 X 的记忆"
```

---

## 📊 性能指标

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| **召回率@10** | >85% | Top-10 结果中相关的比例 |
| **精确率@10** | >80% | Top-10 结果中正确的比例 |
| **响应时间** | <2s | 查询到返回的时间 |
| **embedding 更新** | <5min/100 条 | 批量更新耗时 |

---

## 🔗 与现有 Skills 协同

### 前置 Skill
- **agent-memory-systems**: 提供记忆数据源
- **memory_search**: 提供关键词检索基线

### 协同 Skill
- **self-improving-agent**: 检索结果用于自我改进
- **llm-wiki-manager**: 检索结果用于 Wiki 编译

### 后置 Skill
- **无**: 检索完成后无需后续

---

## 📥 输入输出格式

### 输入
```json
{
  "query": "用户查询文本",
  "top_k": 5,
  "similarity_threshold": 0.75,
  "memory_types": ["semantic", "episodic"],
  "date_range": {"start": "2026-04-01", "end": "2026-04-17"}
}
```

### 输出
```json
{
  "query": "用户查询文本",
  "results": [
    {
      "memory_id": "mem-001",
      "content": "记忆内容...",
      "similarity": 0.92,
      "source": "MEMORY.md#L45",
      "date": "2026-04-15",
      "type": "semantic"
    }
  ],
  "total_found": 5,
  "search_time_ms": 156
}
```

---

## 🧪 测试用例

### T01: 基础语义搜索
**输入**: "超级个体"  
**预期**: 返回所有相关记忆（即使不包含"超级个体"关键词）

### T02: 同义词识别
**输入**: "AI 助手"  
**预期**: 返回包含"龙龟"、"智能体"、"agent"的记忆

### T03: 跨语言搜索
**输入**: "AI assistant" (英文)  
**预期**: 返回中文记忆（如果内容相关）

### T04: 时间范围过滤
**输入**: "龙心 OS" + 时间范围（本周）  
**预期**: 只返回本周内的相关记忆

### T05: 低相似度查询
**输入**: "今天天气"（与记忆无关）  
**预期**: 返回空结果或低相似度提示

---

## 📈 版本迭代

| 版本 | 时间 | 改动点 |
|------|------|--------|
| v1.0 | 2026-04-17 | 初始版本（基础语义检索） |
| v1.1 | 待规划 | 添加语义聚类 + 摘要 |
| v2.0 | 待规划 | 多模态检索（图片/音频） |

---

## 💬 核心金句

> "记忆不是关键词的集合，而是语义的网络。"

> "人类记忆是关联式的——看到一个词，想起一串事。"

> "好的检索系统，应该像老朋友一样懂你。"

---

_记忆语义检索增强 Skill v1.0 · 2026-04-17 · 龙心 OS_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/知识图谱/智能查询系统]] — 🔍 智能查询与推荐系�?
- [[03-知识地基层/五行分类/五行分类图谱全息阐释]] — 五行分类图谱全息阐释
- [[03-知识地基层/五行分类/五行系统总览]] — 五行系统总览
- [[03-知识地基层/五行分类/生克制化关系]] — 生克制化关系详解
- [[03-知识地基层/象思维/核心方法]] — 象思维核心方法
- [[03-知识地基层/象思维/核心概念]] — 象思维核心概念

<!-- AI-LINKS-END -->
