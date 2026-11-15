"""水行人分智能体 · learning_loop.py
自主学习引擎：盲区检测/知识蒸馏
"""
from typing import Dict, List


class WaterLearningLoop:
    """水行学习循环"""

    def __init__(self):
        self.knowledge_gaps = []
        self.distillation_log = []

    def detect_blind_spots(self, user_input: str, kb_result: Dict) -> List[str]:
        """检测用户问题中未被知识覆盖的盲区"""
        blind_spots = []
        key_concepts = ["智慧", "恐惧", "依赖", "包容", "变通", "直觉", "焦虑", "共情",
                        "想象力", "深度思考", "沉溺", "拖延", "灵感", "逃避", "润泽"]
        for concept in key_concepts:
            if concept in user_input:
                covered = False
                for domain in kb_result.get("matched_domains", []):
                    if concept in str(kb_result.get("knowledge", {})):
                        covered = True
                        break
                if not covered:
                    blind_spots.append(concept)
                    self.knowledge_gaps.append(concept)
        return blind_spots

    def distill_knowledge(self, conversation: List[Dict]) -> Dict:
        """从对话中蒸馏新知"""
        insights = []
        for turn in conversation[-5:]:
            user_msg = turn.get("user", "")
            assistant_msg = turn.get("assistant", "")
            if "原来" in user_msg or "明白" in user_msg:
                insights.append({"source": "用户顿悟", "content": user_msg[-50:]})
            if "润泽" in user_msg or "智慧" in user_msg or "包容" in user_msg:
                insights.append({"source": "水行关键词触发", "content": user_msg[-50:]})
        return {"new_insights": insights, "total_gaps": len(self.knowledge_gaps)}
