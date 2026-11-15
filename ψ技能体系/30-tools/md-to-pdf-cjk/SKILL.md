---
name: md-to-pdf-cjk
parent_skill: ai-os
description: Convert Markdown files to professional PDF documents with full CJK (Chinese/Japanese/Korean) support. Uses reportlab for reliable rendering without external dependencies like wkhtmltopdf or LaTeX.
author: zacjiang
version: 1.0.0
tags: markdown, pdf, chinese, japanese, korean, CJK, convert, report, document
---

# Markdown to PDF (CJK Support)

Convert Markdown to professional PDFs with full Chinese/Japanese/Korean text support.

## Why This Exists

Most Markdown-to-PDF tools break on CJK characters, require LaTeX, or need heavy dependencies. This skill uses reportlab for lightweight, reliable PDF generation that works on any server — including 2GB RAM VPS instances.

## Usage

```bash
python3 {baseDir}/scripts/md_to_pdf.py input.md "Document Title" output.pdf
```

## Features

- ✅ Full CJK text rendering (Chinese, Japanese, Korean)
- ✅ Markdown headings, bold, italic, bullet lists, code blocks
- ✅ Tables with proper column alignment
- ✅ Automatic page breaks and numbering
- ✅ Lightweight — runs on minimal servers (2GB RAM)
- ✅ No LaTeX, no wkhtmltopdf, no Chrome/Puppeteer needed

## Supported Markdown Elements

- `# H1` through `#### H4` headings
- `**bold**` and `*italic*`
- `- bullet lists` (nested supported)
- `| table | rows |` (pipe-delimited tables)
- `` `inline code` `` and ``` code blocks ```
- `---` horizontal rules

## Dependencies

```bash
pip3 install reportlab
```

## Font Configuration

The script auto-detects CJK fonts in common locations:
- `/usr/share/fonts/` (Linux)
- `/System/Library/Fonts/` (macOS)

If no CJK font is found, it falls back to Helvetica (CJK characters will not render). Install a CJK font:

```bash
# RHEL/CentOS/Alibaba Cloud Linux
sudo yum install -y google-noto-sans-cjk-ttc-fonts

# Ubuntu/Debian
sudo apt install -y fonts-noto-cjk
```

## Use Cases

- Generate PDF reports from AI analysis (audit reports, summaries)
- Convert documentation to distributable format
- Create invoices, proposals, or contracts in CJK languages
- Batch convert multiple Markdown files to PDF

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-deps/README]] — Ghost SCA Scanner
- [[09-技能库/self-improving/heartbeat-rules]] — Heartbeat Rules
- [[ψ技能体系/30-tools/markitdown-skill/SKILL]] — MarkItDown Skill
- [[ψ技能体系/30-tools/minimax-docx/references/cjk_typography]] — CJK Typography & Mixed-Script Guide
- [[ψ技能体系/30-tools/minimax-docx/references/troubleshooting]] — Troubleshooting Guide — Symptom-Driven
- [[ψ技能体系/30-tools/minimax-docx/references/typography_guide]] — Professional Document Design & Typography Guide

<!-- AI-LINKS-END -->
