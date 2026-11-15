"""水行人分智能体 · agent_router.py
引擎路由：根据场景和状态路由到对应的调适引擎
"""
from typing import Dict, Optional

class WaterAgentRouter:
    """水行智能体路由"""

    def __init__(self):
        self.engine_map = {
            "拔阴取阳": ["S02", "S03", "S04", "S05", "S14", "S15"],
            "化克为生": ["S08", "S09", "S10", "S11"],
            "五行调适": ["S08", "S09", "S10", "S11", "S12"],
            "相生强化": ["S09", "S10", "S13"],
            "九层评估": ["S01", "S14", "S15"],
        }

    def route(self, scene_code: str, state: str) -> Dict:
        """根据场景和状态路由到对应引擎"""
        recommended_engines = []
        for engine, scenes in self.engine_map.items():
            if scene_code in scenes:
                recommended_engines.append(engine)

        return {
            "scene": scene_code,
            "state": state,
            "recommended_engines": recommended_engines,
            "primary_engine": recommended_engines[0] if recommended_engines else "一般诊断",
        }

    def estimate_level(self, state: str, yin_score: int, yang_score: int) -> int:
        """粗略估算九层层级"""
        diff = yin_score - yang_score
        if diff <= -3:
            return 2  # 健康区间（沉静明辨）
        elif diff <= 0:
            return 4  # 失衡起点（多疑善感）
        elif diff <= 2:
            return 5  # 控制层级（依赖退缩）
        else:
            return 6  # 过度补偿（世故放纵）

    def get_transformation_plan(self, level: int, scene: str) -> Dict:
        """根据层级和场景生成转化方案"""
        plans = {
            "烦转辩": {
                "适用": ["S02", "S15", "S03"],
                "口诀": "阴水烦转阳水辩",
                "操作": "当焦虑烦躁升起时→立刻问三个问题：①不确定性具体是什么？②已知什么还缺什么？③核心矛盾在哪？→将烦能量导向深度辨析",
                "心法": "烦躁是迷雾，辨析是灯塔——将不安转为清晰洞察",
            },
            "痴转智": {
                "适用": ["S04", "S05", "S14"],
                "口诀": "阴水痴转阳水智",
                "操作": "当依赖逃避念头出现时→自问'我是在依附他人寻求安全，还是相信自己本具智慧？'→锚定'我是智慧源泉，不是安全乞丐'",
                "心法": "依赖是虚幻的避风港，智慧是真实的灯塔",
            },
            "金生水": {
                "适用": ["S09", "S08"],
                "口诀": "框架生智慧",
                "操作": "当迷茫不安时→建立清晰的工作流程SOP、知识管理体系、项目分析框架→用结构滋养因不确定而焦渴的智慧",
                "心法": "清晰的规则是智慧流动的河道",
            },
            "水生木": {
                "适用": ["S10", "S15"],
                "口诀": "智慧生行动",
                "操作": "将辨析出的思路转化为最小可执行步骤→制定具体行动计划→智慧(水)催生行动(木)→行动带来进展感",
                "心法": "最深沉的智慧也必须在行动中绽放",
            },
        }

        matched = []
        for name, plan in plans.items():
            if scene in plan["适用"]:
                matched.append(plan)
        return {"level": level, "plans": matched}
