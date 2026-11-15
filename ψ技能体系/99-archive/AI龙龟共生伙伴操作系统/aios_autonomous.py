#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI OS 自主智能体 - opencode skill 入口 v3.0
完整架构: 底层(龙心OS 1+5引擎+四大域) + 中间层(自动诊断→分派→决策→追踪) + 上层(人类决策)

使用方式:
  python aios_autonomous.py "帮我分析团队协作问题"  → 走底层引擎
  python aios_autonomous.py --decision               → 走中间层决策引擎（demo数据）
  python aios_autonomous.py --decision '{"金月湾":{...}}'  → 自定义数据
  python aios_autonomous.py --status                  → 查看系统状态
  python aios_autonomous.py --goal "..."             → 设置长期目标
"""
import json, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-os')))

from aios.core.aios_autonomous import AIOSAutonomous
from aios.decision.engine import process_daily_data, DecisionEngine


if __name__ == '__main__':
    # 中间层：决策引擎模式
    if len(sys.argv) >= 2 and sys.argv[1] == '--decision':
        from aios.decision.engine import DecisionEngine
        engine = DecisionEngine()
        if len(sys.argv) >= 3:
            import ast
            stores = ast.literal_eval(sys.argv[2])
            result = engine.run(stores)
        else:
            result = process_daily_data()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # 底层：AI OS 自主智能体模式
    agent = AIOSAutonomous(mode="hybrid")

    if len(sys.argv) < 2:
        print(json.dumps(agent.get_status(), ensure_ascii=False))
        sys.exit(0)

    if sys.argv[1] == '--help':
        print(json.dumps({
            "name": "AI OS 自主智能体 v3.0",
            "description": "完整架构: 底层(龙心OS 1+5引擎+四大域) + 中间层(自动诊断→分派→决策→追踪) + 上层(人类决策)",
            "usage": [
                "python aios_autonomous.py '请求'   → 底层引擎处理",
                "python aios_autonomous.py --decision → 中间层决策引擎",
                "python aios_autonomous.py --status   → 系统状态",
            ],
        }, ensure_ascii=False))
        sys.exit(0)

    if sys.argv[1] == '--status':
        print(json.dumps(agent.get_status(), ensure_ascii=False))
    elif sys.argv[1] == '--goal':
        desc = ' '.join(sys.argv[2:]) or "持续学习和进化"
        print(json.dumps(agent.set_goal(desc), ensure_ascii=False))
    else:
        result = agent.process(' '.join(sys.argv[1:]))
        print(json.dumps(result, ensure_ascii=False, indent=2))
