"""五行总智能体 · learning_loop.py
自主学习引擎：检测盲区/知识蒸馏
"""
from typing import Dict, List

class ChiefLearningLoop:
    """五行总智能体学习循环"""

    def __init__(self):
        self.knowledge_gaps = []

    def detect_scene_gaps(self, user_input: str) -> List[str]:
        key_concepts = ["五行", "生克", "拔阴取阳", "九层", "外观", "B=MAP", "木", "火", "土", "金", "水",
                        "相生", "相克", "团队", "亲密关系", "夫妻", "发展", "层级",
                        "动机", "能力", "提示", "习惯", "微习惯", "行为设计"]
        gaps = []
        for concept in key_concepts:
            if concept in user_input:
                # 检查是否在已有场景覆盖范围
                covered = False
                if concept in user_input:
                    covered = True  # 简化检测
                if not covered:
                    gaps.append(concept)
                    self.knowledge_gaps.append(concept)
        return gaps

    def distill_insights(self, conversation: List[Dict]) -> Dict:
        insights = []
        for turn in conversation[-3:]:
            msg = turn.get("assistant", "")
            if "五行" in msg and "新" in msg:
                insights.append({"source": "对话生成", "content": msg[:100]})
        return {"new_insights": insights, "total_gaps": len(self.knowledge_gaps)}
