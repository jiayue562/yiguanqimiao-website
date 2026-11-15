---
title: "MCP协议定义"
created: "2026-03-22"
tags: [MCP, 协议定义, JSON格式, 规范]
---

# MCP协议定义

## 📋 协议总览

MCP（机器控制协议）定义了AI OS中所有协同交互的标准化格式

---

## 📊 三大核心协议

### 1. 人机协同协议（human-ai）
- **用途**：人向AI发出决策指令，AI向人反馈执行结果
- **特点**：支持个性化参数，带解释性说明
- **格式**：JSON，版本1.0

### 2. 机内协同协议（internal）
- **用途**：AI与Skills、Skills与Skills之间的调用和数据传递
- **特点**：无缝组合，数据透明传递
- **格式**：JSON，版本1.0

### 3. 系统扩展协议（system-extension）
- **用途**：外部工具/服务接入AI OS
- **特点**：无缝融入，可扩展
- **格式**：JSON，版本1.0

---

## 📖 核心金句

> "MCP让整个AI OS成为有机整体，协同高效，无歧义。"

---

## 🔗 关联文件

- `MCP协议通信-SKILL.md`：主技能文件
- `MCP协议使用案例.md`：使用案例
- `MCP协议优化记录.md`：优化记录

---

**标签**：`#MCP` `#协议定义` `#JSON格式` `#规范`

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/AI-OS六层架构智能体/references/MCP协议层]] — MCP层 · 多协议协同总线
- [[09-技能库/AI龙龟共生伙伴操作系统/优化现有Skills指南]] — 优化现有Skills指南
- [[09-技能库/MCP协议管理/SKILL]] — MCP 协议管理 Skill v2.0
- [[09-技能库/MCP协议通信/SKILL]] — MCP协议通信Skill v1.0
- [[09-技能库/MCP协议通信/references/MCP协议优化记录]] — MCP协议优化记录
- [[09-技能库/MCP协议通信/references/MCP协议使用案例]] — MCP协议使用案例
- [[09-技能库/mcp-protocol/SKILL]] — MCP协议配置 Skill
- [[09-技能库/resources_MCP协议优化记录]] — MCP协议优化记录
- [[09-技能库/resources_MCP协议使用案例]] — MCP协议使用案例
- [[09-技能库/resources_MCP协议定义]] — MCP协议定义

<!-- AI-LINKS-END -->
