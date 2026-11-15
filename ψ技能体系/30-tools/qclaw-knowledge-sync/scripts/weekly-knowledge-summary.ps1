# 周知识摘要生成脚本
# 用法：.\weekly-knowledge-summary.ps1
# 功能：读取过去 7 天的工作记忆，整理成本周知识摘要，写入 MEMORY.md

$ErrorActionPreference = "Stop"

$MemoryDir = "$env:USERPROFILE\.openclaw\workspace\memory"
$MemoryFile = "$env:USERPROFILE\.openclaw\workspace\MEMORY.md"
$OutputFile = "$env:TEMP\weekly-summary.md"

# 获取过去 7 天的日期
$Days = -7..-1 | ForEach-Object { (Get-Date).AddDays($_).ToString("yyyy-MM-dd") }

Write-Host "📚 生成周知识摘要"
Write-Host "时间范围：$($Days[0]) 到 $($Days[-1])"
Write-Host ""

# 收集所有日常笔记
$AllNotes = @()
foreach ($day in $Days) {
    $notePath = Join-Path $MemoryDir "$day.md"
    if (Test-Path $notePath) {
        $content = Get-Content $notePath -Raw
        $AllNotes += [PSCustomObject]@{
            Date = $day
            Content = $content
        }
        Write-Host "✅ 读取：$day.md"
    } else {
        Write-Host "⚠️  不存在：$day.md"
    }
}

if ($AllNotes.Count -eq 0) {
    Write-Host "❌ 没有找到任何笔记"
    exit 0
}

# 生成摘要（简化版 - 实际应由 AI 处理）
$Summary = @"
## 周知识摘要 - $(Get-Date -Format "yyyy-MM-dd")

### 本周概览
- 记录天数：$($AllNotes.Count)/7
- 主要话题：[待 AI 填充]

### 关键学习
[待 AI 填充]

### 重要决策
[待 AI 填充]

### 待跟进事项
[待 AI 填充]

---
_生成时间：$(Get-Date -Format "yyyy-MM-dd HH:mm")_

"@

# 保存摘要（供 AI 后续处理）
$Summary | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host ""
Write-Host "📄 摘要草稿已生成：$OutputFile"
Write-Host ""
Write-Host "下一步：由 AI 填充具体内容并写入 MEMORY.md"
