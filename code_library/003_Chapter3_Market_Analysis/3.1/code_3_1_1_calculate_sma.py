import pandas as pd
import numpy as np
from typing import Union

def calculate_sma(data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
    """
    计算简单移动平均线（SMA）
    
    **设计原理**：
    - **平滑价格波动**：通过计算N个周期的平均值，平滑价格波动，识别趋势方向
    - **滞后性**：SMA是滞后指标，反映历史价格的平均水平
    - **参数可配置**：周期参数可配置，适应不同时间尺度的趋势分析
    
    **为什么这样设计**：
    1. **趋势识别**：移动平均线是趋势分析的基础，能有效识别趋势方向
    2. **平滑噪声**：通过平均计算，过滤短期价格波动，突出长期趋势
    3. **通用性**：SMA是最基础的技术指标，被广泛使用和验证
    
    **使用场景**：
    - 趋势识别：通过多条SMA的排列判断趋势方向
    - 支撑阻力：SMA可以作为动态支撑阻力位
    - 交易信号：价格与SMA的关系产生交易信号
    
    **注意事项**：
    - SMA是滞后指标，不能预测未来，只能反映历史趋势
    - 周期越长，滞后性越强，但稳定性越好
    - 在震荡市中，SMA可能产生假信号
    
    Args:
        data: 价格数据DataFrame，必须包含close列
        period: 周期（默认20）
        column: 计算列名（默认'close'）
    
    Returns:
        SMA序列
    """
    # 设计原理：使用pandas的rolling方法计算移动平均
    # 原因：rolling方法高效且支持向量化计算，性能好
    # min_periods=1：即使数据不足period个，也计算可用数据的平均值
    # 为什么这样设计：确保即使数据不足也能得到结果，提高鲁棒性
    return data[column].rolling(window=period, min_periods=1).mean()

