# 龙心OS开发设计文档：从理论蓝图到可运行实现

> **文档属性**：开发设计（工程实现版）
> **版本**：v1.0
> **编制日期**：2026-07-31
> **上游文档**：《龙心OS顶层设计梳理.md》（理论版，v1.0，2026-07-31）
> **代码基线**：`C:\Users\jia'yue\.agents\skills\10-kernel\龙心OS`（v8.0 引擎目录，2026-07-29 代码审计）
> **性质定位**：面向工程的开发设计文档，含架构设计、差距分析、模块设计、接口契约、开发计划、测试策略
> **适用范围**：龙心OS调度中枢 + 五大引擎 + 三扩展引擎 + 上下文记忆系统 + 双尺度治理

---

## 摘要

本开发设计文档是《龙心OS顶层设计梳理》的工程落地方案。顶层设计文档解决了"龙心OS是什么、五大引擎如何构成认知闭环、理论底座如何统一"的问题；本开发文档解决"龙心OS如何被实现、代码如何组织、接口如何契约、差距如何弥合"的问题。

文档基于对现有代码基线（2026-07-29）的完整审计，识别出六大工程差距：**心脏引擎调用桩（stub）化、上下文管理器纯内存化、扩展引擎游离于调度之外、契约传参与实际实现不对齐、双路由治理缺位、版本治理缺失**。据此提出目标架构与分阶段开发计划。

文档核心技术主张：

1. **统一引擎协议**：定义 `Engine` 协议与 `TaskContext`/`EngineResult` 数据模型，使五大引擎与三扩展引擎以同一契约被调度中枢调用，弥合"契约文档"与"实际实现"的错位。
2. **调度中枢真实化**：将 `invoke_heart_engine` 从返回字符串的桩实现升级为动态加载并真实调用引擎类的方法，实现"1+5引擎"真实联动。
3. **上下文持久化**：将纯内存会话升级为磁盘持久化 + 向量索引双层架构，支撑跨会话记忆与 LLM-Wiki 知识回流。
4. **扩展引擎接入调度**：具身关系格式塔作为象思维临床模式接入；瓶颈诊断+压缩策略作为调度中枢组织治理层接入。
5. **双尺度治理落地**：个体认知尺度（任务级认知闭环）与组织治理尺度（系统级瓶颈压缩+红绿灯授权）以统一运行时实现。

文档遵循"现状→差距→目标→模块→接口→计划→测试→部署"的工程开发范式，为龙心OS从"理论+原型"走向"可运行系统"提供完整技术路线。

---

## 目录

- 第一章 开发概述：目标、范围与原则
- 第二章 架构设计：目标架构与模块划分
- 第三章 现状差距分析：代码基线审计
- 第四章 统一引擎协议：数据模型与接口契约
- 第五章 调度中枢设计：总智能体实现
- 第六章 五大引擎开发设计
- 第七章 扩展引擎接入设计：临床模式与组织治理
- 第八章 上下文与记忆系统设计
- 第九章 双尺度架构实现
- 第十章 三OS接口契约演进
- 第十一章 版本治理与配置管理
- 第十二章 开发计划与里程碑
- 第十三章 测试策略
- 第十四章 部署、分发与运维
- 附录A 术语表 / 附录B 现有代码文件索引 / 附录C 接口签名速查

---

# 第一章 开发概述：目标、范围与原则

## 1.1 开发目标

龙心OS开发设计的总目标：**将顶层设计中"1+5引擎认知操作系统"的理论蓝图，实现为一套可运行、可测试、可维护、可进化的认知引擎系统**。

具体目标分解为五层：

| 目标层级 | 目标描述 | 验收判据 |
|---------|---------|---------|
| T1 可运行 | 调度中枢能真实调用五大引擎并返回结构化结果 | `scheduler.run("...")` 返回含各引擎真实输出的 SchedulerResult |
| T2 可测试 | 每个引擎与调度中枢具备单元测试与集成测试 | 测试覆盖率 ≥ 80%，集成测试通过率 100% |
| T3 可维护 | 引擎以统一协议接入，新增引擎不改动调度中枢 | 新增引擎只需注册，无需修改 scheduler 核心逻辑 |
| T4 可进化 | 会话记忆持久化，支持跨会话复用与知识回流 | 重启后会话可恢复，高质量问答可回写知识库 |
| T5 可治理 | 双尺度治理落地：任务级认知闭环 + 系统级瓶颈压缩 | 组织治理层能识别瓶颈并输出压缩策略 |

## 1.2 开发范围

**本开发文档覆盖**：
- 调度中枢（`engines/调度中枢/`）的真实化改造
- 五大引擎（象思维/知识学习/五色光/人机协同/知行合一）的协议对齐与功能补全
- 三扩展引擎（具身格式塔/瓶颈诊断/瓶颈压缩）的接入
- 上下文管理器持久化与记忆系统
- 三OS接口契约的演进
- 双尺度治理运行时
- 版本治理、测试、部署

**本开发文档不覆盖**：
- 龙脑OS（思维模型库）内部实现——仅定义龙心→龙脑接口
- 龙爪OS（执行层）内部实现——仅定义龙心→龙爪接口
- 五行人格心理学OS 内部实现——已作为常驻子系统存在，仅维护接口
- 前端界面/CLI 交互层（另行立项）

## 1.3 设计原则

开发实现遵循六项原则（与顶层设计一脉相承，并增加工程约束）：

1. **契约先行**：先定义 `Engine` 协议与数据模型，再实现引擎，确保接口对齐。
2. **降级优先**：任何引擎不可用时，调度中枢优雅降级，绝不拖垮主流程。
3. **单一职责**：每个引擎只负责一个认知环节，调度中枢只负责路由。
4. **可观测性**：所有引擎输出带 `engine_id`/`status`/`models_used`，支持审计与复盘。
5. **持久化边界**：会话状态可持久化，引擎逻辑保持无状态（状态由上下文管理器持有）。
6. **版本可追溯**：引擎、契约、配置均纳入版本治理。

## 1.4 术语约定

| 术语 | 定义 |
|------|------|
| 引擎（Engine） | 实现 `Engine` 协议的认知组件，五大引擎+三扩展引擎 |
| 调度中枢（Scheduler） | 龙心OS 总智能体，负责任务分类、引擎路由、结果整合 |
| 任务上下文（TaskContext） | 一次认知任务的全部输入，含类型/层级/描述/关键词 |
| 引擎结果（EngineResult） | 引擎执行后的输出，含状态/内容/使用模型 |
| 调度结果（SchedulerResult） | 调度中枢聚合后的总输出 |
| 常驻子系统（Resident Subsystem） | 五行OS、龙爪OS 等在龙心调度下常驻的子系统 |
| 组织治理层（Governance Layer） | 瓶颈诊断+压缩+红绿灯授权组成的系统级治理运行时 |

---

# 第二章 架构设计：目标架构与模块划分

## 2.1 目标架构总览

