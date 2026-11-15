# Multi Search Engine

## 基本信息

- **名称**: multi-search-engine
- **版本**: v2.0.1
- **描述**: 集成17个搜索引擎（8国内+9国际），支持高级搜索语法
- **发布时间**: 2026-02-06

## 搜索引擎

**国内（8个）**: 百度、必应、360、搜狗、微信、头条、集思录
**国际（9个）**: Google、DuckDuckGo、Yahoo、Brave、Startpage、Ecosia、Qwant、WolframAlpha

## 核心功能

- 高级搜索操作符（site:, filetype:, intitle:等）
- DuckDuckGo Bangs快捷命令
- 时间筛选（小时/天/周/月/年）
- 隐私保护搜索
- WolframAlpha知识计算

## 更新记录

### v2.0.1 (2026-02-06)
- 精简文档，优化发布

### v2.0.0 (2026-02-06)
- 新增9个国际搜索引擎
- 强化深度搜索能力

### v1.0.0 (2026-02-04)
- 初始版本：8个国内搜索引擎

## 使用示例

```javascript
// Google搜索
web_fetch({"url": "https://www.google.com/search?q=python"})

// 隐私搜索
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy"})

// 站内搜索
web_fetch({"url": "https://www.google.com/search?q=site:github.com+python"})
```

MIT License

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/04-Knowledge/六大OS_SKILL审计报告]] — 六大OS·SKILL全面审计报告
- [[00-索引与导航/知识图谱/智能查询系统]] — 🔍 智能查询与推荐系�?
- [[01-核心体系/龙脑-思维模型顶层设计/NS3491F-04-三库同步指引]] — 三库同步指引
- [[09-技能库/resources_usage-examples]] — IMA 技能使用示例
- [[ψ技能体系/30-tools/multi-search-engine/SKILL]] — Multi Search Engine
- [[ψ技能体系/30-tools/multi-search-engine/references/advanced-search]] — 国内搜索引擎深度搜索指南
- [[ψ技能体系/30-tools/multi-search-engine/references/international-search]] — 国际搜索引擎深度搜索指南

<!-- AI-LINKS-END -->
