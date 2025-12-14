"""
文件名: code_5_2_filter_by_liquidity.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.2/code_5_2_filter_by_liquidity.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: filter_by_liquidity

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_by_liquidity(
    stocks: List[str],
    date: str = None,
    min_turnover: float = 0.01,  # 最小换手率
    min_volume: float = 1000000   # 最小成交量（手）
) -> List[str]:
        """
    filter_by_liquidity函数
    
    **设计原理**：
    - **核心功能**：实现filter_by_liquidity的核心逻辑
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
    filtered = []
    
    for stock_code in stocks:
        # 获取成交量和换手率
        market_data = get_market_data(stock_code, date=date)
        if market_data.empty:
            continue
        
        volume = market_data['volume'].iloc[-1]
        turnover = market_data.get('turnover', 0)
        
        # 检查流动性
        if volume >= min_volume and turnover >= min_turnover:
            filtered.append(stock_code)
    
    return filtered