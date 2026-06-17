# 上下文工程标准操作流程

## SOP-01：上下文优化
1. 接收输入（session_id, context_items, max_tokens）
2. prioritizer 按优先级排序
3. summarizer 生成摘要
4. optimizer 执行裁剪
5. scorer 质量评分
6. 输出优化后的上下文

## SOP-02：跨 Skills 上下文传递
1. 发起方调用 shared-store.set(namespace, data)
2. dependency-tracker 记录依赖关系
3. 接收方调用 shared-store.get(namespace)
4. 协议验证（protocol.md）
5. 注入到接收方 Prompt
