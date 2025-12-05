# -*- coding: utf-8 -*-
"""
扩展因子模块
============

根据《补充因子构建模块完善建议》，添加以下因子类型：
- 规模因子（Size）：市值因子，小盘股溢价
- 波动率因子（Volatility）：低波动率效应
- 流动性因子（Liquidity）：换手率、成交额
- 情绪因子（Sentiment）：预期调整等（预留）

这些因子常被业界顶尖基金经理使用，可有效分散单一因子失效风险。
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Union
from datetime import datetime, timedelta
import logging

from .base_factor import BaseFactor

logger = logging.getLogger(__name__)


# ====================== 规模因子 ======================

class SizeFactor(BaseFactor):
    """
    规模因子（市值因子）
    
    公式: Size = -log(市值)
    
    经济学逻辑：
    - 小市值股票存在溢价效应
    - Fama-French三因子模型核心因子之一
    
    A股实证：
    - 小盘股溢价在多数年份显著
    - 但需注意流动性风险
    """
    
    name = "Size"
    category = "size"
    description = "规模因子（市值）"
    direction = -1  # 市值越小越好
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算规模因子（负对数市值）"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.market_cap  # 总市值（亿元）
            ).filter(
                valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 负对数市值（市值越小，因子值越大）
            df['size_factor'] = -np.log(df['market_cap'].clip(lower=1))
            
            result = df.set_index('code')['size_factor']
            result = result.reindex(stocks)
            
            logger.info(f"规模因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"规模因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class MarketCapFactor(BaseFactor):
    """
    市值因子（原始市值）
    
    用于市值中性化等处理
    """
    
    name = "MarketCap"
    category = "size"
    description = "市值因子"
    direction = 0  # 无方向
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算对数市值"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.market_cap
            ).filter(
                valuation.code.in_(stocks)
            )
            
            df = jq.get_fundamentals(q, date=date)
            
            if df.empty:
                return pd.Series(index=stocks, dtype=float)
            
            # 对数市值
            df['log_cap'] = np.log(df['market_cap'].clip(lower=1))
            
            result = df.set_index('code')['log_cap']
            return result.reindex(stocks)
            
        except Exception as e:
            logger.error(f"市值因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


# ====================== 波动率因子 ======================

class VolatilityFactor(BaseFactor):
    """
    波动率因子
    
    公式: Volatility = 过去N日收益率标准差
    
    经济学逻辑：
    - 低波动率股票长期表现更好（低波动率异象）
    - 高波动率可能反映投机行为
    
    A股实证：
    - 低波动率效应在A股同样有效
    - 通常采用20-60日窗口
    """
    
    name = "Volatility"
    category = "volatility"
    description = "波动率因子"
    direction = -1  # 波动率越低越好
    
    def __init__(self, jq_client=None, lookback_days: int = 60, **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算波动率因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 获取历史价格
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 5,
                fields=['close'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            volatility_dict = {}
            
            for stock in stocks:
                stock_prices = prices[prices['code'] == stock]['close']
                
                if len(stock_prices) < 20:
                    volatility_dict[stock] = np.nan
                    continue
                
                # 计算日收益率标准差（年化）
                returns = stock_prices.pct_change().dropna()
                vol = returns.std() * np.sqrt(252)  # 年化波动率
                
                # 负号：低波动率得高分
                volatility_dict[stock] = -vol
            
            result = pd.Series(volatility_dict)
            logger.info(f"波动率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"波动率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class BetaFactor(BaseFactor):
    """
    Beta因子
    
    公式: Beta = Cov(股票收益, 市场收益) / Var(市场收益)
    
    经济学逻辑：
    - 低Beta股票在熊市中表现更好
    - Beta套利策略
    """
    
    name = "Beta"
    category = "volatility"
    description = "Beta因子"
    direction = -1  # 低Beta更好
    
    def __init__(self, jq_client=None, lookback_days: int = 120, benchmark: str = '000300.XSHG', **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
        self.benchmark = benchmark
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算Beta因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 获取基准收益
            benchmark_prices = jq.get_price(
                self.benchmark,
                end_date=date,
                count=self.lookback_days + 5,
                fields=['close'],
                panel=False
            )
            
            if benchmark_prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            benchmark_returns = benchmark_prices['close'].pct_change().dropna()
            
            # 获取股票收益
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 5,
                fields=['close'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            beta_dict = {}
            market_var = benchmark_returns.var()
            
            for stock in stocks:
                stock_prices = prices[prices['code'] == stock]['close']
                
                if len(stock_prices) < 60:
                    beta_dict[stock] = np.nan
                    continue
                
                stock_returns = stock_prices.pct_change().dropna()
                
                # 对齐
                common_idx = stock_returns.index.intersection(benchmark_returns.index)
                if len(common_idx) < 30:
                    beta_dict[stock] = np.nan
                    continue
                
                cov = np.cov(stock_returns.loc[common_idx], benchmark_returns.loc[common_idx])[0, 1]
                beta = cov / market_var if market_var > 0 else np.nan
                
                # 负号：低Beta得高分
                beta_dict[stock] = -beta
            
            result = pd.Series(beta_dict)
            logger.info(f"Beta因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"Beta因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


# ====================== 流动性因子 ======================

class TurnoverFactor(BaseFactor):
    """
    换手率因子
    
    公式: Turnover = 过去N日平均换手率
    
    经济学逻辑：
    - 低换手率可能表示机构持仓稳定
    - 高换手率可能反映投机炒作
    
    A股实证：
    - 低换手率效应在A股有效
    - 但需要区分流动性不足和稳定持仓
    """
    
    name = "Turnover"
    category = "liquidity"
    description = "换手率因子"
    direction = -1  # 换手率越低越好
    
    def __init__(self, jq_client=None, lookback_days: int = 20, **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算换手率因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 获取换手率数据
            turnover_data = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days,
                fields=['turnover_ratio'],
                panel=False
            )
            
            if turnover_data.empty:
                return pd.Series(index=stocks, dtype=float)
            
            turnover_dict = {}
            
            for stock in stocks:
                stock_turnover = turnover_data[turnover_data['code'] == stock]['turnover_ratio']
                
                if len(stock_turnover) < 5:
                    turnover_dict[stock] = np.nan
                    continue
                
                avg_turnover = stock_turnover.mean()
                # 负号：低换手率得高分
                turnover_dict[stock] = -avg_turnover
            
            result = pd.Series(turnover_dict)
            logger.info(f"换手率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"换手率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class AmountFactor(BaseFactor):
    """
    成交额因子
    
    公式: Amount = log(过去N日平均成交额)
    
    经济学逻辑：
    - 成交额反映市场关注度
    - 适中的成交额表示流动性良好
    """
    
    name = "Amount"
    category = "liquidity"
    description = "成交额因子"
    direction = 0  # 无明确方向，用于流动性筛选
    
    def __init__(self, jq_client=None, lookback_days: int = 20, **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算成交额因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            # 获取成交额数据
            amount_data = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days,
                fields=['money'],
                panel=False
            )
            
            if amount_data.empty:
                return pd.Series(index=stocks, dtype=float)
            
            amount_dict = {}
            
            for stock in stocks:
                stock_amount = amount_data[amount_data['code'] == stock]['money']
                
                if len(stock_amount) < 5:
                    amount_dict[stock] = np.nan
                    continue
                
                avg_amount = stock_amount.mean()
                # 对数成交额
                amount_dict[stock] = np.log(max(avg_amount, 1))
            
            result = pd.Series(amount_dict)
            logger.info(f"成交额因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"成交额因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


class IlliquidityFactor(BaseFactor):
    """
    非流动性因子（Amihud ILLIQ）
    
    公式: ILLIQ = |日收益率| / 日成交额 的平均值
    
    经济学逻辑：
    - 衡量价格对成交量的敏感度
    - 高ILLIQ表示流动性差
    
    参考：Amihud (2002)
    """
    
    name = "Illiquidity"
    category = "liquidity"
    description = "非流动性因子"
    direction = -1  # 非流动性越低越好
    
    def __init__(self, jq_client=None, lookback_days: int = 20, **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算非流动性因子"""
        if self.jq_client is None:
            raise ValueError("需要JQData客户端")
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d')
            
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 1,
                fields=['close', 'money'],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            illiq_dict = {}
            
            for stock in stocks:
                stock_data = prices[prices['code'] == stock].copy()
                
                if len(stock_data) < 10:
                    illiq_dict[stock] = np.nan
                    continue
                
                stock_data['return'] = stock_data['close'].pct_change().abs()
                stock_data['illiq'] = stock_data['return'] / (stock_data['money'] / 1e8 + 1e-10)
                
                avg_illiq = stock_data['illiq'].dropna().mean()
                # 负号：低非流动性得高分
                illiq_dict[stock] = -np.log(avg_illiq + 1e-10)
            
            result = pd.Series(illiq_dict)
            logger.info(f"非流动性因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
            
        except Exception as e:
            logger.error(f"非流动性因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)


# ====================== 综合因子 ======================

class CompositeSizeFactor(BaseFactor):
    """综合规模因子"""
    
    name = "CompositeSize"
    category = "size"
    description = "综合规模因子"
    direction = -1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算综合规模因子（等权组合）"""
        size = SizeFactor(jq_client=self.jq_client).calculate_raw(stocks, date)
        return size  # 目前只有一个规模因子


class CompositeVolatilityFactor(BaseFactor):
    """综合波动率因子"""
    
    name = "CompositeVolatility"
    category = "volatility"
    description = "综合波动率因子"
    direction = -1
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算综合波动率因子"""
        vol = VolatilityFactor(jq_client=self.jq_client).calculate_raw(stocks, date)
        beta = BetaFactor(jq_client=self.jq_client).calculate_raw(stocks, date)
        
        # 等权组合
        combined = (vol.fillna(0) + beta.fillna(0)) / 2
        return combined


class CompositeLiquidityFactor(BaseFactor):
    """综合流动性因子"""
    
    name = "CompositeLiquidity"
    category = "liquidity"
    description = "综合流动性因子"
    direction = 0
    
    def calculate_raw(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        **kwargs
    ) -> pd.Series:
        """计算综合流动性因子"""
        turnover = TurnoverFactor(jq_client=self.jq_client).calculate_raw(stocks, date)
        illiq = IlliquidityFactor(jq_client=self.jq_client).calculate_raw(stocks, date)
        
        # 等权组合
        combined = (turnover.fillna(0) + illiq.fillna(0)) / 2
        return combined

