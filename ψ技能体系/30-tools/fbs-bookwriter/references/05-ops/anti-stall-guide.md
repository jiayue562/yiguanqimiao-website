# 防卡顿执行指南

> **版本**：2.1.1  
> **目标**：缩短首响等待、避免长时间无输出、限制宿主侧大文件解析。

---

## 1. 首响（intake-router）

| 手段 | 说明 |
|------|------|
| **`--fast`** | 跳过场景包 **全量** `loadScenePack`，仅执行乐包 `registerBook`；适合「先开口再加载」的交互。 |
| **场景包超时降级** | 默认约 **15s**（`FBS_SCENE_PACK_TIMEOUT_MS` 可覆盖）；超时则自动降级为仅 `registerBook`，避免网络/企微阻塞首响。 |
| **JSON 字段** | `intake-router --json` 返回 `performance`，含 `intakeFast` / `scenePackSkippedFast` / `scenePackTimedOut`。 |

推荐命令：

```bash
node scripts/intake-router.mjs --book-root <书稿根> --intent auto --json --enforce-required --fast
# 或
node scripts/fbs-cli-bridge.mjs intake -- --book-root <书稿根> --intent auto --json --fast
```

---

## 2. 宿主画像与记忆文件

- 宿主 `memory/`、`memery/` 下 `*_memory.md`：**单次最多解析 24 个文件**（按文件名排序后截断）。
- 单文件读入：**超过约 96KB 部分截断**，避免极端大文件阻塞同步读。

---

## 3. 长任务（与既有文档对齐）

- S3 写作：**单轮最多改 2 个文件**；**单文件操作超过约 30s 无输出**须打一行进度（见 `SKILL.md`）。
- 全景质检：见 `quality-panorama-orchestrator.mjs` 心跳与 partial 交付。
- **与对话层阈值分层一致**：预计整段耗时 **>15s** 时**开始前**先说明时长；**执行中**以约 **30s** 为心跳/单行提示节奏（详见 [`references/03-product/07-ux-design.md`](../03-product/07-ux-design.md) 原则2）。

---

## 4. 机读配置

`fbs-runtime-hints.json` → `antiStall`。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/SKILL]] — 福帮手出品 | 高质量长文档手稿工具链（FBS-BookWriter）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/information-ownership-and-arbitration]] — 信息产权、场景包坐标与记忆仲裁
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/runtime-mandatory-contract]] — 运行时强制契约（主 Agent / 宿主对齐）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/skill-cli-bridge-matrix]] — Skill ↔ 脚本 ↔ CLI 联动矩阵（非 MCP）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/03-product/NS08213-07-ux-design]] — UX 设计规范（对话层防卡顿 · 流畅度设计）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/03-product/NS08213-08-visual]] — 视觉资产生成策略
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-context-compression]] — 上下文压缩策略（P1 B1）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-performance-ux]] — 体验与防卡顿专项（性能 / 价值显性化）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-subtask-contract]] — 长任务 / 辅助子任务机读契约（FBS）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/s3-write-constraints]] — S3 写作阶段写入约束（规范真值）

<!-- AI-LINKS-END -->
