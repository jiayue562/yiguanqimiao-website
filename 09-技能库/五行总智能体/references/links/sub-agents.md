# 五个分智能体链接

> **版本**: v3.0  
> **创建**: 2026-04-04  
> **作用**: 分智能体快速引用路径

---

## 🌿 分智能体引用格式

```markdown
五行总智能体 SKILL.md 引用格式：

总智能体（快思考）：[[五行总智能体]]

分智能体（慢思考）：
- [[🌿 木行人分智能体.skills]]
- [[🔥 火行人分智能体.skills]]
- [[🌏 土行人分智能体.skills]]
- [[⚔️ 金行人分智能体.skills]]
- [[💧 水行人分智能体.skills]]
```

---

## 📍 分智能体路径

### 主技能路径

```
五行总智能体（主智能体）
  路径: C:\Users\jia'yue\.workbuddy\skills\五行总智能体\
  SKILL.md: SKILL.md
  references:
    - theory.md（五行人格心理学完整理论体系）
    - integration-notes.md（跨体系整合指南）
    - architecture-overview.md（系统架构总览）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）
```

### 分智能体路径

```
木行人分智能体（已独立封装）
  路径: C:\Users\jia'yue\.workbuddy\skills\木行人分智能体.skills\
  SKILL.md: SKILL.md（9260+字完整体系）
  references:
    - theory.md（木行人一心三界五行九层体系）
    - practice.md（拔阴取阳实践指南）
    - transformation.md（化克为生完整路径）
    - integration-notes.md（跨体系整合）
  templates:
    - input_template.md（诊断输入模板）
    - output_template.md（报告输出模板）
    - workflow_template.md（七步流程模板）
  test-cases: test-cases.md（测试用例）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）

火行人分智能体（已独立封装）
  路径: C:\Users\jia'yue\.workbuddy\skills\火行人分智能体.skills\
  SKILL.md: SKILL.md（27000+字完整体系）
  references:
    - theory.md（火行人一心三界五行九层体系）
    - practice.md（B=MAP行为设计实践体系）
    - transformation.md（化克为生完整路径）
    - integration-notes.md（跨体系整合）
  templates:
    - input_template.md（诊断输入模板）
    - output_template.md（报告输出模板）
    - workflow_template.md（七步流程模板）
  test-cases: test-cases.md（测试用例）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）

土行人分智能体（已独立封装）
  路径: C:\Users\jia'yue\.workbuddy\skills\土行人分智能体.skills\
  SKILL.md: SKILL.md（15000+字完整体系）
  references:
    - theory.md（土行人一心三界五行九层体系）
    - practice.md（B=MAP行为设计实践体系）
    - transformation.md（化克为生完整路径）
    - integration-notes.md（跨体系整合）
  templates:
    - input_template.md（诊断输入模板）
    - output_template.md（报告输出模板）
    - workflow_template.md（七步流程模板）
  test-cases: test-cases.md（测试用例）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）

金行人分智能体（已独立封装）
  路径: C:\Users\jia'yue\.workbuddy\skills\金行人分智能体.skills\
  SKILL.md: SKILL.md（15000+字完整体系）
  references:
    - theory.md（金行人一心三界五行九层体系）
    - practice.md（拔阴取阳实践指南）
    - transformation.md（化克为生完整路径）
    - integration-notes.md（跨体系整合）
  templates:
    - input_template.md（诊断输入模板）
    - output_template.md（报告输出模板）
    - workflow_template.md（七步流程模板）
  test-cases: test-cases.md（测试用例）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）

水行人分智能体（已独立封装）
  路径: C:\Users\jia'yue\.workbuddy\skills\水行人分智能体.skills\
  SKILL.md: SKILL.md（9260+字完整体系）
  references:
    - theory.md（水行人一心三界五行九层体系）
    - practice.md（B=MAP行为设计实践体系）
    - transformation.md（化克为生完整路径）
    - integration-notes.md（跨体系整合）
  templates:
    - input_template.md（诊断输入模板）
    - output_template.md（报告输出模板）
    - workflow_template.md（七步流程模板）
  test-cases: test-cases.md（测试用例）
  triggers:
    - auto-trigger.json（WorkBuddy自动触发规则）
```

---

## 🔄 调用关系

### 总智能体调用分智能体

```yaml
调用方式: "引用式"
触发条件: 
  - 总智能体需要调用某个分智能体
  - 用户需要五行专门分析
调用示例: 
  - "详细分析一下木行人的性格特质"
  - "深度剖析火行人的成长路径"
```

### 调度原则

1. **独立性原则**：每个分智能体都是独立可部署的Skill，可以单独使用
2. **协同性原则**：总智能体可以调度任意组合的分智能体
3. **完整性原则**：每个分智能体都包含完整的一心三界五行九层体系
4. **复用性原则**：总智能体的理论体系可以被分智能体引用

---

## 🎯 核心优势

1. **1+5模式优势**
   - 总智能体（快思考）负责智能路由
   - 分智能体（慢思考）负责深度分析
   - 快慢结合，既精准又深入

2. **生态模式优势**
   - 主Skill + 子Skill
   - 总智能体可独立运行
   - 分智能体可独立使用
   - 灵活性高，维护方便

3. **知识复用优势**
   - 理论体系集中管理
   - 避免重复劳动
   - 知识一致性保证

4. **场景覆盖优势**
   - 七大场景（S0-S9）全覆盖
   - 每个场景都有明确的路由规则
   - 智能调度，无需人工干预

---

## 📊 质量指标

### 封装完成度

| 分智能体 | SKILL.md字数 | references文件数 | templates文件数 | test-cases | triggers |
|---------|--------------|--------------|----------------|-----------|---------|
| 木行人 | 9,260+ | 4 | 3 | ✅ | ✅ |
| 火行人 | 27,000+ | 4 | 3 | ✅ | ✅ |
| 土行人 | 15,000+ | 4 | 3 | ✅ | ✅ |
| 金行人 | 15,000+ | 4 | 3 | ✅ | ✅ |
| 水行人 | 9,260+ | 4 | 3 | ✅ | ✅ |

### 核心特性

| 特性 | 木行人 | 火行人 | 土行人 | 金行人 | 水行人 |
|-----|-------|-------|-------|-------|-------|
| 一心三界五行九层 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 拔阴取阳四步法 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 化克为生完整路径 | ✅ | ✅ | ✅ | ✅ | ✅ |
| B=MAP模型整合 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 七步诊断流程 | ✅ | ✅ | ✅ | ✅ | ✅ |
| WorkBuddy全局规则 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 🎯 下一步优化方向

### 短期优化（本月）
1. 完成Obsidian知识库的手动存储
2. 完成五行人格心理学知识图谱的总索引
3. 优化WorkBuddy自动触发的准确率

### 中期优化（下季度）
1. 构建五行人格心理学总智能体v4.0系统升级
2. 实现AI自动化调度优化
3. 扩展更多应用场景

### 长期优化（下年度）
1. 构建完整的五行人格心理学应用平台
2. 实现跨平台知识同步
3. 开发可视化交互界面

---

**五行总智能体分智能体链接 v1.0** · **生态协同导航**  
*主智能体智能调度，分智能体独立分析，1+5模式完美协同* 🔗
