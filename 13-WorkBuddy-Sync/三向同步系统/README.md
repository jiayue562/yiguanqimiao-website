# 三向同步系统 v1.0 使用说明

> **最后更新**: 2026-04-17 | **状态**: ✅ 生产就绪

---

## 🎯 系统概览

三向同步系统实现了 **Obsidian ↔ WorkBuddy Brain ↔ IMA** 三个知识库之间的双向同步。

### 核心特性

| 特性 | 说明 |
|------|------|
| **WorkBuddy → Obsidian** | 将WorkBuddy Brain中的内容同步到Obsidian知识库 |
| **Obsidian → WorkBuddy** | 反向同步，将Obsidian中的新内容同步到WorkBuddy |
| **Obsidian → IMA** | 批量迁移Obsidian所有Markdown文件到IMA笔记库 |
| **增量同步** | 只同步修改过的文件，提高效率 |
| **批量同步** | 批量处理，避免API限流 |
| **进度显示** | 实时显示同步进度和百分比 |
| **错误重试** | 失败自动重试，提高成功率 |

---

## 📁 文件结构

```
三向同步系统/
├── scripts/
│   ├── sync.py              # 主同步脚本（全模式+增量模式）
│   └── batch_sync_to_ima.py # 批量同步脚本（Obsidian → IMA）
├── config.json              # 配置文件（可选）
└── README.md                # 本文档
```

---

## 🚀 快速开始

### 1. WorkBuddy → Obsidian（增量同步）

```powershell
# 进入脚本目录
cd "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts"

# 运行全量同步
python sync.py --mode full

# 运行增量同步（推荐日常使用）
python sync.py --mode incremental

# 干运行模式（不实际修改文件）
python sync.py --mode full --dry-run

# 强制同步所有文件
python sync.py --mode full --force

# 详细输出模式
python sync.py --mode full --verbose
```

### 2. Obsidian → WorkBuddy（反向同步）

```powershell
# 反向同步Obsidian中的内容到WorkBuddy
python sync.py --mode reverse
```

### 3. Obsidian → IMA（批量迁移）

```powershell
# 批量迁移Obsidian所有文件到IMA（默认每批10个文件）
python sync.py --mode batch

# 自定义参数示例
python sync.py --mode batch --batch-size 20 --rate-delay 3

# 每批5个文件，批间延迟1秒
python sync.py --mode batch --batch-size 5 --rate-delay 1
```

---

## 📋 命令行参数

### 通用参数

| 参数 | 说明 | 默认值 |
|------|------|
| `--mode` | 同步模式：`full`（全量）/ `incremental`（增量）/ `reverse`（反向）/ `batch`（批量） | `incremental` |
| `--dry-run` | 干运行模式，不实际修改文件 | `False` |
| `--force` | 强制同步所有文件，忽略时间戳检查 | `False` |
| `--verbose` | 详细输出，显示每个文件的处理过程 | `False` |

### 批量模式专属参数

| 参数 | 说明 | 默认值 |
|------|------|
| `--batch-size` | 每批处理的文件数量 | `10` |
| `--rate-delay` | 批间延迟时间（秒） | `2` |
| `--max-retries` | 每个文件最大重试次数 | `3` |

---

## 📊 同步模式详解

### 模式1：WorkBuddy → Obsidian（forward）

**功能**：将WorkBuddy Brain中的内容同步到Obsidian知识库

**流程**：
1. 扫描WorkBuddy Brain中的文件
2. 根据文件内容自动分类到对应目录：
   - `01-Conversations` → 对话记录
   - `02-Memory` → 记忆系统
   - `03-Skills` → 技能库
   - `04-Knowledge` → 知识沉淀
3. 检查Obsidian中是否已存在同名文件
4. 根据时间戳决定是否需要同步
5. 执行文件复制

**适用场景**：
- ✅ 将WorkBuddy中的对话记录归档到Obsidian
- ✅ 将长期记忆备份到Obsidian
- ✅ 同步技能和工具配置

### 模式2：Obsidian → WorkBuddy（reverse）

**功能**：从Obsidian反向同步到WorkBuddy

**流程**：
1. 扫描Obsidian知识库中的文件
2. 比较文件时间戳
3. 同步Obsidian中更新的内容到WorkBuddy

