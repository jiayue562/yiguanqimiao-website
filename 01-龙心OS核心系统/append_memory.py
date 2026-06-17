#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追加今天的工作记录到memory文件
"""

import os
from datetime import datetime

# Memory文件路径（注意：用户名包含单引号，需要使用双引号包裹原始字符串）
MEMORY_FILE = r"c:/Users/jia'yue/WorkBuddy/Claw/.workbuddy/memory/2026-05-25.md"

# 今天完成的工作记录
new_work = """

---

## 《09第九章 化克为生》深度学习与三库存储 (2026-05-25 23:46)

### 完成内容
1. **文档转换**：使用markitdown将《09第九章 化克为生-3489.docx》转换为Markdown格式
2. **深度学习**：逐行学习（每一行都不遗漏），挖掘5大核心知识点：
   - 五行相克关系（木克土、土克水、水克火、火克金、金克木）
   - 人我之间的相克（亲密关系、领导力、团队关系）
   - 化克为生的方法（通过生出对方的阳面属性来化解相克）
   - 自身五行相克的救治（个人内在五行失衡的调节方法）
   - 刚柔相济的智慧（土行的阴柔与阳刚两面性的应用）
3. **创建深度学习文档**（15.6KB）：
   - 核心摘要、详细内容学习（逐行深挖）
   - 知识图谱、核心金句、标签体系
   - 总索引、隐秘知识联系、实践应用
4. **创建知识图谱文件**（Mermaid格式）：
   - 理论关系图谱、测评对比图谱
   - 身心关系图谱、隐秘联系图谱
5. **建立双向链接**（7个）：
   - [[东西方心理学的殊途同归]]
   - [[五行人格测评题·完整题库与计分体系]]
   - [[凤脑OS]]
   - [[味藏店长龙爪]]
   - [[五行信任模型]]
   - [[五行人格心理学]]
   - [[凤心OS]]
6. **打标签**（主标签7个 + 关联标签20个）
7. **三库存储**：
   - ✅ Obsidian：`D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/`（2个文件）
   - ✅ IMA：上传到「以观其妙书院」知识库→「龙龟神将备份资料」文件夹（2个文件，note_id: 7464704767171135 + 7464704775558181）
   - ✅ LLM Wiki：`C:\\Users\\jia'yue/.workbuddy/wiki-knowledge/`（2个文件）

### 核心发现
1. **土行的两面性**：土行人可以表现阴柔一面（接近水）或阳刚一面（接近金），这是土行的调停者智慧
2. **功课在相生的一方**：主导者（生人者）需要承担更多责任，这与"责任越大，修行越大"异曲同工
3. **金水组合多于土金组合**：人性本能地选择"被照顾"而非"照顾别人"，这是人性趋利避害的真相
4. **生出阳面属性**：这与积极心理学的"优势导向"不谋而合
5. **通过相生链化解相克**：这是系统思维中的"增加反馈回路"

### 技术突破
- **IMA上传**：使用import_doc方法（media_type=11）绕过COS签名问题
- **Python脚本**：避免PowerShell here-document的编码问题
- **三库同步**：Obsidian + IMA + LLM Wiki 完整存储

### 下一步
- [ ] 将"化克为生"方法论整合到凤脑OS（L2理论基石）
- [ ] 创建"五行相克与转化"专题知识库
- [ ] 补充"化克为生"在亲密关系中的详细案例
- [ ] 将"土行两面性"写入五行人格心理学诊断指南
"""

def append_to_memory():
    """追加工作内容到memory文件"""
    try:
        # 读取现有内容
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 追加新内容
        content += new_work
        
        # 写回文件
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 获取更新后的文件大小
        file_size = os.path.getsize(MEMORY_FILE)
        
        print(f"✅ 已追加工作记录到Memory文件")
        print(f"📊 文件大小: {file_size} 字节")
        print(f"📝 追加内容: 《09第九章 化克为生》深度学习与三库存储")
        print(f"🔗 双向链接: 7个")
        print(f"🏷️  标签: 主标签7个 + 关联标签20个")
        print(f"📚 三库存储: Obsidian ✅ + IMA ✅ + LLM Wiki ✅")
        
        return True
        
    except Exception as e:
        print(f"❌ 追加失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("更新Memory文件...")
    print("=" * 60)
    
    if append_to_memory():
        print("\n" + "=" * 60)
        print("✅ Memory文件更新完成！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Memory文件更新失败！")
        print("=" * 60)
