# -*- coding: utf-8 -*-
"""
五维评分系统 - 统一引擎

基于《市场主线识别模块五维评分系统设计方案.pdf》设计

五大维度：
1. 资金维度 (30%) - 主力资金流强度
2. 热度维度 (20%) - 市场关注度和情绪强度（复用integrated_heatmap）
3. 动量维度 (20%) - 价格趋势和强度
4. 政策维度 (15%) - 政策支持力度
5. 龙头维度 (15%) - 龙头股表现及示范效应

数据源统一使用：
- 同花顺API（行业/概念资金流向）
- 东方财富API（涨停池、龙虎榜）
- 所有数据通过AKShare获取

设计原则：
1. 数据源一致性 - 所有维度使用相同的原始数据
2. 算法可靠性 - 使用排名百分位法，避免极值影响
3. 时间衰减 - 近期数据权重更高
4. 可解释性 - 每个因子计算过程透明
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# 统一数据源配置
# ============================================================

# 数据源类型枚举
class DataSourceType:
    """数据源类型"""
    AKSHARE = "akshare"      # 免费开源（当前使用）
    JQDATA = "jqdata"        # 聚宽（下一阶段）
    WIND = "wind"            # 万德（未来扩展）
    
    @staticmethod
    def get_all():
        return [DataSourceType.AKSHARE, DataSourceType.JQDATA, DataSourceType.WIND]
    
    @staticmethod
    def get_name(source_type: str) -> str:
        names = {
            DataSourceType.AKSHARE: "AKShare（免费）",
            DataSourceType.JQDATA: "聚宽JQData（付费）",
            DataSourceType.WIND: "万德Wind（机构级）",
        }
        return names.get(source_type, source_type)
    
    @staticmethod
    def get_status(source_type: str) -> str:
        """获取数据源状态"""
        status = {
            DataSourceType.AKSHARE: "✅ 已启用",
            DataSourceType.JQDATA: "⏳ 待开通",
            DataSourceType.WIND: "⏳ 待开通",
        }
        return status.get(source_type, "未知")


# 数据源配置（按数据源类型分类）
UNIFIED_DATA_SOURCES = {
    DataSourceType.AKSHARE: {
        "name": "AKShare",
        "status": "已启用",
        "description": "免费开源金融数据，通过同花顺/东方财富API获取",
        "sector_flow": {
            "name": "行业板块资金流向",
            "api": "ak.stock_fund_flow_industry(symbol='即时')",
            "provider": "同花顺",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
        },
        "concept_flow": {
            "name": "概念板块资金流向",
            "api": "ak.stock_fund_flow_concept(symbol='即时')",
            "provider": "同花顺",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
        },
        "limit_up_pool": {
            "name": "涨停池",
            "api": "ak.stock_zt_pool_em(date='YYYYMMDD')",
            "provider": "东方财富",
            "used_by": ["热度维度", "龙头维度"],
        },
        "dragon_tiger": {
            "name": "龙虎榜",
            "api": "ak.stock_lhb_detail_em(start_date, end_date)",
            "provider": "东方财富",
            "used_by": ["热度维度", "龙头维度"],
        },
        "northbound": {
            "name": "北向资金",
            "api": "ak.stock_hsgt_fund_flow_summary_em()",
            "provider": "东方财富",
            "used_by": ["资金维度"],
        },
    },
    DataSourceType.JQDATA: {
        "name": "聚宽JQData",
        "status": "待开通",
        "description": "专业量化数据平台，提供Level2数据、因子数据等",
        "sector_flow": {
            "name": "行业板块资金流向",
            "api": "jq.get_money_flow(industry='xxx')",  # 预留接口
            "provider": "聚宽",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
            "note": "需要JQData账号和API Key",
        },
        "concept_flow": {
            "name": "概念板块资金流向",
            "api": "jq.get_concept_money_flow(concept='xxx')",  # 预留接口
            "provider": "聚宽",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
        },
        "limit_up_pool": {
            "name": "涨停池",
            "api": "jq.get_limit_up_stocks(date='xxx')",  # 预留接口
            "provider": "聚宽",
            "used_by": ["热度维度", "龙头维度"],
        },
        "dragon_tiger": {
            "name": "龙虎榜",
            "api": "jq.get_dragon_tiger_list(date='xxx')",  # 预留接口
            "provider": "聚宽",
            "used_by": ["热度维度", "龙头维度"],
        },
        "northbound": {
            "name": "北向资金",
            "api": "jq.get_northbound_flow(date='xxx')",  # 预留接口
            "provider": "聚宽",
            "used_by": ["资金维度"],
        },
    },
    DataSourceType.WIND: {
        "name": "万德Wind",
        "status": "待开通",
        "description": "机构级金融数据平台，提供全球市场数据、另类数据等",
        "sector_flow": {
            "name": "行业板块资金流向",
            "api": "w.wsd(industry, 'money_flow', ...)",  # 预留接口
            "provider": "万德",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
            "note": "需要Wind终端和API授权",
        },
        "concept_flow": {
            "name": "概念板块资金流向",
            "api": "w.wsd(concept, 'money_flow', ...)",  # 预留接口
            "provider": "万德",
            "used_by": ["资金维度", "动量维度", "龙头维度"],
        },
        "limit_up_pool": {
            "name": "涨停池",
            "api": "w.wset('limitup', ...)",  # 预留接口
            "provider": "万德",
            "used_by": ["热度维度", "龙头维度"],
        },
        "dragon_tiger": {
            "name": "龙虎榜",
            "api": "w.wset('lhb', ...)",  # 预留接口
            "provider": "万德",
            "used_by": ["热度维度", "龙头维度"],
        },
        "northbound": {
            "name": "北向资金",
            "api": "w.wsd('northbound', 'net_inflow', ...)",  # 预留接口
            "provider": "万德",
            "used_by": ["资金维度"],
        },
    },
}


# ============================================================
# 五维评分权重配置（来自PDF设计方案）
# ============================================================

DIMENSION_WEIGHTS = {
    "funds": {
        "name": "资金维度",
        "weight": 0.30,
        "color": "#3B82F6",
        "icon": "💰",
        "description": "衡量主线题材的资金流强度",
        "factors": [
            {"name": "主力净流入排名", "weight": 0.40, "desc": "当日净流入在所有板块中的排名百分位"},
            {"name": "连续流入天数", "weight": 0.25, "desc": "主力资金连续流入的天数（需历史数据）"},
            {"name": "流入强度比", "weight": 0.20, "desc": "净流入/总流入，反映资金净流入强度"},
            {"name": "北向资金加成", "weight": 0.15, "desc": "北向资金当日是否净流入"},
        ],
    },
    "heat": {
        "name": "热度维度",
        "weight": 0.20,
        "color": "#EF4444",
        "icon": "🔥",
        "description": "衡量市场关注度和情绪强度",
        "factors": [
            {"name": "涨跌幅强度", "weight": 0.25, "desc": "涨幅越高，市场关注度越高"},
            {"name": "资金流入强度", "weight": 0.25, "desc": "资金净流入越多，机构认可度越高"},
            {"name": "涨停板数量", "weight": 0.20, "desc": "涨停股越多，板块炒作热度越高"},
            {"name": "龙虎榜活跃度", "weight": 0.15, "desc": "龙虎榜越多，游资参与度越高"},
            {"name": "龙头股强度", "weight": 0.15, "desc": "龙头越强，板块带动效应越强"},
        ],
    },
    "momentum": {
        "name": "动量维度",
        "weight": 0.20,
        "color": "#10B981",
        "icon": "📈",
        "description": "刻画主线题材的价格趋势和强度",
        "factors": [
            {"name": "价格动量", "weight": 0.40, "desc": "近期涨跌幅，衡量短期强势程度"},
            {"name": "相对强度", "weight": 0.30, "desc": "相对大盘的超额收益"},
            {"name": "成交量动量", "weight": 0.30, "desc": "成交额排名，反映资金活跃度"},
        ],
    },
    "policy": {
        "name": "政策维度",
        "weight": 0.15,
        "color": "#8B5CF6",
        "icon": "📜",
        "description": "评估主线获得的政策支撑力度",
        "factors": [
            {"name": "政策关联度", "weight": 0.50, "desc": "是否为当前政策重点支持方向"},
            {"name": "事件催化", "weight": 0.30, "desc": "近期是否有重大政策事件"},
            {"name": "产业趋势", "weight": 0.20, "desc": "行业是否处于上升周期"},
        ],
    },
    "leader": {
        "name": "龙头维度",
        "weight": 0.15,
        "color": "#F59E0B",
        "icon": "👑",
        "description": "反映题材内领涨股的表现及示范效应",
        "factors": [
            {"name": "龙头涨幅", "weight": 0.50, "desc": "龙头股涨幅，反映带动效应"},
            {"name": "龙头数量", "weight": 0.30, "desc": "板块内强势股数量"},
            {"name": "连板高度", "weight": 0.20, "desc": "最高连板数（如有）"},
        ],
    },
}


# 短中长期权重调整（来自PDF设计方案）
PERIOD_WEIGHT_ADJUSTMENTS = {
    "short": {
        "name": "短期(3-5日)",
        "description": "注重捕捉瞬时热点",
        "adjustments": {
            "funds": 0.25,
            "heat": 0.30,     # 短期提高热度权重
            "momentum": 0.25,  # 短期提高动量权重
            "policy": 0.10,
            "leader": 0.10,
        },
    },
    "medium": {
        "name": "中期(15-30日)",
        "description": "平衡热度持续性",
        "adjustments": {
            "funds": 0.30,
            "heat": 0.20,
            "momentum": 0.20,
            "policy": 0.15,
            "leader": 0.15,
        },
    },
    "long": {
        "name": "长期(60-180日)",
        "description": "侧重资金和政策持续性",
        "adjustments": {
            "funds": 0.35,     # 长期提高资金权重
            "heat": 0.10,     # 长期降低热度权重
            "momentum": 0.15,
            "policy": 0.25,    # 长期提高政策权重
            "leader": 0.15,
        },
    },
}


# ============================================================
# 评分结果数据结构
# ============================================================

@dataclass
class DimensionScore:
    """单维度评分"""
    name: str = ""
    score: float = 0.0          # 0-100
    weight: float = 0.0         # 权重
    weighted_score: float = 0.0  # 加权后得分
    color: str = ""
    icon: str = ""
    factors: List[Dict] = field(default_factory=list)  # 因子详情
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "weight": round(self.weight * 100, 0),
            "weighted_score": round(self.weighted_score, 1),
            "color": self.color,
            "icon": self.icon,
            "factors": self.factors,
        }


@dataclass
class FiveDimensionResult:
    """五维评分结果"""
    
    # 主线标识
    name: str = ""
    type: str = ""  # industry/concept
    
    # 五维评分
    funds_score: DimensionScore = field(default_factory=DimensionScore)
    heat_score: DimensionScore = field(default_factory=DimensionScore)
    momentum_score: DimensionScore = field(default_factory=DimensionScore)
    policy_score: DimensionScore = field(default_factory=DimensionScore)
    leader_score: DimensionScore = field(default_factory=DimensionScore)
    
    # 综合评分
    total_score: float = 0.0
    
    # 排名和等级
    rank: int = 0
    level: str = ""  # 极强/强/中等/弱/极弱
    level_color: str = ""
    
    # 原始数据
    change_pct: float = 0.0
    net_inflow: float = 0.0
    leader_stock: str = ""
    leader_change: float = 0.0
    
    # 趋势
    trend: str = "unknown"
    trend_change: float = 0.0
    
    # 周期
    period: str = "medium"
    
    # 信号
    signal: str = ""
    signal_desc: str = ""
    
    def calculate_total(self):
        """计算综合得分"""
        self.total_score = (
            self.funds_score.weighted_score +
            self.heat_score.weighted_score +
            self.momentum_score.weighted_score +
            self.policy_score.weighted_score +
            self.leader_score.weighted_score
        )
        
        # 设置等级
        if self.total_score >= 80:
            self.level = "极强"
            self.level_color = "#EF4444"
            self.signal = "买入"
            self.signal_desc = "强主线，可重点配置"
        elif self.total_score >= 65:
            self.level = "强"
            self.level_color = "#F97316"
            self.signal = "持有"
            self.signal_desc = "较强主线，可适当参与"
        elif self.total_score >= 50:
            self.level = "中等"
            self.level_color = "#EAB308"
            self.signal = "观察"
            self.signal_desc = "一般主线，观察为主"
        elif self.total_score >= 35:
            self.level = "弱"
            self.level_color = "#22C55E"
            self.signal = "减仓"
            self.signal_desc = "弱主线，控制仓位"
        else:
            self.level = "极弱"
            self.level_color = "#6B7280"
            self.signal = "卖出"
            self.signal_desc = "暂不参与"
        
        return self.total_score
    
    def get_radar_data(self) -> List[Dict]:
        """获取雷达图数据"""
        return [
            {"dimension": "资金", "score": self.funds_score.score, "full": 100},
            {"dimension": "热度", "score": self.heat_score.score, "full": 100},
            {"dimension": "动量", "score": self.momentum_score.score, "full": 100},
            {"dimension": "政策", "score": self.policy_score.score, "full": 100},
            {"dimension": "龙头", "score": self.leader_score.score, "full": 100},
        ]
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.type,
            "total_score": round(self.total_score, 1),
            "rank": self.rank,
            "level": self.level,
            "level_color": self.level_color,
            "signal": self.signal,
            "signal_desc": self.signal_desc,
            "dimensions": {
                "funds": self.funds_score.to_dict(),
                "heat": self.heat_score.to_dict(),
                "momentum": self.momentum_score.to_dict(),
                "policy": self.policy_score.to_dict(),
                "leader": self.leader_score.to_dict(),
            },
            "raw_data": {
                "change_pct": round(self.change_pct, 2),
                "net_inflow": round(self.net_inflow, 2),
                "leader_stock": self.leader_stock,
                "leader_change": round(self.leader_change, 2),
            },
            "trend": self.trend,
            "trend_change": round(self.trend_change, 1),
            "period": self.period,
        }


# ============================================================
# 五维评分引擎
# ============================================================

class FiveDimensionEngine:
    """
    五维评分引擎
    
    统一管理五个维度的评分计算，确保：
    1. 数据源一致性
    2. 算法可靠性
    3. 评分可解释性
    4. 多数据源支持（AKShare/JQData/Wind）
    """
    
    def __init__(self, data_source: str = DataSourceType.AKSHARE):
        """
        初始化引擎
        
        Args:
            data_source: 数据源类型，可选 "akshare", "jqdata", "wind"
        """
        self.dimension_config = DIMENSION_WEIGHTS
        self.period_adjustments = PERIOD_WEIGHT_ADJUSTMENTS
        self.results: List[FiveDimensionResult] = []
        
        # 数据源配置
        self.data_source = data_source
        self.data_source_config = UNIFIED_DATA_SOURCES.get(data_source, UNIFIED_DATA_SOURCES[DataSourceType.AKSHARE])
        
        # 缓存中间计算结果
        self._all_changes = []
        self._all_inflows = []
        self._all_leader_changes = []
        self._limit_up_data = {}
        self._lhb_data = []
        self._northbound_data = {}
    
    def calculate(
        self,
        sector_data: List[Dict],
        concept_data: List[Dict],
        limit_up_data: Dict = None,
        lhb_data: List[Dict] = None,
        northbound_data: Dict = None,
        period: str = "medium",
        history_scores: Dict[str, float] = None,
    ) -> List[FiveDimensionResult]:
        """
        计算五维评分
        
        Args:
            sector_data: 行业板块数据
            concept_data: 概念板块数据
            limit_up_data: 涨停池数据
            lhb_data: 龙虎榜数据
            northbound_data: 北向资金数据
            period: 评分周期 (short/medium/long)
            history_scores: 历史评分（用于趋势计算）
        
        Returns:
            五维评分结果列表
        """
        self.results = []
        
        # 缓存数据
        self._limit_up_data = limit_up_data or {}
        self._lhb_data = lhb_data or []
        self._northbound_data = northbound_data or {}
        
        # 获取周期权重
        weights = self._get_period_weights(period)
        
        # 预计算所有值（用于排名百分位计算）
        all_data = sector_data + concept_data
        self._all_changes = [self._safe_float(d.get("change_pct") or d.get("涨跌幅") or d.get("行业-涨跌幅")) for d in all_data]
        self._all_inflows = [self._safe_float(d.get("main_net_inflow") or d.get("net_inflow") or d.get("净额")) for d in all_data]
        self._all_leader_changes = [self._safe_float(d.get("leader_change") or d.get("领涨股-涨跌幅")) for d in all_data]
        
        # 计算行业板块
        for item in sector_data:
            result = self._calculate_single(item, "industry", weights, period, history_scores)
            if result:
                self.results.append(result)
        
        # 计算概念板块
        for item in concept_data:
            result = self._calculate_single(item, "concept", weights, period, history_scores)
            if result:
                self.results.append(result)
        
        # 排序并设置排名
        self.results.sort(key=lambda x: x.total_score, reverse=True)
        for i, result in enumerate(self.results):
            result.rank = i + 1
        
        return self.results
    
    def _get_period_weights(self, period: str) -> Dict[str, float]:
        """获取周期对应的权重"""
        if period in self.period_adjustments:
            return self.period_adjustments[period]["adjustments"]
        return {k: v["weight"] for k, v in self.dimension_config.items()}
    
    def _calculate_single(
        self,
        item: Dict,
        item_type: str,
        weights: Dict[str, float],
        period: str,
        history_scores: Dict[str, float] = None,
    ) -> Optional[FiveDimensionResult]:
        """计算单个板块的五维评分"""
        
        # 提取名称
        name = (item.get("sector_name") or item.get("board_name") or 
                item.get("行业") or item.get("概念") or "")
        if not name:
            return None
        
        # 提取原始数据
        change_pct = self._safe_float(item.get("change_pct") or item.get("涨跌幅") or item.get("行业-涨跌幅"))
        net_inflow = self._safe_float(item.get("main_net_inflow") or item.get("net_inflow") or item.get("净额"))
        inflow = self._safe_float(item.get("inflow") or item.get("流入资金")) or 1
        leader_stock = item.get("leader_stock") or item.get("领涨股") or ""
        leader_change = self._safe_float(item.get("leader_change") or item.get("领涨股-涨跌幅"))
        
        # 创建结果对象
        result = FiveDimensionResult(
            name=name,
            type=item_type,
            change_pct=change_pct,
            net_inflow=net_inflow,
            leader_stock=leader_stock,
            leader_change=leader_change,
            period=period,
        )
        
        # 1. 计算资金维度
        result.funds_score = self._calculate_funds_dimension(
            net_inflow, inflow, weights["funds"]
        )
        
        # 2. 计算热度维度（复用integrated_heatmap的逻辑）
        result.heat_score = self._calculate_heat_dimension(
            change_pct, net_inflow, leader_change, weights["heat"]
        )
        
        # 3. 计算动量维度
        result.momentum_score = self._calculate_momentum_dimension(
            change_pct, weights["momentum"]
        )
        
        # 4. 计算政策维度
        result.policy_score = self._calculate_policy_dimension(
            name, change_pct, net_inflow, weights["policy"]
        )
        
        # 5. 计算龙头维度
        result.leader_score = self._calculate_leader_dimension(
            leader_change, name, weights["leader"]
        )
        
        # 计算综合得分
        result.calculate_total()
        
        # 计算趋势
        if history_scores and name in history_scores:
            prev_score = history_scores[name]
            result.trend_change = result.total_score - prev_score
            if result.trend_change > 5:
                result.trend = "rising"
            elif result.trend_change < -5:
                result.trend = "falling"
            else:
                result.trend = "stable"
        
        return result
    
    def _calculate_funds_dimension(
        self,
        net_inflow: float,
        inflow: float,
        weight: float,
    ) -> DimensionScore:
        """
        计算资金维度评分 (0-100)
        
        因子：
        1. 主力净流入排名 (40%)
        2. 连续流入天数 (25%) - 暂用净流入正负替代
        3. 流入强度比 (20%)
        4. 北向资金加成 (15%)
        """
        config = self.dimension_config["funds"]
        factors = []
        
        # 1. 主力净流入排名 (40%)
        rank_score = self._calculate_percentile(net_inflow, self._all_inflows)
        factors.append({
            "name": "主力净流入排名",
            "score": rank_score,
            "weight": 40,
            "raw_value": f"{net_inflow:+.2f}亿",
        })
        
        # 2. 连续流入天数 (25%) - 用净流入正负替代
        continuous_score = 100 if net_inflow > 0 else 30
        if net_inflow > 5:
            continuous_score = 100
        elif net_inflow > 2:
            continuous_score = 80
        elif net_inflow > 0:
            continuous_score = 60
        factors.append({
            "name": "资金流向强度",
            "score": continuous_score,
            "weight": 25,
            "raw_value": "净流入" if net_inflow > 0 else "净流出",
        })
        
        # 3. 流入强度比 (20%)
        inflow_ratio = net_inflow / max(inflow, 0.01) if inflow > 0 else 0
        ratio_score = min(max(inflow_ratio * 100, 0), 100)
        factors.append({
            "name": "流入强度比",
            "score": ratio_score,
            "weight": 20,
            "raw_value": f"{inflow_ratio*100:.1f}%",
        })
        
        # 4. 北向资金加成 (15%)
        north_net = self._northbound_data.get("today_net", 0)
        north_score = 80 if north_net > 0 else 40
        if north_net > 50:
            north_score = 100
        elif north_net > 20:
            north_score = 90
        factors.append({
            "name": "北向资金",
            "score": north_score,
            "weight": 15,
            "raw_value": f"{north_net:+.2f}亿",
        })
        
        # 计算加权得分
        total_score = (
            rank_score * 0.40 +
            continuous_score * 0.25 +
            ratio_score * 0.20 +
            north_score * 0.15
        )
        
        return DimensionScore(
            name=config["name"],
            score=total_score,
            weight=weight,
            weighted_score=total_score * weight,
            color=config["color"],
            icon=config["icon"],
            factors=factors,
        )
    
    def _calculate_heat_dimension(
        self,
        change_pct: float,
        net_inflow: float,
        leader_change: float,
        weight: float,
    ) -> DimensionScore:
        """
        计算热度维度评分 (0-100)
        
        复用integrated_heatmap的5因子模型：
        1. 涨跌幅强度 (25%)
        2. 资金流入强度 (25%)
        3. 涨停板数量 (20%) - 使用估算
        4. 龙虎榜活跃度 (15%) - 使用估算
        5. 龙头股强度 (15%)
        """
        config = self.dimension_config["heat"]
        factors = []
        
        # 1. 涨跌幅强度 (25%)
        change_score = self._calculate_percentile(change_pct, self._all_changes)
        factors.append({
            "name": "涨跌幅强度",
            "score": change_score,
            "weight": 25,
            "raw_value": f"{change_pct:+.2f}%",
        })
        
        # 2. 资金流入强度 (25%)
        flow_score = self._calculate_percentile(net_inflow, self._all_inflows)
        factors.append({
            "name": "资金流入强度",
            "score": flow_score,
            "weight": 25,
            "raw_value": f"{net_inflow:+.2f}亿",
        })
        
        # 3. 涨停板数量 (20%) - 使用涨幅+资金估算
        total_limit_up = self._limit_up_data.get("up_limit_count", 0)
        if total_limit_up > 0:
            # 涨幅高+资金流入大 → 涨停股可能更多
            limit_up_score = (change_score * 0.6 + flow_score * 0.4)
            if change_pct > 5:
                limit_up_score = min(100, limit_up_score * 1.2)
            elif change_pct > 3:
                limit_up_score = min(100, limit_up_score * 1.1)
        else:
            limit_up_score = 50  # 无数据时给中等分
        factors.append({
            "name": "涨停板热度",
            "score": limit_up_score,
            "weight": 20,
            "raw_value": f"全市场{total_limit_up}只涨停",
        })
        
        # 4. 龙虎榜活跃度 (15%)
        total_lhb = len(self._lhb_data)
        if total_lhb > 0:
            # 龙头涨幅高 → 龙虎榜可能性更高
            leader_percentile = self._calculate_percentile(leader_change, self._all_leader_changes)
            lhb_score = (change_score * 0.4 + leader_percentile * 0.6)
            if leader_change >= 9.5:
                lhb_score = min(100, lhb_score * 1.3)
            elif leader_change >= 5:
                lhb_score = min(100, lhb_score * 1.1)
        else:
            lhb_score = 50  # 无数据时给中等分
        factors.append({
            "name": "龙虎榜活跃度",
            "score": lhb_score,
            "weight": 15,
            "raw_value": f"全市场{total_lhb}只上榜",
        })
        
        # 5. 龙头股强度 (15%)
        leader_score = self._calculate_percentile(leader_change, self._all_leader_changes)
        factors.append({
            "name": "龙头股强度",
            "score": leader_score,
            "weight": 15,
            "raw_value": f"{leader_change:+.2f}%",
        })
        
        # 计算加权得分
        total_score = (
            change_score * 0.25 +
            flow_score * 0.25 +
            limit_up_score * 0.20 +
            lhb_score * 0.15 +
            leader_score * 0.15
        )
        
        return DimensionScore(
            name=config["name"],
            score=total_score,
            weight=weight,
            weighted_score=total_score * weight,
            color=config["color"],
            icon=config["icon"],
            factors=factors,
        )
    
    def _calculate_momentum_dimension(
        self,
        change_pct: float,
        weight: float,
    ) -> DimensionScore:
        """
        计算动量维度评分 (0-100)
        
        因子：
        1. 价格动量 (40%)
        2. 相对强度 (30%)
        3. 成交量动量 (30%)
        """
        config = self.dimension_config["momentum"]
        factors = []
        
        # 1. 价格动量 (40%) - 涨跌幅排名
        price_score = self._calculate_percentile(change_pct, self._all_changes)
        factors.append({
            "name": "价格动量",
            "score": price_score,
            "weight": 40,
            "raw_value": f"{change_pct:+.2f}%",
        })
        
        # 2. 相对强度 (30%) - 简化：涨幅>0即为正向
        # 实际应减去大盘涨幅，这里简化处理
        relative_score = 50 + change_pct * 10  # 每涨1%加10分
        relative_score = min(max(relative_score, 0), 100)
        factors.append({
            "name": "相对强度",
            "score": relative_score,
            "weight": 30,
            "raw_value": f"超额{change_pct:+.2f}%",
        })
        
        # 3. 成交量动量 (30%) - 用资金流入排名替代
        volume_score = self._calculate_percentile(change_pct, self._all_changes)
        factors.append({
            "name": "成交活跃度",
            "score": volume_score,
            "weight": 30,
            "raw_value": f"排名{int(100-volume_score)}%",
        })
        
        # 计算加权得分
        total_score = (
            price_score * 0.40 +
            relative_score * 0.30 +
            volume_score * 0.30
        )
        
        return DimensionScore(
            name=config["name"],
            score=total_score,
            weight=weight,
            weighted_score=total_score * weight,
            color=config["color"],
            icon=config["icon"],
            factors=factors,
        )
    
    def _calculate_policy_dimension(
        self,
        name: str,
        change_pct: float,
        net_inflow: float,
        weight: float,
    ) -> DimensionScore:
        """
        计算政策维度评分 (0-100)
        
        因子：
        1. 政策关联度 (50%) - 使用关键词匹配
        2. 事件催化 (30%) - 使用资金+涨幅推断
        3. 产业趋势 (20%) - 使用涨幅趋势推断
        """
        config = self.dimension_config["policy"]
        factors = []
        
        # 政策热点关键词（根据当前市场热点调整）
        policy_keywords = {
            # 高政策支持度 (80-100分)
            "新能源": 90, "芯片": 90, "半导体": 90, "人工智能": 95, "AI": 95,
            "机器人": 90, "新基建": 85, "数字经济": 85, "碳中和": 85,
            "军工": 85, "航天": 85, "国产替代": 90, "信创": 90,
            # 中等政策支持度 (60-80分)
            "医药": 70, "消费": 65, "新材料": 75, "储能": 80,
            "光伏": 75, "风电": 75, "电池": 80, "汽车": 70,
            # 一般政策支持度 (40-60分)
            "金融": 50, "银行": 45, "保险": 50, "房地产": 40,
            "建筑": 50, "化工": 55, "钢铁": 45, "煤炭": 50,
        }
        
        # 1. 政策关联度 (50%)
        policy_score = 50  # 默认中等
        for keyword, score in policy_keywords.items():
            if keyword in name:
                policy_score = max(policy_score, score)
        factors.append({
            "name": "政策关联度",
            "score": policy_score,
            "weight": 50,
            "raw_value": "高" if policy_score >= 80 else ("中" if policy_score >= 60 else "低"),
        })
        
        # 2. 事件催化 (30%) - 资金大幅流入+大涨可能有事件
        event_score = 50  # 基础分
        if net_inflow > 5 and change_pct > 3:
            event_score = 90
        elif net_inflow > 2 or change_pct > 2:
            event_score = 70
        elif net_inflow > 0 or change_pct > 0:
            event_score = 60
        factors.append({
            "name": "事件催化",
            "score": event_score,
            "weight": 30,
            "raw_value": "强" if event_score >= 80 else ("中" if event_score >= 60 else "弱"),
        })
        
        # 3. 产业趋势 (20%) - 用涨幅推断
        trend_score = min(max(50 + change_pct * 10, 0), 100)
        factors.append({
            "name": "产业趋势",
            "score": trend_score,
            "weight": 20,
            "raw_value": "上升" if change_pct > 0 else "下降",
        })
        
        # 计算加权得分
        total_score = (
            policy_score * 0.50 +
            event_score * 0.30 +
            trend_score * 0.20
        )
        
        return DimensionScore(
            name=config["name"],
            score=total_score,
            weight=weight,
            weighted_score=total_score * weight,
            color=config["color"],
            icon=config["icon"],
            factors=factors,
        )
    
    def _calculate_leader_dimension(
        self,
        leader_change: float,
        name: str,
        weight: float,
    ) -> DimensionScore:
        """
        计算龙头维度评分 (0-100)
        
        因子：
        1. 龙头涨幅 (50%)
        2. 龙头数量 (30%) - 用涨幅估算
        3. 连板高度 (20%) - 用涨停数据
        """
        config = self.dimension_config["leader"]
        factors = []
        
        # 1. 龙头涨幅 (50%)
        leader_score = self._calculate_percentile(leader_change, self._all_leader_changes)
        # 涨停额外加分
        if leader_change >= 9.5:
            leader_score = min(100, leader_score * 1.2)
        factors.append({
            "name": "龙头涨幅",
            "score": leader_score,
            "weight": 50,
            "raw_value": f"{leader_change:+.2f}%",
        })
        
        # 2. 龙头数量 (30%) - 用涨幅和资金估算强势股数量
        count_score = leader_score  # 龙头强则通常板块内强势股多
        factors.append({
            "name": "强势股数量",
            "score": count_score,
            "weight": 30,
            "raw_value": "较多" if count_score >= 70 else ("中等" if count_score >= 50 else "较少"),
        })
        
        # 3. 连板高度 (20%) - 从涨停数据中提取
        continuous = self._limit_up_data.get("continuous_limit", {})
        # 确保键转换为整数进行比较
        try:
            if continuous:
                int_keys = [int(k) for k in continuous.keys() if str(k).isdigit()]
                max_continuous = max(int_keys) if int_keys else 0
            else:
                max_continuous = 0
        except (ValueError, TypeError):
            max_continuous = 0
        continuous_score = min(max_continuous * 20, 100) if max_continuous else 50
        factors.append({
            "name": "连板高度",
            "score": continuous_score,
            "weight": 20,
            "raw_value": f"最高{max_continuous}板" if max_continuous else "暂无连板",
        })
        
        # 计算加权得分
        total_score = (
            leader_score * 0.50 +
            count_score * 0.30 +
            continuous_score * 0.20
        )
        
        return DimensionScore(
            name=config["name"],
            score=total_score,
            weight=weight,
            weighted_score=total_score * weight,
            color=config["color"],
            icon=config["icon"],
            factors=factors,
        )
    
    def _calculate_percentile(self, value: float, all_values: List[float]) -> float:
        """
        计算排名百分位得分 (0-100)
        
        使用排名百分位法，避免极值影响
        """
        if not all_values:
            return 50.0
        
        # 过滤无效值
        valid_values = [v for v in all_values if v is not None and not math.isnan(v)]
        if not valid_values:
            return 50.0
        
        # 计算有多少值小于当前值
        count_less = sum(1 for v in valid_values if v < value)
        percentile = (count_less / len(valid_values)) * 100
        
        return percentile
    
    def _safe_float(self, value: Any) -> float:
        """安全转换为浮点数"""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def get_methodology(self) -> Dict:
        """获取方法论说明"""
        return {
            "title": "五维评分系统方法论",
            "source": "《市场主线识别模块五维评分系统设计方案.pdf》",
            
            "dimensions": [
                {
                    "name": dim["name"],
                    "weight": f"{dim['weight']*100:.0f}%",
                    "icon": dim["icon"],
                    "color": dim["color"],
                    "description": dim["description"],
                    "factors": dim["factors"],
                }
                for dim in self.dimension_config.values()
            ],
            
            "data_sources": {
                "current": self.data_source,
                "current_name": DataSourceType.get_name(self.data_source),
                "current_status": DataSourceType.get_status(self.data_source),
                "available": {
                    source: {
                        "name": DataSourceType.get_name(source),
                        "status": DataSourceType.get_status(source),
                        "config": UNIFIED_DATA_SOURCES.get(source, {}),
                    }
                    for source in DataSourceType.get_all()
                },
            },
            
            "period_weights": self.period_adjustments,
            
            "scoring_method": {
                "method": "排名百分位法",
                "formula": "得分 = (小于当前值的数量 / 总数量) × 100",
                "range": "0-100分",
                "advantage": "避免极值影响，结果稳定可靠",
            },
            
            "level_interpretation": {
                "极强(≥80分)": "强主线，可重点配置",
                "强(65-80分)": "较强主线，可适当参与",
                "中等(50-65分)": "一般主线，观察为主",
                "弱(35-50分)": "弱主线，控制仓位",
                "极弱(<35分)": "暂不参与",
            },
        }
    
    def set_data_source(self, data_source: str):
        """
        切换数据源
        
        Args:
            data_source: 数据源类型 "akshare", "jqdata", "wind"
        """
        if data_source in UNIFIED_DATA_SOURCES:
            self.data_source = data_source
            self.data_source_config = UNIFIED_DATA_SOURCES[data_source]
            logger.info(f"数据源已切换为: {DataSourceType.get_name(data_source)}")
        else:
            logger.warning(f"未知数据源: {data_source}，保持当前数据源")
    
    def get_available_data_sources(self) -> List[Dict]:
        """获取可用数据源列表"""
        return [
            {
                "type": source,
                "name": DataSourceType.get_name(source),
                "status": DataSourceType.get_status(source),
                "description": UNIFIED_DATA_SOURCES.get(source, {}).get("description", ""),
            }
            for source in DataSourceType.get_all()
        ]
    
    def get_top_mainlines(self, n: int = 10) -> List[FiveDimensionResult]:
        """获取前N条主线"""
        return self.results[:n]
    
    def get_by_dimension(self, dimension: str, n: int = 10) -> List[FiveDimensionResult]:
        """按单一维度排序获取前N条"""
        dim_map = {
            "funds": lambda x: x.funds_score.score,
            "heat": lambda x: x.heat_score.score,
            "momentum": lambda x: x.momentum_score.score,
            "policy": lambda x: x.policy_score.score,
            "leader": lambda x: x.leader_score.score,
        }
        
        if dimension not in dim_map:
            return self.results[:n]
        
        sorted_results = sorted(self.results, key=dim_map[dimension], reverse=True)
        return sorted_results[:n]


# 导出
__all__ = [
    "FiveDimensionEngine",
    "FiveDimensionResult",
    "DimensionScore",
    "DIMENSION_WEIGHTS",
    "PERIOD_WEIGHT_ADJUSTMENTS",
    "UNIFIED_DATA_SOURCES",
    "DataSourceType",
]

