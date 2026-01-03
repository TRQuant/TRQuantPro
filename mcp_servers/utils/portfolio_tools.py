"""
Portfolio MCP工具

组合管理与执行工具

Author: TRQuant Team
Date: 2025-12-18
"""

from typing import Dict, Any, List
from mcp.types import Tool

from .portfolio_manager import (
    get_portfolio, StrategyAllocation, OrderSide, RiskConfig
)


PORTFOLIO_TOOLS = [
    Tool(
        name="portfolio.stats",
        description="获取组合统计信息",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="portfolio.positions",
        description="获取持仓列表",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="portfolio.add_strategy",
        description="添加策略到组合",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_id": {"type": "string"},
                "strategy_name": {"type": "string"},
                "weight": {"type": "number", "description": "资金权重(0-1)"},
                "max_positions": {"type": "integer", "default": 10}
            },
            "required": ["strategy_id", "strategy_name", "weight"]
        }
    ),
    Tool(
        name="portfolio.list_strategies",
        description="列出组合中的策略",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="portfolio.rebalance",
        description="重新平衡策略权重",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="portfolio.order",
        description="创建并执行订单",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "side": {"type": "string", "enum": ["buy", "sell"]},
                "quantity": {"type": "integer"},
                "price": {"type": "number"},
                "strategy_id": {"type": "string"}
            },
            "required": ["symbol", "side", "quantity", "price"]
        }
    ),
    Tool(
        name="portfolio.orders",
        description="获取订单列表",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["pending", "filled", "cancelled", "all"]}
            }
        }
    ),
    Tool(
        name="portfolio.risk_signals",
        description="获取风险信号(止损/止盈)",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="portfolio.update_prices",
        description="更新持仓价格",
        inputSchema={
            "type": "object",
            "properties": {
                "prices": {"type": "object", "description": "{symbol: price}"}
            },
            "required": ["prices"]
        }
    ),
    Tool(
        name="portfolio.set_risk",
        description="设置风险参数",
        inputSchema={
            "type": "object",
            "properties": {
                "max_position_pct": {"type": "number"},
                "stop_loss_pct": {"type": "number"},
                "take_profit_pct": {"type": "number"},
                "max_drawdown": {"type": "number"}
            }
        }
    )
]


def _handle_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    return {"status": "success", **portfolio.get_stats()}


def _handle_positions(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    positions = portfolio.get_positions_summary()
    return {
        "status": "success",
        "count": len(positions),
        "positions": positions
    }


def _handle_add_strategy(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    
    allocation = StrategyAllocation(
        strategy_id=args.get("strategy_id", ""),
        strategy_name=args.get("strategy_name", ""),
        weight=args.get("weight", 0.1),
        max_positions=args.get("max_positions", 10)
    )
    
    portfolio.add_strategy(allocation)
    return {
        "status": "success",
        "strategy": allocation.to_dict()
    }


def _handle_list_strategies(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    strategies = [s.to_dict() for s in portfolio.strategies.values()]
    return {
        "status": "success",
        "count": len(strategies),
        "strategies": strategies
    }


def _handle_rebalance(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    allocations = portfolio.rebalance_strategies()
    return {
        "status": "success",
        "total_value": portfolio.total_value,
        "allocations": allocations
    }


def _handle_order(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    
    symbol = args.get("symbol", "")
    side = OrderSide.BUY if args.get("side") == "buy" else OrderSide.SELL
    quantity = args.get("quantity", 0)
    price = args.get("price", 0)
    strategy_id = args.get("strategy_id", "")
    
    order = portfolio.create_order(symbol, side, quantity, price, strategy_id)
    success = portfolio.execute_order(order.order_id, price)
    
    return {
        "status": "success" if success else "failed",
        "order": order.to_dict()
    }


def _handle_orders(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    status_filter = args.get("status", "all")
    
    orders = []
    for order in portfolio.orders.values():
        if status_filter == "all" or order.status.value == status_filter:
            orders.append(order.to_dict())
    
    return {
        "status": "success",
        "count": len(orders),
        "orders": orders
    }


def _handle_risk_signals(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    signals = portfolio.get_risk_signals()
    return {
        "status": "success",
        "count": len(signals),
        "signals": signals
    }


def _handle_update_prices(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    prices = args.get("prices", {})
    
    portfolio.update_prices(prices)
    return {
        "status": "success",
        "updated": len(prices),
        "total_value": portfolio.total_value
    }


def _handle_set_risk(args: Dict[str, Any]) -> Dict[str, Any]:
    portfolio = get_portfolio()
    
    if "max_position_pct" in args:
        portfolio.risk_config.max_position_pct = args["max_position_pct"]
    if "stop_loss_pct" in args:
        portfolio.risk_config.stop_loss_pct = args["stop_loss_pct"]
    if "take_profit_pct" in args:
        portfolio.risk_config.take_profit_pct = args["take_profit_pct"]
    if "max_drawdown" in args:
        portfolio.risk_config.max_drawdown = args["max_drawdown"]
    
    return {
        "status": "success",
        "risk_config": portfolio.risk_config.to_dict()
    }


PORTFOLIO_HANDLERS = {
    "portfolio.stats": _handle_stats,
    "portfolio.positions": _handle_positions,
    "portfolio.add_strategy": _handle_add_strategy,
    "portfolio.list_strategies": _handle_list_strategies,
    "portfolio.rebalance": _handle_rebalance,
    "portfolio.order": _handle_order,
    "portfolio.orders": _handle_orders,
    "portfolio.risk_signals": _handle_risk_signals,
    "portfolio.update_prices": _handle_update_prices,
    "portfolio.set_risk": _handle_set_risk
}
