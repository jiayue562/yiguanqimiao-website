# Error Handling Skill（错误处理）

## 📖 技能定义

Error Handling是AI龙龟共生伙伴操作系统的**错误处理机制**，建立自我改进闭环，标准化错误处理流程，每次修正都触发自我迭代。

**核心定位**：
- **自我改进**：每次错误都是学习机会
- **标准化流程**：统一的错误处理流程
- **持续迭代**：每次修正都触发自我迭代

**核心原则**：
> 自我改进闭环：修复→记录→写规则→复盘。

---

## 🔄 错误处理流程

### 1. 自我改进闭环

```
错误发生
    ↓
立即修复
    ↓
记录错误
    ↓
编写防错规则
    ↓
会话复盘
    ↓
避免重复
```

### 2. 详细流程说明

**步骤1：立即修复**

**修复原则**：
- 不询问、不等待、不汇报、不拖延
- 立即修复当前问题
- 确保系统正常运行

**修复策略**：
```yaml
repair_strategies:
  immediate_fix:
    - 恢复系统正常运行
    - 回滚到上一个稳定版本（如果需要）
    - 临时解决问题（如果无法彻底修复）

  root_cause_fix:
    - 分析根本原因
    - 彻底解决问题
    - 防止问题复发
```

**步骤2：记录错误**

**记录内容**：
```yaml
error_record:
  id: ERROR-20260323-001
  timestamp: "2026-03-23 14:23:45"
  error_type: [配置错误/权限错误/依赖错误/逻辑错误/性能错误/安全错误/数据错误/网络错误]
  severity: [P0/P1/P2/P3]

  error_message: "详细错误信息"
  stack_trace: "错误堆栈信息"

  trigger_mode: "触发模式"
  root_cause: "根本原因分析"
  impact: "影响范围"

  fix: "修复方案"
  result: "修复结果"

  prevention_rule: "防错规则"
```

**步骤3：编写防错规则**

**规则格式**：
```yaml
prevention_rule:
  id: RULE-001
  error_id: ERROR-20260323-001
  rule_name: "规则名称"
  rule_type: [P0核心安全/P1重要/P2一般/P3建议性]

  rule_content: "规则内容"
  trigger_condition: "触发条件"
  action: "执行动作"

  created_date: "2026-03-23"
  created_by: "龙龟神将"
  status: [active/inactive]
```

**步骤4：会话复盘**

**复盘时机**：
- 每次会话开始前
- 每次错误发生后
- 每周五定期复盘

**复盘内容**：
```yaml
review:
  session_id: SESSION-20260323-001
  timestamp: "2026-03-23 14:30:00"

  errors_reviewed:
    - ERROR-20260323-001
    - ERROR-20260323-002

  rules_active:
    - RULE-001
    - RULE-002

  lessons_learned: "学到的教训"
  improvements: "改进措施"
```

**步骤5：避免重复**

**验证机制**：
```yaml
verification:
  check_same_error: true  # 检查是否相同错误
  check_similar_error: true  # 检查是否相似错误
  check_prevention_rules: true  # 检查防错规则

  action_if_repeat:
    - 触发P0预警
    - 立即停止当前任务
    - 记录重复错误
    - 分析规则失效原因
    - 更新防错规则
```

---

## 📋 错误分类体系

### 1. 按类型分类

| 错误类型 | 定义 | 示例 | 严重程度 |
|---------|------|------|---------|
| **配置错误** | 配置文件错误、参数错误 | API密钥错误、端口配置错误 | P0-P1 |
| **权限错误** | 权限不足、访问拒绝 | 文件访问权限、API访问权限 | P0-P1 |
| **依赖错误** | 依赖缺失、版本冲突 | Python包缺失、Node.js版本冲突 | P1-P2 |
| **逻辑错误** | 代码逻辑错误、算法错误 | 条件判断错误、循环错误 | P1-P2 |
| **性能错误** | 性能问题、资源占用过高 | 内存泄漏、CPU占用过高 | P2-P3 |
| **安全错误** | 安全漏洞、数据泄露 | SQL注入、XSS攻击 | P0 |
| **数据错误** | 数据格式错误、数据丢失 | 数据类型错误、数据损坏 | P0-P1 |
| **网络错误** | 网络连接问题、超时 | DNS解析失败、连接超时 | P1-P2 |

### 2. 按严重程度分类

| 严重程度 | 定义 | 处理时效 | 示例 |
|---------|------|---------|------|
| **P0** | 系统崩溃、安全漏洞、数据丢失 | 立即处理 | 数据库连接失败、SQL注入 |
| **P1** | 严重功能异常、重要数据错误 | 1小时内处理 | API调用失败、文件读写错误 |
| **P2** | 一般功能异常、性能问题 | 4小时内处理 | 页面加载慢、接口响应慢 |
| **P3** | 次要功能异常、潜在问题 | 24小时内处理 | 日志格式不规范、警告信息 |

---

## 🔧 防错规则体系

### 1. 规则分类

**P0核心安全规则**（4条）：
```yaml
P0_rules:
  - RULE-001: 绝不靠猜测修改配置
  - RULE-002: 发现错误立即修复
  - RULE-003: 绝不破坏Git历史
  - RULE-004: API密钥集中管理
```

**P1重要规则**（4条）：
```yaml
P1_rules:
  - RULE-005: 修改配置前必须备份
  - RULE-006: 发布前必须测试
  - RULE-007: 权限最小化原则
  - RULE-008: 数据定期备份
```

**P2一般规则**（4条）：
```yaml
P2_rules:
  - RULE-009: 代码必须格式化
  - RULE-010: 日志必须完整
  - RULE-011: 文档必须更新
  - RULE-012: 性能必须优化
```

