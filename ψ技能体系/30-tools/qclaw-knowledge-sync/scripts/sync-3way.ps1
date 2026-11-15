# 三向知识库同步脚本（v5.1 · 干净版）
# 功能：WorkBuddy(OpcCla) → Obsidian → IMA
# 配置来源：~/.config/qclaw/sync.json + ~/.config/ima/*

param(
    [ValidateSet("all", "workbuddy-to-obsidian", "obsidian-to-ima")]
    [string]$Direction = "all",
    [switch]$DryRun,
    [switch]$Force     # 跳过修改时间比较
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# === 加载配置 ===
$configPath = "$env:USERPROFILE\.config\qclaw\sync.json"
if (-not (Test-Path $configPath)) {
    Write-Host "❌ 配置文件不存在: $configPath"
    exit 1
}
$cfg = Get-Content $configPath -Raw | ConvertFrom-Json

$obsidianVault = $cfg.obsidian_vault
$wbPath = $cfg.workbuddy_kb
$kbName = $cfg.ima.knowledge_base_name
$folderId = $cfg.ima.target_folder_id

# IMA 凭证
$imaClientId = Get-Content "$env:USERPROFILE\.config\ima\client_id" -Raw | ForEach-Object { $_.Trim() }
$imaApiKey = Get-Content "$env:USERPROFILE\.config\ima\api_key" -Raw | ForEach-Object { $_.Trim() }
if (-not $imaClientId -or -not $imaApiKey) {
    Write-Host "❌ IMA 凭证缺失"
    exit 1
}

Write-Host "================================"
Write-Host " 三向知识库同步"
Write-Host " 方向: $Direction"
if ($DryRun) { Write-Host " [预览模式] - 不会实际写入" }
Write-Host "================================"
Write-Host ""

# === IMA API 调用 ===
function Invoke-IMAApi {
    param($Path, $Body)
    $url = "https://ima.qq.com/$Path"
    $headers = @{
        "ima-openapi-clientid" = $imaClientId
        "ima-openapi-apikey" = $imaApiKey
        "Content-Type" = "application/json; charset=utf-8"
    }
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    try {
        $resp = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $utf8Bytes -ErrorAction Stop
        if ($resp.code -ne 0) {
            Write-Host "  ⚠️ IMA API 异常: code=$($resp.code), msg=$($resp.msg)"
            return $null
        }
        return $resp.data
    } catch {
        Write-Host "  ❌ IMA API 失败: $_"
        return $null
    }
}

# === 方向1: WorkBuddy → Obsidian ===
function Sync-WorkBuddyToObsidian {
    Write-Host "--- 方向1: WorkBuddy → Obsidian ---"
    
    if (-not (Test-Path $wbPath)) {
        Write-Host "❌ WorkBuddy 路径不存在: $wbPath"
        return
    }
    if (-not (Test-Path $obsidianVault)) {
        Write-Host "❌ Obsidian 路径不存在: $obsidianVault"
        return
    }
    
    $files = Get-ChildItem -Path $wbPath -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue
    $count = 0; $skip = 0
    
    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($wbPath.Length + 1)
        $targetFile = Join-Path $obsidianVault "00-WorkBuddy-Sync" $relativePath
        $targetDir = Split-Path $targetFile -Parent
        
        # 检查是否需要同步
        if ((-not $Force) -and (Test-Path $targetFile)) {
            $targetTime = (Get-Item $targetFile).LastWriteTime
            if ($file.LastWriteTime -le $targetTime) {
                $skip++; continue  # 目标更新或相同，跳过
            }
        }
        
        if ($DryRun) {
            Write-Host "  [DRY] $relativePath → Obsidian"
            $count++; continue
        }
        
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        }
        Copy-Item -Path $file.FullName -Destination $targetFile -Force
        Write-Host "  ✅ $relativePath"
        $count++
    }
    
    Write-Host "→ 结果: 同步 $count, 跳过 $skip"
    Write-Host ""
}

