---
title: "三OS接口契约 v1.0"
description: "龙心OS、龙脑OS、龙爪OS之间的API接口定义——输入输出格式、调用协议、错误处理"
version: "1.2"
updated: "2026-07-29"
tags: [龙心OS, 龙脑OS, 龙爪OS, 接口契约]
---

# 三OS接口契约 v1.0

> 三OS通过龙心OS总智能体统一调度，不直接互相调用。
> 龙爪OS执行前可查询龙脑OS获取推荐模型。

---

## 一、总体架构

```
用户输入
    │
    ▼
龙心OS总智能体（唯一入口）
    │
    ├──→ 龙脑OS（查询方法论/思维模型）
    │        返回：模型ID + 组合规则 + 约束条件
    │
    └──→ 龙爪OS（执行工作流/SOP）
             返回：执行状态 + 步骤结果 + 进度
```

---

## 二、龙心OS → 龙脑OS 接口

### 2.1 查询思维模型推荐

```
请求：GET_MODEL_RECOMMENDATION
{
  "task_type": "JY|ZL|FA|WD|GT|XX|CZ|CY",  // 任务类型（选刃决策树分类）
  "task_description": "本月毛利下降3%的原因分析",  // 任务描述文本
  "context": {  // 上下文
    "domain": "味藏餐饮",
    "urgency": "high|medium|low",
    "constraints": ["需在30分钟内完成"]
  }
}

返回：MODEL_RECOMMENDATION
{
  "primary_chain": [  // 首选模型链
    {"model_id": "bottleneck_theory", "reason": "定位阻塞环节"},
    {"model_id": "five_layer_analysis", "reason": "逐层穿透根因"}
  ],
  "alternative_chain": [  // 备选模型链
    {"model_id": "systems_thinking", "reason": "检查多环节联动"},
    {"model_id": "pareto", "reason": "筛选20%核心因素"}
  ],
  "selection_rule": "先首选，不适配则切换备选并声明理由",
  "reference_files": [  // 参考知识库文件
    "02-思维模型/02-问题分析类/五层分析法.md",
    "03-理论/02-社会认知类/认知吝啬者理论.md"
  ],
  "confidence": 0.85  // 推荐置信度
}
```

### 2.2 查询方法论约束

```
请求：GET_METHODOLOGY_CONSTRAINT
{
  "engine_id": "xiang_si_wei|five_color|knowledge_learning",
  "task_type": "analysis|creation|decision"
}

返回：METHODOLOGY_CONSTRAINT
{
  "constraint_rules": [
    "推理前必须声明所用模型",
    "输出中保留模型使用痕迹",
    "切换模型需声明理由"
  ],
  "applicable_models": ["model_id1", "model_id2"],
  "forbidden_patterns": ["无来源论断", "单一视角结论"]
}
```

---

## 三、龙心OS → 龙爪OS 接口

### 3.1 执行工作流

```
请求：EXECUTE_WORKFLOW
{
  "workflow_id": "workflow_project_001",
  "project_name": "毛利下降分析",
  "project_category": "经营分析",
  "steps": [  // 由龙脑OS推荐或龙心OS指定的步骤
    {
      "step_id": 1,
      "name": "数据采集与根因定位",
      "recommended_models": ["瓶颈理论", "五层分析法"],
      "input": {"毛利数据": "上月12.8%→本月9.5%"},
      "timeout_seconds": 300
    },
    {
      "step_id": 2,
      "name": "方案制定",
      "recommended_models": ["5W2H", "决策矩阵"],
      "input": {"根因": "损耗率上升"},
      "timeout_seconds": 600
    }
  ],
  "callbacks": {
    "on_step_complete": "龙心OS/回调/step_complete",
    "on_workflow_complete": "龙心OS/回调/workflow_complete",
    "on_error": "龙心OS/回调/on_error"
  }
}

返回：WORKFLOW_EXECUTION_RESULT
{
  "workflow_id": "workflow_project_001",
  "status": "running|completed|failed|paused",
  "current_step": 1,
  "total_steps": 2,
  "step_results": [
    {
      "step_id": 1,
      "status": "completed",
      "output": "根因定位结果...",
      "models_used": ["瓶颈理论", "五层分析法"],
      "duration_seconds": 45
    }
  ],
  "overall_progress": 0.5,
  "error": null
}
```

### 3.2 查询执行进度

```
请求：GET_WORKFLOW_PROGRESS
{
  "workflow_id": "workflow_project_001"
}

返回：WORKFLOW_PROGRESS
{
  "workflow_id": "workflow_project_001",
  "status": "running|completed|failed|paused",
  "current_step": 1,
  "total_steps": 2,
  "step_status": "in_progress|completed|pending",
  "overall_progress": 0.5,
  "estimated_remaining": "5分钟"
}
```

