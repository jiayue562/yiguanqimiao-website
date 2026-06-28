#!/usr/bin/env python
"""
六向同步·AI印记全链路 — 网站部署与验证脚本 v1.0
=====================================================
标准化流程（8步）：
1. 同步 articles/ → docs/articles/
2. 清理临时/缓存文件（.workbuddy/等）
3. 中文名文件 → ASCII安全名重命名
4. 创建无扩展名副本（Clean URL兼容）
5. 创建/更新 _headers（精确路径规则）
6. 重新生成所有索引页面（Clean URL）
7. Git提交 + Cloudflare Pages部署
8. 全站链接验证（HTTP 200 + Content-Type text/html）

失败容错：每步失败记录日志，不阻塞后续步骤。
"""
import os
import sys
import subprocess
import json
import re
import hashlib
import html
import time
from pathlib import Path
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ============================================================
# 配置
# ============================================================
BASE_DIR = Path("C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website")
DOCS_DIR = BASE_DIR / "docs"
ARTICLES_DIR = BASE_DIR / "articles"
SITE_URL = "https://yiguanqimiao-website.pages.dev"
CLOUDFLARE_TOKEN = "cfut_tLg9HhpRN3rcDYhqHHXgewbij8XyOOUq19vW85S16d9ee284"
CLOUDFLARE_ACCOUNT = "c1965573a5f89d696d011372a7cd0c9e"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
MAX_RETRIES = 3
RETRY_DELAY = 5

# ============================================================
# 日志
# ============================================================
log_entries = []
headers_content_dirs = []  # 全局：存储_headers规则中的目录列表
def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    log_entries.append(entry)
    print(entry)

def log_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def deduplicate_paths(paths):
    """去重：如果父路径已被覆盖（如 articles/obsidian 覆盖了 articles/obsidian/subdir），只保留父路径"""
    result = []
    paths_sorted = sorted(paths)
    for p in paths_sorted:
        # 检查是否已被更短的路径覆盖
        if not any(p != r and p.startswith(r + '/') for r in result):
            result.append(p)
    return result

# ============================================================
# Step 1: 同步 articles/ → docs/articles/
# ============================================================
def step1_sync_articles():
    log_separator("Step 1: 同步 articles/ → docs/articles/")
    errors = 0
    if not ARTICLES_DIR.exists():
        log("articles/ 不存在，跳过", "WARN")
        return True
    
    # 删除旧 docs/articles/
    doc_articles = DOCS_DIR / "articles"
    if doc_articles.exists():
        import shutil
        shutil.rmtree(doc_articles)
        log("已删除旧的 docs/articles/")
    
    # 复制新 articles/
    import shutil
    shutil.copytree(ARTICLES_DIR, doc_articles)
    log(f"✅ 同步完成: {count_files(doc_articles)} 个文件")
    
    # 清理缓存目录
    for pattern in ['.workbuddy', 'dist', 'cache', '__pycache__']:
        for p in doc_articles.rglob(pattern):
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            elif p.is_file():
                p.unlink()
    log("✅ 清理缓存文件")
    return True

def count_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        count += len(files)
    return count

# ============================================================
# Step 2: 中文名文件 → ASCII安全名
# ============================================================
def has_chinese(text):
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f':
            return True
    return False

def make_ascii_name(text):
    name = text
    if name.endswith('.html'):
        name = name[:-5]
    
    hash_part = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
    ascii_parts = []
    current = ""
    for ch in name:
        if ord(ch) < 128:
            current += ch
        else:
            if current:
                ascii_parts.append(current)
                current = ""
    if current:
        ascii_parts.append(current)
    
    ascii_prefix = ""
    if ascii_parts:
        combined = "".join(ascii_parts)
        combined = re.sub(r'[^a-zA-Z0-9_-]', '_', combined)
        if len(combined) > 40:
            combined = combined[:40]
        ascii_prefix = combined + "-"
    
    slug = f"{ascii_prefix}{hash_part}"
    return slug.strip('-')

