"""
凤爪OS · 学习循环
version: v1.0 (2026-07-21)
"""


class FengZhaoLearning:
    """凤爪OS学习引擎"""

    BLIND_SPOTS = [
        "庄子三无如何在8大应用场景中差异化应用",
        "至人无己与心理健康的关系边界",
        "神人无功如何与现代社会激励机制共存",
        "不同人格对三无修法的敏感度差异",
    ]

    def detect_gap(self, user_input: str) -> list:
        triggered = []
        for spot in self.BLIND_SPOTS:
            for kw in spot.split("如何"):
                if kw[:4] in user_input:
                    triggered.append(spot)
                    break
        return triggered


learning = FengZhaoLearning()
