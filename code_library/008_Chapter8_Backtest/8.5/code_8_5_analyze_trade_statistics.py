"""
文件名: code_8_5_analyze_trade_statistics.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_analyze_trade_statistics.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_trade_statistics

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TradeRecord:
    """交易记录"""
    date: str
    security: str
    action: str  # 'buy' or 'sell'
    price: float
    amount: int
    commission: float
    pnl: float = 0.0  # 卖出时的盈亏

class TradeStatisticsAnalyzer:
    """交易统计分析器"""
    
    def analyze_trade_statistics(
        self,
        trades: List[TradeRecord],
        equity_curve: pd.DataFrame = None
    ) -> Dict[str, Any]:
            """
    analyze_trade_statistics函数
    
    **设计原理**：
    - **核心功能**：实现analyze_trade_statistics的核心逻辑
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
        if not trades:
            return {}
        
        # 转换为DataFrame
        trades_df = pd.DataFrame([
            {
                'date': t.date,
                'security': t.security,
                'action': t.action,
                'price': t.price,
                'amount': t.amount,
                'commission': t.commission,
                'pnl': t.pnl,
                'value': t.price * t.amount
            }
            for t in trades
        ])
        
        # 基本统计
        total_trades = len(trades_df)
        buy_trades = len(trades_df[trades_df['action'] == 'buy'])
        sell_trades = len(trades_df[trades_df['action'] == 'sell'])
        
        # 交易频率
        if equity_curve is not None:
            equity_curve = equity_curve.sort_values('date')
            start_date = pd.to_datetime(equity_curve['date'].iloc[0])
            end_date = pd.to_datetime(equity_curve['date'].iloc[-1])
            days = (end_date - start_date).days
            trades_per_day = total_trades / days if days > 0 else 0
            trades_per_month = total_trades / (days / 30) if days > 0 else 0
        else:
            trades_per_day = 0
            trades_per_month = 0
        
        # 交易分布（按日期）
        trades_df['date'] = pd.to_datetime(trades_df['date'])
        trades_by_date = trades_df.groupby(trades_df['date'].dt.date).size()
        
        # 交易分布（按股票）
        trades_by_security = trades_df.groupby('security').size()
        
        # 交易分布（按月份）
        trades_df['year_month'] = trades_df['date'].dt.to_period('M')
        trades_by_month = trades_df.groupby('year_month').size()
        
        return {
            'total_trades': total_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'trades_per_day': trades_per_day,
            'trades_per_month': trades_per_month,
            'trades_by_date': trades_by_date.to_dict(),
            'trades_by_security': trades_by_security.to_dict(),
            'trades_by_month': trades_by_month.to_dict(),
            'most_traded_security': trades_by_security.idxmax() if len(trades_by_security) > 0 else None,
            'most_traded_month': trades_by_month.idxmax() if len(trades_by_month) > 0 else None
        }