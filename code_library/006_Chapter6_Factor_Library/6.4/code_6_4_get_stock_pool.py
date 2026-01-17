"""
文件名: code_6_4_get_stock_pool.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4_get_stock_pool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: get_stock_pool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def get_stock_pool(self, date: Union[str, datetime]) -> List[str]:
        """
    get_stock_pool函数
    
    **设计原理**：
    - **核心功能**：实现get_stock_pool的核心逻辑
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
    if self.jq_client is None:
        raise ValueError("需要JQData客户端")
    
    import jqdatasdk as jq
    
    if self.stock_pool == "hs300":
        return jq.get_index_stocks("000300.XSHG", date=date)
    elif self.stock_pool == "zz500":
        return jq.get_index_stocks("000905.XSHG", date=date)
    elif self.stock_pool == "zz1000":
        return jq.get_index_stocks("000852.XSHG", date=date)
    else:  # all_a
        securities = jq.get_all_securities(types=["stock"], date=date)
        return securities.index.tolist()