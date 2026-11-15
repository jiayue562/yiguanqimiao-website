# 🔗 三向同步系统 - 快速开始

> WorkBuddy Brain ↔ Obsidian ↔ IMA 三向知识同步系统

## ✅ 安装状态

| 组件 | 状态 | 版本/信息 |
|------|------|----------|
| 三向同步系统 Skill | ✅ 已安装 | v1.0.0 |
| Obsidian CLI | ✅ 已安装 | v0.2.3 (scoop) |
| IMA API | ✅ 已配置 | 以观其妙书院 |
| WorkBuddy Brain | ✅ 已配置 | 本地路径 |

## 📁 配置信息

### 知识库位置
- **Obsidian**: `D:\以观其妙书院知识库\以观其妙书院`
- **IMA**: 知识库 "以观其妙书院" → 文件夹 "龙龟神将备份资料"
- **WorkBuddy Brain**: `C:\Users\jia'yue\AppData\Roaming\WorkBuddy\User\globalStorage\tencent-cloud.coding-copilot\brain\`

### API 凭证
- **Client ID**: `87e4c9978e1b50b3918e20313b7084ed`
- **API Key**: 已配置（存储在 `ima-skills/config.json`）

## 🚀 快速使用

### 1. Obsidian CLI 基础命令

```bash
# 查看默认仓库
obsidian-cli print-default

# 列出所有笔记
obsidian-cli list

# 搜索笔记
obsidian-cli search "关键词"

# 搜索笔记内容
obsidian-cli search-content "关键词"

# 打开每日笔记
obsidian-cli daily

# 创建新笔记
obsidian-cli create "文件夹/笔记名" --content "内容"

# 打印笔记内容
obsidian-cli print "笔记名"

# 移动/重命名笔记（自动更新链接）
obsidian-cli move "旧路径" "新路径"

# 删除笔记
obsidian-cli delete "笔记名"
```

### 2. 三向同步脚本

```powershell
# 完整同步（WorkBuddy → Obsidian → IMA）
powershell -ExecutionPolicy Bypass -File "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1" -Mode full

# 增量同步
powershell -ExecutionPolicy Bypass -File "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1" -Mode incremental

# 干运行（预览变更，不实际执行）
powershell -ExecutionPolicy Bypass -File "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1" -Mode full -DryRun

# 仅同步 WorkBuddy → Obsidian
powershell -ExecutionPolicy Bypass -File "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1" -Mode workbuddy-to-obsidian

# 仅同步 WorkBuddy → IMA
powershell -ExecutionPolicy Bypass -File "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1" -Mode workbuddy-to-ima
```

### 3. Python 同步脚本

```bash
# 批量同步到 IMA
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\batch_sync_to_ima.py"

# 诊断同步问题
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\diagnose_skip.py"
```

## 📂 文件结构

```
三向同步系统/
├── SKILL.md                    # 技能主文档
├── QUICK_START.md             # 本快速开始文档
├── config/
│   ├── tri_sync_config.json   # 主配置文件
│   └── sync_summary.json      # 配置汇总
├── scripts/
│   ├── tri-sync.ps1           # 主同步脚本（PowerShell）
│   ├── sync.py                # 同步脚本（Python）
│   ├── batch_sync_to_ima.py   # 批量同步到 IMA
│   ├── ima_sync.py            # IMA API 客户端
│   └── setup.ps1              # 安装配置脚本
└── README.md                  # 详细文档
```

## ⚙️ 配置文件

主配置文件: `config/tri_sync_config.json`

```json
{
  "sources": {
    "workbuddy": {
      "path": "C:\\Users\\jia'yue\\AppData\\Roaming\\WorkBuddy\\...",
      "type": "local"
    },
    "obsidian": {
      "vault": "D:\\以观其妙书院知识库\\以观其妙书院",
      "sync_folder": "00-WorkBuddy-Sync"
    },
    "ima": {
      "endpoint": "https://ima.qq.com",
      "folder": "龙龟神将备份资料"
    }
  }
}
```

## 🔄 自动化设置

### 定时任务（Windows 任务计划程序）

```powershell
# 创建每日 23:30 自动同步任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -File `"C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\tri-sync.ps1`" -Mode incremental"

$trigger = New-ScheduledTaskTrigger -Daily -At "23:30"

Register-ScheduledTask -TaskName "三向同步系统-每日备份" `
    -Action $action -Trigger $trigger -Description "WorkBuddy Brain ↔ Obsidian ↔ IMA 三向同步"
```

## 🛡️ 安全说明

- ✅ IMA 凭证仅存储在本地配置文件
- ✅ 支持排除敏感文件（.git, node_modules 等）
- ✅ 同步前自动备份冲突文件
- ✅ 支持干运行模式预览变更

## 📞 故障排除

### 常见问题

1. **obsidian-cli 未找到**
   ```bash
   scoop install obsidian-cli
   ```

2. **权限错误**
   - 以管理员身份运行 PowerShell
   - 或添加 `-ExecutionPolicy Bypass` 参数

3. **路径问题**
   - Windows 路径中的单引号已自动处理
   - 所有脚本已更新为正确路径

4. **IMA API 错误**
   - 检查 `ima-skills/config.json` 中的凭证
   - 确认网络连接正常

## 📊 更新日志

### 2026-04-21 更新
- ✅ 更新所有脚本路径为正确的 "以观其妙书院"
- ✅ 更新 IMA API 凭证为最新版本
- ✅ 验证 obsidian-cli v0.2.3 安装
- ✅ 创建快速开始文档

---

**版本**: 1.0.0  
**最后更新**: 2026-04-21  
**维护者**: 龙龟神将

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/SKILL]] — 🔗 三向同步系统 (Tri-Sync System) v4.1
- [[13-WorkBuddy-Sync/三向同步系统/scripts/IMA_API测试报告]] — IMA API同步测试报告
- [[01-核心体系/agents_知识库建设完成报告]] — 知识库建设完成报告
- [[03-知识地基层/记忆系统_SESSION]] — SESSION.md - 会话上下文
- [[03-知识地基层/记忆系统_对话技术性总结_2026-03-27_严格九部析_v7]] — 对话技术性总结报告（第八次创建·v7）
- [[05-五行人格心理学/理论基石/系统配置_同步报告_20260417]] — 🔄 三向同步报告
- [[20-工作记录与复盘/02-每日日志/2026-04-15]] — 2026-04-15 日志
- [[20-工作记录与复盘/_从根目录迁入/日签/三库同步状态]] — 三库同步状态
- [[20-工作记录与复盘/三向同步_三向同步系统整合方案]] — 第六步：三向同步系统整合方案 v1.0
- [[09-技能库/ima笔记/config]] — IMA Skill 凭证配置

<!-- AI-LINKS-END -->
