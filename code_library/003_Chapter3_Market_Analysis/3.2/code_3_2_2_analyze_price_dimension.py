from typing import Dict
import pandas as pd

def analyze_price_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析价格维度
    
    **设计原理**：
    - **多周期分析**：同时分析1日、5日、20日涨跌幅，提供不同时间尺度的价格变化
    - **相对位置**：计算价格在近期高低点之间的相对位置，反映价格水平
    - **趋势强度**：通过移动平均线斜率判断价格趋势，反映趋势强度
    
    **为什么这样设计**：
    1. **全面性**：多周期分析提供全面的价格变化信息
    2. **相对性**：相对位置比绝对价格更有意义，便于不同时期对比
    3. **趋势性**：趋势强度反映价格变化的方向和速度
    
    **使用场景**：
    - 市场状态判断时，分析价格维度
    - 策略生成时，根据价格维度选择策略类型
    - 风险控制时，根据价格位置调整仓位
    
    Args:
        data: 市场数据
    
    Returns:
        价格维度评分字典
    """
    # 设计原理：多周期涨跌幅计算
    # 原因：不同周期的涨跌幅反映不同时间尺度的价格变化
    # 1日：短期波动，反映当日市场情绪
    # 5日：中期变化，反映一周市场走势
    # 20日：长期趋势，反映一个月市场方向
    price_change_1d = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]
    price_change_5d = (data['close'].iloc[-1] - data['close'].iloc[-6]) / data['close'].iloc[-6]
    price_change_20d = (data['close'].iloc[-1] - data['close'].iloc[-21]) / data['close'].iloc[-21]
    
    # 设计原理：价格相对位置计算
    # 原因：相对位置比绝对价格更有意义，反映价格在近期区间的位置
    # 公式：位置 = (当前价格 - 最低价) / (最高价 - 最低价)
    # 取值范围：0-1，0表示最低点，1表示最高点
    # 为什么这样设计：便于判断价格是否处于高位或低位，指导交易决策
    recent_high = data['high'].tail(20).max()
    recent_low = data['low'].tail(20).min()
    price_position = (data['close'].iloc[-1] - recent_low) / (recent_high - recent_low)
    
    # 设计原理：价格趋势强度计算
    # 原因：移动平均线斜率反映价格趋势的方向和强度
    # 公式：趋势 = (当前MA - 5日前MA) / 5日前MA
    # 正值表示上升趋势，负值表示下降趋势，绝对值表示趋势强度
    # 为什么这样设计：趋势强度比趋势方向更有价值，强趋势更可靠
    from core.market_analysis.trend_analysis import calculate_sma
    sma_20 = calculate_sma(data, period=20)
    price_trend = (sma_20.iloc[-1] - sma_20.iloc[-5]) / sma_20.iloc[-5]
    
    # 验证测试：添加新的返回值
    result = {
        'price_change_1d': price_change_1d,
        'price_change_5d': price_change_5d,
        'price_change_20d': price_change_20d,
        'price_position': price_position,
        'price_trend': price_trend,
        'test_field': '这是验证自动更新的测试字段'  # 新增字段用于验证
    }
    
    return result

