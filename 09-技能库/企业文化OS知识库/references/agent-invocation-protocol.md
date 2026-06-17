# 企业文化OS知识库智能体 · 调用协议

> **文档定位**：定义其他智能体如何调用企业文化OS知识库智能体
> **版本**：v1.0 | **创建日期**：2026-04-10 | **维护者**：龙龟神将

---

## 📋 协议概述

### 协议定位

**本协议定义了企业文化OS知识库智能体作为知识底座，为其他智能体提供知识服务的标准接口。**

```
┌─────────────────────────────────────────────────────────────┐
│                    智能体调用关系图                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        用户层                                │
│                           │                                  │
│                           ↓                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 龙心OS总智能体层                      │   │
│  │              （全局调度中枢）                         │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                  │
│           ┌─────────────┼─────────────┐                    │
│           ↓             ↓             ↓                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ 企业文化OS │  │  企业文化  │  │  五行人格  │          │
│  │ 知识库智能体│  │   Skill    │  │  总智能体  │          │
│  │  (知识底座) │  │  (应用层)  │  │  (专业层)  │          │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘          │
│         │               │               │                 │
│         │         ┌─────┘               │                 │
│         │         ↓                     │                 │
│         │    ┌─────────┐                │                 │
│         └───→│ 知识调用 │←───────────────┘                 │
│              │  协议接口 │                                  │
│              └─────────┘                                  │
│                                                             │
│  说明：企业文化OS知识库智能体作为知识底座，为其他智能体      │
│        提供企业文化理论知识支撑                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔌 调用接口

### 接口定义

```yaml
接口名称: 企业文化OS知识库智能体调用接口
接口版本: v1.0
接口类型: 智能体间协同接口
调用方式: 同步调用 / 异步回调

输入参数:
  query:
    type: string
    required: true
    description: "查询意图或问题描述"
    example: "如何诊断企业文化问题？"
  
  scene_type:
    type: enum
    required: true
    options: [S1, S2, S3, S4, S5]
    description: "场景类型"
    S1: "快速查询"
    S2: "深度理解"
    S3: "诊断分析"
    S4: "方案设计"
    S5: "系统规划"
  
  depth_level:
    type: enum
    required: false
    default: "medium"
    options: [shallow, medium, deep]
    description: "知识深度要求"
  
  cross_domain:
    type: boolean
    required: false
    default: false
    description: "是否需要跨域知识联系"
  
  output_format:
    type: enum
    required: false
    default: "structured"
    options: [structured, narrative, bullet_points, json]
    description: "输出格式"

输出结果:
  knowledge_nodes:
    type: array
    description: "相关知识节点列表"
    items:
      - node_id: "节点ID"
        title: "节点标题"
        content: "节点内容摘要"
        relevance_score: "相关度分数(0-1)"
  
  cross_domain_links:
    type: array
    description: "跨域知识联系"
    items:
      - target_domain: "目标知识域"
        link_type: "联系类型"
        description: "联系描述"
  
  recommended_engines:
    type: array
    description: "推荐调用的协同引擎"
    items:
      - engine_name: "引擎名称"
        reason: "推荐理由"
  
  output_content:
    type: string
    description: "格式化输出内容"
  
  metadata:
    type: object
    description: "元数据"
    properties:
      query_time: "查询耗时(ms)"
      knowledge_version: "知识库版本"
      confidence_score: "置信度分数"
```

---

## 📡 调用场景

### 场景1：龙心OS总智能体调用

**场景描述**：龙心OS总智能体识别到企业文化相关需求，调用知识库智能体获取知识支撑。

```yaml
调用方: 龙心OS总智能体
被调用方: 企业文化OS知识库智能体

调用流程:
  1. 龙心OS识别场景 → 判断为企业文化相关
  2. 构建握手包:
     ```yaml
     query: "企业文化诊断方法论"
     scene_type: "S3"
     depth_level: "deep"
     cross_domain: true
     output_format: "structured"
     ```
  3. 发送调用请求
  4. 接收返回结果
  5. 整合到最终输出

