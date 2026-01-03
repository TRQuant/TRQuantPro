"""
文件名: code_7_1_init.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_init.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: init

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def init(ContextInfo):
        """
    init函数
    
    **设计原理**：
    - **核心功能**：实现init的核心逻辑
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
    # 策略参数
    ContextInfo.max_position = 0.1
    ContextInfo.stop_loss = 0.08
    ContextInfo.take_profit = 0.2
    
    # 股票池
    ContextInfo.universe = ContextInfo.get_stock_list_in_sector('沪深300')
    
    # 账号配置
    ContextInfo.accID = 'your_account_id'
    
    # 定时任务
    ContextInfo.run_time('rebalance', '09:35:00', 'SH')
    ContextInfo.run_time('risk_control', '14:50:00', 'SH')