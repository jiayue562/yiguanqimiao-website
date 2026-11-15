# 发版与主包策略核对清单

> **版本**：2.1.2  
> **适用**：维护者打 `pack:workbuddy` / `pack:codebuddy` / `pack:release` 前自检。  
> **主包约定**：默认主包为 **WorkBuddy**（`npm run pack:release` 仅产出 WorkBuddy 包）。

---

## 0. CI 分层（PR vs 发版）

| 层级 | 命令 | 适用场景 |
|------|------|----------|
| **fast** | `npm run ci:fast`（`npm test` + `validate:runtime-hints` + `audit:consistency`） | PR、日常推送，分钟级反馈 |
| **release** | `npm run ci:release`（fast + `audit:all` + `manifest:scripts` + `gate:evolution`） | 发版标签、发布前全绿 |

---

## 1. 自动化门禁（须全绿）

| 命令 | 说明 |
|------|------|
| `npm test` | 全量 Vitest |
| `npm run test:contract` | 契约类快测（可选作本地首跑） |
| `npm run pack:skill-gates` | 版本三角、场景包、链接、manifest、`validate-runtime-hints`、ux-flow、consistency-audit、契约单测 |
| `npm run quality:audit:full` | `references/**/*.md` 机器可检项 |
| `npm run build:check` | 构建链自检 |
| `npm run audit:all:strict` | P0 八段严模式（与 CI `--strict` 对齐） |
| `npm run ci:release` | 发版前推荐一键（见 §0） |
| `node scripts/validate-runtime-hints.mjs --skill-root .` | 机读 hints 单独复验（已含于 pack:skill-gates） |

**合并全稿**：跨平台请使用 `node scripts/merge-chapters.mjs`（勿依赖 bash `$OUTPUT` 片段）。

---

## 2. 产物与文档

- [ ] `dist/` 仅保留**当前版本**（如 v2.1.2）主通道 zip、校验 JSON 与团队移交包；旧版与临时目录可执行 `npm run clean:dist`（删 `*-temp`、`test-unzip`）或 `npm run clean:dist:prune`（另删 `v210` 等历史 zip/报告）。
- [ ] 默认发版命令使用 `npm run pack:release`（仅 WorkBuddy 主包）；如需三通道，显式使用 `npm run pack:release:all`。
- [ ] `dist/` 下目标包与 `*.verification.json`（若流程生成）符合本次发布说明。
- [ ] `SKILL.md` / `package.json` / `_plugin_meta.json` / 双通道 `channel-manifest.json` 版本一致（由 `pack:skill-gates` 与 `consistency-audit` 覆盖）。
- [ ] 用户侧索引无断链（`references/01-core/skill-index.md`）。

---

## 3. 分发边界

- [ ] 企业侧-only 文档未误入用户 ZIP（见 `documentation-layers.md`）。
- [ ] WorkBuddy / CodeBuddy 各自 manifest 与插件元数据指向正确技能 ID。

---

## 4. 大变更时的增量建议

- 文档大面积改动：先 `npm run quality:audit:incremental`（缩小范围）。
- 检索/台账约定变更：确认 `fbs-runtime-hints.json` 与 `search-policy.json` 已同步，并跑 `validate-runtime-hints`。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/README-v2.1.2]] — FBS-BookWriter v2.1.2 审核版说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-cli-bridge-matrix]] — Skill ↔ 脚本 ↔ CLI 联动矩阵（非 MCP）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/writing-phase-alert-tiers]] — 写作阶段告警分级（Blocker / Warning / Info）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-continuous-improvement]] — 福帮手持续改进与进化门控（P0–P2 总览）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-source-of-truth-matrix]] — FBS-BookWriter 真源矩阵（发版与审计用）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-subtask-contract]] — 长任务 / 辅助子任务机读契约（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/html-deliverable-gate]] — HTML 交付档位（D1 / D2 / D3）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/lexicon-governance]] — 词表与质检规则演进治理（策略 C）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/platform-ops-brief]] — 平台运维简报（构建 · 交付 · 心跳）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/quality-gates-brief]] — 质量门禁辅助简报（主题锁 · VCR · 国标）

<!-- AI-LINKS-END -->
