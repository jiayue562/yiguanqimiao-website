# 观其妙书院知识库整合 · 手动执行脚本

> ⚠️ **重要提醒**：执行前请备份知识库！
> 备份命令：`robocopy "D:\以观其妙书院知识库" "D:\以观其妙书院知识库-备份-20260411" /E /COPYALL`

---

## 📋 当前问题诊断

### 1. 重复核心目录（需要合并至 01-龙心OS核心系统/）

| 源目录 | 文件数 | 操作 |
|--------|--------|------|
| 01-核心独创Skills/ | 95 | **移动到** 01-龙心OS核心系统/01-五大引擎/ |
| 01-核心架构/ | 待统计 | **移动到** 01-龙心OS核心系统/ |
| 01-核心体系/ | 122 | **移动到** 01-龙心OS核心系统/ |
| 01-龙心OS核心系统/ | 已存在 | **保留**（作为目标目录）|

### 2. 重复五行目录（需要合并至统一位置）

| 源目录 | 文件数 | 目标 |
|--------|--------|------|
| 五行人格心理学/ | 待统计 | 合并到 05-五行人格心理学/ |
| 02-五行人格心理学/ | 58 | 合并到 05-五行人格心理学/ |
| 03-五行人格心理学/ | 待统计 | 合并到 05-五行人格心理学/ |
| 04-五行人格心理学/ | 待统计 | 合并到 05-五行人格心理学/ |
| 05-五行人格心理学/ | 147 | **保留**（作为目标目录）|

### 3. 重复凤脑OS（需要删除一个）

| 目录 | 文件数 | 操作 |
|------|--------|------|
| 03-凤脑OS知识地基层/ | 待统计 | **保留** |
| 05-凤脑OS知识地基层/ | 12 | **删除**（与03重复）|

### 4. 重复其他目录

| 源目录 | 操作 |
|--------|------|
| 02-独创方法论/ | 合并到相关目录或归档 |
| 02-方法论库/ | 合并到相关目录或归档 |
| 02-思维模型/ | 合并到 01-思维模型体系/ |
| 02-理论基石/ | 合并到 03-凤脑OS知识地基层/ |
| 02-躯体系统Skills/ | 合并到相关Skills目录 |
| 03-人格体系/ | 合并到 05-五行人格心理学/ |
| 03-文化智慧/ | 归档或合并到心文化 |
| 03-五行分类图谱/ | 合并到 03-凤脑OS知识地基层/ |
| 04-五行人格与应用/ | 合并到 05-五行人格心理学/ |
| 04-专业领域/ | 合并到 02-专业领域知识库矩阵/ |
| 05-个人成长/ | 合并到 05-个人成长/（保留一个）|
| 05-技术实现/ | 归档或移动到 08-工具与脚本/ |
| 05-修行文化/ | 合并到心文化相关目录 |
| 06-观其妙书院/ | 归档 |
| 06-课程体系/ | 合并到相关课程目录 |
| 06-三向同步系统/ | 合并到 06-知识库建设/ |
| 06-生活管理/ | 归档或移动到 05-个人成长/ |
| 06-项目管理/ | 归档或移动到 04-个人成长/ |
| 06-心文化/ | 合并到 05-心文化信仰/ |
| 06-AI OS技能系统/ | 归档或合并到Skills目录 |
| 07-内容创作系统/ | 归档或移动到相关内容目录 |
| 五行人格心理学/ | 合并到 05-五行人格心理学/ |
| WorkBuddy知识备份体系/ | 合并到 WorkBuddy知识沉淀/ |
| WorkBuddy知识备份系统/ | 删除（重复）|

---

## 🔧 执行脚本

### PowerShell 脚本 1：合并核心目录

```powershell
# 观其妙书院知识库整合 - Phase 3
# 合并核心目录到 01-龙心OS核心系统/

$basePath = "D:\以观其妙书院知识库\观其妙书院"
$targetDir = "$basePath\01-龙心OS核心系统"

# 确保目标目录存在
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force
}

# 1. 合并 01-核心独创Skills/ → 01-龙心OS核心系统/01-五大引擎/
$source1 = "$basePath\01-核心独创Skills"
$target1 = "$targetDir\01-五大引擎"
if (Test-Path $source1) {
    if (!(Test-Path $target1)) {
        New-Item -ItemType Directory -Path $target1 -Force
    }
    Get-ChildItem -Path $source1 -File | Move-Item -Destination $target1 -Force
    Remove-Item -Path $source1 -Recurse -Force
    Write-Host "✓ 已合并: 01-核心独创Skills/ → 01-五大引擎/"
}

# 2. 合并 01-核心架构/ → 01-龙心OS核心系统/（文件直接移动）
$source2 = "$basePath\01-核心架构"
if (Test-Path $source2) {
    Get-ChildItem -Path $source2 -File | Move-Item -Destination $targetDir -Force
    Get-ChildItem -Path $source2 -Directory | ForEach-Object {
        $subTarget = "$targetDir\$($_.Name)"
        if (!(Test-Path $subTarget)) {
            New-Item -ItemType Directory -Path $subTarget -Force
        }
        Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $subTarget -Force
    }
    Remove-Item -Path $source2 -Recurse -Force
    Write-Host "✓ 已合并: 01-核心架构/"
}

# 3. 合并 01-核心体系/ → 01-龙心OS核心系统/
$source3 = "$basePath\01-核心体系"
if (Test-Path $source3) {
    Get-ChildItem -Path $source3 -File | Move-Item -Destination $targetDir -Force
    Get-ChildItem -Path $source3 -Directory | ForEach-Object {
        $subTarget = "$targetDir\$($_.Name)"
        if (!(Test-Path $subTarget)) {
            New-Item -ItemType Directory -Path $subTarget -Force
        }
        Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $subTarget -Force
    }
    Remove-Item -Path $source3 -Recurse -Force
    Write-Host "✓ 已合并: 01-核心体系/"
}

Write-Host "`n=== Phase 3 完成 ==="
```

### PowerShell 脚本 2：删除重复凤脑OS

```powershell
# 观其妙书院知识库整合 - Phase 4
# 删除重复的 05-凤脑OS知识地基层/

