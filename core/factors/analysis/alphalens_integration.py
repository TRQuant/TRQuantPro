# -*- coding: utf-8 -*-
"""
Alphalens因子分析集成
=====================

整合Alphalens进行专业的因子分析，包括：
- IC（信息系数）分析
- 收益率分析
- 换手率分析
- 因子衰减分析

如果未安装alphalens，使用内置简化版本
"""
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# 尝试导入alphalens
ALPHALENS_AVAILABLE = False
try:
    import alphalens
    from alphalens.utils import get_clean_factor_and_forward_returns
    from alphalens.performance import factor_information_coefficient
    from alphalens.tears import create_full_tear_sheet
    ALPHALENS_AVAILABLE = True
    logger.info("✅ Alphalens已安装")
except ImportError:
    logger.warning("Alphalens未安装，使用内置简化版本")


@dataclass
class FactorAnalysisResult:
    """因子分析结果"""
    factor_name: str
    ic_mean: float = 0.0
    ic_std: float = 0.0
    ir: float = 0.0  # IC信息比率
    ic_series: Optional[pd.Series] = None
    quantile_returns: Optional[pd.DataFrame] = None
    turnover: float = 0.0
    factor_decay: Optional[pd.DataFrame] = None
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "factor_name": self.factor_name,
            "ic_mean": self.ic_mean,
            "ic_std": self.ic_std,
            "ir": self.ir,
            "turnover": self.turnover,
            "summary": self.summary,
        }


