# Fathom Routing Reference

**App name:** `fathom`
**Base URL proxied:** `api.fathom.ai`

## API Path Pattern

```
/fathom/external/v1/{resource}
```

## Common Endpoints

### List Meetings
```bash
GET /fathom/external/v1/meetings
```

With filters:
```bash
GET /fathom/external/v1/meetings?created_after=2025-01-01T00:00:00Z&teams[]=Sales
```

### Get Summary
```bash
GET /fathom/external/v1/recordings/{recording_id}/summary
```

Async callback:
```bash
GET /fathom/external/v1/recordings/{recording_id}/summary?destination_url=https://example.com/webhook
```

### Get Transcript
```bash
GET /fathom/external/v1/recordings/{recording_id}/transcript
```

Async callback:
```bash
GET /fathom/external/v1/recordings/{recording_id}/transcript?destination_url=https://example.com/webhook
```

### List Teams
```bash
GET /fathom/external/v1/teams
```

### List Team Members
```bash
GET /fathom/external/v1/team_members?team=Sales
```

### Create Webhook
```bash
POST /fathom/external/v1/webhooks
Content-Type: application/json

{
  "destination_url": "https://example.com/webhook",
  "triggered_for": ["my_recordings", "my_shared_with_team_recordings"],
  "include_transcript": true,
  "include_summary": true,
  "include_action_items": true
}
```

### Delete Webhook
```bash
DELETE /fathom/external/v1/webhooks/{id}
```

## Notes

- Recording IDs are integers
- Timestamps are in ISO 8601 format
- OAuth users cannot use inline transcript/summary parameters on `/meetings` endpoint - use dedicated `/recordings/{id}/summary` and `/recordings/{id}/transcript` endpoints instead
- Use cursor-based pagination with `cursor` parameter
- Webhook `triggered_for` options: `my_recordings`, `shared_external_recordings`, `my_shared_with_team_recordings`, `shared_team_recordings`
- Webhook secrets are used to verify webhook signatures

## Resources

- [Fathom API Documentation](https://developers.fathom.ai)
- [LLM Reference](https://developers.fathom.ai/llms.txt)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/attio/README]] — Attio Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/baserow/README]] — Baserow Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/cal-com/README]] — Cal.com Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/calendly/README]] — Calendly Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/callrail/README]] — CallRail Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clickfunnels/README]] — ClickFunnels Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/fireflies/README]] — Fireflies Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/granola-mcp/README]] — Granola MCP Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/manus/README]] — Manus Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/microsoft-teams/README]] — Microsoft Teams Routing Reference

<!-- AI-LINKS-END -->
