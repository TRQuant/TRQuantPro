"""
文件名: code_7_1_initialize.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_initialize.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: initialize

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def initialize(context):
        """
    initialize函数
    
    **设计原理**：
    - **核心功能**：实现initialize的核心逻辑
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
    # 必须调用
    set_benchmark('000300.XSHG')
    
    # 可选配置
    set_slippage(PriceRelatedSlippage(0.002))
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 策略参数初始化
    context.params = {
        'max_position': 0.1,
        'stop_loss': 0.08,
        'take_profit': 0.2
    }
    
    # 定时任务
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')