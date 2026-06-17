# 六向知识库同步脚本 (Six-Way Sync v1.0)
# 管道: WorkBuddy -> Obsidian -> IMA -> GitHub -> Cloudflare Pages -> pages.dev
# 作者: 以观其妙书院 . 悟空

param(
    [ValidateSet("all", "wb-to-obs", "obs-to-ima", "obs-to-github", "github-to-cf", "dryrun")]
    [string]$Direction = "all",
    [string]$CommitMessage = ("Six-Way Sync - " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss"))
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$rootDir = "D:\以观其妙书院知识库\以观其妙书院"
$scriptsDir = "$env:USERPROFILE\.agents\skills\qclaw-knowledge-sync\scripts"
$startTime = Get-Date

Write-Host ""
Write-Host "=== Six-Way Knowledge Sync ==="
Write-Host "WorkBuddy -> Obsidian -> IMA -> GitHub -> CF"
Write-Host "Direction: $Direction"
Write-Host ""

# Step 1: WorkBuddy -> Obsidian
function Step1-WBtoObsidian {
    Write-Host "`n[1/5] WorkBuddy -> Obsidian"
    python "$scriptsDir\sync-3way.py" --direction wb-to-obs
    if ($?) { Write-Host "  [OK] Step 1 done" }
    else { Write-Host "  [!] Step 1 partial" }
}

# Step 2: Obsidian -> IMA
function Step2-ObsToIMA {
    Write-Host "`n[2/5] Obsidian -> IMA (cloud backup)"
    python "$scriptsDir\sync-3way.py" --direction obs-to-ima
    if ($?) { Write-Host "  [OK] Step 2 done" }
    else { Write-Host "  [!] Step 2 partial" }
}

# Step 3: Obsidian -> GitHub
function Step3-ObsToGitHub {
    Write-Host "`n[3/5] Obsidian -> GitHub"
    Set-Location $rootDir
    $status = git status --porcelain
    if (-not $status) {
        Write-Host "  [SKIP] No changes"
        return
    }
    $count = ($status -split "`n").Count
    Write-Host "  Changed files: $count"
    git add -A
    git commit -m $CommitMessage
    git push origin master 2>&1
    if ($?) { Write-Host "  [OK] Step 3 done" }
    else { Write-Host "  [!] Git push failed, check network" }
}

# Step 4: GitHub -> Cloudflare Pages
function Step4-GitHubToCF {
    Write-Host "`n[4/5] GitHub -> Cloudflare Pages"
    Write-Host "  GitHub Actions triggered automatically"
    Write-Host "  Monitor: https://github.com/jiayue562/yiguanqimiao-website/actions"
    Write-Host "  [OK] Step 4 triggered"
}

# Step 5: CF Pages -> pages.dev
function Step5-CFToPages {
    Write-Host "`n[5/5] Cloudflare Pages -> pages.dev"
    $cfToken = "YOUR_CF_TOKEN"
    $cfAccount = "c1965573a5f89d696d011372a7cd0c9e"
    $headers = @{
        "Authorization" = "Bearer $cfToken"
        "Content-Type" = "application/json"
    }
    $url = "https://api.cloudflare.com/client/v4/accounts/$cfAccount/pages/projects/yiguanqimiao-website/deployments"
    $body = @{ branch = "master" } | ConvertTo-Json
    try {
        $utf8Body = [System.Text.Encoding]::UTF8.GetBytes($body)
        $resp = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $utf8Body -ErrorAction Stop
        if ($resp.success) {
            Write-Host "  [OK] CF Pages deployment triggered"
            Write-Host "  URL: https://yiguanqimiao-website.pages.dev"
        } else {
            Write-Host "  [!] CF API error"
        }
    } catch {
        Write-Host "  [!] Direct deploy failed: $_"
        Write-Host "  Please deploy manually in CF Dashboard"
    }
}

# Main flow
switch ($Direction) {
    "all" {
        Step1-WBtoObsidian
        Step2-ObsToIMA
        Step3-ObsToGitHub
        Step4-GitHubToCF
        Step5-CFToPages
    }
    "wb-to-obs" { Step1-WBtoObsidian }
    "obs-to-ima" { Step2-ObsToIMA }
    "obs-to-github" { Step3-ObsToGitHub }
    "github-to-cf" { Step4-GitHubToCF; Step5-CFToPages }
    "dryrun" {
        Write-Host "[DRY RUN] Will execute:"
        Write-Host "  1. WorkBuddy -> Obsidian (copy .md files)"
        Write-Host "  2. Obsidian -> IMA (upload to Tencent cloud)"
        Write-Host "  3. Obsidian -> GitHub (git push)"
        Write-Host "  4. GitHub -> Cloudflare Pages (trigger Actions)"
        Write-Host "  5. CF Pages -> pages.dev (CDN acceleration)"
        Write-Host "  Source: $rootDir"
    }
}

$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds
Write-Host ""
Write-Host "=== Six-Way Sync Complete ==="
Write-Host "Time: $([math]::Round($duration, 1))s"
Write-Host "yiguanqimiao . Wukong"
Write-Host ""
