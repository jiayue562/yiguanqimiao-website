# 上下文工程实践指南

## 典型场景

### 场景1：长会话优化
会话超过 30 轮时，使用 summarizer 生成摘要，prioritizer 决定保留哪些上下文。

### 场景2：跨 Skills 调用
agent-memory-systems -> 上下文工程 -> LLM Wiki，协议统一传递。

### 场景3：质量门禁
每次上下文变更后，通过 scorer 评分，低于 60 分自动触发优化。
