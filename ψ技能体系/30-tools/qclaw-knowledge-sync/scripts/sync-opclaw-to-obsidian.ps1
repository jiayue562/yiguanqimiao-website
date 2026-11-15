# OpcCla → Obsidian 同步脚本
# 功能：将 OpcCla 知识库内容同步到 Obsidian 本地知识库

param(
    [string]$Source = "$env:USERPROFILE\.OpcCla 知识库",
    [string]$Target = "D:\以观其妙书院知识库\观其妙书院",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "🐢 OpcCla → Obsidian 同步开始"
Write-Host "源：$Source"
Write-Host "目标：$Target"
Write-Host ""

# 检查源目录是否存在
if (-not (Test-Path $Source)) {
    Write-Host "❌ 源目录不存在：$Source"
    exit 1
}

# 检查目标目录是否存在
if (-not (Test-Path $Target)) {
    Write-Host "❌ 目标目录不存在：$Target"
    exit 1
}

# 确保目标子目录存在
$subdirs = @("areas", "projects", "resources", "journal", "ideas", "templates")
foreach ($dir in $subdirs) {
    $targetDir = Join-Path $Target $dir
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        Write-Host "✅ 创建目录：$dir"
    }
}

# 扫描源目录
Write-Host "📂 扫描源目录..."
$sourceFiles = Get-ChildItem -Path $Source -File -Recurse | Where-Object { $_.Name -notlike ".*" }

$syncCount = 0
$skipCount = 0
$errorCount = 0

foreach ($file in $sourceFiles) {
    $relativePath = $file.FullName.Substring($Source.Length + 1)
    $targetPath = Join-Path $Target $relativePath
    
    # 确保目标子目录存在
    $targetDir = Split-Path $targetPath -Parent
    if (-not (Test-Path $targetDir)) {
        if ($DryRun) {
            Write-Host "[DRY-RUN] 将创建目录：$targetDir"
        } else {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }
    }
    
    # 检查文件是否已存在
    if (Test-Path $targetPath) {
        $sourceTime = $file.LastWriteTime
        $targetTime = (Get-Item $targetPath).LastWriteTime
        
        if ($sourceTime -le $targetTime) {
            $skipCount++
            continue  # 跳过未修改的文件
        }
    }
    
    if ($DryRun) {
        Write-Host "[DRY-RUN] 将同步：$relativePath"
        $syncCount++
        continue
    }
    
    try {
        # 复制文件
        Copy-Item -Path $file.FullName -Destination $targetPath -Force
        Write-Host "✅ 同步：$relativePath"
        $syncCount++
    } catch {
        Write-Host "❌ 失败：$relativePath - $_"
        $errorCount++
    }
}

Write-Host ""
Write-Host "========== 同步完成 =========="
Write-Host "新增/更新：$syncCount"
Write-Host "跳过：$skipCount (无变化)"
Write-Host "失败：$errorCount"
