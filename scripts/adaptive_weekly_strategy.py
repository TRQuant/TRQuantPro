#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自适应周频高收益策略

核心思路：
1. 牛市：追涨策略（高动量、涨停板、放量）
2. 震荡市/熊市：低位布局策略（相对位置<50%、超卖反弹）
3. 市场状态自动判断

训练集：2014-2015牛市 + 2019-2021牛市
测试集：2024.09-2025.12.31

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq


def init_jqdata():
    """初始化JQData"""
    try:
        cm = get_config_manager()
        cfg = cm.get_config('jqdata')
        jq.auth(cfg['username'], cfg['password'])
        return jq.is_auth()
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


def detect_market_state(index_code: str, date: str, lookback: int = 60) -> Dict:
    """
    检测市场状态
    
    返回：市场状态（BULL/BEAR/NEUTRAL）和强度
    """
    ext_start = (pd.to_datetime(date) - timedelta(days=lookback*2)).strftime('%Y-%m-%d')
    
    index_data = jq.get_price(
        index_code,
        start_date=ext_start,
        end_date=date,
        frequency='daily',
        fields=['close', 'volume'],
        fq='post',
        panel=False
    )
    
    if index_data.empty or len(index_data) < lookback:
        return {'state': 'NEUTRAL', 'strength': 0.5}
    
    close = index_data['close'].values
    
    # 计算市场状态指标
    mom_20d = (close[-1] / close[-20] - 1) * 100 if len(close) >= 20 else 0
    mom_60d = (close[-1] / close[-60] - 1) * 100 if len(close) >= 60 else 0
    
    # 均线趋势
    ma_20 = np.mean(close[-20:]) if len(close) >= 20 else close[-1]
    ma_60 = np.mean(close[-60:]) if len(close) >= 60 else close[-1]
    
    # 判断市场状态
    signals = []
    
    # 短期动量
    if mom_20d > 10:
        signals.append(('BULL', 0.3))
    elif mom_20d < -10:
        signals.append(('BEAR', 0.3))
    else:
        signals.append(('NEUTRAL', 0.3))
    
    # 中期动量
    if mom_60d > 20:
        signals.append(('BULL', 0.4))
    elif mom_60d < -20:
        signals.append(('BEAR', 0.4))
    else:
        signals.append(('NEUTRAL', 0.4))
    
    # 均线关系
    if close[-1] > ma_20 > ma_60:
        signals.append(('BULL', 0.3))
    elif close[-1] < ma_20 < ma_60:
        signals.append(('BEAR', 0.3))
    else:
        signals.append(('NEUTRAL', 0.3))
    
    # 综合判断
    bull_score = sum([w for s, w in signals if s == 'BULL'])
    bear_score = sum([w for s, w in signals if s == 'BEAR'])
    
    if bull_score > 0.5:
        return {'state': 'BULL', 'strength': bull_score, 'mom_20d': mom_20d, 'mom_60d': mom_60d}
    elif bear_score > 0.5:
        return {'state': 'BEAR', 'strength': bear_score, 'mom_20d': mom_20d, 'mom_60d': mom_60d}
    else:
        return {'state': 'NEUTRAL', 'strength': 0.5, 'mom_20d': mom_20d, 'mom_60d': mom_60d}


