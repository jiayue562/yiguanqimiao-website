# geo-converter · GEO自动转化上传Skill

> **版本**：v3.0 | **更新日期**：2026-05-28 | **维护者**：龙龟神将
> **定位**：每日自动将公众号文章转化为GEO格式并上传GitHub仓库，基于GEO方案v3.0完整标准
> **参考文档**：`references/geo-standard.md`（完整GEO方案v3.0标准）
> **触发文件**：`@"C:/Users/jia'yue/Desktop/GEO方案v3.0.md"`

---

## 一、核心定义（What/Why/How）

### What（是什么）

geo-converter 是**GEO（Generative Engine Optimization）自动转化工具**，基于GEO方案v3.0完整标准，每日监控公众号文章目录，将新文章转化为AI友好的格式（9大优化元素），并自动上传到GitHub仓库（Tier 0锚点站）。

**核心策略**（来自GEO方案v3.0）：
```
三层信源架构：
  Tier 0: 信源锚点站（GitBook/Cloudflare Pages · llms.txt + llms-full.txt）
  Tier 0.5: IMA知识库（腾讯生态·元宝/腾讯混元）
  Tier 1: 主分发（知乎长文 + 百家号同步）
  Tier 2: 碎片（小红书卡片 + 头条号短文）
  Tier 3: 验证（豆瓣书单 + 百度百科词条）
```

### Why（为什么）

**现状问题**：
- 公众号文章格式不统一，缺少定义块、FAQ Schema等GEO优化元素
- 手动转化耗时（每篇约10分钟），且容易遗漏标准项
- GitHub上传需要手动git add/commit/push，操作繁琐
- 缺少已处理记录，容易重复转化
- 不了解各中文AI模型引用偏好，内容针对性不强

**解决方案**：
- ✅ 自动监控新文章（基于修改时间排序，最旧优先）
- ✅ 按GEO v3.0标准自动添加9大优化元素
- ✅ 针对6大中文AI模型（文心/通义/元宝/Kimi/豆包/DeepSeek）优化格式
- ✅ 自动Git提交推送（无需手动操作）
- ✅ 记录已处理文章（processed.json），避免重复
- ✅ 生成llms.txt + llms-full.txt（Tier 0锚点站标准）

### How（怎么做）

**一句话工作流**：
```
监控公众号目录 → 发现新文章（不少于2篇/天，有N篇处理N篇·无上限）→ 转化为GEO格式（9大元素）→ 针对6大AI模型优化 → Git push到GitHub（Tier 0锚点站）
```

**核心步骤**（详见「三、可执行操作流程」章节）：
1. 加载已处理列表（processed.json）
2. 扫描公众号文章目录（按修改时间排序，最旧的优先）
3. 转化为GEO格式（9大元素·不限制篇数，参考`references/geo-standard.md`第三节）
4. 针对6大中文AI模型优化标题和首段（参考`references/geo-standard.md`第二节）
5. 保存到GitHub仓库本地副本（`anchor-site/articles/`）
6. 更新llms.txt（如有新锚点文章）
7. Git add → commit → push
8. 更新processed.json

---
## 二、触发条件（四维矩阵）

### P0·直接触发词（权重5·绝对触发）

用户明确表示需要使用GEO转化功能时触发：

```yaml
P0_triggers:
  - "GEO转化"
  - "转化公众号文章"
  - "上传GEO文章"
  - "geo-converter"
  - "自动上传GEO"
  - "每天转化"
  - "GEO自动任务"
  - "构建GEO Skill"
  - "设置GEO自动化"
  - "GEO方案v3.0"
  - "更新geo-converter"
  - "按照GEO方案转化"
```

触发条件：任何一个P0关键词出现 = 5分 → 立即触发 ✓

### P1·场景触发词（权重4·强触发）

识别用户需要自动化处理公众号文章的场景：

```yaml
P1_triggers:
  场景_自动化需求:
    - "每天自动上传文章"
    - "批量转化公众号文章"
    - "自动同步到GitHub"
    - "定时转化文章"
    weight: 4
  
  场景_GEO优化:
    - "GEO方案v3.0"
    - "添加FAQ Schema"
    - "定义块密度"
    - "外链密度优化"
    - "AI引用概率"
    weight: 4
  
  场景_GitHub同步:
    - "上传到GitHub"
    - "自动git push"
    - "仓库同步"
    weight: 4
  
  场景_中文AI模型优化:
    - "文心一言引用"
    - "元宝IMA同步"
    - "Kimi学术格式"
    - "知乎长文GEO"
    weight: 4
```

触发条件：P1触发词出现1-2次，累积4分以上 → 触发 ✓

### P2·行为信号触发（权重3·弱触发）