```
┌────────────────────────────────────────────────────────────────────┐
│                        龙心OS 运行时（Runtime）                       │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  调度中枢 Scheduler（总智能体）                                │  │
│  │  classify → route → invoke → aggregate → feedback            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│              │                    │                   │             │
│  ┌───────────▼──────┐   ┌────────▼────────┐   ┌──────▼─────────┐   │
│  │  五大引擎层        │   │ 扩展引擎层       │   │ 组织治理层       │   │
│  │  (Engine协议)     │   │ (Engine协议)     │   │ (Governance)    │   │
│  │  象思维            │   │ 具身格式塔       │   │ 瓶颈诊断        │   │
│  │  知识学习          │   │ (象思维临床模式) │   │ 瓶颈压缩策略    │   │
│  │  五色光            │   │                 │   │ 红绿灯授权      │   │
│  │  人机协同          │   └─────────────────┘   │ (CP-01~06)     │   │
│  │  知行合一          │                          └────────────────┘   │
│  └───────────────────┘                                              │
│              │                    │                                  │
│  ┌───────────▼────────────────────▼──────────────────────────────┐  │
│  │  上下文与记忆层 Context & Memory                               │  │
│  │  会话上下文(持久化) · 长期知识库(LLM-Wiki回流) · 人在回路确认     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│              │                                                    │
│  ┌───────────▼──────────────────────────────────────────────────┐  │
│  │  三OS桥接层                                                    │  │
│  │  龙脑OS(选刃引擎·模型推荐) · 龙爪OS(执行工作流) · 五行OS(常驻)   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## 2.2 分层职责

| 层 | 职责 | 关键组件 | 依赖 |
|----|------|---------|------|
| 调度层 | 任务分类、引擎路由、结果整合、降级熔断 | Scheduler | 引擎层、记忆层、三OS桥接层 |
| 引擎层 | 具体认知操作（五大引擎+扩展引擎） | Engine 实例 | 方法论文档、自身状态 |
| 治理层 | 系统级瓶颈识别与压缩 | Governance | 引擎层、调度统计 |
| 记忆层 | 会话上下文、长期知识、人在回路 | ContextManager | 磁盘存储、向量索引 |
| 桥接层 | 三OS协作 | BrainOSBridge/ClawOSBridge/Resident | 龙脑/龙爪/五行 |

## 2.3 模块划分（目录结构目标）

```
龙心OS/
├── SKILL.md                      # 引擎总入口（现有）
├── 三OS接口契约.md                 # 契约文档（演进为 v2.0）
├── core/                         # [新增] 运行时核心
│   ├── protocol.py               # Engine 协议 + 数据模型
│   ├── registry.py               # 引擎注册表
│   ├── runtime.py                # 运行时装配
│   └── version.py                # 版本管理
├── engines/                      # 引擎目录（现有，改造）
│   ├── 调度中枢/                  # 总智能体（真实化改造）
│   │   ├── scheduler.py          # 调度核心（升级）
│   │   ├── context_manager.py    # 上下文（持久化升级）
│   │   ├── governance.py         # [新增] 组织治理层
│   │   └── subsystems/           # 常驻子系统（现有）
│   ├── 象思维/                    # 引擎（协议对齐 + 临床模式接入）
│   ├── 知识学习Skills/            # 引擎（协议对齐 + Wiki回流）
│   ├── 五色光思维/                # 引擎（协议对齐）
│   ├── 人机协同五象限/            # 引擎（协议对齐 + 治理接口）
│   ├── 知行合一/                  # 引擎（协议对齐）
│   ├── 具身关系格式塔引擎/          # 扩展引擎（临床模式注册）
│   ├── 串行瓶颈诊断引擎/           # 扩展引擎（治理层接入）
│   └── 瓶颈压缩策略引擎/           # 扩展引擎（治理层接入）
├── tests/                        # [新增] 测试目录
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── regression/               # 回归测试
├── runtime/                      # [新增] 运行时数据
│   ├── sessions/                 # 会话持久化 JSONL
│   ├── governance_logs/          # 治理日志
│   └── version.json              # 运行时版本状态
```

## 2.4 关键架构决策（ADR）

| ADR | 决策 | 理由 | 替代方案（否决） |
|----|------|------|----------------|
| ADR-01 | 引擎以 Python 协议（Protocol/ABC）统一接口 | 现有引擎均为 Python，协议化改造最小 | 独立微服务（过重，超出本地认知系统规模） |
| ADR-02 | 调度中枢动态加载引擎模块 | 新增引擎不改调度核心，可维护性 | 硬编码 if/elif（每次加引擎改调度） |
| ADR-03 | 会话持久化用 JSONL 文件 + 可选向量索引 | 简单可靠，人类可读，支持审计 | 数据库（引入外部依赖） |
| ADR-04 | 扩展引擎以"子模式/治理层"接入而非独立路由 | 保持1+5格局不变，符合顶层设计 | 扩展引擎独立路由（破坏1+5格局） |
| ADR-05 | 组织治理层以调度统计为输入，不侵入引擎内部 | 治理与执行解耦，引擎保持无状态 | 治理逻辑内嵌调度（耦合过紧） |

---

# 第三章 现状差距分析：代码基线审计

## 3.1 审计范围与方法

审计对象：`C:\Users\jia'yue\.agents\skills\10-kernel\龙心OS` 下全部 Python 与契约文档（2026-07-29 代码基线）。

审计方法：静态代码审查 + 契约对照（三OS接口契约 vs 实际实现）。

## 3.2 代码基线盘点

### 3.2.1 调度中枢（`engines/调度中枢/scheduler.py`，578 行）

**已具备的能力**：
- 任务分类 `classify_task`：基于关键词打分（8 种任务类型 JY/ZL/FA/WD/GT/XX/CZ/CY）
- 任务分层 `determine_task_level`：LIGHT/STANDARD/DEEP 三层动员
- 引擎选择 `determine_engines`：任务类型→引擎映射 + 层级扩围
- 龙脑OS 查询 `query_brain_os`：动态加载选刃引擎，含熔断器 CircuitBreaker
- 龙爪OS 派发 `dispatch_to_claw_os`：生成工作流计划
- 常驻子系统派发：五行OS/龙爪OS 深度共生
- 并发调度 `run_concurrent`：多线程
- 健康状态 `get_health_status`：心跳探针

**关键缺陷（GAP-01）**：
- `invoke_heart_engine()`（第362-371行）为 **stub 实现**——仅返回 `f"{engine_name}引擎处理完成"` 字符串，**并未真实调用五大引擎**。这意味着当前调度中枢的"引擎激活"是模拟的，五大引擎的 Python 类（象思维引擎、五色光引擎等）从未被调度中枢真正执行。
- 引擎选择 `determine_engines` 使用硬编码映射表，未从注册表读取。

### 3.2.2 上下文管理器（`engines/调度中枢/context_manager.py`，177 行）

**已具备的能力**：
- 会话创建/查询、轮次记录、人在回路确认级别（AUTO/NOTIFY/CONFIRM/APPROVE）
- 确认请求生成、偏好设置、会话摘要

**关键缺陷（GAP-02）**：
- `self.sessions` 为**纯内存 dict**，进程重启后全部丢失，无磁盘持久化
- 无向量索引/语义检索能力，无法支撑跨会话知识复用
- 未与 LLM-Wiki 知识回流打通

### 3.2.3 五大引擎（`engines/` 下各目录）

**已具备的能力**：
- 象思维：认知模式四步法+感知模式（观比体化）+象类型学（XiangSiWeiEngine）
- 五色光思维：五色引擎（五色光引擎.py）
- 人机协同五象限：五象限引擎（五象限引擎.py）
- 知识学习：十项指令（knowledge_learning.py）
- 知行合一：三阶段（action_knowledge.py）
- 均含 SKILL.md、references、triggers、templates、scripts

**关键缺陷（GAP-03）**：
- **无统一协议**：各引擎的 `run()` 签名、返回结构各不相同，调度中枢无法统一调用
- 大部分引擎的 Python 实现为"模板/规则"级别，输出格式化文本而非结构化数据
- 引擎之间无直接协作接口（如象思维→五色光的红光转译无代码支撑）

### 3.2.4 扩展引擎（`engines/` 下三目录）

**已具备的能力**：
- 具身关系格式塔：E0-E6 七态推断（gestalt_engine.py）
- 串行瓶颈诊断：瓶颈定位（bottleneck_diagnosis.py）
- 瓶颈压缩策略：CP 策略（bottleneck_compress.py）

**关键缺陷（GAP-04）**：
- **游离于调度之外**：三个扩展引擎的 Python 实现未接入调度中枢，与顶层设计"融入1+5格局"的目标不一致
- 具身格式塔未注册为象思维临床模式
- 瓶颈诊断/压缩未形成组织治理层

### 3.2.5 三OS接口契约（`三OS接口契约.md`，302 行）

**已具备的能力**：
- 龙心→龙脑（模型推荐）、龙心→龙爪（工作流）、龙爪→龙脑（步骤模型）
- 统一错误码 E000-E010、降级策略
- 五行OS 深度共生接口（v1.1/v1.2 演进）

**关键缺陷（GAP-05）**：
- 契约中定义的请求/返回结构（如 `GET_MODEL_RECOMMENDATION`）与实际 `scheduler.query_brain_os` 的实参（`format_output_with_context(bt, description)`）**传参不对齐**
- 契约文档描述与代码实现存在漂移，缺契约测试（Contract Test）

## 3.3 差距清单汇总

| 编号 | 差距 | 严重度 | 涉及模块 | 本开发文档对应章节 |
|------|------|--------|---------|------------------|
| GAP-01 | 心脏引擎调用桩化（五大引擎未被真实调用） | 严重 | scheduler.py | 第四、五章 |
| GAP-02 | 上下文管理器纯内存化 | 严重 | context_manager.py | 第八章 |
| GAP-03 | 引擎无统一协议，无法统一调用 | 严重 | 五大引擎 | 第四、六章 |
| GAP-04 | 扩展引擎游离调度之外 | 高 | 三扩展引擎 | 第七章 |
| GAP-05 | 契约传参与实现不对齐 | 高 | 三OS接口契约 | 第十章 |
| GAP-06 | 版本治理缺失 | 中 | 全局 | 第十一章 |

## 3.4 风险与优先级

| 风险 | 影响 | 缓解策略 |
|------|------|---------|
| GAP-01/GAP-03 为结构性差距，改造涉及面广 | 改造期调度中枢功能回退 | 采用"协议适配器"渐进改造：先定义协议，再逐个引擎适配，最后切换调度调用点 |
| 现有引擎的模板输出依赖 | 真实化后输出形态变化 | 保留 `format_text()` 兼容层，新增 `run_structured()` 结构化输出 |
| 测试基线薄弱 | 改造引入回归 | 先补集成测试（对现状行为做快照），再改造 |

