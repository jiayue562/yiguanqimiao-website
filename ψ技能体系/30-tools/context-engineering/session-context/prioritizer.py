# -*- coding: utf-8 -*-
# 上下文优先级排序器 - 智能排序上下文重要性
# 龙心 OS · 2026-04-16

from typing import List, Dict
from datetime import datetime, timedelta

class ContextPrioritizer:
    """上下文优先级排序器"""
    
    def __init__(self):
        self.default_weights = {
            'relevance': 0.4,      # 相关性
            'recency': 0.3,        # 时效性
            'importance': 0.2,     # 重要性
            'completeness': 0.1,   # 完整性
        }
    
    def prioritize(self, contexts: List[Dict], criteria: List[str] = None, weights: Dict[str, float] = None) -> List[Dict]:
        """
        优先级排序
        
        Args:
            contexts: 上下文列表
            criteria: 排序标准
            weights: 权重配置
        
        Returns:
            ranked_contexts: 排序后的上下文
        """
        if criteria is None:
            criteria = ['relevance', 'recency', 'importance']
        
        if weights is None:
            weights = self.default_weights
        
        # 计算每个上下文的综合分数
        scored_contexts = []
        for ctx in contexts:
            score = self._calculate_score(ctx, criteria, weights)
            scored_contexts.append({
                **ctx,
                'score': score
            })
        
        # 按分数降序排序
        scored_contexts.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_contexts
    
    def _calculate_score(self, context: Dict, criteria: List[str], weights: Dict[str, float]) -> float:
        """计算综合分数"""
        total_score = 0.0
        total_weight = 0.0
        
        for criterion in criteria:
            if criterion == 'relevance':
                score = self._score_relevance(context)
            elif criterion == 'recency':
                score = self._score_recency(context)
            elif criterion == 'importance':
                score = self._score_importance(context)
            elif criterion == 'completeness':
                score = self._score_completeness(context)
            else:
                score = 0.5  # 默认分数
            
            weight = weights.get(criterion, 0.25)
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _score_relevance(self, context: Dict) -> float:
        """相关性评分 (0-1)"""
        # 基于关键词匹配
        keywords = context.get('keywords', [])
        relevance_tags = context.get('relevance_tags', [])
        
        if len(relevance_tags) == 0:
            return 0.5
        
        # 高相关性标签
        high_relevance = ['核心', '关键', '必须', '重要']
        high_count = sum(1 for tag in relevance_tags if any(kw in tag for kw in high_relevance))
        
        return min(1.0, 0.5 + (high_count / len(relevance_tags)) * 0.5)
    
    def _score_recency(self, context: Dict) -> float:
        """时效性评分 (0-1)"""
        timestamp = context.get('timestamp')
        
        if not timestamp:
            return 0.5
        
        try:
            if isinstance(timestamp, str):
                ctx_time = datetime.fromisoformat(timestamp)
            else:
                ctx_time = timestamp
            
            now = datetime.now()
            age = now - ctx_time
            
            # 24 小时内：1.0
            # 3 天内：0.8
            # 7 天内：0.6
            # 30 天内：0.4
            # 超过 30 天：0.2
            
            if age < timedelta(hours=24):
                return 1.0
            elif age < timedelta(days=3):
                return 0.8
            elif age < timedelta(days=7):
                return 0.6
            elif age < timedelta(days=30):
                return 0.4
            else:
                return 0.2
        except:
            return 0.5
    
    def _score_importance(self, context: Dict) -> float:
        """重要性评分 (0-1)"""
        importance = context.get('importance', 'medium')
        
        importance_map = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.5,
            'low': 0.3,
            'trivial': 0.1
        }
        
        return importance_map.get(importance, 0.5)
    
    def _score_completeness(self, context: Dict) -> float:
        """完整性评分 (0-1)"""
        content = context.get('content', '')
        
        if not content:
            return 0.0
        
        # 基于内容长度评估完整性
        length = len(content)
        
        if length >= 500:
            return 1.0
        elif length >= 200:
            return 0.8
        elif length >= 100:
            return 0.6
        elif length >= 50:
            return 0.4
        else:
            return 0.2


def prioritize(contexts: List[Dict], criteria: List[str] = None, weights: Dict[str, float] = None) -> List[Dict]:
    """便捷函数"""
    prioritizer = ContextPrioritizer()
    return prioritizer.prioritize(contexts, criteria, weights)


if __name__ == "__main__":
    # 测试
    test_contexts = [
        {
            'content': '核心目标：构建上下文工程系统',
            'timestamp': datetime.now().isoformat(),
            'importance': 'high',
            'keywords': ['核心', '目标'],
            'relevance_tags': ['核心目标']
        },
        {
            'content': '讨论细节：一些详细的讨论内容',
            'timestamp': (datetime.now() - timedelta(days=5)).isoformat(),
            'importance': 'medium',
            'keywords': ['讨论'],
            'relevance_tags': ['细节']
        },
        {
            'content': '结论：上下文工程是核心能力',
            'timestamp': datetime.now().isoformat(),
            'importance': 'critical',
            'keywords': ['结论', '核心'],
            'relevance_tags': ['核心结论']
        },
    ]
    
    ranked = prioritize(test_contexts)
    
    print("优先级排序结果:")
    for i, ctx in enumerate(ranked, 1):
        print(f"{i}. 分数：{ctx['score']:.2f} - {ctx['content'][:50]}")
