"""
文件名: code_8_2_analyze_trades.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_analyze_trades.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_trades

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import pandas as pd
import numpy as np

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

class TradeAnalyzer:
    """交易分析器"""
    
    def analyze_trades(
        self,
        trades: List[TradeRecord],
        equity_curve: pd.DataFrame = None
    ) -> Dict[str, Any]:
            """
    analyze_trades函数
    
    **设计原理**：
    - **核心功能**：实现analyze_trades的核心逻辑
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
        
        # 转换为DataFrame便于分析
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
        
        # 交易次数
        trade_count = len(trades_df)
        buy_count = len(trades_df[trades_df['action'] == 'buy'])
        sell_count = len(trades_df[trades_df['action'] == 'sell'])
        
        # 胜率（只考虑卖出交易）
        sell_trades = trades_df[trades_df['action'] == 'sell']
        winning_trades = sell_trades[sell_trades['pnl'] > 0]
        win_rate = len(winning_trades) / len(sell_trades) if len(sell_trades) > 0 else 0
        
        # 盈亏比
        avg_profit = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
        losing_trades = sell_trades[sell_trades['pnl'] < 0]
        avg_loss = abs(losing_trades['pnl'].mean()) if len(losing_trades) > 0 else 0
        profit_loss_ratio = avg_profit / avg_loss if avg_loss > 0 else 0
        
        # 平均持仓周期
        avg_holding_period = self._calculate_avg_holding_period(trades_df)
        
        # 换手率
        turnover_rate = self._calculate_turnover_rate(trades_df, equity_curve)
        
        # 交易成本
        total_commission = trades_df['commission'].sum()
        total_trade_value = trades_df['value'].sum()
        commission_rate = total_commission / total_trade_value if total_trade_value > 0 else 0
        
        # 单笔交易统计
        trade_stats = {
            'avg_trade_value': trades_df['value'].mean(),
            'max_trade_value': trades_df['value'].max(),
            'min_trade_value': trades_df['value'].min(),
            'total_trade_value': total_trade_value
        }
        
        return {
            'trade_count': trade_count,
            'buy_count': buy_count,
            'sell_count': sell_count,
            'win_rate': win_rate,
            'profit_loss_ratio': profit_loss_ratio,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'avg_holding_period': avg_holding_period,
            'turnover_rate': turnover_rate,
            'total_commission': total_commission,
            'commission_rate': commission_rate,
            'trade_stats': trade_stats
        }
    
    def _calculate_avg_holding_period(self, trades_df: pd.DataFrame) -> float:
        """计算平均持仓周期（天）"""
        # 按股票分组，计算买入到卖出的时间
        holding_periods = []
        
        for security in trades_df['security'].unique():
            security_trades = trades_df[trades_df['security'] == security].sort_values('date')
            
            # 配对买入和卖出
            buy_dates = security_trades[security_trades['action'] == 'buy']['date'].tolist()
            sell_dates = security_trades[security_trades['action'] == 'sell']['date'].tolist()
            
            for buy_date, sell_date in zip(buy_dates, sell_dates):
                period = (pd.to_datetime(sell_date) - pd.to_datetime(buy_date)).days
                if period > 0:
                    holding_periods.append(period)
        
        return np.mean(holding_periods) if holding_periods else 0
    
    def _calculate_turnover_rate(
        self,
        trades_df: pd.DataFrame,
        equity_curve: pd.DataFrame = None
    ) -> float:
        """计算换手率"""
        if equity_curve is None:
            return 0
        
        # 计算总交易金额
        total_trade_value = trades_df['value'].sum()
        
        # 计算平均资产
        avg_equity = equity_curve['equity'].mean()
        
        # 换手率 = 总交易金额 / 平均资产
        return total_trade_value / avg_equity if avg_equity > 0 else 0