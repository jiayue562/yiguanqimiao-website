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

<!-- FUSION-LINK-BEGIN -->
## 🔗 同名版本对照（融合时生成）

> 本文件是副库/研学库版本；主库另有同名现行版本，**两版内容不同，均未覆盖**。
- 主库现行版本：[[09-技能库/skill-creator/references/workflows|主库现行版本]]

<!-- FUSION-LINK-END -->
