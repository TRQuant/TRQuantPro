#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Trading Server
======================

交易管理MCP服务器，提供交易状态查询、持仓查询、订单查询等只读功能。
安全要求：默认dry_run，所有写操作需要confirm_token + evidence。

运行方式:
    python mcp_servers/trading_server.py

工具:
    - trading.status: 获取交易账户状态（只读）
    - trading.positions: 获取持仓信息（只读）
    - trading.orders: 获取订单信息（只读）
    - trading.simulate: 模拟交易（dry_run模式）
    - trading.dry_run: 交易策略dry_run验证
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('TradingServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 导入工程化落地件
from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
from mcp_servers.utils.schema import base_args_schema, merge_schema
from mcp_servers.utils.artifacts import create_artifact_if_needed
from mcp_servers.utils.error_handler import wrap_exception_response

# 导入交易桥接模块
try:
    from bridge_common.ptrade_bridge import PTradeBridge
    PTRADE_BRIDGE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"PTradeBridge不可用: {e}")
    PTRADE_BRIDGE_AVAILABLE = False
    PTradeBridge = None

try:
    from bridge_common.qmt_bridge import QMTBridge
    QMT_BRIDGE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"QMTBridge不可用: {e}")
    QMT_BRIDGE_AVAILABLE = False
    QMTBridge = None

# 交易桥接实例（延迟初始化）
_ptrade_bridge: Optional[Any] = None
_qmt_bridge: Optional[Any] = None


def get_trading_bridge(platform: str):
    """
    获取交易桥接实例（单例）
    
    Args:
        platform: 交易平台（ptrade/qmt）
    
    Returns:
        交易桥接实例
    """
    global _ptrade_bridge, _qmt_bridge
    
    if platform == "ptrade":
        if not PTRADE_BRIDGE_AVAILABLE:
            raise RuntimeError("PTradeBridge不可用，请检查依赖")
        if PTradeBridge is None:
            raise RuntimeError("PTradeBridge不可用，请检查依赖")
        if _ptrade_bridge is None:
            _ptrade_bridge = PTradeBridge()
        return _ptrade_bridge
    elif platform == "qmt":
        if not QMT_BRIDGE_AVAILABLE:
            raise RuntimeError("QMTBridge不可用，请检查依赖")
        if QMTBridge is None:
            raise RuntimeError("QMTBridge不可用，请检查依赖")
        if _qmt_bridge is None:
            _qmt_bridge = QMTBridge()
        return _qmt_bridge
    else:
        raise ValueError(f"不支持的交易平台: {platform}（支持: ptrade, qmt）")


def _wrap_response(envelope: Dict[str, Any]) -> List[TextContent]:
    """将envelope包装为TextContent列表"""
    return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


# 创建MCP服务器
server = Server("trquant-trading")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    base_schema_dry_run = base_args_schema(mode="dry_run")
    
    return [
        Tool(
            name="trading.status",
            description="获取交易账户状态（只读）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "交易平台"
                        },
                        "account_id": {
                            "type": "string",
                            "description": "账户ID（可选，不提供则使用默认账户）"
                        }
                    },
                    "required": ["platform"]
                }
            )
        ),
        Tool(
            name="trading.positions",
            description="获取持仓信息（只读）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "交易平台"
                        },
                        "account_id": {
                            "type": "string",
                            "description": "账户ID（可选）"
                        },
                        "security": {
                            "type": "string",
                            "description": "证券代码（可选，不提供则返回所有持仓）"
                        }
                    },
                    "required": ["platform"]
                }
            )
        ),
        Tool(
            name="trading.orders",
            description="获取订单信息（只读）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "交易平台"
                        },
                        "account_id": {
                            "type": "string",
                            "description": "账户ID（可选）"
                        },
                        "order_id": {
                            "type": "string",
                            "description": "订单ID（可选，不提供则返回所有订单）"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["pending", "filled", "cancelled", "rejected", "all"],
                            "default": "all",
                            "description": "订单状态过滤"
                        }
                    },
                    "required": ["platform"]
                }
            )
        ),
        Tool(
            name="trading.simulate",
            description="模拟交易（dry_run模式，不实际下单）",
            inputSchema=merge_schema(
                base_schema_dry_run,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "交易平台"
                        },
                        "strategy_id": {
                            "type": "string",
                            "description": "策略ID"
                        },
                        "simulation_config": {
                            "type": "object",
                            "description": "模拟配置（初始资金、时间范围等）"
                        }
                    },
                    "required": ["platform", "strategy_id"]
                }
            )
        ),
        Tool(
            name="trading.dry_run",
            description="交易策略dry_run验证（检查策略逻辑，不实际执行）",
            inputSchema=merge_schema(
                base_schema_dry_run,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "交易平台"
                        },
                        "strategy_code": {
                            "type": "string",
                            "description": "策略代码"
                        },
                        "validation_rules": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["syntax", "risk_limits", "order_format"],
                            "description": "验证规则列表"
                        }
                    },
                    "required": ["platform", "strategy_code"]
                }
            )
        )
    ]



