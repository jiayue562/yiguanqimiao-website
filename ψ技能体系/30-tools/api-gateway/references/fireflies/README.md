# Fireflies Routing Reference

**App name:** `fireflies`
**Base URL proxied:** `api.fireflies.ai`

## API Path Pattern

```
/fireflies/graphql
```

Fireflies uses GraphQL. All requests are POST to a single `/graphql` endpoint.

## GraphQL Queries

### User
```graphql
{ user { user_id name email is_admin } }
```

### Users
```graphql
{ users { user_id name email is_admin } }
```

### Transcripts
```graphql
{ transcripts { id title date duration host_email privacy } }
```

### Transcript by ID
```graphql
query($id: String!) {
  transcript(id: $id) {
    id title date duration
    summary { overview action_items }
    sentences { text speaker_name }
  }
}
```

### Channels
```graphql
{ channels { id title created_at is_private } }
```

### Contacts
```graphql
{ contacts { email name picture last_meeting_date } }
```

### Bites
```graphql
{ bites { id name transcript_id summary status } }
```

### AskFred Threads
```graphql
{ askfred_threads { id title created_at } }
```

## GraphQL Mutations

### Upload Audio
```graphql
mutation($input: AudioUploadInput!) {
  uploadAudio(input: $input) { success message }
}
```

### Delete Transcript
```graphql
mutation($id: String!) {
  deleteTranscript(id: $id) { success }
}
```

### Update Meeting Title
```graphql
mutation($id: String!, $title: String!) {
  updateMeetingTitle(id: $id, title: $title) { success }
}
```

### AskFred
```graphql
mutation($input: CreateAskFredThreadInput!) {
  createAskFredThread(input: $input) { id title }
}
```

## Notes

- All requests are POST with Content-Type: application/json
- Request body: `{ "query": "...", "variables": {...} }`
- User IDs are ULIDs
- Rate limits: 50 calls/day (free), more on Business plan
- Summary field contains AI-generated content

## Resources

- [Fireflies API Documentation](https://docs.fireflies.ai/)
- [Fireflies GraphQL API](https://docs.fireflies.ai/graphql-api)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/baserow/README]] — Baserow Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/box/README]] — Box Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/buffer/README]] — Buffer Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clicksend/README]] — ClickSend Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/fathom/README]] — Fathom Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/granola-mcp/README]] — Granola MCP Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/linear/README]] — Linear Routing Reference

<!-- AI-LINKS-END -->
