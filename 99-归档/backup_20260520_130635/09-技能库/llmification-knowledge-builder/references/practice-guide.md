# Practice Guide.md - LLMification 实操指南

> **用途**：LLMification Knowledge Builder的实操执行手册
> **适用人群**：知识库建设者、AI系统管理员、知识工程师
> **前置条件**：已理解三层架构理论（Raw→Wiki→Schema）

---

## 🎯 实操场景

### 场景1：企业知识库建设

**背景**：
某公司有大量PDF手册、网页文档、培训材料，分散在不同平台，员工难以快速找到准确信息。

**目标**：
使用LLMification方法，构建三层架构的企业知识库。

**执行步骤**：

**Step 1：Raw Layer准备**
```
knowledge-base/
├── raw/
│   ├── 手册/
│   │   ├── 产品手册-v1.0.pdf
│   │   └── 培训手册-2024.pdf
│   ├── 网页/
│   │   ├── 官网产品介绍.html
│   │   └── 技术文档.html
│   └── 文档/
│       ├── 员工指南.docx
│       └── 流程说明.txt
```

**Step 2：Wiki Layer编译**
```bash
# 编译产品手册
/compile raw/手册/产品手册-v1.0.pdf

# 编译网页文档
/compile raw/网页/官网产品介绍.html

# 编译员工指南
/compile raw/文档/员工指南.docx
```

**输出示例**：
```markdown
---
path: knowledge-base/wiki/产品手册.md
tags: ["#产品", "#手册"]
created_at: 2026-04-08T10:00:00
lifecycle_stage: published
source_raw: raw/手册/产品手册-v1.0.pdf
---

# 产品手册 v1.0

## 核心功能

### 功能1：用户管理
- 创建用户
- 修改用户信息
- 删除用户

### 功能2：订单管理
- 创建订单
- 查询订单
- 取消订单

## 常见问题

### Q1：如何创建用户？
A：使用以下步骤...

### Q2：订单取消后如何退款？
A：参考[[退款流程]]文档。

## 相关文档
- [[员工指南]]
- [[培训手册]]
```

**Step 3：Schema Layer定义**
```bash
# 定义全局Schema
/define-schema global
```

**生成**：`CLAUDE.md`
```yaml
file_naming: "kebab-case"
tag_format: "#标签"
reference_format: "[[文档名]]"
max_heading_level: 6
```

**Step 4：Query测试**
```bash
# 自然语言查询
/query "如何创建用户账户？"

/query "订单取消后的退款流程是什么？"
```

**结果**：
```
Query: "如何创建用户账户？"
Answer: 要创建用户账户，请按照以下步骤：
1. 访问用户管理页面
2. 点击"创建用户"按钮
3. 填写用户信息
4. 点击提交

相关信息：[[产品手册]] -> 功能1：用户管理
```

---

### 场景2：个人知识资产系统化

**背景**：
个人研究者收集了大量论文、书籍笔记、网页资料，管理混乱，查找困难。

**目标**：
构建个人三层知识库系统，提升知识管理效率。

**执行步骤**：

**Step 1：Raw Layer整理**
```
personal-kb/
├── raw/
│   ├── 论文/
│   │   ├── 论文1.pdf
│   │   └── 论文2.pdf
│   ├── 书籍/
│   │   ├── 书籍1笔记.md
│   │   └── 书籍2笔记.md
│   └── 网页/
│       ├── 文章1.html
│       └── 文章2.html
```

**Step 2：增量编译**
```bash
# 先编译核心论文
/compile raw/论文/论文1.pdf

# 再编译书籍笔记
/compile raw/书籍/书籍1笔记.md

# 增量编译网页资料
/update "机器学习"
```

**输出示例**：
```markdown
---
path: personal-kb/wiki/机器学习核心概念.md
tags: ["#机器学习", "#深度学习", "#神经网络"]
created_at: 2026-04-08T12:00:00
lifecycle_stage: published
---

# 机器学习核心概念

## 核心理论

### 神经网络
神经网络是机器学习的一种模型...

### 深度学习
深度学习是神经网络的延伸...

## 相关研究

### 论文1：[[Attention Is All You Need]]
核心观点：Transformer架构的核心...

### 论文2：[[BERT: Pre-training of Deep Bidirectional Transformers]]
核心贡献：预训练语言模型...

## 实践应用

### 应用1：图像识别
参考[[计算机视觉]]

### 应用2：自然语言处理
参考[[NLP技术栈]]
```

**Step 3：一致性检查**
```bash
# 检查整个知识库
/check all

# 修复发现的孤岛
/merge ["孤岛1.md", "孤岛2.md"]
```

---

### 场景3：AI原生内容管理

**背景**：
需要为AI Agent（如Claude、GPT）构建优化的知识库，提升响应质量。

**目标**：
使用LLMification方法，创建AI原生的知识表达。

**执行步骤**：

**Step 1：设计AI友好结构**
```markdown
# AI优化版知识库

## 核心概念（LLM易于理解）

### 概念定义
使用清晰的定义和示例...

### 算法步骤
使用编号和代码块...

## 常见问题（FAQ格式）

### 问题1：[具体问题]
**答案**：[简洁准确回答]

**相关概念**：[[概念1]], [[概念2]]
```

**Step 2：Wiki Layer优化**
```bash
/compile raw/资料/技术文档.md
```

