# -*- coding: utf-8 -*-
# 上下文优先级排序器

from typing import List, Dict


def prioritize(context_items):
    for item in context_items:
        if "priority" not in item:
            item["priority"] = _auto_priority(item)
    return sorted(context_items, key=lambda x: (x.get("priority", 5), x.get("timestamp", "")))


def _auto_priority(item):
    value = item.get("value", "")
    key = item.get("key", "")
    score = 0
    if len(value) > 500:
        score += 1
    important = ["决策", "结论", "关键", "方案", "核心"]
    if any(kw in key or kw in value[:100] for kw in important):
        score += 2
    if "timestamp" in item:
        score += 1
    return max(1, 5 - score)


def filter_by_threshold(context_items, min_priority=3):
    return [i for i in context_items if i.get("priority", 5) <= min_priority]
