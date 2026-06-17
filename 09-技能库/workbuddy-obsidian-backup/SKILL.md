---
name: workbuddy-obsidian-backup
description: "将WorkBuddy所有内容备份到Obsidian知识库，作为知识资产沉淀。支持自动分类存储和定期备份。"
homepage: https://www.codebuddy.cn/docs/workbuddy/Overview
metadata: {"category": "backup", "requires": {"obsidian_vault": "C:\\Users\\jia'yue\\Desktop\\以观其妙书院知识库\\观其妙书院\\"}}
---

# WorkBuddy → Obsidian 备份技能

## 🎯 功能概述

本技能提供将WorkBuddy系统所有内容备份到Obsidian知识库的完整解决方案，实现：

1. ✅ **全量备份**: 备份WorkBuddy所有知识资产
2. ✅ **分类存储**: 按照文件类型和内容分类存储
3. ✅ **定期备份**: 支持自动化定时备份
4. ✅ **差异备份**: 只备份新增或修改的内容
5. ✅ **元数据维护**: 保持文件属性和关系

## 📁 备份目录结构

在Obsidian知识库中创建的备份结构：

```
WorkBuddy知识备份体系/
├── 00-系统配置/
│   ├── TOOLS.md          # 工具列表和状态
│   ├── USER.md           # 用户配置文件
│   ├── SESSION.md        # 会话记录
│   └── SOUL.md           # 灵魂配置
│
├── 01-技能库/
│   ├── 技能列表.md       # 所有技能的索引
│   ├── browser-automation/     # 浏览器自动化技能
│   ├── obsidian/               # Obsidian技能
│   ├── web-search-plus/        # 网络搜索技能
│   └── ...                     # 其他技能
│
├── 02-记忆系统/
│   ├── 记忆库.md         # 核心记忆总览
│   ├── 长期记忆/         # 长期存储的知识
│   ├── 工作记忆/         # 近期会话记录
│   └── 技能记忆/         # 技能使用历史
│
├── 03-对话记录/
│   ├── 对话归档.md       # 所有对话索引
│   ├── 2026-03/         # 按年月归档
│   │   ├── 2026-03-16-工作流优化.md
│   │   ├── 2026-03-16-browser-automation修复.md
│   │   └── 2026-03-16-obsidian备份设置.md
│   └── 关系图.md         # 对话关系图谱
│
├── 04-知识沉淀/
│   ├── 思维模型/         # 核心思维模型
│   ├── 五行人格心理学/   # 人格分析体系
│   ├── 五色光思维/       # 教员方法论
│   ├── 象思维/           # 象思维理论
│   ├── 企业文化/         # 企业文化建设
│   ├── AI技术应用/       # AI应用指南
│   └── 龙龟神将进化/     # AI共生伙伴进化记录
│
├── 05-工作流/
│   ├── 自动化任务/       # 自动化配置
│   ├── 日常巡检/         # 系统维护记录
│   └── 优化建议/         # 系统优化方案
│
├── 06-项目文件/
│   ├── Claw项目/         # Claw项目文档
│   └── 其他项目/         # 其他项目文件
│
└── 备份日志/
    ├── 备份统计.md       # 备份数据统计
    ├── 备份报告_2026-03-16.md  # 单次备份报告
    └── 问题记录.md       # 备份异常记录
```

## 🚀 快速开始

### 方法1: 手动备份（立即执行）
```bash
# 运行备份命令
python workbuddy_backup.py --obsidian-path "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\" --full-backup
```

### 方法2: 自动备份（设置定时任务）
```bash
# 设置每日23:30自动备份
python workbuddy_backup.py --obsidian-path "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\" --schedule "daily" --time "23:30"
```

### 方法3: 差异备份（仅备份变更）
```bash
# 仅备份上次备份后有变化的文件
python workbuddy_backup.py --obsidian-path "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\" --incremental
```

## 🔧 配置文件

创建配置文件 `workbuddy_backup_config.json`:

