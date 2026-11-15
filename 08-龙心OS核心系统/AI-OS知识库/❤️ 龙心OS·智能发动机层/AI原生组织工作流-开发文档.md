---
title: "AI原生组织工作流·开发文档"
created: "2026-06-11"
tags: [开发文档, AI原生组织, 工作流, 数据模型, 龙心OS, Skill]
aliases: [AI原生组织工作流Skill, 组织工作流]
---

# AI原生组织工作流 · 开发文档

> **版本**：v1.0 | **关联Skill**：`~/.workbuddy/skills/AI原生组织工作流/SKILL.md`

---

## 核心定位

AI原生组织工作流是龙心OS的任务分解引擎，基于"AI原生组织"的串行/并行/瓶颈三分类模型，对每次任务自动进行工作分解与标注。

### 三分类标注体系

| 符号 | 类别 | 含义 |
|------|------|------|
| 🟢 [AI] | AI并行 | 龙龟独立完成，无需悟空干预 |
| 🔴 [人] | 人串行 | 悟空必须亲自决策/判断/批准 |
| 🟡 [⇄] | 串联瓶颈 | AI做完后需等待悟空处理的节点 |

### 工作流四阶段

1. **任务分析** → 识别三类工作
2. **并行执行** → 执行所有🟢 [AI]
3. **收敛报告** → 标记🟡 [⇄]，呈现结果
4. **完成总结** → 输出统计 + 压缩建议

---

## 文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| SKILL.md | `~/.workbuddy/skills/AI原生组织工作流/SKILL.md` | 主Skill规则 |
| 开发文档 | `~/.workbuddy/skills/AI原生组织工作流/references/开发文档.md` | 完整开发技术文档 |
| 瓶颈日志 | `~/.workbuddy/skills/AI原生组织工作流/references/bottleneck-log.md` | 串行瓶颈记录 |

---

## 双向链接

- [[AI原生组织-深度学习报告]]
- [[悟空-AI原生组织诊断报告]]
- [[人机协同五象限·理论体系完整版]]
- [[龙心OS总索引]]

---

**创建日期**: 2026-06-11
**版本**: v1.0

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/04-Knowledge/附录B-AI龙龟共生OS-Skills生态全图]] — 附录B：AI龙龟共生OS · Skills生态全图
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙爪OS：AI原生组织岗位智能体/学习资料/岗位智能体生成器-开发文档（AI原生组织版）]] — 岗位智能体生成器 · 开发文档（AI原生组织版）
- [[01-核心体系/龙心OS_人机协同四象限.skills]] — 人机协同四象限.skills
- [[01-核心体系/龙心OS_📖Harness-Engineering编排层]] — Harness Engineering编排层
- [[01-核心体系/龙心OS_🤝 人机协同五象限Skills]] — 人机协同五象限.skills
- [[ψ技能体系/10-kernel/龙心OS/engines/串行瓶颈诊断引擎/SKILL]] — 串行瓶颈诊断引擎
- [[ψ技能体系/10-kernel/龙脑OS/AI原生组织方法论/diagnosis/AI原生组织工作流/SKILL]] — AI原生组织工作流Skill v1.0 - 人机协同五象限执行层工具
- [[ψ技能体系/10-kernel/龙脑OS/AI原生组织方法论/diagnosis/AI原生组织工作流/references/bottleneck-log]] — 瓶颈日志
- [[ψ技能体系/10-kernel/龙脑OS/AI原生组织方法论/diagnosis/AI原生组织工作流/references/开发文档]] — AI原生组织工作流·开发文档
- [[ψ技能体系/20-claws/01-weizang/AI原生组织工作流/SKILL]] — AI原生组织工作流Skill v1.0

<!-- AI-LINKS-END -->
