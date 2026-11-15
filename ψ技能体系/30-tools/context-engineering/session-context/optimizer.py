# -*- coding: utf-8 -*-
# 上下文优化器 - 压缩冗余，保留关键信息
# 龙心 OS · 2026-04-16

import re
from typing import List, Dict

class ContextOptimizer:
    """上下文优化器"""
    
    def __init__(self):
        self.key_patterns = [
            r'核心.*',
            r'关键.*',
            r'重要.*',
            r'必须.*',
            r'总结.*',
            r'结论.*',
        ]
    
    def optimize(self, context: str, target_length: int = 1500, preserve_key_info: bool = True) -> str:
        """
        优化上下文
        
        Args:
            context: 原始上下文
            target_length: 目标长度 (tokens)
            preserve_key_info: 是否保留关键信息
        
        Returns:
            optimized_context: 优化后的上下文
        """
        # 1. 分割为段落
        paragraphs = context.split('\n\n')
        
        # 2. 评估每个段落的重要性
        scored_paragraphs = []
        for para in paragraphs:
            score = self._score_paragraph(para, preserve_key_info)
            scored_paragraphs.append((para, score))
        
        # 3. 按重要性排序
        scored_paragraphs.sort(key=lambda x: x[1], reverse=True)
        
        # 4. 选择最重要的段落，直到达到目标长度
        optimized = []
        current_length = 0
        
        for para, score in scored_paragraphs:
            para_length = len(para) // 4  # 估算 token 数
            if current_length + para_length <= target_length:
                optimized.append(para)
                current_length += para_length
        
        # 5. 重新组合
        return '\n\n'.join(optimized)
    
    def _score_paragraph(self, paragraph: str, preserve_key_info: bool) -> float:
        """评估段落重要性"""
        score = 0.0
        
        # 基于位置的分数（开头和结尾更重要）
        # 基于关键词的分数
        if preserve_key_info:
            for pattern in self.key_patterns:
                if re.search(pattern, paragraph, re.IGNORECASE):
                    score += 2.0
        
        # 基于长度的分数（中等长度最佳）
        length = len(paragraph)
        if 100 <= length <= 500:
            score += 1.0
        
        # 基于格式的分数（列表、代码块更重要）
        if '```' in paragraph or '- ' in paragraph or '1. ' in paragraph:
            score += 1.5
        
        return score


def optimize_context(context: str, target_length: int = 1500, preserve_key_info: bool = True) -> str:
    """便捷函数"""
    optimizer = ContextOptimizer()
    return optimizer.optimize(context, target_length, preserve_key_info)


if __name__ == "__main__":
    # 测试
    test_context = """
# 会议记录

## 核心目标
构建上下文工程系统

## 关键决策
1. 采用模块化架构
2. 优先实现核心功能
3. 与现有 Skills 协同

## 重要事项
- 必须保证质量
- 需要定期优化
- 保持文档更新

## 讨论内容
这里是一些详细的讨论内容，包含了很多细节信息...
（此处省略 1000 字）

## 结论
上下文工程是核心能力，需要优先发展
"""
    
    optimized = optimize_context(test_context, target_length=200)
    print("原始长度:", len(test_context))
    print("优化后长度:", len(optimized))
    print("\n优化结果:")
    print(optimized)
