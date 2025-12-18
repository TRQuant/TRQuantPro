"""
文件名: code_5_1_create_base_pool.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.1/code_5_1_create_base_pool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: create_base_pool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def create_base_pool(
    pool_type: str = "all_market",
    universe: str = "all"
) -> StockPool:
        """
    create_base_pool函数
    
    **设计原理**：
    - **核心功能**：实现create_base_pool的核心逻辑
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
    pool = StockPool(
        description=f"{pool_type}股票池 - {universe}"
    )
    
    if pool_type == "all_market":
        # 获取全市场股票
        stocks = get_all_stocks(universe=universe)
    elif pool_type == "industry":
        # 获取行业股票
        stocks = get_industry_stocks(universe=universe)
    elif pool_type == "sector":
        # 获取板块股票
        stocks = get_sector_stocks(universe=universe)
    
    for stock_code in stocks:
        stock_info = get_stock_info(stock_code)
        item = StockPoolItem(
            code=stock_code,
            name=stock_info.get("name", ""),
            industry=stock_info.get("industry", ""),
            source="base",
            entry_reason=f"{pool_type}基础股票池"
        )
        pool.add_stock(item)
    
    pool.calculate_summary()
    return pool