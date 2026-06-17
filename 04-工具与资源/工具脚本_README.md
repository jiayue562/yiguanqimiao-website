---
title: "验证工具目录"
type: index
tags: [工具, 验证, 脚本]
created: 2026-03-19
version: 1.0
---

# 📂 验证工具目录

> 知识库验证和管理工具集合

---

## 🛠️ 工具列表

| 工具 | 功能 | 状态 |
|------|------|------|
| [link_validator.py](link_validator.py) | 双向链接验证 | ✅ 可用 |
| [incremental_backup.py](incremental_backup.py) | 增量备份工具 | ✅ 可用 |
| [smart_classifier.py](smart_classifier.py) | 智能文件分类 | ✅ 可用 |

---

## 🚀 使用方法

### 1. 链接验证工具

```powershell
python link_validator.py
```

功能：
- 检测破损链接
- 统计链接密度
- 生成链接报告

### 2. 增量备份工具

```powershell
# 执行备份
python incremental_backup.py backup

# 列出备份历史
python incremental_backup.py list

# 恢复备份
python incremental_backup.py restore

# 恢复指定日期
python incremental_backup.py restore --date 20260319_143000
```

功能：
- 文件哈希比对
- 只备份变更文件
- 支持版本回滚

### 3. 智能文件分类

```powershell
python smart_classifier.py
```

功能：
- 按扩展名分类
- 按文件名模式分类
- 按内容关键词分类
- 生成统计报告

---

## 📋 输出文件

运行工具后会在 `00-索引与导航/` 目录下生成：
- `🔍 链接验证报告.md` - 链接完整性报告
- `📈 文件分类统计.md` - 文件分类统计报告

备份文件保存在 `备份/` 目录

---

## 🔗 关联文档

- [[📚 知识库总索引]]
- [[📋 文档标准化模板]]
- [[🔗 双向链接规范]]

---

*最后更新: 2026-03-19*
