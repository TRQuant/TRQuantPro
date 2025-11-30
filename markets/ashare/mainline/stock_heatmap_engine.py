"""
个股热度评分引擎

基于《市场主线识别模块之热度评分设计方案.pdf》设计

8个热度因子：
1. 主线热度 (15%) - 所属主题热度评分
2. 公司新闻数 (15%) - 媒体曝光度
3. 龙虎榜次数 (15%) - 游资关注度
4. 涨停次数 (15%) - 资金追捧度
5. 热点概念重合度 (10%) - 题材叠加效应
6. 板块热度占比 (10%) - 板块领军性
7. 股吧/雪球提及数 (10%) - 散户讨论热度
8. 估值提升热度 (10%) - 炒作溢价度

策略应用：
- 主线内部精选策略
- 短线轮动策略
- 事件驱动策略
- 风险监控与止盈
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class StockHeatLevel(Enum):
    """个股热度等级"""
    EXTREMELY_HOT = "极热"   # 90+
    VERY_HOT = "很热"        # 75-90
    HOT = "热门"             # 60-75
    WARM = "温和"            # 40-60
    COLD = "冷门"            # <40


class StockSignal(Enum):
    """个股信号"""
    STRONG_BUY = "强烈关注"
    BUY = "关注"
    WATCH = "观察"
    CAUTION = "谨慎"
    AVOID = "回避"


@dataclass
class StockHeatmapScore:
    """个股热度评分结果"""
    
    # 股票标识
    stock_code: str = ""
    stock_name: str = ""
    
    # 所属主线
    mainline_name: str = ""
    mainline_type: str = ""
    
    # 8个因子得分 (0-100)
    mainline_heat_score: float = 0.0    # 主线热度 (15%)
    news_score: float = 0.0             # 公司新闻数 (15%)
    lhb_score: float = 0.0              # 龙虎榜次数 (15%)
    limit_up_score: float = 0.0         # 涨停次数 (15%)
    concept_overlap_score: float = 0.0  # 热点概念重合度 (10%)
    sector_share_score: float = 0.0     # 板块热度占比 (10%)
    social_score: float = 0.0           # 股吧/雪球提及数 (10%)
    valuation_heat_score: float = 0.0   # 估值提升热度 (10%)
    
    # 综合得分
    total_score: float = 0.0
    
    # 等级和信号
    heat_level: StockHeatLevel = StockHeatLevel.COLD
    signal: StockSignal = StockSignal.WATCH
    
    # 排名
    rank: int = 0
    rank_in_sector: int = 0  # 板块内排名
    
    # 市场数据
    change_pct: float = 0.0
    turnover_rate: float = 0.0
    pe_ratio: float = 0.0
    market_cap: float = 0.0  # 市值（亿）
    
    def calculate_total(self) -> float:
        """计算总分（加权求和）"""
        self.total_score = (
            self.mainline_heat_score * 0.15 +
            self.news_score * 0.15 +
            self.lhb_score * 0.15 +
            self.limit_up_score * 0.15 +
            self.concept_overlap_score * 0.10 +
            self.sector_share_score * 0.10 +
            self.social_score * 0.10 +
            self.valuation_heat_score * 0.10
        )
        
        # 设置热度等级
        if self.total_score >= 90:
            self.heat_level = StockHeatLevel.EXTREMELY_HOT
        elif self.total_score >= 75:
            self.heat_level = StockHeatLevel.VERY_HOT
        elif self.total_score >= 60:
            self.heat_level = StockHeatLevel.HOT
        elif self.total_score >= 40:
            self.heat_level = StockHeatLevel.WARM
        else:
            self.heat_level = StockHeatLevel.COLD
        
        # 设置信号
        if self.total_score >= 80:
            self.signal = StockSignal.STRONG_BUY
        elif self.total_score >= 65:
            self.signal = StockSignal.BUY
        elif self.total_score >= 50:
            self.signal = StockSignal.WATCH
        elif self.total_score >= 35:
            self.signal = StockSignal.CAUTION
        else:
            self.signal = StockSignal.AVOID
        
        return self.total_score
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "mainline_name": self.mainline_name,
            "mainline_type": self.mainline_type,
            "mainline_heat_score": round(self.mainline_heat_score, 1),
            "news_score": round(self.news_score, 1),
            "lhb_score": round(self.lhb_score, 1),
            "limit_up_score": round(self.limit_up_score, 1),
            "concept_overlap_score": round(self.concept_overlap_score, 1),
            "sector_share_score": round(self.sector_share_score, 1),
            "social_score": round(self.social_score, 1),
            "valuation_heat_score": round(self.valuation_heat_score, 1),
            "total_score": round(self.total_score, 1),
            "heat_level": self.heat_level.value,
            "signal": self.signal.value,
            "rank": self.rank,
            "rank_in_sector": self.rank_in_sector,
            "change_pct": round(self.change_pct, 2),
            "turnover_rate": round(self.turnover_rate, 2),
            "pe_ratio": round(self.pe_ratio, 2),
            "market_cap": round(self.market_cap, 2),
        }
    
    def get_factor_breakdown(self) -> List[Dict]:
        """获取因子分解"""
        return [
            {"name": "主线热度", "score": self.mainline_heat_score, "weight": 15, "desc": "所属主题热度评分"},
            {"name": "公司新闻", "score": self.news_score, "weight": 15, "desc": "媒体曝光度"},
            {"name": "龙虎榜次数", "score": self.lhb_score, "weight": 15, "desc": "游资关注度"},
            {"name": "涨停次数", "score": self.limit_up_score, "weight": 15, "desc": "资金追捧度"},
            {"name": "概念重合度", "score": self.concept_overlap_score, "weight": 10, "desc": "题材叠加效应"},
            {"name": "板块占比", "score": self.sector_share_score, "weight": 10, "desc": "板块领军性"},
            {"name": "社交提及", "score": self.social_score, "weight": 10, "desc": "散户讨论热度"},
            {"name": "估值热度", "score": self.valuation_heat_score, "weight": 10, "desc": "炒作溢价度"},
        ]


class StockHeatmapEngine:
    """
    个股热度评分引擎
    
    用途：
    1. 从主线板块中筛选热度最高的个股
    2. 识别板块龙头股
    3. 短线轮动策略选股
    4. 事件驱动策略信号
    """
    
    # 因子权重配置
    FACTOR_WEIGHTS = {
        "mainline_heat": 0.15,
        "news": 0.15,
        "lhb": 0.15,
        "limit_up": 0.15,
        "concept_overlap": 0.10,
        "sector_share": 0.10,
        "social": 0.10,
        "valuation_heat": 0.10,
    }
    
    def __init__(self):
        """初始化引擎"""
        self.mainline_heatmap = {}  # 主线热度缓存
    
    def set_mainline_heatmap(self, heatmap: Dict[str, float]):
        """
        设置主线热度映射
        
        Args:
            heatmap: {主线名称: 热度得分}
        """
        self.mainline_heatmap = heatmap
    
    def calculate_stock_scores(
        self,
        stocks_data: List[Dict],
        hot_concepts: List[str] = None
    ) -> List[StockHeatmapScore]:
        """
        批量计算个股热度评分
        
        Args:
            stocks_data: 个股数据列表
            hot_concepts: 当前热门概念列表
        
        Returns:
            个股热度评分列表（已排序）
        """
        if not stocks_data:
            return []
        
        hot_concepts = hot_concepts or []
        
        # 收集归一化参数
        all_news = [d.get("news_count", 0) for d in stocks_data]
        all_lhb = [d.get("lhb_count", 0) for d in stocks_data]
        all_limit_up = [d.get("limit_up_count", 0) for d in stocks_data]
        all_social = [d.get("social_mentions", 0) for d in stocks_data]
        all_valuation = [d.get("valuation_change", 0) for d in stocks_data]
        
        norm_params = {
            "news": self._get_norm_params(all_news),
            "lhb": self._get_norm_params(all_lhb),
            "limit_up": self._get_norm_params(all_limit_up),
            "social": self._get_norm_params(all_social),
            "valuation": self._get_norm_params(all_valuation),
        }
        
        # 按板块分组计算板块占比
        sector_groups = {}
        for d in stocks_data:
            sector = d.get("sector", "")
            if sector not in sector_groups:
                sector_groups[sector] = []
            sector_groups[sector].append(d)
        
        # 计算每个个股的评分
        scores = []
        for data in stocks_data:
            score = self._calculate_single_score(
                data, norm_params, hot_concepts, sector_groups
            )
            scores.append(score)
        
        # 全局排序
        scores.sort(key=lambda x: x.total_score, reverse=True)
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        # 板块内排序
        sector_ranks = {}
        for score in scores:
            sector = score.mainline_name
            if sector not in sector_ranks:
                sector_ranks[sector] = 1
            score.rank_in_sector = sector_ranks[sector]
            sector_ranks[sector] += 1
        
        return scores
    
    def _calculate_single_score(
        self,
        data: Dict,
        norm_params: Dict,
        hot_concepts: List[str],
        sector_groups: Dict
    ) -> StockHeatmapScore:
        """计算单个个股的热度评分"""
        
        score = StockHeatmapScore(
            stock_code=data.get("code", ""),
            stock_name=data.get("name", ""),
            mainline_name=data.get("sector", ""),
            mainline_type=data.get("sector_type", ""),
            change_pct=data.get("change_pct", 0),
            turnover_rate=data.get("turnover_rate", 0),
            pe_ratio=data.get("pe_ratio", 0),
            market_cap=data.get("market_cap", 0),
        )
        
        # 1. 主线热度 (15%)
        mainline_heat = self.mainline_heatmap.get(data.get("sector", ""), 50)
        score.mainline_heat_score = mainline_heat
        
        # 2. 公司新闻数 (15%)
        news_count = data.get("news_count", 0)
        score.news_score = self._normalize_value(news_count, norm_params["news"])
        
        # 3. 龙虎榜次数 (15%)
        lhb_count = data.get("lhb_count", 0)
        score.lhb_score = self._normalize_value(lhb_count, norm_params["lhb"])
        
        # 4. 涨停次数 (15%)
        limit_up_count = data.get("limit_up_count", 0)
        score.limit_up_score = self._normalize_value(limit_up_count, norm_params["limit_up"])
        
        # 5. 热点概念重合度 (10%)
        stock_concepts = data.get("concepts", [])
        overlap_count = sum(1 for c in stock_concepts if c in hot_concepts)
        max_overlap = min(len(hot_concepts), 5)  # 最多5个热门概念
        score.concept_overlap_score = (overlap_count / max_overlap * 100) if max_overlap > 0 else 0
        
        # 6. 板块热度占比 (10%)
        sector = data.get("sector", "")
        if sector in sector_groups:
            sector_stocks = sector_groups[sector]
            total_heat = sum(s.get("heat_proxy", 0) for s in sector_stocks)
            stock_heat = data.get("heat_proxy", 0)
            score.sector_share_score = (stock_heat / total_heat * 100) if total_heat > 0 else 0
        else:
            score.sector_share_score = 50  # 默认中等
        
        # 7. 股吧/雪球提及数 (10%)
        social_mentions = data.get("social_mentions", 0)
        score.social_score = self._normalize_value(social_mentions, norm_params["social"])
        
        # 8. 估值提升热度 (10%)
        valuation_change = data.get("valuation_change", 0)
        score.valuation_heat_score = self._normalize_value(valuation_change, norm_params["valuation"])
        
        # 计算总分
        score.calculate_total()
        
        return score
    
    def _get_norm_params(self, values: List[float]) -> Dict:
        """获取归一化参数"""
        if not values:
            return {"min": 0, "max": 1}
        
        return {
            "min": min(values),
            "max": max(values),
        }
    
    def _normalize_value(
        self,
        value: float,
        params: Dict,
        target_min: float = 0,
        target_max: float = 100
    ) -> float:
        """Min-Max归一化"""
        min_val = params["min"]
        max_val = params["max"]
        
        if max_val == min_val:
            return target_max if value > 0 else target_min
        
        normalized = (value - min_val) / (max_val - min_val)
        scaled = normalized * (target_max - target_min) + target_min
        
        return max(target_min, min(target_max, scaled))
    
    def get_top_stocks_by_sector(
        self,
        scores: List[StockHeatmapScore],
        sector: str,
        top_n: int = 5
    ) -> List[StockHeatmapScore]:
        """
        获取板块内热度最高的个股
        
        Args:
            scores: 所有个股评分
            sector: 板块名称
            top_n: 返回数量
        
        Returns:
            板块内Top N个股
        """
        sector_stocks = [s for s in scores if s.mainline_name == sector]
        sector_stocks.sort(key=lambda x: x.total_score, reverse=True)
        return sector_stocks[:top_n]
    
    def get_leader_stocks(
        self,
        scores: List[StockHeatmapScore],
        threshold: float = 75
    ) -> List[StockHeatmapScore]:
        """
        获取龙头股（高热度个股）
        
        Args:
            scores: 所有个股评分
            threshold: 热度阈值
        
        Returns:
            龙头股列表
        """
        return [s for s in scores if s.total_score >= threshold]
    
    def get_rising_stars(
        self,
        current_scores: List[StockHeatmapScore],
        previous_scores: List[StockHeatmapScore],
        min_increase: float = 10
    ) -> List[Tuple[StockHeatmapScore, float]]:
        """
        获取热度快速上升的个股
        
        Args:
            current_scores: 当前评分
            previous_scores: 上期评分
            min_increase: 最小上升幅度
        
        Returns:
            [(个股评分, 上升幅度), ...]
        """
        prev_map = {s.stock_code: s.total_score for s in previous_scores}
        
        rising = []
        for score in current_scores:
            prev_score = prev_map.get(score.stock_code, 0)
            increase = score.total_score - prev_score
            if increase >= min_increase:
                rising.append((score, increase))
        
        rising.sort(key=lambda x: x[1], reverse=True)
        return rising
    
    def generate_trading_signals(
        self,
        scores: List[StockHeatmapScore]
    ) -> Dict[str, List[StockHeatmapScore]]:
        """
        生成交易信号分组
        
        Returns:
            {
                "strong_buy": [...],
                "buy": [...],
                "watch": [...],
                "caution": [...],
                "avoid": [...]
            }
        """
        signals = {
            "strong_buy": [],
            "buy": [],
            "watch": [],
            "caution": [],
            "avoid": [],
        }
        
        for score in scores:
            if score.signal == StockSignal.STRONG_BUY:
                signals["strong_buy"].append(score)
            elif score.signal == StockSignal.BUY:
                signals["buy"].append(score)
            elif score.signal == StockSignal.WATCH:
                signals["watch"].append(score)
            elif score.signal == StockSignal.CAUTION:
                signals["caution"].append(score)
            else:
                signals["avoid"].append(score)
        
        return signals


class StockDataAggregator:
    """
    个股数据聚合器
    
    从多个数据源聚合个股热度因子数据
    """
    
    def __init__(self):
        pass
    
    def aggregate_from_market_data(
        self,
        stocks: List[Dict],
        lhb_data: List[Dict] = None,
        news_data: Dict = None,
    ) -> List[Dict]:
        """
        从市场数据聚合个股热度因子
        
        Args:
            stocks: 个股基础数据列表
            lhb_data: 龙虎榜数据
            news_data: 新闻数据 {股票代码: 新闻数量}
        
        Returns:
            聚合后的个股数据列表
        """
        lhb_data = lhb_data or []
        news_data = news_data or {}
        
        # 统计龙虎榜次数
        lhb_counts = {}
        for item in lhb_data:
            code = item.get("代码", "")
            if code:
                lhb_counts[code] = lhb_counts.get(code, 0) + 1
        
        # 处理每只股票
        result = []
        for stock in stocks:
            code = stock.get("code", "")
            
            # 合并数据
            stock_data = {
                **stock,
                "lhb_count": lhb_counts.get(code, 0),
                "news_count": news_data.get(code, 0),
                # 估算其他因子
                "social_mentions": self._estimate_social_mentions(stock),
                "valuation_change": self._estimate_valuation_change(stock),
                "heat_proxy": self._calculate_heat_proxy(stock),
            }
            
            result.append(stock_data)
        
        return result
    
    def _estimate_social_mentions(self, stock: Dict) -> float:
        """估算社交媒体提及数"""
        change_pct = abs(stock.get("change_pct", 0))
        turnover = stock.get("turnover_rate", 0)
        
        base = 10
        change_factor = change_pct * 5
        turnover_factor = turnover * 2
        
        return base + change_factor + turnover_factor
    
    def _estimate_valuation_change(self, stock: Dict) -> float:
        """估算估值变化"""
        change_pct = stock.get("change_pct", 0)
        # 涨幅越大，估值提升越多
        return max(0, change_pct * 2)
    
    def _calculate_heat_proxy(self, stock: Dict) -> float:
        """计算热度代理指标（用于板块占比）"""
        change_pct = abs(stock.get("change_pct", 0))
        turnover = stock.get("turnover_rate", 0)
        volume = stock.get("volume", 0) / 1e8  # 转为亿
        
        return change_pct + turnover + volume


# 导出
__all__ = [
    "StockHeatmapEngine",
    "StockHeatmapScore",
    "StockHeatLevel",
    "StockSignal",
    "StockDataAggregator",
]

