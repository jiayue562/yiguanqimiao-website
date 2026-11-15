# Skill 构建 SOP - 龙心 OS 技能开发标准流程

> 🔧 从需求到部署的完整流程 · 第 4 步

---

## 📋 流程总览

```
需求分析 → 技能搜索 → 安全审查 → 安装配置 → 测试验证 → 文档沉淀
    ↓          ↓          ↓          ↓          ↓          ↓
 明确需求   ClawHub    skill-vetter  安装技能   功能测试   写入 TOOLS.md
          本地技能   手动审查      配置凭证   集成测试   更新 SOP
```

---

## 步骤 1: 需求分析

### 明确需求

**输入**: 用户描述的功能需求

**输出**: 结构化的技能需求文档

**模板**:
```markdown
## 技能需求

### 功能描述
[一句话描述技能功能]

### 使用场景
- 场景 1
- 场景 2

### 期望行为
[技能应该如何响应用户请求]

### 优先级
🔴 高 / 🟡 中 / 🟢 低
```

### 需求分类

| 类别 | 示例 | 推荐方案 |
|------|------|----------|
| 记忆系统 | 写入/读取记忆 | 已有技能组合 |
| 搜索获取 | 联网搜索/公众号 | web-search-plus |
| 文件处理 | PDF/Word/Excel | 专用技能 |
| 自动化 | 定时任务 | cron-helper |
| 安全审查 | 技能 vetting | skill-vetter |

---

## 步骤 2: 技能搜索

### 搜索渠道

**优先级顺序**:
1. **本地已安装** (`skills_extra` + `~/.agents/skills`)
2. **ClawHub** (官方市场)
3. **GitHub** (开源技能)
4. **自研** (创建新技能)

### 搜索命令

```powershell
# ClawHub 搜索
openclaw skills search <keyword>

# 本地技能列表
openclaw skills list

# 查看技能详情
openclaw skills show <skill-name>
```

### 搜索技巧

| 技巧 | 示例 | 说明 |
|------|------|------|
| 同义词 | `summarize` / `summary` / `abstract` | 多词搜索 |
| 功能描述 | `pdf reader` / `document convert` | 描述功能 |
| 场景 | `wechat search` / `公众号` | 使用场景 |

---

## 步骤 3: 安全审查

### 自动审查 (skill-vetter)

```powershell
openclaw skills vet <skill-name>
```

**检查项**:
- [ ] 权限申请是否合理
- [ ] 网络请求目标是否可信
- [ ] 代码是否有混淆
- [ ] 依赖来源是否可靠
- [ ] 是否有恶意代码迹象

### 手动审查清单

| 检查项 | 通过标准 | 状态 |
|--------|----------|------|
| 来源可信 | 官方市场/知名作者 | ⬜ |
| 权限合理 | 最小权限原则 | ⬜ |
| 代码清晰 | 无混淆/加密 | ⬜ |
| 依赖安全 | 无未知依赖 | ⬜ |
| 文档完整 | 有使用说明 | ⬜ |

### 风险等级

| 等级 | 标准 | 处理 |
|------|------|------|
| 🟢 安全 | 全部通过 | 直接安装 |
| 🟡 低风险 | 1-2 项存疑 | 告知用户后决定 |
| 🔴 高风险 | 3 项以上存疑 | 拒绝安装 |

---

## 步骤 4: 安装配置

### 安装命令

```powershell
# 从 ClawHub 安装
openclaw skills install <skill-name>

# 本地安装 (复制技能目录)
Copy-Item -Path "source/skill" -Destination "~/.agents/skills/" -Recurse
```

### 配置凭证

**常见凭证类型**:

| 类型 | 存储位置 | 示例 |
|------|----------|------|
| API Key | `~/.config/<skill>/api_key` | IMA API Key |
| Client ID | `~/.config/<skill>/client_id` | IMA Client ID |
| Token | 环境变量 | `export TOKEN=xxx` |

### 配置模板

```powershell
# 创建配置目录
New-Item -ItemType Directory -Force -Path "~/.config/<skill>"

# 写入凭证
echo "your_api_key" > "~/.config/<skill>/api_key"

# 验证配置
cat "~/.config/<skill>/api_key"
```

---

## 步骤 5: 测试验证

### 功能测试

