"""
文件名: code_8_1___init__.py
保存路径: code_library/008_Chapter8_Backtest/8.1/code_8_1___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.1_Backtest_Framework_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class Portfolio:
    """投资组合"""
    
    def __init__(self, initial_cash: float = 1000000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.total_value_history = []
        self.cash_history = []
        self.date_history = []
    
    def add_position(self, security: str, amount: float, price: float):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        if security in self.positions:
            # 更新持仓
            pos = self.positions[security]
            total_cost = pos.cost_value + amount * price
            total_amount = pos.amount + amount
            pos.amount = total_amount
            pos.cost_price = total_cost / total_amount if total_amount > 0 else price
        else:
            # 新建持仓
            self.positions[security] = Position(security, amount, price)
    
    def remove_position(self, security: str, amount: float, price: float):
        """减少持仓"""
        if security not in self.positions:
            return
        
        pos = self.positions[security]
        if amount >= pos.amount:
            del self.positions[security]
        else:
            pos.amount -= amount
    
    def get_total_value(self) -> float:
        """获取总资产"""
        positions_value = sum(pos.market_value for pos in self.positions.values())
        return self.cash + positions_value