**适用场景**：
- ✅ Obsidian中编辑的内容需要同步回WorkBuddy
- ✅ 多设备使用时保持内容一致

### 模式3：Obsidian → IMA（batch）⭐

**功能**：批量迁移Obsidian所有Markdown文件到IMA笔记库

**核心特性**：
- ✅ **批量处理**：每批处理指定数量文件，避免API限流
- ✅ **进度显示**：实时显示 `[当前/总数] (百分比%)`
- ✅ **错误重试**：每个文件最多重试3次，失败自动记录
- ✅ **速率控制**：批间延迟，避免连续触发API限流
- ✅ **智能跳过**：自动跳过配置文件和系统文件

**流程**：
```
扫描Obsidian → 读取文件内容 → 生成IMA笔记 → 创建笔记 → 重试机制 → 下一批
```

**文件类型识别**：
- `.md` → 添加 `Obsidian` 标签
- `.py` → 添加 `Python` 标签
- `.json` → 添加 `JSON` 标签
- 其他 → 自动识别文件类型

---

## 🔧 配置说明

### 手动配置（config.json）

如果需要自定义路径，可以创建 `config.json`：

```json
{
  "workbuddy_brain": "C:/Users/jia'yue/AppData/Roaming/WorkBuddy/User/globalStorage/tencent-cloud.coding-copilot/brain",
  "obsidian_vault": "D:/以观其妙书院知识库/以观其妙书院",
  "sync_folder": "00-WorkBuddy-Sync",
  "ima_endpoint": "https://ima.qq.com",
  "ima_client_id": "87e4c9978e1b50b3918e20313b7084ed",
  "ima_api_key": "gep8bpF4dsT/7rN32p61y6r2KN0RPZADIWm+HBx7ce2UT7f6lUUuBd3hJCmojQ1aHPjZMOL6vA=="
}
```

---

## 📈 性能优化建议

### 批量同步参数调优

| 场景 | 推荐参数 | 说明 |
|------|-----------|------|
| **首次运行** | `--batch-size 5 --rate-delay 3` | 小批量测试，验证流程 |
| **日常同步** | `--batch-size 10 --rate-delay 2` | 默认参数，平衡速度和稳定性 |
| **大量文件** | `--batch-size 20 --rate-delay 3` | 大批量，适合大知识库 |
| **快速同步** | `--batch-size 20 --rate-delay 1` | 最快速度，但可能触发限流 |

### 速率限制应对

如果遇到API限流，系统会自动：
1. 检测到 "rate limit" 错误
2. 等待 `rate-delay` 秒
3. 自动重试

---

## 🎯 使用场景

### 场景1：首次完整迁移

```powershell
# 完整迁移Obsidian到IMA
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\sync.py" --mode batch --batch-size 10 --rate-delay 2
```

### 场景2：日常增量同步

```powershell
# 日常增量同步（WorkBuddy → Obsidian）
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\sync.py" --mode incremental
```

### 场景3：测试批量同步

```powershell
# 测试5个文件
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\sync.py" --mode batch --batch-size 5

# 测试1个文件（调试用）
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\sync.py" --mode batch --batch-size 1
```

---

## 📊 同步报告

同步完成后会自动生成报告：

### 增量/反向同步报告

```
# 三向同步报告

**同步时间**: 2026-04-17 11:12:00
**模式**: full/incremental/reverse

## 统计
| 指标 | 数值 |
|------|------|
| 扫描文件 | 150 |
| 已同步 | 148 |
| 已跳过 | 2 |
| 错误数量 | 0 |

## 路径
- **WorkBuddy Brain**: C:\Users\jia'yue\AppData\...
- **Obsidian Vault**: D:\以观其妙书院知识库\以观其妙书院
- **同步文件夹**: 00-WorkBuddy-Sync
```

### 批量同步报告

```
# 三向同步报告

**同步时间**: 2026-04-17 11:15:00
**批量大小**: 10
**批间延迟**: 2秒

## 统计
| 指标 | 数值 |
|------|------|
| 总文件数 | 1234 |
| 成功同步 | 1230 |
| 跳过文件 | 4 |
| 失败文件 | 0 |
| 错误次数 | 12 |

## 路径
- **Obsidian Vault**: D:\以观其妙书院知识库\以观其妙书院
- **IMA API**: https://ima.qq.com
```

---

## 🔍 故障排查

