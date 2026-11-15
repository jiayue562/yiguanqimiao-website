# 读者验收清单（模板）

> **用途**：**机检通过后**、**S4/S5 前**，由 **作者或主编** 做「像不像一本书 / 能不能交付」的人工验收。  
> **原则**：能由脚本完成的（字数、A 类词、链接、待核实）**不在此重复**；此处只列 **人判项**。  
> **建议路径**：本书根 `.fbs/reader-uat.md`（按需从模板复制）。

---

## 验收对象

- **书稿范围**：（例如：全书 / 第 2 批扩写 / 单章）
- **验收日期**：
- **验收人**：

---

## A. 叙事与结构

- [ ] 开篇是否 **3 秒内** 让读者知道「为谁写、解决什么」
- [ ] 章与章之间 **无重复论证**（论点不循环打转）
- [ ] 小结与下章 **有承上启下**（非孤立堆叠）

---

## B. 可信度与风格

- [ ] 数据、引语、案例是否有 **出处或 MAT**（与 `pending-verification` 一致）
- [ ] 术语与 `术语锁定记录.md` **一致**（无同义混用）
- [ ] **「AI 腔」** 在可接受范围（可结合 `quality-AI-scan` 结果）

---

## C. 读者体验

- [ ] **目标读者** 阅读负担可接受（不过密专业术语、不过长段落）
- [ ] 敏感表述、品牌口径符合 **约定与合规**

---

## D. 结论

- [ ] **通过** — 可进入下一门禁（如 S4 合并或 S5）
- [ ] **不通过** — 记录问题清单（见下），并走 **修订熔断**（见 `fbs-narrative-gates-and-parity.md` §5），**禁止**无清单无限改稿

### 问题清单（不通过时必填）

| 位置 | 现象 | 建议动作（回退大纲 / 补素材 / 局部改稿） |
|------|------|------------------------------------------|
| | | |

---

## 与「checkpoint:human-verify」对齐

本清单对应 **必须由人判** 的验收点；机器项以 `quality-auditor`、`expansion-gate`、`chapter-status` 等为准。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/生生-文化操作系统/NS68C5D-13-总审核报告-20260827]] — 《生生：文化操作系统》交付前总审核报告
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/expansion-fact-tagging]] — 扩写与精修中的事实标注（MAT / 待证实）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/s3-refinement-phase]] — S3.7 精修阶段（扩写后的润色与事实收口）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/02-quality/genre-completion-checklist]] — 体裁化完成度清单（Warning 级）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-narrative-gates-and-parity]] — 叙事门控与外部工作流对标（福帮手 × 工程化协作范式）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/template-narrative-context]] — 叙述 CONTEXT 冻结（模板）
- [[ψ技能体系/30-tools/fbs-bookwriter/releases/codebuddy-review-v2.1.1]] — CodeBuddy 插件包说明（v2.1.1）

<!-- AI-LINKS-END -->
