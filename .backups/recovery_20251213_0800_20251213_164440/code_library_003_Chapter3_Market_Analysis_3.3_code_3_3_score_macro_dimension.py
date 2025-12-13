"""
宏观维度评分函数

设计原理：
1. 综合考虑GDP增速、CPI、PMI、货币政策等宏观指标
2. 使用分段评分法，对不同指标区间赋予不同分值
3. 各指标权重分配：GDP(30%)、CPI(20%)、PMI(25%)、货币政策(25%)
4. 评分范围：0-100分
"""

import pandas as pd
from typing import Dict, Any


def score_macro_dimension(
    gdp_growth: float,
    cpi: float,
    pmi: float,
    monetary_policy: str
) -> Dict[str, Any]:
    """
    宏观维度评分
    
    Args:
        gdp_growth: GDP增速（%）
        cpi: CPI（%）
        pmi: PMI（50为荣枯线）
        monetary_policy: 货币政策（'loose'宽松/'neutral'中性/'tight'紧缩）
    
    Returns:
        包含评分和详细信息的字典
    """
    score = 0.0
    details = {}
    
    # 1. GDP增速评分（0-30分）
    # 理想区间：5-7%
    if 5 <= gdp_growth <= 7:
        gdp_score = 30
    elif 4 <= gdp_growth < 5 or 7 < gdp_growth <= 8:
        gdp_score = 25
    elif 3 <= gdp_growth < 4 or 8 < gdp_growth <= 9:
        gdp_score = 20
    elif 2 <= gdp_growth < 3 or 9 < gdp_growth <= 10:
        gdp_score = 15
    else:
        gdp_score = max(0, 30 - abs(gdp_growth - 6) * 5)
    
    score += gdp_score
    details['gdp_score'] = gdp_score
    details['gdp_growth'] = gdp_growth
    
    # 2. CPI评分（0-20分）
    # 理想区间：1.5-2.5%
    if 1.5 <= cpi <= 2.5:
        cpi_score = 20
    elif 1.0 <= cpi < 1.5 or 2.5 < cpi <= 3.0:
        cpi_score = 15
    elif 0.5 <= cpi < 1.0 or 3.0 < cpi <= 3.5:
        cpi_score = 10
    else:
        cpi_score = max(0, 20 - abs(cpi - 2.0) * 10)
    
    score += cpi_score
    details['cpi_score'] = cpi_score
    details['cpi'] = cpi
    
    # 3. PMI评分（0-25分）
    # 50为荣枯线，高于50表示扩张
    if pmi >= 52:
        pmi_score = 25
    elif 50 <= pmi < 52:
        pmi_score = 20
    elif 48 <= pmi < 50:
        pmi_score = 15
    elif 46 <= pmi < 48:
        pmi_score = 10
    else:
        pmi_score = max(0, 25 - (50 - pmi) * 2.5)
    
    score += pmi_score
    details['pmi_score'] = pmi_score
    details['pmi'] = pmi
    
    # 4. 货币政策评分（0-25分）
    policy_scores = {
        'loose': 25,    # 宽松政策有利于市场
        'neutral': 15,  # 中性政策
        'tight': 5      # 紧缩政策不利于市场
    }
    policy_score = policy_scores.get(monetary_policy.lower(), 10)
    
    score += policy_score
    details['policy_score'] = policy_score
    details['monetary_policy'] = monetary_policy
    
    return {
        'macro_score': round(score, 2),
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

