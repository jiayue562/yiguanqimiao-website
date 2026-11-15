---
name: baidu-search
parent_skill: ai-os
description: Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Baidu Search

Search the web via Baidu AI Search API.

## Prerequisites

### API Key Configuration
This skill requires a **BAIDU_API_KEY** to be configured in OpenClaw.

If you don't have an API key yet, please visit:
**https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey**

For detailed setup instructions, see:
[references/apikey-fetch.md](references/apikey-fetch.md)

## Usage

```bash
python3 skills/baidu-search/scripts/search.py '<JSON>'
```

## Request Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | str | yes | - | Search query |
| count | int | no | 10 | Number of results to return, range 1-50 |
| freshness | str | no | Null | Time range, two formats: format one is ”YYYY-MM-DDtoYYYY-MM-DD“, and format two includes pd, pw, pm, and py, representing the past 24 hours, past 7 days, past 31 days, and past 365 days respectively |

## Examples

```bash
# Basic search
python3 scripts/search.py '{"query":"人工智能"}'

# Freshness first format "YYYY-MM-DDtoYYYY-MM-DD" example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"2025-09-01to2025-09-08"
}'

# Freshness second format pd、pw、pm、py example
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"pd"
}'

# set count, the number of results to return
python3 scripts/search.py '{
  "query":"旅游景点",
  "count": 20,
}'
```

## Current Status

Fully functional.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/ghost-scan-deps/agents/analyze/agent]] — Analysis Agent
- [[09-技能库/resources_CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/resources_FAQ]] — Frequently Asked Questions
- [[09-技能库/web-search-plus/FAQ]] — Frequently Asked Questions
- [[ψ技能体系/30-tools/tavily/references/api-reference]] — Tavily API Reference

<!-- AI-LINKS-END -->
