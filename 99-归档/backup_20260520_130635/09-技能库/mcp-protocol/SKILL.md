# MCP协议配置 Skill

## 核心定位

个人AI OS的**通用协同语言**，打通人机、机机的共生联动链路。

> 核心理念：MCP是"协同总线"，解决异构系统的信息孤岛问题。

---

## 触发条件

- 用户提到"MCP"、"协同协议"、"系统联动"
- 需要配置多个Skills/工具的协同
- 需要定义人机协同的数据格式
- 需要扩展外部工具/服务接入

---

## 三大核心MCP协议

### 1. 人机协同协议

**定义**：规范人向AI发出的决策指令、AI向人反馈的执行结果的格式

```json
{
  "protocol": "human-ai-collaboration",
  "version": "1.0",
  "instruction": {
    "type": "decision | query | task",
    "content": "指令内容",
    "personalization": {
      "thinking_model": "第一性原理/长期主义/GEO...",
      "cultural_tag": "儒家/佛学/道家...",
      "personality": "理性/感性/专业/生活化",
      "values": ["核心价值观1", "核心价值观2"]
    }
  },
  "response": {
    "type": "result | explanation | question",
    "content": "返回内容",
    "reasoning": "推理过程说明",
    "confidence": 0.95,
    "references": ["参考文档1", "参考文档2"]
  }
}
```

### 2. 机内协同协议

**定义**：规范AI与Skills、AI与Skills之间的调用规则、数据同步格式

```json
{
  "protocol": "intra-system-collaboration",
  "version": "1.0",
  "task": {
    "id": "task-uuid",
    "parent_id": "父任务ID",
    "description": "任务描述",
    "required_skills": ["skill1", "skill2"],
    "input_data": {},
    "output_schema": {}
  },
  "skill_chain": [
    {
      "skill": "skill-name",
      "input": {},
      "output": {},
      "status": "pending|running|completed|failed"
    }
  ],
  "data_flow": {
    "from": "skill-a",
    "to": "skill-b",
    "transform": "数据转换规则"
  }
}
```

### 3. 系统扩展协议

**定义**：规范外部工具/服务接入AI OS的通信规则

```json
{
  "protocol": "system-extension",
  "version": "1.0",
  "service": {
    "name": "服务名称",
    "type": "tool|skill|api|knowledge_base",
    "endpoint": "接入地址",
    "capabilities": ["能力1", "能力2"],
    "authentication": {
      "type": "api_key|oauth|token",
      "credentials": "加密存储"
    }
  },
  "integration": {
    "mcp_config": "MCP配置文件",
    "capability_mapping": "能力映射",
    "fallback_strategy": "降级策略"
  }
}
```

---

## 个性化参数嵌入

所有MCP协议都嵌入个性化参数字段：

```json
{
  "personalization": {
    "thinking_model": "思维模型标识",
    "cultural_dna": "文化DNA标签",
    "personality_params": {
      "tone": "语气偏好",
      "detail_level": "详细程度",
      "response_style": "回复风格"
    },
    "values_alignment": ["核心价值1", "价值2"]
  }
}
```

---

## 现有MCP配置

### WorkBuddy MCP服务器

位置：`C:\Users\jia'yue\.workbuddy\mcp.json`

```json
{
  "mcpServers": {
    "ima-knowledge": {
      "command": "npx",
      "args": ["@clawhub/ima-mcp-server"],
      "env": {
        "IMA_API_KEY": "已配置",
        "IMA_CLIENT_ID": "59a1edb848ec905552c0fbc8041213bf"
      }
    }
  }
}
```

---

## 与其他Skills协同

| 协同Skill | 协同方式 |
|-----------|---------|
| CLI指令体系 | 解析指令中的个性化参数 |
| Skills管理 | 提供Skills调用的标准协议 |
| Framework | 作为框架的通信底层 |
| 人机协同五象限 | 支撑分工协作的数据传递 |

---

## 协议验证工具

### 验证命令

```bash
# 验证人机协同协议
python mcp_validator.py --protocol human-ai --file instruction.json

# 验证机内协同协议
python mcp_validator.py --protocol intra-system --file task.json

# 验证系统扩展协议
python mcp_validator.py --protocol extension --file service.json
```

---

## 存储位置

- **协议配置**: `C:\Users\jia'yue\Desktop\以观其妙书院知识库\观其妙书院\05-系统配置\MCP协议\`
- **验证工具**: `08-工具与脚本\MCP验证\`
- **使用日志**: `05-系统配置\MCP协议\使用日志.md`

---

## 核心原则

1. **标准化** - 所有协同通过协议规范
2. **个性化嵌入** - 默认携带信仰/文化/思维模型参数
3. **轻量化** - 适配个人场景，极简高效
4. **可扩展** - 新工具无缝接入

---

*MCP协议配置 Skill v1.0 · 2026-03-19*
