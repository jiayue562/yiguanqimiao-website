---
name: model-usage
parent_skill: ai-os
description: Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current (most recent) model or a full model breakdown. Trigger when asked for model-level usage/cost data from codexbar, or when you need a scriptable per-model summary from codexbar cost JSON.
version: 1.0.0
metadata: {"clawdbot":{"emoji":"📊","os":["darwin"],"requires":{"bins":["codexbar"]},"install":[{"id":"brew-cask","kind":"brew","cask":"steipete/tap/codexbar","bins":["codexbar"],"label":"Install CodexBar (brew cask)"}]}}
---

# Model usage

## Overview
Get per-model usage cost from CodexBar's local cost logs. Supports "current model" (most recent daily entry) or "all models" summaries for Codex or Claude.

TODO: add Linux CLI support guidance once CodexBar CLI install path is documented for Linux.

## Quick start
1) Fetch cost JSON via CodexBar CLI or pass a JSON file.
2) Use the bundled script to summarize by model.

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

## Current model logic
- Uses the most recent daily row with `modelBreakdowns`.
- Picks the model with the highest cost in that row.
- Falls back to the last entry in `modelsUsed` when breakdowns are missing.
- Override with `--model <name>` when you need a specific model.

## Inputs
- Default: runs `codexbar cost --format json --provider <codex|claude>`.
- File or stdin:

```bash
codexbar cost --provider codex --format json > /tmp/cost.json
python {baseDir}/scripts/model_usage.py --input /tmp/cost.json --mode all
cat /tmp/cost.json | python {baseDir}/scripts/model_usage.py --input - --mode current
```

## Output
- Text (default) or JSON (`--format json --pretty`).
- Values are cost-only per model; tokens are not split by model in CodexBar output.

## References
- Read `references/codexbar-cli.md` for CLI flags and cost JSON fields.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Skill安全扫描（朱雀实验室）/SKILL]] — Tencent Zhuque Skill Scanner
- [[09-技能库/ghost-scan-deps/SKILL]] — Ghost Security SCA Scanner — Orchestrator
- [[09-技能库/ghost-scan-secrets/SKILL]] — Ghost Security Secrets Scanner — Orchestrator
- [[09-技能库/obsidian/SKILL]] — Obsidian
- [[ψ技能体系/00-foundation/obsidian/SKILL]] — Obsidian
- [[ψ技能体系/30-tools/model-usage/references/codexbar-cli]] — CodexBar CLI quick ref (usage + cost)

<!-- AI-LINKS-END -->
