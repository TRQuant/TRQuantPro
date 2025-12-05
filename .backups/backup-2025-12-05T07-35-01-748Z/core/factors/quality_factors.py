# -*- coding: utf-8 -*-
"""
质量因子模块
============

包含以下因子：
- ROE: 净资产收益率
- GrossMargin: 毛利率
- AssetTurnover: 资产周转率
- Leverage: 杠杆率（负向）

A股特点：
- 质量因子在熊市表现出色
- 高质量公司长期跑赢市场
- 需要关注盈利质量而非仅看数字
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime
import logging

from .base_factor import BaseFactor

logger = logging.getLogger(__name__)


class ROEFactor(BaseFactor):
    """
    ROE因子 (Return on Equity)
    
    公式: ROE = 净利润 / 净资产
    
    经济学逻辑：
    - ROE是衡量股东回报的核心指标
    - 高ROE表示公司盈利能力强
    
    A股实证：
    - IC约0.038，是最有效的质量因子之一
    - 长期稳定的高ROE公司更有价值
    """
    
    name = "ROE"
    category = "quality"
    description = "净资产收益率因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算ROE因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算ROE因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            q = query(
                indicator.code,
                indicator.roe
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # ROE一般在0-50%之间，超出可能是异常
            df['ROE'] = df['roe'].clip(-20, 50)
            
            result = df.set_index('code')['ROE']
            result = result.reindex(stocks)
            
            logger.info(f"ROE因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"ROE因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# ROE因子
def calculate_roe_factor(stocks, date):
    """计算ROE因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    
    q = query(
        indicator.code,
        indicator.roe
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    df['ROE'] = df['roe'].clip(-20, 50)
    
    return df.set_index('code')['ROE']
'''


class GrossMarginFactor(BaseFactor):
    """
    毛利率因子
    
    公式: 毛利率 = (营业收入 - 营业成本) / 营业收入
    
    经济学逻辑：
    - 毛利率反映产品定价能力和成本控制
    - 高毛利率通常意味着竞争优势
    
    A股实证：
    - 在消费、医药行业效果好
    - 需要行业内比较
    """
    
    name = "GrossMargin"
    category = "quality"
    description = "毛利率因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算毛利率因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算毛利率因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            q = query(
                indicator.code,
                indicator.gross_profit_margin  # 毛利率
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 毛利率在0-100%之间
            df['GrossMargin'] = df['gross_profit_margin'].clip(0, 100)
            
            result = df.set_index('code')['GrossMargin']
            result = result.reindex(stocks)
            
            logger.info(f"毛利率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"毛利率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# 毛利率因子
def calculate_gross_margin_factor(stocks, date):
    """计算毛利率因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    
    q = query(
        indicator.code,
        indicator.gross_profit_margin
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    df['GrossMargin'] = df['gross_profit_margin'].clip(0, 100)
    
    return df.set_index('code')['GrossMargin']
'''


class AssetTurnoverFactor(BaseFactor):
    """
    资产周转率因子
    
    公式: 资产周转率 = 营业收入 / 总资产
    
    经济学逻辑：
    - 反映资产使用效率
    - 高周转率表示资产利用充分
    
    A股实证：
    - 在零售、制造业中效果好
    - 是杜邦分析的重要组成部分
    """
    
    name = "AssetTurnover"
    category = "quality"
    description = "资产周转率因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算资产周转率因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算资产周转率因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, income, balance
            
            # 获取营业收入
            q_income = query(
                income.code,
                income.operating_revenue
            ).filter(
                income.code.in_(stocks)
            )
            
            df_income = jq.get_fundamentals(q_income, date=date)
            
            # 获取总资产
            q_balance = query(
                balance.code,
                balance.total_assets
            ).filter(
                balance.code.in_(stocks)
            )
            
            df_balance = jq.get_fundamentals(q_balance, date=date)
            
            if df_income.empty or df_balance.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 合并计算
            df_income = df_income.set_index('code')
            df_balance = df_balance.set_index('code')
            
            turnover = df_income['operating_revenue'] / df_balance['total_assets']
            
            # 处理极端值
            turnover = turnover.clip(0, 5)
            
            result = turnover.reindex(stocks)
            
            logger.info(f"资产周转率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"资产周转率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# 资产周转率因子
def calculate_asset_turnover_factor(stocks, date):
    """计算资产周转率因子"""
    from jqdatasdk import query, income, balance, get_fundamentals
    
    # 营业收入
    q_income = query(
        income.code,
        income.operating_revenue
    ).filter(income.code.in_(stocks))
    df_income = get_fundamentals(q_income, date=date)
    
    # 总资产
    q_balance = query(
        balance.code,
        balance.total_assets
    ).filter(balance.code.in_(stocks))
    df_balance = get_fundamentals(q_balance, date=date)
    
    # 计算周转率
    df_income = df_income.set_index('code')
    df_balance = df_balance.set_index('code')
    
    turnover = df_income['operating_revenue'] / df_balance['total_assets']
    
    return turnover.clip(0, 5)
'''


class LeverageFactor(BaseFactor):
    """
    杠杆因子（负向）
    
    公式: 杠杆 = 总负债 / 总资产
    
    经济学逻辑：
    - 高杠杆增加财务风险
    - 低杠杆公司更稳健
    
    A股实证：
    - 在熊市中低杠杆股票表现更好
    - 银行等金融股杠杆天然较高
    """
    
    name = "Leverage"
    category = "quality"
    description = "杠杆因子（负向）"
    direction = -1  # 越小越好
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算杠杆因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算杠杆因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, balance
            
            q = query(
                balance.code,
                balance.total_liability,
                balance.total_assets
            ).filter(
                balance.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 计算资产负债率
            df['Leverage'] = df['total_liability'] / df['total_assets']
            
            # 处理极端值
            df['Leverage'] = df['Leverage'].clip(0, 1)
            
            result = df.set_index('code')['Leverage']
            result = result.reindex(stocks)
            
            logger.info(f"杠杆因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"杠杆因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# 杠杆因子（负向）
def calculate_leverage_factor(stocks, date):
    """计算杠杆因子"""
    from jqdatasdk import query, balance, get_fundamentals
    
    q = query(
        balance.code,
        balance.total_liability,
        balance.total_assets
    ).filter(balance.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    df['Leverage'] = df['total_liability'] / df['total_assets']
    df['Leverage'] = df['Leverage'].clip(0, 1)
    
    # 注意：杠杆是负向因子，选股时应选择杠杆低的
    return df.set_index('code')['Leverage']
'''


class CompositeQualityFactor(BaseFactor):
    """
    复合质量因子
    
    综合ROE、毛利率、周转率、杠杆四个因子。
    注意：杠杆是负向因子，组合时取负值。
    """
    
    name = "CompositeQuality"
    category = "quality"
    description = "复合质量因子"
    direction = 1
    
    def __init__(self, jq_client=None, weights: Optional[dict] = None, **kwargs):
        """
        初始化
        
        Args:
            weights: 因子权重
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.weights = weights or {
            'ROE': 0.35,
            'GrossMargin': 0.25,
            'AssetTurnover': 0.20,
            'Leverage': 0.20  # 负向因子
        }
        
        self.roe_factor = ROEFactor(jq_client=jq_client, **kwargs)
        self.margin_factor = GrossMarginFactor(jq_client=jq_client, **kwargs)
        self.turnover_factor = AssetTurnoverFactor(jq_client=jq_client, **kwargs)
        self.leverage_factor = LeverageFactor(jq_client=jq_client, **kwargs)
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算复合质量因子"""
        factors = {}
        
        if self.weights.get('ROE', 0) > 0:
            factors['ROE'] = self.roe_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('GrossMargin', 0) > 0:
            factors['GrossMargin'] = self.margin_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('AssetTurnover', 0) > 0:
            factors['AssetTurnover'] = self.turnover_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('Leverage', 0) > 0:
            # 杠杆取负值（低杠杆得分高）
            factors['Leverage'] = -self.leverage_factor.calculate(stocks, date, **kwargs).values
        
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
        
        logger.info(f"复合质量因子计算完成: 有效值 {composite.notna().sum()}/{len(stocks)}")
        return composite
    
    def get_ptrade_code(self) -> str:
        return '''
# 复合质量因子
def calculate_composite_quality_factor(stocks, date, weights=None):
    """计算复合质量因子"""
    if weights is None:
        weights = {'ROE': 0.35, 'GrossMargin': 0.25, 'AssetTurnover': 0.20, 'Leverage': 0.20}
    
    roe = calculate_roe_factor(stocks, date)
    margin = calculate_gross_margin_factor(stocks, date)
    turnover = calculate_asset_turnover_factor(stocks, date)
    leverage = calculate_leverage_factor(stocks, date)
    
    def zscore(s):
        return (s - s.mean()) / s.std() if s.std() > 0 else s - s.mean()
    
    # 杠杆取负值
    composite = (
        zscore(roe.fillna(0)) * weights['ROE'] +
        zscore(margin.fillna(0)) * weights['GrossMargin'] +
        zscore(turnover.fillna(0)) * weights['AssetTurnover'] +
        zscore(-leverage.fillna(0)) * weights['Leverage']
    )
    
    return zscore(composite)
'''

