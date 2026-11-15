#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
记忆语义检索引擎
基于 embedding 向量相似度的智能记忆检索

版本：v1.0
创建：2026-04-17
"""

import sys
import io

# Windows 编码兼容性
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_ST = True
except ImportError:
    HAS_ST = False
    print("⚠️ 未安装 sentence-transformers，请运行：pip install sentence-transformers scikit-learn")


class MemorySemanticSearch:
    """记忆语义检索引擎"""
    
    def __init__(self, memory_dir: str, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化语义检索引擎
        
        Args:
            memory_dir: 记忆目录路径
            model_name: embedding 模型名称
        """
        self.memory_dir = Path(memory_dir)
        self.model_name = model_name
        self.model = None
        self.memory_embeddings = None
        self.memory_texts = []
        self.memory_metadata = []
        self.embedding_cache_file = Path(memory_dir) / "embedding_cache.json"
        
    def load_model(self):
        """加载 embedding 模型"""
        if not HAS_ST:
            raise ImportError("sentence-transformers 未安装")
        
        print(f"🔍 加载模型：{self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print("✅ 模型加载完成")
        
    def load_memories(self, date_range: Optional[Tuple[str, str]] = None) -> int:
        """
        加载记忆文件
        
        Args:
            date_range: 日期范围 (start_date, end_date)，格式 YYYY-MM-DD
            
        Returns:
            加载的记忆数量
        """
        print(f"📂 加载记忆：{self.memory_dir}")
        
        memory_files = sorted(self.memory_dir.glob("*.md"))
        count = 0
        
        for file_path in memory_files:
            # 跳过缓存文件
            if file_path.name.startswith("embedding_cache"):
                continue
                
            # 日期范围过滤
            if date_range:
                file_date = file_path.stem  # YYYY-MM-DD
                if file_date < date_range[0] or file_date > date_range[1]:
                    continue
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 提取有效内容（跳过 markdown 标题）
                lines = content.split('\n')
                valid_lines = [line for line in lines if not line.startswith('#')]
                text = '\n'.join(valid_lines)
                
                if len(text.strip()) > 50:  # 跳过过短内容
                    self.memory_texts.append(text)
                    self.memory_metadata.append({
                        'file': file_path.name,
                        'date': file_path.stem,
                        'path': str(file_path),
                        'length': len(text)
                    })
                    count += 1
                    
            except Exception as e:
                print(f"⚠️ 读取失败 {file_path.name}: {e}")
                
        print(f"✅ 加载 {count} 个记忆文件")
        return count
        
    def build_embeddings(self, use_cache: bool = True) -> np.ndarray:
        """
        构建记忆 embedding
        
        Args:
            use_cache: 是否使用缓存
            
        Returns:
            embedding 数组
        """
        # 检查缓存
        if use_cache and self.embedding_cache_file.exists():
            print("📦 使用缓存的 embedding")
            return self._load_embeddings_from_cache()
            
        if self.model is None:
            self.load_model()
            
        print(f"🔧 构建 {len(self.memory_texts)} 个记忆的 embedding")
        self.memory_embeddings = self.model.encode(self.memory_texts, show_progress_bar=True)
        
        # 保存缓存
        self._save_embeddings_to_cache()
        
        print(f"✅ Embedding 构建完成，形状：{self.memory_embeddings.shape}")
        return self.memory_embeddings
        
    def _save_embeddings_to_cache(self):
        """保存 embedding 到缓存"""
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'model_name': self.model_name,
            'memory_count': len(self.memory_texts),
            'memories': [
                {
                    'metadata': meta,
                    'embedding': emb.tolist()
                }
                for meta, emb in zip(self.memory_metadata, self.memory_embeddings)
            ]
        }
        
        with open(self.embedding_cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 Embedding 缓存已保存：{self.embedding_cache_file}")
        
    def _load_embeddings_from_cache(self) -> np.ndarray:
        """从缓存加载 embedding"""
        with open(self.embedding_cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
            
        self.memory_metadata = [m['metadata'] for m in cache_data['memories']]
        self.memory_embeddings = np.array([m['embedding'] for m in cache_data['memories']])
        
        print(f"✅ 从缓存加载 {len(self.memory_metadata)} 个 embedding")
        return self.memory_embeddings
        
    def search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.75) -> List[Dict]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            similarity_threshold: 相似度阈值
            
        Returns:
            搜索结果列表
        """
        if self.memory_embeddings is None:
            raise ValueError("请先构建 embedding")
            
        if self.model is None:
            self.load_model()
            
        # 编码查询
        query_embedding = self.model.encode([query])
        
        # 计算余弦相似度
        similarities = cosine_similarity(query_embedding, self.memory_embeddings)[0]
        
        # 过滤和排序
        results = []
        for idx, sim in enumerate(similarities):
            if sim >= similarity_threshold:
                results.append({
                    'metadata': self.memory_metadata[idx],
                    'similarity': float(sim),
                    'preview': self.memory_texts[idx][:200] + '...' if len(self.memory_texts[idx]) > 200 else self.memory_texts[idx]
                })
                
        # 按相似度排序
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:top_k]
        
    def search_and_print(self, query: str, top_k: int = 5):
        """搜索并打印结果"""
        print(f"\n🔍 搜索：{query}\n")
        
        results = self.search(query, top_k=top_k)
        
        if not results:
            print("❌ 未找到相关记忆")
            return
            
        for i, result in enumerate(results, 1):
            print(f"{i}. 相似度：{result['similarity']:.3f} | 文件：{result['metadata']['file']}")
            print(f"   日期：{result['metadata']['date']}")
            print(f"   预览：{result['preview']}")
            print()


def main():
    """主函数 - 测试语义检索"""
    # 配置
    memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    # 创建检索引擎
    searcher = MemorySemanticSearch(str(memory_dir))
    
    # 加载记忆
    searcher.load_memories()
    
    # 构建 embedding
    searcher.build_embeddings()
    
    # 测试搜索
    test_queries = [
        "龙心 OS 架构",
        "思维模型",
        "自主学习",
        "知识治理"
    ]
    
    for query in test_queries:
        searcher.search_and_print(query, top_k=3)


if __name__ == "__main__":
    main()
