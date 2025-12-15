# -*- coding: utf-8 -*-
"""
回测MCP服务器（增强版 v2.0）
============================
支持三层回测架构：
- Fast: 快速验证 (<5秒)
- Standard: 标准回测 (<30秒)
- Precise: 精确回测 (BulletTrade/QMT)

支持多周期：日/周/分钟
支持多策略：动量/均值回归/自定义
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("backtest-server-v2")


TOOLS = [
    # 快速回测
    Tool(
        name="backtest.fast",
        description="快速回测 - 向量化计算，<5秒完成，用于策略初筛",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "start_date": {"type": "string", "description": "开始日期 YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "结束日期 YYYY-MM-DD"},
                "strategy": {
                    "type": "string",
                    "description": "策略类型: momentum/mean_reversion",
                    "default": "momentum"
                },
                "lookback": {"type": "integer", "description": "回看周期", "default": 20},
                "top_n": {"type": "integer", "description": "选股数量", "default": 10}
            },
            "required": ["securities", "start_date", "end_date"]
        }
    ),
    # 标准回测
    Tool(
        name="backtest.standard",
        description="标准回测 - 事件驱动，完整交易成本模拟",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "strategy": {"type": "string", "default": "momentum"},
                "initial_capital": {"type": "number", "default": 1000000},
                "commission_rate": {"type": "number", "default": 0.0003}
            },
            "required": ["securities", "start_date", "end_date"]
        }
    ),
    # BulletTrade回测
    Tool(
        name="backtest.bullettrade",
        description="BulletTrade精确回测 - 完整模拟，支持复杂策略",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_code": {"type": "string", "description": "策略代码"},
                "strategy_file": {"type": "string", "description": "策略文件路径"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "initial_capital": {"type": "number", "default": 1000000},
                "frequency": {"type": "string", "default": "1d"}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    # QMT回测
    Tool(
        name="backtest.qmt",
        description="QMT回测 - 使用xtquant引擎",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_code": {"type": "string"},
                "stock_pool": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "data_period": {
                    "type": "string",
                    "description": "数据周期: 1d/1m/5m/15m/30m/60m",
                    "default": "1d"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    # 完整流程
    Tool(
        name="backtest.full_pipeline",
        description="完整回测流程 - 从策略生成到结果分析",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "strategy": {"type": "string", "default": "momentum"},
                "levels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "回测层级: fast/standard/precise",
                    "default": ["fast"]
                }
            },
            "required": ["securities", "start_date", "end_date"]
        }
    ),
    # 结果对比
    Tool(
        name="backtest.compare",
        description="对比多个回测结果",
        inputSchema={
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "回测结果列表"
                }
            },
            "required": ["results"]
        }
    )
]


def _init_path():
    import sys
    base = str(__file__).rsplit("/mcp_servers", 1)[0]
    if base not in sys.path:
        sys.path.insert(0, base)


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        _init_path()
        
        if name == "backtest.fast":
            result = await _handle_fast(arguments)
        elif name == "backtest.standard":
            result = await _handle_standard(arguments)
        elif name == "backtest.bullettrade":
            result = await _handle_bullettrade(arguments)
        elif name == "backtest.qmt":
            result = await _handle_qmt(arguments)
        elif name == "backtest.full_pipeline":
            result = await _handle_full_pipeline(arguments)
        elif name == "backtest.compare":
            result = await _handle_compare(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.exception(f"工具执行错误: {name}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_fast(args: Dict) -> Dict:
    """快速回测"""
    from core.backtest import (
        UnifiedBacktestManager, 
        UnifiedBacktestConfig,
        MomentumStrategy,
        MeanReversionStrategy
    )
    
    config = UnifiedBacktestConfig(
        start_date=args["start_date"],
        end_date=args["end_date"],
        securities=args["securities"],
        use_mock=True
    )
    
    manager = UnifiedBacktestManager(config)
    
    # 创建策略
    strategy_type = args.get("strategy", "momentum")
    params = {
        "lookback": args.get("lookback", 20),
        "top_n": args.get("top_n", 10)
    }
    
    if strategy_type == "momentum":
        strategy = MomentumStrategy(params)
    elif strategy_type == "mean_reversion":
        strategy = MeanReversionStrategy(params)
    else:
        return {"error": f"未知策略类型: {strategy_type}"}
    
    result = manager.run_fast(strategy)
    
    return {
        "success": result.success,
        "level": "fast",
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "calmar_ratio": round(result.calmar_ratio, 2),
            "win_rate": f"{result.win_rate*100:.1f}%"
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "error": result.error
    }


async def _handle_standard(args: Dict) -> Dict:
    """标准回测"""
    from core.backtest import (
        UnifiedBacktestManager,
        UnifiedBacktestConfig,
        MomentumStrategy
    )
    
    config = UnifiedBacktestConfig(
        start_date=args["start_date"],
        end_date=args["end_date"],
        securities=args["securities"],
        initial_capital=args.get("initial_capital", 1000000),
        commission_rate=args.get("commission_rate", 0.0003),
        use_mock=True
    )
    
    manager = UnifiedBacktestManager(config)
    strategy = MomentumStrategy({"lookback": 20, "top_n": 10})
    
    result = manager.run_standard(strategy)
    
    return {
        "success": result.success,
        "level": "standard",
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%",
            "total_trades": result.total_trades
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "error": result.error
    }


async def _handle_bullettrade(args: Dict) -> Dict:
    """BulletTrade回测"""
    try:
        from core.bullettrade import BulletTradeEngine, BTConfig
        
        bt_config = BTConfig(
            start_date=args["start_date"],
            end_date=args["end_date"],
            initial_capital=args.get("initial_capital", 1000000),
            frequency=args.get("frequency", "1d")
        )
        
        engine = BulletTradeEngine(bt_config)
        
        if args.get("strategy_code"):
            result = engine.run_backtest(strategy_code=args["strategy_code"])
        elif args.get("strategy_file"):
            result = engine.run_backtest(strategy_path=args["strategy_file"])
        else:
            return {"error": "需要提供 strategy_code 或 strategy_file"}
        
        return {
            "success": result.success,
            "level": "precise",
            "engine": "bullettrade",
            "metrics": {
                "total_return": f"{result.total_return:.2f}%",
                "annual_return": f"{result.annual_return:.2f}%",
                "sharpe_ratio": round(result.sharpe_ratio or 0, 2),
                "max_drawdown": f"{result.max_drawdown:.2f}%",
                "win_rate": f"{(result.win_rate or 0)*100:.1f}%"
            }
        }
    except ImportError:
        return {"error": "BulletTrade未安装，请执行: pip install bullet-trade"}
    except Exception as e:
        return {"error": f"BulletTrade回测失败: {e}"}


async def _handle_qmt(args: Dict) -> Dict:
    """QMT回测"""
    try:
        from core.qmt import run_qmt_backtest, QMTDataPeriod
        
        # 解析周期
        period_map = {
            "1d": QMTDataPeriod.DAILY,
            "1m": QMTDataPeriod.MIN_1,
            "5m": QMTDataPeriod.MIN_5,
            "15m": QMTDataPeriod.MIN_15,
            "30m": QMTDataPeriod.MIN_30,
            "60m": QMTDataPeriod.MIN_60,
        }
        
        result = run_qmt_backtest(
            strategy_code=args.get("strategy_code", ""),
            start_date=args["start_date"],
            end_date=args["end_date"],
            stock_pool=args.get("stock_pool", []),
            data_period=period_map.get(args.get("data_period", "1d"), QMTDataPeriod.DAILY)
        )
        
        return {
            "success": result.success,
            "level": "precise",
            "engine": "qmt",
            "message": result.message,
            "metrics": {
                "total_return": f"{result.total_return*100:.2f}%",
                "annual_return": f"{result.annual_return*100:.2f}%",
                "sharpe_ratio": round(result.sharpe_ratio, 2),
                "max_drawdown": f"{result.max_drawdown*100:.2f}%"
            },
            "duration_seconds": round(result.duration_seconds, 2)
        }
    except Exception as e:
        return {"error": f"QMT回测失败: {e}"}


async def _handle_full_pipeline(args: Dict) -> Dict:
    """完整回测流程"""
    from core.backtest import UnifiedBacktestManager, UnifiedBacktestConfig, BacktestLevel
    
    config = UnifiedBacktestConfig(
        start_date=args["start_date"],
        end_date=args["end_date"],
        securities=args["securities"],
        use_mock=True
    )
    
    manager = UnifiedBacktestManager(config)
    
    levels = [BacktestLevel(l) for l in args.get("levels", ["fast"])]
    
    results = manager.run_full_pipeline(
        strategy_type=args.get("strategy", "momentum"),
        levels=levels
    )
    
    output = {"success": True, "results": {}}
    
    for level, result in results.items():
        if hasattr(result, 'success'):
            output["results"][level] = {
                "success": result.success,
                "total_return": f"{result.total_return*100:.2f}%",
                "sharpe_ratio": round(result.sharpe_ratio, 2),
                "max_drawdown": f"{result.max_drawdown*100:.2f}%",
                "duration": round(result.duration_seconds, 2)
            }
    
    return output


async def _handle_compare(args: Dict) -> Dict:
    """对比回测结果"""
    results = args.get("results", [])
    
    if not results:
        return {"error": "没有提供回测结果"}
    
    comparison = []
    for i, r in enumerate(results):
        comparison.append({
            "index": i + 1,
            "name": r.get("name", f"策略{i+1}"),
            "total_return": r.get("total_return", "N/A"),
            "sharpe_ratio": r.get("sharpe_ratio", "N/A"),
            "max_drawdown": r.get("max_drawdown", "N/A")
        })
    
    return {
        "success": True,
        "comparison": comparison,
        "best": max(comparison, key=lambda x: float(str(x.get("sharpe_ratio", 0)).replace("N/A", "0")))
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="backtest-server-v2",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