---

# 第四章 统一引擎协议：数据模型与接口契约

## 4.1 设计目标

统一引擎协议的目标：**让调度中枢以同一方式调用所有引擎，引擎之间以同一结构交换数据**，弥合 GAP-03。

## 4.2 核心数据模型

### 4.2.1 TaskContext（任务上下文）

```python
@dataclass
class TaskContext:
    task_type: TaskType        # JY/ZL/FA/WD/GT/XX/CZ/CY
    task_level: TaskLevel      # LIGHT/STANDARD/DEEP
    description: str           # 用户原始输入
    domain: str = ""           # 领域（味藏餐饮等）
    urgency: str = "medium"    # high/medium/low
    keywords: List[str] = field(default_factory=list)
    context: dict = field(default_factory=dict)  # 扩展上下文（会话引用等）
```

### 4.2.2 EngineResult（引擎结果）

```python
@dataclass
class EngineResult:
    engine_id: str             # 引擎唯一标识（如 "xiang_si_wei"）
    status: str                # ok / degraded / failed / circuit_open
    output: Any = None         # 结构化输出（引擎特定）
    text: str = ""             # 人类可读摘要（供整合展示）
    error: Optional[str] = None
    models_used: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    confidence: float = 0.0    # 置信度（治理层与审计用）
```

### 4.2.3 SchedulerResult（调度结果）

```python
@dataclass
class SchedulerResult:
    task_id: str
    task_type: TaskType
    task_level: TaskLevel
    engines_activated: List[str]
    heart_engine_results: Dict[str, EngineResult]
    governance_result: Optional[GovernanceResult] = None   # [新增] 治理层输出
    brain_os_result: Optional[EngineResult] = None
    claw_os_result: Optional[EngineResult] = None
    resident_results: Optional[dict] = None
    final_output: Any = None
    status: str = "completed"
    error: Optional[str] = None
```

### 4.2.4 GovernanceResult（治理层结果）— 新增

```python
@dataclass
class GovernanceResult:
    bottlenecks: List[Bottleneck]      # 识别出的瓶颈（INF/DEC/CRD/CTX）
    compression_plan: List[str]        # CP-01~06 压缩策略
    traffic_light: str                 # green/yellow/red 红绿灯授权
    recommendation: str                # 治理建议文本
```

### 4.2.5 Bottleneck（瓶颈）— 新增

```python
@dataclass
class Bottleneck:
    kind: str            # BN-INF / BN-DEC / BN-CRD / BN-CTX
    stage: str           # 所属认知环节（input/process/output）
    severity: float      # 0~1 严重度
    evidence: str        # 证据描述
    suggested_policy: str  # 建议策略编号 CP-01~06
```

## 4.3 Engine 协议（接口契约）

### 4.3.1 协议定义

```python
class Engine(ABC):
    """引擎协议：所有引擎必须实现以下接口。"""

    @property
    @abstractmethod
    def engine_id(self) -> str:
        """引擎唯一标识，与调度注册表一致。"""

    @abstractmethod
    def run(self, task_ctx: TaskContext) -> EngineResult:
        """执行认知操作，返回结构化结果。

        实现要求：
        1. 必须以 try/except 包裹核心逻辑，失败时返回 status="failed" 而非抛异常
        2. 必须填充 engine_id、status、output、text
        3. 尽量填充 models_used 与 confidence（供审计与治理层）
        4. 不得修改 task_ctx（只读），状态写入由调用方持久化
        """

    def capability(self) -> List[str]:
        """声明引擎能力标签，供调度中枢路由参考（可选）。"""
        return []
```

### 4.3.2 引擎适配策略

对现有五大引擎，**不重写其认知逻辑**，而是新增协议适配层：

```
engines/<引擎名>/
├── 原引擎类.py        # 保留现有认知逻辑（不动）
├── engine_adapter.py  # [新增] 实现 Engine 协议，包装原引擎类
└── SKILL.md
```

适配层示例（象思维）：

```python
from core.protocol import Engine, TaskContext, EngineResult

class XiangSiWeiAdapter(Engine):
    @property
    def engine_id(self) -> str:
        return "xiang_si_wei"

    def __init__(self):
        from 象思维引擎 import XiangSiWeiEngine
        self._inner = XiangSiWeiEngine()

    def run(self, task_ctx: TaskContext) -> EngineResult:
        try:
            result = self._inner.run(task_ctx.description)
            return EngineResult(
                engine_id="xiang_si_wei",
                status="ok",
                output={
                    "xiang_type": result.xiang_type.value,
                    "cognition_steps": [s.name for s in result.cognition],
                    "perception_steps": [s.name for s in result.perception],
                    "insight": result.insight,
                },
                text=self._inner.format_text(result),
                models_used=["象思维四步法", "观比体化"],
            )
        except Exception as e:
            return EngineResult(engine_id="xiang_si_wei", status="failed", error=str(e))
```

## 4.4 引擎注册表（Registry）

```python
# core/registry.py
ENGINE_REGISTRY: Dict[str, type] = {
    # 五大引擎
    "xiang_si_wei":      "engines.象思维.engine_adapter.XiangSiWeiAdapter",
    "knowledge_learning": "engines.知识学习Skills.engine_adapter.KnowledgeLearningAdapter",
    "five_color":        "engines.五色光思维.engine_adapter.FiveColorAdapter",
    "human_machine":     "engines.人机协同五象限.engine_adapter.HumanMachineAdapter",
    "action_knowledge":  "engines.知行合一.engine_adapter.ActionKnowledgeAdapter",
    # 扩展引擎
    "gestalt":           "engines.具身关系格式塔引擎.engine_adapter.GestaltAdapter",
    "bottleneck_diag":   "engines.串行瓶颈诊断引擎.engine_adapter.BottleneckDiagAdapter",
    "bottleneck_compress": "engines.瓶颈压缩策略引擎.engine_adapter.BottleneckCompressAdapter",
}

def get_engine(engine_id: str) -> Engine:
    """延迟加载引擎实例（import_string + 实例化）。"""
```

注册表设计要点：
- **字符串路径延迟导入**：调度中枢不直接 import 引擎类，通过字符串路径在运行时加载——新增引擎只需在注册表加一行
- **实例缓存**：同一引擎复用单例，避免重复实例化

## 4.5 错误处理与降级（统一）

引擎层错误处理统一遵循三OS契约的错误码语义，并补充引擎级规范：

| 场景 | EngineResult.status | 错误信息 | 调度中枢动作 |
|------|--------------------|---------|-------------|
| 引擎正常 | ok | — | 正常聚合 |
| 引擎内部异常 | failed | str(e) | 记入熔断器，触发降级/备选引擎 |
| 引擎未注册 | failed | "engine not registered" | 记录并跳过 |
| 引擎超时 | failed | "timeout" | 重试1次后跳过 |

---

---

# 第五章 调度中枢设计：总智能体实现

## 5.1 调度中枢职责（最终态）

调度中枢是龙心OS总智能体，承担六项职责：

1. **意图识别**：将用户输入分类为任务类型（8类）
2. **分层动员**：按任务层级决定引擎动员深度（LIGHT/STANDARD/DEEP）
3. **引擎路由**：从注册表选择并调用引擎
4. **龙脑/龙爪协同**：向龙脑OS查询模型推荐，向龙爪OS派发执行
5. **常驻子系统派发**：五行OS、龙爪OS深度共生
6. **结果整合与治理**：聚合引擎输出 + 组织治理层反馈

## 5.2 调度主流程（升级后 run()）

```
run(description, urgency, keywords)
│
├─ 1. classify_task()            # 意图识别（规则评分，保留现状）
├─ 2. determine_task_level()     # 分层动员（保留现状）
├─ 3. query_brain_os()           # 龙脑模型推荐（保留现状+契约对齐）
├─ 4. determine_engines()        # 引擎路由（改为从注册表解析）
├─ 5. invoke_engines()           # [改造] 真实调用五大引擎
│     for engine_id in engines:
│         engine = registry.get_engine(engine_id)
│         result = engine.run(task_ctx)      # ← 真实调用，替代 stub
│         heart_engine_results[engine_id] = result
│         if failed → 熔断 + 备选引擎
├─ 6. dispatch_to_claw_os()      # 龙爪执行（保留现状）
├─ 7. dispatch_resident()        # 常驻子系统（保留现状）
├─ 8. run_governance()           # [新增] 组织治理层
│     瓶颈诊断（BN-INF/DEC/CRD/CTX）
│     → 瓶颈压缩（CP-01~06）→ 红绿灯授权
├─ 9. aggregate()                # 结果整合 + 持久化会话
└─ 10. return SchedulerResult
```

## 5.3 invoke_engines 真实化改造（GAP-01 解决方案）

### 5.3.1 现状问题