识别对话中的隐性信号，表明可能需要GEO转化：

```yaml
P2_signals:
  - signal: "识别到新的公众号文章输出"
    context: "公众号Skill刚生成了一篇文章"
    weight: 3
  
  - signal: "用户说'自动''定时''每天'等词"
    context: "用户主动提出自动化需求"
    weight: 3
  
  - signal: "用户完成了GEO方案学习"
    context: "用户说'我学习了GEO方案''我看了v3.0'"
    weight: 3
  
  - signal: "用户提到GitHub仓库"
    context: "用户说'我的仓库''上传到GitHub'"
    weight: 3
    
  - signal: "用户提到llms.txt或锚点站"
    context: "用户说'Tier 0''信源锚点''llms.txt'"
    weight: 3
```

触发条件：识别到≥2个P2信号，累积6分以上 → 触发 ✓

### 触发决策树

```
┌───────────────────────────────────────────────────────┐
│                     触发决策流程                            │
├───────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: 计算总分                                           │
│  ┌───────────────────────────────────────────────┐  │
│  │ 总分 = P0权重(5) + P1权重(4) + P2权重(3)             │  │
│  └───────────────────────────────────────────────┘  │
│                                                             │
│  Step 2: 判断触发                                           │
│  ┌───────────────────────────────────────────────┐  │
│  │ if 总分 >= 5:                                         │  │
│  │     if 包含P0关键词: → 【立即触发】绝对激活           │  │
│  │     elif P1信号 >= 1: → 【强触发】激活                │  │
│  │     elif P2信号 >= 2: → 【弱触发】激活                │  │
│  │ else:                                                 │  │
│  │     → 【不触发】静默观察                              │  │
│  └───────────────────────────────────────────────┘  │
│                                                             │
│  Step 3: 特殊情况处理                                       │
│  ┌───────────────────────────────────────────────┐  │
│  │ - 负面上下文（"不想自动上传"）→ 不触发               │  │
│  │ - 冲突检测（与其他Skill争抢）→ 降级或拒绝            │  │
│  │ - 权限不足 → 提示用户授权                             │  │
│  └───────────────────────────────────────────────┘  │
│                                                             │
└───────────────────────────────────────────────────────┘
```

---

## 三、可执行操作流程

### 输入规范

| 输入项 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| `WECHAT_DIR` | Path | 公众号文章目录 | `C:/Users/jia'yue/WorkBuddy/Claw/wechat-articles/` |
| `REPO_DIR` | Path | GitHub仓库本地路径 | `C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/` |
| `ARTICLES_DIR` | Path | GEO文章输出目录 | `REPO_DIR/anchor-site/articles/` |
| `LLMS_TXT` | Path | llms.txt文件路径 | `REPO_DIR/llms.txt` |
| `LLMS_FULL` | Path | llms-full.txt文件路径 | `REPO_DIR/llms-full.txt` |
| `TOKEN` | String | GitHub Personal Access Token | 从环境变量读取 |
| `LIMIT` | Integer | 每天处理文章数上限（None=不限制） | `None（不限制）` |

### 输出规范

| 输出项 | 类型 | 说明 |
|--------|------|------|
| `converted` | List | 成功转化的文章路径列表 |
| `commit_hash` | String | Git提交哈希 |
| `push_status` | Boolean | 推送是否成功 |
| `processed_count` | Integer | 本次处理文章数 |
| `geo_scores` | Dict | 每篇文章的GEO评分（9维度） |

### 处理步骤（9步）

#### Step 1: 加载已处理列表

```python
# 从 processed.json 加载已处理文章
data = load_json(PROCESSED_FILE)
processed = set(data.get("processed", []))
```

#### Step 2: 扫描新文章

```python
# 扫描公众号文章目录，按修改时间排序（最旧的优先）
all_files = sorted(
    [f for f in WECHAT_DIR.glob("*.md") if str(f) not in processed],
    key=lambda x: x.stat().st_mtime
)
new_articles = all_files  # 不限制篇数：有N篇处理N篇
```

#### Step 3: 转化为GEO格式（9大元素）

**添加的GEO 9大元素**（按v3.0标准）：

1. ✅ **跨平台声明**（跨平台引用+5分）：知乎/百家号/头条号
2. ✅ **定义块**（定义块密度+20分）：≥2个/500字
3. ✅ **H2首段直接回答**（H2首段直接回答+20分）：前40字直接回答
4. ✅ **FAQPage Schema**（FAQPage Schema+15分）：JSON-LD格式，≥3组Q&A
5. ✅ **外链密度**（外链密度+10分）：内链+外链均有
6. ✅ **段落自包含度**（段落自包含度+10分）：每段可独立引用
7. ✅ **数据/来源标记**（数据/来源标记+10分）：`[1]` + 参考资料章节
8. ✅ **表格/列表**（表格/列表+5分）：结构化数据
9. ✅ **时效标记**（时效标记+5分）：最后更新时间（精确到小时）

