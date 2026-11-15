---
name: deep-research-en-add-fields
user-invocable: true
description: Add field definitions to existing research outline.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Fields - Supplement Research Fields

## Trigger
`/research-add-fields`

## Workflow

### Step 1: Auto-locate Fields File
Find `*/fields.yaml` file in current working directory, auto-read existing fields definitions.

### Step 2: Get Supplement Source
Ask user to choose:
- **A. User direct input**: User provides field names and descriptions
- **B. Web Search**: Launch agent to search common fields in this domain

### Step 3: Display and Confirm
- Display suggested new fields list
- User confirms which fields to add
- User specifies field category and detail_level

### Step 4: Save Update
Append confirmed fields to fields.yaml, save file.

## Output
Updated `{topic}/fields.yaml` file (in-place modification, requires user confirmation)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-code/SKILL]] — Find Issues
- [[09-技能库/ghost-scan-secrets/agents/summarize/agent]] — Summarize Agent
- [[ψ技能体系/30-tools/deep-research/research-en/research-add-items/SKILL]] — Research Add Items - Supplement Research Objects
- [[ψ技能体系/30-tools/deep-research/research-en/research-deep/SKILL]] — Research Deep - Deep Research
- [[ψ技能体系/30-tools/deep-research/research-en/research-report/SKILL]] — Research Report - Summary Report
- [[ψ技能体系/30-tools/deep-research/research-en/research/SKILL]] — Research Skill - Preliminary Research

<!-- AI-LINKS-END -->
