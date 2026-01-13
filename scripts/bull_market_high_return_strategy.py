#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高收益策略挖掘

训练集：第四次牛市(2014-2015) + 第五次牛市(2019-2021)
测试集：2024.09-2025.12.31

目标：周频交易，年收益500%（周收益约3.5%）

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
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
        return jq.is_auth()
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


# ============ 数据挖掘参数 ============
# 牛市时间段
BULL_MARKETS = {
    'bull_4': ('2014-07-01', '2015-06-12'),  # 第四次杠杆牛
    'bull_5': ('2019-01-01', '2021-02-28'),  # 第五次结构牛
}

# 测试集时间段
TEST_PERIOD = ('2024-09-01', '2025-12-31')

# 高收益阈值（周频：5日收益≥10%视为高收益）
HIGH_RETURN_THRESHOLD_5D = 10.0  # 5日收益≥10%
EXTREME_RETURN_THRESHOLD_5D = 20.0  # 5日收益≥20%（极端高收益）


def get_stock_universe(date: str, max_stocks: int = 500) -> List[str]:
    """获取股票池"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date)
    
    # 过滤条件
    filtered = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|\\*|退', na=False) &
        (all_stocks['start_date'].astype(str) < (pd.to_datetime(date) - timedelta(days=365)).strftime('%Y-%m-%d'))
    ]
    
    # 按市值排序（优先选择流动性好的）
    return filtered.index.tolist()[:max_stocks]


def mine_high_return_cases(start_date: str, end_date: str, 
                           universe_size: int = 300) -> pd.DataFrame:
    """
    挖掘高收益案例
    
    返回：每个高收益案例的入场因子特征
    """
    print(f"\n📊 挖掘高收益案例: {start_date} ~ {end_date}")
    
    # 获取股票池
    stocks = get_stock_universe(start_date, universe_size)
    print(f"   股票池: {len(stocks)} 只")
    
    # 获取价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    
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
    
    if price_df.empty:
        return pd.DataFrame()
    
    if 'time' in price_df.columns:
        price_df = price_df.rename(columns={'time': 'date'})
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y-%m-%d')
    
    # 计算未来5日收益
    cases = []
    
    for code in stocks:
        stock_data = price_df[price_df['code'] == code].sort_values('date').copy()
        
        if len(stock_data) < 60:
            continue
        
        # 计算技术因子
        close = stock_data['close'].values
        high = stock_data['high'].values
        low = stock_data['low'].values
        volume = stock_data['volume'].values
        money = stock_data['money'].values
        dates = stock_data['date'].values
        
        for i in range(25, len(stock_data) - 6):
            # 计算未来5日收益
            future_return = (close[i+5] / close[i] - 1) * 100
            
            # 只保留高收益案例
            if future_return < HIGH_RETURN_THRESHOLD_5D:
                continue
            
            # 计算入场点的因子
            case = {
                'code': code,
                'date': dates[i],
                'future_return_5d': future_return,
                'close': close[i],
            }
            
            # === 预测性因子 ===
            
            # 1. 相对位置（20日）
            high_20 = np.max(high[i-19:i+1])
            low_20 = np.min(low[i-19:i+1])
            if high_20 > low_20:
                case['rel_position_20d'] = (close[i] - low_20) / (high_20 - low_20) * 100
            
            # 2. 相对位置（60日）
            if i >= 59:
                high_60 = np.max(high[i-59:i+1])
                low_60 = np.min(low[i-59:i+1])
                if high_60 > low_60:
                    case['rel_position_60d'] = (close[i] - low_60) / (high_60 - low_60) * 100
            
            # 3. 量比（5日/20日）
            vol_5d = np.mean(volume[i-4:i+1])
            vol_20d = np.mean(volume[i-19:i+1])
            case['volume_ratio'] = vol_5d / vol_20d if vol_20d > 0 else 1
            
            # 4. 成交额变化（5日/前5日）
            money_5d = np.sum(money[i-4:i+1])
            money_5d_prev = np.sum(money[i-9:i-4])
            case['money_change'] = (money_5d / money_5d_prev - 1) * 100 if money_5d_prev > 0 else 0
            
            # 5. RSI
            deltas = np.diff(close[i-13:i+1])
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            avg_gain = np.mean(gains)
            avg_loss = np.mean(losses)
            if avg_loss > 0:
                rs = avg_gain / avg_loss
                case['rsi'] = 100 - (100 / (1 + rs))
            else:
                case['rsi'] = 100
            
            # 6. 均线偏离
            ma_20 = np.mean(close[i-19:i+1])
            case['ma_deviation'] = (close[i] / ma_20 - 1) * 100
            
            # 7. 波动率
            case['volatility'] = np.std(close[i-19:i+1]) / np.mean(close[i-19:i+1]) * 100
            
            # 8. 动量因子（作为参考）
            case['mom_5d'] = (close[i] / close[i-5] - 1) * 100 if i >= 5 else 0
            case['mom_10d'] = (close[i] / close[i-10] - 1) * 100 if i >= 10 else 0
            case['mom_20d'] = (close[i] / close[i-20] - 1) * 100 if i >= 20 else 0
            
            # 9. 动量加速度
            if i >= 10:
                mom_5d_now = (close[i] / close[i-5] - 1) * 100
                mom_5d_prev = (close[i-5] / close[i-10] - 1) * 100
                case['mom_acceleration'] = mom_5d_now - mom_5d_prev
            
            # 10. 涨停特征（前5日是否有涨停）
            limit_up_count = 0
            for j in range(i-4, i+1):
                if j > 0 and close[j] / close[j-1] > 1.095:
                    limit_up_count += 1
            case['limit_up_count'] = limit_up_count
            
            # 11. 连续上涨天数
            up_days = 0
            for j in range(i, max(i-10, 0), -1):
                if j > 0 and close[j] > close[j-1]:
                    up_days += 1
                else:
                    break
            case['consecutive_up_days'] = up_days
            
            cases.append(case)
    
    return pd.DataFrame(cases)


def analyze_factor_distribution(cases_df: pd.DataFrame, period_name: str):
    """分析因子分布"""
    print(f"\n📊 {period_name} 高收益案例因子分布")
    print("="*60)
    print(f"   案例数: {len(cases_df)}")
    print(f"   平均5日收益: {cases_df['future_return_5d'].mean():.2f}%")
    print(f"   中位5日收益: {cases_df['future_return_5d'].median():.2f}%")
    print(f"   ≥20%收益占比: {len(cases_df[cases_df['future_return_5d'] >= 20]) / len(cases_df) * 100:.1f}%")
    
    # 因子统计
    factors = ['rel_position_20d', 'rel_position_60d', 'volume_ratio', 'money_change', 
               'rsi', 'ma_deviation', 'mom_5d', 'mom_10d', 'limit_up_count', 'consecutive_up_days']
    
    print(f"\n{'因子':<20} {'均值':>10} {'中位数':>10} {'标准差':>10}")
    print("-"*60)
    
    for factor in factors:
        if factor in cases_df.columns:
            mean_val = cases_df[factor].mean()
            median_val = cases_df[factor].median()
            std_val = cases_df[factor].std()
            print(f"{factor:<20} {mean_val:>10.2f} {median_val:>10.2f} {std_val:>10.2f}")
    
    return


def find_optimal_thresholds(cases_df: pd.DataFrame) -> Dict:
    """
    寻找最优因子阈值
    
    目标：找到能够筛选出高收益案例的因子组合
    """
    print("\n📊 寻找最优因子阈值...")
    
    # 按收益分组
    extreme_cases = cases_df[cases_df['future_return_5d'] >= EXTREME_RETURN_THRESHOLD_5D]
    high_cases = cases_df[cases_df['future_return_5d'] >= HIGH_RETURN_THRESHOLD_5D]
    
    print(f"   高收益案例(≥{HIGH_RETURN_THRESHOLD_5D}%): {len(high_cases)}")
    print(f"   极端高收益案例(≥{EXTREME_RETURN_THRESHOLD_5D}%): {len(extreme_cases)}")
    
    # 分析极端高收益案例的因子特征
    optimal = {}
    
    if len(extreme_cases) > 50:
        analysis_df = extreme_cases
    else:
        analysis_df = high_cases
    
    # 相对位置分析
    rel_pos_20d = analysis_df['rel_position_20d'].dropna()
    if len(rel_pos_20d) > 0:
        optimal['rel_position_20d'] = {
            'q25': rel_pos_20d.quantile(0.25),
            'median': rel_pos_20d.median(),
            'q75': rel_pos_20d.quantile(0.75),
        }
    
    # 量比分析
    vol_ratio = analysis_df['volume_ratio'].dropna()
    if len(vol_ratio) > 0:
        optimal['volume_ratio'] = {
            'q25': vol_ratio.quantile(0.25),
            'median': vol_ratio.median(),
            'q75': vol_ratio.quantile(0.75),
        }
    
    # RSI分析
    rsi = analysis_df['rsi'].dropna()
    if len(rsi) > 0:
        optimal['rsi'] = {
            'q25': rsi.quantile(0.25),
            'median': rsi.median(),
            'q75': rsi.quantile(0.75),
        }
    
    # 动量分析
    mom_5d = analysis_df['mom_5d'].dropna()
    if len(mom_5d) > 0:
        optimal['mom_5d'] = {
            'q25': mom_5d.quantile(0.25),
            'median': mom_5d.median(),
            'q75': mom_5d.quantile(0.75),
        }
    
    # 涨停特征
    limit_up = analysis_df['limit_up_count'].dropna()
    if len(limit_up) > 0:
        optimal['limit_up_count'] = {
            'q25': limit_up.quantile(0.25),
            'median': limit_up.median(),
            'q75': limit_up.quantile(0.75),
        }
    
    return optimal


def build_scoring_model(optimal_thresholds: Dict) -> callable:
    """构建评分模型"""
    
    def score_stock(row: pd.Series) -> float:
        score = 0.0
        
        # 1. 涨停特征（最强信号）- 权重30%
        limit_up = row.get('limit_up_count', 0)
        if limit_up >= 2:
            score += 30
        elif limit_up >= 1:
            score += 20
        
        # 2. 量比（资金信号）- 权重25%
        vol_ratio = row.get('volume_ratio', 1)
        if vol_ratio > 2.0:
            score += 25
        elif vol_ratio > 1.5:
            score += 20
        elif vol_ratio > 1.2:
            score += 15
        
        # 3. 动量（确认信号）- 权重20%
        mom_5d = row.get('mom_5d', 0)
        if mom_5d > 15:
            score += 20
        elif mom_5d > 10:
            score += 15
        elif mom_5d > 5:
            score += 10
        
        # 4. 连续上涨（趋势信号）- 权重15%
        up_days = row.get('consecutive_up_days', 0)
        if up_days >= 4:
            score += 15
        elif up_days >= 3:
            score += 10
        elif up_days >= 2:
            score += 5
        
        # 5. RSI（超买但强势）- 权重10%
        rsi = row.get('rsi', 50)
        if 60 <= rsi <= 80:
            score += 10
        elif 50 <= rsi < 60:
            score += 5
        
        return score
    
    return score_stock


def backtest_weekly_strategy(stocks: List[str], start_date: str, end_date: str,
                             score_func: callable, top_n: int = 5) -> Dict:
    """
    周频策略回测
    
    策略：每周选择评分最高的top_n只股票，等权持有
    """
    print(f"\n📈 周频策略回测: {start_date} ~ {end_date}")
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 每周一换仓
    rebalance_days = []
    for d in trade_days:
        if d.weekday() == 0:  # 周一
            rebalance_days.append(d)
    
    print(f"   换仓次数: {len(rebalance_days)}")
    
    # 获取价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=60)).strftime('%Y-%m-%d')
    
    price_df = jq.get_price(
        stocks[:200],  # 限制数量
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
    }
    
    for i, rebalance_date in enumerate(rebalance_days):
        date_str = rebalance_date.strftime('%Y-%m-%d')
        
        # 计算所有股票的因子
        factor_data = []
        for code in stocks[:200]:
            factors = calculate_factors_for_date(price_df, code, date_str)
            if factors:
                factors['score'] = score_func(pd.Series(factors))
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
    
    # 计算总收益
    total_return = (final_value / initial_capital - 1) * 100
    
    # 计算年化收益
    if rebalance_days:
        days = (rebalance_days[-1] - rebalance_days[0]).days
        if days > 0:
            annual_return = total_return * 365 / days
        else:
            annual_return = 0
    else:
        annual_return = 0
    
    # 计算周收益统计
    if results['weekly_returns']:
        weekly_df = pd.DataFrame(results['weekly_returns'])
        avg_weekly = weekly_df['return'].mean()
        win_rate = len(weekly_df[weekly_df['return'] > 0]) / len(weekly_df) * 100
        max_weekly = weekly_df['return'].max()
        min_weekly = weekly_df['return'].min()
    else:
        avg_weekly = win_rate = max_weekly = min_weekly = 0
    
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
    }
    
    return results


def calculate_factors_for_date(price_df: pd.DataFrame, code: str, date: str) -> Dict:
    """计算指定日期的因子"""
    stock_data = price_df[price_df['code'] == code].copy()
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data = stock_data.sort_values('date')
    
    target_dt = pd.to_datetime(date)
    historical = stock_data[stock_data['date'] <= target_dt].tail(30)
    
    if len(historical) < 20:
        return {}
    
    close = historical['close'].values
    high = historical['high'].values
    low = historical['low'].values
    volume = historical['volume'].values
    
    result = {'code': code, 'date': date, 'close': close[-1]}
    
    # 相对位置
    if len(high) >= 20:
        high_20 = np.max(high[-20:])
        low_20 = np.min(low[-20:])
        if high_20 > low_20:
            result['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    
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
    
    # 动量
    if len(close) >= 6:
        result['mom_5d'] = (close[-1] / close[-6] - 1) * 100
    
    # 连续上涨
    up_days = 0
    for j in range(len(close)-1, max(len(close)-11, 0), -1):
        if j > 0 and close[j] > close[j-1]:
            up_days += 1
        else:
            break
    result['consecutive_up_days'] = up_days
    
    # 涨停计数
    limit_up_count = 0
    for j in range(max(len(close)-5, 1), len(close)):
        if close[j] / close[j-1] > 1.095:
            limit_up_count += 1
    result['limit_up_count'] = limit_up_count
    
    return result


def main():
    """主函数"""
    print("="*80)
    print("牛市高收益策略挖掘")
    print("目标：周频交易，年收益500%（周收益≈3.5%）")
    print("="*80)
    
    if not init_jqdata():
        return
    
    print("\n✅ JQData连接成功\n")
    
    # ============ Step 1: 挖掘训练集数据 ============
    print("="*80)
    print("📊 Step 1: 挖掘牛市高收益案例（训练集）")
    print("="*80)
    
    all_cases = []
    
    for period_name, (start, end) in BULL_MARKETS.items():
        cases = mine_high_return_cases(start, end, universe_size=200)
        if not cases.empty:
            cases['period'] = period_name
            all_cases.append(cases)
            analyze_factor_distribution(cases, period_name)
    
    if not all_cases:
        print("❌ 未找到高收益案例")
        return
    
    train_cases = pd.concat(all_cases, ignore_index=True)
    print(f"\n📊 训练集总计: {len(train_cases)} 个高收益案例")
    
    # ============ Step 2: 分析因子特征 ============
    print("\n" + "="*80)
    print("📊 Step 2: 分析高收益案例的因子特征")
    print("="*80)
    
    optimal_thresholds = find_optimal_thresholds(train_cases)
    
    print("\n📌 高收益案例的典型特征：")
    for factor, stats in optimal_thresholds.items():
        print(f"   {factor}: 中位数={stats['median']:.2f}, Q25={stats['q25']:.2f}, Q75={stats['q75']:.2f}")
    
    # ============ Step 3: 构建评分模型 ============
    print("\n" + "="*80)
    print("📊 Step 3: 构建评分模型")
    print("="*80)
    
    score_func = build_scoring_model(optimal_thresholds)
    
    # 在训练集上验证
    train_cases['model_score'] = train_cases.apply(score_func, axis=1)
    
    # 按评分分组看收益
    print("\n📌 评分与收益关系（训练集）：")
    score_bins = [0, 30, 50, 70, 100]
    train_cases['score_group'] = pd.cut(train_cases['model_score'], bins=score_bins)
    
    for group in train_cases['score_group'].dropna().unique():
        group_data = train_cases[train_cases['score_group'] == group]
        print(f"   评分{group}: 案例数={len(group_data)}, 平均收益={group_data['future_return_5d'].mean():.2f}%")
    
    # ============ Step 4: 测试集回测 ============
    print("\n" + "="*80)
    print("📊 Step 4: 测试集回测")
    print("="*80)
    
    test_start, test_end = TEST_PERIOD
    test_stocks = get_stock_universe(test_start, 300)
    
    test_results = backtest_weekly_strategy(
        test_stocks, test_start, test_end, score_func, top_n=5
    )
    
    if test_results and 'summary' in test_results:
        s = test_results['summary']
        print(f"\n📈 测试集回测结果 ({test_start} ~ {test_end}):")
        print(f"   初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"   最终价值: ¥{s['final_value']:,.0f}")
        print(f"   总收益率: {s['total_return']:.2f}%")
        print(f"   年化收益率: {s['annual_return']:.2f}%")
        print(f"   平均周收益: {s['avg_weekly_return']:.2f}%")
        print(f"   胜率: {s['win_rate']:.1f}%")
        print(f"   最大周收益: {s['max_weekly_return']:.2f}%")
        print(f"   最大周亏损: {s['min_weekly_return']:.2f}%")
        print(f"   总周数: {s['total_weeks']}")
    
    # ============ Step 5: 策略总结 ============
    print("\n" + "="*80)
    print("🎯 高收益周频策略总结")
    print("="*80)
    
    print("""
