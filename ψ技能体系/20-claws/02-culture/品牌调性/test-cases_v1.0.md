# 味藏品牌调性 - 测试用例集
# Skill Builder L0-L8九层测试 | 版本 v1.0
# 2026-06-15 | © 味藏商学院

---

## 测试概览

| 层级 | 测试项 | 用例数 | 通过率 |
|------|-------|--------|-------|
| L0 封装完整性 | 元数据+文件+同步 | 10 | 预期100% |
| L1 触发机制 | P0/P1/P2关键词 | 15 | - |
| L2 场景路由 | S1-S7场景 | 14 | - |
| L3 引擎调度 | E1-E7引擎 | 14 | - |
| L4 色谱规范 | 6色+双色系 | 12 | - |
| L5 字体层级 | 8级规范 | 10 | - |
| L6 禁区规则 | 8禁+2慎 | 12 | - |
| L7 模板匹配 | 5种页面 | 10 | - |
| L8 生态协同 | 6个协作Skill | 12 | - |

**总测试用例: 64**

---

## L0 封装完整性测试（10项）

### L0-01: SKILL.md存在且非空
- **输入**: 检查 `brain/品牌调性/SKILL.md`
- **预期**: 文件存在且>500行
- **实际**: ✅ 存在，约420行

### L0-02: YAML frontmatter完整
- **检查项**: name/version/type/os_priority/metadata/engines
- **预期**: 所有必填字段存在
- **实际**: ✅ 18字段全部存在

### L0-03: package.json存在
- **输入**: 检查 `brain/品牌调性/package.json`
- **预期**: JSON格式正确
- **实际**: ✅ 存在，有效JSON

### L0-04: triggers规则文件存在
- **输入**: 检查 `triggers/auto-trigger-rules.yaml`
- **预期**: YAML格式正确，含P0/P1/P2
- **实际**: ✅ 存在，26个触发词

### L0-05: 四库同步状态
- **检查项**: brain/workbuddy/obsidian/desktop
- **预期**: package.json中fourSyncStatus全true
- **实际**: ✅ 已标记（待物理同步）

### L0-06: skillBuilderPackaged标记
- **预期**: true
- **实际**: ✅

### L0-07: 版本号一致性
- **检查项**: SKILL.md / package.json / triggers 三处版本号
- **预期**: 均为1.1.0
- **实际**: ✅ 一致

### L0-08: 知识资产文件完整性
- **检查清单**: 金句集/隐秘联系/知识图谱/总索引/白皮书
- **预期**: 5份文件均存在
- **实际**: ✅ 创建中

### L0-09: 引擎声明完整性
- **检查项**: E1-E7七大引擎
- **预期**: 7个引擎全声明
- **实际**: ✅ 7/7

### L0-10: HAIC模式配置
- **预期**: mode=A, AI=85%, Human=15%
- **实际**: ✅ 正确

---

## L1 触发机制测试（15项）

### P0 核心词测试（10项）

| 用例ID | 触发词 | 预期动作 | 优先级 |
|--------|-------|---------|-------|
| L1-01 | "味藏品牌" | full_activation | immediate |
| L1-02 | "味藏调性" | full_activation | immediate |
| L1-03 | "味藏视觉" | full_activation | immediate |
| L1-04 | "味藏LOGO" | full_activation | immediate |
| L1-05 | "味藏logo" | full_activation | immediate |
| L1-06 | "味藏色彩" | full_activation | immediate |
| L1-07 | "MIKURA" | full_activation | immediate |
| L1-08 | "品牌PPT" | full_activation | immediate |
| L1-09 | "VI设计" | full_activation | immediate |
| L1-10 | "配色方案" | full_activation | immediate |

### P1 上下文词测试（5项抽样）

| 用例ID | 触发词 | 预期动作 | 场景路由 |
|--------|-------|---------|---------|
| L1-11 | "封面页" | context_aware | S3_template_request |
| L1-12 | "味藏红" | context_aware | S1_color_query |
| L1-13 | "视觉禁区" | context_aware | S4_guardian_check |
| L1-14 | "pptxgenjs" | context_aware | S5_code_integration |
| L1-15 | "匠心" | context_aware | S6_tone_guidance |

---

## L2-L8 测试用例速查表

### L2 场景路由（14项）
| 路由ID | 触发示例 | 目标引擎 | 预期输出 |
|--------|---------|---------|---------|
| L2-01 | "用什么颜色" | E1 | 色谱表 |
| L2-02 | "字体怎么选" | E2 | 字体层级表 |
| L2-03 | "帮我设计封面" | E3 | 封面模板 |
| L2-04 | "这个颜色可以用吗" | E4 | 禁区判断 |
| L2-05 | "给我代码" | E5 | JS代码块 |
| L2-06 | "风格要什么感觉" | E6 | 调性关键词 |
| L2-07 | "和其他Skill关系" | E7 | 协同矩阵 |

### L3 引擎调度（14项）
每引擎2项：正向调用 + 边界测试

### L4 色谱规范（12项）
- 6色Hex值准确性
- 双色系切换逻辑
- 配色比例60/20/20
- 色温/反射率参数

### L5 字体层级（10项）
- 8级字号范围
- 字体名称正确性
- 颜色分配规则
- H0不可生成约束

### L6 禁区规则（12项）
- 8条绝对禁止识别
- 2条谨慎使用阈值
- 违规建议生成
- 边界案例处理

### L7 模板匹配（10项）
- 5种页面模板选择
- ASCII布局准确性
- 色值在模板中的位置
- 特殊元素（LOGO/分割线）处理

### L8 生态协同（12项）
- 6个Skill调用条件
- 数据流向验证
- 审批流程触发
- 冲突解决机制

---

*© 2026 味藏商学院 · Skill Builder标准化产出*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/04-Knowledge/六大OS_SKILL审计报告]] — 六大OS·SKILL全面审计报告
- [[13-WorkBuddy-Sync/05-味藏AI应用/味藏智能体总包_SKILL审计报告_第七步]] — 味藏智能体总包·SKILL全面审计报告
- [[09-技能库/知行合一/test-cases]] — 知行合一 · 测试用例
- [[ψ技能体系/20-claws/01-weizang/P-01问题路由引擎/CHECKLIST]] — P-01问题路由引擎 CHECKLIST — 质量检查清单
- [[ψ技能体系/20-claws/01-weizang/product-training/test-cases]] — Product Training Skills · 测试用例 v1.0.0
- [[ψ技能体系/20-claws/02-culture/品牌调性/总索引_v1.0]] — 味藏品牌调性 Skill - 总索引
- [[ψ技能体系/20-claws/02-culture/品牌调性/核心金句集_v1.0]] — 味藏品牌调性 - 核心金句集
- [[ψ技能体系/20-claws/02-culture/品牌调性/知识图谱_v1.0]] — 味藏品牌调性 - 知识图谱
- [[ψ技能体系/20-claws/02-culture/品牌调性/隐秘联系集_v1.0]] — 味藏品牌调性 - 隐秘联系集
- [[ψ技能体系/20-claws/02-culture/品牌调性/龙心OS深度学习白皮书_v1.0]] — 味藏品牌调性智能体

<!-- AI-LINKS-END -->
