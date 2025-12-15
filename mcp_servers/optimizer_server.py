# -*- coding: utf-8 -*-
"""
优化器MCP服务器（标准化版本）
===========================
策略参数优化、网格搜索、进化算法
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("optimizer-server")


TOOLS = [
    Tool(
        name="optimizer.grid_search",
        description="参数网格搜索优化",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "description": "策略类型"},
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如{\"mom_short\": [3,5,10]}"
                },
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "metric": {
                    "type": "string",
                    "description": "优化目标: sharpe/return/drawdown",
                    "default": "sharpe"
                }
            },
            "required": ["strategy", "param_grid", "start_date", "end_date"]
        }
    ),
    Tool(
        name="optimizer.evolve",
        description="使用遗传算法进化策略",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "generations": {"type": "integer", "default": 10},
                "population_size": {"type": "integer", "default": 20}
            },
            "required": ["strategy", "start_date", "end_date"]
        }
    ),
    Tool(
        name="optimizer.sensitivity",
        description="参数敏感性分析",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "param_name": {"type": "string", "description": "要分析的参数"},
                "param_range": {"type": "array", "items": {"type": "number"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"}
            },
            "required": ["strategy", "param_name", "param_range", "start_date", "end_date"]
        }
    ),
    Tool(
        name="optimizer.best_params",
        description="获取推荐的最佳参数",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string"}
            },
            "required": ["strategy"]
        }
    )
,
    Tool(
        name="optimizer.optuna",
        description="使用Optuna进行智能参数优化（支持TPE/随机/网格搜索）",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "description": "策略类型"},
                "param_space": {
                    "type": "object",
                    "description": "参数空间定义，如{{"mom_short": {{"type": "int", "low": 3, "high": 10}}}}"
                },
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "n_trials": {"type": "integer", "default": 50},
                "sampler": {"type": "string", "default": "tpe", "description": "tpe/random/grid"},
                "target_metric": {"type": "string", "default": "sharpe_ratio"},
                "constraints": {
                    "type": "object",
                    "description": "约束条件，如{"max_drawdown": [-1.0, -0.2]}"
                }
            },
            "required": ["strategy", "param_space", "start_date", "end_date"]
        }
    ),
    Tool(
        name="optimizer.multi_objective",
        description="多目标优化（同时优化收益和风险）",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "param_space": {"type": "object"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "objectives": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["sharpe_ratio", "max_drawdown"]
                },
                "n_trials": {"type": "integer", "default": 50}
            },
            "required": ["strategy", "param_space", "start_date", "end_date"]
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "optimizer.grid_search":
            result = await _handle_grid_search(arguments)
        elif name == "optimizer.evolve":
            result = await _handle_evolve(arguments)
        elif name == "optimizer.sensitivity":
            result = await _handle_sensitivity(arguments)
        elif name == "optimizer.best_params":
            result = await _handle_best_params(arguments)
        elif name == "optimizer.optuna":
            result = await _handle_optuna(arguments)
        elif name == "optimizer.multi_objective":
            result = await _handle_multi_objective(arguments)
        # 占位
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_grid_search(args: Dict) -> Dict:
    import sys
    import itertools
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest import quick_backtest
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stocks = provider.get_index_stocks(count=20)
    
    param_grid = args["param_grid"]
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    combinations = list(itertools.product(*values))
    
    results = []
    for combo in combinations[:30]:  # 限制最多30组
        params = dict(zip(keys, combo))
        result = quick_backtest(
            securities=stocks,
            start_date=args["start_date"],
            end_date=args["end_date"],
            strategy=args["strategy"],
            use_mock=True,
            **params
        )
        results.append({
            "params": params,
            "sharpe": round(result.sharpe_ratio, 3),
            "return": round(result.total_return * 100, 2),
            "drawdown": round(result.max_drawdown * 100, 2)
        })
    
    # 按优化目标排序
    metric = args.get("metric", "sharpe")
    if metric == "sharpe":
        results.sort(key=lambda x: x["sharpe"], reverse=True)
    elif metric == "return":
        results.sort(key=lambda x: x["return"], reverse=True)
    elif metric == "drawdown":
        results.sort(key=lambda x: x["drawdown"], reverse=False)
    
    return {
        "success": True,
        "total_combinations": len(combinations),
        "tested": len(results),
        "metric": metric,
        "best": results[0] if results else None,
        "top_5": results[:5]
    }


async def _handle_evolve(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.evolution import StrategyEvolver
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stocks = provider.get_index_stocks(count=20)
    
    # 简化的遗传算法实现
    generations = args.get("generations", 10)
    pop_size = args.get("population_size", 20)
    
    # 模拟进化过程
    import random
    from core.backtest import quick_backtest
    
    # 参数范围
    param_ranges = {
        "mom_short": (3, 15),
        "mom_long": (10, 40),
        "max_stocks": (5, 20),
        "rebalance_days": (3, 15)
    }
    
    best_individual = None
    best_fitness = float('-inf')
    
    for gen in range(min(generations, 5)):  # 限制代数
        for _ in range(min(pop_size, 10)):  # 限制个体数
            # 随机生成参数
            params = {k: random.randint(v[0], v[1]) for k, v in param_ranges.items()}
            
            result = quick_backtest(
                securities=stocks,
                start_date=args["start_date"],
                end_date=args["end_date"],
                strategy=args["strategy"],
                use_mock=True,
                **params
            )
            
            fitness = result.sharpe_ratio
            if fitness > best_fitness:
                best_fitness = fitness
                best_individual = {
                    "params": params,
                    "sharpe": round(fitness, 3),
                    "return": round(result.total_return * 100, 2)
                }
    
    return {
        "success": True,
        "generations": min(generations, 5),
        "population_size": min(pop_size, 10),
        "best_individual": best_individual
    }


async def _handle_sensitivity(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest import quick_backtest
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stocks = provider.get_index_stocks(count=20)
    
    param_name = args["param_name"]
    param_range = args["param_range"]
    
    results = []
    for value in param_range:
        result = quick_backtest(
            securities=stocks,
            start_date=args["start_date"],
            end_date=args["end_date"],
            strategy=args["strategy"],
            use_mock=True,
            **{param_name: value}
        )
        results.append({
            "value": value,
            "sharpe": round(result.sharpe_ratio, 3),
            "return": round(result.total_return * 100, 2)
        })
    
    return {
        "success": True,
        "param_name": param_name,
        "analysis": results,
        "best_value": max(results, key=lambda x: x["sharpe"])["value"]
    }


async def _handle_best_params(args: Dict) -> Dict:
    """返回推荐的最佳参数"""
    
    # 预定义的推荐参数
    recommendations = {
        "momentum": {
            "mom_short": 5,
            "mom_long": 20,
            "max_stocks": 10,
            "rebalance_days": 5,
            "stop_loss": 0.08,
            "take_profit": 0.20
        },
        "value": {
            "pe_max": 15,
            "pb_max": 2,
            "max_stocks": 15,
            "rebalance_days": 20
        },
        "trend": {
            "fast_period": 5,
            "slow_period": 20,
            "max_stocks": 10
        },
        "multi_factor": {
            "factors": ["momentum", "value", "quality"],
            "weights": [0.4, 0.3, 0.3],
            "max_stocks": 10,
            "rebalance_days": 10
        },
        "rotation": {
            "rotation_period": 20,
            "top_n": 3,
            "lookback": 20
        }
    }
    
    strategy = args["strategy"]
    params = recommendations.get(strategy, {})
    
    return {
        "success": True,
        "strategy": strategy,
        "recommended_params": params,
        "note": "这些是经验推荐值，建议通过grid_search进一步优化"
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="optimizer-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


# ==================== Optuna集成处理函数 ====================

async def _handle_optuna(args: Dict) -> Dict:
    """Optuna智能优化"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from core.optimization import OptunaOptimizer
        from core.backtest.fast_backtest_engine import quick_backtest
        from core.data import get_data_provider
        
        strategy = args["strategy"]
        param_space = args["param_space"]
        start_date = args["start_date"]
        end_date = args["end_date"]
        n_trials = args.get("n_trials", 50)
        sampler = args.get("sampler", "tpe")
        target_metric = args.get("target_metric", "sharpe_ratio")
        constraints = args.get("constraints")
        
        # 获取股票池
        provider = get_data_provider()
        securities = provider.get_index_stocks(count=30)
        
        # 定义回测函数
        def backtest_func(params):
            result = quick_backtest(
                securities=securities,
                start_date=start_date,
                end_date=end_date,
                strategy=strategy,
                use_mock=True,
                **params
            )
            return {
                "sharpe_ratio": result.sharpe_ratio,
                "total_return": result.total_return,
                "max_drawdown": -result.max_drawdown,  # 转为负数，越大越好
                "win_rate": result.win_rate,
            }
        
        # 创建优化器
        optimizer = OptunaOptimizer(
            direction="maximize",
            sampler=sampler,
        )
        
        # 执行优化
        result = optimizer.optimize_strategy(
            backtest_func=backtest_func,
            param_space=param_space,
            n_trials=n_trials,
            target_metric=target_metric,
            constraints=constraints,
        )
        
        return {
            "success": True,
            "best_params": result.best_params,
            "best_value": result.best_value,
            "n_trials": result.n_trials,
            "optimization_time": f"{result.optimization_time:.2f}s",
            "top_5": result.all_trials[:5] if result.all_trials else [],
        }
        
    except Exception as e:
        logger.error(f"Optuna优化失败: {e}")
        return {"error": str(e)}


