"""
十倍股评估 MCP工具 V2

基于V2评估系统的MCP工具定义

Author: TRQuant Team
Date: 2025-12-20
Version: 2.0
"""

from typing import Dict, Any, List, Optional
from mcp.types import Tool
import logging

logger = logging.getLogger(__name__)

# 延迟导入，避免循环依赖
_evaluator_v2 = None
_data_fetcher = None

def get_evaluator_v2():
    """获取V2评估器实例（单例）"""
    global _evaluator_v2
    if _evaluator_v2 is None:
        from mcp_servers.utils.tenbagger_v2 import get_evaluator_v2 as _get_evaluator
        _evaluator_v2 = _get_evaluator()
    return _evaluator_v2

def get_data_fetcher():
    """获取数据获取器实例（单例）"""
    global _data_fetcher
    if _data_fetcher is None:
        from mcp_servers.utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
        from jqdata.client import JQDataClient
        from config.config_manager import get_config_manager
        
        # 初始化JQData客户端
        jq_client = JQDataClient()
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        jq_client.authenticate(jq_config['username'], jq_config['password'])
        
        _data_fetcher = TenbaggerDataFetcher(jq_client)
    return _data_fetcher


# ==================== 工具处理器 ====================

# 使用适配器模式（解耦架构）
def _get_adapter():
    """获取适配器实例（延迟加载）"""
    try:
        from mcp_servers.utils.adapters.tenbagger_adapter import get_tenbagger_adapter
        return get_tenbagger_adapter()
    except ImportError:
        # 如果适配器不可用，返回None，使用直接调用方式
        logger.warning("适配器不可用，使用直接调用方式")
        return None

