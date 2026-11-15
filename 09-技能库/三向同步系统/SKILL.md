---
name: 三向同步系统
description: |
  AI龙龟共生伙伴操作系统的三向知识同步系统，实现 WorkBuddy Brain、Obsidian、IMA 三个知识库的双向同步。
  支持完整的读取、写入，管理功能，通过 obsidian-cli 和 IMA OpenAPI 实现自动化同步。
  当用户需要备份知识库，同步笔记，管理多平台知识资产时触发此技能。v2.0配套AI OS v4.3。
homepage: https://www.codebuddy.cn/docs/workbuddy/Overview
metadata:
  version: "2.0.0"
  updated: "2026-04-24"
  category: "knowledge-sync"
  requires:
    obsidian_cli: "@yakitrak/obsidian-cli"
    ima_api: "https://ima.qq.com/agent-interface"
  paths:
    workbuddy_brain: "C:\\Users\\jia'yue\\AppData\\Roaming\\WorkBuddy\\User\\globalStorage\\tencent-cloud.coding-copilot\\brain\\"
    obsidian_vault: "D:\\以观其妙书院知识库\\以观其妙书院"
    ima_endpoint: "https://ima.qq.com"
---

# 🔗 三向同步系统 (Tri-Sync System) v2.0

> **WorkBuddy Brain ↔ Obsidian ↔ IMA** 三向知识同步系统
> 
> 版本: 2.0.0 | 更新: 2026-04-24 | AI OS v4.3配套

## 🎯 核心功能

1. **三向同步**: WorkBuddy Brain、Obsidian、IMA 三个知识库双向同步
2. **obsidian-cli 集成**: 完整的 Obsidian CRUD 操作（读取、写入、管理）
3. **IMA API 集成**: 云端知识库备份与同步
4. **自动分类**: 智能识别内容类型，自动分类存储
5. **定时备份**: 支持自动化定时同步任务
6. **冲突解决**: 智能处理版本冲突，保留最新内容

## 📁 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    🔗 三向同步系统 v1.0                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ WorkBuddy    │◄──►│   同步引擎   │◄──►│   Obsidian   │  │
│  │   Brain      │    │   (CLI/API)  │    │   (obsidian- │  │
│  │              │    │              │    │     cli)     │  │
│  └──────────────┘    └──────┬───────┘    └──────────────┘  │
│                             │                               │
│                             ▼                               │
│                      ┌──────────────┐                      │
│                      │      IMA     │                      │
│                      │  (云端备份)   │                      │
│                      └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 快速开始

### 1. 安装配置

```powershell
# 运行安装脚本
.\scripts\setup.ps1
```

### 2. 运行同步

```powershell
# 全量同步
.\scripts\tri-sync.ps1 -Mode full

# 增量同步
.\scripts\tri-sync.ps1 -Mode incremental

# 干运行（预览变更）
.\scripts\tri-sync.ps1 -Mode full -DryRun
```

## 📋 同步目录结构

### Obsidian 同步结构
```
D:\以观其妙书院知识库\以观其妙书院\
├── 00-WorkBuddy同步/
│   ├── 01-对话记录/      # 对话会话记录
│   ├── 02-记忆系统/      # 长期记忆和工作记忆
│   ├── 03-技能库/        # 技能文档
│   └── 04-知识沉淀/      # 知识沉淀文档
└── 同步索引.md
```

## 🔧 核心命令

### obsidian-cli 命令

```bash
# 读取笔记
obsidian-cli read "笔记名称"

# 创建/写入笔记
obsidian-cli write "笔记名称" --content "内容"

# 追加内容
obsidian-cli append "笔记名称" --content "追加内容"

# 搜索笔记
obsidian-cli search "关键词"

# 列出所有笔记
obsidian-cli list
```

### 三向同步 CLI

```powershell
# 同步所有内容
.\scripts\tri-sync.ps1 -Mode full

# 仅同步对话记录
.\scripts\tri-sync.ps1 -Mode incremental

# 干运行（预览变更）
.\scripts\tri-sync.ps1 -DryRun

# 强制重新同步
.\scripts\tri-sync.ps1 -Force
```

## ⚙️ 配置文件

配置文件路径: `config/tri_sync_config.json`

```json
{
  "version": "1.0.0",
  "sources": {
    "workbuddy": {
      "path": "C:\\Users\\jia'yue\\AppData\\Roaming\\WorkBuddy\\...",
      "type": "local"
    },
    "obsidian": {
      "vault": "D:\\以观其妙书院知识库\\以观其妙书院",
      "sync_folder": "00-WorkBuddy同步"
    },
    "ima": {
      "endpoint": "https://ima.qq.com"
    }
  }
}
```

## 🔄 自动化配置

### 定时任务（Windows 任务计划程序）

```powershell
# 创建每日 23:30 自动同步任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-File `"C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1`" -Mode incremental"

$trigger = New-ScheduledTaskTrigger -Daily -At "23:30"

Register-ScheduledTask -TaskName "三向同步系统-每日备份" `
    -Action $action -Trigger $trigger -Description "WorkBuddy Brain ↔ Obsidian ↔ IMA 三向同步"
```

## 📊 监控和报告

同步完成后自动生成报告：

```markdown
# 三向同步报告

**同步时间**: 2026-04-17 10:30:00  
**同步模式**: full

## 统计

| 指标 | 数值 |
|------|------|
| 扫描文件 | 156 |
| 已同步 | 23 |
| 已跳过 | 133 |
| 错误 | 0 |
```

## 🛡️ 安全说明

- IMA 凭证仅存储在本地 `~/.config/ima/credentials`
- 凭证仅用于官方 IMA API 认证
- 不会将凭证发送到任何第三方服务
- 支持排除敏感文件模式

## 📞 故障排除

### 常见问题

1. **obsidian-cli 未找到**: 运行 `npm install -g @yakitrak/obsidian-cli`
2. **权限错误**: 以管理员身份运行 PowerShell
3. **路径问题**: Windows 路径中的单引号已自动处理
4. **IMA API 错误**: 检查凭证文件是否正确配置

---

**版本**: 1.0.0  
**最后更新**: 2026-04-17  
**兼容性**: WorkBuddy 1.0+, Obsidian 1.0+, IMA API  
**许可证**: MIT

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/2026-08-26]] — 2026-08-26 工作日志
- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[03-知识地基层/记忆系统_MEMORY_WorkBuddy]] — MEMORY.md - 龙龟神将长期记忆（WorkBuddy工作记忆）
- [[03-知识地基层/记忆系统_同步报告_20260327]] — 同步报告_20260327
- [[09-技能库/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[ψ技能体系/00-foundation/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始

<!-- AI-LINKS-END -->
