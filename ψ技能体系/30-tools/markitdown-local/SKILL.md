---
name: markitdown-local
parent_skill: ai-os
description: |
  统一文档转换技能 - 将 PDF/DOCX/PPTX/Excel/图片/音频转换为可读的 Markdown 内容。
  当用户需要读取非文本格式文件（PDF、Word、PPT、Excel、图片、音频）时使用此技能。
  支持批量转换和内容提取。
metadata:
  openclaw:
    emoji: '📄'
    requires: { }
---

# markitdown-local - 统一文档转换

## 功能

- **PDF → Markdown**: 提取文本 + 保留结构
- **DOCX → Markdown**: 保留样式 + 表格
- **PPTX → Markdown**: 每页幻灯片转章节
- **XLSX → Markdown**: 表格转 Markdown 表格
- **图片 → 文本**: OCR 识别 (中文/英文)
- **音频 → 文本**: 语音转录

## 使用方式

### 方式 1: 使用现有技能组合

```powershell
# PDF 转图片 + OCR
python -m pdf2image input.pdf
# 然后用 vision-3.5.0 处理图片

# DOCX/XLSX/PPTX
# 使用对应的专用技能：
# - excel-xlsx-1.0.2
# - word-docx-1.0.2
# - powerpoint-pptx-1.0.1
```

### 方式 2: Python 脚本

```python
# 安装 markitdown
pip install markitdown

# 使用
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("file.pdf")
print(result.text_content)
```

## 已安装替代技能

| 格式 | 技能 | 命令 |
|------|------|------|
| PDF | `pdf-to-image-preview` | 转图片后 OCR |
| DOCX | `word-docx-1.0.2` | 直接读取 |
| XLSX | `excel-xlsx-1.0.2` | 直接读取 |
| PPTX | `powerpoint-pptx-1.0.1` | 直接读取 |
| 图片 | `vision-3.5.0` | OCR 识别 |
| 音频 | `openai-whisper` | 语音转文字 |

## 推荐工作流

```
用户请求：读取 [文件]
    ↓
判断格式
    ↓
PDF → pdf-to-image → vision OCR
DOCX → word-docx 技能
XLSX → excel-xlsx 技能
PPTX → powerpoint-pptx 技能
图片 → vision OCR
音频 → whisper 转录
    ↓
合并输出 Markdown
```

## 注意事项

1. **PDF 处理**: 扫描件需要 OCR，文本 PDF 可直接提取
2. **大文件**: 超过 50MB 建议分批处理
3. **加密文件**: 需要密码的文件无法处理
4. **表格复杂**: 复杂表格可能格式丢失

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[16-工具与资源/工具技能_PPT读取技能包]] — PPT读取技能包
- [[09-技能库/PPT读取/test-cases]] — PPT读取 Skill 测试用例
- [[09-技能库/腾讯文档/references/slide_references]] — 幻灯片（Slide / PPT）参考文档
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/workbuddy-delivery-tier2]] — WorkBuddy 交付链与 Tier2 插件（FBS）

<!-- AI-LINKS-END -->
