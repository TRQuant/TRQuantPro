"""
文件名: code_8_3_analyze_annual_return.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_analyze_annual_return.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_annual_return

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class AnnualReturnAnalyzer:
    """年化收益分析器"""
    
    def analyze_annual_return(
        self,
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        分析年化收益
        
        Args:
            equity_curve: 净值曲线
        
        Returns:
            Dict: 年化收益分析结果
        """
        equity_curve = equity_curve.sort_values('date')
        
        # 计算总收益
        initial_equity = equity_curve['equity'].iloc[0]
        final_equity = equity_curve['equity'].iloc[-1]
        total_return = (final_equity / initial_equity) - 1
        
        # 计算时间跨度
        start_date = pd.to_datetime(equity_curve['date'].iloc[0])
        end_date = pd.to_datetime(equity_curve['date'].iloc[-1])
        days = (end_date - start_date).days
        years = days / 365.25
        
        # 设计原理：年化收益率（复利计算）
        # 原因：复利计算更准确反映实际收益，考虑了收益再投资
        # 公式：年化收益率 = (1 + 总收益率)^(1/年数) - 1
        # 适用场景：长期投资策略，收益会再投资
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 设计原理：年化收益率（简单计算）
        # 原因：简单计算便于理解，但不考虑复利效应
        # 公式：年化收益率 = 总收益率 / 年数
        # 适用场景：短期策略或粗略估算
        annual_return_simple = total_return / years if years > 0 else 0
        
        # 设计原理：月度收益率计算
        # 原因：月度收益提供更细粒度的收益分析
        # 实现方式：按年月分组，取每月最后一天的净值，计算月度收益率
        equity_curve['year_month'] = pd.to_datetime(equity_curve['date']).dt.to_period('M')
        monthly_equity = equity_curve.groupby('year_month')['equity'].last()
        monthly_returns = monthly_equity.pct_change().dropna()
        
        # 设计原理：月度年化收益（几何平均）
        # 原因：几何平均考虑复利效应，更准确反映长期收益
        # 公式：月度年化收益 = (月度收益乘积)^(12/月数) - 1
        # 适用场景：评估策略的长期表现
        monthly_annual_return = (1 + monthly_returns).prod() ** (12 / len(monthly_returns)) - 1 if len(monthly_returns) > 0 else 0
        
        # 年度收益分解
        equity_curve['year'] = pd.to_datetime(equity_curve['date']).dt.year
        yearly_returns = self._calculate_yearly_returns(equity_curve)
        
        return {
            'total_return': total_return,
            'years': years,
            'annual_return': annual_return,
            'annual_return_simple': annual_return_simple,
            'monthly_annual_return': monthly_annual_return,
            'monthly_returns': monthly_returns,
            'yearly_returns': yearly_returns,
            'avg_monthly_return': monthly_returns.mean(),
            'monthly_return_std': monthly_returns.std()
        }
    
    def _calculate_yearly_returns(self, equity_curve: pd.DataFrame) -> Dict[int, float]:
        """计算年度收益"""
        yearly_returns = {}
        
        for year in equity_curve['year'].unique():
            year_data = equity_curve[equity_curve['year'] == year].sort_values('date')
            if len(year_data) > 0:
                year_start = year_data['equity'].iloc[0]
                year_end = year_data['equity'].iloc[-1]
                yearly_returns[year] = (year_end / year_start) - 1
        
        return yearly_returns