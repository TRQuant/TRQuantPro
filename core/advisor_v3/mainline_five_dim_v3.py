"""
V3.0 五维主线识别模块
=====================

整合桌面App的五维评分系统 (资金/热度/动量/政策/龙头)，提供V3专用接口。

五大维度 (来自桌面App):
1. 💰 资金维度 (25-30%) - 主力净流入、北向资金
2. 🔥 热度维度 (20%) - 涨跌幅强度、涨停板、龙虎榜
3. 📈 动量维度 (20%) - 价格动量、相对强度、成交活跃度
4. 📜 政策维度 (15-20%) - 政策关联度、事件催化、产业趋势
5. 👑 龙头维度 (15%) - 龙头涨幅、强势股数量、连板高度

信号规则:
- 买入: 总分 >= 75 (强主线，可重点配置)
- 持有: 总分 60-75 (较强主线，适当参与)
- 观察: 总分 45-60 (一般主线，观察为主)
- 卖出: 总分 < 45 (弱主线，暂不参与)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ V3 专用数据结构 ============

class MainlineSignal(Enum):
    """主线信号"""
    STRONG_BUY = "强买入"  # >= 80
    BUY = "买入"          # 65-80
    HOLD = "持有"         # 50-65
    WATCH = "观察"        # 35-50
    SELL = "卖出"         # < 35


@dataclass
class DimensionScoreV3:
    """单维度评分 (V3格式)"""
    name: str              # 维度名称
    score: float           # 0-100分
    weight: float          # 权重
    weighted_score: float  # 加权得分
    icon: str              # 图标
    color: str             # 颜色
    rank: int = 0          # 该维度排名
    factors: List[Dict] = field(default_factory=list)  # 因子详情
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "score": round(self.score, 1),
            "weight": round(self.weight * 100, 0),
            "weighted_score": round(self.weighted_score, 1),
            "icon": self.icon,
            "color": self.color,
            "rank": self.rank,
            "factors": self.factors,
        }


@dataclass
class MainlineResultV3:
    """
    V3.0 主线识别结果
    """
    # 基础信息
    name: str              # 主线名称
    mainline_type: str     # "industry" / "concept"
    code: str = ""         # 主线代码
    
    # 五维评分
    funds_score: DimensionScoreV3 = None
    heat_score: DimensionScoreV3 = None
    momentum_score: DimensionScoreV3 = None
    policy_score: DimensionScoreV3 = None
    leader_score: DimensionScoreV3 = None
    
    # 综合评分
    total_score: float = 0.0
    
    # 排名和信号
    rank: int = 0
    signal: MainlineSignal = MainlineSignal.WATCH
    signal_desc: str = ""
    
    # 原始数据
    change_pct: float = 0.0
    net_inflow: float = 0.0
    leader_stock: str = ""
    leader_change: float = 0.0
    
    # 趋势
    trend: str = "unknown"  # "rising" / "falling" / "stable"
    trend_change: float = 0.0
    
    def get_signal(self) -> MainlineSignal:
        """根据得分获取信号"""
        if self.total_score >= 80:
            return MainlineSignal.STRONG_BUY
        elif self.total_score >= 65:
            return MainlineSignal.BUY
        elif self.total_score >= 50:
            return MainlineSignal.HOLD
        elif self.total_score >= 35:
            return MainlineSignal.WATCH
        else:
            return MainlineSignal.SELL
    
    def get_radar_data(self) -> List[Dict]:
        """获取雷达图数据"""
        return [
            {"dimension": "资金", "score": self.funds_score.score if self.funds_score else 0},
            {"dimension": "热度", "score": self.heat_score.score if self.heat_score else 0},
            {"dimension": "动量", "score": self.momentum_score.score if self.momentum_score else 0},
            {"dimension": "政策", "score": self.policy_score.score if self.policy_score else 0},
            {"dimension": "龙头", "score": self.leader_score.score if self.leader_score else 0},
        ]
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "mainline_type": self.mainline_type,
            "code": self.code,
            "total_score": round(self.total_score, 1),
            "rank": self.rank,
            "signal": self.signal.value,
            "signal_desc": self.signal_desc,
            "dimensions": {
                "funds": self.funds_score.to_dict() if self.funds_score else None,
                "heat": self.heat_score.to_dict() if self.heat_score else None,
                "momentum": self.momentum_score.to_dict() if self.momentum_score else None,
                "policy": self.policy_score.to_dict() if self.policy_score else None,
                "leader": self.leader_score.to_dict() if self.leader_score else None,
            },
            "raw_data": {
                "change_pct": round(self.change_pct, 2),
                "net_inflow": round(self.net_inflow, 2),
                "leader_stock": self.leader_stock,
                "leader_change": round(self.leader_change, 2),
            },
            "trend": self.trend,
            "trend_change": round(self.trend_change, 1),
            "radar_data": self.get_radar_data(),
        }
    
    @property
    def is_strong_mainline(self) -> bool:
        """是否为强主线"""
        return self.total_score >= 65
    
    @property
    def is_investable(self) -> bool:
        """是否可投资"""
        return self.signal in [MainlineSignal.STRONG_BUY, MainlineSignal.BUY, MainlineSignal.HOLD]


class MainlineFiveDimScorerV3:
    """
    V3.0 五维主线识别器
    
    封装桌面App的 FiveDimensionEngine，提供V3专用接口
    
    特性:
    1. 统一数据源管理 (AKShare/JQData)
    2. 可配置的周期权重 (短期/中期/长期)
    3. 实时数据获取
    4. 结果缓存
    """
    
    # 五维配置 (来自桌面App)
    DIMENSION_CONFIG = {
        "funds": {
            "name": "资金维度",
            "weight": 0.30,
            "icon": "💰",
            "color": "#3B82F6",
            "factors": [
                {"name": "主力净流入排名", "weight": 0.40},
                {"name": "资金流向强度", "weight": 0.25},
                {"name": "流入强度比", "weight": 0.20},
                {"name": "北向资金", "weight": 0.15},
            ],
        },
        "heat": {
            "name": "热度维度",
            "weight": 0.20,
            "icon": "🔥",
            "color": "#EF4444",
            "factors": [
                {"name": "涨跌幅强度", "weight": 0.25},
                {"name": "资金流入强度", "weight": 0.25},
                {"name": "涨停板热度", "weight": 0.20},
                {"name": "龙虎榜活跃度", "weight": 0.15},
                {"name": "龙头股强度", "weight": 0.15},
            ],
        },
        "momentum": {
            "name": "动量维度",
            "weight": 0.20,
            "icon": "📈",
            "color": "#10B981",
            "factors": [
                {"name": "价格动量", "weight": 0.40},
                {"name": "相对强度", "weight": 0.30},
                {"name": "成交活跃度", "weight": 0.30},
            ],
        },
        "policy": {
            "name": "政策维度",
            "weight": 0.15,
            "icon": "📜",
            "color": "#8B5CF6",
            "factors": [
                {"name": "政策关联度", "weight": 0.50},
                {"name": "事件催化", "weight": 0.30},
                {"name": "产业趋势", "weight": 0.20},
            ],
        },
        "leader": {
            "name": "龙头维度",
            "weight": 0.15,
            "icon": "👑",
            "color": "#F59E0B",
            "factors": [
                {"name": "龙头涨幅", "weight": 0.50},
                {"name": "强势股数量", "weight": 0.30},
                {"name": "连板高度", "weight": 0.20},
            ],
        },
    }
    
    # 周期权重调整
    PERIOD_WEIGHTS = {
        "short": {  # 短期 (3-5日)
            "funds": 0.25, "heat": 0.30, "momentum": 0.25, "policy": 0.10, "leader": 0.10
        },
        "medium": {  # 中期 (15-30日) - 默认
            "funds": 0.30, "heat": 0.20, "momentum": 0.20, "policy": 0.15, "leader": 0.15
        },
        "long": {  # 长期 (60-180日)
            "funds": 0.35, "heat": 0.10, "momentum": 0.15, "policy": 0.25, "leader": 0.15
        },
    }
    
    def __init__(self, period: str = "medium", use_cache: bool = True):
        """
        初始化
        
        Args:
            period: 评分周期 ("short" / "medium" / "long")
            use_cache: 是否使用缓存
        """
        self.period = period
        self.use_cache = use_cache
        self._engine = None
        self._fetcher = None
        self._results: List[MainlineResultV3] = []
        self._last_update: Optional[datetime] = None
        
    def _ensure_engine(self):
        """确保引擎已初始化"""
        if self._engine is None:
            try:
                from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
                self._engine = FiveDimensionEngine()
                logger.info("MainlineFiveDimScorerV3: 引擎初始化成功")
            except Exception as e:
                logger.error(f"MainlineFiveDimScorerV3: 引擎初始化失败 - {e}")
                raise
    
    def _ensure_fetcher(self):
        """确保数据获取器已初始化"""
        if self._fetcher is None:
            try:
                from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
                self._fetcher = RealDataFetcher()
                logger.info("MainlineFiveDimScorerV3: 数据获取器初始化成功")
            except Exception as e:
                logger.error(f"MainlineFiveDimScorerV3: 数据获取器初始化失败 - {e}")
                raise
    
    def analyze(self, refresh: bool = False) -> List[MainlineResultV3]:
        """
        执行主线分析
        
        Args:
            refresh: 是否强制刷新数据
            
        Returns:
            主线评分结果列表
        """
        # 检查缓存
        if not refresh and self.use_cache and self._results:
            cache_age = datetime.now() - self._last_update if self._last_update else timedelta(hours=999)
            if cache_age < timedelta(minutes=30):
                logger.info("MainlineFiveDimScorerV3: 使用缓存数据")
                return self._results
        
        self._ensure_engine()
        self._ensure_fetcher()
        
        try:
            # 获取数据
            logger.info("MainlineFiveDimScorerV3: 正在获取数据...")
            
            sector_result = self._fetcher.fetch_sector_flow()
            sector_data = sector_result.data if sector_result.success else []
            
            concept_result = self._fetcher.fetch_concept_board()
            concept_data = concept_result.data if concept_result.success else []
            
            sentiment_result = self._fetcher.fetch_market_sentiment()
            limit_up_data = sentiment_result.data if sentiment_result.success else {}
            
            lhb_result = self._fetcher.fetch_dragon_tiger()
            lhb_data = lhb_result.data if lhb_result.success else []
            
            north_result = self._fetcher.fetch_northbound_flow()
            north_data = north_result.data if north_result.success else {}
            
            # 计算五维评分
            logger.info("MainlineFiveDimScorerV3: 正在计算五维评分...")
            raw_results = self._engine.calculate(
                sector_data=sector_data,
                concept_data=concept_data,
                limit_up_data=limit_up_data,
                lhb_data=lhb_data,
                northbound_data=north_data,
                period=self.period,
            )
            
            # 转换为V3格式
            self._results = [self._convert_to_v3(r) for r in raw_results]
            self._last_update = datetime.now()
            
            logger.info(f"MainlineFiveDimScorerV3: 分析完成，共{len(self._results)}条主线")
            
            return self._results
            
        except Exception as e:
            logger.error(f"MainlineFiveDimScorerV3: 分析失败 - {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _convert_to_v3(self, raw_result) -> MainlineResultV3:
        """将内部结果转换为V3格式"""
        
        result = MainlineResultV3(
            name=raw_result.name,
            mainline_type=raw_result.type,
            total_score=raw_result.total_score,
            rank=raw_result.rank,
            change_pct=raw_result.change_pct,
            net_inflow=raw_result.net_inflow,
            leader_stock=raw_result.leader_stock,
            leader_change=raw_result.leader_change,
            trend=raw_result.trend,
            trend_change=raw_result.trend_change,
        )
        
        # 转换各维度评分
        result.funds_score = self._convert_dimension(raw_result.funds_score)
        result.heat_score = self._convert_dimension(raw_result.heat_score)
        result.momentum_score = self._convert_dimension(raw_result.momentum_score)
        result.policy_score = self._convert_dimension(raw_result.policy_score)
        result.leader_score = self._convert_dimension(raw_result.leader_score)
        
        # 设置信号
        result.signal = result.get_signal()
        result.signal_desc = self._get_signal_desc(result.signal)
        
        return result
    
    def _convert_dimension(self, dim_score) -> DimensionScoreV3:
        """转换单维度评分"""
        return DimensionScoreV3(
            name=dim_score.name,
            score=dim_score.score,
            weight=dim_score.weight,
            weighted_score=dim_score.weighted_score,
            icon=dim_score.icon,
            color=dim_score.color,
            factors=dim_score.factors,
        )
    
    def _get_signal_desc(self, signal: MainlineSignal) -> str:
        """获取信号描述"""
        desc_map = {
            MainlineSignal.STRONG_BUY: "极强主线，可重点配置",
            MainlineSignal.BUY: "强主线，可适当参与",
            MainlineSignal.HOLD: "一般主线，持有观察",
            MainlineSignal.WATCH: "弱主线，谨慎操作",
            MainlineSignal.SELL: "极弱主线，暂不参与",
        }
        return desc_map.get(signal, "")
    
    def get_top_mainlines(self, n: int = 10) -> List[MainlineResultV3]:
        """获取前N条主线"""
        if not self._results:
            self.analyze()
        return self._results[:n]
    
    def get_strong_mainlines(self) -> List[MainlineResultV3]:
        """获取所有强主线 (score >= 65)"""
        if not self._results:
            self.analyze()
        return [r for r in self._results if r.is_strong_mainline]
    
    def get_investable_mainlines(self) -> List[MainlineResultV3]:
        """获取所有可投资主线"""
        if not self._results:
            self.analyze()
        return [r for r in self._results if r.is_investable]
    
    def get_by_dimension(self, dimension: str, n: int = 10) -> List[MainlineResultV3]:
        """
        按单一维度排序获取前N条
        
        Args:
            dimension: "funds" / "heat" / "momentum" / "policy" / "leader"
            n: 返回数量
        """
        if not self._results:
            self.analyze()
        
        dim_map = {
            "funds": lambda x: x.funds_score.score if x.funds_score else 0,
            "heat": lambda x: x.heat_score.score if x.heat_score else 0,
            "momentum": lambda x: x.momentum_score.score if x.momentum_score else 0,
            "policy": lambda x: x.policy_score.score if x.policy_score else 0,
            "leader": lambda x: x.leader_score.score if x.leader_score else 0,
        }
        
        if dimension not in dim_map:
            return self._results[:n]
        
        sorted_results = sorted(self._results, key=dim_map[dimension], reverse=True)
        return sorted_results[:n]
    
    def get_mainline_by_name(self, name: str) -> Optional[MainlineResultV3]:
        """根据名称获取主线"""
        if not self._results:
            self.analyze()
        
        for r in self._results:
            if r.name == name:
                return r
        return None
    
    def get_stocks_in_mainline(self, mainline_name: str) -> List[Dict]:
        """
        获取主线内的股票列表
        
        TODO: 实现从数据源获取主线内股票
        """
        # 占位实现
        logger.warning(f"get_stocks_in_mainline: 暂未实现 - {mainline_name}")
        return []
    
    def get_summary(self) -> str:
        """获取分析摘要"""
        if not self._results:
            return "暂无分析结果"
        
        strong_count = len([r for r in self._results if r.total_score >= 65])
        very_strong_count = len([r for r in self._results if r.total_score >= 80])
        
        top5 = self._results[:5]
        top5_text = "\n".join([
            f"   {i+1}. {r.name} ({r.total_score:.1f}分) - {r.signal.value}"
            for i, r in enumerate(top5)
        ])
        
        summary = f"""
