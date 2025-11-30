# 数据源快速参考

## 📊 可用API一览

| API | 数据源 | 状态 | 数据量 | 用途 |
|-----|--------|------|--------|------|
| 北向资金 | 东方财富 | ✅ | ~4条 | 外资流向 |
| 市场资金 | 东方财富 | ✅ | ~121条 | 大盘资金 |
| 涨停池 | 东方财富 | ✅ | ~70条 | 涨停股票 |
| 龙虎榜 | 东方财富 | ✅ | ~63条 | 游资动向 |
| 概念板块 | 同花顺 | ✅ | ~386条 | 概念热度 |
| 行业板块 | 同花顺 | ✅ | ~90条 | 行业轮动 |

## 🚀 快速使用

### 获取所有数据
```python
from markets.ashare.mainline import RealDataFetcher

fetcher = RealDataFetcher()
data = fetcher.fetch_all_data()

# 板块资金流向
for item in data['sector_flow'].data[:5]:
    print(f"{item['sector_name']}: {item['change_pct']:+.2f}%")
```

### 运行主线分析
```python
from markets.ashare.mainline import MainlineAnalysisEngine

engine = MainlineAnalysisEngine()
result = engine.run_full_analysis()

for ml in result['mainlines']:
    print(f"{ml.name}: {ml.score}分")
```

### 生成Cursor Prompt
```python
from markets.ashare.mainline import generate_analysis_prompt

prompt = generate_analysis_prompt()
# 复制到Cursor Chat
```

### 测试连接
```python
from markets.ashare.mainline import RealDataFetcher

fetcher = RealDataFetcher()
status = fetcher.test_all_connections()
print(status)
```

## 📁 文件位置

| 文件 | 路径 |
|------|------|
| 数据获取器 | `markets/ashare/mainline/real_data_fetcher.py` |
| 分析引擎 | `markets/ashare/mainline/analysis_engine.py` |
| Cursor集成 | `markets/ashare/mainline/cursor_integration.py` |
| 状态面板 | `gui/widgets/data_status_panel.py` |
| 缓存目录 | `~/.local/share/jqquant/cache/` |
| 分析输出 | `~/.local/share/jqquant/analysis_outputs/` |

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| 东方财富超时 | 已自动切换同花顺 |
| MongoDB未连接 | `sudo systemctl start mongod` |
| AKShare未安装 | `pip install akshare -U` |
| 数据为空 | 使用缓存数据 |

## 📈 数据字段

### 板块资金流向
- `sector_name`: 行业名称
- `change_pct`: 涨跌幅(%)
- `main_net_inflow`: 净流入(亿)
- `leader_stock`: 领涨股

### 概念板块
- `board_name`: 概念名称
- `change_pct`: 涨跌幅(%)
- `net_inflow`: 净流入(亿)
- `company_count`: 成分股数

### 北向资金
- `today_net`: 今日净流入(亿)
- `week_net`: 本周净流入(亿)
- `month_net`: 本月净流入(亿)

### 市场情绪
- `up_limit_count`: 涨停家数
- `down_limit_count`: 跌停家数
- `sentiment_score`: 情绪得分(0-100)

