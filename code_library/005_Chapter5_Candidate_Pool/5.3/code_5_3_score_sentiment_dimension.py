"""
文件名: code_5_3_score_sentiment_dimension.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_score_sentiment_dimension.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: score_sentiment_dimension

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def score_sentiment_dimension(
    stock_code: str,
    limit_data: Dict,
    lhb_data: Dict,
    market_sentiment: Dict
) -> float:
        """
    score_sentiment_dimension函数
    
    **设计原理**：
    - **核心功能**：实现score_sentiment_dimension的核心逻辑
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
    score = 0.0
    
    # 1. 涨跌停评分（0-50分）
    limit_up_count = limit_data.get('limit_up_count', 0)  # 涨停次数（近20日）
    limit_down_count = limit_data.get('limit_down_count', 0)  # 跌停次数（近20日）
    
    # 涨跌停评分
    if limit_up_count >= 3 and limit_down_count == 0:
        limit_score = 50
    elif limit_up_count >= 2 and limit_down_count == 0:
        limit_score = 40
    elif limit_up_count >= 1 and limit_down_count == 0:
        limit_score = 30
    elif limit_up_count > limit_down_count:
        limit_score = 20
    elif limit_down_count == 0:
        limit_score = 15
    else:
        limit_score = max(0, 10 - limit_down_count * 5)
    
    # 2. 龙虎榜评分（0-30分）
    lhb_count = lhb_data.get('count', 0)  # 上榜次数（近20日）
    speculator_ratio = lhb_data.get('speculator_ratio', 0)  # 游资参与度（0-1）
    
    # 龙虎榜评分
    if lhb_count >= 3 and speculator_ratio > 0.5:
        lhb_score = 30
    elif lhb_count >= 2 and speculator_ratio > 0.3:
        lhb_score = 25
    elif lhb_count >= 1:
        lhb_score = 20
    else:
        lhb_score = 10
    
    # 3. 市场情绪评分（0-20分）
    market_heat = market_sentiment.get('heat', 0)  # 市场热度（0-1）
    capital_sentiment = market_sentiment.get('capital_sentiment', 0)  # 资金情绪（0-1）
    
    # 市场情绪评分
    sentiment_score = (market_heat * 0.6 + capital_sentiment * 0.4) * 20
    
    score = limit_score + lhb_score + sentiment_score
    return min(100, max(0, score))