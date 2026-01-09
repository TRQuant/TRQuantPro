#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多维因子计算器 - 计算已验证因子（100%权重）

功能：
1. 计算7个已验证因子（基于438个历史10%+案例）
2. 综合得分计算（100%已验证因子，不再使用聚宽因子融合）
3. 因子选择与权重优化支持
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

import pandas as pd
import numpy as np
from tqdm import tqdm

logger = logging.getLogger(__name__)

# 已验证因子（基于历史10%+案例，100%权重）
from .validated_factor_calculator import ValidatedFactorCalculator


class FactorDimension(Enum):
    """因子维度"""
    FUNDAMENTAL = "fundamental"     # 基本面
    TECHNICAL = "technical"         # 技术面
    CAPITAL = "capital"             # 资金面
    SENTIMENT = "sentiment"         # 情绪/事件
    MARKET_ENV = "market_env"       # 市场环境


@dataclass
class FactorConfig:
    """因子配置"""
    # 基本面因子权重
    fundamental_weights: Dict = field(default_factory=lambda: {
        'roe': 0.25,
        'growth': 0.30,
        'revenue_growth': 0.20,
        'peg': 0.15,
        'gross_margin': 0.10,
    })
    
    # 技术面因子权重
    technical_weights: Dict = field(default_factory=lambda: {
        'momentum_5d': 0.15,
        'momentum_10d': 0.20,
        'momentum_20d': 0.25,
        'rel_strength': 0.20,
        'rsi': 0.10,
        'volume_ratio': 0.10,
    })
    
    # 资金面因子权重
    capital_weights: Dict = field(default_factory=lambda: {
        'fin_change': 0.40,
        'turnover_rate': 0.30,
        'on_billboard': 0.30,
    })
    
    # 情绪/事件因子权重
    sentiment_weights: Dict = field(default_factory=lambda: {
        'concept_count': 0.50,
        'industry_hot': 0.50,
    })
    
    # 市场环境因子权重
    market_env_weights: Dict = field(default_factory=lambda: {
        'market_trend': 0.50,
        'sector_rotation': 0.50,
    })
    
    # 维度权重
    dimension_weights: Dict = field(default_factory=lambda: {
        'fundamental': 0.15,
        'technical': 0.35,
        'capital': 0.25,
        'sentiment': 0.15,
        'market_env': 0.10,
    })


