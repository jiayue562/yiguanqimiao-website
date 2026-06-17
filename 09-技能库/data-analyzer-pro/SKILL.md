# data-analyzer-pro

## 技能简介
专业级数据分析工具，支持自然语言查询、可视化图表生成、SQL/NoSQL 数据连接和高级统计分析。

## 核心功能
1. **自然语言查询**：用中文/英文提问，自动生成 SQL
2. **可视化图表**：自动生成图表（柱状图、折线图、饼图等）
3. **多数据源支持**：MySQL、PostgreSQL、MongoDB、CSV、Excel
4. **统计分析**：描述性统计、相关性分析、回归分析
5. **预测建模**：时间序列预测、分类模型

## 数据源支持
- **关系型数据库**：MySQL、PostgreSQL、SQLite、SQL Server
- **NoSQL 数据库**：MongoDB、Redis、Elasticsearch
- **文件格式**：CSV、Excel、JSON、Parquet
- **云服务**：Google BigQuery、AWS Redshift、Snowflake
- **API 数据**：REST API、GraphQL

## 安装方法
```bash
npm install -g data-analyzer-pro
```

## 使用示例
```python
# 自然语言查询示例
query = "分析2025年各季度的销售额趋势"
result = analyzer.query_natural_language(query)

# 可视化示例
chart = analyzer.create_chart(
    data=result,
    chart_type="line",
    x_axis="quarter",
    y_axis="sales"
)

# 统计分析示例
stats = analyzer.analyze_statistics(
    data=result,
    metrics=["mean", "std", "min", "max", "correlation"]
)
```

## 可视化类型
- **基础图表**：柱状图、折线图、饼图、散点图
- **高级图表**：热力图、桑基图、雷达图、箱线图
- **地理图表**：地图、轨迹图、热力地图
- **交互式图表**：支持缩放、筛选、高亮

## 机器学习功能
1. **预测分析**：ARIMA、Prophet、LSTM
2. **分类模型**：随机森林、XGBoost、神经网络
3. **聚类分析**：K-means、DBSCAN、层次聚类
4. **异常检测**：Isolation Forest、LOF、统计方法

## 版本信息
- 当前版本：3.2.0
- 最后更新：2026-03-19
- 社区评分：⭐⭐⭐⭐⭐ (4.7/5.0)

## 相关资源
- [官方文档](https://data-analyzer-pro.dev/docs)
- [GitHub 仓库](https://github.com/data-science-agents/data-analyzer-pro)
- [示例项目](https://github.com/data-analyzer-pro/examples)