---
name: 质量门禁规则
parent_skill: ai-os
description: G1/G2/G3三级门禁体系——AI OS输出质量的三道关口
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## 质量门禁规则 v1.0

### 三级门禁

**G1 格式门禁（自动）**
- 检查输出是否符合SKILL.md格式
- 检查字段完整性
- 检查编码一致性

**G2 逻辑门禁（自动+人工）**
- 检查逻辑自洽性
- 检查数据一致性
- 检查引用准确性

**G3 业务门禁（人工）**
- 检查业务适配性
- 检查可执行性
- 检查价值观对齐

### 门禁流程
输入 → G1自动检查 → 通过 → G2检查 → P0/P1需人工 → P2自动 → G3人工抽检
                     不通过 → 退回修改          不通过 → 退回
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS/岗位智能体生成器-开发文档全案]] — 岗位智能体生成器 · 开发文档全案
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙爪OS：AI原生组织岗位智能体/学习资料/岗位智能体生成器-开发文档全案]] — 岗位智能体生成器 · 开发文档全案
- [[16-工具与资源/工具脚本_知识库验证系统]] — 🤖 知识库验证系统
- [[09-技能库/PPT读取/test-cases]] — PPT读取 Skill 测试用例
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/lint-config]] — Linting 配置
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s5]] — S5 节点

<!-- AI-LINKS-END -->
