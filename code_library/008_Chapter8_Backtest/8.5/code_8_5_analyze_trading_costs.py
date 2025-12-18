"""
文件名: code_8_5_analyze_trading_costs.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_analyze_trading_costs.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_trading_costs

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class TradingCostAnalyzer:
    """交易成本分析器"""
    
    def analyze_trading_costs(
        self,
        trades: List[TradeRecord],
        equity_curve: pd.DataFrame
    ) -> Dict[str, Any]:
            """
    analyze_trading_costs函数
    
    **设计原理**：
    - **核心功能**：实现analyze_trading_costs的核心逻辑
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
                'value': t.price * t.amount,
                'commission': t.commission
            }
            for t in trades
        ])
        
        # 总手续费
        total_commission = trades_df['commission'].sum()
        
        # 总交易金额
        total_trade_value = trades_df['value'].sum()
        
        # 手续费率
        commission_rate = total_commission / total_trade_value if total_trade_value > 0 else 0
        
        # 平均资产
        equity_curve = equity_curve.sort_values('date')
        avg_equity = equity_curve['equity'].mean()
        
        # 成本占比
        cost_ratio = total_commission / avg_equity if avg_equity > 0 else 0
        
        # 按时间段分解成本
        trades_df['date'] = pd.to_datetime(trades_df['date'])
        trades_df['year_month'] = trades_df['date'].dt.to_period('M')
        monthly_costs = trades_df.groupby('year_month')['commission'].sum().to_dict()
        
        return {
            'total_commission': total_commission,
            'total_trade_value': total_trade_value,
            'commission_rate': commission_rate,
            'cost_ratio': cost_ratio,
            'monthly_costs': monthly_costs
        }