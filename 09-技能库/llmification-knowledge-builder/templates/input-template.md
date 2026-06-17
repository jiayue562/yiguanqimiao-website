# LLMification 输入模板

> **用途**：标准化LLMification Knowledge Builder的输入格式
> **版本**：v1.0

---

## 📋 基本信息

| 字段 | 说明 | 示例 |
|------|------|------|
| **知识库名称** | 知识库的标识名称 | "企业产品知识库" |
| **作用域** | global（全局）或 specific（特定） | "corporate" |
| **知识库路径** | 知识库的根目录 | `D:\knowledge-base\` |
| **版本** | 知识库版本号 | "v1.0" |

---

## 📂 文件夹结构

```
{知识库路径}/
├── raw/                  # Raw Layer - 原始资料（只读）
│   ├── 手册/
│   │   ├── 产品手册-v1.0.pdf
│   │   └── 员工手册.pdf
│   ├── 文档/
│   │   ├── 技术文档.md
│   │   └── 流程说明.md
│   ├── 网页/
│   │   ├── 官网介绍.html
│   │   └── API文档.html
│   └── 其他/
│       ├── 会议记录.docx
│       └── 培训材料.pptx
│
├── wiki/                 # Wiki Layer - 结构化知识（LLM维护）
│   ├── 核心概念/
│   ├── 操作指南/
│   ├── 常见问题/
│   └── 参考资料/
│
└── schema/               # Schema Layer - 机器行为规则
    ├── CLAUDE.md
    └── AGENTS.md
```

---

## 📄 Raw Layer 输入规范

### 原始资料清单

| 文件名 | 类型 | 路径 | 描述 |
|--------|------|------|------|
| 示例文件.pdf | PDF | `raw/手册/` |  |
| 示例文档.docx | DOCX | `raw/文档/` |  |
| 示例网页.html | HTML | `raw/网页/` |  |
| 示例笔记.md | Markdown | `raw/文档/` |  |

### 原始资料元数据

```yaml
raw_material:
  file_name: "文件名"
  file_path: "raw/子文件夹/文件名.扩展名"
  file_type: "pdf/docx/html/text"
  encoding: "utf-8"
  language: "zh-CN/en-US"
  created_at: "ISO8601"
  updated_at: "ISO8601"
  lifecycle_stage: "pending/compiled"
```

---

## 📝 Wiki Layer 输入规范

### 编译参数

```yaml
compilation_params:
  llm_model: "gpt-4/claude-3.5-sonnet"
  temperature: 0.3
  max_tokens: 4000
  output_format: "markdown"
  preserve_structure: true
  add_metadata: true
  create_links: true
```

### Wiki 文档规范

```yaml
wiki_document:
  path: "wiki/子文件夹/文件名.md"
  title: "文档标题"
  tags: ["#标签1", "#标签2", "#标签3"]
  references: ["[[相关文档1]]", "[[相关文档2]]"]
  metadata:
    created_at: "ISO8601"
    updated_at: "ISO8601"
    lifecycle_stage: "draft/published"
    source_raw: "raw/原始文件名"
    version: "v1.0"
    author: "作者名"
```

---

## 🔒 Schema Layer 输入规范

### Schema 定义

```yaml
schema_definition:
  scope: "global/specific"
  version: "1.0"
  rules:
    file_naming: "kebab-case/snake_case"
    tag_format: "#tag"
    reference_format: "[[document_name]]"
    metadata_format: "YAML frontmatter"
    max_heading_level: 6
    max_file_size: 50000  # 字符数
    allowed_formats: ["md"]
  compilation_constraints:
    - "保留原始资料的核心信息"
    - "使用LLM原生表达（Markdown+Mermaid+代码块）"
    - "建立双向链接网络"
    - "添加元数据标签"
```

### 行为规则示例

#### CLAUDE.md

```yaml
claud_behavior:
  style: "technical/concise"
  tone: "professional/friendly"
  response_format: "structured"
  max_context_length: 4000
  code_examples: true
  mermaid_diagrams: true
```

#### AGENTS.md

```yaml
agent_behavior:
  default_model: "gpt-4"
  fallback_model: "gpt-3.5-turbo"
  max_retries: 3
  timeout: 30
  cache_enabled: true
  cache_ttl: 3600
