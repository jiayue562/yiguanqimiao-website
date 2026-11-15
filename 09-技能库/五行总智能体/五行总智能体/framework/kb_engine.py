"""五行总智能体 · kb_engine.py
知识地基引擎：五行总纲L7知识查询/跨域关联
"""
from typing import Dict, List, Optional


class ChiefKnowledgeEngine:
    """五行总智能体知识引擎"""

    KNOWLEDGE_DOMAIN = {
        "一心本体": {
            "keywords": ["一心", "觉知", "本体", "纯粹", "意识源头"],
            "core_axioms": ["一心是超越二元对立的纯粹觉知", "觉知如银幕人格如影像", "修行即从认同者变观察者"],
        },
        "三界维度": {
            "keywords": ["三界", "身语意", "精气神", "信息", "能量", "物质"],
            "core_axioms": ["三界=行为显化层+能量运作层+系统结构层", "识人需三界同观修身需三界同修"],
        },
        "五行性格": {
            "keywords": ["木行人", "火行人", "土行人", "金行人", "水行人", "阳面", "阴面"],
            "core_axioms": ["五行=五种生命能量原型", "阳面=美德阴面=习气"],
        },
        "九层发展": {
            "keywords": ["九层", "层级", "发展", "健康", "不健康", "光谱"],
            "core_axioms": ["1-3健康·阳五行显化", "4-6一般·阴阳交战", "7-9不健康·阴五行深渊"],
        },
        "生克规律": {
            "keywords": ["生克", "相生", "相克", "木克土", "金克木", "通关"],
            "core_axioms": ["相生=滋养支持", "相克=制约冲突", "化解相克=引入通关五行"],
        },
        "转化技术": {
            "keywords": ["拔阴取阳", "化克为生", "相生强化", "戒怒", "戒恨", "戒怨"],
            "core_axioms": ["拔阴取阳=戒怒恨怨恼烦", "化克为生=引入通关五行", "相生强化=按相生链条配置"],
        },
        "B=MAP整合": {
            "keywords": ["B=MAP", "福格", "动机", "能力", "提示", "行为设计"],
            "core_axioms": ["动机需对应五行核心欲望", "能力需顺应五行特质", "提示利用五行感官特征"],
        },
        "象思维": {
            "keywords": ["象思维", "观象", "取象", "运象", "物象", "意象", "原象"],
            "core_axioms": ["象思维=直观类比整体观照", "观物象→取意象→运原象"],
        },
        "外观识别": {
            "keywords": ["外观", "身形", "面色", "声音", "步伐", "五行外观"],
            "core_axioms": ["木瘦身修长面色青声直长", "火面红润声尖快行动敏捷"],
        },
    }

    HIDDEN_CONNECTIONS = [
        ("一心·纯粹觉知", "量子意识/观察者效应", "意识可能是物质世界的基础"),
        ("三界·身语意", "心理学行为/认知/情绪", "身语意对应行为-认知-情绪三领域"),
        ("三界·精气神", "中医藏象/能量医学", "精气神是中医生命观的核心框架"),
        ("五行性格", "大五人格/MBTI", "五行人格是大五人格的东方动态版本"),
        ("九层发展", "马斯洛需求层次", "1-3层=自我实现4-6层=尊重归属7-9层=安全需求受挫"),
        ("九层发展", "柯尔伯格道德发展", "九层与道德发展层级同构"),
        ("生克·木克土", "变革管理/创新阻", "木克土=创新突破对现有稳定的扰动"),
        ("生克·金克木", "创新管理/规则张力", "金克木=规则与创新的永恒张力"),
        ("生克·水克火", "情绪调节/过度冷静", "水克火=过度理性抑制热情"),
        ("拔阴取阳·戒怒", "CBT认知重构", "怒转学=认知重构：信念→新行为"),
        ("拔阴取阳·戒怨", "ACT接纳承诺", "怨转思=ACT认知解离：观察而不认同"),
        ("拔阴取阳·戒烦", "行为激活疗法", "烦转辩=行为激活：最小行动打破停滞"),
        ("化克为生·引入通关", "系统论杠杆解", "最小干预点=引入通关五行撬动模式转变"),
        ("相生强化·链条配置", "组织行为学", "木火土金水链条=Tuckman团队发展阶段"),
        ("B=MAP×五行动机", "自我决定理论(SDT)", "五行动机=自主/胜任/关系三种需求"),
        ("B=MAP×五行能力", "执行功能模型", "能力链五维与五行特质适配"),
        ("B=MAP×五行提示", "习惯叠加/锚点", "行动提示嫁接既有习惯"),
        ("象思维·观物象", "皮尔士符号学", "物象→意象→原象=icon-index-symbol"),
        ("外观识别", "体型学/外胚层/内胚层", "五行外观与谢尔顿体型学对应"),
        ("五行人格·整体架构", "系统论/全息理论", "一心三界五行九层=系统要素+维度+动力+过程"),
    ]

    def query(self, topic: str) -> Dict:
        target_domains = []
        for dname, dconfig in self.KNOWLEDGE_DOMAIN.items():
            if any(kw in topic for kw in dconfig["keywords"]):
                target_domains.append(dname)
        if not target_domains:
            target_domains = list(self.KNOWLEDGE_DOMAIN.keys())
        return {
            "topic": topic,
            "matched_domains": target_domains,
            "connections": [c for c in self.HIDDEN_CONNECTIONS if any(kw in topic for kw in [c[0][:2], c[1][:2]])],
        }

    def cross_domain_connect(self, a: str, b: str) -> Optional[Dict]:
        for conn in self.HIDDEN_CONNECTIONS:
            if (a in conn[0] or a in conn[1]) and (b in conn[0] or b in conn[1]):
                return {"concept_a": a, "concept_b": b, "connection": conn[2]}
        return None
