"""
文件名: code_8_6_报告生成流程.py
保存路径: code_library/008_Chapter8_Backtest/8.6/code_8_6_报告生成流程.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.6_Backtest_Report_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 报告生成流程

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.backtest_report import BacktestReportGenerator
from core.bullettrade import BulletTradeEngine

# 执行回测和分析
bt_engine = BulletTradeEngine(config)
bt_result = bt_engine.run_backtest(strategy_path, start_date, end_date)

# 生成回测报告
report_generator = BacktestReportGenerator()
report = report_generator.generate_report(
    bt_result=bt_result,
    return_analysis=return_analysis,
    risk_analysis=risk_analysis,
    trade_analysis=trade_analysis
)