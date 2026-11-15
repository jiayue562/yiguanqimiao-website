---
name: cloudflare
parent_skill: ai-os
description: Cloudflare 平台全面参考文档——Workers、D1、R2、AI Gateway、Durable Objects、WAF、Zero Trust、Pages 等 100+ 产品。当用户询问 Cloudflare 相关技术问题时，作为权威参考知识源。
---

# Cloudflare Platform Reference

When the user asks about Cloudflare products, architecture, or deployment:

1. **Workers** → Serverless functions, 100+ languages, 300+ locations
   - Use Wrangler CLI for local dev/deploy
   - Durable Objects for stateful workloads
   - Cron Triggers for scheduled tasks

2. **D1** → Serverless SQLite database, REST API access
3. **R2** → S3-compatible object storage, no egress fees
4. **AI Gateway** → Universal gateway for 100+ AI model providers
5. **Workers AI** → Run AI models on Cloudflare's global network
6. **Pages** → Static site hosting with CI/CD integration
7. **Zero Trust** → Identity-aware access control
8. **DDoS/WAF** → Edge security with customizable rules

## CLI Commands
- wrangler → Workers CLI (init/dev/deploy)
- 
px wrangler → Without global install
- opencode code --provider cloudflare-ai-gateway → Use CF as model provider

## MCP
Cloudflare API MCP server provides access to 2,500+ API endpoints.
Configure in opencode.json as a remote MCP server.

## Quick Links
- Docs: https://developers.cloudflare.com/
- Workers Playground: https://workers.cloudflare.com/playground
- Dashboard: https://dash.cloudflare.com/

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Skill安全扫描（朱雀实验室）/SKILL]] — Tencent Zhuque Skill Scanner
- [[09-技能库/codeconductor/skills]] — Skills Profile — Code Creation & AI Development
- [[09-技能库/resources_CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/self-improving/boundaries]] — Security Boundaries
- [[09-技能库/skill-creator/SKILL]] — Skill Creator
- [[09-技能库/web-search-plus/CHANGELOG]] — Changelog - Web Search Plus

<!-- AI-LINKS-END -->
