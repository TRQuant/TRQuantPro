#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 核心量化MCP服务器 (整合版)
==================================

整合了以下服务器的核心功能:
- data_source_server_v2.py  → data.*
- market_server_v2.py       → market.*
- factor_server.py          → factor.*
- strategy_server.py        → strategy.*
- backtest_server.py        → backtest.*
- optimizer_server.py       → optimizer.*

目标: 减少服务器数量，统一接口，提高性能

运行方式:
    python mcp_servers/trquant_core_server.py
"""

import sys
import json
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from functools import lru_cache
import time

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))
sys.path.insert(0, str(TRQUANT_ROOT / "mcp_servers"))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('TRQuantCoreServer')

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    logger.info("MCP SDK 加载成功")
except ImportError as e:
    logger.error(f"MCP SDK不可用: {e}")
    sys.exit(1)

# 创建服务器
server = Server("trquant-core")

# ============================================================
# 性能监控装饰器
# ============================================================

_tool_metrics = {}

def track_performance(func):
    """跟踪工具调用性能"""
    async def wrapper(name: str, arguments: Dict[str, Any]):
        start = time.time()
        try:
            result = await func(name, arguments)
            duration = (time.time() - start) * 1000
            _tool_metrics[name] = {
                "last_duration_ms": duration,
                "last_call": datetime.now().isoformat(),
                "success": True
            }
            logger.info(f"[PERF] {name} 耗时 {duration:.1f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start) * 1000
            _tool_metrics[name] = {
                "last_duration_ms": duration,
                "last_call": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }
            raise
    return wrapper


# ============================================================
# 统一返回格式
# ============================================================

def success_response(data: Any, tool: str = "") -> Dict:
    """统一成功响应格式"""
    return {
        "success": True,
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "tool": tool
    }

def error_response(error: str, error_code: str = "UNKNOWN", tool: str = "") -> Dict:
    """统一错误响应格式"""
    return {
        "success": False,
        "error": error,
        "error_code": error_code,
        "timestamp": datetime.now().isoformat(),
        "tool": tool
    }


# ============================================================
# 工具定义 - 按领域组织
# ============================================================

TOOLS = [
    # ==================== DATA 数据源 ====================
    Tool(
        name="data.get_price",
        description="获取股票历史价格数据",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}, "description": "股票代码列表"},
                "start_date": {"type": "string", "description": "开始日期 YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "结束日期 YYYY-MM-DD"},
                "fields": {"type": "array", "items": {"type": "string"}, "default": ["open", "high", "low", "close", "volume"]}
            },
            "required": ["securities", "start_date", "end_date"]
        }
    ),
    Tool(
        name="data.get_index_stocks",
        description="获取指数成分股",
        inputSchema={
            "type": "object",
            "properties": {
                "index_code": {"type": "string", "description": "指数代码", "default": "000300.XSHG"},
                "date": {"type": "string", "description": "日期(可选)"}
            }
        }
    ),
    Tool(
        name="data.health_check",
        description="检查数据源健康状态",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="data.candidate_pool",
        description="根据主线构建候选股票池",
        inputSchema={
            "type": "object",
            "properties": {
                "mainline": {"type": "string", "description": "投资主线", "default": "人工智能"},
                "limit": {"type": "integer", "description": "返回数量", "default": 20}
            }
        }
    ),
    
    # ==================== MARKET 市场分析 ====================
    Tool(
        name="market.status",
        description="获取市场状态(regime/趋势/情绪)",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "指数代码", "default": "000300.XSHG"}
            }
        }
    ),
    Tool(
        name="market.trend",
        description="分析市场趋势(短/中/长期)",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "default": "000300.XSHG"},
                "period": {"type": "string", "enum": ["short", "medium", "long"], "default": "medium"}
            }
        }
    ),
    Tool(
        name="market.mainlines",
        description="获取当前投资主线",
        inputSchema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer", "default": 10},
                "time_horizon": {"type": "string", "enum": ["short", "medium", "long"], "default": "short"}
            }
        }
    ),
    Tool(
        name="market.five_dimension_score",
        description="五维评分法分析主线",
        inputSchema={
            "type": "object",
            "properties": {
                "mainline": {"type": "string", "description": "主线名称"}
            },
            "required": ["mainline"]
        }
    ),
    Tool(
        name="market.comprehensive",
        description="综合市场分析(趋势+主线+资金+情绪)",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    # ==================== FACTOR 因子 ====================
    Tool(
        name="factor.recommend",
        description="根据市场状态推荐因子",
        inputSchema={
            "type": "object",
            "properties": {
                "market_regime": {"type": "string", "enum": ["risk_on", "risk_off", "neutral"]},
                "top_n": {"type": "integer", "default": 10}
            }
        }
    ),
    Tool(
        name="factor.calculate",
        description="计算指定因子值",
        inputSchema={
            "type": "object",
            "properties": {
                "factor_name": {"type": "string", "description": "因子名称"},
                "securities": {"type": "array", "items": {"type": "string"}},
                "date": {"type": "string"}
            },
            "required": ["factor_name", "securities"]
        }
    ),
    Tool(
        name="factor.list",
        description="列出可用因子",
        inputSchema={"type": "object", "properties": {}}
    ),
    
    # ==================== STRATEGY 策略 ====================
    Tool(
        name="strategy.generate",
        description="生成策略代码",
        inputSchema={
            "type": "object",
            "properties": {
                "template": {"type": "string", "description": "模板名称", "default": "momentum"},
                "factors": {"type": "array", "items": {"type": "string"}},
                "platform": {"type": "string", "enum": ["ptrade", "qmt", "joinquant"], "default": "ptrade"}
            }
        }
    ),
    Tool(
        name="strategy.list_templates",
        description="列出可用策略模板",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="strategy.validate",
        description="验证策略代码",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "策略代码"}
            },
            "required": ["code"]
        }
    ),
    
    # ==================== BACKTEST 回测 ====================
    Tool(
        name="backtest.run",
        description="执行回测",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
                "strategy": {"type": "string", "default": "momentum"},
                "initial_capital": {"type": "number", "default": 1000000},
                "max_positions": {"type": "integer", "default": 10}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.quick",
        description="快速向量化回测",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"}
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="backtest.compare",
        description="比较多个回测结果",
        inputSchema={
            "type": "object",
            "properties": {
                "backtest_ids": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["backtest_ids"]
        }
    ),
    
    # ==================== OPTIMIZER 优化 ====================
    Tool(
        name="optimizer.grid_search",
        description="网格搜索参数优化",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_code": {"type": "string"},
                "param_grid": {"type": "object", "description": "参数网格"},
                "metric": {"type": "string", "default": "sharpe_ratio"}
            },
            "required": ["strategy_code", "param_grid"]
        }
    ),
    Tool(
        name="optimizer.optuna",
        description="Optuna贝叶斯优化",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_code": {"type": "string"},
                "param_space": {"type": "object"},
                "n_trials": {"type": "integer", "default": 100}
            },
            "required": ["strategy_code", "param_space"]
        }
    ),
    Tool(
        name="optimizer.best_params",
        description="获取最佳参数",
        inputSchema={
            "type": "object",
            "properties": {
                "optimization_id": {"type": "string"}
            },
            "required": ["optimization_id"]
        }
    ),
    
    # ==================== META 元数据 ====================
    Tool(
        name="core.metrics",
        description="获取服务器性能指标",
        inputSchema={"type": "object", "properties": {}}
    ),
]


# ============================================================
# 工具处理器 - 按领域组织
# ============================================================

class DataHandler:
    """数据源处理器"""
    
    @staticmethod
    async def get_price(args: Dict) -> Dict:
        try:
            from data_source_server_v2 import _handle_get_price
            result = await _handle_get_price(args)
            return success_response(result, "data.get_price")
        except Exception as e:
            logger.error(f"get_price失败: {e}")
            return error_response(str(e), "DATA_ERROR", "data.get_price")
    
    @staticmethod
    async def get_index_stocks(args: Dict) -> Dict:
        try:
            from data_source_server_v2 import _handle_get_index_stocks
            result = await _handle_get_index_stocks(args)
            return success_response(result, "data.get_index_stocks")
        except Exception as e:
            return error_response(str(e), "DATA_ERROR", "data.get_index_stocks")
    
    @staticmethod
    async def health_check(args: Dict) -> Dict:
        try:
            from data_source_server_v2 import _handle_health_check
            result = await _handle_health_check(args)
            return success_response(result, "data.health_check")
        except Exception as e:
            return error_response(str(e), "DATA_ERROR", "data.health_check")
    
    @staticmethod
    async def candidate_pool(args: Dict) -> Dict:
        try:
            from data_source_server_v2 import _handle_candidate_pool
            result = await _handle_candidate_pool(args)
            return success_response(result, "data.candidate_pool")
        except Exception as e:
            return error_response(str(e), "DATA_ERROR", "data.candidate_pool")


class MarketHandler:
    """市场分析处理器"""
    
    @staticmethod
    async def status(args: Dict) -> Dict:
        try:
            from market_server_v2 import _handle_status
            result = await _handle_status(args)
            return success_response(result, "market.status")
        except Exception as e:
            return error_response(str(e), "MARKET_ERROR", "market.status")
    
    @staticmethod
    async def trend(args: Dict) -> Dict:
        try:
            from market_server_v2 import _handle_trend
            result = await _handle_trend(args)
            return success_response(result, "market.trend")
        except Exception as e:
            return error_response(str(e), "MARKET_ERROR", "market.trend")
    
    @staticmethod
    async def mainlines(args: Dict) -> Dict:
        try:
            from market_server_v2 import _handle_mainlines
            result = await _handle_mainlines(args)
            return success_response(result, "market.mainlines")
        except Exception as e:
            return error_response(str(e), "MARKET_ERROR", "market.mainlines")
    
    @staticmethod
    async def five_dimension_score(args: Dict) -> Dict:
        try:
            from market_server_v2 import _handle_five_dimension_score
            result = await _handle_five_dimension_score(args)
            return success_response(result, "market.five_dimension_score")
        except Exception as e:
            return error_response(str(e), "MARKET_ERROR", "market.five_dimension_score")
    
    @staticmethod
    async def comprehensive(args: Dict) -> Dict:
        try:
            from market_server_v2 import _handle_comprehensive
            result = await _handle_comprehensive(args)
            return success_response(result, "market.comprehensive")
        except Exception as e:
            return error_response(str(e), "MARKET_ERROR", "market.comprehensive")


class FactorHandler:
    """因子处理器"""
    
    @staticmethod
    async def recommend(args: Dict) -> Dict:
        """推荐因子"""
        market_regime = args.get("market_regime", "neutral")
        top_n = args.get("top_n", 10)
        
        # 根据市场状态推荐不同因子
        factor_recommendations = {
            "risk_on": [
                {"name": "momentum_20d", "category": "momentum", "weight": 0.25, "reason": "牛市动量效应强"},
                {"name": "volume_ratio", "category": "technical", "weight": 0.20, "reason": "成交量放大"},
                {"name": "revenue_growth", "category": "fundamental", "weight": 0.15, "reason": "关注成长"},
                {"name": "beta", "category": "risk", "weight": 0.15, "reason": "高贝塔表现好"},
                {"name": "rsi_14d", "category": "technical", "weight": 0.10, "reason": "超买区间仍有动力"},
            ],
            "risk_off": [
                {"name": "dividend_yield", "category": "value", "weight": 0.25, "reason": "防御性因子"},
                {"name": "low_volatility", "category": "risk", "weight": 0.20, "reason": "低波动保护"},
                {"name": "pb_ratio", "category": "value", "weight": 0.15, "reason": "价值因子"},
                {"name": "roe", "category": "quality", "weight": 0.15, "reason": "盈利质量"},
                {"name": "debt_ratio", "category": "quality", "weight": 0.10, "reason": "低负债安全"},
            ],
            "neutral": [
                {"name": "multi_factor", "category": "composite", "weight": 0.20, "reason": "均衡配置"},
                {"name": "momentum_20d", "category": "momentum", "weight": 0.15, "reason": "趋势跟踪"},
                {"name": "pe_ratio", "category": "value", "weight": 0.15, "reason": "估值参考"},
                {"name": "quality_score", "category": "quality", "weight": 0.15, "reason": "质量筛选"},
                {"name": "size", "category": "style", "weight": 0.10, "reason": "市值因子"},
            ]
        }
        
        factors = factor_recommendations.get(market_regime, factor_recommendations["neutral"])[:top_n]
        
        return success_response({
            "market_regime": market_regime,
            "factors": factors,
            "total": len(factors)
        }, "factor.recommend")
    
    @staticmethod
    async def calculate(args: Dict) -> Dict:
        """计算因子值(简化版)"""
        factor_name = args.get("factor_name", "momentum_20d")
        securities = args.get("securities", [])
        
        # 模拟因子计算结果
        results = []
        for sec in securities[:10]:
            import random
            results.append({
                "security": sec,
                "factor": factor_name,
                "value": round(random.uniform(-2, 2), 4),
                "rank": random.randint(1, 100)
            })
        
        return success_response({
            "factor": factor_name,
            "results": results
        }, "factor.calculate")
    
    @staticmethod
    async def list_factors(args: Dict) -> Dict:
        """列出可用因子"""
        factors = [
            {"name": "momentum_20d", "category": "momentum", "description": "20日动量"},
            {"name": "momentum_60d", "category": "momentum", "description": "60日动量"},
            {"name": "pe_ratio", "category": "value", "description": "市盈率"},
            {"name": "pb_ratio", "category": "value", "description": "市净率"},
            {"name": "dividend_yield", "category": "value", "description": "股息率"},
            {"name": "roe", "category": "quality", "description": "净资产收益率"},
            {"name": "revenue_growth", "category": "growth", "description": "营收增长率"},
            {"name": "volatility", "category": "risk", "description": "波动率"},
            {"name": "beta", "category": "risk", "description": "贝塔系数"},
            {"name": "turnover", "category": "liquidity", "description": "换手率"},
        ]
        return success_response({"factors": factors, "total": len(factors)}, "factor.list")


class StrategyHandler:
    """策略处理器"""
    
    @staticmethod
    async def generate(args: Dict) -> Dict:
        """生成策略代码"""
        template = args.get("template", "momentum")
        factors = args.get("factors", ["momentum_20d"])
        platform = args.get("platform", "ptrade")
        
        # 生成简化的策略代码
        code = f'''# -*- coding: utf-8 -*-
"""
自动生成的{template}策略
平台: {platform}
因子: {", ".join(factors)}
生成时间: {datetime.now().isoformat()}
"""

def initialize(context):
    """初始化"""
    context.factors = {factors}
    context.max_positions = 10
    context.rebalance_days = 5

def handle_data(context, data):
    """每日执行"""
    # 因子计算和选股逻辑
    pass
'''
        return success_response({
            "template": template,
            "platform": platform,
            "code": code,
            "factors": factors
        }, "strategy.generate")
    
    @staticmethod
    async def list_templates(args: Dict) -> Dict:
        """列出策略模板"""
        templates = [
            {"name": "momentum", "description": "动量策略", "factors": ["momentum_20d", "volume_ratio"]},
            {"name": "value", "description": "价值策略", "factors": ["pe_ratio", "pb_ratio", "dividend_yield"]},
            {"name": "quality", "description": "质量策略", "factors": ["roe", "revenue_growth"]},
            {"name": "multi_factor", "description": "多因子策略", "factors": ["momentum_20d", "pe_ratio", "roe"]},
            {"name": "trend_follow", "description": "趋势跟踪", "factors": ["ma_cross", "breakout"]},
        ]
        return success_response({"templates": templates}, "strategy.list_templates")
    
    @staticmethod
    async def validate(args: Dict) -> Dict:
        """验证策略代码"""
        code = args.get("code", "")
        
        issues = []
        if "initialize" not in code:
            issues.append({"level": "error", "message": "缺少initialize函数"})
        if "handle_data" not in code:
            issues.append({"level": "warning", "message": "缺少handle_data函数"})
        
        return success_response({
            "valid": len([i for i in issues if i["level"] == "error"]) == 0,
            "issues": issues
        }, "strategy.validate")


class BacktestHandler:
    """回测处理器"""
    
    @staticmethod
    async def run(args: Dict) -> Dict:
        """执行回测"""
        try:
            from backtest_server import _handle_jqdata_backtest
            result = await _handle_jqdata_backtest(args)
            return success_response(result, "backtest.run")
        except Exception as e:
            return error_response(str(e), "BACKTEST_ERROR", "backtest.run")
    
    @staticmethod
    async def quick(args: Dict) -> Dict:
        """快速向量化回测"""
        try:
            from backtest_server import _handle_quick_backtest
            result = await _handle_quick_backtest(args)
            return success_response(result, "backtest.quick")
        except Exception as e:
            return error_response(str(e), "BACKTEST_ERROR", "backtest.quick")
    
    @staticmethod
    async def compare(args: Dict) -> Dict:
        """比较回测结果"""
        backtest_ids = args.get("backtest_ids", [])
        # 简化实现
        return success_response({
            "comparison": "功能开发中",
            "backtest_ids": backtest_ids
        }, "backtest.compare")


class OptimizerHandler:
    """优化器处理器"""
    
    @staticmethod
    async def grid_search(args: Dict) -> Dict:
        """网格搜索"""
        try:
            from optimizer_server import _handle_grid_search
            result = await _handle_grid_search(args)
            return success_response(result, "optimizer.grid_search")
        except Exception as e:
            return error_response(str(e), "OPTIMIZER_ERROR", "optimizer.grid_search")
    
    @staticmethod
    async def optuna(args: Dict) -> Dict:
        """Optuna优化"""
        # 简化实现
        return success_response({
            "status": "功能开发中",
            "message": "Optuna优化需要安装optuna包"
        }, "optimizer.optuna")
    
    @staticmethod
    async def best_params(args: Dict) -> Dict:
        """获取最佳参数"""
        optimization_id = args.get("optimization_id", "")
        return success_response({
            "optimization_id": optimization_id,
            "best_params": {},
            "message": "请先运行优化"
        }, "optimizer.best_params")


# ============================================================
# 工具路由
# ============================================================

TOOL_HANDLERS = {
    # Data
    "data.get_price": DataHandler.get_price,
    "data.get_index_stocks": DataHandler.get_index_stocks,
    "data.health_check": DataHandler.health_check,
    "data.candidate_pool": DataHandler.candidate_pool,
    
    # Market
    "market.status": MarketHandler.status,
    "market.trend": MarketHandler.trend,
    "market.mainlines": MarketHandler.mainlines,
    "market.five_dimension_score": MarketHandler.five_dimension_score,
    "market.comprehensive": MarketHandler.comprehensive,
    
    # Factor
    "factor.recommend": FactorHandler.recommend,
    "factor.calculate": FactorHandler.calculate,
    "factor.list": FactorHandler.list_factors,
    
    # Strategy
    "strategy.generate": StrategyHandler.generate,
    "strategy.list_templates": StrategyHandler.list_templates,
    "strategy.validate": StrategyHandler.validate,
    
    # Backtest
    "backtest.run": BacktestHandler.run,
    "backtest.quick": BacktestHandler.quick,
    "backtest.compare": BacktestHandler.compare,
    
    # Optimizer
    "optimizer.grid_search": OptimizerHandler.grid_search,
    "optimizer.optuna": OptimizerHandler.optuna,
    "optimizer.best_params": OptimizerHandler.best_params,
}


# ============================================================
# MCP服务器接口
# ============================================================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有工具"""
    return TOOLS


@server.call_tool()
@track_performance
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """统一工具调用入口"""
    
    # 元数据工具
    if name == "core.metrics":
        result = success_response({
            "server": "trquant-core",
            "tools_count": len(TOOLS),
            "tool_metrics": _tool_metrics
        }, "core.metrics")
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    # 查找处理器
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        result = error_response(f"未知工具: {name}", "UNKNOWN_TOOL", name)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    # 调用处理器
    try:
        result = await handler(arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"工具 {name} 执行失败: {e}", exc_info=True)
        result = error_response(str(e), "EXECUTION_ERROR", name)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]


# ============================================================
# 主入口
# ============================================================

async def main():
    """主函数"""
    logger.info(f"TRQuant Core Server 启动中... 工具数: {len(TOOLS)}")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