现有 `invoke_heart_engine()` 仅返回字符串占位，五大引擎的 Python 类从未被执行。这是当前调度中枢最严重的差距。

### 5.3.2 改造方案

```python
def invoke_engines(self, task_ctx: TaskContext,
                   engine_ids: List[str]) -> Dict[str, EngineResult]:
    results: Dict[str, EngineResult] = {}
    for engine_id in engine_ids:
        try:
            engine = get_engine(engine_id)          # 注册表延迟加载
            if engine is None:
                results[engine_id] = EngineResult(engine_id=engine_id,
                                                  status="failed",
                                                  error="engine not registered")
                continue
            result = engine.run(task_ctx)           # 真实执行
            results[engine_id] = result
        except Exception as e:
            results[engine_id] = EngineResult(engine_id=engine_id,
                                              status="failed", error=str(e))
    return results
```

### 5.3.3 降级与备选（保留现有熔断思想）

- 任一引擎 `failed` → 尝试备选引擎（依据 `FALLBACK_MAP`）
- 全部引擎不可用 → 返回基础兜底输出（"建议使用五层分析法"等），状态置 `degraded`

```python
FALLBACK_MAP = {
    "xiang_si_wei":       ["five_color"],
    "knowledge_learning": ["xiang_si_wei"],
    "five_color":         ["human_machine"],
    "human_machine":      ["xiang_si_wei"],
    "action_knowledge":   ["knowledge_learning"],
}
```

## 5.4 引擎路由升级（GAP-01 配套）

`determine_engines` 由硬编码映射改为 **注册表 + 任务类型映射**：

```python
def determine_engines(self, task_type: TaskType, level: TaskLevel) -> List[str]:
    base = TASK_ENGINE_MAP.get(task_type, ["xiang_si_wei"])[:]
    if level == TaskLevel.DEEP:
        return list(ENGINE_REGISTRY.keys())[:5]   # 五大引擎全动员
    if level == TaskLevel.STANDARD and len(base) < 2:
        base.append("five_color")
    return [eid for eid in base if eid in ENGINE_REGISTRY]  # 过滤未注册
```

要点：返回的引擎 ID 必须存在于注册表，未注册的自动过滤，避免调用失败。

## 5.5 调度中枢兼容性策略

为降低改造风险，调度中枢采用**双轨输出**：

- `heart_engine_results`：新协议的结构化结果（EngineResult）
- `legacy_summary`：兼容旧调用的文本摘要（拼接各引擎 text 字段）

这样既满足新协议，又保留现有调用方的兼容。

---

# 第六章 五大引擎开发设计

本章逐一给出五大引擎的协议适配与功能补全设计。统一采用"现状→协议适配→功能补全"三段式。

## 6.1 象思维引擎

### 6.1.1 现状

`象思维引擎.py`（114行）实现：认知模式四步法（取象→类比→体悟→运化）、感知模式（观比体化）、象类型学（无象/有象/意象/道象）。输出为格式化文本。

### 6.1.2 协议适配

- 新增 `engine_adapter.py` 实现 `Engine` 协议（见第四章示例）
- `output` 结构化：`xiang_type` / `cognition_steps` / `perception_steps` / `insight`
- `models_used = ["象思维四步法", "观比体化"]`

### 6.1.3 功能补全

| 补全项 | 说明 | 优先级 |
|--------|------|--------|
| 象类型自动推断 | 从描述关键词推断象态（无象/有象/意象/道象），替代默认 YOU | P1 |
| 洞察生成增强 | 基于认知步骤产物生成可落地的意象建议（非固定模板） | P1 |
| 临床模式注册 | 接入具身关系格式塔作为"临床模式"子路由（见第七章） | P1 |
| 结果置信度 | 对象态推断输出置信度（供治理层） | P2 |

## 6.2 知识学习引擎

### 6.2.1 现状

`knowledge_learning.py` 实现十项认知指令框架。目录含 SKILL.md、test-cases.md。

### 6.2.2 协议适配

- 新增 `engine_adapter.py`
- `output` 结构化：`steps_applied`（应用的指令）/ `extracted_entities` / `concepts` / `relations`
- `models_used`：按实际应用的指令集填写

### 6.2.3 功能补全

| 补全项 | 说明 | 优先级 |
|--------|------|--------|
| 十指令流水线 | 将剖析→解构→透视→阐释→推演→思辨→溯源→融合→启发→映射实现为可调用流水线（当前为框架） | P0 |
| 易经卦变整合 | 将本卦/变卦/互卦/错卦/综卦/杂卦映射到指令子流程 | P1 |
| LLM-Wiki 回流 | 编译产物写回知识库（raw 只读 / wiki 可写），实现"机器编译、人类审核" | P1 |
| 结构化 JSON | 输出含实体、概念、关系、谱系的 JSON 结构 | P0 |

## 6.3 五色光思维引擎

### 6.3.1 现状

`五色光引擎.py` 实现五色引擎。含 CHECKLIST/COMPLETION_REPORT、triggers。

### 6.3.2 协议适配

- 新增 `engine_adapter.py`
- `output` 结构化：`selected_sequence` / `per_color_output` / `decision`
- `models_used`：按使用的颜色序列

### 6.3.3 功能补全

| 补全项 | 说明 | 优先级 |
|--------|------|--------|
| 序列库 | 内置经典序列（问题分析/决策制定/创意激发/危机处理/战略规划/冲突解决） | P0 |
| 主持人机制 | 无色主持人角色：序列控制、时间管理、纠偏话术 | P1 |
| 单色聚焦校验 | 校验当前输出是否偏离当前颜色的思维模式 | P2 |
| 五行映射 | 白=金/红=火/黄=土/绿=木/蓝=水（工具谱系，权威映射） | P1 |
| 红绿灯协同 | 与人机协同治理层的红绿灯授权联动 | P2 |

## 6.4 人机协同五象限引擎

### 6.4.1 现状

`五象限引擎.py` 实现五象限模型。含 references（theory/sop/prompts/practice-guide）。

### 6.4.2 协议适配

- 新增 `engine_adapter.py`
- `output` 结构化：`quadrant`（Q1-Q5）/ `human_role` / `ai_role` / `collaboration_plan`
- `models_used`：协作协议相关模型

### 6.4.3 功能补全

| 补全项 | 说明 | 优先级 |
|--------|------|--------|
| 象限判定 | 基于人知/不知×AI知/不知四要素打分判定象限 | P0 |
| 治理接口 | 提供组织治理层所需的瓶颈证据接口（供Governance采集） | P1 |
| SECI映射 | 输出含SECI阶段标注（社外化/外化/组合/内化） | P2 |

## 6.5 知行合一引擎

### 6.5.1 现状

`action_knowledge.py` 实现三阶段模型（表示空间→压缩→泛化）。

### 6.5.2 协议适配

- 新增 `engine_adapter.py`
- `output` 结构化：`stage`（表示空间/压缩/泛化）/ `representation` / `principles` / `applications`
- `models_used`：对应知识学习指令

### 6.5.3 功能补全

| 补全项 | 说明 | 优先级 |
|--------|------|--------|
| 双螺旋闭环 | 每次执行后反馈回表示空间，形成进化闭环 | P0 |
| 与知识学习联动 | 泛化阶段的输入自动路由到知识学习编译产物 | P1 |
| 反馈持久化 | 实践反馈写入会话记忆，支撑跨会话进化 | P1 |

## 6.6 五大引擎统一规范

所有引擎实现必须遵守：

1. `run()` 不抛异常（内部捕获，返回 failed 状态）
2. `output` 为可 JSON 序列化结构
3. `text` 为人类可读摘要（供整合层展示）
4. `models_used` 声明使用的模型/方法（审计与治理依据）
5. 状态无持久化（状态由 ContextManager 持有）

---

---

# 第七章 扩展引擎接入设计：临床模式与组织治理

本章落实顶层设计第三章的融入方案：三个扩展引擎不改变1+5格局，分别以"临床模式"与"组织治理层"接入（解决 GAP-04）。

## 7.1 接入架构总览

```
调度中枢 Scheduler
│
├── 五大引擎路由（个体认知尺度）
│     ├── 象思维 ──── 子模式: 具身关系格式塔（临床模式·E0-E6）
│     ├── 知识学习 ──── └─ LLM-Wiki回流
│     ├── 五色光
│     ├── 人机协同 ──── 提供治理证据
│     └── 知行合一
│
└── 组织治理层 Governance（系统级尺度）
      ├── 串行瓶颈诊断（BN-INF/BN-DEC/BN-CRD/BN-CTX）
      ├── 瓶颈压缩策略（CP-01~06）
      └── 红绿灯授权（green/yellow/red）
```

## 7.2 具身关系格式塔 → 象思维临床模式

### 7.2.1 设计目标

将 `gestalt_engine.py`（E0-E6 七态推断）注册为象思维引擎的"临床模式"，使象思维从"意象把握"扩展为"关系在场感知"。

