"""
行业维度评分函数

设计原理：
1. 综合考虑行业收入增速、利润增速、景气度等指标
2. 使用相对排名法，与全市场平均水平对比
3. 各指标权重分配：收入增速(30%)、利润增速(30%)、景气度(25%)、政策支持(15%)
4. 评分范围：0-100分
"""

import pandas as pd
from typing import Dict, Any


def score_industry_dimension(
    revenue_growth: float,
    profit_growth: float,
    industry_pmi: float,
    policy_support: float
) -> Dict[str, Any]:
    """
    行业维度评分
    
    Args:
        revenue_growth: 行业收入增速（%）
        profit_growth: 行业利润增速（%）
        industry_pmi: 行业PMI（50为荣枯线）
        policy_support: 政策支持度（0-1，1表示最强支持）
    
    Returns:
        包含评分和详细信息的字典
    """
    score = 0.0
    details = {}
    
    # 1. 收入增速评分（0-30分）
    if revenue_growth >= 20:
        revenue_score = 30
    elif revenue_growth >= 15:
        revenue_score = 27
    elif revenue_growth >= 10:
        revenue_score = 24
    elif revenue_growth >= 5:
        revenue_score = 18
    elif revenue_growth >= 0:
        revenue_score = 12
    else:
        revenue_score = max(0, 12 + revenue_growth * 2)
    
    score += revenue_score
    details['revenue_score'] = round(revenue_score, 2)
    details['revenue_growth'] = revenue_growth
    
    # 2. 利润增速评分（0-30分）
    if profit_growth >= 30:
        profit_score = 30
    elif profit_growth >= 20:
        profit_score = 27
    elif profit_growth >= 10:
        profit_score = 24
    elif profit_growth >= 5:
        profit_score = 18
    elif profit_growth >= 0:
        profit_score = 12
    else:
        profit_score = max(0, 12 + profit_growth * 1.5)
    
    score += profit_score
    details['profit_score'] = round(profit_score, 2)
    details['profit_growth'] = profit_growth
    
    # 3. 行业景气度评分（0-25分）
    if industry_pmi >= 55:
        pmi_score = 25
    elif industry_pmi >= 52:
        pmi_score = 22
    elif industry_pmi >= 50:
        pmi_score = 18
    elif industry_pmi >= 48:
        pmi_score = 12
    elif industry_pmi >= 45:
        pmi_score = 8
    else:
        pmi_score = max(0, 25 - (50 - industry_pmi) * 2.5)
    
    score += pmi_score
    details['pmi_score'] = round(pmi_score, 2)
    details['industry_pmi'] = industry_pmi
    
    # 4. 政策支持度评分（0-15分）
    policy_score = policy_support * 15
    score += policy_score
    details['policy_score'] = round(policy_score, 2)
    details['policy_support'] = policy_support
    
    return {
        'industry_score': round(score, 2),
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

