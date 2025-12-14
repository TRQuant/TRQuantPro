"""
文件名: code_8_5_从BulletTrade结果提取交易记录.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_从BulletTrade结果提取交易记录.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 从BulletTrade结果提取交易记录

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.bullettrade import BulletTradeEngine, BTConfig

# 执行BulletTrade回测
bt_engine = BulletTradeEngine(config)
bt_result = bt_engine.run_backtest(strategy_path, start_date, end_date)

# 提取交易记录
trades = bt_result.trades  # List[TradeRecord]