---
title: wechat-publisher 测试文章
cover: ./assets/default-cover.jpg
---

# wechat-publisher Skill 测试

欢迎使用 **wechat-publisher** skill！

## 核心功能

### 1. Markdown 自动转换
- 标准 Markdown 转换为微信公众号格式
- 自动处理样式和排版
- 支持多种主题

### 2. 图片自动上传
- 本地图片自动上传
- 网络图片自动处理
- 无需手动操作

### 3. 一键发布
```bash
./scripts/publish.sh example.md
```

## 代码示例

```python
def publish_article(file):
    """发布到微信公众号"""
    return wenyan.publish(file)
```

## 使用步骤

1. 配置凭证（TOOLS.md）
2. 准备 Markdown 文件
3. 运行发布脚本

## 封面图说明

本测试文章使用相对路径引用封面：
```markdown
cover: ./assets/default-cover.jpg
```

这样发布到 GitHub 后，其他用户克隆 skill 也能直接使用！

## 测试总结

如果看到这篇文章，说明 skill 工作正常！

---

*由 wechat-publisher 自动发布*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-25]] — 2026-06-25 工作日志
- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[20-工作记录与复盘/02-每日日志/2026-04-15]] — 2026-04-15 日志
- [[09-技能库/wechat-articles/SKILL]] — 微信公众号文章搜索技能
- [[ψ技能体系/20-claws/03-academy/SKILL]] — 以观其妙书院龙爪
- [[ψ技能体系/20-claws/03-academy/wechat-article-pro/SKILL]] — 微信公众平台文章发布 Skill (专业版)
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/README]] — wechat-publisher
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/SKILL]] — wechat-publisher
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/references/themes]] — wenyan-cli 主题列表
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/references/troubleshooting]] — 故障排查指南

<!-- AI-LINKS-END -->
