#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最终联调测试 — 覆盖三OS全部修复项的完整验证
龙心调度器 + 龙脑选刃 + 龙爪执行 + 8引擎 + 上下文管理 + 人在回路 + 触发配置

版本：v2.0（重写，路径已修正）
创建：2026-07-28
"""

import sys
import os
import json
import importlib.util

# ---- 路径修正：从 调度中枢 出发定位各模块 ----
_HERE = os.path.dirname(os.path.abspath(__file__))
_DRAGON_HEART = os.path.normpath(os.path.join(_HERE, "..", ".."))      # 龙心OS
_ENGINES = os.path.join(_DRAGON_HEART, "engines")
_BRAIN_OS = os.path.normpath(os.path.join(_DRAGON_HEART, "..", "龙脑OS"))
_CLAW_FW = os.path.normpath(os.path.join(
    os.path.expanduser("~"), ".workbuddy", "skills", "龙爪OS", "framework"))
_CLAW_TRIG = os.path.normpath(os.path.join(
    os.path.expanduser("~"), ".workbuddy", "skills", "龙爪OS", "triggers"))

for p in (_DRAGON_HEART, _ENGINES, _BRAIN_OS, _CLAW_FW):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from scheduler import Scheduler
from 选刃引擎 import BladeEngine, TaskType as BrainTaskType
from context_manager import ContextManager


def import_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# 动态导入各引擎与框架模块
ENGINE_PATHS = {
    "action_knowledge": os.path.join(_ENGINES, "知行合一", "action_knowledge.py"),
    "knowledge_learning": os.path.join(_ENGINES, "知识学习Skills", "knowledge_learning.py"),
    "gestalt_engine": os.path.join(_ENGINES, "具身关系格式塔引擎", "gestalt_engine.py"),
    "bottleneck_diagnosis": os.path.join(_ENGINES, "串行瓶颈诊断引擎", "bottleneck_diagnosis.py"),
    "bottleneck_compress": os.path.join(_ENGINES, "瓶颈压缩策略引擎", "bottleneck_compress.py"),
    "five_color": os.path.join(_ENGINES, "五色光思维", "五色光引擎.py"),
    "five_quadrant": os.path.join(_ENGINES, "人机协同五象限", "五象限引擎.py"),
    "xiang_si_wei": os.path.join(_ENGINES, "象思维", "象思维引擎.py"),
    "step_executor": os.path.join(_CLAW_FW, "step_executor.py"),
    "progress_tracker": os.path.join(_CLAW_FW, "progress_tracker.py"),
    "workflow_router": os.path.join(_CLAW_FW, "workflow_router.py"),
}

MODULES = {}
for name, path in ENGINE_PATHS.items():
    m = import_from_path(name, path)
    MODULES[name] = m
    if m is None:
        print(f"  [WARN] 模块未加载: {name} @ {path}")

# 各引擎的主类（约定：引擎文件名去下划线 + Engine）
ENGINE_MAIN_CLASS = {
    "action_knowledge": "KnowledgeActionEngine",
    "knowledge_learning": "KnowledgeLearningEngine",
    "gestalt_engine": "GestaltEngine",
    "bottleneck_diagnosis": "BottleneckDiagnosisEngine",
    "bottleneck_compress": "BottleneckCompressionEngine",
    "five_color": "FiveColorEngine",
    "five_quadrant": "FiveQuadrantEngine",
    "xiang_si_wei": "XiangSiWeiEngine",
}


PASS = 0
FAIL = 0
TOTAL = 0


def check(condition, msg):
    global PASS, FAIL, TOTAL
    TOTAL += 1
    if condition:
        PASS += 1
        print(f"  [PASS] {msg}")
    else:
        FAIL += 1
        print(f"  [FAIL] {msg}")


def engine_sample(arg):
    return arg


print("=" * 64)
print("龙龟三OS 最终联调测试 v2.0")
print("=" * 64)

# Test 1: 龙心调度器 + 龙脑选刃引擎（真实接线）
print("\n=== 1. 龙心调度器 + 龙脑选刃引擎（真实调用）===")
scheduler = Scheduler()
blade = BladeEngine()
cases = [
    ("为什么这个月毛利下降了？", "high", "JY"),
    ("该不该开新店？", "high", "ZL"),
    ("怎么做储值活动方案？", "medium", "FA"),
    ("团队执行力差，问题在哪？", "medium", "WD"),
    ("最近状态不好怎么调整？", "medium", "CZ"),
    ("除了金枪鱼还能做什么爆品？", "medium", "CY"),
]
for desc, urg, expected in cases:
    r = scheduler.run(desc, urg)
    check(r.task_type.value == expected, f"调度器分类: {desc[:18]}… → {r.task_type.value}")
    check(r.brain_os_result is not None, f"  龙脑OS已查询")
    if r.brain_os_result:
        # 关键：必须是真实调用选刃引擎（status=ok），而非MOCK
        check(r.brain_os_result.status == "ok", f"  选刃引擎真实调用(status=ok)")
        check(len(r.brain_os_result.output["recommended_models"]) >= 1,
              f"  真实推荐模型 {r.brain_os_result.output['recommended_models']}")

# Test 2: 8 个引擎全部有可执行 .py 且能 run
print("\n=== 2. 8 个龙心引擎全部可执行 ===")
SAMPLES = {
    "action_knowledge": ("AI原生组织",),
    "knowledge_learning": ("AI原生组织通过消除信息不对称实现碳硅合一", "AI原生组织"),
    "gestalt_engine": ("团队氛围紧张",),
    "bottleneck_diagnosis": ("跨部门沟通不畅，等批复很慢",),
    "bottleneck_compress": ("BN-INF", 8.0),
    "five_color": ("是否要开第二家味藏门店",),
    "five_quadrant": ("用AI辅助撰写味藏品牌白皮书",),
    "xiang_si_wei": ("如何让味藏的品牌更有东方禅意",),
}
for key, cls in ENGINE_MAIN_CLASS.items():
    mod = MODULES.get(key)
    check(mod is not None, f"{key}: 模块已加载")
    if mod is None:
        continue
    eng_cls = getattr(mod, cls, None)
    check(eng_cls is not None, f"{key}: 主类 {cls} 存在")
    if eng_cls is None:
        continue
    try:
        inst = eng_cls()
        res = inst.run(*SAMPLES[key])
        check(res is not None, f"{key}: run() 返回非空")
    except Exception as e:
        check(False, f"{key}: run() 异常 {e}")

# Test 3: 龙爪OS Framework 层
print("\n=== 3. 龙爪OS Framework 层 ===")
StepExecutor = getattr(MODULES["step_executor"], "StepExecutor", None)
StepDefinition = getattr(MODULES["step_executor"], "StepDefinition", None)
ProgressTracker = getattr(MODULES["progress_tracker"], "ProgressTracker", None)
WorkflowRouter = getattr(MODULES["workflow_router"], "WorkflowRouter", None)

check(all([StepExecutor, StepDefinition, ProgressTracker, WorkflowRouter]),
      "龙爪OS 三大Framework类均已加载")

if StepExecutor and StepDefinition:
    ex = StepExecutor()
    step = StepDefinition(1, "根因分析", "毛利下降原因", ["五层分析法"], {}, 300)
    rs = ex.execute_step(step)
    check(rs.status.value == "completed", f"step_executor: 执行成功")
    check(len(rs.models_used) >= 1, f"  使用模型数 {len(rs.models_used)}")

if ProgressTracker:
    tr = ProgressTracker()
    wp = tr.create_workflow("test_001", 5, due_in_minutes=120)
    tr.start_workflow("test_001")
    tr.update_step_progress("test_001", 1, True)
    tr.update_step_progress("test_001", 2, True)
    check(wp.completed_steps == 2, f"progress_tracker: 完成2步")
    check(abs(wp.overall_progress - 0.4) < 1e-6, f"  进度 {wp.overall_progress}")

if WorkflowRouter:
    rt = WorkflowRouter()
    tpl = rt.route("梳理企业文化理念")
    check(tpl is not None and len(tpl.steps) >= 4, f"workflow_router: 路由成功({len(tpl.steps)}步)")
    tpl2 = rt.route("做一次五行人格测评")
    check("五行" in tpl2.project_type or "人格" in tpl2.project_type,
          f"  五行人格路由命中: {tpl2.project_type}")
    tpl3 = rt.route("味藏本月经营分析")
    check("味藏" in tpl3.project_type, f"  味藏路由命中: {tpl3.project_type}")

# Test 4: 上下文管理 + 人在回路
print("\n=== 4. 上下文管理 + 人在回路 ===")
cm = ContextManager()
sid = "final_test_001"
t1 = cm.add_turn(sid, "为什么毛利下降", "JY", "standard", ["知识学习"], "根因定位完成")
check(t1.turn_id == 1, f"上下文: 第1轮记录")
t2 = cm.add_turn(sid, "该不该开新店", "ZL", "deep",
                 ["象思维", "五色光", "人机协同", "知识学习", "知行合一"], "决策分析完成")
confirm = cm.get_confirm_request(sid, t2)
check(confirm is not None, f"人在回路: 战略决策需确认")
if confirm:
    check(confirm['level'] == 'approve', f"  确认级别: {confirm['level']}")
summary = cm.get_session_summary(sid)
check(summary['total_turns'] == 2, f"会话摘要: {summary['total_turns']}轮")

# Test 5: 自动触发配置
print("\n=== 5. 自动触发配置 ===")
cfg_path = os.path.join(_CLAW_TRIG, "auto-activate.json")
check(os.path.isfile(cfg_path), f"auto-activate.json 存在: {cfg_path}")
if os.path.isfile(cfg_path):
    with open(cfg_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    check('龙爪OS' in cfg, f"龙爪OS配置存在")
    check(cfg['龙爪OS']['active'] is True, f"  激活状态: {cfg['龙爪OS']['active']}")
    check('sub_skills' in cfg['龙爪OS'], f"  子技能配置存在")
yaml_path = os.path.join(_CLAW_TRIG, "trigger-rules.yaml")
check(os.path.isfile(yaml_path), f"trigger-rules.yaml 存在: {yaml_path}")

# Test 6: 三OS 完整链路联调
print("\n=== 6. 三OS 完整链路联调 ===")
full = scheduler.run("怎么做储值活动方案？", "medium", ["活动", "储值"])
check(full.status == "completed", f"完整链路: 状态 {full.status}")
check(full.task_type.value == "FA", f"  分类 {full.task_type.value}")
check(full.task_level.value == "standard", f"  级别 {full.task_level.value}")
check(full.brain_os_result is not None and full.brain_os_result.status == "ok",
      f"  龙脑OS真实调用")
check(full.claw_os_result is not None, f"  龙爪OS分发成功")
if full.claw_os_result:
    check(full.claw_os_result.status == "dispatched", f"  龙爪状态 {full.claw_os_result.status}")

# Test 7: 降级测试
print("\n=== 7. 降级测试 ===")
s_no_brain = Scheduler(brain_os_available=False)
rf1 = s_no_brain.run("毛利下降原因？", "high")
check(rf1.status == "completed", f"龙脑不可用: 降级成功")
check(rf1.brain_os_result is None, f"  龙脑返回None")

s_no_claw = Scheduler(claw_os_available=False)
rf2 = s_no_claw.run("毛利下降原因？", "high")
check(rf2.status == "completed", f"龙爪不可用: 降级成功")
check(rf2.claw_os_result is None, f"  龙爪返回None")

# Summary
print(f"\n{'=' * 64}")
rate = (PASS / TOTAL * 100) if TOTAL else 0
print(f"总计: {TOTAL} 项 | PASS: {PASS} | FAIL: {FAIL} | 通过率: {rate:.1f}%")
print(f"{'=' * 64}")
sys.exit(0 if FAIL == 0 else 1)
