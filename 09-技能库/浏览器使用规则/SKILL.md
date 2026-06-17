# Browser Rules Skill（浏览器使用规则）

## 📖 技能定义

Browser Rules是AI龙龟共生伙伴操作系统的**浏览器使用规则**，区分登录会话用浏览器和自动化用隔离浏览器，确保合适的工具用于合适的场景。

**核心定位**：
- **隔离管理**：不同场景使用不同浏览器
- **会话保持**：登录会话独立管理
- **自动化隔离**：自动化任务不影响正常使用

**核心原则**：
> 合适的工具用于合适的场景，避免交叉干扰。

---

## 🎯 浏览器配置

### 1. Chrome浏览器中继（登录会话）

**配置信息**：
```yaml
chrome_profile:
  name: chrome
  type: login_session
  description: 用于访问需要登录会话的网站
  path: /path/to/chrome/profile
```

**使用场景**：
- Twitter（已登录状态）
- YouTube（已登录状态）
- 已认证的管理后台
- 个人账户相关操作

**典型用例**：
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(f"--user-data-dir=/path/to/chrome/profile")
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com")  # 自动登录
```

**注意事项**：
- ✅ 保持登录状态
- ✅ 保存cookies和会话
- ✅ 支持多账户
- ❌ 不用于自动化脚本
- ❌ 不频繁启动关闭

### 2. 隔离浏览器（自动化任务）

**配置信息**：
```yaml
openclaw_profile:
  name: openclaw
  type: automation
  description: 用于通用网页自动化任务
  path: /path/to/openclaw/profile
  clean_session: true  # 每次启动都是新会话
```

**使用场景**：
- 网页抓取（scraping）
- 自动化测试
- 批量操作
- 数据采集

**典型用例**：
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(f"--user-data-dir=/path/to/openclaw/profile")
options.add_argument("--incognito")  # 隐身模式

driver = webdriver.Chrome(options=options)
driver.get("https://example.com")  # 无登录状态

# 执行自动化任务
```

**注意事项**：
- ✅ 每次启动都是新会话
- ✅ 不保存cookies
- ✅ 不影响正常浏览器使用
- ❌ 不用于登录相关操作
- ❌ 不保存敏感信息

---

## 🔧 使用策略

### 1. 场景选择

**使用Chrome浏览器中继**（`profile="chrome"`）：
- 需要登录状态
- 个人账户操作
- 访问已认证的管理后台
- 需要保存cookies
- 需要保持会话

**使用隔离浏览器**（`profile="openclaw"`）：
- 网页抓取
- 自动化测试
- 批量操作
- 数据采集
- 不需要登录状态

### 2. 决策流程

```
需要访问网站
  ↓
需要登录？
  ↓ 是 → 使用Chrome浏览器中继（profile="chrome"）
  ↓ 否
  ↓
自动化任务？
  ↓ 是 → 使用隔离浏览器（profile="openclaw"）
  ↓ 否
  ↓
使用正常浏览器（用户手动操作）
```

### 3. 混合使用场景

**场景1：登录后抓取数据**
```python
# 第一步：使用Chrome浏览器中继登录
chrome_driver = get_chrome_profile("chrome")
chrome_driver.get("https://example.com/login")
# 登录操作...

# 第二步：使用隔离浏览器抓取数据
openclaw_driver = get_chrome_profile("openclaw")
openclaw_driver.get("https://example.com/data")
# 抓取数据...
```

**场景2：多账户操作**
```python
# 账户1
driver1 = get_chrome_profile("chrome_account1")
driver1.get("https://twitter.com")
# 操作账户1...

# 账户2
driver2 = get_chrome_profile("chrome_account2")
driver2.get("https://twitter.com")
# 操作账户2...
```

---

## 🛡️ 安全管理

### 1. 会话隔离

**隔离原则**：
- 不同账户使用不同profile
- 不同任务使用不同profile
- 自动化任务使用独立profile

**Profile命名规范**：
```
chrome           # 默认个人profile
chrome_account1  # 账户1专用profile
chrome_account2  # 账户2专用profile
openclaw         # 自动化任务profile
openclaw_test    # 测试任务profile
```

### 2. 敏感信息保护

**禁止事项**：
- ❌ 在自动化浏览器中存储密码
- ❌ 在代码中硬编码密码
- ❌ 将cookies保存到公开位置