**测试清单**:

| 测试项 | 测试方法 | 预期结果 |
|--------|----------|----------|
| 基本功能 | 执行核心功能 | 正常响应 |
| 边界条件 | 输入极端值 | 优雅处理 |
| 错误处理 | 故意触发错误 | 清晰报错 |
| 性能 | 大数据量 | 可接受延迟 |

### 集成测试

```powershell
# 测试技能调用
openclaw skills run <skill-name> --args "test input"

# 检查输出
# 预期：结构化输出，无错误
```

### 验证标准

- [ ] 功能正常
- [ ] 无安全警告
- [ ] 文档完整
- [ ] 凭证配置正确
- [ ] 与其他技能无冲突

---

## 步骤 6: 文档沉淀

### 更新 TOOLS.md

**添加技能条目**:

```markdown
### 新增技能

| 技能 | 功能 | 位置 |
|------|------|------|
| `<skill-name>` | [功能描述] | `~/.agents/skills/` |
```

### 创建使用示例

**示例模板**:

```markdown
## <skill-name> 使用示例

### 基本用法
```
[用户指令示例]
```

### 高级用法
```
[复杂场景示例]
```

### 注意事项
- 注意 1
- 注意 2
```

### 写入 LEARNINGS.md

**经验提炼**:

```markdown
### [技能名称] 安装经验

**来源**: 本次安装实践

**经验**:
1. [经验点 1]
2. [经验点 2]

**SOP**:
[标准化流程]
```

---

## 📊 技能安装清单模板

### 已安装技能

```markdown
| 技能名称 | 功能 | 安装日期 | 状态 | 备注 |
|----------|------|----------|------|------|
| skill-1 | 功能 1 | 2026-04-13 | ✅ | 正常 |
| skill-2 | 功能 2 | 2026-04-13 | ✅ | 需配置 |
```

### 待安装技能

```markdown
| 技能名称 | 功能 | 优先级 | 预计安装日期 |
|----------|------|--------|--------------|
| skill-3 | 功能 3 | 🔴 高 | 2026-04-14 |
| skill-4 | 功能 4 | 🟡 中 | 2026-04-15 |
```

---

## 🔄 持续优化

### 技能审查周期

| 周期 | 审查内容 |
|------|----------|
| 每周 | 新安装技能审查 |
| 每月 | 已安装技能使用情况 |
| 每季 | 技能库整体优化 |

### 技能淘汰标准

- 6 个月未使用
- 有更好替代品
- 存在安全风险
- 作者停止维护

---

## 🎯 9 条核心指令实现

### 指令实现状态

| 指令 | 功能 | 实现方式 | 状态 |
|------|------|----------|------|
| 指令一 | 写入记忆 | `edit` + MEMORY.md | ✅ |
| 指令二 | 调取记忆 | `memory_search` + `memory_get` | ✅ |
| 指令三 | 记忆蒸馏 | AI 总结 + `edit` | ✅ |
| 指令四 | 联网搜索 | `web-search-plus` | ✅ |
| 指令五 | 深度研究 | `web-search-plus` + `web_fetch` | ✅ |
| 指令六 | 读取文件 | `read` + 文档技能 | ✅ |
| 指令七 | 批量读取 | `Get-ChildItem` + AI 整合 | ✅ |
| 指令八 | 知识沉淀 | `edit` + MEMORY.md | ✅ |
| 指令九 | 定时任务 | `cron-helper` + 脚本 | ✅ |

---

## 📌 快速参考

### 常用命令

```powershell
# 搜索技能
openclaw skills search <keyword>

# 安装技能
openclaw skills install <skill-name>

# 安全审查
openclaw skills vet <skill-name>

# 列出技能
openclaw skills list

# 查看技能详情
openclaw skills show <skill-name>

# 更新技能
openclaw skills update <skill-name>
```

### 配置路径

| 配置 | 路径 |
|------|------|
| 技能目录 | `~/.agents/skills/` |
| 配置目录 | `~/.config/<skill>/` |
| 工作区 | `~/.openclaw/workspace/` |
| 记忆文件 | `~/.openclaw/workspace/MEMORY.md` |

---

_龙心 OS Skill 构建 SOP v1.0 · 最后更新：2026-04-13 · 悟空 × 龙龟 共同维护_
