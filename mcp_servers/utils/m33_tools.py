"""
M3.3 MCP工具定义
"""

from typing import Dict, Any, List
from mcp.types import Tool

POOL_TOOLS = [
    Tool(
        name="pool.add_universe",
        description="添加股票到L0全量池",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "description": "股票列表 [{symbol, name}, ...]"}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="pool.filter_l1",
        description="从L0筛选到L1粗筛池",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="pool.filter_l2",
        description="从L1筛选到L2精筛池",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="pool.filter_l3",
        description="从L2筛选到L3重点关注池",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="pool.get",
        description="获取指定层级候选池",
        inputSchema={
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["L0", "L1", "L2", "L3"]},
                "limit": {"type": "integer", "default": 50}
            },
            "required": ["level"]
        }
    ),
    Tool(
        name="pool.search",
        description="搜索候选股票",
        inputSchema={
            "type": "object",
            "properties": {"keyword": {"type": "string"}},
            "required": ["keyword"]
        }
    ),
    Tool(
        name="pool.stats",
        description="获取候选池统计信息",
        inputSchema={"type": "object", "properties": {}}
    )
]

CHAIN_TOOLS = [
    Tool(
        name="chain.list",
        description="列出所有预定义产业链",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="chain.get",
        description="获取产业链详情",
        inputSchema={
            "type": "object",
            "properties": {"chain_name": {"type": "string"}},
            "required": ["chain_name"]
        }
    ),
    Tool(
        name="chain.find_node",
        description="查找产业节点",
        inputSchema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"]
        }
    ),
    Tool(
        name="chain.map_stock",
        description="将股票映射到产业节点",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "node_id": {"type": "string"}
            },
            "required": ["symbol", "node_id"]
        }
    ),
    Tool(
        name="chain.get_upstream",
        description="获取上游产业",
        inputSchema={
            "type": "object",
            "properties": {
                "node_id": {"type": "string"},
                "depth": {"type": "integer", "default": 1}
            },
            "required": ["node_id"]
        }
    ),
    Tool(
        name="chain.get_downstream",
        description="获取下游产业",
        inputSchema={
            "type": "object",
            "properties": {
                "node_id": {"type": "string"},
                "depth": {"type": "integer", "default": 1}
            },
            "required": ["node_id"]
        }
    ),
    Tool(
        name="chain.related_stocks",
        description="获取关联股票",
        inputSchema={
            "type": "object",
            "properties": {"symbol": {"type": "string"}},
            "required": ["symbol"]
        }
    ),
    Tool(
        name="chain.impact_analysis",
        description="产业链传导影响分析",
        inputSchema={
            "type": "object",
            "properties": {
                "node_id": {"type": "string"},
                "impact_type": {"type": "string", "default": "positive"}
            },
            "required": ["node_id"]
        }
    ),
    Tool(
        name="chain.stats",
        description="获取产业链图谱统计",
        inputSchema={"type": "object", "properties": {}}
    )
]

M33_TOOLS = POOL_TOOLS + CHAIN_TOOLS

from .candidate_pool import get_candidate_pool, FilterCriteria, PoolLevel
from .industry_chain import get_industry_chain


