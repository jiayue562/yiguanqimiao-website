# Grafana Routing Reference

**App name:** `grafana`
**Base URL proxied:** User's Grafana instance

## API Path Pattern

```
/grafana/api/{resource}
```

## Organization & User

### Get Current Organization
```bash
GET /grafana/api/org
```

### Get Current User
```bash
GET /grafana/api/user
```

## Dashboards

### Search Dashboards
```bash
GET /grafana/api/search?type=dash-db
```

Query params: `type`, `query`, `tag`, `folderIds`, `limit`

### Get Dashboard by UID
```bash
GET /grafana/api/dashboards/uid/{uid}
```

### Create/Update Dashboard
```bash
POST /grafana/api/dashboards/db
Content-Type: application/json

{
  "dashboard": {
    "title": "Dashboard Title",
    "panels": [],
    "schemaVersion": 30
  },
  "overwrite": false
}
```

### Delete Dashboard
```bash
DELETE /grafana/api/dashboards/uid/{uid}
```

## Folders

### List Folders
```bash
GET /grafana/api/folders
```

### Get Folder
```bash
GET /grafana/api/folders/{uid}
```

### Create Folder
```bash
POST /grafana/api/folders
Content-Type: application/json

{"title": "Folder Name"}
```

### Delete Folder
```bash
DELETE /grafana/api/folders/{uid}
```

## Data Sources

### List Data Sources
```bash
GET /grafana/api/datasources
```

### Get Data Source
```bash
GET /grafana/api/datasources/{id}
GET /grafana/api/datasources/uid/{uid}
GET /grafana/api/datasources/name/{name}
```

### Create Data Source
```bash
POST /grafana/api/datasources
Content-Type: application/json

{
  "name": "Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy"
}
```

### Delete Data Source
```bash
DELETE /grafana/api/datasources/{id}
```

## Annotations

### List Annotations
```bash
GET /grafana/api/annotations
```

Query params: `from`, `to`, `dashboardUID`, `tags`, `limit`

### Create Annotation
```bash
POST /grafana/api/annotations
Content-Type: application/json

{
  "dashboardUID": "abc123",
  "time": 1609459200000,
  "text": "Annotation text",
  "tags": ["tag1"]
}
```

### Delete Annotation
```bash
DELETE /grafana/api/annotations/{id}
```

## Teams

### Search Teams
```bash
GET /grafana/api/teams/search
```

### Create Team
```bash
POST /grafana/api/teams
Content-Type: application/json

{"name": "Team Name"}
```

## Alert Rules

### List Alert Rules
```bash
GET /grafana/api/v1/provisioning/alert-rules
GET /grafana/api/ruler/grafana/api/v1/rules
```

## Other Endpoints

### Service Accounts
```bash
GET /grafana/api/serviceaccounts/search
```

### Plugins
```bash
GET /grafana/api/plugins
```

## Notes

- Dashboard UIDs are unique identifiers
- Annotations use epoch timestamps in milliseconds
- Admin operations may require elevated permissions
- Alert rules use provisioning API (`/api/v1/provisioning/...`)

## Resources

- [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/box/README]] — Box Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/calendly/README]] — Calendly Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/dropbox/README]] — Dropbox Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/eventbrite/README]] — Eventbrite Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/getresponse/README]] — GetResponse Routing Reference

<!-- AI-LINKS-END -->
