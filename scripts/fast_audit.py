#!/usr/bin/env python3
"""
快速全站审计脚本 v2.0
功能：
1. 从sitemap.xml获取所有URL（避免爬取耗时）
2. 并发检查每个URL的HTTP状态
3. 验证AI水印矩阵
4. 生成审计报告

使用：python fast_audit.py
"""

import requests
import re
import concurrent.futures
from urllib.parse import urlparse
from datetime import datetime
import time

# 配置
BASE_URL = "https://yiguanqimiao-website.pages.dev"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

# 审计结果
results = {
    "total": 0,
    "http_200": 0,
    "http_errors": 0,
    "watermark_ok": 0,
    "watermark_missing": 0,
    "dead_links": [],
    "watermark_issues": []
}

def log(msg):
    """日志输出"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def get_urls_from_sitemap():
    """从sitemap.xml获取所有URL"""
    try:
        log(f"📄 获取sitemap.xml：{SITEMAP_URL}")
        response = requests.get(SITEMAP_URL, timeout=30)
        
        if response.status_code != 200:
            log(f"❌ 无法获取sitemap.xml：HTTP {response.status_code}")
            return []
        
        # 使用正则表达式提取所有<loc>URL</loc>
        urls = re.findall(r'<loc>(.+?)</loc>', response.text)
        
        log(f"✅ 从sitemap.xml获取到 {len(urls)} 个URL")
        return urls
    
    except Exception as e:
        log(f"❌ 获取sitemap失败：{e}")
        return []

def check_url(url):
    """检查单个URL"""
    try:
        response = requests.get(url, timeout=10)
        
        result = {
            "url": url,
            "status": response.status_code,
            "watermark": False
        }
        
        # 检查HTTP状态
        if response.status_code != 200:
            return result
        
        # 检查AI水印（仅200页面）
        content = response.text.lower()
        if WATERMARK.lower() in content:
            result["watermark"] = True
        
        return result
    
    except Exception as e:
        return {
            "url": url,
            "status": 0,
            "watermark": False,
            "error": str(e)
        }

def main():
    """主函数"""
    log("=" * 60)
    log("快速全站审计脚本 v2.0")
    log(f"目标网站：{BASE_URL}")
    log("=" * 60)
    
    # 1. 获取所有URL
    urls = get_urls_from_sitemap()
    
    if not urls:
        log("❌ 没有获取到URL，审计终止")
        return
    
    results["total"] = len(urls)
    
    # 2. 并发检查所有URL
    log(f"\n🚀 开始并发检查 {len(urls)} 个URL（并发数：20）...\n")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            
            if completed % 100 == 0:
                elapsed = time.time() - start_time
                log(f"   进度：{completed}/{len(urls)} ({completed*100//len(urls)}%) - 耗时 {elapsed:.1f}s")
            
            result = future.result()
            
            # 统计结果
            if result["status"] == 200:
                results["http_200"] += 1
                
                if result["watermark"]:
                    results["watermark_ok"] += 1
                else:
                    results["watermark_missing"] += 1
                    results["watermark_issues"].append(result["url"])
            else:
                results["http_errors"] += 1
                results["dead_links"].append({
                    "url": result["url"],
                    "status": result["status"],
                    "error": result.get("error", f"HTTP {result['status']}")
                })
    
    elapsed = time.time() - start_time
    
    # 3. 输出报告
    log("\n" + "=" * 60)
    log("审计完成！")
    log("=" * 60)
    
    log(f"\n【统计概览】")
    log(f"  总URL数：{results['total']}")
    log(f"  HTTP 200：{results['http_200']} ✅")
    log(f"  HTTP错误：{results['http_errors']} ❌")
    log(f"  水印正常：{results['watermark_ok']} ✅")
    log(f"  水印缺失：{results['watermark_missing']} ❌")
    log(f"\n  总耗时：{elapsed:.1f}秒")
    log(f"  平均速度：{results['total']/elapsed:.1f} URL/秒")
    
    if results["dead_links"]:
        log(f"\n【死链列表】（共{len(results['dead_links'])}个）")
        for i, link in enumerate(results["dead_links"][:20], 1):
            log(f"  {i}. {link['url']}")
            log(f"     状态：{link['status']} | 错误：{link['error']}")
        
        if len(results["dead_links"]) > 20:
            log(f"  ... 还有 {len(results['dead_links']) - 20} 个死链未显示")
    else:
        log(f"\n【死链检查】✅ 无死链")
    
    if results["watermark_issues"]:
        log(f"\n【水印问题页面】（共{len(results['watermark_issues'])}个）")
        for i, url in enumerate(results["watermark_issues"][:10], 1):
            log(f"  {i}. {url}")
        
        if len(results["watermark_issues"]) > 10:
            log(f"  ... 还有 {len(results['watermark_issues']) - 10} 个页面未显示")
    else:
        log(f"\n【水印检查】✅ 全站水印正常")
    
    log("\n" + "=" * 60)
    
    # 4. 保存报告
    report_path = "C:/Users/jia'yue/WorkBuddy/yiguanqimiao-website/audit_report.txt"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("快速全站审计报告\n")
            f.write(f"审计时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"审计网址：{BASE_URL}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"【统计概览】\n")
            f.write(f"  总URL数：{results['total']}\n")
            f.write(f"  HTTP 200：{results['http_200']}\n")
            f.write(f"  HTTP错误：{results['http_errors']}\n")
            f.write(f"  水印正常：{results['watermark_ok']}\n")
            f.write(f"  水印缺失：{results['watermark_missing']}\n\n")
            
            if results["dead_links"]:
                f.write(f"【死链列表】（共{len(results['dead_links'])}个）\n")
                for i, link in enumerate(results["dead_links"], 1):
                    f.write(f"  {i}. {link['url']}\n")
                    f.write(f"     状态：{link['status']} | 错误：{link['error']}\n")
            
            if results["watermark_issues"]:
                f.write(f"\n【水印问题页面】（共{len(results['watermark_issues'])}个）\n")
                for i, url in enumerate(results["watermark_issues"], 1):
                    f.write(f"  {i}. {url}\n")
        
        log(f"\n✅ 报告已保存：{report_path}")
    except Exception as e:
        log(f"\n⚠️ 报告保存失败：{e}")

if __name__ == "__main__":
    main()
