# -*- coding: utf-8 -*-
"""
策略MCP服务器
=============
策略模板管理、策略生成、策略优化、平台转换

功能：
1. 策略模板列表
2. 策略生成（多平台）
3. 策略参数优化
4. 策略代码验证
5. 平台转换
"""

import logging
import json
from typing import Dict, List, Any
import sys
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入官方MCP SDK
try:
    from mcp.server.models import InitializationOptions
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    import sys
    print(f'官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}', file=sys.stderr)
    sys.exit(1)

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("strategy-server")


TOOLS = [
    # 策略模板
    Tool(
        name="strategy_template.list",
        description="列出所有可用的策略模板",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "过滤分类: momentum/value/trend/mean_reversion/rotation",
                }
            }
        }
    ),
    Tool(
        name="strategy_template.info",
        description="获取策略模板详情",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "策略名称"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="strategy_template.generate",
        description="生成策略代码",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_type": {
                    "type": "string",
                    "description": "策略类型: momentum/mean_reversion/rotation"
                },
                "params": {
                    "type": "object",
                    "description": "策略参数"
                },
                "platform": {
                    "type": "string",
                    "description": "目标平台: joinquant/bullettrade/ptrade/qmt",
                    "default": "joinquant"
                }
            },
            "required": ["strategy_type"]
        }
    ),
    # 策略验证
    Tool(
        name="strategy.validate",
        description="验证策略代码",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "策略代码"},
                "platform": {"type": "string", "default": "joinquant"}
            },
            "required": ["code"]
        }
    ),
    # 平台转换
    Tool(
        name="strategy.convert",
        description="转换策略代码到其他平台",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "策略代码"},
                "from_platform": {"type": "string", "default": "joinquant"},
                "to_platform": {"type": "string", "description": "目标平台"},
                "strategy_name": {"type": "string", "default": "strategy"}
            },
            "required": ["code", "to_platform"]
        }
    ),
    # 策略优化
    Tool(
        name="strategy.optimize",
        description="优化策略参数",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_type": {"type": "string"},
                "param_ranges": {
                    "type": "object",
                    "description": "参数范围，如 {\"max_stocks\": [5, 10, 15]}"
                },
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "target_metric": {
                    "type": "string",
                    "description": "优化目标: sharpe_ratio/total_return/max_drawdown",
                    "default": "sharpe_ratio"
                },
                "n_trials": {"type": "integer", "default": 10}
            },
            "required": ["strategy_type", "param_ranges", "start_date", "end_date"]
        }
    ),
    # 策略保存
    Tool(
        name="strategy.save",
        description="保存策略到文件",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string"},
                "filename": {"type": "string"},
                "platform": {"type": "string", "default": "joinquant"}
            },
            "required": ["code", "filename"]
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
        
        if name == "strategy_template.list":
            result = await _handle_list(arguments)
        elif name == "strategy_template.info":
            result = await _handle_info(arguments)
        elif name == "strategy_template.generate":
            result = await _handle_generate(arguments)
        elif name == "strategy.validate":
            result = await _handle_validate(arguments)
        elif name == "strategy.convert":
            result = await _handle_convert(arguments)
        elif name == "strategy.optimize":
            result = await _handle_optimize(arguments)
        elif name == "strategy.save":
            result = await _handle_save(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.exception(f"工具执行错误: {name}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_list(args: Dict) -> Dict:
    """列出策略模板"""
    from core.templates import list_strategies
    
    strategies = list_strategies()
    
    # 过滤分类
    category = args.get("category")
    if category:
        strategies = [s for s in strategies if s["category"] == category]
    
    return {
        "success": True,
        "count": len(strategies),
        "strategies": strategies
    }


async def _handle_info(args: Dict) -> Dict:
    """获取策略详情"""
    from core.templates import StrategyFactory
    
    name = args["name"]
    
    try:
        template = StrategyFactory.get_template(name)
        return {
            "success": True,
            "name": name,
            "display_name": template.name,
            "description": template.description,
            "category": template.category.value,
            "risk_level": template.risk_level,
            "suitable_market": template.suitable_market,
            "params": [
                {
                    "name": s.name,
                    "type": s.type.__name__,
                    "default": s.default,
                    "min": s.min_val,
                    "max": s.max_val,
                    "description": s.description
                }
                for s in template.get_param_specs()
            ],
            "documentation": template.get_doc()
        }
    except ValueError as e:
        return {"success": False, "error": str(e)}


async def _handle_generate(args: Dict) -> Dict:
    """生成策略代码"""
    from core.templates import create_strategy
    
    strategy_type = args["strategy_type"]
    params = args.get("params", {})
    platform = args.get("platform", "joinquant")
    
    try:
        code = create_strategy(strategy_type, params, platform)
        return {
            "success": True,
            "strategy_type": strategy_type,
            "platform": platform,
            "params": params,
            "code": code,
            "code_lines": len(code.split("\n"))
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def _handle_validate(args: Dict) -> Dict:
    """验证策略代码"""
    code = args["code"]
    platform = args.get("platform", "joinquant")
    
    result = {
        "success": True,
        "valid": True,
        "errors": [],
        "warnings": [],
        "info": {}
    }
    
    # 语法检查
    try:
        compile(code, "<strategy>", "exec")
    except SyntaxError as e:
        result["valid"] = False
        result["errors"].append(f"语法错误 (行{e.lineno}): {e.msg}")
        return result
    
    # 检查必要函数
    required_funcs = {
        "joinquant": ["initialize", "handle_data"],
        "bullettrade": ["initialize", "handle_data"],
        "ptrade": ["initialize"],
        "qmt": ["init"],
    }
    
    for func in required_funcs.get(platform, []):
        if f"def {func}" not in code:
            result["warnings"].append(f"缺少函数: {func}")
    
    # 检查风控函数
    if "stop_loss" not in code.lower():
        result["warnings"].append("建议: 添加止损逻辑")
    if "take_profit" not in code.lower():
        result["warnings"].append("建议: 添加止盈逻辑")
    
    # 代码信息
    result["info"] = {
        "lines": len(code.split("\n")),
        "has_stop_loss": "stop_loss" in code.lower(),
        "has_take_profit": "take_profit" in code.lower(),
        "has_benchmark": "set_benchmark" in code,
    }
    
    return result


async def _handle_convert(args: Dict) -> Dict:
    """转换策略代码"""
    from core.templates import export_strategy
    
    code = args["code"]
    to_platform = args["to_platform"]
    strategy_name = args.get("strategy_name", "strategy")
    
    try:
        converted = export_strategy(code, to_platform, strategy_name)
        return {
            "success": True,
            "from_platform": args.get("from_platform", "joinquant"),
            "to_platform": to_platform,
            "code": converted,
            "code_lines": len(converted.split("\n"))
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def _handle_optimize(args: Dict) -> Dict:
    """优化策略参数"""
    from core.templates import create_strategy
    from core.backtest import UnifiedBacktestManager, UnifiedBacktestConfig, MomentumStrategy, MeanReversionStrategy
    import itertools
    
    strategy_type = args["strategy_type"]
    param_ranges = args["param_ranges"]
    securities = args.get("securities", ["000001.XSHE", "600000.XSHG"])
    start_date = args["start_date"]
    end_date = args["end_date"]
    target_metric = args.get("target_metric", "sharpe_ratio")
    n_trials = args.get("n_trials", 10)
    
    # 生成参数组合
    param_names = list(param_ranges.keys())
    param_values = list(param_ranges.values())
    all_combinations = list(itertools.product(*param_values))[:n_trials]
    
    results = []
    best_result = None
    best_metric = float("-inf") if target_metric != "max_drawdown" else float("inf")
    
    config = UnifiedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        securities=securities,
        use_mock=True
    )
    
    manager = UnifiedBacktestManager(config)
    
    for combo in all_combinations:
        params = dict(zip(param_names, combo))
        
        # 创建策略
        if strategy_type == "momentum":
            strategy = MomentumStrategy(params)
        elif strategy_type == "mean_reversion":
            strategy = MeanReversionStrategy(params)
        else:
            continue
        
        # 运行回测
        bt_result = manager.run_fast(strategy)
        
        if bt_result.success:
            metric_value = getattr(bt_result, target_metric, 0)
            
            trial_result = {
                "params": params,
                "total_return": round(bt_result.total_return * 100, 2),
                "sharpe_ratio": round(bt_result.sharpe_ratio, 2),
                "max_drawdown": round(bt_result.max_drawdown * 100, 2),
                target_metric: round(metric_value, 4) if target_metric not in ["total_return", "max_drawdown"] else round(metric_value * 100, 2)
            }
            results.append(trial_result)
            
            # 更新最佳
            is_better = (
                (target_metric != "max_drawdown" and metric_value > best_metric) or
                (target_metric == "max_drawdown" and metric_value > best_metric)  # 回撤越小越好，但存储为负数
            )
            
            if is_better:
                best_metric = metric_value
                best_result = trial_result
    
    # 按目标指标排序
    results.sort(key=lambda x: x[target_metric], reverse=(target_metric != "max_drawdown"))
    
    return {
        "success": True,
        "strategy_type": strategy_type,
        "target_metric": target_metric,
        "trials": len(results),
        "best_params": best_result["params"] if best_result else None,
        "best_metric": best_result[target_metric] if best_result else None,
        "results": results[:10],  # 返回前10个结果
    }


async def _handle_save(args: Dict) -> Dict:
    """保存策略"""
    from pathlib import Path
    
    code = args["code"]
    filename = args["filename"]
    platform = args.get("platform", "joinquant")
    
    # 保存路径
    base_dir = Path(__file__).parent.parent / "strategies" / platform
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 确保文件名以 .py 结尾
    if not filename.endswith(".py"):
        filename += ".py"
    
    filepath = base_dir / filename
    filepath.write_text(code, encoding="utf-8")
    
    return {
        "success": True,
        "path": str(filepath),
        "platform": platform,
        "filename": filename
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
