---
name: workbuddy-tri-sync
description: "WorkBuddy三向同步技能：将WorkBuddy所有内容备份到Obsidian知识库和IMA观其妙书院（悟空）知识库，实现知识资产的完整沉淀。"
homepage: https://www.codebuddy.cn/docs/workbuddy/Overview
metadata: {
  "category": "backup",
  "version": "2.0",
  "requires": {
    "obsidian_vault": "D:\\以观其妙书院知识库\\观其妙书院",
    "ima_notebook": "观其妙书院（悟空）"
  },
  "features": ["obsidian_backup", "ima_sync", "tri_sync", "auto_backup"]
}
---

# WorkBuddy 三向同步技能 v2.0

## 🎯 功能概述

本技能实现 **WorkBuddy ↔ Obsidian ↔ IMA** 三向同步，将WorkBuddy系统中的所有知识资产完整备份到：

1. **Obsidian知识库**（本地）- `D:\以观其妙书院知识库\观其妙书院`
2. **IMA知识库**（云端）- `观其妙书院（悟空）`

实现知识资产的三重保障和跨平台访问。

---

## 📁 同步目录结构

### Obsidian 备份结构

```
D:\以观其妙书院知识库\观其妙书院\
├── WorkBuddy知识备份体系/           # 主备份目录
│   ├── 00-系统配置/                 # 系统配置文件
│   │   ├── TOOLS.md
│   │   ├── USER.md
│   │   ├── SOUL.md
│   │   ├── SESSION.md
│   │   └── mcp.json
│   │
│   ├── 01-技能库/                   # 所有Skills
│   │   ├── 龙心OS/
│   │   ├── 象思维/
│   │   ├── 五色光思维/
│   │   ├── 五行人格心理学/
│   │   ├── 知识学习Skills/
│   │   ├── 知行合一/
│   │   ├── 人机协同五象限/
│   │   ├── workbuddy-obsidian-backup/
│   │   └── ... (其他所有技能)
│   │
│   ├── 02-记忆系统/                 # 记忆文件
│   │   ├── MEMORY.md
│   │   ├── 2026-04-09.md
│   │   └── ... (每日日志)
│   │
│   ├── 03-对话记录/                 # 对话历史
│   │   ├── 2026-04/
│   │   │   ├── 2026-04-09-任务1.md
│   │   │   └── ...
│   │   └── 对话关系图谱.md
│   │
│   ├── 04-知识沉淀/                 # 核心知识
│   │   ├── 思维模型/
│   │   ├── 五行人格心理学/
│   │   ├── 五色光思维/
│   │   ├── 象思维/
│   │   ├── 企业文化/
│   │   ├── AI技术应用/
│   │   └── 龙龟神将进化/
│   │
│   ├── 05-工作流/                   # 自动化配置
│   │   ├── 自动化任务/
│   │   ├── 日常巡检/
│   │   └── 优化建议/
│   │
│   ├── 06-项目文件/                 # 项目文档
│   │   └── Claw项目/
│   │
│   └── 同步日志/                    # 同步记录
│       ├── 备份统计.md
│       ├── 备份报告_2026-04-09.md
│       └── 问题记录.md
```

### IMA 备份结构

```
观其妙书院（悟空）知识库/
├── 🏠 核心身份与关系
│   ├── SOUL.md - 龙龟神将核心身份
│   ├── USER.md - 悟空用户画像
│   └── 木火共生关系.md
│
├── 🧠 记忆系统
│   ├── MEMORY.md - 长期记忆档案
│   └── 每日日志/
│       ├── 2026-04-09.md
│       └── ...
│
├── 🛠️ 技能库索引
│   ├── 技能总览.md
│   └── 技能分类目录.md
│
├── 📚 知识沉淀
│   ├── 思维模型库/
│   ├── 五行人格心理学/
│   ├── 五色光思维/
│   └── 象思维/
│
└── 🔄 同步记录
    └── 三向同步报告.md
```

---

## 🚀 使用方法

