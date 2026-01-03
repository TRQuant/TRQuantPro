"""
文件名: code_8_3_extract_nav_curve_from_bullettrade.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_extract_nav_curve_from_bullettrade.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 从BulletTrade结果提取净值曲线

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.bullettrade import BulletTradeEngine, BTConfig

# 执行BulletTrade回测
bt_engine = BulletTradeEngine(config)
bt_result = bt_engine.run_backtest(strategy_path, start_date, end_date)

# 提取净值曲线
equity_curve = bt_result.equity_curve  # DataFrame: date, equity
initial_equity = equity_curve['equity'].iloc[0]
final_equity = equity_curve['equity'].iloc[-1]