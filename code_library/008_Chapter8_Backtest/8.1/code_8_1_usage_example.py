"""
文件名: code_8_1_使用示例.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 执行完整双层回测工作流
results = run_complete_backtest_workflow(
    strategy_path="strategies/my_strategy.py",
    start_date="2023-01-01",
    end_date="2024-12-31",
    deploy_to_ptrade=True,
    deploy_to_qmt=False
)

# 查看结果
print("\n回测结果汇总:")
print(f"内部回测（BulletTrade）: {results['internal_backtest']}")
print(f"PTrade回测: {results['ptrade_backtest']}")
print(f"部署状态: {results['deployment_status']}")