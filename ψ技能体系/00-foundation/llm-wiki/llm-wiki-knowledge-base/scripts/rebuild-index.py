# -*- coding: utf-8 -*-
# LLM Wiki 重建索引脚本
# 龙心 OS · 2026-04-16

import os
import re
from pathlib import Path
from datetime import datetime

# 基础路径
BASE_DIR = Path(r"C:\Users\jia'yue\.agents\skills\llm-wiki-knowledge-base")
LAYER2_WIKI = BASE_DIR / "architecture" / "layer2-wiki"

def rebuild_index():
    """
    重建 Wiki 索引
    """
    print("=" * 60)
    print("  LLM Wiki 重建索引")
    print("=" * 60)
    print("")
    
    # 扫描所有页面
    wiki_files = list(LAYER2_WIKI.glob("**/*.md"))
    total_pages = len(wiki_files)
    
    print(f"Step 1: 扫描页面")
    print("-" * 40)
    print(f"  总页面数：{total_pages}")
    print("")
    
    if total_pages == 0:
        print("  ⚠️ Wiki 为空，无法重建索引")
        return
    
    # 提取概念和链接
    print(f"Step 2: 提取概念和链接")
    print("-" * 40)
    
    concept_index = {}  # 概念名 → 页面列表
    link_graph = {}     # 页面 → 相关链接
    
    for f in wiki_files:
        page_name = f.stem
        
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取标题作为主概念
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            if title not in concept_index:
                concept_index[title] = []
            concept_index[title].append(page_name)
        
        # 提取双向链接
        links = re.findall(r'\[\[(.+?)\]\]', content)
        link_graph[page_name] = links
        
        # 添加到链接索引
        for link in links:
            if link not in concept_index:
                concept_index[link] = []
            concept_index[link].append(page_name)
    
    print(f"  概念数：{len(concept_index)}")
    print(f"  链接关系：{sum(len(v) for v in link_graph.values())}")
    print("")
    
    # 生成索引文件
    print(f"Step 3: 生成索引文件")
    print("-" * 40)
    
    index_path = LAYER2_WIKI / "INDEX.md"
    
    index_content = f"""# LLM Wiki 索引

> 📚 自动生成的知识索引 · 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}

**总页面数**: {total_pages}  
**概念数**: {len(concept_index)}  
**链接关系**: {sum(len(v) for v in link_graph.values())}

---

## 概念索引

"""
    
    # 按字母顺序排列概念
    sorted_concepts = sorted(concept_index.keys())
    
    for concept in sorted_concepts:
        pages = concept_index[concept]
        page_links = ', '.join([f"[[{p}]]" for p in set(pages)])
        index_content += f"### {concept}\n\n{page_links}\n\n"
    
    index_content += f"""---

## 页面列表

"""
    
    # 按字母顺序排列页面
    sorted_pages = sorted(link_graph.keys())
    
    for page in sorted_pages:
        index_content += f"- [[{page}]]\n"
    
    index_content += f"""
---

## 链接图谱

"""
    
    # 显示高连接度页面
    page_link_counts = [(p, len(links)) for p, links in link_graph.items()]
    page_link_counts.sort(key=lambda x: x[1], reverse=True)
    
    index_content += "| 页面 | 链接数 |\n|------|--------|\n"
    for page, count in page_link_counts[:20]:
        index_content += f"| [[{page}]] | {count} |\n"
    
    index_content += f"""
---

_索引生成：{datetime.now().strftime('%Y-%m-%d %H:%M')} · LLM Wiki 知识编译器 v1.0_
"""
    
    # 保存索引
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✓ 索引已重建：{index_path}")
    print("")
    
    # 保存链接图谱（JSON 格式）
    print(f"Step 4: 保存链接图谱")
    print("-" * 40)
    
    import json
    graph_path = LAYER2_WIKI / "link-graph.json"
    
    graph_data = {
        'updated_at': datetime.now().isoformat(),
        'total_pages': total_pages,
        'concepts': len(concept_index),
        'link_graph': link_graph
    }
    
    with open(graph_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 链接图谱已保存：{graph_path}")
    print("")
    
    print("=" * 60)
    print("  索引重建完成")
    print("=" * 60)
    print(f"  总页面数：{total_pages}")
    print(f"  概念数：{len(concept_index)}")
    print(f"  索引文件：{index_path}")
    print(f"  图谱文件：{graph_path}")
    print("")

if __name__ == "__main__":
    rebuild_index()
