"""
文件名: code_6_4_filter_stocks.py
保存路径: code_library/006_Chapter6_Factor_Library/6.4/code_6_4_filter_stocks.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.4_Factor_Pipeline_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: filter_stocks

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def filter_stocks(self, stocks: List[str], date: Union[str, datetime]) -> List[str]:
        """
    filter_stocks函数
    
    **设计原理**：
    - **核心功能**：实现filter_stocks的核心逻辑
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
        return stocks
    
    import jqdatasdk as jq
    
    filtered = []
    
    try:
        # 过滤ST
        st_info = jq.get_extras("is_st", stocks, end_date=date, count=1)
        if not st_info.empty:
            st_stocks = st_info.iloc[0][st_info.iloc[0] == True].index.tolist()
        else:
            st_stocks = []
        
        # 过滤停牌
        paused_info = jq.get_price(
            stocks, end_date=date, count=1, fields=["paused"], panel=False
        )
        if not paused_info.empty:
            paused_stocks = paused_info[paused_info["paused"] == 1]["code"].tolist()
        else:
            paused_stocks = []
        
        # 过滤上市不足N天的股票
        securities = jq.get_all_securities(types=["stock"], date=date)
        min_listing_days = 60  # 至少上市60天
        
        for stock in stocks:
            if stock in st_stocks:
                continue
            if stock in paused_stocks:
                continue
            
            # 检查上市时间
            if stock in securities.index:
                listing_date = securities.loc[stock, "start_date"]
                if isinstance(date, str):
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                else:
                    date_obj = date
                
                days_since_listing = (date_obj - listing_date).days
                if days_since_listing < min_listing_days:
                    continue
            
            filtered.append(stock)
        
        logger.info(f"股票过滤完成: {len(stocks)} -> {len(filtered)}")
        return filtered
    
    except Exception as e:
        logger.error(f"股票过滤失败: {e}")
        return stocks