# -*- coding: utf-8 -*-
# 上下文质量评分器
# 龙心 OS · 2026-04-16

from typing import Dict, List

class ContextScorer:
    """上下文质量评分器"""
    
    def __init__(self):
        self.dimensions = {
            'relevance': self._score_relevance,
            'completeness': self._score_completeness,
            'conciseness': self._score_conciseness,
            'timeliness': self._score_timeliness,
            'consistency': self._score_consistency,
        }
        
        self.weights = {
            'relevance': 0.3,
            'completeness': 0.25,
            'conciseness': 0.2,
            'timeliness': 0.15,
            'consistency': 0.1,
        }
    
    def score(self, context: Dict) -> Dict:
        """
        评分
        
        Args:
            context: 上下文数据
        
        Returns:
            score_result: 评分结果
        """
        dimension_scores = {}
        
        for dim_name, scorer_func in self.dimensions.items():
            score = scorer_func(context)
            dimension_scores[dim_name] = score
        
        # 计算加权总分
        total_score = sum(
            dimension_scores[dim] * self.weights[dim]
            for dim in dimension_scores
        ) * 100
        
        return {
            'total_score': total_score,
            'dimensions': dimension_scores,
            'level': self._get_level(total_score * 100)
        }
    
    def _score_relevance(self, context: Dict) -> float:
        """相关性评分 (0-1)"""
        relevance_tags = context.get('relevance_tags', [])
        if not relevance_tags:
            return 0.5
        
        high_relevance = ['核心', '关键', '必须', '重要']
        high_count = sum(1 for tag in relevance_tags if any(kw in tag for kw in high_relevance))
        
        return min(1.0, 0.5 + (high_count / len(relevance_tags)) * 0.5)
    
    def _score_completeness(self, context: Dict) -> float:
        """完整性评分 (0-1)"""
        content = context.get('content', '')
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
    
    def _score_conciseness(self, context: Dict) -> float:
        """简洁性评分 (0-1)"""
        content = context.get('content', '')
        
        # 冗余信息比例评估
        redundancy_ratio = content.count('的') / len(content) if len(content) > 0 else 0
        
        # 冗余比例越低，简洁性越高
        if redundancy_ratio < 0.05:
            return 1.0
        elif redundancy_ratio < 0.1:
            return 0.8
        elif redundancy_ratio < 0.15:
            return 0.6
        else:
            return 0.4
    
    def _score_timeliness(self, context: Dict) -> float:
        """时效性评分 (0-1)"""
        from datetime import datetime, timedelta
        
        timestamp = context.get('timestamp')
        if not timestamp:
            return 0.5
        
        try:
            if isinstance(timestamp, str):
                ctx_time = datetime.fromisoformat(timestamp)
            else:
                ctx_time = timestamp
            
            age = datetime.now() - ctx_time
            
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
    
    def _score_consistency(self, context: Dict) -> float:
        """一致性评分 (0-1)"""
        # 简化版本：检查是否有冲突标记
        conflicts = context.get('conflicts', [])
        
        if len(conflicts) == 0:
            return 1.0
        else:
            return max(0.0, 1.0 - len(conflicts) * 0.2)
    
    def _get_level(self, score: float) -> str:
        """获取评分等级"""
        if score >= 90:
            return "优秀"
        elif score >= 75:
            return "良好"
        elif score >= 60:
            return "需改进"
        else:
            return "需关注"


def score_context(context: Dict) -> Dict:
    """便捷函数"""
    scorer = ContextScorer()
    return scorer.score(context)


if __name__ == "__main__":
    # 测试
    test_context = {
        'content': '核心目标：构建上下文工程系统。关键功能包括优化、摘要、优先级排序。',
        'keywords': ['核心', '关键', '上下文'],
        'relevance_tags': ['核心目标', '关键功能'],
        'timestamp': None,
        'importance': 'high',
        'conflicts': []
    }
    
    result = score_context(test_context)
    
    print("上下文质量评分:")
    print(f"综合评分：{result['total_score']:.1f}/100 ({result['level']})")
    print("\n维度评分:")
    for dim, score in result['dimensions'].items():
        print(f"  {dim}: {score*100:.0f}%")
