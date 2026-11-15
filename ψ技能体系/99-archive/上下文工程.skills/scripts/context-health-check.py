# -*- coding: utf-8 -*-
# 上下文健康检查脚本

import sys, os, importlib.util
from pathlib import Path

_BASE = str(Path(__file__).parent.parent)

def _load_mod(relpath):
    full = os.path.join(_BASE, relpath)
    name = os.path.splitext(os.path.basename(relpath))[0]
    spec = importlib.util.spec_from_file_location(name, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_checker_mod = _load_mod("quality-assessment/checker.py")
_scorer_mod = _load_mod("quality-assessment/scorer.py")
_optimizer_mod = _load_mod("quality-assessment/optimizer.py")
check = _checker_mod.check
score = _scorer_mod.score
get_optimization_tips = _optimizer_mod.get_optimization_tips


def main():
    print("=" * 60)
    print("  上下文健康检查")
    print("=" * 60)
    print()

    test_context = [
        {"key": "project", "value": "AI OS 知识库构建", "priority": 1, "timestamp": "2026-05-20"},
        {"key": "decision", "value": "采用五行分类作为知识库分类体系", "priority": 2},
        {"key": "status", "value": "Phase 5 完成", "priority": 3},
        {"key": "next_step", "value": "IMA 同步", "priority": 3},
    ]

    print("检查对象: 测试上下文 (4项)")
    print()

    ch = check(test_context)
    print("健康状态: %s" % ("OK 通过" if ch["healthy"] else "WARN 需关注"))
    print("健康评分: %d/100" % ch["score"])
    for c in ch["checks"]:
        icon = "OK" if c["passed"] else "WARN"
        print("  [%s] %s: %s" % (icon, c["name"], c["detail"]))

    print()
    sc = score(test_context)
    print("质量评分: %d/100" % sc["score"])
    for dim, val in sc["dimensions"].items():
        print("  - %s: %s" % (dim, val))

    print()
    tips = get_optimization_tips(test_context)
    if tips:
        print("优化建议:")
        for tip in tips:
            print("  * %s" % tip)
    else:
        print("无需优化")

    print()
    print("=" * 60)
    print("  检查完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
