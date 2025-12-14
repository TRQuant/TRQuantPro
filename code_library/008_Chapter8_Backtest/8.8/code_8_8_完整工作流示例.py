"""
文件名: code_8_8_完整工作流示例.py
保存路径: code_library/008_Chapter8_Backtest/8.8/code_8_8_完整工作流示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.8_Optimization_Suggestions_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 完整工作流示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 完整的回测后优化建议工作流
from core.bullettrade import BulletTradeEngine, BTConfig
from core.backtest_analyzer import BacktestAnalyzer
from core.optimization_suggestions import (
    ProblemIdentifier,
    OptimizationSuggestionGenerator,
    StrategyComparator
)

# 1. 执行回测
bt_engine = BulletTradeEngine(config)
bt_result = bt_engine.run_backtest(strategy_path, start_date, end_date)

# 2. 执行回测分析
analyzer = BacktestAnalyzer()
return_analysis = analyzer.analyze_returns(bt_result.equity_curve, bt_result.benchmark_curve)
risk_analysis = analyzer.analyze_risk(bt_result.equity_curve, bt_result.returns)
trade_analysis = analyzer.analyze_trades(bt_result.trades, bt_result.equity_curve)

# 3. 识别问题
problem_identifier = ProblemIdentifier()
problems = problem_identifier.identify_problems(
    return_analysis=return_analysis,
    risk_analysis=risk_analysis,
    trade_analysis=trade_analysis
)

# 4. 生成优化建议
suggestion_generator = OptimizationSuggestionGenerator()
suggestions = suggestion_generator.generate_suggestions(
    problems=problems,
    backtest_result=bt_result
)

# 5. 输出优化建议报告
print("=" * 60)
print("回测后优化建议报告")
print("=" * 60)

print(f"\n识别到 {len(problems)} 个问题:")
for i, problem in enumerate(problems, 1):
    print(f"\n{i}. [{problem['severity']}] {problem['category']}: {problem['problem']}")
    print(f"   描述: {problem['description']}")
    print(f"   建议: {problem['suggestion']}")

print(f"\n优化方向 ({len(suggestions['optimization_directions'])} 个):")
for direction in suggestions['optimization_directions']:
    print(f"\n{direction['category']} ({direction['priority']}优先级):")
    for rec in direction['recommendations']:
        print(f"  - {rec}")