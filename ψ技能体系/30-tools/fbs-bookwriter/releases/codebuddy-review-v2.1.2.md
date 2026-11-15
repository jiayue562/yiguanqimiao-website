# CodeBuddy 插件包说明（v2.1.2）

- **版本**：`2.1.2`
- **状态**：入口状态机固化·意图单真源·IntentOps 门禁增强版
- **产物**：`dist/fbs-bookwriter-v212-codebuddy.zip`
- **校验报告**：`dist/fbs-bookwriter-v212-codebuddy.verification.json`
- **通道清单**：`codebuddy/channel-manifest.json`
- **插件元数据**：`.codebuddy-plugin/plugin.json`（plugin-id: fbs-bookwriter-v212）

## 本次核心变更（相对 v2.1.1）

- **[I1] canonical 真源落地**：新增意图单真源 `intent-canonical.json`。
- **[I2] NLU 决策升级**：支持 Top-K 候选、置信分带、冲突消歧与弱信号降级。
- **[I3] 槽位补全**：`bookRoot/stage/targetChapter/outputFormat/riskMode` 最小补全能力落地。
- **[I4] 入口状态机信号**：`intake-router` 统一输出 `entryStateMachine` 字段。
- **[I5] 治理可观测性增强**：新增 `intent-ops-report` 供周报和词典治理使用。

## 构建入口

- `npm run pack:codebuddy`（仅 CodeBuddy 包）
- `npm run pack:release`（同时构建 WorkBuddy + CodeBuddy + OpenClaw）

## 提交 / 自测建议

1. 运行 `npm run pack:codebuddy`
2. 核查 `dist/fbs-bookwriter-v212-codebuddy.verification.json`
3. 重点确认 `.codebuddy-plugin/plugin.json`、`codebuddy/channel-manifest.json`、`references/01-core/intent-canonical.json` 已进入 ZIP 且版本一致

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/README-v2.1.2]] — FBS-BookWriter v2.1.2 审核版说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/brand-platform-convention]] — 品牌与平台规范（FBS × 福帮手 × 双通道宿主）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/entry-state-machine-ops-onepager]] — 入口状态机（运营 1 页版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/entry-state-machine-tech-manual]] — 入口状态机（技术细则版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-final-draft-governance]] — 终稿状态机与版本治理（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-source-of-truth-matrix]] — FBS-BookWriter 真源矩阵（发版与审计用）
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/codebuddy-review-v2.1.1]] — CodeBuddy 插件包说明（v2.1.1）
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/workbuddy-review-v2.1.1]] — WorkBuddy 官方审核包说明（v2.1.1）
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/workbuddy-review-v2.1.2]] — WorkBuddy 官方审核包说明（v2.1.2）

<!-- AI-LINKS-END -->
