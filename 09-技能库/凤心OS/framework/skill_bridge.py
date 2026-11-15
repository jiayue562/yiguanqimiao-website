"""
凤心OS · 技能桥接层
凤心OS↔子智能体通信 · 结果整合 · 三端存储同步
version: v1.0 (2026-07-21)
"""


class SkillBridge:
    """凤心OS与五行分智能体之间的通信桥接"""

    # 子智能体路径索引
    AGENT_PATHS = {
        "木行人分智能体": {
            "skill": "~/.workbuddy/skills/木行人分智能体/SKILL.md",
            "expert": "mu-xing-ren",
            "framework": "~/.workbuddy/skills/木行人分智能体/framework/",
        },
        "火行人分智能体": {
            "skill": "~/.workbuddy/skills/火行人分智能体/SKILL.md",
            "expert": "huo-xing-ren",
            "framework": "~/.workbuddy/skills/火行人分智能体/framework/",
        },
        "土行人分智能体": {
            "skill": "~/.workbuddy/skills/土行人分智能体/SKILL.md",
            "expert": "tu-xing-ren",
            "framework": "~/.workbuddy/skills/土行人分智能体/framework/",
        },
        "金行人分智能体": {
            "skill": "~/.workbuddy/skills/金行人分智能体/SKILL.md",
            "expert": "jin-xing-ren",
            "framework": "~/.workbuddy/skills/金行人分智能体/framework/",
        },
        "水行人分智能体": {
            "skill": "~/.workbuddy/skills/水行人分智能体/SKILL.md",
            "expert": "shui-xing-ren",
            "framework": "~/.workbuddy/skills/水行人分智能体/framework/",
        },
        "五行总智能体": {
            "skill": "~/.workbuddy/skills/五行总智能体/SKILL.md",
            "expert": "wu-xing-zong-zhi-neng-ti",
            "framework": "~/.workbuddy/skills/五行总智能体/framework/",
        },
    }

    def __init__(self):
        self.conversation_history = []

    def route_to_agent(self, agent_name: str, context: dict) -> str:
        """
        生成调度指令，将任务路由到指定的子智能体
        返回调度说明字符串
        """
        if agent_name not in self.AGENT_PATHS:
            return f"错误：未知智能体 {agent_name}"

        agent_info = self.AGENT_PATHS[agent_name]
        instruction = (
            f"【凤心OS → {agent_name} 调度指令】\n"
            f"Expert: {agent_info['expert']}\n"
            f"Skill: {agent_info['skill']}\n"
            f"Framework: {agent_info['framework']}\n"
            f"场景上下文: {context.get('description', '通用诊断')}\n"
            f"分析模式: 慢思考（质疑→分析→验证→重构）"
        )
        return instruction

    def integrate_results(self, results: list) -> str:
        """
        整合多个子智能体的分析结果
        """
        if not results:
            return "无分析结果"

        # 检查生克协调性
        result_map = {}
        for r in results:
            if "element" in r:
                result_map[r["element"]] = r.get("summary", "")

        integration_parts = []

        # 如果有木和土的结果，检查木克土
        if "木" in result_map and "土" in result_map:
            integration_parts.append("⚠ 木克土关系检测：需检查木行的生发是否过度克制了土行的稳定")
        if "金" in result_map and "木" in result_map:
            integration_parts.append("⚠ 金克木关系检测：需检查金行的规则是否过度抑制了木行的创造")
        if "水" in result_map and "火" in result_map:
            integration_parts.append("⚠ 水克火关系检测：需检查水行的冷静是否过度压制了火行的热情")

        # 组合
        summary_parts = [r.get("summary", "") for r in results if "summary" in r]
        integration_parts.insert(0, f"整合{len(results)}个智能体分析成果")

        return "\n".join(integration_parts + [""] + summary_parts)

    def record_conversation(self, role: str, content: str):
        """记录对话历史，供后续学习"""
        self.conversation_history.append({
            "role": role,
            "content_snippet": content[:200],
        })

    def get_path_for_agent(self, agent_name: str) -> dict:
        """获取指定智能体的路径信息"""
        return self.AGENT_PATHS.get(agent_name, {})


# 单例
skill_bridge = SkillBridge()
