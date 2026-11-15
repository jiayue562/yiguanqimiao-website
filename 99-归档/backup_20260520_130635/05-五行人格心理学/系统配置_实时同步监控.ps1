# WorkBuddy-Obsidian 实时同步监控脚本
# 版本：v2.0 - 支持实时监控和智能分类
# 创建时间：2026-03-12
# 维护者：龙龟神将自主进化系统

param(
    [string]$WorkBuddyPath = "C:\Users\jia'yue\WorkBuddy\20260312123940",
    [string]$ObsidianPath = "C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院",
    [int]$CheckInterval = 30 # 检查间隔（秒）
)

# 日志函数
function Write-SyncLog {
    param([string]$Message, [string]$Type = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Type] $Message"
    Write-Host $LogMessage
    Add-Content -Path "$ObsidianPath\05-系统配置\同步日志.txt" -Value $LogMessage
}

# 文件变化检测函数
function Get-FileChanges {
    param([string]$Path)
    
    $CurrentFiles = Get-ChildItem $Path -Recurse -File | 
        Select-Object FullName, Length, LastWriteTime
    
    return $CurrentFiles
}

# 智能分类函数
function Invoke-IntelligentClassification {
    param([string]$FilePath)
    
    $Content = Get-Content $FilePath -Raw
    $FileName = Split-Path $FilePath -Leaf
    
    # 基于内容和文件名的智能分类逻辑
    if ($FileName -match "龙龟|神将|故事") {
        return "01-核心体系\龙龟神将故事"
    }
    elseif ($FileName -match "五色光|方法论|思维") {
        return "01-核心体系\五大工具系统"
    }
    elseif ($FileName -match "观其妙|书院|超级个体") {
        return "01-核心体系\观其妙书院"
    }
    elseif ($FileName -match "对话|聊天|交流") {
        return "02-对话记录"
    }
    elseif ($Content -match "大圆满|觉知|心文化") {
        return "01-核心体系\心文化大圆满"
    }
    else {
        return "00-索引与导航\待分类"
    }
}

# 标准化处理函数
function Invoke-Standardization {
    param([string]$SourceFile, [string]$TargetCategory)
    
    $TargetPath = Join-Path $ObsidianPath $TargetCategory
    $TargetFile = Join-Path $TargetPath (Split-Path $SourceFile -Leaf)
    
    # 确保目标目录存在
    if (-not (Test-Path $TargetPath)) {
        New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    }
    
    # 复制文件并添加标准化元数据
    $Content = Get-Content $SourceFile -Raw
    $StandardizedContent = @"
# 标准化知识资产

**来源**：WorkBuddy系统实时同步  
**同步时间**：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  
**分类**：$TargetCategory  
**维护者**：龙龟神将自主进化系统  

---

$Content

---

**标签**：#实时同步 #知识沉淀 #标准化资产  
**状态**：✅ 已同步到Obsidian知识库
"@
    
    Set-Content -Path $TargetFile -Value $StandardizedContent
    Write-SyncLog "文件已标准化同步: $SourceFile -> $TargetFile" -Type "SUCCESS"
}

# 知识图谱更新函数
function Update-KnowledgeGraph {
    param([string]$NewFile)
    
    $GraphFile = "$ObsidianPath\00-索引与导航\知识图谱\动态知识网络.md"
    
    if (-not (Test-Path $GraphFile)) {
        $InitialContent = @"
# 动态知识网络图谱

## 📊 实时更新状态

**最后更新**：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  
**同步文件总数**：0  
**知识网络节点**：建设中...

## 🔗 知识关联网络

```mermaid
graph TD
    A[WorkBuddy系统] --> B[实时同步监控]
    B --> C[Obsidian知识库]
    C --> D[知识图谱更新]
    D --> E[智能推荐系统]
    E --> A
```

## 📈 同步统计

| 时间 | 新增文件 | 分类 | 状态 |
|------|----------|------|------|
"@
        Set-Content -Path $GraphFile -Value $InitialContent
    }
    
    $NewEntry = "| $(Get-Date -Format 'MM-dd HH:mm') | $(Split-Path $NewFile -Leaf) | $(Invoke-IntelligentClassification $NewFile) | ✅ 已同步 |"
    Add-Content -Path $GraphFile -Value $NewEntry
}

# 主监控循环
function Start-RealtimeSync {
    Write-SyncLog "启动WorkBuddy-Obsidian实时同步监控" -Type "INFO"
    Write-SyncLog "监控路径: $WorkBuddyPath" -Type "INFO"
    Write-SyncLog "目标路径: $ObsidianPath" -Type "INFO"
    Write-SyncLog "检查间隔: $CheckInterval 秒" -Type "INFO"
    
    # 初始化文件状态记录
    $LastFileState = @{}
    
    while ($true) {
        try {
            $CurrentFiles = Get-FileChanges $WorkBuddyPath
            
            foreach ($File in $CurrentFiles) {
                $FileKey = $File.FullName
                $CurrentState = @{
                    Size = $File.Length
                    LastWrite = $File.LastWriteTime
                }
                
                # 检测文件变化
                if (-not $LastFileState.ContainsKey($FileKey) -or 
                    $LastFileState[$FileKey].Size -ne $CurrentState.Size -or
                    $LastFileState[$FileKey].LastWrite -ne $CurrentState.LastWrite) {
                    
                    # 新文件或文件已更改
                    Write-SyncLog "检测到文件变化: $FileKey" -Type "CHANGE"
                    
                    # 智能分类和标准化处理
                    $TargetCategory = Invoke-IntelligentClassification $FileKey
                    Invoke-Standardization -SourceFile $FileKey -TargetCategory $TargetCategory
                    
                    # 更新知识图谱
                    Update-KnowledgeGraph -NewFile $FileKey
                    
                    # 更新状态记录
                    $LastFileState[$FileKey] = $CurrentState
                }
            }
            
            # 清理已删除的文件记录
            $RemovedFiles = $LastFileState.Keys | Where-Object { 
                -not (Test-Path $_) 
            }
            
            foreach ($RemovedFile in $RemovedFiles) {
                Write-SyncLog "文件已删除: $RemovedFile" -Type "DELETE"
                $LastFileState.Remove($RemovedFile)
            }
            
            # 等待下一次检查
            Start-Sleep -Seconds $CheckInterval
            
        } catch {
            Write-SyncLog "监控过程中出现错误: $($_.Exception.Message)" -Type "ERROR"
            Start-Sleep -Seconds 60 # 错误后等待1分钟再重试
        }
    }
}

# 启动实时同步监控
Start-RealtimeSync