def _handle_pool_add_universe(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    symbols = args.get("symbols", [])
    count = pool.add_to_universe(symbols)
    return {"status": "success", "added": count, "total": len(pool.get_pool(PoolLevel.L0_UNIVERSE))}


def _handle_pool_filter_l1(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    criteria = FilterCriteria()
    candidates = pool.filter_to_l1(criteria)
    return {"status": "success", "filtered": len(candidates), "candidates": [c.to_dict() for c in candidates[:20]]}


def _handle_pool_filter_l2(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    criteria = FilterCriteria()
    candidates = pool.filter_to_l2(criteria)
    return {"status": "success", "filtered": len(candidates), "candidates": [c.to_dict() for c in candidates[:20]]}


def _handle_pool_filter_l3(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    criteria = FilterCriteria()
    candidates = pool.filter_to_l3(criteria)
    return {"status": "success", "filtered": len(candidates), "candidates": [c.to_dict() for c in candidates[:20]]}


def _handle_pool_get(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    level_str = args.get("level", "L3")
    limit = args.get("limit", 50)
    level_map = {"L0": PoolLevel.L0_UNIVERSE, "L1": PoolLevel.L1_FILTERED, "L2": PoolLevel.L2_REFINED, "L3": PoolLevel.L3_FOCUSED}
    level = level_map.get(level_str, PoolLevel.L3_FOCUSED)
    candidates = pool.get_pool(level)[:limit]
    return {"status": "success", "level": level_str, "count": len(candidates), "candidates": [c.to_dict() for c in candidates]}


def _handle_pool_search(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    keyword = args.get("keyword", "")
    results = pool.search(keyword)
    return {"status": "success", "keyword": keyword, "count": len(results), "results": [c.to_dict() for c in results[:30]]}


def _handle_pool_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    pool = get_candidate_pool()
    return {"status": "success", **pool.get_stats()}


def _handle_chain_list(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    return {"status": "success", "chains": chain.list_chains()}


def _handle_chain_get(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    chain_name = args.get("chain_name", "")
    nodes = chain.get_chain_nodes(chain_name)
    return {
        "status": "success",
        "chain_name": chain_name,
        "upstream": [n.to_dict() for n in nodes["upstream"]],
        "midstream": [n.to_dict() for n in nodes["midstream"]],
        "downstream": [n.to_dict() for n in nodes["downstream"]]
    }


def _handle_chain_find_node(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    name = args.get("name", "")
    nodes = chain.find_nodes_by_name(name)
    return {"status": "success", "keyword": name, "count": len(nodes), "nodes": [n.to_dict() for n in nodes]}


def _handle_chain_map_stock(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    symbol = args.get("symbol", "")
    node_id = args.get("node_id", "")
    chain.map_stock_to_industry(symbol, node_id)
    return {"status": "success", "symbol": symbol, "node_id": node_id}


def _handle_chain_get_upstream(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    node_id = args.get("node_id", "")
    depth = args.get("depth", 1)
    upstream = chain.get_upstream(node_id, depth)
    return {"status": "success", "node_id": node_id, "upstream": [n.to_dict() for n in upstream]}


def _handle_chain_get_downstream(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    node_id = args.get("node_id", "")
    depth = args.get("depth", 1)
    downstream = chain.get_downstream(node_id, depth)
    return {"status": "success", "node_id": node_id, "downstream": [n.to_dict() for n in downstream]}


def _handle_chain_related_stocks(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    symbol = args.get("symbol", "")
    related = chain.get_related_stocks(symbol, 1)
    return {"status": "success", "symbol": symbol, **related}


def _handle_chain_impact_analysis(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    node_id = args.get("node_id", "")
    impact_type = args.get("impact_type", "positive")
    impacts = chain.analyze_chain_impact(node_id, impact_type)
    return {"status": "success", "trigger": node_id, "impact_type": impact_type, "impacts": impacts}


def _handle_chain_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    chain = get_industry_chain()
    return {"status": "success", **chain.get_stats()}


M33_HANDLERS = {
    "pool.add_universe": _handle_pool_add_universe,
    "pool.filter_l1": _handle_pool_filter_l1,
    "pool.filter_l2": _handle_pool_filter_l2,
    "pool.filter_l3": _handle_pool_filter_l3,
    "pool.get": _handle_pool_get,
    "pool.search": _handle_pool_search,
    "pool.stats": _handle_pool_stats,
    "chain.list": _handle_chain_list,
    "chain.get": _handle_chain_get,
    "chain.find_node": _handle_chain_find_node,
    "chain.map_stock": _handle_chain_map_stock,
    "chain.get_upstream": _handle_chain_get_upstream,
    "chain.get_downstream": _handle_chain_get_downstream,
    "chain.related_stocks": _handle_chain_related_stocks,
    "chain.impact_analysis": _handle_chain_impact_analysis,
    "chain.stats": _handle_chain_stats
}
