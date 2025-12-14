"""
文件名: code_8_2_使用示例.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 从BulletTrade回测结果中分析交易
trade_analyzer = TradeAnalyzer()

# 分析交易
trade_result = trade_analyzer.analyze_trades(
    trades=bt_result.trades,
    equity_curve=bt_result.equity_curve
)

print(f"交易次数: {trade_result['trade_count']}")
print(f"买入次数: {trade_result['buy_count']}")
print(f"卖出次数: {trade_result['sell_count']}")
print(f"胜率: {trade_result['win_rate']:.2%}")
print(f"盈亏比: {trade_result['profit_loss_ratio']:.2f}")
print(f"平均持仓周期: {trade_result['avg_holding_period']:.1f}天")
print(f"换手率: {trade_result['turnover_rate']:.2f}")
print(f"总手续费: {trade_result['total_commission']:.2f}")