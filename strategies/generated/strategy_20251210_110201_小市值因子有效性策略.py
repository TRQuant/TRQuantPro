# -*- coding: utf-8 -*-
"""
策略代码: 小市值因子有效性策略
策略ID: strategy_20251210_110201
投资主线: 小市值因子有效性
生成时间: 2025-12-10T11:02:01.499569

研究卡引用:
- 小市值因子有效性研究 (分数: 0.221)
- 小市值因子有效性研究 (分数: 0.221)
- 动量因子组合策略 (分数: 0.000)

约束条件:
- 单票最大仓位: 0.1
- 最大回撤: 0.15
- 最小持仓数: 10
- 最大持仓数: 50
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any

# 策略参数
STRATEGY_ID = "strategy_20251210_110201"
STRATEGY_NAME = "小市值因子有效性策略"
MAINLINE = "小市值因子有效性"

# 因子配置
FACTORS = [
  "factor_market_cap",
  "factor_pe"
]
FACTOR_WEIGHTS = {
  "factor_market_cap": 0.5,
  "factor_pe": 0.5
}

# 候选股票池
CANDIDATE_POOL = [
  "000001",
  "000002",
  "000003",
  "000004",
  "000005",
  "000006",
  "000007",
  "000008",
  "000009",
  "000010"
]

# 约束条件
MAX_POSITION_SIZE = 0.1
MAX_DRAWDOWN = 0.15
MIN_POSITIONS = 10
MAX_POSITIONS = 50

# 入场条件
ENTRY_CONDITIONS = [
  "factor_factor_market_cap_score > 0.6",
  "factor_factor_pe_score > 0.6"
]

# 出场条件
EXIT_CONDITIONS = [
  "drawdown > 10%",
  "holding_days > 20"
]


def calculate_factor_scores(data: pd.DataFrame) -> pd.DataFrame:
    """
    计算因子得分
    
    Args:
        data: 股票数据DataFrame
    
    Returns:
        包含因子得分的DataFrame
    """
    scores = pd.DataFrame(index=data.index)
    
    for factor_name in FACTORS:
        # 这里需要根据实际因子计算逻辑实现
        # 示例：假设因子值在data中
        if factor_name in data.columns:
            scores[f"{factor_name}_score"] = data[factor_name]
        else:
            # 默认得分
            scores[f"{factor_name}_score"] = 0.5
    
    return scores


def check_entry_conditions(data: pd.DataFrame, scores: pd.DataFrame) -> pd.Series:
    """
    检查入场条件
    
    Args:
        data: 股票数据
        scores: 因子得分
    
    Returns:
        布尔Series，True表示满足入场条件
    """
    result = pd.Series(True, index=data.index)
    
    # 简化实现：检查因子得分
    for factor_name in FACTORS:
        score_col = f"{factor_name}_score"
        if score_col in scores.columns:
            result = result & (scores[score_col] > 0.6)
    
    return result


def check_exit_conditions(positions: Dict[str, Any], current_data: pd.DataFrame) -> List[str]:
    """
    检查出场条件
    
    Args:
        positions: 当前持仓
        current_data: 当前数据
    
    Returns:
        需要平仓的股票列表
    """
    exit_stocks = []
    
    for stock_code, position in positions.items():
        # 检查回撤
        if "drawdown" in position and position["drawdown"] > MAX_DRAWDOWN:
            exit_stocks.append(stock_code)
            continue
        
        # 检查持仓天数
        if "holding_days" in position and position["holding_days"] > 20:
            exit_stocks.append(stock_code)
            continue
    
    return exit_stocks


def select_stocks(data: pd.DataFrame, scores: pd.DataFrame) -> List[str]:
    """
    选择股票
    
    Args:
        data: 股票数据
        scores: 因子得分
    
    Returns:
        选中的股票代码列表
    """
    # 计算综合得分
    total_score = pd.Series(0.0, index=data.index)
    for factor_name, weight in FACTOR_WEIGHTS.items():
        score_col = f"{factor_name}_score"
        if score_col in scores.columns:
            total_score += scores[score_col] * weight
    
    # 检查入场条件
    entry_mask = check_entry_conditions(data, scores)
    
    # 筛选候选池
    candidate_mask = data.index.isin(CANDIDATE_POOL) if CANDIDATE_POOL else pd.Series(True, index=data.index)
    
    # 综合筛选
    final_mask = entry_mask & candidate_mask
    
    # 按得分排序
    selected = total_score[final_mask].sort_values(ascending=False)
    
    # 限制持仓数
    num_positions = min(MAX_POSITIONS, max(MIN_POSITIONS, len(selected)))
    selected_stocks = selected.head(num_positions).index.tolist()
    
    return selected_stocks


def calculate_position_weights(stocks: List[str], scores: pd.DataFrame) -> Dict[str, float]:
    """
    计算仓位权重
    
    Args:
        stocks: 选中的股票列表
        scores: 因子得分
    
    Returns:
        股票代码到权重的字典
    """
    if not stocks:
        return {}
    
    # 计算综合得分
    total_scores = {}
    for stock in stocks:
        score = 0.0
        for factor_name, weight in FACTOR_WEIGHTS.items():
            score_col = f"{factor_name}_score"
            if score_col in scores.columns and stock in scores.index:
                score += scores.loc[stock, score_col] * weight
        total_scores[stock] = score
    
    # 归一化权重
    total = sum(total_scores.values())
    if total == 0:
        # 等权重
        weight = 1.0 / len(stocks)
        return {stock: min(weight, MAX_POSITION_SIZE) for stock in stocks}
    
    weights = {stock: min(score / total, MAX_POSITION_SIZE) for stock, score in total_scores.items()}
    
    # 确保总权重为1
    total_weight = sum(weights.values())
    if total_weight > 0:
        weights = {stock: weight / total_weight for stock, weight in weights.items()}
    
    return weights


def run_strategy(data: pd.DataFrame) -> Dict[str, Any]:
    """
    运行策略
    
    Args:
        data: 股票数据DataFrame
    
    Returns:
        策略结果字典
    """
    # 计算因子得分
    scores = calculate_factor_scores(data)
    
    # 选择股票
    selected_stocks = select_stocks(data, scores)
    
    # 计算仓位权重
    weights = calculate_position_weights(selected_stocks, scores)
    
    return {
        "selected_stocks": selected_stocks,
        "weights": weights,
        "num_positions": len(selected_stocks),
        "total_weight": sum(weights.values())
    }


if __name__ == "__main__":
    # 示例使用
    print(f"策略: {STRATEGY_NAME}")
    print(f"主线: {MAINLINE}")
    print(f"因子: {', '.join(FACTORS)}")
    print(f"候选池大小: {len(CANDIDATE_POOL)}")
