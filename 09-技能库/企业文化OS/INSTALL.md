# 企业文化OS · 技术栈安装指南

> **版本**: v1.0 | **创建**: 2026-04-10 | **维护者**: 龙龟神将

---

## 📦 安装清单

企业文化OS采用六层技术栈架构：

```
┌─────────────────────────────────────────┐
│  Layer 6: SOP层（标准化操作程序）          │
│  - 诊断SOP / 设计SOP / 落地SOP            │
├─────────────────────────────────────────┤
│  Layer 5: 工作流层（Workflow）            │
│  - 七步落地工作流 / 诊断工作流 / 迭代工作流 │
├─────────────────────────────────────────┤
│  Layer 4: Framework层（框架调度）          │
│  - 任务调度 / 状态管理 / 执行监控          │
├─────────────────────────────────────────┤
│  Layer 3: MCP层（通信协议）               │
│  - 子智能体通信 / 数据同步 / 协同协议      │
├─────────────────────────────────────────┤
│  Layer 2: Skills层（技能单元）            │
│  - 9个子智能体Skills + 总调度Skill         │
├─────────────────────────────────────────┤
│  Layer 1: CLI层（命令入口）               │
│  - 诊断CLI / 设计CLI / 落地CLI            │
└─────────────────────────────────────────┘
```

---

## ✅ 安装状态

| 层级 | 组件 | 状态 | 路径 |
|------|------|------|------|
| CLI | 企业文化诊断CLI | 🔄 安装中 | `cli/diagnose-cli.md` |
| CLI | 企业文化设计CLI | ⏳ 待安装 | `cli/design-cli.md` |
| CLI | 企业文化落地CLI | ⏳ 待安装 | `cli/implement-cli.md` |
| Skills | 企业文化诊断子智能体 | ⏳ 待构建 | `skills/qiye-wenhua-zhenduan/` |
| Skills | 融入时代子智能体 | ⏳ 待构建 | `skills/rongru-shidai/` |
| Skills | 经营心法子智能体 | ⏳ 待构建 | `skills/jingying-xinfa/` |
| Skills | 氛围营造子智能体 | ⏳ 待构建 | `skills/fenwei-yingzao/` |
| Skills | 礼乐仪式子智能体 | ⏳ 待构建 | `skills/liyi-yishi/` |
| Skills | 功勋体系子智能体 | ⏳ 待构建 | `skills/gongxun-tixi/` |
| Skills | 企业商学院子智能体 | ⏳ 待构建 | `skills/qiye-shangxueyuan/` |
| Skills | 企业大事件子智能体 | ⏳ 待构建 | `skills/qiye-dashijian/` |
| Skills | 企业文化总智能体 | ⏳ 待构建 | `skills/qiye-wenhua-zongti/` |
| MCP | 子智能体通信协议 | ⏳ 待配置 | `mcp/qiye-wenhua-mcp.json` |
| Framework | 任务调度框架 | ⏳ 待配置 | `framework/qiye-wenhua-framework.yaml` |
| 工作流 | 七步落地工作流 | ⏳ 待创建 | `workflow/7step-workflow.md` |
| SOP | 诊断→设计→落地SOP | ⏳ 待创建 | `sop/qiye-wenhua-sop.md` |

---

## 🚀 快速开始

### 1. 诊断入口
```bash
# 启动企业文化诊断
企业文化诊断 --企业名称="XX公司" --行业="互联网" --规模="100-500人"
```

### 2. 设计入口
```bash
# 启动企业文化设计
企业文化设计 --诊断报告="path/to/report.md" --重点模块="经营心法,氛围营造"
```

### 3. 落地入口
```bash
# 启动企业文化落地
企业文化落地 --设计方案="path/to/design.md" --阶段="第一阶段"
```

---

## 📁 目录结构

```
企业文化OS/
├── README.md                 # 总览文档
├── INSTALL.md               # 本安装指南
├── cli/                     # CLI层
│   ├── diagnose-cli.md     # 诊断CLI
│   ├── design-cli.md       # 设计CLI
│   └── implement-cli.md    # 落地CLI
├── skills/                  # Skills层（9+1）
│   ├── qiye-wenhua-zhenduan/      # 诊断子智能体
│   ├── rongru-shidai/             # 融入时代
│   ├── jingying-xinfa/            # 经营心法
│   ├── fenwei-yingzao/            # 氛围营造
│   ├── liyi-yishi/                # 礼乐仪式
│   ├── gongxun-tixi/              # 功勋体系
│   ├── qiye-shangxueyuan/         # 企业商学院
│   ├── qiye-dashijian/            # 企业大事件
│   └── qiye-wenhua-zongti/        # 总智能体
├── mcp/                     # MCP层
│   └── qiye-wenhua-mcp.json
├── framework/               # Framework层
│   └── qiye-wenhua-framework.yaml
├── workflow/                # 工作流层
│   ├── 7step-workflow.md
│   ├── diagnose-workflow.md
│   └── iterate-workflow.md
└── sop/                     # SOP层
    ├── diagnose-sop.md
    ├── design-sop.md
    └── implement-sop.md
```

---

## 🔧 安装步骤

### Step 1: CLI层安装
- [x] 创建CLI目录结构
- [ ] 编写诊断CLI文档
- [ ] 编写设计CLI文档
- [ ] 编写落地CLI文档

### Step 2: Skills层安装
- [ ] 使用Skill Builder构建9个子智能体
- [ ] 配置自动触发规则
- [ ] 测试子智能体调用

### Step 3: MCP层安装
- [ ] 定义子智能体通信协议
- [ ] 配置数据同步机制
- [ ] 测试跨智能体调用

### Step 4: Framework层安装
- [ ] 配置任务调度器
- [ ] 配置状态管理
- [ ] 配置执行监控

### Step 5: 工作流层安装
- [ ] 创建七步落地工作流
- [ ] 创建诊断工作流
- [ ] 创建迭代工作流

### Step 6: SOP层安装
- [ ] 编写诊断SOP
- [ ] 编写设计SOP
- [ ] 编写落地SOP

---

## 📊 安装进度

| 阶段 | 进度 | 状态 |
|------|------|------|
| CLI层 | 0% | 🔄 进行中 |
| Skills层 | 0% | ⏳ 等待中 |
| MCP层 | 0% | ⏳ 等待中 |
| Framework层 | 0% | ⏳ 等待中 |
| 工作流层 | 0% | ⏳ 等待中 |
| SOP层 | 0% | ⏳ 等待中 |

**总体进度**: 0% | **预计完成时间**: 2026-04-12

---

## 📝 更新日志

### v1.0 (2026-04-10)
- 初始版本创建
- 定义六层技术栈架构
- 创建安装清单和目录结构

---

**企业文化OS · 技术栈安装指南** · 龙龟神将维护