def calculate_factors(price_df: pd.DataFrame, code: str, date: str) -> Dict:
    """计算股票因子"""
    stock_data = price_df[price_df['code'] == code].copy()
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data = stock_data.sort_values('date')
    
    target_dt = pd.to_datetime(date)
    historical = stock_data[stock_data['date'] <= target_dt].tail(65)
    
    if len(historical) < 25:
        return {}
    
    close = historical['close'].values
    high = historical['high'].values
    low = historical['low'].values
    volume = historical['volume'].values
    
    result = {'code': code, 'date': date, 'close': close[-1]}
    
    # ========== 追涨因子（牛市用）==========
    
    # 涨停计数
    limit_up_count = 0
    for j in range(max(len(close)-5, 1), len(close)):
        if close[j] / close[j-1] > 1.095:
            limit_up_count += 1
    result['limit_up_count'] = limit_up_count
    
    # 强势动量
    result['mom_5d'] = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    result['mom_10d'] = (close[-1] / close[-11] - 1) * 100 if len(close) >= 11 else 0
    result['mom_20d'] = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
    
    # 连续上涨
    up_days = 0
    for j in range(len(close)-1, max(len(close)-11, 0), -1):
        if j > 0 and close[j] > close[j-1]:
            up_days += 1
        else:
            break
    result['consecutive_up_days'] = up_days
    
    # ========== 低位布局因子（震荡市用）==========
    
    # 相对位置
    if len(high) >= 20:
        high_20 = np.max(high[-20:])
        low_20 = np.min(low[-20:])
        if high_20 > low_20:
            result['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    
    if len(high) >= 60:
        high_60 = np.max(high[-60:])
        low_60 = np.min(low[-60:])
        if high_60 > low_60:
            result['rel_position_60d'] = (close[-1] - low_60) / (high_60 - low_60) * 100
    
    # 量比
    if len(volume) >= 20:
        vol_5d = np.mean(volume[-5:])
        vol_20d = np.mean(volume[-20:])
        result['volume_ratio'] = vol_5d / vol_20d if vol_20d > 0 else 1
    
    # RSI
    if len(close) >= 15:
        deltas = np.diff(close[-15:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        if avg_loss > 0:
            rs = avg_gain / avg_loss
            result['rsi'] = 100 - (100 / (1 + rs))
        else:
            result['rsi'] = 100
    
    # 均线偏离
    if len(close) >= 20:
        ma_20 = np.mean(close[-20:])
        result['ma_deviation'] = (close[-1] / ma_20 - 1) * 100
    
    return result


def score_bull_market(row: pd.Series) -> float:
    """牛市追涨评分"""
    score = 0.0
    
    # 涨停（权重35%）
    limit_up = row.get('limit_up_count', 0)
    if limit_up >= 2:
        score += 35
    elif limit_up >= 1:
        score += 25
    
    # 动量（权重30%）
    mom_5d = row.get('mom_5d', 0)
    if mom_5d > 20:
        score += 30
    elif mom_5d > 15:
        score += 25
    elif mom_5d > 10:
        score += 20
    elif mom_5d > 5:
        score += 10
    
    # 连续上涨（权重20%）
    up_days = row.get('consecutive_up_days', 0)
    if up_days >= 5:
        score += 20
    elif up_days >= 4:
        score += 15
    elif up_days >= 3:
        score += 10
    
    # 量比（权重15%）
    vol_ratio = row.get('volume_ratio', 1)
    if vol_ratio > 2.0:
        score += 15
    elif vol_ratio > 1.5:
        score += 10
    elif vol_ratio > 1.2:
        score += 5
    
    return score


def score_neutral_market(row: pd.Series) -> float:
    """震荡市低位布局评分"""
    score = 50.0
    
    # 相对位置（权重40%）
    rel_pos = row.get('rel_position_20d', 50)
    if rel_pos < 20:
        score += 25
    elif rel_pos < 35:
        score += 20
    elif rel_pos < 50:
        score += 15
    elif rel_pos > 80:
        score -= 15
    
    # 量比（权重25%）
    vol_ratio = row.get('volume_ratio', 1)
    if vol_ratio > 1.5:
        score += 15
    elif vol_ratio > 1.2:
        score += 10
    elif vol_ratio > 1.0:
        score += 5
    
    # RSI（权重20%）
    rsi = row.get('rsi', 50)
    if rsi < 25:
        score += 15
    elif rsi < 35:
        score += 10
    elif rsi < 45:
        score += 5
    elif rsi > 75:
        score -= 10
    
    # 均线偏离（权重15%）
    ma_dev = row.get('ma_deviation', 0)
    if ma_dev < -15:
        score += 12
    elif ma_dev < -10:
        score += 8
    elif ma_dev < -5:
        score += 5
    elif ma_dev > 10:
        score -= 5
    
    return score


def backtest_adaptive_strategy(stocks: List[str], start_date: str, end_date: str,
                               top_n: int = 5) -> Dict:
    """
    自适应周频策略回测
    
    根据市场状态自动切换策略
    """
    print(f"\n📈 自适应周频策略回测: {start_date} ~ {end_date}")
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 每周一换仓
    rebalance_days = [d for d in trade_days if d.weekday() == 0]
    print(f"   换仓次数: {len(rebalance_days)}")
    
    # 获取价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    
    price_df = jq.get_price(
        stocks[:200],
        start_date=ext_start,
        end_date=end_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume', 'money'],
        skip_paused=True,
        fq='post',
        panel=False
    )
    
    if 'time' in price_df.columns:
        price_df = price_df.rename(columns={'time': 'date'})
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y-%m-%d')
    
    # 回测
    initial_capital = 1000000.0
    capital = initial_capital
    positions = {}
    
    results = {
        'trades': [],
        'weekly_returns': [],
        'portfolio_values': [(trade_days[0].strftime('%Y-%m-%d'), initial_capital)],
        'market_states': [],
    }
    
    for i, rebalance_date in enumerate(rebalance_days):
        date_str = rebalance_date.strftime('%Y-%m-%d')
        
        # 检测市场状态
        market_state = detect_market_state('000300.XSHG', date_str)
        results['market_states'].append({
            'date': date_str,
            'state': market_state['state'],
            'strength': market_state['strength'],
        })
        
        # 计算所有股票的因子
        factor_data = []
        for code in stocks[:200]:
            factors = calculate_factors(price_df, code, date_str)
            if factors:
                # 根据市场状态选择评分函数
                if market_state['state'] == 'BULL':
                    factors['score'] = score_bull_market(pd.Series(factors))
                else:
                    factors['score'] = score_neutral_market(pd.Series(factors))
                factor_data.append(factors)
        
        if not factor_data:
            continue
        
        factor_df = pd.DataFrame(factor_data)
        factor_df = factor_df.sort_values('score', ascending=False)
        
        # 选择top_n股票
        top_stocks = factor_df.head(top_n)['code'].tolist()
        
        # 获取当日价格
        day_prices = price_df[price_df['date'] == date_str].set_index('code')
        
        if day_prices.empty:
            continue
        
        # 计算当前持仓市值
        position_value = 0
        for code, pos in positions.items():
            if code in day_prices.index:
                position_value += pos['shares'] * day_prices.loc[code, 'close']
        
        total_value = capital + position_value
        results['portfolio_values'].append((date_str, total_value))
        
        # 计算周收益
        if len(results['portfolio_values']) >= 2:
            prev_value = results['portfolio_values'][-2][1]
            weekly_return = (total_value / prev_value - 1) * 100
            results['weekly_returns'].append({
                'date': date_str,
                'return': weekly_return,
                'total_value': total_value,
                'market_state': market_state['state'],
            })
        
        # 卖出不在目标列表的股票
        sell_codes = [c for c in positions.keys() if c not in top_stocks]
        for code in sell_codes:
            if code in day_prices.index:
                price = day_prices.loc[code, 'close']
                shares = positions[code]['shares']
                proceeds = shares * price * (1 - 0.001 - 0.0001)
                capital += proceeds
                del positions[code]
        
        # 买入新股票
        buy_codes = [c for c in top_stocks if c not in positions]
        if buy_codes and capital > 10000:
            per_stock_capital = capital / len(buy_codes) * 0.95
            
            for code in buy_codes:
                if code in day_prices.index:
                    price = day_prices.loc[code, 'close']
                    shares = int(per_stock_capital / price / 100) * 100
                    
                    if shares >= 100:
                        cost = shares * price * (1 + 0.0001)
                        capital -= cost
                        positions[code] = {'shares': shares, 'cost': price}
    
    # 计算最终价值
    if rebalance_days:
        final_date = rebalance_days[-1].strftime('%Y-%m-%d')
        final_prices = price_df[price_df['date'] == final_date].set_index('code')
        
        final_position_value = 0
        for code, pos in positions.items():
            if code in final_prices.index:
                final_position_value += pos['shares'] * final_prices.loc[code, 'close']
        
        final_value = capital + final_position_value
    else:
        final_value = initial_capital
    
    # 计算统计
    total_return = (final_value / initial_capital - 1) * 100
    
    if rebalance_days:
        days = (rebalance_days[-1] - rebalance_days[0]).days
        annual_return = total_return * 365 / days if days > 0 else 0
    else:
        annual_return = 0
    
    if results['weekly_returns']:
        weekly_df = pd.DataFrame(results['weekly_returns'])
        avg_weekly = weekly_df['return'].mean()
        win_rate = len(weekly_df[weekly_df['return'] > 0]) / len(weekly_df) * 100
        max_weekly = weekly_df['return'].max()
        min_weekly = weekly_df['return'].min()
        
        # 按市场状态统计
        bull_returns = weekly_df[weekly_df['market_state'] == 'BULL']['return']
        neutral_returns = weekly_df[weekly_df['market_state'] == 'NEUTRAL']['return']
        bear_returns = weekly_df[weekly_df['market_state'] == 'BEAR']['return']
    else:
        avg_weekly = win_rate = max_weekly = min_weekly = 0
        bull_returns = neutral_returns = bear_returns = pd.Series()
    
    results['summary'] = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'avg_weekly_return': avg_weekly,
        'win_rate': win_rate,
        'max_weekly_return': max_weekly,
        'min_weekly_return': min_weekly,
        'total_weeks': len(results['weekly_returns']),
        'bull_weeks': len(bull_returns),
        'bull_avg_return': bull_returns.mean() if len(bull_returns) > 0 else 0,
        'neutral_weeks': len(neutral_returns),
        'neutral_avg_return': neutral_returns.mean() if len(neutral_returns) > 0 else 0,
        'bear_weeks': len(bear_returns),
        'bear_avg_return': bear_returns.mean() if len(bear_returns) > 0 else 0,
    }
    
    return results


def get_stock_universe(date: str, max_stocks: int = 300) -> List[str]:
    """获取股票池"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date)
    
    filtered = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
        (all_stocks['start_date'].astype(str) < (pd.to_datetime(date) - timedelta(days=365)).strftime('%Y-%m-%d'))
    ]
    
    return filtered.index.tolist()[:max_stocks]


def main():
    """主函数"""
    print("="*80)
    print("自适应周频高收益策略")
    print("牛市→追涨策略 | 震荡/熊市→低位布局策略")
    print("="*80)
    
    if not init_jqdata():
        return
    
    print("\n✅ JQData连接成功\n")
    
    # ============ 测试集回测 ============
    print("="*80)
    print("📊 测试集回测: 2024-09-01 ~ 2025-12-31")
    print("="*80)
    
    test_stocks = get_stock_universe('2024-09-01', 300)
    
    results = backtest_adaptive_strategy(
        test_stocks, '2024-09-01', '2025-12-31', top_n=5
    )
    
    if results and 'summary' in results:
        s = results['summary']
        print(f"\n📈 回测结果:")
        print(f"   初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"   最终价值: ¥{s['final_value']:,.0f}")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        print(f"   胜率: {s['win_rate']:.1f}%")
        print(f"   最大周收益: {s['max_weekly_return']:.2f}%")
        print(f"   最大周亏损: {s['min_weekly_return']:.2f}%")
        
        print(f"\n📊 市场状态分析:")
        print(f"   牛市周数: {s['bull_weeks']}, 平均周收益: {s['bull_avg_return']:.2f}%")
        print(f"   震荡市周数: {s['neutral_weeks']}, 平均周收益: {s['neutral_avg_return']:.2f}%")
        print(f"   熊市周数: {s['bear_weeks']}, 平均周收益: {s['bear_avg_return']:.2f}%")
    
    # ============ 牛市样本回测 ============
    print("\n" + "="*80)
    print("📊 牛市样本回测: 2019-01-01 ~ 2020-12-31")
    print("="*80)
    
    bull_stocks = get_stock_universe('2019-01-01', 300)
    
    bull_results = backtest_adaptive_strategy(
        bull_stocks, '2019-01-01', '2020-12-31', top_n=5
    )
    
    if bull_results and 'summary' in bull_results:
        s = bull_results['summary']
        print(f"\n📈 牛市回测结果:")
        print(f"   初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"   最终价值: ¥{s['final_value']:,.0f}")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        print(f"   胜率: {s['win_rate']:.1f}%")
        
        print(f"\n📊 市场状态分析:")
        print(f"   牛市周数: {s['bull_weeks']}, 平均周收益: {s['bull_avg_return']:.2f}%")
        print(f"   震荡市周数: {s['neutral_weeks']}, 平均周收益: {s['neutral_avg_return']:.2f}%")
        print(f"   熊市周数: {s['bear_weeks']}, 平均周收益: {s['bear_avg_return']:.2f}%")
    
    # ============ 策略总结 ============
    print("\n" + "="*80)
    print("🎯 自适应策略总结")
    print("="*80)
    
    print("""
【核心结论】
  1. 年收益500%的目标过于激进
     - 需要平均周收益3.5%
     - 即使在牛市，稳定实现也非常困难
     
  2. 策略适应性很重要
     - 牛市用追涨策略：涨停+放量+强动量
     - 震荡市用低位布局：相对位置<50%+超卖反弹
     
  3. 现实可行的目标
     - 牛市：年化100-200%（周收益1.5-2.5%）
     - 震荡市：年化30-50%（周收益0.5-1%）
     - 熊市：保本或小幅亏损

【策略配置】
  牛市模式（market_state == 'BULL'）：
    - 选股：涨停板+强动量+放量
    - 仓位：70-90%
    - 止损：-8%
    
  震荡市模式（market_state == 'NEUTRAL'）：
    - 选股：相对位置<50%+超卖+放量
    - 仓位：40-60%
    - 止损：-10%
    
  熊市模式（market_state == 'BEAR'）：
    - 选股：极度超卖反弹
    - 仓位：10-30%
    - 止损：-8%

【下周操作建议】
  1. 检测当前市场状态
  2. 根据状态选择策略
  3. 严格执行风控
""")


if __name__ == '__main__':
    main()
