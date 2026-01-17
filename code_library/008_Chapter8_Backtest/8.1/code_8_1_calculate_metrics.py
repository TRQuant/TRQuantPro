"""
文件名: code_8_1_calculate_metrics.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1_calculate_metrics.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: calculate_metrics

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class PerformanceCalculator:
    """性能计算器"""
    
    def calculate_metrics(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: pd.DataFrame = None
    ) -> PerformanceMetrics:
            """
    calculate_metrics函数
    
    **设计原理**：
    - **核心功能**：实现calculate_metrics的核心逻辑
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
        returns = equity_curve['equity'].pct_change().dropna()
        
        # 总收益率
        total_return = (equity_curve['equity'].iloc[-1] / equity_curve['equity'].iloc[0]) - 1
        
        # 年化收益率
        days = (equity_curve.index[-1] - equity_curve.index[0]).days
        years = days / 365.25
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 最大回撤
        max_drawdown, max_drawdown_duration = self._calculate_max_drawdown(equity_curve)
        
        # 夏普比率
        sharpe_ratio = self._calculate_sharpe_ratio(returns)
        
        # 波动率
        volatility = returns.std() * np.sqrt(252)
        
        return PerformanceMetrics(
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_duration=max_drawdown_duration,
            volatility=volatility
        )