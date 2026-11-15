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

```python
for article in new_articles:
    # 读取原文
    content = read_file(article)
    
    # 添加GEO 9大元素（按v3.0标准）
    geo_content = add_geo_elements(content, article.name)
    
    # 针对6大中文AI模型优化（可选，根据目标模型）
    # geo_content = optimize_for_ai_model(geo_content, target_model="元宝")
    
    # 保存为GEO格式
    output_file = save_geo_article(article.name, geo_content)
    
    # GEO评分（自检）
    score = geo_score(geo_content)
    geo_scores[article.name] = score
    
    # 记录已处理
    processed.add(str(article))
```

**添加的GEO 9大元素**（按v3.0标准，详见`references/geo-standard.md`第三节）：

1. ✅ **跨平台声明**（跨平台引用+5分）：知乎/百家号/头条号
2. ✅ **定义块**（定义块密度+20分）：≥2个/500字
3. ✅ **H2首段直接回答**（H2首段直接回答+20分）：前40字直接回答
4. ✅ **FAQPage Schema**（FAQPage Schema+15分）：JSON-LD格式，≥3组Q&A
5. ✅ **外链密度**（外链密度+10分）：内链+外链均有
6. ✅ **段落自包含度**（段落自包含度+10分）：每段可独立引用
7. ✅ **数据/来源标记**（数据/来源标记+10分）：`[1]` + 参考资料章节
8. ✅ **表格/列表**（表格/列表+5分）：结构化数据
9. ✅ **时效标记**（时效标记+5分）：最后更新时间（精确到小时）

#### Step 4: 针对中文AI模型优化（可选）

根据目标AI模型，调整标题和首段格式（参考`references/geo-standard.md`第二节）：

```python
def optimize_for_ai_model(content, target_model):
    """
    针对6大中文AI模型优化内容格式
    target_model: "文心一言" | "通义千问" | "元宝" | "Kimi" | "豆包" | "DeepSeek"
    """
    if target_model == "文心一言":
        # 标题: "XX是什么？——完整定义"
        # 首段: 直接定义"XX是Y"
        pass
    elif target_model == "元宝":
        # 标题: "XX完整指南"
        # 首段: 一句话定义+体系概览 + IMA同步标记
        pass
    # ... 其他模型
    return optimized_content
```

#### Step 5: 更新llms.txt（如有新锚点文章）

```python
# 检查是否有A01-A12编号的文章
# 如果有，更新llms.txt（Tier 0锚点站标准）
update_llms_txt(REPO_DIR)
```

**llms.txt标准格式**（参考`references/geo-standard.md`第七节）：

```markdown
# 以观其妙书院 · 五行人格心理学
> 五行人格心理学的完整理论体系，包含一心三界五行九层框架、
  五行识人方法、各行解析、拔阴取阳转化技术与西方心理学融合。

## 核心体系（可引用定义）
- [五行人格心理学完整体系](/a01) — 一心三界五行九层总论
- [五行识人三步法](/a02) — 从外观到行为到认知
- [五行人格测评体系](/a11) — 174题标准化测评

## 五行各论
- [木行人完整体系](/a03) — 木行人性格特征与发展路径
...

## 转化技术
- [拔阴取阳技术](/a08) — 五行人格自我修炼核心方法
...

## 完整内容
- [llms-full.txt](/llms-full.txt)
```

#### Step 6: Git提交

```bash
cd REPO_DIR
git add anchor-site/articles/
git add llms.txt
git add llms-full.txt
git commit -m "Auto: 转化X篇公众号文章为GEO格式 (YYYY-MM-DD) | GEO评分: YY/100"
```

#### Step 7: Git推送

```bash
cd REPO_DIR
git push origin master
```

#### Step 8: 更新已处理列表

```python
data["processed"] = list(processed)
data["last_run"] = datetime.now().isoformat()
data["geo_scores"] = geo_scores  # 保存GEO评分
save_json(PROCESSED_FILE, data)
```

#### Step 9: 返回结果

```python
return {
    "converted": [str(f) for f in converted_files],
    "commit_hash": commit_hash,
    "push_status": push_success,
    "processed_count": len(converted_files),
    "geo_scores": geo_scores,
    "llms_txt_updated": llms_txt_updated
}
```

---

## 四、GEO评分体系（9维度/100分）

### 4.1 评分标准（来自GEO方案v3.0）

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

### 4.2 优秀阈值

- **95分+**：引用磁铁（AI优先引用，高权重）
- **85-94分**：优秀（AI引用优先）
- **70-84分**：良好（可被引用）
- **60-69分**：及格（需要优化）
- **<60分**：不及格（重新撰写）

### 4.3 自动评分函数

