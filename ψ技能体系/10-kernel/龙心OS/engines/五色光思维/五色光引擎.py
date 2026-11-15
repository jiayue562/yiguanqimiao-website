#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙心OS · 五色光思维引擎
白(事实) / 红(情感) / 黄(价值) / 绿(创意) / 蓝(控制) + 主持人
德博诺六顶思考帽的东方化重构

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LightColor(Enum):
    WHITE = "白"   # 事实 · 客观数据
    RED = "红"     # 情感 · 直觉感受
    YELLOW = "黄"  # 价值 · 积极收益
    GREEN = "绿"   # 创意 · 可能性
    BLUE = "蓝"    # 控制 · 流程与风险


@dataclass
class ColorView:
    color: LightColor
    dimension: str
    focus: str
    prompt: str
    output: str = ""


@dataclass
class FiveColorResult:
    topic: str
    views: List[ColorView] = field(default_factory=list)
    sequence: List[str] = field(default_factory=list)
    host_summary: str = ""


class FiveColorEngine:
    """五色光思维：对任一议题给出五色平行的立体审视，主持人(蓝)统合。"""

    COLOR_META = {
        LightColor.WHITE: ("事实", "客观收集数据，剥离立场", "列出与议题相关的可验证事实与数据"),
        LightColor.RED: ("情感", "直觉与感受，不要求理由", "表达对此议题的第一直觉与情绪反应"),
        LightColor.YELLOW: ("价值", "积极面与收益", "寻找议题中的希望、价值与正向可能"),
        LightColor.GREEN: ("创意", "可能性与新点子", "发散生成非常规的解决思路"),
        LightColor.BLUE: ("控制", "流程审视与风险控制", "检查前面的思考是否跑题，并识别风险"),
    }

    # 默认运作用色序列（蓝光在首尾控制）
    DEFAULT_SEQUENCE = [LightColor.WHITE, LightColor.RED, LightColor.YELLOW,
                        LightColor.GREEN, LightColor.BLUE]

    def run(self, topic: str, sequence: Optional[List[LightColor]] = None) -> FiveColorResult:
        seq = sequence or self.DEFAULT_SEQUENCE
        result = FiveColorResult(topic=topic, sequence=[c.value for c in seq])
        for color in seq:
            dim, focus, prompt = self.COLOR_META[color]
            view = ColorView(color=color, dimension=dim, focus=focus, prompt=prompt)
            result.views.append(view)
        # 主持人(蓝)统合摘要
        result.host_summary = (
            f"关于「{topic}」：先以白光夯实事实，红光诚实表达感受，"
            f"黄光挖掘价值，绿光发散创意，最后由蓝光控制节奏并识别风险，"
            f"形成平行而完整的决策光谱。"
        )
        return result

    def format_text(self, result: FiveColorResult) -> str:
        lines = [f"【五色光思维 · {result.topic}】"]
        for v in result.views:
            lines.append(f"  {v.color.value}光（{v.dimension}）：{v.focus} — {v.prompt}")
        lines.append(f"  🎙 主持人：{result.host_summary}")
        return "\n".join(lines)


def demo():
    engine = FiveColorEngine()
    r = engine.run("是否要开第二家味藏门店")
    print(engine.format_text(r))


if __name__ == "__main__":
    demo()
