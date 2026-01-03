"""
文件名: code_8_3_analyze_total_return.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_analyze_total_return.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_total_return

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class TotalReturnAnalyzer:
    """总收益分析器"""
    
    def analyze_total_return(
        self,
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    analyze_total_return函数
    
    **设计原理**：
    - **核心功能**：实现analyze_total_return的核心逻辑
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
        
        # 初始和最终净值
        initial_equity = equity_curve['equity'].iloc[0]
        final_equity = equity_curve['equity'].iloc[-1]
        
        # 总收益率
        total_return = (final_equity / initial_equity) - 1
        
        # 收益曲线（相对于初始净值）
        equity_curve['return_curve'] = (equity_curve['equity'] / initial_equity) - 1
        
        # 日收益率
        equity_curve['daily_return'] = equity_curve['equity'].pct_change()
        
        # 收益统计
        daily_returns = equity_curve['daily_return'].dropna()
        return_stats = {
            'mean': daily_returns.mean(),
            'std': daily_returns.std(),
            'min': daily_returns.min(),
            'max': daily_returns.max(),
            'median': daily_returns.median(),
            'skewness': daily_returns.skew(),
            'kurtosis': daily_returns.kurtosis()
        }
        
        # 收益分布
        return_distribution = self._analyze_return_distribution(daily_returns)
        
        # 最大单日收益和最大单日亏损
        max_daily_gain = daily_returns.max()
        max_daily_loss = daily_returns.min()
        
        # 收益为正的天数占比
        positive_days_ratio = (daily_returns > 0).sum() / len(daily_returns)
        
        return {
            'initial_equity': initial_equity,
            'final_equity': final_equity,
            'total_return': total_return,
            'return_curve': equity_curve[['date', 'return_curve']],
            'return_stats': return_stats,
            'return_distribution': return_distribution,
            'max_daily_gain': max_daily_gain,
            'max_daily_loss': max_daily_loss,
            'positive_days_ratio': positive_days_ratio,
            'total_days': len(equity_curve)
        }
    
    def _analyze_return_distribution(self, returns: pd.Series) -> Dict[str, Any]:
        """分析收益分布"""
        return {
            'positive_count': (returns > 0).sum(),
            'negative_count': (returns < 0).sum(),
            'zero_count': (returns == 0).sum(),
            'positive_ratio': (returns > 0).sum() / len(returns),
            'negative_ratio': (returns < 0).sum() / len(returns),
            'bins': {
                '>5%': (returns > 0.05).sum(),
                '2%-5%': ((returns > 0.02) & (returns <= 0.05)).sum(),
                '0-2%': ((returns > 0) & (returns <= 0.02)).sum(),
                '-2%-0': ((returns >= -0.02) & (returns < 0)).sum(),
                '-5%--2%': ((returns >= -0.05) & (returns < -0.02)).sum(),
                '<-5%': (returns < -0.05).sum()
            }
        }