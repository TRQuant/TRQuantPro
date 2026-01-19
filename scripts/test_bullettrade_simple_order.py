#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade 回测验证脚本（最简单的订单方式）
============================================

使用最简单的order函数，不指定任何style参数
"""

import sys
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    print("=" * 70)
    print("🚀 BulletTrade 回测验证（最简单的订单方式）")
    print("=" * 70)
    
    try:
        # 1. 设置环境变量
        print("\n📦 步骤1: 设置JQData环境变量...")
        from config.config_manager import get_config_manager
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        
        os.environ['JQDATA_USER'] = jq_config['username']
        os.environ['JQDATA_PASSWORD'] = jq_config['password']
        os.environ['DEFAULT_DATA_PROVIDER'] = 'jqdata'
        print("   ✅ 环境变量已设置")
        
        # 2. 导入 BulletTrade 模块
        print("\n📦 步骤2: 导入 BulletTrade 模块...")
        from core.bullettrade.engine import BulletTradeEngine
        from core.bullettrade.config import BTConfig
        print("   ✅ 导入成功")
        
        # 3. 创建最简单的策略代码
        print("\n📝 步骤3: 创建最简单的策略代码...")
        strategy_code = '''
# 最简单的买入持有策略

from jqdata import *

def initialize(context):
    """初始化函数"""
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    context.stocks = ['000001.XSHE', '600000.XSHG']
    set_universe(context.stocks)
    context.bought = False

def handle_data(context, data):
    """每日处理函数"""
    if not context.bought:
        # 最简单的买入：使用order_value，不指定style
        for stock in context.stocks:
            if stock in data:
                # 每只股票买入25万（总资金50%）
                order_value(stock, 250000)
                log.info(f'[买入] {stock}, 金额: 250000')
        context.bought = True
    else:
        # 10天后卖出
        if (context.current_dt.date() - context.start_date.date()).days >= 10:
            for stock in context.stocks:
                if stock in context.portfolio.positions:
                    pos = context.portfolio.positions[stock]
                    if pos.total_amount > 0:
                        order_target(stock, 0)
                        log.info(f'[卖出] {stock}')
'''
        print("   ✅ 策略代码已创建（最简单的订单方式）")
        
        # 4. 配置回测参数（使用成功的日期范围：2020-07-01 至 2020-07-31）
        print("\n⚙️  步骤4: 配置回测参数...")
        config = BTConfig(
            start_date='2020-07-01',  # 使用成功记录的日期范围
            end_date='2020-07-31',
            initial_capital=1000000.0,
            benchmark='000300.XSHG',
            frequency='day',
            data_provider='jqdata',
        )
        print(f"   开始日期: {config.start_date}")
        print(f"   结束日期: {config.end_date}")
        print(f"   数据源: {config.data_provider}")
        print("   ✅ 配置完成")
        
        # 5. 创建回测引擎
        print("\n🔧 步骤5: 创建 BulletTrade 引擎...")
        engine = BulletTradeEngine(config)
        print("   ✅ 引擎创建成功")
        
        # 6. 执行回测
        print("\n⏳ 步骤6: 执行回测...")
        output_dir = PROJECT_ROOT / 'backtest_results' / 'test_simple_order'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        result = engine.run_backtest(
            strategy_code=strategy_code,
            output_dir=str(output_dir)
        )
        
        if result:
            print("\n✅ 回测执行成功！")
            
            # 读取metrics.json
            metrics_file = output_dir / 'metrics.json'
            if metrics_file.exists():
                import json
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    metrics = json.load(f)
                    if 'metrics' in metrics:
                        m = metrics['metrics']
                        print(f"\n📈 回测结果:")
                        print(f"   策略收益: {m.get('策略收益', 0):.2f}%")
                        print(f"   策略年化收益: {m.get('策略年化收益', 0):.2f}%")
                        print(f"   交易盈利次数: {m.get('交易盈利次数', 0)}")
                        print(f"   交易亏损次数: {m.get('交易亏损次数', 0)}")
                        
                        if 'meta' in metrics:
                            meta = metrics['meta']
                            initial = meta.get('initial_total_value', 0)
                            final = meta.get('final_total_value', 0)
                            print(f"\n   初始资金: {initial:,.2f}")
                            print(f"   最终资金: {final:,.2f}")
                            if final != initial:
                                print(f"   ✅ 产生了实际收益: {final - initial:,.2f} ({((final/initial-1)*100):.2f}%)")
        
        print("\n" + "=" * 70)
        print("✅ BulletTrade 回测验证完成！")
        print("=" * 70)
        return 0
        
    except Exception as e:
        print(f"\n❌ 回测失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
