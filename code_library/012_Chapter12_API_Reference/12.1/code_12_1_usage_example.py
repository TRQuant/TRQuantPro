"""
文件名: code_12_1_使用示例.py
保存路径: code_library/012_Chapter12_API_Reference/12.1/code_12_1_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/012_Chapter12_API_Reference/12.1_Module_API_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.bullettrade import BulletTradeEngine, BTConfig

# 创建回测配置
config = BTConfig(
    initial_capital=1000000,  # 初始资金
    commission=0.0003,  # 手续费率
    slippage=0.001,  # 滑点
)

# 初始化回测引擎
engine = BulletTradeEngine(config)

# 执行回测
result = engine.run_backtest(
    strategy_code=strategy_code,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# 查看结果
print(f"总收益率: {result['total_return']:.2%}")
print(f"年化收益率: {result['annual_return']:.2%}")
print(f"夏普比率: {result['sharpe_ratio']:.2f}")
print(f"最大回撤: {result['max_drawdown']:.2%}")