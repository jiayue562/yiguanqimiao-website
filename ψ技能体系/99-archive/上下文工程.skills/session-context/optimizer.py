# -*- coding: utf-8 -*-
# 上下文优化器 - 裁剪/排序/合并上下文项

from typing import List, Dict


def optimize(context_items, max_tokens=4096, reserved_priority=3):
    if not context_items:
        return []
    sorted_items = sorted(context_items, key=lambda x: x.get("priority", 5))
    retained = [i for i in sorted_items if i.get("priority", 5) <= reserved_priority]
    total_tokens = sum(len(i.get("value", "")) * 1.5 for i in retained)
    if total_tokens <= max_tokens:
        return retained
    result = []
    used = 0
    for item in retained:
        tokens = len(item.get("value", "")) * 1.5
        if used + tokens <= max_tokens:
            result.append(item)
            used += tokens
        else:
            remaining = int((max_tokens - used) / 1.5)
            if remaining > 20:
                item["value"] = item.get("value", "")[:remaining] + "..."
                result.append(item)
            break
    return result


def merge(base, incoming, dedup_key="key"):
    seen = {}
    for item in base + incoming:
        k = item.get(dedup_key, "")
        if k not in seen or item.get("priority", 5) < seen[k].get("priority", 5):
            seen[k] = item
    return list(seen.values())
