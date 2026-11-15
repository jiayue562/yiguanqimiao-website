#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
具身关系格式塔引擎 — E0-E6具身样态推断
基于"合于场域之道→疗愈自然显化"的核心公式

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class EmbodiedState(Enum):
    E0 = "E0"  # 未分化·原初场域
    E1 = "E1"  # 感知锚定·具身定位
    E2 = "E2"  # 关系涌现·互动模式
    E3 = "E3"  # 样态分化·特征显化
    E4 = "E4"  # 反身觉知·自我观察
    E5 = "E5"  # 整合重构·新样态形成
    E6 = "E6"  # 场域共振·与道合一


STATE_LABELS = {
    EmbodiedState.E0: "未分化·原初场域",
    EmbodiedState.E1: "感知锚定·具身定位",
    EmbodiedState.E2: "关系涌现·互动模式",
    EmbodiedState.E3: "样态分化·特征显化",
    EmbodiedState.E4: "反身觉知·自我观察",
    EmbodiedState.E5: "整合重构·新样态形成",
    EmbodiedState.E6: "场域共振·与道合一",
}


@dataclass
class GestaltProfile:
    state: EmbodiedState
    description: str
    keywords: List[str]
    suggested_action: str


@dataclass
class GestaltResult:
    current_state: EmbodiedState
    state_label: str
    profile: GestaltProfile
    transition_path: List[EmbodiedState]
    integration_suggestion: str


class GestaltEngine:
    def __init__(self):
        self.profiles = {
            EmbodiedState.E0: GestaltProfile(
                EmbodiedState.E0, "混沌未分，一切可能", ["模糊", "不确定", "全新"],
                "先不做判断，充分感知场域"
            ),
            EmbodiedState.E1: GestaltProfile(
                EmbodiedState.E1, "身体感知到具体的信号", ["紧张", "放松", "温暖", "冷"],
                "锚定这个身体信号，用语言描述它"
            ),
            EmbodiedState.E2: GestaltProfile(
                EmbodiedState.E2, "关系中的互动模式浮现", ["对抗", "回避", "依赖", "支持"],
                "识别关系模式，不评判好坏"
            ),
            EmbodiedState.E3: GestaltProfile(
                EmbodiedState.E3, "特征分化，轮廓清晰", ["独特", "边界", "差异"],
                "允许特征存在，不试图改变"
            ),
            EmbodiedState.E4: GestaltProfile(
                EmbodiedState.E4, "觉察自己在觉察", ["元认知", "旁观", "觉知"],
                "保持观看，不介入"
            ),
            EmbodiedState.E5: GestaltProfile(
                EmbodiedState.E5, "碎片整合为新的整体", ["连接", "重组", "升华"],
                "让新样态自然形成"
            ),
            EmbodiedState.E6: GestaltProfile(
                EmbodiedState.E6, "与更大的场域共振", ["合一", "自然", "不费力"],
                "不执着于这个状态，让它自然来去"
            ),
        }

    def infer_state(self, context: str) -> Tuple[EmbodiedState, float]:
        context_lower = context.lower()
        scores = {state: 0 for state in EmbodiedState}
        for state, profile in self.profiles.items():
            for kw in profile.keywords:
                if kw in context_lower:
                    scores[state] += 1
        best = max(scores, key=scores.get)
        confidence = scores[best] / max(sum(scores.values()), 1)
        return best, confidence

    def get_transition_path(self, from_state: EmbodiedState, to_state: EmbodiedState) -> List[EmbodiedState]:
        states = list(EmbodiedState)
        try:
            start = states.index(from_state)
            end = states.index(to_state)
            if start <= end:
                return states[start:end+1]
            return states[start:] + states[:end+1]
        except ValueError:
            return [from_state, to_state]

    def run(self, context: str) -> GestaltResult:
        state, _ = self.infer_state(context)
        profile = self.profiles[state]
        path = self.get_transition_path(state, EmbodiedState.E6)
        return GestaltResult(
            current_state=state,
            state_label=STATE_LABELS[state],
            profile=profile,
            transition_path=path,
            integration_suggestion=f"从{STATE_LABELS[state]}出发，沿{'→'.join(STATE_LABELS[s] for s in path)}路径整合"
        )


def demo():
    engine = GestaltEngine()
    test_contexts = ["团队氛围紧张", "突然有个新想法", "一切都很顺利"]
    for ctx in test_contexts:
        result = engine.run(ctx)
        print(f"[{ctx}] → {result.state_label} | 建议: {result.profile.suggested_action}")

if __name__ == "__main__":
    demo()
