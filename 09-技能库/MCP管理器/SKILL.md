---
name: mcporter
description: "Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation."
description_zh: "管理和调用 MCP 服务器与工具"
description_en: "Manage and call MCP servers & tools"
version: 1.0.0
---

# mcporter

Use `mcporter` to work with MCP servers directly.

Quick start
- `mcporter list`
- `mcporter list <server> --schema`
- `mcporter call <server.tool> key=value`

Call tools
- Selector: `mcporter call linear.list_issues team=ENG limit:5`
- Function syntax: `mcporter call "linear.create_issue(title: \"Bug\")"`
- Full URL: `mcporter call https://api.example.com/mcp.fetch url:https://example.com`
- Stdio: `mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com`
- JSON payload: `mcporter call <server.tool> --args '{"limit":5}'`

Auth + config
- OAuth: `mcporter auth <server | url> [--reset]`
- Config: `mcporter config list|get|add|remove|import|login|logout`

Daemon
- `mcporter daemon start|status|stop|restart`

Codegen
- CLI: `mcporter generate-cli --server <name>` or `--command <url>`
- Inspect: `mcporter inspect-cli <path> [--json]`
- TS: `mcporter emit-ts <server> --mode client|types`

Notes
- Config default: `./config/mcporter.json` (override with `--config`).
- Prefer `--output json` for machine-readable results.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>
- [[09-技能库/ghost-scan-secrets/agents/scan/agent]] — Scan Agent
- [[09-技能库/resources_template-finding]] — Secret Finding: <title>
- [[ψ技能体系/30-tools/MCP管理器/SKILL]] — mcporter
- [[ψ技能体系/30-tools/api-gateway/references/sunsama-mcp/README]] — Sunsama MCP Routing Reference
- [[ψ技能体系/30-tools/mcp-builder/reference/mcp_best_practices]] — MCP Server Best Practices
- [[ψ技能体系/30-tools/mcporter/SKILL]] — mcporter

<!-- AI-LINKS-END -->