### 方法1: 手动执行三向同步

```bash
# 执行完整三向同步
python tri_sync.py

# 或执行增量同步
python simple_incremental_backup.py

# 或使用批处理文件
run_backup.bat
```

### 方法2: 自动定时同步

已配置每日自动同步：
- **时间**: 每天 23:30
- **模式**: 增量备份（仅同步变更内容）
- **范围**: WorkBuddy → Obsidian → IMA

### 方法3: 对话中触发

在WorkBuddy对话中，可以直接说：
- "执行三向同步"
- "备份到Obsidian和IMA"
- "同步知识库"

---

## ⚙️ 配置说明

### 配置文件位置
`C:\Users\jia'yue\.workbuddy\skills\workbuddy-obsidian-backup\config.json`

### 关键配置项

```json
{
  "workbuddy_path": "C:\\Users\\jia'yue\\.workbuddy",
  "obsidian_vault_path": "D:\\以观其妙书院知识库\\观其妙书院",
  
  "ima_config": {
    "client_id": "87e4c9978e1b50b3918e20313b7084ed",
    "api_key": "s/hxYqVaGQocwxhbaelqwbfywl6/1scRfZrisQ/zjAmP+wKJ0mciHHQa9SMv7T/qFJT9zRxROA==",
    "base_url": "https://ima.qq.com",
    "notebook_name": "观其妙书院（悟空）"
  },
  
  "backup_options": {
    "incremental_backup": true,
    "preserve_timestamps": true,
    "create_backup_log": true,
    "backup_schedule": "daily",
    "backup_time": "23:30",
    "sync_to_ima": true
  }
}
```

---

## 📊 同步报告示例

每次同步完成后自动生成报告：

```markdown
# 🔄 三向同步报告

## 同步时间
2026-04-09 10:45:00

## 同步统计

| 目标 | 同步文件数 | 状态 |
|------|-----------|------|
| Obsidian | 156 | ✅ 成功 |
| IMA | 12 | ✅ 成功 |

## 同步内容详情

### WorkBuddy → Obsidian
- 技能库: 45个Skills
- 记忆系统: 23个文件
- 对话记录: 15个会话
- 系统配置: 6个文件

### WorkBuddy → IMA
- 核心记忆: 4个文件
- 知识沉淀: 8个文档

## 下次同步
预计时间: 2026-04-09 23:30

---
*自动生成 by 龙龟神将*
```

---

## 🔒 安全保护

### 排除的敏感文件
- `*.env` - 环境变量文件
- `*.key` - 密钥文件
- `password*` - 密码相关
- `secret*` - 机密信息
- `node_modules/` - 依赖目录
- `__pycache__/` - Python缓存

### 备份验证
- 文件完整性校验（SHA256）
- 备份后自动验证
- 异常自动重试

---

## 🛠️ 故障排除

### 常见问题

1. **IMA同步失败**
   - 检查Client ID和API Key是否正确
   - 确认网络连接正常
   - 检查IMA服务状态

2. **Obsidian路径错误**
   - 确认Obsidian知识库路径存在
   - 检查目录写入权限
   - 验证路径格式（Windows使用双反斜杠）

3. **文件冲突**
   - 系统会自动保留最新版本
   - 冲突文件会记录在同步日志中

### 调试模式
```bash
python tri_sync.py --debug --dry-run
```

---

## 📈 监控指标

- 备份成功率
- 同步文件数量
- 存储空间使用
- 同步耗时
- 异常次数

---

## 🔄 版本历史

### v2.0 (2026-04-09)
- ✅ 更新IMA凭证配置
- ✅ 完善三向同步功能
- ✅ 优化分类存储逻辑
- ✅ 增强错误处理

### v1.0 (2026-03-16)
- ✅ 初始版本发布
- ✅ 支持WorkBuddy → Obsidian备份
- ✅ 基础分类存储

---

**版本**: 2.0  
**最后更新**: 2026-04-09  
**维护者**: 龙龟神将  
**状态**: ✅ 生产就绪
