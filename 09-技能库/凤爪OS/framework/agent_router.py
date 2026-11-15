"""
凤爪OS · 路由引擎
应用接口层 → 凤心OS发动机路由
version: v1.0 (2026-07-21)
"""


class FengZhaoRouter:
    """凤爪OS路由：场景识别后路由到凤心OS"""

    def route_to_fengxin(self, handshake: dict) -> dict:
        """根据握手包路由到凤心OS"""
        scene = handshake.get("scene", "general")
        elements = handshake.get("elements", [])
        priority = handshake.get("priority", "normal")

        route = {"to": "凤心OS", "instruction": "", "urgency": priority}

        if scene == "人格测评":
            route["instruction"] = "人格测评场景→凤心OS调用五行总智能体+对应分智能体测评分析"
        elif elements:
            route["instruction"] = f"{scene}场景+{elements}线索→凤心OS五维感知矩阵评分→路由对应分智能体"
        else:
            route["instruction"] = f"{scene}场景→凤心OS通用分析"

        return route

    def route_to_zhuangzi(self, handshake: dict) -> dict:
        """检测到庄子三无相关输入时，直接调用凤爪OS庄子修身模块"""
        route = {"to": "凤爪OS·庄子修身", "instruction": "", "urgency": "normal"}
        route["instruction"] = "庄子三无修身→三无诊断(无己/无功/无名)+五行转化+B=MAP微习惯"
        return route

    def get_scene_prompt(self, scene: str) -> str:
        """返回场景提示词模板"""
        prompts = {
            "亲密关系": "从五行生克角度分析伴侣/夫妻关系，给出化克为生建议",
            "亲子关系": "从五行人格角度分析亲子互动模式，给出因材施教建议",
            "领导力": "从五行能量角度分析领导风格，给出补益提升建议",
            "团队建设": "从五行团队配置角度分析，给出团队优化建议",
            "高效沟通": "从五行语言模式角度分析沟通问题，给出针对性建议",
            "健康养生": "从五行养生角度给出个性化建议",
            "日常生活": "从五行日常应用角度分析",
            "人格测评": "调用五行人格测评体系进行分析",
        }
        return prompts.get(scene, "通用分析")


router = FengZhaoRouter()
