---
name: markitdown
parent_skill: ai-os
version: 1.0
description: 将 PDF/DOCX/PPTX/Excel 等文档转换为 Markdown 格式
tags: [markitdown, 文档转换, PDF转换, Word转换, Excel转换]
---


# Markitdown 技能

## 技能简介
多格式文档转Markdown工具，支持PDF、DOCX、PPTX、Excel等格式转换为可读文本。

## 触发关键词
- markitdown
- 文档转换
- PDF转Markdown
- Word转Markdown
- Excel转Markdown
- 读取PDF
- 读取Word文档

## 核心功能
1. **PDF转换**：将PDF文件转换为Markdown
2. **Word转换**：将DOCX/DOC文件转换为Markdown
3. **Excel转换**：将XLSX/XLS文件转换为Markdown表格
4. **PPT转换**：将PPTX文件转换为Markdown

## 使用方法

### 安装命令
```bash
npm install -g markitdown
```

### 基本使用
```bash
markitdown document.pdf -o output.md
markitdown document.docx -o output.md
markitdown spreadsheet.xlsx -o output.md
```

### 在龙龟神将中使用
直接发送文件路径给我，我会自动识别并转换：
```
请读取并总结这个文件：
D:\文档\报告.pdf
```

## 支持的格式
| 格式 | 扩展名 | 支持程度 |
|------|--------|----------|
| PDF | .pdf | ✅ 完全支持 |
| Word | .docx, .doc | ✅ 完全支持 |
| Excel | .xlsx, .xls | ✅ 完全支持 |
| PowerPoint | .pptx, .ppt | ✅ 完全支持 |
| 图片 | .png, .jpg | ✅ OCR识别 |
| 文本 | .txt, .md | ✅ 直接读取 |

## 替代方案
如果markitdown未安装，我也可以：
1. 直接读取纯文本文件（.txt, .md）
2. 使用read_file工具读取图片并进行OCR
3. 尝试其他在线转换服务

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[16-工具与资源/工具技能_PPT读取技能包]] — PPT读取技能包
- [[20-工作记录与复盘/journal_2026-04-14_每日备份报告]] — 2026-04-14 Obsidian备份执行报告
- [[09-技能库/PPT读取/test-cases]] — PPT读取 Skill 测试用例
- [[09-技能库/ima-skill/notes/references/api]] — IMA笔记 API
- [[09-技能库/腾讯文档/references/docengine_references]] — DOC 编辑引擎 API 参考

<!-- AI-LINKS-END -->
