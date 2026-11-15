# Teams 收件箱与福帮手编排对齐（策略 B）

> **版本**：2.1.1  
> **状态**：约定稿；以宿主实际 JSON  schema 为准迭代。

---

## 1. 目的

当 WorkBuddy 在工作区使用 **`.workbuddy/teams/<teamId>/inboxes/*.json`** 时，福帮手多智能体（team-lead / reviewer / writer）的**任务状态**宜与收件箱字段对齐，避免「对话里并行、磁盘未同步」。

---

## 2. 建议字段映射（逻辑层）

| 福帮手概念 | 宿主 inbox 建议含义 |
|------------|---------------------|
| 当前阶段（S0–S6） | `metadata.stage` 或团队 config 扩展 |
| 待办质检类型（P/C/B） | `task.type` / `role` |
| 阻塞原因 | `status.blockedReason` |
| 书稿根 | 与 `workspacePath` / `bookRoot` 一致 |

---

## 3. 落地策略

1. **探测**：若存在 `.workbuddy/teams/**/inboxes/team-lead.json`，首响提示「检测到团队编排目录」。  
2. **写入**：仅由 **team-lead** 或明确授权脚本写入 inbox；子智能体优先落盘 `.fbs/` 再通知。  
3. **冲突**：以 `.fbs` 与 `workbuddy-resume.json` 为准；inbox 为协调层。

---

## 4. 相关

- [`multi-agent-horizontal-sync.md`](./multi-agent-horizontal-sync.md)  
- `intake-router` JSON 中 `firstResponseContext`（环境三元组）

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/information-ownership-and-arbitration]] — 信息产权、场景包坐标与记忆仲裁
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/qc-agent-briefing-template]] — 质检子智能体任务模板
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-full-spec]] — FBS-BookWriter 完整规范（skill-full-spec）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/ux-optimization-rules]] — UX 优化统一规则中心（v2.1.1）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/brand-outputs]] — 品牌输出规范与版权页参数
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-subtask-contract]] — 长任务 / 辅助子任务机读契约（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/host-qc-and-fbs-reports]] — 宿主侧质检脚本与 FBS 报告落盘约定
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/multi-agent-horizontal-sync]] — 多智能体横向协同（架构模式 · 磁盘协议）

<!-- AI-LINKS-END -->
