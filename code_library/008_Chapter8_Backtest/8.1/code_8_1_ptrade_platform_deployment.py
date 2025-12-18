"""
文件名: code_8_1_ptrade_platform_deployment.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_ptrade_platform_deployment.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: PTrade平台部署

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.ptrade_integration import PTradeConfig, PTradeDeployer

# 配置PTrade连接
ptrade_config = PTradeConfig(
    host="ptrade.gjzq.com",
    port=7709,
    account_id="8885019982",
    strategy_path="/path/to/ptrade/strategies"
)

# 创建部署器
deployer = PTradeDeployer(ptrade_config)

# 部署策略代码（聚宽风格 → PTrade格式）
strategy_code = load_strategy_code("strategies/my_strategy.py")
ptrade_code = deployer.convert_to_ptrade(strategy_code)

# 上传到PTrade平台
deployer.upload_strategy(
    strategy_name="my_strategy",
    strategy_code=ptrade_code
)

# 在PTrade平台执行回测
backtest_result = deployer.run_backtest(
    strategy_name="my_strategy",
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# 如果回测通过，启动实盘交易
if backtest_result.total_return > 0.15:  # 收益率超过15%
    deployer.start_live_trading("my_strategy")