"""五行总智能体 · scene_parser.py
场景理解引擎：识别用户输入中的五行相关场景
"""
from typing import Dict, List

class ChiefSceneParser:
    """五行总场景解析器"""

    SCENES = {
        "S00": {"keywords": ["总智能体", "1+5", "龙心OS"], "scene": "系统调度"},
        "S01": {"keywords": ["五行分析", "五行判断", "五行人格", "五行识人"], "scene": "五行快速判断"},
        "S02": {"keywords": ["木行人", "木行", "木性", "生发", "仁德", "创新"], "scene": "木行单行分析"},
        "S03": {"keywords": ["火行人", "火行", "火性", "炎上", "热情", "礼德"], "scene": "火行单行分析"},
        "S04": {"keywords": ["土行人", "土行", "土性", "运化", "信实", "承载"], "scene": "土行单行分析"},
        "S05": {"keywords": ["金行人", "金行", "金性", "收敛", "义理", "决断"], "scene": "金行单行分析"},
        "S06": {"keywords": ["水行人", "水行", "水性", "润下", "智慧", "涵藏"], "scene": "水行单行分析"},
        "S07": {"keywords": ["五行关系", "五行配合", "相生", "相克", "生克"], "scene": "五行关系分析"},
        "S08": {"keywords": ["生克", "相生", "相克", "木克土", "水克火", "金克木"], "scene": "生克关系检测"},
        "S09": {"keywords": ["拔阴取阳", "认不是", "找好处", "转化", "化性"], "scene": "拔阴取阳转化"},
        "S10": {"keywords": ["相生强化", "滋养", "能量补给", "五行调适"], "scene": "相生强化方案"},
        "S11": {"keywords": ["外观", "识人", "脸型", "身形", "面相", "五行外观"], "scene": "外观五步识别"},
        "S12": {"keywords": ["九层", "层级", "发展", "健康", "失衡", "不健康"], "scene": "九层层级定位"},
        "S13": {"keywords": ["团队", "配置", "组织", "管理", "搭配", "人才"], "scene": "团队五行配置"},
        "S14": {"keywords": ["亲密关系", "夫妻", "伴侣", "恋爱", "婚姻", "五行夫妻"], "scene": "亲密关系分析"},
        "S15": {"keywords": ["B=MAP", "福格", "行为设计", "微习惯", "习惯养成"], "scene": "B=MAP行为设计"},
    }

    def parse(self, user_input: str) -> Dict:
        """解析用户输入，返回场景识别结果"""
        matched_scenes = []
        for code, config in self.SCENES.items():
            if any(kw in user_input for kw in config["keywords"]):
                matched_scenes.append({"code": code, "scene": config["scene"]})
        
        # 判断需要调度哪些分智能体
        element_map = {
            "木": "S02", "火": "S03", "土": "S04", "金": "S05", "水": "S06"
        }
        needed_agents = []
        for elem, code in element_map.items():
            if any(code == s["code"] for s in matched_scenes):
                needed_agents.append(elem)

        return {
            "matched_scenes": matched_scenes[:3],
            "primary_scene": matched_scenes[0] if matched_scenes else None,
            "needed_agents": needed_agents,
            "primary_element": needed_agents[0] if needed_agents else None,
        }