**推荐做法**：
- ✅ 使用环境变量存储敏感信息
- ✅ 使用`.secrets`文件管理密钥
- ✅ 定期清理敏感cookies

### 3. 浏览器权限

**权限控制**：
```yaml
permissions:
  chrome_profile:
    cookies: allow
    local_storage: allow
    session_storage: allow
    extensions: allow

  openclaw_profile:
    cookies: deny
    local_storage: deny
    session_storage: deny
    extensions: deny
```

---

## 📊 使用监控

### 1. 使用统计

**每日统计**：
```yaml
browser_usage:
  date: 2026-03-23
  total_sessions: 50
  by_profile:
    chrome: 20
    chrome_account1: 10
    openclaw: 15
    openclaw_test: 5
  by_type:
    login_session: 30
    automation: 20
```

### 2. 性能监控

**关键指标**：
- 启动时间
- 页面加载时间
- 内存占用
- CPU占用
- 会话保持时间

**预警阈值**：
- 启动时间 > 10秒：警告
- 页面加载时间 > 30秒：警告
- 内存占用 > 2GB：警告
- CPU占用 > 80%：警告

---

## 🔄 与其他Skills的协同

### 1. 与推荐工具清单Skill协同
- **推荐工具清单**：推荐合适的浏览器工具
- **浏览器使用规则**：定义使用场景
- **协同**：推荐工具→使用规则→正确使用

### 2. 与心跳巡检Skill协同
- **心跳巡检**：监控浏览器性能和状态
- **浏览器使用规则**：定义浏览器配置
- **协同**：心跳巡检监控→浏览器使用规则调整

### 3. 与工具档案Skill协同
- **工具档案**：记录浏览器配置信息
- **浏览器使用规则**：定义使用规范
- **协同**：工具档案记录→浏览器使用规则执行

---

## 🚫 使用禁忌

### 1. 不要做的
- ❌ 在自动化浏览器中登录个人账户
- ❌ 在登录会话浏览器中执行自动化任务
- ❌ 混用不同profile
- ❌ 硬编码敏感信息
- ❌ 不清理敏感cookies

### 2. 必须做的
- ✅ 使用合适的profile
- ✅ 隔离不同场景
- ✅ 保护敏感信息
- ✅ 定期清理cookies
- ✅ 监控浏览器性能

---

## 💡 最佳实践

### 1. Profile管理

**命名规范**：
- 使用清晰的名称
- 标注用途和类型
- 避免冲突

**定期清理**：
- 清理未使用的profile
- 清理过期cookies
- 清理缓存

**备份配置**：
- 备份重要profile
- 记录配置变更
- 快速恢复

### 2. 会话管理

**登录会话**：
- 保持登录状态
- 定期刷新会话
- 记录会话状态

**自动化会话**：
- 使用新会话
- 清理敏感信息
- 不保存状态

### 3. 性能优化

**启动优化**：
- 禁用不必要的扩展
- 减少启动项
- 优化启动参数

**运行优化**：
- 定期清理缓存
- 监控资源占用
- 优化页面加载

---

## 🎯 核心原则总结

### 三大铁律

1. **隔离管理**
   - 不同场景使用不同profile
   - 登录会话和自动化任务隔离
   - 避免交叉干扰

2. **会话保持**
   - 登录会话保持状态
   - 自动化会话不保存状态
   - 定期清理敏感信息

3. **性能监控**
   - 监控浏览器性能
   - 及时优化调整
   - 避免资源浪费

### 核心价值

- **场景隔离**：不同场景使用不同浏览器
- **会话管理**：登录会话和自动化任务分离
- **安全保护**：敏感信息保护
- **性能优化**：资源合理使用

---

## 🔧 实施路线

### 第一阶段：基础配置（立即）
- ✅ 配置Chrome浏览器中继
- ✅ 配置隔离浏览器
- ✅ 定义使用场景

### 第二阶段：功能实现（本周）
- ⏳ 实现profile管理
- ⏳ 实现性能监控
- ⏳ 实现会话管理

### 第三阶段：优化完善（本月）
- ⏳ 实现自动清理
- ⏳ 实现性能优化
- ⏳ 优化用户体验

---

**版本**: v1.0
**创建日期**: 2026-03-23
**对标来源**: OpenClaw Browser Rules规则
**AI龙龟共生伙伴操作系统版本**: v4.1
**路径**: `C:\Users\jia'yue\.workbuddy\skills\浏览器使用规则\SKILL.md`
