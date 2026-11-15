---
name: hermes-agent
parent_skill: ai-os
description: Invoke Hermes Agent (NousResearch open-source AI Agent) to process tasks.
---

# Hermes Agent Skill

## Function
Invoke Hermes Agent (NousResearch open-source AI Agent) to process tasks.

## Usage

### 1. Single Query (Recommended)
```powershell
hermes -z "your question"
```

### 2. Interactive Chat
```powershell
hermes
```

### 3. Resume Last Session
```powershell
hermes -c
```

## Configuration
- Config file: `C:\Users\jia'yue\.hermes\config.yaml`
- API Key file: `C:\Users\jia'yue\.hermes\.env`
- Current model: **DeepSeek** (deepseek-chat)

## Available Commands
| Command | Description |
|---------|-------------|
| `hermes` | Start interactive TUI |
| `hermes -z "query"` | Single query mode |
| `hermes -c` | Resume last session |
| `hermes -m <model>` | Temporarily switch model |
| `hermes status` | Show status |
| `hermes model` | Switch default model |
| `hermes skills` | Manage Skills |
| `hermes dashboard` | Start Web UI (port 9119) |

## Examples
**User**: "Help me use Hermes to query Python best practices"
**Assistant**: Call `hermes -z "Python best practices"` and return results

## Notes
- Hermes is a standalone program, not a built-in QClaw feature
- Configured with DeepSeek API (direct access in China, no proxy needed)
- Supports 200+ models (via OpenRouter or other providers)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/baidu-search/SKILL]] — Baidu Search
- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>
- [[09-技能库/resources_CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/web-search-plus/CHANGELOG]] — Changelog - Web Search Plus
- [[ψ技能体系/20-claws/03-academy/xhs-publish-note/BOOTSTRAP]] — BOOTSTRAP.md - Hello, World
- [[ψ技能体系/30-tools/himalaya/references/configuration]] — Himalaya Configuration Reference

<!-- AI-LINKS-END -->
