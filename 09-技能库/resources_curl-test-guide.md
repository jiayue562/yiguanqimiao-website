# 🔧 curl 命令行测试 IMA API 连接

## 🚀 一键测试方法

### Windows 用户
1. **方法一（推荐）**：双击运行 `scripts/curl-test.bat`
2. **方法二**：右键点击 `scripts/curl-test.ps1`，选择"使用 PowerShell 运行"

### macOS/Linux 用户
1. 给脚本添加执行权限：`chmod +x scripts/curl-test.sh`
2. 运行：`./scripts/curl-test.sh`

## 📝 直接命令行测试

### 基本 curl 命令
```bash
curl -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" \
  -H "Content-Type: application/json" \
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" \
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" \
  -d '{"cursor":"0"}'
```

### 带格式化的漂亮输出
```bash
curl -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" \
  -H "Content-Type: application/json" \
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" \
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" \
  -d '{"cursor":"0"}' | python -m json.tool
```

### 带详细日志的输出
```bash
curl -v -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" \
  -H "Content-Type: application/json" \
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" \
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" \
  -d '{"cursor":"0"}'
```

## 📊 结果解读

### ✅ 连接成功
```json
{
    "code": 0,
    "message": "success",
    "data": {
        "folders": [...],
        "next_cursor": "..."
    }
}
```

### ❌ 常见错误

| 状态码 | 含义 | 解决方法 |
|--------|------|----------|
| 400 | 参数错误 | 检查请求体格式 |
| 401 | 认证失败 | 检查 API 凭证 |
| 403 | 权限不足 | 检查 API 权限设置 |
| 404 | 接口不存在 | 检查 URL 是否正确 |
| 500 | 服务器错误 | 稍后重试 |
| 502/503/504 | 网关错误 | 网络或服务器问题 |

## 🔧 问题排查

### 1. curl 未安装
```bash
# 检查 curl
curl --version

# Windows 安装 curl（如果未安装）
# 1. 下载 https://curl.se/windows/
# 2. 或使用 winget: winget install curl.curl
```

### 2. 网络连接问题
```bash
# 测试网络连接
ping ima.qq.com

# 测试 HTTPS 连接
curl -I "https://ima.qq.com"
```

### 3. 证书问题（macOS/Linux）
```bash
# 忽略证书验证（不推荐，仅用于测试）
curl -k ...
```

## 📱 平台特定命令

### Windows PowerShell
```powershell
curl.exe -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" `
  -H "Content-Type: application/json" `
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" `
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" `
  -d '{"cursor":"0"}'
```

### Windows CMD
```cmd
curl -X POST "https://ima.qq.com/openapi/note/v1/list_note_folder_by_cursor" ^
  -H "Content-Type: application/json" ^
  -H "X-OpenApi-ClientId: 59a1edb848ec905552c0fbc8041213bf" ^
  -H "X-OpenApi-Sign: NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==" ^
  -d "{\"cursor\":\"0\"}"
```

## 💡 高级选项

### 1. 保存响应到文件
```bash
curl ... > response.json
```

### 2. 设置超时时间
```bash
curl --max-time 10 ...
```

### 3. 显示进度条
```bash
curl --progress-bar ...
```

## 🎯 快速验证

运行这个最简单的命令，只看状态码：
```bash
curl -s -o /dev/null -w "%{http_code}" -X POST ... 
```

如果返回 `200` 表示 HTTP 层连接成功。