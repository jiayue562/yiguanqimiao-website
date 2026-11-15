# WorkBuddy + Obsidian + IMA 三向同步脚本
# 支持：WorkBuddy → Obsidian, WorkBuddy → IMA, Obsidian → IMA, 三向同步

param(
    [ValidateSet("all", "workbuddy-to-obsidian", "workbuddy-to-ima", "obsidian-to-ima", "workbuddy-to-obsidian-to-ima")]
    [string]$Direction = "all",
    [string]$WorkBuddyPath = "C:\Users\jia'yue\WorkBuddy",
    [string]$ObsidianVault = "D:\以观其妙书院知识库\以观其妙书院",
    [string]$KnowledgeBaseName = "以观其妙书院",
    [string]$FolderId = "folder_7441985942068358",
    [switch]$DryRun
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"

# IMA 配置
$IMA_CLIENT_ID = "87e4c9978e1b50b3918e20313b7084ed"
$IMA_API_KEY = "gep8bpF4dsT/7rN32p61y6r2KN0RPZADIWm+HBx7ce2UT7f6lUUuBd3hJCmojQ1aHPjZMOL6vA=="

Write-Host "=== 🐢 三向知识库同步 (增强版) ==="
Write-Host "方向: $Direction"
Write-Host "WorkBuddy: $WorkBuddyPath"
Write-Host "Obsidian: $ObsidianVault"
Write-Host "IMA: $KnowledgeBaseName / $FolderId"
Write-Host "预览模式: $($DryRun.IsPresent)"
Write-Host ""

# 辅助函数：同步文件到 Obsidian
function Sync-ToObsidian {
    param($SourcePath, $TargetPath, $Filter = "*.md")
    
    if (-not (Test-Path $SourcePath)) {
        Write-Host "❌ 源目录不存在: $SourcePath"
        return
    }
    
    Write-Host "📂 同步: $SourcePath → $TargetPath"
    
    $files = Get-ChildItem -Path $SourcePath -Filter $Filter -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike ".*" }
    $count = 0
    
    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($SourcePath.Length + 1)
        $targetFile = Join-Path $TargetPath $relativePath
        
        $targetDir = Split-Path $targetFile -Parent
        if (-not (Test-Path $targetDir)) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
            }
            Write-Host "  [CREATE] $targetDir"
        }
        
        if (Test-Path $targetFile) {
            $sourceTime = $file.LastWriteTime
            $targetTime = (Get-Item $targetFile).LastWriteTime
            if ($sourceTime -le $targetTime) {
                continue  # 目标更新，跳过
            }
        }
        
        if (-not $DryRun) {
            Copy-Item -Path $file.FullName -Destination $targetFile -Force
        }
        $count++
    }
    
    Write-Host "✅ 同步完成: $count 个文件"
}

# 辅助函数：IMA API 调用
function Invoke-IMAApi {
    param($path, $body)
    $url = "https://ima.qq.com/$path"
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    return Invoke-RestMethod -Uri $url -Method Post -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -Header @{
        "ima-openapi-clientid" = $IMA_CLIENT_ID
        "ima-openapi-apikey" = $IMA_API_KEY
    }
}

