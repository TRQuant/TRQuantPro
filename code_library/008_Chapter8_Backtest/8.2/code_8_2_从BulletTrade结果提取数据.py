"""
文件名: code_8_2_从BulletTrade结果提取数据.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_从BulletTrade结果提取数据.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 从BulletTrade结果提取数据

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.backtest_analyzer import BacktestAnalyzer
from core.bullettrade import BulletTradeEngine

# 执行BulletTrade回测
bt_engine = BulletTradeEngine(config)
bt_result = bt_engine.run_backtest(strategy_path, start_date, end_date)

# 从BulletTrade结果中提取净值曲线
equity_curve = bt_result.equity_curve  # DataFrame: date, equity
benchmark_curve = bt_result.benchmark_curve  # DataFrame: date, equity

# 创建分析器
analyzer = BacktestAnalyzer()

# 分析收益
return_analysis = analyzer.analyze_returns(equity_curve, benchmark_curve)