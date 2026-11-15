# IMA Skill 凭证配置

## 已配置的凭证

```
IMA_OPENAPI_CLIENTID=87e4c9978e1b50b3918e20313b7084ed
IMA_OPENAPI_APIKEY=s/hxYqVaGQocwxhbaelqwbfywl6/1scRfZrisQ/zjAmP+wKJ0mciHHQa9SMv7T/qFJT9zRxROA==
```

## PowerShell 调用方式（Windows 直接使用�?

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
- 状态：�?已验证可�?

---\n
> ?? ����: [[ima�ʼ�]]

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[13-WorkBuddy-Sync/三向同步系统/scripts/IMA_API测试报告]] — IMA API同步测试报告
- [[00-索引与导航/核心系统_00-02-学习方法论]] — 00-02-学习方法论
- [[01-核心体系/AI智能体_01-AI与智能体]] — 01-AI与智能体
- [[02-信仰文化体系/项目实践_02-01-进行中的项目]] — 02-01-进行中的项目
- [[16-工具与资源/NSF418C-04-01-软件工具]] — 04-01-软件工具

<!-- AI-LINKS-END -->
