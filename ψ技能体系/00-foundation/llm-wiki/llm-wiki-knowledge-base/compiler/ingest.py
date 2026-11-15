# -*- coding: utf-8 -*-
# LLM Wiki 知识编译器 - 录入模块
# 龙心 OS · 2026-04-16

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime

# 基础路径
BASE_DIR = Path(r"C:\Users\jia'yue\.agents\skills\llm-wiki-knowledge-base")
LAYER1_RAW = BASE_DIR / "architecture" / "layer1-raw"
LAYER2_WIKI = BASE_DIR / "architecture" / "layer2-wiki"
LAYER3_SCHEMA = BASE_DIR / "architecture" / "layer3-schema"

def ensure_dirs():
    """确保目录存在"""
    for d in [LAYER1_RAW, LAYER2_WIKI, LAYER3_SCHEMA]:
        d.mkdir(parents=True, exist_ok=True)
    print("✓ 目录结构检查完成")

def save_raw(content, source_url=None, source_type="article"):
    """
    保存原始资料到 Layer 1
    
    Args:
        content: 原始内容
        source_url: 来源 URL
        source_type: 类型 (article/paper/code/dataset)
    
    Returns:
        raw_path: 保存路径
        raw_hash: 内容哈希
    """
    # 创建子目录
    raw_dir = LAYER1_RAW / source_type
    raw_dir.mkdir(exist_ok=True)
    
    # 生成文件名（基于内容哈希）
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{content_hash}.md"
    
    # 保存文件
    raw_path = raw_dir / filename
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(f"# 原始资料\n\n")
        f.write(f"**来源**: {source_url or '未知'}\n")
        f.write(f"**类型**: {source_type}\n")
        f.write(f"**归档时间**: {datetime.now().isoformat()}\n")
        f.write(f"**内容哈希**: {content_hash}\n\n")
        f.write("---\n\n")
        f.write(content)
    
    print(f"✓ 原始资料已保存：{raw_path}")
    return raw_path, content_hash

def extract_concepts(content):
    """
    从内容中提取核心概念
    
    TODO: 使用 LLM 提取
    当前为简化版本，提取标题和关键词
    
    Args:
        content: 文档内容
    
    Returns:
        concepts: 概念列表
    """
    concepts = []
    
    # 提取标题
    lines = content.split('\n')
    for line in lines[:10]:
        if line.startswith('# '):
            concepts.append({
                'name': line[2:].strip(),
                'type': 'title'
            })
    
    # 提取关键词（简化：提取加粗文本）
    import re
    bold_texts = re.findall(r'\*\*(.+?)\*\*', content)
    for text in bold_texts[:5]:
        concepts.append({
            'name': text,
            'type': 'keyword'
        })
    
    # 去重
    seen = set()
    unique_concepts = []
    for c in concepts:
        if c['name'] not in seen:
            seen.add(c['name'])
            unique_concepts.append(c)
    
    return unique_concepts[:5]  # 限制 5 个核心概念

