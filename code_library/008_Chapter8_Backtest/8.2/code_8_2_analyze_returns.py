"""
文件名: code_8_2_analyze_returns.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_analyze_returns.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_returns

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class ReturnAnalyzer:
    """收益分析器"""
    
    def analyze_returns(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
            """
    analyze_returns函数
    
    **设计原理**：
    - **核心功能**：实现analyze_returns的核心逻辑
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
        # 计算日收益率
        equity_curve = equity_curve.sort_values('date')
        equity_curve['returns'] = equity_curve['equity'].pct_change()
        returns = equity_curve['returns'].dropna()
        
        # 总收益率
        initial_equity = equity_curve['equity'].iloc[0]
        final_equity = equity_curve['equity'].iloc[-1]
        total_return = (final_equity / initial_equity) - 1
        
        # 年化收益率
        days = (equity_curve['date'].iloc[-1] - equity_curve['date'].iloc[0]).days
        years = days / 365.25
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 月度收益率
        equity_curve['year_month'] = pd.to_datetime(equity_curve['date']).dt.to_period('M')
        monthly_returns = equity_curve.groupby('year_month')['equity'].last().pct_change().dropna()
        
        # 超额收益（相对于基准）
        excess_return = None
        if benchmark_curve is not None:
            benchmark_curve = benchmark_curve.sort_values('date')
            benchmark_returns = benchmark_curve['equity'].pct_change().dropna()
            benchmark_annual_return = self._calculate_annual_return(
                benchmark_curve['equity'].iloc[0],
                benchmark_curve['equity'].iloc[-1],
                days
            )
            excess_return = annual_return - benchmark_annual_return
        
        # 收益稳定性（月度收益率的稳定性）
        monthly_volatility = monthly_returns.std()
        monthly_sharpe = monthly_returns.mean() / monthly_volatility if monthly_volatility > 0 else 0
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'excess_return': excess_return,
            'monthly_returns': monthly_returns,
            'monthly_volatility': monthly_volatility,
            'monthly_sharpe': monthly_sharpe,
            'returns': returns,
            'positive_months': (monthly_returns > 0).sum(),
            'negative_months': (monthly_returns < 0).sum(),
            'total_months': len(monthly_returns)
        }
    
    def _calculate_annual_return(
        self,
        initial_value: float,
        final_value: float,
        days: int
    ) -> float:
        """计算年化收益率"""
        total_return = (final_value / initial_value) - 1
        years = days / 365.25
        return (1 + total_return) ** (1 / years) - 1 if years > 0 else 0