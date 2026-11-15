# 记忆压缩归档 PowerShell 脚本
# 功能：自动压缩 3 个月前的记忆到冷存储

param(
    [string]$MemoryDir = "$env:USERPROFILE\.openclaw\workspace\memory",
    [string]$ArchiveDir = "$env:USERPROFILE\.openclaw\workspace\memory\archive",
    [int]$DaysToKeep = 90,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Memory Archive - 记忆压缩归档" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Time: $timestamp"
Write-Host "Memory Dir: $MemoryDir"
Write-Host "Archive Dir: $ArchiveDir"
Write-Host "Keep Days: $DaysToKeep"
Write-Host "Dry Run: $DryRun"
Write-Host ""

# 1. Calculate cutoff date
$cutoffDate = (Get-Date).AddDays(-$DaysToKeep)
Write-Host "[1/4] Calculating cutoff date..."
Write-Host "  Cutoff: $cutoffDate.ToString('yyyy-MM-dd')"
Write-Host ""

# 2. Find old memories
Write-Host "[2/4] Finding memories older than $DaysToKeep days..."
$oldFiles = Get-ChildItem -Path $MemoryDir -Filter "*.md" -File | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate -and $_.Name -notlike "embedding_cache*" }

if ($oldFiles.Count -eq 0) {
    Write-Host "OK: No memories to archive" -ForegroundColor Green
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Archive Complete - Nothing to archive" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    exit 0
}

Write-Host "  Found $($oldFiles.Count) files to archive" -ForegroundColor Yellow
foreach ($file in $oldFiles | Select-Object -First 5) {
    Write-Host "    - $($file.Name) ($($file.LastWriteTime.ToString('yyyy-MM-dd')))"
}
if ($oldFiles.Count -gt 5) {
    Write-Host "    ... and $($oldFiles.Count - 5) more"
}
Write-Host ""

# 3. Create archive directory
Write-Host "[3/4] Creating archive directory..."
if (-not (Test-Path $ArchiveDir)) {
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Would create: $ArchiveDir"
    } else {
        New-Item -ItemType Directory -Path $ArchiveDir -Force | Out-Null
        Write-Host "OK: Created $ArchiveDir" -ForegroundColor Green
    }
} else {
    Write-Host "OK: Archive directory exists" -ForegroundColor Green
}
Write-Host ""

# 4. Archive memories
Write-Host "[4/4] Archiving memories..."

$archiveMonth = $cutoffDate.ToString("yyyy-MM")
$monthArchiveDir = Join-Path $ArchiveDir $archiveMonth

if (-not (Test-Path $monthArchiveDir)) {
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Would create: $monthArchiveDir"
    } else {
        New-Item -ItemType Directory -Path $monthArchiveDir -Force | Out-Null
    }
}

$archivedCount = 0
$totalSize = 0

foreach ($file in $oldFiles) {
    $destFile = Join-Path $monthArchiveDir $file.Name
    
    if ($DryRun) {
        Write-Host "  [DRY-RUN] Would move: $($file.Name) -> $monthArchiveDir"
        $archivedCount++
        $totalSize += $file.Length
    } else {
        # Move file
        Move-Item -Path $file.FullName -Destination $monthArchiveDir -Force
        Write-Host "  OK: $($file.Name)" -ForegroundColor Green
        $archivedCount++
        $totalSize += $file.Length
    }
}

# Generate archive index
if (-not $DryRun) {
    $indexFile = Join-Path $monthArchiveDir "archive-index.json"
    $indexData = @{
        archive_month = $archiveMonth
        created = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        file_count = $archivedCount
        total_size_bytes = $totalSize
        files = ($oldFiles | ForEach-Object {
            @{
                name = $_.Name
                date = $_.LastWriteTime.ToString("yyyy-MM-dd")
                size = $_.Length
            }
        })
    } | ConvertTo-Json -Depth 3
    
    $indexData | Out-File -FilePath $indexFile -Encoding UTF8
    Write-Host "OK: Archive index created: $indexFile" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Archive Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Files archived: $archivedCount"
Write-Host "Total size: $([math]::Round($totalSize / 1KB, 2)) KB"
Write-Host "Archive location: $monthArchiveDir"
Write-Host "Space saved: $([math]::Round($totalSize / 1KB, 2)) KB"

if (-not $DryRun) {
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Verify archive integrity"
    Write-Host "2. Compress archive directory (optional)"
    Write-Host "3. Upload to cold storage (IMA/cloud)"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Archive Completed Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
