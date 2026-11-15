# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[16-工具与资源/templates_idea]] — {{TITLE}}
- [[09-技能库/automation-workflows/SKILL]] — Automation Workflows
- [[09-技能库/skill-creator/references/workflows]] — Workflow Patterns
- [[09-技能库/技能创建指南/references/workflows]] — Workflow Patterns
- [[ψ技能体系/30-tools/mcp-builder/SKILL]] — MCP Server Development Guide
- [[ψ技能体系/30-tools/skill-creator/references/workflows]] — Workflow Patterns
- [[ψ技能体系/30-tools/提示词工程专家/CLAUDE]] — Prompt Engineering Expert Skill

<!-- AI-LINKS-END -->
