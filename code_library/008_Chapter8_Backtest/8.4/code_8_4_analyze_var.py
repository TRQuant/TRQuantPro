"""
文件名: code_8_4_analyze_var.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_analyze_var.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_var

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class ValueAtRiskAnalyzer:
    """风险价值分析器"""
    
    def analyze_var(
        self,
        returns: pd.Series,
        confidence_levels: List[float] = [0.95, 0.99]
    ) -> Dict[str, Any]:
            """
    analyze_var函数
    
    **设计原理**：
    - **核心功能**：实现analyze_var的核心逻辑
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
        # 年化收益率
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * np.sqrt(252)
        
        var_results = {}
        cvar_results = {}
        
        for conf_level in confidence_levels:
            alpha = 1 - conf_level
            
            # VaR（参数法，假设正态分布）
            var_param = annual_return - annual_volatility * np.abs(np.percentile([0], alpha * 100))
            var_param = annual_return - annual_volatility * 1.645 if conf_level == 0.95 else annual_return - annual_volatility * 2.326
            
            # VaR（历史法）
            var_historical = np.percentile(returns, alpha * 100) * np.sqrt(252)
            
            # CVaR（条件风险价值）
            cvar_historical = returns[returns <= np.percentile(returns, alpha * 100)].mean() * np.sqrt(252) if len(returns[returns <= np.percentile(returns, alpha * 100)]) > 0 else 0
            
            var_results[conf_level] = {
                'var_parametric': var_param,
                'var_historical': var_historical
            }
            
            cvar_results[conf_level] = {
                'cvar_historical': cvar_historical
            }
        
        return {
            'var_results': var_results,
            'cvar_results': cvar_results,
            'annual_return': annual_return,
            'annual_volatility': annual_volatility
        }