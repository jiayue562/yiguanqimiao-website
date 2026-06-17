# Good Tools to Use Skill（推荐工具清单）

## 📖 技能定义

Good Tools to Use是AI龙龟共生伙伴操作系统的**推荐工具清单**，明确可调用的AI、搜索、部署等工具及使用限制，定义最佳实践和使用规范。

**核心定位**：
- **不是**强制使用的工具列表
- **而是**推荐和已验证的工具清单
- **目标**：提供最佳工具选择和使用指导

**核心原则**：
> 合适的工具用于合适的场景，避免工具滥用和资源浪费。

---

## 🎯 推荐工具清单

### 1. AI工具

#### Gemini API（Google）

**功能**：图像生成（Imagen 3模型）

**用途**：
- 内容配图生成
- 社交媒体图片
- 文章插图
- 封面设计

**使用限制**：
- 单日请求限制：100次
- 单次图片数量：最多4张
- 图片分辨率：最高1024x1024

**最佳实践**：
- ✅ 生成配图前先检查是否已有现成图片
- ✅ 明确描述图片内容和风格
- ✅ 生成后人工审核质量
- ❌ 不生成敏感或违规内容

**配置示例**：
```python
import google.generativeai as genai

genai.configure(api_key="${secrets.gemini_api_key}")
model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')

prompt = "生成一张现代简约风格的配图，主题是AI与人机协同"
response = model.generate_content(prompt)
```

#### xAI API（马斯克旗下）

**功能**：集成Grok/X，获取Twitter实时情报

**用途**：
- Twitter趋势分析
- 实时热点追踪
- 用户行为分析
- 社交媒体监控

**使用限制**：
- 单日请求限制：500次
- 数据延迟：1-5分钟
- 数据保留期：7天

**最佳实践**：
- ✅ 定期检索关键话题
- ✅ 分析趋势变化
- ✅ 结合其他数据源验证
- ❌ 不滥用API导致限流

**配置示例**：
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.x.ai/v1",
    api_key="${secrets.xai_api_key}"
)

response = client.chat.completions.create(
    model="grok-beta",
    messages=[{"role": "user", "content": "分析当前Twitter热门话题"}]
)
```

#### LarryBrain Pro

**功能**：按需调用的32项技能工具

**用途**：
- 专业领域知识查询
- 技能工具调用
- 自动化任务执行
- 多场景应用

**技能清单**：
- 数据分析（5项）
- 内容生成（8项）
- 代码生成（7项）
- 翻译服务（6项）
- 图像处理（6项）

**使用限制**：
- 单日请求限制：1000次
- 单次任务时长：最长5分钟
- 并发任务数：最多3个

**最佳实践**：
- ✅ 根据场景选择合适技能
- ✅ 批量任务合并调用
- ✅ 监控任务执行状态
- ❌ 不超时占用资源

### 2. 搜索工具

#### Brave Search API

**功能**：网页搜索服务（无需Google）

**用途**：
- 网页信息检索
- 实时新闻搜索
- 知识问答
- 链接收集

**使用限制**：
- 单日请求限制：2000次
- 搜索结果数量：最多50条
- 数据延迟：实时

**最佳实践**：
- ✅ 明确搜索关键词
- ✅ 过滤和排序结果
- ✅ 验证信息准确性
- ❌ 不重复搜索相同内容

**配置示例**：
```python
from brave import Brave

brave = Brave(api_key="${secrets.brave_search_key}")

results = brave.search(
    query="AI龙龟共生伙伴操作系统",
    count=10,
    freshness="week"  # 限定时间范围
)
```

### 3. 部署工具

#### Netlify API

**功能**：生产环境部署工具

**用途**：
- 网站部署
- CDN加速
- 域名管理
- 环境变量配置

**使用限制**：
- ⚠️ **会产生费用，需谨慎使用**
- 单月免费额度：300GB带宽
- 部署次数：无限制
- 并发部署：最多5个

**最佳实践**：
- ✅ 部署前先在测试环境验证
- ✅ 使用Git触发自动部署
- ✅ 监控部署状态和日志
- ❌ 不在生产环境直接调试

**配置示例**：
```python
import netlify

