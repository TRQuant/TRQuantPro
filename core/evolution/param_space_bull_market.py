#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市策略参数空间定义

定义用于进化优化的参数范围和约束。
"""

from typing import Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class ParamRange:
    """参数范围"""
    min: float
    max: float
    step: float = 1.0
    param_type: str = 'float'  # 'float' or 'int'


# 牛市策略参数空间
BULL_MARKET_PARAM_SPACE: Dict[str, ParamRange] = {
    # 选股参数
    'max_stocks': ParamRange(min=5, max=20, step=1, param_type='int'),
    'min_total_score': ParamRange(min=25.0, max=35.0, step=0.5, param_type='float'),
    
    # 因子权重（牛市调整）
    'momentum_20d_weight': ParamRange(min=0.15, max=0.25, step=0.01, param_type='float'),
    'rel_position_weight': ParamRange(min=0.10, max=0.20, step=0.01, param_type='float'),
    'market_cap_weight': ParamRange(min=0.12, max=0.18, step=0.01, param_type='float'),
    'momentum_5d_weight': ParamRange(min=0.10, max=0.18, step=0.01, param_type='float'),
    'turnover_rate_weight': ParamRange(min=0.10, max=0.16, step=0.01, param_type='float'),
    'roe_weight': ParamRange(min=0.05, max=0.12, step=0.01, param_type='float'),
    'growth_weight': ParamRange(min=0.03, max=0.10, step=0.01, param_type='float'),
    
    # 调仓频率（牛市可更频繁）
    'rebalance_days': ParamRange(min=3, max=10, step=1, param_type='int'),
    
    # 止损止盈（牛市更激进）
    'stop_loss': ParamRange(min=-0.12, max=-0.06, step=0.01, param_type='float'),  # -12% ~ -6%
    'take_profit': ParamRange(min=0.20, max=0.40, step=0.02, param_type='float'),  # +20% ~ +40%
    'trailing_stop': ParamRange(min=-0.10, max=-0.05, step=0.01, param_type='float'),  # -10% ~ -5%
    
    # 仓位管理
    'single_position_max': ParamRange(min=0.10, max=0.25, step=0.01, param_type='float'),  # 10% ~ 25%
    'min_cash_ratio': ParamRange(min=0.05, max=0.15, step=0.01, param_type='float'),  # 5% ~ 15%
    
    # 因子筛选阈值
    'min_momentum_20d': ParamRange(min=-5.0, max=5.0, step=1.0, param_type='float'),
    'max_momentum_20d': ParamRange(min=20.0, max=35.0, step=2.0, param_type='float'),
    'max_rel_position': ParamRange(min=60.0, max=85.0, step=5.0, param_type='float'),
    'min_market_cap': ParamRange(min=20.0, max=40.0, step=5.0, param_type='float'),
    'max_market_cap': ParamRange(min=250.0, max=350.0, step=25.0, param_type='float'),
}


def get_param_value(param_name: str, encoded_value: float) -> Any:
    """
    将编码值（0-1）转换为实际参数值
    
    Args:
        param_name: 参数名
        encoded_value: 编码值（0-1）
    
    Returns:
        实际参数值
    """
    if param_name not in BULL_MARKET_PARAM_SPACE:
        raise ValueError(f"未知参数: {param_name}")
    
    param_range = BULL_MARKET_PARAM_SPACE[param_name]
    
    # 归一化到[min, max]
    value = param_range.min + encoded_value * (param_range.max - param_range.min)
    
    # 按step对齐
    if param_range.param_type == 'int':
        value = int(round(value / param_range.step) * param_range.step)
        value = max(param_range.min, min(param_range.max, value))
    else:
        value = round(value / param_range.step) * param_range.step
        value = max(param_range.min, min(param_range.max, value))
    
    return value


def decode_individual(individual: list) -> Dict[str, Any]:
    """
    解码个体（参数向量）为参数字典
    
    Args:
        individual: 个体（参数编码列表，每个值在0-1之间）
    
    Returns:
        参数字典
    """
    param_names = list(BULL_MARKET_PARAM_SPACE.keys())
    
    if len(individual) != len(param_names):
        raise ValueError(f"个体维度不匹配: {len(individual)} != {len(param_names)}")
    
    params = {}
    for i, param_name in enumerate(param_names):
        params[param_name] = get_param_value(param_name, individual[i])
    
    # 归一化因子权重（确保总和为1）
    weight_params = [k for k in params.keys() if k.endswith('_weight')]
    if weight_params:
        total_weight = sum([params[k] for k in weight_params])
        if total_weight > 0:
            for k in weight_params:
                params[k] = params[k] / total_weight
    
    return params


def encode_params(params: Dict[str, Any]) -> list:
    """
    将参数字典编码为个体（参数向量）
    
    Args:
        params: 参数字典
    
    Returns:
        个体（参数编码列表）
    """
    individual = []
    param_names = list(BULL_MARKET_PARAM_SPACE.keys())
    
    for param_name in param_names:
        if param_name not in params:
            # 使用默认值
            param_range = BULL_MARKET_PARAM_SPACE[param_name]
            default_value = (param_range.min + param_range.max) / 2.0
            params[param_name] = default_value
        
        param_range = BULL_MARKET_PARAM_SPACE[param_name]
        value = params[param_name]
        
        # 归一化到[0, 1]
        if param_range.max > param_range.min:
            encoded = (value - param_range.min) / (param_range.max - param_range.min)
            encoded = max(0.0, min(1.0, encoded))
        else:
            encoded = 0.5
        
        individual.append(encoded)
    
    return individual
