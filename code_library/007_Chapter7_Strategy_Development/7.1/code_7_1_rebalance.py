"""
文件名: code_7_1_rebalance.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.1/code_7_1_rebalance.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.1_Strategy_Template_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: rebalance

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

MARKET_NEUTRAL_TEMPLATE = {
    'trading_logic': '''def rebalance(context):
        """
    rebalance函数
    
    **设计原理**：
    - **核心功能**：实现rebalance的核心逻辑
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
    # 获取因子数据
    factor_data = get_factor_values(
        context.universe,
        context.factors,
        end_date=context.current_dt.strftime('%Y-%m-%d'),
        count=1
    )
    
    if factor_data is None:
        return
    
    # 计算综合得分
    scores = pd.DataFrame(index=context.universe)
    for factor in context.factors:
        if factor in factor_data:
            values = factor_data[factor].iloc[-1]
            scores[factor] = (values - values.mean()) / values.std()
    
    scores['composite'] = scores.mean(axis=1)
    scores = scores.dropna()
    
    # 多头：得分最高的股票
    long_stocks = scores.nlargest(context.max_stocks // 2, 'composite').index.tolist()
    
    # 空头：得分最低的股票（需要融券）
    short_stocks = scores.nsmallest(context.max_stocks // 2, 'composite').index.tolist()
    
    log.info(f"多头: {long_stocks}")
    log.info(f"空头: {short_stocks}")
    
    # 执行多头
    long_weight = 0.5 / len(long_stocks) if long_stocks else 0
    for stock in long_stocks:
        order_target_percent(stock, long_weight)
    
    # 空头需要券商支持融券
    # 这里仅记录，实际执行需要配置融券账户
    log.info("空头部分需要融券支持")'''
}