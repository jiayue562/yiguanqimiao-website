$vault = "D:\以观其妙书院知识库\以观其妙书院"
$skillsSrc = "C:\Users\jia'yue\.agents\skills"
$target = Join-Path $vault "ψ技能体系"

Write-Host "[Sync] Starting WorkBuddy skills sync..."
Write-Host "[Sync] Source: $skillsSrc"
Write-Host "[Sync] Target: $target"

$robocopyArgs = @(
    $skillsSrc,
    $target,
    "/E",
    "/COPY:DAT",
    "/R:1",
    "/W:1",
    "/XD", ".git", "__pycache__", "node_modules", ".obsidian", ".claude", ".codebuddy", ".cursor", ".github", ".smart-env", ".trash", ".workbuddy",
    "/XF", ".gitignore", "_history.json", "scm_file_list.json", "scm_version.json"
)

$result = robocopy @robocopyArgs 2>&1
Write-Host "[Sync] robocopy completed."
Write-Host "[Sync] Source SKILL.md: $(Get-ChildItem $skillsSrc -Recurse -Filter 'SKILL.md' | Measure-Object | Select-Object -ExpandProperty Count)"
Write-Host "[Sync] Target SKILL.md: $(Get-ChildItem $target -Recurse -Filter 'SKILL.md' | Measure-Object | Select-Object -ExpandProperty Count)"
Write-Host "[Sync] Done."