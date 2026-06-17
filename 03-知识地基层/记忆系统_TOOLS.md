---
title: "TOOLS.md - 可用工具与技能"
created: "2026-03-19"
version: "1.0"
tags: [记忆系统, 工具, 技能]
---

# TOOLS.md - 可用工具与技能

## 🎯 技能系统架构

### 龙心OS 五大引擎

| 引擎 | 名称 | 功能 | 触发关键词 |
|------|------|------|-----------|
| 🐉 象思维 | 心 | 0→1 直觉洞察，原创突破 | 象思维、0→1、原创 |
| 📚 知识学习 | 脑 | 十项认知指令，知识重构 | 深度学习、剖析、解构 |
| 🌈 五色光思维 | 眼 | 五色分治，同频共振 | 五色光、白光、红光 |
| 🤝 人机协同四象限 | 手 | 四象限分工，最优协作 | 人机协同、四象限 |
| 🔄 知行合一 | 血 | 表示空间→压缩→泛化 | 知行沉淀、总结 |

### 专业技能包

#### 1. AI 开发类
- **adaptive-subagents**: 子任务智能调度
- **agent-orchestrator**: 多智能体协调规划
- **agent-memory-systems**: 记忆系统架构
- **self-improving-agent**: 自我进化引擎

#### 2. 知识管理类
- **obsidian**: Obsidian 知识库管理（通过 obsidian-cli）
- **ima-skills**: IMA 笔记管理（需要 API Key 配置）
- **notesmd**: Obsidian 命令行操作
- **workbuddy-obsidian-backup**: 定时备份到 Obsidian

#### 3. 安全审计类
- **ghost-scan-code**: SAST 代码安全扫描
- **ghost-scan-deps**: SCA 依赖漏洞扫描
- **ghost-scan-secrets**: 密钥/凭证泄露扫描

#### 4. 思维模型类
- **五色光思维**: 结构化同频思考决策系统
- **象思维**: 0→1 原创突破引擎
- **zhi-shi-xue-xi**: 十项认知指令深度学习

#### 5. 自动化运营类
- **office-automation-pro**: Office 文档自动化
- **workflow-designer-pro**: 工作流设计
- **browser-automation**: 浏览器自动化

#### 6. 文档处理类
- **pdf**: PDF 读取/编辑/合并/OCR
- **docx**: Word 文档创建/编辑
- **pptx**: PPT 幻灯片制作

#### 7. 学习与搜索类
- **self-learning**: 自主学习新技能
- **web-search-plus**: 智能搜索路由
- **super-search**: 搜索历史记忆

## 🔧 工具配置

### 环境变量配置

#### IMA 笔记系统
```powershell
$env:IMA_OPENAPI_CLIENTID = "59a1edb848ec905552c0fbc8041213bf"
$env:IMA_OPENAPI_APIKEY = "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A=="
```

### MCP 配置

#### 已配置的 MCP 服务器
- **暂无**（如有需要可配置）

## 📂 技能文件位置

### 用户级技能
```
C:\Users\jia'yue\.workbuddy\skills\
```

### 项目级技能
```
C:\Users\jia'yue\WorkBuddy\20260319115639\.workbuddy\skills\
```

## 🔄 技能同步状态

| 技能名称 | 状态 | 最后更新 |
|---------|------|---------|
| 龙心OS | ✅ 已安装 | 2026-03-19 |
| 人机协同四象限 | ✅ 已安装 v2.1 | 2026-03-19 |
| 五色光思维 | ✅ 已安装 v1.0 | 2026-03-19 |
| 象思维 | ✅ 已安装 v1.0 | 2026-03-19 |
| 知识学习 Skills | ✅ 已安装 | 2026-03-19 |
| obsidian | ✅ 已安装 | 2026-03-19 |
| ima-skills | ✅ 已配置 | 2026-03-19 |
| 知行合一自我进化 | ✅ 已安装 | 2026-03-19 |

## 🛠️ 可用命令

### Obsidian 操作
```powershell
obsidian-cli search "query"              # 搜索笔记
obsidian-cli search-content "query"      # 全文搜索
obsidian-cli create "Folder/New note"    # 创建笔记
obsidian-cli move "old" "new"            # 移动/重命名
obsidian-cli delete "path/note"          # 删除笔记
```

### IMA 操作
- 搜索笔记
- 浏览笔记本
- 读取笔记内容
- 创建新笔记
- 追加内容

### 自动化操作
- 定时备份（每日 23:30）
- 自动归档对话
- 知行合一沉淀

## 📋 技能调用规则

### 自动触发条件

| 关键词 | 技能 | 场景 |
|-------|------|------|
| 象思维、0→1、原创 | 象思维 | 创新突破 |
| 五色光、白光、红光 | 五色光思维 | 分析决策 |
| 人机协同、四象限 | 人机协同四象限 | 任务分工 |
| 深度学习、剖析 | 知识学习 | 学习理解 |
| 笔记、备忘录 | ima-skills | 笔记管理 |
| Obsidian、库 | obsidian | 知识库 |

### 手动调用方式

直接说出需求，龙心OS 会自动识别场景并调度合适的引擎。

## 🔗 关联文档

- `[[SOUL.md]]` - 龙龟神将身份与长期记忆
- `[[USER.md]]` - 用户偏好与习惯
- `[[SESSION.md]]` - 当前会话上下文
- `[[MEMORY.md]]` - 记忆系统架构

---

**文档版本**: 1.0
**最后更新**: 2026-03-19
**维护者**: 龙龟神将
