#!/usr/bin/env bash
# ============================================================
# 一键部署脚本：GEO转化 + 部署到 Cloudflare Pages + GitHub
# 用法：每次公众号文章写完 → 运行此脚本
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WEBSITE_DIR="/c/Users/jia'yue/WorkBuddy/yiguanqimiao-website"
PYTHON="/c/Users/jia'yue/.workbuddy/binaries/python/versions/3.13.12/python.exe"

CF_TOKEN="cfut_W6SqH8ROMt6Deh9DX7mmIHqyIYPdZMWnYvtbInwcc8321845"
CF_ACCOUNT="c1965573a5f89d696d011372a7cd0c9e"
GH_TOKEN="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"

echo "🚀 开始一键部署..."
echo ""

# Step 1: GEO 优化
echo "📝 Step 1/4: GEO转化..."
cd "$WEBSITE_DIR"
"$PYTHON" scripts/geo_optimize.py
echo ""

# Step 2: 准备 dist 目录
echo "📦 Step 2/4: 准备部署包..."
rm -rf dist
mkdir -p dist
cp -r articles dist/
# 修复根首页链接：articles/index.html 内的相对路径需加 articles/ 前缀才能从根目录访问
"$PYTHON" -c "
import re
with open('dist/articles/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# 将相对链接改为 articles/ 前缀
html = re.sub(r'href=\"(?!https?://)(?!articles/)([^\"]+)\"', r'href=\"articles/\1\"', html)
html = html.replace('href=\"articles/articles/', 'href=\"articles/')
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('   ✅ 根首页链接已修复')
"
cp llms.txt dist/
cp sitemap.xml dist/ 2>/dev/null || true
cp robots.txt dist/ 2>/dev/null || true
echo "   ✅ dist 准备完成 ($(find dist -type f | wc -l) 个文件)"
echo ""

# Step 3: 部署到 Cloudflare Pages
echo "☁️  Step 3/4: 部署到 Cloudflare Pages..."
CLOUDFLARE_API_TOKEN="$CF_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT" \
    npx wrangler pages deploy dist --project-name="yiguanqimiao-website" --branch=main --commit-dirty=true
echo ""

# Step 4: 推送到 GitHub（备用 + SEO）
echo "🔗 Step 4/4: 推送到 GitHub..."
GIT_SSL_NO_VERIFY=1 git add articles/ llms.txt sitemap.xml robots.txt 2>/dev/null || true
GIT_SSL_NO_VERIFY=1 git commit -m "GEO同步: $(date '+%Y-%m-%d %H:%M') - 五行人格心理学内容更新" 2>/dev/null || true
GIT_SSL_NO_VERIFY=1 git push "https://${GH_TOKEN}@github.com/jiayue562/yiguanqimiao-website.git" master 2>/dev/null || echo "   ⚠️ GitHub推送跳过（网络不可达，Cloudflare已部署成功）"
echo ""

echo "============================================"
echo "🎉 部署完成！"
echo "🌐 https://yiguanqimiao-website.pages.dev/"
echo "🤖 AI爬取入口: https://yiguanqimiao-website.pages.dev/llms.txt"
echo "============================================"
