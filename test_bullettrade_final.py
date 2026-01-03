#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade 完整测试
===================
测试 BulletTrade 回测功能，使用正确的 API
"""

import sys
from pathlib import Path

# 添加 extension/venv 到路径
extension_venv = Path(__file__).parent / "extension" / "venv" / "lib" / "python3.12" / "site-packages"
if extension_venv.exists():
    sys.path.insert(0, str(extension_venv))
    print(f"✅ 已添加路径: {extension_venv}")

print("=" * 60)
print("🧪 BulletTrade 完整回测测试")
print("=" * 60)

from core.bullettrade import BulletTradeEngine, BTConfig

# 创建配置
config = BTConfig(
    start_date="2024-01-01",
    end_date="2024-01-10",
    initial_capital=1000000,
    frequency="day"
)

print(f"\n📋 回测配置:")
print(f"   开始日期: {config.start_date}")
print(f"   结束日期: {config.end_date}")
print(f"   初始资金: {config.initial_capital:,.0f}")
print(f"   频率: {config.frequency}")

# 创建引擎
engine = BulletTradeEngine(config)
print("\n✅ BulletTradeEngine 创建成功")

# 使用正确的 BulletTrade API
strategy_code = '''
# 简单动量策略 - 使用正确的 BulletTrade API
def initialize(context):
    context.lookback = 5
    context.stocks = ['000001.XSHE', '600000.XSHG']
    context.total_value = context.portfolio.total_value

def handle_data(context, data):
    # 使用 order_target_value 而不是 order_target_percent
    # 每个股票分配 50% 的资金
    target_value = context.portfolio.total_value * 0.5
    
    for stock in context.stocks:
        # 获取当前持仓价值
        current_value = context.portfolio.positions.get(stock, {}).get('total_value', 0)
        
        # 计算需要调整的金额
        diff = target_value - current_value
        
        if abs(diff) > 100:  # 最小交易金额
            if diff > 0:
                # 买入
                order_target_value(stock, target_value)
            else:
                # 卖出
                order_target_value(stock, target_value)
'''

print("\n📝 策略代码 (使用正确的 API):")
print("   - 使用 order_target_value() 函数")
print("   - 每个股票分配 50% 资金")

# 执行回测
print("\n🚀 开始执行回测...")
try:
    result = engine.run_backtest(
        strategy_code=strategy_code,
        start_date="2024-01-01",
        end_date="2024-01-10"
    )
    
    print("\n✅ 回测执行完成！")
    print(f"\n📊 回测结果:")
    print(f"   总收益率: {result.total_return:.2f}%")
    print(f"   年化收益: {result.annual_return:.2f}%")
    print(f"   夏普比率: {result.sharpe_ratio:.2f}")
    print(f"   最大回撤: {result.max_drawdown:.2f}%")
    print(f"   日胜率: {result.win_rate:.2f}%")
    print(f"   交易胜率: {result.trade_win_rate:.2f}%")
    print(f"   交易天数: {result.trading_days}")
    print(f"   交易次数: {result.total_trades}")
    print(f"   初始资金: {result.initial_capital:,.2f}")
    print(f"   最终资金: {result.final_capital:,.2f}")
    print(f"   是否盈利: {result.is_profitable()}")
    print(f"   运行耗时: {result.runtime_seconds:.2f}秒")
    
    if result.report_path:
        print(f"\n📄 报告路径: {result.report_path}")
    if result.csv_path:
        print(f"📊 CSV路径: {result.csv_path}")
    
    # 获取详细指标
    metrics = result.get_metrics()
    print(f"\n📈 详细指标:")
    for key, value in list(metrics.items())[:5]:
        print(f"   {key}: {value}")
        
except Exception as e:
    print(f"\n❌ 回测执行失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ BulletTrade 测试完成！")
print("=" * 60)
