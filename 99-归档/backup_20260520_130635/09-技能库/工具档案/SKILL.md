# TOOLSmd Skill（工具档案）

## 📖 技能定义

TOOLSmd是AI龙龟共生伙伴操作系统的**本地环境配置速查表**，记录SSH连接信息、API路径、部署目标、已安装工具、服务器/设备名称等核心配置信息，随技术栈迭代同步更新。

**核心定位**：
- **不是**正式文档
- **而是**运行所需的速查小抄（cheat sheet）
- **目标**：只保留核心事实信息，快速查询

**核心原则**：
> 随技术栈迭代同步更新，保持配置信息的准确性和时效性。

---

## 🎯 核心内容

### 1. 本地环境配置

**系统信息**：
```yaml
local_system:
  os: Windows 11
  shell: PowerShell
  workspace: c:/Users/jia'yue/WorkBuddy/
  encoding: UTF-8
  timezone: Asia/Shanghai
```

**已安装工具**：
```yaml
installed_tools:
  - git
  - node
  - python
  - obsidian
  - workbuddy
  - openclaw
```

**环境变量**：
```yaml
env_vars:
  PATH: [已配置关键路径]
  WORKSPACE: c:/Users/jia'yue/WorkBuddy/
  PYTHONPATH: [Python库路径]
  NODE_PATH: [Node.js模块路径]
```

### 2. SSH连接信息

**服务器列表**：
```yaml
ssh_connections:
  production_server:
    host: example.com
    port: 22
    user: deploy
    key_path: ~/.ssh/production_key
    description: 生产环境服务器

  staging_server:
    host: staging.example.com
    port: 22
    user: deploy
    key_path: ~/.ssh/staging_key
    description: 测试环境服务器
```

**连接模板**：
```bash
# 生产环境
ssh -i ~/.ssh/production_key deploy@example.com

# 测试环境
ssh -i ~/.ssh/staging_key deploy@staging.example.com
```

### 3. API路径

**内部API**：
```yaml
internal_apis:
  workbuddy_api:
    base_url: https://api.workbuddy.cn
    version: v1
    endpoints:
      - /chat
      - /memory
      - /skills

  ima_api:
    base_url: https://ima.qq.com/agent-interface
    client_id: 59a1edb848ec905552c0fbc8041213bf
    api_key: [存储在.secrets文件]
```

**外部API**：
```yaml
external_apis:
  gemini_api:
    base_url: https://generativelanguage.googleapis.com
    api_key: [存储在.secrets文件]

  xai_api:
    base_url: https://api.x.ai
    api_key: [存储在.secrets文件]

  brave_search:
    base_url: https://api.search.brave.com
    api_key: [存储在.secrets文件]
```

### 4. 部署目标

**部署环境**：
```yaml
deployment_targets:
  production:
    host: example.com
    path: /var/www/example.com
    method: git
    branch: main
    pre_deploy:
      - npm install
      - npm run build
    post_deploy:
      - systemctl restart nginx

  staging:
    host: staging.example.com
    path: /var/www/staging.example.com
    method: git
    branch: develop
    pre_deploy:
      - npm install
      - npm run build
    post_deploy:
      - systemctl restart nginx
```

**部署脚本**：
```bash
# 部署到生产环境
deploy production

# 部署到测试环境
deploy staging
```

### 5. 服务器/设备名称

**服务器列表**：
```yaml
servers:
  production:
    name: prod-01
    ip: 192.168.1.100
    role: production
    status: active

  staging:
    name: staging-01
    ip: 192.168.1.101
    role: staging
    status: active

  database:
    name: db-01
    ip: 192.168.1.102
    role: database
    status: active
```

**设备列表**：
```yaml
devices:
  local_pc:
    name: JiaYue-PC
    os: Windows 11
    role: development
    status: active

  laptop:
    name: JiaYue-Laptop
    os: Windows 10
    role: mobile
    status: inactive
```

---

## 🔄 更新机制

### 1. 实时更新

**触发条件**：
- 安装新工具时
- 配置新服务器时
- 添加新API时
- 修改部署流程时

**执行动作**：
- 立即更新配置文件
- 标注更新时间和原因
- 同步到长期记忆

### 2. 定期验证（每月）

**验证流程**：
1. 读取所有配置
2. 逐项验证准确性
3. 测试关键连接
4. 更新过期信息
5. 记录验证结果

**验证检查项**：
- ✅ SSH连接是否正常
- ✅ API密钥是否有效
- ✅ 部署流程是否可用
- ✅ 工具版本是否最新
- ✅ 服务器状态是否正常

---

## 🔍 查询机制

### 1. 快速查询

**常用查询**：
```bash
# 查询SSH连接
query ssh production

# 查询API路径
query api workbuddy

# 查询部署目标
query deploy production

# 查询工具版本
query tool git
```

