#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期策略 - 近5年回测验证

专门针对S2加速期阶段股票进行长周期回测：
1. 每年6月1日筛选S2阶段股票
2. 持有一年计算收益
3. 统计所有高回报股票
"""

import sys
import os

# 工作目录：/home/taotao/.cursor/worktrees/TRQuant/ope
PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate


# ============================================================
# 优化后的S2阶段识别器（放宽条件）
# ============================================================

class S2StageIdentifier:
    """S2加速期识别器
    
    S2加速期特征：
    - 市值：50-500亿
    - 利润增速：>25%
    - ROE：>12%
    - 业绩爆发期，最佳买入时机
    """
    
    def is_s2_stage(self, market_cap: float, revenue_growth: float,
                    profit_growth: float, roe: float) -> Tuple[bool, float]:
        """判断是否为S2加速期
        
        Returns:
            (是否S2阶段, 得分)
        """
        score = 50  # 基础分
        
        # 市值条件：50-500亿（最佳）
        if 50 <= market_cap <= 300:
            score += 15
        elif 30 <= market_cap <= 500:
            score += 10
        elif market_cap > 500 or market_cap < 30:
            return False, 0
        
        # 利润增速：>25%（核心条件）
        if profit_growth >= 0.50:
            score += 20
        elif profit_growth >= 0.30:
            score += 15
        elif profit_growth >= 0.25:
            score += 10
        else:
            return False, 0
        
        # ROE：>12%
        if roe >= 0.20:
            score += 15
        elif roe >= 0.15:
            score += 10
        elif roe >= 0.12:
            score += 5
        else:
            return False, 0
        
        # 营收增速加分
        if revenue_growth >= 0.30:
            score += 10
        elif revenue_growth >= 0.20:
            score += 5
        
        return True, score


# ============================================================
# 数据获取
# ============================================================

def get_all_stocks(date_str: str) -> pd.DataFrame:
    """获取所有A股"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    
    # 过滤ST、退市、科创板、北交所
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &
        ~all_stocks.index.str.startswith('8')
    ]
    return valid


def get_fundamentals(codes: List[str], date_str: str) -> pd.DataFrame:
    """获取基本面数据（直接从聚宽获取）"""
    batch_size = 1000
    all_dfs = []
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i+batch_size]
        q = jq.query(
            jq.valuation.code,
            jq.valuation.market_cap,
            jq.valuation.pe_ratio,
            jq.indicator.roe,
            jq.indicator.inc_revenue_year_on_year,
            jq.indicator.inc_net_profit_year_on_year,
        ).filter(jq.valuation.code.in_(batch))
        
        df = jq.get_fundamentals(q, date=date_str)
        if df is not None and not df.empty:
            all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True).set_index('code')
    return pd.DataFrame()


def get_stock_return(code: str, start_date: str, end_date: str) -> Optional[float]:
    """计算单只股票收益率"""
    try:
        price_df = jq.get_price(
            code,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False
        )
        
        if price_df is None or len(price_df) < 2:
            return None
        
        start_price = price_df['close'].iloc[0]
        end_price = price_df['close'].iloc[-1]
        
        if start_price <= 0:
            return None
        
        return (end_price - start_price) / start_price
        
    except Exception:
        return None


# ============================================================
# S2策略筛选与回测
# ============================================================

@dataclass
class StockResult:
    """股票结果"""
    code: str
    name: str
    screen_date: str
    market_cap: float
    profit_growth: float
    revenue_growth: float
    roe: float
    score: float
    return_1y: Optional[float] = None


def screen_s2_stocks(screen_date: str, stocks_df: pd.DataFrame) -> List[StockResult]:
    """筛选S2阶段股票"""
    identifier = S2StageIdentifier()
    
    codes = stocks_df.index.tolist()
    fundamentals = get_fundamentals(codes, screen_date)
    
    results = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            
            market_cap = fund.get('market_cap', 0)
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            
            # 基本过滤
            if pe <= 0 or pe > 200:
                continue
            
            # S2阶段判断
            is_s2, score = identifier.is_s2_stage(market_cap, revenue_growth, profit_growth, roe)
            
            if is_s2:
                name = stocks_df.loc[code, 'display_name'] if code in stocks_df.index else code
                results.append(StockResult(
                    code=code,
                    name=name,
                    screen_date=screen_date,
                    market_cap=market_cap,
                    profit_growth=profit_growth,
                    revenue_growth=revenue_growth,
                    roe=roe,
                    score=score
                ))
                
        except Exception:
            continue
    
    # 按得分排序
    results.sort(key=lambda x: x.score, reverse=True)
    return results


