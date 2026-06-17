# IMA 技能快速使用指南

## 📋 技能已安装完成

IMA 技能已成功安装到你的 WorkBuddy 系统中。以下是完整的配置和使用指南：

### ✅ 安装状态
- **技能位置**: `C:\Users\jia'yue\.workbuddy\skills\ima-skills\`
- **API 凭证**: 已配置完成
  - Client ID: `59a1edb848ec905552c0fbc8041213bf`
  - API Key: `NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==`
- **技能文件**: 已创建完整
  - `SKILL.md` - 主技能描述文件
  - `references/api.md` - API接口文档
  - `references/usage-examples.md` - 使用示例
  - `references/quick-start.md` - 快速使用指南
  - `scripts/test-with-creds.py` - Python测试脚本（直接使用凭证）
  - `scripts/test-api.py` - Python测试脚本（使用环境变量）
  - `scripts/test-api.sh` - Bash测试脚本
  - `scripts/test-api.ps1` - PowerShell测试脚本
  - `scripts/configure.ps1` - PowerShell配置脚本
  - `scripts/set-env.cmd` - CMD环境变量设置脚本

## 🔧 环境变量配置

### 方法1：临时设置（当前会话）
打开 PowerShell 或 CMD，运行：
```powershell
$env:IMA_OPENAPI_CLIENTID = "59a1edb848ec905552c0fbc8041213bf"
$env:IMA_OPENAPI_APIKEY = "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A=="
```

### 方法2：永久设置（系统环境变量）
打开 PowerShell（管理员权限），运行：
```powershell
[System.Environment]::SetEnvironmentVariable("IMA_OPENAPI_CLIENTID", "59a1edb848ec905552c0fbc8041213bf", "User")
[System.Environment]::SetEnvironmentVariable("IMA_OPENAPI_APIKEY", "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A==", "User")
```

或者使用 CMD（管理员权限）：
```cmd
setx IMA_OPENAPI_CLIENTID "59a1edb848ec905552c0fbc8041213bf"
setx IMA_OPENAPI_APIKEY "NmwwfdyB2ytuws6jeStZlZcouyijpDYiWSLNAS/fzSRKeGAJ1ZILYXK35G9M2CzVMEGepxc88A=="
```

## 🧪 测试连接

### 使用已配置的凭证测试
```bash
python C:\Users\jia'yue\.workbuddy\skills\ima-skills\scripts\test-with-creds.py
```

### 使用环境变量测试
```bash
python C:\Users\jia'yue\.workbuddy\skills\ima-skills\scripts\test-api.py
```

## 🚀 如何使用技能

IMA 技能会自动触发，当你说到以下关键词时：

### 触发关键词
- "笔记"、"备忘录"、"记事"、"记录"
- "知识库"、"文档"、"资料"
- "查找笔记"、"搜索笔记"、"查看笔记"
- "创建笔记"、"新建笔记"、"记录一下"
- "追加内容"、"添加内容"、"补充笔记"

### 常用命令示例
1. **查看笔记本列表**
   ```
   "列出我的笔记本"
   ```

2. **搜索笔记**
   ```
   "搜索关于AI的笔记"
   ```

3. **创建新笔记**
   ```
   "创建一篇关于龙心OS的笔记"
   ```

4. **读取笔记内容**
   ```
   "查看我的会议记录笔记"
   ```

5. **追加内容到笔记**
   ```
   "在我的学习笔记中添加新的内容"
   ```

## 📁 技能文件结构

```
ima-skills/
├── SKILL.md                    # 主技能描述文件
├── references/
│   ├── api.md                  # API接口文档
│   ├── usage-examples.md       # 使用示例
│   └── quick-start.md          # 快速使用指南
├── scripts/
│   ├── test-with-creds.py      # Python测试脚本（直接使用凭证）
│   ├── test-api.py             # Python测试脚本（使用环境变量）
│   ├── test-api.sh             # Bash测试脚本
│   ├── test-api.ps1            # PowerShell测试脚本
│   ├── configure.ps1           # PowerShell配置脚本
│   └── set-env.cmd             # CMD环境变量设置脚本
```

## ⚠️ 注意事项

1. **隐私保护**: 在公开场合，技能只展示笔记标题和摘要，不会直接显示完整内容
2. **操作确认**: 重要操作（如删除、修改）需要二次确认
3. **编码要求**: 所有文本内容必须使用 UTF-8 编码
4. **API 限制**: IMA API 可能有调用频率限制，请合理使用

## 🔄 技能更新

如果需要更新技能，可以通过以下方式：
1. 访问原仓库：https://clawhub.ai/iampennyli/ima-skills
2. 查看最新版本和更新说明
3. 手动更新技能文件

## 📞 技术支持

如果遇到问题：
1. 检查环境变量是否正确设置
2. 运行测试脚本验证连接
3. 查看 API 文档了解接口详情
4. 联系 IMA 官方技术支持

---

**IMA 技能已安装完成，现在你可以开始使用它来管理你的个人笔记了！**