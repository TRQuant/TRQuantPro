"""
估值维度评分函数

设计原理：
1. 综合考虑PE、PB及其历史分位数等估值指标
2. 使用分位数排名法，分位数越低表示估值越便宜
3. 各指标权重分配：PE分位数(30%)、PB分位数(30%)、综合分位数(20%)
4. 评分范围：0-100分
"""

import pandas as pd
from typing import Dict, Any


def score_valuation_dimension(
    pe_ratio: float,
    pb_ratio: float,
    pe_percentile: float,
    pb_percentile: float
) -> Dict[str, Any]:
    """
    估值维度评分
    
    Args:
        pe_ratio: PE比率（市盈率）
        pb_ratio: PB比率（市净率）
        pe_percentile: PE历史分位数（0-100，越低表示越便宜）
        pb_percentile: PB历史分位数（0-100，越低表示越便宜）
    
    Returns:
        包含评分和详细信息的字典
    """
    score = 0.0
    details = {}
    
    # 1. PE分位数评分（0-30分）
    # 分位数越低，估值越便宜，评分越高
    if pe_percentile <= 20:
        pe_score = 30
    elif pe_percentile <= 40:
        pe_score = 25
    elif pe_percentile <= 60:
        pe_score = 20
    elif pe_percentile <= 80:
        pe_score = 12
    else:
        pe_score = max(0, 12 - (pe_percentile - 80) * 0.6)
    
    score += pe_score
    details['pe_score'] = round(pe_score, 2)
    details['pe_ratio'] = pe_ratio
    details['pe_percentile'] = pe_percentile
    
    # 2. PB分位数评分（0-30分）
    # 分位数越低，估值越便宜，评分越高
    if pb_percentile <= 20:
        pb_score = 30
    elif pb_percentile <= 40:
        pb_score = 25
    elif pb_percentile <= 60:
        pb_score = 20
    elif pb_percentile <= 80:
        pb_score = 12
    else:
        pb_score = max(0, 12 - (pb_percentile - 80) * 0.6)
    
    score += pb_score
    details['pb_score'] = round(pb_score, 2)
    details['pb_ratio'] = pb_ratio
    details['pb_percentile'] = pb_percentile
    
    # 3. 综合分位数评分（0-20分）
    # 综合考虑PE和PB的分位数
    combined_score = (pe_percentile + pb_percentile) / 2
    if combined_score <= 30:
        combined_bonus = 20
    elif combined_score <= 50:
        combined_bonus = 15
    elif combined_score <= 70:
        combined_bonus = 10
    else:
        combined_bonus = 5
    
    score += combined_bonus
    details['combined_bonus'] = combined_bonus
    details['combined_percentile'] = round(combined_score, 2)
    
    return {
        'valuation_score': round(score, 2),
        'details': details,
        'level': _get_score_level(score)
    }


def _get_score_level(score: float) -> str:
    """根据评分返回等级"""
    if score >= 80:
        return '优秀'
    elif score >= 60:
        return '良好'
    elif score >= 40:
        return '一般'
    else:
        return '较差'
