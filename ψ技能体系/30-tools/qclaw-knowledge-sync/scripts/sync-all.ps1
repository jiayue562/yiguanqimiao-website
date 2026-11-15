# 三向同步统一入口脚本
# 用法：.\sync-all.ps1 [-Direction all|opclaw-to-obsidian|obsidian-to-ima] [-DryRun]

param(
    [ValidateSet("all", "opclaw-to-obsidian", "obsidian-to-ima")]
    [string]$Direction = "all",
    [switch]$DryRun
)

$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$ObsidianVault = "D:\以观其妙书院知识库\观其妙书院"
$OpcClaKnowledge = "$env:USERPROFILE\.OpcCla 知识库"

Write-Host "🐢 三向知识库同步"
Write-Host "方向：$Direction"
Write-Host "预览模式：$($DryRun.IsPresent)"
Write-Host ""

if ($Direction -eq "all" -or $Direction -eq "opclaw-to-obsidian") {
    Write-Host "========== 步骤 1: OpcCla → Obsidian =========="
    & "$ScriptDir\sync-opclaw-to-obsidian.ps1" -Source $OpcClaKnowledge -Target $ObsidianVault -DryRun:$DryRun
    Write-Host ""
}

if ($Direction -eq "all" -or $Direction -eq "obsidian-to-ima") {
    Write-Host "========== 步骤 2: Obsidian → IMA =========="
    & "$ScriptDir\sync-obsidian-to-ima.ps1" -ObsidianVault $ObsidianVault -KnowledgeBaseName "以观其妙书院" -DryRun:$DryRun
    Write-Host ""
}

Write-Host "🎉 同步完成！"
