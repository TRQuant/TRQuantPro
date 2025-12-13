from typing import Dict
import pandas as pd

def analyze_volume_dimension(data: pd.DataFrame) -> Dict[str, float]:
    """
    分析成交量维度
    
    **设计原理**：
    - **成交量变化**：分析不同周期的成交量变化，反映资金流向
    - **量价关系**：分析价格与成交量的配合关系，判断趋势强度
    - **成交量趋势**：分析成交量的趋势方向，判断资金持续性
    
    **为什么这样设计**：
    1. **资金流向**：成交量变化反映资金流入流出，是市场情绪的重要指标
    2. **趋势确认**：量价配合确认趋势强度，量价背离提示趋势可能反转
    3. **持续性**：成交量趋势反映资金持续性，持续放量更可靠
    
    **使用场景**：
    - 市场状态判断时，分析成交量维度
    - 策略生成时，根据量价关系选择策略类型
    - 风险控制时，根据成交量变化调整仓位
    
    Args:
        data: 市场数据
    
    Returns:
        成交量维度评分字典
    """
    # 设计原理：多周期成交量变化计算
    # 原因：不同周期的成交量变化反映不同时间尺度的资金流向
    # 1日：短期资金流向，反映当日资金情绪
    # 5日：中期资金流向，反映一周资金趋势
    volume_change_1d = (data['volume'].iloc[-1] - data['volume'].iloc[-2]) / data['volume'].iloc[-2]
    volume_change_5d = (data['volume'].tail(5).mean() - data['volume'].tail(10).head(5).mean()) / \
                      data['volume'].tail(10).head(5).mean()
    
    # 设计原理：量价关系分析
    # 原因：量价关系反映市场资金流向和趋势强度
    # 量价配合：价格上涨 + 成交量放大 = 强势（资金认可，趋势可持续）
    # 量价背离：价格上涨 + 成交量萎缩 = 弱势（资金不认可，趋势不可持续）
    # 为什么这样设计：量价配合是技术分析的核心，反映市场真实意图
    # 评分逻辑：配合时得1.0分（强势），背离时得0.5分（弱势）
    price_change = (data['close'].iloc[-1] - data['close'].iloc[-2]) / data['close'].iloc[-2]
    volume_ratio = data['volume'].iloc[-1] / data['volume'].tail(20).mean()
    price_volume_match = 1.0 if (price_change > 0 and volume_ratio > 1.0) or \
                              (price_change < 0 and volume_ratio < 1.0) else 0.5
    
    # 设计原理：成交量趋势计算
    # 原因：成交量趋势反映资金持续性，持续放量更可靠
    # 公式：趋势 = (近期平均成交量 - 前期平均成交量) / 前期平均成交量
    # 正值表示成交量上升，负值表示成交量下降
    volume_trend = (data['volume'].tail(5).mean() - data['volume'].tail(10).head(5).mean()) / \
                   data['volume'].tail(10).head(5).mean()
    
    return {
        'volume_change_1d': volume_change_1d,
        'volume_change_5d': volume_change_5d,
        'volume_ratio': volume_ratio,
        'price_volume_match': price_volume_match,
        'volume_trend': volume_trend
    }

