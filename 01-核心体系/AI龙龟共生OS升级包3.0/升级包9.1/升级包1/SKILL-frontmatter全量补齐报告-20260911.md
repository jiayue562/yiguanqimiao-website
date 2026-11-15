# SKILL frontmatter 全量补齐报告

> **工具抽象层·第三件。** 悟空发话「全量改」，本次把 `~/.workbuddy/skills` 下**全部 285 个活跃技能**补上接口声明。
> 权威源：Hello-Agents《从零开始构建智能体》Ch7（`Tool` / 参数自描述 / `ToolRegistry`）；规范：`Claw/SKILL接口规范.md`。

- 日期：2026-09-11 ｜ 执行：龙龟神将 ｜ 授权：悟空（全量）
- 迁移器：`Claw/_skill_frontmatter_migrate.py` ｜ 备份：`Claw/_skill_fm_backup_20260911/`（285 份改前原件）

---

## 一、一句话结论

**285 个技能的接口骨架，从 0% 到 100%；平均接口完整度 1.87 → 2.55 分；正文一个字节没动。**

翻成人话：AIOS 以前是 **285 件没贴标签的工具**，现在是 **285 件贴好标签、插孔槽位已经留出来的工具**——但插孔里还没接线（IO 语义待补）。

---

## 二、五道安全闸（改 285 个文件凭什么敢）

| 闸 | 措施 | 实测结果 |
|---|---|---|
| 1 | 只动 frontmatter 块，正文 md5 逐文件比对 | **285/285 正文未变** |
| 2 | 已有字段绝不覆盖（保留原顺序原值） | **0 覆盖**（DU-DS 等抽样确认 17 字段原样） |
| 3 | 幂等（重复执行结果一致） | 复跑 **需改动 0** |
| 4 | dry-run 默认，显式 `--apply` 才写盘 | 先 dry-run → 限量 5 → 全量 280 |
| 5 | 集中备份（保持相对路径，不污染技能目录） | `_skill_fm_backup_20260911/` **285 份** |

**另外加了一道验尸闸**：改完用**标准 YAML 解析器**全量校验，防 285 个技能集体加载失败——见第四节。

---

## 三、改前 / 改后对照（实测）

| 指标 | 改前 | 改后 |
|---|---|---|
| 活跃技能 | 284 | **285**（+1：本轮新建技能） |
| 无 frontmatter | 26 | **0** |
| 接口完整度均分 | **1.87 / 4** | **2.55 / 4** |
| 4 分（语义可编排） | **0** | **12** |
| 3 分（结构就位，IO 待填） | — | **133** |
| 2 分 | — | 140 |
| 接口骨架就位（有 inputs/outputs 键） | **0** | **285 / 285 = 100%** |
| IO 真值（可真正编排） | 0 | **24 / 285** |

**字段补齐明细**（本次实际补的）：

| 字段 | 补了 |
|---|---|
| `name` | 26 |
| `description` | 52 |
| `triggers` | 113 |
| `layer` | 280 |
| `inputs` / `outputs` | 285 / 285（结构骨架；其中 inputs 13、outputs 18 从正文提取到真值） |

> **诚实声明**：IO 语义（每个技能到底吃什么吐什么）**没有编造**。能从正文明确提取的才提（24 个技能）；提不到的写 `inputs:` + `# TODO 待补` 骨架，**绝不填假值**。所以均分只到 2.55 而不是 4.0——这是真实成绩，不是注水。

---

## 四、改完验尸：59 个原有 frontmatter 不合法（重要）

用标准 YAML 解析器校验，**59 个文件解析失败**。为确认不是本次改动造成，我把**改前备份**用同一把尺子量了一遍：

| | 校验数 | 不合法 | 无 frontmatter |
|---|---|---|---|
| 改**前**（备份原件） | 259 | **59** | 26 |
| 改**后**（现文件） | 285 | **59** | **0** |

**不合法数量一个没增加（59 = 59）**——证明：这 59 个**原本就坏**，不是本次改坏的。我的改动只做了两件事：无 frontmatter 26→0，不合法 59→59（不变）。

典型病灶（原文如此）：

```yaml
path: "C:\Users\jia'yue\.workbuddy\skills"   # \U 是 YAML 非法转义
title: "某技能"                                 # 后跟游离标量行
```

**处理建议**：这 59 个属**原有质量问题**，修复需逐个改正文（骨架级），**本次不动**，清单附于附录。

---

## 五、还剩什么没补（IO 语义待补清单）

按层统计「IO 真值覆盖率」——这就是下一步该干的活：

