# 顾问报告场景包 · 本地规则补丁（local-rule）

> **体裁**：consultant · **版本**：2.1.1  
> **适用时机**：四级降级链 L3 阶段自动读取。  
> **与 consultant.md 的关系**：本文件补充**质量规则检查项**，不重复 consultant.md 已有的 S0 收集要素内容。

---

## L3 降级时的体裁感知规则（Q层叠加）

### 结论质量规则

| ID | 规则 | 违反信号 |
|----|------|---------|
| CON-C1 | 每个核心建议须包含：现状描述 → 问题定位 → 解决路径 → 预期收益 | 直接给结论无逻辑链 |
| CON-C2 | 数据引用须为近3年内数据（行业报告等），标注来源机构与年份 | "市场规模XXX亿"无来源 |
| CON-C3 | 定量建议（如"降本20%"）须有测算依据或假设条件说明 | 数字无依据 |
| CON-C4 | 风险章节须覆盖：执行风险、市场风险、时间风险三个维度 | 仅提一种风险类型 |

### 结构规则

| ID | 规则 | 违反信号 |
|----|------|---------|
| CON-S1 | 执行摘要须在前3页内，且独立可读（不依赖正文） | 无执行摘要或仅一句话 |
| CON-S2 | 每个建议须有优先级标注（P0/P1/P2 或 高/中/低） | 建议列表无优先级 |
| CON-S3 | 结论章节须与执行摘要保持一致（不出现新结论） | 正文有摘要未提及的建议 |

### 立场规则

| ID | 规则 | 违反信号 |
|----|------|---------|
| CON-L1 | 报告须声明立场约束（受委托方 / 独立第三方） | 无立场声明 |
| CON-L2 | 涉及竞争对手分析时须使用中性表述 | "A公司明显劣势于B公司"无依据 |

---

## L3 离线告知模板

```
【场景包降级通知】
当前场景包（consultant）已降级至 L3 本地规则模式。
可用能力：结论质量规则（CON-C1~C4）、结构规范（CON-S1~S3）、立场约束（CON-L1~L2）
不可用：云端行业数据模板、企业专属报告格式
顾问报告写作不受阻断，请手动补充数据来源与立场声明。
```

---

*v2.1.0 · E3 落地 · 2026-04-11*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[05-五行人格心理学/00-入口/📦 五行人格心理学-市场产值测算v1.0]] — 五行人格心理学·市场产值测算 v1.0
- [[05-五行人格心理学/00-入口/📦 五行人格心理学-市场定位与客户画像v1.0]] — 五行人格心理学·市场定位与客户画像 v1.0
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/temporal-accuracy-samples]] — 时效与年份规则：样例与例外（防误报）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/genealogy-local-rule]] — 家谱场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/general-local-rule]] — 通用写书场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/ghostwriter-local-rule]] — 代撰稿场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/personal-book-local-rule]] — 个人出书场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/report-local-rule]] — 调查报告场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/training-local-rule]] — 培训教材场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/whitepaper-local-rule]] — 行业白皮书场景包 · 本地规则补丁（local-rule）

<!-- AI-LINKS-END -->