client = netlify.Client(access_token="${secrets.netlify_token}")

# 触发部署
site_id = "your-site-id"
deploy = client.deploy_site(site_id, dir="./dist")

# 监控部署状态
print(f"Deploy state: {deploy.state}")
```

### 4. 本地工具

#### Voicebox（本地语音克隆）

**功能**：基于Qwen3-TTS通义千问语音模型的语音克隆

**用途**：
- 语音合成
- 语音克隆
- 多角色配音
- 音频生成

**使用限制**：
- 无云服务依赖
- 本地计算资源消耗较高
- 单次生成时长：最长10分钟
- 音频格式：支持MP3/WAV

**最佳实践**：
- ✅ 合理设置采样率和比特率
- ✅ 使用高质量音频样本
- ✅ 批量任务分批处理
- ❌ 不在低性能设备上使用

**配置示例**：
```python
from voicebox import Voicebox

# 初始化语音克隆器
vb = Voicebox(model="Qwen3-TTS")

# 克隆声音
voice = vb.clone_voice(
    reference_audio="./reference.wav",
    text="这是AI龙龟共生伙伴操作系统的语音",
    output="./output.mp3"
)
```

#### AgentMail

**功能**：AI代理专属邮箱

**用途**：
- 邮件发送
- 邮件接收
- 邮件处理
- 自动回复

**使用限制**：
- 单日发送限制：500封
- 单封邮件大小：最大25MB
- 附件类型：支持常见格式

**最佳实践**：
- ✅ 明确邮件主题和收件人
- ✅ 规范邮件格式
- ✅ 重要邮件人工审核
- ❌ 不发送垃圾邮件

**配置示例**：
```python
from agentmail import AgentMail

mail = AgentMail(
    smtp_server="smtp.example.com",
    smtp_port=587,
    username="${secrets.agentmail_user}",
    password="${secrets.agentmail_pass}"
)

mail.send(
    to="recipient@example.com",
    subject="AI龙龟共生伙伴操作系统更新",
    body="系统已完成升级..."
)
```

#### find-skills

**功能**：从Vercel-labs代码仓库获取技能发现能力

**用途**：
- 技能搜索
- 技能安装
- 技能更新
- 技能管理

**使用限制**：
- 仅本地使用
- 不连接外部仓库
- 技能数量：最多100个
- 技能大小：单个最大10MB

**最佳实践**：
- ✅ 定期更新技能库
- ✅ 验证技能安全性
- ✅ 备份技能配置
- ❌ 不安装未经验证的技能

**配置示例**：
```bash
# 搜索技能
find-skills search "data-analysis"

# 安装技能
find-skills install data-analysis

# 更新技能
find-skills update data-analysis
```

---

## 🔄 工具选择策略

### 1. 按场景选择

| 场景 | 推荐工具 | 备选工具 |
|------|---------|---------|
| **图像生成** | Gemini API | Midjourney, DALL-E |
| **Twitter分析** | xAI API | Twitter API, Tweepy |
| **网页搜索** | Brave Search | Google Search API, Bing Search |
| **网站部署** | Netlify API | Vercel, GitHub Pages |
| **语音合成** | Voicebox（本地） | ElevenLabs, Azure TTS |
| **邮件处理** | AgentMail | SendGrid, Mailgun |
| **技能管理** | find-skills | npm, pip |

### 2. 按性能选择

**高性能任务**：
- 使用本地工具（Voicebox）
- 使用专业API（LarryBrain Pro）
- 避免云服务延迟

**高可靠性任务**：
- 使用成熟工具（Netlify API）
- 使用多源验证（Brave Search + 其他）
- 使用备份方案

**高安全性任务**：
- 使用本地处理（Voicebox）
- 使用加密传输（AgentMail）
- 使用权限控制（find-skills）

---

## 📊 工具使用监控

### 1. 使用统计

**每日统计**：
```yaml
usage_stats:
  date: 2026-03-23
  tools:
    gemini_api:
      requests: 25
      success_rate: 98%
      avg_response_time: 2.5s

    xai_api:
      requests: 15
      success_rate: 95%
      avg_response_time: 1.8s

    brave_search:
      requests: 50
      success_rate: 99%
      avg_response_time: 0.8s