📊 主线五维评分摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 统计:
   • 分析主线: {len(self._results)} 条
   • 极强主线(≥80): {very_strong_count} 条
   • 强主线(≥65): {strong_count} 条

🏆 Top 5 主线:
{top5_text}

💡 投资建议:
   • 可重点关注前{min(5, very_strong_count)}条极强主线
   • 可适当参与前{min(10, strong_count)}条强主线
   • 建议分散配置，单一主线不超过20%

📅 更新时间: {self._last_update.strftime('%Y-%m-%d %H:%M') if self._last_update else '未更新'}
"""
        return summary.strip()


# ============ 便捷函数 ============

def analyze_mainlines(period: str = "medium") -> List[MainlineResultV3]:
    """
    便捷函数：执行主线分析
    
    Args:
        period: 周期 ("short" / "medium" / "long")
        
    Returns:
        主线评分结果列表
    """
    scorer = MainlineFiveDimScorerV3(period=period)
    return scorer.analyze()


def get_top_mainlines(n: int = 10, period: str = "medium") -> List[MainlineResultV3]:
    """
    便捷函数：获取前N条主线
    """
    scorer = MainlineFiveDimScorerV3(period=period)
    return scorer.get_top_mainlines(n)


def get_strong_mainlines(period: str = "medium") -> List[MainlineResultV3]:
    """
    便捷函数：获取所有强主线
    """
    scorer = MainlineFiveDimScorerV3(period=period)
    return scorer.get_strong_mainlines()
