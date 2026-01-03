"""
因子分析工具
============
集成Alphalens进行因子分析
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

try:
    import alphalens as al
    ALPHALENS_AVAILABLE = True
except ImportError:
    logger.warning("Alphalens未安装，因子分析功能将受限")
    ALPHALENS_AVAILABLE = False


def analyze_factor(
    factor_data: pd.Series,
    prices: pd.DataFrame,
    periods: Tuple[int, ...] = (1, 5, 10),
    quantiles: int = 5
) -> Dict:
    """
    使用Alphalens分析因子
    
    Args:
        factor_data: 因子数据（Series，index为(date, symbol)的MultiIndex）
        prices: 价格数据（DataFrame，index为date，columns为symbol）
        periods: 前瞻期（天数）
        quantiles: 分位数数量
    
    Returns:
        Dict: 分析结果，包含IC、IR、分组收益等
    """
    if not ALPHALENS_AVAILABLE:
        raise ImportError("Alphalens未安装，请运行: pip install alphalens-reloaded")
    
    try:
        # 准备因子数据
        factor_data_clean = al.utils.get_clean_factor_and_forward_returns(
            factor_data,
            prices,
            periods=periods,
            quantiles=quantiles,
            bins=None,
            binning_by_group=False,
            max_loss=0.35
        )
        
        # IC分析
        ic = al.performance.factor_information_coefficient(factor_data_clean)
        ic_mean = ic.mean()
        ic_std = ic.std()
        ir = ic_mean / ic_std if ic_std > 0 else 0
        
        # 分组收益分析
        mean_returns = al.performance.mean_return_by_quantile(factor_data_clean)
        
        # 累积收益
        cumulative_returns = al.performance.factor_cumulative_returns(
            factor_data_clean,
            period=periods[0]
        )
        
        # 分位数收益
        quantile_returns = al.performance.mean_return_by_quantile(factor_data_clean)
        
        return {
            "success": True,
            "ic": ic,
            "ic_mean": ic_mean,
            "ic_std": ic_std,
            "ir": ir,
            "mean_returns": mean_returns,
            "cumulative_returns": cumulative_returns,
            "quantile_returns": quantile_returns,
            "factor_data_clean": factor_data_clean
        }
        
    except Exception as e:
        logger.error(f"因子分析失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def calculate_ic_ir(
    factor_data: pd.Series,
    returns: pd.DataFrame,
    periods: Tuple[int, ...] = (1, 5, 10)
) -> Dict:
    """
    计算因子IC和IR
    
    Args:
        factor_data: 因子数据
        returns: 收益率数据
        periods: 前瞻期
    
    Returns:
        Dict: IC和IR统计
    """
    if not ALPHALENS_AVAILABLE:
        raise ImportError("Alphalens未安装")
    
    try:
        # 对齐数据
        factor_aligned, returns_aligned = al.utils.get_clean_factor_and_forward_returns(
            factor_data,
            returns,
            periods=periods
        )
        
        ic = al.performance.factor_information_coefficient(factor_aligned)
        
        result = {}
        for period in periods:
            period_ic = ic[period]
            result[f"period_{period}"] = {
                "ic_mean": period_ic.mean(),
                "ic_std": period_ic.std(),
                "ir": period_ic.mean() / period_ic.std() if period_ic.std() > 0 else 0,
                "ic_positive_ratio": (period_ic > 0).sum() / len(period_ic)
            }
        
        return {
            "success": True,
            "ic": ic,
            "periods": result
        }
    except Exception as e:
        logger.error(f"IC/IR计算失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def factor_quantile_returns(
    factor_data: pd.Series,
    prices: pd.DataFrame,
    quantiles: int = 5,
    period: int = 1
) -> pd.DataFrame:
    """
    计算因子分位数收益
    
    Args:
        factor_data: 因子数据
        prices: 价格数据
        quantiles: 分位数数量
        period: 前瞻期
    
    Returns:
        pd.DataFrame: 分位数收益表
    """
    if not ALPHALENS_AVAILABLE:
        raise ImportError("Alphalens未安装")
    
    try:
        factor_data_clean = al.utils.get_clean_factor_and_forward_returns(
            factor_data,
            prices,
            periods=(period,),
            quantiles=quantiles
        )
        
        mean_returns = al.performance.mean_return_by_quantile(factor_data_clean)
        return mean_returns
        
    except Exception as e:
        logger.error(f"分位数收益计算失败: {e}")
        raise


def create_factor_tear_sheet(
    factor_data: pd.Series,
    prices: pd.DataFrame,
    periods: Tuple[int, ...] = (1, 5, 10),
    quantiles: int = 5
) -> None:
    """
    创建因子分析报告（使用Alphalens的tear sheet）
    
    Args:
        factor_data: 因子数据
        prices: 价格数据
        periods: 前瞻期
        quantiles: 分位数数量
    """
    if not ALPHALENS_AVAILABLE:
        raise ImportError("Alphalens未安装")
    
    try:
        factor_data_clean = al.utils.get_clean_factor_and_forward_returns(
            factor_data,
            prices,
            periods=periods,
            quantiles=quantiles
        )
        
        al.tears.create_factor_tear_sheet(factor_data_clean, long_short=True, group_adjust=False)
        
    except Exception as e:
        logger.error(f"创建因子tear sheet失败: {e}")
        raise

