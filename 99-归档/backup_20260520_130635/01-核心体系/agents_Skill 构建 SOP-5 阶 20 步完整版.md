# Skill 构建 SOP - 5 阶 20 步完整版

> 🔧 从理论到 Skill 的工业化生产流程 · 第四步核心交付物

---

## 📋 流程总览

```
阶段一：理论解析 (Step 1-4)
    ↓
阶段二：架构设计 (Step 5-8)
    ↓
阶段三：SKILL.md 编码 (Step 9-12)
    ↓
阶段四：测试验证 (Step 13-15)
    ↓
阶段五：部署上线 (Step 16-20)
```

**总耗时**: 手动 3-5 小时 → Skill Builder 自动化 30-60 分钟

---

## 📍 阶段一：理论解析（Step 1-4）

### Step 1: 核心定义提取

**提问**: 这个 Skill 解决什么问题？

**输出**: 一句话核心定义（<30 字）

**检验**: 能否一句话说清

**模板**:
```
[动词] + [对象] + [价值]
例：自动化构建 Skill 包，从理论到部署 30 分钟完成
```

---

### Step 2: 可执行操作流程识别

**拆解**: 理论里有几个"操作步骤"？

**排序**: 这些步骤的逻辑优先级是什么？

**输出**: N 步操作流程图

**模板**:
```mermaid
graph LR
    A[步骤 1] --> B[步骤 2]
    B --> C[步骤 3]
    C --> D[步骤 N]
```

---

### Step 3: 输入输出规范化

| 维度 | 内容 |
|------|------|
| **Input** | 用户提供什么信息？ |
| **Process** | Skill 内部如何处理？ |
| **Output** | 返回什么具体结果？ |

**模板**:
```yaml
input:
  required:
    - field1: string
    - field2: string
  optional:
    - field3: string

process:
  - step1: validate input
  - step2: process logic
  - step3: generate output

output:
  format: markdown/json
  fields:
    - result: string
    - details: array
```

---

### Step 4: 核心算法/逻辑提炼

**识别**: 理论中的"关键决策点"在哪？

**规则**: 每个决策点的规则是什么？

**输出**: 决策树/流程图

**模板**:
```
IF 条件 A THEN
    执行动作 X
ELSE IF 条件 B THEN
    执行动作 Y
ELSE
    执行动作 Z
```

---

## 📍 阶段二：架构设计（Step 5-8）

### Step 5: Skill 粒度判断

**问题 1**: 这个 Skill 是单体还是生态？
- 单体：一个 SKILL.md 搞定
- 生态：主 Skill + 子 Skill（需要协调）

**问题 2**: 有没有依赖关系？
- 独立：可单独调用
- 依赖：需要先调 X 再调 Y

**输出**: Skill 生态图

**判断矩阵**:

| 维度 | 单体 Skill | 生态 Skill |
|------|------------|------------|
| 操作步数 | 3-7 步 | 8 步以上 |
| 决策点数 | 1-2 个 | 3 个以上 |
| 依赖关系 | 独立 | 有依赖链 |
| 触发复杂度 | 简单 | 复杂 |

---

### Step 6: 触发机制设计

| 维度 | 说明 | 示例 |
|------|------|------|
| **直接触发词** | 用户明确说出 | "构建 Skill" |
| **场景触发词** | 隐含指向 | "这个流程能自动化吗" |
| **信号触发** | 对话中的行为信号 | 重复操作≥3 次 |

**输出**: 四维触发矩阵

---

### Step 7: 关键词权重设计

| 优先级 | 权重 | 说明 |
|--------|------|------|
| P0 | 5 | 绝对触发 |
| P1 | 4 | 强触发 |
| P2 | 3 | 弱触发 |

**输出**: 权重表

---

### Step 8: 与现有 Skills 的关系映射

**问题**: 与哪些 Skills 协同？

**流程**: 调用顺序是什么？

**输出**: 协同图

**模板**:
```yaml
collaborations:
  - skill: skill-vetter
    relation: downstream
    trigger: on_skill_generated
  
  - skill: memory-systems
    relation: parallel
    share: usage_data
```

---

## 📍 阶段三：SKILL.md 编码（Step 9-12）

### Step 9: SKILL.md 主文档编写

**【必填部分】**
1. 标题 + 版本
2. 一句话核心定义
3. 三行问题陈述（What/Why/How）
4. 核心能力（3-5 个子能力）
5. 使用边界

**【功能设计部分】**
6. 触发条件（直接词 + 场景 + 信号）
7. 激活后的行为（第一步 - 第 N 步）
8. 核心原则（禁忌 + 必须）
9. 与其他 Skills 的关系

**【实现部分】**
10. 标准输入格式
11. 处理流程（伪代码/决策树）
12. 标准输出格式
13. 示例（真实案例）
14. 异常处理

---

### Step 10: References 参考资料编写

| 文件 | 内容 | 必填 |
|------|------|------|
| theory.md | 理论完整版 | ⭕ 推荐 |
| practice-guide.md | 实操指南 | ⭕ 推荐 |
| prompts.md | 提示词模板 | ⭕ 推荐 |
| sop.md | 标准操作流程 | ⭕ 推荐 |

