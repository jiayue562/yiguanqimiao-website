# Buffer Routing Reference

**App name:** `buffer`
**Service API host:** `api.buffer.com`

## API Path Pattern

```
/buffer/
```

Buffer uses GraphQL - all requests are POST to the base endpoint (no `/graphql` path needed).

## Queries

### Account
```graphql
query {
    account {
        id
        email
        name
        avatar
        timezone
        organizations { id name }
    }
}
```

### Channels
```graphql
query GetChannels($organizationId: OrganizationId!) {
    channels(organizationId: $organizationId) {
        id
        name
        service
        displayName
        avatar
        isDisconnected
    }
}
```

### Single Channel
```graphql
query GetChannel($channelId: ChannelId!) {
    channel(channelId: $channelId) {
        id
        name
        service
        postingSchedule { days times }
    }
}
```

### Posts
```graphql
query GetPosts($channelId: ChannelId!, $status: PostStatus, $first: Int) {
    posts(channelId: $channelId, status: $status, first: $first) {
        edges {
            node { id text status dueAt }
        }
        pageInfo { hasNextPage endCursor }
    }
}
```

### Single Post
```graphql
query GetPost($postId: PostId!) {
    post(id: $postId) {
        id
        text
        status
        dueAt
        channel { id name service }
    }
}
```

## Mutations

### Create Post
```graphql
mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
        ... on Post { id text status dueAt }
        ... on InvalidInputError { message }
    }
}
```

**Input:**
- `channelId` (required): Target channel
- `text`: Post content
- `schedulingType` (required): "scheduled", "draft", "now"
- `dueAt`: ISO 8601 datetime
- `mode` (required): "queue" or "share"

### Create Idea
```graphql
mutation CreateIdea($input: CreateIdeaInput!) {
    createIdea(input: $input) {
        ... on Idea { id title text }
        ... on InvalidInputError { message }
    }
}
```

## Platform Metadata

Each platform supports specific metadata in `CreatePostInput.metadata`:

| Platform | Key Fields |
|----------|------------|
| Instagram | type, firstComment, shouldShareToFeed, geolocation |
| Facebook | type, linkAttachment, firstComment, annotations |
| LinkedIn | linkAttachment, firstComment, annotations |
| Twitter | thread, retweet |
| Pinterest | title, url, boardServiceId |
| YouTube | title, privacy, categoryId, notifySubscribers, madeForKids |
| TikTok | title |
| Google Business | type, title, detailsOffer, detailsEvent |
| Mastodon | thread, spoilerText |
| Threads | type, thread, linkAttachment, topic |
| Bluesky | thread, linkAttachment |

## Key Types

**Account**: id, email, name, avatar, timezone, organizations, preferences, connectedApps

**Organization**: id, name, ownerEmail, channelCount, channels, members, limits

**Channel**: id, name, service, displayName, avatar, timezone, isDisconnected, isQueuePaused, postingSchedule, postingGoal, weeklyPostingLimit, allowedActions

**Post**: id, text, status, schedulingType, dueAt, sentAt, author, channel, assets, tags, notes, metadata, error

**Idea**: id, organizationId, content, groupId, position

## Supported Services

- Instagram, Facebook, Twitter/X, LinkedIn
- Pinterest, TikTok, YouTube, Google Business
- Mastodon, Threads, Bluesky, StartPage

## Post Status Values

- `draft` - Saved as draft
- `scheduled` - Scheduled for publishing
- `sent` - Published
- `failed` - Failed to publish

## Pagination

Cursor-based pagination with `first`, `after`, and `pageInfo`.

## Review Requirements

- **Default to draft mode.** Use `schedulingType: "draft"` unless the user explicitly requests a scheduled or immediate release.
- **Confirm channel and content.** Before any mutation, show the target channel name/service, post text, timing choice, and relevant metadata for user review.
- **Use read checks first.** Retrieve the account, channel, and existing post details before changing Buffer content.
- **Small scoped changes only.** Handle one channel/post set at a time unless the user confirms a broader batch.

## Notes

- All requests are POST with JSON body
- Use `query` field for queries, include `variables` for parameters
- Scheduling requires ISO 8601 datetime strings
- Uses API key authentication

## Resources

- [Buffer API Documentation](https://developers.buffer.com/reference.html)
- [Buffer Getting Started](https://developers.buffer.com/guides/getting-started.html)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ima-skill/SKILL]] — ima-skill
- [[09-技能库/ima-skills/ima-skill/SKILL]] — ima-skill
- [[09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/SKILL]] — ima-skill
- [[ψ技能体系/30-tools/api-gateway/references/dropbox/README]] — Dropbox Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/fireflies/README]] — Fireflies Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/jobber/README]] — Jobber Routing Reference

<!-- AI-LINKS-END -->
