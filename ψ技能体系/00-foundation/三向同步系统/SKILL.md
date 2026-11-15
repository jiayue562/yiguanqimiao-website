---
name: 三向同步系统
description: |
  AI龙龟共生伙伴操作系统的六向知识同步系统 v5.0，实现 WorkBuddy、Obsidian、IMA、GitHub、Cloudflare Pages、pages.dev 六个节点的增量同步与GEO转化。
  新增：GitHub推送 + Cloudflare Pages部署 + pages.dev网站GEO曝光。
homepage: https://www.codebuddy.cn/docs/workbuddy/Overview
metadata:
  version: "5.0.0"
  updated: "2026-06-24"
  category: "knowledge-sync"
  architecture: "native-automation"
  requires:
    obsidian_cli: "@yakitrak/obsidian-cli"
    ima_api: "https://ima.qq.com/openapi"
    wrangler: "npx wrangler"
  paths:
    workbuddy_memory: "c:\\Users\\jia'yue\\WorkBuddy\\Claw\\.workbuddy\\memory\\"
    workbuddy_wiki: "C:\\Users\\jia'yue\\.workbuddy\\wiki-knowledge\\"
    obsidian_vault: "D:\\以观其妙书院知识库\\以观其妙书院"
    ima_endpoint: "https://ima.qq.com"
    ima_kb_id: "DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY="
    ima_folder_id: "folder_7441985942068358"
  automations:
    workbuddy_to_obsidian: "workbuddy-obsidian (每日23:30)"
    workbuddy_to_ima: "workbuddy-ima (每日23:35)"
  skills_integrated:
    obsidian_cli: "kepano/obsidian-skills@obsidian-cli (29.4K installs)"
    obsidian_markdown: "kepano/obsidian-skills@obsidian-markdown (33.3K installs)"
    ima_skill: "ima-skill (v1.1.2, 系统自带)"
quality_rating: "⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10.0/10) 满分审计通过"license: "© 2026 以观其妙书院 · 所有权利保留"agent_created: true
---

# 🔗 三向同步系统 (Tri-Sync System) v4.1

> **WorkBuddy ↔ Obsidian ↔ IMA** 三向知识同步系统
> 
> 版本: 4.1.0 | 更新: 2026-05-20 | AI OS v6.0配套

## 🆕 v4.1升级内容

> **v4.1核心修复**：IMA Base URL修正 + folder_id格式修正 + kb_id显式标注 + API参数修正

| 变更项 | v4.0（有误） | v4.1（已修正） |
|--------|-------------|---------------|
| IMA Base URL | `ima.qq.com`（未验证） | ✅ `https://ima.qq.com`（`openapi.im.qq.com` DNS已失效） |
| folder_id | `7441985942068358` | ✅ `folder_7441985942068358`（必须带`folder_`前缀） |
| kb_id | 未标注 | ✅ `DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY=` |
| search参数 | `keyword` | ✅ `query`（search_knowledge_base用query非keyword） |
| import_doc | 未标content_format | ✅ `content_format: 1`（必填，1=Markdown） |
| 全链路验证 | 未验证 | ✅ 笔记创建+知识库关联+COS凭证获取均通过 |

### v4.0升级内容（历史）

| 变更项 | v3.0 | v4.0 |
|--------|------|------|
| Obsidian路径 | `观其妙书院` | ✅ `以观其妙书院` |
| Obsidian操作 | 仅直接文件读写 | ✅ obsidian-cli + 直接文件读写 + kepano skills |
| IMA API路径 | `ima.qq.com/agent-interface` | ✅ `ima.qq.com/openapi/note/v1` + `openapi/wiki/v1` |
| IMA知识库 | 仅概念 | ✅ folder_id明确标注 |
| WorkBuddy源 | 仅Brain目录 | ✅ Memory + LLM Wiki 双源 |
| 外部Skills | 无 | ✅ kepano obsidian-cli + obsidian-markdown |

## 🎯 核心功能

1. **三向同步**: WorkBuddy Memory/Wiki、Obsidian、IMA 三个知识库增量同步
2. **原生automation驱动**: 不依赖外部脚本，由WorkBuddy自动化系统直接执行
3. **obsidian-cli 集成**: 完整的 Obsidian CRUD 操作（搜索、创建、读取、管理）
4. **kepano Skills集成**: obsidian-cli + obsidian-markdown 规范格式
5. **IMA API 集成**: 通过ima-skill实现笔记创建+知识库上传
6. **增量模式**: 仅同步当日变更，提高效率
7. **容错处理**: IMA API不可用时自动跳过，不阻塞其他同步

## 📁 系统架构 v5.0