class MultiFactorCalculator:
    """多维因子计算器"""
    
    def __init__(
        self,
        config: FactorConfig = None,
        verbose: bool = True,
        factor_selection: Optional[List[str]] = None,  # 因子选择（默认None表示使用全部7个因子）
        factor_weights: Optional[Dict[str, float]] = None,  # 因子权重（默认None表示使用理论权重）
    ):
        self.config = config or FactorConfig()
        self.verbose = verbose
        # 默认使用全部7个已验证因子
        self._factor_selection = factor_selection  # None=使用全部7个因子，否则使用指定的因子
        self._factor_weights = factor_weights  # None=使用理论权重，否则使用自定义权重
        self.jq = None
        self._init_jqdata()
        
        # 已验证因子计算器（基于历史10%+案例，100%权重）
        self.validated_factor_calculator: Optional[ValidatedFactorCalculator] = None
        try:
            self.validated_factor_calculator = ValidatedFactorCalculator(verbose=False)
        except Exception as e:
            logger.warning(f"ValidatedFactorCalculator初始化失败: {e}")
    
    def set_factor_config(
        self,
        factor_selection: Optional[List[str]] = None,
        factor_weights: Optional[Dict[str, float]] = None,
    ):
        """设置因子选择和权重配置"""
        self._factor_selection = factor_selection
        self._factor_weights = factor_weights
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            self.jq = jq
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
    
    def calculate_fundamental_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算基本面因子"""
        q = self.jq.query(
            self.jq.valuation.code,
            self.jq.valuation.market_cap,
            self.jq.valuation.pe_ratio,
            self.jq.valuation.pb_ratio,
            self.jq.valuation.ps_ratio,
            self.jq.indicator.roe,
            self.jq.indicator.inc_net_profit_year_on_year,
            self.jq.indicator.inc_revenue_year_on_year,
            self.jq.indicator.gross_profit_margin,
        ).filter(
            self.jq.valuation.code.in_(codes)
        )
        
        df = self.jq.get_fundamentals(q, date=date)
        if df is None or df.empty:
            return pd.DataFrame({'code': codes})
        
        # 计算PEG
        df['peg'] = df['pe_ratio'] / df['inc_net_profit_year_on_year'].replace(0, np.nan)
        df['peg'] = df['peg'].clip(-10, 10)
        
        # 标准化评分（百分位排名）
        df['roe_score'] = df['roe'].clip(-20, 50).rank(pct=True) * 100
        df['growth_score'] = df['inc_net_profit_year_on_year'].clip(-100, 500).rank(pct=True) * 100
        df['revenue_growth_score'] = df['inc_revenue_year_on_year'].clip(-50, 200).rank(pct=True) * 100
        df['peg_score'] = (2 - df['peg'].clip(0, 2)).rank(pct=True) * 100
        df['gross_margin_score'] = df['gross_profit_margin'].clip(0, 80).rank(pct=True) * 100
        
        # 综合基本面得分
        weights = self.config.fundamental_weights
        df['fundamental_score'] = (
            df['roe_score'] * weights.get('roe', 0.25) +
            df['growth_score'] * weights.get('growth', 0.30) +
            df['revenue_growth_score'] * weights.get('revenue_growth', 0.20) +
            df['peg_score'] * weights.get('peg', 0.15) +
            df['gross_margin_score'] * weights.get('gross_margin', 0.10)
        )
        
        return df
    
    def calculate_technical_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算技术面因子"""
        start_dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=60)
        
        prices = self.jq.get_price(
            codes,
            start_date=start_dt.strftime('%Y-%m-%d'),
            end_date=date,
            frequency='daily',
            fields=['close', 'high', 'low', 'volume', 'money'],
            panel=False,
            skip_paused=True,
            fq='post'
        )
        
        if prices is None or prices.empty:
            return pd.DataFrame({'code': codes})
        
        results = []
        for code in codes:
            code_df = prices[prices['code'] == code].reset_index(drop=True)
            if len(code_df) < 20:
                results.append({'code': code})
                continue
            
            close = code_df['close']
            high = code_df['high']
            low = code_df['low']
            volume = code_df['volume']
            money = code_df['money']
            
            result = {'code': code}
            
            # 动量
            result['momentum_5d'] = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
            result['momentum_10d'] = (close.iloc[-1] / close.iloc[-10] - 1) * 100 if len(close) >= 10 else 0
            result['momentum_20d'] = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
            
            # 相对位置
            high_20 = high.tail(20).max()
            low_20 = low.tail(20).min()
            result['rel_strength'] = (close.iloc[-1] - low_20) / (high_20 - low_20) * 100 if high_20 != low_20 else 50
            
            # RSI
            delta = close.diff()
            gain = delta.where(delta > 0, 0).tail(14).mean()
            loss = (-delta.where(delta < 0, 0)).tail(14).mean()
            result['rsi'] = 100 - (100 / (1 + gain / loss)) if loss != 0 else 50
            
            # 量比
            avg_vol_5 = volume.tail(5).mean()
            avg_vol_20 = volume.tail(20).mean()
            result['volume_ratio'] = avg_vol_5 / avg_vol_20 if avg_vol_20 > 0 else 1
            
            # 流动性
            result['avg_money'] = money.tail(5).mean() / 10000  # 万元
            
            # 波动率
            returns = close.pct_change().dropna()
            result['volatility'] = returns.tail(20).std() * np.sqrt(252) * 100
            
            # 突破信号
            high_60 = high.max()
            result['near_high'] = 1 if close.iloc[-1] >= high_60 * 0.95 else 0
            
            results.append(result)
        
        df = pd.DataFrame(results)
        
        # 技术面评分
        # 动量：适度最佳（5~25%）
        df['momentum_5d_score'] = 100 - np.abs(df.get('momentum_5d', 0) - 5).clip(0, 30) * 3
        df['momentum_10d_score'] = 100 - np.abs(df.get('momentum_10d', 0) - 10).clip(0, 40) * 2.5
        df['momentum_20d_score'] = 100 - np.abs(df.get('momentum_20d', 0) - 15).clip(0, 50) * 2
        
        # 相对位置：中低位（30-60%）最佳
        df['rel_strength_score'] = 100 - np.abs(df.get('rel_strength', 50) - 45).clip(0, 50) * 2
        
        # RSI：40-60最佳
        df['rsi_score'] = 100 - np.abs(df.get('rsi', 50) - 50).clip(0, 30) * 3
        
        # 量比
        df['volume_ratio_score'] = df.get('volume_ratio', 1).clip(0.5, 3).rank(pct=True) * 100
        
        # 综合技术面得分
        weights = self.config.technical_weights
        df['technical_score'] = (
            df.get('momentum_5d_score', 50) * weights.get('momentum_5d', 0.15) +
            df.get('momentum_10d_score', 50) * weights.get('momentum_10d', 0.20) +
            df.get('momentum_20d_score', 50) * weights.get('momentum_20d', 0.25) +
            df.get('rel_strength_score', 50) * weights.get('rel_strength', 0.20) +
            df.get('rsi_score', 50) * weights.get('rsi', 0.10) +
            df.get('volume_ratio_score', 50) * weights.get('volume_ratio', 0.10)
        )
        
        return df
    
    def calculate_capital_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算资金面因子"""
        results = []
        
        # 融资融券
        try:
            mtss_start = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=10)
            mtss = self.jq.get_mtss(codes, start_date=mtss_start.strftime('%Y-%m-%d'), end_date=date)
        except:
            mtss = None
        
        # 龙虎榜
        try:
            billboard = self.jq.get_billboard_list(stock_list=codes, end_date=date, count=10)
        except:
            billboard = None
        
        # 换手率
        try:
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.turnover_ratio,
            ).filter(
                self.jq.valuation.code.in_(codes)
            )
            turnover_df = self.jq.get_fundamentals(q, date=date)
        except:
            turnover_df = None
        
        for code in codes:
            result = {'code': code}
            
            # 融资余额变化
            if mtss is not None and not mtss.empty:
                code_mtss = mtss[mtss['sec_code'] == code]
                if len(code_mtss) >= 2:
                    result['fin_change'] = (code_mtss['fin_value'].iloc[-1] / code_mtss['fin_value'].iloc[0] - 1) * 100
                else:
                    result['fin_change'] = 0
            else:
                result['fin_change'] = 0
            
            # 龙虎榜
            if billboard is not None and not billboard.empty:
                code_bill = billboard[billboard['code'] == code]
                result['on_billboard'] = 1 if len(code_bill) > 0 else 0
                result['billboard_count'] = len(code_bill)
            else:
                result['on_billboard'] = 0
                result['billboard_count'] = 0
            
            # 换手率
            if turnover_df is not None and not turnover_df.empty:
                code_turnover = turnover_df[turnover_df['code'] == code]
                if not code_turnover.empty:
                    result['turnover_rate'] = code_turnover['turnover_ratio'].iloc[0]
                else:
                    result['turnover_rate'] = 0
            else:
                result['turnover_rate'] = 0
            
            results.append(result)
        
        df = pd.DataFrame(results)
        
        # 资金面评分
        df['fin_change_score'] = df['fin_change'].clip(-20, 20).rank(pct=True) * 100
        df['turnover_rate_score'] = df['turnover_rate'].clip(0, 20).rank(pct=True) * 100
        df['billboard_score'] = df['on_billboard'] * 50 + df['billboard_count'].clip(0, 5) * 10
        
        # 综合资金面得分
        weights = self.config.capital_weights
        df['capital_score'] = (
            df['fin_change_score'] * weights.get('fin_change', 0.40) +
            df['turnover_rate_score'] * weights.get('turnover_rate', 0.30) +
            df['billboard_score'] * weights.get('on_billboard', 0.30)
        )
        
        return df
    
    def calculate_sentiment_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算情绪/事件因子"""
        results = []
        
        for code in codes:
            result = {'code': code}
            
            # 概念数量
            try:
                concepts = self.jq.get_concept(code, date)
                result['concept_count'] = len(concepts) if concepts is not None else 0
            except:
                result['concept_count'] = 0
            
            # 行业
            try:
                industry = self.jq.get_industry(code, date)
                result['industry'] = list(industry.get(code, {}).get('sw_l1', {}).values())[0] if industry else '未知'
            except:
                result['industry'] = '未知'
            
            results.append(result)
        
        df = pd.DataFrame(results)
        
        # 情绪评分
        df['concept_score'] = df['concept_count'].clip(0, 20).rank(pct=True) * 100
        
        # 行业热度（简化：概念多的行业热度高）
        if 'industry' in df.columns:
            industry_counts = df.groupby('industry')['concept_count'].mean()
            df['industry_hot_score'] = df['industry'].map(industry_counts).rank(pct=True) * 100
        else:
            df['industry_hot_score'] = 50
        
        # 综合情绪得分
        weights = self.config.sentiment_weights
        df['sentiment_score'] = (
            df['concept_score'] * weights.get('concept_count', 0.50) +
            df.get('industry_hot_score', 50) * weights.get('industry_hot', 0.50)
        )
        
        return df
    
    def calculate_market_env_factors(self, date: str) -> Dict:
        """计算市场环境因子"""
        result = {
            'date': date,
            'market_trend': 0,
            'market_trend_score': 50,
        }
        
        try:
            # 沪深300趋势
            prices = self.jq.get_price(
                '000300.XSHG',
                end_date=date,
                count=20,
                frequency='daily',
                fields=['close'],
                fq='post'
            )
            
            if prices is not None and len(prices) >= 20:
                result['market_trend'] = (prices['close'].iloc[-1] / prices['close'].iloc[0] - 1) * 100
                
                # 市场环境评分
                if result['market_trend'] > 5:
                    result['market_trend_score'] = 80  # 牛市
                elif result['market_trend'] > 0:
                    result['market_trend_score'] = 60  # 弱势上涨
                elif result['market_trend'] > -5:
                    result['market_trend_score'] = 40  # 弱势下跌
                else:
                    result['market_trend_score'] = 20  # 熊市
        except:
            pass
        
        return result
    
    def calculate_all_factors(self, codes: List[str], date: str) -> pd.DataFrame:
        """计算所有维度因子并综合打分"""
        if self.verbose:
            print(f"\n计算 {len(codes)} 只股票的多维因子 @ {date}")
        
        # 分批处理避免超时
        batch_size = 100
        all_results = []
        
        for i in range(0, len(codes), batch_size):
            batch_codes = codes[i:i+batch_size]
            
            # 计算各维度因子
            fundamental_df = self.calculate_fundamental_factors(batch_codes, date)
            technical_df = self.calculate_technical_factors(batch_codes, date)
            capital_df = self.calculate_capital_factors(batch_codes, date)
            sentiment_df = self.calculate_sentiment_factors(batch_codes, date)
            market_env = self.calculate_market_env_factors(date)
            
            # 合并
            df = fundamental_df[['code', 'market_cap', 'roe', 'inc_net_profit_year_on_year', 'fundamental_score']].copy()
            df = df.rename(columns={'inc_net_profit_year_on_year': 'growth'})
            
            tech_cols = ['code', 'momentum_5d', 'momentum_10d', 'momentum_20d', 'rel_strength', 
                        'rsi', 'volume_ratio', 'avg_money', 'technical_score']
            tech_cols = [c for c in tech_cols if c in technical_df.columns]
            df = df.merge(technical_df[tech_cols], on='code', how='left')
            
            cap_cols = ['code', 'fin_change', 'turnover_rate', 'on_billboard', 'capital_score']
            cap_cols = [c for c in cap_cols if c in capital_df.columns]
            df = df.merge(capital_df[cap_cols], on='code', how='left')
            
            sent_cols = ['code', 'concept_count', 'industry', 'sentiment_score']
            sent_cols = [c for c in sent_cols if c in sentiment_df.columns]
            df = df.merge(sentiment_df[sent_cols], on='code', how='left')
            
            # 市场环境因子
            df['market_trend'] = market_env['market_trend']
            df['market_env_score'] = market_env['market_trend_score']
            
            all_results.append(df)
        
        result_df = pd.concat(all_results, ignore_index=True)
        
        # 填充缺失值
        score_cols = ['fundamental_score', 'technical_score', 'capital_score', 'sentiment_score', 'market_env_score']
        for col in score_cols:
            if col in result_df.columns:
                result_df[col] = result_df[col].fillna(50)
        
        # 计算旧版综合得分（保留作为参考，但不作为最终得分）
        dim_weights = self.config.dimension_weights
        result_df['legacy_total_score'] = (
            result_df.get('fundamental_score', 50) * dim_weights.get('fundamental', 0.15) +
            result_df.get('technical_score', 50) * dim_weights.get('technical', 0.35) +
            result_df.get('capital_score', 50) * dim_weights.get('capital', 0.25) +
            result_df.get('sentiment_score', 50) * dim_weights.get('sentiment', 0.15) +
            result_df.get('market_env_score', 50) * dim_weights.get('market_env', 0.10)
        )

        # 使用已验证因子得分（100%权重，基于历史10%+案例）
        if self.validated_factor_calculator is not None:
            try:
                validated_df = self.validated_factor_calculator.calculate_all_validated_factors(
                    codes,
                    date,
                    factor_selection=self._factor_selection,
                    factor_weights=self._factor_weights,
                )
                if not validated_df.empty and 'validated_score' in validated_df.columns:
                    # 合并已验证因子得分
                    result_df = result_df.merge(
                        validated_df[['code', 'validated_score']],
                        on='code',
                        how='left'
                    )
                    # total_score直接等于validated_score（100%已验证因子）
                    result_df['total_score'] = result_df['validated_score'].fillna(0).clip(0, 100)
                    if self.verbose:
                        print(f"✅ 使用已验证因子得分（100%权重，7因子完整组合）")
                else:
                    # 如果没有计算出validated_score，使用legacy_total_score作为兜底
                    result_df['total_score'] = result_df['legacy_total_score']
                    logger.warning(f"已验证因子计算返回空结果，使用legacy_total_score作为兜底@{date}")
            except Exception as e:
                logger.warning(f"已验证因子计算失败，使用legacy_total_score作为兜底@{date}: {e}")
                # 回退到legacy_total_score
                result_df['total_score'] = result_df['legacy_total_score']
        else:
            # 如果没有已验证因子计算器，使用legacy_total_score
            result_df['total_score'] = result_df['legacy_total_score']
            logger.warning("ValidatedFactorCalculator未初始化，使用legacy_total_score")
        
        return result_df


def main():
    """测试多维因子计算"""
    calculator = MultiFactorCalculator()
    
    # 测试股票
    test_codes = ['000001.XSHE', '000002.XSHE', '600000.XSHG', '600036.XSHG']
    
    df = calculator.calculate_all_factors(test_codes, '2025-12-20')
    print(df)


if __name__ == '__main__':
    main()
