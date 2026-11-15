"""
凤心OS · 自主学习循环
持续进化机制 · 每轮对话后自动沉淀知识
version: v1.0 (2026-07-21)
"""

import json
from datetime import datetime


class LearningLoop:
    """凤心OS自主学习引擎：知识蒸馏+盲区检测+进化记录"""

    # 跨域联系总数（从kb_engine引用）
    HIDDEN_CONNECTIONS_COUNT = 22

    def __init__(self):
        self.interactions = []
        self.blind_spots = set()

    # 盲区初始检测
    BLIND_SPOT_DETECTIONS = {
        "五行识别混淆": "当用户描述的行为特征同时符合多行时，如何精准判定主导行",
        "认知偏差深度归因": "某一偏差背后可能同时涉及多个系统1特征的综合作用",
        "跨行拔阴取阳": "阴水恐+阴金冷同时出现时，应先拔哪行？", 
        "双系统融合边界": "何种情境下快思考的直觉判断准确度高于慢思考的逻辑分析",
        "峰终定律×五行": "不同五行人格的峰终敏感度是否不同（如木行更关注峰值，土行更关注终点）",
        "框架效应×五行适应": "不同五行对同一框架的情绪反应强度是否不同",
    }

    def record_interaction(self, user_input: str, route: dict, output: str):
        """记录交互日志"""
        self.interactions.append({
            "timestamp": datetime.now().isoformat(),
            "input_snippet": user_input[:100],
            "route_type": route.get("route_type", "unknown"),
            "agents": route.get("agents", []),
        })

    def detect_knowledge_gap(self, user_input: str) -> list:
        """检测当前输入是否触发了已知盲区"""
        triggered = []
        for spot, desc in self.BLIND_SPOT_DETECTIONS.items():
            keywords = spot.replace("混淆", "").replace("归因", "").replace("转化", "")
            if any(kw in user_input for kw in keywords.split("、")):
                triggered.append({
                    "盲区": spot,
                    "描述": desc,
                    "建议": "触发盲区→建议结合五色光思维(蓝/白/红光)多角度分析"
                })
        return triggered

    def summarize_knowledge(self) -> dict:
        """生成当前知识状态摘要"""
        total_interactions = len(self.interactions)
        route_counts = {}
        for i in self.interactions:
            rt = i["route_type"]
            route_counts[rt] = route_counts.get(rt, 0) + 1

        return {
            "总交互次数": total_interactions,
            "路由分布": route_counts,
            "盲区检测": list(self.BLIND_SPOT_DETECTIONS.keys()),
            "跨域联系数": self.HIDDEN_CONNECTIONS_COUNT,
        }


# 单例
learning_loop = LearningLoop()
