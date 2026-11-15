#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI OS 决策引擎 - opencode skill 入口

opencode 通过此脚本调用中间层，实现：
  输入日数据 → 自动诊断 → 自动分派 → 决策建议 → 追踪闭环

使用方式:
  python decision_skill.py "{\"金月湾\":{\"revenue_rate\":134.6,...}}"
  python decision_skill.py --demo       # 使用内置测试数据
  python decision_skill.py --tickets    # 查看当前工单状态
"""
import json, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-os')))

from aios.decision.engine import process_daily_data, DecisionEngine
from aios.decision.dispatcher import TaskTracker


def load_tracker():
    """从持久化文件加载追踪器"""
    tracker_file = os.path.expanduser("~/.aios/task_tracker.json")
    if os.path.exists(tracker_file):
        with open(tracker_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    return None


def save_tracker(tickets: list):
    """保存工单到持久化文件"""
    tracker_file = os.path.expanduser("~/.aios/task_tracker.json")
    os.makedirs(os.path.dirname(tracker_file), exist_ok=True)
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump({"tickets": tickets, "updated_at": __import__('datetime').datetime.now().isoformat()},
                  f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print(json.dumps({
            "name": "AI OS 决策引擎",
            "description": "输入日经营数据 → 自动诊断 → 自动分派 → 决策建议 → 追踪闭环",
            "usage": [
                "python decision_skill.py --demo   使用内置测试数据运行",
                "python decision_skill.py --tickets 查看当前工单状态",
                "python decision_skill.py '{\"门店名\":{...}}' 自定义数据",
            ],
        }, ensure_ascii=False))
        sys.exit(0)

    if sys.argv[1] == '--tickets':
        data = load_tracker()
        if data:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"message": "暂无工单记录"}, ensure_ascii=False))
        sys.exit(0)

    if sys.argv[1] == '--demo':
        result = process_daily_data()
    else:
        stores = json.loads(sys.argv[1])
        engine = DecisionEngine()
        result = engine.run(stores)

    # 保存工单
    if result.get("dispatched_tickets"):
        save_tracker(result["dispatched_tickets"])

    print(json.dumps(result, ensure_ascii=False, indent=2))
