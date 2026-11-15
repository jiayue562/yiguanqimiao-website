# Calendly Routing Reference

**App name:** `calendly`
**Base URL proxied:** `api.calendly.com`

## API Path Pattern

```
/calendly/{resource}
```

## Common Endpoints

### Get Current User
```bash
GET /calendly/users/me
```

### List Event Types
```bash
GET /calendly/event_types?user=USER_URI&active=true
```

### Get an Event Type
```bash
GET /calendly/event_types/{uuid}
```

### List Scheduled Events
```bash
GET /calendly/scheduled_events?user=USER_URI&status=active&min_start_time=2025-03-01T00:00:00Z
```

### Get a Scheduled Event
```bash
GET /calendly/scheduled_events/{uuid}
```

### Cancel a Scheduled Event
```bash
POST /calendly/scheduled_events/{uuid}/cancellation
Content-Type: application/json

{
  "reason": "Meeting rescheduled"
}
```

### List Event Invitees
```bash
GET /calendly/scheduled_events/{event_uuid}/invitees
```

### Get Available Times
```bash
GET /calendly/event_type_available_times?event_type=EVENT_TYPE_URI&start_time=2025-03-15T00:00:00Z&end_time=2025-03-22T00:00:00Z
```

### Get User Busy Times
```bash
GET /calendly/user_busy_times?user=USER_URI&start_time=2025-03-15T00:00:00Z&end_time=2025-03-22T00:00:00Z
```

### List Organization Memberships
```bash
GET /calendly/organization_memberships?organization=ORGANIZATION_URI
```

### List Webhook Subscriptions
```bash
GET /calendly/webhook_subscriptions?organization=ORGANIZATION_URI&scope=organization
```

### Create Webhook Subscription
```bash
POST /calendly/webhook_subscriptions
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "events": ["invitee.created", "invitee.canceled"],
  "organization": "ORGANIZATION_URI",
  "scope": "organization"
}
```

### Delete Webhook Subscription
```bash
DELETE /calendly/webhook_subscriptions/{uuid}
```

## Notes

- Resource identifiers are full URIs (e.g., `https://api.calendly.com/users/AAAA`)
- Timestamps are in ISO 8601 format
- Availability endpoints have a 7-day maximum range per request
- Webhooks require a paid Calendly plan (Standard, Teams, or Enterprise)
- Available webhook events: `invitee.created`, `invitee.canceled`, `routing_form_submission.created`
- Use `page_token` for pagination

## Resources

- [Calendly Developer Portal](https://developer.calendly.com/)
- [API Reference](https://developer.calendly.com/api-docs)
- [Event Types](https://developer.calendly.com/api-docs/e2f95ebd44914-list-user-s-event-types)
- [Scheduled Events](https://developer.calendly.com/api-docs/d61a40b4ea90e-list-events)
- [Availability](https://developer.calendly.com/api-docs/4241cf0f7f0d4-get-event-type-available-times)
- [Webhooks](https://developer.calendly.com/api-docs/c1ddc06ce1f1a-create-webhook-subscription)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/acuity-scheduling/README]] — Acuity Scheduling Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/airtable/README]] — Airtable Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/apify/README]] — Apify Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/apollo/README]] — Apollo Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/beehiiv/README]] — beehiiv Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/brave-search/README]] — Brave Search Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/cal-com/README]] — Cal.com Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/chargebee/README]] — Chargebee Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/dropbox-business/README]] — Dropbox Business Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/dropbox/README]] — Dropbox Routing Reference

<!-- AI-LINKS-END -->
