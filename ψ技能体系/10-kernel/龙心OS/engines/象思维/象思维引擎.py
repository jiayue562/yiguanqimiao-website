#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心OS · 象思维引擎
认知模式四步法（取象→类比→体悟→运化）
感知模式（观→比→体→化）
象类型学（老子四象：无象 / 有象 / 意象 / 道象）

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class XiangType(Enum):
    WU = "无象"    # 未显化的混沌
    YOU = "有象"   # 具体可感之象
    YI = "意象"    # 意在言外之象
    DAO = "道象"   # 合道之象


@dataclass
class CognitionStep:
    step: int
    name: str
    method: str
    output: str = ""


@dataclass
class PerceptionStep:
    step: int
    name: str
    method: str


@dataclass
class XiangSiWeiResult:
    context: str
    cognition: List[CognitionStep] = field(default_factory=list)
    perception: List[PerceptionStep] = field(default_factory=list)
    xiang_type: XiangType = XiangType.YOU
    insight: str = ""


class XiangSiWeiEngine:
    """象思维：0→1 的原创性直觉洞察引擎。"""

    COGNITION_PIPELINE = [
        ("取象", "从情境中抓取最具代表性的象"),
        ("类比", "以已知之象映照未知之象"),
        ("体悟", "以身/心代入，得默会之知"),
        ("运化", "将象转化为可落地的意象与行动"),
    ]

    PERCEPTION_PIPELINE = [
        ("观", "静观其变，不急于判断"),
        ("比", "异中求同、同中求异"),
        ("体", "以身体与情感共鸣"),
        ("化", "将感受转化为创见"),
    ]

    TYPE_GUIDANCE = {
        XiangType.WU: "尚处混沌，宜先放空再取象",
        XiangType.YOU: "象已具体，可直接类比运化",
        XiangType.YI: "意在言外，宜以体悟补足",
        XiangType.DAO: "已合道，可直接落地为道象产品",
    }

    def __init__(self, default_type: XiangType = XiangType.YOU):
        self.default_type = default_type

    def run(self, context: str, xiang_type: Optional[XiangType] = None) -> XiangSiWeiResult:
        xt = xiang_type or self.default_type
        result = XiangSiWeiResult(context=context, xiang_type=xt)

        for i, (name, method) in enumerate(self.COGNITION_PIPELINE, 1):
            result.cognition.append(CognitionStep(step=i, name=name, method=method))

        for i, (name, method) in enumerate(self.PERCEPTION_PIPELINE, 1):
            result.perception.append(PerceptionStep(step=i, name=name, method=method))

        result.insight = (
            f"针对「{context}」，以象思维运作：先{self.COGNITION_PIPELINE[0][0]}抓取核心象，"
            f"经{self.COGNITION_PIPELINE[1][0]}与{self.COGNITION_PIPELINE[2][0]}抵达默会之知，"
            f"终由{self.COGNITION_PIPELINE[3][0]}落地。当前象态为「{xt.value}」——{self.TYPE_GUIDANCE[xt]}。"
        )
        return result

    def format_text(self, result: XiangSiWeiResult) -> str:
        lines = [f"【象思维 · {result.context}】"]
        lines.append("  认知模式四步法：")
        for s in result.cognition:
            lines.append(f"    {s.step}. {s.name}：{s.method}")
        lines.append("  感知模式（观比体化）：")
        for s in result.perception:
            lines.append(f"    {s.step}. {s.name}：{s.method}")
        lines.append(f"  象类型：{result.xiang_type.value}")
        lines.append(f"  💡 {result.insight}")
        return "\n".join(lines)


def demo():
    engine = XiangSiWeiEngine()
    r = engine.run("如何让味藏的品牌更有东方禅意")
    print(engine.format_text(r))


if __name__ == "__main__":
    demo()
