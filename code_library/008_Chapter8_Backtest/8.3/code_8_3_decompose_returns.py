"""
文件名: code_8_3_decompose_returns.py
保存路径: code_library/008_Chapter8_Backtest/8.3/code_8_3_decompose_returns.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.3_Return_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: decompose_returns

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class ReturnDecompositionAnalyzer:
    """收益分解分析器"""
    
    def decompose_returns(
        self,
        trades: List[TradeRecord],
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    decompose_returns函数
    
    **设计原理**：
    - **核心功能**：实现decompose_returns的核心逻辑
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
                'security': t.security,
                'action': t.action,
                'price': t.price,
                'amount': t.amount,
                'pnl': t.pnl
            }
            for t in trades
        ])
        
        # 按行业分解（需要行业信息）
        industry_decomposition = self._decompose_by_industry(trades_df)
        
        # 按个股分解
        stock_decomposition = self._decompose_by_stock(trades_df)
        
        # 按时间维度分解
        time_decomposition = self._decompose_by_time(equity_curve)
        
        return {
            'industry_decomposition': industry_decomposition,
            'stock_decomposition': stock_decomposition,
            'time_decomposition': time_decomposition
        }
    
    def _decompose_by_stock(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """按个股分解收益"""
        sell_trades = trades_df[trades_df['action'] == 'sell']
        
        stock_pnl = sell_trades.groupby('security')['pnl'].sum()
        total_pnl = stock_pnl.sum()
        
        stock_contribution = {
            stock: {
                'pnl': pnl,
                'contribution': pnl / total_pnl if total_pnl != 0 else 0,
                'trade_count': len(sell_trades[sell_trades['security'] == stock])
            }
            for stock, pnl in stock_pnl.items()
        }
        
        return {
            'total_pnl': total_pnl,
            'stock_contributions': stock_contribution,
            'top_contributors': sorted(
                stock_contribution.items(),
                key=lambda x: x[1]['pnl'],
                reverse=True
            )[:10]
        }
    
    def _decompose_by_time(self, equity_curve: pd.DataFrame) -> Dict[str, Any]:
        """按时间维度分解收益"""
        equity_curve = equity_curve.sort_values('date')
        equity_curve['date'] = pd.to_datetime(equity_curve['date'])
        
        # 月度收益
        equity_curve['year_month'] = equity_curve['date'].dt.to_period('M')
        monthly_equity = equity_curve.groupby('year_month')['equity'].last()
        monthly_returns = monthly_equity.pct_change().dropna()
        
        # 季度收益
        equity_curve['quarter'] = equity_curve['date'].dt.to_period('Q')
        quarterly_equity = equity_curve.groupby('quarter')['equity'].last()
        quarterly_returns = quarterly_equity.pct_change().dropna()
        
        # 年度收益
        equity_curve['year'] = equity_curve['date'].dt.year
        yearly_equity = equity_curve.groupby('year')['equity'].last()
        yearly_returns = yearly_equity.pct_change().dropna()
        
        return {
            'monthly_returns': monthly_returns.to_dict(),
            'quarterly_returns': quarterly_returns.to_dict(),
            'yearly_returns': yearly_returns.to_dict(),
            'best_month': monthly_returns.idxmax(),
            'worst_month': monthly_returns.idxmin(),
            'best_quarter': quarterly_returns.idxmax(),
            'worst_quarter': quarterly_returns.idxmin()
        }
    
    def _decompose_by_industry(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """按行业分解收益（需要行业信息）"""
        # 这里需要从股票代码获取行业信息
        # 简化示例
        return {}