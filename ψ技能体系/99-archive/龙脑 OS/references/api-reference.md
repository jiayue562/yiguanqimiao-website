# 龙脑OS API参考

## 核心接口

### engine_router(input)
路由用户输入到对应的知识库和思维模型。

**参数**:
- input(dict): {scene_code, context, history}

**返回**:
- output(dict): {model_list, confidence, knowledge_bases}

### model_finder(keywords, scene)
根据关键词和场景查找匹配的思维模型。

**参数**:
- keywords(list): 关键词列表
- scene(str): 场景代码 S0-S9

**返回**:
- models(list): 匹配模型列表

### cross_domain_search(topic, depth)
跨域知识检索。

**参数**:
- topic(str): 主题
- depth(str): "quick"|"deep"

**返回**:
- results(dict): 跨域关联结果

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/AI龙龟共生伙伴操作系统/references/integration-protocol]] — AI OS 三层整合协议
- [[ψ技能体系/20-claws/00-wuxing/凤心OS/references/scene-router]] — 场景路由模块 (Scene Router)
- [[ψ技能体系/20-claws/00-wuxing/凤脑OS/references/integration-patterns]] — 凤脑OS集成模式 (Integration Patterns)
- [[ψ技能体系/30-tools/tavily/references/api-reference]] — Tavily API Reference
- [[ψ技能体系/99-archive/龙心 OS/references/architecture-guide]] — 龙心 OS 架构指南
- [[ψ技能体系/99-archive/龙心 OS/references/scene-classification-guide]] — 龙心 OS 架构指南

<!-- AI-LINKS-END -->
