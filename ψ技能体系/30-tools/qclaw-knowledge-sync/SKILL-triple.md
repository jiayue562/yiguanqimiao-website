---
name: 三向知识库同步增强版
description: |
  增强版三向知识库同步 - 实现 WorkBuddy (LLM Wiki) + Obsidian + IMA 之间的知识同步与备份。
  当用户需要同步知识库、备份笔记、或将本地知识同步到云端时使用此技能。
  支持单向同步（WorkBuddy→Obsidian, WorkBuddy→IMA, Obsidian→IMA）和三向同步。
metadata:
  openclaw:
    emoji: '🔄'
    requires: { env: ['IMA_OPENAPI_CLIENTID', 'IMA_OPENAPI_APIKEY'] }
    primaryEnv: 'IMA_OPENAPI_CLIENTID'
  security:
    credentials_usage: |
      This skill uses user-provisioned IMA OpenAPI credentials to sync knowledge
      to the official IMA API (ima.qq.com). Credentials are read from ~/.config/ima
      and only sent to ima.qq.com as HTTP headers.
    allowed_domains:
      - ima.qq.com
---

# 三向知识库同步增强版

## 功能

### 支持的同步方向

| 同步方向 | 描述 | 状态 |
|----------|------|------|
| WorkBuddy → Obsidian | 将 WorkBuddy 知识库备份到 Obsidian | ✅ |
| WorkBuddy → IMA | 将 WorkBuddy 知识库备份到 IMA 云端 | ✅ |
| Obsidian → IMA | 将 Obsidian 笔记同步到 IMA 云端 | ✅ |
| Obsidian → WorkBuddy | 将 Obsidian 同步回 WorkBuddy | ✅ |
| IMA → Obsidian | 从 IMA 下载笔记到 Obsidian | ✅ |
| 三向同步 | 同时同步三个知识库 | ✅ |

## 配置

### 1. IMA 凭证配置

```bash
# 方式 A - 配置文件（推荐）
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```

### 2. 路径配置

默认路径（在脚本参数中可以覆盖）：

| 知识库 | 默认路径 |
|--------|----------|
| WorkBuddy (LLM Wiki) | `C:\Users\jia'yue\WorkBuddy` |
| Obsidian | `D:\以观其妙书院知识库\以观其妙书院` |
| IMA 知识库 | 以观其妙书院 |
| IMA 文件夹 | 龙龟神将备份资料 (folder_7441985942068358) |

## 使用方法

### 完整三向同步

```powershell
# 三向同步所有内容
.\scripts\sync-triple.ps1 -Direction all

# 仅同步 WorkBuddy → Obsidian → IMA
.\scripts\sync-triple.ps1 -Direction workbuddy-to-obsidian-to-ima
```

### 单向同步

```powershell
# WorkBuddy → Obsidian
.\scripts\sync-triple.ps1 -Direction workbuddy-to-obsidian

# WorkBuddy → IMA
.\scripts\sync-triple.ps1 -Direction workbuddy-to-ima

# Obsidian → IMA
.\scripts\sync-triple.ps1 -Direction obsidian-to-ima
```

### 指定路径

```powershell
# 指定 WorkBuddy 路径
.\scripts\sync-triple.ps1 -WorkBuddyPath "C:\Users\jia'yue\WorkBuddy" -Direction workbuddy-to-ima

# 指定 Obsidian 路径
.\scripts\sync-triple.ps1 -ObsidianVault "D:\以观其妙书院知识库\以观其妙书院" -Direction obsidian-to-ima
```

### 预览模式

```powershell
# 预览模式，不实际执行同步
.\scripts\sync-triple.ps1 -Direction all -DryRun
```

## 同步规则

1. **文件过滤**：默认跳过隐藏文件（以 `.` 开头）和系统文件
2. **冲突处理**：比较修改时间，保留最新版本
3. **增量同步**：只同步新增或修改的文件
4. **错误恢复**：遇到错误跳过该文件，继续同步其他文件

## API 限流说明

IMA API 有请求频率限制（200001）和每日总量限制（200005）。同步大量文件时：
- 脚本会自动处理限流错误
- 可以在明天继续同步剩余文件
- 建议每次同步不超过 500 个文件

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[13-WorkBuddy-Sync/三向同步系统/SKILL]] — 🔗 三向同步系统 (Tri-Sync System) v4.1
- [[01-核心体系/龙脑-思维模型顶层设计/NS3491F-04-三库同步指引]] — 三库同步指引
- [[20-工作记录与复盘/_从根目录迁入/日签/三库同步状态]] — 三库同步状态
- [[20-工作记录与复盘/三向同步_三向同步系统整合方案]] — 第六步：三向同步系统整合方案 v1.0
- [[AI原生组织/NS92885-00-总索引-AI原生组织]] — 00-总索引 · AI原生组织（龙心OS结构化总导航）
- [[ψ技能体系/00-foundation/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[ψ技能体系/00-foundation/三向同步系统/SKILL]] — 🔗 三向同步系统 (Tri-Sync System) v4.1
- [[ψ技能体系/30-tools/qclaw-knowledge-sync/SKILL]] — qclaw-knowledge-sync - 三向知识库同步
- [[ψ技能体系/30-tools/三向知识库同步/SKILL]] — 三向知识库同步总控 Skill

<!-- AI-LINKS-END -->
