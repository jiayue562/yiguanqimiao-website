# 龙心 OS 架构指南

> framework/ 目录对应代码架构说明

## 三层架构

```
概念层（概念澄清）
  ├── 声明：龙心 OS 本质是智能体（生命体）
  └── 区分"智能体" vs "普通 Skill"

架构层（Framework 突破）
  ├── core.py              — 核心调度循环（感知→决策→行动）
  ├── scene_classifier.py  — S0-S9 场景分类器
  ├── engine_router.py     — 引擎路由决策
  └── feedback_learner.py  — 反馈学习与优化

载体层（Skill 结构）
  ├── triggers/            — 自动触发配置
  ├── templates/           — 输出模板
  └── scripts/             — 运维脚本
```

## 核心文件说明

| 文件 | 功能 | 关键类/函数 |
|------|------|-------------|
| `framework/core.py` | 核心调度循环 | `schedule_loop()`, `perceive()`, `decide()`, `act()` |
| `framework/scene_classifier.py` | S0-S9 场景分类 | `classify(context) -> (scene, confidence)` |
| `framework/engine_router.py` | 引擎路由分配 | `route(scene, context) -> [engine_ids]` |
| `framework/feedback_learner.py` | 反馈学习 | `learn(feedback)`, `optimize_routing()` |

## 数据流

```
用户输入
  → perceive()     [context, sentiment, topic]
    → classify()   [S0-S9 + confidence]
      → route()    [engine list + priority]
        → execute() [engine output]
          → present() [integrated response]
            → learn() [feedback → optimize]
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/AI-OS六层架构智能体/references/决策层]] — 决策层 v1.0
- [[09-技能库/五行总智能体/references/architecture-overview]] — 五行总智能体系统架构总览
- [[ψ技能体系/20-claws/01-weizang/P-01问题路由引擎/references/feedback-card-template]] — feedback-card-template
- [[ψ技能体系/99-archive/龙心 OS/CHECKLIST]] — 龙心OS CHECKLIST — 质量检查清单
- [[ψ技能体系/99-archive/龙心 OS/framework/core.py]] — 龙心 OS Framework 层
- [[ψ技能体系/99-archive/龙心 OS/references/scene-classification-guide]] — 龙心 OS 架构指南
- [[ψ技能体系/99-archive/龙脑 OS/references/api-reference]] — 龙脑OS API参考

<!-- AI-LINKS-END -->
