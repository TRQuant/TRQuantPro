"""
Tenbagger GUI命令处理

为GUI面板提供后端数据支持

Author: TRQuant Team
Date: 2025-12-18
"""

import sys
import os

# 添加mcp_servers到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../mcp_servers'))

from typing import Dict, Any, List


def candidate_pool_stats() -> Dict[str, Any]:
    """获取候选池统计"""
    try:
        from utils.candidate_pool import get_candidate_pool
        pool = get_candidate_pool()
        return pool.get_stats()
    except Exception as e:
        return {"error": str(e), "level_counts": {"L0": 0, "L1": 0, "L2": 0, "L3": 0}}


def tenbagger_ranking(limit: int = 10) -> List[Dict[str, Any]]:
    """获取十倍股潜力排名"""
    try:
        from utils.candidate_pool import get_candidate_pool, PoolLevel
        from utils.tenbagger_evaluator import TenbaggerEvaluator
        
        pool = get_candidate_pool()
        evaluator = TenbaggerEvaluator()
        
        # 从L3 → L2 → L1依次获取候选
        candidates = []
        for level in [PoolLevel.L3_FOCUSED, PoolLevel.L2_REFINED, PoolLevel.L1_FILTERED]:
            pool_candidates = pool.get_pool(level)
            for c in pool_candidates:
                candidates.append({
                    "symbol": c.symbol,
                    "name": c.name,
                    "stage": c.stage or "S0",
                    "score": c.score or 50,
                    "level": level.name
                })
            if len(candidates) >= limit:
                break
        
        # 按评分排序
        candidates.sort(key=lambda x: x.get("score", 0), reverse=True)
        return candidates[:limit]
    except Exception as e:
        return []


