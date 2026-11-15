# IMA Skill 凭证配置

## 已配置的凭证

```
IMA_OPENAPI_CLIENTID=87e4c9978e1b50b3918e20313b7084ed
IMA_OPENAPI_APIKEY=s/hxYqVaGQocwxhbaelqwbfywl6/1scRfZrisQ/zjAmP+wKJ0mciHHQa9SMv7T/qFJT9zRxROA==
```

## PowerShell 调用方式（Windows 直接使用）

```powershell
$clientId = "87e4c9978e1b50b3918e20313b7084ed"
$apiKey = "s/hxYqVaGQocwxhbaelqwbfywl6/1scRfZrisQ/zjAmP+wKJ0mciHHQa9SMv7T/qFJT9zRxROA=="
$baseUrl = "https://ima.qq.com/openapi/note/v1"

function Invoke-ImaApi {
    param([string]$Endpoint, [string]$Body)
    $headers = @{
        "ima-openapi-clientid" = $clientId
        "ima-openapi-apikey" = $apiKey
        "Content-Type" = "application/json; charset=utf-8"
    }
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
    $response = Invoke-RestMethod -Uri "$baseUrl/$Endpoint" -Method Post -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -Headers $headers
    return $response
}
```

## 凭证来源
- 获取地址：https://ima.qq.com/agent-interface
- 最后更新：2026-03-28
- 状态：✅ 已验证可用

<!-- FUSION-LINK-BEGIN -->
## 🔗 同名版本对照（融合时生成）

> 本文件是副库/研学库版本；主库另有同名现行版本，**两版内容不同，均未覆盖**。
- 主库现行版本：[[09-技能库/ima笔记/config|主库现行版本]]

<!-- FUSION-LINK-END -->
