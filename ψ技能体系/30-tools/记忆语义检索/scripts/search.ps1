# 记忆语义检索 PowerShell 脚本

> 🔍 语义搜索入口脚本

**用法**:
```powershell
# 基础搜索
.\search.ps1 -Query "龙心 OS"

# 指定结果数量
.\search.ps1 -Query "思维模型" -TopK 10

# 构建 embedding（首次使用）
.\search.ps1 -BuildEmbeddings

# 完整测试
.\search.ps1 -Test
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -Query | 搜索查询 | 必需 |
| -TopK | 返回结果数 | 5 |
| -Threshold | 相似度阈值 | 0.75 |
| -BuildEmbeddings | 构建 embedding | False |
| -Test | 运行测试 | False |

---

_记忆语义检索 PowerShell 脚本 v1.0 · 2026-04-17_