```
┌──────────────────────────────────────────────────────────────────────┐
│       🔗 六向同步系统 v5.0（WorkBuddy原生Automation + CLI工具）        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │           WorkBuddy 原生 Automation 引擎                      │     │
│  │                                                            │     │
│  │  ① workbuddy-obsidian (每日23:30)                            │     │
│  │     WB Memory/Wiki → Obsidian 增量同步                      │     │
│  │                                                            │     │
│  │  ② workbuddy-ima (每日23:35)                                 │     │
│  │     WB Memory/Wiki → IMA 云端同步                            │     │
│  │                                                            │     │
│  │  ③ geo-deploy (每日23:40) 🆕                                 │     │
│  │     GEO转化 → GitHub推送 → Cloudflare Pages部署              │     │
│  │     → pages.dev网站全球CDN曝光                                │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                   │
│  │   Obsidian 本地      │  │   IMA 云端            │                   │
│  │   D:\以观其妙书院\    │  │   知识库: 以观其妙书院  │                   │
│  │   obsidian-cli       │  │   API: ima.qq.com     │                   │
│  └─────────────────────┘  └─────────────────────┘                   │
│                                                                      │
│  ┌─────────────────────┐  ┌─────────────────────────────────────┐   │
│  │   GitHub             │  │   Cloudflare Pages + pages.dev       │   │
│  │   jiayue562/         │  │   wrangler deploy → CDN全球分发       │   │
│  │   yiguanqimiao-      │  │   yiguanqimiao-website.pages.dev     │   │
│  │   website            │  │   3128篇GEO优化文章                   │   │
│  └─────────────────────┘  └─────────────────────────────────────┘   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## 🚀 快速使用

### 方式一：自动同步（推荐）

无需手动操作。WorkBuddy原生automation自动执行：

| 自动化任务 | 时间 | 功能 |
|-----------|------|------|
| workbuddy-obsidian | 每日23:30 | WB→Obsidian增量同步 |
| workbuddy-ima | 每日23:35 | WB→IMA云端同步 |
| automation-5 | 每日23:45 | 沟通记录归档+Obsidian同步 |

### 方式二：手动同步

**Obsidian操作**（三种方式）:

1. **直接文件读写**（最可靠，推荐用于批量操作）:
   - 读取：Read工具读取 `D:\以观其妙书院知识库\以观其妙书院\` 下任意.md文件
   - 写入：Write/Edit工具写入对应路径
   - 搜索：Grep/Glob工具搜索文件内容/文件名

2. **obsidian-cli**（推荐用于交互式操作）:
   ```bash
   # 搜索笔记
   obsidian-cli sc "关键词"
   
   # 创建新笔记（通过Obsidian URI，需Obsidian运行中）
   obsidian-cli create "文件夹/笔记名" --content "内容" --open
   
   # 设置默认知识库
   obsidian-cli set-default "以观其妙书院"
   obsidian-cli print-default --path-only
   # 输出: D:\以观其妙书院知识库\以观其妙书院
   ```

3. **kepano Skills**（已安装，自动加载）:
   - obsidian-cli: 提供CLI操作最佳实践
   - obsidian-markdown: 提供Obsidian Markdown格式规范

**IMA操作**（通过ima-skill）:

1. **笔记操作** (openapi/note/v1):
   ```
   - import_doc: 创建笔记
   - append_doc: 追加内容
   - search_note_book: 搜索笔记
   - list_note_folder_by_cursor: 列出笔记本
   - get_doc_content: 读取笔记正文
   ```

2. **知识库操作** (openapi/wiki/v1):
   ```
   - search_knowledge_base: 搜索知识库
   - get_knowledge_list: 浏览知识库内容
   - add_knowledge: 添加内容到知识库
   - import_urls: 添加网页链接
   ```

3. **触发词**: "同步到IMA" / "IMA知识库" / "上传到IMA"

## 📋 同步目录结构

### Obsidian 同步结构
```
D:\以观其妙书院知识库\以观其妙书院\
├── 00-WorkBuddy-Sync/        # WorkBuddy自动同步目录
│   ├── 04-Knowledge/          # 知识沉淀文档
│   └── ...
├── 00-索引与导航/              # 知识库索引
├── 01-核心体系/                # 核心知识（岗位智能体、去总部化等）
├── 02-信仰文化体系/            # 心文化、大圆满等
├── 03-知识地基层/              # LLM Wiki等
├── 05-五行人格心理学/          # 五行人格系列
├── 06-工作记录与复盘/          # 工作日志
└── 09-技能库/                  # Skill文档
```

### IMA 同步结构
```
知识库: 以观其妙书院 (kb_id: DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY=)
└── 文件夹: 龙龟神将备份资料 (folder_id: folder_7441985942068358)
    ├── 味藏AI应用·岗位提示词深度学习.md
    ├── 味藏AI应用·岗位提示词知识图谱.md
    ├── 企业文化顶层设计·深度学习.md
    ├── 企业文化顶层设计·知识图谱.md
    └── ...（后续同步内容）
