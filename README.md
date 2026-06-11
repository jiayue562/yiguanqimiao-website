# 以观其妙书院 - 网站自动化部署

本仓库实现每日公众号文章自动 GEO 转化并部署到 GitHub Pages。

## 功能特性

- ✅ **每日自动部署**：每天早上 6:00（北京时间）自动执行
- ✅ **GEO 优化**：自动生成 `llms.txt`，优化 AI 模型索引
- ✅ **Cloudflare 集成**：自动清理 CDN 缓存
- ✅ **安全凭证管理**：所有敏感信息通过 GitHub Secrets 管理
- ✅ **手动触发支持**：可随时手动触发部署

## 网站结构

```
yiguanqimiao-website/
├── .github/workflows/    # GitHub Actions 工作流
├── articles/             # 公众号文章（Markdown 格式）
├── dist/                # 构建输出目录（自动生成）
├── scripts/              # 构建和优化脚本
├── llms.txt             # GEO 优化文件
└── README.md            # 本文件
```

## 快速开始

### 1. 配置 GitHub Secrets

在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加：

| Secret 名称 | 说明 |
|-------------|------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账户 ID |
| `CLOUDFLARE_ZONE_ID` | Cloudflare Zone ID |
| `WECHAT_PUBLISHER_TOKEN` | 微信公众号 API Token（可选） |
| `WECOM_BOT_WEBHOOK` | 企业微信机器人 Webhook（可选） |

### 2. 启用 GitHub Pages

1. 进入仓库 **Settings → Pages**
2. **Source** 选择 **GitHub Actions**

### 3. 配置 Cloudflare

1. 在 Cloudflare 中添加域名（或使用现有域名）
2. 设置 CNAME 记录指向 `jiayue562.github.io`
3. 获取 **Zone ID** 并添加到 GitHub Secrets

## 使用说明

### 自动部署

每天早上 6:00（北京时间）自动执行：
1. 获取最新公众号文章
2. GEO 优化处理
3. 构建网站
4. 部署到 GitHub Pages
5. 清理 Cloudflare 缓存

### 手动部署

1. 进入仓库 **Actions** 标签
2. 选择 **Deploy to GitHub Pages with Cloudflare**
3. 点击 **Run workflow**
4. 可选：指定文章来源和是否 GEO 优化

### 添加新文章

将 Markdown 格式的文章放入 `articles/` 目录，然后：
- 等待自动部署，或
- 手动触发部署

## GEO 优化

本网站遵循 GEO（Generative Engine Optimization）最佳实践：

- ✅ 提供结构化的 `llms.txt` 文件
- ✅ 使用语义化 HTML 标签
- ✅ 提供清晰的内容描述和元数据
- ✅ 优化文章结构和可读性

## 技术栈

- **部署**：GitHub Pages
- **CDN**：Cloudflare
- **自动化**：GitHub Actions
- **构建**：Node.js

## 安全说明

⚠️ **重要**：
- 所有敏感信息通过 **GitHub Secrets** 管理
- 永远不要将密码或 Token 提交到代码中
- 定期轮换 API Token

## 相关链接

- **网站**：https://jiayue562.github.io/yiguanqimiao-website/
- **公众号**：以观其妙书院
- **GitHub**：https://github.com/jiayue562/yiguanqimiao-website

## 维护者

- **龙龟神将**（AI 助手）
- **悟空**（人类维护者）

---

**最后更新**：2026-06-12
