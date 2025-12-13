#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Strategy Optimizer Server
=================================

策略优化MCP服务器，提供策略参数优化、结果对比等功能。

运行方式:
    python mcp_servers/strategy_optimizer_server.py

工具:
    - optimizer.run: 运行优化
    - optimizer.get_results: 获取优化结果
    - optimizer.compare: 对比优化方案
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
logger = logging.getLogger('StrategyOptimizerServer')

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
from mcp_servers.utils.schema import base_args_schema, merge_schema
from mcp_servers.utils.artifacts import create_artifact_if_needed

# 导入核心模块
try:
    from core.factor_weight_optimizer import FactorWeightOptimizer, get_factor_weight_optimizer
    from core.strategy_manager import StrategyVersionControl
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"核心模块不可用: {e}")
    CORE_MODULES_AVAILABLE = False

# 优化结果存储目录
OPTIMIZATION_DIR = TRQUANT_ROOT / ".taorui" / "artifacts" / "optimization"
OPTIMIZATION_DIR.mkdir(parents=True, exist_ok=True)


def save_optimization_result(optimization_id: str, result: Dict[str, Any]) -> Path:
    """保存优化结果"""
    result_file = OPTIMIZATION_DIR / f"{optimization_id}.json"
    result["optimization_id"] = optimization_id
    result["saved_at"] = datetime.now().isoformat()
    result_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    return result_file


def load_optimization_result(optimization_id: str) -> Optional[Dict[str, Any]]:
    """加载优化结果"""
    result_file = OPTIMIZATION_DIR / f"{optimization_id}.json"
    if not result_file.exists():
        return None
    try:
        return json.loads(result_file.read_text(encoding='utf-8'))
    except Exception as e:
        logger.error(f"加载优化结果失败: {e}")
        return None


