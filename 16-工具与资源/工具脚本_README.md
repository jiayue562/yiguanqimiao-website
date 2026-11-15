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

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/知识图谱/link-validation_20260520_130624]] — 链接验证报告
- [[00-索引与导航/🏛️ 知识库体系建设完整方案 v3.0]] — 🏛️ 以观其妙书院知识库体系建设完整方案 v3.0
- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[02-信仰文化体系/项目实践_02-02-已完成项目]] — 02-02-已完成项目
- [[16-工具与资源/工具脚本_使用说明]] — 📚 知识库验证系统 - 使用说明
- [[16-工具与资源/工具脚本_知识库验证系统]] — 🤖 知识库验证系统
- [[20-工作记录与复盘/_从根目录迁入/日签/三库同步状态]] — 三库同步状态
- [[09-技能库/腾讯文档/references/unsupported_feature_reporting]] — 不支持能力上报规范（report_unsupported_feature）
- [[_vault_config]] — Vault 配置
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/lint-config]] — Linting 配置

<!-- AI-LINKS-END -->
