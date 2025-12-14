"""
文件名: code_6_1__neutralize.py
保存路径: code_library/006_Chapter6_Factor_Library/6.1/code_6_1__neutralize.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.1_Factor_Calculation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: _neutralize

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

def _neutralize(self, values: pd.Series, stocks: List[str], date: Union[str, datetime]) -> pd.Series:
        """
    _neutralize函数
    
    **设计原理**：
    - **核心功能**：实现_neutralize的核心逻辑
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
    # 获取行业信息
    industries = self._get_industries(stocks, date)
    
    # 按行业分组，计算行业均值
    industry_means = {}
    for stock, industry in industries.items():
        if industry not in industry_means:
            industry_means[industry] = []
        if stock in values.index and not pd.isna(values[stock]):
            industry_means[industry].append(values[stock])
    
    # 计算行业均值
    for industry in industry_means:
        industry_means[industry] = np.mean(industry_means[industry]) if industry_means[industry] else 0
    
    # 中性化：减去行业均值
    neutralized = values.copy()
    for stock, industry in industries.items():
        if stock in neutralized.index and industry in industry_means:
            neutralized[stock] = neutralized[stock] - industry_means[industry]
    
    return neutralized