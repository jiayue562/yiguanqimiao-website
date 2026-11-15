---
title: "BOOTSTRAP.md - 启动配置"
created: "2026-03-19"
version: "1.0"
tags: [记忆系统, 启动, 配置]
---

# BOOTSTRAP.md - 启动配置

## 🚀 系统启动流程

### 启动阶段

#### 1. 初始化阶段
```
加载用户配置 → 加载记忆系统 → 加载技能包 → 准备就绪
```

#### 2. 检查清单
- [x] Obsidian 知识库可访问
- [x] IMA 笔记服务已配置
- [x] 五大引擎已加载
- [x] 四层记忆系统已就绪
- [x] 工作目录已设置

### 启动参数

#### 环境配置
```powershell
工作目录: C:\Users\jia'yue\WorkBuddy\20260319115639
Obsidian库: C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院
技能目录: C:\Users\jia'yue\.workbuddy\skills
```

#### 凭证状态
- **IMA Client ID**: ✅ 已配置
- **IMA API Key**: ✅ 已配置
- **环境变量**: ✅ 已设置

## ⚙️ 核心配置

### 龙心OS 配置
```yaml
version: "1.1"
engine:
  - 象思维
  - 知识学习
  - 五色光思维
  - 人机协同四象限
  - 知行合一自我进化
auto_trigger: true
memory_sync: true
```

### 记忆系统配置
```yaml
layers:
  - SOUL.md (核心身份)
  - USER.md (用户偏好)
  - TOOLS.md (工具技能)
  - SESSION.md (会话上下文)
sync:
  - WorkBuddy
  - Obsidian
  - IMA
```

## 📋 首次启动检查

### 必需文件
- [x] SOUL.md - 核心身份
- [x] USER.md - 用户偏好
- [x] TOOLS.md - 工具列表
- [x] SESSION.md - 会话上下文
- [x] MEMORY.md - 记忆架构
- [x] AGENTS.md - 智能体配置
- [x] BOOTSTRAP.md - 启动配置
- [x] HEARTBEAT.md - 心跳监控
- [x] IDENTITY.md - 身份认证

### 必需技能
- [x] 龙心OS
- [x] obsidian
- [x] ima-skills
- [x] 人机协同四象限
- [x] 五色光思维
- [x] 象思维
- [x] 知识学习

## 🔄 初始化脚本

### 自动初始化
```powershell
# 1. 加载用户配置
# 2. 同步 Obsidian 知识库
# 3. 同步 IMA 笔记
# 4. 加载当前会话状态
# 5. 准备就绪
```

### 手动初始化命令
```powershell
# 刷新知识库
obsidian-cli refresh

# 同步笔记
ima sync

# 重载技能
skill reload
```

## 🎯 启动模式

### 标准模式
- 完整加载五大引擎
- 启用所有记忆层
- 开启自动触发

### 轻量模式
- 仅加载核心技能
- 仅启用工作记忆
- 手动触发为主

### 调试模式
- 加载所有诊断工具
- 详细日志输出
- 单步执行

---

**文档版本**: 1.0
**最后更新**: 2026-03-19

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[03-知识地基层/记忆系统_AGENTS]] — AGENTS.md - 智能体配置
- [[03-知识地基层/记忆系统_ERRORS]] — ERRORS.md - 错误记录与规避
- [[03-知识地基层/记忆系统_HEARTBEAT]] — HEARTBEAT.md - 心跳监控与任务管理
- [[03-知识地基层/记忆系统_MEMORY]] — MEMORY.md - 记忆系统架构 v2.1
- [[03-知识地基层/记忆系统_MEMORY_WorkBuddy]] — MEMORY.md - 龙龟神将长期记忆（WorkBuddy工作记忆）
- [[03-知识地基层/记忆系统_SESSION]] — SESSION.md - 会话上下文
- [[03-知识地基层/记忆系统_TOOLS]] — TOOLS.md - 可用工具与技能
- [[03-知识地基层/记忆系统_记忆系统安装完成报告-v3.0]] — 记忆系统安装完成报告 v3.0
- [[20-工作记录与复盘/_从根目录迁入/日签/本周回顾]] — 本周回顾
- [[20-工作记录与复盘/journal_2026-03-11]] — 2026-03-11 对话

<!-- AI-LINKS-END -->
