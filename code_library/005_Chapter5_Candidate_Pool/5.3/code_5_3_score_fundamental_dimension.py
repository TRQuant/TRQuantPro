"""
文件名: code_5_3_score_fundamental_dimension.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_score_fundamental_dimension.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: score_fundamental_dimension

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def score_fundamental_dimension(
    stock_code: str,
    financial_data: Dict,
    valuation_data: Dict
) -> float:
        """
    score_fundamental_dimension函数
    
    **设计原理**：
    - **核心功能**：实现score_fundamental_dimension的核心逻辑
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
    
    # 1. 盈利能力评分（0-35分）
    roe = financial_data.get('roe', 0)  # ROE（%）
    roa = financial_data.get('roa', 0)  # ROA（%）
    net_profit_margin = financial_data.get('net_profit_margin', 0)  # 净利润率（%）
    
    # 盈利能力评分
    profit_score = 0
    if roe > 20:
        profit_score += 12
    elif roe > 15:
        profit_score += 10
    elif roe > 10:
        profit_score += 8
    else:
        profit_score += max(0, roe / 10 * 8)
    
    if roa > 10:
        profit_score += 12
    elif roa > 7:
        profit_score += 10
    elif roa > 5:
        profit_score += 8
    else:
        profit_score += max(0, roa / 5 * 8)
    
    if net_profit_margin > 20:
        profit_score += 11
    elif net_profit_margin > 15:
        profit_score += 9
    elif net_profit_margin > 10:
        profit_score += 7
    else:
        profit_score += max(0, net_profit_margin / 10 * 7)
    
    profit_score = min(35, profit_score)
    
    # 2. 成长性评分（0-35分）
    revenue_growth = financial_data.get('revenue_growth', 0)  # 营收增速（%）
    profit_growth = financial_data.get('profit_growth', 0)  # 净利润增速（%）
    revenue_quality = financial_data.get('revenue_quality', 0)  # 营收质量（0-1）
    
    # 成长性评分
    growth_score = 0
    if revenue_growth > 30:
        growth_score += 12
    elif revenue_growth > 20:
        growth_score += 10
    elif revenue_growth > 10:
        growth_score += 8
    else:
        growth_score += max(0, revenue_growth / 10 * 8)
    
    if profit_growth > 50:
        growth_score += 12
    elif profit_growth > 30:
        growth_score += 10
    elif profit_growth > 20:
        growth_score += 8
    else:
        growth_score += max(0, profit_growth / 20 * 8)
    
    growth_score += revenue_quality * 11
    growth_score = min(35, growth_score)
    
    # 3. 估值水平评分（0-20分）
    pe = valuation_data.get('pe', 0)  # PE
    pb = valuation_data.get('pb', 0)  # PB
    peg = valuation_data.get('peg', 0)  # PEG
    
    # 估值水平评分（估值越低，评分越高）
    valuation_score = 0
    if 10 <= pe <= 25:
        valuation_score += 7
    elif 5 <= pe < 10 or 25 < pe <= 40:
        valuation_score += 5
    elif pe < 5 or 40 < pe <= 60:
        valuation_score += 3
    else:
        valuation_score += max(0, 7 - abs(pe - 20) / 10)
    
    if 1 <= pb <= 3:
        valuation_score += 7
    elif 0.5 <= pb < 1 or 3 < pb <= 5:
        valuation_score += 5
    else:
        valuation_score += max(0, 7 - abs(pb - 2) / 0.5)
    
    if 0.5 <= peg <= 1.5:
        valuation_score += 6
    elif 0.3 <= peg < 0.5 or 1.5 < peg <= 2:
        valuation_score += 4
    else:
        valuation_score += max(0, 6 - abs(peg - 1) / 0.5)
    
    valuation_score = min(20, valuation_score)
    
    # 4. 财务健康评分（0-10分）
    debt_ratio = financial_data.get('debt_ratio', 0)  # 负债率（%）
    cash_flow = financial_data.get('cash_flow', 0)  # 经营现金流（万元）
    asset_quality = financial_data.get('asset_quality', 0)  # 资产质量（0-1）
    
    # 财务健康评分
    health_score = 0
    if debt_ratio < 30:
        health_score += 4
    elif debt_ratio < 50:
        health_score += 3
    elif debt_ratio < 70:
        health_score += 2
    else:
        health_score += max(0, 4 - (debt_ratio - 30) / 10)
    
    if cash_flow > 0:
        health_score += 3
    elif cash_flow > -10000:
        health_score += 2
    else:
        health_score += 1
    
    health_score += asset_quality * 3
    health_score = min(10, health_score)
    
    score = profit_score + growth_score + valuation_score + health_score
    return min(100, max(0, score))