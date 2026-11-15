# 五大子智能体集成指南

## 调度协议

每个子智能体 Skill 必须实现以下接口：

`
trigger_conditions:  # 触发条件列表
  - trigger: "关键词/模式"
    scene: "所属 S 场景"
    action: "执行动作描述"
  - trigger: "..."
    scene: "..."
    action: "..."

output_format:  # 输出格式
  - type: "Markdown/JSON/Text"
  - structure: "核心输出结构"
`

## 注册流程

1. 子智能体 Skill 放在 ~/.agents/skills/ 下
2. 在 frontmatter 中声明 parent_skill: 龙心 OS
3. 在 sub_skills: 中添加
4. 在场景识别矩阵中添加对应 S 代码

## 当前注册的子智能体

| Skill | 场景 | 触发模式 |
|-------|------|----------|
| 知行合一 | S4/S5 | 自动调度 |
| 知识学习 | S2/S7 | 自动调度 |
| 人机协同五象限 | S0/S1/S5 | 自动调度 |
| 象思维 | S3/S8 | 自动调度 |
| 五色光思维 | S4/S6 | 自动调度 |

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI OS智能体激活框架/NSCDC1B-01-AI OS功能架构·完整映射]] — AI OS功能架构·完整映射
- [[03-知识地基层/五大 Skills/NS1B07C-99-五大 Skills 验证报告]] — 五大 Skills 自动安装验证报告
- [[09-技能库/AI-OS六层架构智能体/references/决策层]] — 决策层 v1.0
- [[09-技能库/五行人格心理学/L3智能调度内核/references/场景识别矩阵]] — 五行人格心理学操作系统 - 场景识别矩阵 v1.0
- [[ψ技能体系/20-claws/01-weizang/weizang-chief/references/scene-routing]] — 味藏总智能体 · references/scene-routing.md
- [[ψ技能体系/20-claws/01-weizang/味藏店长标准版/references/7s-architecture]] — 7S架构说明
- [[ψ技能体系/99-archive/龙心 OS/scripts/test-cases]] — 龙心 OS 实际对话测试用例

<!-- AI-LINKS-END -->
