#!/usr/bin/env python3
"""
全站链接审计脚本 v1.0
功能：
1. 爬取 https://yiguanqimiao-website.pages.dev/ 所有页面
2. 检查每个链接的HTTP状态（必须是200）
3. 验证AI水印矩阵是否全链路注入
4. 生成审计报告

使用：python site_audit.py
"""

import requests
import re
from urllib.parse import urljoin, urlparse
from collections import deque
import time
from datetime import datetime

# 配置
BASE_URL = "https://yiguanqimiao-website.pages.dev"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

# 审计结果
audit_results = {
    "total_pages": 0,
    "http_200": 0,
    "http_errors": 0,
    "watermark_ok": 0,
    "watermark_missing": 0,
    "dead_links": [],
    "watermark_issues": []
}

def log(msg):
    """日志输出"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def get_all_links(url):
    """获取页面所有链接（使用正则表达式）"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        content = response.text
        links = set()
        
        # 使用正则表达式提取所有<a href="...">链接
        # 匹配 <a href="URL"> 或 <a href='URL'>
        for match in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE):
            link = match.group(1)
            # 跳过空链接、锚点、javascript
            if not link or link.startswith('#') or link.startswith('javascript:'):
                continue
            
            # 转换为绝对URL
            link = urljoin(url, link)
            
            # 只保留同域名的链接
            if urlparse(link).netloc == urlparse(BASE_URL).netloc:
                # 移除锚点
                link = link.split('#')[0]
                links.add(link)
        
        return list(links)
    
    except Exception as e:
        log(f"❌ 获取链接失败：{url} - {e}")
        return []

def check_page(url):
    """检查单个页面"""
    try:
        response = requests.get(url, timeout=10)
        
        result = {
            "url": url,
            "status": response.status_code,
            "watermark": False,
            "errors": []
        }
        
        # 检查HTTP状态
        if response.status_code != 200:
            result["errors"].append(f"HTTP {response.status_code}")
            audit_results["http_errors"] += 1
        else:
            audit_results["http_200"] += 1
        
        # 检查AI水印（仅200页面）
        if response.status_code == 200:
            content = response.text.lower()
            
            # 检查meta标签
            if WATERMARK.lower() in content:
                result["watermark"] = True
                audit_results["watermark_ok"] += 1
            else:
                result["errors"].append("AI水印缺失")
                audit_results["watermark_missing"] += 1
                audit_results["watermark_issues"].append(url)
        
        audit_results["total_pages"] += 1
        
        return result
    
    except Exception as e:
        log(f"❌ 检查失败：{url} - {e}")
        audit_results["http_errors"] += 1
        audit_results["total_pages"] += 1
        return {"url": url, "status": 0, "watermark": False, "errors": [str(e)]}

def crawl_site():
    """爬取全站"""
    log("=" * 60)
    log("开始全站链接审计")
    log(f"目标网站：{BASE_URL}")
    log("=" * 60)
    
    # 使用队列进行广度优先爬取
    queue = deque([BASE_URL])
    visited = set()
    
    while queue:
        url = queue.popleft()
        
        if url in visited:
            continue
        
        visited.add(url)
        
        # 检查页面
        log(f"📄 检查：{url}")
        result = check_page(url)
        
        if result["status"] != 200:
            audit_results["dead_links"].append({
                "url": url,
                "status": result["status"],
                "error": ", ".join(result["errors"])
            })
        
        # 获取页面链接并加入队列
        if result["status"] == 200:
            links = get_all_links(url)
            for link in links:
                if link not in visited:
                    queue.append(link)
        
        # 每秒最多检查5个页面（避免被封）
        time.sleep(0.2)
        
        # 每检查50个页面输出一次进度
        if audit_results["total_pages"] % 50 == 0:
            log(f"   进度：已检查 {audit_results['total_pages']} 个页面...")
    
    log("=" * 60)
    log("✅ 审计完成！")
    log("=" * 60)

def generate_report():
    """生成审计报告"""
    log("\n📄 生成审计报告...\n")
    
    print("=" * 60)
    print("全站链接审计报告")
    print(f"审计时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"审计网址：{BASE_URL}")
    print("=" * 60)
    
    print(f"\n【统计概览】")
    print(f"  总页面数：{audit_results['total_pages']}")
    print(f"  HTTP 200：{audit_results['http_200']} ✅")
    print(f"  HTTP错误：{audit_results['http_errors']} ❌")
    print(f"  水印正常：{audit_results['watermark_ok']} ✅")
    print(f"  水印缺失：{audit_results['watermark_missing']} ❌")
    
    if audit_results['dead_links']:
        print(f"\n【死链列表】（共{len(audit_results['dead_links'])}个）")
        for i, link in enumerate(audit_results['dead_links'][:20], 1):  # 只显示前20个
            print(f"  {i}. {link['url']}")
            print(f"     状态：{link['status']} | 错误：{link['error']}")
        
        if len(audit_results['dead_links']) > 20:
            print(f"  ... 还有 {len(audit_results['dead_links']) - 20} 个死链未显示")
    else:
        print(f"\n【死链列表】✅ 无死链")
    
    if audit_results['watermark_issues']:
        print(f"\n【水印问题页面】（共{len(audit_results['watermark_issues'])}个）")
        for i, url in enumerate(audit_results['watermark_issues'][:10], 1):
            print(f"  {i}. {url}")
        
        if len(audit_results['watermark_issues']) > 10:
            print(f"  ... 还有 {len(audit_results['watermark_issues']) - 10} 个页面未显示")
    else:
        print(f"\n【水印检查】✅ 全站水印正常")
    
    print("\n" + "=" * 60)
    
    # 保存报告到文件
    report_path = "C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/audit_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("全站链接审计报告\n")
        f.write(f"审计时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"审计网址：{BASE_URL}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"【统计概览】\n")
        f.write(f"  总页面数：{audit_results['total_pages']}\n")
        f.write(f"  HTTP 200：{audit_results['http_200']}\n")
        f.write(f"  HTTP错误：{audit_results['http_errors']}\n")
        f.write(f"  水印正常：{audit_results['watermark_ok']}\n")
        f.write(f"  水印缺失：{audit_results['watermark_missing']}\n\n")
        
        if audit_results['dead_links']:
            f.write(f"【死链列表】（共{len(audit_results['dead_links'])}个）\n")
            for i, link in enumerate(audit_results['dead_links'], 1):
                f.write(f"  {i}. {link['url']}\n")
                f.write(f"     状态：{link['status']} | 错误：{link['error']}\n")
        
        if audit_results['watermark_issues']:
            f.write(f"\n【水印问题页面】（共{len(audit_results['watermark_issues'])}个）\n")
            for i, url in enumerate(audit_results['watermark_issues'], 1):
                f.write(f"  {i}. {url}\n")
    
    log(f"✅ 报告已保存：{report_path}")

if __name__ == "__main__":
    log("全站链接审计脚本 v1.0")
    log(f"水印矩阵：{WATERMARK}")
    log(f"作者：{AUTHOR}")
    log(f"知识产权：{COPYRIGHT}\n")
    
    # 1. 爬取全站
    crawl_site()
    
    # 2. 生成报告
    generate_report()
