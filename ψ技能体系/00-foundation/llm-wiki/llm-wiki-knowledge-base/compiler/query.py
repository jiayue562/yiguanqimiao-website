# -*- coding: utf-8 -*-
# LLM Wiki 知识编译器 - 查询调用模块
# 龙心 OS · 2026-04-16

import os, re, json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\jia'yue\.agents\skills\llm-wiki-knowledge-base")
LAYER2_WIKI = BASE_DIR / "architecture" / "layer2-wiki"

def query_by_name(name):
    """
    通过概念名查询 Wiki 页面

    Args:
        name: 概念名

    Returns:
        page: 页面内容 dict 或 None
    """
    # 精确匹配
    for f in LAYER2_WIKI.glob(f"**/{name}.md"):
        return _load_page(f)

    # 模糊匹配
    for f in LAYER2_WIKI.glob("**/*.md"):
        stem = f.stem
        if name.lower() in stem.lower():
            return _load_page(f)

    return None

def _load_page(path):
    """加载单个页面"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    links = re.findall(r"\[\[(.+?)\]\]", content)
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)

    return {
        "path": str(path),
        "name": path.stem,
        "title": title_match.group(1) if title_match else path.stem,
        "content": content,
        "links": links,
        "link_count": len(links),
    }

def query_by_tag(tag):
    """
    通过标签查询

    Args:
        tag: 标签名（不含 #）

    Returns:
        pages: 匹配页面列表
    """
    results = []
    for f in LAYER2_WIKI.glob("**/*.md"):
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        if f"#{tag}" in content:
            results.append(_load_page(f))
    return results

def query_related(name, max_depth=2):
    """
    查询某概念的关联网络

    Args:
        name: 概念名
        max_depth: 最大遍历深度

    Returns:
        network: 关联网络 dict
    """
    visited = set()
    network = {"nodes": [], "edges": []}

    def traverse(current, depth=0):
        if current in visited or depth > max_depth:
            return
        visited.add(current)

        page = query_by_name(current)
        if not page:
            return

        network["nodes"].append({"name": current, "depth": depth})
        for link in page["links"]:
            network["edges"].append({"from": current, "to": link})
            traverse(link, depth + 1)

    traverse(name)
    return network

def query_index():
    """
    查询完整索引

    Returns:
        index: 索引数据
    """
    index_path = LAYER2_WIKI / "INDEX.md"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return {"path": str(index_path), "content": f.read()}
    return None

def search_keyword(keyword):
    """
    关键词搜索（全库扫描）

    Args:
        keyword: 搜索关键词

    Returns:
        results: 匹配页面列表
    """
    results = []
    for f in LAYER2_WIKI.glob("**/*.md"):
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        if keyword.lower() in content.lower():
            page = _load_page(f)
            # 提取上下文
            idx = content.lower().find(keyword.lower())
            start = max(0, idx - 40)
            end = min(len(content), idx + len(keyword) + 40)
            page["context"] = content[start:end]
            results.append(page)
    return results

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "index"

    if cmd == "index":
        idx = query_index()
        print(idx["content"] if idx else "索引不存在")
    elif cmd == "search" and len(sys.argv) > 2:
        results = search_keyword(sys.argv[2])
        for r in results[:10]:
            print(f"  [{r['name']}] {r.get('context', '')[:60]}...")
    elif cmd in ("related", "rel") and len(sys.argv) > 2:
        net = query_related(sys.argv[2])
        print(f"节点: {len(net['nodes'])}, 边: {len(net['edges'])}")
        for n in net["nodes"]:
            print(f"  {'  ' * n['depth']}{n['name']}")
