# Tier1 本地市场技能常见问题（WorkBuddy）

> **版本**：2.1.1  

## `workbuddy/channel-manifest.json` 里的 `preferredSkills` 与源码树不一致？

**正常现象。** 清单列出的是「建议从 `~/.workbuddy/skills-marketplace/skills/` 安装」的技能 id；**源码仓库**可能只 **部分** 拷贝到 `.codebuddy/skills/` 用于开发/打包演示。部分技能（如 `humanizer`、`pptx-generator`）**仅随市场安装**，不要求出现在仓库目录中。

## `minimax-xlsx` 在仓库里有，为何不在 `preferredSkills`？

**刻意设计。** WorkBuddy 本地市场 **不将 minimax-xlsx 作为 Tier1 依赖**；Excel 统一走 **Tier2 `xlsx` 插件**（见 `provider-registry.yml` 的 `xlsx-data`）。仓库中的 `minimax-xlsx` 为可选增强包，探测逻辑以 `host-capability` 为准。

## 用户看到「只装了 3/17 个技能」是否正常？

**正常。** `intake-router` / `host-capability` 会给出 `tier1.marketplaceSummary`（已探测/总数）。未全部安装时按 **provider 降级链路** 执行，并在文案中提示「未装全为正常」。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/docs/history/SMART-MEMORY-ARCHITECTURE-v2.0.2]] — 智能记忆架构说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/brand-platform-convention]] — 品牌与平台规范（FBS × 福帮手 × 双通道宿主）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/ux-agent-playbook]] — Agent 用户体验执行清单（速查）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/workbuddy-delivery-tier2]] — WorkBuddy 交付链与 Tier2 插件（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/plugin-bus-spec]] — Plugin Bus 协议规范 v3.0
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/workbuddy-host-integration]] — WorkBuddy 宿主集成说明（最小契约）

<!-- AI-LINKS-END -->
