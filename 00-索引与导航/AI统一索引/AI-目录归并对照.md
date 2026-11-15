# 合并同类项 · 目录与重复内容对照

> 生成：2026-11-14 13:48:06　|　协议 `index-first-v1 + merge-v1`

## 一、判定结论

- 磁盘 md 17,017 篇；统一索引收录 **14,250** 篇；**真遗漏 0 篇**。
- 字节完全相同的重复 **33 组 / 38 份副本**：全部为技能包功能构件，物理删除会使技能包失效 → **只在索引层折叠，不物理归并**。
- 「同名异文 2,373 组」绝大多数是 `SKILL.md`(1,164) / `README.md`(228) / `test-cases.md`(133) 等技能包标准构件，分属不同技能、各有语义，**不是同一文章的多个版本**，无需取舍。
- 书稿 5 目录、AI 原生组织 4 目录等语义同类组，两两文件交集为 **0**：不是重复副本，合并只改善外观、不减少冗余，却需重算命名空间短码与全量双链 → **仅登记归属，不物理合并**。
- 根目录 21 篇散落 md 全部在索引内且各有入链，是**有意的根级导航层**，移入文件夹会断链 → 保留。

## 二、已执行的物理整理（B 档）

| 源目录 | 并入 | 移动文件 | 说明 |
|---|---|---|---|
| `19-系统配置` | `10-系统配置` | 6 | 消除上一轮编号消重留下的同名残留 |
| `22-工作记录与复盘` | `20-工作记录与复盘` | 107 | 消除上一轮编号消重留下的同名残留 |

- 同名异文冲突 1 处：`MEMORY备份.md` 字节不同，源侧加 `-来自22` 后缀，**两版零覆盖保留**。
- `scripts`（4 个脚本）、`微信公众号草稿库`（约 180 个草稿 HTML）含大量非 md 资产，**不是空目录，未移动**。
- 共 113 个文件迁移、873 处双链同步改写、369 个文件正文正向重建校验 PASS；逐字节备份与一键回滚见备份目录。

## 三、字节完全相同重复组（索引层折叠）

| 组 | 份数 | 主本 canonical | 副本 |
|---|---|---|---|
| DUP-001 | 2 | `08-龙心OS核心系统/AI-OS知识库/🧠 龙脑OS·知识地基层/L7理论基石/总索引.md` | `ψ技能体系/00-foundation/llm-wiki/llm-wiki-knowledge-base/architecture/layer1-raw/🧠 龙脑OS·知识地基层/L7理论基石/总索引.md` |
| DUP-002 | 2 | `09-技能库/ai-os/AI_OS_╫╘╢»╗»╩╣╙├╓╕─╧.md` | `ψ技能体系/99-archive/ai-os/AI_OS_╫╘╢»╗»╩╣╙├╓╕─╧.md` |
| DUP-003 | 2 | `09-技能库/ghost-scan-code/prompts/nominator.md` | `09-技能库/resources_nominator.md` |
| DUP-004 | 2 | `09-技能库/ghost-scan-code/prompts/planner.md` | `09-技能库/resources_planner.md` |
| DUP-005 | 2 | `09-技能库/ghost-scan-code/prompts/verifier.md` | `09-技能库/resources_verifier.md` |
| DUP-006 | 3 | `09-技能库/ima-skill/SKILL.md` | `09-技能库/ima-skills/ima-skill/SKILL.md`、`09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/SKILL.md` |
| DUP-007 | 5 | `09-技能库/ima-skill/knowledge-base/SKILL.md` | `09-技能库/ima-skills/ima-skill/knowledge-base/SKILL.md`、`09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/knowledge-base/SKILL.md`、`09-技能库/腾讯ima/knowledge-base/SKILL.md`、`ψ技能体系/00-foundation/ima/knowledge-base/SKILL.md` |
| DUP-008 | 3 | `09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/notes/SKILL.md` | `09-技能库/腾讯ima/notes/SKILL.md`、`ψ技能体系/00-foundation/ima/notes/SKILL.md` |
| DUP-009 | 2 | `09-技能库/resources_skill_creation_guide.md` | `09-技能库/self-learning/references/skill_creation_guide.md` |
| DUP-010 | 2 | `09-技能库/self-improving/SKILL.md` | `ψ技能体系/10-kernel/龙心OS/self-improving/SKILL.md` |
| DUP-011 | 2 | `09-技能库/web-search-plus/README.md` | `ψ技能体系/30-tools/web-search-plus/README.md` |
| DUP-012 | 2 | `09-技能库/workbuddy-obsidian-backup/README.md` | `ψ技能体系/40-rules/workbuddy-obsidian-backup/README.md` |
| DUP-013 | 2 | `09-技能库/知行合一自我进化/references/README.md` | `ψ技能体系/99-archive/知行合一自我进化/references/README.md` |
| DUP-014 | 2 | `09-技能库/腾讯ima/SKILL.md` | `ψ技能体系/00-foundation/ima/SKILL.md` |
| DUP-015 | 2 | `09-技能库/腾讯ima/knowledge-base/references/api.md` | `ψ技能体系/00-foundation/ima/knowledge-base/references/api.md` |
| DUP-016 | 2 | `09-技能库/腾讯文档/doc/doc_format/README.md` | `ψ技能体系/30-tools/腾讯文档/doc/README.md` |
| DUP-017 | 2 | `09-技能库/麦肯锡思考框架/01-逻辑思考/01-MECE原则/SKILL.md` | `ψ技能体系/10-kernel/龙脑OS/models/麦肯锡思考框架/01-逻辑思考/01-MECE原则/SKILL.md` |
| DUP-018 | 2 | `09-技能库/麦肯锡思考框架/01-逻辑思考/02-金字塔结构/SKILL.md` | `ψ技能体系/10-kernel/龙脑OS/models/麦肯锡思考框架/01-逻辑思考/02-金字塔结构/SKILL.md` |
| DUP-019 | 2 | `09-技能库/麦肯锡思考框架/01-逻辑思考/03-五色光思维/SKILL.md` | `ψ技能体系/10-kernel/龙脑OS/models/麦肯锡思考框架/01-逻辑思考/03-五色光思维/SKILL.md` |
| DUP-020 | 2 | `13-WorkBuddy-Sync/三向同步系统/README.md` | `ψ技能体系/00-foundation/三向同步系统/README.md` |
| DUP-021 | 2 | `13-WorkBuddy-Sync/三向同步系统/SKILL.md` | `ψ技能体系/00-foundation/三向同步系统/SKILL.md` |
| DUP-022 | 2 | `ψ技能体系/00-foundation/ima/notes/references/api.md` | `ψ技能体系/30-tools/ima-skill/notes/references/api.md` |
| DUP-023 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/化学平衡/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/化学平衡/SKILL.md` |
| DUP-024 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/失效模式/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/失效模式/SKILL.md` |
| DUP-025 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/奥卡姆剃刀/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/奥卡姆剃刀/SKILL.md` |
| DUP-026 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/子Skills/第一阶段-通用底层思维/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/子Skills/第一阶段-通用底层思维/SKILL.md` |
| DUP-027 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/帕累托法则/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/帕累托法则/SKILL.md` |
| DUP-028 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/控制论/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/控制论/SKILL.md` |
| DUP-029 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/易经错综复杂/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/易经错综复杂/SKILL.md` |
| DUP-030 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/氧化还原/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/氧化还原/SKILL.md` |
| DUP-031 | 2 | `ψ技能体系/10-kernel/龙脑OS/models/思维模型库/系统延迟/SKILL.md` | `ψ技能体系/30-tools/workbuddy/思维模型库/系统延迟/SKILL.md` |
| DUP-032 | 2 | `ψ技能体系/30-tools/PPT 演示文稿/SKILL.md` | `ψ技能体系/30-tools/pptx-generator/SKILL.md` |
| DUP-033 | 2 | `ψ技能体系/30-tools/summarize/SKILL.md` | `ψ技能体系/30-tools/内容总结/SKILL.md` |

