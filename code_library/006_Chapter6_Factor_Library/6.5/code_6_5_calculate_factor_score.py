"""
文件名: code_6_5_calculate_factor_score.py
保存路径: code_library/006_Chapter6_Factor_Library/6.5/code_6_5_calculate_factor_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.5_Factor_Pool_Integration_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: calculate_factor_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def calculate_factor_score(
    self,
    stocks: List[str],
    date: Union[str, datetime],
    period: str = "medium",
    factor_weights: Optional[Dict[str, float]] = None,
) -> pd.Series:
        """
    calculate_factor_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_factor_score的核心逻辑
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
    if factor_weights is None:
        factor_weights = self.DEFAULT_FACTOR_WEIGHTS.get(period, {})
    
    if not factor_weights:
        logger.warning(f"未找到周期 {period} 的因子权重配置")
        return pd.Series(index=stocks, dtype=float)
    
    # 计算各因子值
    factor_results = {}
    for factor_name in factor_weights.keys():
        try:
            result = self.factor_manager.calculate_factor(
                factor_name, stocks, date
            )
            if result and not result.values.empty:
                factor_results[factor_name] = result.values
        except Exception as e:
            logger.warning(f"因子计算失败: {factor_name}, 错误: {e}")
            continue
    
    if not factor_results:
        logger.warning("所有因子计算失败")
        return pd.Series(index=stocks, dtype=float)
    
    # 对齐所有因子的股票列表
    all_stocks = set()
    for values in factor_results.values():
        all_stocks.update(values.index)
    
    # 构建因子值DataFrame
    factor_df = pd.DataFrame(index=list(all_stocks))
    for name, values in factor_results.items():
        factor_df[name] = values
    
    # 标准化各因子
    for name in factor_df.columns:
        factor_df[name] = (factor_df[name] - factor_df[name].mean()) / factor_df[name].std()
    
    # 加权组合
    combined_score = pd.Series(0.0, index=factor_df.index)
    total_weight = 0
    
    for factor_name, weight in factor_weights.items():
        if factor_name in factor_df.columns:
            combined_score += factor_df[factor_name] * weight
            total_weight += weight
    
    # 归一化
    if total_weight > 0:
        combined_score = combined_score / total_weight
    
    # 重新索引到原始股票列表
    combined_score = combined_score.reindex(stocks)
    
    return combined_score