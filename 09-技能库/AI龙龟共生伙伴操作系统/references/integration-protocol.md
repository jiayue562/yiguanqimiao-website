---
title: "AI OS 三层整合协议"
description: "龙心OS × 龙脑OS × 龙爪OS 协同调用协议"
version: "1.0"
created: "2026-04-10"
---

# AI OS 三层整合协议

## 协议概述

本文档定义龙心OS、龙脑OS、龙爪OS三层之间的**调用协议、数据格式、状态同步、错误处理**机制。

---

## 一、调用协议

### 1.1 龙心OS → 龙脑OS 调用

#### 调用场景
龙心OS识别场景后，需要调用思维模型时，向龙脑OS发起请求。

#### 请求格式
```yaml
# 龙心OS → 龙脑OS 请求
request:
  header:
    request_id: "uuid"           # 请求唯一标识
    timestamp: "ISO8601"         # 请求时间
    source: "龙心OS"              # 请求来源
    target: "龙脑OS"              # 目标系统
    
  body:
    scene_type: "S2"             # 场景类型 S0-S9
    scene_description: "深度理解企业文化理论"
    required_models:             # 需要的思维模型
      - category: "系统思考"
        model_name: "系统思考"
        priority: 1
      - category: "分析框架"
        model_name: "MECE原则"
        priority: 2
    context:                     # 上下文信息
      user_intent: "理解企业文化的深层结构"
      history_summary: "用户之前讨论了企业文化的定义"
      constraints: ["时间限制", "深度要求"]
```

#### 响应格式
```yaml
# 龙脑OS → 龙心OS 响应
response:
  header:
    request_id: "uuid"           # 对应请求ID
    timestamp: "ISO8601"
    source: "龙脑OS"
    target: "龙心OS"
    status: "success"            # success / partial / failed
    
  body:
    models_provided:
      - model_id: "system_thinking_001"
        model_name: "系统思考"
        content: "系统思考的完整框架..."
        application_guide: "如何在企业文化分析中应用..."
        related_models: ["MECE原则", "金字塔原理"]
        
    knowledge_graph:
      related_concepts: ["组织文化", "价值观", "行为模式"]
      cross_domain_links: 5      # 跨域知识联系数量
      
    recommendations:
      next_models: ["利益相关者分析", "变革管理"]
      combination_suggestion: "建议与SWOT组合使用"
```

### 1.2 龙心OS → 龙爪OS 调用

#### 调用场景
龙心OS完成场景识别和引擎路由后，需要执行具体项目或工作流时，向龙爪OS发起请求。

#### 请求格式
```yaml
# 龙心OS → 龙爪OS 请求
request:
  header:
    request_id: "uuid"
    timestamp: "ISO8601"
    source: "龙心OS"
    target: "龙爪OS"
    
  body:
    execution_type: "project"    # project / workflow / sop
    execution_name: "企业文化咨询项目"
    
    engine_routing:              # 引擎路由结果
      primary_engine: "象思维"
      secondary_engines: ["五色光", "知识学习"]
      execution_sequence: ["象思维", "知识学习", "五色光", "知行合一"]
      
    model_requirements:          # 从龙脑OS获取的模型
      - model_name: "系统思考"
        usage_stage: "诊断阶段"
      - model_name: "SWOT分析"
        usage_stage: "分析阶段"
      
    project_context:
      goal: "完成企业文化诊断与设计"
      scope: ["现状诊断", "理念提炼", "落地设计"]
      timeline: "4周"
      resources: ["访谈对象", "问卷工具", "分析模板"]
```

#### 响应格式
```yaml
# 龙爪OS → 龙心OS 响应
response:
  header:
    request_id: "uuid"
    timestamp: "ISO8601"
    source: "龙爪OS"
    target: "龙心OS"
    status: "in_progress"        # in_progress / completed / failed
    
  body:
    project_id: "proj_001"
    execution_plan:
      phases:
        - phase_id: 1
          name: "项目启动"
          steps: ["目标定义", "范围确认", "资源分配"]
          status: "completed"
          
        - phase_id: 2
          name: "文化诊断"
          steps: ["访谈执行", "问卷发放", "数据分析"]
          status: "in_progress"
          current_step: "访谈执行"
          
    progress:
      overall: 25%                 # 整体进度
      current_phase: 60%           # 当前阶段进度
      
    engine_calls:                  # 引擎调用记录
      - step: "访谈设计"
        engine: "象思维"
        model: "用户画像"
        result: "完成"
        
    issues:
      - type: "warning"
        description: "访谈对象时间协调困难"
        suggestion: "调整访谈时间或增加线上访谈"
```

### 1.3 龙爪OS → 龙脑OS 调用

#### 调用场景
龙爪OS执行项目步骤时，需要具体思维模型支持，直接向龙脑OS请求。

#### 请求格式
```yaml
# 龙爪OS → 龙脑OS 请求
request:
  header:
    request_id: "uuid"
    source: "龙爪OS"
    target: "龙脑OS"
    
  body:
    project_context:
      project_id: "proj_001"
      current_phase: "文化诊断"
      current_step: "数据分析"
      
    model_request:
      purpose: "分析访谈数据，提取文化主题"
      preferred_category: "分析框架"
      specific_models: ["主题分析", "编码分析"]
      
    data_context:
      data_type: "访谈记录"
      data_volume: "15份访谈记录，约3万字"
      key_questions: ["价值观", "行为模式", "痛点"]
```

