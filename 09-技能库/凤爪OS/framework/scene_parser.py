"""
凤爪OS · 场景识别引擎
应用接口层 · 接收意图 · 场景分发 · 输出握手包
version: v1.0 (2026-07-21)
"""


class FengZhaoSceneParser:
    """凤爪OS：从用户输入中识别场景类型，输出握手包"""

    # 八大应用场景
    SCENES = {
        "亲密关系": {"keywords": ["伴侣", "夫妻", "婚姻", "恋爱", "对象", "男朋友", "女朋友", "老公", "老婆"], "weight": 2},
        "亲子关系": {"keywords": ["孩子", "儿子", "女儿", "父母", "亲子", "教育", "育儿", "家长"], "weight": 2},
        "领导力": {"keywords": ["领导", "管理", "带领", "团队领导", "负责人", "主管", "经理", "总监"], "weight": 2},
        "团队建设": {"keywords": ["团队", "同事", "合作", "协作", "部门", "公司", "组织", "配合"], "weight": 2},
        "高效沟通": {"keywords": ["沟通", "说话", "表达", "交流", "说话方式", "怎么说", "沟通技巧"], "weight": 2},
        "健康养生": {"keywords": ["健康", "养生", "身体", "睡眠", "饮食", "运动", "中医", "调理"], "weight": 2},
        "日常生活": {"keywords": ["日常", "生活", "习惯", "作息", "个人", "自己", "普通"], "weight": 1},
        "人格测评": {"keywords": ["测评", "测试", "性格", "五行分析", "识人", "诊断", "我是什么"], "weight": 3},
    }

    # 五行线索检测
    WUXING_SIGNALS = {
        "木": ["愤怒", "顶撞", "不服", "创新", "规划", "领导", "主见", "固执", "傲慢"],
        "火": ["急躁", "炫耀", "热情", "表达", "社交", "演讲", "虚荣", "焦虑", "兴奋"],
        "土": ["猜疑", "依赖", "担心", "稳定", "包容", "可靠", "固执", "怨", "纠结"],
        "金": ["挑剔", "批评", "规则", "秩序", "完美", "标准", "刻薄", "冷漠", "决断"],
        "水": ["恐惧", "拖延", "多思", "智慧", "变通", "共情", "柔和", "逃避", "洞察"],
    }

    # 情感温度识别
    EMOTION_TEMPS = {
        "高愤怒": {"keywords": ["气死", "愤怒", "受不了", "忍不了"], "temp": "🔥🔥🔥"},
        "中焦虑": {"keywords": ["担心", "焦虑", "烦", "不安", "害怕"], "temp": "🔥🔥"},
        "低平静": {"keywords": ["想了解", "请问", "如何", "为什么"], "temp": "☀️"},
        "高喜悦": {"keywords": ["开心", "太好了", "成功", "突破"], "temp": "✨✨✨"},
        "低落": {"keywords": ["没意思", "难过", "失落", "失败", "累"], "temp": "🌧️"},
    }

    def parse(self, user_input: str) -> dict:
        """解析用户输入，输出握手包"""
        result = {
            "scene": "general",
            "scene_weight": 0,
            "elements": [],
            "emotion_temp": "☀️",
            "priority": "normal",
            "confidence": 0.0,
        }

        # 1. 场景识别
        max_weight = 0
        for scene_name, config in self.SCENES.items():
            for kw in config["keywords"]:
                if kw in user_input:
                    if config["weight"] > max_weight:
                        max_weight = config["weight"]
                        result["scene"] = scene_name
                        result["scene_weight"] = config["weight"]

        # 2. 五行线索
        for element, signals in self.WUXING_SIGNALS.items():
            for s in signals:
                if s in user_input:
                    result["elements"].append(element)
                    break

        # 3. 情感温度
        for temp_name, config in self.EMOTION_TEMPS.items():
            for kw in config["keywords"]:
                if kw in user_input:
                    result["emotion_temp"] = config["temp"]
                    break

        # 4. 优先级
        if "🔥🔥🔥" in result["emotion_temp"] or result["scene_weight"] >= 3:
            result["priority"] = "high"
        elif "🔥🔥" in result["emotion_temp"] or result["scene_weight"] >= 2:
            result["priority"] = "medium"

        # 5. 置信度
        confidence = 0.0
        if result["scene"] != "general":
            confidence += 0.4
        if result["elements"]:
            confidence += 0.3 * min(1.0, len(result["elements"]) / 2)
        if result["emotion_temp"] != "☀️":
            confidence += 0.2
        result["confidence"] = min(1.0, confidence)

        return result

    def format_handshake(self, handshake: dict) -> str:
        """格式化握手包"""
        return (
            f"【握手包】场景={handshake['scene']}(权重{handshake['scene_weight']}) "
            f"五行线索={handshake['elements']} "
            f"情感温度={handshake['emotion_temp']} "
            f"优先级={handshake['priority']} "
            f"置信度={handshake['confidence']:.0%}"
        )


# 单例
scene_parser = FengZhaoSceneParser()
