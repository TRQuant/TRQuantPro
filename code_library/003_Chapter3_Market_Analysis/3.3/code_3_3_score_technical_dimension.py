"""
技术维度评分函数

设计原理：
1. 综合考虑价格动量、成交量动量、趋势强度、突破信号等技术指标
2. 使用分段评分法，对不同指标区间赋予不同分值
3. 各指标权重分配：价格动量(30%)、成交量动量(25%)、趋势强度(25%)、突破信号(20%)
4. 评分范围：0-100分
"""

import pandas as pd
from typing import Dict, Any


def score_technical_dimension(
    price_momentum: float,
    volume_momentum: float,
    trend_strength: float,
    breakout_signal: bool
) -> Dict[str, Any]:
    """
    技术维度评分
    
    Args:
        price_momentum: 价格动量（近5日/10日累计涨幅，%）
        volume_momentum: 成交量动量（量比，当前成交量/平均成交量）
        trend_strength: 趋势强度（0-1，1表示最强趋势）
        breakout_signal: 突破信号（True表示出现突破）
    
    Returns:
        包含评分和详细信息的字典
    """
    score = 0.0
    details = {}
    
    # 1. 价格动量评分（0-30分）
    if price_momentum >= 15:
        price_score = 30
    elif price_momentum >= 10:
        price_score = 25
    elif price_momentum >= 5:
        price_score = 20
    elif price_momentum >= 0:
        price_score = 12
    else:
        price_score = max(0, 12 + price_momentum * 2)
    
    score += price_score
    details['price_score'] = round(price_score, 2)
    details['price_momentum'] = price_momentum
    
    # 2. 成交量动量评分（0-25分）
    if volume_momentum >= 2.0:
        volume_score = 25
    elif volume_momentum >= 1.5:
        volume_score = 20
    elif volume_momentum >= 1.2:
        volume_score = 15
    elif volume_momentum >= 1.0:
        volume_score = 10
    else:
        volume_score = max(0, 10 + (volume_momentum - 1.0) * 20)
    
    score += volume_score
    details['volume_score'] = round(volume_score, 2)
    details['volume_momentum'] = volume_momentum
    
    # 3. 趋势强度评分（0-25分）
    if trend_strength >= 0.8:
        trend_score = 25
    elif trend_strength >= 0.6:
        trend_score = 20
    elif trend_strength >= 0.4:
        trend_score = 15
    elif trend_strength >= 0.2:
        trend_score = 10
    else:
        trend_score = max(0, trend_strength * 50)
    
    score += trend_score
    details['trend_score'] = round(trend_score, 2)
    details['trend_strength'] = trend_strength
    
    # 4. 突破信号评分（0-20分）
    breakout_score = 20 if breakout_signal else 0
    score += breakout_score
    details['breakout_score'] = breakout_score
    details['breakout_signal'] = breakout_signal
    
    return {
        'technical_score': round(score, 2),
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
