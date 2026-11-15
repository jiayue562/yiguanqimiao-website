---
title: "context7 - 实时文档查询"
created: "2026-03-27"
tags: [context7, documentation, realtime, api]
version: "1.0"
---

# context7 - 实时文档查询 Skills

## 功能定位

**L2层·知识学习引擎扩展** - 提供实时文档和框架API查询能力，与龙心OS的📚知识学习引擎深度整合。

## 核心能力

1. **实时文档查询**
   - 查询最新框架/库的官方文档
   - 支持版本指定（如 `langchain@v0.2`）
   - 返回结构化信息而非原始网页

2. **API示例获取**
   - 提取代码示例
   - 提供多语言支持
   - 智能选择最佳实践

3. **框架对比分析**
   - 对比不同框架的API差异
   - 识别版本迁移路径
   - 规避已知问题

## 使用场景

- 学习新框架时快速获取官方文档
- 调试时需要最新API信息
- 确认某个函数/方法的正确用法
- 版本升级前的兼容性检查

## 调用方式

```
当需要查询某个框架/库的实时文档时，自动调用此Skills。
支持：React、Vue、LangChain、OpenAI、Anthropic等主流框架。
```

## MCP配置

如需启用MCP方式，添加配置：
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp"]
    }
  }
}
```

## 龙心OS整合

- 与📚知识学习引擎协同：学习新知识时自动查询最新文档
- 与🐉象思维协同：0→1创新时验证技术可行性
- 与🔄知行合一协同：沉淀技术洞察

---

**版本**: 1.0 | **维护者**: 龙龟神将 | **更新**: 2026-03-27

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/知识图谱/智能查询系统]] — 🔍 智能查询与推荐系�?
- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[09-技能库/rag-skill/SKILL]] — rag-skill - 知识库RAG增强
- [[10-系统配置/同步报告_20260515]] — 三向同步报告
- [[ψ技能体系/30-tools/context7/SKILL]] — context7 - 实时文档查询 Skills v1.1
- [[ψ技能体系/30-tools/deep-research/agents/web-search-modules/general-web]] — General Web Module

<!-- AI-LINKS-END -->