```

**每周统计**：
- 总请求数
- 成功率
- 平均响应时间
- 错误率
- 成本统计

### 2. 性能监控

**关键指标**：
- 响应时间
- 成功率
- 错误率
- 成本
- 资源消耗

**预警阈值**：
- 响应时间 > 5秒：警告
- 成功率 < 95%：警告
- 错误率 > 5%：警告
- 成本超过预算：警告

---

## 🔒 安全管理

### 1. 密钥管理

**集中管理**：
- 所有API密钥统一存储在`.secrets`文件
- 不在代码中硬编码密钥
- 使用环境变量引用密钥

**密钥轮换**：
- 每季度轮换一次
- 发现泄露立即轮换
- 记录轮换历史

### 2. 权限控制

**最小权限原则**：
- 只授予必要权限
- 定期审查权限
- 撤销不再需要的权限

**访问控制**：
- 只允许授权服务访问
- 记录所有访问日志
- 发现异常立即处理

---

## 🚫 使用禁忌

### 1. 不要做的
- ❌ 超过API请求限制
- ❌ 在生产环境直接调试
- ❌ 不验证工具输出就使用
- ❌ 忽略成本监控
- ❌ 共享API密钥

### 2. 必须做的
- ✅ 选择合适的工具
- ✅ 遵循使用限制
- ✅ 监控工具性能
- ✅ 定期更新工具版本
- ✅ 保护API密钥

---

## 💡 最佳实践

### 1. 工具选择

**按需选择**：
- 明确需求和场景
- 评估工具适用性
- 比较性能和成本
- 选择最优方案

**组合使用**：
- 多工具组合完成任务
- 利用各自优势
- 避免单一依赖
- 提高可靠性

### 2. 性能优化

**缓存机制**：
- 缓存重复查询结果
- 设置合理的缓存时间
- 定期清理过期缓存

**批量处理**：
- 合并相似请求
- 批量调用API
- 减少请求次数

**异步调用**：
- 非阻塞方式调用
- 并行处理任务
- 提高响应速度

### 3. 错误处理

**重试机制**：
- 失败时自动重试
- 设置重试次数和间隔
- 记录失败原因

**降级策略**：
- 主工具失败时切换备选
- 确保核心功能可用
- 提前测试降级方案

**监控告警**：
- 实时监控工具状态
- 异常时及时告警
- 记录处理过程

---

## 🎯 核心原则总结

### 三大铁律

1. **合适工具用于合适场景**
   - 不盲目使用工具
   - 评估适用性和成本
   - 选择最优方案

2. **遵循使用限制**
   - 不超过API请求限制
   - 监控性能和成本
   - 及时优化和调整

3. **安全第一**
   - 密钥集中管理
   - 最小权限原则
   - 定期审查权限

### 核心价值

- **工具齐全**：覆盖AI、搜索、部署等场景
- **性能可靠**：成熟工具，稳定可用
- **成本可控**：明确限制，合理使用
- **安全可控**：权限管理，访问控制

---

## 🔧 实施路线

### 第一阶段：基础工具（立即）
- ✅ 集成Gemini API
- ✅ 集成Brave Search
- ✅ 集成xAI API

### 第二阶段：高级工具（本周）
- ⏳ 集成Netlify API
- ⏳ 配置Voicebox
- ⏳ 配置AgentMail

### 第三阶段：优化完善（本月）
- ⏳ 建立性能监控
- ⏳ 实施使用统计
- ⏳ 优化工具选择策略

---

**版本**: v1.1
**创建日期**: 2026-03-23
**更新日期**: 2026-04-03
**对标来源**: OpenClaw Good Tools to Use规则
**AI龙龟共生伙伴操作系统版本**: v4.1
**路径**: `C:\Users\jia'yue\.workbuddy\skills\推荐工具清单\SKILL.md`
**更新说明**: v1.1更新对标20个提示词中的工具列表，补充Voicebox、AgentMail、Brave Search、LarryBrain Pro、find-skills等工具
