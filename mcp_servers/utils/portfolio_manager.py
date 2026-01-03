"""
M5: 多策略组合与执行

策略组合管理、风险控制、执行引擎

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OrderSide(Enum):
    """订单方向"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class Position:
    """持仓"""
    symbol: str
    quantity: int = 0
    avg_cost: float = 0.0
    current_price: float = 0.0
    strategy_id: str = ""
    
    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price
    
    @property
    def pnl(self) -> float:
        return (self.current_price - self.avg_cost) * self.quantity
    
    @property
    def pnl_pct(self) -> float:
        if self.avg_cost == 0:
            return 0
        return (self.current_price - self.avg_cost) / self.avg_cost
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "avg_cost": self.avg_cost,
            "current_price": self.current_price,
            "market_value": self.market_value,
            "pnl": self.pnl,
            "pnl_pct": self.pnl_pct,
            "strategy_id": self.strategy_id
        }


@dataclass
class Order:
    """订单"""
    order_id: str
    symbol: str
    side: OrderSide
    quantity: int
    price: float = 0.0
    order_type: str = "market"
    strategy_id: str = ""
    status: OrderStatus = OrderStatus.PENDING
    filled_qty: int = 0
    filled_price: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type,
            "strategy_id": self.strategy_id,
            "status": self.status.value,
            "filled_qty": self.filled_qty,
            "filled_price": self.filled_price,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class StrategyAllocation:
    """策略配置"""
    strategy_id: str
    strategy_name: str
    weight: float              # 资金权重
    max_positions: int = 10    # 最大持仓数
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "strategy_name": self.strategy_name,
            "weight": self.weight,
            "max_positions": self.max_positions,
            "enabled": self.enabled
        }


@dataclass
class RiskConfig:
    """风险配置"""
    max_position_pct: float = 0.1       # 单票最大仓位
    max_sector_pct: float = 0.3         # 单行业最大仓位
    max_drawdown: float = 0.15          # 最大回撤
    stop_loss_pct: float = 0.08         # 止损线
    take_profit_pct: float = 0.20       # 止盈线
    daily_loss_limit: float = 0.03      # 日亏损限制
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_position_pct": self.max_position_pct,
            "max_sector_pct": self.max_sector_pct,
            "max_drawdown": self.max_drawdown,
            "stop_loss_pct": self.stop_loss_pct,
            "take_profit_pct": self.take_profit_pct,
            "daily_loss_limit": self.daily_loss_limit
        }


class RiskManager:
    """风险管理器"""
    
    def __init__(self, config: RiskConfig):
        self.config = config
        self._alerts: List[Dict] = []
    
    def check_position_limit(self, position_value: float, total_value: float) -> bool:
        """检查单票仓位限制"""
        if total_value == 0:
            return True
        return (position_value / total_value) <= self.config.max_position_pct
    
    def check_stop_loss(self, position: Position) -> bool:
        """检查止损"""
        return position.pnl_pct <= -self.config.stop_loss_pct
    
    def check_take_profit(self, position: Position) -> bool:
        """检查止盈"""
        return position.pnl_pct >= self.config.take_profit_pct
    
    def evaluate_risk_level(self, portfolio_stats: Dict) -> RiskLevel:
        """评估组合风险等级"""
        drawdown = portfolio_stats.get("drawdown", 0)
        daily_pnl = portfolio_stats.get("daily_pnl_pct", 0)
        
        if drawdown > self.config.max_drawdown or daily_pnl < -self.config.daily_loss_limit:
            return RiskLevel.EXTREME
        elif drawdown > self.config.max_drawdown * 0.7:
            return RiskLevel.HIGH
        elif drawdown > self.config.max_drawdown * 0.4:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def generate_risk_signals(self, positions: Dict[str, Position]) -> List[Dict]:
        """生成风险信号"""
        signals = []
        
        for symbol, pos in positions.items():
            if self.check_stop_loss(pos):
                signals.append({
                    "type": "stop_loss",
                    "symbol": symbol,
                    "action": "sell",
                    "reason": f"触发止损({pos.pnl_pct*100:.1f}%)"
                })
            elif self.check_take_profit(pos):
                signals.append({
                    "type": "take_profit",
                    "symbol": symbol,
                    "action": "reduce",
                    "reason": f"触发止盈({pos.pnl_pct*100:.1f}%)"
                })
        
        return signals


