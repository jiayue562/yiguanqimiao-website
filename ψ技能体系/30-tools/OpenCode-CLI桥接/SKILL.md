---
name: opencode-cli-bridge
parent_skill: ai-os
description: WorkBuddy → OpenCode CLI桥接。通过 opencode run 命令在非交互模式下调用OpenCode的Agent（sm-chief/build/plan/general等），获取结果后返回WorkBuddy。
version: 1.0.0
metadata:
  audience: 悟空
  type: 桥接Skill
---

# OpenCode CLI 桥接

## 核心能力

通过 `opencode run` CLI 让 WorkBuddy 直接调用 OpenCode 的 Agent 能力。

## CLI 命令模板

```bash
# 基础调用
opencode run --agent <agent名> --format json "<任务描述>"

# 指定模型
opencode run --agent sm-chief -m anthropic/claude-sonnet-4-20250514 "<任务>"

# 指定工作目录
opencode run --agent sm-chief --dir "/c/Users/jia'yue/WorkBuddy/Claw" "<任务>"
```

## 可用 Agent

| Agent | 模式 | 用途 |
|-------|------|------|
| `sm-chief` | primary | 味藏店长总控·7S智能体调度 |
| `build` | subagent | 全工具开发Agent |
| `plan` | subagent | 只分析规划，不改代码 |
| `general` | subagent | 通用复杂任务 |
| `explore` | subagent | 代码库搜索（只读） |

## 使用场景

### 场景1：触发味藏7S月度诊断
```
opencode run --agent sm-chief "执行2026年5月人才盘点，用九宫格+559型评分+离职风险预警"
```

### 场景2：分析味藏门店数据
```
opencode run --agent sm-chief "分析松山湖店本月经营数据，按包间/卡座双维度拆解，检查成本率是否≤65%"
```

### 场景3：跨S闭环诊断
```
opencode run --agent sm-chief "金月湾店本周离职风险预警2人，触发跨S联动：检查SV价值观+Sty氛围，联合输出诊断报告"
```

### 场景4：代码/文件分析（build agent）
```
opencode run --agent build "分析 Desktop/味藏店长岗位Skills-1+N完整闭环设计-v7.1.md 的结构完整性"
```

## 注意事项

1. `--format json` 适合脚本解析，去掉则获得人类可读输出
2. sm-chief 依赖 `~/.agents/skills/sm-*` 7S分智能体Skills
3. sm-chief 通过 workbuddy-bridge Plugin 可反向写入WorkBuddy记忆
4. 每次 `opencode run` 创建独立会话，不共享上下文
5. 执行时间取决于任务复杂度，简单查询5-15秒，复杂分析30-60秒

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[03-知识地基层/记忆系统_AGENTS]] — AGENTS.md - 智能体配置
- [[03-知识地基层/记忆系统_obsidian-backup-system]] — 🚀 WorkBuddy ↔ Obsidian 知识备份系统
- [[03-知识地基层/记忆系统_skills-sync-summary]] — Skills文档同步检查报告
- [[03-知识地基层/记忆系统_同步报告_20260410]] — WorkBuddy三向同步报告
- [[05-五行人格心理学/理论基石/系统配置_Obsidian知识库同步机制]] — 🔄 Obsidian知识库同步机制
- [[09-技能库/五行人格心理学OS/completion-report]] — 🎉 五行人格心理�?OS 封装完成报告

<!-- AI-LINKS-END -->