**优化输出**：
```markdown
---
path: ai-kb/wiki/技术文档-ai版.md
tags: ["#AI优化", "#技术文档"]
format: "markdown"
---

# 技术文档 - AI优化版

## 快速参考

### API端点
| 端点 | 方法 | 描述 |
|-------|------|------|
| /api/users | GET | 获取用户列表 |
| /api/users/:id | GET | 获取单个用户 |
| /api/users | POST | 创建用户 |

### 常见错误
| 错误码 | 原因 | 解决方案 |
|-------|------|---------|
| 400 | 参数错误 | 检查参数格式 |
| 401 | 未授权 | 检查API密钥 |
| 404 | 资源不存在 | 确认资源ID |

## 详细说明

### 创建用户
```python
# 示例代码
import requests

response = requests.post(
    "http://api.example.com/api/users",
    json={
        "name": "张三",
        "email": "zhangsan@example.com"
    },
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

print(response.json())
```

## 相关文档
- [[API文档完整版]]
- [[错误处理指南]]
```

**Step 3：Schema Layer配置**
```yaml
# CLAUDE.md
ai_knowledge_base:
  style: "technical"
  format_preference: "code-first"
  response_style: "concise"
  max_context_length: 4000
```

---

## 🛠️ 常见问题与解决方案

### Q1：Raw Layer应该放什么文件？

**A**：
- ✅ 原始资料（PDF、DOCX、HTML、Text）
- ✅ 未经LLM修改的文档
- ❌ 不要放已经Wiki化的文档

### Q2：如何处理重复内容？

**A**：
使用`/merge`指令：
```bash
/merge ["文档1.md", "文档2.md"]
```
LLM会自动识别重复内容并合并。

### Q3：Schema Layer如何定义？

**A**：
根据知识库的用途定义：
```yaml
# 个人知识库
scope: "personal"
rules:
  file_naming: "snake_case"
  tag_format: "#个人笔记"

# 企业知识库
scope: "corporate"
rules:
  file_naming: "kebab-case"
  tag_format: "#官方文档"
```

### Q4：如何更新已有知识？

**A**：
使用`/update`指令进行增量更新：
```bash
/update "机器学习"
```
LLM会找到相关文档并追加新内容。

### Q5：知识库多大合适？

**A**：
- 个人知识库：建议< 1000个文档
- 企业知识库：建议< 10000个文档
- 超过建议拆分为多个子知识库

---

## 📊 性能优化建议

### 1. 分层存储
```
knowledge-base/
├── raw/           # 原始资料（冷存储）
├── wiki/          # 结构化知识（热存储）
└── schema/        # 行为规则（规则存储）
```

### 2. 增量编译
- 避免全量重编
- 使用`/update`进行增量更新
- 定期执行`/check`维护一致性

### 3. 索引优化
- 建立清晰的标签体系
- 使用双向链接建立知识网络
- 控制文档长度（建议< 5000字）

### 4. 查询优化
- 使用精确的自然语言查询
- 避免过于宽泛的关键词
- 结合标签和引用进行精准检索

---

## 🔗 工具集成

### 与Obsidian集成

**存储路径**：
```bash
knowledge-base/wiki/ → Obsidian库
```

**配置**：
```json
{
  "attachmentFolderPath": "knowledge-base/raw",
  "newFileLocation": "current",
  "newFileTemplatePath": "templates/wiki-template.md"
}
```

### 与WorkBuddy集成

**自动触发**：
- 当检测到"知识库建设"、"文档整理"等关键词时自动激活
- 自动执行`/compile`、`/update`、`/query`等操作

**配置**：
```yaml
# WorkBuddy Rule
triggers:
  - "知识库"
  - "文档整理"
  - "资料系统化"
auto_operations:
  - "/compile"
  - "/update"
  - "/check"
```

---

## ✅ 质量检查清单

在发布知识库前，使用此清单进行质量检查：

### Raw Layer检查
- [ ] 所有文件都在`raw/`文件夹
- [ ] 文件格式统一（PDF/DOCX/HTML/Text）
- [ ] 文件名清晰明确
- [ ] 没有重复文件

### Wiki Layer检查
- [ ] 所有文档符合Markdown格式
- [ ] 标题层级清晰（最多6级）
- [ ] 标签体系统一（使用#前缀）
- [ ] 双向链接完整（使用`[[文档名]]`）
- [ ] 元数据完整（YAML frontmatter）

### Schema Layer检查
- [ ] `CLAUDE.md`已定义
- [ ] `AGENTS.md`已定义（如需要）
- [ ] 规则清晰明确
- [ ] 版本控制信息完整

### 整体检查
- [ ] 一致性检查通过（`/check`）
- [ ] 无知识孤岛
- [ ] 查询响应准确
- [ ] 性能满足要求

---

## 📚 进阶主题

### 主题1：多语言知识库

**方法**：
在Wiki Layer中使用语言标签：
```markdown
---
tags: ["#技术", "#English", "#中文"]
---
```

### 主题2：版本管理

**方法**：
在文件名中包含版本：
```bash
knowledge-base/wiki/产品手册-v1.0.md
knowledge-base/wiki/产品手册-v2.0.md
```

### 主题3：权限控制

**方法**：
在Schema Layer中定义访问规则：
```yaml
access_control:
  public:
    - tags: ["#公开", "#文档"]
  internal:
    - tags: ["#内部", "#流程"]
  admin:
    - tags: ["#管理", "#配置"]
```

---

**实操指南版本**：v1.0  
**最后更新**：2026-04-08  
**维护者**：龙龟神将
