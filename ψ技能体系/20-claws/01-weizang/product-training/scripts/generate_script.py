"""
Product Training Skills · 话术预处理脚本 v1.0.0
© 2026 味藏商学院 · 所有权利保留

用途：AI预处理·基于菜品信息自动生成3+1话术初稿
触发：龙心OS M2话术生成引擎调用
注意：此为AI辅助草稿生成，最终话术必须经马循德+后厨大师傅确认
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional


# === 3+1话术结构定义 ===
THREE_PLUS_ONE = {
    "selling_point_1": {"max_sentences": 2, "max_seconds": 5, "focus": "品质差异"},
    "selling_point_2": {"max_sentences": 2, "max_seconds": 5, "focus": "口感体验"},
    "selling_point_3": {"max_sentences": 2, "max_seconds": 5, "focus": "独特价值"},
    "story": {"max_seconds": 30, "focus": "情感连接"},
}

# === 四种场景变体 ===
SCENE_VARIANTS = {
    "商务宴请": {"tone": "专业尊贵", "keywords": ["面子", "品质", "稀有", "体面", "规格"]},
    "情侣约会": {"tone": "浪漫精致", "keywords": ["浪漫", "仪式", "精致", "体验", "特别"]},
    "家庭聚餐": {"tone": "温暖丰盛", "keywords": ["实惠", "丰盛", "健康", "安心", "分享"]},
}

# === 四点价值提取法 ===
VALUE_DIMENSIONS = {
    "产地价值": "食材从哪里来，为什么好（地域/季节/等级）",
    "工艺价值": "怎么做的，区别普通做法的独特之处（刀工/火候/时间）",
    "口感价值": "吃起来什么感受，为什么独特（味觉/触觉/层次）",
    "文化价值": "背后有什么故事/传统/仪式感",
}


class ScriptGenerator:
    """3+1话术自动生成器"""

    def __init__(self, dish_info: Dict):
        self.dish = dish_info
        self.name = dish_info.get("name", "未命名菜品")
        self.category = dish_info.get("category", "")
        self.ingredients = dish_info.get("ingredients", [])
        self.process = dish_info.get("process", "")
        self.origin = dish_info.get("origin", "")
        self.culture = dish_info.get("culture", "")
        self.taste = dish_info.get("taste", {})
        self.price_range = dish_info.get("price_range", "")

    def generate_selling_points(self) -> List[Dict]:
        """生成3个卖点"""
        points = []

        # SP1: 品质差异（产地+食材）
        point1_parts = []
        if self.origin:
            point1_parts.append(f"来自{self.origin}")
        if self.ingredients:
            key_ingredient = self.ingredients[0] if isinstance(self.ingredients[0], str) else self.ingredients[0].get("name", "")
            quality_desc = self.ingredients[0].get("quality", "") if isinstance(self.ingredients[0], dict) else ""
            if quality_desc:
                point1_parts.append(f"{key_ingredient}·{quality_desc}")
            else:
                point1_parts.append(f"精选{key_ingredient}")
        points.append({
            "id": "SP1_品质差异",
            "draft": "·".join(point1_parts) if point1_parts else f"精选{self.name}主食材",
            "type": "quality",
        })

        # SP2: 口感体验
        taste_parts = []
        if self.taste:
            taste_parts.append(
                self.taste.get("primary", "")
                or self.taste.get("texture", "")
                or self.taste.get("mouthfeel", "")
            )
        if self.process:
            taste_parts.append(f"采用{self.process}工艺")
        points.append({
            "id": "SP2_口感体验",
            "draft": "·".join(taste_parts) if taste_parts else f"独特口感·匠心工艺",
            "type": "taste",
        })

        # SP3: 独特价值
        value_parts = []
        if self.culture:
            value_parts.append(self.culture)
        if self.price_range:
            value_parts.append(f"{self.price_range}价位·物超所值")
        else:
            value_parts.append("味藏匠心出品")
        points.append({
            "id": "SP3_独特价值",
            "draft": "·".join(value_parts),
            "type": "value",
        })

        return points

    def generate_story(self) -> Dict:
        """生成匠心故事框架"""
        elements = {
            "who": f"味藏后厨{self.category}团队",
            "what": self.process or f"每日手工制作{self.name}",
            "how": "从选材到出品·每一道工序都倾注专注",
            "why": f"让{self.name}不止是一道菜·更是一份用心",
        }

        story_draft = (
            f"[{elements['who']}] → [{elements['what']}] → "
            f"[{elements['how']}] → [{elements['why']}]"
        )
        return {"draft": story_draft, "elements": elements, "target_length": "30秒"}

    def generate_scene_variants(self, selling_points: List[Dict], story: Dict) -> Dict:
        """生成三种场景变体"""
        variants = {}
        for scene, config in SCENE_VARIANTS.items():
            adapted_points = []
            for sp in selling_points:
                adapted = sp["draft"]
                for kw in config["keywords"]:
                    if kw in ["稀有", "品质", "体面"] and scene == "商务宴请":
                        adapted = adapted.replace("品质", "顶级品质").replace("精选", "臻选")
                    elif kw in ["浪漫", "精致", "特别"] and scene == "情侣约会":
                        adapted = adapted.replace("品质", "精致").replace("工艺", "匠心")
                    elif kw in ["实惠", "丰盛", "健康"] and scene == "家庭聚餐":
                        adapted = adapted.replace("品质", "安心品质").replace("精选", "严选")
                adapted_points.append(adapted)

            variants[scene] = {
                "tone": config["tone"],
                "selling_points": adapted_points,
                "story_focus": {
                    "商务宴请": "体面感·稀有度·规格",
                    "情侣约会": "浪漫感·仪式·精致",
                    "家庭聚餐": "丰盛感·安心·健康",
                }.get(scene, ""),
            }
        return variants

    def generate_full_card(self) -> Dict:
        """生成完整话术卡"""
        selling_points = self.generate_selling_points()
        story = self.generate_story()
        scene_variants = self.generate_scene_variants(selling_points, story)

        card = {
            "skill": "product-training",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "status": "DRAFT·待马循德+后厨大师傅确认",
            "dish": {
                "name": self.name,
                "category": self.category,
                "price_range": self.price_range,
            },
            "three_plus_one": {
                "selling_point_1": selling_points[0],
                "selling_point_2": selling_points[1],
                "selling_point_3": selling_points[2],
                "story": story,
            },
            "scene_variants": scene_variants,
            "quality_gates": {
                "G1_后厨确认": "⏳ 待确认",
                "G2_前厅试讲": "⏳ 待试讲",
                "G3_客户反馈": "⏳ 待收集",
            },
            "warning": "⚠️ 此为由AI生成的草稿，必须经三道验证(G1→G2→G3)后方可上线使用",
        }
        return card

    def to_json(self, indent: int = 2, ensure_ascii: bool = False) -> str:
        """输出JSON格式"""
        return json.dumps(self.generate_full_card(), indent=indent, ensure_ascii=ensure_ascii)

    def to_markdown(self) -> str:
        """输出Markdown格式话术卡"""
        card = self.generate_full_card()
        tpo = card["three_plus_one"]
        md = f"""# {card['dish']['name']} · 3+1话术卡

