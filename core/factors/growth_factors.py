# -*- coding: utf-8 -*-
"""
成长因子模块
============

包含以下因子：
- RevenueGrowth (营收增速): 营业收入同比增速
- ProfitGrowth (利润增速): 净利润同比增速
- ROEChange (ROE变化): ROE同比变化

A股特点：
- 成长因子在牛市表现突出
- 需要关注增长的质量和可持续性
- 分析师预期修正是重要的前瞻性指标
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime
import logging

from .base_factor import BaseFactor

logger = logging.getLogger(__name__)


class RevenueGrowthFactor(BaseFactor):
    """
    营收增速因子
    
    公式: 营收增速 = (营收_t - 营收_t-1) / |营收_t-1|
    
    经济学逻辑：
    - 营收增长反映业务规模扩张
    - 是最基础的成长性指标
    
    A股实证：
    - IC约0.025，在成长股中更有效
    - 需要结合毛利率判断增长质量
    """
    
    name = "RevenueGrowth"
    category = "growth"
    description = "营收增速因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算营收增速因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算营收增速因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            q = query(
                indicator.code,
                indicator.inc_revenue_year_on_year  # 营收同比增速
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 处理极端值：限制在-100%到500%之间
            df['RevenueGrowth'] = df['inc_revenue_year_on_year'].clip(-100, 500)
            
            result = df.set_index('code')['RevenueGrowth']
            result = result.reindex(stocks)
            
            logger.info(f"营收增速因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"营收增速因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# 营收增速因子
def calculate_revenue_growth_factor(stocks, date):
    """计算营收增速因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    
    q = query(
        indicator.code,
        indicator.inc_revenue_year_on_year
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    # 限制极端值
    df['RevenueGrowth'] = df['inc_revenue_year_on_year'].clip(-100, 500)
    
    return df.set_index('code')['RevenueGrowth']
'''


class ProfitGrowthFactor(BaseFactor):
    """
    利润增速因子
    
    公式: 利润增速 = (净利润_t - 净利润_t-1) / |净利润_t-1|
    
    经济学逻辑：
    - 利润增长直接反映盈利能力提升
    - 是投资者最关注的指标之一
    
    A股实证：
    - IC约0.035，效果稳定
    - 扣非净利润增速更能反映主业情况
    """
    
    name = "ProfitGrowth"
    category = "growth"
    description = "利润增速因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算利润增速因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算利润增速因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            q = query(
                indicator.code,
                indicator.inc_net_profit_year_on_year  # 净利润同比增速
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 处理极端值
            df['ProfitGrowth'] = df['inc_net_profit_year_on_year'].clip(-100, 500)
            
            result = df.set_index('code')['ProfitGrowth']
            result = result.reindex(stocks)
            
            logger.info(f"利润增速因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"利润增速因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# 利润增速因子
def calculate_profit_growth_factor(stocks, date):
    """计算利润增速因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    
    q = query(
        indicator.code,
        indicator.inc_net_profit_year_on_year
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    df['ProfitGrowth'] = df['inc_net_profit_year_on_year'].clip(-100, 500)
    
    return df.set_index('code')['ProfitGrowth']
'''


class ROEChangeFactor(BaseFactor):
    """
    ROE变化因子
    
    公式: ROE变化 = ROE_t - ROE_t-1
    
    经济学逻辑：
    - ROE提升表示盈利能力改善
    - 是杜邦分析的核心指标
    
    A股实证：
    - 在价值股中效果较好
    - 需要结合杠杆变化判断
    """
    
    name = "ROEChange"
    category = "growth"
    description = "ROE变化因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算ROE变化因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算ROE变化因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            from datetime import timedelta
            
            # 获取当前ROE
            q = query(
                indicator.code,
                indicator.roe
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df_current = jq.get_fundamentals(q, date=date)
            
            if df_current.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 获取一年前的ROE
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            date_1y_ago = date - timedelta(days=365)
            
            df_1y_ago = jq.get_fundamentals(q, date=date_1y_ago)
            
            # 合并计算变化
            df_current = df_current.set_index('code')
            df_1y_ago = df_1y_ago.set_index('code')
            
            roe_change = df_current['roe'] - df_1y_ago['roe'].reindex(df_current.index)
            
            # 处理极端值
            roe_change = roe_change.clip(-50, 50)
            
            result = roe_change.reindex(stocks)
            
            logger.info(f"ROE变化因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"ROE变化因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# ROE变化因子
def calculate_roe_change_factor(stocks, date):
    """计算ROE变化因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    from datetime import datetime, timedelta
    
    q = query(
        indicator.code,
        indicator.roe
    ).filter(indicator.code.in_(stocks))
    
    # 当前ROE
    df_current = get_fundamentals(q, date=date)
    
    # 一年前ROE
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    date_1y_ago = date - timedelta(days=365)
    df_1y_ago = get_fundamentals(q, date=date_1y_ago)
    
    # 计算变化
    df_current = df_current.set_index('code')
    df_1y_ago = df_1y_ago.set_index('code')
    
    roe_change = df_current['roe'] - df_1y_ago['roe'].reindex(df_current.index)
    
    return roe_change.clip(-50, 50)
'''


class CompositeGrowthFactor(BaseFactor):
    """
    复合成长因子
    
    综合营收增速、利润增速、ROE变化三个因子。
    """
    
    name = "CompositeGrowth"
    category = "growth"
    description = "复合成长因子"
    direction = 1
    
    def __init__(self, jq_client=None, weights: Optional[dict] = None, **kwargs):
        """
        初始化
        
        Args:
            weights: 因子权重
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.weights = weights or {
            'RevenueGrowth': 0.3,
            'ProfitGrowth': 0.4,
            'ROEChange': 0.3
        }
        
        self.revenue_factor = RevenueGrowthFactor(jq_client=jq_client, **kwargs)
        self.profit_factor = ProfitGrowthFactor(jq_client=jq_client, **kwargs)
        self.roe_change_factor = ROEChangeFactor(jq_client=jq_client, **kwargs)
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算复合成长因子"""
        factors = {}
        
        if self.weights.get('RevenueGrowth', 0) > 0:
            factors['RevenueGrowth'] = self.revenue_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('ProfitGrowth', 0) > 0:
            factors['ProfitGrowth'] = self.profit_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('ROEChange', 0) > 0:
            factors['ROEChange'] = self.roe_change_factor.calculate(stocks, date, **kwargs).values
        
        df = pd.DataFrame(factors)
        
        # 加权平均
        composite = pd.Series(0, index=df.index)
        total_weight = 0
        
        for name, weight in self.weights.items():
            if name in df.columns:
                factor_values = df[name].fillna(0)
                composite += factor_values * weight
                total_weight += weight
        
        if total_weight > 0:
            composite /= total_weight
        
        composite.index = stocks
        
        logger.info(f"复合成长因子计算完成: 有效值 {composite.notna().sum()}/{len(stocks)}")
        return composite
    
    def get_ptrade_code(self) -> str:
        return '''
# 复合成长因子
def calculate_composite_growth_factor(stocks, date, weights=None):
    """计算复合成长因子"""
    if weights is None:
        weights = {'RevenueGrowth': 0.3, 'ProfitGrowth': 0.4, 'ROEChange': 0.3}
    
    revenue = calculate_revenue_growth_factor(stocks, date)
    profit = calculate_profit_growth_factor(stocks, date)
    roe_change = calculate_roe_change_factor(stocks, date)
    
    def zscore(s):
        return (s - s.mean()) / s.std() if s.std() > 0 else s - s.mean()
    
    composite = (
        zscore(revenue.fillna(0)) * weights['RevenueGrowth'] +
        zscore(profit.fillna(0)) * weights['ProfitGrowth'] +
        zscore(roe_change.fillna(0)) * weights['ROEChange']
    )
    
    return zscore(composite)
'''

