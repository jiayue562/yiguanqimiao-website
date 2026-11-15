# -*- coding: utf-8 -*-
# LLM Wiki 知识编译器 - 健康检查模块
# 龙心 OS · 2026-04-16

import os
import re
from pathlib import Path
from datetime import datetime, timedelta

# 基础路径
BASE_DIR = Path(r"C:\Users\jia'yue\.agents\skills\llm-wiki-knowledge-base")
LAYER2_WIKI = Path.home() / '.OpcClaw 知识库' / 'knowledge-base'

def check_wiki_health():
    """
    检查 Wiki 健康状态
    
    Returns:
        report: 健康检查报告
    """
    print("=" * 60)
    print("  LLM Wiki 健康检查")
    print("=" * 60)
    print("")
    
    # 统计文件
    wiki_files = list(LAYER2_WIKI.glob("**/*.md"))
    total_pages = len(wiki_files)
    
    print(f"1. 基础统计:")
    print("-" * 40)
    print(f"  总页面数：{total_pages}")
    print("")
    
    if total_pages == 0:
        print("  WARN Wiki 为空，请先录入知识")
        return
    
    # 检查链接
    print(f"2. 链接检查:")
    print("-" * 40)
    pages_with_links = 0
    orphan_pages = []
    total_links = 0
    
    for f in wiki_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 查找双向链接 [[xxx]]
        links = re.findall(r'\[\[(.+?)\]\]', content)
        link_count = len(links)
        total_links += link_count
        
        if link_count > 0:
            pages_with_links += 1
        else:
            orphan_pages.append(f.name)
    
    link_rate = (pages_with_links / total_pages) * 100
    orphan_rate = (len(orphan_pages) / total_pages) * 100
    avg_links = total_links / total_pages
    
    print(f"  有链接页面：{pages_with_links}/{total_pages} ({link_rate:.1f}%)")
    print(f"  孤立页面：{len(orphan_pages)} ({orphan_rate:.1f}%)")
    print(f"  平均链接数：{avg_links:.1f} 个/页面")
    print("")
    
    # 健康评估
    print(f"3. 健康评估:")
    print("-" * 40)
    
    issues = []
    
    # 链接率检查
    if link_rate >= 80:
        print(f"  OK 链接率：{link_rate:.1f}% (目标>80%)")
    else:
        print(f"  WARN 链接率：{link_rate:.1f}% (目标>80%)")
        issues.append(f"链接率过低 ({link_rate:.1f}%)")
    
    # 孤立率检查
    if orphan_rate <= 5:
        print(f"  OK 孤立率：{orphan_rate:.1f}% (目标<5%)")
    else:
        print(f"  WARN 孤立率：{orphan_rate:.1f}% (目标<5%)")
        issues.append(f"孤立页面过多 ({orphan_rate:.1f}%)")
    
    # 平均链接数检查
    if avg_links >= 3:
        print(f"  OK 平均链接数：{avg_links:.1f} (目标≥3)")
    else:
        print(f"  WARN 平均链接数：{avg_links:.1f} (目标≥3)")
        issues.append(f"平均链接数不足 ({avg_links:.1f})")
    
    print("")
    
    # 孤立页面列表
    if orphan_pages:
        print(f"4. 孤立页面列表:")
        print("-" * 40)
        for page in orphan_pages[:10]:  # 显示前 10 个
            print(f"  - {page}")
        if len(orphan_pages) > 10:
            print(f"  ... 还有 {len(orphan_pages) - 10} 个")
        print("")
    
    # 修复建议
    if issues:
        print(f"5. 修复建议:")
        print("-" * 40)
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("")
        print("  建议操作:")
        if link_rate < 80:
            print("  - 为页面添加双向链接")
        if orphan_rate > 5:
            print("  - 为孤立页面建立链接")
        if avg_links < 3:
            print("  - 增加页面间关联")
    else:
        print(f"5. 健康状态:")
        print("-" * 40)
        print("  OK 所有指标正常")
    
    print("")
    print("=" * 60)
    print("  检查完成")
    print("=" * 60)
    
    # 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_pages': total_pages,
        'pages_with_links': pages_with_links,
        'orphan_pages': orphan_pages,
        'link_rate': link_rate,
        'orphan_rate': orphan_rate,
        'avg_links': avg_links,
        'issues': issues,
        'health_score': calculate_health_score(link_rate, orphan_rate, avg_links)
    }
    
    # 保存报告
    save_report(report)
    
    return report

def calculate_health_score(link_rate, orphan_rate, avg_links):
    """
    计算健康分数
    
    Args:
        link_rate: 链接率
        orphan_rate: 孤立率
        avg_links: 平均链接数
    
    Returns:
        score: 0-100 分
    """
    # 链接率权重 40%
    link_score = min(link_rate, 100) * 0.4
    
    # 孤立率权重 30%（反向）
    orphan_score = max(0, (100 - orphan_rate)) * 0.3
    
    # 平均链接数权重 30%
    avg_links_score = min(avg_links / 3 * 100, 100) * 0.3
    
    total_score = link_score + orphan_score + avg_links_score
    return round(total_score, 1)

def save_report(report):
    """
    保存健康检查报告
    
    Args:
        report: 报告数据
    """
    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"health-check_{timestamp}.md"
    
    content = f"""# LLM Wiki 健康检查报告

**检查时间**: {report['timestamp']}  
**健康分数**: {report['health_score']}/100

---

## 基础统计

| 指标 | 数值 |
|------|------|
| 总页面数 | {report['total_pages']} |
| 有链接页面 | {report['pages_with_links']} |
| 孤立页面 | {len(report['orphan_pages'])} |

---

## 健康指标

| 指标 | 数值 | 目标 | 状态 |
|------|------|------|------|
| 链接率 | {report['link_rate']:.1f}% | >80% | {'✅' if report['link_rate'] >= 80 else '⚠️'} |
| 孤立率 | {report['orphan_rate']:.1f}% | <5% | {'✅' if report['orphan_rate'] <= 5 else '⚠️'} |
| 平均链接数 | {report['avg_links']:.1f} | ≥3 | {'✅' if report['avg_links'] >= 3 else '⚠️'} |

---

## 问题列表

{chr(10).join('- ' + issue for issue in report['issues']) or '无'}

---

## 孤立页面

{chr(10).join('- ' + page for page in report['orphan_pages'][:20]) or '无'}

---

_报告生成：{datetime.now().strftime('%Y-%m-%d %H:%M')} · LLM Wiki 健康检查 v1.0_
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] 报告已保存：{report_path}")

if __name__ == "__main__":
    report = check_wiki_health()
    if report:
        print(f"\n健康分数：{report['health_score']}/100")
