---
name: super-save
parent_skill: ai-os
description: Save important project knowledge to memory. Use when user wants to preserve architectural decisions, significant bug fixes, design patterns, or important implementation details for team reference.
allowed-tools: Bash(node *)
---

# Super Save

Save important project knowledge based on what the user wants to preserve.

## Step 1: Understand User Request

Analyze what the user is asking to save from the conversation.

## Step 2: Format Content

```
[SAVE:<username>:<date>]

<Username> wanted to <goal/problem>.

Claude suggested <approach/solution>.

<Username> decided to <decision made>.

<key details, files if relevant>

[/SAVE]
```

Example:
```
[SAVE:prasanna:2026-02-04]

Prasanna wanted to create a skill for saving project knowledge.

Claude suggested using a separate container tag (repo_<hash>) for shared team knowledge.

Prasanna decided to keep it simple - no transcript fetching, just save what user asks for.

Files: src/save-project-memory.js, src/lib/container-tag.js

[/SAVE]
```

Keep it natural. Capture the conversation flow.

## Step 3: Save

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/save-project-memory.cjs" "FORMATTED_CONTENT"
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/automation-workflows/SKILL]] — Automation Workflows
- [[09-技能库/humanizer/README]] — Humanizer
- [[09-技能库/humanizer/SKILL]] — Humanizer: Remove AI Writing Patterns
- [[09-技能库/self-improving/learning]] — Learning Mechanics
- [[09-技能库/笔记搜索/SKILL]] — qmd - Quick Markdown Search

<!-- AI-LINKS-END -->
