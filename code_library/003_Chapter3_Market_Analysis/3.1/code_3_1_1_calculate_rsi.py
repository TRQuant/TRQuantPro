import pandas as pd
import numpy as np
from typing import Union

def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
    """
    计算RSI指标
    
    **设计原理**：
    - **相对强弱**：通过比较上涨和下跌的幅度，计算相对强弱指数
    - **超买超卖**：RSI值在0-100之间，70以上为超买，30以下为超卖
    - **动量指标**：RSI反映价格动量的强弱，能识别极端状态
    
    **为什么这样设计**：
    1. **极端识别**：RSI能识别超买超卖状态，提示可能的反转
    2. **动量测量**：通过涨跌幅度比较，量化价格动量
    3. **广泛应用**：RSI是最常用的超买超卖指标之一
    
    **使用场景**：
    - 超买超卖判断：RSI > 70超买，RSI < 30超卖
    - 背离分析：价格与RSI的背离提示趋势可能反转
    - 趋势确认：RSI与价格同向，确认趋势强度
    
    **注意事项**：
    - RSI在强趋势中可能长期处于超买/超卖状态
    - 需要结合其他指标使用，避免单一指标判断
    - 参数需要根据市场特性调整
    
    Args:
        data: 价格数据DataFrame
        period: 周期（默认14）
        column: 计算列名（默认'close'）
    
    Returns:
        RSI序列（0-100）
    """
    # 设计原理：计算价格变化
    # 原因：RSI基于价格变化计算，需要先计算价格差值
    # 为什么这样设计：价格变化是RSI计算的基础
    delta = data[column].diff()
    
    # 设计原理：分离上涨和下跌
    # 原因：RSI需要分别计算上涨和下跌的平均值
    # gain：上涨幅度（只保留正值）
    # loss：下跌幅度（只保留负值，转为正值）
    # 为什么这样设计：分别计算上涨和下跌，才能计算相对强弱
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # 设计原理：计算相对强弱比（RS）
    # 原因：RS = 平均上涨幅度 / 平均下跌幅度
    # RS值越大，上涨动量越强
    # 为什么这样设计：RS反映上涨和下跌的相对强度
    rs = gain / loss
    
    # 设计原理：计算RSI
    # 公式：RSI = 100 - (100 / (1 + RS))
    # 原因：将RS转换为0-100的指标，便于使用
    # 为什么这样设计：0-100的范围更直观，70以上超买，30以下超卖
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