```

---

## 🔄 生命周期管理

### 编译状态

```yaml
lifecycle:
  raw_to_wiki:
    status: "pending/in_progress/completed/failed"
    started_at: "ISO8601"
    completed_at: "ISO8601"
    error_message: "错误信息（如有）"
  
  wiki_validation:
    status: "pending/in_progress/completed/failed"
    validation_results:
      schema_compliance: "pass/fail"
      link_integrity: "pass/fail"
      tag_consistency: "pass/fail"
      orphan_detection: "pass/fail"
  
  knowledge_check:
    status: "pending/in_progress/completed"
    check_timestamp: "ISO8601"
    violation_count: 0
    orphan_count: 0
    repair_count: 0
```

---

## 📊 质量指标

### 编译质量指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| 结构完整性 | 标题层级、段落结构清晰 | 100% |
| 内容保留度 | 保留原始资料核心信息比例 | ≥ 95% |
| LLM原生性 | Markdown、代码块、Mermaid图表使用 | 100% |
| 元数据完整度 | YAML frontmatter、标签、引用 | 100% |
| 链接完整性 | 双向链接、引用文档存在 | 100% |

### 一致性检查指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| Schema符合度 | 符合Schema Layer规则的比例 | 100% |
| 链接有效性 | 所有链接指向存在的文档 | 100% |
| 标签一致性 | 标签格式和分类一致 | 100% |
| 孤岛检测 | 未被引用的文档数量 | 0 |

---

## 🎯 编译请求模板

### 批量编译请求

```yaml
batch_compile_request:
  knowledge_base: "知识库名称"
  scope: "corporate"
  sources:
    - "raw/手册/*.pdf"
    - "raw/文档/*.docx"
    - "raw/网页/*.html"
  compilation_params:
    llm_model: "gpt-4"
    temperature: 0.3
    max_tokens: 4000
  schema_definition: "schema/config.yaml"
  output_path: "wiki/"
  notification:
    on_success: "email/webhook"
    on_failure: "email/webhook"
```

### 增量更新请求

```yaml
incremental_update_request:
  knowledge_base: "知识库名称"
  action: "merge"
  sources:
    - "raw/新文档.pdf"
  target_topic: "主题关键词"
  update_strategy: "append/merge/replace"
  validation_required: true
```

---

## 🔍 查询输入格式

### 自然语言查询

```yaml
query_request:
  user_query: "自然语言查询问题"
  scope: "global/specific"
  max_results: 5
  include_references: true
  response_format: "markdown/code/json"
  context_length: 2000
```

### 查询优化建议

| 查询类型 | 示例 | 优化建议 |
|-----------|------|-----------|
| 事实查询 | "产品的核心功能是什么？" | 使用具体的关键词 |
| 流程查询 | "如何创建用户账户？" | 分步骤描述流程 |
| 对比查询 | "功能A和功能B的区别是什么？" | 明确对比维度 |
| 示例查询 | "给我一个代码示例" | 指定编程语言和场景 |

---

## ⚠️ 错误处理

### 常见错误类型

| 错误类型 | 说明 | 解决方案 |
|-----------|------|---------|
| 文件格式错误 | 原始文件格式不支持 | 转换为支持的格式（PDF/DOCX/HTML/Text） |
| 编码错误 | 文件编码问题 | 统一使用UTF-8编码 |
| Schema违规 | Wiki文档不符合Schema规则 | 根据Schema Layer规则修正 |
| 链接失效 | 引用的文档不存在 | 检查文档路径或创建缺失文档 |
| 编译失败 | LLM编译过程失败 | 检查LLM API连接和参数配置 |

### 错误恢复流程

```yaml
error_recovery:
  step1: "记录错误日志"
  step2: "分析错误原因"
  step3: "提供修复建议"
  step4: "自动修复（如可能）"
  step5: "人工审核（自动修复失败时）"
```

---

## 📈 性能监控

### 编译性能指标

| 指标 | 说明 | 记录频率 |
|------|------|---------|
| 编译耗时 | 单个文档编译时间 | 每次编译 |
| 编译成功率 | 成功编译文档比例 | 每日汇总 |
| LLM调用次数 | LLM API调用总次数 | 每日汇总 |
| Token消耗 | 编译过程消耗的Token数 | 每日汇总 |
| 错误率 | 编译失败比例 | 每日汇总 |

### 查询性能指标

| 指标 | 说明 | 记录频率 |
|------|------|---------|
| 查询响应时间 | 从查询到响应的时间 | 每次查询 |
| 检索准确率 | 相关文档在前5结果中的比例 | 每周汇总 |
| 答案质量评分 | 用户对答案质量的评分 | 每周汇总 |
| 缓存命中率 | 从缓存获取答案的比例 | 每周汇总 |

---

**输入模板版本**：v1.0  
**最后更新**：2026-04-08  
**维护者**：龙龟神将
