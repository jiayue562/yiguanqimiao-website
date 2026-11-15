# -*- coding: utf-8 -*-
# 上下文质量评分器

from typing import List, Dict


def score(context_items):
    if not context_items:
        return {"score": 0, "dimensions": {}, "issues": ["上下文为空"]}

    n = len(context_items)
    issues = []
    dims = {}

    has_all = sum(1 for i in context_items if "key" in i and "value" in i and "priority" in i)
    dims["completeness"] = round(has_all / n * 100, 1)
    if dims["completeness"] < 80:
        issues.append("完整性不足: %d%%" % dims["completeness"])

    has_pri = sum(1 for i in context_items if i.get("priority") is not None)
    dims["relevance"] = round(has_pri / n * 100, 1)

    has_ts = sum(1 for i in context_items if "timestamp" in i)
    dims["freshness"] = round(has_ts / n * 100, 1)

    unique_keys = len(set(i.get("key", "") for i in context_items))
    dims["diversity"] = round(min(unique_keys / max(n, 1), 1) * 100, 1)

    avg_len = sum(len(i.get("value", "")) for i in context_items) / max(n, 1)
    if avg_len < 50:
        compact = 60
        issues.append("上下文项过于简短")
    elif avg_len > 2000:
        compact = 40
        issues.append("上下文项过长，建议摘要")
    else:
        compact = 100
    dims["compactness"] = compact

    weights = {"completeness": 0.3, "relevance": 0.25, "freshness": 0.15,
               "diversity": 0.1, "compactness": 0.2}
    total = sum(dims[k] * weights[k] for k in weights)
    return {"score": round(total, 1), "dimensions": dims, "issues": issues}