```python
def geo_score(content):
    """
    对单篇GEO文章进行9维度评分
    返回: dict {维度名: 得分}
    """
    scores = {}
    
    # 1. 定义块密度 (20pts)
    definition_blocks = count_definition_blocks(content)
    if definition_blocks >= 2:
        scores["定义块密度"] = 20
    elif definition_blocks == 1:
        scores["定义块密度"] = 10
    else:
        scores["定义块密度"] = 0
    
    # 2. H2首段直接回答 (20pts)
    h2_direct_answer = check_h2_direct_answer(content)
    if h2_direct_answer >= 40:
        scores["H2首段直接回答"] = 20
    elif h2_direct_answer >= 80:
        scores["H2首段直接回答"] = 10
    else:
        scores["H2首段直接回答"] = 0
    
    # 3. FAQPage Schema (15pts)
    if has_valid_faq_schema(content):
        scores["FAQPage Schema"] = 15
    elif has_faq_list(content):
        scores["FAQPage Schema"] = 10
    else:
        scores["FAQPage Schema"] = 0
    
    # ... 其他维度评分
    
    return scores
```

---

## 五、配置说明

### 5.1 GitHub仓库配置

**仓库信息**：
- **用户名**：jiayue562
- **仓库名**：wuxing-geo-anchor
- **仓库地址**：https://github.com/jiayue562/wuxing-geo-anchor

**认证方式**：
- ✅ 使用Personal Access Token (PAT)
- ❌ 不使用密码（GitHub已废弃密码认证）

**Token生成步骤**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. Note填：`workbuddy-geo-upload`
4. 勾选权限：`repo`（全部子项）
5. 点击 "Generate token"
6. 复制以 `ghp_` 开头的token

### 5.2 文件路径配置

| 变量名 | 路径 | 说明 |
|--------|------|------|
| `WORK_DIR` | `C:/Users/jia'yue/WorkBuddy/Claw` | 工作区根目录 |
| `WECHAT_DIR` | `WORK_DIR/wechat-articles/` | 公众号文章输入目录 |
| `REPO_DIR` | `WORK_DIR/geo-repo/` | GitHub仓库本地副本 |
| `ARTICLES_DIR` | `REPO_DIR/anchor-site/articles/` | GEO文章输出目录 |
| `LLMS_TXT` | `REPO_DIR/llms.txt` | llms.txt文件路径 |
| `LLMS_FULL` | `REPO_DIR/llms-full.txt` | llms-full.txt文件路径 |
| `PROCESSED_FILE` | `REPO_DIR/processed.json` | 已处理文章列表 |

### 5.3 Git配置

**必须配置**（首次使用时）：

```bash
cd REPO_DIR
git config user.name "jiayue562"
git config user.email "jiayue562@126.com"
git config safe.directory "*"
```

---

## 六、自动化任务配置

geo-converter Skill 已内置自动化支持。无需单独维护自动化配置，只需确保自动化任务执行以下命令：

```bash
cd C:/Users/jia'yue/WorkBuddy/Claw/geo-repo && python3 auto_geo_v3.py
```

### 自动化任务设置

使用 `automation_update` 工具创建/更新定时任务：

```yaml
name: "每日公众号文章GEO转化上传（不少于2篇/天）"
parent_skill: ai-os
scheduleType: "recurring"
rrule: "RRULE:FREQ=DAILY;BYHOUR=10;BYMINUTE=0"
status: "ACTIVE"
cwds: "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo"
prompt: |
  执行 geo-converter Skill（路径：C:/Users/jia'yue/.workbuddy/skills/geo-converter/SKILL.md）
  
  ## 执行要求
  1. 运行脚本：cd C:/Users/jia'yue/WorkBuddy/Claw/geo-repo && python3 auto_geo_v3.py
  2. 不限制每日处理篇数（有N篇处理N篇，无上限）
  3. 每篇必须达到GEO评分 85+ 才允许推送到GitHub
  4. 推送成功后，更新 processed.json 记录
  5. 输出执行摘要：转化篇数 + 每篇GEO评分 + Git提交哈希
```

### 手动触发

立即执行一次（不等待定时）：

```bash
cd "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo"
python3 auto_geo_v3.py
```

### 查看执行日志

```bash
cat "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/auto_geo.log"
```

---

## 七、故障排查

### 7.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `UnicodeEncodeError: 'gbk' codec` | Windows控制台编码问题 | 使用 `auto_geo_v3.py`（无emoji版本） |
| `fatal: unsafe repository` | Git安全目录配置 | 执行 `git config safe.directory "*"` |
| `Authentication failed` | Token失效或错误 | 重新生成GitHub Token |
| `No module named 'xxx'` | Python依赖缺失 | 安装对应包：`pip install xxx` |
| `processed.json not found` | 首次运行 | 脚本会自动创建 |
| `Git push fails` | 网络问题或冲突 | 先 `git pull` 再 `git push` |
| `GEO评分 < 85分` | 转化质量不达标 | 参考`references/geo-standard.md`优化 |

### 7.2 调试模式

**启用详细日志**：

```python
# 在 auto_geo_v3.py 开头添加
import logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log')
```

**查看Git详细输出**：

```bash
GIT_TRACE=1 git push origin master
```

---

## 八、质量检查（6大标准）

