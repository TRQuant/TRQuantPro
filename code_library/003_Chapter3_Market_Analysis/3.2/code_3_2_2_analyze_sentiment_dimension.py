from typing import Dict
import pandas as pd

def analyze_sentiment_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析情绪维度
    
    **设计原理**：
    - **市场情绪指标**：通过价格波动、成交量变化等间接指标反映市场情绪
    - **情绪周期**：分析情绪的周期性变化，识别情绪拐点
    - **情绪强度**：量化情绪强度，判断市场情绪是否过度乐观或悲观
    
    **为什么这样设计**：
    1. **间接测量**：市场情绪难以直接测量，通过价格、成交量等间接指标反映
    2. **周期性**：市场情绪具有周期性，识别周期有助于判断市场状态
    3. **极端情绪**：极端情绪往往预示市场反转，是重要的交易信号
    
    **使用场景**：
    - 市场状态判断时，分析情绪维度
    - 策略生成时，根据情绪状态选择策略类型（情绪极端时反向操作）
    - 风险控制时，根据情绪强度调整仓位
    
    **注意事项**：
    - 情绪数据需要额外的数据源（如新闻情绪、社交媒体情绪等）
    - 当前实现基于价格和成交量的间接指标
    - 实际应用中建议结合外部情绪数据源
    
    Args:
        data: 市场数据
    
    Returns:
        情绪维度评分字典
    """
    # 设计原理：波动率作为情绪指标
    # 原因：高波动率通常反映市场情绪不稳定，低波动率反映情绪稳定
    # 计算：使用20日滚动标准差作为波动率指标
    # 为什么这样设计：波动率是市场情绪的重要间接指标，高波动率往往伴随恐慌或狂热
    volatility = data['close'].tail(20).std() / data['close'].tail(20).mean()
    
    # 设计原理：涨跌比作为情绪指标
    # 原因：连续上涨或下跌反映市场情绪的持续性
    # 计算：统计最近20日中上涨和下跌的天数比例
    # 为什么这样设计：连续上涨反映乐观情绪，连续下跌反映悲观情绪
    price_changes = data['close'].tail(20).diff()
    up_days = (price_changes > 0).sum()
    down_days = (price_changes < 0).sum()
    up_down_ratio = up_days / (down_days + 1)  # 避免除零
    
    # 设计原理：成交量异常作为情绪指标
    # 原因：异常放量通常反映市场情绪极端化（恐慌或狂热）
    # 计算：当前成交量与平均成交量的比值
    # 为什么这样设计：异常放量往往出现在情绪极端时，是重要的反转信号
    volume_ratio = data['volume'].iloc[-1] / data['volume'].tail(20).mean()
    volume_anomaly = abs(volume_ratio - 1.0)  # 偏离正常值的程度
    
    # 设计原理：价格位置作为情绪指标
    # 原因：价格处于极端位置时，市场情绪往往也处于极端状态
    # 计算：价格在近期高低点之间的相对位置
    # 为什么这样设计：高位往往伴随过度乐观，低位往往伴随过度悲观
    recent_high = data['high'].tail(20).max()
    recent_low = data['low'].tail(20).min()
    price_position = (data['close'].iloc[-1] - recent_low) / (recent_high - recent_low)
    # 极端位置：接近1（过度乐观）或接近0（过度悲观）
    sentiment_extreme = abs(price_position - 0.5) * 2  # 归一化到0-1
    
    # 综合情绪评分
    # 设计原理：综合多个情绪指标
    # 原因：单一指标可能不准确，综合多个指标更可靠
    # 评分逻辑：
    # - 波动率高 -> 情绪不稳定 -> 得分低
    # - 涨跌比极端 -> 情绪极端 -> 得分低
    # - 成交量异常 -> 情绪极端 -> 得分低
    # - 价格位置极端 -> 情绪极端 -> 得分低
    # 为什么这样设计：综合评分能更准确地反映市场情绪状态
    sentiment_score = 1.0 - min(volatility * 2, 1.0)  # 波动率越高，情绪越不稳定
    sentiment_score = sentiment_score * (1.0 - min(volume_anomaly * 0.5, 0.5))  # 成交量异常降低得分
    sentiment_score = sentiment_score * (1.0 - sentiment_extreme * 0.3)  # 极端位置降低得分
    
    return {
        'volatility': volatility,
        'up_down_ratio': up_down_ratio,
        'volume_anomaly': volume_anomaly,
        'price_position': price_position,
        'sentiment_extreme': sentiment_extreme,
        'sentiment_score': sentiment_score
    }

