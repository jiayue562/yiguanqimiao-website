# WorkBuddy 交付链与 Tier2 插件（FBS）

> **目的**：把「MD/HTML 为默认、多格式走宿主」落到**可执行顺序**，避免用户找不到 Word/PDF/幻灯片导出路径。  
> **真值**：以 `host-capability-detect.mjs` 输出的 `.fbs/host-capability.json` 中 `plugins.enabled` 为准。

## 1. 能力分层（简述）

| 层级 | 典型能力 | 用户侧说法 |
|------|-----------|------------|
| Tier2 插件 | `docx`、`pdf`、`pptx`、`xlsx`、`playwright-cli` | 「用宿主里的文档/导出能力」 |
| Tier1 市场技能 | `minimax-docx`、`minimax-pdf`、`pptx-generator` 等 | 「增强型排版/印刷」 |
| 仓库脚本 | `assets/build.mjs`、合并稿 | 「本地构建 HTML / 合并全书稿」 |

## 2. 推荐顺序（S4/S5）

1. **定稿内容**以书稿目录下 Markdown 真值为准（`deliverables/` 约定见 `channel-manifest`）。
2. **HTML 预览**：`assets/build.mjs` 或宿主预览；若 `presentationBridgeSupported`，可走 `host-consume-presentation` 展示链路。
3. **Word/PDF/PPTX/XLSX**：优先走 **已启用的 Tier2 插件**；Tier1 作为增强（见 `provider-registry.yml`）。
4. 向用户说明时**不复述**插件内部代号；只说「导出为 Word」「生成 PDF」等。

## 3. 与 `intake-router` 的衔接

`firstResponseContext.deliveryAndPreview` 会给出**对人话**的交付与文件夹提示；Agent 应优先遵循该块，再查本文件细节。

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/fbs-bookwriter/docs/history/SMART-MEMORY-ARCHITECTURE-v2.0.2]] — 智能记忆架构说明
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/brand-platform-convention]] — 品牌与平台规范（FBS × 福帮手 × 双通道宿主）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workbuddy-agent-briefings]] — 宿主平台多智能体委托话术（S3 / S5）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/workflow-volumes/workflow-s4]] — S4 节点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/delivery-guide]] — 交付指南：从 MD 到多格式
- [[ψ技能体系/30-tools/fbs-bookwriter/references/05-ops/fbs-optimization-roadmap-spec]] — FBS 优化路线图规格（P0–P2）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/plugin-bus-spec]] — Plugin Bus 协议规范 v3.0
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/s5-full-delivery-sop]] — S5 全格式交付 SOP（Plugin Bus v3.0）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/tier1-marketplace-faq]] — Tier1 本地市场技能常见问题（WorkBuddy）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/06-plugin/workbuddy-host-integration]] — WorkBuddy 宿主集成说明（最小契约）

<!-- AI-LINKS-END -->
