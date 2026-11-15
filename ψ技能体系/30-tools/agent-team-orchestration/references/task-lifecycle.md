# Task Lifecycle

Task states, transitions, comment conventions, and decision logging.

## States

```
Inbox → Assigned → In Progress → Review → Done | Failed
```

| State | Meaning | Owner |
|-------|---------|-------|
| **Inbox** | New task, unassigned | Orchestrator |
| **Assigned** | Agent selected, not yet started | Orchestrator |
| **In Progress** | Agent actively working | Assigned agent |
| **Review** | Work complete, awaiting verification | Reviewer |
| **Done** | Verified and shipped | Orchestrator |
| **Failed** | Abandoned with documented reason | Orchestrator |

## Transition Rules

**Orchestrator transitions:**
- Inbox → Assigned (picks the agent)
- Assigned → In Progress (spawns the agent or sends the task)
- Review → Done (accepts the deliverable)
- Any state → Failed (with reason)

**Agents transition:**
- In Progress → Review (submits deliverable with handoff comment)

**Reviewers transition:**
- Review → In Progress (returns with feedback — agent must address it)
- Review → Done (approves — orchestrator confirms)

**Never skip Review.** The orchestrator may override for trivial tasks, but document it.

## Comment Conventions

Every state change gets a comment. Format:

```
[Agent] [Action]: [Details]
```

### Required comments:

**Starting work:**
```
[Builder] Starting: Picking up auth module. Questions: Should rate limiting be per-user or per-IP?
```

**Blocker found:**
```
[Builder] Blocked: Need API credentials for the payment gateway. Who has access?
```

**Submitting for review:**
```
[Builder] Handoff: Auth module complete at /shared/artifacts/auth/.
- Added JWT validation middleware
- Tests at /shared/artifacts/auth/tests/
- Run `npm test -- --grep auth` to verify
- Known issue: refresh token rotation not implemented (out of scope per spec)
- Next: Reviewer checks error handling paths
```

**Review feedback:**
```
[Reviewer] Feedback: Two issues found.
1. Missing input validation on email field — SQL injection risk
2. Error messages expose internal paths in production mode
Returning to builder. Fix both, then resubmit.
```

**Completion:**
```
[Reviewer] Approved: All issues addressed. Auth module ready to ship.
```

**Failure:**
```
[Orchestrator] Failed: Deprioritized — superseded by new auth provider integration. Preserving spec at /shared/specs/auth-v1.md for reference.
```

## Decision Logging

Architecture or product decisions made during task execution go in a shared decisions directory.

```markdown
# Decision: [Title]
**Date:** YYYY-MM-DD
**Author:** [Agent]
**Status:** Proposed | Accepted | Rejected
**Task:** [Task ID if applicable]

## Context
Why this decision came up.

## Options Considered
1. Option A — tradeoffs
2. Option B — tradeoffs

## Decision
What was chosen and why.

## Consequences
What changes as a result.
```

**When to log a decision:**
- Choosing between two valid architectural approaches
- Changing a spec during implementation
- Rejecting a requirement as infeasible
- Any choice that future agents will wonder "why did we do it this way?"

## Multi-Step Task Workflows

Complex tasks split into sub-tasks. Track the parent relationship:

```
Task #12: Build user dashboard
  ├── #12a: Write spec (Assigned: Spec writer)
  ├── #12b: Review spec (Assigned: Builder — feasibility check)
  ├── #12c: Build frontend (Assigned: Builder)
  ├── #12d: Build API endpoints (Assigned: Builder)
  └── #12e: Integration test (Assigned: Reviewer)
```

The orchestrator tracks the parent task and only marks it Done when all sub-tasks complete.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Harness-Engineering/references/orchestration-layer]] — Harness Engineering - Orchestration Layer
- [[09-技能库/ghost-scan-secrets/agents/summarize/agent]] — Summarize Agent
- [[09-技能库/resources_agent]] — Summarize Agent
- [[09-技能库/self-improving/boundaries]] — Security Boundaries
- [[CONVENTIONS]] — Writing & Agent Conventions
- [[ψ技能体系/10-kernel/龙心OS/self-improving/boundaries]] — Security Boundaries
- [[ψ技能体系/30-tools/agent-team-orchestration/references/communication]] — Communication
- [[ψ技能体系/30-tools/agent-team-orchestration/references/patterns]] — Patterns

<!-- AI-LINKS-END -->
