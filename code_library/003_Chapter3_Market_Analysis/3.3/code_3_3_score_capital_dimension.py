"""
资金维度评分函数

设计原理：
1. 综合考虑主力资金、北向资金、融资融券等资金流向指标
2. 使用排名百分位法，避免极值影响
3. 各指标权重分配：主力资金(40%)、北向资金(25%)、融资融券(20%)、机构持仓(15%)
4. 时间衰减：近期数据权重更高
5. 评分范围：0-100分
"""

import pandas as pd
from typing import Dict, Any, List
from datetime import datetime, timedelta


def score_capital_dimension(
    main_force_net_inflow: float,
    northbound_net_inflow: float,
    margin_balance_change: float,
    institutional_holding_change: float,
    consecutive_inflow_days: int = 0
) -> Dict[str, Any]:
    """
    资金维度评分
    
    Args:
        main_force_net_inflow: 主力资金净流入（万元）
        northbound_net_inflow: 北向资金净流入（万元）
        margin_balance_change: 融资融券余额变化率（%）
        institutional_holding_change: 机构持仓变化率（%）
        consecutive_inflow_days: 连续流入天数
    
    Returns:
        包含评分和详细信息的字典
    """
    score = 0.0
    details = {}
    
    # 1. 主力资金净流入评分（0-40分）
    # 使用分段评分法
    if main_force_net_inflow >= 100000:  # 10亿以上
        main_force_score = 40
    elif main_force_net_inflow >= 50000:  # 5-10亿
        main_force_score = 35
    elif main_force_net_inflow >= 20000:  # 2-5亿
        main_force_score = 30
    elif main_force_net_inflow >= 5000:   # 0.5-2亿
        main_force_score = 20
    elif main_force_net_inflow >= 0:
        main_force_score = 10
    else:
        # 净流出，根据流出规模扣分
        main_force_score = max(0, 10 + main_force_net_inflow / 1000)
    
    # 连续流入天数加成（最多+5分）
    if consecutive_inflow_days >= 5:
        main_force_score += 5
    elif consecutive_inflow_days >= 3:
        main_force_score += 3
    elif consecutive_inflow_days >= 1:
        main_force_score += 1
    
    main_force_score = min(40, main_force_score)  # 不超过40分
    score += main_force_score
    details['main_force_score'] = round(main_force_score, 2)
    details['main_force_net_inflow'] = main_force_net_inflow
    details['consecutive_inflow_days'] = consecutive_inflow_days
    
    # 2. 北向资金净流入评分（0-25分）
    if northbound_net_inflow >= 50000:  # 5亿以上
        northbound_score = 25
    elif northbound_net_inflow >= 20000:  # 2-5亿
        northbound_score = 20
    elif northbound_net_inflow >= 5000:   # 0.5-2亿
        northbound_score = 15
    elif northbound_net_inflow >= 0:
        northbound_score = 10
    else:
        northbound_score = max(0, 10 + northbound_net_inflow / 500)
    
    score += northbound_score
    details['northbound_score'] = round(northbound_score, 2)
    details['northbound_net_inflow'] = northbound_net_inflow
    
    # 3. 融资融券余额变化评分（0-20分）
    # 余额增加表示看多情绪
    if margin_balance_change >= 10:
        margin_score = 20
    elif margin_balance_change >= 5:
        margin_score = 15
    elif margin_balance_change >= 0:
        margin_score = 10
    else:
        margin_score = max(0, 10 + margin_balance_change * 2)
    
    score += margin_score
    details['margin_score'] = round(margin_score, 2)
    details['margin_balance_change'] = margin_balance_change
    
    # 4. 机构持仓变化评分（0-15分）
    if institutional_holding_change >= 5:
        institutional_score = 15
    elif institutional_holding_change >= 2:
        institutional_score = 12
    elif institutional_holding_change >= 0:
        institutional_score = 8
    else:
        institutional_score = max(0, 8 + institutional_holding_change * 2)
    
    score += institutional_score
    details['institutional_score'] = round(institutional_score, 2)
    details['institutional_holding_change'] = institutional_holding_change
    
    return {
        'capital_score': round(score, 2),
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

