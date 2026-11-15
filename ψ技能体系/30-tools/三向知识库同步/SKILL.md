---
name: 三向知识库同步
parent_skill: ai-os
description: OpcClaw/Obsidian/IMA三向知识库同步总控 - 实现三层知识库之间的单向/双向同步与冲突合并
---

# 三向知识库同步总控 Skill

> 🔄 OpcClaw ↔ Obsidian ↔ IMA 三向同步引擎

**版本**: v2.0  
**创建**: 2026-04-17  
**作者**: 悟空 × 龙龟神将  
**状态**: ✅ 已安装并配置

---

## 🎯 一句话核心定义

**三向知识库同步引擎** - 实现 OpcClaw、Obsidian、IMA 之间的自动同步、备份和知识资产管理。

---

## 📋 三行问题陈述

**What**: 三个知识库（OpcClaw/Obsidian/IMA）之间的双向/三向同步  
**Why**: 避免知识孤岛，确保知识资产安全，实现随时随地访问  
**How**: 调用现有 qclaw-knowledge-sync + ima-skill + obsidian-cli 协同工作

---

## 🧠 核心能力

1. **OpcClaw → Obsidian**: 将 OpcClaw 知识库导出到本地 Obsidian Vault
2. **Obsidian → IMA**: 将 Obsidian 笔记同步到 IMA 云端
3. **IMA → Obsidian**: 从 IMA 下载笔记到本地 Obsidian
4. **冲突检测**: 比较修改时间，避免重复同步
5. **定时同步**: 配置 cron 任务实现每日自动同步
6. **安全体检**: 定期扫描知识库安全风险

---

## 🚫 使用边界

### 做什么
- ✅ 三向知识库同步
- ✅ 备份和恢复
- ✅ 冲突检测和解决
- ✅ 定时自动同步
- ✅ 安全体检

### 不做什么
- ❌ 修改原始文件内容（保持原样）
- ❌ 删除任何知识库的内容（除非明确指示）
- ❌ 同步非 Markdown 文件（除非特别配置）

---

## 🔄 触发条件

### P0 直接触发（权重 5）
```
三向同步、知识库同步、同步 Obsidian、同步 IMA、
备份知识库、OpcClaw 同步、知识资产沉淀、
sync、backup knowledge、sync to IMA
```

### P1 场景触发（权重 4）
```
把 OpcClaw 的内容备份到 Obsidian
将 Obsidian 笔记同步到 IMA
从 IMA 下载笔记
配置自动同步
知识库安全吗
```

### P2 信号触发（权重 3）
```
"同步.*知识库"、"备份.*笔记"、
"Obsidian.*IMA"、"OpcClaw.*Obsidian"
```

---

## ⚡ 激活后的行为流程

```
用户输入
    ↓
1. 意图识别（同步方向/操作类型）
    ↓
2. 凭证验证（IMA credentials）
    ↓
3. 路径验证（Obsidian Vault / OpcClaw 知识库）
    ↓
4. 选择同步模式
    ├── 单向同步（OpcClaw→Obsidian 或 Obsidian→IMA）
    ├── 双向同步（检测冲突）
    ├── 三向同步（完整同步）
    └── 预览模式（DryRun）
    ↓
5. 执行同步
    ↓
6. 输出报告（成功/失败/冲突）
    ↓
7. 询问是否配置定时同步
```

---

## 📐 核心原则

### 必须
- ✅ 同步前验证凭证和路径
- ✅ 大文件分批同步（>10MB）
- ✅ 输出详细同步报告
- ✅ 冲突时询问用户如何处理
- ✅ 首次同步使用 DryRun 预览

### 禁忌
- ❌ 不验证直接同步
- ❌ 静默覆盖用户文件
- ❌ 同步过程中断不报告
- ❌ 忽略 API 速率限制

---

## 📥 标准输入格式

### 完整同步
```markdown
**意图**: 三向同步
**同步方向**: OpcClaw→Obsidian→IMA / 单向 / 双向
**预览模式**: 是/否
**冲突处理**: 保留新版本/询问我/跳过
```

### 备份
```markdown
**意图**: 备份知识库
**源路径**: [OpcClaw/Obsidian/IMA]
**目标路径**: [OpcClaw/Obsidian/IMA]
**备份范围**: 全部/指定目录/指定文件
```

### 定时同步
```markdown
**意图**: 配置自动同步
**频率**: 每日/每周/每月
**时间**: HH:MM
**同步方向**: [方向]
```

---

## 🔄 处理流程（决策树）

```
用户输入
    │
    ├─ 包含"预览/DryRun"？
    │   └─ 是 → 预览模式（不实际同步）
    │
    ├─ 包含"OpcClaw→Obsidian"？
    │   └─ 是 → 调用 sync-opclaw-to-obsidian.ps1
    │
    ├─ 包含"Obsidian→IMA"？
    │   └─ 是 → 调用 sync-obsidian-to-ima.ps1
    │
    ├─ 包含"三向同步/完整同步"？
    │   └─ 是 → 依次执行 OpcClaw→Obsidian→IMA
    │
    ├─ 包含"定时/自动"？
    │   └─ 是 → 配置 cron 任务
    │
    └─ 默认 → 询问同步方向和模式
```

---

## 📤 标准输出格式

