# IMA Skills 知识库使用指南

> 📘 IMA 知识库完整功能激活与配置指南 · 2026-04-16

**版本**: v1.0  
**创建**: 2026-04-16  
**状态**: 已配置，待验证

---

## 📋 配置状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **IMA Skill** | ✅ 已安装 | ~/.agents/skills/ima-skill/ |
| **Client ID** | ✅ 已配置 | 87e4c9978e1b50b3918e20313b7084ed |
| **API Key** | ✅ 已配置 | 76 字符 |
| **凭证位置** | ✅ 正确 | ~/.config/ima/client_id + ~/.config/ima/api_key |

---

## 🚀 快速开始

### 1. 验证凭证

打开 PowerShell，运行：

```powershell
# 检查凭证文件
Get-Content "$env:USERPROFILE\.config\ima\client_id"
Get-Content "$env:USERPROFILE\.config\ima\api_key"
```

应该显示：
- Client ID: `87e4c9978e1b50b3918e20313b7084ed`
- API Key: 76 字符的密钥

---

### 2. 使用 IMA 知识库功能

#### 读取功能

**查看知识库列表**:
```
用户："我有哪些知识库？"
```

**搜索知识库内容**:
```
用户："搜索知识库中的 [关键词]"
```

**浏览知识库内容**:
```
用户："查看 [知识库名称] 的内容"
```

---

#### 写入功能

**上传文件到知识库**:
```
用户："把这个文件上传到知识库"
附件：[文件]
```

**添加网页到知识库**:
```
用户："把这个网页添加到知识库"
URL: [网页链接]
```

**创建笔记**:
```
用户："帮我记一下：[笔记内容]"
```

---

#### 管理功能

**创建知识库**:
```
用户："创建一个新的知识库，名字叫 [名称]"
```

**重命名知识库**:
```
用户："把 [旧名称] 改名为 [新名称]"
```

**删除内容**:
```
用户："删除知识库中的 [内容名称]"
```

---

## 🔧 核心功能

### 功能 1: 笔记管理

**支持操作**:
- ✅ 创建笔记
- ✅ 编辑笔记
- ✅ 删除笔记
- ✅ 搜索笔记
- ✅ 浏览笔记列表

**API 路径**: `openapi/note/v1/*`

---

### 功能 2: 知识库管理

**支持操作**:
- ✅ 创建知识库
- ✅ 浏览知识库列表
- ✅ 搜索知识库
- ✅ 获取知识库详情
- ✅ 添加内容到知识库
- ✅ 删除知识库内容

**API 路径**: `openapi/wiki/v1/*`

---

### 功能 3: 文件上传

**支持文件类型**:

| 类型 | 扩展名 | media_type |
|------|--------|------------|
| PDF | .pdf | 1 |
| Word | .doc, .docx | 3 |
| PPT | .ppt, .pptx | 4 |
| Excel | .xls, .xlsx, .csv | 5 |
| Markdown | .md, .markdown | 7 |
| 图片 | .png, .jpg, .jpeg, .webp | 9 |
| 文本 | .txt | 13 |
| XMind | .xmind | 14 |
| 音频 | .mp3, .m4a, .wav, .aac | 15 |

**上传流程**:
1. 检查文件名是否重复 (`check_repeated_names`)
2. 文件类型检测 (`preflight-check.cjs`)
3. 上传到 COS (`create_media` + COS Upload)
4. 添加到知识库 (`add_knowledge`)

---

### 功能 4: 网页收藏

**支持操作**:
- ✅ 添加单个网页
- ✅ 批量添加（最多 10 个）
- ✅ 添加到指定文件夹
- ✅ 微信文章收藏

**API**: `import_urls`

---

## 📁 目录结构

```
ima-skill/
├── SKILL.md                          # 主技能定义
├── knowledge-base/
│   ├── SKILL.md                      # 知识库功能定义
│   ├── references/
│   │   └── api.md                    # API 完整文档
│   └── scripts/
│       ├── cos-upload.cjs            # COS 上传脚本
│       └── preflight-check.cjs       # 文件预检脚本
├── notes/
│   ├── SKILL.md                      # 笔记功能定义
│   └── references/
│       └── api.md                    # 笔记 API 文档
└── scripts/
    └── test-knowledge-base.py        # 知识库测试脚本
```

