---
name: 其他AIOS组件
description: AIOS生态中不属于核心OS的外部技能分类索引——用于自动路由发现和按需加载
version: "1.0"
created: "2026-06-24"
tags:
  - 其他AIOS组件
  - 外部技能
  - 生态
  - AIOS
parent_skill: ai-os
---

# 其他AIOS组件 · 外部技能分类索引

> **核心定位**：AI龙龟共生OS生态中不属于核心OS（龙心/龙脑/龙爪/五行）的外部技能的**分类索引**。当龙心OS的场景识别器检测到非核心OS需求时，从此索引中查找匹配的外部技能进行路由。

> **总数**：~100+个外部技能（含已安装的community skills）

---

## 分类索引

### 工具执行类 (20+)

| 技能 | 路径 | 触发场景 | 自动路由条件 |
|------|------|---------|------------|
| agent-browser | `agent-browser-clawdbot/` | 浏览器自动化 | 用户说"打开网页" |
| playwright-browser | `playwright-browser-automation/` | Playwright测试 | 浏览器录制/截图 |
| clawbrowser | `clawbrowser/` | Playwright CLI | 无头浏览器 |
| browser-use | `browser-use/` | 网站交互 | 表单填写/点击 |
| web-access | `web-access/` | 联网操作 | 搜索+网页抓取 |
| web-scraper | `web-scraper/` | 网页内容提取 | 抓取结构化数据 |
| web-search-plus | `web-search-plus/` | 多引擎搜索 | 信息检索 |
| tavily | `tavily/` | AI搜索API | 研究型搜索 |
| perplexity | `perplexity/` | Perplexity搜索 | AI答案引擎 |
| multi-search-engine | `multi-search-engine/` | 16引擎搜索 | 中文搜索引擎 |
| web-search-exa | `web-search-exa/` | Exa语义搜索 | 神经搜索 |
| context7 | `context7/` | 实时文档查询 | 框架API查询 |
| imap-smtp-email | `imap-smtp-email/` | 邮件收发 | 邮件处理 |
| email-skill | `email-skill/` | 邮件自动化 | Gmail/Outlook |
| himalaya | `himalaya/` | IMAP邮件CLI | 终端邮件 |
| gmail | `gmail/` | Gmail API | Google邮件 |
| github | `github/` | GitHub CLI | PR/Issue管理 |
| trello | `trello/` | Trello API | 看板管理 |
| obsidian-cli | `obsidian-cli/` | Obsidian CLI | 笔记操作 |
| notesmd | `notesmd/` | Obsidian vault | 纯Markdown笔记 |

### 内容创作类 (15+)

| 技能 | 路径 | 触发场景 | 自动路由条件 |
|------|------|---------|------------|
| content-factory | `content-factory/` | 多格式内容生成 | 输入→多平台输出 |
| content-creator-wiki | `content-creator-wiki/` | 创作者知识库 | 选题/素材管理 |
| podcast-ops | `podcast-ops/` | 播客→内容管线 | RSS处理 |
| video-creator-ai | `video-creator-ai/` | AI视频创作 | 视频生成 |
| humanizer | `humanizer/` | 去AI味 | 文本润色 |
| fbs-bookwriter | `fbs-bookwriter/` | 写书工具 | 长文档生成 |
| minimax-docx | `minimax-docx/` | Word文档 | DOCX生成 |
| minimax-pdf | `minimax-pdf/` | PDF文档 | 高质量PDF |
| minimax-xlsx | `minimax-xlsx/` | Excel文档 | 电子表格 |
| pptx-generator | `pptx-generator/` | PPT生成 | 演示文稿 |
| md-to-pdf-cjk | `md-to-pdf-cjk/` | Markdown→PDF | 中文字体PDF |
| deck-generator | `deck-generator/` | AI插图PPT | 演示文档 |
| tencent-docs | `tencent-docs/` | 腾讯文档 | 在线文档 |
| wechat-publisher | `wechat-publisher/` | 微信公众号 | 一键发布 |
| wechat-article-pro | `wechat-article-pro/` | 深度文章 | AI写作+配图 |

### 学习研究类 (10+)