def generate_entity_page(concept, content, source_path):
    """
    生成实体页面
    
    Args:
        concept: 概念信息
        content: 原始内容
        source_path: 原始资料路径
    
    Returns:
        wiki_path: Wiki 页面路径
    """
    wiki_dir = LAYER2_WIKI / "entities"
    wiki_dir.mkdir(exist_ok=True)
    
    # 生成文件名
    entity_name = concept['name'].replace(' ', '_').replace('/', '_')
    filename = f"{entity_name}.md"
    wiki_path = wiki_dir / filename
    
    # 生成页面内容
    page_content = f"""# {concept['name']}

> 📌 实体页面 · 自动生成

**类型**: {concept.get('type', 'concept')}  
**创建时间**: {datetime.now().isoformat()}  
**来源**: [{source_path.name}]({source_path})

---

## 定义

{content[:500]}...

---

## 相关内容

<!-- 双向链接 -->
- [[相关概念 1]]
- [[相关概念 2]]
- [[相关概念 3]]

---

## 参考资料

- 来源：{source_path}

---

_创建：{datetime.now().strftime('%Y-%m-%d')} · LLM Wiki 知识编译器 v1.0_
"""
    
    with open(wiki_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    print(f"✓ 实体页面已生成：{wiki_path}")
    return wiki_path

def generate_concept_page(concept, related_concepts):
    """
    生成概念页面
    
    Args:
        concept: 概念信息
        related_concepts: 相关概念列表
    
    Returns:
        wiki_path: Wiki 页面路径
    """
    wiki_dir = LAYER2_WIKI / "concepts"
    wiki_dir.mkdir(exist_ok=True)
    
    # 生成文件名
    concept_name = concept['name'].replace(' ', '_').replace('/', '_')
    filename = f"{concept_name}.md"
    wiki_path = wiki_dir / filename
    
    # 生成页面内容
    links = '\n'.join([f"- [[{c['name']}]]" for c in related_concepts[:3]])
    
    page_content = f"""# {concept['name']}

> 💡 概念页面 · 自动生成

**类型**: {concept.get('type', 'concept')}  
**创建时间**: {datetime.now().isoformat()}

---

## 核心定义

<!-- 由 LLM 填充核心定义 -->

---

## 相关概念

{links or '- 暂无相关链接'}

---

## 应用场景

<!-- 由 LLM 填充应用场景 -->

---

_创建：{datetime.now().strftime('%Y-%m-%d')} · LLM Wiki 知识编译器 v1.0_
"""
    
    with open(wiki_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    print(f"✓ 概念页面已生成：{wiki_path}")
    return wiki_path

def ingest_document(content, source_url=None, source_type="article"):
    """
    完整录入流程
    
    Args:
        content: 文档内容
        source_url: 来源 URL
        source_type: 类型
    
    Returns:
        result: 编译结果
    """
    print("=" * 60)
    print("  LLM Wiki 知识编译器 - 录入流程")
    print("=" * 60)
    print("")
    
    # Step 1: 保存原始资料
    print("Step 1: 保存原始资料到 Layer 1")
    raw_path, raw_hash = save_raw(content, source_url, source_type)
    print("")
    
    # Step 2: 提取核心概念
    print("Step 2: 提取核心概念")
    concepts = extract_concepts(content)
    print(f"  提取到 {len(concepts)} 个核心概念:")
    for c in concepts:
        print(f"    - {c['name']} ({c['type']})")
    print("")
    
    # Step 3: 生成 Wiki 页面
    print("Step 3: 生成 Wiki 页面")
    wiki_pages = []
    
    # 生成实体页面
    for concept in concepts[:2]:  # 前 2 个作为实体
        wiki_path = generate_entity_page(concept, content, raw_path)
        wiki_pages.append(wiki_path)
    
    # 生成概念页面
    for concept in concepts[2:]:  # 其余作为概念
        wiki_path = generate_concept_page(concept, concepts)
        wiki_pages.append(wiki_path)
    
    print("")
    
    # Step 4: 更新索引
    print("Step 4: 更新索引")
    index_path = LAYER2_WIKI / "INDEX.md"
    update_index(wiki_pages)
    print("")
    
    # 输出结果
    print("=" * 60)
    print("  编译完成")
    print("=" * 60)
    print(f"  原始资料：{raw_path}")
    print(f"  Wiki 页面：{len(wiki_pages)} 个")
    print(f"  核心概念：{len(concepts)} 个")
    print("")
    
    return {
        'raw_path': str(raw_path),
        'raw_hash': raw_hash,
        'wiki_pages': [str(p) for p in wiki_pages],
        'concepts': concepts
    }

def update_index(wiki_pages):
    """
    更新 Wiki 索引
    
    Args:
        wiki_pages: Wiki 页面列表
    """
    index_path = LAYER2_WIKI / "INDEX.md"
    
    # 读取现有索引
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
    else:
        index_content = "# LLM Wiki 索引\n\n> 自动生成的知识索引\n\n---\n\n## 页面列表\n\n"
    
    # 添加新页面
    for page in wiki_pages:
        page_name = page.name.replace('.md', '')
        index_content += f"- [[{page_name}]]\n"
    
    # 保存索引
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✓ 索引已更新：{index_path}")

if __name__ == "__main__":
    # 测试
    ensure_dirs()
    
    # 示例内容
    test_content = """
# React Query 核心概念

React Query 是一个强大的 **数据获取库**，用于 React 应用。

## 核心特性

- **自动缓存**: 自动管理查询缓存
- **背景更新**: 智能背景数据更新
- **乐观更新**: 乐观 UI 更新支持

## 使用场景

适用于需要频繁获取和更新服务器数据的应用。
"""
    
    result = ingest_document(test_content, "https://tanstack.com/query", "article")
    print(json.dumps(result, ensure_ascii=False, indent=2))
