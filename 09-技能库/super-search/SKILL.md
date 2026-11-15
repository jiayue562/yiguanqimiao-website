---
name: super-search
description: Search your coding memory. Use when user asks about past work, previous sessions, how something was implemented, what they worked on before, or wants to recall information from earlier sessions.
allowed-tools: Bash(node:*)
---

# Super Search

Search Supermemory for past coding sessions, decisions, and saved information.

## How to Search

Run the search script with the user's query and optional scope flag:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" [--user|--repo|--both] "USER_QUERY_HERE"
```

### Scope Flags

- `--both` (default): Search both personal session and project memories across team members in parallel
- `--user`: Search personal/user memories across sessions
- `--repo`: Search project/repo memories across team members

## Examples

- User asks "what did I work on yesterday":

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" "work yesterday recent activity"
  ```

- User asks "how did we implement auth" (project-specific):

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" --repo "authentication implementation"
  ```

- User asks "what are my coding preferences":
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" --user "coding preferences style"
  ```

## Present Results

The script outputs formatted memory results with timestamps and relevance scores. Present them clearly to the user and offer to search again with different terms if needed.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/resources_FAQ]] — Frequently Asked Questions
- [[09-技能库/self-improving/boundaries]] — Security Boundaries
- [[09-技能库/web-search-plus/FAQ]] — Frequently Asked Questions
- [[ψ技能体系/10-kernel/龙心OS/self-improving/boundaries]] — Security Boundaries
- [[ψ技能体系/20-claws/03-academy/xhs-publish-note/AGENTS]] — AGENTS.md - Your Workspace
- [[ψ技能体系/30-tools/agent-team-orchestration/references/communication]] — Communication

<!-- AI-LINKS-END -->
