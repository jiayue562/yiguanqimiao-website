# -*- coding: utf-8 -*-
# 上下文优化建议生成器

import sys, os, importlib.util

def _load_mod(relpath):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full = os.path.join(base, relpath)
    name = os.path.splitext(os.path.basename(relpath))[0]
    spec = importlib.util.spec_from_file_location(name, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_score_mod = _load_mod("quality-assessment/scorer.py")
_check_mod = _load_mod("quality-assessment/checker.py")
score = _score_mod.score
check = _check_mod.check


def get_optimization_tips(context_items):
    tips = []
    if not context_items:
        tips.append("上下文为空，请至少提供 1 项上下文")
        return tips
    sc = score(context_items)
    if sc["score"] < 60:
        tips.append("质量评分偏低 (%d)" % sc["score"])
        tips.extend(sc["issues"])
    ch = check(context_items)
    for c in ch["checks"]:
        if not c["passed"]:
            tips.append(c["detail"])
    n = len(context_items)
    if n > 20:
        tips.append("上下文项过多 (%d)，建议精简到 10-15 项" % n)
    avg_len = sum(len(i.get("value", "")) for i in context_items) / n
    if avg_len > 1000:
        tips.append("平均长度 %d 字，建议摘要到 200 字以内" % int(avg_len))
    if avg_len < 20:
        tips.append("上下文过于简短 (%d 字)，建议补充更多信息" % int(avg_len))
    priorities = [i.get("priority", 5) for i in context_items]
    if sum(1 for p in priorities if p <= 2) == 0:
        tips.append("没有高优先级项 (P1-P2)，建议标注关键上下文")
    return tips


def auto_optimize(context_items):
    original_sc = score(context_items)
    sorted_items = sorted(context_items, key=lambda x: x.get("priority", 5))
    optimized = sorted_items[:15]
    for item in optimized:
        val = item.get("value", "")
        if len(val) > 500:
            item["value"] = val[:497] + "..."
    optimized_sc = score(optimized)
    tips = get_optimization_tips(context_items)
    return {
        "optimized": optimized,
        "original_score": original_sc["score"],
        "optimized_score": optimized_sc["score"],
        "tips": tips
    }