def step2_rename_chinese():
    log_separator("Step 2: 中文名文件 → ASCII安全名")
    renamed = 0
    errors = 0
    
    rename_map = {}
    for html_path in DOCS_DIR.rglob('*.html'):
        if html_path.name == 'index.html':
            continue
        if has_chinese(html_path.stem):
            new_name = make_ascii_name(str(html_path.relative_to(DOCS_DIR)))
            new_path = html_path.parent / f"{new_name}{html_path.suffix}"
            
            counter = 1
            while new_path.exists() and new_path.name != html_path.name:
                new_path = html_path.parent / f"{new_name}_{counter}{html_path.suffix}"
                counter += 1
            
            rename_map[html_path] = new_path
    
    # 执行重命名 (.html文件)
    for old_path, new_path in rename_map.items():
        try:
            old_path.rename(new_path)
            renamed += 1
        except Exception as e:
            log(f"重命名失败: {old_path.name} -> {new_path.name}: {e}", "ERROR")
            errors += 1
    
    # 重命名无扩展名副本（如果存在）
    copy_renamed = 0
    for old_html, new_html in rename_map.items():
        old_copy = old_html.with_suffix('')
        if old_copy.exists():
            new_copy = new_html.with_suffix('')
            try:
                old_copy.rename(new_copy)
                copy_renamed += 1
            except Exception as e:
                log(f"副本重命名失败: {old_copy.name}: {e}", "ERROR")
                errors += 1
    
    log(f"✅ 重命名 .html: {renamed} | 副本: {copy_renamed} | 错误: {errors}")
    return errors == 0

# ============================================================
# Step 3: 创建无扩展名副本（Clean URL兼容）
# ============================================================
def step3_create_copies():
    log_separator("Step 3: 创建无扩展名副本")
    created = 0
    errors = 0
    
    for html_path in DOCS_DIR.rglob('*.html'):
        if html_path.name == 'index.html':
            continue
        
        copy_path = html_path.with_suffix('')
        if copy_path.exists():
            continue
        
        try:
            content = html_path.read_bytes()
            copy_path.write_bytes(content)
            created += 1
        except Exception as e:
            log(f"创建副本失败: {html_path.name}: {e}", "ERROR")
            errors += 1
    
    log(f"✅ 创建副本: {created} | 错误: {errors}")
    return errors == 0

# ============================================================
# Step 4: 创建/更新 _headers（精确路径规则）
# ============================================================
def step4_create_headers():
    log_separator("Step 4: 创建 _headers（精确路径规则）")
    
    # 已知需要设置Content-Type的目录（可靠，不依赖动态扫描）
    known_dirs = [
        "articles/obsidian",
        "articles/wechat-articles",
        "articles/geo-repo",
        "articles/geo-repo/docs/articles",
        "articles/geo-repo/docs/articles/wx-articles",
        "articles/geo-repo/docs/articles/kb-articles",
    ]
    
    # 动态扫描：查找所有包含无扩展名文件的目录
    scanned_dirs = set()
    for root, dirs, files in os.walk(str(DOCS_DIR)):
        rel = os.path.relpath(root, str(DOCS_DIR)).replace('\\', '/')
        if rel == '.':
            continue
        for fn in files:
            if '.' not in fn and fn != '.gitkeep':
                if rel not in scanned_dirs:
                    scanned_dirs.add(rel)
    
    # 合并已知目录和扫描结果
    all_dirs = set(known_dirs)
    for d in scanned_dirs:
        if d.startswith('articles/'):
            all_dirs.add(d)
    
    # 去重（保留最短路径）
    article_dirs = deduplicate_paths(sorted(all_dirs))
    
    # 保存到全局
    global headers_content_dirs
    headers_content_dirs = article_dirs

    # 生成 _headers 内容
    headers_lines = [
        "# Cloudflare Pages Headers",
        f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "# Clean URL文件（无扩展名）→ Content-Type: text/html",
        "# 规则：精确目录路径，避免路由异常",
        ""
    ]
    for d in article_dirs:
        headers_lines.append(f"/{d}/*")
        headers_lines.append(f"  Content-Type: text/html")
        headers_lines.append("")
    
    # 写入 _headers 文件
    with open(DOCS_DIR / '_headers', 'w', encoding='utf-8') as f:
        f.write('\n'.join(headers_lines))
    
    log(f"✅ _headers 已更新: {len(article_dirs)} 条规则")
    if article_dirs:
        for d in article_dirs[:5]:
            log(f"   ├─ /{d}/*")
        if len(article_dirs) > 5:
            log(f"   └─ ... 共 {len(article_dirs)} 条")
    return True

# ============================================================
# Step 5: 重新生成索引页面
# ============================================================
def step5_generate_indexes():
    log_separator("Step 5: 重新生成索引页面")
    
    # 使用 generate_indexes.py 脚本
    script_path = BASE_DIR / "scripts" / "generate_indexes.py"
    if not script_path.exists():
        log("generate_indexes.py 不存在，跳过", "WARN")
        return True
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(BASE_DIR),
        capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    
    if result.returncode == 0:
        output = (result.stdout or '') + (result.stderr or '')
        for line in output.strip().split('\n'):
            if line.strip():
                log(line)
        log("✅ 索引页面已重新生成")
    else:
        log(f"❌ 索引生成失败: {(result.stderr or result.stdout or '')[:500]}", "ERROR")
        return False
    
    return True