### 7.2.2 接入机制

**方案A（推荐）：子模式路由**——象思维适配器内部持有格式塔引擎，当任务上下文标记 `mode="clinical"` 时调用临床流程：

```python
class XiangSiWeiAdapter(Engine):
    def run(self, task_ctx: TaskContext) -> EngineResult:
        if task_ctx.context.get("mode") == "clinical":
            return self._run_clinical(task_ctx)   # 临床模式
        return self._run_cognitive(task_ctx)      # 默认认知模式

    def _run_clinical(self, task_ctx: TaskContext) -> EngineResult:
        gestalt = GestaltEngine()
        g = gestalt.run(task_ctx.description)
        # 临床四步：起手观象→场域全息→微扰动→体化印证
        return EngineResult(
            engine_id="xiang_si_wei",
            status="ok",
            output={
                "mode": "clinical",
                "gestalt_state": g.state_label,          # E0-E6
                "profile": g.profile.description,
                "suggested_action": g.profile.suggested_action,
                "transition_path": [s.label for s in g.transition_path],
            },
            text=f"【临床模式】场域状态：{g.state_label}｜{g.profile.suggested_action}",
            models_used=["具身关系格式塔", "E0-E6样态"],
        )
```

### 7.2.3 临床模式触发条件

| 触发信号 | 说明 |
|---------|------|
| 任务关键词含"感受/氛围/关系/场域/状态/情绪" | 关系性感知场景 |
| 任务上下文 mode="clinical" | 显式指定 |
| 前一轮结果含情感维度 | 连续会话中承接情感线索 |

### 7.2.4 数据模型对齐

格式塔 E0-E6 状态映射为象思维象态的深化：

| 格式塔状态 | 象思维象态 | 语义 |
|-----------|-----------|------|
| E0 未分化 | 无象 | 混沌未显 |
| E1-E2 感知锚定/关系涌现 | 有象 | 具体可感 |
| E3-E4 样态分化/反身觉知 | 意象 | 意蕴渐显 |
| E5-E6 整合重构/场域共振 | 道象 | 合道之象 |

## 7.3 瓶颈诊断 + 瓶颈压缩 → 组织治理层

### 7.3.1 设计目标

将 `bottleneck_diagnosis.py` 与 `bottleneck_compress.py` 组合为调度中枢的**组织治理层**（Governance），实现系统级瓶颈识别与压缩。

### 7.3.2 治理层实现（governance.py）

```python
class Governance:
    """组织治理层：瓶颈诊断 → 压缩策略 → 红绿灯授权。"""

    def __init__(self, diagnosis_engine, compress_engine):
        self.diag = diagnosis_engine      # 串行瓶颈诊断引擎
        self.compress = compress_engine   # 瓶颈压缩策略引擎

    def run(self, task_ctx: TaskContext,
            engine_results: Dict[str, EngineResult],
            session_stats: dict) -> GovernanceResult:
        # 1. 瓶颈诊断：结合引擎结果与调度统计识别瓶颈
        bottlenecks = self._detect_bottlenecks(engine_results, session_stats)
        # 2. 压缩策略：对每个瓶颈生成 CP-01~06 策略
        plan = self._generate_plan(bottlenecks)
        # 3. 红绿灯授权：综合任务层级与瓶颈严重度
        light = self._decide_traffic_light(task_ctx, bottlenecks)
        return GovernanceResult(
            bottlenecks=bottlenecks,
            compression_plan=plan,
            traffic_light=light,
            recommendation=self._compose_recommendation(bottlenecks, plan, light),
        )

    def _detect_bottlenecks(self, results, stats) -> List[Bottleneck]:
        """四类瓶颈检测：
        BN-INF：信息供给不足/过载 → 引擎输入缺失、知识库命中低
        BN-DEC：决策环节耗时 → 任务层级高但引擎输出迟疑
        BN-CRD：信任缺失 → 常驻子系统未命中、用户二次确认多
        BN-CTX：上下文断层 → 会话跨度大、知识未回流
        """
        # 实际实现调用 diagnosis_engine.run(...)，此处为设计说明
        return self.diag.analyze(results, stats)

    def _decide_traffic_light(self, task_ctx, bottlenecks) -> str:
        if task_ctx.task_level == TaskLevel.DEEP:
            return "red"          # 深度任务：人类全权
        if any(b.severity > 0.7 for b in bottlenecks):
            return "yellow"       # 严重瓶颈：人机协同
        return "green"            # 常规任务：AI自主
```

### 7.3.3 红绿灯授权语义

| 灯 | 授权范围 | 人类职责 | AI职责 |
|----|---------|---------|--------|
| 绿 | AI自主执行 | 事后抽查 | 全流程执行 |
| 黄 | 人机协同 | 关键节点把关 | 常规推进 |
| 红 | 人类全权 | 决策拍板 | 参谋建议 |

### 7.3.4 治理层触发时机

- **每轮任务**：轻量治理（仅记录统计）
- **会话结束**：深度治理（产出治理报告）
- **定时心跳**：全系统治理（扫描跨会话瓶颈）

## 7.4 扩展引擎接入验证标准

| 验证项 | 判据 |
|--------|------|
| 临床模式 | `scheduler.run("团队氛围紧张，帮我感受下", context={"mode":"clinical"})` 返回含 gestalt_state 的结果 |
| 治理层 | `scheduler.run("...")` 返回 SchedulerResult.governance_result 含 bottlenecks+traffic_light |
| 1+5格局 | 调度激活列表仍为五大引擎（扩展引擎不单独计入 engines_activated） |

---

# 第八章 上下文与记忆系统设计

## 8.1 设计目标

将上下文管理器从纯内存升级为**持久化 + 可检索**的记忆系统（解决 GAP-02），并打通 LLM-Wiki 知识回流，实现"越用越聪明"。

## 8.2 三层记忆架构

```
┌──────────────────────────────────────────────┐
│  L1 会话上下文（短期）                          │
│  当前会话轮次、正在进行的任务、临时偏好           │
│  存储：runtime/sessions/<session_id>.jsonl     │
├──────────────────────────────────────────────┤
│  L2 跨会话记忆（中期）                          │
│  历史会话摘要、长期偏好、已确认决策               │
│  存储：runtime/memories/<persona>.json          │
├──────────────────────────────────────────────┤
│  L3 长期知识库（长期·LLM-Wiki三层）              │
│  raw（只读原文）/ wiki（LLM编译）/ schema（规则）│
│  存储：知识库目录（三层架构）                    │
└──────────────────────────────────────────────┘
```

## 8.3 会话上下文持久化（GAP-02 解决方案）

### 8.3.1 存储设计

```python
class PersistentContextManager:
    def __init__(self, base_dir: str = "runtime/sessions"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _path(self, session_id: str) -> str:
        safe_id = session_id.replace("/", "_")
        return os.path.join(self.base_dir, f"{safe_id}.jsonl")

    def add_turn(self, session_id: str, turn: dict) -> None:
        with open(self._path(session_id), "a", encoding="utf-8") as f:
            f.write(json.dumps(turn, ensure_ascii=False) + "\n")

    def load_session(self, session_id: str) -> List[dict]:
        path = self._path(session_id)
        if not os.path.exists(path):
            return []
        with open(path, encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def summarize(self, session_id: str, last_n: int = 10) -> str:
        """生成会话摘要（供跨会话记忆注入）"""
        turns = self.load_session(session_id)[-last_n:]
        return "\n".join(f"[{t['task_type']}] {t['query'][:80]} → {t.get('summary','')[:100]}"
                         for t in turns)
```

### 8.3.2 迁移策略

现有 `ContextManager` 保留内存 API，新增持久化后端，通过 `storage_backend` 参数切换：

```python
class ContextManager:
    def __init__(self, storage: str = "memory"):   # memory | persistent
        self.memory = PersistentContextManager() if storage == "persistent" else None
```

## 8.4 人在回路确认（保留并增强）

现有确认级别 AUTO/NOTIFY/CONFIRM/APPROVE 保留，增强：

1. **确认记录持久化**：确认历史写入会话文件，供审计
2. **红绿灯联动**：APPROVE 级任务（深度决策）自动映射为治理层"红灯"授权
3. **确认话术模板化**：不同任务类型使用差异化确认文案

## 8.5 LLM-Wiki 知识回流设计

### 8.5.1 回流链路

```
知识学习引擎编译产物
    │
    ├──→ wiki 层（LLM可写）：实体/概念/关系页面
    │       └── 人类审核（通过率>80%目标）
    ├──→ raw 层（只读）：原文备份 + 元数据
    └──→ 索引更新：双向链接网络刷新
```

### 8.5.2 回流实现