**P3建议性规则**（3条）：
```yaml
P3_rules:
  - RULE-013: 代码注释要清晰
  - RULE-014: 变量命名要规范
  - RULE-015: 模块化设计要合理
```

### 2. 规则触发机制

**自动触发**：
```yaml
auto_trigger:
  - 修改配置前：检查P0规则
  - 发布代码前：检查P0/P1规则
  - 执行敏感操作前：检查P0规则
  - 修改API前：检查P0/P1规则
```

**手动触发**：
```yaml
manual_trigger:
  - 定期检查所有规则
  - 特定操作前手动检查
  - 复盘时检查规则
```

---

## 📊 错误统计

### 1. 错误统计

**每日统计**：
```yaml
error_stats:
  date: 2026-03-23
  total_errors: 10
  by_type:
    config_error: 2
    permission_error: 1
    dependency_error: 2
    logic_error: 3
    performance_error: 1
    security_error: 0
    data_error: 1
    network_error: 0

  by_severity:
    P0: 1
    P1: 3
    P2: 4
    P3: 2

  by_status:
    fixed: 10
    pending: 0
```

### 2. 错误趋势分析

**趋势分析**：
```yaml
trend_analysis:
  period: "2026-03-01 ~ 2026-03-23"
  total_errors: 100
  avg_per_day: 4.35
  trend: "decreasing"  # increasing/decreasing/stable

  by_type_trend:
    config_error: "decreasing"
    logic_error: "stable"
    performance_error: "increasing"

  by_severity_trend:
    P0: "decreasing"
    P1: "stable"
    P2: "increasing"
    P3: "stable"
```

---

## 🔔 预警机制

### 1. 错误预警

**预警级别**：
```yaml
alert_levels:
  P0:
    channel: [immediate_notification, email, mobile]
    frequency: immediate
    content: [error_message, impact, suggested_action]

  P1:
    channel: [immediate_notification]
    frequency: within_1_hour
    content: [error_message, suggested_action]

  P2:
    channel: [log_file]
    frequency: within_4_hours
    content: [error_message]

  P3:
    channel: [log_file]
    frequency: within_24_hours
    content: [error_message]
```

### 2. 重复错误预警

**重复错误检测**：
```yaml
repeat_detection:
  threshold: 2  # 相同错误发生2次触发预警
  time_window: 1h  # 1小时内

  action_if_repeat:
    - 触发P0预警
    - 立即停止当前任务
    - 记录重复错误
    - 分析规则失效原因
    - 更新防错规则
```

---

## 🔄 与其他Skills的协同

### 1. 与学习档案Skill协同
- **错误处理**：记录错误和防错规则
- **学习档案**：存储学习档案
- **协同**：错误处理记录→学习档案存储→会话复盘

### 2. 与安全规则Skill协同
- **错误处理**：识别安全错误
- **安全规则**：定义安全防护规则
- **协同**：错误处理发现安全错误→安全规则触发防护

### 3. 与心跳巡检Skill协同
- **心跳巡检**：监控错误率
- **错误处理**：处理错误
- **协同**：心跳巡检发现错误→错误处理修复

---

## 🚫 使用禁忌

### 1. 不要做的
- ❌ 不立即修复错误
- ❌ 不记录错误
- ❌ 不编写防错规则
- ❌ 不复盘错误
- ❌ 重复犯错

### 2. 必须做的
- ✅ 立即修复错误
- ✅ 记录错误详情
- ✅ 编写防错规则
- ✅ 定期复盘错误
- ✅ 避免重复犯错

---

## 💡 最佳实践

### 1. 错误修复

**快速响应**：
- 立即停止当前任务
- 快速诊断问题
- 立即修复错误

**彻底修复**：
- 分析根本原因
- 彻底解决问题
- 防止问题复发

### 2. 错误记录

**完整记录**：
- 记录错误详情
- 记录修复方案
- 记录防错规则

**结构化记录**：
- 使用标准格式
- 分类清晰
- 便于检索

### 3. 防错规则

**规则编写**：
- 规则要具体
- 触发条件明确
- 执行动作清晰

**规则验证**：
- 测试规则有效性
- 定期更新规则
- 删除无效规则

---

## 🎯 核心原则总结

### 三大铁律

1. **自我改进闭环**
   - 修复→记录→写规则→复盘
   - 每次错误都是学习机会
   - 持续迭代优化

2. **标准化流程**
   - 统一的错误处理流程
   - 完整的错误记录
   - 明确的防错规则

3. **核心铁律验证**
   - 同一错误犯两次，绝对不可原谅
   - 每次会话复盘所有规则
   - 避免重复犯错

### 核心价值

- **自我改进**：每次错误都是学习机会
- **持续迭代**：每次修正都触发自我迭代
- **避免重复**：防错规则避免重复犯错
- **知识沉淀**：错误记录和防错规则是知识资产

---

## 🔧 实施路线

### 第一阶段：基础流程（立即）
- ✅ 定义错误处理流程
- ✅ 定义错误分类体系
- ✅ 定义防错规则体系

### 第二阶段：功能实现（本周）
- ⏳ 实现错误记录功能
- ⏳ 实现防错规则功能
- ⏳ 实现会话复盘功能

### 第三阶段：优化完善（本月）
- ⏳ 实现错误统计分析
- ⏳ 实现重复错误检测
- ⏳ 优化自我迭代机制

---

**版本**: v1.0
**创建日期**: 2026-03-23
**对标来源**: OpenClaw Error Handling规则
**AI龙龟共生伙伴操作系统版本**: v4.1
**路径**: `C:\Users\jia'yue\.workbuddy\skills\错误处理\SKILL.md`