返回结果示例:
  knowledge_nodes:
    - node_id: "culture_diagnosis_001"
      title: "企业文化四层次诊断模型"
      content: "从精神层、制度层、物质层、行为层四个维度进行诊断..."
      relevance_score: 0.95
    - node_id: "culture_diagnosis_002"
      title: "文化诊断七步法"
      content: "需求诊断→阶段判断→模块选择→内容生成→落地设计→输出交付→持续进化"
      relevance_score: 0.92
  
  cross_domain_links:
    - target_domain: "五行人格心理学"
      link_type: "理论融合"
      description: "企业文化×五行人格：不同人格类型对文化的偏好差异"
  
  recommended_engines:
    - engine_name: "五色光思维"
      reason: "用于多维诊断分析"
    - engine_name: "象思维"
      reason: "用于文化创新设计"
  
  output_content: "[格式化后的诊断方法论]"
```

### 场景2：企业文化Skill调用

**场景描述**：企业文化Skill在执行过程中需要查询理论知识，调用知识库智能体。

```yaml
调用方: 企业文化Skill
被调用方: 企业文化OS知识库智能体

调用流程:
  1. 企业文化Skill执行到某一步骤
  2. 需要理论支撑 → 调用知识库
  3. 构建握手包:
     ```yaml
     query: "企业家精神的核心要素"
     scene_type: "S1"
     depth_level: "medium"
     cross_domain: false
     output_format: "bullet_points"
     ```
  4. 获取知识 → 继续执行

返回结果示例:
  knowledge_nodes:
    - node_id: "entrepreneur_spirit_001"
      title: "企业家精神五大要素"
      content: "创新精神、冒险精神、责任担当、坚韧意志、社会责任"
      relevance_score: 0.98
  
  output_content: |
    企业家精神核心要素：
    • 创新精神：突破常规，创造新价值
    • 冒险精神：承担风险，把握机遇
    • 责任担当：对结果负责，勇于承担
    • 坚韧意志：面对挫折，坚持不懈
    • 社会责任：关注社会，回馈社会
```

### 场景3：五行人格总智能体调用

**场景描述**：五行人格总智能体需要企业文化知识，进行跨域融合分析。

```yaml
调用方: 五行人格总智能体
被调用方: 企业文化OS知识库智能体

调用流程:
  1. 五行人格分析涉及组织文化
  2. 需要企业文化理论支撑
  3. 构建握手包:
     ```yaml
     query: "五行人格与企业文化建设的关联"
     scene_type: "S4"
     depth_level: "deep"
     cross_domain: true
     output_format: "structured"
     ```
  4. 获取跨域知识 → 融合分析

返回结果示例:
  knowledge_nodes:
    - node_id: "culture_personality_001"
      title: "木行人领导力与企业文化"
      content: "木行人擅长创新文化、愿景引领..."
      relevance_score: 0.94
    - node_id: "culture_personality_002"
      title: "火行人执行力文化"
      content: "火行人擅长打造高效执行文化..."
      relevance_score: 0.91
  
  cross_domain_links:
    - target_domain: "五行人格心理学"
      link_type: "应用融合"
      description: "五行人格类型与企业文化偏好匹配模型"
    - target_domain: "领导力"
      link_type: "理论支撑"
      description: "不同人格类型的领导风格对文化的影响"
```

---

## 🔄 调用流程

### 标准调用流程

```
┌─────────────────────────────────────────────────────────────┐
│                  智能体调用标准流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  步骤1: 构建握手包                                           │
│  ├── 明确查询意图                                            │
│  ├── 确定场景类型(S1-S5)                                     │
│  ├── 设置深度要求                                            │
│  └── 指定输出格式                                            │
│                          ↓                                  │
│  步骤2: 发送调用请求                                         │
│  ├── 通过MCP协议发送                                         │
│  ├── 设置超时时间(默认30秒)                                  │
│  └── 等待响应                                                │
│                          ↓                                  │
│  步骤3: 处理返回结果                                         │
│  ├── 解析知识节点                                            │
│  ├── 提取跨域联系                                            │
│  ├── 获取推荐引擎                                            │
│  └── 整合输出内容                                            │
│                          ↓                                  │
│  步骤4: 反馈与记录                                           │
│  ├── 记录调用日志                                            │
│  ├── 评估结果质量                                            │
│  └── 提供优化反馈（可选）                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 错误处理

