# SKILL 接口规范 v1.0

> **工具抽象层·第二件。** 教程 Ch7 说：一个 `Tool` 要有统一 `run()`、要有 `get_parameters()` 自描述。AIOS 是规则级实装，没有 `run()`——那 AIOS 的"接口"长什么样？
> **答：写在 frontmatter 里。** 本规范把 Ch7 的 Tool 抽象翻译成 AIOS 规则级契约。
> 配套：`Claw/_skill_registry_build.py`（自动扫描）+ `Claw/SKILL注册表.md`（产物）。本规范**零侵入**——不改任何现有 SKILL，只规定"以后怎么长"与"旧的怎么补"。

- 版本：v1.1 ｜ 日期：2026-09-11（v1.1：§5 更新为「全量补齐已完成」）
- 权威源：Hello-Agents Ch7（`Tool`/`ToolParameter`/`ToolRegistry`）
- 落地原则：**翻译，不照搬**。不要 Python 类，要元数据契约。

---

## 一、为什么 AIOS 需要接口（不是好高骛远）

先看一组刚测出来的数字（`SKILL注册表.md`）：

| 指标 | 值 | 含义 |
|---|---|---|
| 活跃技能 | 284 | 东西不少 |
| 接口完整度均分 | **1.87 / 4** | 不到一半 |
| 四维全满（可编排） | **0 个** | 一个都没有 |
| 缺输入输出声明 | **284 / 284** | **100% 没有接口** |

翻译成人话：**AIOS 有 284 件工具，但没有一件贴了标签。** 想串两个技能完成任务，只能靠"我记得它俩能接"——这是记忆，不是接口；记忆会错，接口不会。

**代价**（可算的）：每次编排一个新流程，平均多花 3-5 分钟试错（试到能接上为止）；出错时无法定位是"技能选错了"还是"参数传错了"。接口建起来后，这两笔都省。

---

## 二、接口契约（frontmatter schema）

### 2.1 字段表

| 字段 | 必选 | 类型 | 说明 | 对应 Ch7 |
|---|---|---|---|---|
| `name` | ✅ | str | 唯一技能名 | `Tool.name` |
| `description` | ✅ | str | **一句话「治什么」**（可检索的主键） | `Tool.description` |
| `triggers` | ✅ | list | 何时该被调用（触发词/场景） | `get_parameters()` |
| `inputs` | ✅ | list | 输入参数（见 2.2） | `ToolParameter[]` |
| `outputs` | ✅ | list | 产出物 | `Tool.run()` 返回值 |
| `preconditions` | ⬜ | list | 前置条件 | — |
| `cost` | ⬜ | str | **可算代价**（时间/精力/风险） | — |
| `asserts` | ⬜ | list | 验证断言（怎么知道做对了） | — |
| `layer` | ⬜ | str | 所属层 | — |
| `version` | ⬜ | str | 版本 | — |
| `agent_created` | ⬜ | bool | 是否模型自建 | — |

> **AIOS 特色两字段**：`cost`（每条建议配可算代价——悟空语言风格硬校验）与 `asserts`（验证刀）。教程没有，AIOS 有。

### 2.2 inputs / outputs 的条目结构

```yaml
inputs:
  - name: 文档路径
    type: path          # path | text | list | json | url | file
    required: true
    desc: 待审计的权威源文件
    default: ""         # 可选
outputs:
  - name: 审计报告
    type: file
    path: 桌面（双盘）
    desc: md + docx
```

---

## 三、接口完整度分级（0-4 分）

扫描器按四维打分，**四维缺一即不算"可编排"**：

| 分 | 条件 | 状态 |
|---|---|---|
| **0** | 连 frontmatter 都没有 | ❌ 不可用 |
| **1** | 有名字 | ⚠️ 可被人找 |
| **2** | + 有「治什么」 | ⚠️ 可被人理解 |
| **3** | + 有触发条件 | ⚠️ 可被半自动调用 |
| **4** | + 有 inputs/outputs | ✅ **可被编排** |

当前 AIOS：**4 分 = 0 个**。这就是"从文档库到可编排系统"要跨的那道坎。

---

## 四、正例 / 反例

### 4.1 反例（现状，1-2 分）

```yaml
---
name: 某技能
description: 用于处理各类文档。
---
```
**病**：`description` 没有"治什么"（"各类文档"等于没说）；无 triggers（不知道啥时候用）；无 inputs/outputs（不知道怎么调）。

### 4.2 正例（4 分）

```yaml
---
name: 大文档对照审计
description: 拿一份外部权威源文档当尺子，给自身体系做对口体检，出五级分档审计报告。
triggers: [审计, 对照, 深入学习这份文档, 哪里需要升级]
layer: 通用工具
inputs:
  - name: 权威源文档
    type: path
    required: true
    desc: PDF/长教材/白皮书
  - name: 审计对象
    type: text
    required: true
    desc: 要体检的体系（如 AIOS / 某书稿）
outputs:
  - name: 审计报告
    type: file
    path: 桌面（双盘）
    desc: md + docx，含五级发现与落位
preconditions: [有权威源文件, 有明确的审计对象]
cost: 约 1-3 个工作时段（视文档体量）
asserts: [每条发现落到具体路径, 每条建议配可算代价]
version: 1.0
agent_created: true
---
```

