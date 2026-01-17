#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
超额收益优化器

基于验证分析结果，优化选股策略以提升超额收益能力：

优化方向：
1. 过滤异常值：ROE上限50%，排除异常财务数据
2. 增加动量因子：20日动量、相对强度(RS)
3. 增加资金流向：换手率、量比
4. 行业轮动：选择近期强势行业
5. 限制追高：排除近期涨幅过大的股票
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AlphaOptimizedRecommender:
    """超额收益优化选股器"""
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
        
        # 优化后的参数
        self.params = {
            # 基本面筛选（优化）
            "market_cap_min": 50,    # 提高市值下限，排除微盘股
            "market_cap_max": 500,   # 降低市值上限，聚焦成长股
            "roe_min": 10,           # 提高ROE下限
            "roe_max": 50,           # 新增ROE上限，排除异常值
            "growth_min": 20,        # 提高增长率下限
            "growth_max": 500,       # 新增增长率上限，排除异常值
            
            # 动量筛选（新增）
            "momentum_min": -5,      # 20日动量下限
            "momentum_max": 25,      # 20日动量上限（限制追高）
            "rs_min": 0.8,           # 相对强度下限（跑赢大盘）
            
            # 量价筛选（新增）
            "turnover_min": 2,       # 换手率下限%
            "turnover_max": 20,      # 换手率上限%
            
            # 评分权重（优化）
            "weight_roe": 0.25,
            "weight_growth": 0.20,
            "weight_momentum": 0.25,  # 新增动量权重
            "weight_rs": 0.20,        # 新增相对强度权重
            "weight_value": 0.10,     # 估值权重
        }
    
    def _init_jqdata(self):
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            if jq_config:
                jq.auth(jq_config.get('username'), jq_config.get('password'))
                if jq.is_auth():
                    self.jq = jq
                    logger.info("JQData初始化成功")
        except Exception as e:
            logger.warning(f"JQData初始化失败: {e}")
    
    def get_strong_industries(self, date: str, top_n: int = 5) -> List[str]:
        """获取近期强势行业"""
        if not self.jq:
            return []
        
        try:
            # 获取申万一级行业
            industries = self.jq.get_industries(name='sw_l1')
            
            # 计算各行业近20日涨幅
            end_dt = datetime.strptime(date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=30)
            
            industry_returns = []
            for idx, row in industries.iterrows():
                try:
                    # 获取行业指数
                    industry_code = idx
                    stocks = self.jq.get_industry_stocks(industry_code, date=date)[:20]
                    
                    if not stocks:
                        continue
                    
                    # 计算平均涨幅
                    df = self.jq.get_price(
                        stocks,
                        start_date=start_dt.strftime("%Y-%m-%d"),
                        end_date=date,
                        frequency='daily',
                        fields=['close'],
                        panel=False
                    )
                    
                    if df is not None and not df.empty:
                        returns = df.groupby('code').apply(
                            lambda x: (x['close'].iloc[-1] / x['close'].iloc[0] - 1) * 100
                            if len(x) > 0 else 0
                        )
                        avg_ret = returns.mean()
                        
                        industry_returns.append({
                            'code': industry_code,
                            'name': row['name'],
                            'return': avg_ret,
                        })
                except:
                    continue
            
            # 排序取TOP
            industry_returns = sorted(industry_returns, key=lambda x: x['return'], reverse=True)
            strong_industries = [i['code'] for i in industry_returns[:top_n]]
            
            logger.info(f"强势行业: {[i['name'] for i in industry_returns[:top_n]]}")
            return strong_industries
            
        except Exception as e:
            logger.warning(f"获取强势行业失败: {e}")
            return []
    
    def get_stock_momentum(self, code: str, date: str) -> Dict[str, float]:
        """获取股票动量指标"""
        if not self.jq:
            return {}
        
        try:
            end_dt = datetime.strptime(date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=60)
            
            df = self.jq.get_price(
                code,
                start_date=start_dt.strftime("%Y-%m-%d"),
                end_date=date,
                frequency='daily',
                fields=['close', 'volume', 'money']
            )
            
            if df is None or len(df) < 20:
                return {}
            
            close = df['close']
            
            # 20日动量
            momentum_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
            
            # 5日动量
            momentum_5d = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
            
            # 计算相对强度（相对沪深300）
            bench_df = self.jq.get_price(
                "000300.XSHG",
                start_date=start_dt.strftime("%Y-%m-%d"),
                end_date=date,
                frequency='daily',
                fields=['close']
            )
            
            rs = 1.0
            if bench_df is not None and len(bench_df) >= 20:
                bench_ret = bench_df['close'].iloc[-1] / bench_df['close'].iloc[-20] - 1
                stock_ret = close.iloc[-1] / close.iloc[-20] - 1
                rs = (1 + stock_ret) / (1 + bench_ret) if bench_ret > -1 else 1
            
            # 换手率（近5日平均）
            turnover = df['money'].tail(5).sum() / (df['close'].tail(5).mean() * 100000000) * 100
            
            return {
                'momentum_20d': momentum_20d,
                'momentum_5d': momentum_5d,
                'rs': rs,
                'turnover': turnover,
            }
        except:
            return {}
    
    def get_recommendations(self, date: str, top_n: int = 15) -> List[Dict]:
        """获取优化后的股票推荐"""
        if not self.jq:
            return []
        
        try:
            # 1. 获取强势行业
            strong_industries = self.get_strong_industries(date, top_n=8)
            
            # 2. 获取所有A股
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            stocks = stocks[~stocks.index.str.startswith('688')]  # 排除科创板
            stocks = stocks[~stocks['display_name'].str.contains('ST')]  # 排除ST
            stock_list = stocks.index.tolist()[:1000]
            
            # 3. 获取基本面数据
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.market_cap,
                self.jq.valuation.pe_ratio,
                self.jq.indicator.roe,
                self.jq.indicator.inc_net_profit_year_on_year,
            ).filter(
                self.jq.valuation.code.in_(stock_list),
                self.jq.valuation.market_cap.between(
                    self.params["market_cap_min"], 
                    self.params["market_cap_max"]
                ),
            )
            
            df = self.jq.get_fundamentals(q, date=date)
            
            if df is None or df.empty:
                return []
            
            # 4. 基本面筛选（优化）
            df = df[df['roe'] >= self.params["roe_min"]]
            df = df[df['roe'] <= self.params["roe_max"]]
            df = df[df['inc_net_profit_year_on_year'] >= self.params["growth_min"]]
            df = df[df['inc_net_profit_year_on_year'] <= self.params["growth_max"]]
            df = df.dropna(subset=['roe', 'inc_net_profit_year_on_year'])
            
            if df.empty:
                return []
            
            # 5. 获取行业信息并筛选强势行业
            candidates = []
            for _, row in df.iterrows():
                code = row['code']
                
                # 获取行业
                try:
                    ind_info = self.jq.get_industry(code, date=date)
                    industry = ind_info.get(code, {}).get('sw_l1', {}).get('industry_code', '')
                    
                    # 优先选择强势行业
                    in_strong_industry = industry in strong_industries
                except:
                    industry = ''
                    in_strong_industry = False
                
                # 获取动量指标
                momentum = self.get_stock_momentum(code, date)
                
                if not momentum:
                    continue
                
                # 动量筛选
                if not (self.params["momentum_min"] <= momentum.get('momentum_20d', 0) <= self.params["momentum_max"]):
                    continue
                
                # 相对强度筛选
                if momentum.get('rs', 0) < self.params["rs_min"]:
                    continue
                
                # 换手率筛选
                if not (self.params["turnover_min"] <= momentum.get('turnover', 0) <= self.params["turnover_max"]):
                    continue
                
                # 获取名称
                try:
                    sec_info = self.jq.get_security_info(code)
                    name = sec_info.display_name if sec_info else code
                except:
                    name = code
                
                # 计算综合评分
                roe_score = min(row['roe'] / 20, 1) * 100  # ROE归一化
                growth_score = min(row['inc_net_profit_year_on_year'] / 100, 1) * 100  # 增长率归一化
                momentum_score = (momentum.get('momentum_20d', 0) + 10) / 35 * 100  # 动量归一化
                rs_score = min(momentum.get('rs', 1) - 0.8, 0.4) / 0.4 * 100  # RS归一化
                
                # PE估值评分（低PE得高分）
                pe = row.get('pe_ratio', 50)
                value_score = max(0, (50 - min(pe, 100)) / 50 * 100) if pe > 0 else 50
                
                # 综合评分
                total_score = (
                    roe_score * self.params["weight_roe"] +
                    growth_score * self.params["weight_growth"] +
                    momentum_score * self.params["weight_momentum"] +
                    rs_score * self.params["weight_rs"] +
                    value_score * self.params["weight_value"]
                )
                
                # 强势行业加分
                if in_strong_industry:
                    total_score *= 1.15
                
                candidates.append({
                    'code': code,
                    'name': name,
                    'market_cap': row['market_cap'],
                    'roe': row['roe'],
                    'growth': row['inc_net_profit_year_on_year'],
                    'pe': row.get('pe_ratio', 0),
                    'momentum_20d': momentum.get('momentum_20d', 0),
                    'momentum_5d': momentum.get('momentum_5d', 0),
                    'rs': momentum.get('rs', 1),
                    'turnover': momentum.get('turnover', 0),
                    'in_strong_industry': in_strong_industry,
                    'score': total_score,
                })
            
            # 排序取TOP
            candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
            return candidates[:top_n]
            
        except Exception as e:
            logger.error(f"获取推荐失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def validate_recommendations(self, date: str, stocks: List[Dict]) -> List[Dict]:
        """验证推荐的实际收益"""
        if not self.jq or not stocks:
            return []
        
        results = []
        
        # 获取基准收益
        bench = self._get_returns("000300.XSHG", date)
        bench_20d = bench.get('ret_20d', 0)
        
        for stock in stocks:
            returns = self._get_returns(stock['code'], date)
            if returns and 'ret_20d' in returns:
                results.append({
                    **stock,
                    'ret_5d': returns.get('ret_5d', 0),
                    'ret_10d': returns.get('ret_10d', 0),
                    'ret_20d': returns.get('ret_20d', 0),
                    'alpha_20d': returns.get('ret_20d', 0) - bench_20d,
                    'bench_20d': bench_20d,
                })
        
        return results
    
    def _get_returns(self, code: str, start_date: str) -> Dict[str, float]:
        """获取收益率"""
        try:
            end_dt = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=35)
            
            df = self.jq.get_price(
                code,
                start_date=start_date,
                end_date=end_dt.strftime("%Y-%m-%d"),
                frequency='daily',
                fields=['close'],
                skip_paused=True,
                fq='post'
            )
            
            if df is None or len(df) < 2:
                return {}
            
            base = df.iloc[0]['close']
            
            returns = {}
            if len(df) > 5:
                returns['ret_5d'] = (df.iloc[5]['close'] / base - 1) * 100
            if len(df) > 10:
                returns['ret_10d'] = (df.iloc[10]['close'] / base - 1) * 100
            if len(df) > 20:
                returns['ret_20d'] = (df.iloc[20]['close'] / base - 1) * 100
            else:
                returns['ret_20d'] = (df.iloc[-1]['close'] / base - 1) * 100
            
            return returns
        except:
            return {}