def list_optimization_results(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """列出所有优化结果"""
    results = []
    for result_file in sorted(OPTIMIZATION_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(result_file.read_text(encoding='utf-8'))
            results.append({
                "optimization_id": data.get("optimization_id", result_file.stem),
                "method": data.get("method", "unknown"),
                "status": data.get("status", "unknown"),
                "created_at": data.get("created_at", data.get("saved_at", "")),
                "best_score": data.get("best_score"),
                "iterations": data.get("iterations", 0)
            })
        except Exception as e:
            logger.warning(f"读取优化结果失败 {result_file}: {e}")
            continue
    
    # 分页
    total = len(results)
    results = results[offset:offset+limit]
    
    return {
        "results": results,
        "total": total,
        "limit": limit,
        "offset": offset
    }


# 创建MCP服务器
server = Server("trquant-strategy-optimizer")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema_read = base_args_schema(mode="read")
    base_schema_dry_run = base_args_schema(mode="dry_run")
    
    return [
        Tool(
            name="optimizer.run",
            description="运行策略优化（因子权重优化或参数优化）",
            inputSchema=merge_schema(
                base_schema_dry_run,
                {
                    "type": "object",
                    "properties": {
                        "optimization_type": {
                            "type": "string",
                            "enum": ["factor_weights", "strategy_params"],
                            "description": "优化类型：factor_weights（因子权重）或strategy_params（策略参数）"
                        },
                        "factors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "因子列表（factor_weights类型需要）"
                        },
                        "strategy_id": {
                            "type": "string",
                            "description": "策略ID（strategy_params类型需要）"
                        },
                        "parameter_ranges": {
                            "type": "object",
                            "description": "参数范围（strategy_params类型需要，格式：{\"param_name\": [min, max, step]}）"
                        },
                        "method": {
                            "type": "string",
                            "enum": ["grid_search", "random_search"],
                            "default": "grid_search",
                            "description": "优化方法"
                        },
                        "target_metric": {
                            "type": "string",
                            "enum": ["sharpe_ratio", "total_return", "max_drawdown", "win_rate"],
                            "default": "sharpe_ratio",
                            "description": "优化目标指标"
                        },
                        "backtest_config": {
                            "type": "object",
                            "description": "回测配置（start_date, end_date, initial_capital等）"
                        }
                    },
                    "required": ["optimization_type"]
                }
            )
        ),
        Tool(
            name="optimizer.get_results",
            description="获取优化结果",
            inputSchema=merge_schema(
                base_schema_read,
                {
                    "type": "object",
                    "properties": {
                        "optimization_id": {
                            "type": "string",
                            "description": "优化任务ID"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 100,
                            "description": "结果数量限制（列表时使用）"
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "偏移量（列表时使用）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="optimizer.compare",
            description="对比多个优化方案",
            inputSchema=merge_schema(
                base_schema_read,
                {
                    "type": "object",
                    "properties": {
                        "optimization_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要对比的优化任务ID列表"
                        },
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "default": ["sharpe_ratio", "total_return", "max_drawdown"],
                            "description": "要对比的指标列表"
                        }
                    },
                    "required": ["optimization_ids"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具"""
    import json
    
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "optimizer.run":
            optimization_type = arguments.get("optimization_type")
            if not optimization_type:
                raise ValueError("optimization_type是必需的")
            
            method = arguments.get("method", "grid_search")
            target_metric = arguments.get("target_metric", "sharpe_ratio")
            backtest_config = arguments.get("backtest_config", {})
            
            optimization_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if mode == "dry_run":
                # 模拟优化
                result = {
                    "optimization_id": optimization_id,
                    "mode": "dry_run",
                    "optimization_type": optimization_type,
                    "method": method,
                    "target_metric": target_metric,
                    "status": "simulated",
                    "message": "这是dry_run模式，未实际执行优化",
                    "estimated_iterations": 100,
                    "estimated_time_seconds": 300
                }
            else:
                # 实际执行优化
                if not CORE_MODULES_AVAILABLE:
                    raise RuntimeError("核心模块不可用，无法执行优化")
                
                if optimization_type == "factor_weights":
                    # 因子权重优化
                    factors = arguments.get("factors", [])
                    if not factors:
                        raise ValueError("factor_weights类型需要factors参数")
                    
                    optimizer = get_factor_weight_optimizer()
                    
                    # 定义评估函数（这里需要根据实际回测结果来评估）
                    def eval_func(weights: Dict[str, float]) -> float:
                        # TODO: 这里应该调用回测接口，根据回测结果计算得分
                        # 目前返回一个模拟得分
                        logger.warning("使用模拟评估函数，实际应调用回测接口")
                        # 简单模拟：权重和越大，得分越高（实际应该基于回测结果）
                        return sum(weights.values())
                    
                    opt_result = optimizer.grid_search(
                        factor_names=factors,
                        eval_func=eval_func,
                        weight_range=(0.0, 0.5),
                        step=0.1,
                        constraint_sum=1.0
                    )
                    
                    result = {
                        "optimization_id": optimization_id,
                        "mode": "execute",
                        "optimization_type": optimization_type,
                        "method": method,
                        "target_metric": target_metric,
                        "status": "completed",
                        "best_weights": opt_result.best_weights,
                        "best_score": opt_result.best_performance,
                        "iterations": opt_result.iterations,
                        "time_cost": opt_result.time_cost,
                        "all_results": [
                            {"weights": w, "score": s} 
                            for w, s in opt_result.all_results[:10]  # 只返回前10个
                        ]
                    }
                    
                    # 保存结果
                    save_optimization_result(optimization_id, result)
                    
                elif optimization_type == "strategy_params":
                    # 策略参数优化（TODO: 需要实现）
                    raise NotImplementedError("strategy_params优化尚未实现，请使用factor_weights")
                else:
                    raise ValueError(f"未知的优化类型: {optimization_type}")
            
            result = create_artifact_if_needed(result, "optimization", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-strategy-optimizer",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "optimizer.get_results":
            optimization_id = arguments.get("optimization_id")
            
            if optimization_id:
                # 获取单个结果
                result = load_optimization_result(optimization_id)
                if not result:
                    raise FileNotFoundError(f"优化结果不存在: {optimization_id}")
                
                result = create_artifact_if_needed(result, "optimization", artifact_policy, trace_id)
            else:
                # 列出所有结果
                limit = arguments.get("limit", 100)
                offset = arguments.get("offset", 0)
                result = list_optimization_results(limit, offset)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-strategy-optimizer",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "optimizer.compare":
            optimization_ids = arguments.get("optimization_ids", [])
            if not optimization_ids:
                raise ValueError("optimization_ids是必需的")
            
            metrics = arguments.get("metrics", ["sharpe_ratio", "total_return", "max_drawdown"])
            
            # 加载所有优化结果
            results = []
            for opt_id in optimization_ids:
                result = load_optimization_result(opt_id)
                if result:
                    results.append(result)
                else:
                    logger.warning(f"优化结果不存在: {opt_id}")
            
            if not results:
                raise ValueError("没有找到有效的优化结果")
            
            # 对比分析
            comparison = {
                "optimization_ids": optimization_ids,
                "metrics": metrics,
                "results": []
            }
            
            for result in results:
                comparison["results"].append({
                    "optimization_id": result.get("optimization_id"),
                    "method": result.get("method", "unknown"),
                    "best_score": result.get("best_score"),
                    "best_weights": result.get("best_weights", {}),
                    "iterations": result.get("iterations", 0),
                    "time_cost": result.get("time_cost", 0),
                    "created_at": result.get("created_at", result.get("saved_at", ""))
                })
            
            # 找出最佳结果
            if results:
                best_result = max(results, key=lambda r: r.get("best_score", float("-inf")))
                comparison["best"] = {
                    "optimization_id": best_result.get("optimization_id"),
                    "score": best_result.get("best_score")
                }
            
            comparison = create_artifact_if_needed(comparison, "optimization", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=comparison,
                server_name="trquant-strategy-optimizer",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        else:
            raise ValueError(f"未知工具: {name}")
    
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-strategy-optimizer",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except FileNotFoundError as e:
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=str(e),
            server_name="trquant-strategy-optimizer",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查优化任务ID是否正确",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except NotImplementedError as e:
        envelope = wrap_error_response(
            error_code="NOT_IMPLEMENTED",
            error_message=str(e),
            server_name="trquant-strategy-optimizer",
            tool_name=name,
            version="1.0.0",
            error_hint="该功能尚未实现",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-strategy-optimizer",
            tool_name=name,
            version="1.0.0",
            error_details={"exception_type": type(e).__name__},
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


if __name__ == "__main__":
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())










