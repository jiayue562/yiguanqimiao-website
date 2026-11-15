---
name: wechat-article-spider
parent_skill: ai-os
version: 1.0.0
description: 微信公众号文章爬虫 - 将微信公号文章转换为 Markdown + 本地图片
---

# wechat-article-spider

微信公众号文章爬虫 - 将微信公号文章转换为 Markdown + 本地图片

## 执行指令

```bash
cd scripts && pip install -r requirements.txt && python main.py
```

## 功能

- ✅ 输入微信公号文章 URL
- ✅ 自动抓取文章内容
- ✅ 下载所有图片到 `images/` 文件夹
- ✅ 生成 Markdown 文件，图片使用相对路径引用

## 安装

```bash
cd wechat-article-dl/scripts
pip install -r requirements.txt
```

## 用法

### 命令行

```bash
python main.py <文章 URL> [输出目录]
```

### 示例

```bash
# 下载到当前目录
python main.py https://mp.weixin.qq.com/s/xxxxx

# 指定输出目录
python main.py https://mp.weixin.qq.com/s/xxxxx ./my-articles
```

### 输出结构

```
output/
├── 文章标题.md
└── images/
    ├── img_001_xxx.jpg
    ├── img_002_xxx.png
    └── ...
```

## 注意事项

- 微信文章可能有反爬机制，如遇失败可稍后重试
- 部分动态加载的图片可能无法获取
- 图片文件名使用哈希值避免重复

## 依赖

- requests
- beautifulsoup4
- lxml

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/agents_Skill 构建 SOP]] — Skill 构建 SOP - 龙心 OS 技能开发标准流程
- [[09-技能库/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[09-技能库/ima-skills/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/example]] — wechat-publisher 测试文章
- [[ψ技能体系/20-claws/03-academy/wechat-publisher/references/troubleshooting]] — 故障排查指南

<!-- AI-LINKS-END -->