# 辅助函数：同步文件到 IMA
function Sync-ToIMA {
    param($SourcePath, $Filter = "*.md")
    
    if (-not (Test-Path $SourcePath)) {
        Write-Host "❌ 源目录不存在: $SourcePath"
        return
    }
    
    # 获取知识库 ID
    $searchBody = @{ query = $KnowledgeBaseName; cursor = "0"; limit = 10 } | ConvertTo-Json
    $searchResult = Invoke-IMAApi "openapi/wiki/v1/search_knowledge_base" $searchBody
    
    if ($searchResult.code -ne 0) {
        Write-Host "❌ 搜索知识库失败: $($searchResult.msg)"
        return
    }
    
    $kbId = $searchResult.data.info_list[0].kb_id
    Write-Host "📚 知识库 ID: $kbId"
    
    $files = Get-ChildItem -Path $SourcePath -Filter $Filter -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 50
    
    $success = 0
    $failed = 0
    
    foreach ($file in $files) {
        Write-Host "  上传: $($file.Name)..."
        
        # 1. Create media
        $createBody = @{
            file_name = $file.Name
            file_size = $file.Length
            content_type = "text/markdown"
            knowledge_base_id = $kbId
            file_ext = "md"
        } | ConvertTo-Json -Depth 10
        
        $createResult = Invoke-IMAApi "openapi/wiki/v1/create_media" $createBody
        
        if ($createResult.code -ne 0) {
            Write-Host "    ❌ 创建失败: $($createResult.msg)"
            $failed++
            continue
        }
        
        # 2. Upload to COS
        $cosKey = $createResult.data.cos_credential.cos_key
        $credential = $createResult.data.cos_credential
        
        $nodeResult = node "C:\Users\jia'yue\.agents\skills\ima-skill\knowledge-base\scripts\cos-upload.cjs" `
            --file $file.FullName `
            --secret-id $credential.secret_id `
            --secret-key $credential.secret_key `
            --token $credential.token `
            --bucket $credential.bucket_name `
            --region $credential.region `
            --cos-key $cosKey `
            --content-type "text/markdown" `
            --start-time $credential.start_time `
            --expired-time $credential.expired_time
        
        if ($nodeResult -notmatch "Upload successful") {
            Write-Host "    ❌ COS 上传失败"
            $failed++
            continue
        }
        
        # 3. Add knowledge
        $addBody = @{
            media_type = 7
            media_id = $createResult.data.media_id
            title = $file.Name
            knowledge_base_id = $kbId
            folder_id = $FolderId
            file_info = @{
                cos_key = $cosKey
                file_size = $file.Length
                file_name = $file.Name
            }
        } | ConvertTo-Json -Depth 10
        
        $addResult = Invoke-IMAApi "openapi/wiki/v1/add_knowledge" $addBody
        
        if ($addResult.code -eq 0) {
            $success++
            Write-Host "    ✅ 成功"
        } else {
            $failed++
            Write-Host "    ❌ 添加失败: $($addResult.msg)"
        }
        
        # 限流保护
        Start-Sleep -Milliseconds 500
    }
    
    Write-Host "✅ IMA 同步完成: 成功 $success, 失败 $failed"
}

# 执行同步
switch ($Direction) {
    "all" {
        Write-Host "========== 三向同步: WorkBuddy → Obsidian → IMA =========="
        
        Write-Host "`n步骤 1: WorkBuddy → Obsidian"
        Sync-ToObsidian -SourcePath $WorkBuddyPath -TargetPath $ObsidianVault
        
        Write-Host "`n步骤 2: WorkBuddy → IMA"
        Sync-ToIMA -SourcePath $WorkBuddyPath
        
        Write-Host "`n步骤 3: Obsidian → IMA"
        Sync-ToIMA -SourcePath $ObsidianVault
    }
    
    "workbuddy-to-obsidian" {
        Write-Host "========== WorkBuddy → Obsidian =========="
        Sync-ToObsidian -SourcePath $WorkBuddyPath -TargetPath $ObsidianVault
    }
    
    "workbuddy-to-ima" {
        Write-Host "========== WorkBuddy → IMA =========="
        Sync-ToIMA -SourcePath $WorkBuddyPath
    }
    
    "obsidian-to-ima" {
        Write-Host "========== Obsidian → IMA =========="
        Sync-ToIMA -SourcePath $ObsidianVault
    }
    
    "workbuddy-to-obsidian-to-ima" {
        Write-Host "========== WorkBuddy → Obsidian → IMA =========="
        
        Write-Host "`n步骤 1: WorkBuddy → Obsidian"
        Sync-ToObsidian -SourcePath $WorkBuddyPath -TargetPath $ObsidianVault
        
        Write-Host "`n步骤 2: Obsidian → IMA"
        Sync-ToIMA -SourcePath $ObsidianVault
    }
}

Write-Host ""
Write-Host "🎉 同步完成！"