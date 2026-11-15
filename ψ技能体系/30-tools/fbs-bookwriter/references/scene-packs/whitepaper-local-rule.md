# 行业白皮书场景包 · 本地规则补丁（local-rule）

> **体裁**：whitepaper · **版本**：2.1.1  
> **适用时机**：四级降级链 L3 阶段自动读取。  
> **与 whitepaper.md 的关系**：本文件补充**质量规则检查项**，不重复 whitepaper.md 已有的 S0/S2 内容。  
> **与 report 的区别**：whitepaper 强调"行业洞察+量化表达+结论可追溯"；report 强调"多方核实+当事方回应"。

---

## L3 降级时的体裁感知规则（Q层叠加）

### 数据质量规则

| ID | 规则 | 违反信号 |
|----|------|---------|
| WP-D1 | 每个核心数据点须有3类来源之一：官方统计/行业报告/学术论文 | "市场规模约X亿"无来源 |
| WP-D2 | 数据须标注年份，且为近3年内（政策类可放宽至5年） | 数据年份超过5年未说明 |
| WP-D3 | 同一指标若多处引用须使用同一来源（避免数据打架） | 同类数据在不同章出现不同数字 |
| WP-D4 | 预测性数据须明确标注"预测"及预测方法 | "2030年将达X"无方法说明 |

### 结论质量规则

| ID | 规则 | 违反信号 |
|----|------|---------|
| WP-C1 | 结论须可从文中数据直接推导，不引入额外假设 | 结论与正文数据无直接关系 |
| WP-C2 | 趋势判断须区分"短期（1-2年）/中期（3-5年）/长期（5年+）" | "趋势明显"无时间维度 |
| WP-C3 | 建议须与问题一一对应（不出现无对应问题的建议） | 建议章节多于问题章节 |

### 引用规范

| ID | 规则 | 违反信号 |
|----|------|---------|
| WP-R1 | 引用须包含：来源名称、发布机构、年份（三要素） | "据某报告"无机构名称 |
| WP-R2 | 直接引用须加引号，间接引用须改写（非逐字抄录） | 大段文字无引号无来源 |
| WP-R3 | 参考文献列表须按正文引用顺序编号 | 文献列表与正文注脚顺序不符 |

---

## L3 离线告知模板

```
【场景包降级通知】
当前场景包（whitepaper）已降级至 L3 本地规则模式。
可用能力：数据质量规则（WP-D1~D4）、结论质量（WP-C1~C3）、引用规范（WP-R1~R3）
不可用：云端行业数据库、引用格式自动填充
白皮书写作不受阻断，请确保所有数据均有3类来源之一支撑。
```

---

*v2.1.0 · E3 落地 · 2026-04-11*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/temporal-accuracy-samples]] — 时效与年份规则：样例与例外（防误报）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/consultant-local-rule]] — 顾问报告场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/genealogy-local-rule]] — 家谱场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/general-local-rule]] — 通用写书场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/ghostwriter-local-rule]] — 代撰稿场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/personal-book-local-rule]] — 个人出书场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/report-local-rule]] — 调查报告场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/report]] — 调查报告场景包——本地内容置入规范（降级用）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/training-local-rule]] — 培训教材场景包 · 本地规则补丁（local-rule）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/scene-packs/whitepaper]] — 行业白皮书场景包（本地内置规范）

<!-- AI-LINKS-END -->
