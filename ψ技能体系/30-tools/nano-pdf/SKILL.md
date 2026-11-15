---
name: nano-pdf
parent_skill: ai-os
description: "Edit PDFs with natural-language instructions using the nano-pdf CLI."
description_zh: "用自然语言编辑 PDF 文件"
description_en: "Edit PDFs with natural language"
version: 1.0.0
---

# nano-pdf

Use `nano-pdf` to apply edits to a specific page in a PDF using a natural-language instruction.

## Quick start

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
```

Notes:
- Page numbers are 0-based or 1-based depending on the tool's version/config; if the result looks off by one, retry with the other.
- Always sanity-check the output PDF before sending it out.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Skill安全扫描（朱雀实验室）/SKILL]] — Tencent Zhuque Skill Scanner
- [[09-技能库/humanizer/README]] — Humanizer
- [[09-技能库/humanizer/SKILL]] — Humanizer: Remove AI Writing Patterns
- [[ψ技能体系/30-tools/adaptive-subagents/SKILL]] — Adaptive Subagent Routing

<!-- AI-LINKS-END -->
