# Sheet 表格操作参考文档

本文件包含腾讯文档 MCP 中 Sheet（在线表格）相关工具的完整 API 说明、详细调用示例、参数说明和返回值说明。

---

## 通用说明

### Sheet 工具概述

Sheet 工具专门用于操作腾讯文档中的在线表格（Excel格式），提供表格信息的查询、范围数据的获取以及批量更新等功能。

### 响应结构

所有 API 返回都包含：
- `error`: 错误信息（成功时为空）
- `trace_id`: 调用链追踪 ID


## 工具调用示例

## OperationSheet

### 功能说明
进行表格编辑操作的时候，通过生成对应操作的脚本代码，进行编辑操作。

#### 调用示例
```json
{
  "file_id": "doc_1234567890",
  "js_script": "
      // 获取当前活动的工作表
      const sheet = SpreadsheetApp.getActiveSheet();
      // 设置 A1 单元格的背景颜色为红色
      const range1 = sheet.getRange("A1");
      range1.setBackground("#ff0000");
      // 设置 A1:B2 范围的所有单元格为黄色背景
      const range2 = sheet.getRange("A1:B2");
      range2.setBackground("#ffff00");
  ",
  "sheet_id": "BB08J2",
}
```


#### 参数说明

- `file_id` (string 必填)：在线文档 ID
- `sheet_id` (string 非必填)：表格工作表 ID，如果获取不到，默认为 `BB08J2`
- `js_script` (string 必填)：JavaScript 脚本内容，如上例所示，通过 js-script-rule.md 生成对应脚本

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/resources_api_references]] — 腾讯文档 MCP 工具完整参考
- [[09-技能库/resources_sheet_references]] — Sheet 表格操作参考文档
- [[09-技能库/腾讯会议/references/api_references]] — 腾讯会议 MCP 工具完整参考
- [[09-技能库/腾讯文档/references/diagram_references]] — 图形化文档（思维导图 / 流程图）参考文档
- [[09-技能库/腾讯文档/references/slide_references]] — 幻灯片（Slide / PPT）参考文档
- [[09-技能库/腾讯文档/sheet/api/mcp-api]] — 腾讯文档 Sheet MCP 工具完整参考
- [[09-技能库/腾讯文档/sheet/api/operation-api]] — Sheet 表格操作参考文档
- [[ψ技能体系/30-tools/jinshuju/SKILL]] — 金数据（Jinshuju）操作专家
- [[ψ技能体系/30-tools/腾讯文档/sheet/mcp-api]] — 腾讯文档 Sheet MCP 工具完整参考

<!-- AI-LINKS-END -->