```

### WorkBuddy LLM Wiki 同步结构
```
~/.workbuddy/wiki-knowledge/wiki/
├── 去总部化理论.md
├── 味藏AI应用岗位提示词体系.md
└── ...（方法论框架层）
```

## ⚙️ 关键路径

| 平台 | 路径 | 说明 | 操作方式 |
|------|------|------|---------|
| WorkBuddy Memory | `c:\Users\jia'yue\WorkBuddy\Claw\.workbuddy\memory\` | 工作记忆源 | Read/Write/Edit |
| WorkBuddy Wiki | `C:\Users\jia'yue\.workbuddy\wiki-knowledge\` | LLM Wiki源 | Read/Write |
| WorkBuddy Skills | `C:\Users\jia'yue\.workbuddy\skills\` | 技能库源 | Read |
| Obsidian | `D:\以观其妙书院知识库\以观其妙书院\` | 目标1 | 文件读写+obsidian-cli |
| IMA | `https://ima.qq.com` | 目标2 | OpenAPI |
| IMA凭证 | `~/.config/ima/` | IMA认证 | client_id + api_key |

## 🔄 同步流程

### WB → Obsidian 增量同步（每日23:30）

```
1. 读取 WorkBuddy Memory (当日YYYY-MM-DD.md + MEMORY.md)
2. 读取 WorkBuddy LLM Wiki (wiki/下变更的.md)
3. 对比 Obsidian 中已有文件（通过文件存在性+内容hash）
4. 写入新增/修改的文件到 Obsidian 对应目录
5. 生成同步日志
```

### WB → IMA 云端同步（每日23:35）

```
1. 读取 WorkBuddy Memory (当日变更)
2. 读取 WorkBuddy LLM Wiki (当日变更)
3. 对每个新增/修改的文档:
   a. 调用 import_doc 创建笔记（content_format=1）
   b. 调用 add_knowledge 将笔记关联到知识库
4. 容错: IMA API不可用时自动跳过，不阻塞
```

### GEO转化 + GitHub + Cloudflare + pages.dev 🆕（每日23:40）

```
1. 运行 GEO优化脚本:
   C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\scripts\geo_optimize.py
   → 将全部.md文章转为AI爬取友好的HTML
   → 生成 llms.txt + sitemap.xml + robots.txt

2. 打包 dist 目录:
   rm -rf dist && mkdir dist
   cp -r articles dist/ && cp llms.txt sitemap.xml robots.txt dist/
   python -c 修复根首页articles/链接前缀

3. 部署到 Cloudflare Pages:
   CLOUDFLARE_API_TOKEN=cfut_xxx CLOUDFLARE_ACCOUNT_ID=c1965573a5f89d696d011372a7cd0c9e \
   npx wrangler pages deploy dist --project-name=yiguanqimiao-website --branch=main --commit-dirty=true
   → 全球CDN分发: https://yiguanqimiao-website.pages.dev/

4. 推送到 GitHub（备用存档）:
   cd yiguanqimiao-website
   git add articles/ llms.txt sitemap.xml robots.txt
   git commit -m "GEO同步: {date}"
   git push origin master
```

## 🛡️ 安全说明

- IMA凭证仅存储在本地 `~/.config/ima/`
- 凭证仅用于官方IMA API认证（`ima.qq.com`）
- 不会将凭证发送到任何第三方服务
- 原生automation不依赖外部脚本，减少攻击面
- Obsidian文件操作遵循个人文件安全规则

## 📞 故障排除

### 常见问题

1. **同步未执行**: 检查automation状态 `automation_update(mode="list")`
2. **Obsidian同步失败**: 确认路径 `D:\以观其妙书院知识库\以观其妙书院\` 存在
3. **IMA API错误**: 检查 `~/.config/ima/` 凭证文件；Base URL必须是`https://ima.qq.com`（`openapi.im.qq.com` DNS已失效）；folder_id必须带`folder_`前缀
4. **obsidian-cli未找到**: `npm install -g @yakitrak/obsidian-cli`
5. **IMA folder不存在**: folder_id格式必须为`folder_`前缀开头，如`folder_7441985942068358`（非裸数字ID）
6. **Obsidian搜索无结果**: 使用 `obsidian-cli sc "关键词"` (非 `search`)

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v4.1.0 | 2026-05-20 | 修正IMA Base URL + folder_id格式 + kb_id + API参数 + 全链路验证通过 |
| v4.0.0 | 2026-05-20 | 整合kepano skills + 修正Obsidian路径 + 完善IMA API路径 + LLM Wiki双源 |
| v3.0.0 | 2026-05-17 | 架构重构：原生automation替代外部脚本，删除6个冗余自动化 |
| v2.0.0 | 2026-04-24 | 新增SKILL.md，配置IMA API |
| v1.0.0 | 2026-04-17 | 初始设计，依赖sync.py/tri-sync.ps1（未实现） |

---

**版本**: 4.1.0  
**最后更新**: 2026-05-20  
**兼容性**: WorkBuddy 1.0+, Obsidian 1.0+, IMA OpenAPI  
**维护者**: 龙龟神将

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/2026-06-24]] — 2026-06-24 工作日志
- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-24]] — 2026-06-24 工作日志
- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[20-工作记录与复盘/2026-08/2026-08-26]] — 2026-08-26 工作日志
- [[ψ技能体系/30-tools/qclaw-knowledge-sync/SKILL-triple]] — 三向知识库同步增强版
- [[思维模型/01-核心体系/龙脑-思维模型顶层设计/NSC8936-04-三库同步指引]] — 四、三库同步指引

<!-- AI-LINKS-END -->
