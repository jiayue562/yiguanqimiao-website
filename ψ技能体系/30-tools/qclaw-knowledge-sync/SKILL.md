---
name: qclaw-knowledge-sync
parent_skill: ai-os
description: |
  三向知识库同步技能 - 实现 OpcCla + Obsidian + IMA 之间的知识同步与备份。
  当用户需要同步知识库、备份笔记、或将本地知识同步到云端时使用此技能。
  支持单向同步（Obsidian→IMA）和双向同步（检测冲突并合并）。
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

# qclaw-knowledge-sync - 三向知识库同步

## 功能

- **OpcCla → Obsidian**: 将 OpcCla 知识库导出到本地 Obsidian
- **Obsidian → IMA**: 将 Obsidian 笔记同步到 IMA 云端知识库
- **IMA → Obsidian**: 从 IMA 下载笔记到本地 Obsidian
- **冲突检测**: 比较修改时间，避免重复同步

## 配置

### 1. IMA 凭证配置

```bash
# 方式 A - 配置文件（推荐）
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key

# 方式 B - 环境变量
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"
```

### 2. 路径配置

编辑脚本参数或创建配置文件 `~/.config/qclaw/sync.json`:

```json
{
  "obsidian_vault": "D:\\以观其妙书院知识库\\观其妙书院",
  "opclaw_knowledge": "C:\\Users\\<user>\\.OpcCla 知识库",
  "knowledge_base_name": "以观其妙书院"
}
```

## 使用

### 同步 Obsidian → IMA

```powershell
# 完整同步
.\scripts\sync-obsidian-to-ima.ps1

# 指定知识库
.\scripts\sync-obsidian-to-ima.ps1 -ObsidianVault "D:\以观其妙书院知识库\观其妙书院" -KnowledgeBaseName "以观其妙书院"

# 预览模式（不实际同步）
.\scripts\sync-obsidian-to-ima.ps1 -DryRun
```

### 同步 OpcCla → Obsidian

```powershell
.\scripts\sync-opclaw-to-obsidian.ps1 -Source "C:\Users\<user>\.OpcCla 知识库" -Target "D:\以观其妙书院知识库\观其妙书院"
```

### 定时同步

使用 OpenClaw cron 配置每日自动同步：

```bash
openclaw cron add --schedule "0 2 * * *" --command "sync-obsidian-to-ima.ps1"
```

## 注意事项

1. **首次同步**: 建议先用 `-DryRun` 预览，确认无误后再执行
2. **冲突处理**: 脚本会比较修改时间，较新的版本会覆盖较旧的
3. **大文件**: 单个文件超过 10MB 可能失败，建议分批同步
4. **网络**: 确保能访问 ima.qq.com

## 故障排除

- **凭证错误**: 检查 `~/.config/ima/client_id` 和 `~/.config/ima/api_key`
- **权限问题**: 确保对 Obsidian Vault 有读写权限
- **API 限制**: IMA API 有速率限制，大批量同步时添加延迟

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[03-知识地基层/记忆系统_BOOTSTRAP]] — BOOTSTRAP.md - 启动配置
- [[20-工作记录与复盘/三向同步_三向同步系统整合方案]] — 第六步：三向同步系统整合方案 v1.0
- [[ψ技能体系/00-foundation/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[ψ技能体系/30-tools/qclaw-knowledge-sync/SKILL-triple]] — 三向知识库同步增强版
- [[ψ技能体系/30-tools/三向知识库同步/SKILL]] — 三向知识库同步总控 Skill

<!-- AI-LINKS-END -->