### 常见问题

**问题1：IMA客户端初始化失败**
```
解决方法：
1. 检查IMA API Key是否正确
2. 检查网络连接
3. 查看config.json中的配置
```

**问题2：文件读取失败**
```
解决方法：
1. 检查文件编码是否为UTF-8
2. 确认文件未被其他程序占用
3. 使用 --verbose 参数查看详细错误信息
```

**问题3：API限流**
```
解决方法：
1. 增加 --rate-delay 参数（如 3或5秒）
2. 减少 --batch-size 参数（如 5或10）
3. 等待一段时间后重试
```

**问题4：同步目录创建失败**
```
解决方法：
1. 检查目标路径是否存在
2. 确认是否有写入权限
3. 尝试手动创建目录
```

---

## 📝 日志和调试

### 启用详细日志

```powershell
# 详细模式，查看每个文件的处理过程
python "C:\Users\jia'yue\.workbuddy\skills\三向同步系统\scripts\sync.py" --mode batch --verbose
```

### 查看同步日志

同步日志会保存在对应目录：
- **WorkBuddy同步日志**: `sync_log.txt`
- **批量同步日志**: `batch_sync_log.txt`

---

## 🎯 最佳实践

1. **首次使用建议**
   - 先用 `--dry-run` 模式测试
   - 用小批量（`--batch-size 5`）验证
   - 确认流程正常后再进行完整同步

2. **日常使用建议**
   - 使用增量同步模式，减少文件处理
   - 定期反向同步，保持内容一致性
   - 设置合理的批量大小和延迟参数

3. **大知识库同步建议**
   - 使用较大的批量大小（`--batch-size 20`）
   - 增加批间延迟（`--rate-delay 3`）
   - 分多次同步，避免长时间连续运行

4. **数据安全建议**
   - 定期备份Obsidian知识库
   - 同步前确认IMA API凭据安全
   - 保留原始同步报告，便于回滚

---

## 📞 技术支持

### 文件结构

- **sync.py**: 主同步脚本，包含三个核心函数
  - `sync_workbuddy_to_obsidian()`: WorkBuddy → Obsidian
  - `sync_obsidian_to_workbuddy()`: Obsidian → WorkBuddy
  - `batch_sync_obsidian_to_ima()`: Obsidian → IMA
  
- **batch_sync_to_ima.py**: 批量同步实现
  - `batch_sync()`: 批量同步核心逻辑
  - 进度显示、错误重试、速率控制

### API集成

- **IMA API**: 使用IMA OpenAPI进行笔记操作
  - `create_note()`: 创建笔记
  - 自动标签识别
  - 错误处理和重试机制

---

## 📅 更新日志

### v1.0 (2026-04-17)
- ✅ 完成三大同步模式：WorkBuddy ↔ Obsidian ↔ IMA
- ✅ 实现批量同步功能，支持进度显示和错误重试
- ✅ 添加速率控制和参数配置
- ✅ 完善错误处理和日志记录
- ✅ 创建完整使用文档

### 未来计划
- [ ] 添加定时任务支持
- [ ] 实现文件内容差异检测
- [ ] 添加同步冲突解决机制
- [ ] 支持更多文件类型（图片、PDF等）

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- **WorkBuddy反馈**: 通过WorkBuddy内置反馈渠道
- **Obsidian支持**: https://forum.obsidian.md/
- **IMA文档**: IMA接口文档

---

**文档版本**: v1.0  
**最后更新**: 2026-04-17  
**维护者**: 龙龟神将

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/龙脑-思维模型顶层设计/NS3491F-04-三库同步指引]] — 三库同步指引
- [[03-知识地基层/记忆系统_obsidian-backup-system]] — 🚀 WorkBuddy ↔ Obsidian 知识备份系统
- [[03-知识地基层/记忆系统_skills-sync-summary]] — Skills文档同步检查报告
- [[03-知识地基层/记忆系统_workbuddy-obsidian-backup-summary-20260331]] — WorkBuddy-Obsidian备份系统对话总结
- [[05-五行人格心理学/理论基石/系统配置_Obsidian知识库同步机制]] — 🔄 Obsidian知识库同步机制
- [[05-五行人格心理学/理论基石/系统配置_同步报告_20260416]] — WorkBuddy三向同步报告

<!-- AI-LINKS-END -->
