---
name: "市场趋势分析"
description: "运行市场趋势分析，生成趋势信号和可视化图表"
command: |
  cd notebooks/research && \
  python -c "
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent.parent
  sys.path.insert(0, str(project_root))
  
  from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
  from datetime import datetime
  
  config = MarketTrendAnalyzerConfig(scoring_style='smooth_grouped')
  analyzer = MarketTrendAnalyzer(config)
  result = analyzer.analyze('000300.XSHG', datetime.now().strftime('%Y-%m-%d'))
  print(f'趋势得分: {result.trend_score}')
  print(f'趋势方向: {result.trend_direction.value}')
  print(f'市场状态: {result.market_regime.value}')
  "
---

# 市场趋势分析命令

执行市场趋势分析，使用MarketTrendAnalyzer分析当前市场趋势。

## 使用方式

在Cursor Chat中：
```
@market-trend-analysis
```

或在Agent模式中直接调用。

## 输出

- 趋势得分（-100到100）
- 趋势方向（强势上涨/上涨趋势/震荡盘整等）
- 市场状态（牛市/熊市/震荡）
- 置信度