| 层 | 技能数 | IO 真值 | 覆盖率 |
|---|---|---|---|
| 通用工具 | 171 | 17 | 10% |
| 龙脑OS·刀库 | 46 | 0 | 0% |
| 书稿·五行人格心理学 | 25 | 1 | 4% |
| 味藏岗位 | 17 | 2 | 12% |
| 项目·书稿工作流 | 8 | 1 | 12% |
| 项目·小红书 | 7 | 1 | 14% |
| 灵魂层 | 4 | 0 | 0% |
| 工具·IMA | 3 | 0 | 0% |
| 基础层·foundation | 1 | 0 | 0% |
| 龙心OS | 1 | 0 | 0% |
| 龙爪OS | 1 | 1 | 100% |
| 龙脑OS | 1 | 1 | 100% |

**高价值优先补录建议**（按「第一次被编排」触发）：

1. **三 OS + 灵魂层（7 个）**——AIOS 主干，编排命脉，人工精补，约 1 个工作时段；
2. **味藏 17 岗**——岗位接口高度同构，可套一套模板批量补，约 1 个工作时段；
3. **龙脑OS·刀库 46 把刀**——刀刀都有「治什么」，接口同构（输入=问题，输出=结论），可半自动批量补；
4. 其余按需——**用哪个补哪个**，不再全量手改。

---

## 六、回滚方法（万一）

```powershell
# 整目录回滚
Copy-Item 'C:\Users\jia'yue\WorkBuddy\Claw\_skill_fm_backup_20260911\*' 'C:\Users\jia'yue\.workbuddy\skills\' -Recurse -Force
# 单文件回滚
Copy-Item '<备份>\<相对路径>\SKILL.md' '<skills>\<相对路径>\SKILL.md' -Force
```

备份为**改前原件**，覆盖即还原。

---

## 七、待悟空拍板

1. **59 个原有 YAML 不合法**是否要一并修？（骨架级，本次未动）
2. **IO 语义补录**从哪一层开始？（建议：三 OS + 灵魂层先，7 个）
3. 本次产物是否进六向同步？（报告含内部路径，按公开端纪律**不上网站/公众号**）

---

## 附录：59 个原有 frontmatter 不合法文件清单

