"""
M3.3.1: 分层候选池模块 (Layered Candidate Pool)

实现L0-L3四层候选池筛选：
- L0: 全量股票池
- L1: 粗筛池（基础筛选）
- L2: 精筛池（因子筛选）
- L3: 重点关注池（综合评分）

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PoolLevel(Enum):
    """候选池层级"""
    L0_UNIVERSE = "L0"
    L1_FILTERED = "L1"
    L2_REFINED = "L2"
    L3_FOCUSED = "L3"


@dataclass
class StockCandidate:
    """股票候选"""
    symbol: str
    name: str
    level: PoolLevel
    score: float = 0.0
    stage: Optional[str] = None
    scorecard: Optional[Dict] = None
    tags: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    events: List[Dict] = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "level": self.level.value,
            "score": self.score,
            "stage": self.stage,
            "scorecard": self.scorecard,
            "tags": self.tags,
            "reasons": self.reasons,
            "events": self.events,
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class FilterCriteria:
    """筛选条件"""
    exclude_st: bool = True
    exclude_suspended: bool = True
    min_market_cap: float = 30.0
    max_market_cap: float = 2000.0
    min_turnover: float = 0.5
    min_roe: float = 5.0
    min_revenue_growth: float = 0.0
    min_profit_growth: float = 0.0
    industries: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    min_stage: str = "S1"
    min_scorecard: float = 40.0
    min_events: int = 1


class LayeredCandidatePool:
    """分层候选池管理器"""
    
    def __init__(self, mongo_uri: Optional[str] = None):
        self._db = None
        self._collection = None
        self._pools: Dict[PoolLevel, Dict[str, StockCandidate]] = {
            PoolLevel.L0_UNIVERSE: {},
            PoolLevel.L1_FILTERED: {},
            PoolLevel.L2_REFINED: {},
            PoolLevel.L3_FOCUSED: {}
        }
        self._stats = {"last_updated": None, "total_candidates": 0, "level_counts": {}}
        
        if mongo_uri:
            self._init_mongodb(mongo_uri)
    
    def _init_mongodb(self, mongo_uri: str):
        try:
            from pymongo import MongoClient
            client = MongoClient(mongo_uri)
            self._db = client.trquant
            self._collection = self._db.candidate_pool
            logger.info("候选池MongoDB连接成功")
        except Exception as e:
            logger.warning(f"候选池MongoDB连接失败: {e}")
    
    def add_to_universe(self, symbols: List[Dict[str, str]]) -> int:
        count = 0
        for item in symbols:
            symbol = item.get("symbol")
            name = item.get("name", symbol)
            if symbol and symbol not in self._pools[PoolLevel.L0_UNIVERSE]:
                self._pools[PoolLevel.L0_UNIVERSE][symbol] = StockCandidate(
                    symbol=symbol, name=name, level=PoolLevel.L0_UNIVERSE
                )
                count += 1
        self._update_stats()
        return count
    
    def filter_to_l1(self, criteria: FilterCriteria, stock_data: Optional[Dict] = None) -> List[StockCandidate]:
        l1_candidates = []
        stock_data = stock_data or {}
        
        for symbol, candidate in self._pools[PoolLevel.L0_UNIVERSE].items():
            data = stock_data.get(symbol, {})
            reasons = []
            
            if criteria.exclude_st and data.get("is_st", False):
                continue
            if criteria.exclude_suspended and data.get("is_suspended", False):
                continue
            
            market_cap = data.get("market_cap", 0)
            if market_cap > 0:
                if market_cap < criteria.min_market_cap or market_cap > criteria.max_market_cap:
                    continue
                reasons.append(f"市值{market_cap:.1f}亿")
            
            new_candidate = StockCandidate(
                symbol=symbol, name=candidate.name, level=PoolLevel.L1_FILTERED,
                reasons=reasons, tags=["L1_PASS"]
            )
            self._pools[PoolLevel.L1_FILTERED][symbol] = new_candidate
            l1_candidates.append(new_candidate)
        
        self._update_stats()
        return l1_candidates
    
    def filter_to_l2(self, criteria: FilterCriteria, fundamental_data: Optional[Dict] = None) -> List[StockCandidate]:
        l2_candidates = []
        fundamental_data = fundamental_data or {}
        
        for symbol, candidate in self._pools[PoolLevel.L1_FILTERED].items():
            data = fundamental_data.get(symbol, {})
            reasons = list(candidate.reasons)
            tags = list(candidate.tags)
            
            roe = data.get("roe", 0)
            if roe < criteria.min_roe:
                continue
            if roe > 0:
                reasons.append(f"ROE {roe:.1f}%")
            
            tags.append("L2_PASS")
            new_candidate = StockCandidate(
                symbol=symbol, name=candidate.name, level=PoolLevel.L2_REFINED,
                reasons=reasons, tags=tags
            )
            self._pools[PoolLevel.L2_REFINED][symbol] = new_candidate
            l2_candidates.append(new_candidate)
        
        self._update_stats()
        return l2_candidates
    
    def filter_to_l3(self, criteria: FilterCriteria, 
                     stage_data: Optional[Dict] = None,
                     scorecard_data: Optional[Dict] = None,
                     event_data: Optional[Dict] = None) -> List[StockCandidate]:
        l3_candidates = []
        stage_data = stage_data or {}
        scorecard_data = scorecard_data or {}
        event_data = event_data or {}
        
        stage_order = {"S0": 0, "S1": 1, "S2": 2, "S3": 3, "S4": 4, "S5": 5}
        min_stage_order = stage_order.get(criteria.min_stage, 1)
        
        for symbol, candidate in self._pools[PoolLevel.L2_REFINED].items():
            reasons = list(candidate.reasons)
            tags = list(candidate.tags)
            
            stage = stage_data.get(symbol, "S0")
            if stage_order.get(stage, 0) < min_stage_order:
                continue
            reasons.append(f"阶段:{stage}")
            
            scorecard = scorecard_data.get(symbol, {})
            total_score = scorecard.get("total_score", 0)
            if total_score < criteria.min_scorecard:
                continue
            reasons.append(f"评分:{total_score:.1f}")
            
            events = event_data.get(symbol, [])
            if len(events) < criteria.min_events:
                continue
            
            tags.append("L3_FOCUSED")
            new_candidate = StockCandidate(
                symbol=symbol, name=candidate.name, level=PoolLevel.L3_FOCUSED,
                stage=stage, score=total_score, scorecard=scorecard,
                events=events, reasons=reasons, tags=tags
            )
            self._pools[PoolLevel.L3_FOCUSED][symbol] = new_candidate
            l3_candidates.append(new_candidate)
        
        l3_candidates.sort(key=lambda x: x.score, reverse=True)
        self._update_stats()
        return l3_candidates
    
    def get_pool(self, level: PoolLevel) -> List[StockCandidate]:
        return list(self._pools[level].values())
    
    def get_candidate(self, symbol: str, level: Optional[PoolLevel] = None) -> Optional[StockCandidate]:
        if level:
            return self._pools[level].get(symbol)
        for lvl in [PoolLevel.L3_FOCUSED, PoolLevel.L2_REFINED, PoolLevel.L1_FILTERED, PoolLevel.L0_UNIVERSE]:
            if symbol in self._pools[lvl]:
                return self._pools[lvl][symbol]
        return None
    
    def search(self, keyword: str, level: Optional[PoolLevel] = None) -> List[StockCandidate]:
        results = []
        levels = [level] if level else list(PoolLevel)
        for lvl in levels:
            for candidate in self._pools[lvl].values():
                if (keyword.lower() in candidate.symbol.lower() or 
                    keyword.lower() in candidate.name.lower()):
                    results.append(candidate)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "last_updated": self._stats["last_updated"],
            "total_candidates": self._stats["total_candidates"],
            "level_counts": {
                "L0": len(self._pools[PoolLevel.L0_UNIVERSE]),
                "L1": len(self._pools[PoolLevel.L1_FILTERED]),
                "L2": len(self._pools[PoolLevel.L2_REFINED]),
                "L3": len(self._pools[PoolLevel.L3_FOCUSED])
            }
        }
    
    def _update_stats(self):
        self._stats["last_updated"] = datetime.now().isoformat()
        self._stats["total_candidates"] = sum(len(pool) for pool in self._pools.values())
    
    def clear(self, level: Optional[PoolLevel] = None):
        if level:
            self._pools[level].clear()
        else:
            for lvl in PoolLevel:
                self._pools[lvl].clear()
        self._update_stats()


_candidate_pool: Optional[LayeredCandidatePool] = None

def get_candidate_pool(mongo_uri: Optional[str] = None) -> LayeredCandidatePool:
    global _candidate_pool
    if _candidate_pool is None:
        _candidate_pool = LayeredCandidatePool(mongo_uri)
    return _candidate_pool
