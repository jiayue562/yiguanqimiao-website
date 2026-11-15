# Todoist Routing Reference

**App name:** `todoist`
**Base URL proxied:** `api.todoist.com`

## API Path Pattern

```
/todoist/api/v1/{resource}
```

## Common Endpoints

### List Projects
```bash
GET /todoist/api/v1/projects
```

### Get Project
```bash
GET /todoist/api/v1/projects/{id}
```

### Create Project
```bash
POST /todoist/api/v1/projects
Content-Type: application/json

{
  "name": "My Project",
  "color": "blue"
}
```

### Update Project
```bash
POST /todoist/api/v1/projects/{id}
Content-Type: application/json

{
  "name": "Updated Name"
}
```

### Delete Project
```bash
DELETE /todoist/api/v1/projects/{id}
```

### List Tasks
```bash
GET /todoist/api/v1/tasks
GET /todoist/api/v1/tasks?project_id={project_id}
GET /todoist/api/v1/tasks?filter={filter}
```

### Get Task
```bash
GET /todoist/api/v1/tasks/{id}
```

### Create Task
```bash
POST /todoist/api/v1/tasks
Content-Type: application/json

{
  "content": "Buy groceries",
  "priority": 2,
  "due_string": "tomorrow"
}
```

### Update Task
```bash
POST /todoist/api/v1/tasks/{id}
Content-Type: application/json

{
  "content": "Updated content",
  "priority": 4
}
```

### Close Task (Complete)
```bash
POST /todoist/api/v1/tasks/{id}/close
```

### Reopen Task
```bash
POST /todoist/api/v1/tasks/{id}/reopen
```

### Delete Task
```bash
DELETE /todoist/api/v1/tasks/{id}
```

### List Sections
```bash
GET /todoist/api/v1/sections
GET /todoist/api/v1/sections?project_id={project_id}
```

### Create Section
```bash
POST /todoist/api/v1/sections
Content-Type: application/json

{
  "name": "In Progress",
  "project_id": "123456"
}
```

### Delete Section
```bash
DELETE /todoist/api/v1/sections/{id}
```

### List Labels
```bash
GET /todoist/api/v1/labels
```

### Create Label
```bash
POST /todoist/api/v1/labels
Content-Type: application/json

{
  "name": "urgent",
  "color": "red"
}
```

### Delete Label
```bash
DELETE /todoist/api/v1/labels/{id}
```

### List Comments
```bash
GET /todoist/api/v1/comments?task_id={task_id}
GET /todoist/api/v1/comments?project_id={project_id}
```

### Create Comment
```bash
POST /todoist/api/v1/comments
Content-Type: application/json

{
  "task_id": "123456",
  "content": "This is a comment"
}
```

### Delete Comment
```bash
DELETE /todoist/api/v1/comments/{id}
```

## Notes

- Task and Project IDs are strings
- Priority values: 1 (normal) to 4 (urgent)
- Use only one due date format per request: `due_string`, `due_date`, or `due_datetime`
- Comments require either `task_id` or `project_id`
- Close/reopen/delete operations return 204 No Content

## Resources

- [Todoist API v1 Documentation](https://developer.todoist.com/api/v1)
- [Todoist Filter Syntax](https://todoist.com/help/articles/introduction-to-filters)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/attio/README]] — Attio Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clockify/README]] — Clockify Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/coda/README]] — Coda Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/companycam/README]] — CompanyCam Routing Reference

<!-- AI-LINKS-END -->
