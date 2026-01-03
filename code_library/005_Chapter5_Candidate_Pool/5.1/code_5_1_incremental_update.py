"""
文件名: code_5_1_incremental_update.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.1/code_5_1_incremental_update.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.1_Stock_Pool_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: incremental_update

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def incremental_update(self, pool: StockPool):
        """
    incremental_update函数
    
    **设计原理**：
    - **核心功能**：实现incremental_update的核心逻辑
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
    # 获取最新数据
    new_pool = self.build_pool()
    
    # 找出新增和删除的股票
    existing_codes = set(pool.get_codes())
    new_codes = set(new_pool.get_codes())
    
    added_codes = new_codes - existing_codes
    removed_codes = existing_codes - new_codes
    
    # 更新股票池
    for code in added_codes:
        stock = new_pool.get_stock_by_code(code)
        pool.add_stock(stock)
    
    for code in removed_codes:
        pool.remove_stock(code)
    
    pool.updated_at = datetime.now().isoformat()
    pool.calculate_summary()