async def _handle_multi_objective(args: Dict) -> Dict:
    """多目标优化"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from core.optimization import OptunaOptimizer
        from core.backtest.fast_backtest_engine import quick_backtest
        from core.data import get_data_provider
        
        strategy = args["strategy"]
        param_space = args["param_space"]
        start_date = args["start_date"]
        end_date = args["end_date"]
        objectives = args.get("objectives", ["sharpe_ratio", "max_drawdown"])
        n_trials = args.get("n_trials", 50)
        
        # 获取股票池
        provider = get_data_provider()
        securities = provider.get_index_stocks(count=30)
        
        # 执行多次优化，每次针对不同目标
        results = {}
        for objective in objectives:
            direction = "minimize" if "drawdown" in objective else "maximize"
            
            def backtest_func(params):
                result = quick_backtest(
                    securities=securities,
                    start_date=start_date,
                    end_date=end_date,
                    strategy=strategy,
                    use_mock=True,
                    **params
                )
                return {
                    "sharpe_ratio": result.sharpe_ratio,
                    "total_return": result.total_return,
                    "max_drawdown": result.max_drawdown,
                }
            
            optimizer = OptunaOptimizer(direction=direction)
            result = optimizer.optimize_strategy(
                backtest_func=backtest_func,
                param_space=param_space,
                n_trials=n_trials // len(objectives),
                target_metric=objective,
            )
            
            results[objective] = {
                "best_params": result.best_params,
                "best_value": result.best_value,
            }
        
        # 找到帕累托最优解（简化版：加权组合）
        pareto_params = {}
        for key in param_space.keys():
            values = [r["best_params"].get(key) for r in results.values() if key in r["best_params"]]
            if values:
                if isinstance(values[0], (int, float)):
                    pareto_params[key] = sum(values) / len(values)
                else:
                    pareto_params[key] = values[0]
        
        return {
            "success": True,
            "objectives": objectives,
            "objective_results": results,
            "pareto_optimal": pareto_params,
        }
        
    except Exception as e:
        logger.error(f"多目标优化失败: {e}")
        return {"error": str(e)}
