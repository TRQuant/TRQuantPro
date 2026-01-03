import pandas as pd
import numpy as np
from typing import Union

def calculate_bollinger_bands(data: pd.DataFrame, 
                              period: int = 20, 
                              std_dev: float = 2.0,
                              column: str = 'close') -> pd.DataFrame:
    """
    计算布林带（Bollinger Bands）
    
    **设计原理**：
    - **动态通道**：布林带是动态的价格通道，随价格波动调整
    - **标准差原理**：使用标准差衡量价格波动，上轨和下轨距离中轨的标准差倍数
    - **波动性指标**：布林带宽度反映市场波动性，宽度越大波动越大
    
    **为什么这样设计**：
    1. **相对位置**：布林带能识别价格在波动区间中的相对位置
    2. **波动性测量**：布林带宽度反映市场波动性，是重要的风险指标
    3. **交易信号**：价格触及上下轨可能产生交易信号
    
    **使用场景**：
    - 超买超卖判断：价格触及上轨可能超买，触及下轨可能超卖
    - 波动性分析：布林带宽度反映市场波动性
    - 趋势确认：价格沿中轨运行，确认趋势方向
    
    **注意事项**：
    - 在强趋势中，价格可能长期沿上轨或下轨运行
    - 布林带不能预测价格方向，只能反映相对位置
    - 参数需要根据市场特性调整
    
    Args:
        data: 价格数据DataFrame
        period: 周期（默认20）
        std_dev: 标准差倍数（默认2.0）
        column: 计算列名（默认'close'）
    
    Returns:
        DataFrame包含upper、middle、lower三列
    """
    # 导入SMA计算函数
    from core.market_analysis.trend_analysis import calculate_sma
    
    # 设计原理：中轨 = SMA
    # 原因：中轨是价格的平均水平，使用SMA计算
    # 为什么这样设计：SMA是价格的平均水平，适合作为中轨
    sma = calculate_sma(data, period=period, column=column)
    
    # 设计原理：计算标准差
    # 原因：标准差反映价格波动性，用于计算上下轨
    # 为什么这样设计：标准差是衡量波动性的标准方法
    std = data[column].rolling(window=period).std()
    
    # 设计原理：上轨 = 中轨 + 标准差 * 倍数
    # 原因：上轨是中轨加上一定倍数的标准差，反映价格上限
    # 为什么这样设计：标准差倍数通常为2，覆盖约95%的价格波动
    upper = sma + (std * std_dev)
    
    # 设计原理：下轨 = 中轨 - 标准差 * 倍数
    # 原因：下轨是中轨减去一定倍数的标准差，反映价格下限
    # 为什么这样设计：与上轨对称，形成价格通道
    lower = sma - (std * std_dev)
    
    return pd.DataFrame({
        'upper': upper,
        'middle': sma,
        'lower': lower
    })

