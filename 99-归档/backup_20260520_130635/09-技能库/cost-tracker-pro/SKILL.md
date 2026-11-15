# cost-tracker-pro

## 技能简介
企业级 AI 模型成本管控工具，实时统计模型消耗、计算使用费用、实现成本管控，支持预算管理和优化建议。

## 核心功能
1. **成本统计**：实时统计 AI 模型调用成本
2. **预算管理**：设置预算和告警阈值
3. **优化建议**：基于使用模式提供优化建议
4. **报告生成**：自动生成成本分析报告
5. **多模型支持**：支持主流 AI 模型成本跟踪

## 支持的 AI 模型
- **OpenAI**：GPT-4o、GPT-4、GPT-3.5-Turbo、DALL·E、Whisper
- **Anthropic**：Claude 3、Claude 2
- **Google**：Gemini Pro、PaLM 2
- **微软**：Azure OpenAI、Copilot
- **开源模型**：Llama、Mistral、Qwen、DeepSeek
- **国内模型**：文心一言、通义千问、智谱GLM

## 安装方法
```bash
npm install -g cost-tracker-pro
```

## 使用示例
```javascript
const { CostTracker } = require('cost-tracker-pro');

// 初始化成本跟踪器
const tracker = new CostTracker({
  models: {
    'gpt-4o': { provider: 'openai', pricePerToken: 0.000005 },
    'claude-3-opus': { provider: 'anthropic', pricePerToken: 0.000015 },
    'gemini-pro': { provider: 'google', pricePerToken: 0.0000015 }
  },
  budget: {
    monthly: 1000, // 每月预算
    alertThreshold: 0.8, // 告警阈值 80%
    dailyLimit: 50 // 每日限制
  }
});

// 跟踪单个调用
async function trackAPICall(model, tokens, metadata = {}) {
  const cost = await tracker.record({
    model: model,
    inputTokens: tokens.input,
    outputTokens: tokens.output,
    timestamp: new Date(),
    userId: metadata.userId,
    projectId: metadata.projectId
  });

  // 检查预算
  const budgetStatus = await tracker.checkBudget();
  
  if (budgetStatus.exceeded) {
    console.warn(`预算超出: ${budgetStatus.current}/${budgetStatus.limit}`);
  }

  return cost;
}

// 生成成本报告
async function generateCostReport(period = 'monthly') {
  const report = await tracker.generateReport({
    period: period,
    breakdownBy: ['model', 'user', 'project'],
    includeRecommendations: true,
    includeTrends: true
  });

  // 优化建议
  const recommendations = report.recommendations;
  
  // 成本趋势
  const trends = report.trends;
  
  // 详细数据
  const detailedData = report.data;

  return report;
}
```

## 成本维度
1. **按模型**：不同模型的成本分布
2. **按用户**：不同用户的成本使用
3. **按项目**：不同项目的成本分配
4. **按时间**：每日、每周、每月成本趋势
5. **按功能**：不同功能模块的成本

## 预算管理功能
1. **预算设置**：设置总预算、部门预算、项目预算
2. **告警机制**：预算超支自动告警
3. **使用限制**：设置单用户、单项目使用限制
4. **配额管理**：分配和使用配额管理

## 优化建议系统
1. **模型选择建议**：基于任务推荐性价比高的模型
2. **使用模式优化**：优化 API 调用模式和频率
3. **缓存策略建议**：推荐缓存策略降低重复计算
4. **参数优化建议**：优化模型参数降低 token 消耗

## 报告功能
- **日报**：每日成本报告
- **周报**：每周成本趋势分析
- **月报**：月度预算使用报告
- **专项报告**：特定项目或用户使用报告
- **预测报告**：未来成本预测

## 集成能力
1. **财务管理系统**：与财务系统对接
2. **项目管理工具**：与 Jira、Asana 等集成
3. **监控告警系统**：集成告警通知
4. **API 网关**：实时成本控制

## 安全特性
1. **数据加密**：成本数据加密存储
2. **权限控制**：基于角色的成本数据访问
3. **审计日志**：完整操作记录
4. **合规性**：符合财务审计要求

## 版本信息
- 当前版本：1.6.0
- 最后更新：2026-03-19
- 社区评分：⭐⭐⭐⭐⭐ (4.9/5.0)

## 相关资源
- [官方文档](https://cost-tracker-pro.dev/docs)
- [GitHub 仓库](https://github.com/enterprise-agents/cost-tracker-pro)
- [API 参考](https://cost-tracker-pro.dev/api)