"""
文件名: code_8_1_初始化BulletTrade引擎.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_初始化BulletTrade引擎.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 初始化BulletTrade引擎

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.bullettrade import BulletTradeEngine, BTConfig

# 创建回测配置
# 设计原理：配置参数分离，便于复用和测试
# 原因：不同策略可能需要不同的回测配置，分离配置便于管理
config = BTConfig(
    start_date="2023-01-01",
    end_date="2024-12-31",
    initial_capital=1000000,  # 设计考虑：初始资金影响回测结果，需要合理设置
    commission_rate=0.0003,  # 设计考虑：手续费率影响收益，需要与实际一致
    stamp_tax_rate=0.001,  # 设计考虑：印花税仅卖出时收取，需要准确模拟
    slippage=0.001,  # 设计考虑：滑点影响大单交易，需要合理估计
    benchmark="000300.XSHG",  # 设计考虑：基准用于计算超额收益，选择市场代表性指数
    data_provider="jqdata"  # 设计原理：使用JQData作为数据源，与策略生成保持一致
)

# 创建回测引擎
# 设计原理：引擎与配置分离，支持多配置复用
engine = BulletTradeEngine(config)

# 检查BulletTrade CLI可用性
# 设计原理：检查CLI可用性，不可用时降级到简化引擎
# 原因：CLI提供完整功能，简化引擎提供基本功能，保证系统可用性
if engine.check_cli_available():
    print("BulletTrade CLI可用")
else:
    print("警告：BulletTrade CLI不可用，将使用简化回测引擎")