---

## 二、状态同步协议

### 2.1 状态定义

```yaml
# 三层系统状态定义
system_states:
  龙心OS:
    - idle: 空闲，等待输入
    - perceiving: 感知上下文
    - routing: 引擎路由中
    - monitoring: 监控执行
    - integrating: 结果整合
    
  龙脑OS:
    - standby: 待命
    - retrieving: 检索模型
    - combining: 组合模型
    - optimizing: 优化匹配
    
  龙爪OS:
    - ready: 准备就绪
    - planning: 项目规划
    - executing: 执行中
    - tracking: 进度跟踪
    - completing: 项目收尾
```

### 2.2 同步机制

#### 实时同步（同步调用）
```yaml
# 适用于关键决策点
sync_points:
  - 场景识别完成 → 立即通知龙脑OS准备模型
  - 引擎路由完成 → 立即通知龙爪OS启动执行
  - 步骤完成 → 立即反馈龙心OS调整路由
```

#### 异步同步（消息队列）
```yaml
# 适用于非关键信息
async_updates:
  - 进度更新: 每10%进度推送一次
  - 日志记录: 批量异步写入
  - 性能指标: 定时汇总上报
```

### 2.3 状态广播

```yaml
# 状态变更广播
state_broadcast:
  event_type: "state_change"
  timestamp: "ISO8601"
  source_system: "龙心OS"
  old_state: "routing"
  new_state: "monitoring"
  
  broadcast_targets:
    - 龙脑OS: "准备知识供给"
    - 龙爪OS: "开始执行监控"
    - 用户界面: "显示执行进度"
```

---

## 三、错误处理协议

### 3.1 错误分级

```yaml
error_levels:
  P0_致命错误:
    description: "系统无法继续运行"
    examples: ["龙心OS引擎路由失败", "龙脑OS模型库损坏"]
    action: "立即停止，人工介入"
    
  P1_严重错误:
    description: "当前任务无法完成"
    examples: ["龙爪OS项目执行失败", "模型调用超时"]
    action: "回滚到上一个稳定状态，重新规划"
    
  P2_一般错误:
    description: "部分功能受影响"
    examples: ["单个模型返回结果不完整", "进度同步延迟"]
    action: "降级处理，继续执行"
    
  P3_轻微警告:
    description: "不影响主流程"
    examples: ["非关键模型加载慢", "日志写入延迟"]
    action: "记录日志，继续执行"
```

### 3.2 错误处理流程

```yaml
error_handling_flow:
  检测:
    - 超时检测: 调用超过30秒视为超时
    - 异常检测: 返回结果格式异常
    - 一致性检测: 状态不一致
    
  分类:
    - 根据错误分级标准确定级别
    - 根据错误类型确定处理策略
    
  响应:
    P0: 立即熔断，通知用户，等待人工处理
    P1: 尝试重试3次，失败后回滚，重新规划
    P2: 降级使用备用方案，记录日志
    P3: 忽略警告，记录日志
    
  恢复:
    - 自动恢复: 系统自愈机制
    - 手动恢复: 用户确认后恢复
    - 重启恢复: 重启相关服务
```

### 3.3 熔断机制

```yaml
circuit_breaker:
  触发条件:
    - 连续5次调用失败
    - 错误率超过50%（最近10次）
    - P0错误发生
    
  熔断动作:
    - 停止向故障系统发送请求
    - 切换到备用系统或降级方案
    - 通知用户当前状态
    
  恢复策略:
    - 熔断后5分钟尝试半开状态
    - 发送探测请求验证恢复
    - 成功后逐步放开流量
```

---

## 四、数据格式标准

### 4.1 通用头部格式

```yaml
header_standard:
  version: "1.0"                 # 协议版本
  request_id: "uuid"             # 请求唯一标识
  timestamp: "ISO8601"           # 时间戳
  source: "system_name"          # 来源系统
  target: "system_name"          # 目标系统
  trace_id: "trace_uuid"         # 链路追踪ID
  
  authentication:
    token_type: "Bearer"
    token: "encrypted_token"
    permissions: ["read", "write", "execute"]
```

### 4.2 上下文传递格式

```yaml
context_format:
  session_context:
    session_id: "session_uuid"
    user_id: "user_identifier"
    conversation_history: []       # 对话历史摘要
    user_preferences: {}           # 用户偏好
    
  task_context:
    task_id: "task_uuid"
    task_type: "project"
    task_status: "in_progress"
    task_progress: 25
    
  system_context:
    龙心OS_state: "monitoring"
    龙脑OS_state: "retrieving"
    龙爪OS_state: "executing"
    active_engines: ["象思维", "知识学习"]
    active_models: ["系统思考", "MECE"]
```

### 4.3 结果返回格式

