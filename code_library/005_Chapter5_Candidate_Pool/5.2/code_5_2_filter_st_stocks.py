"""
文件名: code_5_2_filter_st_stocks.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.2/code_5_2_filter_st_stocks.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: filter_st_stocks

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_st_stocks(stocks: List[str], date: str = None) -> List[str]:
        """
    filter_st_stocks函数
    
    **设计原理**：
    - **核心功能**：实现filter_st_stocks的核心逻辑
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
        # 检查是否为ST股票
        stock_info = get_stock_info(stock_code, date=date)
        
        # ST股票通常名称包含"ST"或"*ST"
        if stock_info and ("ST" in stock_info.get("name", "") or 
                          "*ST" in stock_info.get("name", "")):
            continue
        
        # 检查是否被ST处理
        if stock_info and stock_info.get("is_st", False):
            continue
        
        filtered.append(stock_code)
    
    return filtered