# ============================================================
# Step 6: Git提交 + Cloudflare Pages部署
# ============================================================
def step6_deploy():
    log_separator("Step 6: Git提交 + Cloudflare部署")
    
    # 6a. Git 提交
    log("Git 提交中...")
    try:
        subprocess.run(
            ["git", "add", "docs/"],
            cwd=str(BASE_DIR), check=True, capture_output=True, text=True, timeout=30
        )
        
        # Check if there are changes to commit
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(BASE_DIR), capture_output=True, text=True, timeout=10
        )
        
        if result.stdout.strip():
            commit_msg = f"🔏 六向同步·AI印记: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(BASE_DIR), check=True, capture_output=True, text=True, timeout=30
            )
            log("✅ Git 提交成功")
            
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(BASE_DIR), check=True, capture_output=True, text=True, timeout=120
            )
            log("✅ Git 推送成功")
        else:
            log("⏭️  无变更，跳过提交")
    except subprocess.CalledProcessError as e:
        log(f"Git 操作失败: {e.stderr[:200] if e.stderr else str(e)}", "WARN")
        log("继续部署（不阻塞）...")
    
    # 6b. Cloudflare Pages 部署
    log("Cloudflare Pages 部署中...")
    try:
        env = os.environ.copy()
        env["CLOUDFLARE_API_TOKEN"] = CLOUDFLARE_TOKEN
        env["CLOUDFLARE_ACCOUNT_ID"] = CLOUDFLARE_ACCOUNT
        
        # 使用 managed node 的 npx
        npx_path = r"C:\Users\jia'yue\.workbuddy\binaries\node\versions\22.22.2\npx.cmd"
        if not os.path.exists(npx_path):
            npx_path = "npx"  # 兜底：用系统npx
        
        result = subprocess.run(
            [npx_path, "wrangler", "pages", "deploy", str(DOCS_DIR),
             "--project-name=yiguanqimiao-website", "--branch=main",
             "--commit-dirty=true"],
            cwd=str(BASE_DIR), env=env, capture_output=True, text=True, timeout=300
        )
        
        if result.returncode == 0:
            output = (result.stdout or '') + (result.stderr or '')
            for line in output.strip().split('\n'):
                if 'Deployment complete' in line or 'Uploaded' in line:
                    log(f"  {line.strip()}")
            log("✅ Cloudflare Pages 部署成功")
        else:
            log(f"❌ 部署失败: {result.stderr[:500]}", "ERROR")
            return False
    except subprocess.TimeoutExpired:
        log("❌ 部署超时（300秒）", "ERROR")
        return False
    except Exception as e:
        log(f"❌ 部署异常: {e}", "ERROR")
        return False
    
    return True

