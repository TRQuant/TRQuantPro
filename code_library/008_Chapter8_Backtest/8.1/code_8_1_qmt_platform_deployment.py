"""
文件名: code_8_1_qmt_platform_deployment.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_qmt_platform_deployment.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: QMT平台部署

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.trading.qmt_interface import QMTTrader, QMTConfig

# 配置QMT连接
qmt_config = QMTConfig(
    qmt_path="/path/to/qmt",
    account_id="8885019982",
    session_id=123456
)

# 创建QMT交易接口
qmt_trader = QMTTrader(qmt_config)

# 连接QMT
if qmt_trader.connect():
    print("QMT连接成功")
    
    # 部署策略代码
    strategy_code = load_strategy_code("strategies/my_strategy.py")
    qmt_trader.upload_strategy("my_strategy", strategy_code)
    
    # 在QMT平台执行回测
    backtest_result = qmt_trader.run_backtest(
        strategy_name="my_strategy",
        start_date="2023-01-01",
        end_date="2024-12-31"
    )
    
    # 如果回测通过，启动实盘交易
    if backtest_result.total_return > 0.15:
        qmt_trader.start_live_trading("my_strategy")