"""
投资组合优化工具
================
集成PyPortfolioOpt进行组合优化
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

try:
    from pypfopt import EfficientFrontier, risk_models, expected_returns
    from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
    PYPFOPT_AVAILABLE = True
except ImportError:
    logger.warning("PyPortfolioOpt未安装，组合优化功能将受限")
    PYPFOPT_AVAILABLE = False

try:
    import empyrical as emp
    EMPYRICAL_AVAILABLE = True
except ImportError:
    try:
        import empyrical_reloaded as emp
        EMPYRICAL_AVAILABLE = True
    except ImportError:
        logger.warning("Empyrical未安装，绩效指标计算将受限")
        EMPYRICAL_AVAILABLE = False


def optimize_portfolio(
    returns: pd.DataFrame,
    method: str = "max_sharpe",
    risk_free_rate: float = 0.02,
    constraints: Optional[Dict] = None,
    market_neutral: bool = False
) -> Dict:
    """
    优化投资组合
    
    Args:
        returns: 收益率数据（DataFrame，index为date，columns为symbol）
        method: 优化方法（"max_sharpe", "min_volatility", "efficient_risk", "efficient_return"）
        risk_free_rate: 无风险利率
        constraints: 额外约束条件
        market_neutral: 是否市场中性
    
    Returns:
        Dict: 优化结果，包含权重、预期收益、波动率、夏普比率等
    """
    if not PYPFOPT_AVAILABLE:
        raise ImportError("PyPortfolioOpt未安装，请运行: pip install pyportfolioopt")
    
    try:
        # 计算预期收益和协方差矩阵
        mu = expected_returns.mean_historical_return(returns)
        S = risk_models.sample_cov(returns)
        
        # 创建有效前沿
        ef = EfficientFrontier(mu, S)
        
        # 添加约束
        if constraints:
            for constraint_type, constraint_value in constraints.items():
                if constraint_type == "max_weight":
                    ef.add_constraint(lambda w: w <= constraint_value)
                elif constraint_type == "min_weight":
                    ef.add_constraint(lambda w: w >= constraint_value)
        
        # 执行优化
        if method == "max_sharpe":
            weights = ef.max_sharpe(risk_free_rate=risk_free_rate)
        elif method == "min_volatility":
            weights = ef.min_volatility()
        elif method == "efficient_risk":
            target_vol = constraints.get("target_volatility", 0.15) if constraints else 0.15
            weights = ef.efficient_risk(target_volatility=target_vol)
        elif method == "efficient_return":
            target_return = constraints.get("target_return", 0.20) if constraints else 0.20
            weights = ef.efficient_return(target_return=target_return, market_neutral=market_neutral)
        else:
            raise ValueError(f"未知的优化方法: {method}")
        
        # 清理权重（移除接近0的权重）
        cleaned_weights = ef.clean_weights()
        
        # 计算组合指标
        perf = ef.portfolio_performance(risk_free_rate=risk_free_rate, verbose=False)
        
        return {
            "success": True,
            "weights": cleaned_weights,
            "expected_return": perf[0],
            "volatility": perf[1],
            "sharpe_ratio": perf[2],
            "method": method
        }
        
    except Exception as e:
        logger.error(f"组合优化失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def calculate_portfolio_metrics(
    returns: pd.Series,
    benchmark: Optional[pd.Series] = None,
    risk_free_rate: float = 0.02
) -> Dict:
    """
    计算投资组合绩效指标
    
    Args:
        returns: 组合收益率序列
        benchmark: 基准收益率序列（可选）
        risk_free_rate: 无风险利率
    
    Returns:
        Dict: 绩效指标
    """
    if not EMPYRICAL_AVAILABLE:
        logger.warning("Empyrical未安装，使用简化指标计算")
        return _calculate_simple_metrics(returns, benchmark, risk_free_rate)
    
    try:
        metrics = {}
        
        # 基本指标
        metrics["total_return"] = emp.cum_returns_final(returns)
        metrics["annual_return"] = emp.annual_return(returns, period='daily')
        metrics["volatility"] = emp.annual_volatility(returns, period='daily')
        metrics["sharpe_ratio"] = emp.sharpe_ratio(returns, risk_free=risk_free_rate, period='daily')
        metrics["sortino_ratio"] = emp.sortino_ratio(returns, risk_free=risk_free_rate, period='daily')
        metrics["calmar_ratio"] = emp.calmar_ratio(returns, period='daily')
        
        # 回撤指标
        drawdown = emp.max_drawdown(returns)
        metrics["max_drawdown"] = drawdown
        
        # 胜率
        metrics["win_rate"] = (returns > 0).sum() / len(returns)
        
        # 与基准比较
        if benchmark is not None:
            metrics["alpha"] = emp.alpha(returns, benchmark, risk_free=risk_free_rate, period='daily')
            metrics["beta"] = emp.beta(returns, benchmark, risk_free=risk_free_rate)
            metrics["information_ratio"] = emp.information_ratio(returns, benchmark)
            metrics["tracking_error"] = emp.tracking_error(returns, benchmark)
        
        return {
            "success": True,
            "metrics": metrics
        }
        
    except Exception as e:
        logger.error(f"绩效指标计算失败: {e}")
        return {
            "success": False,
            "error": str(e),
            "metrics": _calculate_simple_metrics(returns, benchmark, risk_free_rate)
        }


def _calculate_simple_metrics(
    returns: pd.Series,
    benchmark: Optional[pd.Series],
    risk_free_rate: float
) -> Dict:
    """简化的指标计算（当Empyrical不可用时）"""
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + returns.mean()) ** 252 - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
    
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "win_rate": (returns > 0).sum() / len(returns)
    }


def discrete_allocation(
    weights: Dict[str, float],
    latest_prices: pd.Series,
    total_portfolio_value: float = 100000
) -> Dict:
    """
    离散化分配（将权重转换为实际股数）
    
    Args:
        weights: 权重字典 {symbol: weight}
        latest_prices: 最新价格 {symbol: price}
        total_portfolio_value: 总组合价值
    
    Returns:
        Dict: 分配结果
    """
    if not PYPFOPT_AVAILABLE:
        raise ImportError("PyPortfolioOpt未安装")
    
    try:
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=total_portfolio_value)
        allocation, leftover = da.lp_portfolio()
        
        return {
            "success": True,
            "allocation": allocation,
            "leftover": leftover,
            "total_value": total_portfolio_value - leftover
        }
    except Exception as e:
        logger.error(f"离散化分配失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

