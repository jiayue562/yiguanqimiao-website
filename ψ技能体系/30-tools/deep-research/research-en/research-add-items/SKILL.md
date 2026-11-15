---
name: deep-research-en-add-items
user-invocable: true
description: Add items (research objects) to existing research outline.
allowed-tools: Bash, Read, Write, Glob, WebSearch, Task, AskUserQuestion
---

# Research Add Items - Supplement Research Objects

## Trigger
`/research-add-items`

## Workflow

### Step 1: Auto-locate Outline
Find `*/outline.yaml` file in current working directory, auto-read.

### Step 2: Get Supplement Sources in Parallel
Simultaneously:
- **A. Ask user**: What items to supplement? Any specific names?
- **B. Ask if Web Search needed**: Launch agent to search for more items?

### Step 3: Merge and Update
- Append new items to outline.yaml
- Display to user for confirmation
- Avoid duplicates
- Save updated outline

## Output
Updated `{topic}/outline.yaml` file (in-place modification)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-code/SKILL]] — Find Issues
- [[09-技能库/self-learning/SKILL]] — Self-Learning Skill Generator
- [[ψ技能体系/30-tools/deep-research/research-en/research-add-fields/SKILL]] — Research Add Fields - Supplement Research Fields
- [[ψ技能体系/30-tools/deep-research/research-en/research-deep/SKILL]] — Research Deep - Deep Research
- [[ψ技能体系/30-tools/deep-research/research-en/research-report/SKILL]] — Research Report - Summary Report
- [[ψ技能体系/30-tools/deep-research/research-en/research/SKILL]] — Research Skill - Preliminary Research

<!-- AI-LINKS-END -->
