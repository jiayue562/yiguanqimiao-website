# -*- coding: utf-8 -*-
"""
龙心OS · 多轮反哺记忆（深度共生·闭环增强）
==========================================

读取五行 / 龙爪 共享共生记忆（JSON-Lines feed），统计各常驻子系统历史派发频次，
用于「龙心派发 → 五行/龙爪回灌 → 影响后续路由」的多轮反哺闭环：
  - 某子系统被派发越多次，其后续同类意图的路由置信度越高（封顶 0.99）
  - 调度中枢 dispatch_all 据此提升成熟子系统的优先级，抑制误触

与两子系统共享同一 feed 路径常量，保证读写落点一致。
"""

import os
import json

# 与 wuxing_subsystem / longzhao_subsystem 共享的 feed 落点
WUXING_FEED = os.path.expanduser(
    "~/.workbuddy/skills/五行人格心理学OS/runtime/longxin_symbiosis_feed.jsonl"
)
LONGZHAO_FEED = os.path.expanduser(
    "~/.workbuddy/skills/龙爪OS/runtime/longzhao_symbiosis_feed.jsonl"
)


def read_history() -> dict:
    """读取两 feed，统计各子系统历史派发次数。返回 {"wuxing_os": n, "longzhao_os": n}。"""
    hist = {"wuxing_os": 0, "longzhao_os": 0}
    for name, feed in (("wuxing_os", WUXING_FEED), ("longzhao_os", LONGZHAO_FEED)):
        if os.path.isfile(feed):
            try:
                with open(feed, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            json.loads(line)
                            hist[name] += 1
                        except Exception:
                            continue
            except Exception:
                continue
    return hist


def boost_for(sub_name: str, history: dict, base: float = 0.5) -> float:
    """多轮反哺：历史派发次数越多，路由置信度越高（封顶 0.99）。"""
    n = history.get(sub_name, 0)
    return min(0.99, round(base + 0.03 * n, 3))
