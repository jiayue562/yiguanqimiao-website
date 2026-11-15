# Zoho Bigin Routing Reference

**App name:** `zoho-bigin`
**Base URL proxied:** `www.zohoapis.com`

## API Path Pattern

```
/zoho-bigin/bigin/v2/{resource}
```

## Common Endpoints

### List Contacts
```bash
GET /zoho-bigin/bigin/v2/Contacts?fields=First_Name,Last_Name,Email
```

### Get Contact
```bash
GET /zoho-bigin/bigin/v2/Contacts/{id}
```

### Create Contact
```bash
POST /zoho-bigin/bigin/v2/Contacts
Content-Type: application/json

{
  "data": [{
    "Last_Name": "Smith",
    "First_Name": "John",
    "Email": "john@example.com"
  }]
}
```

### Update Contact
```bash
PUT /zoho-bigin/bigin/v2/Contacts
Content-Type: application/json

{
  "data": [{
    "id": "{record_id}",
    "Phone": "+1-555-1234"
  }]
}
```

### Delete Contact
```bash
DELETE /zoho-bigin/bigin/v2/Contacts?ids={id1},{id2}
```

### Search Contacts
```bash
GET /zoho-bigin/bigin/v2/Contacts/search?email=john@example.com
GET /zoho-bigin/bigin/v2/Contacts/search?criteria=(Last_Name:equals:Smith)
```

### List Companies (Accounts)
```bash
GET /zoho-bigin/bigin/v2/Accounts?fields=Account_Name,Website
```

### Get Users
```bash
GET /zoho-bigin/bigin/v2/users?type=ActiveUsers
```

### Get Modules
```bash
GET /zoho-bigin/bigin/v2/settings/modules
```

## Available Modules

| Module | API Name | Description |
|--------|----------|-------------|
| Contacts | `Contacts` | Individual people |
| Companies | `Accounts` | Organizations/businesses |
| Pipelines | `Pipelines` | Sales opportunities/deals |
| Products | `Products` | Items you sell |
| Tasks | `Tasks` | To-do items |
| Events | `Events` | Calendar appointments |
| Calls | `Calls` | Phone call logs |
| Notes | `Notes` | Notes attached to records |

## Notes

- The `fields` query parameter is **required** for list operations
- Module API names are case-sensitive (e.g., `Contacts`, not `contacts`)
- Companies are accessed via the `Accounts` module
- Sales opportunities are in the `Pipelines` module (not `Deals`)
- Record IDs are numeric strings (e.g., `7255024000000596045`)
- Maximum 200 records per page, 100 per create/update/delete
- Some modules (Tasks, Events, Calls, Notes) require additional OAuth scopes

## Resources

- [Bigin API Overview](https://www.bigin.com/developer/docs/apis/v2/)
- [Bigin REST API Documentation](https://www.bigin.com/developer/docs/apis/)
- [Modules API](https://www.bigin.com/developer/docs/apis/modules-api.html)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/apollo/README]] — Apollo Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/callrail/README]] — CallRail Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clickfunnels/README]] — ClickFunnels Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/cognito-forms/README]] — Cognito Forms Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/eventbrite/README]] — Eventbrite Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/getresponse/README]] — GetResponse Routing Reference

<!-- AI-LINKS-END -->
