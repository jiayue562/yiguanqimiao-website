#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心OS 总智能体调度中枢
意图识别 → 场景分类 → 引擎路由 → 龙脑查询 → 龙爪执行 → 结果整合

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import os
import sys

# 动态加载龙脑OS 选刃引擎（同属 10-kernel，向上三层：调度中枢→engines→龙心OS→10-kernel）
_BRAIN_OS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "龙脑OS")
)
if _BRAIN_OS_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_OS_DIR)

try:
    from 选刃引擎 import BladeEngine as _BladeEngine, TaskType as _BrainTaskType
    _BLADE_ENGINE = _BladeEngine()
    _BLADE_AVAILABLE = True
except Exception:  # pragma: no cover - 选刃引擎缺失时降级
    _BLADE_ENGINE = None
    _BLADE_AVAILABLE = False

# 常驻子系统注册表（深度共生·2026-07-29）：五行人格心理学OS等作为龙心总调度下的常驻子系统。
# 调度中枢加载即注册，使五行执行子系统常驻于总调度上下文（非按需临时挂载）。
import os as _os
_SCHED_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _SCHED_DIR not in sys.path:
    sys.path.insert(0, _SCHED_DIR)
try:
    from subsystems import (
        dispatch_all as _dispatch_resident,
        heartbeat_all as _heartbeat_resident,
        list_resident as _list_resident,
        longzhao_subsystem as _longzhao_subsystem,
    )
    _RESIDENT_ENABLED = True
except Exception:  # pragma: no cover - 子系统层缺失时降级，绝不拖垮主流程
    _RESIDENT_ENABLED = False
    _dispatch_resident = None
    _heartbeat_resident = None
    _list_resident = None


class TaskLevel(Enum):
    LIGHT = "light"
    STANDARD = "standard"
    DEEP = "deep"


class TaskType(Enum):
    JY = "JY"  # 经营分析型
    ZL = "ZL"  # 战略决策型
    FA = "FA"  # 方案设计型
    WD = "WD"  # 问题诊断型
    GT = "GT"  # 沟通协作型
    XX = "XX"  # 学习研究型
    CZ = "CZ"  # 自我成长型
    CY = "CY"  # 创意创新型
    UNKNOWN = "UNKNOWN"  # 未知


@dataclass
class TaskContext:
    task_type: TaskType = TaskType.UNKNOWN
    task_level: TaskLevel = TaskLevel.LIGHT
    description: str = ""
    domain: str = ""
    urgency: str = "medium"
    keywords: List[str] = field(default_factory=list)


@dataclass
class EngineResult:
    engine_id: str
    status: str
    output: Any = None
    error: Optional[str] = None
    models_used: List[str] = field(default_factory=list)


@dataclass
class SchedulerResult:
    task_id: str
    task_type: TaskType
    task_level: TaskLevel
    engines_activated: List[str]
    brain_os_result: Optional[EngineResult] = None
    claw_os_result: Optional[EngineResult] = None
    resident_results: Optional[dict] = None
    heart_engine_results: Dict[str, EngineResult] = field(default_factory=dict)
    final_output: Any = None
    status: str = "completed"
    error: Optional[str] = None


