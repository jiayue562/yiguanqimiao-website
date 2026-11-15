# Memory Template

Copy this structure to `~/self-improving/memory.md` on first use.

```markdown
# Self-Improving Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

## Recent (last 7 days)
<!-- New corrections pending confirmation -->
```

## Initial Directory Structure

Create on first activation:

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
touch ~/self-improving/{memory.md,index.md,corrections.md,heartbeat-state.md}
```

## Index Template

For `~/self-improving/index.md`:

```markdown
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last compaction: never
```

## Corrections Log Template

For `~/self-improving/corrections.md`:

```markdown
# Corrections Log

<!-- Format:
## YYYY-MM-DD
- [HH:MM] Changed X → Y
  Type: format|technical|communication|project
  Context: where correction happened
  Confirmed: pending (N/3) | yes | no
-->
```

## Heartbeat State Template

For `~/self-improving/heartbeat-state.md`:

```markdown
# Self-Improving Heartbeat State

last_heartbeat_started_at: never
last_reviewed_change_at: never
last_heartbeat_result: never

## Last actions
- none yet
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/self-improving/heartbeat-rules]] — Heartbeat Rules
- [[09-技能库/self-improving/heartbeat-state]] — Heartbeat State Template
- [[09-技能库/self-improving/setup]] — Setup — Self-Improving Agent
- [[ψ技能体系/10-kernel/龙心OS/self-improving/heartbeat-rules]] — Heartbeat Rules
- [[ψ技能体系/10-kernel/龙心OS/self-improving/memory-template]] — Memory Template
- [[ψ技能体系/10-kernel/龙心OS/self-improving/setup]] — Setup — Self-Improving Agent

<!-- AI-LINKS-END -->
