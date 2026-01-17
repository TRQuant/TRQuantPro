#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSPI股票预测性因子回测

基于2019-2021牛市研究发现，应用预测性因子组合到PSPI股票，
并验证周频/月频换仓的回报率。

核心预测因子（基于研究）:
1. 相对位置 < 50% （中期预测力最强，收益差19.37%）
2. 量比 > 1.1 （底部放量信号）
3. RSI < 50 （超卖区域）
4. 均线偏离 < 0 （低于20日均线）

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

# 确保项目路径
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq


def init_jqdata():
    """初始化JQData连接"""
    try:
        cm = get_config_manager()
        cfg = cm.get_config('jqdata')
        jq.auth(cfg['username'], cfg['password'])
        
        if jq.is_auth():
            print("✅ JQData连接成功")
            return True
        return False
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


# PSPI概念股票
PSPI_STOCKS = {
    '688323.XSHG': '瑞华泰',
    '000859.XSHE': '国风新材',
    '600458.XSHG': '时代新材',
    '300054.XSHE': '鼎龙股份',
    '002643.XSHE': '万润股份',
    '002254.XSHE': '泰和新材',
    '300429.XSHE': '强力新材',
}


def calculate_predictive_factors(price_df: pd.DataFrame, code: str, date: str) -> Dict:
    """计算预测性因子"""
    stock_data = price_df[price_df['code'] == code].copy()
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data = stock_data.sort_values('date')
    
    target_dt = pd.to_datetime(date)
    historical = stock_data[stock_data['date'] <= target_dt].tail(60)
    
    if len(historical) < 20:
        return {}
    
    close = historical['close'].values
    high = historical['high'].values
    low = historical['low'].values
    volume = historical['volume'].values
    
    result = {
        'code': code,
        'date': date,
        'close': close[-1],
    }
    
    # 1. 相对位置（最强预测因子）- 越低越好
    if len(high) >= 20:
        high_20 = np.max(high[-20:])
        low_20 = np.min(low[-20:])
        if high_20 > low_20:
            result['rel_position'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    
    # 2. 量比 - 底部放量
    if len(volume) >= 20:
        vol_5d = np.mean(volume[-5:])
        vol_20d = np.mean(volume[-20:])
        result['volume_ratio'] = vol_5d / vol_20d if vol_20d > 0 else 1
    
    # 3. RSI - 超卖区域
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
    
    # 4. 均线偏离 - 低于均线更好
    if len(close) >= 20:
        ma_20 = np.mean(close[-20:])
        result['ma_deviation'] = (close[-1] / ma_20 - 1) * 100
    
    # 5. 波动率
    if len(close) >= 20:
        result['volatility'] = np.std(close[-20:]) / np.mean(close[-20:]) * 100
    
    # 6. 动量（作为参考，不作为主要选股依据）
    if len(close) >= 6:
        result['mom_5d'] = (close[-1] / close[-6] - 1) * 100
    if len(close) >= 21:
        result['mom_20d'] = (close[-1] / close[-21] - 1) * 100
    
    return result


def calculate_predictive_score(row: pd.Series) -> float:
    """
    计算预测性评分
    
    基于研究结论：
    - 相对位置 < 50% 最强预测（收益差19.37%）
    - 量比 > 1.1 底部放量（收益差13.33%）
    - RSI < 50 超卖区域
    - 均线偏离 < 0 低于均线
    """
    score = 50.0  # 基础分
    
    # 1. 相对位置（权重40%）- 最强预测因子
    rel_pos = row.get('rel_position', 50)
    if rel_pos < 30:
        score += 20  # 极低位，最佳
    elif rel_pos < 50:
        score += 15  # 低位，较好
    elif rel_pos < 70:
        score += 5   # 中位
    else:
        score -= 10  # 高位，风险
    
    # 2. 量比（权重25%）- 底部放量
    vol_ratio = row.get('volume_ratio', 1)
    if vol_ratio > 1.5:
        score += 15  # 明显放量
    elif vol_ratio > 1.2:
        score += 10  # 小幅放量
    elif vol_ratio > 1.0:
        score += 5   # 略有放量
    elif vol_ratio < 0.7:
        score -= 5   # 缩量
    
    # 3. RSI（权重20%）- 超卖区域
    rsi = row.get('rsi', 50)
    if rsi < 30:
        score += 12  # 超卖，弹性最大
    elif rsi < 40:
        score += 8   # 偏低
    elif rsi < 50:
        score += 5   # 中性偏低
    elif rsi > 70:
        score -= 10  # 超买风险
    
    # 4. 均线偏离（权重15%）- 低于均线更好
    ma_dev = row.get('ma_deviation', 0)
    if ma_dev < -10:
        score += 10  # 大幅偏离，超卖
    elif ma_dev < -5:
        score += 7
    elif ma_dev < 0:
        score += 4   # 略低于均线
    elif ma_dev > 10:
        score -= 5   # 过度偏离均线
    
    return min(max(score, 0), 100)


def backtest_predictive_strategy(stocks: List[str], start_date: str, end_date: str,
                                  rebalance_freq: str = 'weekly') -> Dict:
    """
    回测预测性因子策略
    
    参数:
    - stocks: 股票列表
    - start_date: 开始日期
    - end_date: 结束日期
    - rebalance_freq: 换仓频率 ('weekly' 或 'monthly')
    """
    print(f"\n📊 回测预测性因子策略: {start_date} ~ {end_date}, 频率: {rebalance_freq}")
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 确定换仓日期
    if rebalance_freq == 'weekly':
        rebalance_days = trade_days[::5]
    else:
        rebalance_days = trade_days[::20]
    
    # 获取完整价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    
    try:
        price_df = jq.get_price(
            stocks,
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
    except Exception as e:
        print(f"❌ 获取价格数据失败: {e}")
        return {}
    
    # 回测参数
    initial_capital = 1000000.0
    capital = initial_capital
    positions = {}
    max_positions = 3
    
    results = {
        'trades': [],
        'portfolio_values': [],
        'factor_history': [],
    }
    
    for rebalance_date in rebalance_days:
        date_str = rebalance_date.strftime('%Y-%m-%d')
        
        # 计算所有股票的预测性因子
        factor_data = []
        for code in stocks:
            factors = calculate_predictive_factors(price_df, code, date_str)
            if factors:
                factor_data.append(factors)
        
        if not factor_data:
            continue
        
        factor_df = pd.DataFrame(factor_data)
        factor_df['score'] = factor_df.apply(calculate_predictive_score, axis=1)
        factor_df['name'] = factor_df['code'].map(PSPI_STOCKS)
        factor_df = factor_df.sort_values('score', ascending=False)
        
        # 记录因子历史
        results['factor_history'].append({
            'date': date_str,
            'factors': factor_df[['code', 'name', 'score', 'rel_position', 'volume_ratio', 'rsi', 'ma_deviation']].to_dict('records')
        })
        
        # 选择得分最高的股票
        top_stocks = factor_df.head(max_positions)['code'].tolist()
        
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
        
        results['portfolio_values'].append({
            'date': date_str,
            'capital': capital,
            'position_value': position_value,
            'total_value': total_value,
        })
        
        # 卖出不在目标列表的股票
        sell_codes = [c for c in positions.keys() if c not in top_stocks]
        for code in sell_codes:
            if code in day_prices.index:
                price = day_prices.loc[code, 'close']
                shares = positions[code]['shares']
                proceeds = shares * price * (1 - 0.001 - 0.0001)
                capital += proceeds
                
                pnl = proceeds - positions[code]['shares'] * positions[code]['cost']
                pnl_pct = (price / positions[code]['cost'] - 1) * 100
                
                results['trades'].append({
                    'date': date_str,
                    'code': code,
                    'name': PSPI_STOCKS.get(code, ''),
                    'action': 'SELL',
                    'shares': shares,
                    'price': price,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                })
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
                        
                        # 获取买入时的因子值
                        stock_factors = factor_df[factor_df['code'] == code].iloc[0] if len(factor_df[factor_df['code'] == code]) > 0 else None
                        
                        results['trades'].append({
                            'date': date_str,
                            'code': code,
                            'name': PSPI_STOCKS.get(code, ''),
                            'action': 'BUY',
                            'shares': shares,
                            'price': price,
                            'pnl': 0,
                            'score': stock_factors['score'] if stock_factors is not None else 0,
                            'rel_position': stock_factors.get('rel_position', 0) if stock_factors is not None else 0,
                            'volume_ratio': stock_factors.get('volume_ratio', 0) if stock_factors is not None else 0,
                        })
    
    # 计算最终价值
    final_date = trade_days[-1].strftime('%Y-%m-%d')
    final_prices = price_df[price_df['date'] == final_date].set_index('code')
    
    final_position_value = 0
    for code, pos in positions.items():
        if code in final_prices.index:
            final_position_value += pos['shares'] * final_prices.loc[code, 'close']
    
    final_value = capital + final_position_value
    total_return = (final_value / initial_capital - 1) * 100
    
    days = (trade_days[-1] - trade_days[0]).days
    annual_return = total_return * 365 / days if days > 0 else 0
    
    # 计算胜率
    trades_df = pd.DataFrame(results['trades'])
    if not trades_df.empty:
        sell_trades = trades_df[trades_df['action'] == 'SELL']
        if len(sell_trades) > 0:
            win_rate = len(sell_trades[sell_trades['pnl'] > 0]) / len(sell_trades) * 100
        else:
            win_rate = 0
    else:
        win_rate = 0
    
    results['summary'] = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'total_trades': len(results['trades']),
        'win_rate': win_rate,
        'days': days,
    }
    
    return results


def main():
    """主函数"""
    print("="*80)
    print("PSPI股票预测性因子回测")
    print("="*80)
    print(f"\n分析日期: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    # 初始化
    if not init_jqdata():
        return
    
    stocks = list(PSPI_STOCKS.keys())
    
    # 获取最新交易日
    trade_days = jq.get_trade_days(end_date=datetime.now(), count=5)
    latest_date = trade_days[-1].strftime('%Y-%m-%d')
    
    print(f"最新交易日: {latest_date}\n")
    
    # ============ 1. 当前预测性因子分析 ============
    print("="*80)
    print("📊 当前预测性因子分析")
    print("="*80)
    
    ext_start = (pd.to_datetime(latest_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    price_df = jq.get_price(
        stocks,
        start_date=ext_start,
        end_date=latest_date,
        frequency='daily',
        fields=['open', 'close', 'high', 'low', 'volume', 'money'],
        skip_paused=True,
        fq='post',
        panel=False
    )
    
    if 'time' in price_df.columns:
        price_df = price_df.rename(columns={'time': 'date'})
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y-%m-%d')
    
    factor_data = []
    for code in stocks:
        factors = calculate_predictive_factors(price_df, code, latest_date)
        if factors:
            factor_data.append(factors)
    
    factor_df = pd.DataFrame(factor_data)
    factor_df['score'] = factor_df.apply(calculate_predictive_score, axis=1)
    factor_df['name'] = factor_df['code'].map(PSPI_STOCKS)
    factor_df = factor_df.sort_values('score', ascending=False)
    
    print(f"\n{'股票':<12} {'预测评分':>8} {'相对位置':>8} {'量比':>6} {'RSI':>6} {'均线偏离':>8} {'5日动量':>8}")
    print("-"*80)
    
    for _, row in factor_df.iterrows():
        rel_pos = row.get('rel_position', 0) or 0
        vol_r = row.get('volume_ratio', 0) or 0
        rsi = row.get('rsi', 0) or 0
        ma_dev = row.get('ma_deviation', 0) or 0
        mom_5d = row.get('mom_5d', 0) or 0
        
        # 预测性标记
        pred_mark = ""
        if rel_pos < 50 and vol_r > 1.1:
            pred_mark = " ★★★"
        elif rel_pos < 50:
            pred_mark = " ★★"
        elif vol_r > 1.2:
            pred_mark = " ★"
        
        print(f"{row['name']:<12} {row['score']:>8.1f} {rel_pos:>7.1f}% {vol_r:>6.2f} "
              f"{rsi:>6.1f} {ma_dev:>7.2f}% {mom_5d:>7.2f}%{pred_mark}")
    
    print("\n📌 预测性选股建议（基于研究）:")
    print("   ★★★ = 相对位置<50% + 量比>1.1（最佳预测组合）")
    print("   ★★  = 相对位置<50%（强预测信号）")
    print("   ★   = 量比>1.2（底部放量信号）")
    
    # ============ 2. 回测验证 ============
    print("\n" + "="*80)
    print("📈 回测验证（过去6个月）")
    print("="*80)
    
    end_date = latest_date
    start_date = (pd.to_datetime(end_date) - timedelta(days=180)).strftime('%Y-%m-%d')
    
    # 周频回测
    print("\n" + "-"*40)
    print("【周频换仓回测】（预测性因子策略）")
    print("-"*40)
    
    weekly_results = backtest_predictive_strategy(stocks, start_date, end_date, 'weekly')
    
    if weekly_results and 'summary' in weekly_results:
        s = weekly_results['summary']
        print(f"\n周频回测结果:")
        print(f"  初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"  最终价值: ¥{s['final_value']:,.0f}")
        print(f"  总收益率: {s['total_return']:.2f}%")
        print(f"  年化收益: {s['annual_return']:.2f}%")
        print(f"  交易次数: {s['total_trades']}")
        print(f"  胜率: {s['win_rate']:.1f}%")
    
    # 月频回测
    print("\n" + "-"*40)
    print("【月频换仓回测】（预测性因子策略）")
    print("-"*40)
    
    monthly_results = backtest_predictive_strategy(stocks, start_date, end_date, 'monthly')
    
    if monthly_results and 'summary' in monthly_results:
        s = monthly_results['summary']
        print(f"\n月频回测结果:")
        print(f"  初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"  最终价值: ¥{s['final_value']:,.0f}")
        print(f"  总收益率: {s['total_return']:.2f}%")
        print(f"  年化收益: {s['annual_return']:.2f}%")
        print(f"  交易次数: {s['total_trades']}")
        print(f"  胜率: {s['win_rate']:.1f}%")
    
    # ============ 3. 综合建议 ============
    print("\n" + "="*80)
    print("🎯 综合投资建议")
    print("="*80)
    
    if weekly_results and monthly_results:
        w_ret = weekly_results['summary']['total_return']
        m_ret = monthly_results['summary']['total_return']
        w_win = weekly_results['summary']['win_rate']
        m_win = monthly_results['summary']['win_rate']
        
        print(f"\n📊 换仓频率对比:")
        print(f"  周频换仓: {w_ret:.2f}%, 胜率{w_win:.1f}%")
        print(f"  月频换仓: {m_ret:.2f}%, 胜率{m_win:.1f}%")
        
        if w_ret > m_ret:
            print(f"  ➡️ 建议：周频换仓更优（高出{w_ret - m_ret:.2f}%）")
        else:
            print(f"  ➡️ 建议：月频换仓更优（高出{m_ret - w_ret:.2f}%）")
    
    # 当前推荐
    print("\n📌 当前投资推荐（基于预测性因子）:")
    top_stocks = factor_df.head(3)
    for idx, (_, row) in enumerate(top_stocks.iterrows(), 1):
        rel_pos = row.get('rel_position', 0) or 0
        vol_r = row.get('volume_ratio', 0) or 0
        
        pred_signal = []
        if rel_pos < 50:
            pred_signal.append(f"相对位置低({rel_pos:.1f}%)")
        if vol_r > 1.1:
            pred_signal.append(f"量比放大({vol_r:.2f})")
        
        signal_str = ", ".join(pred_signal) if pred_signal else "等待更好信号"
        
        print(f"  {idx}. {row['name']}({row['code']}): 评分={row['score']:.1f}")
        print(f"     预测信号: {signal_str}")
    
    print("\n⚠️ 风险提示:")
    print("  1. 预测性因子基于历史牛市研究，需结合当前市场环境")
    print("  2. 相对位置<50%是最强预测信号（历史收益差19.37%）")
    print("  3. 量比>1.1表示底部有资金关注")
    print("  4. 建议仓位: 单票≤15%, 总仓位≤50%")
    print("  5. 止损位: -10%")


if __name__ == '__main__':
    main()
