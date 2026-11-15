# FBS-BookWriter 真源矩阵（发版与审计用）

> **用途**：避免 `SKILL.md`、`search-policy.json`、`scale-tiers.json`、脚本行为漂移；**发版前**对照本表。

| 真源 | 路径 | 维护规则 |
|------|------|----------|
| 认知资产与商业口径（愿景层） | `references/05-ops/cognitive-asset-threeization.md` + `fbs-runtime-hints.json` → `cognitiveAsset` | 叙事与机读块同步；首响 `cognitiveAssetSnapshot` 由 intake 从 hints 派生，不得手写分叉 |
| 技能包版本 | `package.json` → `version` | 与 `SKILL.md` frontmatter、`scripts/version.mjs`、`_plugin_meta.json` 一致 |
| 运行时提示 | `fbs-runtime-hints.json` → `version` | 与 `package.json.version` 一致（`validate-runtime-hints.mjs` 校验） |
| 联网策略版本 | `references/05-ops/search-policy.json` → `version` | 大改时 bump；`project-config.skillPolicyVersionNote` 可记摘要 |
| 规模档位 | `references/05-ops/scale-tiers.json` | `xl-project-init.mjs`、`SKILL` 规模表引用此处 |
| 门禁分级叙述 | `references/02-quality/writing-phase-alert-tiers.md` | 与 `fbs-runtime-hints.json` → `gates` 交叉引用 |
| 脚本清单 | `scripts/generated/scripts-manifest.json` | `npm run manifest:scripts`；`evolution-gate` 校验 |

**发版 Checklist（最小）**

1. `npm run manifest:scripts`  
2. `npm run validate:runtime-hints`  
3. `npm run audit:consistency`  
4. `npm test`

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/memory-layer-matrix]] — 记忆分层与写入矩阵（策略 A / B / C 总览）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/outline-freeze]] — 大纲冻结与变更单（防结构漂移）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-3-workflow.full]] — FBS-BookWriter 第 3 节（完整版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-cli-bridge-matrix]] — Skill ↔ 脚本 ↔ CLI 联动矩阵（非 MCP）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/quality-check]] — 去AI味审校体系与评分模型
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/writing-phase-alert-tiers]] — 写作阶段告警分级（Blocker / Warning / Info）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-continuous-improvement]] — 福帮手持续改进与进化门控（P0–P2 总览）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/html-deliverable-gate]] — HTML 交付档位（D1 / D2 / D3）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/large-scale-book-strategy]] — 大规模书稿应对策略（M1 / M2 / M3）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/lexicon-governance]] — 词表与质检规则演进治理（策略 C）

<!-- AI-LINKS-END -->
