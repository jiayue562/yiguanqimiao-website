# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/agent-memory-systems/SKILL]] — Agent Memory Systems
- [[09-技能库/humanizer/SKILL]] — Humanizer: Remove AI Writing Patterns
- [[09-技能库/resources_output-patterns]] — Output Patterns
- [[09-技能库/resources_pattern-template]] — Pattern Template
- [[09-技能库/self-improving-agent/templates/pattern-template]] — Pattern Template
- [[09-技能库/skill-creator/references/output-patterns]] — Output Patterns
- [[ψ技能体系/10-kernel/龙心OS/self-improving-agent/templates/pattern-template]] — Pattern Template
- [[ψ技能体系/10-kernel/龙心OS/self-learning/references/skill_creation_guide]] — Skill Creator Guide
- [[ψ技能体系/30-tools/skill-creator/references/output-patterns]] — Output Patterns

<!-- AI-LINKS-END -->
