# FIX — Repair Broken Formulas in an Existing xlsx

This is an EDIT task. You MUST preserve all original sheets and data. Never create a new workbook.

## Workflow

```bash
# Step 1: Identify errors
python3 SKILL_DIR/scripts/formula_check.py input.xlsx --json

# Step 2: Unpack
python3 SKILL_DIR/scripts/xlsx_unpack.py input.xlsx /tmp/xlsx_work/

# Step 3: Fix each broken <f> element in the worksheet XML using the Edit tool
#   (see Error-to-Fix mapping below)

# Step 4: Pack and validate
python3 SKILL_DIR/scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
python3 SKILL_DIR/scripts/formula_check.py output.xlsx
```

## Error-to-Fix Mapping

| Error | Fix Strategy |
|-------|-------------|
| `#DIV/0!` | Wrap: `IFERROR(original_formula, "-")` |
| `#NAME?` | Fix misspelled function (e.g. `SUMM` → `SUM`) |
| `#REF!` | Reconstruct the broken reference |
| `#VALUE!` | Fix type mismatch |

For the full list of Excel error types and advanced diagnostics, see `validate.md`.

## Critical Rules

- The output MUST contain the same sheets as the input. Do NOT create a new workbook.
- Only modify the specific `<f>` elements that are broken — everything else must be untouched.
- After packing, always run `formula_check.py` to confirm all errors are resolved.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Excel 文件处理/SKILL]] — MiniMax XLSX Skill
- [[09-技能库/Excel 文件处理/references/create]] — Build New xlsx from Scratch
- [[09-技能库/Excel 文件处理/references/edit]] — Minimal-Invasive Editing of Existing xlsx
- [[09-技能库/Excel 文件处理/references/format]] — Financial Formatting & Output Standards — Complete Agent Guide
- [[09-技能库/Excel 文件处理/references/ooxml-cheatsheet]] — OOXML SpreadsheetML Cheat Sheet
- [[09-技能库/Excel 文件处理/references/validate]] — Formula Validation & Recalculation Guide
- [[09-技能库/ghost-scan-code/prompts/analyzer]] — Analyzer Agent
- [[ψ技能体系/30-tools/Excel 文件处理/SKILL]] — MiniMax XLSX Skill
- [[ψ技能体系/30-tools/deep-research/research-en/research/SKILL]] — Research Skill - Preliminary Research
- [[ψ技能体系/30-tools/minimax-docx/references/openxml_element_order]] — OpenXML Child Element Ordering Rules

<!-- AI-LINKS-END -->