```json
{
  "obsidian_vault_path": "C:\\Users\\jia'yue\\Desktop\\以观其妙书院知识库\\观其妙书院\\",
  "workbuddy_path": "C:\\Users\\jia'yue\\.workbuddy\\",
  "backup_targets": {
    "system_config": ["TOOLS.md", "USER.md", "SESSION.md", "SOUL.md", "mcp.json", "settings.json"],
    "skills": {
      "include_all": true,
      "exclude": [],
      "include_files": ["SKILL.md", "README.md", "*.py", "*.sh", "*.json", "*.yaml"]
    },
    "memories": {
      "source": "C:\\Users\\jia'yue\\AppData\\Roaming\\WorkBuddy\\User\\globalStorage\\tencent-cloud.coding-copilot\\brain\\",
      "include_patterns": ["*.md", "*.json"]
    },
    "projects": {
      "claw": "C:\\Users\\jia'yue\\WorkBuddy\\Claw\\"
    }
  },
  "backup_options": {
    "incremental_backup": true,
    "preserve_timestamps": true,
    "create_backup_log": true,
    "compress_old_backups": false,
    "max_backup_versions": 30
  },
  "classification_rules": {
    "by_extension": {
      ".md": "文档",
      ".py": "代码/Python",
      ".js": "代码/JavaScript",
      ".json": "配置",
      ".yaml": "配置/YAML",
      ".sh": "脚本/Shell",
      ".html": "网页/HTML"
    },
    "by_filename": {
      "SKILL.md": "技能/文档",
      "README.md": "文档/说明",
      "*.config.json": "配置/系统",
      "settings.json": "配置/用户"
    },
    "by_content": {
      "思维模型": ["五色光", "象思维", "五行"],
      "技术文档": ["API", "函数", "类", "模块"],
      "对话记录": ["用户说", "助手说", "对话"]
    }
  }
}
```

## 📊 监控和报告

备份完成后生成报告：

```markdown
# 📊 WorkBuddy → Obsidian 备份报告

## 基本信息
- **备份时间**: 2026-03-16 10:30:00
- **备份类型**: 全量备份
- **执行时长**: 5分23秒
- **备份状态**: ✅ 成功

## 备份统计
| 类别 | 文件数 | 大小 | 新增 | 修改 | 删除 |
|------|--------|------|------|------|------|
| 系统配置 | 6 | 45KB | 1 | 2 | 0 |
| 技能库 | 57 | 2.3MB | 3 | 5 | 0 |
| 记忆系统 | 23 | 890KB | 12 | 3 | 0 |
| 对话记录 | 15 | 1.1MB | 15 | 0 | 0 |
| **总计** | **101** | **4.3MB** | **31** | **10** | **0** |

## 详细记录
- ✅ 已备份: TOOLS.md (系统配置更新)
- ✅ 已备份: browser-automation/SKILL.md (新技能安装)
- ✅ 已备份: 8dce1e276da744ba8d3095c2da782f86/overview.md (会话记录)
- ⚠️ 跳过: node_modules/ (排除目录)
- ⚠️ 跳过: *.pyc (排除文件类型)

## 下次备份建议
- 计划时间: 2026-03-17 10:30:00
- 备份类型: 差异备份
- 预估大小: ~120KB
```

## ⚙️ 高级功能

### 1. 智能分类
基于文件内容和元数据自动分类：
- 按文件扩展名
- 按文件命名模式
- 按内容关键词
- 按修改时间

### 2. 关系映射
创建文件间关系：
- 双向链接（Obsidian风格）
- 引用关系图
- 时间线视图
- 知识图谱

### 3. 版本控制
- 保留历史版本
- 差异对比
- 版本回滚
- 备份时间线

### 4. 安全保护
- 排除敏感文件（*.env, 密码等）
- 加密备份选项
- 完整性校验
- 备份验证

## 🔄 自动化配置

### 自动化任务配置
```toml
# .workbuddy/automations/workbuddy-obsidian-backup/automation.toml
name = "WorkBuddy-Obsidian每日备份"
prompt = "执行WorkBuddy到Obsidian的全量备份"
rrule = "FREQ=DAILY;BYHOUR=23;BYMINUTE=30"
cwds = ["C:\\Users\\jia'yue\\.workbuddy"]
status = "ACTIVE"
```

### 手动触发备份
```bash
# 在WorkBuddy对话中使用
使用 "workbuddy-obsidian-backup" 技能执行全量备份
```

## 📞 故障排除

### 常见问题
1. **权限问题**: 确保有Obsidian目录的写入权限
2. **路径问题**: Windows路径中的单引号需要转义
3. **空间不足**: 检查磁盘空间
4. **文件锁定**: 确保文件未被其他程序占用

### 调试模式
```bash
python workbuddy_backup.py --obsidian-path "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\" --debug --dry-run
```

## 🔍 性能优化

### 优化建议
1. **增量备份**: 默认启用，大幅减少备份时间
2. **并行处理**: 多文件同时备份
3. **缓存机制**: 减少重复读取
4. **压缩存储**: 可选启用压缩

## 📈 监控指标

监控关键指标：
- 备份成功率
- 备份时长
- 文件数量变化
- 存储空间使用
- 异常次数

---

**版本**: 1.0.0  
**最后更新**: 2026-03-16  
**兼容性**: WorkBuddy 1.0+, Obsidian 1.0+  
**许可证**: MIT