"""五行总智能体 · skill_bridge.py
Skill桥接：与分智能体和外部系统的通信接口
"""
from typing import Dict, List

class ChiefSkillBridge:
    """五行总智能体桥接"""

    def dispatch_to_sub_agent(self, agent_name: str, data: Dict) -> Dict:
        """调度到分智能体"""
        return {
            "target": agent_name,
            "action": "analyze",
            "payload": data,
            "return_format": "diagnosis_report",
        }

    def collect_results(self, results: List[Dict]) -> Dict:
        """收集分智能体结果并整合"""
        return {
            "type": "integrated_report",
            "elements_analyzed": len(results),
            "reports": results,
            "summary": self._generate_summary(results),
        }

    def _generate_summary(self, results: List[Dict]) -> str:
        return f"共分析{len(results)}个五行维度。如需深度转化建议，请指定具体五行。"