```yaml
错误类型:
  - code: "KNOWLEDGE_NOT_FOUND"
    message: "未找到相关知识"
    solution: "扩展查询关键词或降低深度要求"
  
  - code: "TIMEOUT"
    message: "查询超时"
    solution: "简化查询或增加超时时间"
  
  - code: "INVALID_PARAMETER"
    message: "参数无效"
    solution: "检查参数格式和取值范围"
  
  - code: "SERVICE_UNAVAILABLE"
    message: "服务不可用"
    solution: "稍后重试或联系管理员"

错误响应格式:
  error:
    code: "错误代码"
    message: "错误描述"
    suggestion: "解决建议"
    timestamp: "错误发生时间"
```

---

## 📊 调用示例

### 示例1：完整调用流程

```python
# 伪代码示例

# 1. 构建握手包
handshake = {
    "query": "如何设计企业文化建设方案",
    "scene_type": "S4",
    "depth_level": "deep",
    "cross_domain": True,
    "output_format": "structured"
}

# 2. 发送调用请求
response = agent.invoke(
    target="企业文化OS知识库智能体",
    request=handshake,
    timeout=30
)

# 3. 处理返回结果
if response.success:
    knowledge_nodes = response.data.knowledge_nodes
    cross_domain_links = response.data.cross_domain_links
    recommended_engines = response.data.recommended_engines
    
    # 整合知识到输出
    final_output = integrate_knowledge(
        original_content,
        knowledge_nodes,
        cross_domain_links
    )
    
    # 根据推荐调用协同引擎
    for engine in recommended_engines:
        if engine.engine_name == "五色光思维":
            invoke_wuseguang(final_output)
else:
    handle_error(response.error)

# 4. 记录调用日志
log_invocation(
    caller="龙心OS总智能体",
    target="企业文化OS知识库智能体",
    query=handshake.query,
    result=response.success,
    timestamp=now()
)
```

### 示例2：快速查询

```yaml
# 快速查询场景（S1）

请求:
  query: "企业文化四层次模型"
  scene_type: "S1"
  depth_level: "shallow"
  output_format: "bullet_points"

响应:
  knowledge_nodes:
    - title: "企业文化四层次模型"
      content: "精神层、制度层、物质层、行为层"
  
  output_content: |
    企业文化四层次模型：
    • 精神层：使命、愿景、价值观（核心）
    • 制度层：管理制度、行为规范
    • 物质层：企业标识、办公环境
    • 行为层：领导行为、员工行为
```

---

## 🔐 安全与权限

### 调用权限

```yaml
允许调用的智能体:
  - 龙心OS总智能体
  - 企业文化Skill
  - 五行人格总智能体
  - 象思维
  - 知识学习Skills
  - 五色光思维
  - 人机协同五象限
  - 知行合一

权限级别:
  - level: "full_access"
    agents: ["龙心OS总智能体", "企业文化Skill"]
    permissions: ["读取", "查询", "跨域关联"]
  
  - level: "read_only"
    agents: ["五行人格总智能体", "象思维", "知识学习Skills"]
    permissions: ["读取", "查询"]
```

### 限流策略

```yaml
限流规则:
  - 单智能体: 每分钟最多10次调用
  - 全局: 每分钟最多50次调用
  - 突发流量: 允许瞬时峰值×2

超限处理:
  - 返回错误码: "RATE_LIMIT_EXCEEDED"
  - 建议: "请稍后重试"
  - 记录: 记录超限事件用于优化
```

---

## 📈 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 响应时间 | <500ms | 平均响应时间 |
| 成功率 | ≥99% | 调用成功比例 |
| 知识覆盖率 | 100% | 核心领域覆盖 |
| 并发处理 | ≥10 | 同时处理请求数 |
| 缓存命中率 | ≥80% | 常用知识缓存 |

---

## 🎯 核心金句

> "企业文化OS知识库智能体作为知识底座，为整个智能体生态提供理论支撑。"

> "调用协议是智能体间的'通用语言'，确保知识的高效流通与协同。"

> "知识底座的价值不在于存储，而在于被调用、被融合、被创新。"

---

**文档版本**: v1.0  
**创建日期**: 2026-04-10  
**维护者**: 龙龟神将  
**关联文档**: SKILL.md、agent-core-capabilities.md、framework-autonomy.md