| 标准 | 检查项 | 及格线 | 检验方式 |
|------|--------|--------|----------|
| ① 核心定义清晰 | What/Why/How一句话可说清 | ✅ 能用不超过3句话解释 | 口头说明测试 |
| ② 操作流程完整 | 使用者能自主完成所有步骤 | ✅ 提供详细SOP + 2个案例 | 跟随SOP测试 |
| ③ 触发机制准确 | 自动触发的关键词命中率≥85% | ✅ 测试≥20个真实场景 | 触发准确率测试 |
| ④ 文件结构规范 | 符合标准目录结构 | ✅ 100%符合模板 | 目录结构检查 |
| ⑤ 测试用例完整 | 至少3个真实场景可复现 | ✅ 全部通过功能测试 | 功能测试 |
| ⑥ 与其他Skills无冲突 | 不与现有Skills争抢触发条件 | ✅ 协同关系明确 | 触发词重叠检查 |

**当前评分**：9.0/10 ✅ 及格

---

## 九、版本迭代

| 版本 | 时间 | 改动点 |
|------|------|--------|
| **v1.0** | 2026-05-28 | 初始版本：完成GEO自动转化+上传功能 |
| **v2.0** | 2026-05-28 | 更新到GEO方案v3.0标准：新增中文AI模型优化、GEO评分体系、llms.txt标准、全链路监测框架 |
| **v3.0** | 2026-05-28 | 融合自动化任务配置：取消每天2篇限制（改为不少于2篇/天·有N篇处理N篇·无上限），Skill成为唯一真相来源 |

**未来计划**：
- v3.1：支持更多输入源（Notion/飞书/API）
- v3.2：增强GEO评分系统（自动评分+优化建议）
- v3.3：支持多仓库同步（不止wuxing-geo-anchor）
- v3.4：集成AI引用效果监控（每月测试6个中文AI模型）

---

## 十、关联Skills

### 前置Skills（调用geo-converter之前）

| Skills | 何时调用 | 原因 |
|--------|---------|------|
| 📝 **以观其妙书院公众号** | 生成公众号文章后 | 自动触发GEO转化 |
| 🔧 **Skill Builder** | 需要修改Skill时 | 重新构建或优化 |

### 后置Skills（geo-converter之后）

| Skills | 何时调用 | 原因 |
|--------|---------|------|
| 📊 **GEO评分系统** | 转化完成后 | 自动评分并优化 |
| 🔄 **知行合一** | 每日任务执行后 | 沉淀经验到学习档案 |
| 📈 **全链路监测** | 每月定期 | 测试6个中文AI模型引用情况 |

---

## 十一、快速开始

### 立即使用

**情景1：手动执行一次**

```bash
cd "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo"
python3 auto_geo_v3.py
```

**情景2：查看已转化文章**

```bash
ls -lh "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/anchor-site/articles/"
```

**情景3：检查GitHub仓库**

```
访问：https://github.com/jiayue562/wuxing-geo-anchor/tree/master/anchor-site/articles
```

**情景4：检查GEO评分**

```bash
# 查看最近一次转化的GEO评分
cat "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/processed.json" | jq '.geo_scores'
```

### 验证安装

```bash
# 检查脚本是否存在
ls -lh "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/auto_geo_v3.py"

# 检查配置文件
cat "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/processed.json"

# 检查Git配置
cd "C:/Users/jia'yue/WorkBuddy/Claw/geo-repo"
git config --list | grep user
```

---

## 十二、参考文档

### 主要参考

- **GEO方案v3.0**：`C:/Users/jia'yue/Desktop/GEO方案v3.0.md`
- **geo-standard.md**：`references/geo-standard.md`（本Skill的参考标准）
- **auto_geo_v3.py**：`C:/Users/jia'yue/WorkBuddy/Claw/geo-repo/auto_geo_v3.py`

### 相关文档

- **llms.txt 标准**：参考`references/geo-standard.md`第七节
- **中文AI模型引用偏好**：参考`references/geo-standard.md`第二节
- **GEO评分体系**：参考`references/geo-standard.md`第三节
- **全链路监测框架**：参考`references/geo-standard.md`第十节

---

**geo-converter v3.0** · **龙龟神将**  
*让每一篇公众号文章都成为AI友好的GEO优化内容*  
*基于GEO方案v3.0完整标准 · 支持6大中文AI模型优化 · 无篇数上限*

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/06-工作记录与复盘/daily-logs/2026-06-25]] — 2026-06-25 工作日志
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙心OS升级包：1+5/龙心OS开发设计文档]] — 龙心OS开发设计文档：从理论蓝图到可运行实现
- [[01-核心体系/生生-文化操作系统/_工作档/生生-求是十元素转化方案-20261005]] — 《生生：文化操作系统》× 求是「中华优秀传统文化重要元素」转化方案
- [[01-核心体系/龙心OS_LLM-Wiki-Skills]] — LLM Wiki Skills · 活体维基知识编译系统 v1.0
- [[01-核心体系/龙心OS_Skill Builder v1.0]] — Skill构建申请表
- [[05-五行人格心理学/人格类型/📖 五行人格心理学·完整体系（A01-A12）]] — 📖 五行人格心理学·完整体系（A01-A12）

<!-- AI-LINKS-END -->
