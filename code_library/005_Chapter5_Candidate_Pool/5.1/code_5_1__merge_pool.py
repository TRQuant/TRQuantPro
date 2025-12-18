"""
文件名: code_5_1__merge_pool.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.1/code_5_1__merge_pool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: _merge_pool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def _merge_pool(self, source_pool: StockPool, source_name: str):
        """
    _merge_pool函数
    
    **设计原理**：
    - **核心功能**：实现_merge_pool的核心逻辑
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
    added = 0
    for stock in source_pool.stocks:
        if self.current_pool.add_stock(stock):
            added += 1
    logger.info(f"合并 {source_name}：新增 {added} 只，已存在 {len(source_pool.stocks) - added} 只")