class AlphalensAnalyzer:
    """Alphalens因子分析器"""
    
    def __init__(self, use_alphalens: bool = True):
        """
        初始化
        
        Args:
            use_alphalens: 是否使用alphalens库（如果已安装）
        """
        self.use_alphalens = use_alphalens and ALPHALENS_AVAILABLE
        
    def analyze_factor(
        self,
        factor_data: pd.DataFrame,
        prices: pd.DataFrame,
        periods: List[int] = [1, 5, 10, 20],
        quantiles: int = 5,
    ) -> FactorAnalysisResult:
        """
        分析因子
        
        Args:
            factor_data: 因子数据，Index为日期，columns为股票代码
            prices: 价格数据，Index为日期，columns为股票代码
            periods: 分析周期列表
            quantiles: 分位数
        
        Returns:
            因子分析结果
        """
        if self.use_alphalens:
            return self._analyze_with_alphalens(factor_data, prices, periods, quantiles)
        else:
            return self._analyze_builtin(factor_data, prices, periods, quantiles)
    
    def _analyze_with_alphalens(
        self,
        factor_data: pd.DataFrame,
        prices: pd.DataFrame,
        periods: List[int],
        quantiles: int,
    ) -> FactorAnalysisResult:
        """使用Alphalens分析"""
        try:
            # 转换为alphalens格式
            factor_series = factor_data.stack()
            factor_series.index.names = ['date', 'asset']
            
            # 获取清洗后的因子和远期收益
            factor_clean, forward_returns = get_clean_factor_and_forward_returns(
                factor=factor_series,
                prices=prices,
                periods=tuple(periods),
                quantiles=quantiles,
            )
            
            # 计算IC
            ic = factor_information_coefficient(factor_clean, forward_returns)
            ic_mean = ic.mean()
            ic_std = ic.std()
            
            # 计算IR（IC均值/IC标准差）
            ir = ic_mean / (ic_std + 1e-8)
            
            return FactorAnalysisResult(
                factor_name="factor",
                ic_mean=float(ic_mean.iloc[0]) if hasattr(ic_mean, 'iloc') else float(ic_mean),
                ic_std=float(ic_std.iloc[0]) if hasattr(ic_std, 'iloc') else float(ic_std),
                ir=float(ir.iloc[0]) if hasattr(ir, 'iloc') else float(ir),
                ic_series=ic,
                summary={
                    "periods": periods,
                    "quantiles": quantiles,
                    "data_points": len(factor_clean),
                }
            )
            
        except Exception as e:
            logger.error(f"Alphalens分析失败: {e}")
            return self._analyze_builtin(factor_data, prices, periods, quantiles)
    
    def _analyze_builtin(
        self,
        factor_data: pd.DataFrame,
        prices: pd.DataFrame,
        periods: List[int],
        quantiles: int,
    ) -> FactorAnalysisResult:
        """内置简化分析"""
        try:
            # 计算收益率
            returns = prices.pct_change()
            
            # 计算各周期IC
            ic_results = {}
            for period in periods:
                forward_ret = returns.shift(-period).rolling(period).sum()
                
                ic_series = []
                for date in factor_data.index:
                    if date not in forward_ret.index:
                        continue
                    factor_row = factor_data.loc[date].dropna()
                    ret_row = forward_ret.loc[date].dropna()
                    common = factor_row.index.intersection(ret_row.index)
                    if len(common) > 10:
                        ic = factor_row[common].corr(ret_row[common])
                        ic_series.append(ic)
                
                if ic_series:
                    ic_results[period] = {
                        'mean': np.nanmean(ic_series),
                        'std': np.nanstd(ic_series),
                        'series': ic_series
                    }
            
            # 汇总结果
            if ic_results:
                first_period = periods[0]
                ic_mean = ic_results[first_period]['mean']
                ic_std = ic_results[first_period]['std']
                ir = ic_mean / (ic_std + 1e-8)
                
                return FactorAnalysisResult(
                    factor_name="factor",
                    ic_mean=ic_mean,
                    ic_std=ic_std,
                    ir=ir,
                    ic_series=pd.Series(ic_results[first_period]['series']),
                    summary={
                        "periods": periods,
                        "quantiles": quantiles,
                        "ic_by_period": {p: ic_results[p]['mean'] for p in ic_results},
                    }
                )
            
            return FactorAnalysisResult(factor_name="factor")
            
        except Exception as e:
            logger.error(f"内置分析失败: {e}")
            return FactorAnalysisResult(factor_name="factor")
    
    def calculate_ic(
        self,
        factor_data: pd.DataFrame,
        returns: pd.DataFrame,
        method: str = "spearman"
    ) -> pd.Series:
        """
        计算IC序列
        
        Args:
            factor_data: 因子数据
            returns: 收益率数据
            method: 相关性方法 (spearman/pearson)
        
        Returns:
            IC序列
        """
        ic_list = []
        dates = factor_data.index.intersection(returns.index)
        
        for date in dates:
            factor_row = factor_data.loc[date].dropna()
            ret_row = returns.loc[date].dropna()
            common = factor_row.index.intersection(ret_row.index)
            
            if len(common) > 10:
                if method == "spearman":
                    ic = factor_row[common].rank().corr(ret_row[common].rank())
                else:
                    ic = factor_row[common].corr(ret_row[common])
                ic_list.append((date, ic))
        
        if ic_list:
            return pd.Series(dict(ic_list))
        return pd.Series()
    
    def calculate_ir(self, ic_series: pd.Series) -> float:
        """计算信息比率 IR = IC均值 / IC标准差"""
        if len(ic_series) == 0:
            return 0.0
        return ic_series.mean() / (ic_series.std() + 1e-8)
    
    def quantile_analysis(
        self,
        factor_data: pd.DataFrame,
        returns: pd.DataFrame,
        quantiles: int = 5
    ) -> pd.DataFrame:
        """
        分位数收益分析
        
        Args:
            factor_data: 因子数据
            returns: 收益率数据
            quantiles: 分位数
        
        Returns:
            各分位数平均收益
        """
        results = []
        dates = factor_data.index.intersection(returns.index)
        
        for date in dates:
            factor_row = factor_data.loc[date].dropna()
            ret_row = returns.loc[date].dropna()
            common = factor_row.index.intersection(ret_row.index)
            
            if len(common) < quantiles * 5:
                continue
            
            factor_values = factor_row[common]
            ret_values = ret_row[common]
            
            # 分组
            bins = pd.qcut(factor_values, quantiles, labels=False, duplicates='drop')
            
            for q in range(quantiles):
                mask = bins == q
                if mask.sum() > 0:
                    results.append({
                        'date': date,
                        'quantile': q + 1,
                        'return': ret_values[mask].mean()
                    })
        
        if results:
            df = pd.DataFrame(results)
            return df.groupby('quantile')['return'].mean()
        return pd.DataFrame()
    
    def factor_decay_analysis(
        self,
        factor_data: pd.DataFrame,
        prices: pd.DataFrame,
        max_periods: int = 20
    ) -> pd.DataFrame:
        """
        因子衰减分析
        
        Args:
            factor_data: 因子数据
            prices: 价格数据
            max_periods: 最大分析周期
        
        Returns:
            各周期IC
        """
        returns = prices.pct_change()
        results = []
        
        for period in range(1, max_periods + 1):
            forward_ret = returns.shift(-period)
            ic_series = self.calculate_ic(factor_data, forward_ret)
            
            if len(ic_series) > 0:
                results.append({
                    'period': period,
                    'ic_mean': ic_series.mean(),
                    'ic_std': ic_series.std(),
                    'ir': ic_series.mean() / (ic_series.std() + 1e-8)
                })
        
        return pd.DataFrame(results)
