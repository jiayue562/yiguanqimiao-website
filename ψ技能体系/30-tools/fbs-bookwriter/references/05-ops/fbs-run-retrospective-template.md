# FBS 运行复盘报告（模板）

> **用途**：宿主侧或人工复盘时横向对比多次运行；与技能包规范无关字段可删。

## 元信息

| 字段 | 填写 |
|------|------|
| 复盘区间 |  |
| 书稿目录 / bookRoot |  |
| 技能包版本 |  |
| 宿主 | WorkBuddy / CodeBuddy / 其他 |

## 一、执行摘要

- 用户目标（一句话）：
- 声称完成 vs 实际完成（是/否）：

## 二、量化真值（必填）

| 项 | 声称值 | **工具测量值**（命令） |
|----|--------|------------------------|
| ChXX 字符数 |  | `node scripts/expansion-word-verify.mjs --book-root … --file … --target-chars …` 或 `--from-plan` |
| 全书总字符 |  | 同上或宿主统计 |

> **规则**：「声称值」不得仅来自模型口述；须附脚本输出或等价 `fs` 长度。

## 三、并行与子智能体

| 项 | 填写 |
|----|------|
| 并行章节数 |  |
| Subagent 类型（如 code-explorer / writer） |  |
| 是否注入 book-context-brief + 术语表 |  |

## 四、问题与根因（条目化）

1. 
2. 

## 五、整改项是否已映射技能包

- [ ] 已对照 `references/01-core/s3-expansion-phase.md` / `search-policy.json` → `expansionS35`
- [ ] 已执行 `node scripts/retro-action-sync.mjs --book-root <本书根> [--enforce-p0]`，并确认 `.fbs/retro-unresolved.md` 已纳入本轮执行输入
- [ ] 开工前门禁已运行 `node scripts/run-p0-audits.mjs --skill-root <技能根> --book-root <本书根>`（默认含 `retro-action-sync --enforce-p0 --allow-missing-report`）

## 六、局限性

（截断、宿主 token、未复现分支等）

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/runtime-mandatory-contract]] — 运行时强制契约（主 Agent / 宿主对齐）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-expansion-phase]] — S3.5 内容扩写阶段（初稿后的迭代扩写）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-refinement-phase]] — S3.7 精修阶段（扩写后的润色与事实收口）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-authoritative-supplement]] — SKILL.md 权威补充（§0 平台约束 × §1 品牌约束 × §宿主集成指南）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s3-writing-guide]] — S3 节点 — 写稿规范与 Brief 模板
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/template-narrative-context]] — 叙述 CONTEXT 冻结（模板）
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/workbuddy-integration-checklist]] — WorkBuddy 审核 / 集成检查清单（FBS-BookWriter v2.1.2）
- [[ψ技能体系/30-tools/fbs-bookwriter/scripts/_deprecated/README]] — scripts/_deprecated — 废弃脚本归档目录
- [[ψ技能体系/30-tools/knowledge-framework-builder/references/input-schema]] — input-schema.md —— 知识框架梳理 Skill 输入数据契约

<!-- AI-LINKS-END -->
