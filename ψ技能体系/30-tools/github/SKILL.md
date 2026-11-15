---
name: github
parent_skill: ai-os
description: "Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries."
description_zh: "管理 GitHub Issues、PR 和 CI"
description_en: "Manage GitHub issues, PRs, and CI runs"
version: 1.0.0
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Pull Requests

Check CI status on a PR:
```bash
gh pr checks 55 --repo owner/repo
```

List recent workflow runs:
```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:
```bash
gh run view <run-id> --repo owner/repo
```

View logs for failed steps only:
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## API for Advanced Queries

The `gh api` command is useful for accessing data not available through other subcommands.

Get PR with specific fields:
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON Output

Most commands support `--json` for structured output.  You can use `--jq` to filter:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/ghost-scan-deps/agents/scan/agent]] — Scan Agent
- [[09-技能库/resources_CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/resources_FAQ]] — Frequently Asked Questions
- [[09-技能库/web-search-plus/FAQ]] — Frequently Asked Questions
- [[ψ技能体系/30-tools/github-cli/SKILL]] — GitHub Skill

<!-- AI-LINKS-END -->
