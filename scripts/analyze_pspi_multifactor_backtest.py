#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSPI概念股票多因子分析与回测

挖掘预测性因子组合，并回测周频/月频换仓的回报率。

因子分类：
1. 估值因子：PE、PB、PS、市值
2. 成长因子：营收增长、净利润增长、ROE
3. 技术因子：相对位置、波动率、换手率
4. 资金因子：主力资金、北向资金
5. 动量因子：5日/20日/60日动量（参考但不过度依赖）

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

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


# PSPI概念股票列表
PSPI_STOCKS = {
    '688323.XSHG': '瑞华泰',
    '000859.XSHE': '国风新材',
    '600458.XSHG': '时代新材',
    '300054.XSHE': '鼎龙股份',
    '002643.XSHE': '万润股份',
    '002254.XSHE': '泰和新材',
    '300429.XSHE': '强力新材',
}


def get_valuation_factors(stocks: List[str], date: str) -> pd.DataFrame:
    """获取估值因子"""
    try:
        q = jq.query(
            jq.valuation.code,
            jq.valuation.pe_ratio,
            jq.valuation.pb_ratio,
            jq.valuation.ps_ratio,
            jq.valuation.market_cap,
            jq.valuation.circulating_market_cap,
            jq.valuation.turnover_ratio,
            jq.valuation.pe_ratio_lyr,
        ).filter(
            jq.valuation.code.in_(stocks)
        )
        df = jq.get_fundamentals(q, date=date)
        return df
    except Exception as e:
        print(f"⚠️ 获取估值因子失败: {e}")
        return pd.DataFrame()


def get_financial_factors(stocks: List[str], date: str) -> pd.DataFrame:
    """获取财务因子"""
    try:
        q = jq.query(
            jq.indicator.code,
            jq.indicator.roe,
            jq.indicator.roa,
            jq.indicator.gross_profit_margin,
            jq.indicator.net_profit_margin,
            jq.indicator.inc_revenue_year_on_year,
            jq.indicator.inc_net_profit_year_on_year,
            jq.indicator.inc_operation_profit_year_on_year,
        ).filter(
            jq.indicator.code.in_(stocks)
        )
        df = jq.get_fundamentals(q, date=date)
        return df
    except Exception as e:
        print(f"⚠️ 获取财务因子失败: {e}")
        return pd.DataFrame()


def get_price_data(stocks: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """获取价格数据"""
    try:
        df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            skip_paused=True,
            fq='post',
            panel=False
        )
        if 'time' in df.columns:
            df = df.rename(columns={'time': 'date'})
        return df
    except Exception as e:
        print(f"⚠️ 获取价格数据失败: {e}")
        return pd.DataFrame()


