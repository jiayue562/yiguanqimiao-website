# 时效与年份规则：样例与例外（防误报）

> **权威配置**：`search-policy.json` → `temporalAccuracy` / `hardcodeYearDetection`  
> **目的**：训练校准「应拦截」与「应放行」，减少机械误触。

---

## 应拦截 / 须先检索或标注

| 样例 | 期望 |
|------|------|
| 正文写「截至 **2024** 年行业规模达 …」且无来源 | 拦截 → WebSearch 或标「（年份待核实）」 |
| 检索 query 写「AI 应用 **2025** 报告」作为固定后缀 | 按 policy 改用「最新」等相对时效词 |

---

## 应放行（例外须标注来源或上下文）

| 样例 | 期望 |
|------|------|
| 用户明确：「统计截止 **2023** 年底」 | 放行，禁止再包装为「当前」「最新」 |
| 历史叙述：「**2020** 年颁布某某条例」且有文献标题 | 放行 |
| S0 时间戳检索已写入 `s0TimestampBaseline` | 当日日期引用以该基准为准 |

---

## 季度表述

- 仅写「Q1」→ 须补「（1–3 月）」或标精度不足（见 policy `quarterForbiddenNote`）。

---

维护：与 `search-policy.json` 同版本迭代时复核本页样例。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/生生-文化操作系统/NS68C5D-10-参考文献-附录E]] — 附录E 参考文献
- [[05-五行人格心理学/00-入口/📦 五行人格心理学-市场定位与客户画像v1.0]] — 五行人格心理学·市场定位与客户画像 v1.0
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/expansion-fact-tagging]] — 扩写与精修中的事实标注（MAT / 待证实）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/multi-agent-horizontal-sync]] — 多智能体横向协同（架构模式 · 磁盘协议）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/web-search-reverse-verification]] — 联网检索：反向验证查询（模型 / 价格 / 版本）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/consultant-local-rule]] — 顾问报告场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/whitepaper-local-rule]] — 行业白皮书场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/scripts/agents/fbs-reviewer]] — FBS Reviewer Agent

<!-- AI-LINKS-END -->
