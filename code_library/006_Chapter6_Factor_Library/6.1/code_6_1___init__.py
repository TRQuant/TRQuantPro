"""
文件名: code_6_1___init__.py
保存路径: code_library/006_Chapter6_Factor_Library/6.1/code_6_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.1_Factor_Calculation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class VolatilityFactor(BaseFactor):
    """
    波动率因子
    
    公式: Volatility = 过去N日收益率标准差
    
    经济学逻辑：
    - 低波动率股票长期表现更好（低波动率异象）
    - 高波动率可能反映投机行为
    
    A股实证：
    - 低波动率效应在A股同样有效
    - 通常采用20-60日窗口
    """
    
    name = "Volatility"
    category = "volatility"
    description = "波动率因子"
    direction = -1  # 波动率越低越好
    
    def __init__(self, jq_client=None, lookback_days: int = 60, **kwargs):
        super().__init__(jq_client=jq_client, **kwargs)
        self.lookback_days = lookback_days
    
    def calculate_raw(self, stocks: List[str], date: Union[str, datetime], **kwargs) -> pd.Series:
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
            
            # 获取历史价格
            prices = jq.get_price(
                stocks,
                end_date=date,
                count=self.lookback_days + 5,
                fields=["close"],
                panel=False
            )
            
            if prices.empty:
                return pd.Series(index=stocks, dtype=float)
            
            volatility_dict = {}
            
            for stock in stocks:
                stock_prices = prices[prices["code"] == stock]["close"]
                
                if len(stock_prices) < 20:
                    volatility_dict[stock] = np.nan
                    continue
                
                # 计算日收益率标准差（年化）
                returns = stock_prices.pct_change().dropna()
                vol = returns.std() * np.sqrt(252)  # 年化波动率
                
                # 负号：低波动率得高分
                volatility_dict[stock] = -vol
            
            result = pd.Series(volatility_dict)
            logger.info(f"波动率因子计算完成: 有效值 {result.notna().sum()}/{len(stocks)}")
            return result
        
        except Exception as e:
            logger.error(f"波动率因子计算失败: {e}")
            return pd.Series(index=stocks, dtype=float)