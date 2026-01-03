"""
文件名: code_8_3_analyze_excess_return.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_analyze_excess_return.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_excess_return

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class ExcessReturnAnalyzer:
    """超额收益分析器"""
    
    def analyze_excess_return(
        self,
        equity_curve: pd.DataFrame,
        benchmark_curve: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        分析超额收益
        
        Args:
            equity_curve: 策略净值曲线
            benchmark_curve: 基准净值曲线
        
        Returns:
            Dict: 超额收益分析结果
        """
        # 设计原理：数据对齐
        # 原因：策略和基准的数据日期可能不完全一致，需要对齐
        # 实现方式：按日期排序，确保数据顺序一致
        equity_curve = equity_curve.sort_values('date')
        benchmark_curve = benchmark_curve.sort_values('date')
        
        # 设计原理：数据合并
        # 原因：需要同时计算策略和基准的收益，进行对比
        # 实现方式：使用pd.merge按日期合并，只保留共同日期
        # 注意事项：如果日期不匹配，会丢失部分数据，需要确保数据完整性
        merged = pd.merge(
            equity_curve[['date', 'equity']],
            benchmark_curve[['date', 'equity']],
            on='date',
            suffixes=('_strategy', '_benchmark')
        )
        
        # 计算收益率
        merged['return_strategy'] = merged['equity_strategy'].pct_change()
        merged['return_benchmark'] = merged['equity_benchmark'].pct_change()
        
        # 超额收益（日度）
        merged['excess_return'] = merged['return_strategy'] - merged['return_benchmark']
        
        # 累计超额收益
        merged['cumulative_excess_return'] = (1 + merged['excess_return']).cumprod() - 1
        
        # 总超额收益
        initial_strategy = merged['equity_strategy'].iloc[0]
        final_strategy = merged['equity_strategy'].iloc[-1]
        strategy_total_return = (final_strategy / initial_strategy) - 1
        
        initial_benchmark = merged['equity_benchmark'].iloc[0]
        final_benchmark = merged['equity_benchmark'].iloc[-1]
        benchmark_total_return = (final_benchmark / initial_benchmark) - 1
        
        total_excess_return = strategy_total_return - benchmark_total_return
        
        # 年化超额收益
        days = (pd.to_datetime(merged['date'].iloc[-1]) - pd.to_datetime(merged['date'].iloc[0])).days
        years = days / 365.25
        annual_excess_return = total_excess_return / years if years > 0 else 0
        
        # 信息比率（超额收益的夏普比率）
        excess_returns = merged['excess_return'].dropna()
        information_ratio = excess_returns.mean() * np.sqrt(252) / excess_returns.std() if excess_returns.std() > 0 else 0
        
        # 跟踪误差（超额收益的标准差）
        tracking_error = excess_returns.std() * np.sqrt(252)
        
        return {
            'strategy_total_return': strategy_total_return,
            'benchmark_total_return': benchmark_total_return,
            'total_excess_return': total_excess_return,
            'annual_excess_return': annual_excess_return,
            'information_ratio': information_ratio,
            'tracking_error': tracking_error,
            'excess_return_series': merged[['date', 'excess_return', 'cumulative_excess_return']],
            'excess_return_stats': {
                'mean': excess_returns.mean(),
                'std': excess_returns.std(),
                'min': excess_returns.min(),
                'max': excess_returns.max()
            }
        }