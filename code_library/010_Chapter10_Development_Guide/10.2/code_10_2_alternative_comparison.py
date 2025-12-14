"""
文件名: code_10_2_alternative_comparison.py
保存路径: code_library/010_Chapter10_Development_Guide/10.2/code_10_2_alternative_comparison.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.2_Development_Principles_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 替代方案对比

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# core/ 模块划分示例
core/
├── data_source/          # 数据源模块
│   ├── jqdata_client.py  # JQData客户端
│   ├── akshare_client.py # AKShare客户端
│   └── data_source_manager.py  # 数据源管理器
│
├── market_analysis/      # 市场分析模块
│   ├── trend_analyzer.py # 趋势分析器
│   └── market_status.py  # 市场状态判断
│
├── mainline/            # 主线识别模块
│   ├── mainline_scanner.py  # 主线扫描器
│   └── mainline_scorer.py   # 主线评分器
│
├── candidate_pool/      # 候选池模块
│   ├── pool_builder.py  # 候选池构建器
│   └── stock_scorer.py  # 股票评分器
│
├── factor/              # 因子模块
│   ├── factor_calculator.py  # 因子计算器
│   └── factor_library.py     # 因子库
│
├── strategy/            # 策略模块
│   ├── strategy_generator.py  # 策略生成器
│   └── strategy_optimizer.py  # 策略优化器
│
└── backtest/            # 回测模块
    ├── bullettrade_engine.py  # BulletTrade引擎
    └── backtest_analyzer.py   # 回测分析器