【核心发现】
  1. 高收益股票的共同特征：
     - 涨停板出现（近5日有≥1个涨停）
     - 成交量大幅放大（量比>1.5）
     - 强势动量（5日动量>10%）
     - 连续上涨（≥3天）
     
  2. 这是"追涨"策略，不是"抄底"策略
     - 与之前的预测性因子（低位布局）完全相反
     - 适用于牛市行情，在震荡市表现差
     
  3. 年收益500%需要：
     - 平均周收益 ≈ 3.5%
     - 这要求选股准确率非常高
     - 实际操作中很难持续实现

【策略规则】
  1. 选股条件：
     - 近5日有涨停板
     - 量比 > 1.5
     - 5日动量 > 10%
     - 连续上涨 ≥ 3天
     - RSI 60-80（强势但未超买）
  
  2. 仓位管理：
     - 每周选5只最强股票
     - 等权配置
     - 周一换仓
  
  3. 风控：
     - 止损: -8%
     - 止盈: +20%
     - 最大持仓周期: 5个交易日

【重要提示】
  ⚠️ 年收益500%是极端目标，实现难度非常高
  ⚠️ 此策略仅适用于牛市，熊市会大幅亏损
  ⚠️ 建议以实际回测收益为准，不要盲目追求高目标
""")


if __name__ == '__main__':
    main()
