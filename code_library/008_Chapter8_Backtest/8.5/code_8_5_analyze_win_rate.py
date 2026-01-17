"""
文件名: code_8_5_analyze_win_rate.py
保存路径: code_library/008_Chapter8_Backtest/8.5/code_8_5_analyze_win_rate.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.5_Trade_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: analyze_win_rate

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np
from typing import Dict, List, Optional

class WinRateAnalyzer:
    """胜率分析器"""
    
    def analyze_win_rate(
        self,
        trades: List[TradeRecord]
    ) -> Dict[str, Any]:
            """
    analyze_win_rate函数
    
    **设计原理**：
    - **核心功能**：实现analyze_win_rate的核心逻辑
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
        # 只考虑卖出交易
        sell_trades = [t for t in trades if t.action == 'sell']
        
        if not sell_trades:
            return {}
        
        # 盈利和亏损交易
        winning_trades = [t for t in sell_trades if t.pnl > 0]
        losing_trades = [t for t in sell_trades if t.pnl < 0]
        breakeven_trades = [t for t in sell_trades if t.pnl == 0]
        
        # 胜率
        win_rate = len(winning_trades) / len(sell_trades) if len(sell_trades) > 0 else 0
        
        # 平均盈利和平均亏损
        avg_profit = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        avg_loss = abs(np.mean([t.pnl for t in losing_trades])) if losing_trades else 0
        
        # 盈亏比
        profit_loss_ratio = avg_profit / avg_loss if avg_loss > 0 else 0
        
        # 总盈利和总亏损
        total_profit = sum([t.pnl for t in winning_trades])
        total_loss = abs(sum([t.pnl for t in losing_trades]))
        
        # 盈亏分布
        pnl_distribution = self._analyze_pnl_distribution(sell_trades)
        
        return {
            'total_trades': len(sell_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'breakeven_trades': len(breakeven_trades),
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'avg_loss': avg_loss,
            'profit_loss_ratio': profit_loss_ratio,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'net_pnl': total_profit - total_loss,
            'pnl_distribution': pnl_distribution
        }
    
    def _analyze_pnl_distribution(self, trades: List[TradeRecord]) -> Dict[str, int]:
        """分析盈亏分布"""
        pnls = [t.pnl for t in trades]
        
        return {
            '>10%': len([p for p in pnls if p > 0.1]),
            '5%-10%': len([p for p in pnls if 0.05 < p <= 0.1]),
            '0-5%': len([p for p in pnls if 0 < p <= 0.05]),
            '0': len([p for p in pnls if p == 0]),
            '-5%-0': len([p for p in pnls if -0.05 <= p < 0]),
            '-10%--5%': len([p for p in pnls if -0.1 <= p < -0.05]),
            '<-10%': len([p for p in pnls if p < -0.1])
        }