$basePath = "D:\以观其妙书院知识库\观其妙书院"
$duplicateDir = "$basePath\05-凤脑OS知识地基层"

if (Test-Path $duplicateDir) {
    $fileCount = (Get-ChildItem -Path $duplicateDir -File -Recurse).Count
    Remove-Item -Path $duplicateDir -Recurse -Force
    Write-Host "✓ 已删除: 05-凤脑OS知识地基层/ ($fileCount 个文件)"
} else {
    Write-Host "目录不存在，跳过"
}

Write-Host "`n=== Phase 4 完成 ==="
```

### PowerShell 脚本 3：合并五行心理学目录

```powershell
# 观其妙书院知识库整合 - Phase 5
# 合并五行心理学目录到 05-五行人格心理学/

$basePath = "D:\以观其妙书院知识库\观其妙书院"
$targetDir = "$basePath\05-五行人格心理学"

# 确保目标目录存在
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force
}

# 需要合并的目录
$sourceDirs = @(
    "$basePath\五行人格心理学",
    "$basePath\02-五行人格心理学",
    "$basePath\03-五行人格心理学",
    "$basePath\04-五行人格心理学"
)

foreach ($sourceDir in $sourceDirs) {
    if (Test-Path $sourceDir) {
        $fileCount = (Get-ChildItem -Path $sourceDir -File -Recurse).Count
        Get-ChildItem -Path $sourceDir -File | Move-Item -Destination $targetDir -Force
        Get-ChildItem -Path $sourceDir -Directory | ForEach-Object {
            $subTarget = "$targetDir\$($_.Name)"
            if (!(Test-Path $subTarget)) {
                New-Item -ItemType Directory -Path $subTarget -Force
            }
            Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $subTarget -Force
        }
        Remove-Item -Path $sourceDir -Recurse -Force
        Write-Host "✓ 已合并: $sourceDir/ ($fileCount 个文件)"
    }
}

Write-Host "`n=== Phase 5 完成 ==="
```

### PowerShell 脚本 4：归档重复目录

```powershell
# 观其妙书院知识库整合 - Phase 2 补充
# 归档重复的旧目录

$basePath = "D:\以观其妙书院知识库\观其妙书院"
$archiveDir = "$basePath\99-归档\重复目录"

New-Item -ItemType Directory -Path $archiveDir -Force

# 需要归档的目录
$dirsToArchive = @(
    "02-独创方法论",
    "02-方法论库",
    "02-躯体系统Skills",
    "03-人格体系",
    "03-文化智慧",
    "04-专业领域",
    "05-技术实现",
    "06-观其妙书院",
    "06-课程体系",
    "06-生活管理",
    "06-项目管理",
    "06-AI OS技能系统",
    "WorkBuddy知识备份体系",
    "WorkBuddy知识备份系统"
)

foreach ($dir in $dirsToArchive) {
    $fullPath = "$basePath\$dir"
    if (Test-Path $fullPath) {
        $archiveName = $dir
        $targetPath = "$archiveDir\$archiveName"
        $counter = 1
        while (Test-Path $targetPath) {
            $targetPath = "$archiveDir\$archiveName-$counter"
            $counter++
        }
        Move-Item -Path $fullPath -Destination $targetPath
        Write-Host "✓ 已归档: $dir/"
    }
}

Write-Host "`n=== Phase 2 补充完成 ==="
```

---

## 📊 执行顺序建议

1. **先备份**：执行 `robocopy` 备份整个知识库
2. **Phase 3**：先合并核心目录（风险较低）
3. **Phase 5**：合并五行心理学
4. **Phase 4**：删除重复凤脑OS
5. **Phase 2 补充**：归档其他重复目录
6. **手动检查**：检查整合后的目录结构
7. **更新索引**：更新总索引文档

---

## ⚠️ 风险提示

- **Phase 3（合并核心目录）**：中风险，涉及文件移动
- **Phase 4（删除凤脑OS）**：高风险，确认03-目录完整后再删除05-
- **Phase 5（合并五行心理学）**：中风险，建议先备份

---

**脚本生成时间**：2026-04-11 08:10
**执行者**：龙龟神将
