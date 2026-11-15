# Theory.md - LLMification 理论依据

> **来源**：Andrej Karpathy的"LLM Wiki"方法论
> **核心论文**：从检索增强（RAG）到知识编译（Knowledge Compilation）的范式跃迁
> **关键洞察**：LLM Native知识表达是知识管理的未来方向

---

## 📖 核心理论

### 范式转变

**传统模式：检索增强生成（RAG）**
```
用户查询 → 检索外部知识库 → 找到相关片段 → 输入LLM → 生成回答
```

**LLMification模式：知识编译**
```
原始资料 → LLM编译 → 结构化Wiki → 自然语言查询 → LLM直接回答
```

**核心差异**：
- RAG：检索时实时搜索，响应速度慢，上下文窗口限制
- LLMification：预编译知识，LLM原生表达，检索精准度高

---

## 🏗️ 三层架构理论

### Raw Layer（原始资料层）

**定义**：未经LLM修改的只读原始资料

**特点**：
- 文件夹：`raw/`
- 格式：PDF/DOCX/HTML/Text
- 属性：绝对只读，LLM只能"读取不能修改"
- 作用：保证源资料的完整性与可追溯性

**设计原则**：
```
Raw Layer的"只读"是知识可信性的根基
任何对原始资料的修改都应溯源到明确的版本控制
```

---

### Wiki Layer（LLM工作区）

**定义**：LLM维护的结构化知识图谱

**特点**：
- 格式：Markdown（LLM原生表达）
- 维护者：LLM（可增删改）
- 结构：层级标题 + 双向链接 + 标签体系
- 作用：知识编译后的LLM可理解表达

**Wiki Layer的设计原则**：
```markdown
# 标题（层级清晰）

## 核心概念
- 使用项目符号和编号
- 避免冗长的段落
- LLM擅长结构化信息

## 代码示例
```python
def example():
    pass
```

## 双向链接
- [[相关概念1]]：说明关联关系
- [[相关文档2]]：建立知识网络

## 标签
#标签1 #标签2 #标签3
```

---

### Schema Layer（机器行为规则层）

**定义**：机器可理解的知识库行为规则

**组成**：
- `CLAUDE.md`：Claude AI的行为规则
- `AGENTS.md`：其他AI Agent的行为规则

**作用**：
- 定义文件命名规范
- 定义标签体系
- 定义引用格式
- 定义元数据格式
- 约束LLM在Wiki Layer的行为

**Schema Layer示例**：
```yaml
file_naming: "kebab-case"
tag_format: "#tag"
reference_format: "[[document_name]]"
metadata_format: "YAML frontmatter"
max_heading_level: 6
compilation_rules:
  - "保留原始资料的核心信息"
  - "使用LLM原生表达"
  - "建立双向链接"
```

---

## 🔄 知识生命周期理论

### Entry阶段（增量编译）

**流程**：
```
Raw Layer文件 → LLM理解 → 语义分析 → 结构化 → Wiki Layer Markdown
```

**核心算法**：
```python
def compile_to_wiki(raw_content):
    # 1. 语义理解
    topics = extract_topics(raw_content)
    
    # 2. 结构化
    structure = organize_hierarchical(topics)
    
    # 3. LLM原生表达
    wiki_md = to_llm_native_format(structure)
    
    # 4. 添加元数据
    wiki_md = add_metadata(wiki_md)
    
    # 5. Schema校验
    if validate_schema(wiki_md):
        return wiki_md
    else:
        return schema_violation_report
```

---

### Query阶段（检索调用）

**流程**：
```
自然语言查询 → 语义搜索（Wiki Layer）→ 相关片段 → Invoke → 回答
```

**核心算法**：
```python
def query_handler(natural_query):
    # 1. 语义搜索
    wiki_segments = semantic_search(natural_query)
    
    # 2. Schema约束
    valid_segments = filter_by_schema(wiki_segments)
    
    # 3. Invoke
    answer = invoke_llm(valid_segments)
    
    return answer
```

**优势**：
- 语义搜索：而非关键词匹配
- Schema约束：保证回答的规范性与一致性
- 直接调用：无需复杂的检索拼接

---

### Check阶段（自修复）

**流程**：
```
一致性检查 → 孤岛检测 → 修复建议 → 自动修复
```

**检查项**：
- Wiki Layer与Schema Layer的一致性
- 知识孤岛（未被引用的文档）
- 标签一致性
- 双向链接完整性

**自修复算法**：
```python
def self_repair_check():
    # 1. 一致性检查
    violations = check_schema_consistency()
    
    # 2. 孤岛检测
    orphans = detect_knowledge_orphans()
    
    # 3. 修复建议
    repair_suggestions = generate_repair_suggestions(violations, orphans)
    
    # 4. 自动修复
    repaired = auto_repair(repair_suggestions)
    
    return {
        "violations": violations,
        "orphans": orphans,
        "repaired": repaired
    }
```

---

## 🔮 未来发展方向

### 1. 微调Fine-tuning

**概念**：
基于Wiki Layer的知识，对LLM进行专有领域微调。

**优势**：
- 知识内化到模型参数中
- 减少检索依赖
- 提升响应速度与质量

**挑战**：
- 需要大量训练数据
- 计算资源消耗大
- 知识更新困难

---

### 2. Internalization内部化

**概念**：
将外部知识库"消化"为模型的内化知识。

**意义**：
- 真正的知识理解（而非存储）
- 更强的推理能力
- 更好的泛化性能

**路径**：
```
Raw Layer → Wiki Layer → 微调 → Internalization
```

---

## 💡 核心金句

1. **"从检索增强到知识编译，是知识管理的范式跃迁"**

2. **"LLM Native知识表达，是知识管理的未来方向"**

3. **"Raw Layer的只读，是知识可信性的根基"**

4. **"Wiki Layer是LLM的工作区，但受Schema Layer约束"**

5. **"知识不是存储的，而是编译的、内化的"**

---

**理论文档版本**：v1.0  
**最后更新**：2026-04-08  
**维护者**：龙龟神将
