#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龙脑OS 选刃引擎
将选刃决策树文档中的8类场景映射表转化为可程序调用的匹配引擎

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    JY = "JY"  # 经营分析型
    ZL = "ZL"  # 战略决策型
    FA = "FA"  # 方案设计型
    WD = "WD"  # 问题诊断型
    GT = "GT"  # 沟通协作型
    XX = "XX"  # 学习研究型
    CZ = "CZ"  # 自我成长型
    CY = "CY"  # 创意创新型


TASK_LABELS = {
    TaskType.JY: "经营分析型",
    TaskType.ZL: "战略决策型",
    TaskType.FA: "方案设计型",
    TaskType.WD: "问题诊断型",
    TaskType.GT: "沟通协作型",
    TaskType.XX: "学习研究型",
    TaskType.CZ: "自我成长型",
    TaskType.CY: "创意创新型",
}


@dataclass
class ModelRecommendation:
    model_id: str
    name: str
    priority: str  # primary / alternative
    reason: str


@dataclass
class BladeChain:
    primary_chain: List[ModelRecommendation]
    alternative_chain: List[ModelRecommendation]
    combination_logic: str
    confidence: float


class BladeEngine:
    def __init__(self):
        self._build_chains()

    def _build_chains(self):
        self.chains: Dict[TaskType, BladeChain] = {}

        self.chains[TaskType.JY] = BladeChain(
            primary_chain=[
                ModelRecommendation("bottleneck_theory", "瓶颈理论", "primary", "定位阻塞环节"),
                ModelRecommendation("five_layer_analysis", "五层分析法", "primary", "逐层穿透根因"),
            ],
            alternative_chain=[
                ModelRecommendation("systems_thinking", "系统思维", "alternative", "检查多环节联动"),
                ModelRecommendation("pareto", "帕累托法则", "alternative", "筛选20%核心因素"),
                ModelRecommendation("probabilistic", "概率思维", "alternative", "量化不确定性"),
            ],
            combination_logic="瓶颈理论定位阻塞点 → 五层分析法逐层拆解 → 帕累托筛选核心因素",
            confidence=0.90
        )

        self.chains[TaskType.ZL] = BladeChain(
            primary_chain=[
                ModelRecommendation("yijing", "易经错综复杂", "primary", "五维全局审视"),
                ModelRecommendation("decision_matrix", "决策矩阵", "primary", "多指标量化评分"),
                ModelRecommendation("second_order", "二阶思维", "primary", "考虑后果的后果"),
            ],
            alternative_chain=[
                ModelRecommendation("probabilistic", "概率思维", "alternative", "量化不确定性"),
                ModelRecommendation("inversion", "逆向思维", "alternative", "反向推演风险"),
                ModelRecommendation("opportunity_cost", "机会成本", "alternative", "隐性代价分析"),
            ],
            combination_logic="错综复杂五维审视 → 决策矩阵量化评分 → 二阶思维推演后果",
            confidence=0.85
        )

        self.chains[TaskType.FA] = BladeChain(
            primary_chain=[
                ModelRecommendation("5w2h", "5W2H", "primary", "无死角检查清单"),
                ModelRecommendation("pyramid", "金字塔原理", "primary", "结构化表达"),
                ModelRecommendation("orid", "ORID", "primary", "从事实到行动的闭环"),
            ],
            alternative_chain=[
                ModelRecommendation("framework", "框架思维", "alternative", "套用已有框架"),
                ModelRecommendation("value_focus", "价值聚焦", "alternative", "锚定核心价值"),
            ],
            combination_logic="5W2H全面检查 → 金字塔原理组织内容 → ORID落地闭环",
            confidence=0.88
        )

        self.chains[TaskType.WD] = BladeChain(
            primary_chain=[
                ModelRecommendation("five_whys", "5Whys", "primary", "单线因果深挖"),
                ModelRecommendation("systems_thinking", "系统思维", "primary", "多环节联动检查"),
                ModelRecommendation("socratic", "苏格拉底式提问", "primary", "澄清问题本身"),
            ],
            alternative_chain=[
                ModelRecommendation("five_dimension", "五维问题拆解法", "alternative", "多维度拆解"),
                ModelRecommendation("chaos_to_clarity", "从一团乱麻到清晰方案", "alternative", "混沌结构化"),
            ],
            combination_logic="苏格拉底式提问界定问题 → 5Whys深挖根因 → 系统思维横向扩展",
            confidence=0.85
        )

        self.chains[TaskType.GT] = BladeChain(
            primary_chain=[
                ModelRecommendation("six_hats", "六顶思考帽", "primary", "剥离人与立场"),
                ModelRecommendation("rapoport", "拉波波特法则", "primary", "让对方听见反对"),
                ModelRecommendation("sbi", "SBI反馈模型", "primary", "用事实替代评判"),
            ],
            alternative_chain=[
                ModelRecommendation("five_levels", "沟通五层次", "alternative", "关系深度诊断"),
                ModelRecommendation("rule_of_three", "三的法则", "alternative", "简洁有力表达"),
            ],
            combination_logic="六顶思考帽平行思考 → 拉波波特法则说服 → SBI给出反馈",
            confidence=0.82
        )

        self.chains[TaskType.XX] = BladeChain(
            primary_chain=[
                ModelRecommendation("ten_integration", "十种知识整合方式", "primary", "跨领域连接"),
                ModelRecommendation("first_principles", "第一性原理", "primary", "回归本质"),
                ModelRecommendation("framework", "框架思维", "primary", "套入认知结构"),
            ],
            alternative_chain=[
                ModelRecommendation("jiaoyuan", "教员方法论", "alternative", "矛盾论×实践论"),
                ModelRecommendation("first_to_second", "从第一层到第二层", "alternative", "表层到深层"),
            ],
            combination_logic="第一性原理拆解本质 → 框架思维定位 → 十种整合方式连接",
            confidence=0.87
        )

        self.chains[TaskType.CZ] = BladeChain(
            primary_chain=[
                ModelRecommendation("five_layer_analysis", "五层分析法", "primary", "人性层+意义层向内审视"),
                ModelRecommendation("inversion", "逆向思维", "primary", "反向推演路径"),
                ModelRecommendation("value_focus", "价值聚焦", "primary", "锚定方向"),
            ],
            alternative_chain=[
                ModelRecommendation("guanbithua", "观比体化", "alternative", "共情体感向内看"),
                ModelRecommendation("anchor_to_breakthrough", "从锚定到破局", "alternative", "方向感重建"),
            ],
            combination_logic="五层分析法向内审视 → 逆向思维反推路径 → 价值聚焦锚定方向",
            confidence=0.80
        )

        self.chains[TaskType.CY] = BladeChain(
            primary_chain=[
                ModelRecommendation("guanbithua", "观比体化", "primary", "象思维原创灵感"),
                ModelRecommendation("scamper", "SCAMPER", "primary", "七维度结构化创新"),
                ModelRecommendation("inversion", "逆向思维", "primary", "打破思维惯性"),
            ],
            alternative_chain=[
                ModelRecommendation("first_principles", "第一性原理", "alternative", "从本质重新构建"),
                ModelRecommendation("einstein", "爱因斯坦式提问", "alternative", "假设重构可能性"),
            ],
            combination_logic="观比体化感知原创 → SCAMPER七维改造 → 逆向思维破惯性",
            confidence=0.85
        )

    def recommend(self, task_type: TaskType) -> Optional[BladeChain]:
        return self.chains.get(task_type)

    def get_all_model_ids(self) -> List[str]:
        all_ids = set()
        for chain in self.chains.values():
            for m in chain.primary_chain + chain.alternative_chain:
                all_ids.add(m.model_id)
        return sorted(all_ids)

    def format_output(self, task_type: TaskType) -> Optional[Dict]:
        chain = self.recommend(task_type)
        if not chain:
            return None
        return {
            "task_type": task_type.value,
            "task_label": TASK_LABELS[task_type],
            "primary_chain": [{"model_id": m.model_id, "name": m.name, "reason": m.reason} for m in chain.primary_chain],
            "alternative_chain": [{"model_id": m.model_id, "name": m.name, "reason": m.reason} for m in chain.alternative_chain],
            "combination_logic": chain.combination_logic,
            "confidence": chain.confidence,
        }


def demo():
    engine = BladeEngine()
    for t in TaskType:
        r = engine.format_output(t)
        if r:
            print(f"[{r['task_label']}] {r['combination_logic']} (confidence={r['confidence']})")
    print(f"\n全部模型数: {len(engine.get_all_model_ids())}")


if __name__ == "__main__":
    demo()
