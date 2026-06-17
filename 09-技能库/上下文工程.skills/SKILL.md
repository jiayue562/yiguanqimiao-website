# 上下文工程.skills

> 会话上下文的优化、注入和质量评估 · 跨 Skills 上下文协同

**版本**: v1.0
**创建**: 2026-05-20
**标签**: #上下文 #会话管理 #Prompt 工程 #跨 Skill 协同
**归属**: 龙爪 OS 子技能
**粒度**: 生态 Skill（依赖 agent-memory-systems / LLM Wiki / knowledge-base-manager）

---

## What / Why / How

| | 描述 |
|---|------|
| **What** | 上下文的优化、注入、优先级排序和质量评估 |
| **Why** | 大模型会话中上下文窗口有限，必须高效管理；跨 Skills 调用时上下文需要统一协议 |
| **How** | 4 个核心模块（session-context / prompt-context / cross-skill-context / quality-assessment）+ 2 个脚本 |

---

## 核心能力

| 模块 | 能力 | 说明 |
|------|------|------|
| **session-context** | 上下文优化/摘要/优先级 | 管理单次会话的上下文窗口 |
| **prompt-context** | 模板注入/A/B 测试 | 管理 Prompt 维度的上下文 |
| **cross-skill-context** | 统一协议/共享存储/依赖追踪 | 跨 Skills 上下文协同 |
| **quality-assessment** | 质量评分/健康检查/优化建议 | 上下文质量的持续改进 |

---

## 触发条件

### 直接触发词（P0-权重 5）
- 上下文优化、上下文注入、上下文摘要
- 会话管理、Prompt 管理、跨 Skill 上下文

### 场景触发词（P1-权重 4）
- "上下文太长了帮我优化"
- "跨 Skill 调用上下文"
- "帮我总结当前会话上下文"

### 信号触发（P2-权重 3）
- 会话超过 30 轮（上下文窗口可能溢出）
- 跨 Skills 链式调用（需要统一上下文协议）
- 质量评分低于阈值

---

## 行为流程

```
输入触发信号
  ↓
session-context/prioritizer.py -> 优先级排序
  ↓
session-context/summarizer.py -> 上下文摘要
  ↓
prompt-context/injector.py -> 注入到 Prompt
  ↓
cross-skill-context/protocol.md -> 跨 Skills 协议
  ↓
quality-assessment/scorer.py -> 质量评分
  ↓
输出优化后的上下文
```

---

## 核心原则

### 必须
- 所有上下文变更必须记录日志
- 跨 Skills 调用必须遵守 protocol.md
- 质量评分必须 >= 60 分才能输出

### 禁止
- 不丢失关键上下文（优先级 Top-3 必须保留）
- 不注入未经验证的上下文
- 不破坏其他 Skills 的上下文空间

---

## 与其他 Skills 协同

| Skill | 协同方式 |
|-------|----------|
| agent-memory-systems | 使用记忆系统作为上下文持久化存储 |
| LLM Wiki 知识库 | 从 Wiki 获取知识上下文增强 Prompt |
| knowledge-base-manager | 同步三库上下文（Obsidian/OpcCla/IMA） |
| self-improving-agent | 学习上下文优化策略和效果反馈 |
| super-save/search | 快速保存/检索上下文快照 |

---

## 标准输入输出

### 输入格式
```json
{"session_id": "str", "context_items": [], "max_tokens": 4096}
```

### 输出格式
```json
{"optimized_context": [], "summary": "str", "quality_score": 0-100}
```

---

## 异常处理

| 异常 | 处理 |
|------|------|
| 上下文为空 | 返回空列表 + WARN 日志 |
| 优先级冲突 | 按 priority 降序排序，同优先级按时间倒序 |
| 跨 Skills 协议不匹配 | 降级为本地上下文处理 + ERROR 日志 |
| 质量评分偏低 | 截断低优先级项直至 >= 60 分 |

---

## 文件结构

```
上下文工程.skills/
├── SKILL.md
├── session-context/      # 会话上下文管理
├── prompt-context/       # Prompt 上下文
├── cross-skill-context/  # 跨 Skills 上下文
├── quality-assessment/   # 质量评估
├── scripts/              # 脚本
├── templates/            # 模板
├── triggers/             # 触发配置
└── references/           # 参考文档
```
