# 数据分析架构设计

> 参考《市场主流量化助手平台对比分析报告》和《机构级量化研究与实盘交易平台构建方案》

## 📚 学习总结

### 主流平台架构对比

| 平台 | 数据接入 | 分析方式 | AI能力 | 特点 |
|------|----------|----------|--------|------|
| **PandaAI** | TuShare Pro + 多源 | 可视化工作流 | 量化大模型 | 零代码拖拽 |
| **多平台AI助手** | 依赖目标平台 | 自然语言生成代码 | 专业Prompt | 跨平台适配 |
| **中金AIQuant** | 券商自有数据 | GUI+代码双模式 | 机器学习辅助 | 券商直连 |
| **韬睿量化** | 多数据源开放 | 代码为主 | Cursor集成 | 本地专业 |

### 关键设计理念

1. **数据中台**：统一数据接口，支持多数据源
2. **本地缓存**：MongoDB + 文件，减少API调用
3. **事件驱动**：回测与实盘一致的架构
4. **AI辅助**：LLM生成代码和分析

## 🏗️ 韬睿量化数据分析架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户界面层                                │
├─────────────────────────────────────────────────────────────────┤
│  GUI面板  │  Cursor IDE  │  命令行工具  │  Web API              │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        分析引擎层                                │
├─────────────────────────────────────────────────────────────────┤
│  MainlineAnalysisEngine  │  ScoringModel  │  LLM Analyzer       │
│  ├─ 数据采集             │  ├─ 六维评分    │  ├─ 政策分析        │
│  ├─ 数据验证             │  ├─ 权重计算    │  ├─ 行业分析        │
│  ├─ 板块分析             │  └─ 综合评级    │  ├─ 主线综合        │
│  ├─ 资金分析             │                 │  └─ 研报摘要        │
│  ├─ 情绪分析             │                 │                     │
│  └─ 主线综合             │                 │                     │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        数据获取层                                │
├─────────────────────────────────────────────────────────────────┤
│  RealDataFetcher                                                │
│  ├─ fetch_sector_flow()     板块资金流向                        │
│  ├─ fetch_concept_board()   概念板块行情                        │
│  ├─ fetch_northbound_flow() 北向资金                            │
│  ├─ fetch_market_sentiment() 市场情绪                           │
│  ├─ fetch_macro_data()      宏观数据                            │
│  └─ fetch_dragon_tiger()    龙虎榜                              │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                        数据源层                                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  AKShare    │  │  MongoDB    │  │  文件缓存   │             │
│  │  (实时API)  │  │  (本地缓存) │  │  (离线备份) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
│  优先级: AKShare → MongoDB → 文件缓存 → 示例数据                │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 模块结构

```
markets/ashare/mainline/
├── __init__.py              # 模块导出
├── real_data_fetcher.py     # 真实数据获取器
├── analysis_engine.py       # 主线分析引擎
├── cursor_integration.py    # Cursor IDE集成
├── scoring_model.py         # 评分模型
├── llm_analyzer.py          # LLM分析器
├── data_sources.py          # 数据源定义
└── engine.py                # 原有引擎（保留兼容）
```

## 🔌 数据源配置

### 数据源选择（已优化）

| API | 原数据源 | 现数据源 | 原因 |
|-----|----------|----------|------|
| 板块资金流向 | 东方财富 | **同花顺** | 东方财富反爬虫 |
| 概念板块 | 东方财富 | **同花顺** | 东方财富反爬虫 |
| 北向资金 | 东方财富 | 东方财富 | 正常 |
| 涨停池 | 东方财富 | 东方财富 | 正常 |
| 龙虎榜 | 东方财富 | 东方财富 | 正常 |

### AKShare接口（当前使用）
```python
# 板块资金流向（同花顺）
ak.stock_fund_flow_industry(symbol="即时")

# 概念板块（同花顺）
ak.stock_fund_flow_concept(symbol="即时")

# 北向资金（东方财富）
ak.stock_hsgt_fund_flow_summary_em()

# 涨停池（东方财富）
ak.stock_zt_pool_em(date="20251128")

# 龙虎榜（东方财富）
ak.stock_lhb_detail_em(start_date="20251128", end_date="20251128")
```

### MongoDB（缓存层）
```python
# 连接配置
mongo_uri = "mongodb://localhost:27017"
db_name = "jqquant"

# 缓存结构
{
    "key": "sector_flow",
    "data": [...],
    "updated_at": datetime
}
```

## 🎯 使用方式

### 1. 命令行分析
```python
from markets.ashare.mainline import MainlineAnalysisEngine

engine = MainlineAnalysisEngine()
result = engine.run_full_analysis()

for ml in result['mainlines']:
    print(f"{ml.name}: {ml.score}分")
```

### 2. 生成Cursor Prompt
```python
from markets.ashare.mainline import generate_analysis_prompt

prompt = generate_analysis_prompt()
# 复制到Cursor Chat进行深度分析
```

### 3. 快速分析
```python
from markets.ashare.mainline import quick_analysis

prompt = quick_analysis()
```

### 4. 策略开发Prompt
```python
from markets.ashare.mainline import strategy_prompt

prompt = strategy_prompt("人工智能")
```

## 📊 分析流程

1. **数据采集** → 从AKShare获取实时数据
2. **数据验证** → 检查完整性和时效性
3. **板块分析** → 资金流向、概念热度
4. **资金分析** → 北向资金、主力方向
5. **情绪分析** → 涨跌停、市场情绪
6. **主线综合** → 多维度识别投资主线
7. **报告生成** → 生成Cursor分析Prompt

## 🔮 未来规划

### 短期（1-2周）
- [x] 创建数据状态面板
- [x] 修复东方财富API问题（切换同花顺）
- [x] 添加API连接测试功能
- [ ] 添加数据质量监控

### 中期（1-2月）
- [ ] 接入TuShare Pro数据源
- [ ] 实现因子计算引擎
- [ ] 开发回测集成模块

### 长期（3-6月）
- [ ] 接入Wind/Choice专业数据
- [ ] 开发Cursor VSCode插件
- [ ] 实现策略自动生成

## 📝 相关文档

| 文档 | 说明 |
|------|------|
| [DATA_SOURCE_DEVELOPMENT.md](DATA_SOURCE_DEVELOPMENT.md) | 完整开发文档 |
| [DATA_SOURCE_QUICK_REF.md](DATA_SOURCE_QUICK_REF.md) | 快速参考 |

## 📚 参考资料

1. **PandaAI量化平台** - 可视化工作流架构
2. **多平台AI量化助手** - 跨平台代码生成
3. **中金AIQuant** - 券商量化终端集成
4. **QuantConnect LEAN** - 模块化回测引擎
5. **vn.py** - 事件驱动交易框架

## 📅 更新日志

### 2025-11-28
- ✅ 创建数据状态面板 (`data_status_panel.py`)
- ✅ 修复北向资金API（使用 `stock_hsgt_fund_flow_summary_em`）
- ✅ 替换东方财富板块API为同花顺
- ✅ 添加API连接测试功能
- ✅ 集成数据状态面板到GUI
- ✅ 创建开发文档

