"""
文件名: code_5_2_filter_fundamental.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.2/code_5_2_filter_fundamental.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: filter_fundamental

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_fundamental(
    stocks: List[str],
    date: str = None,
    min_roe: float = 0.10,           # 最小ROE
    min_profit_growth: float = 0.30, # 最小净利润增长率
    min_revenue_growth: float = 0.20 # 最小营收增长率
) -> List[str]:
        """
    filter_fundamental函数
    
    **设计原理**：
    - **核心功能**：实现filter_fundamental的核心逻辑
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
    
    # 批量获取财务数据
    batch_size = 1000
    for i in range(0, len(stocks), batch_size):
        batch = stocks[i:i + batch_size]
        
        try:
            # 获取财务指标
            fundamental_data = get_fundamental_data(batch, date=date)
            
            for stock_code in batch:
                if stock_code not in fundamental_data:
                    continue
                
                data = fundamental_data[stock_code]
                
                # 检查ROE
                roe = data.get("roe", 0)
                if roe < min_roe:
                    continue
                
                # 检查净利润增长率
                profit_growth = data.get("profit_growth", 0)
                if profit_growth < min_profit_growth:
                    continue
                
                # 检查营收增长率
                revenue_growth = data.get("revenue_growth", 0)
                if revenue_growth < min_revenue_growth:
                    continue
                
                filtered.append(stock_code)
        
        except Exception as e:
            logger.warning(f"获取财务数据失败: {e}")
            continue
    
    return filtered