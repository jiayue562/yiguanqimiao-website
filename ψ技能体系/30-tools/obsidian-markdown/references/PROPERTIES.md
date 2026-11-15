# Properties (Frontmatter) Reference

Properties use YAML frontmatter at the start of a note:

```yaml
---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
aliases:
  - My Note
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 4.5
completed: false
due: 2024-02-01T14:30:00
---
```

## Property Types

| Type | Example |
|------|---------|
| Text | `title: My Title` |
| Number | `rating: 4.5` |
| Checkbox | `completed: true` |
| Date | `date: 2024-01-15` |
| Date & Time | `due: 2024-01-15T14:30:00` |
| List | `tags: [one, two]` or YAML list |
| Links | `related: "[[Other Note]]"` |

## Default Properties

- `tags` - Note tags (searchable, shown in graph view)
- `aliases` - Alternative names for the note (used in link suggestions)
- `cssclasses` - CSS classes applied to the note in reading/editing view

## Tags

```markdown
#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
```

Tags can contain: letters (any language), numbers (not first character), underscores `_`, hyphens `-`, forward slashes `/` (for nesting).

In frontmatter:

```yaml
---
tags:
  - tag1
  - nested/tag2
---
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[16-工具与资源/templates_resource]] — {{TITLE}}
- [[09-技能库/Skill安全扫描（朱雀实验室）/SKILL]] — Tencent Zhuque Skill Scanner
- [[09-技能库/ghost-scan-code/SKILL]] — Find Issues
- [[09-技能库/ghost-scan-deps/agents/analyze/analyzer]] — Analyzer Agent
- [[09-技能库/obsidian/SKILL]] — Obsidian
- [[CONVENTIONS]] — Writing & Agent Conventions
- [[ψ技能体系/30-tools/obsidian-markdown/SKILL]] — Obsidian Flavored Markdown Skill
- [[ψ技能体系/30-tools/obsidian-markdown/references/CALLOUTS]] — Callouts Reference

<!-- AI-LINKS-END -->
