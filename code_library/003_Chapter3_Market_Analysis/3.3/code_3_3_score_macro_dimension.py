from typing import Dict, List, Optional

def score_macro_dimension(gdp_growth: float, cpi: float, pmi: float, 
                         monetary_policy: str) -> float:
    """
    score_macro_dimension函数
    
    **设计原理**：
    - **核心功能**：实现score_macro_dimension的核心逻辑
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
    
    # 1. GDP增速评分（0-30分）
    # 理想区间：5-7%
    if 5 <= gdp_growth <= 7:
        gdp_score = 30
    elif 4 <= gdp_growth < 5 or 7 < gdp_growth <= 8:
        gdp_score = 25
    elif 3 <= gdp_growth < 4 or 8 < gdp_growth <= 9:
        gdp_score = 20
    elif 2 <= gdp_growth < 3 or 9 < gdp_growth <= 10:
        gdp_score = 15
    else:
        gdp_score = max(0, 30 - abs(gdp_growth - 6) * 5)
    
    # 2. CPI评分（0-20分）
    # 理想区间：1.5-2.5%
    if 1.5 <= cpi <= 2.5:
        cpi_score = 20
    elif 1.0 <= cpi < 1.5 or 2.5 < cpi <= 3.0:
        cpi_score = 15
    elif 0.5 <= cpi < 1.0 or 3.0 < cpi <= 3.5:
        cpi_score = 10
    else:
        cpi_score = max(0, 20 - abs(cpi - 2.0) * 10)
    
    # 3. PMI评分（0-30分）
    # 50为荣枯线，>50表示扩张
    if pmi >= 52:
        pmi_score = 30
    elif 50 <= pmi < 52:
        pmi_score = 25
    elif 48 <= pmi < 50:
        pmi_score = 15
    elif 46 <= pmi < 48:
        pmi_score = 10
    else:
        pmi_score = max(0, (pmi - 40) * 1.5)
    
    # 4. 货币政策评分（0-20分）
    policy_scores = {
        'loose': 20,    # 宽松：利好市场
        'neutral': 15,  # 中性：中性
        'tight': 5      # 紧缩：利空市场
    }
    policy_score = policy_scores.get(monetary_policy, 10)
    
    score = gdp_score + cpi_score + pmi_score + policy_score
    return min(100, max(0, score))# 测试自动更新 - 08:37:11