def calculate_technical_factors(price_df: pd.DataFrame, code: str) -> Dict:
    """计算技术因子"""
    stock_data = price_df[price_df['code'] == code].sort_values('date').copy()
    
    if len(stock_data) < 60:
        return {}
    
    latest = stock_data.iloc[-1]
    
    # 基础价格数据
    close = stock_data['close'].values
    high = stock_data['high'].values
    low = stock_data['low'].values
    volume = stock_data['volume'].values
    money = stock_data['money'].values
    
    result = {
        'code': code,
        'close': latest['close'],
        'date': latest['date'],
    }
    
    # 1. 动量因子
    result['mom_5d'] = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    result['mom_20d'] = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
    result['mom_60d'] = (close[-1] / close[-61] - 1) * 100 if len(close) >= 61 else 0
    
    # 2. 相对位置（0-100，越高表示越接近高点）
    high_20 = np.max(high[-20:]) if len(high) >= 20 else high[-1]
    low_20 = np.min(low[-20:]) if len(low) >= 20 else low[-1]
    if high_20 > low_20:
        result['rel_position_20d'] = (close[-1] - low_20) / (high_20 - low_20) * 100
    else:
        result['rel_position_20d'] = 50
    
    # 3. 波动率（20日标准差/均值）
    if len(close) >= 20:
        result['volatility_20d'] = np.std(close[-20:]) / np.mean(close[-20:]) * 100
    else:
        result['volatility_20d'] = 0
    
    # 4. 量比（5日均量/20日均量）
    if len(volume) >= 20:
        vol_5d = np.mean(volume[-5:])
        vol_20d = np.mean(volume[-20:])
        result['volume_ratio'] = vol_5d / vol_20d if vol_20d > 0 else 1
    else:
        result['volume_ratio'] = 1
    
    # 5. 资金流入强度（5日成交额增长）
    if len(money) >= 10:
        money_5d = np.sum(money[-5:])
        money_5d_prev = np.sum(money[-10:-5])
        result['money_flow'] = (money_5d / money_5d_prev - 1) * 100 if money_5d_prev > 0 else 0
    else:
        result['money_flow'] = 0
    
    # 6. 均线偏离度（收盘价/MA20 - 1）
    if len(close) >= 20:
        ma_20 = np.mean(close[-20:])
        result['ma_deviation'] = (close[-1] / ma_20 - 1) * 100
    else:
        result['ma_deviation'] = 0
    
    # 7. RSI
    if len(close) >= 15:
        deltas = np.diff(close[-15:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        if avg_loss > 0:
            rs = avg_gain / avg_loss
            result['rsi_14'] = 100 - (100 / (1 + rs))
        else:
            result['rsi_14'] = 100
    else:
        result['rsi_14'] = 50
    
    # 8. 动量加速度（5日动量 - 前5日动量）
    if len(close) >= 11:
        mom_5d_now = (close[-1] / close[-6] - 1) * 100
        mom_5d_prev = (close[-6] / close[-11] - 1) * 100
        result['mom_acceleration'] = mom_5d_now - mom_5d_prev
    else:
        result['mom_acceleration'] = 0
    
    return result


def get_multifactor_data(stocks: List[str], date: str) -> pd.DataFrame:
    """获取多因子数据"""
    print(f"📥 获取多因子数据: {date}")
    
    # 获取估值因子
    valuation_df = get_valuation_factors(stocks, date)
    
    # 获取财务因子
    financial_df = get_financial_factors(stocks, date)
    
    # 获取价格数据（计算技术因子）
    start_date = (pd.to_datetime(date) - timedelta(days=120)).strftime('%Y-%m-%d')
    price_df = get_price_data(stocks, start_date, date)
    
    # 计算技术因子
    tech_factors = []
    for code in stocks:
        factors = calculate_technical_factors(price_df, code)
        if factors:
            tech_factors.append(factors)
    
    tech_df = pd.DataFrame(tech_factors)
    
    # 合并所有因子
    result = tech_df.copy()
    
    if not valuation_df.empty:
        result = result.merge(valuation_df, on='code', how='left')
    
    if not financial_df.empty:
        result = result.merge(financial_df, on='code', how='left')
    
    return result


def calculate_factor_score(row: pd.Series) -> float:
    """计算多因子综合评分"""
    score = 50.0  # 基础分
    
    # === 1. 估值因子（20%权重）===
    # PE：适中为佳（20-50之间加分）
    pe = row.get('pe_ratio', 0)
    if pe and 0 < pe < 100:
        if 15 <= pe <= 40:
            score += 5
        elif pe > 100 or pe < 0:
            score -= 5
    
    # PB：适中为佳（1-5之间加分）
    pb = row.get('pb_ratio', 0)
    if pb and 0 < pb < 20:
        if 1 <= pb <= 5:
            score += 5
        elif pb > 10:
            score -= 3
    
    # 市值：中小盘加分（20-200亿）
    market_cap = row.get('market_cap', 0)
    if market_cap and 20 <= market_cap <= 300:
        score += 5
    elif market_cap and market_cap > 500:
        score -= 3
    
    # === 2. 成长因子（30%权重）===
    # ROE：越高越好
    roe = row.get('roe', 0)
    if roe and roe > 0:
        if roe >= 15:
            score += 10
        elif roe >= 10:
            score += 5
        elif roe >= 5:
            score += 2
    
    # 营收增长：正增长加分
    rev_growth = row.get('inc_revenue_year_on_year', 0)
    if rev_growth and rev_growth > 0:
        if rev_growth >= 30:
            score += 8
        elif rev_growth >= 15:
            score += 5
        elif rev_growth >= 5:
            score += 2
    
    # 净利润增长：正增长加分
    profit_growth = row.get('inc_net_profit_year_on_year', 0)
    if profit_growth and profit_growth > 0:
        if profit_growth >= 30:
            score += 8
        elif profit_growth >= 15:
            score += 5
        elif profit_growth >= 5:
            score += 2
    
    # === 3. 技术因子（30%权重）===
    # 相对位置：中等位置加分（30-70之间）
    rel_pos = row.get('rel_position_20d', 50)
    if 30 <= rel_pos <= 70:
        score += 5
    elif rel_pos >= 80:
        score -= 3  # 过高风险
    
    # 量比：放量加分
    vol_ratio = row.get('volume_ratio', 1)
    if vol_ratio and vol_ratio > 1.2:
        score += 5
    elif vol_ratio and vol_ratio > 1.5:
        score += 8
    
    # 资金流入：正流入加分
    money_flow = row.get('money_flow', 0)
    if money_flow and money_flow > 0:
        if money_flow >= 30:
            score += 8
        elif money_flow >= 15:
            score += 5
        elif money_flow >= 5:
            score += 2
    
    # RSI：中性区间加分（30-70）
    rsi = row.get('rsi_14', 50)
    if 40 <= rsi <= 60:
        score += 5
    elif rsi > 80 or rsi < 20:
        score -= 5  # 超买/超卖风险
    
    # === 4. 动量因子（20%权重）- 作为参考 ===
    # 20日动量：适度正动量加分
    mom_20d = row.get('mom_20d', 0)
    if mom_20d and 5 <= mom_20d <= 30:
        score += 5
    elif mom_20d and mom_20d > 50:
        score -= 3  # 涨幅过大风险
    
    # 动量加速度：正加速加分
    mom_acc = row.get('mom_acceleration', 0)
    if mom_acc and mom_acc > 0:
        score += min(mom_acc, 5)
    
    return min(max(score, 0), 100)


def backtest_strategy(stocks: List[str], start_date: str, end_date: str, 
                      rebalance_freq: str = 'weekly') -> Dict:
    """
    回测多因子策略
    
    参数:
    - stocks: 股票列表
    - start_date: 开始日期
    - end_date: 结束日期
    - rebalance_freq: 换仓频率 ('weekly' 或 'monthly')
    """
    print(f"\n📊 开始回测: {start_date} ~ {end_date}, 换仓频率: {rebalance_freq}")
    
    # 获取交易日
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 确定换仓日期
    if rebalance_freq == 'weekly':
        rebalance_days = trade_days[::5]  # 每5个交易日
    else:  # monthly
        rebalance_days = trade_days[::20]  # 每20个交易日
    
    # 获取完整价格数据
    ext_start = (pd.to_datetime(start_date) - timedelta(days=120)).strftime('%Y-%m-%d')
    price_df = get_price_data(stocks, ext_start, end_date)
    
    if price_df.empty:
        print("❌ 无法获取价格数据")
        return {}
    
    # 按日期建立价格索引
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y-%m-%d')
    
    # 回测参数
    initial_capital = 1000000.0
    capital = initial_capital
    positions = {}  # {code: {'shares': n, 'cost': x}}
    max_positions = 3  # PSPI板块最多持3只
    
    results = {
        'trades': [],
        'portfolio_values': [],
        'rebalances': [],
    }
    
    for rebalance_date in rebalance_days:
        date_str = rebalance_date.strftime('%Y-%m-%d')
        
        # 获取当日多因子数据
        factor_data = get_multifactor_data(stocks, date_str)
        
        if factor_data.empty:
            continue
        
        # 计算评分
        factor_data['score'] = factor_data.apply(calculate_factor_score, axis=1)
        factor_data['name'] = factor_data['code'].map(PSPI_STOCKS)
        
        # 排序选股
        factor_data = factor_data.sort_values('score', ascending=False)
        top_stocks = factor_data.head(max_positions)['code'].tolist()
        
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
        
        # 记录组合价值
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
                proceeds = shares * price * (1 - 0.001 - 0.0001)  # 印花税+佣金
                capital += proceeds
                
                pnl = proceeds - positions[code]['shares'] * positions[code]['cost']
                results['trades'].append({
                    'date': date_str,
                    'code': code,
                    'name': PSPI_STOCKS.get(code, ''),
                    'action': 'SELL',
                    'shares': shares,
                    'price': price,
                    'pnl': pnl,
                })
                del positions[code]
        
        # 买入新股票
        buy_codes = [c for c in top_stocks if c not in positions]
        if buy_codes and capital > 10000:
            per_stock_capital = capital / len(buy_codes) * 0.95  # 95%资金
            
            for code in buy_codes:
                if code in day_prices.index:
                    price = day_prices.loc[code, 'close']
                    shares = int(per_stock_capital / price / 100) * 100  # 整手
                    
                    if shares >= 100:
                        cost = shares * price * (1 + 0.0001)  # 佣金
                        capital -= cost
                        positions[code] = {'shares': shares, 'cost': price}
                        
                        results['trades'].append({
                            'date': date_str,
                            'code': code,
                            'name': PSPI_STOCKS.get(code, ''),
                            'action': 'BUY',
                            'shares': shares,
                            'price': price,
                            'pnl': 0,
                        })
        
        # 记录换仓
        results['rebalances'].append({
            'date': date_str,
            'top_stocks': factor_data.head(max_positions)[['code', 'name', 'score']].to_dict('records'),
            'positions': list(positions.keys()),
            'total_value': total_value,
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
    
    # 计算年化收益
    days = (trade_days[-1] - trade_days[0]).days
    annual_return = total_return * 365 / days if days > 0 else 0
    
    results['summary'] = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'total_trades': len(results['trades']),
        'rebalances': len(results['rebalances']),
        'days': days,
    }
    
    return results


def analyze_and_backtest():
    """分析并回测PSPI概念股票"""
    
    print("="*80)
    print("PSPI概念股票多因子分析与回测")
    print("="*80)
    print(f"\n分析日期: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    # 初始化JQData
    if not init_jqdata():
        return
    
    stocks = list(PSPI_STOCKS.keys())
    
    # 获取最新交易日
    trade_days = jq.get_trade_days(end_date=datetime.now(), count=5)
    latest_date = trade_days[-1].strftime('%Y-%m-%d')
    
    print(f"最新交易日: {latest_date}\n")
    
    # ============ 1. 当前多因子分析 ============
    print("="*80)
    print("📊 当前多因子分析")
    print("="*80)
    
    factor_data = get_multifactor_data(stocks, latest_date)
    
    if not factor_data.empty:
        factor_data['score'] = factor_data.apply(calculate_factor_score, axis=1)
        factor_data['name'] = factor_data['code'].map(PSPI_STOCKS)
        factor_data = factor_data.sort_values('score', ascending=False)
        
        print(f"\n{'股票':<12} {'评分':>6} {'PE':>8} {'PB':>6} {'ROE':>6} {'营收增长':>8} {'量比':>6} {'相对位置':>8}")
        print("-"*80)
        
        for _, row in factor_data.iterrows():
            pe = row.get('pe_ratio', 0) or 0
            pb = row.get('pb_ratio', 0) or 0
            roe = row.get('roe', 0) or 0
            rev_g = row.get('inc_revenue_year_on_year', 0) or 0
            vol_r = row.get('volume_ratio', 0) or 0
            rel_p = row.get('rel_position_20d', 0) or 0
            
            print(f"{row['name']:<12} {row['score']:>6.1f} {pe:>8.1f} {pb:>6.2f} "
                  f"{roe:>6.1f}% {rev_g:>7.1f}% {vol_r:>6.2f} {rel_p:>7.1f}%")
        
        # 当前推荐
        print("\n📌 当前多因子推荐排名:")
        for idx, (_, row) in enumerate(factor_data.iterrows(), 1):
            rec = "★★★" if row['score'] >= 75 else "★★" if row['score'] >= 65 else "★"
            print(f"  {idx}. {row['name']}({row['code']}): 评分={row['score']:.1f} {rec}")
    
    # ============ 2. 回测验证 ============
    print("\n" + "="*80)
    print("📈 回测验证（过去6个月）")
    print("="*80)
    
    # 回测时间范围
    end_date = latest_date
    start_date = (pd.to_datetime(end_date) - timedelta(days=180)).strftime('%Y-%m-%d')
    
    # 周频回测
    print("\n" + "-"*40)
    print("【周频换仓回测】")
    print("-"*40)
    
    weekly_results = backtest_strategy(stocks, start_date, end_date, 'weekly')
    
    if weekly_results and 'summary' in weekly_results:
        s = weekly_results['summary']
        print(f"\n周频回测结果:")
        print(f"  初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"  最终价值: ¥{s['final_value']:,.0f}")
        print(f"  总收益率: {s['total_return']:.2f}%")
        print(f"  年化收益: {s['annual_return']:.2f}%")
        print(f"  交易次数: {s['total_trades']}")
        print(f"  换仓次数: {s['rebalances']}")
    
    # 月频回测
    print("\n" + "-"*40)
    print("【月频换仓回测】")
    print("-"*40)
    
    monthly_results = backtest_strategy(stocks, start_date, end_date, 'monthly')
    
    if monthly_results and 'summary' in monthly_results:
        s = monthly_results['summary']
        print(f"\n月频回测结果:")
        print(f"  初始资金: ¥{s['initial_capital']:,.0f}")
        print(f"  最终价值: ¥{s['final_value']:,.0f}")
        print(f"  总收益率: {s['total_return']:.2f}%")
        print(f"  年化收益: {s['annual_return']:.2f}%")
        print(f"  交易次数: {s['total_trades']}")
        print(f"  换仓次数: {s['rebalances']}")
    
    # ============ 3. 综合建议 ============
    print("\n" + "="*80)
    print("🎯 综合投资建议")
    print("="*80)
    
    if weekly_results and monthly_results:
        w_ret = weekly_results['summary']['total_return']
        m_ret = monthly_results['summary']['total_return']
        
        print(f"\n📊 换仓频率对比:")
        print(f"  周频换仓: {w_ret:.2f}%")
        print(f"  月频换仓: {m_ret:.2f}%")
        
        if w_ret > m_ret:
            print(f"  ➡️ 建议：周频换仓更优（高出{w_ret - m_ret:.2f}%）")
        else:
            print(f"  ➡️ 建议：月频换仓更优（高出{m_ret - w_ret:.2f}%）")
    
    print("\n📌 多因子选股要点:")
    print("  1. 优先选择ROE > 10%、营收增长 > 15%的成长股")
    print("  2. PE在15-40之间、PB在1-5之间估值合理")
    print("  3. 量比 > 1.2表示资金关注度提升")
    print("  4. 相对位置在30%-70%之间安全边际较高")
    print("  5. 动量因子作为辅助，不过度依赖")
    
    print("\n⚠️ 风险提示:")
    print("  1. 历史回测不代表未来收益")
    print("  2. PSPI概念股波动较大，注意仓位控制")
    print("  3. 建议分散投资，单只股票仓位 ≤ 15%")
    print("  4. 设置止损位: -10%")
    
    return weekly_results, monthly_results


if __name__ == '__main__':
    analyze_and_backtest()
