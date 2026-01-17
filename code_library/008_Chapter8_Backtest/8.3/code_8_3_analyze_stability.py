"""
文件名: code_8_3_analyze_stability.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_analyze_stability.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_stability

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class ReturnStabilityAnalyzer:
    """收益稳定性分析器"""
    
    def analyze_stability(
        self,
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    analyze_stability函数
    
    **设计原理**：
    - **核心功能**：实现analyze_stability的核心逻辑
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
        equity_curve = equity_curve.sort_values('date')
        equity_curve['date'] = pd.to_datetime(equity_curve['date'])
        
        # 月度收益
        equity_curve['year_month'] = equity_curve['date'].dt.to_period('M')
        monthly_equity = equity_curve.groupby('year_month')['equity'].last()
        monthly_returns = monthly_equity.pct_change().dropna()
        
        # 收益稳定性指标
        stability_metrics = {
            'monthly_return_mean': monthly_returns.mean(),
            'monthly_return_std': monthly_returns.std(),
            'monthly_return_cv': monthly_returns.std() / abs(monthly_returns.mean()) if monthly_returns.mean() != 0 else 0,  # 变异系数
            'positive_months_ratio': (monthly_returns > 0).sum() / len(monthly_returns),
            'consecutive_positive_months': self._max_consecutive_positive(monthly_returns),
            'consecutive_negative_months': self._max_consecutive_negative(monthly_returns)
        }
        
        # 收益持续性
        persistence_metrics = self._analyze_persistence(monthly_returns)
        
        return {
            'monthly_returns': monthly_returns,
            'stability_metrics': stability_metrics,
            'persistence_metrics': persistence_metrics
        }
    
    def _max_consecutive_positive(self, returns: pd.Series) -> int:
        """最大连续盈利月数"""
        max_consecutive = 0
        current_consecutive = 0
        
        for ret in returns:
            if ret > 0:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _max_consecutive_negative(self, returns: pd.Series) -> int:
        """最大连续亏损月数"""
        max_consecutive = 0
        current_consecutive = 0
        
        for ret in returns:
            if ret < 0:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _analyze_persistence(self, monthly_returns: pd.Series) -> Dict[str, Any]:
        """分析收益持续性"""
        # 计算自相关
        autocorr = monthly_returns.autocorr(lag=1)
        
        # 计算收益序列的趋势
        trend = np.polyfit(range(len(monthly_returns)), monthly_returns.values, 1)[0]
        
        return {
            'autocorrelation': autocorr,
            'trend': trend,
            'is_persistent': abs(autocorr) > 0.2  # 自相关绝对值大于0.2认为有持续性
        }