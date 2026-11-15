# -*- coding: utf-8 -*-
# 上下文摘要器 - 自动生成会话摘要
# 龙心 OS · 2026-04-16

from typing import List, Dict
from datetime import datetime

class ContextSummarizer:
    """上下文摘要器"""
    
    def __init__(self):
        self.summary_styles = {
            'bullet': self._bullet_summary,
            'paragraph': self._paragraph_summary,
            'timeline': self._timeline_summary,
        }
    
    def summarize(self, conversation: List[Dict], max_length: int = 500, style: str = 'bullet') -> str:
        """
        生成会话摘要
        
        Args:
            conversation: 对话历史列表
            max_length: 最大长度
            style: 摘要风格 (bullet/paragraph/timeline)
        
        Returns:
            summary: 会话摘要
        """
        # 1. 提取关键信息
        key_points = self._extract_key_points(conversation)
        
        # 2. 选择摘要风格
        summarizer_func = self.summary_styles.get(style, self._bullet_summary)
        summary = summarizer_func(key_points, max_length)
        
        return summary
    
    def _extract_key_points(self, conversation: List[Dict]) -> List[Dict]:
        """提取关键要点"""
        key_points = []
        
        for msg in conversation:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            # 提取关键信息
            if any(keyword in content.lower() for keyword in ['核心', '关键', '重要', '总结', '结论']):
                key_points.append({
                    'role': role,
                    'content': content[:200],  # 限制长度
                    'importance': 'high'
                })
            elif len(content) > 100:  # 长消息可能包含重要信息
                key_points.append({
                    'role': role,
                    'content': content[:200],
                    'importance': 'medium'
                })
        
        return key_points
    
    def _bullet_summary(self, key_points: List[Dict], max_length: int) -> str:
        """列表式摘要"""
        summary_lines = ["## 会话摘要\n"]
        current_length = 0
        
        for point in key_points:
            line = f"- {point['content']}"
            if current_length + len(line) <= max_length:
                summary_lines.append(line)
                current_length += len(line)
        
        return '\n'.join(summary_lines)
    
    def _paragraph_summary(self, key_points: List[Dict], max_length: int) -> str:
        """段落式摘要"""
        summary_parts = []
        current_length = 0
        
        for point in key_points:
            if current_length + len(point['content']) <= max_length:
                summary_parts.append(point['content'])
                current_length += len(point['content'])
        
        return ' '.join(summary_parts)
    
    def _timeline_summary(self, key_points: List[Dict], max_length: int) -> str:
        """时间线式摘要"""
        summary_lines = ["## 时间线\n"]
        current_length = 0
        timestamp = datetime.now()
        
        for i, point in enumerate(key_points, 1):
            line = f"{timestamp.strftime('%H:%M')} - {point['content']}"
            if current_length + len(line) <= max_length:
                summary_lines.append(line)
                current_length += len(line)
        
        return '\n'.join(summary_lines)


def summarize(conversation: List[Dict], max_length: int = 500, style: str = 'bullet') -> str:
    """便捷函数"""
    summarizer = ContextSummarizer()
    return summarizer.summarize(conversation, max_length, style)


if __name__ == "__main__":
    # 测试
    test_conversation = [
        {'role': 'user', 'content': '帮我构建上下文工程系统'},
        {'role': 'assistant', 'content': '好的，核心步骤包括：1. 定义架构 2. 实现功能 3. 测试验证'},
        {'role': 'user', 'content': '关键是要与现有 Skills 协同'},
        {'role': 'assistant', 'content': '重要考虑点：与 agent-memory 协同，与 LLM Wiki 协同，统一协议'},
        {'role': 'user', 'content': '总结：需要创建独立 Skill'},
    ]
    
    summary = summarize(test_conversation, style='bullet')
    print("会话摘要:")
    print(summary)