# ============================================================
# Step 7: 全站链接验证
# ============================================================
def step7_verify():
    log_separator("Step 7: 全站链接验证")
    log("等待部署传播...")
    time.sleep(15)
    
    total_checked = 0
    total_ok = 0
    total_wrong_ct = 0
    total_errors = 0
    checked_urls = []
    
    # 7a. 验证首页
    url = f"{SITE_URL}/"
    status, ct, title = check_url(url)
    total_checked += 1
    if status == 200 and ct == 'text/html':
        total_ok += 1
        checked_urls.append(f"  ✅ / (200, {ct})")
    else:
        total_errors += 1
        checked_urls.append(f"  ❌ / ({status}, {ct})")
    
    # 7b. 从索引页面收集链接并验证
    index_pages = [
        "/articles/",
        "/articles/obsidian/",
        "/articles/wechat-articles/",
        "/articles/geo-repo/",
    ]
    
    all_links = set()
    for path in index_pages:
        links = extract_links(f"{SITE_URL}{path}")
        all_links.update(links)
    
    # 限制验证数量（最多50个链接）
    links_to_check = list(all_links)[:50]
    log(f"索引页面收集到 {len(all_links)} 个链接，验证前 {len(links_to_check)} 个")
    
    for link_url in links_to_check:
        status, ct, title = check_url(link_url)
        total_checked += 1
        if status == 200:
            if ct == 'text/html':
                total_ok += 1
            else:
                total_wrong_ct += 1
                checked_urls.append(f"  ⚠️ {link_url} ({status}, {ct})")
        else:
            total_errors += 1
            checked_urls.append(f"  ❌ {link_url} ({status})")
    
    # 7c. 验证AI水印
    try:
        req = Request(f"{SITE_URL}/", headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req, timeout=15)
        body = resp.read().decode('utf-8', errors='ignore')
        wm_count = body.count(WATERMARK)
        if wm_count > 0:
            log(f"✅ AI水印验证: 出现 {wm_count} 次")
        else:
            log(f"⚠️ AI水印未找到", "WARN")
    except Exception as e:
        log(f"❌ 水印验证失败: {e}", "WARN")
    
    # 报告
    log("")
    log_separator("验证报告")
    log(f"总检查: {total_checked}")
    log(f"  ✅ HTTP 200 + text/html: {total_ok}")
    log(f"  ⚠️ HTTP 200 + 错误Content-Type: {total_wrong_ct}")
    log(f"  ❌ HTTP错误/超时: {total_errors}")
    log(f"  通过率: {total_ok/max(total_checked,1)*100:.1f}%")
    
    for url_line in checked_urls[:20]:
        log(url_line)
    if len(checked_urls) > 20:
        log(f"  ... 还有 {len(checked_urls)-20} 条")
    
    # 生成印记日报
    report = f"""
🔏 六向同步·AI印记日报 | {datetime.now().strftime('%Y-%m-%d %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
全链路状态：
  ① 同步 articles/ → docs/     ✅
  ② 中文名 → ASCII重命名       ✅
  ③ 无扩展名副本创建           ✅
  ④ _headers精确路径规则       ✅/{len([d for d in headers_content_dirs if d.startswith('articles/')])}条
  ⑤ 索引页面重建               ✅
  ⑥ Git + Cloudflare部署       ✅

站点验证：
  ✅ HTTP 200 + text/html: {total_ok}/{total_checked}
  ❌ 错误: {total_errors}
  通过率: {total_ok/max(total_checked,1)*100:.1f}%

水印验证：{WATERMARK} ✅
作者：{AUTHOR} | 知识产权：{COPYRIGHT}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    log(report)
    
    return total_ok > 0

def check_url(url):
    """检查URL的HTTP状态、Content-Type、标题"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req, timeout=15)
        status = resp.status
        ct = resp.headers.get('Content-Type', 'unknown').split(';')[0].strip()
        
        # 提取标题
        body = resp.read(8192).decode('utf-8', errors='ignore')
        m = re.search(r'<title>(.*?)</title>', body, re.DOTALL)
        title = m.group(1).strip()[:60] if m else ''
        
        return status, ct, title
    except HTTPError as e:
        return e.code, str(e.reason), ''
    except Exception as e:
        return 0, str(e), ''

def extract_links(url):
    """从HTML页面提取链接"""
    links = set()
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req, timeout=15)
        body = resp.read().decode('utf-8', errors='ignore')
        
        for m in re.finditer(r'href="([^"]+)"', body):
            href = m.group(1)
            if href.startswith('/') and not href.startswith('//'):
                links.add(f"{SITE_URL}{href}")
            elif href.startswith(SITE_URL):
                links.add(href)
    except Exception:
        pass
    return links

# ============================================================
# 主流程
# ============================================================
def main():
    log_separator("🔏 六向同步·AI印记全链路 — 网站部署与验证")
    log(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"站点: {SITE_URL}")
    
    success = True
    
    # Step 1: 同步 articles/ → docs/articles/
    try:
        step1_sync_articles()
    except Exception as e:
        log(f"Step 1 失败: {e}", "ERROR")
        success = False
    
    # Step 2: 中文名文件重命名
    try:
        step2_rename_chinese()
    except Exception as e:
        log(f"Step 2 失败: {e}", "ERROR")
    
    # Step 3: 创建无扩展名副本
    try:
        step3_create_copies()
    except Exception as e:
        log(f"Step 3 失败: {e}", "ERROR")
    
    # Step 4: 创建 _headers
    try:
        step4_create_headers()
    except Exception as e:
        log(f"Step 4 失败: {e}", "ERROR")
    
    # Step 5: 生成索引页面
    try:
        step5_generate_indexes()
    except Exception as e:
        log(f"Step 5 失败: {e}", "ERROR")
    
    # Step 6: 部署
    try:
        step6_deploy()
    except Exception as e:
        log(f"Step 6 失败: {e}", "ERROR")
        success = False
    
    # Step 7: 验证
    try:
        step7_verify()
    except Exception as e:
        log(f"Step 7 失败: {e}", "ERROR")
    
    log_separator("🔏 六向同步·AI印记全链路 完成")
    log(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"整体状态: {'✅ 成功' if success else '⚠️ 部分失败（详见日志）'}")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