def calculate_returns(stocks: List[StockResult], hold_days: int = 252) -> List[StockResult]:
    """计算收益率"""
    for stock in stocks:
        screen_date = datetime.strptime(stock.screen_date, '%Y-%m-%d')
        end_date = screen_date + timedelta(days=hold_days + 30)  # 多加30天确保覆盖
        
        ret = get_stock_return(
            stock.code,
            stock.screen_date,
            end_date.strftime('%Y-%m-%d')
        )
        stock.return_1y = ret
    
    return stocks


# ============================================================
# 主回测流程
# ============================================================

def run_5year_backtest():
    """运行5年回测"""
    
    print("="*70)
    print("S2加速期策略 - 近5年回测")
    print("="*70)
    
    # 认证
    authenticate()
    
    # 每年6月1日筛选
    screen_dates = [
        '2020-06-01',
        '2021-06-01',
        '2022-06-01',
        '2023-06-01',
        '2024-06-01',
    ]
    
    all_results = []
    yearly_stats = []
    
    for screen_date in screen_dates:
        print(f"\n{'='*60}")
        print(f"筛选日期: {screen_date}")
        print("="*60)
        
        # 获取股票列表
        stocks_df = get_all_stocks(screen_date)
        print(f"有效股票: {len(stocks_df)} 只")
        
        # 筛选S2阶段股票
        s2_stocks = screen_s2_stocks(screen_date, stocks_df)
        print(f"S2阶段股票: {len(s2_stocks)} 只")
        
        if not s2_stocks:
            print("无S2阶段股票，跳过")
            continue
        
        # 取前20只
        top_stocks = s2_stocks[:20]
        print(f"选取Top20股票进行回测")
        
        # 计算1年收益
        print("计算1年收益...")
        top_stocks = calculate_returns(top_stocks, hold_days=252)
        
        # 统计
        valid_returns = [s.return_1y for s in top_stocks if s.return_1y is not None]
        if valid_returns:
            avg_return = np.mean(valid_returns)
            max_return = np.max(valid_returns)
            min_return = np.min(valid_returns)
            win_rate = sum(1 for r in valid_returns if r > 0) / len(valid_returns)
            
            print(f"\n{screen_date} 年度统计:")
            print(f"  平均收益: {avg_return*100:.2f}%")
            print(f"  最高收益: {max_return*100:.2f}%")
            print(f"  最低收益: {min_return*100:.2f}%")
            print(f"  胜率: {win_rate*100:.1f}%")
            
            yearly_stats.append({
                'year': screen_date[:4],
                'stock_count': len(valid_returns),
                'avg_return': avg_return,
                'max_return': max_return,
                'min_return': min_return,
                'win_rate': win_rate
            })
        
        all_results.extend(top_stocks)
    
    # ============================================================
    # 汇总分析
    # ============================================================
    
    print("\n" + "="*70)
    print("5年汇总统计")
    print("="*70)
    
    # 年度统计表
    print("\n年度表现:")
    print("-"*70)
    print(f"{'年份':<8} {'股票数':<8} {'平均收益':<12} {'最高收益':<12} {'最低收益':<12} {'胜率':<8}")
    print("-"*70)
    
    for stat in yearly_stats:
        print(f"{stat['year']:<8} {stat['stock_count']:<8} "
              f"{stat['avg_return']*100:>8.2f}%    {stat['max_return']*100:>8.2f}%    "
              f"{stat['min_return']*100:>8.2f}%    {stat['win_rate']*100:>5.1f}%")
    
    # 整体统计
    all_valid_returns = [s.return_1y for s in all_results if s.return_1y is not None]
    if all_valid_returns:
        print("-"*70)
        print(f"{'5年汇总':<8} {len(all_valid_returns):<8} "
              f"{np.mean(all_valid_returns)*100:>8.2f}%    {np.max(all_valid_returns)*100:>8.2f}%    "
              f"{np.min(all_valid_returns)*100:>8.2f}%    "
              f"{sum(1 for r in all_valid_returns if r > 0)/len(all_valid_returns)*100:>5.1f}%")
    
    # ============================================================
    # 高回报股票统计
    # ============================================================
    
    print("\n" + "="*70)
    print("高回报股票统计 (收益 > 50%)")
    print("="*70)
    
    high_return_stocks = [s for s in all_results if s.return_1y is not None and s.return_1y > 0.5]
    high_return_stocks.sort(key=lambda x: x.return_1y, reverse=True)
    
    print(f"\n共 {len(high_return_stocks)} 只高回报股票 (收益>50%):\n")
    print("-"*100)
    print(f"{'排名':<5} {'代码':<12} {'名称':<12} {'筛选日':<12} {'市值(亿)':<10} "
          f"{'利润增速':<10} {'ROE':<8} {'1年收益':<10}")
    print("-"*100)
    
    for i, s in enumerate(high_return_stocks[:50], 1):  # 显示前50只
        print(f"{i:<5} {s.code:<12} {s.name:<12} {s.screen_date:<12} "
              f"{s.market_cap:>8.1f}  {s.profit_growth*100:>8.1f}%  "
              f"{s.roe*100:>6.1f}%  {s.return_1y*100:>8.1f}%")
    
    # ============================================================
    # 超高回报股票（翻倍以上）
    # ============================================================
    
    print("\n" + "="*70)
    print("超高回报股票统计 (收益 > 100%，翻倍)")
    print("="*70)
    
    double_stocks = [s for s in all_results if s.return_1y is not None and s.return_1y > 1.0]
    double_stocks.sort(key=lambda x: x.return_1y, reverse=True)
    
    print(f"\n共 {len(double_stocks)} 只翻倍股票:\n")
    
    for i, s in enumerate(double_stocks, 1):
        print(f"{i}. {s.code} {s.name}")
        print(f"   筛选日: {s.screen_date}, 市值: {s.market_cap:.1f}亿")
        print(f"   利润增速: {s.profit_growth*100:.1f}%, ROE: {s.roe*100:.1f}%")
        print(f"   1年收益: {s.return_1y*100:.1f}%")
        print()
    
    # ============================================================
    # 特征分析
    # ============================================================
    
    print("\n" + "="*70)
    print("高回报股票特征分析")
    print("="*70)
    
    if high_return_stocks:
        avg_mcap = np.mean([s.market_cap for s in high_return_stocks])
        avg_pg = np.mean([s.profit_growth for s in high_return_stocks])
        avg_roe = np.mean([s.roe for s in high_return_stocks])
        
        print(f"\n高回报股票(>50%)平均特征:")
        print(f"  平均市值: {avg_mcap:.1f} 亿")
        print(f"  平均利润增速: {avg_pg*100:.1f}%")
        print(f"  平均ROE: {avg_roe*100:.1f}%")
    
    # 保存结果
    results_df = pd.DataFrame([{
        'code': s.code,
        'name': s.name,
        'screen_date': s.screen_date,
        'market_cap': s.market_cap,
        'profit_growth': s.profit_growth,
        'revenue_growth': s.revenue_growth,
        'roe': s.roe,
        'score': s.score,
        'return_1y': s.return_1y
    } for s in all_results if s.return_1y is not None])
    
    output_path = '/home/taotao/.cursor/worktrees/TRQuant/ope/results'
    os.makedirs(output_path, exist_ok=True)
    results_df.to_csv(f'{output_path}/s2_strategy_5year_results.csv', index=False, encoding='utf-8-sig')
    print(f"\n结果已保存到: {output_path}/s2_strategy_5year_results.csv")
    
    return all_results, yearly_stats


if __name__ == '__main__':
    run_5year_backtest()