## 四、语义同类目录组（仅登记归属，待裁决）

| 组 | 成员 | 索引内 md | 处置 |
|---|---|---|---|
| 书稿 / 专著 | 共生关系书稿、龙心OS顶层设计、龙心OS书稿、生生书稿、象与模书稿 | 150 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| AI 原生组织 | AI原生组织、AI原生组织思维模型、AI原生组织知识库、味藏AI原生组织 | 211 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| AIOS / 龙心OS 系统资料 | AI龙龟共生OS知识库、AIOS心跳巡检、龙心OS顶层设计、08-龙心OS核心系统 | 139 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| 技能体系 | 09-技能库、14-核心独创Skills、ψ技能体系、agents、skills、knowledge-base | 2,845 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| 研学 L3 | Raw原文、Wiki成书 | 106 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| 专项知识库 | 岗位智能体OS知识库、思维模型、AIOS心跳巡检 | 103 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |
| 运营与发布记录 | 周度汇报、微信公众号草稿库 | 1 | 仅登记主题归属，不物理合并（合并只改善外观，不减少冗余，却要重算命名空间短码） |

## 五、无编号遗留顶层目录

共 **23** 个，本轮保持原位；是否收编进编号体系需人工裁决。

`AIOS心跳巡检`、`AI原生组织`、`AI原生组织思维模型`、`AI原生组织知识库`、`AI龙龟共生OS知识库`、`Raw原文`、`Wiki成书`、`WorkBuddy知识备份体系`、`agents`、`knowledge-base`、`scripts`、`skills`、`ψ技能体系`、`共生关系书稿`、`周度汇报`、`味藏AI原生组织`、`岗位智能体OS知识库`、`微信公众号草稿库`、`思维模型`、`生生书稿`、`象与模书稿`、`龙心OS书稿`、`龙心OS顶层设计`

## 六、L5 归档层

- 归档 / 备份 / 存档快照 **2,722** 篇，清单见 `kb-archive.jsonl`。
- **默认不进常规检索**；需要时用 `kb-query.py archive <关键词>` 或 `--include-archive` 显式查询。
- 答案中必须标注「归档快照·非现行版本」；若有字节相同的现行笔记，返回 `current_twin` 指引。

## 七、AI 调用口径

1. 唯一入口仍是 `kb-query.py`；`search` / `resolve` 先经归并规则折叠重复副本。
2. `groups` 子命令返回本对照表的机器可读版本，按主题一次找全相关目录。
3. 常规检索不得把 L5 归档快照当现行依据；显式查询须标注版本性质。
4. 答案只能基于 `articles[].body` 与 `relation` 生成，不得引用未返回的文章。