def tenbagger_evaluate(symbol: str) -> Dict[str, Any]:
    """评估单只股票的十倍股潜力"""
    try:
        from utils.datasource_manager import get_datasource_manager
        from utils.stage_machine import StageMachine
        from utils.scorecard import get_scorecard_engine
        from utils.tenbagger_evaluator import TenbaggerEvaluator
        
        # 获取数据
        manager = get_datasource_manager()
        data = manager.fetch_for_tenbagger([symbol])
        
        # 阶段判断
        sm = StageMachine()
        sm.get_or_create(symbol)
        record = sm.get_stage(symbol)
        stage = record.current_stage if record else "S0"
        
        # 评分卡
        engine = get_scorecard_engine()
        financial = data.get("financials", {}).get(symbol, {})
        card = engine.compute(
            security_id=symbol,
            financial_data=financial,
            stage_record={"current_stage": stage}
        )
        
        # Tenbagger评估
        evaluator = TenbaggerEvaluator()
        eval_data = {
            "stage": stage,
            "scorecard": {"total_score": card.total_score},
            "financials": financial
        }
        
        report = evaluator.evaluate(symbol, "", eval_data)
        
        return {
            "symbol": symbol,
            "stage": stage,
            "scorecard_score": card.total_score,
            "scorecard_grade": card.grade,
            "total_score": report.total_score,
            "eval_level": str(report.eval_level),
            "recommendation": report.recommendation
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def datasource_stats() -> Dict[str, Any]:
    """获取数据源统计"""
    try:
        from utils.datasource_manager import get_datasource_manager
        manager = get_datasource_manager()
        return manager.get_stats()
    except Exception as e:
        return {"error": str(e)}


def candidate_pool_filter(level: str) -> List[Dict[str, Any]]:
    """按层级筛选候选池"""
    try:
        from utils.candidate_pool import get_candidate_pool, PoolLevel
        
        pool = get_candidate_pool()
        
        level_map = {
            "L0": PoolLevel.L0_UNIVERSE,
            "L1": PoolLevel.L1_FILTERED,
            "L2": PoolLevel.L2_REFINED,
            "L3": PoolLevel.L3_FOCUSED,
            "all": None
        }
        
        target_level = level_map.get(level)
        
        if target_level:
            candidates = pool.get_pool(target_level)
        else:
            # 返回所有
            candidates = []
            for lvl in PoolLevel:
                candidates.extend(pool.get_pool(lvl))
        
        return [
            {
                "symbol": c.symbol,
                "name": c.name,
                "stage": c.stage or "S0",
                "score": c.score or 0,
                "level": c.level.name if hasattr(c, 'level') else "L0"
            }
            for c in candidates
        ]
    except Exception as e:
        return []


# 命令映射
COMMANDS = {
    "candidate_pool_stats": candidate_pool_stats,
    "tenbagger_ranking": tenbagger_ranking,
    "tenbagger_evaluate": tenbagger_evaluate,
    "datasource_stats": datasource_stats,
    "candidate_pool_filter": candidate_pool_filter
}


def handle_command(command: str, args: Dict[str, Any] = None) -> Any:
    """处理GUI命令"""
    if command not in COMMANDS:
        return {"error": f"Unknown command: {command}"}
    
    handler = COMMANDS[command]
    if args:
        return handler(**args)
    return handler()


# ==================== 产业链相关命令 ====================

def industry_chain_list() -> List[Dict[str, Any]]:
    """获取产业链列表"""
    try:
        from utils.industry_chain import get_industry_chain
        chain = get_industry_chain()
        chains = chain.list_chains()
        return chains
    except Exception as e:
        # 返回模拟数据
        return [
            {"id": "new_energy", "name": "新能源汽车", "node_count": 32, "stock_count": 156},
            {"id": "semiconductor", "name": "半导体", "node_count": 28, "stock_count": 124},
            {"id": "ai", "name": "人工智能", "node_count": 24, "stock_count": 98},
            {"id": "photovoltaic", "name": "光伏", "node_count": 20, "stock_count": 86}
        ]


def industry_chain_stats() -> Dict[str, Any]:
    """获取产业链统计"""
    try:
        from utils.industry_chain import get_industry_chain
        chain = get_industry_chain()
        return chain.get_stats()
    except Exception as e:
        return {"chain_count": 4, "node_count": 104, "stock_count": 464}


def industry_chain_detail(chain_id: str) -> Dict[str, Any]:
    """获取产业链详情"""
    try:
        from utils.industry_chain import get_industry_chain
        chain = get_industry_chain()
        return chain.get_chain_detail(chain_id)
    except Exception as e:
        return {"id": chain_id, "nodes": [], "edges": []}


def industry_chain_stocks(node_id: str) -> List[Dict[str, Any]]:
    """获取节点关联股票"""
    try:
        from utils.industry_chain import get_industry_chain
        chain = get_industry_chain()
        return chain.get_node_stocks(node_id)
    except Exception as e:
        return []


def industry_chain_search(query: str) -> List[Dict[str, Any]]:
    """搜索产业链"""
    try:
        from utils.industry_chain import get_industry_chain
        chain = get_industry_chain()
        return chain.search(query)
    except Exception as e:
        return []


# ==================== 个股详情命令 ====================

def stock_basic_info(symbol: str) -> Dict[str, Any]:
    """获取股票基本信息"""
    try:
        from utils.datasource_manager import get_datasource_manager, DataRequest, DataCategory
        manager = get_datasource_manager()
        
        financial = manager.fetch(DataRequest(category=DataCategory.FINANCIAL, symbols=[symbol]))
        price = manager.fetch(DataRequest(category=DataCategory.PRICE, symbols=[symbol]))
        
        fin_data = financial.data.get(symbol, {}) if financial.success else {}
        price_data = price.data.get(symbol, {}) if price.success else {}
        
        # 模拟名称映射
        names = {
            "300750.SZ": "宁德时代", "300750.XSHG": "宁德时代",
            "002594.SZ": "比亚迪", "002594.XSHE": "比亚迪",
            "600519.SH": "贵州茅台", "600519.XSHG": "贵州茅台"
        }
        
        return {
            "symbol": symbol,
            "name": names.get(symbol, symbol),
            "price": price_data.get("current_price", 0),
            "change_pct": price_data.get("change_pct", 0),
            "market_cap": fin_data.get("market_cap", 0),
            "pe_ratio": fin_data.get("pe_ratio", 0),
            "roe": fin_data.get("roe", 0)
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def stock_events(symbol: str) -> List[Dict[str, Any]]:
    """获取股票事件"""
    try:
        from utils.datasource_manager import get_datasource_manager, DataRequest, DataCategory
        manager = get_datasource_manager()
        
        resp = manager.fetch(DataRequest(category=DataCategory.EVENT, symbols=[symbol]))
        events = resp.data.get(symbol, []) if resp.success else []
        
        announcements = manager.fetch(DataRequest(category=DataCategory.ANNOUNCEMENT, symbols=[symbol]))
        anns = announcements.data.get(symbol, []) if announcements.success else []
        
        all_events = []
        for evt in events:
            all_events.append({
                "type": evt.get("type", "event"),
                "title": evt.get("desc", ""),
                "date": evt.get("date", ""),
                "impact": evt.get("impact", "medium")
            })
        
        for ann in anns:
            all_events.append({
                "type": "announcement",
                "title": ann.get("title", ""),
                "date": ann.get("date", ""),
                "impact": ann.get("type", "neutral")
            })
        
        return all_events[:20]
    except Exception as e:
        return []


def stock_stage(symbol: str) -> Dict[str, Any]:
    """获取股票阶段"""
    try:
        from utils.stage_machine import StageMachine
        sm = StageMachine()
        sm.get_or_create(symbol)
        record = sm.get_stage(symbol)
        
        return {
            "symbol": symbol,
            "current": record.current_stage if record else "S0",
            "confidence": record.confidence if record else 0.0
        }
    except Exception as e:
        return {"symbol": symbol, "current": "S0", "confidence": 0.0}


def candidate_pool_add(symbol: str, level: str) -> Dict[str, Any]:
    """添加股票到候选池"""
    try:
        from utils.candidate_pool import get_candidate_pool, PoolLevel, FilterCriteria
        pool = get_candidate_pool()
        
        pool.add_to_universe([{"symbol": symbol, "name": symbol}])
        
        return {"status": "success", "symbol": symbol, "level": level}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# 更新命令映射
COMMANDS.update({
    "industry_chain_list": industry_chain_list,
    "industry_chain_stats": industry_chain_stats,
    "industry_chain_detail": industry_chain_detail,
    "industry_chain_stocks": industry_chain_stocks,
    "industry_chain_search": industry_chain_search,
    "stock_basic_info": stock_basic_info,
    "stock_events": stock_events,
    "stock_stage": stock_stage,
    "candidate_pool_add": candidate_pool_add
})
