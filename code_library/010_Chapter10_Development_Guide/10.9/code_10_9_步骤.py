"""
文件名: code_10_9_步骤.py
保存路径: code_library/010_Chapter10_Development_Guide/10.9/code_10_9_步骤.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 步骤

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 批量回测（Walk-Forward）
backtest_results = workflow.run(
    workflow_type="backtest",
    mode="walk_forward",
    window_size=252,  # 一年
    step_size=63,     # 一个季度
    start_date="2020-01-01",
    end_date="2024-12-31"
)

# 2. 参数优化
optimizer_result = optimizer.run(
    strategy_code=strategy_code,
    parameters=["max_position", "stop_loss", "take_profit"],
    method="bayesian_optimization",
    n_trials=100
)

# 3. 数据质量门禁
quality_result = quality.validate(
    data_source="jqdata",
    data_type="ohlcv",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# 4. 对比报告
report_result = report.compare(
    baseline="backtest-batch-1",
    current="backtest-batch-2",
    metrics=["total_return", "sharpe_ratio", "max_drawdown", "win_rate"]
)

# 5. 任务记录
task_result = task_server.create(
    task_type="backtest_batch",
    batch_id="backtest-2024-12-12",
    status="completed",
    progress=100,
    results=backtest_results
)