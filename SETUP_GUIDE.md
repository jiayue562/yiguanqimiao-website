# yiguanqimiao-website 自动化部署配置指南

## 概述
本指南帮助您配置每日公众号文章自动GEO转化并部署到 GitHub Pages 的完整流程。

## 安全说明
⚠️ **重要**：所有敏感信息通过 **GitHub Secrets** 管理，不会存储在代码中。

## 配置步骤

### 步骤 1：创建 GitHub 仓库（如果尚未创建）
1. 访问 https://github.com/new
2. 仓库名：`yiguanqimiao-website`
3. 选择 **Public**（GitHub Pages 免费版需要公开仓库）
4. 勾选 "Add a README file"
5. 点击 "Create repository"

### 步骤 2：配置 GitHub Secrets
在 GitHub 仓库中配置以下 Secrets：

1. 进入仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下 Secrets：

#### 必需的 Secrets：
| Secret 名称 | 说明 | 获取方式 |
|-------------|------|----------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token | 从您提供的信息中填写 |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare 账户 ID | `c1965573a5f89d696d011372a7cd0c9e` |
| `CLOUDFLARE_ZONE_ID` | Cloudflare Zone ID | 在 Cloudflare 控制台获取 |
| `WECHAT_PUBLISHER_TOKEN` | 微信公众号 API Token | 根据需要配置 |
| `WECOM_BOT_WEBHOOK` | 企业微信机器人 Webhook（可选） | 用于接收部署通知 |

#### 如何获取 Cloudflare Zone ID：
1. 登录 https://dash.cloudflare.com
2. 选择您的域名
3. 在右侧边栏找到 **Zone ID**

### 步骤 3：启用 GitHub Pages
1. 进入仓库 → **Settings** → **Pages**
2. **Source** 选择 "GitHub Actions"
3. 保存

### 步骤 4：配置 Cloudflare
1. 登录 https://dash.cloudflare.com
2. 添加域名或配置现有域名
3. 设置 **CNAME** 记录指向 `jiayue562.github.io`
4. 启用 **Always Use HTTPS**

### 步骤 5：推送代码
```bash
cd /c/Users/jia'yue/WorkBuddy/yiguanqimiao-website
git init
git add .
git commit -m "Initial commit: 自动化部署配置"
git remote add origin https://github.com/jiayue562/yiguanqimiao-website.git
git push -u origin main
```

### 步骤 6：验证部署
1. 进入仓库 → **Actions** 标签
2. 查看工作流是否正常运行
3. 访问 https://jiayue562.github.io/yiguanqimiao-website/ 验证部署

## 每日自动化流程

### 自动触发：
- **时间**：每天早上 6:00（北京时间）
- **操作**：
  1. 获取最新公众号文章
  2. GEO 优化处理
  3. 构建网站
  4. 部署到 GitHub Pages
  5. 清理 Cloudflare 缓存
  6. 发送通知（如果配置了）

### 手动触发：
1. 进入仓库 → **Actions**
2. 选择 "Deploy to GitHub Pages with Cloudflare"
3. 点击 "Run workflow"
4. 可选：指定文章来源和是否 GEO 优化

## 自定义配置

### 修改触发时间
编辑 `.github/workflows/deploy.yml` 中的 `cron` 表达式：
```yaml
# 示例：改为每天上午 8:00（北京时间 = 0:00 UTC）
schedule:
  - cron: '0 0 * * *'
```

### 添加 GEO 优化脚本
在 `scripts/geo-optimize.js` 中实现您的 GEO 优化逻辑。

### 添加公众号文章获取脚本
在 `scripts/fetch-wechat-articles.js` 中实现文章获取逻辑。

## 故障排查

### 部署失败
1. 检查 **Actions** 标签页的日志
2. 验证所有 Secrets 是否正确配置
3. 检查 GitHub Pages 设置

### Cloudflare 缓存未清理
1. 验证 `CLOUDFLARE_ZONE_ID` 是否正确
2. 检查 API Token 权限

## 安全建议

⚠️ **重要安全提示**：
1. **永远不要**在代码中硬编码密码或 Token
2. **定期轮换** GitHub Token 和 Cloudflare API Token
3. **使用最小权限原则**配置 API Token
4. **启用双因素认证**（2FA）保护您的 GitHub 和 Cloudflare 账户

## 下一步

配置完成后，您的每日公众号文章将自动：
1. 进行 GEO 优化
2. 转换为网页格式
3. 部署到 GitHub Pages
4. 通过 Cloudflare CDN 加速全球访问

---

**配置完成后，请删除此文件中的任何敏感信息，并妥善保管您的密码和 Token。**
