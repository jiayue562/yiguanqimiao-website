---
name: education
parent_skill: ai-os
description: "Generate study plans, quizzes, flashcards, review materials, track learning progress and schedule study sessions. Use when users ask to create study plans, generate quiz questions, make flashcards, track study progress, or schedule review sessions for any topic."
description_zh: "学习助手：生成学习计划、测验、抽认卡、复习材料并跟踪进度"
description_en: "Study assistant: generate plans, quizzes, flashcards, review materials and track progress"
version: 3.4.1
homepage: https://clawhub.ai/skills/education
allowed-tools: Read,Write,Bash
---

# EDUCATION SKILL

Generate study plans, quizzes, flashcards, and review materials for any topic. Track progress and schedule sessions.

## COMMANDS

### 1. PLAN
Generate a structured study plan for a topic.
```bash
bash scripts/script.sh plan <topic> [--weeks <num>] [--level beginner|intermediate|advanced] [--output json|text]
```

### 2. QUIZ
Generate quiz questions on a topic.
```bash
bash scripts/script.sh quiz <topic> [--count <num>] [--type mcq|truefalse|short] [--difficulty easy|medium|hard]
```

### 3. FLASHCARD
Generate flashcards for key concepts.
```bash
bash scripts/script.sh flashcard <topic> [--count <num>] [--format plain|csv|json]
```

### 4. PROGRESS
Track and display learning progress.
```bash
bash scripts/script.sh progress [--topic <topic>] [--mark <milestone>] [--reset]
```

### 5. SCHEDULE
Create a study schedule with time blocks.
```bash
bash scripts/script.sh schedule <topic> [--hours-per-day <num>] [--days <num>] [--start <date>]
```

### 6. REVIEW
Generate a review checklist based on completed topics.
```bash
bash scripts/script.sh review <topic> [--scope all|weak|recent] [--format checklist|summary]
```

## OUTPUT

All commands print to stdout. Use `--output json` for machine-readable output where supported. Progress data is stored in `~/.education/progress.json`.

## REQUIREMENTS

- bash 4+
- python3 (standard library only)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/resources_CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/resources_FAQ]] — Frequently Asked Questions
- [[09-技能库/resources_output-patterns]] — Output Patterns
- [[09-技能库/web-search-plus/CHANGELOG]] — Changelog - Web Search Plus
- [[09-技能库/web-search-plus/FAQ]] — Frequently Asked Questions
- [[ψ技能体系/30-tools/tutor-skills/SKILL]] — TUTOR SKILLS

<!-- AI-LINKS-END -->