class Scheduler:
    HEART_ENGINES = {
        "xiang_si_wei": "象思维",
        "five_color": "五色光思维",
        "human_machine": "人机协同五象限",
        "knowledge_learning": "知识学习Skills",
        "action_knowledge": "知行合一",
    }

    ENGINE_PATHS = {
        "xiang_si_wei": "龙心OS/engines/象思维/",
        "five_color": "龙心OS/engines/五色光思维/",
        "human_machine": "龙心OS/engines/人机协同五象限/",
        "knowledge_learning": "龙心OS/engines/知识学习Skills/",
        "action_knowledge": "龙心OS/engines/知行合一/",
    }

    EXT_ENGINES = {
        "gestalt": "具身关系格式塔引擎",
        "bottleneck_diag": "串行瓶颈诊断引擎",
        "bottleneck_compress": "瓶颈压缩策略引擎",
    }

    def __init__(self, brain_os_available: bool = True, claw_os_available: bool = True):
        self.brain_os_available = brain_os_available
        self.claw_os_available = claw_os_available

    def classify_task(self, description: str, keywords: List[str] = None) -> TaskType:
        desc_lower = description.lower()
        kw = [k.lower() for k in (keywords or [])]

        score = {t: 0 for t in TaskType}
        task_patterns = {
            TaskType.JY: [
                "分析", "根因", "归因", "数据", "指标", "毛利", "损耗",
                "下降", "上升", "异常", "原因", "为什么", "占比", "复购",
                "转化率", "客单价"
            ],
            TaskType.ZL: [
                "决策", "选择", "该不该", "是否", "方案对比", "投资",
                "战略", "方向", "开新店", "人选"
            ],
            TaskType.FA: [
                "方案", "计划", "设计", "怎么做", "策略", "活动",
                "培训计划", "促销", "项目计划"
            ],
            TaskType.WD: [
                "问题", "诊断", "哪里", "怎么回事", "瓶颈",
                "效率低", "总是", "持续下滑", "故障", "异常", "卡住"
            ],
            TaskType.GT: [
                "沟通", "说服", "协调", "谈判", "反馈", "团队",
                "矛盾", "领导", "同事", "合伙人"
            ],
            TaskType.XX: [
                "学习", "理解", "研究", "深度", "理论", "是什么",
                "概念", "背景", "逻辑"
            ],
            TaskType.CZ: [
                "成长", "人格", "状态", "调整", "短板", "情绪",
                "五行", "身心灵", "焦虑", "迷茫"
            ],
            TaskType.CY: [
                "创新", "创意", "原创", "突破", "爆品", "新",
                "新模式", "跨界", "灵感"
            ],
        }

        for task_type, patterns in task_patterns.items():
            for p in patterns:
                if p in desc_lower:
                    score[task_type] += 1
                for k in kw:
                    if p in k:
                        score[task_type] += 1

        best = max(score, key=score.get)
        return best if score[best] > 0 else TaskType.UNKNOWN

    def determine_task_level(self, task_type: TaskType, urgency: str) -> TaskLevel:
        if urgency == "high" or task_type in [TaskType.ZL, TaskType.CY]:
            return TaskLevel.DEEP
        if task_type in [TaskType.WD, TaskType.FA]:
            return TaskLevel.STANDARD
        return TaskLevel.LIGHT

    def determine_engines(self, task_type: TaskType, level: TaskLevel) -> List[str]:
        task_engine_map = {
            TaskType.JY: ["knowledge_learning", "five_color"],
            TaskType.ZL: ["five_color", "xiang_si_wei"],
            TaskType.FA: ["action_knowledge", "human_machine"],
            TaskType.WD: ["knowledge_learning", "five_color"],
            TaskType.GT: ["human_machine", "xiang_si_wei"],
            TaskType.XX: ["knowledge_learning", "xiang_si_wei"],
            TaskType.CZ: ["xiang_si_wei", "action_knowledge"],
            TaskType.CY: ["xiang_si_wei", "five_color"],
            TaskType.UNKNOWN: ["xiang_si_wei"],
        }

        base = task_engine_map.get(task_type, ["xiang_si_wei"])[:]
        if level == TaskLevel.DEEP:
            full = list(self.HEART_ENGINES.keys())
            base = full if len(base) < 3 else base + ["action_knowledge"]
        elif level == TaskLevel.STANDARD and len(base) < 2:
            base.append("five_color")
        return base

    def query_brain_os(self, task_ctx: TaskContext) -> Optional[EngineResult]:
        if not self.brain_os_available:
            return None
        result = EngineResult(engine_id="brain_os", status="queried")
        try:
            # 真实接线：调用龙脑OS 选刃引擎获取模型推荐（失败时回退默认）
            if _BLADE_AVAILABLE and _BLADE_ENGINE is not None:
                try:
                    bt = _BrainTaskType(task_ctx.task_type.value)
                    out = _BLADE_ENGINE.format_output(bt)
                except Exception:
                    out = None
                if out:
                    models = [m["name"] for m in out["primary_chain"]] + \
                             [m["name"] for m in out["alternative_chain"]]
                    result.output = {
                        "task_type": task_ctx.task_type.value,
                        "recommended_models": models,
                        "combination_logic": out.get("combination_logic", ""),
                        "confidence": out.get("confidence", 0.0),
                    }
                    result.models_used = ["选刃引擎·" + task_ctx.task_type.value]
                    result.status = "ok"
                    return result
            # 回退：默认模型映射（MOCK）
            result.output = {
                "task_type": task_ctx.task_type.value,
                "recommended_models": self._get_default_models(task_ctx.task_type)
            }
            result.models_used = ["选刃决策树(回退)"]
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
        return result

    def _get_default_models(self, task_type: TaskType) -> List[str]:
        defaults = {
            TaskType.JY: ["瓶颈理论", "五层分析法"],
            TaskType.ZL: ["易经错综复杂", "决策矩阵", "二阶思维"],
            TaskType.FA: ["5W2H", "金字塔原理", "ORID"],
            TaskType.WD: ["5Whys", "系统思维", "苏格拉底式提问"],
            TaskType.GT: ["六顶思考帽", "拉波波特法则", "SBI反馈模型"],
            TaskType.XX: ["十种知识整合方式", "第一性原理", "框架思维"],
            TaskType.CZ: ["五层分析法", "逆向思维", "价值聚焦"],
            TaskType.CY: ["观比体化", "SCAMPER", "逆向思维"],
            TaskType.UNKNOWN: ["五层分析法"],
        }
        return defaults.get(task_type, ["五层分析法"])

    def invoke_heart_engine(self, engine_id: str, task_ctx: TaskContext) -> EngineResult:
        result = EngineResult(engine_id=engine_id, status="invoked")
        try:
            engine_name = self.HEART_ENGINES.get(engine_id, engine_id)
            result.output = f"{engine_name}引擎处理完成"
            result.models_used = []
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
        return result

    def dispatch_to_claw_os(self, task_ctx: TaskContext, brain_result: Optional[EngineResult]) -> Optional[EngineResult]:
        if not self.claw_os_available:
            return None
        result = EngineResult(engine_id="claw_os", status="dispatched")
        try:
            models = []
            if brain_result and brain_result.output:
                models = brain_result.output.get("recommended_models", [])
            result.output = {
                "project_name": task_ctx.description[:30],
                "project_category": task_ctx.task_type.value,
                "steps": [
                    {"step_id": 1, "name": "问题分析", "recommended_models": models[:2]},
                    {"step_id": 2, "name": "方案制定", "recommended_models": models[2:4] if len(models) > 2 else ["5W2H"]},
                ]
            }
            result.models_used = models
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
        return result

    def run(self, description: str, urgency: str = "medium", keywords: List[str] = None) -> SchedulerResult:
        task_id = f"task_{hash(description) & 0xFFFF:04x}"
        task_ctx = TaskContext(
            task_type=self.classify_task(description, keywords),
            description=description,
            urgency=urgency,
            keywords=keywords or []
        )
        task_ctx.task_level = self.determine_task_level(task_ctx.task_type, urgency)

        result = SchedulerResult(
            task_id=task_id,
            task_type=task_ctx.task_type,
            task_level=task_ctx.task_level,
            engines_activated=[]
        )

        brain_result = self.query_brain_os(task_ctx)
        result.brain_os_result = brain_result

        engines = self.determine_engines(task_ctx.task_type, task_ctx.task_level)
        result.engines_activated = [self.HEART_ENGINES.get(e, e) for e in engines]

        for engine_id in engines:
            engine_result = self.invoke_heart_engine(engine_id, task_ctx)
            result.heart_engine_results[engine_id] = engine_result
            if engine_result.status == "failed":
                result.status = "degraded"
                fallback = [e for e in self.HEART_ENGINES if e not in result.heart_engine_results]
                if fallback:
                    engine_result = self.invoke_heart_engine(fallback[0], task_ctx)
                    result.heart_engine_results[fallback[0]] = engine_result

        claw_result = self.dispatch_to_claw_os(task_ctx, brain_result)
        result.claw_os_result = claw_result

        # 深度共生：常驻子系统派发（五行人格心理学OS等）
        # 龙心总调度询问各常驻子系统是否处理当前输入，命中则派发并回灌龙心共享共生记忆。
        if _RESIDENT_ENABLED and _dispatch_resident is not None:
            try:
                resident = _dispatch_resident(description)
                if resident:
                    result.resident_results = resident
            except Exception:  # pragma: no cover - 单子系统异常隔离
                pass

        result.final_output = {
            "task_id": task_id,
            "task_type": task_ctx.task_type.value,
            "task_level": task_ctx.task_level.value,
            "engines_activated": result.engines_activated,
            "recommended_models": brain_result.output.get("recommended_models", []) if brain_result else [],
            "workflow_plan": claw_result.output if claw_result else None,
            "resident_results": result.resident_results,
            "status": result.status,
        }

        return result


