---
name: summarize-local
parent_skill: ai-os
description: |
  内容摘要技能 - 自动摘要长文章/PDF/网页/视频/知乎/微博等内容。
  当用户需要快速了解长内容核心要点时使用此技能。
  支持多种内容源和输出格式。
metadata:
  openclaw:
    emoji: '📝'
    requires: { }
---

# summarize-local - 内容摘要

## 功能

- **网页摘要**: 提取核心内容，去除广告和导航
- **PDF 摘要**: 提取关键章节和结论
- **视频摘要**: YouTube/B 站/抖音内容总结
- **文章摘要**: 公众号/知乎/微博长文
- **多格式输出**: 摘要/大纲/关键引用

## 使用方式

### 方式 1: 使用现有技能组合

```powershell
# 网页内容
web_fetch <url> --extractMode markdown
# 然后用 AI 总结

# 视频
# 使用 web_search 查找视频转录
# 然后总结
```

### 方式 2: Python 脚本

```python
# 安装 sumy 或其他摘要库
pip install sumy

# 使用
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer

parser = PlaintextParser.from_string(text)
summarizer = LsaSummarizer()
summary = summarizer(parser.document, 5)  # 5 句摘要
```

## 已安装替代技能

| 功能 | 技能 |
|------|------|
| 网页抓取 | `web_fetch` |
| 网页搜索 | `web-search-plus` |
| 长文处理 | `notesmd` + AI 总结 |
| 视频处理 | `web_search` + AI 总结 |

## 推荐工作流

```
用户提供：URL / 文件 / 文本
    ↓
判断内容源
    ↓
网页 → web_fetch 抓取 → AI 总结
PDF → 提取文本 → AI 总结
视频 → 查找转录 → AI 总结
文本 → 直接 AI 总结
    ↓
输出结构化摘要
```

## 输出格式

```markdown
# [标题] 摘要

## 核心结论
[1-3 句直接答案]

## 关键要点
- 要点 1
- 要点 2
- 要点 3

## 重要数据
- 数据 1 (来源)
- 数据 2 (来源)

## 行动建议
1. [具体行动]
2. [具体行动]

## 原文来源
[URL/文件路径]
```

## 注意事项

1. **长度控制**: 摘要长度根据原文调整
2. **准确性**: 关键数据需标注来源
3. **客观性**: 保持原文观点，不添加主观判断
4. **长内容**: 超过 10 万字建议分段总结

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[01-核心体系/agents_LLM Wiki 知识库激活完成报告]] — LLM Wiki 知识库激活完成报告
- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[01-核心体系/agents_龙心 OS 自主学习系统指令手册]] — 龙心 OS 自主学习系统 - 完整指令手册
- [[16-工具与资源/工具技能_PPT读取技能包]] — PPT读取技能包
- [[08-龙心OS核心系统/记忆系统/TOOLS]] — TOOLS.md - 可用的工具与技能（龙龟神将工具库）

<!-- AI-LINKS-END -->