### 同步报告
```markdown
## 🔄 同步完成报告

### 同步方向
[OpcClaw → Obsidian → IMA]

### 同步统计
- **总文件数**: X 个
- **成功同步**: Y 个
- **跳过（无变化）**: Z 个
- **失败**: W 个
- **冲突**: V 个

### 详细信息
✅ [文件 1] - 同步成功
✅ [文件 2] - 同步成功
⏭️ [文件 3] - 跳过（无变化）
❌ [文件 4] - 失败（原因）
⚠️ [文件 5] - 冲突（待处理）

### 下一步
- [ ] 处理冲突文件
- [ ] 重试失败文件
- [ ] 配置定时同步
```

---

## 📚 示例（真实案例）

### 示例 1: 完整同步
**用户**: "把 OpcClaw 的知识库同步到 Obsidian 和 IMA"  
**输出**: 执行 OpcClaw→Obsidian→IMA，输出同步报告

### 示例 2: 预览模式
**用户**: "预览一下同步，先不同步"  
**输出**: DryRun 模式，显示将同步的文件列表

### 示例 3: 定时同步
**用户**: "每天凌晨 2 点自动同步"  
**输出**: 配置 cron 任务，确认配置成功

---

## ⚠️ 异常处理

| 异常情况 | 处理方式 |
|----------|----------|
| IMA 凭证无效 | 提示重新配置，提供配置步骤 |
| Obsidian Vault 不存在 | 询问正确路径或创建 |
| 文件冲突（两边都修改） | 列出差异，让用户选择 |
| API 速率限制 | 等待后重试，添加延迟 |
| 大文件失败（>10MB） | 建议分批或跳过 |

---

## 🔗 与其他 Skills 的关系

### 前置 Skill
- **ima-skill**: IMA API 调用基础
- **qclaw-knowledge-sync**: 同步脚本执行
- **obsidian-cli**: Obsidian 管理

### 协同 Skill
- **cron-helper**: 定时同步配置
- **skill-vetter**: 安全审查

### 后置 Skill
- **无**: 同步完成后无需后续

---

## 🛠️ 配置说明

### 1. IMA 凭证配置

```bash
# 已配置，无需重复
Client ID: 87e4c9978e1b50b3918e20313b7084ed
API Key: Nz+edkQVyEPzgKkFIpb/4+rc5/sWmSqU3Hvd+AbLtakHt9UGmIko6CihWRIh9Z5L46zCHvPl6g==
位置：~/.config/ima/client_id 和 ~/.config/ima/api_key
```

### 2. 路径配置

```json
{
  "obsidian_vault": "D:\\以观其妙书院知识库\\观其妙书院",
  "opclaw_knowledge": "C:\\Users\\jia'yue\\.OpcClaw 知识库",
  "knowledge_base_name": "以观其妙书院"
}
```

### 3. 脚本位置

```
~/.agents/skills/qclaw-knowledge-sync/scripts/
├── sync-all.ps1                   # 完整三向同步
├── sync-opclaw-to-obsidian.ps1   # OpcClaw→Obsidian
├── sync-obsidian-to-ima.ps1      # Obsidian→IMA
└── security_check_v3.py          # 安全体检
```

---

## 🧪 测试用例

### T01: OpcClaw→Obsidian 同步
**输入**: "把 OpcClaw 的知识库同步到 Obsidian"  
**预期**: 执行 sync-opclaw-to-obsidian.ps1，输出同步报告

### T02: Obsidian→IMA 同步
**输入**: "将 Obsidian 笔记同步到 IMA"  
**预期**: 执行 sync-obsidian-to-ima.ps1，输出同步报告

### T03: 预览模式
**输入**: "预览一下同步，先不同步"  
**预期**: DryRun 模式，显示文件列表

### T04: 定时同步配置
**输入**: "每天凌晨 2 点自动同步"  
**预期**: 配置 cron 任务，确认成功

### T05: 安全体检
**输入**: "检查一下知识库安全吗"  
**预期**: 执行 security_check_v3.py，输出安全评分

---

## 📈 版本迭代

| 版本 | 时间 | 改动点 |
|------|------|--------|
| v1.0 | 2026-04-07 | 初始版本（qclaw-knowledge-sync） |
| v2.0 | 2026-04-17 | 整合三向同步总控功能 |

---

## 💬 核心金句

> "知识不同步，就是孤岛。"

> "OpcClaw 是图纸，Obsidian 是建筑，IMA 是云端备份。"

> "三向同步，知识资产永不丢失。"

---

_三向知识库同步总控 Skill v2.0 · 2026-04-17 · 龙心 OS_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[01-核心体系/agents_龙心 OS 记忆系统架构]] — 龙心 OS 记忆系统架构
- [[03-知识地基层/记忆系统_obsidian-backup-system]] — 🚀 WorkBuddy ↔ Obsidian 知识备份系统
- [[20-工作记录与复盘/三向同步_三向同步系统整合方案]] — 第六步：三向同步系统整合方案 v1.0
- [[ψ技能体系/30-tools/qclaw-knowledge-sync/SKILL-triple]] — 三向知识库同步增强版
- [[ψ技能体系/30-tools/qclaw-knowledge-sync/SKILL]] — qclaw-knowledge-sync - 三向知识库同步

<!-- AI-LINKS-END -->
