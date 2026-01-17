---
name: "生成分析报告"
description: "生成市场趋势分析HTML报告"
command: |
  cd notebooks/research && \
  python -c "
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent.parent
  sys.path.insert(0, str(project_root))
  
  from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
  from datetime import datetime
  import json
  
  config = MarketTrendAnalyzerConfig(scoring_style='smooth_grouped')
  analyzer = MarketTrendAnalyzer(config)
  result = analyzer.analyze('000300.XSHG', datetime.now().strftime('%Y-%m-%d'))
  
  # 生成报告
  report = {
      'date': datetime.now().strftime('%Y-%m-%d'),
      'trend_score': result.trend_score,
      'trend_direction': result.trend_direction.value,
      'market_regime': result.market_regime.value,
      'confidence': result.confidence
  }
  
  output_path = Path('output/reports/market_trend_report.json')
  output_path.parent.mkdir(parents=True, exist_ok=True)
  with open(output_path, 'w', encoding='utf-8') as f:
      json.dump(report, f, ensure_ascii=False, indent=2)
  
  print(f'报告已生成: {output_path}')
  "
---

# 生成分析报告命令

生成市场趋势分析报告，保存为JSON格式。

## 使用方式

在Cursor Chat中：
```
@generate-report
```

## 输出位置

`notebooks/research/output/reports/market_trend_report.json`
