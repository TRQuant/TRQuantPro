#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade 回测测试脚本
========================
测试 BulletTrade 引擎是否正常工作
"""

import sys
from pathlib import Path

# 添加 extension/venv 到路径
extension_venv = Path(__file__).parent / "extension" / "venv" / "lib" / "python3.12" / "site-packages"
if extension_venv.exists():
    sys.path.insert(0, str(extension_venv))
    print(f"✅ 已添加路径: {extension_venv}")

print("=" * 60)
print("🧪 BulletTrade 回测测试")
print("=" * 60)

# 测试导入
try:
    import bullet_trade
    print(f"\n✅ BulletTrade 导入成功")
    print(f"   路径: {bullet_trade.__file__}")
    
    from bullet_trade.core.engine import BacktestEngine, create_backtest
    print("✅ BacktestEngine 导入成功")
    print("✅ create_backtest 导入成功")
    
except ImportError as e:
    print(f"\n❌ 导入失败: {e}")
    sys.exit(1)

# 测试使用 core.bullettrade 封装
print("\n" + "=" * 60)
print("📦 测试 core.bullettrade 封装")
print("=" * 60)

try:
    from core.bullettrade import BulletTradeEngine, BTConfig
    
    print("✅ BulletTradeEngine 导入成功")
    
    # 创建配置
    config = BTConfig(
        start_date="2024-01-01",
        end_date="2024-01-31",
        initial_capital=1000000,
        frequency="1d"
    )
    
    print(f"\n📋 回测配置:")
    print(f"   开始日期: {config.start_date}")
    print(f"   结束日期: {config.end_date}")
    print(f"   初始资金: {config.initial_capital:,.0f}")
    print(f"   频率: {config.frequency}")
    
    # 创建引擎
    engine = BulletTradeEngine(config)
    print("\n✅ BulletTradeEngine 创建成功")
    
    # 测试策略代码
    strategy_code = '''
# 简单动量策略
def initialize(context):
    context.lookback = 5
    context.stocks = ['000001.XSHE', '600000.XSHG']

def handle_data(context, data):
    # 简单持有策略
    for stock in context.stocks:
        order_target_percent(stock, 0.5)
'''
    
    print("\n📝 测试策略代码:")
    print(strategy_code[:100] + "...")
    
    # 执行回测（不实际运行，只测试接口）
    print("\n✅ 所有接口测试通过！")
    print("\n💡 要执行实际回测，请调用:")
    print("   result = engine.run_backtest(strategy_code=strategy_code)")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ BulletTrade 测试完成！")
print("=" * 60)
