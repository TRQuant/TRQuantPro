#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
陈小群战法周回测报告生成器

功能：
1. 以周为周期进行回测
2. 考虑T+1规则（买入后第二天才能卖出）
3. 显示持仓和盈亏信息
4. 显示公司名称
5. 生成完整的周回测报告
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import json
from datetime import datetime, timedelta
import akshare as ak
from typing import Dict, List

from core.strategies.chen_xiaoqun import (
    ChenXiaoqunBacktestConfig,
    ChenXiaoqunBacktestEngine,
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
    
    def get_security_info(self, code):
        """获取证券信息"""
        return self.jq.get_security_info(code)
    
    def get_all_securities(self, types=None, date=None):
        """获取所有证券列表"""
        return self.jq.get_all_securities(types=types, date=date)

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

def get_stock_names(jq_client, codes: List[str]) -> Dict[str, str]:
    """获取股票名称"""
    stock_names = {}
    
    if not jq_client:
        return stock_names
    
    try:
        # 方法1：批量获取所有股票信息
        all_securities = jq_client.get_all_securities(types=['stock'], date=None)
        if all_securities is not None and not all_securities.empty:
            for code in codes:
                if code in all_securities.index:
                    stock_names[code] = all_securities.loc[code, 'display_name']
    except Exception as e:
        print(f"⚠️  批量获取股票名称失败: {e}")
    
    # 方法2：逐个获取（如果批量失败）
    for code in codes:
        if code not in stock_names:
            try:
                info = jq_client.get_security_info(code)
                if info:
                    stock_names[code] = info.display_name
            except Exception as e:
                stock_names[code] = code  # 使用代码作为名称
    
    return stock_names

def get_weekly_trade_days(end_date: str = None, weeks: int = 1) -> List[str]:
    """
    获取指定周数的交易日期
    
    Args:
        end_date: 结束日期（默认今天）
        weeks: 周数（默认1周，2周则weeks=2）
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    end = datetime.strptime(end_date, '%Y-%m-%d')
    start = end - timedelta(days=7 * weeks)
    
    dates = []
    current = start
    while current <= end:
        if current.weekday() < 5:  # 周一到周五
            dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    return dates

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
    print("📊 陈小群战法两周回测报告")
    print("=" * 80)
    
    # 1. 初始化JQData
    print("\n1️⃣ 初始化JQData...")
    jq_client = init_jqdata()
    if not jq_client:
        print("   ⚠️  无法使用JQData，将使用模拟价格")
    
    # 2. 获取最近两周的交易日期
    print("\n2️⃣ 获取最近两周的交易日期...")
    trade_days = get_weekly_trade_days('2026-01-15', weeks=2)
    print(f"   日期范围: {trade_days[0]} ~ {trade_days[-1]}")
    print(f"   交易天数: {len(trade_days)}天")
    for date in trade_days:
        print(f"     - {date}")
    
    # 3. 准备回测数据
    print("\n3️⃣ 准备回测数据...")
    cache_file = Path('data/backtest_cache/chen_xiaoqun_market_data.json')
    
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
    
    # 4. 创建回测引擎
    print("\n4️⃣ 创建回测引擎...")
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
    
    # 5. 执行回测
    print("\n5️⃣ 执行回测...")
    print("   " + "-" * 76)
    
    result = engine.run(
        market_data_history=market_data_history,
        trade_days=trade_days,
        jq_client=jq_client,
        verbose=True
    )
    
    # 6. 获取股票名称
    print("\n6️⃣ 获取股票名称...")
    all_codes = set()
    for trade in result.trades:
        if 'code' in trade:
            all_codes.add(trade['code'])
    for code in engine.positions.keys():
        all_codes.add(code)
    
    stock_names = get_stock_names(jq_client, list(all_codes))
    print(f"   ✅ 获取到 {len(stock_names)} 只股票名称")
    
    # 7. 生成详细报告
    print("\n" + "=" * 80)
    print("📊 两周回测详细报告")
    print("=" * 80)
    
    print(f"\n【回测概况】")
    print(f"   回测期间: {result.start_date} ~ {result.end_date}")
    print(f"   交易天数: {len(trade_days)}天")
    print(f"   初始资金: {result.initial_capital:,.0f}元")
    print(f"   最终资金: {result.final_capital:,.0f}元")
    print(f"   总收益率: {result.total_return*100:.2f}%")
    print(f"   年化收益率: {result.annualized_return*100:.2f}%")
    print(f"   最大回撤: {result.max_drawdown*100:.2f}%")
    print(f"   夏普比率: {result.sharpe_ratio:.2f}")
    
    print(f"\n【交易统计】")
    print(f"   总交易次数: {result.total_trades}")
    buy_trades = [t for t in result.trades if t['action'] == 'buy']
    sell_trades = [t for t in result.trades if t['action'] == 'sell']
    print(f"   买入次数: {len(buy_trades)}")
    print(f"   卖出次数: {len(sell_trades)}")
    print(f"   胜率: {result.win_rate*100:.2f}%")
    
    if sell_trades:
        total_profit = sum(t.get('pnl', 0) for t in sell_trades if t.get('pnl', 0) > 0)
        total_loss = abs(sum(t.get('pnl', 0) for t in sell_trades if t.get('pnl', 0) <= 0))
        profit_factor = total_profit / total_loss if total_loss > 0 else 0
        print(f"   盈亏比: {profit_factor:.2f}")
    
    print(f"\n【每日周期和策略】")
    for cycle in result.daily_cycles:
        print(f"   {cycle['date']}: {cycle['cycle']} | {cycle['strategy']} | 目标仓位{cycle['position']:.2%}")
    
    print(f"\n【交易明细】（考虑T+1规则）")
    if result.trades:
        for i, trade in enumerate(result.trades, 1):
            stock_name = stock_names.get(trade['code'], trade['code'])
            print(f"\n   {i}. {trade['date']} - {trade['action'].upper()}")
            print(f"      股票: {stock_name} ({trade['code']})")
            print(f"      数量: {trade['shares']}股")
            print(f"      价格: {trade['price']:.2f}元")
            print(f"      金额: {trade['amount']:,.0f}元")
            if 'pnl' in trade and trade['pnl'] != 0:
                pnl_pct = (trade['pnl'] / (trade['shares'] * trade.get('price', 1))) * 100 if trade.get('shares', 0) > 0 else 0
                print(f"      盈亏: {trade['pnl']:,.0f}元 ({pnl_pct:.2f}%)")
            if 'reason' in trade:
                print(f"      原因: {trade['reason']}")
            
            # T+1规则提示
            if trade['action'] == 'buy':
                buy_date = datetime.strptime(trade['date'], '%Y-%m-%d')
                next_trade_date = (buy_date + timedelta(days=1)).strftime('%Y-%m-%d')
                # 找到下一个交易日
                if next_trade_date in trade_days:
                    print(f"      ⚠️  T+1规则: 最早可卖出日期 {next_trade_date}")
    else:
        print(f"   ⚠️  无交易记录")
    
    print(f"\n【当前持仓】（含盈亏信息）")
    if engine.positions:
        # 获取持仓股票的最新价格
        position_codes = list(engine.positions.keys())
        if jq_client:
            latest_date = trade_days[-1]
            price_data = engine._get_stock_prices(position_codes, latest_date, jq_client)
        else:
            price_data = {}
        
        total_position_value = 0
        total_pnl = 0
        
        for code, pos in engine.positions.items():
            stock_name = stock_names.get(code, code)
            cost = pos['cost']
            shares = pos['shares']
            cost_basis = cost * shares
            
            # 获取当前价格
            if code in price_data:
                if isinstance(price_data[code], dict):
                    current_price = price_data[code].get('close', cost)
                else:
                    current_price = price_data[code]
            else:
                current_price = cost
            
            current_value = current_price * shares
            pnl = current_value - cost_basis
            pnl_pct = (current_price - cost) / cost * 100
            
            total_position_value += current_value
            total_pnl += pnl
            
            # 计算持仓天数
            buy_date = datetime.strptime(pos['buy_date'], '%Y-%m-%d')
            latest_date_obj = datetime.strptime(trade_days[-1], '%Y-%m-%d')
            holding_days = (latest_date_obj - buy_date).days
            
            print(f"\n   📈 {stock_name} ({code})")
            print(f"      持仓数量: {shares}股")
            print(f"      成本价: {cost:.2f}元")
            print(f"      当前价: {current_price:.2f}元")
            print(f"      成本金额: {cost_basis:,.0f}元")
            print(f"      当前市值: {current_value:,.0f}元")
            print(f"      浮动盈亏: {pnl:,.0f}元 ({pnl_pct:.2f}%)")
            print(f"      买入日期: {pos['buy_date']}")
            print(f"      持仓天数: {holding_days}天")
            
            # T+1规则检查
            if holding_days == 0:
                print(f"      ⚠️  T+1规则: 今日买入，明日才能卖出")
        
        print(f"\n   【持仓汇总】")
        print(f"      持仓数量: {len(engine.positions)}只")
        print(f"      持仓市值: {total_position_value:,.0f}元")
        print(f"      总浮动盈亏: {total_pnl:,.0f}元")
        print(f"      现金: {engine.cash:,.0f}元")
        print(f"      总权益: {engine.cash + total_position_value:,.0f}元")
    else:
        print(f"   - 无持仓")
    
    print(f"\n【策略执行统计】")
    for strategy, count in result.strategy_stats.items():
        print(f"   {strategy}: {count}次")
    
    print(f"\n【每日权益变化】")
    for eq in result.daily_equity:
        print(f"   {eq['date']}: 权益{eq['equity']:,.0f}元, 现金{eq['cash']:,.0f}元, 持仓{eq['position_count']}只, 持仓市值{eq['position_value']:,.0f}元")
    
    print("\n" + "=" * 80)
    print("✅ 周回测报告生成完成")
    print("=" * 80)
    
    return result

if __name__ == '__main__':
    result = main()
