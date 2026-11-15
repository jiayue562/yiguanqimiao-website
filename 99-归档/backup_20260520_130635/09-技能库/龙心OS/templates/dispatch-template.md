# 龙心OS · 引擎调度模板

## 调度请求格式

```yaml
# 调度请求
request:
  timestamp: "2026-04-08T19:00:00+08:00"
  user_input: "用户输入内容"
  conversation_history: [...]
  
# 上下文感知结果
context_perception:
  intent_type: "获取信息/深度理解/创新突破/分析决策/任务执行/系统进化"
  intent_strength: "高/中/低"
  emotion_signals: []
  complexity: "简单/中等/复杂"

# 场景识别结果
scene_classification:
  scene_id: "S0-S9"
  scene_name: "场景名称"
  threshold_score: 0
  
# 引擎路由结果
engine_routing:
  primary_engines: []
  secondary_engines: []
  routing_reason: "路由决策理由"
  
# 执行计划
execution_plan:
  steps: []
  estimated_time: ""
  expected_output: ""
```

## 调度响应格式

```yaml
# 调度响应
response:
  status: "success/pending/clarification"
  declaration: "引擎声明（如「🐉 龙心OS 全系统启动」）"
  
# 激活的引擎
activated_engines:
  - name: "引擎名称"
    path: "引擎路径"
    role: "primary/secondary"
    
# 执行结果
execution_result:
  output: "执行输出"
  insights: []
  
# 知行合一沉淀（如满足条件）
zhixingheyi:
  triggered: true/false
  core_insight: "一句话核心洞察"
  symbol: "象征符号"
  generalization_scenes: []
```

## 快速调度口令

| 口令 | 激活引擎 | 使用场景 |
|------|---------|---------|
| 全系统启动 | 五大引擎全序列 | 重大决策/系统规划 |
| 象感知 | 象思维 | 创新突破/0→1 |
| 五色分析 | 五色光 | 分析决策 |
| 深度学习 | 知识学习 | 深度理解 |
| 象限诊断 | 人机协同五象限 | 任务分工 |
| 知行沉淀 | 知行合一 | 系统进化 |
| 三体一心 | 象思维+五色光 | 复杂分析 |
