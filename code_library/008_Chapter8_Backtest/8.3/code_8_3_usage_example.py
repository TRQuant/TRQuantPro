"""
文件名: code_8_3_使用示例.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 分析超额收益
analyzer = ExcessReturnAnalyzer()
result = analyzer.analyze_excess_return(
    bt_result.equity_curve,
    bt_result.benchmark_curve
)

print(f"策略总收益: {result['strategy_total_return']:.2%}")
print(f"基准总收益: {result['benchmark_total_return']:.2%}")
print(f"总超额收益: {result['total_excess_return']:.2%}")
print(f"年化超额收益: {result['annual_excess_return']:.2%}")
print(f"信息比率: {result['information_ratio']:.2f}")
print(f"跟踪误差: {result['tracking_error']:.2%}")