```python
def flow_to_wiki(engine_result: EngineResult, wiki_store) -> dict:
    """将知识学习引擎的编译产物回流知识库 wiki 层。"""
    if engine_result.engine_id != "knowledge_learning":
        return {"flowed": False, "reason": "非知识学习引擎输出"}
    entities = engine_result.output.get("extracted_entities", [])
    concepts = engine_result.output.get("concepts", [])
    relations = engine_result.output.get("relations", [])
    # 生成实体/概念页面，建立双向链接，写入 wiki 层待审核队列
    return wiki_store.ingest_candidates(
        entities=entities, concepts=concepts, relations=relations,
        source=engine_result.output.get("source", ""),
    )
```

### 8.5.3 回流触发

- **触发点**：知识学习引擎成功完成编译任务后
- **闸门**：质量门槛（实体完整、来源可溯）通过后进入待审队列
- **复利效应**：每次查询的高质量问答写回 wiki，越用越聪明

## 8.6 记忆系统验收标准

| 验证项 | 判据 |
|--------|------|
| 会话持久化 | 进程重启后 load_session 返回历史轮次 |
| 跨会话摘要 | summarize 输出可注入新会话上下文 |
| 知识回流 | 知识学习任务后 wiki 层新增待审候选 |
| 确认可审计 | 确认历史可从会话文件追溯 |

---

---

# 第九章 双尺度架构实现

## 9.1 双尺度运行时设计

顶层设计第四章提出"个体认知尺度×组织治理尺度"双尺度架构。本章给出运行时实现。

```
调度中枢 run()
│
├── 尺度一·个体认知（任务级闭环）
│     classify → route → invoke_engines → aggregate → persist
│     （对应认知闭环：知→创→决→协→行）
│
└── 尺度二·组织治理（系统级优化）
      治理层采集各轮调度统计
      → 瓶颈识别（BN-INF/DEC/CRD/CTX）
      → 瓶颈压缩（CP-01~06）
      → 红绿灯授权（green/yellow/red）
      → 策略回写运行时（影响后续路由）
```

## 9.2 个体认知尺度实现

### 9.2.1 认知环节→引擎映射（运行时）

| 认知环节 | 引擎 | 运行时实现 |
|---------|------|-----------|
| 知 | 象思维 | `get_engine("xiang_si_wei").run(task_ctx)` |
| 创 | 知识学习 | `get_engine("knowledge_learning").run(task_ctx)` |
| 决 | 五色光 | `get_engine("five_color").run(task_ctx)` |
| 协 | 人机协同 | `get_engine("human_machine").run(task_ctx)` |
| 行 | 知行合一 | `get_engine("action_knowledge").run(task_ctx)` |

### 9.2.2 快速通道（引擎间协作）

顶层设计识别出四条引擎快速通道，运行时以"链式任务"实现：

```
链式任务示例：象思维→五色光（0→1→1→N）
1. xiang_result = get_engine("xiang_si_wei").run(task_ctx)
2. five_ctx = clone(task_ctx); five_ctx.context["seed_insight"] = xiang_result.output["insight"]
3. five_result = get_engine("five_color").run(five_ctx)
```

`clone()` 复制任务上下文并注入前置引擎输出，实现引擎间数据传递。

## 9.3 组织治理尺度实现

### 9.3.1 治理数据采集

调度中枢每轮任务向治理层写入调度统计：

```python
def _collect_governance_stats(self, task_ctx, engine_results, session) -> dict:
    return {
        "task_count": self._task_counter,          # 累计任务数
        "engine_latency": {k: v.duration_seconds for k, v in engine_results.items()},
        "engine_failures": {k: v.status for k, v in engine_results.items()},
        "session_turns": session.total_turns,       # 会话跨度
        "resident_hits": self._resident_hit_count,  # 常驻子系统命中
        "confirm_requests": self._confirm_count,    # 人类确认次数
    }
```

### 9.3.2 四类瓶颈的运行时判定

| 瓶颈 | 运行时信号 | 判定逻辑 |
|------|-----------|---------|
| BN-INF | 引擎输出为空、知识库命中低、输入描述过短 | 信息供给不足 |
| BN-DEC | 深度任务占比高、决策类任务多轮未决、确认请求多 | 决策环节拥堵 |
| BN-CRD | 常驻子系统命中率低、引擎失败率高、二次确认多 | 人机信任缺失 |
| BN-CTX | 会话跨度大、跨会话知识未复用、上下文注入缺失 | 上下文断层 |

### 9.3.3 治理闭环

```
治理统计 → 瓶颈识别 → 压缩策略 → 策略生效
     ↑                                    │
     └──── 下一轮统计反馈（闭环）────────────┘
```

策略生效方式：
- **CP-01 信息前置**：治理层建议知识学习引擎提前编译该领域材料
- **CP-02 决策红绿灯**：深度任务自动触发"红灯"人工确认
- **CP-03 信任校准**：降低高失败率引擎的路由权重，提升稳定引擎权重
- **CP-04 上下文池化**：跨会话摘要自动注入新会话上下文

## 9.4 双尺度联动机制

两尺度通过两个运行时组件联动：

1. **治理日志（governance_logs/）**：个体任务的统计沉淀为治理层输入
2. **路由权重（runtime/version.json）**：治理层策略反写路由权重，影响后续任务

```
个体任务统计 ──→ 治理层 ──→ 策略 ──→ 路由权重 ──→ 后续个体任务
   （微观观测）   （宏观诊断） （治理决策） （宏观策略落地）  （微观执行）
```

---

# 第十章 三OS接口契约演进

## 10.1 契约演进目标

解决 GAP-05（契约传参与实际实现不对齐），使三OS接口契约从"设计文档"变为"可验证的契约"。

## 10.2 契约 v2.0 主要变更

### 10.2.1 引擎级契约（新增，核心）

新增龙心OS内部"调度中枢↔引擎"契约，纳入三OS契约文档：

```
请求：ENGINE_INVOKE
{
  "engine_id": "xiang_si_wei|knowledge_learning|five_color|human_machine|action_knowledge|gestalt|bottleneck_diag|bottleneck_compress",
  "task": {
    "task_type": "JY|ZL|FA|WD|GT|XX|CZ|CY",
    "task_level": "light|standard|deep",
    "description": "用户输入",
    "domain": "领域",
    "context": {"mode": "clinical"}   // 扩展
  }
}

返回：ENGINE_RESULT
{
  "engine_id": "...",
  "status": "ok|degraded|failed|circuit_open",
  "output": { ... },                  // 引擎结构化输出
  "text": "人类可读摘要",
  "models_used": ["模型1", "模型2"],
  "confidence": 0.85,
  "duration_seconds": 1.2
}
```

### 10.2.2 治理层契约（新增）

```
请求：GOVERNANCE_RUN
{
  "task_level": "standard",
  "engine_results": {...},
  "session_stats": {...}
}

返回：GOVERNANCE_RESULT
{
  "bottlenecks": [
    {"kind": "BN-CTX", "stage": "input", "severity": 0.8,
     "evidence": "会话跨度大", "suggested_policy": "CP-04"}
  ],
  "compression_plan": ["CP-04 上下文池化"],
  "traffic_light": "yellow",
  "recommendation": "建议注入跨会话摘要"
}
```

### 10.2.3 契约对齐策略

现有 `query_brain_os` 实际调用 `format_output_with_context(bt, description)`，与文档 `GET_MODEL_RECOMMENDATION` 的结构不一致。对齐策略：

1. **保留实际接口**：`format_output_with_context` 作为龙脑引擎的真实 API
2. **契约适配层**：新增 `contract_adapter.py`，将实际返回转换为契约定义的结构
3. **契约测试**：新增 Contract Test，验证实际返回满足契约 schema（见第十三章）

## 10.3 契约文档结构（v2.0）

```
三OS接口契约.md v2.0
├── 一、总体架构
├── 二、龙心→龙脑（保留+适配层说明）
├── 三、龙心→龙爪（保留）
├── 四、龙爪→龙脑（保留）
├── 五、统一错误码（保留）
├── 六、龙心→五行OS（保留）
├── 七、龙心→引擎（新增·本章 10.2.1）
├── 八、治理层契约（新增·本章 10.2.2）
└── 九、契约测试与验证（新增）
```

## 10.4 兼容性策略

- **向后兼容**：v2.0 保留 v1.x 全部既有接口，新增接口不破坏旧调用
- **版本字段**：所有请求/返回增加 `version` 字段，支持运行时协商
- **弃用周期**：旧接口标注 deprecated 后保留两个版本周期

---

# 第十一章 版本治理与配置管理

## 11.1 版本治理目标

解决 GAP-06（版本治理缺失），建立引擎、契约、配置的统一版本管理。

## 11.2 版本层级

| 层级 | 对象 | 版本标识 | 示例 |
|------|------|---------|------|
| L1 | 龙心OS 整体 | 语义化版本 | v8.1.0 |
| L2 | 调度中枢 | 语义化版本 | v2.0.0 |
| L3 | 引擎 | 语义化版本 | v1.2.0 |
| L4 | 接口契约 | 语义化版本 | v2.0.0 |
| L5 | 知识库数据 | 时间戳+哈希 | 2026-07-31-a3f2 |

