import pandas as pd
import numpy as np
from typing import Union

def calculate_ema(data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
    """
    计算指数移动平均线（EMA）
    
    **设计原理**：
    - **加权平均**：对近期价格赋予更高权重，反应更灵敏
    - **指数衰减**：权重按指数衰减，越近期的价格权重越大
    - **快速响应**：相比SMA，EMA对价格变化反应更快
    
    **为什么这样设计**：
    1. **灵敏度**：EMA对价格变化反应更快，能更早捕捉趋势变化
    2. **权重分配**：指数衰减权重更符合市场心理，近期价格更重要
    3. **趋势跟踪**：EMA常用于趋势跟踪策略，能及时跟上趋势
    
    **使用场景**：
    - 趋势跟踪：EMA常用于趋势跟踪策略
    - MACD计算：EMA是MACD指标的基础
    - 交易信号：价格与EMA的关系产生交易信号
    
    **注意事项**：
    - EMA比SMA更敏感，可能产生更多假信号
    - 在震荡市中，EMA可能频繁交叉，产生噪音
    - 周期越短，灵敏度越高，但稳定性越差
    
    Args:
        data: 价格数据DataFrame
        period: 周期（默认20）
        column: 计算列名（默认'close'）
    
    Returns:
        EMA序列
    """
    # 设计原理：使用pandas的ewm方法计算指数移动平均
    # 原因：ewm方法专门用于指数加权移动平均，计算高效
    # span=period：指定衰减因子，span越大，衰减越慢
    # adjust=False：使用递归公式，计算更快
    # 为什么这样设计：EMA计算需要指数衰减，ewm方法是最优选择
    return data[column].ewm(span=period, adjust=False).mean()

