"""
文件名: code_8_1_执行回测.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_执行回测.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 执行回测

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 加载策略代码（聚宽风格）
strategy_path = "strategies/my_strategy.py"

# 执行回测
result = engine.run_backtest(
    strategy_path=strategy_path,
    start_date="2023-01-01",
    end_date="2024-12-31",
    frequency="day"  # 日线回测
)

# 获取回测结果
print(f"总收益率: {result.total_return:.2%}")
print(f"年化收益率: {result.annual_return:.2%}")
print(f"最大回撤: {result.max_drawdown:.2%}")
print(f"夏普比率: {result.sharpe_ratio:.2f}")

# 生成HTML报告
report_path = engine.generate_report(result, output_dir="backtest_results")
print(f"回测报告已生成: {report_path}")