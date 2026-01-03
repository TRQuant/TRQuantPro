import pandas as pd
import numpy as np
from typing import Union

def calculate_macd(data: pd.DataFrame, 
                  fast_period: int = 12, 
                  slow_period: int = 26, 
                  signal_period: int = 9) -> pd.DataFrame:
    """
    计算MACD指标
    
    **设计原理**：
    - **趋势动量**：MACD通过快慢EMA的差值反映价格动量变化
    - **信号确认**：通过信号线（DEA）确认趋势变化
    - **多周期融合**：结合快线、慢线、信号线，提供多层次的趋势信息
    
    **为什么这样设计**：
    1. **动量识别**：MACD能识别价格动量的变化，提前反映趋势转折
    2. **信号确认**：信号线提供二次确认，减少假信号
    3. **广泛应用**：MACD是最常用的趋势指标之一，经过市场验证
    
    **使用场景**：
    - 趋势识别：MACD金叉/死叉识别趋势变化
    - 动量分析：MACD柱状图反映动量强弱
    - 背离分析：价格与MACD的背离提示趋势可能反转
    
    **注意事项**：
    - MACD是滞后指标，不能预测未来
    - 在震荡市中，MACD可能产生假信号
    - 参数需要根据市场特性调整
    
    Args:
        data: 价格数据DataFrame
        fast_period: 快线周期（默认12）
        slow_period: 慢线周期（默认26）
        signal_period: 信号线周期（默认9）
    
    Returns:
        DataFrame包含DIF、DEA、MACD三列
    """
    # 导入EMA计算函数
    from core.market_analysis.trend_analysis import calculate_ema
    
    # 设计原理：计算快线和慢线EMA
    # 原因：快慢EMA的差值反映价格动量的变化
    # 快线（12日）：反应短期趋势
    # 慢线（26日）：反应长期趋势
    # 为什么这样设计：快慢线的差值能捕捉趋势动量的变化
    ema_fast = calculate_ema(data, period=fast_period)
    ema_slow = calculate_ema(data, period=slow_period)
    
    # 设计原理：DIF = 快线 - 慢线
    # 原因：DIF反映快慢线的差值，正值表示上升动量，负值表示下降动量
    # 为什么这样设计：DIF是MACD的核心，反映价格动量的方向和强度
    dif = ema_fast - ema_slow
    
    # 设计原理：DEA = DIF的EMA（信号线）
    # 原因：信号线平滑DIF的波动，提供趋势确认
    # 为什么这样设计：信号线能过滤DIF的噪音，提供更可靠的信号
    dea = dif.ewm(span=signal_period, adjust=False).mean()
    
    # 设计原理：MACD = (DIF - DEA) * 2
    # 原因：MACD柱状图反映DIF与DEA的差值，放大信号强度
    # 乘以2是为了放大信号，使柱状图更明显
    # 为什么这样设计：MACD柱状图能直观反映动量强弱，便于观察
    macd = (dif - dea) * 2
    
    return pd.DataFrame({
        'DIF': dif,
        'DEA': dea,
        'MACD': macd
    })

