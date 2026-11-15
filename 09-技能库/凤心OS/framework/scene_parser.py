"""
凤心OS · 场景识别引擎
1+5模式 · 自动识别场景·感知五行需求
version: v1.0 (2026-07-21)
"""


class SceneParser:
    """凤凰OS引擎：从对话上下文中自动感知、理解场景、五行归类"""

    # 五大场景类型
    SCENE_CATEGORIES = {
        "木行场景": "生发·成长·创新·决策·领导·竞争·愤怒·顶撞·不服",
        "火行场景": "热情·表达·社交·演讲·急躁·炫耀·焦虑·嗔恨·连接",
        "土行场景": "稳定·承载·信义·包容·猜疑·纠结·怨气·依赖·防守",
        "金行场景": "规则·秩序·批判·决断·变革·批评·挑剔·刻薄·冷漠",
        "水行场景": "智慧·流动·恐惧·多思·拖延·逃避·灵感·共情·协调",
    }

    # 认知科学场景（快慢思考）
    COGNITIVE_SCENES = {
        "决策瓶颈": "损失厌恶·不确定性·框架效应·锚定效应",
        "判断偏差": "过度自信·代表性·可得性·叙事谬误",
        "记忆评估": "峰终定律·两个自我·后见之明·过程忽视",
        "行为设计": "B=MAP·动机·能力·提示·微习惯·庆祝",
    }

    # 对话信号→五行归类映射
    SIGNAL_MAP = {
        # 情绪信号
        "愤怒": "木", "急躁": "火", "顶撞": "木", "不服": "木",
        "焦虑": "火/水", "炫耀": "火", "嗔恨": "火",
        "猜疑": "土", "纠结": "土", "怨气": "土", "依赖": "土/水",
        "批评": "金", "挑剔": "金", "冷漠": "金/水",
        "恐惧": "水", "拖延": "水", "逃避": "水", "多思": "水",
        # 认知偏差信号
        "锚定": "cognitive", "框架": "cognitive", "后见之明": "cognitive",
        "过度自信": "cognitive", "峰终": "cognitive",
        # 发展信号
        "成长": "木", "学习": "水/金", "改变": "火/金",
        "习惯": "B=MAP", "目标": "火/金", "关系": "土/水",
    }

    def detect_scene(self, user_input: str) -> dict:
        """
        从用户输入中自动感知场景
        返回：{primary: str, secondary: str, cognitive: bool, confidence: float}
        """
        result = {"primary": "general", "secondary": "", "cognitive": False, "confidence": 0.0}

        # 扫描信号
        matched_elements = []
        for keyword, element in self.SIGNAL_MAP.items():
            if keyword in user_input:
                matched_elements.append(element)

        if not matched_elements:
            return result

        # 统计五行分布
        element_counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0, "cognitive": 0, "B=MAP": 0}
        for e in matched_elements:
            if "/" in e:
                for sub in e.split("/"):
                    if sub in element_counts:
                        element_counts[sub] += 1
            elif e in element_counts:
                element_counts[e] += 1

        # 判定主行
        if element_counts["cognitive"] > 0:
            result["cognitive"] = True
        if element_counts["B=MAP"] > 0:
            result["primary"] = "B=MAP"

        sorted_elements = sorted(element_counts, key=element_counts.get, reverse=True)
        if result["primary"] == "general":
            for e in sorted_elements:
                if element_counts[e] > 0 and e not in ["cognitive", "B=MAP"]:
                    result["primary"] = f"{e}行"
                    break

        # 判定副行
        secondaries = [e for e in sorted_elements if e not in ["cognitive", "B=MAP"] and e != result["primary"].replace("行", "")]
        if secondaries:
            result["secondary"] = f"{secondaries[0]}行"

        # 自信度
        total = sum(element_counts.values())
        result["confidence"] = min(1.0, total * 0.15)

        return result

    def scene_description(self, scene: dict) -> str:
        """将场景结果转化为中文描述"""
        parts = []
        if scene["primary"] != "general":
            parts.append(f"主场景：{scene['primary']}")
        if scene["secondary"]:
            parts.append(f"副场景：{scene['secondary']}")
        if scene["cognitive"]:
            parts.append("认知科学维度(偏差/决策)")
        parts.append(f"置信度：{scene['confidence']:.0%}")
        return " | ".join(parts)


# 单例
scene_parser = SceneParser()