def run_comparison_test():
    """对比测试：原始策略 vs 优化策略"""
    recommender = AlphaOptimizedRecommender()
    
    # 测试日期（使用测试集时期）
    test_dates = ['2025-09-01', '2025-09-15', '2025-10-21', '2025-11-04', '2025-11-18', '2025-12-02']
    
    print("=" * 70)
    print("优化策略测试 - 测试集验证 (2025-09 ~ 2025-12)")
    print("=" * 70)
    
    all_results = []
    
    for date in test_dates:
        print(f"\n验证日期: {date}")
        
        # 获取优化推荐
        stocks = recommender.get_recommendations(date, top_n=15)
        print(f"  优化筛选: {len(stocks)} 只")
        
        if not stocks:
            continue
        
        # 验证收益
        results = recommender.validate_recommendations(date, stocks)
        print(f"  有效验证: {len(results)} 只")
        
        if results:
            avg_ret = np.mean([r['ret_20d'] for r in results])
            avg_alpha = np.mean([r['alpha_20d'] for r in results])
            win_rate = sum(1 for r in results if r['ret_20d'] > 0) / len(results)
            hit_rate = sum(1 for r in results if r['alpha_20d'] > 0) / len(results)
            
            print(f"  20日收益: {avg_ret:.2f}% | 超额: {avg_alpha:.2f}% | 胜率: {win_rate:.1%} | 命中率: {hit_rate:.1%}")
            
            all_results.extend(results)
    
    # 汇总
    if all_results:
        print("\n" + "=" * 70)
        print("优化策略汇总")
        print("=" * 70)
        
        rets_20d = [r['ret_20d'] for r in all_results]
        alphas = [r['alpha_20d'] for r in all_results]
        
        print(f"\n总推荐数: {len(all_results)}")
        print(f"\n收益率:")
        print(f"  平均5日收益: {np.mean([r['ret_5d'] for r in all_results]):.2f}%")
        print(f"  平均10日收益: {np.mean([r['ret_10d'] for r in all_results]):.2f}%")
        print(f"  平均20日收益: {np.mean(rets_20d):.2f}%")
        
        print(f"\n胜率:")
        print(f"  5日胜率: {sum(1 for r in all_results if r['ret_5d'] > 0) / len(all_results):.1%}")
        print(f"  10日胜率: {sum(1 for r in all_results if r['ret_10d'] > 0) / len(all_results):.1%}")
        print(f"  20日胜率: {sum(1 for r in rets_20d if r > 0) / len(rets_20d):.1%}")
        
        print(f"\n超额收益:")
        print(f"  平均超额收益: {np.mean(alphas):.2f}%")
        print(f"  命中率(超额>0): {sum(1 for a in alphas if a > 0) / len(alphas):.1%}")
        
        print(f"\n风险指标:")
        vol = np.std(rets_20d)
        sharpe = (np.mean(rets_20d) - 0.25) / vol if vol > 0 else 0
        print(f"  夏普比率: {sharpe:.3f}")
        print(f"  波动率: {vol:.2f}%")
        print(f"  最大单笔亏损: {min(rets_20d):.2f}%")
        print(f"  最大单笔盈利: {max(rets_20d):.2f}%")
        
        # 与原始策略对比
        print("\n" + "=" * 70)
        print("与原始策略对比（测试集）")
        print("=" * 70)
        print(f"\n{'指标':<20} {'原始策略':<15} {'优化策略':<15} {'改进':<15}")
        print("-" * 65)
        
        # 原始策略指标（从之前验证结果）
        original = {
            'avg_ret_20d': 0.72,
            'win_rate': 0.489,
            'avg_alpha': -0.36,
            'hit_rate': 0.386,
            'sharpe': 0.036,
        }
        
        optimized = {
            'avg_ret_20d': np.mean(rets_20d),
            'win_rate': sum(1 for r in rets_20d if r > 0) / len(rets_20d),
            'avg_alpha': np.mean(alphas),
            'hit_rate': sum(1 for a in alphas if a > 0) / len(alphas),
            'sharpe': sharpe,
        }
        
        print(f"{'平均20日收益':<20} {original['avg_ret_20d']:>10.2f}%    {optimized['avg_ret_20d']:>10.2f}%    {optimized['avg_ret_20d'] - original['avg_ret_20d']:>+10.2f}%")
        print(f"{'20日胜率':<20} {original['win_rate']:>10.1%}    {optimized['win_rate']:>10.1%}    {(optimized['win_rate'] - original['win_rate'])*100:>+10.1f}%")
        print(f"{'超额收益':<20} {original['avg_alpha']:>10.2f}%    {optimized['avg_alpha']:>10.2f}%    {optimized['avg_alpha'] - original['avg_alpha']:>+10.2f}%")
        print(f"{'命中率':<20} {original['hit_rate']:>10.1%}    {optimized['hit_rate']:>10.1%}    {(optimized['hit_rate'] - original['hit_rate'])*100:>+10.1f}%")
        print(f"{'夏普比率':<20} {original['sharpe']:>12.3f}   {optimized['sharpe']:>12.3f}   {optimized['sharpe'] - original['sharpe']:>+12.3f}")
        
        # 保存结果
        df = pd.DataFrame(all_results)
        df.to_csv('results/alpha_optimized_results.csv', index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: results/alpha_optimized_results.csv")


if __name__ == "__main__":
    run_comparison_test()
