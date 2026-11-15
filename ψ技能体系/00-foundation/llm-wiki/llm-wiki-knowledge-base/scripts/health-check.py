# -*- coding: utf-8 -*-
# LLM Wiki 健康检查脚本
# 龙心 OS · 2026-04-16

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'compiler'))

from lint import check_wiki_health

if __name__ == "__main__":
    print("运行 LLM Wiki 健康检查...\n")
    report = check_wiki_health()
    
    if report:
        print(f"\n健康分数：{report['health_score']}/100")
        
        if report['health_score'] >= 90:
            print("OK 健康状态：优秀")
        elif report['health_score'] >= 75:
            print("OK 健康状态：良好")
        elif report['health_score'] >= 60:
            print("WARN 健康状态：需改进")
        else:
            print("WARN 健康状态：需关注")
