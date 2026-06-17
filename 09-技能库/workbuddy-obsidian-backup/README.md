# WorkBuddy → Obsidian 备份技能

## 🎯 简介

本技能提供将WorkBuddy系统所有内容备份到Obsidian知识库的完整解决方案，实现知识资产的系统化沉淀和管理。

## ✨ 核心功能

### 1. 全量备份
- 备份WorkBuddy所有知识资产
- 包括系统配置、技能库、记忆系统、对话记录等

### 2. 智能分类
- 基于文件内容和元数据自动分类
- 按文件类型、命名模式、内容关键词分类

### 3. 增量备份
- 只备份新增或修改的内容
- 大幅减少备份时间和存储空间

### 4. 自动化管理
- 支持定时自动备份
- 备份报告生成
- 历史版本管理

## 📁 安装和使用

### 快速开始

```bash
# 1. 进入技能目录
cd "c:/Users/jia'yue/.workbuddy/skills/workbuddy-obsidian-backup"

# 2. 创建配置文件
copy config_template.json workbuddy_backup_config.json

# 3. 编辑配置文件（可选）
# 修改Obsidian路径等设置

# 4. 运行备份
python backup_script.py --config workbuddy_backup_config.json
```

### 常用命令

```bash
# 全量备份（首次使用推荐）
python backup_script.py --full-backup

# 增量备份（日常使用）
python backup_script.py

# 指定Obsidian路径
python backup_script.py --obsidian-path "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\"

# 模拟运行（不实际备份）
python backup_script.py --dry-run

# 调试模式
python backup_script.py --debug
```

## 🔧 配置说明

### 主要配置项

1. **workbuddy_path**: WorkBuddy安装路径
2. **obsidian_vault_path**: Obsidian知识库路径
3. **backup_targets**: 备份目标配置
4. **backup_options**: 备份选项
5. **classification_rules**: 文件分类规则

### 备份目标

默认备份以下内容：
- ✅ 系统配置文件（TOOLS.md, USER.md等）
- ✅ 技能库（所有skills目录）
- ✅ 记忆系统（brain目录）
- ✅ 项目文件（Claw等项目）
- ✅ 自动化配置（automations目录）

## 📊 备份目录结构

在Obsidian中创建的目录结构：

```
WorkBuddy知识备份体系/
├── 00-系统配置/          # 系统配置文件
├── 01-技能库/           # 所有技能文件
├── 02-记忆系统/         # 记忆和会话记录
├── 03-对话记录/         # 对话历史（按时间归档）
├── 04-知识沉淀/         # 核心知识资产
├── 05-工作流/           # 工作流文档
├── 06-项目文件/         # 项目相关文件
└── 备份日志/            # 备份记录和报告
```

## ⚙️ 自动化配置

### 设置每日自动备份

```toml
# 在.workbuddy/automations/workbuddy-backup/automation.toml中配置
name = "WorkBuddy每日备份到Obsidian"
prompt = "执行WorkBuddy到Obsidian的增量备份"
rrule = "FREQ=DAILY;BYHOUR=23;BYMINUTE=30"
cwds = ["C:\\Users\\jia'yue\\.workbuddy\\skills\\workbuddy-obsidian-backup"]
status = "ACTIVE"
```

### 手动触发备份

在WorkBuddy对话中：
```
使用 "workbuddy-obsidian-backup" 技能执行备份
```

## 📈 监控和报告

### 备份报告示例

每次备份后生成详细报告：

```markdown
# 📊 WorkBuddy → Obsidian 备份报告

## 备份统计
| 类别 | 文件数 | 大小 | 新增 | 修改 | 失败 |
|------|--------|------|------|------|------|
| 系统配置 | 6 | 45KB | 1 | 2 | 0 |
| 技能库 | 57 | 2.3MB | 3 | 5 | 0 |
| 记忆系统 | 23 | 890KB | 12 | 3 | 0 |
| 项目文件 | 15 | 1.1MB | 15 | 0 | 0 |
| **总计** | **101** | **4.3MB** | **31** | **10** | **0** |
```

## 🔍 故障排除

### 常见问题

1. **权限问题**
   ```
   错误: 无法写入Obsidian目录
   解决: 检查目录权限，确保有写入权限
   ```

2. **路径问题**
   ```
   错误: 路径包含特殊字符
   解决: 在配置文件中使用双反斜杠或原始字符串
   ```

3. **文件锁定**
   ```
   错误: 文件被其他程序占用
   解决: 关闭占用文件的程序，或跳过该文件
   ```

### 调试模式

```bash
python backup_script.py --debug --dry-run
```

## 🔄 恢复备份

### 从Obsidian恢复文件

```bash
# 恢复单个文件
copy "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\WorkBuddy知识备份体系\系统配置\TOOLS.md" "C:\Users\jia'yue\.workbuddy\TOOLS.md"

# 恢复整个目录
xcopy "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\WorkBuddy知识备份体系\技能库\*" "C:\Users\jia'yue\.workbuddy\skills\" /E /I
```

## 📝 最佳实践

### 备份策略

1. **首次使用**: 执行全量备份
2. **日常使用**: 设置每日增量备份
3. **定期检查**: 每月检查备份完整性
4. **版本管理**: 保留30天备份历史

### 存储优化

1. 启用增量备份减少存储空间
2. 定期清理旧备份
3. 压缩历史备份（可选）

### 安全建议

1. 定期验证备份完整性
2. 保持多个备份副本
3. 加密敏感信息备份

## 📞 技术支持

### 获取帮助

1. **查看日志**: `备份日志/问题记录.md`
2. **检查配置**: 验证配置文件路径
3. **查看报告**: 分析备份报告中的问题

### 报告问题

在WorkBuddy对话中：
```
报告 "workbuddy-obsidian-backup" 技能问题
```

## 🔄 更新和维护

### 更新技能

```bash
# 从GitHub更新（未来版本）
git pull origin main

# 或重新安装
npx skills add <owner/repo@workbuddy-obsidian-backup>
```

### 维护任务

1. 每月检查备份完整性
2. 每季度更新分类规则
3. 每年评估备份策略

## 📄 许可证

MIT License

## 🎯 版本历史

- **v1.0.0** (2026-03-16): 初始版本
  - 基础备份功能
  - 智能文件分类
  - 增量备份支持
  - 自动化配置

---

**祝您备份顺利，知识沉淀有序！** 🚀