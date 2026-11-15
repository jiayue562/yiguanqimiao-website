#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# UTF-8 BOM

"""
龙爪 OS 工作流路由器
根据项目类型和步骤，路由到对应的思维模型组合

版本：v1.0
创建：2026-04-17
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class WorkflowStep:
    """工作流步骤定义"""
    name: str
    description: str
    thinking_models: List[str]  # 推荐思维模型
    output: str  # 预期输出


@dataclass
class ProjectTemplate:
    """项目模板定义"""
    name: str
    category: str  # 战略/产品/市场/组织/个人
    steps: List[WorkflowStep]
    estimated_duration: str  # 预估时长


class WorkflowRouter:
    """工作流路由器 - 项目/工作流/SOP 路由"""
    
    def __init__(self):
        """初始化路由器"""
        # 项目模板库
        self.project_templates = {
            '超级个体落地': ProjectTemplate(
                name='超级个体落地',
                category='战略',
                steps=[
                    WorkflowStep(
                        name='概念分析',
                        description='从第一性原理出发，理解超级个体本质',
                        thinking_models=['第一性原理', 'MECE 原则'],
                        output='超级个体本质分析文档'
                    ),
                    WorkflowStep(
                        name='市场调研',
                        description='分析市场机会和竞争格局',
                        thinking_models=['SWOT 分析', '波特五力'],
                        output='市场机会评估报告'
                    ),
                    WorkflowStep(
                        name='产品设计',
                        description='设计产品和服务模式',
                        thinking_models=['象思维', '商业模式画布'],
                        output='产品方案'
                    ),
                    WorkflowStep(
                        name='落地实施',
                        description='制定执行计划并落地',
                        thinking_models=['知行合一', 'PDCA 循环'],
                        output='执行计划'
                    ),
                    WorkflowStep(
                        name='复盘优化',
                        description='总结经验，持续优化',
                        thinking_models=['5Why 分析法', '五色光思维'],
                        output='优化建议'
                    )
                ],
                estimated_duration='4-6 周'
            ),
            # 更多项目模板待添加...
        }
    
    def route(self, project_name: str) -> Optional[ProjectTemplate]:
        """根据项目名称路由到对应模板"""
        return self.project_templates.get(project_name)
    
    def get_step_models(self, project_name: str, step_index: int) -> List[str]:
        """获取特定步骤的推荐思维模型"""
        template = self.route(project_name)
        if template and 0 <= step_index < len(template.steps):
            return template.steps[step_index].thinking_models
        return []
    
    def get_all_templates(self) -> Dict[str, ProjectTemplate]:
        """获取所有项目模板"""
        return self.project_templates


def main():
    """测试工作流路由器"""
    router = WorkflowRouter()
    
    print("=" * 70)
    print("龙爪 OS 工作流路由器测试")
    print("=" * 70)
    
    # 测试：超级个体落地项目
    template = router.route('超级个体落地')
    if template:
        print(f"\n项目：{template.name}")
        print(f"类别：{template.category}")
        print(f"预估时长：{template.estimated_duration}")
        print(f"\n工作流步骤:")
        for i, step in enumerate(template.steps, 1):
            print(f"\n步骤{i}: {step.name}")
            print(f"  描述：{step.description}")
            print(f"  思维模型：{', '.join(step.thinking_models)}")
            print(f"  输出：{step.output}")


if __name__ == "__main__":
    main()
