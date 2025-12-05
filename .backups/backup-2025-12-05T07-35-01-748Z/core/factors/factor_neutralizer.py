# -*- coding: utf-8 -*-
"""
因子中性化模块
==============

根据《补充因子构建模块完善建议》，实现：
- 行业中性化：剔除行业效应
- 市值中性化：剔除规模效应
- 风格中性化：剔除多种风险因子

方法：
对因子值做截面回归，将行业哑变量和对数市值作为自变量，
因子原始值为因变量，回归残差即为"纯化"因子值。

参考：
- 东方证券报告
- 因子中性化最佳实践
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Union, Tuple
from datetime import datetime
import logging
from sklearn.linear_model import LinearRegression
import warnings

logger = logging.getLogger(__name__)


class FactorNeutralizer:
    """
    因子中性化处理器
    
    支持：
    - 行业中性化
    - 市值中性化
    - 复合中性化（同时剔除行业和市值）
    """
    
    def __init__(self, jq_client=None):
        """
        初始化
        
        Args:
            jq_client: JQData客户端
        """
        self.jq_client = jq_client
        self._industry_cache = {}
        self._market_cap_cache = {}
    
    def neutralize(
        self,
        factor_values: pd.Series,
        stocks: List[str],
        date: Union[str, datetime],
        neutralize_industry: bool = True,
        neutralize_size: bool = True,
        industry_level: str = 'sw_l1'  # 申万一级行业
    ) -> pd.Series:
        """
        因子中性化
        
        Args:
            factor_values: 原始因子值
            stocks: 股票列表
            date: 日期
            neutralize_industry: 是否行业中性化
            neutralize_size: 是否市值中性化
            industry_level: 行业分类级别
        
        Returns:
            pd.Series: 中性化后的因子值
        """
        if not neutralize_industry and not neutralize_size:
            return factor_values
        
        # 获取有效数据
        valid_idx = factor_values.dropna().index
        if len(valid_idx) < 10:
            logger.warning("有效样本过少，跳过中性化")
            return factor_values
        
        y = factor_values.loc[valid_idx].values
        X_list = []
        
        # 行业哑变量
        if neutralize_industry:
            industry_dummies = self._get_industry_dummies(valid_idx.tolist(), date, industry_level)
            if industry_dummies is not None and not industry_dummies.empty:
                X_list.append(industry_dummies.values)
        
        # 对数市值
        if neutralize_size:
            market_cap = self._get_log_market_cap(valid_idx.tolist(), date)
            if market_cap is not None and not market_cap.empty:
                X_list.append(market_cap.values.reshape(-1, 1))
        
        if not X_list:
            logger.warning("无法获取中性化所需数据，跳过中性化")
            return factor_values
        
        # 构建回归矩阵
        X = np.hstack(X_list)
        
        # 处理缺失值
        valid_mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
        if valid_mask.sum() < 10:
            logger.warning("回归有效样本过少，跳过中性化")
            return factor_values
        
        try:
            # 线性回归
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = LinearRegression()
                model.fit(X[valid_mask], y[valid_mask])
            
            # 残差作为中性化因子
            residuals = y.copy()
            residuals[valid_mask] = y[valid_mask] - model.predict(X[valid_mask])
            
            result = pd.Series(residuals, index=valid_idx)
            
            # 重新索引到原始股票列表
            result = result.reindex(factor_values.index)
            
            logger.debug(f"因子中性化完成: {len(valid_idx)}只股票")
            return result
            
        except Exception as e:
            logger.error(f"因子中性化失败: {e}")
            return factor_values
    
    def _get_industry_dummies(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        industry_level: str
    ) -> Optional[pd.DataFrame]:
        """获取行业哑变量矩阵"""
        if self.jq_client is None:
            return None
        
        cache_key = f"{date}_{industry_level}"
        
        try:
            import jqdatasdk as jq
            
            # 获取行业分类
            industries = jq.get_industry(stocks, date=date)
            
            industry_map = {}
            for stock, ind_info in industries.items():
                if industry_level in ind_info:
                    industry_map[stock] = ind_info[industry_level]['industry_code']
                else:
                    industry_map[stock] = 'Unknown'
            
            industry_series = pd.Series(industry_map)
            industry_series = industry_series.reindex(stocks)
            
            # 创建哑变量
            dummies = pd.get_dummies(industry_series, drop_first=True)
            
            return dummies
            
        except Exception as e:
            logger.warning(f"获取行业分类失败: {e}")
            return None
    
    def _get_log_market_cap(
        self,
        stocks: List[str],
        date: Union[str, datetime]
    ) -> Optional[pd.Series]:
        """获取对数市值"""
        if self.jq_client is None:
            return None
        
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
                return None
            
            log_cap = np.log(df.set_index('code')['market_cap'].clip(lower=1))
            log_cap = log_cap.reindex(stocks)
            
            return log_cap
            
        except Exception as e:
            logger.warning(f"获取市值失败: {e}")
            return None
    
    def neutralize_batch(
        self,
        factor_dict: Dict[str, pd.Series],
        stocks: List[str],
        date: Union[str, datetime],
        neutralize_industry: bool = True,
        neutralize_size: bool = True
    ) -> Dict[str, pd.Series]:
        """
        批量因子中性化
        
        Args:
            factor_dict: 因子值字典
            stocks: 股票列表
            date: 日期
            neutralize_industry: 是否行业中性化
            neutralize_size: 是否市值中性化
        
        Returns:
            Dict[str, pd.Series]: 中性化后的因子值字典
        """
        result = {}
        
        for name, values in factor_dict.items():
            result[name] = self.neutralize(
                values, stocks, date,
                neutralize_industry=neutralize_industry,
                neutralize_size=neutralize_size
            )
        
        return result


class FactorCorrelationAnalyzer:
    """
    因子相关性分析器
    
    功能：
    - 计算因子相关性矩阵
    - 检测因子冗余
    - 因子筛选建议
    """
    
    def __init__(self, correlation_threshold: float = 0.7):
        """
        初始化
        
        Args:
            correlation_threshold: 相关性阈值，超过此值认为冗余
        """
        self.correlation_threshold = correlation_threshold
    
    def calculate_correlation_matrix(
        self,
        factor_dict: Dict[str, pd.Series]
    ) -> pd.DataFrame:
        """
        计算因子相关性矩阵
        
        Args:
            factor_dict: 因子值字典
        
        Returns:
            pd.DataFrame: 相关性矩阵
        """
        factor_df = pd.DataFrame(factor_dict)
        return factor_df.corr(method='spearman')
    
    def detect_redundant_factors(
        self,
        factor_dict: Dict[str, pd.Series]
    ) -> List[Tuple[str, str, float]]:
        """
        检测冗余因子对
        
        Args:
            factor_dict: 因子值字典
        
        Returns:
            List[Tuple[因子1, 因子2, 相关系数]]: 冗余因子对列表
        """
        corr_matrix = self.calculate_correlation_matrix(factor_dict)
        
        redundant_pairs = []
        factors = list(factor_dict.keys())
        
        for i, f1 in enumerate(factors):
            for f2 in factors[i+1:]:
                corr = abs(corr_matrix.loc[f1, f2])
                if corr > self.correlation_threshold:
                    redundant_pairs.append((f1, f2, corr))
        
        return sorted(redundant_pairs, key=lambda x: -x[2])
    
    def suggest_factor_selection(
        self,
        factor_dict: Dict[str, pd.Series],
        ic_values: Optional[Dict[str, float]] = None
    ) -> List[str]:
        """
        建议因子筛选
        
        当存在冗余因子时，保留IC更高的因子
        
        Args:
            factor_dict: 因子值字典
            ic_values: 各因子的IC值
        
        Returns:
            List[str]: 建议保留的因子列表
        """
        if ic_values is None:
            # 没有IC信息，返回所有因子
            return list(factor_dict.keys())
        
        redundant_pairs = self.detect_redundant_factors(factor_dict)
        
        if not redundant_pairs:
            return list(factor_dict.keys())
        
        # 根据IC值决定保留哪个
        to_remove = set()
        
        for f1, f2, _ in redundant_pairs:
            if f1 in to_remove or f2 in to_remove:
                continue
            
            ic1 = ic_values.get(f1, 0)
            ic2 = ic_values.get(f2, 0)
            
            # 移除IC较低的因子
            if abs(ic1) >= abs(ic2):
                to_remove.add(f2)
                logger.info(f"因子冗余: 移除 {f2}，保留 {f1} (IC: {ic1:.4f} vs {ic2:.4f})")
            else:
                to_remove.add(f1)
                logger.info(f"因子冗余: 移除 {f1}，保留 {f2} (IC: {ic1:.4f} vs {ic2:.4f})")
        
        return [f for f in factor_dict.keys() if f not in to_remove]


class TurnoverAnalyzer:
    """
    换手率分析器
    
    评估因子选股的换手率和交易成本影响
    """
    
    def __init__(
        self,
        commission_rate: float = 0.001,  # 佣金费率（单边）
        slippage_rate: float = 0.001,     # 滑点费率
        stamp_tax_rate: float = 0.001     # 印花税率（卖出）
    ):
        """
        初始化
        
        Args:
            commission_rate: 佣金费率
            slippage_rate: 滑点费率
            stamp_tax_rate: 印花税率
        """
        self.commission_rate = commission_rate
        self.slippage_rate = slippage_rate
        self.stamp_tax_rate = stamp_tax_rate
    
    def calculate_turnover(
        self,
        portfolio_history: List[List[str]]
    ) -> List[float]:
        """
        计算历史换手率
        
        Args:
            portfolio_history: 历史持仓列表
        
        Returns:
            List[float]: 每期换手率
        """
        turnovers = []
        
        for i in range(1, len(portfolio_history)):
            prev_stocks = set(portfolio_history[i-1])
            curr_stocks = set(portfolio_history[i])
            
            if not prev_stocks and not curr_stocks:
                turnovers.append(0)
                continue
            
            # 新买入 + 卖出的比例
            new_stocks = curr_stocks - prev_stocks
            sold_stocks = prev_stocks - curr_stocks
            
            total_stocks = len(prev_stocks.union(curr_stocks))
            turnover = (len(new_stocks) + len(sold_stocks)) / (2 * total_stocks) if total_stocks > 0 else 0
            
            turnovers.append(turnover)
        
        return turnovers
    
    def estimate_transaction_cost(
        self,
        turnover: float,
        avg_position_value: float = 1_000_000
    ) -> float:
        """
        估算交易成本
        
        Args:
            turnover: 换手率
            avg_position_value: 平均持仓市值
        
        Returns:
            float: 交易成本
        """
        # 买入成本
        buy_cost = turnover * (self.commission_rate + self.slippage_rate)
        
        # 卖出成本（包含印花税）
        sell_cost = turnover * (self.commission_rate + self.slippage_rate + self.stamp_tax_rate)
        
        return (buy_cost + sell_cost) * avg_position_value
    
    def evaluate_factor_tradability(
        self,
        factor_annual_return: float,
        avg_turnover: float,
        periods_per_year: int = 12
    ) -> Dict[str, float]:
        """
        评估因子可交易性
        
        Args:
            factor_annual_return: 因子年化收益
            avg_turnover: 平均换手率
            periods_per_year: 每年调仓次数
        
        Returns:
            Dict: 评估结果
        """
        # 估算年化交易成本
        cost_per_period = self.estimate_transaction_cost(avg_turnover, 1.0)
        annual_cost = cost_per_period * periods_per_year
        
        # 扣除成本后的净收益
        net_return = factor_annual_return - annual_cost
        
        return {
            'gross_return': factor_annual_return,
            'annual_cost': annual_cost,
            'net_return': net_return,
            'avg_turnover': avg_turnover,
            'is_profitable': net_return > 0,
            'cost_ratio': annual_cost / factor_annual_return if factor_annual_return > 0 else np.inf
        }


# 便捷函数
def create_factor_neutralizer(jq_client=None) -> FactorNeutralizer:
    """创建因子中性化器"""
    return FactorNeutralizer(jq_client=jq_client)


def create_correlation_analyzer(threshold: float = 0.7) -> FactorCorrelationAnalyzer:
    """创建相关性分析器"""
    return FactorCorrelationAnalyzer(correlation_threshold=threshold)


def create_turnover_analyzer() -> TurnoverAnalyzer:
    """创建换手率分析器"""
    return TurnoverAnalyzer()