| # | 文件 | 病灶 |
|---|---|---|
| 1 | `五行人格心理学/辅助Skills/03-记忆上下文/会话上下文管理/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-会话上下文管理 ^ expected <block en |
| 2 | `五行人格心理学/L3智能调度内核/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "L3智能调度内核.skills - 真正读懂意图 ... ^  |
| 3 | `五行人格心理学/辅助Skills/02-诊断评估/九层级别诊断/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-九层级别诊断 ^ expected <block end |
| 4 | `五行人格心理学/辅助Skills/01-路由调度/五行推断引擎/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-五行推断引擎 ^ expected <block end |
| 5 | `五行人格心理学/辅助Skills/02-诊断评估/人格测评问卷/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-人格测评问卷 ^ expected <block end |
| 6 | `五行人格心理学/辅助Skills/04-干预转化/化克为生方案库/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-化克为生方案库 ^ expected <block en |
| 7 | `五行人格心理学/辅助Skills/01-路由调度/场景分类器/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-场景分类器 ^ expected <block end> |
| 8 | `五行人格心理学/辅助Skills/01-路由调度/意图识别器/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-意图识别器 ^ expected <block end> |
| 9 | `五行人格心理学/辅助Skills/04-干预转化/拔阴取阳引导器/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-拔阴取阳引导器 ^ expected <block en |
| 10 | `五行人格心理学/辅助Skills/04-干预转化/每日修炼计划/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-每日修炼计划 ^ expected <block end |
| 11 | `五行人格心理学/辅助Skills/03-记忆上下文/用户画像存储/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-用户画像存储 ^ expected <block end |
| 12 | `五行人格心理学/辅助Skills/03-记忆上下文/进化追踪器/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-进化追踪器 ^ expected <block end> |
| 13 | `五行人格心理学/辅助Skills/02-诊断评估/阴阳状态检测/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格-阴阳状态检测 ^ expected <block end |
| 14 | `五行人格心理学/L6底座层/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格心理学L6底座层 ^ expected <block en |
| 15 | `五行人格心理学/底层知识体系/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格心理学底层知识体系 ^ expected <block e |
| 16 | `五行人格心理学/五行人格总智能体/土行人分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "土行人分智能体 SKILL.md" ^ expected <b |
| 17 | `五行人格心理学/五行人格总智能体/水行人分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "水行人分智能体 SKILL.md" ^ expected <b |
| 18 | `五行人格心理学/五行人格总智能体/火行人分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "火行人分智能体 SKILL.md - 鼓明照世的 ... ^  |
| 19 | `五行人格心理学/五行人格总智能体/金行人分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "金行人分智能体 SKILL.md" ^ expected <b |
| 20 | `五行人格心理学/L3调度层/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格心理学L3调度层 ^ expected <block en |
| 21 | `五行人格心理学/L4五行分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格心理学L4五行分智能体 ^ expected <block |
| 22 | `五行人格心理学/L5记忆层/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格心理学L5记忆层 ^ expected <block en |
| 23 | `五行人格心理学/五行人格总智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: 五行人格总智能体 ^ expected <block end>,  |
| 24 | `五行人格心理学OS/凤脑OS.skills/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "凤脑OS · 知识地基层" ^ expected <block |
| 25 | `Agent护照治理系统/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "Agent护照治理系统" ^ expected <block  |
| 26 | `L1·一心·统摄/SKILL.md` | while scanning a double-quoted scalar in "<unicode string>", line 2, column 7: path: "C:\Users\jia'yue\.workbu |
| 27 | `水行人分智能体/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: name: "💧 水行人分智能体" ^ expected <block end |
| 28 | `思维模型库/供需关系/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "供需关系模型" ^ expected <block end>, |
| 29 | `思维模型库/信号理论/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "信号理论模型" ^ expected <block end>, |
| 30 | `思维模型库/公地悲剧/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "公地悲剧模型" ^ expected <block end>, |
| 31 | `思维模型库/共生关系/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "共生关系" ^ expected <block end>, b |
| 32 | `思维模型库/冗余备份/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "冗余备份" ^ expected <block end>, b |
| 33 | `思维模型库/化学平衡/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "化学平衡" ^ expected <block end>, b |
| 34 | `思维模型库/反馈回路/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "反馈回路" ^ expected <block end>, b |
| 35 | `思维模型库/囚徒困境/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "囚徒困境模型" ^ expected <block end>, |
| 36 | `思维模型库/失效模式/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "失效模式" ^ expected <block end>, b |
| 37 | `思维模型库/奥卡姆剃刀/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "奥卡姆剃刀" ^ expected <block end>,  |
| 38 | `思维模型库/安全边际/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "安全边际" ^ expected <block end>, b |
| 39 | `思维模型库/帕累托法则/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "帕累托法则" ^ expected <block end>,  |
| 40 | `思维模型库/平台战略/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "平台战略模型" ^ expected <block end>, |
| 41 | `思维模型库/护城河理论/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "护城河理论模型" ^ expected <block end> |
| 42 | `思维模型库/控制论/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "控制论" ^ expected <block end>, bu |
| 43 | `思维模型库/最小可行种群/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "最小可行种群" ^ expected <block end>, |
| 44 | `思维模型库/机会成本/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "机会成本模型" ^ expected <block end>, |
| 45 | `思维模型库/比较优势/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "比较优势模型" ^ expected <block end>, |
| 46 | `思维模型库/氧化还原/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "氧化还原" ^ expected <block end>, b |
| 47 | `思维模型库/激励相容/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "激励相容模型" ^ expected <block end>, |
| 48 | `思维模型库/瓶颈理论/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "瓶颈理论" ^ expected <block end>, b |
| 49 | `思维模型库/竞争排斥/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "竞争排斥原理" ^ expected <block end>, |
| 50 | `思维模型库/系统延迟/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "系统延迟" ^ expected <block end>, b |
| 51 | `思维模型库/自催化/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "自催化" ^ expected <block end>, bu |
| 52 | `思维模型库/行为经济学/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "行为经济学模型" ^ expected <block end> |
| 53 | `思维模型库/规模效应/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "规模效应模型" ^ expected <block end>, |
| 54 | `思维模型库/路径依赖/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "路径依赖模型" ^ expected <block end>, |
| 55 | `思维模型库/边际效应/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "边际效应模型" ^ expected <block end>, |
| 56 | `思维模型库/遗传与变异/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "遗传与变异" ^ expected <block end>,  |
| 57 | `思维模型库/长尾理论/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "长尾理论模型" ^ expected <block end>, |
| 58 | `思维模型库/颠覆式创新/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: "颠覆式创新模型" ^ expected <block end> |
| 59 | `思维模型库/易经错综复杂/SKILL.md` | while parsing a block mapping in "<unicode string>", line 1, column 1: title: 易经错综复杂 · 卦变思维决策法 ^ expected <blo |

---

*本报告数据全部来自 `_skill_registry_build.py` / `_fm_validate.py` 实测输出，未做任何估算。*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI协作方法论/七向同步-通道实测与容量报告]] — 七向同步 · 通道实测与容量报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包7.1/载体效力审计报告-20260911]] — 载体效力审计报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/AIOS对照Hello-Agents审计报告-20260911]] — AIOS 对照《Hello-Agents》审计报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL-YAML修复与IO补录报告-20260911]] — SKILL YAML 修复与 IO 语义补录报告
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL接口规范]] — SKILL 接口规范 v1.0
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/SKILL注册表]] — AIOS 技能注册表（SKILL Registry）
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包1/记忆整合建议-2026-09-11]] — 记忆整合建议（只建议，不自动删）
- [[01-核心体系/AI龙龟共生OS升级包3.0/升级包9.1/升级包2/智能体接口层升级开发文档-味藏20人版-20260911]] — 智能体接口层升级开发文档（味藏 20 人版）

<!-- AI-LINKS-END -->
