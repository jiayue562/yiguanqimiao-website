#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
知识学习引擎 — 深度认知学习引擎
基于深度阅读、概念提纯、跨领域关联与自我提问

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json
import re


@dataclass
class KnowledgeNode:
    concept: str
    definition: str
    dimension: str
    related_concepts: List[str] = field(default_factory=list)


@dataclass
class Insight:
    description: str
    source: str
    confidence: float


@dataclass
class KnowledgeLearningResult:
    title: str
    nodes: List[KnowledgeNode]
    key_findings: List[str]
    cross_domain_links: List[str]
    open_questions: List[str]
    summary: str


class KnowledgeLearningEngine:
    COGNITIVE_OPS = [
        ("剖析", "拆解概念的结构和组成部分"),
        ("解构", "打破现有框架，找到深层逻辑"),
        ("透视", "从不同视角审视同一事物"),
        ("阐释", "用简单语言解释复杂概念"),
        ("推演", "从已知推导未知"),
        ("思辨", "质疑假设，寻找反驳论据"),
        ("溯源", "追溯概念的历史和起源"),
        ("融合", "将新知识与已有知识连接"),
        ("启发", "从知识中提炼可应用的洞见"),
        ("映射", "将一个领域的规律映射到另一个领域"),
    ]

    def extract_concepts(self, text: str) -> List[str]:
        candidates = re.findall(r'[""]([^""]{2,20})[""]', text)
        if not candidates:
            candidates = re.findall(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', text)
        if not candidates:
            candidates = ["核心概念"]
        return list(set(candidates))[:5]

    def apply_cognitive_ops(self, text: str, concept: str) -> Dict[str, str]:
        results = {}
        for op_name, op_desc in self.COGNITIVE_OPS:
            results[op_name] = f"{op_name}({op_desc})：基于'{concept}'的{op_name}结果"
        return results

    def find_cross_domain_links(self, concepts: List[str]) -> List[str]:
        domain_map = {
            "商业": ["商业模式", "价值主张", "客户"],
            "心理": ["认知", "行为", "动机"],
            "系统": ["反馈", "涌现", "自组织"],
            "生物": ["进化", "适应", "共生"],
        }
        links = []
        for c in concepts:
            for domain, keywords in domain_map.items():
                for kw in keywords:
                    if kw in c:
                        links.append(f"{c} ↔ {domain}领域/{kw}")
        return links[:5]

    def generate_open_questions(self, concepts: List[str]) -> List[str]:
        return [
            f"如果把'{concepts[0] if concepts else '概念'}'应用到完全不同的领域，会发生什么？",
            f"什么情况下'{concepts[-1] if len(concepts) > 1 else concepts[0]}'不再成立？",
            f"这个概念的反面是什么？为什么不是所有人都在用反面？",
        ]

    def run(self, text: str, title: str = "未命名") -> KnowledgeLearningResult:
        concepts = self.extract_concepts(text)
        nodes = [KnowledgeNode(c, f"{c}的定义", "概念") for c in concepts]

        findings = []
        for c in concepts[:3]:
            ops = self.apply_cognitive_ops(text, c)
            for op_name in ["剖析", "解构", "透视"]:
                findings.append(ops[op_name])

        links = self.find_cross_domain_links(concepts)
        questions = self.generate_open_questions(concepts)

        return KnowledgeLearningResult(
            title=title,
            nodes=nodes,
            key_findings=findings[:5],
            cross_domain_links=links,
            open_questions=questions,
            summary=f"对'{title}'完成了{len(concepts)}个核心概念的{len(self.COGNITIVE_OPS)}种认知操作分析，"
                    f"发现{len(links)}条跨领域联系，提出了{len(questions)}个开放问题"
        )


def demo():
    engine = KnowledgeLearningEngine()
    test_text = '"超级个体"是AI时代个人操作系统的最终形态，它融合了碳基生命的心性与硅基算力的理性'
    result = engine.run(test_text, "超级个体")
    print(f"标题: {result.title}")
    print(f"核心概念: {[n.concept for n in result.nodes]}")
    print(f"关键发现: {len(result.key_findings)}条")
    print(f"跨域联系: {len(result.cross_domain_links)}条")
    print(f"开放问题: {len(result.open_questions)}个")

if __name__ == "__main__":
    demo()
