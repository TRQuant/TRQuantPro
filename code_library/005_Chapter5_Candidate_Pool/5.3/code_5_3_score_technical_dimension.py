"""
文件名: code_5_3_score_technical_dimension.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_score_technical_dimension.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: score_technical_dimension

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def score_technical_dimension(
    stock_code: str,
    price_data: pd.DataFrame,
    volume_data: pd.DataFrame,
    date: str
) -> float:
    """
    技术面评分
    
    Args:
        stock_code: 股票代码
        price_data: 价格数据（包含open, high, low, close）
        volume_data: 成交量数据
        date: 评分日期
    
    Returns:
        技术面评分（0-100分）
    """
    score = 0.0
    
    # 1. 价格趋势评分（0-40分）
    # 计算价格动量（20日收益率）
    returns_20d = (price_data['close'].iloc[-1] / price_data['close'].iloc[-21] - 1) * 100
    
    # 计算趋势强度（均线斜率）
    ma20 = price_data['close'].rolling(20).mean()
    ma60 = price_data['close'].rolling(60).mean()
    trend_strength = (ma20.iloc[-1] - ma20.iloc[-20]) / ma20.iloc[-20] * 100
    
    # 价格趋势评分
    if returns_20d > 20 and trend_strength > 5:
        trend_score = 40
    elif returns_20d > 10 and trend_strength > 2:
        trend_score = 35
    elif returns_20d > 5 and trend_strength > 0:
        trend_score = 30
    elif returns_20d > 0:
        trend_score = 25
    else:
        trend_score = max(0, 20 + returns_20d * 0.5)
    
    # 2. 成交量评分（0-30分）
    # 计算成交量放大倍数
    avg_volume_20d = volume_data['volume'].rolling(20).mean().iloc[-1]
    current_volume = volume_data['volume'].iloc[-1]
    volume_ratio = current_volume / avg_volume_20d if avg_volume_20d > 0 else 1
    
    # 成交量评分
    if volume_ratio > 3:
        volume_score = 30
    elif volume_ratio > 2:
        volume_score = 25
    elif volume_ratio > 1.5:
        volume_score = 20
    elif volume_ratio > 1:
        volume_score = 15
    else:
        volume_score = max(0, 10 + (volume_ratio - 0.5) * 10)
    
    # 3. 技术指标评分（0-20分）
    # 计算MACD、RSI、KDJ等指标
    macd_signal = calculate_macd_signal(price_data)
    rsi_value = calculate_rsi(price_data, period=14)
    kdj_signal = calculate_kdj_signal(price_data)
    
    # 技术指标评分
    indicator_score = 0
    if macd_signal == 'bullish':
        indicator_score += 7
    if 30 < rsi_value < 70:  # RSI在合理区间
        indicator_score += 7
    if kdj_signal == 'bullish':
        indicator_score += 6
    
    # 4. 突破信号评分（0-10分）
    # 检查是否站上均线
    current_price = price_data['close'].iloc[-1]
    ma20_current = ma20.iloc[-1]
    ma60_current = ma60.iloc[-1]
    
    breakthrough_score = 0
    if current_price > ma20_current and ma20_current > ma60_current:
        breakthrough_score = 10
    elif current_price > ma20_current:
        breakthrough_score = 7
    elif current_price > ma60_current:
        breakthrough_score = 5
    
    # 设计原理：技术面评分采用累加方式
    # 原因：多个技术指标综合评分，累加反映整体技术面强度
    # 评分维度：趋势强度、成交量、技术指标、突破信号
    # 为什么这样设计：单一指标可能误判，多指标综合更准确
    score = trend_score + volume_score + indicator_score + breakthrough_score
    
    # 设计原理：得分限制在0-100分
    # 原因：确保评分在合理范围内，便于后续比较和排序
    # 实现方式：使用min和max函数限制范围
    return min(100, max(0, score))