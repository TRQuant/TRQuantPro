"""
文件名: code_8_8_使用示例.py
保存路径: code_library/008_Chapter8_Backtest/8.8/code_8_8_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.8_Optimization_Suggestions_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 对比策略版本
from core.optimization_suggestions import StrategyComparator

# 执行策略对比
comparator = StrategyComparator()
comparison = comparator.compare_strategies(
    strategy1_result={
        'return_metrics': return_analysis_v1,
        'risk_metrics': risk_analysis_v1,
        'trade_metrics': trade_analysis_v1
    },
    strategy2_result={
        'return_metrics': return_analysis_v2,
        'risk_metrics': risk_analysis_v2,
        'trade_metrics': trade_analysis_v2
    }
)

# 查看对比结果
print("收益对比:")
print(f"  总收益改进: {comparison['return_comparison']['total_return']['improvement']:.2%}")
print(f"  年化收益改进: {comparison['return_comparison']['annual_return']['improvement']:.2%}")

print("\n风险对比:")
print(f"  最大回撤改进: {comparison['risk_comparison']['max_drawdown']['improvement']:.2%}")
print(f"  夏普比率改进: {comparison['risk_comparison']['sharpe_ratio']['improvement']:.2f}")

print("\n交易对比:")
print(f"  胜率改进: {comparison['trade_comparison']['win_rate']['improvement']:.2%}")
print(f"  换手率改进: {comparison['trade_comparison']['turnover_rate']['improvement']:.2f}")