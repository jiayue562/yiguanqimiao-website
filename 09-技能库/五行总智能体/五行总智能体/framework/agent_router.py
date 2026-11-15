"""五行总智能体 · agent_router.py
引擎路由：根据场景和解析结果路由到对应分智能体
"""
from typing import Dict, List

class ChiefAgentRouter:
    """五行总智能体路由"""

    AGENT_MAP = {
        "木": {"skill_path": "~/.workbuddy/skills/木行人分智能体/", "name": "木行人分智能体"},
        "火": {"skill_path": "~/.workbuddy/skills/火行人分智能体/", "name": "火行人分智能体"},
        "土": {"skill_path": "~/.workbuddy/skills/土行人分智能体/", "name": "土行人分智能体"},
        "金": {"skill_path": "~/.workbuddy/skills/金行人分智能体/", "name": "金行人分智能体"},
        "水": {"skill_path": "~/.workbuddy/skills/水行人分智能体/", "name": "水行人分智能体"},
    }

    def route(self, needed_agents: List[str], primary_scene: str) -> Dict:
        """根据场景路由到分智能体"""
        agents_to_activate = []
        for agent in needed_agents:
            if agent in self.AGENT_MAP:
                agents_to_activate.append(self.AGENT_MAP[agent])

        if len(agents_to_activate) == 0:
            return {"mode": "general_analysis", "agents": [], "instruction": "进行一般五行分析"}
        elif len(agents_to_activate) == 1:
            return {"mode": "single_element", "agents": agents_to_activate, "instruction": f"调度{agents_to_activate[0]['name']}进行深度分析"}
        else:
            return {"mode": "multi_element", "agents": agents_to_activate, "instruction": f"调度{len(agents_to_activate)}个分智能体进行协同分析"}
