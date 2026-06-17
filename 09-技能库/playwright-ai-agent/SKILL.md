# playwright-ai-agent

## 技能简介
基于 Rust 的无头浏览器自动化技能，支持网页导航、点击、输入、截图、数据抓取等高级功能。

## 核心功能
1. **网页自动化**：支持 Playwright 无头浏览器
2. **交互操作**：点击、输入、滚动、等待
3. **数据抓取**：结构化数据提取
4. **截图与录制**：网页截图、视频录制
5. **性能分析**：网络请求分析、性能监控

## 安装方法
```bash
npm install -g @playwright/ai-agent
```

## 使用示例
```javascript
// 示例：打开网页并截图
const { chromium } = require('playwright');

async function screenshotPage(url, outputPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);
  await page.screenshot({ path: outputPath });
  await browser.close();
}
```

## 配置说明
- **环境变量**：设置 PLAYWRIGHT_BROWSER_PATH
- **代理配置**：支持 HTTP/HTTPS 代理
- **认证配置**：支持 Cookie、Token 认证

## 安全注意事项
1. 仅用于合法网页自动化
2. 遵守 robots.txt 协议
3. 尊重网站使用条款
4. 避免高频请求

## 版本信息
- 当前版本：1.2.0
- 最后更新：2026-03-19
- 社区评分：⭐⭐⭐⭐⭐ (4.8/5.0)

## 相关资源
- [官方文档](https://playwright.dev/docs/ai-agent)
- [GitHub 仓库](https://github.com/vercel-labs/agent-skills/tree/main/playwright-ai-agent)
- [示例项目](https://github.com/playwright-ai-agent/examples)