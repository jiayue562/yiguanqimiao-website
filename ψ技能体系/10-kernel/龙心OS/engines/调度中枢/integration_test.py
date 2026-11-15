#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
三OS联调测试
验证龙心OS调度器 + 龙脑OS选刃引擎 + 龙爪OS工作流路由器是否协同工作

版本：v1.0
创建：2026-07-28
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "龙脑OS"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "99-archive", "龙爪 OS", "framework"))

from scheduler import Scheduler
from 选刃引擎 import BladeEngine, TaskType as BrainTaskType
from workflow_router import WorkflowRouter

PASS = 0
FAIL = 0


def check(condition: bool, msg: str):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {msg}")
    else:
        FAIL += 1
        print(f"  [FAIL] {msg}")


def test_os1_heart_scheduler():
    print("\n=== 测试1：龙心OS调度器 ===")
    scheduler = Scheduler()
    test_cases = [
        ("为什么这个月毛利下降了？", "high", "JY"),
        ("该不该开新店？", "high", "ZL"),
        ("怎么做储值活动方案？", "medium", "FA"),
        ("最近状态不好怎么调整？", "medium", "CZ"),
        ("除了金枪鱼还能做什么爆品？", "medium", "CY"),
    ]
    for desc, urg, expected in test_cases:
        r = scheduler.run(desc, urg)
        check(r.task_type.value == expected, f"{desc[:20]}... → {r.task_type.value} (期望{expected})")


def test_os2_brain_blade():
    print("\n=== 测试2：龙脑OS选刃引擎 ===")
    engine = BladeEngine()
    task_types = [
        (BrainTaskType.JY, "瓶颈理论"),
        (BrainTaskType.ZL, "易经错综复杂"),
        (BrainTaskType.FA, "5W2H"),
        (BrainTaskType.WD, "5Whys"),
        (BrainTaskType.GT, "六顶思考帽"),
        (BrainTaskType.XX, "第一性原理"),
        (BrainTaskType.CZ, "五层分析法"),
        (BrainTaskType.CY, "观比体化"),
    ]
    for tt, expected_model in task_types:
        r = engine.recommend(tt)
        check(r is not None, f"{tt.value} 有推荐结果")
        if r:
            check(any(m.name == expected_model for m in r.primary_chain),
                  f"{tt.value} 首选包含 {expected_model}")

    all_models = engine.get_all_model_ids()
    check(len(all_models) >= 20, f"模型总数 {len(all_models)} >= 20")


def test_os3_claw_workflow():
    print("\n=== 测试3：龙爪OS工作流路由器 ===")
    router = WorkflowRouter()
    template = router.route("超级个体落地")
    check(template is not None, "路由到'超级个体落地'模板")
    if template:
        check(len(template.steps) == 5, f"模板步骤数 = {len(template.steps)}")
        check(len(template.steps[0].thinking_models) >= 1, "第一步有推荐的思维模型")
        check(",".join(template.steps[0].thinking_models), f"第一步模型: {template.steps[0].thinking_models}")


def test_cross_os():
    print("\n=== 测试4：跨OS联调 (龙心→龙脑→龙爪) ===")
    scheduler = Scheduler()
    blade = BladeEngine()
    router = WorkflowRouter()

    result = scheduler.run("怎么做储值活动方案？", "medium", ["活动", "储值"])

    check(result.task_type.value == "FA", f"分类正确: {result.task_type.value}")
    check(result.task_level.value == "standard", f"动员级别: {result.task_level.value}")
    check(len(result.engines_activated) >= 1, f"引擎数: {len(result.engines_activated)}")
    check(len(result.engines_activated) > 0, "至少激活1个引擎")

    brain_result = result.brain_os_result
    check(brain_result is not None, "龙脑OS查询成功")
    if brain_result and brain_result.output:
        models = brain_result.output.get("recommended_models", [])
        check(len(models) >= 1, f"推荐模型数: {len(models)}")

    blade_rec = blade.recommend(BrainTaskType.FA)
    check(blade_rec is not None, "选刃引擎推荐成功")
    if blade_rec:
        check(len(blade_rec.primary_chain) >= 2, f"首选模型链: {len(blade_rec.primary_chain)}个")

    claw_result = result.claw_os_result
    check(claw_result is not None, "龙爪OS分发成功")
    if claw_result and claw_result.output:
        steps = claw_result.output.get("steps", [])
        check(len(steps) >= 1, f"工作流步骤: {len(steps)}步")


def test_error_handling():
    print("\n=== 测试5：异常处理与降级 ===")
    scheduler_no_brain = Scheduler(brain_os_available=False)
    result = scheduler_no_brain.run("毛利下降原因分析？", "high")
    check(result.status == "completed", f"龙脑不可用时仍能完成: {result.status}")
    check(result.brain_os_result is None, "龙脑OS返回None")

    scheduler_no_claw = Scheduler(claw_os_available=False)
    result2 = scheduler_no_claw.run("毛利下降原因分析？", "high")
    check(result2.status == "completed", f"龙爪不可用时仍能完成: {result2.status}")
    check(result2.claw_os_result is None, "龙爪OS返回None")


if __name__ == "__main__":
    print("=" * 60)
    print("三OS联调测试")
    print("=" * 60)

    test_os1_heart_scheduler()
    test_os2_brain_blade()
    test_os3_claw_workflow()
    test_cross_os()
    test_error_handling()

    print(f"\n{'=' * 60}")
    total = PASS + FAIL
    print(f"总计: {total} 项测试 | PASS: {PASS} | FAIL: {FAIL} | 通过率: {PASS/total*100:.1f}%")
    print(f"{'=' * 60}")
