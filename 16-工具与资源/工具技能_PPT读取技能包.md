---
title: "PPT读取技能包"
created: "2026-04-14"
version: "1.0"
tags: [PPT, 文档解析, python-pptx, 技能包, 龙心OS]
category: 工具技能
source: WorkBuddy自动备份
---

# PPT读取技能包

## 核心定义

**PPT读取技能包**是一套将PowerPoint文件转换为Markdown格式的工具集，用于将PPT内容快速提取为可编辑、可搜索的文本格式，赋能龙心OS知识管理工作流。

## 技能架构

```
PPT读取技能包
├── SKILL.md（技能定义）
├── triggers/
│   └── trigger-rules.yaml（触发规则配置）
├── test-cases.md（5个测试用例）
└── 转换脚本/
    ├── read_ppt.py（基础转换脚本）
    └── read_ppt_analysis.py（分析增强脚本）
```

## 核心功能

### 1. 基础转换
- 将PPTX文件转换为Markdown格式
- 提取幻灯片标题和内容
- 保留层级结构和格式

### 2. 分析增强
- 月度经营分析专项模板
- 数据提取与结构化
- 龙心OS深度分析接口

## 安装与使用

### 依赖安装
```bash
pip install python-pptx
```

### 基础使用
```bash
python "C:\Users\jia'yue\WorkBuddy\20260414225819\read_ppt.py"
```

### 分析增强
```bash
python "C:\Users\jia'yue\WorkBuddy\20260414225819\read_ppt_analysis.py"
```

## 触发关键词

| 优先级 | 关键词 |
|--------|--------|
| P0 | 读取PPT、PPT转换、解析PPT、安装PPT技能 |
| P1 | 分析PPT、查看PPT内容、月度经营分析 |

## 技能路径

```
C:\Users\jia'yue\.workbuddy\skills\PPT读取\
```

## 关联文件

- [[01-思维模型体系/易经错综复杂·卦变思维决策法]]（思维模型体系）
- [[龙心OS知识管理工作流]]（工作流整合）

## 核心金句

> "PPT不是终点，是起点——提取内容，赋能龙心OS，让每一页幻灯片都成为可进化的知识资产。"

## 版权信息

© 2026 观其妙书院 | 以文载道，赋能超级个体

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[20-工作记录与复盘/journal_2026-04-14_每日备份报告]] — 2026-04-14 Obsidian备份执行报告
- [[09-技能库/PPT读取/SKILL]] — PPT读取 · 文档转换Skill
- [[09-技能库/PPT读取/test-cases]] — PPT读取 Skill 测试用例
- [[09-技能库/ima-skill/notes/references/api]] — IMA笔记 API
- [[09-技能库/ima-skills/ima-skill/notes/references/api]] — IMA笔记 API
- [[09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/notes/references/api]] — IMA笔记 API
- [[09-技能库/markitdown/SKILL]] — Markitdown 技能
- [[09-技能库/ppt-generator/SKILL]] — ppt-generator - PPT智能生成
- [[09-技能库/wechat-articles/SKILL]] — 微信公众号文章搜索技能
- [[09-技能库/学习能力系统/references/九指令实现]] — 9条指令完整实现

<!-- AI-LINKS-END -->