## 11.3 版本信息结构（runtime/version.json）

```json
{
  "longxin_os": "8.1.0",
  "scheduler": "2.0.0",
  "engines": {
    "xiang_si_wei": "1.2.0",
    "knowledge_learning": "1.1.0",
    "five_color": "1.2.0",
    "human_machine": "1.1.0",
    "action_knowledge": "1.1.0",
    "gestalt": "1.1.0",
    "bottleneck_diag": "1.1.0",
    "bottleneck_compress": "1.1.0"
  },
  "contract": "2.0.0",
  "knowledge_base": {
    "schema": "2026-07-31-a3f2",
    "wiki": "2026-07-31-b9c1",
    "raw": "2026-07-31-d7e5"
  },
  "last_boot": "2026-07-31T10:00:00+08:00"
}
```

## 11.4 版本校验机制

- **启动校验**：`core/version.py` 读取 version.json，校验引擎目录与注册表一致性
- **引擎版本上报**：每个引擎实现 `version()` 方法，调度启动时收集
- **健康探针**：`get_health_status()` 增加版本信息输出（当前已含 brain_os_version，扩展至全引擎）
- **变更记录**：每引擎目录保留 `CHANGELOG.md`，重大变更更新版本号

## 11.5 配置管理

配置集中化（`runtime/config.json`），避免散落硬编码：

```json
{
  "scheduler": {
    "default_urgency": "medium",
    "max_engines_per_task": 5,
    "fallback_enabled": true
  },
  "governance": {
    "enabled": true,
    "bottleneck_severity_threshold": 0.7,
    "light_decide": "hybrid"
  },
  "memory": {
    "storage": "persistent",
    "session_dir": "runtime/sessions",
    "max_session_turns": 100
  },
  "brain_os": {"path": "../龙脑OS"},
  "claw_os": {"enabled": true}
}
```

配置加载优先级：环境变量 > config.json > 代码默认值。

---

---

# 第十二章 开发计划与里程碑

## 12.1 开发策略：协议化渐进改造

采用"**协议先行、适配渐进、切换平滑**"策略：

1. **阶段零（不动现有逻辑）**：定义 `core/protocol.py` 数据模型与 `Engine` 协议
2. **阶段一（加适配层）**：为每个引擎新增 `engine_adapter.py`，不改原引擎逻辑
3. **阶段二（补协议测试）**：编写协议一致性测试，验证适配层符合契约
4. **阶段三（切换调度）**：将调度中枢 `invoke_heart_engine` 切换为注册表调用
5. **阶段四（扩展接入）**：接入扩展引擎（临床模式+治理层）
6. **阶段五（持久化）**：上下文持久化 + LLM-Wiki 回流

## 12.2 里程碑计划

| 里程碑 | 目标 | 主要交付 | 预估工期 |
|--------|------|---------|---------|
| M0 协议定型 | 引擎协议与数据模型冻结 | core/protocol.py、core/registry.py、core/version.py | 0.5周 |
| M1 引擎适配 | 五大引擎+三扩展引擎适配完成 | 8个 engine_adapter.py | 1周 |
| M2 调度真实化 | 调度中枢真实调用引擎 | scheduler.py 改造、引擎路由升级 | 1周 |
| M3 治理落地 | 组织治理层接入 | governance.py、治理测试 | 1周 |
| M4 记忆持久化 | 上下文持久化+知识回流 | PersistentContextManager、wiki回流 | 1周 |
| M5 契约对齐 | 三OS契约v2.0+契约测试 | 契约文档更新、contract_adapter.py | 0.5周 |
| M6 测试加固 | 全量测试通过 | 单元/集成/回归测试 | 1周 |
| M7 部署分发 | 主活体+分发落点 | 版本打包、分发清单 | 0.5周 |

**总工期预估：约 6.5 周**（若投入充分可并行压缩至 3-4 周）。

## 12.3 任务分解（WBS 简表）

```
M0 协议定型
  T0.1 定义 TaskContext/EngineResult/SchedulerResult/GovernanceResult/Bottleneck
  T0.2 定义 Engine 协议（ABC）
  T0.3 定义引擎注册表与延迟加载
  T0.4 定义版本结构

M1 引擎适配
  T1.1 象思维适配器（含临床模式接口预留）
  T1.2 知识学习适配器（含十指令流水线补全）
  T1.3 五色光适配器（含序列库）
  T1.4 人机协同适配器
  T1.5 知行合一适配器
  T1.6 格式塔/瓶颈诊断/瓶颈压缩适配器

M2 调度真实化
  T2.1 invoke_engines 真实调用
  T2.2 determine_engines 注册表化
  T2.3 降级与备选引擎
  T2.4 调度输出双轨（结构化+legacy文本）

M3 治理落地
  T3.1 治理统计采集
  T3.2 四类瓶颈判定
  T3.3 CP-01~06策略实现
  T3.4 红绿灯授权

M4 记忆持久化
  T4.1 PersistentContextManager
  T4.2 跨会话摘要注入
  T4.3 LLM-Wiki回流（flow_to_wiki）
  T4.4 确认记录持久化

M5 契约对齐
  T5.1 契约v2.0文档（引擎/治理新增章节）
  T5.2 contract_adapter.py
  T5.3 契约schema校验工具

M6 测试加固
  T6.1 单元测试（引擎/调度/治理/记忆）
  T6.2 集成测试（端到端）
  T6.3 回归测试（现有demo场景快照）
  T6.4 契约测试

M7 部署分发
  T7.1 版本打包（version.json）
  T7.2 分发清单生成
  T7.3 运维文档
```

## 12.4 风险登记

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 现有引擎模板输出依赖，改造后形态变化 | 中 | 中 | 保留 format_text 兼容层，双轨输出 |
| 引擎真实调用暴露现有实现缺陷 | 中 | 中 | M1 阶段先跑通协议，缺陷单列修复 |
| 治理层误判瓶颈 | 低 | 低 | 阈值可配置，人工可覆盖 |
| 持久化格式变更导致旧会话丢失 | 低 | 低 | JSONL 追加式，天然兼容 |

---

# 第十三章 测试策略

## 13.1 测试层级

```
┌─────────────────────────────────────────┐
│  L1 单元测试（引擎/组件级）               │
│  每个引擎 adapter 的 run() 契约一致性     │
├─────────────────────────────────────────┤
│  L2 集成测试（调度级）                    │
│  scheduler.run() 端到端，引擎真实联动     │
├─────────────────────────────────────────┤
│  L3 契约测试（接口级）                    │
│  实际输出 vs 契约 schema 校验             │
├─────────────────────────────────────────┤
│  L4 回归测试（演进级）                    │
│  现有 demo 场景行为快照比对               │
└─────────────────────────────────────────┘
```

## 13.2 单元测试

**目标**：每个引擎协议一致性（Engine 协议合规）。

测试用例示例（象思维）：

```python
def test_xiang_si_wei_adapter_protocol():
    adapter = XiangSiWeiAdapter()
    ctx = TaskContext(task_type=TaskType.CY, task_level=TaskLevel.STANDARD,
                      description="如何让品牌更有东方禅意")
    result = adapter.run(ctx)
    assert result.engine_id == "xiang_si_wei"
    assert result.status == "ok"
    assert "insight" in result.output
    assert result.text != ""
    assert result.models_used  # 非空
```

**通用协议断言**（每个引擎复用）：
- engine_id 正确
- status ∈ {ok, degraded, failed, circuit_open}
- output 可 JSON 序列化
- text 非空（成功时）
- 异常输入不抛出（返回 failed）

## 13.3 集成测试

**目标**：调度中枢端到端，引擎真实联动。

```python
def test_scheduler_invokes_real_engines():
    scheduler = Scheduler()
    result = scheduler.run("该不该开新店？", urgency="high")
    assert result.status == "completed"
    assert len(result.heart_engine_results) >= 2   # 深度任务多引擎
    for engine_id, er in result.heart_engine_results.items():
        assert er.status == "ok"                    # 真实执行成功
        assert er.output is not None                # 结构化输出

def test_governance_integration():
    scheduler = Scheduler()
    result = scheduler.run("为什么这个月毛利下降了？")
    assert result.governance_result is not None
    assert result.governance_result.traffic_light in ("green", "yellow", "red")

def test_clinical_mode_integration():
    scheduler = Scheduler()
    result = scheduler.run("团队氛围紧张，帮我感受下",
                           keywords=["氛围"], 
                           context={"mode": "clinical"})
    xsw = result.heart_engine_results.get("xiang_si_wei")
    assert xsw and xsw.output.get("mode") == "clinical"
```

## 13.4 契约测试

**目标**：实际实现满足三OS契约 v2.0 的 schema。