def demo():
    scheduler = Scheduler()
    test_cases = [
        ("为什么这个月毛利下降了？", "high", ["毛利", "损耗"]),
        ("该不该开新店？", "high", ["开店", "决策"]),
        ("怎么做储值活动方案？", "medium", ["活动", "储值"]),
        ("团队执行力差，问题在哪？", "medium", ["团队", "执行力"]),
        ("怎么跟料理长沟通成本问题？", "low", ["沟通", "成本"]),
        ("帮我深度学习一下这篇文章", "low", ["学习"]),
        ("最近状态不好，怎么调整？", "medium", ["状态", "调整"]),
        ("除了金枪鱼，还能做什么爆品？", "medium", ["创新", "爆品"]),
        # 深度共生：五行人格心理学OS常驻子系统派发验证
        ("我和对象吵架冷战了怎么办", "medium", ["吵架", "亲密"]),
        # 深度共生：龙爪OS常驻子系统（执行层）派发验证
        ("启动企业文化落地项目，做诊断分析", "medium", ["项目", "企业文化"]),
    ]
    for desc, urg, kw in test_cases:
        r = scheduler.run(desc, urg, kw)
        rr = r.resident_results or {}
        tags = []
        if "wuxing_os" in rr:
            tags.append("五行闭环✅")
        if "longzhao_os" in rr:
            tags.append("龙爪执行✅")
        print(f"[{r.task_id}] {r.task_type.value} | {r.task_level.value} | {', '.join(r.engines_activated)} | {r.status}{' | ' + ' '.join(tags) if tags else ''}")


