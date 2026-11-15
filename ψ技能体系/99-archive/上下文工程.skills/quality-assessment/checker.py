# -*- coding: utf-8 -*-
# 上下文健康检查器


def check(context_items):
    checks = []
    checks.append({
        "name": "non_empty",
        "passed": len(context_items) > 0,
        "detail": "上下文项数: %d" % len(context_items)
    })
    if context_items:
        missing = sum(1 for i in context_items if not all(k in i for k in ("key", "value", "priority")))
        checks.append({
            "name": "field_integrity",
            "passed": missing == 0,
            "detail": "字段缺失项: %d/%d" % (missing, len(context_items))
        })
        invalid = sum(1 for i in context_items if not (1 <= i.get("priority", 0) <= 5))
        checks.append({
            "name": "priority_range",
            "passed": invalid == 0,
            "detail": "优先级越界: %d" % invalid
        })
        total_tokens = sum(len(i.get("value", "")) * 1.5 for i in context_items)
        checks.append({
            "name": "token_limit",
            "passed": total_tokens <= 4096,
            "detail": "总 token: %d/4096" % int(total_tokens)
        })
    passed = sum(1 for c in checks if c["passed"])
    score_val = int(passed / len(checks) * 100) if checks else 0
    return {"healthy": score_val >= 75, "checks": checks, "score": score_val}