### 3.3 深度共生·运行时接线（v3.0 真实执行，2026-07-29）

> 本章 3.1/3.2 为设计契约；v3.0 起已落地真实运行时接线，替换此前「仅文档无代码」状态（审计评分由 2.7→可执行）。

**龙爪OS 真实执行层（v3.0）**
- `framework/step_executor.py`：步骤执行器由模拟桩升级为真实执行——
  - 五行人格心理学OS 项目步骤 → subprocess 真实委派 `五行人格心理学OS/framework/orchestrator.py`（凤爪→凤心→凤脑 全闭环）；
  - 其余项目步骤 → 真实调用龙脑OS 选刃引擎取得模型链 + 产出可执行「执行契约」；
  - 全程 try/except 降级，引擎/编排器不可达时优雅回退。
- `framework/progress_tracker.py`：进度追踪由纯内存升级为磁盘持久化（`runtime/projects/<id>.json`），支持跨会话续跑。
- `framework/longzhao_orchestrator.py`：顶层全闭环入口 `run(project_request)`，串联 路由→真实执行→进度追踪→交付计划，提供 `--json` 供龙心集成。

**龙心OS 常驻子系统接线（深度共生）**
- 龙心OS 调度中枢 `engines/调度中枢/subsystems/longzhao_subsystem.py`：龙爪OS 作为龙心 1+5 总调度下的**常驻执行子系统**（与五行子系统并列），`detect→dispatch→report→heartbeat` 四层闭环。
- 龙心调度 `run()` 末调用 `subsystems.dispatch_all()`，命中执行类意图即派发龙爪编排器，结果回灌龙心共享共生记忆 `龙爪OS/runtime/longzhao_symbiosis_feed.jsonl`。
- 至此「龙心(总调度)→龙爪(执行)↔龙脑(知识)」三方协同闭环成立（此前审计判「三OS未真正协同」已修复）。

**多轮反哺（feed 影响路由，2026-07-29）**
- `subsystems/feedback.py` 读取五行 / 龙爪 共享共生记忆，统计各子系统历史派发频次；
- `dispatch_all()` 据此为成熟子系统提升路由置信度（`confidence = min(0.99, 0.5 + 0.03×历史次数)`），实现「龙心派发→五行/龙爪回灌→影响后续路由」闭环。

---

## 四、龙爪OS → 龙脑OS 接口

### 4.1 查询当前步骤的推荐模型

```
请求：GET_STEP_MODELS
{
  "step_name": "根因分析",
  "step_description": "分析毛利下降的原因",
  "project_category": "经营分析"
}

返回：STEP_MODELS
{
  "recommended_models": [
    {"model_id": "five_whys", "priority": "primary", "reason": "适合单线因果深挖"},
    {"model_id": "bottleneck_theory", "priority": "primary", "reason": "定位阻塞环节"},
    {"model_id": "systems_thinking", "priority": "alternative", "reason": "多环节联动分析"}
  ],
  "usage_rule": "至少选1个primary模型"
}
```

---

## 五、统一错误码

| 错误码 | 含义 | 处理方式 |
|:------:|------|---------|
| E000 | 成功 | 正常处理 |
| E001 | 引擎不可用 | 切换备选引擎或降级到基础模式 |
| E002 | 请求超时 | 重试1次，仍超时则跳过该步骤 |
| E003 | 输入格式错误 | 返回具体的格式要求 |
| E004 | 模型不适用（推理中发现） | 声明切换理由，换备选模型 |
| E005 | 工作流中断 | 保存当前进度，下次可续跑 |
| E010 | 未知错误 | 返回错误详情，人工介入 |

### 降级策略

| 故障场景 | 降级到 | 说明 |
|---------|--------|------|
| 龙脑OS不可用 | 龙心OS使用内置基础模型（免查询） | 5个基础模型：MECE、第一性原理、逆向思维、系统思维、概率思维 |
| 龙爪OS不可用 | 龙心OS直接输出思维模型推荐（跳过执行） | 至少让用户知道"应该用什么模型" |
| 选刃决策树无匹配 | 返回"未知场景，建议使用五层分析法兜底" | 兜底模型固定为五层分析法 |
| 引擎调用超时 | 返回已生成的部分结果+继续处理标记 | 不让用户空等 |

---

## 六、龙心OS → 五行人格心理学OS（凤系列三OS）接口（深度共生）

