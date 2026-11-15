# Unbounce Routing Reference

**App name:** `unbounce`
**Base URL proxied:** `api.unbounce.com`

## API Path Pattern

```
/unbounce/accounts
/unbounce/accounts/{account_id}
/unbounce/accounts/{account_id}/sub_accounts
/unbounce/accounts/{account_id}/pages
/unbounce/sub_accounts/{sub_account_id}
/unbounce/sub_accounts/{sub_account_id}/pages
/unbounce/sub_accounts/{sub_account_id}/domains
/unbounce/sub_accounts/{sub_account_id}/page_groups
/unbounce/pages
/unbounce/pages/{page_id}
/unbounce/pages/{page_id}/form_fields
/unbounce/pages/{page_id}/leads
/unbounce/leads/{lead_id}
/unbounce/domains/{domain_id}
/unbounce/domains/{domain_id}/pages
/unbounce/page_groups/{page_group_id}/pages
/unbounce/users/self
/unbounce/users/{user_id}
```

## Common Endpoints

### List Accounts
```bash
GET /unbounce/accounts
```

### Get Account
```bash
GET /unbounce/accounts/{account_id}
```

### List Sub-Accounts
```bash
GET /unbounce/accounts/{account_id}/sub_accounts
```

### Get Sub-Account
```bash
GET /unbounce/sub_accounts/{sub_account_id}
```

### List Pages
```bash
GET /unbounce/pages
```

### Get Page
```bash
GET /unbounce/pages/{page_id}
```

### List Page Form Fields
```bash
GET /unbounce/pages/{page_id}/form_fields
```

### List Page Leads
```bash
GET /unbounce/pages/{page_id}/leads
```

### Get Lead
```bash
GET /unbounce/leads/{lead_id}
```

### List Domains
```bash
GET /unbounce/sub_accounts/{sub_account_id}/domains
```

### Get Domain
```bash
GET /unbounce/domains/{domain_id}
```

### List Page Groups
```bash
GET /unbounce/sub_accounts/{sub_account_id}/page_groups
```

### List Page Group Pages
```bash
GET /unbounce/page_groups/{page_group_id}/pages
```

### Create Lead
```bash
POST /unbounce/pages/{page_id}/leads
Content-Type: application/json

{
  "conversion": true,
  "visitor_id": "unique-visitor-id",
  "form_submission": {
    "variant_id": "a",
    "submitter_ip": "127.0.0.1",
    "form_data": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### Get Current User
```bash
GET /unbounce/users/self
```

### Get User
```bash
GET /unbounce/users/{user_id}
```

## Query Parameters

- `limit` - Results per page (default: 50, max: 1000)
- `offset` - Skip first N results
- `sort_order` - `asc` or `desc`
- `from` - Start date (RFC 5322 format)
- `to` - End date (RFC 5322 format)
- `count` - When `true`, only return count in metadata
- `role` - Filter pages by role: `viewer` or `author`
- `with_stats` - Include A/B test statistics (for /pages)
- `include_sub_pages` - Include sub-page form fields (for /form_fields)

## Notes

- Page IDs are UUIDs, account/sub-account IDs are integers
- All responses include `metadata` with HATEOAS navigation links
- Page states: `published` or `unpublished`
- Account states: `active` or `suspended`
- Date format: RFC 5322 (e.g., `2026-03-04T10:54:34Z`)

## Resources

- [Unbounce API Documentation](https://developer.unbounce.com/api_reference/)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/acuity-scheduling/README]] — Acuity Scheduling Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/callrail/README]] — CallRail Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/coda/README]] — Coda Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/confluence/README]] — Confluence Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/facebook-page/README]] — Facebook Page Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/getresponse/README]] — GetResponse Routing Reference

<!-- AI-LINKS-END -->
