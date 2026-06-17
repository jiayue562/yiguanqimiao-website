# -*- coding: utf-8 -*-
"""
知识库链接完整性验证器
功能:
  - 扫描所有 .md 文件
  - 提取所有 [[链接]]
  - 验证目标文件是否存在
  - 统计链接率/孤立率/网络密度
  - 生成验证报告
"""
import os, re, sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\以观其妙书院知识库\以观其妙书院")
REPORT_DIR = VAULT / "00-索引与导航" / "知识图谱"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def scan_vault():
    """扫描 vault 生成文件清单和链接数据"""
    all_files = {}
    link_data = defaultdict(list)
    orphan_candidates = set()
    error_links = []
    stats = {
        "total_files": 0,
        "total_links": 0,
        "files_with_links": 0,
        "files_without_links": 0,
        "invalid_links": 0,
        "max_links": 0, "max_links_file": "",
        "broken_links": 0,
    }

    print("=" * 60)
    print("  知识库链接完整性验证")
    print("=" * 60)
    print(f"  扫描路径: {VAULT}")
    print()

    # Phase 1: 扫描所有文件和链接
    for p in VAULT.rglob("*.md"):
        if ".trash" in p.parts or ".git" in p.parts:
            continue
        rel = p.relative_to(VAULT)
        name = p.stem
        all_files[name] = str(rel)
        all_files[str(rel)] = str(rel)

        try:
            content = p.read_text(encoding="utf-8")
        except:
            continue

        links = re.findall(r"\[\[(.+?)\]\]", content)
        cleaned = []
        for link in links:
            # 处理别名 [[file|alias]]
            target = link.split("|")[0].split("#")[0].strip()
            if target:
                cleaned.append(target)

        stats["total_files"] += 1
        stats["total_links"] += len(cleaned)

        if cleaned:
            stats["files_with_links"] += 1
            if len(cleaned) > stats["max_links"]:
                stats["max_links"] = len(cleaned)
                stats["max_links_file"] = str(rel)
            link_data[str(rel)] = cleaned
            for target in cleaned:
                if target not in all_files:
                    error_links.append((str(rel), target))
        else:
            stats["files_without_links"] += 1
            orphan_candidates.add(str(rel))

    stats["invalid_links"] = len(error_links)

    # Phase 2: 构建反向链接
    backlinks = defaultdict(list)
    for src, targets in link_data.items():
        for t in targets:
            backlinks[t].append(src)

    # Phase 3: 统计孤立页面（有入链才算连接）
    connected = set()
    for src in link_data:
        connected.add(src)
        for t in link_data[src]:
            connected.add(t)

    orphans = [f for f in all_files.values()
               if f not in connected and f.endswith(".md")
               and not f.startswith("_") and ".trash" not in f]

    # 输出
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总链接数: {stats['total_links']}")
    print(f"  有链接文件: {stats['files_with_links']}")
    print(f"  无链接文件: {stats['files_without_links']}")
    print(f"  无效链接: {stats['invalid_links']}")
    print(f"  孤立页面（无入链）: {len(orphans)}")
    print(f"  最大链接文件: {stats['max_links_file']} ({stats['max_links']} links)")
    print()

    # 计算网络密度
    if stats["total_files"] > 1:
        max_possible = stats["total_files"] * (stats["total_files"] - 1)
        density = (stats["total_links"] / max_possible) * 100 if max_possible > 0 else 0
    else:
        density = 0

    avg_links = stats["total_links"] / stats["total_files"] if stats["total_files"] > 0 else 0
    link_rate = (stats["files_with_links"] / stats["total_files"]) * 100 if stats["total_files"] > 0 else 0

    # 生成报告
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""# 链接验证报告

**生成时间**: {now}
**扫描路径**: {VAULT}

---

## 基础统计

| 指标 | 数值 |
|------|------|
| 总文件数 | {stats["total_files"]} |
| 总链接数 | {stats["total_links"]} |
| 有链接文件 | {stats["files_with_links"]} |
| 无链接文件 | {stats["files_without_links"]} |
| 无效链接 | {stats["invalid_links"]} |
| 孤立页面 | {len(orphans)} |

## 网络指标

| 指标 | 数值 | 评级 |
|------|------|------|
| 链接率 | {link_rate:.1f}% | {'✅' if link_rate >= 80 else '⚠️'} |
| 平均链接数 | {avg_links:.1f} | {'✅' if avg_links >= 3 else '⚠️'} |
| 网络密度 | {density:.4f}% | {'✅' if density >= 0.1 else '⚠️'} |
| 孤立率 | {(len(orphans)/stats["total_files"])*100:.1f}% | {'✅' if len(orphans)/max(stats["total_files"],1)*100 < 5 else '⚠️'} |

## 无效链接（目标不存在）

"""
    for src, target in error_links[:50]:
        report += f"- [{target}] ← {src}\n"

    if stats["invalid_links"] > 50:
        report += f"- ... 还有 {stats['invalid_links'] - 50} 个\n"

    report += f"""\n## 孤立页面（无入链）\n\n"""
    for o in orphans[:30]:
        report += f"- [[{Path(o).stem}]] ({o})\n"

    report += f"""\n## 反向链接密度 Top 10\n\n| 页面 | 入链数 |\n|------|--------|\n"""
    sorted_bl = sorted(backlinks.items(), key=lambda x: -len(x[1]))[:10]
    for page, sources in sorted_bl:
        report += f"| [[{Path(page).stem}]] | {len(sources)} |\n"

    report += f"""\n---

_验证完成: {now} · 以观其妙书院知识库_
"""

    # 保存报告
    report_path = REPORT_DIR / f"link-validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  报告已保存: {report_path}")
    print()

    # 保存 JSON 数据供其他工具使用
    data = {
        "timestamp": now,
        "stats": stats,
        "orphans": orphans[:100],
        "error_links": error_links[:100],
        "network_density": density,
        "link_rate": link_rate,
        "avg_links": avg_links,
    }
    import json
    (REPORT_DIR / "link-data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 健康评分
    score = min(
        min(link_rate / 80, 1) * 40 +
        max(0, min((100 - len(orphans)/max(stats["total_files"],1)*100) / 5, 1)) * 30 +
        min(avg_links / 3, 1) * 30,
        100
    )
    print(f"  健康评分: {score:.1f}/100")

    if score >= 85:
        print("  状态: 优秀")
    elif score >= 70:
        print("  状态: 良好")
    elif score >= 55:
        print("  状态: 需改进")
    else:
        print("  状态: 需关注")

    return score

if __name__ == "__main__":
    scan_vault()
