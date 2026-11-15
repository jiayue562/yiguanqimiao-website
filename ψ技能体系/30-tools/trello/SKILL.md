---
name: trello
parent_skill: ai-os
description: "Manage Trello boards, lists, and cards via the Trello REST API."
description_zh: "管理 Trello 看板、列表和卡片"
description_en: "Manage Trello boards, lists, and cards"
version: 1.0.0
---

# Trello Skill

Manage Trello boards, lists, and cards directly from the terminal.

## Setup

1. Get your API key: https://trello.com/app-key
2. Generate a token (click "Token" link on that page)
3. Set environment variables:
   ```bash
   export TRELLO_API_KEY="your-api-key"
   export TRELLO_TOKEN="your-token"
   ```

## Usage

All commands use curl to hit the Trello REST API.

### List boards
```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### List lists in a board
```bash
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

### Create a card
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Card description"
```

### Move a card
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

## Notes

- Board/List/Card IDs can be found in the Trello URL or via the list commands
- Rate limits: 300 requests per 10 seconds per API key

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>
- [[09-技能库/resources_FAQ]] — Frequently Asked Questions
- [[09-技能库/resources_template-finding]] — Secret Finding: <title>
- [[09-技能库/web-search-plus/FAQ]] — Frequently Asked Questions
- [[ψ技能体系/30-tools/browser-use/references/cdp-python]] — Raw CDP & Python Session Reference

<!-- AI-LINKS-END -->
