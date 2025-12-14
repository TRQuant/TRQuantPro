"""
文件名: code_8_8_00.py
保存路径: code_library/008_Chapter8_Backtest/8.8/code_8_8_00.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.8_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.strategy_optimizer import StrategyOptimizer

# 初始化策略优化器
optimizer = StrategyOptimizer()

# 执行策略优化
optimization_result = optimizer.optimize(
    strategy=initial_strategy,
    market_context=market_context,  # 来自步骤2
    mainlines=mainlines,  # 来自步骤3
    candidate_pool=candidate_pool,  # 来自步骤4
    factor_recommendations=factor_recommendations,  # 来自步骤5
    backtest_result=backtest_result,  # 来自步骤7
    optimization_config={
        "target_metric": "sharpe_ratio",
        "direction": "maximize",
        "parameters": {
            "lookback_period": {"type": "range", "min": 10, "max": 30},
            "threshold": {"type": "range", "min": 0.01, "max": 0.1}
        },
        "algorithm": "ai_driven",
        "iterations": 50
    }
)

# 获取优化后的策略
optimized_strategy = optimization_result["optimized_strategy"]

# 对比优化前后
comparison = optimizer.compare(
    strategy_1=initial_strategy,
    strategy_2=optimized_strategy
)