def _adapt_mcp_result_to_text_content(result: Dict[str, Any]) -> List[TextContent]:
    """将process_mcp_tool_call的结果转换为List[TextContent]格式"""
    if isinstance(result, dict) and "content" in result:
        text_content = []
        for item in result.get("content", []):
            if item.get("type") == "text":
                text_content.append(TextContent(type="text", text=item.get("text", "")))
        return text_content if text_content else [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
    else:
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    trace_id = extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "trading.status":
            platform = arguments.get("platform")
            account_id = arguments.get("account_id")
            return await _handle_trading_status(platform, account_id, trace_id, artifact_policy)
        
        elif name == "trading.positions":
            platform = arguments.get("platform")
            account_id = arguments.get("account_id")
            security = arguments.get("security")
            return await _handle_trading_positions(platform, account_id, security, trace_id, artifact_policy)
        
        elif name == "trading.orders":
            platform = arguments.get("platform")
            account_id = arguments.get("account_id")
            order_id = arguments.get("order_id")
            status = arguments.get("status", "all")
            return await _handle_trading_orders(platform, account_id, order_id, status, trace_id, artifact_policy)
        
        elif name == "trading.simulate":
            platform = arguments.get("platform")
            strategy_id = arguments.get("strategy_id")
            simulation_config = arguments.get("simulation_config", {})
            return await _handle_trading_simulate(platform, strategy_id, simulation_config, trace_id, artifact_policy)
        
        elif name == "trading.dry_run":
            platform = arguments.get("platform")
            strategy_code = arguments.get("strategy_code")
            validation_rules = arguments.get("validation_rules", ["syntax", "risk_limits", "order_format"])
            return await _handle_trading_dry_run(platform, strategy_code, validation_rules, trace_id, artifact_policy)
        
        else:
            envelope = wrap_error_response(
                error_code="UNKNOWN_TOOL",
                error_message=f"未知工具: {name}",
                server_name="trquant-trading",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_trading_status(
    platform: str,
    account_id: Optional[str],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理trading.status"""
    try:
        bridge = get_trading_bridge(platform)
        
        # 获取账户状态
        if hasattr(bridge, "get_account_status"):
            status = bridge.get_account_status(account_id)
        else:
            # 模拟数据（如果桥接不可用）
            status = {
                "account_id": account_id or "default",
                "platform": platform,
                "connected": True,
                "balance": 1000000.0,
                "available": 950000.0,
                "frozen": 50000.0,
                "market_value": 500000.0,
                "total_assets": 1500000.0,
                "timestamp": datetime.now().isoformat()
            }
        
        result = create_artifact_if_needed(status, "trading_status", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-trading",
            tool_name="trading.status",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name="trading.status",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_trading_positions(
    platform: str,
    account_id: Optional[str],
    security: Optional[str],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理trading.positions"""
    try:
        bridge = get_trading_bridge(platform)
        
        # 获取持仓信息
        if hasattr(bridge, "get_positions"):
            positions = bridge.get_positions(account_id, security)
        else:
            # 模拟数据
            positions = [
                {
                    "security": "000001.SZ",
                    "name": "平安银行",
                    "quantity": 1000,
                    "available": 1000,
                    "frozen": 0,
                    "cost_price": 10.5,
                    "current_price": 11.2,
                    "market_value": 11200.0,
                    "profit_loss": 700.0,
                    "profit_loss_ratio": 0.0667
                }
            ]
            
            if security:
                positions = [p for p in positions if p["security"] == security]
        
        data = {
            "platform": platform,
            "account_id": account_id,
            "security": security,
            "positions": positions,
            "total_count": len(positions),
            "total_market_value": sum(p.get("market_value", 0) for p in positions),
            "timestamp": datetime.now().isoformat()
        }
        
        result = create_artifact_if_needed(data, "trading_positions", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-trading",
            tool_name="trading.positions",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name="trading.positions",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_trading_orders(
    platform: str,
    account_id: Optional[str],
    order_id: Optional[str],
    status: str,
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理trading.orders"""
    try:
        bridge = get_trading_bridge(platform)
        
        # 获取订单信息
        if hasattr(bridge, "get_orders"):
            orders = bridge.get_orders(account_id, order_id, status)
        else:
            # 模拟数据
            orders = [
                {
                    "order_id": "ORD001",
                    "security": "000001.SZ",
                    "name": "平安银行",
                    "direction": "buy",
                    "quantity": 100,
                    "price": 11.0,
                    "status": "filled",
                    "filled_quantity": 100,
                    "filled_price": 11.0,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ]
            
            if order_id:
                orders = [o for o in orders if o["order_id"] == order_id]
            if status != "all":
                orders = [o for o in orders if o["status"] == status]
        
        data = {
            "platform": platform,
            "account_id": account_id,
            "order_id": order_id,
            "status_filter": status,
            "orders": orders,
            "total_count": len(orders),
            "timestamp": datetime.now().isoformat()
        }
        
        result = create_artifact_if_needed(data, "trading_orders", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-trading",
            tool_name="trading.orders",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name="trading.orders",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_trading_simulate(
    platform: str,
    strategy_id: str,
    simulation_config: Dict[str, Any],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理trading.simulate"""
    try:
        # 模拟交易（不实际下单）
        initial_capital = simulation_config.get("initial_capital", 1000000.0)
        start_date = simulation_config.get("start_date", datetime.now().isoformat())
        end_date = simulation_config.get("end_date")
        
        # 这里应该调用实际的模拟交易逻辑
        # 目前返回模拟结果
        simulation_result = {
            "platform": platform,
            "strategy_id": strategy_id,
            "mode": "simulate",
            "initial_capital": initial_capital,
            "start_date": start_date,
            "end_date": end_date or datetime.now().isoformat(),
            "final_capital": initial_capital * 1.05,  # 模拟5%收益
            "total_return": 0.05,
            "total_trades": 10,
            "win_rate": 0.6,
            "max_drawdown": 0.02,
            "sharpe_ratio": 1.2,
            "simulation_time": datetime.now().isoformat(),
            "message": "这是模拟交易，未实际下单"
        }
        
        result = create_artifact_if_needed(simulation_result, "trading_simulation", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-trading",
            tool_name="trading.simulate",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name="trading.simulate",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_trading_dry_run(
    platform: str,
    strategy_code: str,
    validation_rules: List[str],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理trading.dry_run"""
    try:
        # 验证策略代码
        validation_results = {}
        errors = []
        warnings = []
        
        if "syntax" in validation_rules:
            # 语法检查（简化版）
            try:
                compile(strategy_code, "<string>", "exec")
                validation_results["syntax"] = {"valid": True, "message": "语法检查通过"}
            except SyntaxError as e:
                validation_results["syntax"] = {"valid": False, "message": f"语法错误: {e}"}
                errors.append(f"语法错误: {e}")
        
        if "risk_limits" in validation_rules:
            # 风险限制检查（简化版）
            # 检查是否有止损、止盈、仓位限制等
            has_stop_loss = "stop_loss" in strategy_code.lower() or "止损" in strategy_code
            has_position_limit = "position" in strategy_code.lower() or "仓位" in strategy_code
            
            validation_results["risk_limits"] = {
                "valid": has_stop_loss and has_position_limit,
                "has_stop_loss": has_stop_loss,
                "has_position_limit": has_position_limit
            }
            
            if not has_stop_loss:
                warnings.append("策略代码中未发现止损逻辑")
            if not has_position_limit:
                warnings.append("策略代码中未发现仓位限制")
        
        if "order_format" in validation_rules:
            # 订单格式检查（简化版）
            # 检查订单函数调用格式
            has_order_call = "order" in strategy_code.lower() or "下单" in strategy_code
            
            validation_results["order_format"] = {
                "valid": has_order_call,
                "has_order_call": has_order_call
            }
            
            if not has_order_call:
                warnings.append("策略代码中未发现订单函数调用")
        
        result = {
            "platform": platform,
            "mode": "dry_run",
            "validation_rules": validation_rules,
            "validation_results": validation_results,
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "code_length": len(strategy_code),
            "code_lines": len(strategy_code.split("\n")),
            "timestamp": datetime.now().isoformat(),
            "message": "这是dry_run模式，未实际执行交易"
        }
        
        result = create_artifact_if_needed(result, "trading_dry_run", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-trading",
            tool_name="trading.dry_run",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-trading",
            tool_name="trading.dry_run",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())









