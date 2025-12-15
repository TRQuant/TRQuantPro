# -*- coding: utf-8 -*-
"""
回测MCP服务器（标准化版本）
========================
提供快速回测、策略对比、参数优化等功能
"""

import logging
import json
from typing import Dict, List, Any, Optional
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)

# 创建服务器
server = Server("backtest-server")


# ==================== 工具定义 ====================

TOOLS = [
    Tool(
        name="backtest.bullettrade",
        description="使用BulletTrade引擎执行真实回测（聚宽数据源）",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_path": {"type": "string", "description": "策略文件路径"},
                "strategy_code": {"type": "string", "description": "策略代码（与path二选一）"},
                "start_date": {"type": "string", "description": "开始日期，如2024-01-01"},
                "end_date": {"type": "string", "description": "结束日期，如2024-06-30"},
                "initial_capital": {"type": "number", "description": "初始资金", "default": 1000000},
                "benchmark": {"type": "string", "description": "基准指数", "default": "000300.XSHG"},
                "save_to_db": {"type": "boolean", "description": "是否保存到数据库", "default": True}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.bullettrade_batch",
        description="BulletTrade批量回测多个策略",
        inputSchema={
            "type": "object",
            "properties": {
                "strategies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "path": {"type": "string"},
                            "code": {"type": "string"}
                        }
                    },
                    "description": "策略列表"
                },
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "initial_capital": {"type": "number", "default": 1000000}
            },
            "required": ["strategies", "start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.bullettrade_optimize",
        description="BulletTrade参数优化",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_path": {"type": "string", "description": "策略文件路径"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如{\"MAX_STOCKS\": [5,8,10], \"STOP_LOSS\": [-0.05,-0.08]}"
                },
                "target_metric": {"type": "string", "default": "sharpe_ratio"},
                "method": {"type": "string", "default": "grid", "description": "grid/random/bayesian"}
            },
            "required": ["strategy_path", "start_date", "end_date", "param_grid"]
        }
    ),
    Tool(
        name="backtest.qmt",
        description="使用QMT(xtquant)引擎执行回测",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_path": {"type": "string", "description": "策略文件路径"},
                "strategy_code": {"type": "string", "description": "策略代码（与path二选一）"},
                "start_date": {"type": "string", "description": "开始日期，如2024-01-01"},
                "end_date": {"type": "string", "description": "结束日期，如2024-06-30"},
                "initial_capital": {"type": "number", "description": "初始资金", "default": 1000000},
                "benchmark": {"type": "string", "description": "基准指数", "default": "000300.SH"},
                "stock_pool": {"type": "array", "items": {"type": "string"}, "description": "股票池"},
                "qmt_path": {"type": "string", "description": "miniQMT路径"},
                "save_to_db": {"type": "boolean", "description": "是否保存到数据库", "default": True}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.qmt_batch",
        description="QMT批量回测多个策略",
        inputSchema={
            "type": "object",
            "properties": {
                "strategies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "path": {"type": "string"},
                            "code": {"type": "string"}
                        }
                    },
                    "description": "策略列表"
                },
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "initial_capital": {"type": "number", "default": 1000000}
            },
            "required": ["strategies", "start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.qmt_optimize",
        description="QMT参数优化",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_path": {"type": "string", "description": "策略文件路径"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如{"MAX_STOCKS": [5,8,10], "STOP_LOSS": [-0.05,-0.08]}"
                },
                "target_metric": {"type": "string", "default": "sharpe_ratio"},
                "method": {"type": "string", "default": "grid", "description": "grid/random"}
            },
            "required": ["strategy_path", "start_date", "end_date", "param_grid"]
        }
    ),
    Tool(
        name="backtest.quick",
        description="执行快速回测（向量化引擎，<1秒完成）",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表，如['000001.XSHE', '000002.XSHE']"
                },
                "start_date": {"type": "string", "description": "开始日期，如2024-01-01"},
                "end_date": {"type": "string", "description": "结束日期，如2024-06-30"},
                "strategy": {
                    "type": "string", 
                    "description": "策略类型: momentum/value/trend/multi_factor/rotation/breakout",
                    "default": "momentum"
                },
                "use_mock": {"type": "boolean", "description": "使用模拟数据", "default": True}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.compare",
        description="对比多个策略的回测结果",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "strategies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "策略列表，不填则对比所有基础策略"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.optimize",
        description="参数网格搜索优化",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "strategy": {"type": "string", "default": "momentum"},
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如{\"mom_short\": [3,5,10], \"mom_long\": [15,20,30]}"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.generate_strategy",
        description="生成策略代码并导出为指定平台格式",
        inputSchema={
            "type": "object",
            "properties": {
                "template": {
                    "type": "string",
                    "description": "模板名称: momentum/value/trend/multi_factor/rotation/pair_trading/mean_reversion/breakout"
                },
                "params": {"type": "object", "description": "策略参数"},
                "platform": {
                    "type": "string",
                    "description": "目标平台: ptrade/qmt/joinquant",
                    "default": "ptrade"
                },
                "save": {"type": "boolean", "description": "是否保存到文件", "default": True}
            },
            "required": ["template"]
        }
    ),
    Tool(
        name="backtest.list_templates",
        description="列出所有可用的策略模板",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="backtest.data_status",
        description="检查数据源状态",
        inputSchema={"type": "object", "properties": {}}
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    
    try:
        if name == "backtest.bullettrade":
            result = await _handle_bullettrade(arguments)
        elif name == "backtest.bullettrade_batch":
            result = await _handle_bullettrade_batch(arguments)
        elif name == "backtest.bullettrade_optimize":
            result = await _handle_bullettrade_optimize(arguments)
        elif name == "backtest.qmt":
            result = await _handle_qmt(arguments)
        elif name == "backtest.qmt_batch":
            result = await _handle_qmt_batch(arguments)
        elif name == "backtest.qmt_optimize":
            result = await _handle_qmt_optimize(arguments)
        elif name == "backtest.quick":
            result = await _handle_quick_backtest(arguments)
        elif name == "backtest.compare":
            result = await _handle_compare(arguments)
        elif name == "backtest.optimize":
            result = await _handle_optimize(arguments)
        elif name == "backtest.generate_strategy":
            result = await _handle_generate_strategy(arguments)
        elif name == "backtest.list_templates":
            result = await _handle_list_templates()
        elif name == "backtest.data_status":
            result = await _handle_data_status()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
    except Exception as e:
        logger.error(f"工具调用异常: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


# ==================== 工具处理函数 ====================

async def _handle_quick_backtest(args: Dict) -> Dict:
    """快速回测"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest.fast_backtest_engine import quick_backtest
    from core.data import get_data_provider
    
    # 获取股票池
    securities = args.get("securities")
    if not securities:
        provider = get_data_provider()
        securities = provider.get_index_stocks(count=30)
    
    result = quick_backtest(
        securities=securities,
        start_date=args["start_date"],
        end_date=args["end_date"],
        strategy=args.get("strategy", "momentum"),
        use_mock=args.get("use_mock", True)
    )
    
    return {
        "success": True,
        "strategy": args.get("strategy", "momentum"),
        "period": f"{args['start_date']} ~ {args['end_date']}",
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": f"{result.sharpe_ratio:.2f}",
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%",
            "total_trades": result.total_trades
        },
        "duration": f"{result.duration_seconds:.2f}秒"
    }


async def _handle_compare(args: Dict) -> Dict:
    """策略对比"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest.strategy_comparator import StrategyComparator
    from core.data import get_data_provider
    
    securities = args.get("securities")
    if not securities:
        provider = get_data_provider()
        securities = provider.get_index_stocks(count=30)
    
    strategies = args.get("strategies", ["momentum", "value", "trend", "multi_factor"])
    
    comparator = StrategyComparator()
    df = comparator.compare_strategies(
        securities=securities,
        start_date=args["start_date"],
        end_date=args["end_date"],
        strategies=strategies,
        use_mock=True
    )
    
    best = comparator.get_best_strategy("sharpe_ratio")
    
    return {
        "success": True,
        "comparison": df.to_dict(orient="records"),
        "best_strategy": best,
        "ranking": comparator.rank_by("sharpe_ratio").to_dict(orient="records")
    }


async def _handle_optimize(args: Dict) -> Dict:
    """参数优化"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest.fast_backtest_engine import quick_backtest
    from core.data import get_data_provider
    import itertools
    
    securities = args.get("securities")
    if not securities:
        provider = get_data_provider()
        securities = provider.get_index_stocks(count=20)
    
    param_grid = args.get("param_grid", {"mom_short": [3, 5, 10], "mom_long": [15, 20, 30]})
    
    # 生成参数组合
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    combinations = list(itertools.product(*values))
    
    results = []
    for combo in combinations[:20]:  # 限制最多20组
        params = dict(zip(keys, combo))
        result = quick_backtest(
            securities=securities,
            start_date=args["start_date"],
            end_date=args["end_date"],
            strategy=args.get("strategy", "momentum"),
            use_mock=True,
            **params
        )
        results.append({
            "params": params,
            "sharpe": result.sharpe_ratio,
            "return": f"{result.total_return*100:.2f}%"
        })
    
    # 按夏普排序
    results.sort(key=lambda x: x["sharpe"], reverse=True)
    
    return {
        "success": True,
        "total_combinations": len(combinations),
        "tested": len(results),
        "best_params": results[0] if results else None,
        "top_5": results[:5]
    }


async def _handle_generate_strategy(args: Dict) -> Dict:
    """生成策略代码"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import get_any_template
    from core.templates.strategy_exporter import export_strategy, StrategyExporter
    
    template_name = args["template"]
    params = args.get("params", {})
    platform = args.get("platform", "ptrade")
    
    template = get_any_template(template_name)
    if template is None:
        return {"error": f"模板不存在: {template_name}"}
    
    # 生成代码
    code = template.generate_code(params)
    
    # 导出为目标平台
    exported = export_strategy(code, platform, f"{template_name}策略")
    
    # 保存
    filepath = None
    if args.get("save", True):
        exporter = StrategyExporter()
        filepath = exporter.save_strategy(exported, f"{template_name}_{platform}", platform)
    
    return {
        "success": True,
        "template": template_name,
        "platform": platform,
        "filepath": filepath,
        "code_preview": exported[:500] + "..." if len(exported) > 500 else exported
    }


async def _handle_list_templates() -> Dict:
    """列出模板"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import get_all_template_info
    
    return {
        "success": True,
        "templates": get_all_template_info()
    }




async def _handle_qmt(args: Dict) -> Dict:
    """QMT回测处理"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from core.qmt import QMTEngine, QMTConfig
    
    try:
        config = QMTConfig(
            start_date=args["start_date"],
            end_date=args["end_date"],
            initial_capital=args.get("initial_capital", 1000000),
            benchmark=args.get("benchmark", "000300.SH"),
            stock_pool=args.get("stock_pool", []),
            qmt_path=args.get("qmt_path", ""),
        )
        
        engine = QMTEngine(config)
        
        strategy_path = args.get("strategy_path")
        strategy_code = args.get("strategy_code")
        
        if not strategy_path and not strategy_code:
            return {"error": "必须提供 strategy_path 或 strategy_code"}
        
        result = engine.run_backtest(
            strategy_path=strategy_path,
            strategy_code=strategy_code,
        )
        
        # 保存到数据库
        if args.get("save_to_db", True) and result.success:
            try:
                from pymongo import MongoClient
                client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)
                db = client["trquant"]
                doc = result.to_mongodb_doc()
                doc["strategy_path"] = strategy_path or "code_string"
                doc["engine"] = "qmt"
                db.backtest_results.insert_one(doc)
                logger.info("QMT回测结果已保存到MongoDB")
            except Exception as e:
                logger.warning(f"保存到数据库失败: {e}")
        
        return {
            "success": result.success,
            "message": result.message,
            "metrics": result.get_metrics(),
            "report_path": result.report_path,
        }
    except Exception as e:
        logger.error(f"QMT回测失败: {e}", exc_info=True)
        return {"error": str(e)}


async def _handle_qmt_batch(args: Dict) -> Dict:
    """QMT批量回测"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from core.qmt import QMTEngine, QMTConfig
    
    try:
        config = QMTConfig(
            start_date=args["start_date"],
            end_date=args["end_date"],
            initial_capital=args.get("initial_capital", 1000000),
        )
        
        engine = QMTEngine(config)
        strategies = args["strategies"]
        results = engine.run_batch_backtest(
            strategies=strategies,
            start_date=args["start_date"],
            end_date=args["end_date"],
        )
        
        summary = []
        for i, result in enumerate(results):
            if result and result.success:
                summary.append({
                    "strategy": strategies[i].get("name", f"strategy_{i}"),
                    "total_return": f"{result.total_return:.2f}%",
                    "sharpe_ratio": f"{result.sharpe_ratio:.2f}",
                })
        
        return {"success": True, "total": len(strategies), "results": summary}
    except Exception as e:
        logger.error(f"QMT批量回测失败: {e}", exc_info=True)
        return {"error": str(e)}


async def _handle_qmt_optimize(args: Dict) -> Dict:
    """QMT参数优化"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from core.qmt import QMTEngine, QMTConfig, QMTOptimizeConfig
    
    try:
        config = QMTConfig(
            start_date=args["start_date"],
            end_date=args["end_date"],
        )
        
        optimize_config = QMTOptimizeConfig(
            param_grid=args["param_grid"],
            target_metric=args.get("target_metric", "sharpe_ratio"),
            method=args.get("method", "grid"),
        )
        
        engine = QMTEngine(config)
        result = engine.optimize(
            strategy_path=args["strategy_path"],
            optimize_config=optimize_config,
            start_date=args["start_date"],
            end_date=args["end_date"],
        )
        
        return {
            "success": True,
            "best_params": result.best_params,
            "best_metrics": result.best_result.get_metrics() if result.best_result else {},
        }
    except Exception as e:
        logger.error(f"QMT参数优化失败: {e}", exc_info=True)
        return {"error": str(e)}

async def _handle_data_status() -> Dict:
    """数据源状态"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stats = provider.get_stats()
    
    return {
        "success": True,
        "sources": stats["sources_available"],
        "stats": {
            "total_requests": stats["total_requests"],
            "cache_hits": stats["cache_hits"],
            "cache_hit_rate": f"{stats['cache_hit_rate']*100:.1f}%"
        }
    }


# ==================== 主函数 ====================

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="backtest-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
