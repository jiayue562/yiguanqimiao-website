# -*- coding: utf-8 -*-
"""
龙心OS · 常驻子系统注册表（深度共生核心）
========================================

龙心OS 1+5 总调度在加载调度中枢时即导入本模块，使五行人格心理学OS等子系统
**常驻**于总调度上下文（非按需临时挂载）。总调度每轮 run() 会询问各常驻子系统
是否处理当前输入，命中则派发并将结果回灌龙心共享共生记忆。

新增常驻子系统：在 RESIDENT_SUBSYSTEMS 中追加其实例即可，零侵入接入总调度。
"""

from .wuxing_subsystem import wuxing_subsystem
from .longzhao_subsystem import longzhao_subsystem

# 常驻子系统清单（龙心OS总调度加载即注册）
RESIDENT_SUBSYSTEMS = [
    wuxing_subsystem,
    longzhao_subsystem,
]

# 多轮反哺：历史派发频次 → 路由置信度提升
try:
    from .feedback import read_history, boost_for
    _FEEDBACK_ENABLED = True
except Exception:  # pragma: no cover
    _FEEDBACK_ENABLED = False


def dispatch_all(text: str) -> dict:
    """遍历常驻子系统，命中意图者派发并回灌龙心记忆（多轮反哺增强）。

    返回 {subsystem_name: handle_result, ...}；无任何命中返回 {}。
    每个子系统的派发均自带降级，单个失败不影响其余。
    多轮反哺：依据历史 feed 频次为成熟子系统提升路由置信度。
    """
    results = {}
    hist = read_history() if _FEEDBACK_ENABLED else {}
    for sub in RESIDENT_SUBSYSTEMS:
        try:
            conf = boost_for(sub.name, hist) if _FEEDBACK_ENABLED else None
            r = sub.handle(text, confidence=conf)
            if r.get("handled"):
                results[sub.name] = r
        except Exception:  # pragma: no cover - 单子系统异常隔离
            continue
    return results


def heartbeat_all() -> list:
    """常驻存活探针集合（供调度中枢健康检查/共生环存活校验）。"""
    out = []
    for sub in RESIDENT_SUBSYSTEMS:
        try:
            out.append(sub.heartbeat())
        except Exception:
            out.append({"subsystem": getattr(sub, "name", "?"), "status": "error"})
    return out


def list_resident() -> list:
    """已注册常驻子系统清单。"""
    return [
        {"name": s.name, "display": s.display_name, "resident": s.resident, "layer": s.layer}
        for s in RESIDENT_SUBSYSTEMS
    ]