---

## 🔗 协同 Skills

| Skill | 协同方式 |
|-------|----------|
| **llm-wiki-knowledge-base** | 本地 Wiki ↔ IMA 云端同步 |
| **knowledge-base-manager** | 三库同步（Obsidian/OpcCla/IMA） |
| **context-engineering** | 上下文注入到 IMA 笔记 |
| **super-save** | 快速保存到 IMA |

---

## ⚠️ 注意事项

### 凭证安全

- ✅ 凭证仅发送到 `ima.qq.com`
- ✅ 凭证存储在 `~/.config/ima/` 目录
- ✅ 不记录、不存储、不转发凭证
- ❌ 不要将凭证提交到版本控制

### 使用限制

- 单个知识库最多添加 10 个 URL（批量操作）
- 文件大小限制：具体限制参考 IMA 官方文档
- API 调用频率限制：参考 IMA 官方文档

### 错误处理

**常见错误码**:
- `20000`: 成功
- `20004`: 认证失败（检查凭证）
- `40001`: 参数错误
- `40002`: 资源不存在
- `50000`: 服务器错误

---

## 🧪 测试验证

### 运行测试脚本

```powershell
cd ~/.agents/skills/ima-skill/scripts
python test-knowledge-base.py
```

**预期输出**:
```
SUCCESS: 凭证检查通过
SUCCESS: API 调用成功
  知识库数量：N
PASS - 获取知识库列表
PASS - 搜索知识库内容
PASS - 浏览知识库内容
总计：3/3 测试通过
SUCCESS: 所有测试通过！IMA 知识库功能正常
```

---

## 📖 API 文档

完整 API 文档位于：
- 知识库 API: `ima-skill/knowledge-base/references/api.md`
- 笔记 API: `ima-skill/notes/references/api.md`
- 官方文档：https://ima.qq.com/agent-interface

---

## 🆘 故障排查

### 问题 1: 凭证无效

**症状**: API 返回 `20004` 错误

**解决**:
1. 重新获取凭证：https://ima.qq.com/agent-interface
2. 更新凭证文件：
   ```powershell
   "new_client_id" > ~/.config/ima/client_id
   "new_api_key" > ~/.config/ima/api_key
   ```

---

### 问题 2: 网络连接失败

**症状**: 请求超时或连接错误

**解决**:
1. 检查网络连接
2. 检查防火墙设置
3. 确认 `ima.qq.com` 可访问

---

### 问题 3: 文件上传失败

**症状**: 上传过程中断

**解决**:
1. 检查文件大小是否超限
2. 检查文件类型是否支持
3. 运行预检脚本：
   ```powershell
   node ~/.agents/skills/ima-skill/knowledge-base/scripts/preflight-check.cjs --file your-file.pdf
   ```

---

## 📊 功能完成度

| 功能模块 | 完成度 | 状态 |
|----------|--------|------|
| **笔记管理** | 100% | ✅ 完整支持 |
| **知识库管理** | 100% | ✅ 完整支持 |
| **文件上传** | 100% | ✅ 完整支持 |
| **网页收藏** | 100% | ✅ 完整支持 |
| **搜索功能** | 100% | ✅ 完整支持 |
| **文件夹管理** | 100% | ✅ 完整支持 |

---

## 🎯 下一步行动

- [ ] 运行测试脚本验证 API 连接
- [ ] 测试上传文件功能
- [ ] 测试添加网页功能
- [ ] 与 LLM Wiki 知识库协同测试
- [ ] 与三向同步脚本集成

---

_文档创建：2026-04-16 · IMA Skills 知识库使用指南 v1.0_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[13-WorkBuddy-Sync/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始
- [[05-五行人格心理学/理论基石/系统配置_同步报告_20260417]] — 🔄 三向同步报告
- [[20-工作记录与复盘/02-每日日志/2026-04-15]] — 2026-04-15 日志
- [[20-工作记录与复盘/三向同步_三向同步系统整合方案]] — 第六步：三向同步系统整合方案 v1.0
- [[09-技能库/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[ψ技能体系/00-foundation/三向同步系统/QUICK_START]] — 🔗 三向同步系统 - 快速开始

<!-- AI-LINKS-END -->
