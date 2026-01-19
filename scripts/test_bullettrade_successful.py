#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade 回测验证脚本（基于成功回测记录）
============================================

参考成功的回测记录（26.56%收益），使用相同的策略模式
"""

import sys
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    print("=" * 70)
    print("🚀 BulletTrade 回测验证（基于成功回测记录）")
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
        
        # 3. 创建策略代码（参考成功记录，使用简单的order函数）
        print("\n📝 步骤3: 创建策略代码（使用order函数）...")
        strategy_code = '''
# 买入持有策略（使用order函数，参考成功回测记录）

from jqdata import *

def initialize(context):
    """初始化函数"""
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点和佣金
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    # 股票池
    context.stocks = ['000001.XSHE', '600000.XSHG']
    
    # 设置股票池
    set_universe(context.stocks)
    
    # 持仓比例
    context.position_ratio = 0.5
    
    # 持有天数
    context.hold_days = 10
    context.buy_date = None
    context.bought = False
    
    log.info(f'策略初始化完成，股票池: {context.stocks}')

def handle_data(context, data):
    """每日处理函数"""
    current_date = context.current_dt.date()
    
    # 第一天买入
    if not context.bought:
        total_value = context.portfolio.total_value
        target_value_per_stock = total_value * context.position_ratio
        
        # 使用get_current_data()获取当前数据
        current_data = get_current_data()
        
        for stock in context.stocks:
            # 检查股票是否有数据
            if stock in current_data:
                # 获取当前价格
                current_price = current_data[stock].last_price
                
                # 计算目标股数（使用order函数，按数量下单）
                target_shares = int(target_value_per_stock / current_price / 100) * 100  # 按手数（100股）
                
                if target_shares > 0:
                    # 使用order函数按数量买入（不指定style，使用默认订单类型）
                    order(stock, target_shares)
                    log.info(f'[买入] 日期: {current_date}, 股票: {stock}, 数量: {target_shares}, 价格: {current_price:.2f}')
            else:
                log.warn(f'[跳过] 股票 {stock} 不在current_data中')
        
        context.bought = True
        context.buy_date = current_date
    
    # 持有N天后卖出
    elif context.buy_date is not None:
        days_held = (current_date - context.buy_date).days
        
        if days_held >= context.hold_days:
            for stock in context.stocks:
                # 检查是否有持仓
                if stock in context.portfolio.positions:
                    position = context.portfolio.positions[stock]
                    # 检查持仓数量
                    if hasattr(position, 'total_amount') and position.total_amount > 0:
                        # 使用order函数卖出（负数表示卖出）
                        order(stock, -position.total_amount)
                        log.info(f'[卖出] 日期: {current_date}, 股票: {stock}, 数量: {position.total_amount}, 持有天数: {days_held}')
            
            context.buy_date = None
'''
        print("   ✅ 策略代码已创建（使用order函数按数量下单）")
        
        # 4. 配置回测参数
        print("\n⚙️  步骤4: 配置回测参数...")
        config = BTConfig(
            start_date='2024-09-01',
            end_date='2024-10-31',
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
        output_dir = PROJECT_ROOT / 'backtest_results' / 'test_successful'
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
                        print(f"   交易天数: {m.get('交易天数', 0)}")
                        
                        if 'meta' in metrics:
                            meta = metrics['meta']
                            initial = meta.get('initial_total_value', 0)
                            final = meta.get('final_total_value', 0)
                            print(f"\n   初始资金: {initial:,.2f}")
                            print(f"   最终资金: {final:,.2f}")
                            if final != initial:
                                print(f"   ✅ 产生了实际收益: {final - initial:,.2f} ({((final/initial-1)*100):.2f}%)")
                            else:
                                print(f"   ⚠️  收益为0，可能订单未成交")
            
            # 检查日志
            log_file = output_dir / 'backtest.log'
            if log_file.exists():
                print("\n📋 关键日志（买入/卖出/订单/成交）:")
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 查找关键信息
                    key_words = ['买入', '卖出', '订单', '成交', '持仓', 'ERROR', 'WARNING', '取消', '撮合', '限价']
                    lines = [line for line in content.split('\n') 
                            if any(word in line for word in key_words)]
                    for line in lines[:30]:
                        if line.strip():
                            print(f"     {line.strip()}")
        
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
