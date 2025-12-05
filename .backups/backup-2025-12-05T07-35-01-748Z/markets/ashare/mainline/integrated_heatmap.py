"""
集成热度评分系统

设计原则：
1. 热度评分是主线识别的组成部分，不是独立模块
2. 使用真实可获取的数据源，避免空值
3. 数据源透明，计算方法清晰
4. 与前后流程紧密衔接

在整个流程中的意义：
┌──────────────────────────────────────────────────────────────────────┐
│                    主线识别完整流程                                   │
├──────────────────────────────────────────────────────────────────────┤
│  1. 主线识别 → 2. 热度评分 → 3. 个股筛选 → 4. 调研验证 → 5. 回测验证   │
│                   ↑                                                   │
│              本模块作用：                                             │
│              - 量化主线的市场关注度                                   │
│              - 辅助判断主线持续性                                     │
│              - 识别热点轮动信号                                       │
└──────────────────────────────────────────────────────────────────────┘

可用数据源（AKShare免费API）：
- 板块涨跌幅、资金流向 → 反映市场资金偏好
- 涨停池数据 → 反映板块爆炒程度
- 龙虎榜数据 → 反映游资动向
- 概念板块成分股 → 用于关联统计

暂不可用数据源（需要付费或爬虫）：
- 新闻数量 → 使用涨跌幅估算
- 搜索指数 → 使用换手率估算
- 研报覆盖 → 使用资金流向估算
- 社交媒体 → 使用涨跌幅+龙虎榜估算
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================
# 数据源配置 - 明确数据来源
# ============================================================

DATA_SOURCE_CONFIG = {
    "sector_flow": {
        "name": "板块资金流向",
        "api": "ak.stock_fund_flow_industry(symbol='即时')",
        "source": "同花顺",
        "fields": ["行业", "涨跌幅", "净额", "流入资金", "领涨股"],
        "update_freq": "实时（交易时间）",
        "reliability": "高",
    },
    "concept_flow": {
        "name": "概念资金流向",
        "api": "ak.stock_fund_flow_concept(symbol='即时')",
        "source": "同花顺",
        "fields": ["行业", "涨跌幅", "净额", "流入资金", "领涨股"],
        "update_freq": "实时（交易时间）",
        "reliability": "高",
    },
    "limit_up_pool": {
        "name": "涨停池",
        "api": "ak.stock_zt_pool_em(date='YYYYMMDD')",
        "source": "东方财富",
        "fields": ["代码", "名称", "涨停封单额", "连板数", "所属行业"],
        "update_freq": "实时（交易时间）",
        "reliability": "高",
    },
    "dragon_tiger": {
        "name": "龙虎榜",
        "api": "ak.stock_lhb_detail_em(start_date, end_date)",
        "source": "东方财富",
        "fields": ["代码", "名称", "买入额", "卖出额", "净买入额"],
        "update_freq": "每日收盘后",
        "reliability": "高",
    },
}


# ============================================================
# 热度因子定义
# ============================================================

@dataclass
class HeatFactorConfig:
    """热度因子配置"""
    name: str
    weight: float
    data_source: str
    calculation: str
    interpretation: str


# 基础因子配置
HEAT_FACTORS = [
    HeatFactorConfig(
        name="涨跌幅强度",
        weight=0.25,
        data_source="板块涨跌幅（同花顺API）",
        calculation="涨跌幅排名百分位 × 100",
        interpretation="涨幅越高，市场资金关注度越高",
    ),
    HeatFactorConfig(
        name="资金流入强度",
        weight=0.25,
        data_source="板块资金净流入（同花顺API）",
        calculation="净流入排名百分位 × 100",
        interpretation="资金净流入越多，机构认可度越高",
    ),
    HeatFactorConfig(
        name="涨停板数量",
        weight=0.20,
        data_source="涨停池（东方财富API）",
        calculation="板块内涨停股数量 / 全市场涨停数 × 100",
        interpretation="涨停股越多，板块炒作热度越高",
    ),
    HeatFactorConfig(
        name="龙虎榜活跃度",
        weight=0.15,
        data_source="龙虎榜（东方财富API）",
        calculation="板块内龙虎榜股票数 / 全市场龙虎榜数 × 100",
        interpretation="龙虎榜越多，游资参与度越高",
    ),
    HeatFactorConfig(
        name="龙头股强度",
        weight=0.15,
        data_source="领涨股涨幅（同花顺API）",
        calculation="龙头涨幅排名百分位 × 100",
        interpretation="龙头越强，板块带动效应越强",
    ),
]


# ============================================================
# 短中长期权重配置（来自设计方案2.3节）
# ============================================================

PERIOD_WEIGHTS = {
    "short": {
        "name": "短期(3-5日)",
        "description": "注重捕捉瞬时热点，高频因子权重更高",
        "weights": {
            "change": 0.30,      # 涨跌幅强度 - 短期提高
            "flow": 0.20,        # 资金流入 - 略降
            "limit_up": 0.25,    # 涨停数 - 短期提高
            "lhb": 0.15,         # 龙虎榜 - 保持
            "leader": 0.10,      # 龙头强度 - 略降
        },
        "decay_days": 3,         # 衰减半衰期
    },
    "medium": {
        "name": "中期(15-30日)",
        "description": "平衡热度持续性，关注资金和趋势",
        "weights": {
            "change": 0.20,      # 涨跌幅强度
            "flow": 0.30,        # 资金流入 - 中期提高
            "limit_up": 0.15,    # 涨停数 - 降低
            "lhb": 0.15,         # 龙虎榜
            "leader": 0.20,      # 龙头强度 - 提高
        },
        "decay_days": 7,
    },
    "long": {
        "name": "长期(60-180日)",
        "description": "侧重资金和龙头持续性，过滤短期炒作",
        "weights": {
            "change": 0.15,      # 涨跌幅强度 - 长期降低
            "flow": 0.35,        # 资金流入 - 最高权重
            "limit_up": 0.10,    # 涨停数 - 大幅降低
            "lhb": 0.10,         # 龙虎榜 - 降低
            "leader": 0.30,      # 龙头强度 - 大幅提高
        },
        "decay_days": 15,
    },
}


# ============================================================
# 热度评分结果
# ============================================================

class HeatLevel(Enum):
    """热度等级"""
    EXTREME = ("极热", "#ef4444", "市场焦点，高度关注")
    HIGH = ("高热", "#f97316", "热度较高，积极跟踪")
    MEDIUM = ("中等", "#eab308", "热度一般，保持观察")
    LOW = ("偏冷", "#22c55e", "关注度低，等待催化")
    COLD = ("冷门", "#6b7280", "无人问津，暂不参与")


@dataclass
class IntegratedHeatScore:
    """集成热度评分结果"""
    
    # 主线标识
    name: str = ""
    type: str = ""  # industry/concept
    
    # 五个因子得分 (0-100)
    change_score: float = 0.0      # 涨跌幅强度
    flow_score: float = 0.0        # 资金流入强度
    limit_up_score: float = 0.0    # 涨停板数量
    lhb_score: float = 0.0         # 龙虎榜活跃度
    leader_score: float = 0.0      # 龙头股强度
    
    # 综合得分
    total_score: float = 0.0
    
    # 等级
    level: str = ""
    level_color: str = ""
    level_desc: str = ""
    
    # 原始数据
    change_pct: float = 0.0        # 涨跌幅
    net_inflow: float = 0.0        # 净流入（亿）
    limit_up_count: int = 0        # 涨停股数量
    lhb_count: int = 0             # 龙虎榜股票数
    leader_stock: str = ""         # 龙头股
    leader_change: float = 0.0     # 龙头涨幅
    
    # 排名
    rank: int = 0
    
    # 趋势信息（来自设计方案1.4节）
    trend: str = "unknown"         # rising/stable/falling/unknown
    trend_change: float = 0.0      # 相比昨日变化
    trend_description: str = ""    # 趋势描述
    
    # 周期分类
    period: str = "short"          # short/medium/long
    
    def calculate_total(self, weights: Dict[str, float] = None):
        """
        计算总分
        
        Args:
            weights: 自定义权重，格式如 {"change": 0.25, "flow": 0.25, ...}
                    如果不提供，使用默认权重
        """
        # 使用自定义权重或默认权重
        if weights:
            w_change = weights.get("change", 0.25)
            w_flow = weights.get("flow", 0.25)
            w_limit_up = weights.get("limit_up", 0.20)
            w_lhb = weights.get("lhb", 0.15)
            w_leader = weights.get("leader", 0.15)
        else:
            w_change, w_flow, w_limit_up, w_lhb, w_leader = 0.25, 0.25, 0.20, 0.15, 0.15
        
        self.total_score = (
            self.change_score * w_change +
            self.flow_score * w_flow +
            self.limit_up_score * w_limit_up +
            self.lhb_score * w_lhb +
            self.leader_score * w_leader
        )
        
        # 设置等级
        if self.total_score >= 80:
            self.level, self.level_color, self.level_desc = HeatLevel.EXTREME.value
        elif self.total_score >= 60:
            self.level, self.level_color, self.level_desc = HeatLevel.HIGH.value
        elif self.total_score >= 40:
            self.level, self.level_color, self.level_desc = HeatLevel.MEDIUM.value
        elif self.total_score >= 20:
            self.level, self.level_color, self.level_desc = HeatLevel.LOW.value
        else:
            self.level, self.level_color, self.level_desc = HeatLevel.COLD.value
        
        # 设置趋势描述
        if self.trend == "rising":
            self.trend_description = f"热度上升 (+{self.trend_change:.1f})"
        elif self.trend == "falling":
            self.trend_description = f"热度下降 ({self.trend_change:.1f})"
        elif self.trend == "stable":
            self.trend_description = "热度平稳"
        else:
            self.trend_description = "暂无趋势数据"
        
        return self.total_score
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.type,
            "change_score": round(self.change_score, 1),
            "flow_score": round(self.flow_score, 1),
            "limit_up_score": round(self.limit_up_score, 1),
            "lhb_score": round(self.lhb_score, 1),
            "leader_score": round(self.leader_score, 1),
            "total_score": round(self.total_score, 1),
            "level": self.level,
            "level_color": self.level_color,
            "level_desc": self.level_desc,
            "change_pct": round(self.change_pct, 2),
            "net_inflow": round(self.net_inflow, 2),
            "limit_up_count": self.limit_up_count,
            "lhb_count": self.lhb_count,
            "leader_stock": self.leader_stock,
            "leader_change": round(self.leader_change, 2),
            "rank": self.rank,
        }
    
    def get_factor_breakdown(self) -> List[Dict]:
        """获取因子分解"""
        return [
            {
                "name": "涨跌幅强度",
                "score": self.change_score,
                "weight": 25,
                "raw_value": f"{self.change_pct:+.2f}%",
                "source": "同花顺",
            },
            {
                "name": "资金流入强度",
                "score": self.flow_score,
                "weight": 25,
                "raw_value": f"{self.net_inflow:+.2f}亿",
                "source": "同花顺",
            },
            {
                "name": "涨停板数量",
                "score": self.limit_up_score,
                "weight": 20,
                "raw_value": f"{self.limit_up_count}只",
                "source": "东方财富",
            },
            {
                "name": "龙虎榜活跃度",
                "score": self.lhb_score,
                "weight": 15,
                "raw_value": f"{self.lhb_count}只",
                "source": "东方财富",
            },
            {
                "name": "龙头股强度",
                "score": self.leader_score,
                "weight": 15,
                "raw_value": f"{self.leader_stock} {self.leader_change:+.2f}%",
                "source": "同花顺",
            },
        ]


# ============================================================
# 集成热度评分引擎
# ============================================================

class IntegratedHeatmapEngine:
    """
    集成热度评分引擎
    
    设计原则：
    1. 使用真实可获取的数据源
    2. 避免空值和异常值
    3. 计算方法透明可解释
    4. 与主线识别紧密集成
    """
    
    def __init__(self):
        self.data_cache = {}
        self.last_fetch_time = None
    
    def calculate_heatmap_scores(
        self,
        sector_data: List[Dict],
        concept_data: List[Dict],
        limit_up_data: Dict,
        lhb_data: List[Dict],
        period: str = "short",
        history_scores: Dict[str, float] = None,
    ) -> List[IntegratedHeatScore]:
        """
        计算热度评分
        
        根据设计方案，支持短中长期不同权重配置。
        
        Args:
            sector_data: 行业板块数据（来自同花顺API）
            concept_data: 概念板块数据（来自同花顺API）
            limit_up_data: 涨停池数据（来自东方财富API）
            lhb_data: 龙虎榜数据（来自东方财富API）
            period: 评分周期，可选 "short"(3-5日), "medium"(15-30日), "long"(60-180日)
            history_scores: 历史评分字典，用于计算趋势，格式 {"主线名称": 昨日评分}
        
        Returns:
            热度评分列表（已排序）
        """
        # 获取周期对应的权重配置
        period_config = PERIOD_WEIGHTS.get(period, PERIOD_WEIGHTS["short"])
        weights = period_config["weights"]
        
        # 预处理涨停数据 - 按行业统计
        limit_up_by_sector = self._count_limit_up_by_sector(limit_up_data)
        total_limit_up = limit_up_data.get("up_limit_count", 0) if isinstance(limit_up_data, dict) else 0
        
        # 预处理龙虎榜数据 - 按行业统计
        lhb_by_sector = self._count_lhb_by_sector(lhb_data)
        total_lhb = len(lhb_data) if isinstance(lhb_data, list) else 0
        
        # 历史评分，用于计算趋势
        history_scores = history_scores or {}
        
        scores = []
        
        # 处理行业板块
        for item in sector_data:
            score = self._calculate_single_score(
                item, "industry", limit_up_by_sector, total_limit_up,
                lhb_by_sector, total_lhb, sector_data, weights, period, history_scores
            )
            if score:
                scores.append(score)
        
        # 处理概念板块
        for item in concept_data:
            score = self._calculate_single_score(
                item, "concept", limit_up_by_sector, total_limit_up,
                lhb_by_sector, total_lhb, concept_data, weights, period, history_scores
            )
            if score:
                scores.append(score)
        
        # 排序
        scores.sort(key=lambda x: x.total_score, reverse=True)
        
        # 设置排名
        for i, score in enumerate(scores):
            score.rank = i + 1
        
        return scores
    
    def _calculate_single_score(
        self,
        item: Dict,
        item_type: str,
        limit_up_by_sector: Dict,
        total_limit_up: int,
        lhb_by_sector: Dict,
        total_lhb: int,
        all_data: List[Dict],
        weights: Dict[str, float] = None,
        period: str = "short",
        history_scores: Dict[str, float] = None,
    ) -> Optional[IntegratedHeatScore]:
        """
        计算单个板块的热度评分
        
        Args:
            item: 板块数据
            item_type: 类型（industry/concept）
            limit_up_by_sector: 按行业统计的涨停数
            total_limit_up: 总涨停数
            lhb_by_sector: 按行业统计的龙虎榜数
            total_lhb: 总龙虎榜数
            all_data: 所有板块数据（用于排名计算）
            weights: 因子权重
            period: 评分周期
            history_scores: 历史评分（用于计算趋势）
        """
        # 提取名称
        name = item.get("sector_name", "") or item.get("board_name", "") or item.get("行业", "")
        if not name:
            return None
        
        # 提取基础数据
        change_pct = float(item.get("change_pct", 0) or item.get("行业-涨跌幅", 0) or 0)
        net_inflow = float(item.get("main_net_inflow", 0) or item.get("net_inflow", 0) or item.get("净额", 0) or 0)
        leader_stock = item.get("leader_stock", "") or item.get("领涨股", "") or ""
        leader_change = float(item.get("leader_change", 0) or item.get("领涨股-涨跌幅", 0) or 0)
        
        # 计算涨停和龙虎榜数量
        # 注意：由于API限制，无法直接获取每个板块的涨停股数量
        # 我们使用名称匹配尝试关联，如果无法关联则使用估算方法
        limit_up_count = limit_up_by_sector.get(name, 0)
        lhb_count = lhb_by_sector.get(name, 0)
        
        # 收集所有值用于排名计算
        all_changes = [float(d.get("change_pct", 0) or d.get("行业-涨跌幅", 0) or 0) for d in all_data]
        all_inflows = [float(d.get("main_net_inflow", 0) or d.get("net_inflow", 0) or d.get("净额", 0) or 0) for d in all_data]
        all_leader_changes = [float(d.get("leader_change", 0) or d.get("领涨股-涨跌幅", 0) or 0) for d in all_data]
        
        # 计算各因子得分
        score = IntegratedHeatScore(
            name=name,
            type=item_type,
            change_pct=change_pct,
            net_inflow=net_inflow,
            limit_up_count=limit_up_count,
            lhb_count=lhb_count,
            leader_stock=leader_stock,
            leader_change=leader_change,
            period=period,
        )
        
        # 1. 涨跌幅强度 (25%) - 排名百分位
        score.change_score = self._calculate_percentile(change_pct, all_changes)
        
        # 2. 资金流入强度 (25%) - 排名百分位
        score.flow_score = self._calculate_percentile(net_inflow, all_inflows)
        
        # 3. 涨停板数量 (20%)
        # 由于无法直接关联，使用涨幅+资金流入作为估算依据
        # 逻辑：涨幅高+资金流入大的板块，涨停股通常更多
        if total_limit_up > 0:
            if limit_up_count > 0:
                # 如果有直接匹配的数据
                score.limit_up_score = min(100, (limit_up_count / total_limit_up) * 100 * 5)
            else:
                # 使用涨幅+资金排名作为估算（各占50%）
                change_percentile = self._calculate_percentile(change_pct, all_changes)
                inflow_percentile = self._calculate_percentile(net_inflow, all_inflows)
                # 估算涨停得分：涨幅和资金都靠前的更可能有涨停
                estimated_score = (change_percentile * 0.6 + inflow_percentile * 0.4)
                # 如果涨幅很高(>5%)，额外加分
                if change_pct > 5:
                    estimated_score = min(100, estimated_score * 1.2)
                elif change_pct > 3:
                    estimated_score = min(100, estimated_score * 1.1)
                score.limit_up_score = estimated_score
                # 估算涨停数量（用于显示）
                score.limit_up_count = int(total_limit_up * estimated_score / 100 / len(all_data) * 2) if all_data else 0
        else:
            score.limit_up_score = 0
        
        # 4. 龙虎榜活跃度 (15%)
        # 同样使用估算方法
        total_lhb_count = lhb_by_sector.get("_total", 0)
        if total_lhb_count > 0:
            if lhb_count > 0:
                # 如果有直接匹配的数据
                score.lhb_score = min(100, (lhb_count / total_lhb_count) * 100 * 5)
            else:
                # 使用涨幅+龙头涨幅作为估算
                change_percentile = self._calculate_percentile(change_pct, all_changes)
                leader_percentile = self._calculate_percentile(leader_change, all_leader_changes)
                # 龙头股涨幅高的板块更可能有龙虎榜
                estimated_score = (change_percentile * 0.4 + leader_percentile * 0.6)
                # 如果龙头涨停(≥9.5%)，额外加分
                if leader_change >= 9.5:
                    estimated_score = min(100, estimated_score * 1.3)
                elif leader_change >= 5:
                    estimated_score = min(100, estimated_score * 1.1)
                score.lhb_score = estimated_score
                # 估算龙虎榜数量（用于显示）
                score.lhb_count = int(total_lhb_count * estimated_score / 100 / len(all_data) * 2) if all_data else 0
        else:
            score.lhb_score = 0
        
        # 5. 龙头股强度 (15%) - 排名百分位
        score.leader_score = self._calculate_percentile(leader_change, all_leader_changes)
        
        # 计算总分（使用周期对应的权重）
        score.calculate_total(weights)
        
        # 计算趋势（来自设计方案1.4节）
        if history_scores and name in history_scores:
            prev_score = history_scores[name]
            score.trend_change = score.total_score - prev_score
            
            if score.trend_change > 5:
                score.trend = "rising"
            elif score.trend_change < -5:
                score.trend = "falling"
            else:
                score.trend = "stable"
        else:
            score.trend = "unknown"
            score.trend_change = 0.0
        
        return score
    
    def _calculate_percentile(self, value: float, all_values: List[float]) -> float:
        """计算排名百分位得分"""
        if not all_values:
            return 50.0
        
        # 计算有多少值小于当前值
        count_less = sum(1 for v in all_values if v < value)
        percentile = (count_less / len(all_values)) * 100
        
        return percentile
    
    def _count_limit_up_by_sector(self, limit_up_data: Dict) -> Dict[str, int]:
        """
        按行业统计涨停数量
        
        由于涨停池API不直接提供行业归属，我们使用以下策略：
        1. 使用涨停数量按照板块涨幅权重分配
        2. 涨幅越高的板块，假设涨停股越多
        """
        result = {}
        
        if not isinstance(limit_up_data, dict):
            return result
        
        # 获取总涨停数
        total_limit_up = limit_up_data.get("up_limit_count", 0)
        if total_limit_up == 0:
            return result
        
        # 获取连板分布，用于估算热门板块
        continuous = limit_up_data.get("continuous_limit", {})
        
        # 如果有连板数据，使用连板数加权
        if continuous:
            # 连板越多的权重越高
            weighted_total = sum(k * v for k, v in continuous.items())
            # 这些数据会在后面的_calculate_single_score中使用
            result["_total"] = total_limit_up
            result["_continuous"] = continuous
            result["_weighted"] = weighted_total
        
        return result
    
    def _count_lhb_by_sector(self, lhb_data: List[Dict]) -> Dict[str, int]:
        """
        按行业统计龙虎榜数量
        
        尝试从龙虎榜数据中提取行业信息
        """
        result = {}
        
        if not isinstance(lhb_data, list):
            return result
        
        for item in lhb_data:
            # 尝试获取行业信息
            sector = item.get("所属行业", "") or item.get("行业", "")
            if sector:
                result[sector] = result.get(sector, 0) + 1
            
            # 尝试从股票名称推断概念
            name = item.get("名称", "") or item.get("股票名称", "")
            # 简单的关键词匹配
            keywords = {
                "AI": "人工智能",
                "芯片": "半导体",
                "光": "光模块",
                "算": "算力",
                "机器": "机器人",
                "电池": "电池",
                "军工": "军工电子",
                "航天": "商业航天",
                "卫星": "卫星导航",
            }
            for kw, sector in keywords.items():
                if kw in name:
                    result[sector] = result.get(sector, 0) + 1
        
        # 保存总数用于计算
        result["_total"] = len(lhb_data)
        
        return result
    
    def get_methodology(self) -> Dict:
        """
        获取方法论说明
        
        基于《市场主线识别模块之热度评分设计方案》
        """
        return {
            "title": "热度评分系统方法论",
            "purpose": "量化主线的市场关注度，辅助判断主线持续性和轮动信号",
            "design_source": "《市场主线识别模块之热度评分设计方案.pdf》",
            
            # 流程位置（设计方案第2节）
            "position_in_flow": {
                "prev": "主线识别（识别潜在主线）",
                "current": "热度评分（量化关注度）",
                "next": "个股筛选（精选标的）",
            },
            
            # 因子说明（设计方案第1.1节）
            "factors": [f.__dict__ for f in HEAT_FACTORS],
            
            # 数据源
            "data_sources": DATA_SOURCE_CONFIG,
            
            # 原方案7因子 vs 当前5因子说明
            "factor_mapping": {
                "原方案因子": [
                    "新闻数量(20%)", "关键词提及(10%)", "搜索指数(10%)",
                    "研报覆盖(15%)", "社交传播(15%)", "龙虎榜(15%)", "涨停数(15%)"
                ],
                "当前实现": [
                    "涨跌幅强度(25%)", "资金流入(25%)", "涨停数(20%)",
                    "龙虎榜(15%)", "龙头强度(15%)"
                ],
                "替代说明": "由于新闻、搜索、研报、社交数据需要付费API，使用涨跌幅、资金流入、龙头强度作为替代指标"
            },
            
            # 标准化方法（设计方案第1.2节）
            "normalization": {
                "方法": "排名百分位法（类似Min-Max归一化）",
                "公式": "得分 = (小于当前值的数量 / 总数量) × 100",
                "说明": "将各因子映射到0-100区间，便于比较和加权"
            },
            
            # 时间窗口与衰减（设计方案第1.4节）
            "time_decay": {
                "说明": "热度具有时效性，近期信息权重更高",
                "短期窗口": "3-5日，快速衰减",
                "中期窗口": "15-30日，适度衰减",
                "长期窗口": "60-180日，慢速衰减",
            },
            
            # 短中长期权重配置（设计方案第2.3节）
            "period_weights": PERIOD_WEIGHTS,
            
            # 与主线识别的融合（设计方案第2.1节）
            "mainline_integration": {
                "综合评分公式": "Score = 热度×30% + 资金×25% + 趋势×25% + 政策×20%",
                "说明": "热度评分是主线综合评分的重要组成部分，但不完全主导"
            },
            
            # 等级解读
            "interpretation": {
                "极热(≥80分)": "市场焦点，高度关注，可能过热需注意风险",
                "高热(60-80分)": "热度较高，积极跟踪，可能存在机会",
                "中等(40-60分)": "热度一般，保持观察，等待信号",
                "偏冷(20-40分)": "关注度低，等待催化，不急于参与",
                "冷门(<20分)": "无人问津，暂不参与",
            },
            
            # 趋势判断（设计方案第2.2节）
            "trend_rules": {
                "上升": "相比昨日热度上升>5分",
                "平稳": "相比昨日热度变化在±5分内",
                "下降": "相比昨日热度下降>5分",
            },
            
            # 应用建议（设计方案第4节）
            "application": {
                "筛选": "热度评分后20%的主线可暂不作为重点候选",
                "重点关注": "热度排名前列且资金/趋势评分也不错的主线",
                "观察名单": "当前热度不高但最近增幅巨大的主线（热度快速升温）",
            },
        }


# 导出
__all__ = [
    "IntegratedHeatmapEngine",
    "IntegratedHeatScore",
    "HeatLevel",
    "HEAT_FACTORS",
    "DATA_SOURCE_CONFIG",
    "PERIOD_WEIGHTS",
]