async def handle_tenbagger_v2_evaluate(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.evaluate 工具调用"""
    # 优先使用适配器（解耦架构）
    adapter = _get_adapter()
    if adapter:
        args.setdefault("version", "v2")
        return await adapter.handle_evaluate(args)
    
    # 降级：直接调用（向后兼容）
    try:
        symbol = args.get("symbol")
        name = args.get("name", symbol)
        data = args.get("data", {})
        
        if not symbol:
            return {"success": False, "error": "缺少必需参数: symbol"}
        
        evaluator = get_evaluator_v2()
        report = evaluator.evaluate(symbol, name, data)
        
        return {
            "success": True,
            "report": report.to_dict()
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.evaluate 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_batch(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.batch 工具调用"""
    # 优先使用适配器（解耦架构）
    adapter = _get_adapter()
    if adapter:
        args.setdefault("version", "v2")
        return await adapter.handle_batch(args)
    
    # 降级：直接调用（向后兼容）
    try:
        symbols = args.get("symbols", [])
        max_count = args.get("max_count", 100)
        
        if not symbols:
            return {"success": False, "error": "缺少必需参数: symbols"}
        
        evaluator = get_evaluator_v2()
        data_fetcher = get_data_fetcher()
        
        results = []
        for symbol in symbols[:max_count]:
            try:
                # 获取数据
                data = data_fetcher.fetch_stock_data(symbol)
                if not data:
                    continue
                
                # 评估
                report = evaluator.evaluate(symbol, data.get("name", symbol), data)
                results.append(report.to_dict())
            except Exception as e:
                logger.warning(f"评估 {symbol} 失败: {e}")
                continue
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.batch 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.report 工具调用（通过适配器）"""
    # 优先使用适配器（解耦架构）
    adapter = _get_adapter()
    if adapter:
        args.setdefault("version", "v2")
        return await adapter.handle_get_report(args)
    
    # 降级：直接调用（向后兼容）
    try:
        symbol = args.get("symbol")
        
        if not symbol:
            return {"success": False, "error": "缺少必需参数: symbol"}
        
        evaluator = get_evaluator_v2()
        report = evaluator.get_report(symbol)
        
        if not report:
            return {"success": False, "error": f"未找到 {symbol} 的评估报告"}
        
        return {
            "success": True,
            "report": report.to_dict()
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.report 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_recommendations(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.recommendations 工具调用（通过适配器）"""
    # 优先使用适配器（解耦架构）
    adapter = _get_adapter()
    if adapter:
        args.setdefault("version", "v2")
        return await adapter.handle_get_rankings(args)
    
    # 降级：直接调用（向后兼容）
    try:
        min_level = args.get("min_level", "A")  # S+/S/A/B/C/D
        top_n = args.get("top_n", 20)
        
        evaluator = get_evaluator_v2()
        reports = evaluator.get_all_reports()
        
        # 过滤推荐等级
        level_order = {"S+": 6, "S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "REJECTED": 0}
        min_level_value = level_order.get(min_level, 4)
        
        filtered = [
            r.to_dict() for r in reports
            if r.is_recommended and level_order.get(r.recommendation_level, 0) >= min_level_value
        ]
        
        # 按分数排序
        filtered.sort(key=lambda x: x["final_score"], reverse=True)
        
        return {
            "success": True,
            "count": len(filtered[:top_n]),
            "recommendations": filtered[:top_n]
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.recommendations 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.stats 工具调用"""
    try:
        evaluator = get_evaluator_v2()
        reports = evaluator.get_all_reports()
        
        if not reports:
            return {
                "success": True,
                "total": 0,
                "stats": {}
            }
        
        # 统计
        total = len(reports)
        recommended = sum(1 for r in reports if r.is_recommended)
        recommendation_rate = recommended / total if total > 0 else 0
        
        # 等级分布
        level_dist = {}
        for r in reports:
            level = r.recommendation_level
            level_dist[level] = level_dist.get(level, 0) + 1
        
        # 阶段分布
        stage_dist = {}
        for r in reports:
            stage = r.stage
            stage_dist[stage] = stage_dist.get(stage, 0) + 1
        
        # 通过率控制
        from mcp_servers.utils.tenbagger_v2 import get_pass_rate_controller
        controller = get_pass_rate_controller()
        pass_rate_info = controller.get_current_stats()
        
        return {
            "success": True,
            "total": total,
            "recommended": recommended,
            "recommendation_rate": round(recommendation_rate * 100, 2),
            "level_distribution": level_dist,
            "stage_distribution": stage_dist,
            "pass_rate_control": pass_rate_info
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.stats 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_generate_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.generate_report 工具调用（通过适配器）"""
    # 优先使用适配器（解耦架构）
    adapter = _get_adapter()
    if adapter:
        args.setdefault("version", "v2")
        return await adapter.handle_generate_report(args)
    
    # 降级：直接调用（向后兼容）
    try:
        format_type = args.get("format", "markdown")  # markdown/json/html
        output_path = args.get("output_path")
        min_level = args.get("min_level", "A")
        filter_type = args.get("filter_type", "recommended")
        
        evaluator = get_evaluator_v2()
        from mcp_servers.utils.tenbagger_v2 import ReportGenerator
        
        generator = ReportGenerator(evaluator)
        
        # 获取推荐列表
        level_order = {"S+": 6, "S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "REJECTED": 0}
        min_level_value = level_order.get(min_level, 4)
        
        reports = [
            r for r in evaluator.get_all_reports()
            if r.is_recommended and level_order.get(r.recommendation_level, 0) >= min_level_value
        ]
        
        # 生成报告内容
        if format_type == "html":
            content = generator.generate_html(
                reports=reports,
                filter_type=filter_type,
                filter_value=min_level,
                include_metadata=args.get("include_metadata", True)
            )
        elif format_type == "markdown":
            content = generator.generate_markdown(
                reports=reports,
                filter_type=filter_type,
                filter_value=min_level,
                include_metadata=args.get("include_metadata", True)
            )
        else:
            content = generator.generate_json(
                reports=reports,
                filter_type=filter_type,
                filter_value=min_level
            )
        
        # 如果指定了输出路径，保存文件
        if output_path:
            generator.save_report(
                output_path=output_path,
                format=format_type,
                reports=reports,
                filter_type=filter_type,
                filter_value=min_level,
                include_metadata=args.get("include_metadata", True)
            )
        
        return {
            "success": True,
            "format": format_type,
            "output_path": output_path,
            "content": content if format_type in ["html", "markdown"] else None,
            "count": len(reports)
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.generate_report 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def handle_tenbagger_v2_consistency_check(args: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tenbagger_v2.consistency_check 工具调用"""
    try:
        evaluator = get_evaluator_v2()
        from mcp_servers.utils.tenbagger_v2 import get_pass_rate_controller
        
        controller = get_pass_rate_controller()
        consistency_report = controller.check_consistency()
        
        return {
            "success": True,
            "consistency_report": consistency_report.to_dict() if hasattr(consistency_report, 'to_dict') else str(consistency_report)
        }
    except Exception as e:
        logger.error(f"tenbagger_v2.consistency_check 错误: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== MCP工具定义 ====================

TENBAGGER_TOOLS_V2 = [
    Tool(
        name="tenbagger_v2.evaluate",
        description="【V2】评估单只股票的十倍股潜力（三层漏斗+双引擎+三轴阶段）",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码（如：000001.XSHE）"},
                "name": {"type": "string", "description": "股票名称"},
                "data": {
                    "type": "object",
                    "description": "股票数据（可选，如果不提供会自动获取）",
                    "properties": {
                        "is_st": {"type": "boolean"},
                        "revenue_growth_qoq_change": {"type": "number"},
                        "profit_growth_qoq_change": {"type": "number"},
                        "roe": {"type": "number"},
                        "pe_ratio": {"type": "number"},
                        "market_cap": {"type": "number"}
                    }
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger_v2.batch",
        description="【V2】批量评估多只股票（使用三层漏斗筛选）",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "max_count": {"type": "integer", "default": 100, "description": "最大评估数量"}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="tenbagger_v2.report",
        description="【V2】获取股票的详细评估报告",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码"}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger_v2.recommendations",
        description="【V2】获取推荐列表（自动过滤，按等级和分数排序）",
        inputSchema={
            "type": "object",
            "properties": {
                "min_level": {
                    "type": "string",
                    "enum": ["S+", "S", "A", "B", "C", "D"],
                    "default": "A",
                    "description": "最低推荐等级"
                },
                "top_n": {"type": "integer", "default": 20, "description": "返回前N个推荐"}
            }
        }
    ),
    Tool(
        name="tenbagger_v2.stats",
        description="【V2】获取评估统计信息（含通过率控制）",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),
    Tool(
        name="tenbagger_v2.generate_report",
        description="【V2】生成十倍股评估报告（支持markdown/json/html格式）",
        inputSchema={
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["markdown", "json", "html"],
                    "default": "markdown",
                    "description": "报告格式：markdown/json/html"
                },
                "output_path": {"type": "string", "description": "输出文件路径（可选，如指定则保存到文件）"},
                "min_level": {
                    "type": "string",
                    "enum": ["S+", "S", "A", "B", "C", "D"],
                    "default": "A",
                    "description": "最低推荐等级"
                },
                "filter_type": {
                    "type": "string",
                    "enum": ["all", "recommended", "by_level", "by_stage"],
                    "default": "recommended",
                    "description": "过滤类型"
                },
                "include_metadata": {
                    "type": "boolean",
                    "default": True,
                    "description": "是否包含元数据（统计信息、配置等）"
                }
            }
        }
    ),
    Tool(
        name="tenbagger_v2.consistency_check",
        description="【V2】检查评估结果的一致性（通过率控制）",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
]


# ==================== 工具处理器映射 ====================

TENBAGGER_HANDLERS_V2 = {
    "tenbagger_v2.evaluate": handle_tenbagger_v2_evaluate,
    "tenbagger_v2.batch": handle_tenbagger_v2_batch,
    "tenbagger_v2.report": handle_tenbagger_v2_report,
    "tenbagger_v2.recommendations": handle_tenbagger_v2_recommendations,
    "tenbagger_v2.stats": handle_tenbagger_v2_stats,
    "tenbagger_v2.generate_report": handle_tenbagger_v2_generate_report,
    "tenbagger_v2.consistency_check": handle_tenbagger_v2_consistency_check
}