```python
def test_brain_os_contract():
    scheduler = Scheduler()
    ctx = TaskContext(task_type=TaskType.JY, description="毛利分析")
    result = scheduler.query_brain_os(ctx)
    schema = load_contract("GET_MODEL_RECOMMENDATION")
    validate_against_schema(result.output, schema)   # 契约校验

def test_engine_contract():
    for engine_id in ENGINE_REGISTRY:
        result = get_engine(engine_id).run(sample_ctx)
        validate_engine_result(result)                # 引擎契约校验
```

## 13.5 回归测试

**目标**：现有调度行为不因改造回退。

- 对现有 `demo()` 的 10 个测试场景做行为快照（task_type/task_level/engines_activated/status）
- 改造后比对快照，确保分类、分层、激活引擎集合不变（仅引擎结果从 stub 变为真实）

## 13.6 测试覆盖率目标

| 模块 | 覆盖率目标 |
|------|-----------|
| core/protocol.py + registry.py | ≥ 95% |
| 调度中枢 scheduler.py | ≥ 85% |
| 治理层 governance.py | ≥ 90% |
| 上下文管理器 | ≥ 85% |
| 引擎适配器 | ≥ 80% |

---

# 第十四章 部署、分发与运维

## 14.1 部署形态

龙心OS以**本地认知引擎库**形态部署，主活体位于：

```
C:\Users\jia'yue\.agents\skills\10-kernel\龙心OS\
```

## 14.2 运行时初始化（启动流程）

```
启动龙心OS
│
├─ 1. 读取 runtime/config.json
├─ 2. 校验 runtime/version.json 与引擎目录一致性
├─ 3. 初始化引擎注册表（延迟加载声明）
├─ 4. 初始化 PersistentContextManager（恢复历史会话索引）
├─ 5. 初始化治理层（读取治理历史）
├─ 6. 心跳探针（brain_os/claw_os/resident）
└─ 7. 就绪（等待调度输入）
```

## 14.3 分发落点

龙心OS维护多份副本，开发设计文档发布后需同步分发：

| 落点 | 用途 | 同步方式 |
|------|------|---------|
| 主活体 `C:\Users\jia'yue\.agents\skills\10-kernel\龙心OS` | 实际运行 | 代码在此开发 |
| WorkBuddy 副本 | 记忆/协作 | 增量同步 |
| Obsidian 知识库（以观其妙书院） | 知识沉淀 | 文档编译入库 |
| GitHub repo `C:\Users\jia'yue\ai-os`（remote=yiguanqimiao-website） | 版本备份 | git 提交 |

## 14.4 运维监控

- **健康探针**：`get_health_status()` 覆盖调度/龙脑/龙爪/常驻子系统/引擎版本
- **治理日志**：`runtime/governance_logs/` 记录每次治理决策（瓶颈/策略/授权）
- **审计**：`runtime/sessions/` 提供会话完整追溯（含确认记录）
- **日志规范**：操作/决策/错误/进化四类日志（对齐 AI OS 日志规范）

## 14.5 回滚策略

- **L1（配置回滚）**：还原 config.json 前一版本
- **L2（代码回滚）**：还原 engine 目录至前一 git 提交
- **L3（数据回滚）**：JSONL 追加式日志天然支持截断恢复

---

# 附录A 术语表

| 术语 | 定义 |
|------|------|
| Engine | 实现 `Engine` 协议的认知组件（五大引擎+三扩展引擎） |
| Scheduler | 龙心OS 总智能体调度中枢 |
| TaskContext | 一次认知任务的完整输入（类型/层级/描述/上下文） |
| EngineResult | 引擎执行后的结构化结果 |
| SchedulerResult | 调度中枢聚合后的总输出 |
| Governance | 组织治理层（瓶颈诊断+压缩+红绿灯） |
| Bottleneck | 瓶颈（BN-INF/DEC/CRD/CTX） |
| TrafficLight | 红绿灯授权（green/yellow/red） |
| Resident Subsystem | 常驻子系统（五行OS、龙爪OS） |
| Adapter | 协议适配层（engine_adapter.py） |
| Registry | 引擎注册表（core/registry.py） |
| LLM-Wiki 回流 | 知识学习编译产物写回知识库 |

# 附录B 现有代码文件索引（审计基线 2026-07-29）

| 文件 | 行数 | 状态 | 对应改造 |
|------|------|------|---------|
| engines/调度中枢/scheduler.py | 578 | 可运行（引擎stub化） | M2 真实化 |
| engines/调度中枢/context_manager.py | 177 | 可运行（纯内存） | M4 持久化 |
| engines/调度中枢/subsystems/*.py | — | 可运行（深度共生） | 保留 |
| engines/象思维/象思维引擎.py | 114 | 模板级 | M1 适配 |
| engines/五色光思维/五色光引擎.py | — | 模板级 | M1 适配 |
| engines/人机协同五象限/五象限引擎.py | — | 模板级 | M1 适配 |
| engines/知识学习Skills/knowledge_learning.py | — | 框架级 | M1 适配+P0补全 |
| engines/知行合一/action_knowledge.py | — | 模板级 | M1 适配 |
| engines/具身关系格式塔引擎/gestalt_engine.py | 131 | 规则级 | M1 适配+M3 临床 |
| engines/串行瓶颈诊断引擎/bottleneck_diagnosis.py | — | 规则级 | M1 适配+M3 治理 |
| engines/瓶颈压缩策略引擎/bottleneck_compress.py | — | 规则级 | M1 适配+M3 治理 |
| 三OS接口契约.md | 302 | 契约文档 | M5 v2.0 |

# 附录C 接口签名速查

```python
# 引擎协议
class Engine(ABC):
    @property
    def engine_id(self) -> str: ...
    @abstractmethod
    def run(self, task_ctx: TaskContext) -> EngineResult: ...
    def capability(self) -> List[str]: ...

# 注册表
def get_engine(engine_id: str) -> Optional[Engine]: ...
ENGINE_REGISTRY: Dict[str, str]  # id -> 模块路径

# 调度中枢核心
class Scheduler:
    def run(self, description, urgency="medium", keywords=None,
            context: dict = None) -> SchedulerResult: ...
    def run_concurrent(self, contexts, timeout_seconds=30) -> List[SchedulerResult]: ...
    def get_health_status(self) -> dict: ...

# 上下文管理器
class ContextManager:
    def add_turn(self, session_id, turn) -> None: ...
    def load_session(self, session_id) -> List[dict]: ...
    def summarize(self, session_id, last_n=10) -> str: ...

# 治理层
class Governance:
    def run(self, task_ctx, engine_results, session_stats) -> GovernanceResult: ...
```

---

## 结语

本开发设计文档将《龙心OS顶层设计梳理》的理论蓝图转化为可执行的工程路线。核心工程主张：**以统一引擎协议弥合"契约与实现"的错位，以调度中枢真实化打通"1+5引擎"的实际联动，以组织治理层落地双尺度架构，以持久化记忆实现认知系统的自我进化**。

龙心OS从理论走向实现的路径已经清晰：M0 协议定型 → M1 引擎适配 → M2 调度真实化 → M3 治理落地 → M4 记忆持久化 → M5 契约对齐 → M6 测试加固 → M7 部署分发。每一步都有明确的验收判据，每一处改造都有降级与回滚保障。

开发设计的完成，意味着龙心OS正式进入工程实现阶段。后续将以本文档为蓝本，逐里程碑落地代码，并在每个里程碑结束时对照测试策略进行验证。

**文档终。**

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/AI龙龟共生OS/AI龙龟共生OS·开发文档]] — AI龙龟共生OS · 开发文档
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/AI龙龟共生OS/AI龙龟共生OS·顶层设计]] — AI龙龟共生OS · 顶层设计
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙心OS升级包：1+5/龙心OS顶层设计梳理]] — 龙心OS顶层设计梳理：认知操作系统的方法论体系与工程蓝图
- [[01-核心体系/AI龙龟共生OS升级包3.0/龙龟升级/龙爪OS：AI原生组织岗位智能体/岗位智能体OS·开发文档]] — 岗位智能体OS · 开发文档
- [[03-知识地基层/记忆系统_AGENTS]] — AGENTS.md - 智能体配置
- [[03-知识地基层/记忆系统_SESSION]] — SESSION.md - 会话上下文
- [[07-得到大脑同步/_历史归档_20261104/AI 原生组织/NS16D8E-06-AI本体论五大流派拆解与OWL工程实现入门]] — AI本体论五大流派拆解与OWL工程实现入门
- [[09-技能库/Framework核心管理/SKILL]] — Framework 核心管理 Skill
- [[ψ技能体系/30-tools/fbs-bookwriter/scripts/README]] — FBS-BookWriter 脚本索引
- [[ψ技能体系/30-tools/geo-converter/SKILL]] — geo-converter · GEO自动转化上传Skill

<!-- AI-LINKS-END -->