class PortfolioManager:
    """组合管理器"""
    
    def __init__(self, initial_capital: float = 1000000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.orders: Dict[str, Order] = {}
        self.strategies: Dict[str, StrategyAllocation] = {}
        self.risk_config = RiskConfig()
        self.risk_manager = RiskManager(self.risk_config)
        self._order_counter = 0
        self._history: List[Dict] = []
    
    # ==================== 策略管理 ====================
    
    def add_strategy(self, allocation: StrategyAllocation) -> bool:
        """添加策略"""
        self.strategies[allocation.strategy_id] = allocation
        logger.info(f"添加策略: {allocation.strategy_name} (权重{allocation.weight:.0%})")
        return True
    
    def remove_strategy(self, strategy_id: str) -> bool:
        """移除策略"""
        if strategy_id in self.strategies:
            del self.strategies[strategy_id]
            return True
        return False
    
    def rebalance_strategies(self) -> Dict[str, float]:
        """重新平衡策略权重"""
        total_weight = sum(s.weight for s in self.strategies.values() if s.enabled)
        if total_weight == 0:
            return {}
        
        allocations = {}
        total_value = self.total_value
        
        for sid, strategy in self.strategies.items():
            if strategy.enabled:
                target_value = total_value * (strategy.weight / total_weight)
                allocations[sid] = target_value
        
        return allocations
    
    # ==================== 持仓管理 ====================
    
    def update_position(self, symbol: str, quantity: int, price: float, 
                       strategy_id: str = "") -> Position:
        """更新持仓"""
        if symbol in self.positions:
            pos = self.positions[symbol]
            if quantity > 0:
                # 买入：计算平均成本
                total_cost = pos.avg_cost * pos.quantity + price * quantity
                pos.quantity += quantity
                pos.avg_cost = total_cost / pos.quantity if pos.quantity > 0 else 0
            else:
                # 卖出
                pos.quantity += quantity  # quantity为负数
                if pos.quantity <= 0:
                    del self.positions[symbol]
                    return pos
            pos.current_price = price
        else:
            pos = Position(
                symbol=symbol,
                quantity=quantity,
                avg_cost=price,
                current_price=price,
                strategy_id=strategy_id
            )
            self.positions[symbol] = pos
        
        return pos
    
    def update_prices(self, prices: Dict[str, float]):
        """更新持仓价格"""
        for symbol, price in prices.items():
            if symbol in self.positions:
                self.positions[symbol].current_price = price
    
    # ==================== 订单管理 ====================
    
    def create_order(self, symbol: str, side: OrderSide, quantity: int,
                    price: float = 0, strategy_id: str = "") -> Order:
        """创建订单"""
        self._order_counter += 1
        order_id = f"ORD{self._order_counter:06d}"
        
        order = Order(
            order_id=order_id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            strategy_id=strategy_id
        )
        self.orders[order_id] = order
        
        logger.info(f"创建订单: {order_id} {side.value} {symbol} x{quantity}")
        return order
    
    def execute_order(self, order_id: str, filled_price: float) -> bool:
        """执行订单(模拟)"""
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        
        # 检查风险
        if order.side == OrderSide.BUY:
            cost = order.quantity * filled_price
            if cost > self.cash:
                order.status = OrderStatus.REJECTED
                return False
            
            # 执行买入
            self.cash -= cost
            self.update_position(order.symbol, order.quantity, filled_price, order.strategy_id)
        else:
            # 执行卖出
            if order.symbol not in self.positions:
                order.status = OrderStatus.REJECTED
                return False
            
            proceeds = order.quantity * filled_price
            self.cash += proceeds
            self.update_position(order.symbol, -order.quantity, filled_price)
        
        order.status = OrderStatus.FILLED
        order.filled_qty = order.quantity
        order.filled_price = filled_price
        order.updated_at = datetime.now()
        
        # 记录历史
        self._history.append({
            "timestamp": datetime.now().isoformat(),
            "order_id": order_id,
            "action": order.side.value,
            "symbol": order.symbol,
            "quantity": order.quantity,
            "price": filled_price
        })
        
        return True
    
    # ==================== 组合统计 ====================
    
    @property
    def total_value(self) -> float:
        """组合总价值"""
        positions_value = sum(p.market_value for p in self.positions.values())
        return self.cash + positions_value
    
    @property
    def total_pnl(self) -> float:
        """总盈亏"""
        return self.total_value - self.initial_capital
    
    @property
    def total_pnl_pct(self) -> float:
        """总收益率"""
        return self.total_pnl / self.initial_capital
    
    def get_stats(self) -> Dict[str, Any]:
        """获取组合统计"""
        positions_value = sum(p.market_value for p in self.positions.values())
        
        return {
            "initial_capital": self.initial_capital,
            "cash": self.cash,
            "positions_value": positions_value,
            "total_value": self.total_value,
            "total_pnl": self.total_pnl,
            "total_pnl_pct": self.total_pnl_pct,
            "position_count": len(self.positions),
            "strategy_count": len(self.strategies),
            "order_count": len(self.orders),
            "risk_level": self.risk_manager.evaluate_risk_level({
                "drawdown": max(0, -self.total_pnl_pct),
                "daily_pnl_pct": 0
            }).value
        }
    
    def get_positions_summary(self) -> List[Dict]:
        """获取持仓摘要"""
        return [p.to_dict() for p in self.positions.values()]
    
    def get_risk_signals(self) -> List[Dict]:
        """获取风险信号"""
        return self.risk_manager.generate_risk_signals(self.positions)


# 全局实例
_portfolio: Optional[PortfolioManager] = None


def get_portfolio(initial_capital: float = 1000000) -> PortfolioManager:
    global _portfolio
    if _portfolio is None:
        _portfolio = PortfolioManager(initial_capital)
    return _portfolio
