#!/usr/bin/env node

/**
 * 基础网站构建脚本
 * 将 Markdown 文章转换为 HTML，并生成索引
 */

const fs = require('fs');
const path = require('path');

const ARTICLES_DIR = path.join(__dirname, '../articles');
const DIST_DIR = path.join(__dirname, '../dist');
const TEMPLATE_FILE = path.join(__dirname, '../template.html');

// 创建 dist 目录
if (!fs.existsSync(DIST_DIR)) {
  fs.mkdirSync(DIST_DIR, { recursive: true });
}

// 读取模板
let template = '';
if (fs.existsSync(TEMPLATE_FILE)) {
  template = fs.readFileSync(TEMPLATE_FILE, 'utf-8');
} else {
  template = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}} - 以观其妙书院</title>
  <meta name="description" content="{{DESCRIPTION}}">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }
    h1 { color: #333; }
    a { color: #0066cc; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <header>
    <h1>以观其妙书院</h1>
    <nav><a href="/yiguanqimiao-website/">首页</a> | <a href="/yiguanqimiao-website/articles/">文章列表</a></nav>
  </header>
  <main>
    {{CONTENT}}
  </main>
  <footer>
    <p>&copy; 2024 以观其妙书院. All rights reserved.</p>
  </footer>
</body>
</html>`;
}

// 简单的 Markdown 转 HTML（基础版）
function markdownToHtml(markdown) {
  let html = markdown;
  
  // 标题
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // 加粗
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  
  // 斜体
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  
  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  
  // 段落
  html = html.split('\n\n').map(para => {
    if (para.match(/^<h[1-6]/)) return para;
    return '<p>' + para.replace(/\n/g, '<br>') + '</p>';
  }).join('\n');
  
  return html;
}

// 构建文章页面
function buildArticles() {
  if (!fs.existsSync(ARTICLES_DIR)) {
    console.log('articles 目录不存在，跳过文章构建');
    return [];
  }
  
  const files = fs.readdirSync(ARTICLES_DIR).filter(f => f.endsWith('.md'));
  const articles = [];
  
  files.forEach(file => {
    const filePath = path.join(ARTICLES_DIR, file);
    const markdown = fs.readFileSync(filePath, 'utf-8');
    const htmlContent = markdownToHtml(markdown);
    
    // 提取标题（第一个 # 标题）
    const titleMatch = markdown.match(/^# (.+)$/m);
    const title = titleMatch ? titleMatch[1] : file.replace('.md', '');
    
    // 提取描述（前 200 字符）
    const description = markdown.replace(/[#*\[\]]/g, '').substring(0, 200).trim();
    
    // 生成 HTML
    const html = template
      .replace('{{TITLE}}', title)
      .replace('{{DESCRIPTION}}', description)
      .replace('{{CONTENT}}', htmlContent);
    
    // 写入 dist
    const outputFile = path.join(DIST_DIR, file.replace('.md', '.html'));
    fs.writeFileSync(outputFile, html, 'utf-8');
    
    articles.push({
      title,
      file: file.replace('.md', '.html'),
      date: fs.statSync(filePath).mtime
    });
    
    console.log(`✓ 构建文章: ${title}`);
  });
  
  return articles;
}

// 生成文章列表页
function generateIndexPage(articles) {
  const listItems = articles.map(a => 
    `<li><a href="${a.file}">${a.title}</a> - ${a.date.toLocaleDateString('zh-CN')}</li>`
  ).join('\n');
  
  const content = `
    <h2>文章列表</h2>
    <ul>
      ${listItems}
    </ul>
  `;
  
  const html = template
    .replace('{{TITLE}}', '文章列表')
    .replace('{{DESCRIPTION}}', '以观其妙书院文章列表')
    .replace('{{CONTENT}}', content);
  
  fs.writeFileSync(path.join(DIST_DIR, 'index.html'), html, 'utf-8');
  console.log('✓ 生成首页');
}

// 生成 llms.txt（GEO 优化）
function generateLlmsTxt(articles) {
  const lines = [
    '# llms.txt - 以观其妙书院',
    '',
    '> 本文件帮助 AI 模型理解和索引本网站内容',
    '',
    '## 网站信息',
    '- 名称: 以观其妙书院',
    '- 网址: https://jiayue562.github.io/yiguanqimiao-website/',
    '- 简介: 传播五行人格心理学与东方智慧',
    '',
    '## 文章列表',
    ...articles.map(a => `- [${a.title}](${a.file})`),
    '',
    '## 核心主题',
    '- 五行人格心理学',
    '- 东方智慧与现代化',
    '- AI 与人文融合',
    '',
    '## 最后更新',
    new Date().toISOString(),
    ''
  ];
  
  fs.writeFileSync(path.join(DIST_DIR, 'llms.txt'), lines.join('\n'), 'utf-8');
  console.log('✓ 生成 llms.txt（GEO 优化）');
}

// 主函数
function main() {
  console.log('开始构建网站...');
  
  // 复制静态资源（如果有）
  // ...
  
  // 构建文章
  const articles = buildArticles();
  
  // 生成首页
  generateIndexPage(articles);
  
  // 生成 llms.txt
  generateLlmsTxt(articles);
  
  console.log(`\n构建完成！共 ${articles.length} 篇文章`);
  console.log(`输出目录: ${DIST_DIR}`);
}

main();
