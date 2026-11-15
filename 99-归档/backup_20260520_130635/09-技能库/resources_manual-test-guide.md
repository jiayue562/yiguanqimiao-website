# IMA API 手动测试指南

## 准备工作

### 1. 获取 API 凭证（悟空已提供）
- **Client ID**: `59a1edb848ec905552c0fbc8041213bf`
- **API Key**: `NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==`

### 2. 准备测试工具
你可以使用以下任意一种工具：
- **Postman** (推荐，图形界面)
- **cURL** (命令行)
- **PowerShell** (Windows 内置)
- **Python** (需要安装 requests 库)

## 方法一：使用 Postman 测试

### 步骤：
1. 打开 Postman
2. 新建一个 POST 请求
3. 设置 URL: `https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor`
4. 设置 Headers：
   - `Content-Type`: `application/json`
   - `X-OpenApi-ClientId`: `59a1edb848ec905552c0fbc8041213bf`
   - `X-OpenApi-Sign`: `NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==`
5. 设置 Body (raw, JSON):
   ```json
   {
     "cursor": "0"
   }
   ```
6. 点击 Send

### 预期响应：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "folders": [
      {
        "id": "xxx",
        "name": "笔记本名称",
        "notes_count": 10
      }
    ]
  }
}
```

## 方法二：使用 cURL 测试

打开命令行，执行以下命令：

```bash
curl -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" \
  -H "Content-Type: application/json" \
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" \
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" \
  -d '{"cursor":"0"}'
```

## 方法三：使用 PowerShell 测试

打开 PowerShell，执行以下命令：

```powershell
$ClientID = "59a1edb848ec905552c0fbc8041213bf"
$ApiKey = "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A=="
$headers = @{
    "Content-Type" = "application/json"
    "X-OpenApi-ClientId" = $ClientID
    "X-OpenApi-Sign" = $ApiKey
}
$body = '{"cursor":"0"}'
$response = Invoke-RestMethod -Uri "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" -Method Post -Headers $headers -Body $body
Write-Host "响应: $($response | ConvertTo-Json -Depth 10)"
```

## 方法四：使用 Python 测试

创建 `test.py` 文件：

```python
import requests
import json

client_id = "59a1edb848ec905552c0fbc8041213bf"
api_key = "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A=="

url = "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor"
headers = {
    "Content-Type": "application/json",
    "X-OpenApi-ClientId": client_id,
    "X-OpenApi-Sign": api_key
}
data = {
    "cursor": "0"
}

response = requests.post(url, headers=headers, json=data)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

if response.status_code == 200:
    result = response.json()
    if result.get("code") == 0:
        print("✅ API 连接成功！")
        folders = result.get("data", {}).get("folders", [])
        print(f"📁 发现 {len(folders)} 个笔记本")
        for folder in folders:
            print(f"  - {folder.get('name')} (ID: {folder.get('id')}, 笔记数: {folder.get('notes_count')})")
    else:
        print(f"⚠️ API 返回错误: 代码 {result.get('code')}, 消息: {result.get('message')}")
else:
    print(f"❌ 请求失败: HTTP {response.status_code}")
```

运行：
```bash
python test.py
```

## 测试结果解读

### ✅ 连接成功的表现
1. HTTP 状态码 200
2. 响应 JSON 中 `code` 字段为 0
3. `message` 字段为 "success"
4. `data.folders` 包含笔记本列表

### ❌ 常见错误
1. **HTTP 403/401**: API 凭证无效
2. **HTTP 404**: 接口地址错误
3. **HTTP 500**: 服务器内部错误
4. **响应中 code ≠ 0**: API 逻辑错误

### 🔧 故障排查
1. **检查网络连接**: 确保可以访问 `ima.qq.com`
2. **验证凭证**: 确认 Client ID 和 API Key 正确
3. **检查请求格式**: 确保 Headers 和 Body 格式正确
4. **查看错误信息**: 根据返回的错误码和消息排查

## 技能使用说明

一旦测试成功，IMA 技能就可以正常使用。技能会自动触发，当你说到以下内容时：
- "查看我的笔记"
- "搜索关于XX的笔记"
- "创建一篇新笔记"
- "列出我的笔记本"
- "在笔记里添加内容"