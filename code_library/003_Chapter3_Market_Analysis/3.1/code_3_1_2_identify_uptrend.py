import pandas as pd
import numpy as np
from typing import Union

def identify_uptrend(data: pd.DataFrame, 
                    sma_short: int = 5,
                    sma_long: int = 20) -> pd.Series:
    """
    识别上升趋势
    
    **设计原理**：
    - **多条件综合**：综合多个技术指标，提高识别准确性
    - **条件权重**：至少满足3个条件才判断为上升趋势
    - **技术指标融合**：结合均线、MACD、价格形态等多个维度
    
    **为什么这样设计**：
    1. **准确性**：单一指标可能失效，多指标综合更可靠
    2. **稳健性**：至少满足3个条件，避免假信号
    3. **全面性**：从多个维度判断趋势，更全面
    
    **使用场景**：
    - 趋势跟踪策略中，识别上升趋势
    - 买入信号生成时，确认上升趋势
    - 风险控制时，在上升趋势中持有
    
    **注意事项**：
    - 在震荡市中可能产生假信号
    - 需要结合其他分析方法确认
    - 参数需要根据市场特性调整
    
    Args:
        data: 价格数据
        sma_short: 短期均线周期
        sma_long: 长期均线周期
    
    Returns:
        布尔序列，True表示上升趋势
    """
    from core.market_analysis.trend_analysis import calculate_sma, calculate_macd
    
    # 设计原理：计算短期和长期均线
    # 原因：均线排列是判断趋势的基础
    # 为什么这样设计：短期均线在长期均线上方是上升趋势的典型特征
    sma_short_line = calculate_sma(data, period=sma_short)
    sma_long_line = calculate_sma(data, period=sma_long)
    
    # 设计原理：条件1 - 短期均线在长期均线上方
    # 原因：这是多头排列的基础，反映上升趋势
    # 为什么这样设计：均线排列是技术分析的基础判断
    condition1 = sma_short_line > sma_long_line
    
    # 设计原理：条件2 - 价格在短期均线上方
    # 原因：价格在均线上方，说明趋势向上
    # 为什么这样设计：价格与均线的关系反映趋势强度
    condition2 = data['close'] > sma_short_line
    
    # 设计原理：条件3 - MACD金叉或DIF在DEA上方
    # 原因：MACD反映价格动量，DIF在DEA上方表示上升动量
    # 为什么这样设计：MACD是重要的趋势确认指标
    macd_data = calculate_macd(data)
    condition3 = macd_data['DIF'] > macd_data['DEA']
    
    # 设计原理：条件4 - 价格低点逐步抬高
    # 原因：低点逐步抬高是上升趋势的典型特征
    # 为什么这样设计：价格形态是趋势判断的重要依据
    lows = data['low'].rolling(window=3).min()
    condition4 = lows.diff() > 0
    
    # 设计原理：综合判断 - 至少满足3个条件
    # 原因：单一条件可能失效，多条件综合更可靠
    # 为什么这样设计：提高识别准确性，减少假信号
    uptrend = (condition1.astype(int) + 
               condition2.astype(int) + 
               condition3.astype(int) + 
               condition4.astype(int)) >= 3
    
    return uptrend

