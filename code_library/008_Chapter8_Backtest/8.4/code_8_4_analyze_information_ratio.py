"""
文件名: code_8_4_analyze_information_ratio.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_analyze_information_ratio.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_information_ratio

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class InformationRatioAnalyzer:
    """信息比率分析器"""
    
    def analyze_information_ratio(
        self,
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series
    ) -> Dict[str, Any]:
            """
    analyze_information_ratio函数
    
    **设计原理**：
    - **核心功能**：实现analyze_information_ratio的核心逻辑
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
        # 对齐数据
        aligned = pd.DataFrame({
            'strategy': strategy_returns,
            'benchmark': benchmark_returns
        }).dropna()
        
        # 超额收益
        excess_returns = aligned['strategy'] - aligned['benchmark']
        
        # 年化超额收益
        annual_excess_return = excess_returns.mean() * 252
        
        # 跟踪误差（超额收益的标准差）
        tracking_error = excess_returns.std() * np.sqrt(252)
        
        # 信息比率
        information_ratio = annual_excess_return / tracking_error if tracking_error > 0 else 0
        
        # 超额收益稳定性
        excess_return_stability = 1 - (excess_returns.std() / abs(excess_returns.mean())) if excess_returns.mean() != 0 else 0
        
        return {
            'annual_excess_return': annual_excess_return,
            'tracking_error': tracking_error,
            'information_ratio': information_ratio,
            'excess_return_stability': excess_return_stability,
            'excess_returns': excess_returns
        }