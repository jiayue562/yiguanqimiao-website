# -*- coding: utf-8 -*-
# 上下文健康检查脚本
# 龙心 OS · 2026-04-16

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'quality-assessment'))

from scorer import score_context

def check_context_health():
    """检查上下文健康状态"""
    print("=" * 60)
    print("  上下文健康检查")
    print("=" * 60)
    print("")
    
    # 模拟上下文数据
    test_context = {
        'content': '测试上下文内容',
        'keywords': ['测试', '上下文'],
        'relevance_tags': ['核心'],
        'timestamp': None,
        'importance': 'medium'
    }
    
    # 评分
    score_result = score_context(test_context)
    
    print("1. 质量评分:")
    print("-" * 40)
    print(f"  综合评分：{score_result['total_score']:.1f}/100")
    print("")
    
    print("2. 维度评分:")
    print("-" * 40)
    for dim, score in score_result['dimensions'].items():
        status = "OK" if score >= 0.7 else "WARN"
        print(f"  {dim}: {score*100:.0f}% [{status}]")
    print("")
    
    print("3. 健康建议:")
    print("-" * 40)
    if score_result['total_score'] >= 80:
        print("  OK 上下文质量良好")
    elif score_result['total_score'] >= 60:
        print("  WARN 上下文质量需改进")
    else:
        print("  WARN 上下文质量需关注")
    
    print("")
    print("=" * 60)
    print("  检查完成")
    print("=" * 60)
    
    return score_result

if __name__ == "__main__":
    check_context_health()
