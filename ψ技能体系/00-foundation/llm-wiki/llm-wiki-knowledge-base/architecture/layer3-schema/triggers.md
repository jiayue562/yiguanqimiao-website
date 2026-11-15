# 触发规则

> 龙心 OS · LLM Wiki Schema 配置层

---

## 自动触发

| 事件 | 动作 | 优先级 |
|------|------|--------|
| 新资料录入 archive | 自动编译 → 提取→生成→链接 | P0 |
| 新页面创建 | 自动扫描并推荐链接 | P1 |
| 定时健康检查 | 每日凌晨运行 lint | P2 |
| 孤立页面检测 | 自动通知建立链接 | P1 |

## 手动触发

| 用户意图 | 动作 |
|---------|------|
| "编译这篇文档到 Wiki" | ingest_document() |
| "查询/搜索 XX 知识" | query_by_name/search_keyword() |
| "检查 Wiki 健康状态" | check_wiki_health() |
| "重建索引" | rebuild_index() |
| "查看 XX 的关联网络" | query_related() |

## 协同触发

| 来源 Skill | 动作 | 说明 |
|-----------|------|------|
| self-learning 学习完成 | 自动 Ingest | 新知识 → Wiki |
| agent-memory 归档 | 同步更新索引 | 保证索引最新 |
| super-save 保存 | 记录到记忆系统 | 经验 → 语义记忆 |

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[01-核心体系/agents_LLM Wiki 知识库激活完成报告]] — LLM Wiki 知识库激活完成报告
- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[03-知识地基层/五色光思维/NSA05D4-96-Skill 封装完成报告]] — 五色光思维 Skill 封装完成报告
- [[03-知识地基层/记忆系统_HEARTBEAT]] — HEARTBEAT.md - 心跳监控与任务管理
- [[03-知识地基层/象思维/NS6EED6-98-Skill 封装完成报告]] — 象思维 Skill 封装完成报告
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer3-schema/lint-config]] — Linting 配置
- [[ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/reference/practice-guide]] — LLM Wiki 实操指南

<!-- AI-LINKS-END -->