> **状态**：{card['status']} | **生成时间**：{card['generated_at']}

## 🥇 卖点一：品质差异
{tpo['selling_point_1']['draft']}

## 🥈 卖点二：口感体验
{tpo['selling_point_2']['draft']}

## 🥉 卖点三：独特价值
{tpo['selling_point_3']['draft']}

## 📖 匠心故事（30秒）
{tpo['story']['draft']}

## 🔄 三种场景变体
"""
        for scene, variant in card["scene_variants"].items():
            md += f"\n### {scene}版（{variant['tone']}）\n"
            for i, sp in enumerate(variant["selling_points"], 1):
                md += f"- 卖点{i}：{sp}\n"

        md += "\n## ✅ 三道验证\n"
        for gate, status in card["quality_gates"].items():
            md += f"- **{gate}**：{status}\n"

        md += f"\n> {card['warning']}\n"
        return md


# === CLI入口 ===
if __name__ == "__main__":
    # 示例：命令行调用
    if len(sys.argv) > 1:
        dish_name = sys.argv[1]
        origin = sys.argv[2] if len(sys.argv) > 2 else ""
        category = sys.argv[3] if len(sys.argv) > 3 else ""

        sample_dish = {
            "name": dish_name,
            "category": category,
            "origin": origin,
            "ingredients": [{"name": "主食材", "quality": "A级"}],
            "process": "传统工艺",
            "culture": "味藏匠心传承",
            "taste": {"primary": "鲜美", "texture": "细腻"},
            "price_range": "中高端",
        }
    else:
        # 默认示例：蓝鳍金枪鱼大腹
        sample_dish = {
            "name": "蓝鳍金枪鱼大腹",
            "category": "刺身",
            "origin": "日本长崎·冰鲜空运",
            "ingredients": [{"name": "蓝鳍金枪鱼", "quality": "A级·冰鲜原条·5天赏味期"}],
            "process": "江户前传统切法·42°斜切·入口即化",
            "culture": "金枪鱼中的王者·日本料理顶级食材·味藏开鱼仪式文化",
            "taste": {"primary": "入口即化", "texture": "油脂丰腴·细腻柔滑"},
            "price_range": "高端",
        }

    generator = ScriptGenerator(sample_dish)
    print(generator.to_markdown())

    # 同时输出JSON到文件
    import os
    output_dir = os.path.join(os.path.dirname(__file__), "..", "临时输出文件")
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f"话术草稿_{generator.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(generator.to_json())
    print(f"\n✅ JSON已保存：{json_path}")
