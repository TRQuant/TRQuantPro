# -*- coding: utf-8 -*-
"""
价值因子模块
============

包含以下因子：
- EP (盈利收益率): 净利润TTM / 市值
- BP (账面市值比): 净资产 / 市值
- SP (营收收益率): 营业收入TTM / 市值
- DividendYield (股息率): 每股股息 / 股价

A股特点：
- 价值因子在熊市和震荡市表现较好
- 需要剔除ST、*ST股票
- 银行等金融股PB需要单独处理
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime
import logging

from .base_factor import BaseFactor

logger = logging.getLogger(__name__)


class EPFactor(BaseFactor):
    """
    盈利收益率因子 (Earnings-to-Price)
    
    公式: EP = 净利润TTM / 市值
    
    经济学逻辑：
    - EP是PE的倒数，便于处理负值
    - 高EP表示估值便宜，预期收益高
    
    A股实证：
    - IC均值约0.03，在中小盘股更有效
    - 与成长因子负相关
    """
    
    name = "EP"
    category = "value"
    description = "盈利收益率因子"
    direction = 1  # 越大越好
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算EP因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算EP因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            # 查询估值数据
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.market_cap
            ).filter(
                valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 计算EP = 1/PE
            # 处理负PE和极端值
            df['EP'] = np.where(
                (df['pe_ratio'] > 0) & (df['pe_ratio'] < 500),
                1.0 / df['pe_ratio'],
                np.nan
            )
            
            result = df.set_index('code')['EP']
            
            # 确保所有股票都有值
            result = result.reindex(stocks)
            
            logger.info(f"EP因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"EP因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        """生成PTrade代码"""
        return '''
# EP因子 - 盈利收益率
def calculate_ep_factor(stocks, date):
    """
    计算EP因子
    
    Args:
        stocks: 股票列表
        date: 计算日期
    
    Returns:
        pd.Series: EP因子值
    """
    from jqdatasdk import query, valuation, get_fundamentals
    import numpy as np
    
    q = query(
        valuation.code,
        valuation.pe_ratio
    ).filter(valuation.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    # EP = 1/PE，处理异常值
    df['EP'] = np.where(
        (df['pe_ratio'] > 0) & (df['pe_ratio'] < 500),
        1.0 / df['pe_ratio'],
        np.nan
    )
    
    return df.set_index('code')['EP']
'''


class BPFactor(BaseFactor):
    """
    账面市值比因子 (Book-to-Price)
    
    公式: BP = 净资产 / 市值 = 1/PB
    
    经济学逻辑：
    - 高BP表示股价相对净资产便宜
    - 是价值投资的核心指标
    
    A股实证：
    - 在周期性行业效果较好
    - 银行股PB普遍较低，需要行业中性化
    """
    
    name = "BP"
    category = "value"
    description = "账面市值比因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算BP因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算BP因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pb_ratio
            ).filter(
                valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # BP = 1/PB
            df['BP'] = np.where(
                (df['pb_ratio'] > 0) & (df['pb_ratio'] < 50),
                1.0 / df['pb_ratio'],
                np.nan
            )
            
            result = df.set_index('code')['BP']
            result = result.reindex(stocks)
            
            logger.info(f"BP因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"BP因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)
    
    def get_ptrade_code(self) -> str:
        return '''
# BP因子 - 账面市值比
def calculate_bp_factor(stocks, date):
    """计算BP因子"""
    from jqdatasdk import query, valuation, get_fundamentals
    import numpy as np
    
    q = query(
        valuation.code,
        valuation.pb_ratio
    ).filter(valuation.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    df['BP'] = np.where(
        (df['pb_ratio'] > 0) & (df['pb_ratio'] < 50),
        1.0 / df['pb_ratio'],
        np.nan
    )
    
    return df.set_index('code')['BP']
'''


class SPFactor(BaseFactor):
    """
    营收收益率因子 (Sales-to-Price)
    
    公式: SP = 营业收入TTM / 市值 = 1/PS
    
    经济学逻辑：
    - 适用于亏损但有收入的公司
    - 对于互联网、科技公司更有意义
    
    A股实证：
    - 在成长股中效果较差
    - 适合周期股估值
    """
    
    name = "SP"
    category = "value"
    description = "营收收益率因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算SP因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算SP因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.ps_ratio
            ).filter(
                valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # SP = 1/PS
            df['SP'] = np.where(
                (df['ps_ratio'] > 0) & (df['ps_ratio'] < 100),
                1.0 / df['ps_ratio'],
                np.nan
            )
            
            result = df.set_index('code')['SP']
            result = result.reindex(stocks)
            
            logger.info(f"SP因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"SP因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class DividendYieldFactor(BaseFactor):
    """
    股息率因子
    
    公式: DY = 每股股息 / 股价
    
    经济学逻辑：
    - 高股息率表示现金回报高
    - 适合稳健型投资者
    
    A股实证：
    - 在银行、公用事业等行业效果好
    - 需要注意股息的可持续性
    """
    
    name = "DividendYield"
    category = "value"
    description = "股息率因子"
    direction = 1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算股息率因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端来计算股息率因子")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            q = query(
                indicator.code,
                indicator.eps,  # 每股收益
            ).filter(
                indicator.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 获取股价
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=1,
                fields=['close'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            price_dict = prices.groupby('code')['close'].last().to_dict()
            
            # 假设分红率为30%（可以调整或从实际数据获取）
            dividend_ratio = 0.3
            
            df['price'] = df['code'].map(price_dict)
            df['DY'] = np.where(
                (df['eps'] > 0) & (df['price'] > 0),
                (df['eps'] * dividend_ratio) / df['price'],
                np.nan
            )
            
            result = df.set_index('code')['DY']
            result = result.reindex(stocks)
            
            logger.info(f"股息率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"股息率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class CompositeValueFactor(BaseFactor):
    """
    复合价值因子
    
    综合EP、BP、SP、DY四个因子，采用等权或优化权重组合。
    
    组合方法：
    1. 各因子标准化
    2. 等权平均或IC加权
    3. 再次标准化
    """
    
    name = "CompositeValue"
    category = "value"
    description = "复合价值因子"
    direction = 1
    
    def __init__(self, jq_client=None, weights: Optional[dict] = None, **kwargs):
        """
        初始化
        
        Args:
            weights: 因子权重，如 {'EP': 0.3, 'BP': 0.3, 'SP': 0.2, 'DY': 0.2}
        """
        super().__init__(jq_client=jq_client, **kwargs)
        self.weights = weights or {'EP': 0.25, 'BP': 0.25, 'SP': 0.25, 'DY': 0.25}
        
        # 子因子
        self.ep_factor = EPFactor(jq_client=jq_client, **kwargs)
        self.bp_factor = BPFactor(jq_client=jq_client, **kwargs)
        self.sp_factor = SPFactor(jq_client=jq_client, **kwargs)
        self.dy_factor = DividendYieldFactor(jq_client=jq_client, **kwargs)
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算复合价值因子"""
        # 计算各子因子
        factors = {}
        
        if self.weights.get('EP', 0) > 0:
            factors['EP'] = self.ep_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('BP', 0) > 0:
            factors['BP'] = self.bp_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('SP', 0) > 0:
            factors['SP'] = self.sp_factor.calculate(stocks, date, **kwargs).values
        
        if self.weights.get('DY', 0) > 0:
            factors['DY'] = self.dy_factor.calculate(stocks, date, **kwargs).values
        
        # 组合因子
        df = pd.DataFrame(factors)
        
        # 加权平均
        composite = pd.Series(0, index=df.index)
        total_weight = 0
        
        for name, weight in self.weights.items():
            if name in df.columns:
                # 填充缺失值为0（不影响其他因子）
                factor_values = df[name].fillna(0)
                composite += factor_values * weight
                total_weight += weight
        
        if total_weight > 0:
            composite /= total_weight
        
        # 重新索引
        composite.index = stocks
        
        logger.info(f"复合价值因子计算完成: 有效值 {composite.notna().sum()}/{len(stocks)}")
        return composite
    
    def get_ptrade_code(self) -> str:
        return '''
# 复合价值因子
def calculate_composite_value_factor(stocks, date, weights=None):
    """
    计算复合价值因子
    
    Args:
        stocks: 股票列表
        date: 计算日期
        weights: 因子权重
    """
    if weights is None:
        weights = {'EP': 0.25, 'BP': 0.25, 'SP': 0.25, 'DY': 0.25}
    
    # 计算各子因子
    ep = calculate_ep_factor(stocks, date)
    bp = calculate_bp_factor(stocks, date)
    sp = calculate_sp_factor(stocks, date)
    dy = calculate_dy_factor(stocks, date)
    
    # 标准化
    def zscore(s):
        return (s - s.mean()) / s.std() if s.std() > 0 else s - s.mean()
    
    # 加权组合
    composite = (
        zscore(ep.fillna(0)) * weights['EP'] +
        zscore(bp.fillna(0)) * weights['BP'] +
        zscore(sp.fillna(0)) * weights['SP'] +
        zscore(dy.fillna(0)) * weights['DY']
    )
    
    return zscore(composite)
'''

