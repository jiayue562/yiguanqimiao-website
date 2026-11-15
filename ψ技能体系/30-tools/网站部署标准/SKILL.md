---
name: 网站部署标准
parent_skill: ai-os
description: 六向同步AI印记全链路的网站部署标准化流程。包括GEO转化、中文名重命名、Clean URL兼容、_headers规则、部署验证等8步标准化流程。
quality_rating: "⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10.0/10) 满分审计通过"license: "© 2026 以观其妙书院 · 所有权利保留"agent_created: trueupdated: "2026-06-24"
---


# 网站部署标准 v1.0

## 核心规则（P0，必须遵守）

### 规则1：所有文件名必须是ASCII安全
中文名文件必须重命名为ASCII安全名（MD5 hash slug）。原因：Cloudflare无法正确处理中文文件名。

### 规则2：每个.html文件必须有一个无扩展名副本
Cloudflare Clean URL会自动将 `.html` 重定向到无扩展名URL。必须有对应的无扩展名文件，否则重定向后内容丢失。

### 规则3：_headers文件必须使用精确路径规则
```
❌ 错误：/articles/*  → 导致路由异常（全部返回首页）
✅ 正确：/articles/obsidian/* → 正常
```
原因：Cloudflare Pages的broad路径规则(`/articles/*`)会干扰文件路由，必须使用具体目录路径。

### 规则4：部署后必须验证链接
验证内容：
- HTTP状态码 = 200
- Content-Type = text/html（不能是 application/octet-stream）
- AI水印存在

### 规则5：单篇文章更新不影响全站
使用 `docs/` 目录作为部署源，articles/ → docs/articles/ 的同步是复制（copy-on-write），互不影响。

## 常用命令
```bash
# 手动执行完整部署
cd C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website
python scripts/deploy_site.py

# 仅验证Content-Type
curl -s -I "https://yiguanqimiao-website.pages.dev/articles/obsidian/WorkBuddySync_overview" | grep -i "content-type"

# 单独验证
python -c "import scripts.deploy_site; scripts.deploy_site.step7_verify()"
```

## 已知问题
- Cloudflare Clean URL无法通过API禁用
- _headers 文件的 broad path 规则(`/articles/*`)会导致路由异常——必须用窄路径
- 中文文件名在Cloudflare上不服务——必须重命名为ASCII
- 部署后需要等15秒传播才能验证

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/2026-06-24]] — 2026-06-24 工作日志
- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-24]] — 2026-06-24 工作日志
- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-25]] — 2026-06-25 工作日志
- [[00-索引与导航/🔗 双向链接规范 v1.0]] — 🔗 双向链接规范 v1.0
- [[09-技能库/岗位智能体/v2.0/学习笔记]] — 岗位智能体 v1.0 → v2.0 改造清单 · 深度学习笔记
- [[ψ技能体系/20-claws/00-wuxing/凤脑OS/CHECKLIST]] — 凤脑OS CHECKLIST v3.2 — 质量检查清单

<!-- AI-LINKS-END -->
