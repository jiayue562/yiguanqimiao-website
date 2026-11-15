# Sentry Routing Reference

**App name:** `sentry`
**Base URL proxied:** `{subdomain}.sentry.io`

## API Path Pattern

```
/sentry/api/0/{resource}
```

Sentry API uses version `0` prefix in all paths.

## Common Endpoints

### List Organizations
```bash
GET /sentry/api/0/organizations/
```

### Retrieve Organization
```bash
GET /sentry/api/0/organizations/{organization_slug}/
```

### List Organization Projects
```bash
GET /sentry/api/0/organizations/{organization_slug}/projects/
```

### List Organization Members
```bash
GET /sentry/api/0/organizations/{organization_slug}/members/
```

### Retrieve Project
```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/
```

### List Project Issues
```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/issues/
```

Query parameters:
- `statsPeriod` - Stats period: `24h`, `14d`, or empty
- `query` - Sentry search query (default: `is:unresolved`)
- `cursor` - Pagination cursor

### List Organization Issues
```bash
GET /sentry/api/0/organizations/{organization_slug}/issues/
```

### Retrieve Issue
```bash
GET /sentry/api/0/issues/{issue_id}/
```

### Update Issue
```bash
PUT /sentry/api/0/issues/{issue_id}/
Content-Type: application/json

{
  "status": "resolved"
}
```

Status values: `resolved`, `unresolved`, `ignored`

### Delete Issue
```bash
DELETE /sentry/api/0/issues/{issue_id}/
```

### List Issue Events
```bash
GET /sentry/api/0/issues/{issue_id}/events/
```

### List Project Events
```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/events/
```

### List Organization Teams
```bash
GET /sentry/api/0/organizations/{organization_slug}/teams/
```

### Create Team
```bash
POST /sentry/api/0/organizations/{organization_slug}/teams/
Content-Type: application/json

{
  "name": "New Team",
  "slug": "new-team"
}
```

### Retrieve Team
```bash
GET /sentry/api/0/teams/{organization_slug}/{team_slug}/
```

### List Organization Releases
```bash
GET /sentry/api/0/organizations/{organization_slug}/releases/
```

### Create Release
```bash
POST /sentry/api/0/organizations/{organization_slug}/releases/
Content-Type: application/json

{
  "version": "1.0.0",
  "projects": ["project-slug"]
}
```

### Retrieve Release
```bash
GET /sentry/api/0/organizations/{organization_slug}/releases/{version}/
```

### Create Deploy
```bash
POST /sentry/api/0/organizations/{organization_slug}/releases/{version}/deploys/
Content-Type: application/json

{
  "environment": "production"
}
```

## Notes

- Organization and project identifiers use slugs (lowercase, hyphenated)
- Issue IDs are numeric
- Release versions can contain special characters (URL encode as needed)
- Uses cursor-based pagination via Link header
- Most endpoints require OAuth scopes like `event:read`, `project:read`, `org:read`

## Resources

- [Sentry API Documentation](https://docs.sentry.io/api/)
- [Events API](https://docs.sentry.io/api/events/)
- [Projects API](https://docs.sentry.io/api/projects/)
- [Organizations API](https://docs.sentry.io/api/organizations/)
- [Teams API](https://docs.sentry.io/api/teams/)
- [Releases API](https://docs.sentry.io/api/releases/)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/apollo/README]] — Apollo Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/attio/README]] — Attio Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/baserow/README]] — Baserow Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/callrail/README]] — CallRail Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clockify/README]] — Clockify Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/eventbrite/README]] — Eventbrite Routing Reference

<!-- AI-LINKS-END -->
