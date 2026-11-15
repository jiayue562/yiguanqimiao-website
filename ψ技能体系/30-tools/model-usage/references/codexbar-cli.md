# CodexBar CLI quick ref (usage + cost)

## Install
- App: Preferences -> Advanced -> Install CLI
- Repo: ./bin/install-codexbar-cli.sh

## Commands
- Usage snapshot (web/cli sources):
  - codexbar usage --format json --pretty
  - codexbar --provider all --format json
- Local cost usage (Codex + Claude only):
  - codexbar cost --format json --pretty
  - codexbar cost --provider codex|claude --format json

## Cost JSON fields
The payload is an array (one per provider).
- provider, source, updatedAt
- sessionTokens, sessionCostUSD
- last30DaysTokens, last30DaysCostUSD
- daily[]: date, inputTokens, outputTokens, cacheReadTokens, cacheCreationTokens, totalTokens, totalCost, modelsUsed, modelBreakdowns[]
- modelBreakdowns[]: modelName, cost
- totals: totalInputTokens, totalOutputTokens, cacheReadTokens, cacheCreationTokens, totalTokens, totalCost

## Notes
- Cost usage is local-only. It reads JSONL logs under:
  - Codex: ~/.codex/sessions/**/*.jsonl
  - Claude: ~/.config/claude/projects/**/*.jsonl or ~/.claude/projects/**/*.jsonl
- If web usage is required (non-local), use codexbar usage (not cost).

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[16-工具与资源/templates_journal]] — {{DATE}}
- [[09-技能库/obsidian/SKILL]] — Obsidian
- [[09-技能库/笔记搜索/SKILL]] — qmd - Quick Markdown Search
- [[ψ技能体系/30-tools/adaptive-subagents/SKILL]] — Adaptive Subagent Routing
- [[ψ技能体系/30-tools/kimi-webbridge/SKILL]] — Kimi WebBridge
- [[ψ技能体系/30-tools/model-usage/SKILL]] — Model usage

<!-- AI-LINKS-END -->
