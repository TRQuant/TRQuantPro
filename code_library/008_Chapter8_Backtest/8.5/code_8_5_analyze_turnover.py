"""
文件名: code_8_5_analyze_turnover.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_analyze_turnover.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_turnover

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class TurnoverAnalyzer:
    """换手率分析器"""
    
    def analyze_turnover(
        self,
        trades: List[TradeRecord],
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    analyze_turnover函数
    
    **设计原理**：
    - **核心功能**：实现analyze_turnover的核心逻辑
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
        trades_df = pd.DataFrame([
            {
                'date': t.date,
                'action': t.action,
                'value': t.price * t.amount
            }
            for t in trades
        ])
        
        # 总交易金额
        total_trade_value = trades_df['value'].sum()
        
        # 平均资产
        equity_curve = equity_curve.sort_values('date')
        avg_equity = equity_curve['equity'].mean()
        
        # 换手率 = 总交易金额 / 平均资产
        turnover_rate = total_trade_value / avg_equity if avg_equity > 0 else 0
        
        # 年化换手率
        start_date = pd.to_datetime(equity_curve['date'].iloc[0])
        end_date = pd.to_datetime(equity_curve['date'].iloc[-1])
        days = (end_date - start_date).days
        years = days / 365.25
        annual_turnover = turnover_rate / years if years > 0 else 0
        
        # 按时间段分解换手率
        trades_df['date'] = pd.to_datetime(trades_df['date'])
        trades_df['year_month'] = trades_df['date'].dt.to_period('M')
        monthly_turnover = self._calculate_monthly_turnover(trades_df, equity_curve)
        
        return {
            'total_trade_value': total_trade_value,
            'avg_equity': avg_equity,
            'turnover_rate': turnover_rate,
            'annual_turnover': annual_turnover,
            'monthly_turnover': monthly_turnover
        }
    
    def _calculate_monthly_turnover(
        self,
        trades_df: pd.DataFrame,
        equity_curve: pd.DataFrame
    ) -> Dict[str, float]:
        """计算月度换手率"""
        monthly_turnover = {}
        
        for year_month in trades_df['year_month'].unique():
            month_trades = trades_df[trades_df['year_month'] == year_month]
            month_trade_value = month_trades['value'].sum()
            
            # 该月的平均资产
            equity_curve['year_month'] = pd.to_datetime(equity_curve['date']).dt.to_period('M')
            month_equity = equity_curve[equity_curve['year_month'] == year_month]['equity'].mean()
            
            month_turnover = month_trade_value / month_equity if month_equity > 0 else 0
            monthly_turnover[str(year_month)] = month_turnover
        
        return monthly_turnover