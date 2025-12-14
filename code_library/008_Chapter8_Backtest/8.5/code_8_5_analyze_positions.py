"""
文件名: code_8_5_analyze_positions.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_analyze_positions.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_positions

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class PositionAnalyzer:
    """持仓分析器"""
    
    def analyze_positions(
        self,
        trades: List[TradeRecord]
    ) -> Dict[str, Any]:
            """
    analyze_positions函数
    
    **设计原理**：
    - **核心功能**：实现analyze_positions的核心逻辑
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
                'date': pd.to_datetime(t.date),
                'security': t.security,
                'action': t.action,
                'amount': t.amount if t.action == 'buy' else -t.amount
            }
            for t in trades
        ])
        
        # 计算持仓周期
        holding_periods = self._calculate_holding_periods(trades_df)
        
        # 持仓集中度（同时持有的股票数量）
        position_concentration = self._analyze_position_concentration(trades_df)
        
        # 持仓轮换（股票更换频率）
        position_rotation = self._analyze_position_rotation(trades_df)
        
        return {
            'avg_holding_period': np.mean(holding_periods) if holding_periods else 0,
            'median_holding_period': np.median(holding_periods) if holding_periods else 0,
            'max_holding_period': max(holding_periods) if holding_periods else 0,
            'min_holding_period': min(holding_periods) if holding_periods else 0,
            'holding_periods': holding_periods,
            'position_concentration': position_concentration,
            'position_rotation': position_rotation
        }
    
    def _calculate_holding_periods(self, trades_df: pd.DataFrame) -> List[int]:
        """计算持仓周期"""
        holding_periods = []
        
        for security in trades_df['security'].unique():
            security_trades = trades_df[trades_df['security'] == security].sort_values('date')
            
            # 配对买入和卖出
            buy_dates = security_trades[security_trades['amount'] > 0]['date'].tolist()
            sell_dates = security_trades[security_trades['amount'] < 0]['date'].tolist()
            
            for buy_date, sell_date in zip(buy_dates, sell_dates):
                period = (sell_date - buy_date).days
                if period > 0:
                    holding_periods.append(period)
        
        return holding_periods
    
    def _analyze_position_concentration(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """分析持仓集中度"""
        # 按日期统计持仓股票数量
        trades_df = trades_df.sort_values('date')
        position_counts = []
        
        current_positions = {}
        for _, trade in trades_df.iterrows():
            security = trade['security']
            amount = trade['amount']
            
            if security not in current_positions:
                current_positions[security] = 0
            current_positions[security] += amount
            
            if current_positions[security] <= 0:
                del current_positions[security]
            
            position_counts.append(len(current_positions))
        
        return {
            'avg_position_count': np.mean(position_counts) if position_counts else 0,
            'max_position_count': max(position_counts) if position_counts else 0,
            'min_position_count': min(position_counts) if position_counts else 0
        }
    
    def _analyze_position_rotation(self, trades_df: pd.DataFrame) -> Dict[str, Any]:
        """分析持仓轮换"""
        # 计算持仓更换频率
        trades_df = trades_df.sort_values('date')
        rotation_count = 0
        
        current_positions = set()
        for _, trade in trades_df.iterrows():
            security = trade['security']
            
            if trade['action'] == 'buy':
                if security not in current_positions:
                    current_positions.add(security)
            else:  # sell
                if security in current_positions:
                    current_positions.remove(security)
                    rotation_count += 1
        
        return {
            'rotation_count': rotation_count,
            'rotation_frequency': rotation_count / len(trades_df) if len(trades_df) > 0 else 0
        }