| 技能 | 路径 | 触发场景 | 自动路由条件 |
|------|------|---------|------------|
| deep-research | `deep-research/` | 深度研究 | 研究报告 |
| knowledge-framework-builder | `knowledge-framework-builder/` | 知识框架梳理 | 课程/教材分析 |
| newtype | `newtype/` | 多智能体内容 | 写作管线 |
| tutor-skills | `tutor-skills/` | PDF→学习库 | 学习材料 |
| education | `education/` | 学习计划 | 复习/考试 |
| study-planner | `study-planner/` | 备考计划 | 目标拆分 |
| notebooklm-studio | `notebooklm-studio/` | NotebookLM | 播客/报告生成 |
| knowledge-site-creator | `knowledge-site-creator/` | 知识网站 | 一句话生成 |
| material-organizer | `material-organizer/` | 资料整理 | 批量处理 |

### 安全审计类 (5)

| 技能 | 路径 |
|------|------|
| ghost-scan-code | `ghost-scan-code/` |
| ghost-scan-deps | `ghost-scan-deps/` |
| ghost-scan-secrets | `ghost-scan-secrets/` |
| skill-scanner | `skill-scanner/` |
| skills-security-check | `skills-security-check/` |

### 办公协作类 (10+)

| 技能 | 路径 | 触发场景 |
|------|------|---------|
| office-automation-pro | `office-automation-pro/` | Office自动化 |
| office-document-specialist-suite | `office-document-specialist-suite/` | 文档套件 |
| gog | `gog/` | Google Workspace |
| tencent-meeting-mcp | `tencent-meeting-mcp/` | 腾讯会议 |
| email-daily-summary | `email-daily-summary/` | 邮件摘要 |
| ima-skill | `ima-skill/` | IMA知识库 |

### 记忆系统类 (8)

| 技能 | 路径 |
|------|------|
| agent-memory-systems | `agent-memory-systems/` |
| supermemory | `supermemory/` (memory管理) |
| super-search | `super-search/` |
| super-save | `super-save/` |
| learning-archive | `学习档案/` |
| long-term-memory | `长期记忆档案/` |
| memory-compression | `记忆压缩归档/` |
| memory-visualization | `记忆可视化/` |

### 人机协同类 (5)

| 技能 | 路径 |
|------|------|
| agent-orchestrator | `agent-orchestrator/` |
| agent-swarm | `agent-swarm/` |
| agent-team-orchestration | `agent-team-orchestration/` |
| self-improving-agent | `self-improving-agent/` |
| capability-evolver | `capability-evolver/` |

### 平台集成类 (10+)

| 技能 | 路径 |
|------|------|
| api-gateway | `api-gateway/` |
| cloudflare | `cloudflare/` |
| gog | `gog/` |
| github | `github/` |
| mcp-builder | `mcp-builder/` |
| mcporter | `mcporter/` |
| prompt-engineering | `提示词工程专家/` |
| skill-builder | `skill-builder/` |
| skill-creator | `skill-creator/` |
| darwin-skill | `darwin-skill/` |
| claude-code-learning | `claude-code-learning/` |

### 未分类 (10+)

| 技能 | 路径 |
|------|------|
| healthcheck | `healthcheck/` |
| model-usage | `model-usage/` |
| cost-tracker-pro | `cost-tracker-pro/` |
| data-analyzer-pro | `data-analyzer-pro/` |
| frontend-dev | `frontend-dev/` |
| impeccable | `impeccable/` |
| ux-principles | `ux-principles/` |
| diagnose | `diagnose/` |
| hooked-ux | `hooked-ux/` |
| chat-record-skills | `chat-record-skills/` |
| personal-ai-os-framework | `personal-ai-os-framework/` |
| hermes-agent | `hermes-agent/` |

---

## 路由接入规则

1. **核心OS优先**：龙心OS先检查输入是否为五行/方法论/执行需求 → 是则路由到核心OS
2. **外部技能次之**：非核心OS需求 → 查询本索引 → 按分类匹配
3. **按需加载**：外部技能不常驻内存，调用时通过名称加载对应SKILL.md
4. **无匹配时回退**：龙心OS通用对话模式

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI智能体_01-02-技能库]] — 01-02-技能库
- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[09-技能库/Harness-Engineering/references/execution-layer]] — Harness Engineering · 执行层
- [[09-技能库/playwright-ai-agent/SKILL]] — playwright-ai-agent
- [[09-技能库/安装助手-龙龟神将/SKILL]] — Skills安装助手 - 龙龟神将
- [[ψ技能体系/30-tools/playwright-ai-agent/SKILL]] — playwright-ai-agent

<!-- AI-LINKS-END -->
