#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UTF-8 BOM

"""
思维模型.skills - 模型路由器
根据场景和步骤推荐 1-N 个思维模型

版本：v1.0
创建：2026-04-17
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ModelFrequency(Enum):
    """模型频率分类"""
    HIGH = "high"      # 高频（9 个，本能反应）
    MEDIUM = "medium"  # 中频（20 个，场景激活）
    LOW = "low"        # 低频（71 个，按需加载）


@dataclass
class ThinkingModel:
    """思维模型定义"""
    name: str
    frequency: ModelFrequency
    category: str  # 分析/战略/决策/创新/沟通/系统/产品/管理
    description: str
    core_idea: str  # 核心思想
    use_scenarios: List[str]  # 使用场景
    steps: List[str]  # 使用步骤
    output: str  # 预期输出
    triggers: List[str]  # 触发关键词


class ModelRouter:
    """思维模型路由器 - 分层设计 + 动态路由"""
    
    def __init__(self):
        """初始化路由器 - 加载 100 个思维模型"""
        # 高频模型（9 个，本能反应）
        self.high_frequency_models = [
            ThinkingModel(
                name="第一性原理",
                frequency=ModelFrequency.HIGH,
                category="分析",
                description="从基本原理出发，剥离表象，直达本质",
                core_idea="回归事物最基本的条件，将其拆分成各要素进行解构分析，从而找到实现目标最优路径的方法",
                use_scenarios=["理解概念本质", "创新突破", "复杂问题分析", "找到根本原因"],
                steps=[
                    "1. 识别并定义当前的假设或信念",
                    "2. 将问题分解为最基本的事实和要素",
                    "3. 创建新的解决方案和路径",
                    "4. 验证新的假设和结论"
                ],
                output="本质分析文档 + 创新方案",
                triggers=["本质", "根本", "原理", "为什么", "底层逻辑", "第一性"]
            ),
            ThinkingModel(
                name="MECE 原则",
                frequency=ModelFrequency.HIGH,
                category="分析",
                description="相互独立，完全穷尽",
                core_idea="将整体分解为互不重叠、完全穷尽的部分",
                use_scenarios=["问题拆解", "分类整理", "结构化思考", "确保完整性"],
                steps=[
                    "1. 明确整体范围和边界",
                    "2. 确定分类维度",
                    "3. 分解为互不重叠的部分",
                    "4. 验证是否完全穷尽"
                ],
                output="结构化拆解图 + 分类清单",
                triggers=["分类", "分解", "结构化", "完整", "不重叠", "MECE"]
            ),
            ThinkingModel(
                name="SWOT 分析",
                frequency=ModelFrequency.HIGH,
                category="战略",
                description="优势/劣势/机会/威胁分析",
                core_idea="从内部优势劣势和外部机会威胁四个维度全面分析",
                use_scenarios=["战略规划", "竞争分析", "项目评估", "个人发展"],
                steps=[
                    "1. 分析内部优势（Strengths）",
                    "2. 分析内部劣势（Weaknesses）",
                    "3. 分析外部机会（Opportunities）",
                    "4. 分析外部威胁（Threats）",
                    "5. 制定 SO、WO、ST、WT 策略"
                ],
                output="SWOT 分析矩阵 + 策略建议",
                triggers=["优势", "劣势", "机会", "威胁", "内外部", "SWOT"]
            ),
            ThinkingModel(
                name="五色光思维",
                frequency=ModelFrequency.HIGH,
                category="决策",
                description="白光/红光/黄光/绿光/蓝光多维度思考",
                core_idea="从五个维度全面观照问题，实现同频思考",
                use_scenarios=["团队决策", "会议引导", "多角度分析", "全面思考"],
                steps=[
                    "1. 白光：客观事实是什么？",
                    "2. 红光：直觉和情感反应？",
                    "3. 黄光：积极面和价值？",
                    "4. 绿光：创意和可能性？",
                    "5. 蓝光：整体观照和下一步？"
                ],
                output="多维度分析报告 + 综合建议",
                triggers=["多角度", "全面", "团队", "决策", "会议", "五色光"]
            ),
            ThinkingModel(
                name="象思维",
                frequency=ModelFrequency.HIGH,
                category="创新",
                description="观物取象，0→1 原创突破",
                core_idea="通过观察现象提取模式，实现原创性突破",
                use_scenarios=["创意生成", "原创设计", "突破常规", "从 0 到 1"],
                steps=[
                    "1. 观象：观察现象，捕捉信息",
                    "2. 取象：提取模式，形成意象",
                    "3. 运象：运用意象，推理创造",
                    "4. 制器：转化为具体方案"
                ],
                output="原创创意 + 设计方案",
                triggers=["创意", "灵感", "原创", "0 到 1", "突破", "象思维"]
            ),
            ThinkingModel(
                name="金字塔原理",
                frequency=ModelFrequency.HIGH,
                category="沟通",
                description="结论先行，以上统下，归类分组，逻辑递进",
                core_idea="结构化表达和思考的原则",
                use_scenarios=["汇报演示", "写作表达", "逻辑思考", "清晰沟通"],
                steps=[
                    "1. 结论先行：先说核心观点",
                    "2. 以上统下：上层统领下层",
                    "3. 归类分组：MECE 原则分组",
                    "4. 逻辑递进：按逻辑顺序展开"
                ],
                output="结构化文档 + 清晰表达",
                triggers=["表达", "汇报", "结构", "逻辑", "清晰", "金字塔"]
            ),
            ThinkingModel(
                name="5Why 分析法",
                frequency=ModelFrequency.HIGH,
                category="分析",
                description="连续问 5 个为什么，找到根本原因",
                core_idea="通过连续追问找到问题的根本原因",
                use_scenarios=["问题分析", "找到根因", "避免复发", "质量改进"],
                steps=[
                    "1. 明确问题",
                    "2. 问为什么发生",
                    "3. 对答案继续问为什么",
                    "4. 重复 5 次或找到根因",
                    "5. 制定对策"
                ],
                output="根因分析 + 对策建议",
                triggers=["原因", "为什么", "根源", "问题", "5Why"]
            ),
            ThinkingModel(
                name="艾森豪威尔矩阵",
                frequency=ModelFrequency.HIGH,
                category="决策",
                description="重要/紧急四象限",
                core_idea="按重要和紧急两个维度优先排序",
                use_scenarios=["时间管理", "优先级排序", "任务分配", "资源分配"],
                steps=[
                    "1. 列出所有任务",
                    "2. 评估重要性和紧急性",
                    "3. 放入四个象限",
                    "4. 按优先级处理"
                ],
                output="优先级清单 + 行动计划",
                triggers=["优先级", "重要", "紧急", "时间管理", "四象限"]
            ),
            ThinkingModel(
                name="知行合一",
                frequency=ModelFrequency.HIGH,
                category="决策",
                description="从知道到做到，概念落地",
                core_idea="认识和实践的统一，将知识转化为行动",
                use_scenarios=["落地实施", "执行计划", "概念转化", "行动导向"],
                steps=[
                    "1. 表示空间：标签化拆解概念",
                    "2. 压缩提炼：找到核心优势",
                    "3. 泛化落地：场景化实施",
                    "4. 验证优化：持续迭代"
                ],
                output="行动计划 + 执行结果",
                triggers=["落地", "实施", "执行", "怎么做", "行动", "知行合一"]
            )
        ]
        
        # 中频模型（20 个，场景激活）- 示例 10 个
        self.medium_frequency_models = [
            ThinkingModel(
                name="波特五力",
                frequency=ModelFrequency.MEDIUM,
                category="战略",
                description="行业竞争分析五力模型",
                core_idea="从五种竞争力分析行业吸引力",
                use_scenarios=["行业分析", "竞争战略", "市场进入", "投资评估"],
                steps=[
                    "1. 分析现有竞争者",
                    "2. 分析潜在进入者",
                    "3. 分析替代品",
                    "4. 分析供应商议价能力",
                    "5. 分析客户议价能力"
                ],
                output="行业分析报告 + 竞争策略",
                triggers=["行业", "竞争", "供应商", "客户", "替代品", "波特五力"]
            ),
            ThinkingModel(
                name="BCG 矩阵",
                frequency=ModelFrequency.MEDIUM,
                category="战略",
                description="明星/现金牛/问题/瘦狗",
                core_idea="按市场增长率和市场份额分类业务",
                use_scenarios=["产品组合", "资源配置", "业务规划", "投资决策"],
                steps=[
                    "1. 评估市场增长率",
                    "2. 评估市场份额",
                    "3. 放入四个象限",
                    "4. 制定相应策略"
                ],
                output="产品组合分析 + 资源配置建议",
                triggers=["产品组合", "市场份额", "增长", "投资", "BCG"]
            ),
            ThinkingModel(
                name="PDCA 循环",
                frequency=ModelFrequency.MEDIUM,
                category="系统",
                description="计划 - 执行 - 检查 - 行动",
                core_idea="持续改进的循环方法",
                use_scenarios=["质量改进", "流程优化", "持续改进", "项目管理"],
                steps=[
                    "1. Plan：制定计划",
                    "2. Do：执行计划",
                    "3. Check：检查结果",
                    "4. Act：处理改进"
                ],
                output="改进计划 + 执行记录",
                triggers=["改进", "循环", "持续", "优化", "PDCA"]
            ),
            ThinkingModel(
                name="SCQA 框架",
                frequency=ModelFrequency.MEDIUM,
                category="沟通",
                description="情境 - 冲突 - 疑问 - 回答",
                core_idea="结构化叙述和表达的框架",
                use_scenarios=["演讲开场", "报告写作", "故事叙述", "问题引入"],
                steps=[
                    "1. Situation：设定情境",
                    "2. Complication：制造冲突",
                    "3. Question：提出疑问",
                    "4. Answer：给出回答"
                ],
                output="结构化叙述 + 清晰表达",
                triggers=["故事", "叙述", "开场", "引入", "SCQA"]
            ),
            ThinkingModel(
                name="决策矩阵",
                frequency=ModelFrequency.MEDIUM,
                category="决策",
                description="多标准决策分析",
                core_idea="按多个标准评估选项并打分",
                use_scenarios=["多方案选择", "供应商评估", "投资决策", "优先级排序"],
                steps=[
                    "1. 列出所有选项",
                    "2. 确定评估标准",
                    "3. 给每个标准赋权重",
                    "4. 打分并计算总分",
                    "5. 选择最优方案"
                ],
                output="决策分析表 + 最优方案",
                triggers=["选择", "评估", "标准", "权重", "决策矩阵"]
            ),
            ThinkingModel(
                name="商业模式画布",
                frequency=ModelFrequency.MEDIUM,
                category="战略",
                description="9 个构造块描述商业模式",
                core_idea="用 9 个要素全面描述商业模式",
                use_scenarios=["商业模式设计", "创业规划", "业务创新", "战略分析"],
                steps=[
                    "1. 客户细分",
                    "2. 价值主张",
                    "3. 渠道通路",
                    "4. 客户关系",
                    "5. 收入来源",
                    "6. 核心资源",
                    "7. 关键业务",
                    "8. 重要合作",
                    "9. 成本结构"
                ],
                output="商业模式画布图",
                triggers=["商业模式", "画布", "价值主张", "创业"]
            ),
            ThinkingModel(
                name="用户画像",
                frequency=ModelFrequency.MEDIUM,
                category="产品",
                description="目标用户的虚拟代表",
                core_idea="创建典型用户代表来理解用户需求",
                use_scenarios=["产品设计", "市场定位", "用户研究", "需求分析"],
                steps=[
                    "1. 收集用户数据",
                    "2. 识别用户模式",
                    "3. 创建用户画像",
                    "4. 验证和完善"
                ],
                output="用户画像文档 + 需求清单",
                triggers=["用户", "需求", "场景", "画像", "Persona"]
            ),
            ThinkingModel(
                name="MVP",
                frequency=ModelFrequency.MEDIUM,
                category="产品",
                description="最小可行产品",
                core_idea="用最小成本快速验证核心假设",
                use_scenarios=["产品验证", "创业测试", "快速迭代", "风险控制"],
                steps=[
                    "1. 定义核心假设",
                    "2. 设计 MVP",
                    "3. 快速开发",
                    "4. 测试验证",
                    "5. 学习迭代"
                ],
                output="MVP 方案 + 验证结果",
                triggers=["最小可行", "快速验证", "MVP", "迭代"]
            ),
            ThinkingModel(
                name="OKR",
                frequency=ModelFrequency.MEDIUM,
                category="管理",
                description="目标与关键结果",
                core_idea="设定有挑战性的目标并量化关键结果",
                use_scenarios=["目标管理", "团队对齐", "绩效评估", "战略规划"],
                steps=[
                    "1. 设定目标（Objective）",
                    "2. 定义关键结果（Key Results）",
                    "3. 对齐和沟通",
                    "4. 执行和跟踪",
                    "5. 评估和反思"
                ],
                output="OKR 文档 + 进度跟踪",
                triggers=["目标", "关键结果", "OKR", "对齐"]
            ),
            ThinkingModel(
                name="KPI",
                frequency=ModelFrequency.MEDIUM,
                category="管理",
                description="关键绩效指标",
                core_idea="量化评估绩效的关键指标",
                use_scenarios=["绩效管理", "目标考核", "业务监控", "团队评估"],
                steps=[
                    "1. 确定关键成功因素",
                    "2. 设计 KPI 指标",
                    "3. 设定目标值",
                    "4. 监控和评估",
                    "5. 改进和优化"
                ],
                output="KPI 指标体系 + 评估报告",
                triggers=["绩效", "指标", "考核", "KPI"]
            )
        ]
        
        # 低频模型（71 个，按需加载）- 示例 10 个
        self.low_frequency_models = [
            ThinkingModel(
                name="鱼骨图",
                frequency=ModelFrequency.LOW,
                category="分析",
                description="因果分析图",
                core_idea="将问题的可能原因按类别展示",
                use_scenarios=["根因分析", "质量问题", "团队讨论", "问题诊断"],
                steps=[
                    "1. 定义问题（鱼头）",
                    "2. 确定主要类别（大骨）",
                    "3. 头脑风暴可能原因（中骨、小骨）",
                    "4. 分析并找出根因"
                ],
                output="鱼骨图 + 根因清单",
                triggers=["因果", "鱼骨", "石川图", "根因"]
            ),
            ThinkingModel(
                name="六顶思考帽",
                frequency=ModelFrequency.LOW,
                category="决策",
                description="平行思维工具",
                core_idea="用六种颜色的帽子代表六种思维模式",
                use_scenarios=["团队讨论", "平行思维", "避免争论", "全面思考"],
                steps=[
                    "1. 白帽：客观事实",
                    "2. 红帽：情感直觉",
                    "3. 黑帽：谨慎风险",
                    "4. 黄帽：积极价值",
                    "5. 绿帽：创意可能",
                    "6. 蓝帽：控制过程"
                ],
                output="多维度分析结果",
                triggers=["六帽", "平行思维", "德博诺", "六顶思考帽"]
            ),
            ThinkingModel(
                name="系统循环图",
                frequency=ModelFrequency.LOW,
                category="系统",
                description="因果关系循环图",
                core_idea="展示系统中各要素的因果循环关系",
                use_scenarios=["系统分析", "复杂问题", "动态分析", "反馈理解"],
                steps=[
                    "1. 识别关键要素",
                    "2. 确定因果关系",
                    "3. 绘制循环图",
                    "4. 识别增强/调节回路"
                ],
                output="系统循环图 + 杠杆点分析",
                triggers=["系统", "循环", "反馈", "增强", "调节"]
            ),
            ThinkingModel(
                name="非暴力沟通",
                frequency=ModelFrequency.LOW,
                category="沟通",
                description="观察 - 感受 - 需要 - 请求",
                core_idea="通过四要素实现有效沟通",
                use_scenarios=["冲突解决", "有效沟通", "情感表达", "需求表达"],
                steps=[
                    "1. 观察：陈述事实",
                    "2. 感受：表达感受",
                    "3. 需要：说明需求",
                    "4. 请求：提出请求"
                ],
                output="沟通方案 + 解决方案",
                triggers=["沟通", "冲突", "感受", "需要", "NVC"]
            ),
            ThinkingModel(
                name="设计思维",
                frequency=ModelFrequency.LOW,
                category="创新",
                description="以人为本的创新方法",
                core_idea="通过同理心、定义、创意、原型、测试五步实现创新",
                use_scenarios=["产品设计", "服务创新", "用户体验", "问题解决"],
                steps=[
                    "1. 同理心：理解用户",
                    "2. 定义：明确问题",
                    "3. 创意：头脑风暴",
                    "4. 原型：快速制作",
                    "5. 测试：验证改进"
                ],
                output="创新方案 + 原型",
                triggers=["设计", "创新", "用户体验", "设计思维"]
            ),
            ThinkingModel(
                name="SCAMPER",
                frequency=ModelFrequency.LOW,
                category="创新",
                description="7 种创意激发方法",
                core_idea="通过 7 个问题激发创意",
                use_scenarios=["创意生成", "产品改进", "流程优化", "创新思考"],
                steps=[
                    "1. Substitute：替代",
                    "2. Combine：合并",
                    "3. Adapt：改造",
                    "4. Modify：修改",
                    "5. Put to other uses：他用",
                    "6. Eliminate：消除",
                    "7. Reverse：反转"
                ],
                output="创意清单 + 改进方案",
                triggers=["SCAMPER", "创意", "改进", "创新"]
            ),
            ThinkingModel(
                name="价值链分析",
                frequency=ModelFrequency.LOW,
                category="战略",
                description="分析企业价值创造活动",
                core_idea="将企业活动分为基本活动和辅助活动",
                use_scenarios=["竞争优势", "成本分析", "流程优化", "战略定位"],
                steps=[
                    "1. 识别基本活动",
                    "2. 识别辅助活动",
                    "3. 分析价值创造",
                    "4. 找到优化点"
                ],
                output="价值链图 + 优化建议",
                triggers=["价值链", "竞争优势", "成本", "活动"]
            ),
            ThinkingModel(
                name="PEST 分析",
                frequency=ModelFrequency.LOW,
                category="战略",
                description="宏观环境分析",
                core_idea="从政治、经济、社会、技术四个维度分析宏观环境",
                use_scenarios=["战略规划", "市场分析", "投资决策", "风险评估"],
                steps=[
                    "1. 政治环境分析",
                    "2. 经济环境分析",
                    "3. 社会环境分析",
                    "4. 技术环境分析"
                ],
                output="PEST 分析报告",
                triggers=["宏观", "环境", "PEST", "政治", "经济"]
            ),
            ThinkingModel(
                name="利益相关者分析",
                frequency=ModelFrequency.LOW,
                category="管理",
                description="识别和分析利益相关者",
                core_idea="识别所有利益相关者并分析其影响力和利益",
                use_scenarios=["项目管理", "变革管理", "战略规划", "风险管理"],
                steps=[
                    "1. 识别利益相关者",
                    "2. 分析影响力",
                    "3. 分析利益诉求",
                    "4. 制定管理策略"
                ],
                output="利益相关者地图 + 管理策略",
                triggers=["利益相关者", "干系人", "影响力", " stakeholder"]
            ),
            ThinkingModel(
                name="力场分析",
                frequency=ModelFrequency.LOW,
                category="决策",
                description="分析推动力和阻碍力",
                core_idea="分析推动变革的力量和阻碍变革的力量",
                use_scenarios=["变革管理", "决策分析", "问题解决", "阻力分析"],
                steps=[
                    "1. 定义变革或目标",
                    "2. 识别推动力",
                    "3. 识别阻碍力",
                    "4. 制定增强推动力策略",
                    "5. 制定减弱阻碍力策略"
                ],
                output="力场分析图 + 行动策略",
                triggers=["力场", "推动力", "阻碍力", "变革", "Lewin"]
            )
        ]
        
        # 场景到模型的映射
        self.scene_to_models = {
            'S0': ['五色光思维'],  # 日常对话
            'S1': ['艾森豪威尔矩阵', '知行合一'],  # 任务执行
            'S2': ['第一性原理', '5Why 分析法', '金字塔原理'],  # 深度理解
            'S3': ['象思维', '第一性原理'],  # 创意创新
            'S4': ['SWOT 分析', 'MECE 原则', '五色光思维', '知行合一'],  # 分析决策
            'S5': ['SWOT 分析', '波特五力', '第一性原理', '五色光思维', '知行合一'],  # 重大决策
            'S6': ['五色光思维', '金字塔原理', 'SCQA 框架'],  # 会议引导
            'S7': ['MECE 原则', '金字塔原理', '第一性原理'],  # 知识编译
            'S8': ['象思维', '五行分类'],  # 修行文化
            'S9': ['PDCA 循环', '第一性原理', '知行合一']  # 系统进化
        }
    
    def route(self, scene_code: str, input_text: str) -> List[ThinkingModel]:
        """
        根据场景和输入文本路由到思维模型
        
        Args:
            scene_code: 场景代码 (S0-S9)
            input_text: 用户输入文本
            
        Returns:
            List[ThinkingModel]: 推荐的思维模型列表
        """
        # 获取场景对应的模型列表
        scene_model_names = self.scene_to_models.get(scene_code, [])
        
        # 从输入文本中提取额外触发
        triggered_models = self._trigger_from_text(input_text)
        
        # 合并模型列表（去重）
        all_model_names = list(set(scene_model_names + triggered_models))
        
        # 查找模型对象
        selected_models = []
        for model_name in all_model_names:
            model = self._find_model(model_name)
            if model:
                selected_models.append(model)
        
        return selected_models
    
    def _find_model(self, name: str) -> Optional[ThinkingModel]:
        """查找模型"""
        all_models = (
            self.high_frequency_models + 
            self.medium_frequency_models + 
            self.low_frequency_models
        )
        
        for model in all_models:
            if model.name == name:
                return model
        
        return None
    
    def _trigger_from_text(self, text: str) -> List[str]:
        """从文本中触发模型"""
        triggered = []
        # 只从高频和中频模型中触发
        all_models = self.high_frequency_models + self.medium_frequency_models
        
        for model in all_models:
            for trigger in model.triggers:
                if trigger in text:
                    triggered.append(model.name)
                    break
        
        return triggered
    
    def get_model_details(self, name: str) -> Optional[Dict]:
        """获取模型详细信息"""
        model = self._find_model(name)
        if model:
            return {
                'name': model.name,
                'frequency': model.frequency.value,
                'category': model.category,
                'description': model.description,
                'core_idea': model.core_idea,
                'use_scenarios': model.use_scenarios,
                'steps': model.steps,
                'output': model.output,
                'triggers': model.triggers
            }
        return None
    
    def get_models_by_category(self, category: str) -> List[ThinkingModel]:
        """按分类获取模型"""
        all_models = (
            self.high_frequency_models + 
            self.medium_frequency_models + 
            self.low_frequency_models
        )
        
        return [m for m in all_models if m.category == category]
    
    def get_models_by_frequency(self, frequency: ModelFrequency) -> List[ThinkingModel]:
        """按频率获取模型"""
        if frequency == ModelFrequency.HIGH:
            return self.high_frequency_models
        elif frequency == ModelFrequency.MEDIUM:
            return self.medium_frequency_models
        else:
            return self.low_frequency_models
    
    def recommend_for_step(self, project_name: str, step_name: str) -> List[ThinkingModel]:
        """为项目步骤推荐模型"""
        # 项目步骤到模型的映射（示例）
        step_recommendations = {
            ('超级个体落地', '概念分析'): ['第一性原理', 'MECE 原则'],
            ('超级个体落地', '市场调研'): ['SWOT 分析', '波特五力'],
            ('超级个体落地', '产品设计'): ['象思维', '商业模式画布'],
            ('超级个体落地', '落地实施'): ['知行合一', 'PDCA 循环'],
            ('超级个体落地', '复盘优化'): ['5Why 分析法', '五色光思维'],
        }
        
        key = (project_name, step_name)
        model_names = step_recommendations.get(key, [])
        
        models = []
        for name in model_names:
            model = self._find_model(name)
            if model:
                models.append(model)
        
        return models


def main():
    """测试思维模型路由器"""
    router = ModelRouter()
    
    print("=" * 70)
    print("思维模型.skills - 模型路由器测试")
    print("=" * 70)
    
    # 测试 1: 场景路由
    test_cases = [
        ('S0', '你好，最近怎么样？'),
        ('S1', '帮我写一个 Python 脚本'),
        ('S2', '深度学习这篇文章的核心观点'),
        ('S3', '需要创意，这个问题没有标准答案'),
        ('S4', '如何把超级个体概念落地实施？'),
        ('S5', '人生重大决策，应该选择哪个方向？'),
        ('S6', '开会讨论总是跑题，怎么办？'),
        ('S7', '编译这个知识库到 LLM Wiki'),
        ('S8', '修行和文化的关系是什么？'),
        ('S9', '系统如何自动进化优化？')
    ]
    
    print("\n【测试 1: 场景路由】")
    for scene_code, input_text in test_cases:
        models = router.route(scene_code, input_text)
        print(f"\n{scene_code}: {input_text[:20]}...")
        print(f"  推荐模型：{', '.join([m.name for m in models])}")
    
    # 测试 2: 模型详情
    print("\n【测试 2: 模型详情 - 第一性原理】")
    details = router.get_model_details('第一性原理')
    if details:
        print(f"  分类：{details['category']}")
        print(f"  核心思想：{details['core_idea']}")
        print(f"  使用步骤：{len(details['steps'])}步")
    
    # 测试 3: 按分类查询
    print("\n【测试 3: 按分类查询 - 分析类】")
    analysis_models = router.get_models_by_category('分析')
    print(f"  分析类模型：{len(analysis_models)}个")
    print(f"  模型列表：{', '.join([m.name for m in analysis_models])}")
    
    # 测试 4: 项目步骤推荐
    print("\n【测试 4: 项目步骤推荐 - 超级个体落地】")
    steps = ['概念分析', '市场调研', '产品设计', '落地实施', '复盘优化']
    for step in steps:
        models = router.recommend_for_step('超级个体落地', step)
        print(f"  {step}: {', '.join([m.name for m in models])}")


if __name__ == "__main__":
    main()