# === 方向2: Obsidian → IMA ===
function Sync-ObsidianToIMA {
    Write-Host "--- 方向2: Obsidian → IMA ---"
    
    if (-not (Test-Path $obsidianVault)) {
        Write-Host "❌ Obsidian 路径不存在: $obsidianVault"
        return
    }
    
    # 获取知识库 ID
    $searchBody = @{ query = $kbName; cursor = ""; limit = 10 } | ConvertTo-Json
    $searchResult = Invoke-IMAApi "openapi/wiki/v1/search_knowledge_base" $searchBody
    if (-not $searchResult -or -not $searchResult.info_list) {
        Write-Host "❌ 知识库未找到: $kbName"
        return
    }
    $kbId = $searchResult.info_list[0].kb_id
    Write-Host "📚 知识库: $kbName (ID: $kbId)"
    
    # 获取已有 Markdown 文件（去重）
    $existingFiles = @{}
    $cursor = ""
    do {
        $listBody = @{ knowledge_base_id = $kbId; cursor = $cursor; limit = 50 } | ConvertTo-Json
        $listResult = Invoke-IMAApi "openapi/wiki/v1/get_knowledge_list" $listBody
        if (-not $listResult) { break }
        foreach ($item in $listResult.item_list) {
            if ($item.media_type -eq 7) {
                $existingFiles[$item.title] = $item
            }
        }
        $cursor = $listResult.next_cursor
    } while (-not $listResult.is_end)
    
    Write-Host "📊 知识库已有 $($existingFiles.Count) 个 Markdown 文件"
    
    # 扫描 Obsidian 中需要同步的文件
    $files = Get-ChildItem -Path $obsidianVault -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike ".*" }
    
    $success = 0; $failed = 0; $skipped = 0
    $total = $files.Count
    $count = 0
    
    foreach ($file in $files) {
        $count++
        $relativePath = $file.FullName.Substring($obsidianVault.Length + 1)
        $fileName = $file.Name
        
        # 比较修改时间
        if ((-not $Force) -and $existingFiles.ContainsKey($fileName)) {
            $existing = $existingFiles[$fileName]
            $obsidianTime = $file.LastWriteTime.ToUniversalTime()
            $imaTime = [DateTimeOffset]::FromUnixTimeMilliseconds($existing.modify_time).DateTime.ToUniversalTime()
            if ($obsidianTime -le $imaTime) {
                $skipped++; continue
            }
        }
        
        Write-Host "  [$count/$total] $relativePath"
        
        if ($DryRun) {
            $success++; continue
        }
        
        # 读取文件
        try {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8 -ErrorAction Stop
        } catch {
            Write-Host "    ⚠️ 读取失败: $_"
            $failed++; continue
        }
        
        # 检查内容是否为空
        if ([string]::IsNullOrWhiteSpace($content)) {
            Write-Host "    ⚠️ 空文件，跳过"
            $skipped++; continue
        }
        
        # Step 1: Create media
        $createBody = @{
            file_name = $fileName
            file_size = [System.Text.Encoding]::UTF8.GetByteCount($content)
            content_type = "text/markdown"
            knowledge_base_id = $kbId
            file_ext = "md"
        } | ConvertTo-Json -Depth 5
        
        $media = Invoke-IMAApi "openapi/wiki/v1/create_media" $createBody
        if (-not $media) { $failed++; continue }
        
        # Step 2: Upload to COS
        $cosKey = $media.cos_credential.cos_key
        $cred = $media.cos_credential
        
        # 使用 Python COS 上传
        $cosUrl = "https://$($cred.bucket_name).cos.$($cred.region).myqcloud.com/$cosKey"
        $cosScript = "$env:USERPROFILE\.agents\skills\qclaw-knowledge-sync\scripts\cos-upload.py"
        $uploadResult = python $cosScript $cosUrl $file.FullName $cred.token 2>&1
        
        if ($uploadResult -notmatch "Upload successful") {
            Write-Host "    ❌ COS 上传失败: $uploadResult"
            $failed++; continue
        }
        
        # Step 3: Add knowledge
        $fileInfo = @{
            cos_key = $cosKey
            file_size = $file.Length
            file_name = $fileName
        }
        $addBody = @{
            media_type = 7
            media_id = $media.media_id
            title = $fileName
            knowledge_base_id = $kbId
            folder_id = $folderId
            file_info = $fileInfo
        } | ConvertTo-Json -Depth 5
        
        $addResult = Invoke-IMAApi "openapi/wiki/v1/add_knowledge" $addBody
        if ($addResult) {
            Write-Host "    ✅"
            $success++
        } else {
            Write-Host "    ❌ 添加知识库条目失败"
            $failed++
        }
        
        Start-Sleep -Milliseconds 300  # 限流
    }
    
    Write-Host "→ 结果: 成功 $success, 跳过 $skipped, 失败 $failed"
    Write-Host ""
}

# === 主流程 ===
switch ($Direction) {
    "all" {
        Sync-WorkBuddyToObsidian
        Sync-ObsidianToIMA
    }
    "workbuddy-to-obsidian" {
        Sync-WorkBuddyToObsidian
    }
    "obsidian-to-ima" {
        Sync-ObsidianToIMA
    }
}

Write-Host "================================"
Write-Host " 同步完成"
Write-Host "================================"
