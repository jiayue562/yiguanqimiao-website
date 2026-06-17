---
name: markitdown
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
