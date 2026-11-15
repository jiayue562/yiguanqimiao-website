# -*- coding: utf-8 -*-
# 上下文摘要生成器

from typing import List, Dict


def summarize(context_items, max_length=200):
    if not context_items:
        return ""
    lines = []
    for item in context_items:
        key = item.get("key", "")
        val = item.get("value", "")
        pri = item.get("priority", 5)
        lines.append("[P%d] %s: %s" % (pri, key, val[:80]))
    summary = "; ".join(lines)
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."
    return summary


def hierarchical_summary(context_items, levels=3):
    result = {}
    if not context_items:
        return result
    sorted_items = sorted(context_items, key=lambda x: x.get("priority", 5))
    for level in range(1, levels + 1):
        threshold = level * 2
        items = [i for i in sorted_items if i.get("priority", 5) <= threshold]
        result["level_%d" % level] = summarize(items)
    return result
