#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心OS · 人机协同五象限引擎
Q1 目标对齐 / Q2 角色分工 / Q3 信息透明 / Q4 决策权限 / Q5 反馈闭环
将"人+AI"协作拆解为五个可执行的治理象限

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class Quadrant(Enum):
    Q1 = "Q1"  # 目标对齐
    Q2 = "Q2"  # 角色分工
    Q3 = "Q3"  # 信息透明
    Q4 = "Q4"  # 决策权限
    Q5 = "Q5"  # 反馈闭环


@dataclass
class QuadrantPlan:
    quadrant: Quadrant
    name: str
    principle: str
    action: str
    owner: str = ""  # human / ai / shared


@dataclass
class CollaborationResult:
    task: str
    plans: List[QuadrantPlan] = field(default_factory=list)
    summary: str = ""


class FiveQuadrantEngine:
    """人机协同五象限：为任一协作任务生成五象限治理方案。"""

    QUADRANT_META = {
        Quadrant.Q1: ("目标对齐", "人与AI对『要什么』达成共识", "用一句话重写任务目标，双方确认", "shared"),
        Quadrant.Q2: ("角色分工", "明确谁做什么", "列出AI负责项与人类负责项，避免重叠", "shared"),
        Quadrant.Q3: ("信息透明", "共享上下文与约束", "约定输入/输出格式与更新频率", "ai"),
        Quadrant.Q4: ("决策权限", "界定审批边界", "标注哪些需人审批、哪些AI可自主", "human"),
        Quadrant.Q5: ("反馈闭环", "持续校准", "设定复盘节奏与纠偏机制", "shared"),
    }

    def run(self, task: str, human_control: bool = True) -> CollaborationResult:
        result = CollaborationResult(task=task)
        for q in Quadrant:
            name, principle, action, owner = self.QUADRANT_META[q]
            # 决策权限象限：若 human_control 则人审批，否则AI自主
            if q == Quadrant.Q4:
                action = ("人类保留最终审批权" if human_control
                          else "AI在约定范围内自主决策，越界上报")
            plan = QuadrantPlan(quadrant=q, name=name, principle=principle,
                                action=action, owner=owner)
            result.plans.append(plan)
        result.summary = (
            f"任务「{task}」的人机协同方案：目标先对齐(Q1)，再分工(Q2)与透明(Q3)，"
            f"决策权限{'由人把关(Q4)' if human_control else 'AI自主+越界上报(Q4)'}，"
            f"最后以反馈闭环(Q5)持续校准。"
        )
        return result

    def format_text(self, result: CollaborationResult) -> str:
        lines = [f"【人机协同五象限 · {result.task}】"]
        for p in result.plans:
            lines.append(f"  {p.quadrant.value} {p.name}（{p.owner}）：{p.principle} → {p.action}")
        lines.append(f"  🔗 {result.summary}")
        return "\n".join(lines)


def demo():
    engine = FiveQuadrantEngine()
    r = engine.run("用AI辅助撰写味藏品牌白皮书", human_control=True)
    print(engine.format_text(r))


if __name__ == "__main__":
    demo()
