---
name: PPT读取
disable: true
allowed-tools: 
---

# PPT读取 · 文档转换Skill

> **核心定位**：将PowerPoint演示文稿转换为结构化Markdown文档，便于AI深度分析和知识沉淀。
> **版本**：v1.0 | **创建日期**：2026-04-14 | **维护者**：龙龟神将

---

## 📖 核心定义

### What（是什么）
PPT读取Skill是一个**文档格式转换工具**，使用python-pptx库提取PPT中的文本内容、表格数据，并转换为Markdown格式，便于后续AI分析、知识管理和内容沉淀。

### Why（为什么）
- PPT格式难以直接进行文本分析和知识提取
- 转换为Markdown后便于版本控制、搜索和AI处理
- 支持表格结构化输出，保留数据完整性
- 便于将PPT内容沉淀到Obsidian知识库

### How（怎么做）
```
PPT文件 → python-pptx解析 → 提取文本/表格 → 生成Markdown → AI分析/知识沉淀
```

---

## ⚡ 触发条件

### P0·直接触发词（权重5·绝对触发）
- 读取PPT、PPT转换、PPT转Markdown
- 解析PPT、提取PPT内容、PPT内容读取
- 安装PPT技能、PPT读取技能

### P1·场景触发词（权重4·强触发）
- 分析PPT、查看PPT内容、PPT里有啥
- 月度经营分析、经营数据PPT
- 转换演示文稿、幻灯片内容

### P2·信号触发（权重3·弱触发）
- 用户提到PPT文件路径
- 需要分析PPT中的数据
- 需要将PPT内容转为文本

---

## 🎯 核心流程

### 使用方式

#### 方式一：命令行直接执行（推荐）

**步骤1：安装依赖**
```bash
pip install python-pptx
```

**步骤2：执行转换脚本**
```bash
python "C:\Users\jia'yue\WorkBuddy\20260414225819\read_ppt.py"
```

**步骤3：读取生成的Markdown文件**
转换完成后，在 `C:\Users\jia'yue\WorkBuddy\20260414225819\月度经营分析.md` 查看结果

#### 方式二：Python代码调用

```python
from pptx import Presentation

# 读取PPT
prs = Presentation("PPT文件路径.pptx")

# 遍历所有幻灯片
for i, slide in enumerate(prs.slides, 1):
    print(f"\n## 第{i}页\n")
    
    # 提取文本
    for shape in slide.shapes:
        if hasattr(shape, "text") and shape.text.strip():
            print(shape.text.strip())
        
        # 提取表格
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                row_text = " | ".join([cell.text for cell in row.cells])
                print(f"| {row_text} |")
```

---

## 📋 输入输出规范

### 输入规范
| 输入项 | 类型 | 说明 | 必需 |
|--------|------|------|------|
| PPT文件路径 | string | PowerPoint文件(.pptx)的完整路径 | ✅ |
| 输出路径 | string | Markdown文件的保存路径 | 可选 |

### 输出规范
| 输出项 | 类型 | 说明 |
|--------|------|------|
| Markdown文件 | .md | 包含所有幻灯片内容的结构化文档 |
| 表格数据 | Markdown表格 | PPT中的表格转换为Markdown表格格式 |

### 输出格式示例
```markdown
# PPT标题

## 第1页

标题内容

正文内容...

## 第2页

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
```

---

## 🔧 技术实现

### 依赖库
- **python-pptx**: PowerPoint文件解析库
- **Python 3.6+**: 运行环境

### 核心代码结构
```python
# 1. 导入库
from pptx import Presentation

# 2. 加载PPT
prs = Presentation(ppt_path)

# 3. 遍历幻灯片
for slide in prs.slides:
    # 提取文本
    for shape in slide.shapes:
        if hasattr(shape, "text"):
            # 处理文本
            
        if shape.has_table:
            # 处理表格
```

### 功能特性
- ✅ 提取所有幻灯片的文本内容
- ✅ 将表格转换为Markdown格式
- ✅ 保留页面结构（按页组织）
- ✅ 支持中文内容
- ✅ 输出UTF-8编码

---

## 🚀 使用场景

### 场景1：经营分析PPT解析
```
输入：2026年月度经营分析.pptx
输出：月度经营分析.md
用途：AI深度分析经营数据、提取关键指标、生成洞察报告
```

### 场景2：培训课件内容提取
```
输入：培训课程.pptx
输出：培训内容.md
用途：知识沉淀、制作学习笔记、生成问答对
```

### 场景3：会议演示文档归档
```
输入：会议汇报.pptx
输出：会议纪要.md
用途：存档管理、全文检索、内容复用
```

---

## 📁 文件位置

### Skill文件
- **Skill路径**: `~/.workbuddy/skills/PPT读取/`
- **主文档**: `SKILL.md`
- **转换脚本**: `C:\Users\jia'yue\WorkBuddy\20260414225819\read_ppt.py`

### 输出文件
- **默认输出**: `C:\Users\jia'yue\WorkBuddy\20260414225819\月度经营分析.md`

---

## 🔄 与其他Skills的协作

| Skills | 协作方式 | 说明 |
|--------|---------|------|
| 📚 **知识学习** | 后置调用 | PPT转Markdown后，用知识学习进行深度分析 |
| 🐉 **象思维** | 后置调用 | 从PPT内容中提取核心洞察和原象 |
| 🌈 **五色光思维** | 后置调用 | 对PPT内容进行多维度分析 |
| 🔄 **知行合一** | 后置调用 | 将PPT分析结果沉淀到知识库 |

---

## 📝 待办事项

- [ ] 支持PPT中的图片提取和描述
- [ ] 支持图表数据提取
- [ ] 支持批量转换多个PPT文件
- [ ] 集成到龙心OS自动工作流

---

**PPT读取 Skill v1.0** · **龙龟神将**
*让PPT内容触手可及，让知识沉淀更加高效* 📊
