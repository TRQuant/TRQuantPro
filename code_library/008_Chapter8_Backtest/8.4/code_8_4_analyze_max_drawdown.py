"""
文件名: code_8_4_analyze_max_drawdown.py
保存路径: code_library/008_Chapter8_Backtest/8.4/code_8_4_analyze_max_drawdown.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.4_Risk_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_max_drawdown

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

class MaxDrawdownAnalyzer:
    """最大回撤分析器"""
    
    def analyze_max_drawdown(
        self,
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    analyze_max_drawdown函数
    
    **设计原理**：
    - **核心功能**：实现analyze_max_drawdown的核心逻辑
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
        equity = equity_curve['equity'].values
        dates = pd.to_datetime(equity_curve['date'])
        
        # 计算累计最高值
        cumulative_max = np.maximum.accumulate(equity)
        
        # 计算回撤
        drawdown = (equity - cumulative_max) / cumulative_max
        drawdown_series = pd.Series(drawdown, index=dates)
        
        # 最大回撤
        max_drawdown = abs(drawdown.min())
        max_dd_idx = drawdown.idxmin()
        
        # 最大回撤开始和结束时间
        max_dd_start_idx = np.where(equity == cumulative_max[drawdown.idxmin()])[0]
        if len(max_dd_start_idx) > 0:
            max_dd_start_date = dates[max_dd_start_idx[0]]
        else:
            max_dd_start_date = dates[0]
        
        max_dd_end_date = max_dd_idx
        
        # 最大回撤持续时间
        max_dd_duration = (max_dd_end_date - max_dd_start_date).days
        
        # 回撤恢复时间（从最大回撤恢复到新高）
        recovery_date = self._calculate_recovery_date(
            equity_curve, max_dd_end_date, cumulative_max[drawdown.idxmin()]
        )
        recovery_duration = (recovery_date - max_dd_end_date).days if recovery_date else None
        
        # 回撤统计
        drawdown_stats = self._analyze_drawdowns(drawdown_series)
        
        return {
            'max_drawdown': max_drawdown,
            'max_dd_start_date': max_dd_start_date,
            'max_dd_end_date': max_dd_end_date,
            'max_dd_duration': max_dd_duration,
            'recovery_date': recovery_date,
            'recovery_duration': recovery_duration,
            'drawdown_curve': drawdown_series,
            'drawdown_stats': drawdown_stats
        }
    
    def _calculate_recovery_date(
        self,
        equity_curve: pd.DataFrame,
        max_dd_end_date: pd.Timestamp,
        peak_value: float
    ) -> pd.Timestamp:
        """计算回撤恢复日期"""
        equity_curve = equity_curve.sort_values('date')
        dates = pd.to_datetime(equity_curve['date'])
        
        # 找到最大回撤结束后的数据
        after_dd = equity_curve[dates > max_dd_end_date]
        
        if len(after_dd) == 0:
            return None
        
        # 找到第一个超过峰值净值的日期
        recovery_idx = (after_dd['equity'] >= peak_value).idxmax()
        if pd.isna(recovery_idx):
            return None
        
        return pd.to_datetime(equity_curve.loc[recovery_idx, 'date'])
    
    def _analyze_drawdowns(self, drawdown_series: pd.Series) -> Dict[str, Any]:
        """分析回撤统计"""
        drawdowns = drawdown_series[drawdown_series < 0]
        
        return {
            'drawdown_count': len(drawdowns[drawdowns < drawdowns.shift(1)]),  # 回撤次数
            'avg_drawdown': abs(drawdowns.mean()) if len(drawdowns) > 0 else 0,
            'max_drawdown': abs(drawdowns.min()) if len(drawdowns) > 0 else 0,
            'drawdown_std': drawdowns.std() if len(drawdowns) > 0 else 0
        }