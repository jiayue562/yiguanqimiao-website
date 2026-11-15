---
name: API规范
parent_skill: ai-os
description: 内部/外部API统一规范——AI OS API设计标准
version: v1.0
created: 2026-06-27
updated: 2026-06-27
---

## API规范 v1.0

### 内部API
- 模块间调用使用Python import
- 引擎统一接口：process(input, context) -> EngineResult
- 域统一接口：无状态函数式调用

### 外部API
- CLI入口：json.dumps(result, ensure_ascii=False)
- opencode skill入口：标准Python脚本
- 输出格式：统一JSON结构

### API设计原则
1. 输入校验：所有输入需类型检查
2. 错误处理：统一返回{"error": "..."}
3. 版本兼容：向前兼容，废弃标记
4. 无副作用：纯函数优先
```

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/scripts/IMA_API测试报告]] — IMA API同步测试报告
- [[03-知识地基层/记忆系统_ERRORS]] — ERRORS.md - 错误记录与规避
- [[09-技能库/Harness-Engineering/references/execution-layer]] — Harness Engineering · 执行层
- [[09-技能库/resources_quick-start]] — IMA 技能快速使用指南
- [[09-技能库/知识库建设/references/sync-mechanism]] — 同步机制与自动化脚本
- [[ψ技能体系/00-foundation/三向同步系统/scripts/IMA_API测试报告]] — IMA API同步测试报告

<!-- AI-LINKS-END -->