**查询结果格式**：
```yaml
name: production_server
host: example.com
port: 22
user: deploy
key_path: ~/.ssh/production_key
last_updated: 2026-03-23
```

### 2. 批量查询

**查询所有服务器**：
```bash
query all servers
```

**查询所有API**：
```bash
query all apis
```

**查询所有工具**：
```bash
query all tools
```

---

## 🔒 安全管理

### 1. 密钥管理

**集中管理**：
- 所有API密钥统一存储在`.secrets`文件
- 不在配置文件中硬编码密钥
- 使用环境变量引用密钥

**密钥格式**（`.secrets`文件）：
```yaml
secrets:
  ima_api_key: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==
  gemini_api_key: [Gemini API密钥]
  xai_api_key: [xAI API密钥]
  brave_search_key: [Brave Search密钥]
```

**引用方式**：
```yaml
ima_api:
  base_url: https://ima.qq.com/agent-interface
  client_id: 59a1edb848ec905552c0fbc8041213bf
  api_key: ${secrets.ima_api_key}  # 引用.secrets文件中的密钥
```

### 2. 权限控制

**文件权限**：
```yaml
permissions:
  toolsmd:
    read: group
    write: owner
    execute: none

  secrets:
    read: owner
    write: owner
    execute: none
```

**访问控制**：
- 只允许授权用户访问
- 记录所有访问日志
- 定期审计访问记录

---

## 📊 版本控制

### 1. Git管理

**配置文件Git化**：
```bash
git add .workbuddy/toolsmd/
git commit -m "Update toolsmd configuration"
git push
```

**版本标签**：
```bash
git tag -a v1.0 -m "Initial toolsmd setup"
git push --tags
```

### 2. 变更历史

**变更记录格式**：
```markdown
## [日期] [变更内容]

**变更类型**: 新增/修改/删除
**变更原因**: ...
**影响范围**: ...
**测试结果**: ✅ 通过 / ❌ 失败
```

---

## 🚫 使用禁忌

### 1. 不要做的
- ❌ 在配置文件中硬编码密钥
- ❌ 记录过期信息
- ❌ 忽略定期验证
- ❌ 手动修改Git历史
- ❌ 共享`.secrets`文件

### 2. 必须做的
- ✅ 密钥集中管理（`.secrets`文件）
- ✅ 实时更新配置信息
- ✅ 定期验证配置准确性
- ✅ 使用版本控制管理
- ✅ 保护敏感信息

---

## 💡 最佳实践

### 1. 配置管理

**实时更新**：
- 安装新工具时立即记录
- 配置新服务器时立即记录
- 修改部署流程时立即记录
- 标注更新时间和原因

**定期验证**：
- 每月验证一次所有配置
- 测试关键连接（SSH、API）
- 检查工具版本是否最新
- 更新过期信息

### 2. 安全管理

**密钥保护**：
- 使用`.secrets`文件集中管理
- 不要硬编码密钥
- 使用环境变量引用
- 定期轮换密钥

**访问控制**：
- 只允许授权用户访问
- 记录所有访问日志
- 定期审计访问记录
- 发现异常立即处理

### 3. 版本控制

**Git管理**：
- 所有配置文件Git化
- 记录所有变更历史
- 使用版本标签标记里程碑
- 定期备份配置

**回滚机制**：
- 保留历史版本
- 出问题时可快速回滚
- 记录回滚原因和结果

---

## 🎯 核心原则总结

### 三大铁律

1. **速查表定位**
   - 只保留核心事实信息
   - 快速查询，快速获取
   - 不写冗余说明

2. **实时更新**
   - 随技术栈迭代同步更新
   - 安装新工具立即记录
   - 保持信息准确性

3. **安全第一**
   - 密钥集中管理
   - 不硬编码敏感信息
   - 使用环境变量引用

### 核心价值

- **快速查询**：快速获取所需配置信息
- **准确可靠**：实时更新，定期验证
- **安全可控**：密钥集中管理，访问控制
- **版本管理**：Git化管理，可追溯历史

---

## 🔧 实施路线

### 第一阶段：基础配置（立即）
- ✅ 记录本地环境配置
- ✅ 记录SSH连接信息
- ✅ 记录API路径

### 第二阶段：部署配置（本周）
- ⏳ 记录部署目标
- ⏳ 记录服务器列表
- ⏳ 记录部署流程

### 第三阶段：优化完善（本月）
- ⏳ 建立版本控制
- ⏳ 实施定期验证
- ⏳ 优化查询机制

---

**版本**: v1.0
**创建日期**: 2026-03-23
**对标来源**: OpenClaw TOOLSmd规则
**AI龙龟共生伙伴操作系统版本**: v4.1
**路径**: `C:\Users\jia'yue\.workbuddy\skills\工具档案\SKILL.md`