```yaml
result_format:
  status: "success"              # success / partial / failed
  code: 200                      # HTTP风格状态码
  message: "操作成功"
  
  data:
    content: "结果内容"
    format: "markdown"           # markdown / json / yaml
    attachments: []              # 附件列表
    
  metadata:
    execution_time: 1500         # 执行时间（毫秒）
    resource_usage:
      cpu: "30%"
      memory: "256MB"
    
  trace_info:
    request_id: "uuid"
    processing_steps:
      - step: "场景识别"
        duration: 200
      - step: "引擎路由"
        duration: 150
      - step: "模型调用"
        duration: 800
```

---

## 五、性能优化协议

### 5.1 缓存策略

```yaml
cache_strategy:
  龙心OS:
    scene_cache:                 # 场景识别缓存
      ttl: 300                   # 5分钟
      max_size: 1000             # 最多缓存1000个场景
      
  龙脑OS:
    model_cache:                 # 模型缓存
      hot_models:                # 热点模型常驻内存
        - "系统思考"
        - "MECE原则"
        - "金字塔原理"
      cold_cache_ttl: 3600       # 冷模型1小时
      
  龙爪OS:
    project_template_cache:      # 项目模板缓存
      ttl: 86400                 # 24小时
```

### 5.2 批量处理

```yaml
batch_processing:
  适用场景:
    - 多个模型同时调用
    - 批量数据同步
    - 日志批量写入
    
  批量大小:
    model_calls: 5               # 最多同时调用5个模型
    data_sync: 100               # 批量同步100条记录
    log_write: 50                # 批量写入50条日志
```

### 5.3 异步优化

```yaml
async_optimization:
  异步操作:
    - 非关键模型加载
    - 日志记录
    - 知识图谱更新
    - 性能指标上报
    
  异步队列:
    queue_type: "priority_queue"
    max_queue_size: 1000
    worker_threads: 4
```

---

## 六、安全协议

### 6.1 身份认证

```yaml
authentication:
  系统间认证:
    method: "mutual_tls"         # 双向TLS认证
    certificate_rotation: "30d"  # 证书30天轮换
    
  用户认证:
    method: "token_based"
    token_ttl: "24h"
    refresh_token_ttl: "7d"
```

### 6.2 数据加密

```yaml
encryption:
  传输加密:
    protocol: "TLS1.3"
    cipher_suites: ["AES-256-GCM"]
    
  存储加密:
    sensitive_data: "AES-256"
    key_management: "HSM"        # 硬件安全模块
```

### 6.3 访问控制

```yaml
access_control:
  角色定义:
    - admin: 完全控制权限
    - operator: 操作权限
    - viewer: 只读权限
    
  权限矩阵:
    龙心OS: ["admin", "operator"]
    龙脑OS: ["admin", "operator", "viewer"]
    龙爪OS: ["admin", "operator"]
```

---

## 七、监控与日志

### 7.1 监控指标

```yaml
monitoring_metrics:
  性能指标:
    - response_time_p99: 99分位响应时间
    - throughput: 吞吐量（请求/秒）
    - error_rate: 错误率
    - resource_utilization: 资源利用率
    
  业务指标:
    - scene_recognition_accuracy: 场景识别准确率
    - model_match_precision: 模型匹配精准度
    - project_completion_rate: 项目完成率
    - user_satisfaction: 用户满意度
```

### 7.2 日志规范

```yaml
logging_standard:
  日志级别:
    - DEBUG: 调试信息
    - INFO: 一般信息
    - WARN: 警告信息
    - ERROR: 错误信息
    - FATAL: 致命错误
    
  日志格式:
    timestamp: "ISO8601"
    level: "INFO"
    system: "龙心OS"
    component: "scene_router"
    message: "场景识别完成"
    context: {}
    trace_id: "uuid"
```

---

## 八、版本管理

### 8.1 版本兼容性

```yaml
version_compatibility:
  向后兼容:
    - v1.0 客户端可以与 v1.1 服务端通信
    - 新增字段可选，不影响旧版本
    
  不兼容变更:
    - 重大版本升级（v1.x → v2.0）
    - 需要同步升级所有组件
```

### 8.2 版本协商

```yaml
version_negotiation:
  协商流程:
    1. 客户端发送支持的版本列表
    2. 服务端选择共同支持的最高版本
    3. 双方使用该版本通信
    
  降级策略:
    - 如果无共同版本，使用最低版本
    - 记录版本不匹配警告
```

---

## 总结

**三层整合协议的核心原则**：

1. **标准化**：统一的请求/响应格式，降低集成成本
2. **可靠性**：完善的错误处理和熔断机制，确保系统稳定
3. **高性能**：缓存、批量、异步优化，提升系统性能
4. **安全性**：认证、加密、访问控制，保护数据安全
5. **可观测**：监控、日志、追踪，保障系统可观测性

**协议演进方向**：
- 持续优化性能指标
- 扩展新的调用场景
- 增强安全防护能力
- 提升智能化水平

---

**协议版本**: 1.0
**创建时间**: 2026-04-10
**维护者**: 龙龟神将
**关联文档**:
  - three-layer-architecture.md（三层架构详解）
  - SKILL.md（AI OS主文档）
