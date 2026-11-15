"""
凤爪OS · 桥接层
凤爪OS ↔ 凤心OS · 三层架构通信
version: v1.0 (2026-07-21)
"""


class FengZhaoBridge:
    """凤爪OS桥接：与凤心OS、凤脑OS的通信"""

    LAYER_MAP = {
        "凤爪OS": "应用接口层（顶层觉知接待台）·接收意图·场景分发",
        "凤心OS": "智能发动机层（快慢思考·1+5模式）·深度诊断·转化方案",
        "凤脑OS": "知识地基层（17篇·130条跨域联系）·理论支撑·知识查询",
    }

    def build_handshake(self, user_input: str) -> dict:
        """构建握手包"""
        from .scene_parser import scene_parser
        handshake = scene_parser.parse(user_input)
        handshake["layer_call"] = "凤心OS"
        return handshake

    def call_fengxin(self, handshake: dict) -> str:
        """调用凤心OS"""
        from .agent_router import router
        route = router.route_to_fengxin(handshake)
        return f"【凤爪OS→凤心OS】{route['instruction']}（紧急度:{route['urgency']}）"

    def get_full_chain(self, user_input: str) -> str:
        """完整调用链"""
        handshake = self.build_handshake(user_input)
        return (
            f"【三层架构调用链】\n"
            f"凤爪OS(接收)→{self.call_fengxin(handshake)}\n"
            f"凤心OS(分析)→调用对应分智能体\n"
            f"凤脑OS(知识)→理论支撑\n"
            f"握手包: {handshake}"
        )


bridge = FengZhaoBridge()
