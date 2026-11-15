"""
凤心OS · 智能路由引擎
1+5模式 · 快思考总调度 → 慢思考子智能体路由
version: v1.0 (2026-07-21)
"""


class AgentRouter:
    """凤心OS路由核心：根据场景自动调度1-5个分智能体"""

    # 6个子智能体
    AGENTS = {
        "总智能体": "五行总智能体",
        "木": "木行人分智能体",
        "火": "火行人分智能体",
        "土": "土行人分智能体",
        "金": "金行人分智能体",
        "水": "水行人分智能体",
    }

    # 快思考层（总智能体）vs慢思考层（分智能体）
    MODE_FAST = "快思考（毫秒级·象思维+五行图谱·场景归类+路由）"
    MODE_SLOW = "慢思考（秒~分钟级·逻辑思维+一心三界五行九层·深度诊断）"

    # 路由模式
    ROUTE_SINGLE = "单行路由"
    ROUTE_DUAL = "双行路由"
    ROUTE_SHENG_KE = "生克路由"
    ROUTE_GLOBAL = "全五行路由"
    ROUTE_BMAP = "B=MAP行为设计路由"

    def route(self, scene: dict) -> dict:
        """根据场景检测结果决定路由策略"""
        primary = scene.get("primary", "general")
        secondary = scene.get("secondary", "")
        cognitive = scene.get("cognitive", False)

        result = {
            "mode": self.MODE_FAST,
            "route_type": self.ROUTE_SINGLE,
            "agents": [],
            "description": "",
        }

        # 认知科学场景 → 路由到快慢思考协同
        if cognitive:
            result["mode"] = f"{self.MODE_FAST} + {self.MODE_SLOW}"
            result["description"] = "认知偏差检测→激活慢思考纠偏模式"
            result["route_type"] = self.ROUTE_GLOBAL

        # B=MAP行为设计
        if primary == "B=MAP":
            result["route_type"] = self.ROUTE_BMAP
            result["agents"] = [self.AGENTS["总智能体"]]
            result["description"] = "B=MAP行为设计模式·动机+能力+提示三要素分析"
            result["mode"] = self.MODE_FAST
            return result

        # 单行模式
        if primary != "general" and not secondary:
            element = primary.replace("行", "")
            if element in self.AGENTS:
                result["agents"] = [self.AGENTS["总智能体"], self.AGENTS[element]]
                result["description"] = f"单行路由：{primary}→调度{self.AGENTS[element]}深度分析"
                result["mode"] = f"{self.MODE_FAST} → {self.MODE_SLOW}"
                return result

        # 双行模式
        if primary != "general" and secondary:
            p = primary.replace("行", "")
            s = secondary.replace("行", "")
            if p in self.AGENTS and s in self.AGENTS:
                result["agents"] = [self.AGENTS["总智能体"], self.AGENTS[p], self.AGENTS[s]]
                result["route_type"] = self.ROUTE_DUAL
                result["description"] = f"双行路由：{primary}+{secondary}→并行分析"
                result["mode"] = f"{self.MODE_FAST} → {self.MODE_SLOW}×2"
                return result

        # 生克关系路由
        SHENG_KE_PAIRS = {
            ("木", "土"): ("金", "五行总智能体"),
            ("土", "水"): ("金", "五行总智能体"),
            ("水", "火"): ("木", "五行总智能体"),
            ("火", "金"): ("土", "五行总智能体"),
            ("金", "木"): ("水", "五行总智能体"),
            ("木", "火"): ("火", "五行总智能体"),
            ("火", "土"): ("土", "五行总智能体"),
            ("土", "金"): ("金", "五行总智能体"),
            ("金", "水"): ("水", "五行总智能体"),
            ("水", "木"): ("木", "五行总智能体"),
        }
        p, s = primary.replace("行", ""), secondary.replace("行", "")
        pair_key = (p, s)
        if pair_key in SHENG_KE_PAIRS:
            mediator, _ = SHENG_KE_PAIRS[pair_key]
            result["agents"] = [self.AGENTS[p], self.AGENTS[s]]
            if mediator in self.AGENTS:
                result["agents"].append(self.AGENTS[mediator])
            result["route_type"] = self.ROUTE_SHENG_KE
            result["description"] = f"生克路由：{primary}克{secondary}→引入中介调和"
            return result

        # 默认：全五行诊断
        result["agents"] = [self.AGENTS["总智能体"]] + [self.AGENTS[k] for k in ["木", "火", "土", "金", "水"]]
        result["route_type"] = self.ROUTE_GLOBAL
        result["description"] = "全五行路由→全面诊断"
        return result

    def format_route(self, route: dict) -> str:
        """格式化路由结果为可读字符串"""
        agents = "\n  → ".join(route["agents"])
        return (
            f"【路由策略】{route['route_type']}\n"
            f"【认知模式】{route['mode']}\n"
            f"【调度智能体】\n  → {agents}\n"
            f"【说明】{route['description']}"
        )


# 单例
agent_router = AgentRouter()
