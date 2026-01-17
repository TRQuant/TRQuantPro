from typing import Dict
import pandas as pd

def analyze_technical_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析技术维度
    
    **设计原理**：
    - **多指标综合**：综合使用移动平均线、MACD、RSI、布林带等多个技术指标
    - **趋势确认**：多个指标相互确认，提高判断准确性
    - **指标权重**：不同指标在不同市场环境下权重不同
    
    **为什么这样设计**：
    1. **全面性**：单一指标可能失效，多指标综合更可靠
    2. **确认机制**：多个指标同时指向同一方向时，信号更可靠
    3. **适应性**：不同指标适应不同市场环境，综合使用更稳健
    
    **使用场景**：
    - 市场状态判断时，分析技术维度
    - 策略生成时，根据技术指标选择策略类型
    - 风险控制时，根据技术指标调整仓位
    
    Args:
        data: 市场数据
    
    Returns:
        技术维度评分字典
    """
    from core.market_analysis.trend_analysis import (
        calculate_sma, calculate_ema, calculate_macd, 
        calculate_rsi, calculate_bollinger_bands
    )
    
    # 设计原理：移动平均线排列
    # 原因：移动平均线排列反映市场趋势方向
    # 多头排列（短期>中期>长期）：上升趋势，得分1.0
    # 空头排列（短期<中期<长期）：下降趋势，得分-1.0
    # 纠缠状态：震荡市，得分0.0
    # 为什么这样设计：移动平均线排列是技术分析的基础，反映趋势方向
    sma_5 = calculate_sma(data, period=5)
    sma_20 = calculate_sma(data, period=20)
    sma_60 = calculate_sma(data, period=60)
    
    ma_alignment = 0.0
    if sma_5.iloc[-1] > sma_20.iloc[-1] > sma_60.iloc[-1]:
        ma_alignment = 1.0  # 多头排列
    elif sma_5.iloc[-1] < sma_20.iloc[-1] < sma_60.iloc[-1]:
        ma_alignment = -1.0  # 空头排列
    
    # 设计原理：MACD指标
    # 原因：MACD反映价格动量的变化
    # DIF > DEA：上升动量，得分1.0
    # DIF < DEA：下降动量，得分-1.0
    # 为什么这样设计：MACD是重要的趋势指标，能提前反映趋势变化
    macd_data = calculate_macd(data)
    macd_signal = 1.0 if macd_data['DIF'].iloc[-1] > macd_data['DEA'].iloc[-1] else -1.0
    
    # 设计原理：RSI指标
    # 原因：RSI反映市场超买超卖状态
    # RSI > 70：超买，可能回调，得分负
    # RSI < 30：超卖，可能反弹，得分正
    # RSI在50附近：中性，得分0
    # 为什么这样设计：RSI是重要的超买超卖指标，能识别极端状态
    rsi = calculate_rsi(data, period=14)
    # 归一化到-1到1：RSI=50时为0，RSI>50为正，RSI<50为负
    rsi_score = (rsi.iloc[-1] - 50) / 50
    
    # 设计原理：布林带位置
    # 原因：布林带反映价格相对于波动区间的位置
    # 价格接近上轨：可能超买，得分负
    # 价格接近下轨：可能超卖，得分正
    # 价格在中轨附近：中性，得分0
    # 为什么这样设计：布林带能识别价格的相对位置，判断超买超卖
    bb = calculate_bollinger_bands(data)
    # 计算价格在布林带中的相对位置：-1（下轨）到1（上轨）
    bb_range = bb['upper'].iloc[-1] - bb['lower'].iloc[-1]
    if bb_range > 0:
        bb_position = (data['close'].iloc[-1] - bb['middle'].iloc[-1]) / (bb_range / 2)
        # 限制在-1到1之间
        bb_position = max(-1.0, min(1.0, bb_position))
    else:
        bb_position = 0.0
    
    # 设计原理：技术指标综合评分
    # 原因：综合多个技术指标，提高判断准确性
    # 评分逻辑：各指标加权平均
    # 为什么这样设计：单一指标可能失效，综合评分更可靠
    technical_score = (
        ma_alignment * 0.3 +  # 移动平均线权重30%
        macd_signal * 0.3 +  # MACD权重30%
        rsi_score * 0.2 +    # RSI权重20%
        bb_position * 0.2     # 布林带权重20%
    )
    
    return {
        'ma_alignment': ma_alignment,
        'macd_signal': macd_signal,
        'rsi_score': rsi_score,
        'bb_position': bb_position,
        'technical_score': technical_score
    }