---

### Step 11: Templates 模板库编写

| 文件 | 内容 | 必填 |
|------|------|------|
| input_template.md | 输入模板 | ✅ 必须 |
| output_template.md | 输出模板 | ✅ 必须 |
| workflow_template.md | 流程模板 | ⭕ 推荐 |

---

### Step 12: Triggers 触发配置编写

| 文件 | 内容 | 必填 |
|------|------|------|
| trigger-rules.yaml | 关键词权重表 | ✅ 必须 |
| skill-routes.yaml | 与其他 Skills 关系 | ✅ 必须 |
| auto-activate.json | 自动触发规则 | ⭕ 推荐 |

---

## 📍 阶段四：测试验证（Step 13-15）

### Step 13: 单点测试用例设计

| 用例 | 场景 | 目的 |
|------|------|------|
| 用例 1 | 标准场景 | 验证基本功能 |
| 用例 2 | 边界场景 | 验证特殊情况 |
| 用例 3 | 负面场景 | 验证不误触发 |

**输出**: 测试结果表

---

### Step 14: 集成测试

**问题 1**: 与其他 Skills 协同是否正常？

**问题 2**: 触发机制是否误触发？

**问题 3**: 输出是否符合预期？

---

### Step 15: 反馈收集与优化

| 维度 | 检查项 |
|------|--------|
| 准确性 | 触发是否准确？ |
| 完整性 | 逻辑是否完整？ |
| 实用性 | 解决问题了吗？ |

**输出**: 优化清单

---

## 📍 阶段五：部署上线（Step 16-20）

### Step 16: 目录结构部署

```
~/.OpcCla 知识库/skills/[SkillName]/
├── SKILL.md（主文档）
├── references/
│   ├── theory.md
│   ├── practice-guide.md
│   ├── prompts.md
│   └── sop.md
├── templates/
│   ├── input_template.md
│   ├── output_template.md
│   └── workflow_template.md
└── triggers/
    ├── trigger-rules.yaml
    ├── skill-routes.yaml
    └── auto-activate.json
```

---

### Step 17: OpcCla 知识库配置注册

在 `.OpcCla 知识库/rules/` 中创建 `[SkillName]-trigger.mdc`

配置：`alwaysApply: true / global scope`

---

### Step 18: Obsidian 同步

- 将 SKILL.md 同步到知识库的对应目录
- 建立双向链接
- 更新索引

---

### Step 19: 使用验证

- 在实际对话中调用
- 记录反馈（效果怎样？有没有 bug？）
- 收集数据（触发次数/误触发/满意度）

---

### Step 20: 迭代优化

- 每月审视一次使用数据
- 根据反馈优化触发规则
- 根据实际场景扩展能力
- 更新版本号

---

## 📊 质量底线标准

### 必须满足（否则拒绝发布）

| 标准 | 检查方式 |
|------|----------|
| 核心定义 <30 字 | 字数检查 |
| 触发关键词权重表完整 | 文件存在性 |
| 测试用例至少 3 个 | 数量检查 |
| 与其他 Skills 关系图清晰 | 视觉检查 |
| 版本迭代计划明确 | 文件存在性 |

---

## 🔧 Skill Builder 自动化

### 触发词
- "构建 Skill"
- "创建技能"
- "帮我设计一个 Skill"
- "从理论创建 Skill"

### 输入
理论文档 / 核心定义 / 操作流程

### 处理流程
1. 阶段一：自动提取核心定义
2. 阶段二：自动设计触发机制
3. 阶段三：自动生成 SKILL.md 框架
4. 阶段四：自动生成测试用例
5. 阶段五：输出完整 Skill 包

### 输出
- SKILL.md（已填充 70% 内容）
- references/ 空框架
- templates/ 空框架
- triggers/ 空框架
- 检查清单（需手工完成的 30%）

---

## 📌 快速参考

### 5 阶 20 步清单

```
阶段一：理论解析
☐ Step 1: 核心定义提取
☐ Step 2: 操作流程识别
☐ Step 3: 输入输出规范
☐ Step 4: 核心算法提炼

阶段二：架构设计
☐ Step 5: Skill 粒度判断
☐ Step 6: 触发机制设计
☐ Step 7: 关键词权重
☐ Step 8: 协作关系映射

阶段三：SKILL.md 编码
☐ Step 9: 主文档编写
☐ Step 10: References
☐ Step 11: Templates
☐ Step 12: Triggers

阶段四：测试验证
☐ Step 13: 单点测试
☐ Step 14: 集成测试
☐ Step 15: 反馈优化

阶段五：部署上线
☐ Step 16: 目录部署
☐ Step 17: 配置注册
☐ Step 18: Obsidian 同步
☐ Step 19: 使用验证
☐ Step 20: 迭代优化
```

---

_龙心 OS Skill 构建 SOP v1.0 · 最后更新：2026-04-13 · 悟空 × 龙龟 共同维护_
