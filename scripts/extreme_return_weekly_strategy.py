#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
极端高收益周频策略

目标：年收益500%（周收益3.5%）
核心：只在高概率信号出现时交易，否则持现金

策略特点：
1. 极度集中持仓（1-3只）
2. 严格信号触发条件
3. 严格止损止盈
4. 空仓等待机制

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
    try:
        cm = get_config_manager()
        cfg = cm.get_config('jqdata')
        jq.auth(cfg['username'], cfg['password'])
        return jq.is_auth()
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


def get_stock_universe(date: str, max_stocks: int = 500) -> List[str]:
    """获取股票池"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date)
    
    filtered = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
        (all_stocks['start_date'].astype(str) < (pd.to_datetime(date) - timedelta(days=365)).strftime('%Y-%m-%d'))
    ]
    
    return filtered.index.tolist()[:max_stocks]


def calculate_extreme_factors(price_df: pd.DataFrame, code: str, date: str) -> Dict:
    """计算极端高收益因子"""
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
    money = historical['money'].values if 'money' in historical.columns else volume * close
    
    result = {'code': code, 'date': date, 'close': close[-1]}
    
    # ========== 涨停特征（最强信号）==========
    
    # 近5日涨停计数
    limit_up_count = 0
    limit_up_recent = 0  # 最近2日涨停
    for j in range(max(len(close)-5, 1), len(close)):
        if close[j] / close[j-1] > 1.095:
            limit_up_count += 1
            if j >= len(close) - 2:
                limit_up_recent += 1
    result['limit_up_count'] = limit_up_count
    result['limit_up_recent'] = limit_up_recent
    
    # 首板识别（首次涨停）
    is_first_limit_up = False
    if len(close) >= 30:
        # 检查最近1天是否涨停
        if close[-1] / close[-2] > 1.095:
            # 检查前29天是否没有涨停
            prev_limit_ups = 0
            for j in range(len(close)-30, len(close)-1):
                if j > 0 and close[j] / close[j-1] > 1.095:
                    prev_limit_ups += 1
            if prev_limit_ups == 0:
                is_first_limit_up = True
    result['is_first_limit_up'] = is_first_limit_up
    
    # ========== 动量特征 ==========
    
    result['mom_1d'] = (close[-1] / close[-2] - 1) * 100 if len(close) >= 2 else 0
    result['mom_3d'] = (close[-1] / close[-4] - 1) * 100 if len(close) >= 4 else 0
    result['mom_5d'] = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    result['mom_10d'] = (close[-1] / close[-11] - 1) * 100 if len(close) >= 11 else 0
    result['mom_20d'] = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
    
    # 动量加速度
    if len(close) >= 11:
        mom_5d_now = (close[-1] / close[-6] - 1) * 100
        mom_5d_prev = (close[-6] / close[-11] - 1) * 100
        result['mom_acceleration'] = mom_5d_now - mom_5d_prev
    
    # ========== 放量特征 ==========
    
    if len(volume) >= 20:
        vol_1d = volume[-1]
        vol_5d = np.mean(volume[-5:])
        vol_20d = np.mean(volume[-20:])
        result['volume_ratio_1d'] = vol_1d / vol_20d if vol_20d > 0 else 1
        result['volume_ratio_5d'] = vol_5d / vol_20d if vol_20d > 0 else 1
    
    # 成交额爆发
    if len(money) >= 20:
        money_1d = money[-1]
        money_5d = np.sum(money[-5:])
        money_5d_prev = np.sum(money[-10:-5])
        result['money_explosion'] = money_1d / np.mean(money[-20:]) if np.mean(money[-20:]) > 0 else 1
        result['money_change'] = (money_5d / money_5d_prev - 1) * 100 if money_5d_prev > 0 else 0
    
    # ========== 技术位置 ==========
    
    # 相对位置
    if len(high) >= 20:
        high_20 = np.max(high[-20:])
        low_20 = np.min(low[-20:])
        if high_20 > low_20:
            result['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    
    # 突破新高
    if len(high) >= 60:
        high_60 = np.max(high[-60:-1])  # 不包含当日
        result['breakout_60d'] = close[-1] > high_60
        result['breakout_ratio'] = close[-1] / high_60 if high_60 > 0 else 1
    
    # ========== 连续特征 ==========
    
    # 连续上涨天数
    up_days = 0
    for j in range(len(close)-1, max(len(close)-11, 0), -1):
        if j > 0 and close[j] > close[j-1]:
            up_days += 1
        else:
            break
    result['consecutive_up_days'] = up_days
    
    # 连续放量天数
    vol_up_days = 0
    for j in range(len(volume)-1, max(len(volume)-11, 0), -1):
        if j > 0 and volume[j] > volume[j-1]:
            vol_up_days += 1
        else:
            break
    result['consecutive_vol_up_days'] = vol_up_days
    
    return result


def score_extreme_signal(row: pd.Series) -> Tuple[float, str]:
    """
    极端信号评分
    
    返回：(评分, 信号类型)
    """
    score = 0.0
    signal_type = "无信号"
    
    # ========== 策略1: 涨停板启动 ==========
    limit_up = row.get('limit_up_count', 0)
    limit_up_recent = row.get('limit_up_recent', 0)
    is_first_limit_up = row.get('is_first_limit_up', False)
    
    if is_first_limit_up:
        # 首板策略（最强）
        score += 50
        signal_type = "首板启动"
        
        # 放量加分
        vol_ratio = row.get('volume_ratio_1d', 1)
        if vol_ratio > 3:
            score += 25
        elif vol_ratio > 2:
            score += 15
        
        # 突破加分
        if row.get('breakout_60d', False):
            score += 15
    
    elif limit_up_recent >= 1:
        # 连板策略
        score += 40
        signal_type = "连板加速"
        
        if limit_up >= 2:
            score += 20
    
    # ========== 策略2: 强势突破 ==========
    if row.get('breakout_60d', False) and score < 50:
        breakout_ratio = row.get('breakout_ratio', 1)
        mom_5d = row.get('mom_5d', 0)
        vol_ratio = row.get('volume_ratio_5d', 1)
        
        if breakout_ratio > 1.05 and mom_5d > 15 and vol_ratio > 1.5:
            score = 60
            signal_type = "强势突破"
    
    # ========== 策略3: 量价齐升 ==========
    mom_5d = row.get('mom_5d', 0)
    vol_ratio_5d = row.get('volume_ratio_5d', 1)
    money_explosion = row.get('money_explosion', 1)
    
    if mom_5d > 20 and vol_ratio_5d > 1.5 and money_explosion > 2 and score < 50:
        score = 55
        signal_type = "量价齐升"
        
        # 连续上涨加分
        up_days = row.get('consecutive_up_days', 0)
        if up_days >= 4:
            score += 15
    
    # ========== 策略4: 动量加速 ==========
    mom_acceleration = row.get('mom_acceleration', 0)
    
    if mom_acceleration > 15 and mom_5d > 10 and score < 50:
        score = 50
        signal_type = "动量加速"
    
    return score, signal_type


def backtest_extreme_strategy(stocks: List[str], start_date: str, end_date: str,
                              signal_threshold: float = 60,
                              max_positions: int = 3,
                              stop_loss: float = -8.0,
                              take_profit: float = 20.0) -> Dict:
    """
    极端高收益策略回测
    
    特点：
    1. 只在强信号出现时建仓
    2. 极度集中持仓
    3. 严格止损止盈
    """
    print(f"\n📈 极端高收益策略回测: {start_date} ~ {end_date}")
    print(f"   信号阈值: {signal_threshold}")
    print(f"   最大持仓: {max_positions}")
    print(f"   止损: {stop_loss}%")
    print(f"   止盈: {take_profit}%")
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 获取价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    
    price_df = jq.get_price(
        stocks[:300],
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
    positions = {}  # {code: {'shares': int, 'cost': float, 'entry_date': str}}
    
    results = {
        'trades': [],
        'daily_values': [],
        'signals': [],
    }
    
    for trade_date in trade_days:
        date_str = trade_date.strftime('%Y-%m-%d')
        
        # 获取当日价格
        day_prices = price_df[price_df['date'] == date_str].set_index('code')
        
        if day_prices.empty:
            continue
        
        # 计算当前市值
        position_value = 0
        for code, pos in positions.items():
            if code in day_prices.index:
                position_value += pos['shares'] * day_prices.loc[code, 'close']
        
        total_value = capital + position_value
        results['daily_values'].append({
            'date': date_str,
            'capital': capital,
            'position_value': position_value,
            'total_value': total_value,
            'position_count': len(positions),
        })
        
        # ========== 止损止盈检查 ==========
        sell_list = []
        for code, pos in positions.items():
            if code in day_prices.index:
                current_price = day_prices.loc[code, 'close']
                pnl_pct = (current_price / pos['cost'] - 1) * 100
                
                if pnl_pct <= stop_loss:
                    sell_list.append((code, '止损', pnl_pct))
                elif pnl_pct >= take_profit:
                    sell_list.append((code, '止盈', pnl_pct))
        
        for code, reason, pnl_pct in sell_list:
            if code in day_prices.index:
                price = day_prices.loc[code, 'close']
                shares = positions[code]['shares']
                proceeds = shares * price * (1 - 0.001 - 0.0001)
                capital += proceeds
                
                results['trades'].append({
                    'date': date_str,
                    'code': code,
                    'action': 'SELL',
                    'reason': reason,
                    'price': price,
                    'shares': shares,
                    'pnl_pct': pnl_pct,
                })
                
                del positions[code]
        
        # ========== 寻找新信号 ==========
        if len(positions) < max_positions:
            signals = []
            for code in stocks[:300]:
                factors = calculate_extreme_factors(price_df, code, date_str)
                if factors:
                    score, signal_type = score_extreme_signal(pd.Series(factors))
                    if score >= signal_threshold:
                        factors['score'] = score
                        factors['signal_type'] = signal_type
                        signals.append(factors)
            
            if signals:
                # 按评分排序
                signals_df = pd.DataFrame(signals).sort_values('score', ascending=False)
                
                # 记录信号
                for _, row in signals_df.head(5).iterrows():
                    results['signals'].append({
                        'date': date_str,
                        'code': row['code'],
                        'score': row['score'],
                        'signal_type': row['signal_type'],
                    })
                
                # 买入最强信号
                available_slots = max_positions - len(positions)
                buy_candidates = signals_df[~signals_df['code'].isin(positions.keys())].head(available_slots)
                
                for _, row in buy_candidates.iterrows():
                    code = row['code']
                    if code in day_prices.index and capital > 50000:
                        price = day_prices.loc[code, 'close']
                        per_position_capital = capital / available_slots * 0.95
                        shares = int(per_position_capital / price / 100) * 100
                        
                        if shares >= 100:
                            cost = shares * price * (1 + 0.0001)
                            capital -= cost
                            positions[code] = {
                                'shares': shares,
                                'cost': price,
                                'entry_date': date_str,
                            }
                            
                            results['trades'].append({
                                'date': date_str,
                                'code': code,
                                'action': 'BUY',
                                'reason': row['signal_type'],
                                'price': price,
                                'shares': shares,
                                'score': row['score'],
                            })
    
    # 计算最终价值
    if results['daily_values']:
        final_value = results['daily_values'][-1]['total_value']
    else:
        final_value = initial_capital
    
    # 计算统计
    total_return = (final_value / initial_capital - 1) * 100
    
    if trade_days.size > 0:
        days = (trade_days[-1] - trade_days[0]).days
        annual_return = total_return * 365 / days if days > 0 else 0
    else:
        annual_return = 0
    
    # 交易统计
    trades_df = pd.DataFrame(results['trades'])
    if not trades_df.empty:
        sell_trades = trades_df[trades_df['action'] == 'SELL']
        if not sell_trades.empty:
            win_trades = sell_trades[sell_trades['pnl_pct'] > 0]
            win_rate = len(win_trades) / len(sell_trades) * 100
            avg_win = win_trades['pnl_pct'].mean() if len(win_trades) > 0 else 0
            avg_loss = sell_trades[sell_trades['pnl_pct'] <= 0]['pnl_pct'].mean()
            avg_loss = avg_loss if not pd.isna(avg_loss) else 0
        else:
            win_rate = avg_win = avg_loss = 0
        total_trades = len(trades_df)
    else:
        win_rate = avg_win = avg_loss = 0
        total_trades = 0
    
    # 计算周收益
    daily_df = pd.DataFrame(results['daily_values'])
    if not daily_df.empty and len(daily_df) > 5:
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        daily_df = daily_df.set_index('date')
        weekly_returns = daily_df['total_value'].resample('W').last().pct_change() * 100
        avg_weekly = weekly_returns.mean()
        weekly_win_rate = len(weekly_returns[weekly_returns > 0]) / len(weekly_returns.dropna()) * 100 if len(weekly_returns.dropna()) > 0 else 0
    else:
        avg_weekly = 0
        weekly_win_rate = 0
    
    results['summary'] = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'avg_weekly_return': avg_weekly,
        'weekly_win_rate': weekly_win_rate,
        'total_trades': total_trades,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'total_signals': len(results['signals']),
    }
    
    return results


def main():
    """主函数"""
    print("="*80)
    print("极端高收益周频策略")
    print("目标：年收益500%（周收益3.5%）")
    print("="*80)
    
    if not init_jqdata():
        return
    
    print("\n✅ JQData连接成功\n")
    
    # ============ 参数组合测试 ============
    configs = [
        {'signal_threshold': 70, 'max_positions': 1, 'stop_loss': -8, 'take_profit': 20},
        {'signal_threshold': 60, 'max_positions': 2, 'stop_loss': -10, 'take_profit': 25},
        {'signal_threshold': 50, 'max_positions': 3, 'stop_loss': -12, 'take_profit': 30},
    ]
    
    test_stocks = get_stock_universe('2024-09-01', 500)
    
    best_result = None
    best_config = None
    
    for config in configs:
        print("\n" + "="*80)
        results = backtest_extreme_strategy(
            test_stocks, '2024-09-01', '2025-12-31', **config
        )
        
        if results and 'summary' in results:
            s = results['summary']
            print(f"\n📈 回测结果:")
            print(f"   总收益率: {s['total_return']:.2f}%")
            print(f"   年化收益率: {s['annual_return']:.2f}%")
            print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
            print(f"   周胜率: {s['weekly_win_rate']:.1f}%")
            print(f"   交易次数: {s['total_trades']}")
            print(f"   交易胜率: {s['win_rate']:.1f}%")
            print(f"   平均盈利: {s['avg_win']:.2f}%")
            print(f"   平均亏损: {s['avg_loss']:.2f}%")
            
            if best_result is None or s['total_return'] > best_result['summary']['total_return']:
                best_result = results
                best_config = config
    
    # ============ 最佳策略详情 ============
    if best_result:
        print("\n" + "="*80)
        print("🏆 最佳策略配置")
        print("="*80)
        print(f"   信号阈值: {best_config['signal_threshold']}")
        print(f"   最大持仓: {best_config['max_positions']}")
        print(f"   止损: {best_config['stop_loss']}%")
        print(f"   止盈: {best_config['take_profit']}%")
        
        s = best_result['summary']
        print(f"\n📈 最终结果:")
        print(f"   初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"   最终价值: ¥{s['final_value']:,.0f}")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        
        # 打印信号样本
        if best_result['signals']:
            print(f"\n📌 信号样本（共{len(best_result['signals'])}个）:")
            signals_df = pd.DataFrame(best_result['signals'])
            for _, row in signals_df.head(10).iterrows():
                print(f"   {row['date']} | {row['code']} | {row['signal_type']} | 评分:{row['score']:.0f}")
    
    # ============ 牛市回测 ============
    print("\n" + "="*80)
    print("📊 第四次牛市(2014-2015)回测")
    print("="*80)
    
    bull4_stocks = get_stock_universe('2014-07-01', 500)
    bull4_results = backtest_extreme_strategy(
        bull4_stocks, '2014-07-01', '2015-06-12',
        signal_threshold=60, max_positions=2, stop_loss=-8, take_profit=30
    )
    
    if bull4_results and 'summary' in bull4_results:
        s = bull4_results['summary']
        print(f"\n📈 第四次牛市结果:")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        print(f"   交易胜率: {s['win_rate']:.1f}%")
    
    print("\n" + "="*80)
    print("📊 第五次牛市(2019-2021)回测")
    print("="*80)
    
    bull5_stocks = get_stock_universe('2019-01-01', 500)
    bull5_results = backtest_extreme_strategy(
        bull5_stocks, '2019-01-01', '2021-02-28',
        signal_threshold=60, max_positions=2, stop_loss=-8, take_profit=30
    )
    
    if bull5_results and 'summary' in bull5_results:
        s = bull5_results['summary']
        print(f"\n📈 第五次牛市结果:")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        print(f"   交易胜率: {s['win_rate']:.1f}%")
    
    # ============ 策略总结 ============
    print("\n" + "="*80)
    print("🎯 策略总结与下周操作建议")
    print("="*80)
    
    print("""
【年收益500%目标分析】
  - 需要平均周收益: 3.5%
  - 需要选股准确率: 极高
  - 实现难度: ★★★★★（极难）
  
【核心策略信号】
  1. 首板启动（最强）
     - 首次涨停板
     - 成交量爆发(>3倍)
     - 突破60日新高
     
  2. 连板加速
     - 2连板或以上
     - 量价齐升
     
  3. 强势突破
     - 突破60日新高>5%
     - 5日动量>15%
     - 量比>1.5
     
  4. 量价齐升
     - 5日动量>20%
     - 量比>1.5
     - 成交额爆发>2倍

【风控规则】
  - 止损: -8%（绝对执行）
  - 止盈: +20~30%
  - 最大持仓: 1-3只
  - 空仓等待机制

【下周操作建议】
  1. 每日盘后扫描涨停板
  2. 筛选首板+放量+突破
  3. 次日竞价/开盘买入
  4. 严格执行止损止盈
  5. 无信号则空仓等待
""")


if __name__ == '__main__':
    main()
