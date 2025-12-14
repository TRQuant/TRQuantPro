"""
文件名: code_6_3_combine_factors_ic_weighted.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3_combine_factors_ic_weighted.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: combine_factors_ic_weighted

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def combine_factors_ic_weighted(
    self,
    factor_results: Dict[str, FactorResult],
    factor_performances: Dict[str, FactorPerformance]
) -> pd.Series:
        """
    combine_factors_ic_weighted函数
    
    **设计原理**：
    - **核心功能**：实现combine_factors_ic_weighted的核心逻辑
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
    if not factor_results:
        return pd.Series()
    
    # 计算权重
    weights = {}
    total_ic_ir = 0
    
    for name in factor_results.keys():
        performance = factor_performances.get(name)
        if performance and performance.ic_ir > 0:
            weights[name] = performance.ic_ir
            total_ic_ir += performance.ic_ir
    
    if total_ic_ir == 0:
        # 如果所有IC_IR都<=0，使用等权
        return self.combine_factors_equal(factor_results)
    
    # 归一化权重
    weights = {k: v / total_ic_ir for k, v in weights.items()}
    
    # 对齐所有因子的股票列表
    all_stocks = set()
    for result in factor_results.values():
        all_stocks.update(result.stocks)
    
    # 构建因子值DataFrame
    factor_df = pd.DataFrame(index=list(all_stocks))
    for name, result in factor_results.items():
        factor_df[name] = result.values
    
    # IC加权组合
    combined = pd.Series(0.0, index=factor_df.index)
    for name, weight in weights.items():
        if name in factor_df.columns:
            combined += factor_df[name] * weight
    
    return combined