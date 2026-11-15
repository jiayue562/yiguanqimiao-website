# 04-02-代码片段

_核心定义_: 可复用的代码片段、脚本、模板，提升开发效率。

---

## 详细内容

### Python
- **文件操作**
```python
# 读取文件
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 写入文件
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

- **目录遍历**
```python
import os
for root, dirs, files in os.walk('path'):
    for file in files:
        print(os.path.join(root, file))
```

### PowerShell
- **基础命令**
```powershell
# 列出文件
Get-ChildItem -Path "C:\path"

# 创建目录
New-Item -ItemType Directory -Path "C:\newdir"
```

### Bash
- **常用命令**
```bash
# 查找文件
find . -name "*.md"

# 批量重命名
for f in *.txt; do mv "$f" "${f%.txt}.md"; done
```

---

## 关联文件

- [[16-工具与资源]] - 返回上级
- [[NSF418C-04-01-软件工具]] - 软件配置
- [[NSF418C-04-419D-03-资源清单]] - 资源链接

---

## 核心金句

> "不要重复造轮子。"

---

## 标签

#代码 #脚本 #模板 #开发

---
_最后更新: 2026-03-22_

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[00-索引与导航/核心系统_00-01-思维模型]] — 00-01-思维模型
- [[00-索引与导航/核心系统_00-02-学习方法论]] — 00-02-学习方法论
- [[00-索引与导航/核心系统_00-03-知识管理]] — 00-03-知识管理
- [[01-核心体系/AI智能体_01-AI与智能体]] — 01-AI与智能体
- [[02-信仰文化体系/项目实践_02-01-进行中的项目]] — 02-01-进行中的项目
- [[02-信仰文化体系/项目实践_02-02-已完成项目]] — 02-02-已完成项目

<!-- AI-LINKS-END -->
