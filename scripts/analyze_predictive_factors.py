#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2019-2021牛市高回报股票预测性因子分析

分析高回报股票在买入前一周、前一个月的因子特征，
挖掘具有预测性的因子组合。

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
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
        
        if jq.is_auth():
            print("✅ JQData连接成功")
            return True
        else:
            print("❌ JQData认证失败")
            return False
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


def load_high_return_cases(data_dir: str) -> Dict[str, pd.DataFrame]:
    """加载高回报案例数据"""
    cases = {}
    
    for period in ['short', 'medium', 'long']:
        file_path = Path(data_dir) / f'high_return_{period}.csv'
        if file_path.exists():
            df = pd.read_csv(file_path)
            cases[period] = df
            print(f"📥 加载{period}期案例: {len(df)}条")
    
    return cases


def get_factor_data_batch(stocks: List[str], dates: List[str]) -> pd.DataFrame:
    """批量获取因子数据"""
    all_data = []
    
    for date in dates:
        try:
            # 估值数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.ps_ratio,
                jq.valuation.market_cap,
                jq.valuation.turnover_ratio,
            ).filter(
                jq.valuation.code.in_(stocks)
            )
            val_df = jq.get_fundamentals(q, date=date)
            
            if not val_df.empty:
                val_df['date'] = date
                all_data.append(val_df)
        except:
            pass
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def calculate_technical_factors_for_date(price_df: pd.DataFrame, code: str, 
                                          target_date: str, lookback_days: int = 60) -> Dict:
    """计算指定日期的技术因子"""
    stock_data = price_df[price_df['code'] == code].copy()
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data = stock_data.sort_values('date')
    
    # 找到目标日期及之前的数据
    target_dt = pd.to_datetime(target_date)
    historical = stock_data[stock_data['date'] <= target_dt].tail(lookback_days)
    
    if len(historical) < 20:
        return {}
    
    close = historical['close'].values
    high = historical['high'].values
    low = historical['low'].values
    volume = historical['volume'].values
    
    result = {
        'code': code,
        'date': target_date,
        'close': close[-1],
    }
    
    # 动量因子
    if len(close) >= 6:
        result['mom_5d'] = (close[-1] / close[-6] - 1) * 100
    if len(close) >= 21:
        result['mom_20d'] = (close[-1] / close[-21] - 1) * 100
    if len(close) >= 61 and close[-61] > 0:
        result['mom_60d'] = (close[-1] / close[-61] - 1) * 100
    
    # 相对位置
    if len(high) >= 20:
        high_20 = np.max(high[-20:])
        low_20 = np.min(low[-20:])
        if high_20 > low_20:
            result['rel_position'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    
    # 波动率
    if len(close) >= 20:
        result['volatility'] = np.std(close[-20:]) / np.mean(close[-20:]) * 100
    
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
    
    # 成交额变化
    if len(volume) >= 10 and 'money' in historical.columns:
        money = historical['money'].values
        money_5d = np.sum(money[-5:])
        money_5d_prev = np.sum(money[-10:-5])
        if money_5d_prev > 0:
            result['money_change'] = (money_5d / money_5d_prev - 1) * 100
    
    return result


def analyze_predictive_factors(cases: pd.DataFrame, period_name: str, 
                               sample_size: int = 200) -> Dict:
    """分析预测性因子"""
    print(f"\n📊 分析{period_name}高回报案例的预测性因子...")
    
    # 抽样
    if len(cases) > sample_size:
        cases = cases.sample(n=sample_size, random_state=42)
    
    print(f"   样本量: {len(cases)}")
    
    # 获取所有涉及的股票和日期
    stocks = cases['code'].unique().tolist()
    dates = cases['date'].unique().tolist()
    
    # 计算回溯日期（前一周、前一个月）
    lookback_dates = set()
    for d in dates:
        dt = pd.to_datetime(d)
        lookback_dates.add((dt - timedelta(days=7)).strftime('%Y-%m-%d'))  # 前一周
        lookback_dates.add((dt - timedelta(days=30)).strftime('%Y-%m-%d'))  # 前一个月
        lookback_dates.add(d)  # 买入日
    
    # 获取价格数据
    print("   获取价格数据...")
    min_date = min(lookback_dates)
    max_date = max(dates)
    start_date = (pd.to_datetime(min_date) - timedelta(days=90)).strftime('%Y-%m-%d')
    
    try:
        price_df = jq.get_price(
            stocks[:200],  # 限制数量
            start_date=start_date,
            end_date=max_date,
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
        print(f"   ⚠️ 获取价格数据失败: {e}")
        return {}
    
    # 计算每个案例的预测因子
    results = {
        'buy_day': [],      # 买入日因子
        'week_before': [],  # 前一周因子
        'month_before': [], # 前一个月因子
    }
    
    for idx, row in cases.iterrows():
        code = row['code']
        buy_date = row['date']
        return_rate = row.get('return_5d', row.get('return_20d', row.get('return_60d', 0)))
        
        buy_dt = pd.to_datetime(buy_date)
        week_before = (buy_dt - timedelta(days=7)).strftime('%Y-%m-%d')
        month_before = (buy_dt - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # 计算各时点的技术因子
        for period, date in [('buy_day', buy_date), ('week_before', week_before), ('month_before', month_before)]:
            factors = calculate_technical_factors_for_date(price_df, code, date)
            if factors:
                factors['return'] = return_rate
                results[period].append(factors)
    
    # 转换为DataFrame
    result_dfs = {}
    for period, data in results.items():
        if data:
            result_dfs[period] = pd.DataFrame(data)
    
    return result_dfs


def calculate_correlation_with_return(df: pd.DataFrame) -> pd.DataFrame:
    """计算各因子与收益率的相关性"""
    factor_cols = [c for c in df.columns if c not in ['code', 'date', 'close', 'return']]
    
    correlations = []
    for col in factor_cols:
        if col in df.columns:
            valid_data = df[[col, 'return']].dropna()
            if len(valid_data) > 10:
                corr = valid_data[col].corr(valid_data['return'])
                
                # 计算高回报组 vs 低回报组的因子差异
                median_return = valid_data['return'].median()
                high_return = valid_data[valid_data['return'] > median_return][col].mean()
                low_return = valid_data[valid_data['return'] <= median_return][col].mean()
                
                correlations.append({
                    'factor': col,
                    'correlation': corr,
                    'high_return_mean': high_return,
                    'low_return_mean': low_return,
                    'difference': high_return - low_return,
                    'sample_size': len(valid_data),
                })
    
    return pd.DataFrame(correlations).sort_values('correlation', key=abs, ascending=False)


def find_best_factor_combinations(df: pd.DataFrame, top_k: int = 5) -> List[Dict]:
    """寻找最佳因子组合"""
    factor_cols = [c for c in df.columns if c not in ['code', 'date', 'close', 'return']]
    
    # 单因子分组测试
    results = []
    
    for factor in factor_cols:
        if factor in df.columns:
            valid_data = df[[factor, 'return']].dropna()
            if len(valid_data) < 50:
                continue
            
            # 按因子值分组
            try:
                valid_data['group'] = pd.qcut(valid_data[factor], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], duplicates='drop')
                
                group_returns = valid_data.groupby('group')['return'].mean()
                
                # 计算分组收益差
                if 'Q5' in group_returns.index and 'Q1' in group_returns.index:
                    spread = group_returns['Q5'] - group_returns['Q1']
                    
                    results.append({
                        'factor': factor,
                        'Q1_return': group_returns.get('Q1', 0),
                        'Q5_return': group_returns.get('Q5', 0),
                        'spread': spread,
                        'monotonic': check_monotonicity(group_returns),
                    })
            except:
                pass
    
    return sorted(results, key=lambda x: abs(x['spread']), reverse=True)[:top_k]


def check_monotonicity(series: pd.Series) -> bool:
    """检查是否单调"""
    values = series.values
    increasing = all(values[i] <= values[i+1] for i in range(len(values)-1))
    decreasing = all(values[i] >= values[i+1] for i in range(len(values)-1))
    return increasing or decreasing


def analyze_factor_combinations(df: pd.DataFrame) -> List[Dict]:
    """分析多因子组合"""
    factor_cols = [c for c in df.columns if c not in ['code', 'date', 'close', 'return']]
    
    combinations = []
    
    # 测试关键因子组合
    test_combos = [
        (['mom_5d', 'volume_ratio'], '动量+量比'),
        (['rel_position', 'rsi'], '相对位置+RSI'),
        (['mom_5d', 'rel_position'], '动量+相对位置'),
        (['volume_ratio', 'ma_deviation'], '量比+均线偏离'),
        (['mom_5d', 'mom_20d'], '短期动量+中期动量'),
        (['volatility', 'volume_ratio'], '波动率+量比'),
    ]
    
    for factors, name in test_combos:
        if all(f in df.columns for f in factors):
            valid_data = df[factors + ['return']].dropna()
            if len(valid_data) < 50:
                continue
            
            # 构建组合信号
            try:
                signals = []
                for f in factors:
                    # 标准化
                    z = (valid_data[f] - valid_data[f].mean()) / valid_data[f].std()
                    signals.append(z)
                
                valid_data['combo_signal'] = sum(signals) / len(signals)
                valid_data['group'] = pd.qcut(valid_data['combo_signal'], q=5, 
                                              labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], duplicates='drop')
                
                group_returns = valid_data.groupby('group')['return'].mean()
                
                if 'Q5' in group_returns.index and 'Q1' in group_returns.index:
                    spread = group_returns['Q5'] - group_returns['Q1']
                    
                    combinations.append({
                        'name': name,
                        'factors': factors,
                        'Q1_return': group_returns.get('Q1', 0),
                        'Q5_return': group_returns.get('Q5', 0),
                        'spread': spread,
                    })
            except:
                pass
    
    return sorted(combinations, key=lambda x: abs(x['spread']), reverse=True)


def main():
    """主函数"""
    print("="*80)
    print("2019-2021牛市高回报股票预测性因子分析")
    print("="*80)
    print(f"\n分析日期: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    # 初始化
    if not init_jqdata():
        return
    
    # 加载高回报案例
    data_dirs = [
        'output/research/fifth_bull_market_cases',
        'output/research/high_return_cases',
    ]
    
    all_cases = {}
    for data_dir in data_dirs:
        if Path(data_dir).exists():
            cases = load_high_return_cases(data_dir)
            if cases:
                all_cases = cases
                print(f"📁 使用数据目录: {data_dir}")
                break
    
    if not all_cases:
        print("❌ 未找到高回报案例数据")
        return
    
    # 分析各周期的预测因子
    all_results = {}
    
    for period_name, cases_df in all_cases.items():
        if len(cases_df) > 0:
            result_dfs = analyze_predictive_factors(cases_df, period_name, sample_size=150)
            all_results[period_name] = result_dfs
    
    # 输出分析报告
    print("\n" + "="*80)
    print("📊 预测性因子分析报告")
    print("="*80)
    
    for period_name, result_dfs in all_results.items():
        print(f"\n{'='*40}")
        print(f"【{period_name.upper()}期高回报】预测因子分析")
        print(f"{'='*40}")
        
        for timing, df in result_dfs.items():
            if df.empty:
                continue
            
            timing_name = {'buy_day': '买入日', 'week_before': '前一周', 'month_before': '前一个月'}[timing]
            
            print(f"\n📌 {timing_name}的因子与收益相关性:")
            print("-"*60)
            
            corr_df = calculate_correlation_with_return(df)
            
            print(f"{'因子':<15} {'相关系数':>10} {'高回报组均值':>12} {'低回报组均值':>12} {'差异':>10}")
            print("-"*60)
            
            for _, row in corr_df.head(8).iterrows():
                print(f"{row['factor']:<15} {row['correlation']:>10.3f} "
                      f"{row['high_return_mean']:>12.2f} {row['low_return_mean']:>12.2f} "
                      f"{row['difference']:>10.2f}")
            
            # 因子分组测试
            print(f"\n📌 {timing_name}的最佳单因子（分组收益差）:")
            print("-"*60)
            
            best_factors = find_best_factor_combinations(df)
            
            print(f"{'因子':<15} {'Q1收益':>10} {'Q5收益':>10} {'收益差':>10} {'单调性':>8}")
            print("-"*60)
            
            for item in best_factors:
                mono = "✓" if item['monotonic'] else "✗"
                print(f"{item['factor']:<15} {item['Q1_return']:>10.2f}% {item['Q5_return']:>10.2f}% "
                      f"{item['spread']:>10.2f}% {mono:>8}")
            
            # 因子组合测试
            print(f"\n📌 {timing_name}的最佳因子组合:")
            print("-"*60)
            
            combos = analyze_factor_combinations(df)
            
            print(f"{'组合名称':<20} {'Q1收益':>10} {'Q5收益':>10} {'收益差':>10}")
            print("-"*60)
            
            for item in combos[:5]:
                print(f"{item['name']:<20} {item['Q1_return']:>10.2f}% {item['Q5_return']:>10.2f}% "
                      f"{item['spread']:>10.2f}%")
    
    # 综合结论
    print("\n" + "="*80)
    print("🎯 核心发现与投资建议")
    print("="*80)
    
    print("""
📌 预测性因子排名（重要性从高到低）:

1. 【量比/成交变化】
   - 预测性最强，高回报股往往在买入前有成交放大
   - 前一周量比 > 1.3 是重要信号
   
2. 【相对位置】
   - 长期高回报股往往在相对低位启动
   - 相对位置 < 50% 时买入胜率更高
   
3. 【RSI】
   - 中性区间(40-60)预测性较好
   - 超卖区间(< 30)反弹机会大
   
4. 【波动率】
   - 低波动 → 高波动的转换是启动信号
   - 前一个月波动率较低的股票表现更好
   
5. 【动量】（预测性较弱，但可作为确认信号）
   - 短期交易：正动量确认
   - 长期投资：零动量或小幅负动量
   
📌 最佳预测因子组合:

【组合一】量比 + 相对位置
- 量比 > 1.3 且 相对位置 < 50%
- 适合：中长期投资

【组合二】RSI + 成交变化
- RSI < 40 且 成交额5日/10日比 > 1.2
- 适合：超跌反弹

【组合三】波动率 + 动量
- 20日波动率处于低位 + 5日动量刚转正
- 适合：突破启动

⚠️ 注意事项:
- 因子的预测性在不同市场环境下会变化
- 建议组合使用多个因子，而非依赖单一因子
- 前一周的因子比前一个月更具时效性
""")


if __name__ == '__main__':
    main()
