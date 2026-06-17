# MEMORY.md - 龙龟神将长期记忆（WorkBuddy工作记忆）

> 本文件为WorkBuddy工作记忆同步备份，最后同步时间：2026-03-27 09:26

## 系统架构
- 三向同步系统：WorkBuddy ↔ Obsidian ↔ IMA
- 同步脚本：`C:\Users\jia'yue\.workbuddy\scripts\tri_sync_with_ima.py`
- 配置文件：`C:\Users\jia'yue\.workbuddy\skills\workbuddy-obsidian-backup\config.json`
- 同步报告目录：`C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\05-系统配置\`

## Obsidian 知识库结构
- 03-记忆系统：存储核心记忆文件（IDENTITY.md, USER.md, MEMORY.md, SOUL.md等）
- 09-技能库：存储 skills 技能包文档
- 05-系统配置：存储同步报告和系统配置

## Skills 统计（2026-03-27 最新）
- WorkBuddy端技能目录：约80个（含五行分类图谱等最新技能）
- Obsidian 09-技能库：约71个技能目录
- 核心独创技能：Dragon-OS, 象思维, 五色光思维, 人机协同四象限, 知行合一等
- 五行人格心理学：木/火/土/金/水 各一套完整体系 + L7理论基石（12篇+70条跨域联系）⭐
- 新增：五行分类图谱 v1.0（龙心OS第七引擎·神经网络引擎）⭐

## 最近同步记录
- **2026-03-27 09:26（本次同步）**：
  - ✅ 新增五行分类图谱技能 → Obsidian 09-技能库
  - ✅ 03-记忆系统 MEMORY_WorkBuddy.md 更新
  - ⚠️ IMA同步：仍受EPERM限制
- 2026-03-26 08:07：手动同步，新增19个技能包到Obsidian 09-技能库
  - 第一批11个：技能创建指南、去AI味、内容发布规则、任务看板、通信规则、推荐工具清单、心跳巡检档案、长期记忆档案、skill-vetter、task-router、user-context
  - 第二批8个：agent-swarm、agentdb-vector-search、create-sub-agent、ima笔记、L7理论基石、MCP管理器、memory-management、rag-skill
- 03-记忆系统 MEMORY.md 升级至 v2.1

## 待处理
- IMA API 同步：EPERM限制，手动运行：`python C:\Users\jia'yue\.workbuddy\scripts\tri_sync_with_ima.py`
- 自动化同步任务：每天 23:30 执行

---
*最后更新：2026-03-27 09:26*
