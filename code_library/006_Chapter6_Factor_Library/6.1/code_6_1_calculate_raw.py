"""
文件名: code_6_1_calculate_raw.py
保存路径: code_library/006_Chapter6_Factor_Library/6.1/code_6_1_calculate_raw.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.1_Factor_Calculation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: calculate_raw

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class IlliquidityFactor(BaseFactor):
    """
    非流动性因子（Amihud ILLIQ）
    
    公式: ILLIQ = |收益率| / 成交额
    
    经济学逻辑：
    - 反映价格冲击程度
    - 高ILLIQ表示流动性差
    
    A股实证：
    - 低非流动性股票表现更好
    - 是重要的流动性指标
    """
    
    name = "Illiquidity"
    category = "liquidity"
    description = "非流动性因子"
    direction = -1  # 非流动性越低越好
    
    def calculate_raw(self, stocks: List[str], date: Union[str, datetime], **kwargs) -> pd.Series:
            """
    calculate_raw函数
    
    **设计原理**：
    - **核心功能**：实现calculate_raw的核心逻辑
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
        
        try:
            import jqdatasdk as jq
            
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d")
            
            # 获取历史价格和成交额
            lookback_days = kwargs.get("lookback_days", 20)
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=lookback_days + 5,
                fields=["close", "money"],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            illiquidity_dict = {}
            
            for stock in stocks:
                stock_data = prices[prices["code"] == stock]
                
                if len(stock_data) < 10:
                    illiquidity_dict[stock] = np.nan
                    continue
                
                # 计算日收益率
                returns = stock_data["close"].pct_change().dropna()
                
                # 计算成交额
                money = stock_data["money"].iloc[1:]  # 对齐收益率
                
                # 计算ILLIQ（取平均）
                illiq = (abs(returns) / money).mean()
                
                # 负号：低非流动性得高分
                illiquidity_dict[stock] = -illiq
            
            result = pd.Series(illiquidity_dict)
            logger.info(f"非流动性因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
        
        except Exception as e:
            logger.error(f"非流动性因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)