def dispatch_wuxing(text: str) -> dict:
    """便捷入口：直接派发五行人格心理学OS常驻子系统（深度共生）。"""
    if not _RESIDENT_ENABLED or _dispatch_resident is None:
        return {"status": "unavailable", "reason": "常驻子系统层未加载"}
    return _dispatch_resident(text)


def dispatch_resident(text: str) -> dict:
    """便捷入口：派发全部常驻子系统（五行 + 龙爪，多轮反哺增强）。"""
    if not _RESIDENT_ENABLED or _dispatch_resident is None:
        return {"status": "unavailable", "reason": "常驻子系统层未加载"}
    return _dispatch_resident(text)


def dispatch_longzhao(text: str) -> dict:
    """便捷入口：直接派发龙爪OS常驻子系统（执行层）。"""
    if not _RESIDENT_ENABLED or _longzhao_subsystem is None:
        return {"status": "unavailable", "reason": "常驻子系统层未加载"}
    return _longzhao_subsystem.handle(text)


if __name__ == "__main__":
    import argparse as _argparse
    _ap = _argparse.ArgumentParser(description="龙心OS 总智能体调度中枢")
    _ap.add_argument("--demo", action="store_true", help="运行内置演示")
    _ap.add_argument("--wuxing", metavar="TEXT", help="直接派发常驻子系统（五行+龙爪，多轮反哺）")
    _ap.add_argument("--longzhao", metavar="TEXT", help="直接派发龙爪OS常驻子系统（执行层）")
    _ap.add_argument("--residents", action="store_true", help="列出常驻子系统")
    _ap.add_argument("--heartbeat", action="store_true", help="常驻子系统存活探针")
    _args = _ap.parse_args()

    if _args.residents and _list_resident:
        print(json.dumps(_list_resident(), ensure_ascii=False, indent=2))
    elif _args.heartbeat and _heartbeat_resident:
        print(json.dumps(_heartbeat_resident(), ensure_ascii=False, indent=2))
    elif _args.longzhao:
        print(json.dumps(dispatch_longzhao(_args.longzhao), ensure_ascii=False, indent=2))
    elif _args.wuxing:
        print(json.dumps(dispatch_wuxing(_args.wuxing), ensure_ascii=False, indent=2))
    else:
        demo()
