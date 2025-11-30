# -*- coding: utf-8 -*-
"""
主线识别引擎抽象基类
==================

定义主线识别的通用接口，支持A股、美股等多市场扩展。

设计理念：
1. 不仅识别当下热点，更要具备前瞻性
2. 三层分析框架：宏观前瞻 → 中观验证 → 微观确认
3. 政策+资金+产业 多维度综合判断
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class MainlineStage(Enum):
    """主线生命周期阶段"""
    EMERGING = "emerging"       # 启动期 - 政策信号出现，机构开始布局
    GROWING = "growing"         # 成长期 - 资金持续流入，业绩开始兑现
    MATURE = "mature"           # 成熟期 - 共识形成，估值较高
    DECLINING = "declining"     # 衰退期 - 资金撤离，预期下修


class MainlineType(Enum):
    """主线类型"""
    POLICY = "policy"           # 政策驱动型
    INDUSTRY = "industry"       # 产业趋势型
    EVENT = "event"             # 事件驱动型
    CYCLE = "cycle"             # 周期轮动型
    THEME = "theme"             # 主题概念型


@dataclass
class Catalyst:
    """催化剂"""
    name: str
    date: Optional[str]         # 预期日期
    probability: float          # 发生概率 0-1
    impact: str                 # high/medium/low
    description: str
    source: str                 # 信息来源


@dataclass
class Risk:
    """风险因素"""
    name: str
    level: str                  # high/medium/low
    probability: float          # 发生概率 0-1
    description: str
    mitigation: str             # 应对措施


@dataclass
class MainlineScore:
    """主线评分"""
    total_score: float          # 综合得分 0-100
    
    # 分项得分
    policy_score: float         # 政策支持度 0-100
    capital_score: float        # 资金认可度 0-100
    industry_score: float       # 产业景气度 0-100
    timing_score: float         # 时机成熟度 0-100
    risk_score: float           # 风险可控度 0-100
    
    # 前瞻性得分
    foresight_score: float      # 前瞻性评分 0-100
    
    def to_dict(self) -> dict:
        return {
            "total_score": self.total_score,
            "policy_score": self.policy_score,
            "capital_score": self.capital_score,
            "industry_score": self.industry_score,
            "timing_score": self.timing_score,
            "risk_score": self.risk_score,
            "foresight_score": self.foresight_score,
        }


@dataclass
class Mainline:
    """主线对象"""
    id: str
    name: str
    description: str
    mainline_type: MainlineType
    stage: MainlineStage
    
    # 评分
    score: MainlineScore
    
    # 相关信息
    sectors: List[str]          # 相关板块
    stocks: List[str]           # 龙头股票
    catalysts: List[Catalyst]   # 催化剂列表
    risks: List[Risk]           # 风险列表
    
    # 时间信息
    start_date: Optional[str]   # 启动日期
    peak_date: Optional[str]    # 预计高峰
    
    # 投资建议
    recommendation: str         # strong_buy/buy/hold/reduce/avoid
    position_suggestion: float  # 建议仓位 0-1
    
    # 元数据
    created_at: str
    updated_at: str
    data_sources: List[str]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.mainline_type.value,
            "stage": self.stage.value,
            "score": self.score.to_dict(),
            "sectors": self.sectors,
            "stocks": self.stocks,
            "catalysts": [c.__dict__ for c in self.catalysts],
            "risks": [r.__dict__ for r in self.risks],
            "start_date": self.start_date,
            "peak_date": self.peak_date,
            "recommendation": self.recommendation,
            "position_suggestion": self.position_suggestion,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class BaseMainlineEngine(ABC):
    """
    主线识别引擎抽象基类
    
    三层分析框架：
    1. 宏观前瞻（6-12个月）- 政策周期、经济周期、产业趋势
    2. 中观验证（1-3个月）- 行业景气、资金流向、催化剂
    3. 微观确认（1-4周）- 技术形态、龙头表现、市场情绪
    """
    
    def __init__(self, market_type: str):
        self.market_type = market_type
        self._mainlines: Dict[str, Mainline] = {}
    
    # ============================================================
    # 第一层：宏观前瞻分析（6-12个月视角）
    # ============================================================
    
    @abstractmethod
    def analyze_policy_cycle(self) -> Dict:
        """
        分析政策周期
        
        返回:
            - current_phase: 当前政策周期阶段
            - key_policies: 重点政策方向
            - benefited_sectors: 受益板块
            - policy_calendar: 未来政策日历
        """
        pass
    
    @abstractmethod
    def analyze_economic_cycle(self) -> Dict:
        """
        分析经济周期
        
        返回:
            - current_phase: 复苏/过热/滞胀/衰退
            - leading_indicators: 领先指标
            - sector_rotation: 板块轮动建议
        """
        pass
    
    @abstractmethod
    def analyze_industry_trends(self) -> List[Dict]:
        """
        分析全球产业趋势
        
        返回:
            产业趋势列表，每个包含:
            - trend_name: 趋势名称
            - maturity: 成熟度
            - local_opportunities: 本地市场机会
        """
        pass
    
    # ============================================================
    # 第二层：中观验证分析（1-3个月视角）
    # ============================================================
    
    @abstractmethod
    def analyze_sector_prosperity(self, sector: str) -> Dict:
        """
        分析行业景气度
        
        返回:
            - prosperity_index: 景气指数
            - trend: 趋势方向
            - key_indicators: 关键指标
        """
        pass
    
    @abstractmethod
    def analyze_institutional_flow(self) -> Dict:
        """
        分析机构资金流向
        
        返回:
            - net_inflow_sectors: 净流入板块
            - net_outflow_sectors: 净流出板块
            - institution_positions: 机构持仓变化
        """
        pass
    
    @abstractmethod
    def get_catalyst_calendar(self, days: int = 90) -> List[Catalyst]:
        """
        获取催化剂日历
        
        参数:
            days: 未来天数
        
        返回:
            催化剂列表
        """
        pass
    
    # ============================================================
    # 第三层：微观确认分析（1-4周视角）
    # ============================================================
    
    @abstractmethod
    def analyze_sector_technicals(self, sector: str) -> Dict:
        """
        分析板块技术形态
        
        返回:
            - pattern: 形态（突破/蓄势/调整）
            - strength: 强度
            - support_resistance: 支撑阻力位
        """
        pass
    
    @abstractmethod
    def analyze_leader_stocks(self, sector: str) -> List[Dict]:
        """
        分析龙头股表现
        
        返回:
            龙头股列表，每个包含:
            - symbol: 代码
            - name: 名称
            - role: 领涨/跟涨/滞涨
            - score: 龙头得分
        """
        pass
    
    @abstractmethod
    def analyze_market_sentiment(self) -> Dict:
        """
        分析市场情绪
        
        返回:
            - sentiment_index: 情绪指数
            - fear_greed: 恐惧/贪婪
            - indicators: 情绪指标
        """
        pass
    
    # ============================================================
    # 综合分析
    # ============================================================
    
    def discover_mainlines(self, 
                          include_emerging: bool = True,
                          min_score: float = 60) -> List[Mainline]:
        """
        发现投资主线
        
        参数:
            include_emerging: 是否包含启动期主线
            min_score: 最低得分阈值
        
        返回:
            主线列表
        """
        mainlines = []
        
        # 1. 宏观前瞻分析
        policy_analysis = self.analyze_policy_cycle()
        economic_analysis = self.analyze_economic_cycle()
        industry_trends = self.analyze_industry_trends()
        
        # 2. 中观验证
        institutional_flow = self.analyze_institutional_flow()
        catalysts = self.get_catalyst_calendar()
        
        # 3. 综合生成主线
        mainlines = self._generate_mainlines(
            policy_analysis,
            economic_analysis,
            industry_trends,
            institutional_flow,
            catalysts
        )
        
        # 4. 过滤
        if not include_emerging:
            mainlines = [m for m in mainlines if m.stage != MainlineStage.EMERGING]
        
        mainlines = [m for m in mainlines if m.score.total_score >= min_score]
        
        # 5. 排序
        mainlines.sort(key=lambda m: m.score.total_score, reverse=True)
        
        return mainlines
    
    @abstractmethod
    def _generate_mainlines(self,
                           policy_analysis: Dict,
                           economic_analysis: Dict,
                           industry_trends: List[Dict],
                           institutional_flow: Dict,
                           catalysts: List[Catalyst]) -> List[Mainline]:
        """生成主线列表（子类实现）"""
        pass
    
    def score_mainline(self, mainline_id: str) -> MainlineScore:
        """
        计算主线得分
        
        评分权重:
        - 政策支持度: 20%
        - 资金认可度: 25%
        - 产业景气度: 20%
        - 时机成熟度: 15%
        - 风险可控度: 10%
        - 前瞻性: 10%
        """
        mainline = self._mainlines.get(mainline_id)
        if not mainline:
            raise ValueError(f"未找到主线: {mainline_id}")
        
        # 计算各项得分
        policy = self._score_policy(mainline)
        capital = self._score_capital(mainline)
        industry = self._score_industry(mainline)
        timing = self._score_timing(mainline)
        risk = self._score_risk(mainline)
        foresight = self._score_foresight(mainline)
        
        # 加权计算总分
        total = (
            policy * 0.20 +
            capital * 0.25 +
            industry * 0.20 +
            timing * 0.15 +
            risk * 0.10 +
            foresight * 0.10
        )
        
        return MainlineScore(
            total_score=total,
            policy_score=policy,
            capital_score=capital,
            industry_score=industry,
            timing_score=timing,
            risk_score=risk,
            foresight_score=foresight,
        )
    
    @abstractmethod
    def _score_policy(self, mainline: Mainline) -> float:
        """计算政策支持度得分"""
        pass
    
    @abstractmethod
    def _score_capital(self, mainline: Mainline) -> float:
        """计算资金认可度得分"""
        pass
    
    @abstractmethod
    def _score_industry(self, mainline: Mainline) -> float:
        """计算产业景气度得分"""
        pass
    
    @abstractmethod
    def _score_timing(self, mainline: Mainline) -> float:
        """计算时机成熟度得分"""
        pass
    
    @abstractmethod
    def _score_risk(self, mainline: Mainline) -> float:
        """计算风险可控度得分"""
        pass
    
    @abstractmethod
    def _score_foresight(self, mainline: Mainline) -> float:
        """计算前瞻性得分"""
        pass
    
    def get_recommendation(self, score: MainlineScore) -> str:
        """根据得分获取投资建议"""
        if score.total_score >= 85:
            return "strong_buy"
        elif score.total_score >= 70:
            return "buy"
        elif score.total_score >= 50:
            return "hold"
        elif score.total_score >= 30:
            return "reduce"
        else:
            return "avoid"


