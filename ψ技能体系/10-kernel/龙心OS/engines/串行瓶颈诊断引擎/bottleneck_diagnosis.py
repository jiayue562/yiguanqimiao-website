#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
串行瓶颈诊断引擎 — BN-INF/DEC/CRD/CTX瓶颈检测
识别组织/流程中的瓶颈环节

版本：v1.0
创建：2026-07-28
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BottleneckType(Enum):
    BN_INF = "BN-INF"  # 信息瓶颈：信息不对称/信息延迟
    BN_DEC = "BN-DEC"  # 决策瓶颈：决策权不匹配/决策延迟
    BN_CRD = "BN-CRD"  # 协同瓶颈：协同效率低/资源冲突
    BN_CTX = "BN-CTX"  # 上下文瓶颈：缺乏全局视角/局部最优


BN_LABELS = {
    BottleneckType.BN_INF: "信息瓶颈",
    BottleneckType.BN_DEC: "决策瓶颈",
    BottleneckType.BN_CRD: "协同瓶颈",
    BottleneckType.BN_CTX: "上下文瓶颈",
}


@dataclass
class BottleneckReport:
    type: BottleneckType
    severity: float
    location: str
    symptom: str
    root_cause: str
    impact: str
    suggestion: str


@dataclass
class DiagnosisResult:
    bottlenecks: List[BottleneckReport]
    primary_bottleneck: Optional[BottleneckReport]
    overall_severity: float
    summary: str


class BottleneckDiagnosisEngine:
    PATTERNS = {
        BottleneckType.BN_INF: {
            "keywords": ["不知道", "信息不通", "数据不准", "沟通不畅", "没收到"],
            "locations": ["跨部门", "上下级", "系统接口"],
            "symptoms": ["信息不对称", "数据延迟", "重复沟通"],
        },
        BottleneckType.BN_DEC: {
            "keywords": ["等批复", "没人拍板", "权限不够", "决策慢", "不敢定"],
            "locations": ["决策层", "审批环节", "责权边界"],
            "symptoms": ["决策延迟", "推诿扯皮", "决策质量低"],
        },
        BottleneckType.BN_CRD: {
            "keywords": ["各干各的", "资源抢", "冲突", "配合差", "重复劳动"],
            "locations": ["跨团队", "资源分配", "流程交接"],
            "symptoms": ["协同效率低", "资源竞争", "接口摩擦"],
        },
        BottleneckType.BN_CTX: {
            "keywords": ["只顾自己", "看不到全局", "短视", "局部最优", "本位"],
            "locations": ["组织边界", "部门墙", "信息孤岛"],
            "symptoms": ["局部优化", "全局次优", "目标不一致"],
        },
    }

    def detect(self, context: str) -> List[BottleneckReport]:
        reports = []
        context_lower = context.lower()
        for bn_type, patterns in self.PATTERNS.items():
            matched = [kw for kw in patterns["keywords"] if kw in context_lower]
            if matched:
                severity = min(len(matched) / len(patterns["keywords"]) * 10, 10)
                reports.append(BottleneckReport(
                    type=bn_type,
                    severity=round(severity, 1),
                    location=patterns["locations"][len(matched) % len(patterns["locations"])],
                    symptom=patterns["symptoms"][0],
                    root_cause=f"{BN_LABELS[bn_type]}的根本原因分析",
                    impact=f"影响整体效率约{severity * 10}%",
                    suggestion=f"建议优先解决{BN_LABELS[bn_type]}问题"
                ))
        return reports

    def run(self, context: str) -> DiagnosisResult:
        bottlenecks = self.detect(context)
        primary = max(bottlenecks, key=lambda b: b.severity) if bottlenecks else None

        if bottlenecks:
            avg_severity = round(sum(b.severity for b in bottlenecks) / len(bottlenecks), 1)
        else:
            avg_severity = 0

        return DiagnosisResult(
            bottlenecks=bottlenecks,
            primary_bottleneck=primary,
            overall_severity=avg_severity,
            summary=f"检测到{len(bottlenecks)}类瓶颈，主要瓶颈为{BN_LABELS[primary.type] if primary else '无'}"
            + (f"，严重度{avg_severity}/10" if bottlenecks else "")
        )


def demo():
    engine = BottleneckDiagnosisEngine()
    test = "跨部门沟通不畅，等批复很慢，公司信息不通，各团队各干各的"
    result = engine.run(test)
    print(f"瓶颈检测: {len(result.bottlenecks)}类")
    for b in result.bottlenecks:
        print(f"  [{b.type.value}] {b.symptom} (严重度{b.severity}/10)")
    print(f"主要瓶颈: {BN_LABELS[result.primary_bottleneck.type] if result.primary_bottleneck else '无'}")
    print(f"综合严重度: {result.overall_severity}/10")

if __name__ == "__main__":
    demo()