> 五行人格心理学OS（凤爪·执行 / 凤心·决策 / 凤脑·知识）作为龙心OS 1+5 总调度的**常驻五行执行子系统**，
> 形成四层持续共生闭环：龙心(总调度) → 凤爪(执行入口) → 凤心(五行决策) → 凤脑(知识底座)；
> 五行结果经编排器回灌龙心共享共生记忆，凤心决策经 `_longxin_governance()` 上行向龙心统辖。

### 6.1 常驻注册
龙心OS调度中枢（`engines/调度中枢/scheduler.py`）加载时即导入 `subsystems` 注册表，
五行子系统在 `RESIDENT_SUBSYSTEMS` 中常驻（`resident=True`），非按需临时挂载。

### 6.2 意图检测 + 派发
请求（龙心OS统一入口的用户输入文本）：
- 调度中枢 `run()` 每轮询问常驻子系统 `WuxingSubsystem.detect(text)`；
- 命中五行域意图（亲密/吵架/亲子/教育/测评/五行/人格/失眠/拖延/关系/焦虑等强信号）则派发；
- `dispatch(text)` 经 subprocess 调用 `五行人格心理学OS/framework/orchestrator.py --json`，
  跑通 凤爪→凤心→凤脑 全闭环，返回统一自主结果。

返回：WUXING_SUBSYSTEM_RESULT
```
{
  "subsystem": "wuxing_os",
  "handled": true,
  "dispatch": {
    "status": "ok",
    "closed_loop": true,
    "raw": { "scene": "S1·亲密关系", "primary_element": "水", "longxin_governance": {...} }
  },
  "report": { "fed": true, "status": "ok" }
}
```

### 6.3 上行治理（凤心 → 龙心）
凤心OS `auto_trigger._longxin_governance()` 调用 `longxin_bridge.build_governance()` 生成真实治理载荷：
```
{
  "under": "龙心OS 1+5 总调度",
  "runtime_engine": "connected",
  "layer": "五行执行子系统（凤爪·执行 / 凤心·决策 / 凤脑·知识）",
  "scene": "S1·亲密关系", "primary_element": "水", "route_type": "生克路由",
  "governed_at": "<ISO时间戳>"
}
```
该载荷随编排器JSON经subprocess回传龙心，由龙心侧子系统写入共享共生记忆（见6.4）。

### 6.4 共享共生记忆（龙心 ↔ 五行 双向落点）
落点：`~/.workbuddy/skills/五行人格心理学OS/runtime/longxin_symbiosis_feed.jsonl`（单行JSON-Lines）
- 龙心侧（`wuxing_subsystem.report_to_longxin`）为写入方/记忆owner；
- 五行侧（`longxin_bridge.resolve_longxin_feed`）读取同一文件做上行治理核对；
- 路径由双方 `expanduser` 解析，保持一致。

### 6.5 降级策略
| 故障场景 | 降级到 | 说明 |
|---------|--------|------|
| 五行OS编排器未挂载 | 子系统 `dispatch` 返回 `unavailable`，龙心主流程不受影响 | 意图检测仍工作 |
| 凤心治理桥不可达 | `_longxin_governance()` 回退 stub（`runtime_engine: pending`） | 不拖垮凤心决策 |
| 子系统层缺失 | 调度中枢 `run()` 跳过常驻派发（`_RESIDENT_ENABLED=False`） | 其余引擎正常 |

---

## 七、版本与维护

| 版本 | 日期 | 变更 |
|:----:|:----:|------|
| v1.0 | 2026-07-28 | 初始版本 |
| v1.1 | 2026-07-29 | 新增龙心OS→五行人格心理学OS（凤系列三OS）深度共生接口：常驻子系统·四层闭环·上行治理·共享共生记忆 |
| v1.2 | 2026-07-29 | 龙爪OS→龙心常驻子系统接线（真实执行+磁盘持久化）+ 多轮反哺闭环；三OS协同审计项「未真正协同」修复 |

**接口扩展规则**：新接口按`[调用方]_[被调方]_[功能名]`格式命名，新增时保持向后兼容。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/AI龙龟共生OS/AI龙龟共生OS·开发文档]] — AI龙龟共生OS · 开发文档
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/AI龙龟共生OS/AI龙龟共生OS·顶层设计]] — AI龙龟共生OS · 顶层设计
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙爪OS：AI原生组织岗位智能体/岗位智能体OS·开发文档]] — 岗位智能体OS · 开发文档
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙爪OS：AI原生组织岗位智能体/岗位智能体OS·顶层设计]] — 岗位智能体OS · 顶层设计
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙脑OS升级包：思维模型/龙脑动态组方引擎-开发文档]] — 龙脑动态组方引擎 · 开发文档
- [[09-技能库/AI龙龟共生伙伴操作系统/references/three-layer-architecture]] — AI OS 三层架构详解

<!-- AI-LINKS-END -->