对比：从"能被人读"升级到"能被另一段推理直接调用"。

---

## 五、迁移规则——**已执行全量补齐（2026-09-11，悟空发话）**

> **状态：第 1 步全量已完成。** 2026-09-11 悟空改判「全量改」，`Claw/_skill_frontmatter_migrate.py` 对 **285 个活跃技能**一次性补齐接口骨架。
> 结果：接口完整度 **1.87 → 2.55 分**，骨架就位 **0 → 285/285 = 100%**，正文**零字节改动**。
> 详见 `SKILL-frontmatter全量补齐报告-20260911.md`。

### 第 1 步｜全量补骨架 ✅ 已完成（2026-09-11）
- 补了 `name` 26 / `description` 52 / `triggers` 113 / `layer` 280 / `inputs`+`outputs` 285。
- **不发明**：IO 语义能从正文提取才提（24 个技能），提不到写 `inputs:` + `# TODO 待补`，绝不填假值。

### 第 2 步｜IO 语义按需补（进行中）
- 一个技能第一次被"编排"时，把它的 `inputs`/`outputs` 真值补上，替换 TODO 骨架。
- 优先序建议：三 OS + 灵魂层（7）→ 味藏 17 岗（可套模板）→ 龙脑刀库 46（同构）。
- 记录在注册表里，下次扫描自动吸收。

### 第 3 步｜新技能强制（从今天起）
- 新建 SKILL 一律按本规范写 frontmatter（四维必满）。

### 补法（安全模式，已固化）
- 补 frontmatter 属**改动 SKILL 正文**（骨架级，须悟空发话）——本次已获授权。
- **五道安全闸**（已实测）：①只动 fm 块、正文 md5 校验 ②已有字段不覆盖 ③幂等 ④dry-run 默认 ⑤集中备份 `_skill_fm_backup_20260911/`。
- 改完**必过标准 YAML 校验**（`_fm_validate.py`）——防技能集体加载失败。

---

## 六、编排规则（接口建好之后怎么用）

接口的目的不是"填表"，是**能串**。串的方法写进载具（见龙爪OS 增补节）：

1. **选**：按「治什么」查注册表 → 命中技能（不按名字）
2. **串**：上游 `outputs` 喂给下游 `inputs`（变量传递，对应 Ch7 `ToolChain.output_key`）
3. **验**：每个技能的 `asserts` 逐条过；`cost` 累计，超预算先停下问悟空

### 一个串起来的例子

```
「大文档对照审计」                       「SKILL 接口规范」
  inputs:  权威源文档 ──────────────┐
  outputs: 审计报告(五级发现) ───────┤
                                    ↓
                              inputs: 待改造的技能清单
                              outputs: 改造方案
```
两件工具，靠 `outputs→inputs` 咬着，就是一条流水线。**没有接口，这条线只能靠"我记得"。**

---

## 七、边界（不做什么）

- **不做代码级 `ToolRegistry`**：AIOS 是规则级，注册表是**文件**不是**类**。
- **不引入 `ToolChain` 代码**：链式调用用"编排规则 + 变量传递"实现，不写 Python 调度器（关联 GAP-01，不在本轮）。
- **全量补录已完成**（2026-09-11 悟空授权，五道安全闸 + 标准 YAML 复验）；后续 IO 语义**按需补**，不再全量手改。
- **不改 AIOS 自有术语**：仍叫"技能/刀/载具"，`interface` 只作技术注脚。

---

*本规范与 `SKILL注册表.md`、`_skill_registry_build.py`、`_skill_frontmatter_migrate.py`、`_fm_validate.py` 配套。全量骨架补齐已于 2026-09-11 完成（285 个活跃技能）。*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包7.1/载体效力审计报告-20260911]] — 载体效力审计报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/AIOS对照Hello-Agents审计报告-20260911]] — AIOS 对照《Hello-Agents》审计报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL-YAML修复与IO补录报告-20260911]] — SKILL YAML 修复与 IO 语义补录报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL-frontmatter全量补齐报告-20260911]] — SKILL frontmatter 全量补齐报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL注册表]] — AIOS 技能注册表（SKILL Registry）
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/记忆整合建议-2026-09-11]] — 记忆整合建议（只建议，不自动删）
- [[07-得到大脑同步/AI 原生组织/AIO-001-AWS 108页报告拆解：AI 从“用过”到“赚到”，中间卡着十道断点]] — AWS 108页报告拆解：AI 从“用过”到“赚到”，中间卡着十道断点
- [[ψ技能体系/30-tools/fbs-bookwriter/references/01-core/section-4-commands]] — 短指令完整清单（§4 扩展版）
- [[ψ技能体系/30-tools/fbs-bookwriter/references/bibliography]] — 参考文献索引（MAT 编号系统）
- [[ψ技能体系/30-tools/knowledge-framework-builder/references/output-schema]] — output-schema.md —— 知识框架梳理 Skill 输出数据契约

<!-- AI-LINKS-END -->
