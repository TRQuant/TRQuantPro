#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2026-01-13 陈小群战法完整回测测试脚本

功能：
1. 使用JQData获取历史价格数据
2. 考虑涨停、跌停、封板、炸板等规则
3. 根据策略算法决定买卖点
4. 多日回测，考虑历史持仓和周期
5. 生成完整的回测报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import json
from datetime import datetime, timedelta
import akshare as ak

from core.strategies.chen_xiaoqun import (
    ChenXiaoqunBacktestConfig,
    ChenXiaoqunBacktestEngine,
    judge_emotion_cycle_with_confirmation,
    identify_top_themes,
    select_first_board_stocks,
    select_dragon_stocks
)

# 尝试导入JQData
try:
    import jqdatasdk as jq
    from config.config_manager import get_config_manager
    JQ_AVAILABLE = True
except ImportError:
    JQ_AVAILABLE = False
    jq = None

class JQDataWrapper:
    """JQData包装类，提供统一的get_price接口"""
    def __init__(self, jq_module):
        self.jq = jq_module
    
    def get_price(self, security, start_date=None, end_date=None, frequency='daily', fields=None):
        """获取价格数据"""
        return self.jq.get_price(
            security,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            fields=fields
        )

def init_jqdata():
    """初始化JQData"""
    if not JQ_AVAILABLE:
        return None
    
    try:
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        if jq_config:
            jq.auth(jq_config['username'], jq_config['password'])
            print("✅ JQData认证成功")
            return JQDataWrapper(jq)
    except Exception as e:
        print(f"⚠️  JQData初始化失败: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def get_market_data(date_str: str, cache_file: Path):
    """获取市场数据"""
    with open(cache_file, 'r', encoding='utf-8') as f:
        cached_data = json.load(f)
    
    market_data = cached_data.get(date_str)
    if not market_data:
        return None
    
    # 获取涨停板DataFrame
    date_compact = date_str.replace('-', '')
    try:
        limit_up_df = ak.stock_zt_pool_em(date=date_compact)
    except:
        limit_up_df = None
    
    return {
        'limit_up_count': market_data.get('limit_up_count', 0),
        'zhaban_rate': market_data.get('zhaban_rate', 0),
        'max_height': market_data.get('max_height', 0),
        'limit_up_df': limit_up_df,
        'avg_inflow': market_data.get('avg_inflow', 0.0)
    }

def main():
    """主函数"""
    print("=" * 80)
    print("📊 2026-01-13 陈小群战法完整回测测试")
    print("=" * 80)
    
    # 1. 初始化JQData
    print("\n1️⃣ 初始化JQData...")
    jq_client = init_jqdata()
    if not jq_client:
        print("   ⚠️  无法使用JQData，将使用模拟价格")
    
    # 2. 准备回测数据（多日，考虑历史）
    print("\n2️⃣ 准备回测数据...")
    cache_file = Path('data/backtest_cache/chen_xiaoqun_market_data.json')
    
    # 回测日期范围（包含1.13及前几天）
    trade_days = ['2026-01-09', '2026-01-12', '2026-01-13']
    
    market_data_history = {}
    for date_str in trade_days:
        data = get_market_data(date_str, cache_file)
        if data:
            market_data_history[date_str] = data
            print(f"   ✅ {date_str}: 涨停{data['limit_up_count']}只, 炸板率{data['zhaban_rate']:.1f}%")
        else:
            print(f"   ⚠️  {date_str}: 数据缺失")
    
    if not market_data_history:
        print("   ❌ 无有效市场数据")
        return
    
    # 3. 创建回测引擎
    print("\n3️⃣ 创建回测引擎...")
    config = ChenXiaoqunBacktestConfig(
        start_date=trade_days[0],
        end_date=trade_days[-1],
        initial_capital=1000000.0,
        commission=0.0003,
        stamp_tax=0.001,
        slippage=0.001,
        stop_loss_pct=-0.10,
        take_profit_pct=0.20,
        max_holding_days=5
    )
    
    engine = ChenXiaoqunBacktestEngine(config)
    print(f"   ✅ 初始资金: {config.initial_capital:,.0f}元")
    
    # 4. 执行回测
    print("\n4️⃣ 执行回测...")
    print("   " + "-" * 76)
    
    result = engine.run(
        market_data_history=market_data_history,
        trade_days=trade_days,
        jq_client=jq_client,
        verbose=True
    )
    
    # 5. 生成详细报告
    print("\n" + "=" * 80)
    print("5️⃣ 详细回测报告")
    print("=" * 80)
    
    print(f"\n📊 回测概况:")
    print(f"   回测期间: {result.start_date} ~ {result.end_date}")
    print(f"   初始资金: {result.initial_capital:,.0f}元")
    print(f"   最终资金: {result.final_capital:,.0f}元")
    print(f"   总收益率: {result.total_return*100:.2f}%")
    print(f"   年化收益率: {result.annualized_return*100:.2f}%")
    print(f"   最大回撤: {result.max_drawdown*100:.2f}%")
    print(f"   夏普比率: {result.sharpe_ratio:.2f}")
    
    print(f"\n📈 交易统计:")
    print(f"   总交易次数: {result.total_trades}")
    buy_trades = [t for t in result.trades if t['action'] == 'buy']
    sell_trades = [t for t in result.trades if t['action'] == 'sell']
    print(f"   买入次数: {len(buy_trades)}")
    print(f"   卖出次数: {len(sell_trades)}")
    print(f"   胜率: {result.win_rate*100:.2f}%")
    print(f"   盈亏比: {result.profit_factor:.2f}")
    
    print(f"\n💼 当前持仓:")
    if engine.positions:
        for code, pos in engine.positions.items():
            print(f"   - {code}: {pos['shares']}股, 成本价{pos['cost']:.2f}元, 买入日期{pos['buy_date']}")
    else:
        print(f"   - 无持仓")
    
    print(f"\n📅 每日周期记录:")
    for cycle in result.daily_cycles:
        print(f"   {cycle['date']}: {cycle['cycle']} | {cycle['strategy']} | 目标仓位{cycle['position']:.2%}")
    
    print(f"\n💰 交易明细:")
    if result.trades:
        for i, trade in enumerate(result.trades, 1):
            print(f"\n   {i}. {trade['date']} - {trade['action'].upper()}")
            print(f"      股票: {trade['code']}")
            print(f"      数量: {trade['shares']}股")
            print(f"      价格: {trade['price']:.2f}元")
            print(f"      金额: {trade['amount']:,.0f}元")
            if 'pnl' in trade:
                print(f"      盈亏: {trade['pnl']:,.0f}元")
            if 'reason' in trade:
                print(f"      原因: {trade['reason']}")
    else:
        print(f"   ⚠️  无交易记录")
        print(f"\n   原因分析:")
        print(f"   1. 检查JQData是否可用: {'✅' if jq_client else '❌'}")
        print(f"   2. 检查选股结果: {len([s for s in market_data_history.values() if s.get('limit_up_df') is not None])}天有选股数据")
        print(f"   3. 检查价格数据: 需要JQData获取历史价格")
    
    print(f"\n🎯 策略统计:")
    for strategy, count in result.strategy_stats.items():
        print(f"   {strategy}: {count}次")
    
    print("\n" + "=" * 80)
    print("✅ 回测完成")
    print("=" * 80)
    
    return result

if __name__ == '__main__':
    result = main()
