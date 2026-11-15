# LLM Wiki Linting PowerShell 脚本

> 🔍 Linting 检查入口脚本

**用法**:
```powershell
# 完整检查
.\run_linter.ps1 -WikiDir "C:\Users\jia'yue\.OpcClaw 知识库"

# 指定输出报告
.\run_linter.ps1 -WikiDir "..." -Output "lint-report.md"

# 仅检查特定目录
.\run_linter.ps1 -WikiDir "..." -Pattern "skills/*.md"

# 自动修复（询问后）
.\run_linter.ps1 -WikiDir "..." -AutoFix
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -WikiDir | Wiki 知识库目录 | 必需 |
| -Output | 输出报告路径 | lint-report-YYYY-MM-DD.md |
| -Pattern | 文件匹配模式 | *.md |
| -AutoFix | 自动修复 | False |
| -Severity | 报告阈值 | low |

---

_LLM Wiki Linting PowerShell 脚本 v1.0 · 2026-04-17_