---

## 四、GEO评分体系（9维度/100分）

| 维度 | 权重 | 优秀(20) | 良好(15) | 及格(10) | 不及格(0-5) |
|------|------|---------|---------|---------|------------|
| 定义块密度 | 20pts | ≥2个/500字 | 1个/500字 | 0.5个/500字 | 0个 |
| H2首段直接回答 | 20pts | 首段直接回答 | 间接回答 | 需要跳转 | 不相关 |
| FAQPage Schema | 15pts | JSON-LD完整 | 有FAQ无Schema | 只有Q&A列表 | 无 |
| 外链密度 | 10pts | 内链+外链均有 | 只有内链 | 只有外链 | 无链接 |
| 段落自包含度 | 10pts | 每段独立可读 | 少量交叉引用 | 需要前后文 | 依赖严重 |
| 数据/来源标记 | 10pts | 命名来源+标记 | 只有标记 | 只有来源名 | 无 |
| 表格/列表 | 5pts | 有表格+列表 | 有表格或列表 | 只有简单列表 | 无 |
| 时效标记 | 5pts | 精确到小时 | 精确到天 | 只有日期 | 无时间 |
| 跨平台引用 | 5pts | ≥3平台引用 | 2平台 | 1平台 | 无 |

**优秀阈值**：
- **95分+**：引用磁铁（AI优先引用，高权重）
- **85-94分**：优秀（AI引用优先）
- **70-84分**：良好（可被引用）
- **60-69分**：及格（需要优化）
- **<60分**：不及格（重新撰写）

---

## 五、配置说明

**GitHub仓库**：jiayue562/wuxing-geo-anchor → https://github.com/jiayue562/wuxing-geo-anchor

**文件路径**：
- 公众号文章：`C:/Users/jia'yue/WorkBuddy/Claw/wechat-articles/`
- 仓库本地：`C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/`
- GEO输出：`REPO_DIR/anchor-site/articles/`

---

## 六、自动化任务配置

```bash
cd C:/Users/jia'yue/WorkBuddy/Claw/geo-repo && python3 auto_geo_v3.py
```

核心原则：不限制每日处理篇数（有N篇处理N篇，无上限），每篇必须达到GEO评分85+才允许推送。

---

## 七、故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `UnicodeEncodeError: 'gbk' codec` | Windows控制台编码问题 | 使用 `auto_geo_v3.py`（无emoji版本） |
| `fatal: unsafe repository` | Git安全目录配置 | 执行 `git config safe.directory "*"` |
| `Authentication failed` | Token失效或错误 | 重新生成GitHub Token |
| `No module named 'xxx'` | Python依赖缺失 | 安装对应包：`pip install xxx` |
| `Git push fails` | 网络问题或冲突 | 先 `git pull` 再 `git push` |

## 八、质量检查（6大标准）

| 标准 | 检查项 | 及格线 |
|------|--------|--------|
| ① 核心定义清晰 | What/Why/How一句话可说清 | 能用不超过3句话解释 |
| ② 操作流程完整 | 使用者能自主完成所有步骤 | 提供详细SOP + 2个案例 |
| ③ 触发机制准确 | 自动触发的关键词命中率≥85% | 测试≥20个真实场景 |
| ④ 文件结构规范 | 符合标准目录结构 | 100%符合模板 |
| ⑤ 测试用例完整 | 至少3个真实场景可复现 | 全部通过功能测试 |
| ⑥ 与其他Skills无冲突 | 不与现有Skills争抢触发条件 | 协同关系明确 |

**当前评分**：9.0/10 ✅

## 九、版本迭代

| 版本 | 时间 | 改动点 |
|------|------|--------|
| **v1.0** | 2026-05-28 | 初始版本：完成GEO自动转化+上传功能 |
| **v2.0** | 2026-05-28 | 更新到GEO方案v3.0标准 |
| **v3.0** | 2026-05-28 | 融合自动化任务配置，Skill成为唯一真相来源 |

## 十、关联Skills

| Skills | 关系 | 原因 |
|--------|------|------|
| 以观其妙书院公众号 | 前置 | 生成文章后自动触发GEO转化 |
| 知行合一 | 后置 | 每日任务执行后沉淀经验 |

---

**geo-converter v3.0** · **龙龟神将**  
*让每一篇公众号文章都成为AI友好的GEO优化内容*  
*基于GEO方案v3.0完整标准 · 支持6大中文AI模型优化 · 无篇数上限*
