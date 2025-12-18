"""
文件名: code_5_3_calculate_macd_signal.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_calculate_macd_signal.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: calculate_macd_signal

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def calculate_macd_signal(price_data: pd.DataFrame) -> str:
        """
    calculate_macd_signal函数
    
    **设计原理**：
    - **核心功能**：实现calculate_macd_signal的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    ema12 = price_data['close'].ewm(span=12, adjust=False).mean()
    ema26 = price_data['close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    
    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        return 'bullish'  # 金叉
    elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
        return 'bearish'  # 死叉
    else:
        return 'neutral'

def calculate_rsi(price_data: pd.DataFrame, period: int = 14) -> float:
    """计算RSI指标"""
    delta = price_data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_kdj_signal(price_data: pd.DataFrame) -> str:
    """计算KDJ信号"""
    low_min = price_data['low'].rolling(9).min()
    high_max = price_data['high'].rolling(9).max()
    rsv = (price_data['close'] - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()
    j = 3 * k - 2 * d
    
    if k.iloc[-1] > d.iloc[-1] and k.iloc[-2] <= d.iloc[-2]:
        return 'bullish'  # K线上穿D线
    elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] >= d.iloc[-2]:
        return 'bearish'  # K线下穿D线
    else:
        return 'neutral'