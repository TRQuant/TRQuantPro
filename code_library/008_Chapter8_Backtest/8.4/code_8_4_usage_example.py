"""
文件名: code_8_4_使用示例.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 分析最大回撤
analyzer = MaxDrawdownAnalyzer()
result = analyzer.analyze_max_drawdown(bt_result.equity_curve)

print(f"最大回撤: {result['max_drawdown']:.2%}")
print(f"最大回撤开始日期: {result['max_dd_start_date']}")
print(f"最大回撤结束日期: {result['max_dd_end_date']}")
print(f"最大回撤持续时间: {result['max_dd_duration']}天")
if result['recovery_date']:
    print(f"回撤恢复日期: {result['recovery_date']}")
    print(f"回撤恢复时间: {result['recovery_duration']}天")