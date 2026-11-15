# 龙心OS调用协议

## 接口定义
龙脑OS通过 engine_router.py 与龙心OS通信。

### 输入格式
```json
{
  "scene_code": "S0-S9",
  "context": "用户输入全文",
  "history": "最近5轮对话"
}
```

### 输出格式
```json
{
  "model_list": ["模型1", "模型2"],
  "confidence": 0.85,
  "knowledge_bases": ["思维模型库", "五行人格"],
  "recommendation": "推荐方案"
}
```

## 数据流
龙心OS → 场景识别 → 龙脑OS路由 → 知识库匹配 → 模型推荐 → 结果整合 → 龙心OS回复

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL注册表]] — AIOS 技能注册表（SKILL Registry）
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙脑OS升级包：思维模型/龙脑动态组方引擎-开发文档]] — 龙脑动态组方引擎 · 开发文档
- [[09-技能库/AI龙龟共生伙伴操作系统/优化现有Skills指南]] — 优化现有Skills指南
- [[09-技能库/思维模型库/references/integration]] — 思维模型库 · 龙心OS调用协议
- [[09-技能库/麦肯锡思考框架/references/integration]] — 麦肯锡思考框架 · 龙心OS调用协议
- [[ψ技能体系/10-kernel/龙脑OS/models/麦肯锡思考框架/references/integration]] — 麦肯锡思考框架 · 龙心OS调用协议

<!-- AI-LINKS-END -->
