"""
V3.0 筛选条件选项模块
=====================

专为A股设计的筛选条件系统，考虑以下特征:

A股特有现象:
1. 价格脱离基本面 - 炒作、题材、情绪驱动
2. 涨跌停板机制 - ±10%/20%限制
3. T+1交易制度 - 次日才能卖出
4. 政策市特点 - 政策导向明显
5. 游资与机构博弈 - 短线vs长线

提供以下筛选风格:
1. 保守型 (Conservative) - 稳健，重基本面
2. 平衡型 (Balanced) - 均衡，基本面+技术面
3. 激进型 (Aggressive) - 进取，重题材+动量
4. 趋势型 (Trend) - 跟随趋势，重技术
5. 事件驱动型 (Event) - 关注催化剂

每种风格可自定义参数，支持回测优化
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ 枚举定义 ============

class FilterStyle(Enum):
    """筛选风格"""
    CONSERVATIVE = "conservative"   # 保守型
    BALANCED = "balanced"          # 平衡型
    AGGRESSIVE = "aggressive"      # 激进型
    TREND = "trend"               # 趋势型
    EVENT = "event"               # 事件驱动型


class MarketCondition(Enum):
    """市场状态"""
    BULL = "bull"          # 牛市
    BEAR = "bear"          # 熊市
    VOLATILE = "volatile"  # 震荡市


# ============ 筛选条件数据结构 ============

@dataclass
class FundamentalFilterV3:
    """基本面筛选条件"""
    
    # 市值范围 (亿元)
    min_market_cap: float = 30.0
    max_market_cap: float = 500.0
    
    # 盈利能力
    min_roe: float = 0.10          # 最低ROE
    min_gross_margin: float = 0.20  # 最低毛利率
    min_net_margin: float = 0.05    # 最低净利率
    
    # 成长性
    min_revenue_growth: float = 0.10   # 营收增速
    min_profit_growth: float = 0.15    # 净利润增速
    max_profit_growth: float = 5.0     # 排除一次性暴增
    
    # 估值
    max_pe: float = 50.0           # 最高PE
    max_peg: float = 2.0           # 最高PEG
    
    # 财务健康
    max_debt_ratio: float = 0.60   # 最高资产负债率
    
    def to_dict(self) -> Dict:
        return {
            "min_market_cap": self.min_market_cap,
            "max_market_cap": self.max_market_cap,
            "min_roe": self.min_roe,
            "min_gross_margin": self.min_gross_margin,
            "min_net_margin": self.min_net_margin,
            "min_revenue_growth": self.min_revenue_growth,
            "min_profit_growth": self.min_profit_growth,
            "max_profit_growth": self.max_profit_growth,
            "max_pe": self.max_pe,
            "max_peg": self.max_peg,
            "max_debt_ratio": self.max_debt_ratio,
        }


@dataclass
class TechnicalFilterV3:
    """技术面筛选条件"""
    
    # 价格动量
    min_mom_5d: float = -0.05      # 5日最低涨幅
    min_mom_20d: float = 0.0       # 20日最低涨幅
    max_mom_5d: float = 0.20       # 5日最高涨幅 (排除暴涨)
    
    # 价格位置
    min_price_pos_60d: float = 0.20  # 60日价格位置最低
    max_price_pos_60d: float = 0.85  # 60日价格位置最高
    
    # 成交量
    min_vol_ratio: float = 0.8     # 最低量比
    max_vol_ratio: float = 5.0     # 最高量比 (排除异常)
    
    # 均线
    require_ma_golden_cross: bool = False  # 是否要求金叉
    above_ma20: bool = True        # 是否要求站上20日均线
    above_ma60: bool = False       # 是否要求站上60日均线
    
    # RSI
    min_rsi: float = 30.0          # 最低RSI
    max_rsi: float = 80.0          # 最高RSI
    
    def to_dict(self) -> Dict:
        return {
            "min_mom_5d": self.min_mom_5d,
            "min_mom_20d": self.min_mom_20d,
            "max_mom_5d": self.max_mom_5d,
            "min_price_pos_60d": self.min_price_pos_60d,
            "max_price_pos_60d": self.max_price_pos_60d,
            "min_vol_ratio": self.min_vol_ratio,
            "max_vol_ratio": self.max_vol_ratio,
            "require_ma_golden_cross": self.require_ma_golden_cross,
            "above_ma20": self.above_ma20,
            "above_ma60": self.above_ma60,
            "min_rsi": self.min_rsi,
            "max_rsi": self.max_rsi,
        }


@dataclass
class CatalystFilterV3:
    """催化剂/事件筛选条件"""
    
    # 主线热度
    require_hot_industry: bool = False      # 是否要求热门行业
    min_industry_score: float = 50.0        # 行业最低得分
    
    # 资金流向
    require_net_inflow: bool = False        # 是否要求净流入
    min_net_inflow: float = 0.0             # 最低净流入(亿)
    
    # 北向资金
    require_north_inflow: bool = False      # 是否要求北向流入
    min_north_inflow: float = 0.0           # 最低北向流入(亿)
    
    # 连板/涨停
    min_limit_up_count: int = 0             # 20日最低涨停次数
    max_limit_up_count: int = 10            # 20日最高涨停次数
    
    def to_dict(self) -> Dict:
        return {
            "require_hot_industry": self.require_hot_industry,
            "min_industry_score": self.min_industry_score,
            "require_net_inflow": self.require_net_inflow,
            "min_net_inflow": self.min_net_inflow,
            "require_north_inflow": self.require_north_inflow,
            "min_north_inflow": self.min_north_inflow,
            "min_limit_up_count": self.min_limit_up_count,
            "max_limit_up_count": self.max_limit_up_count,
        }


@dataclass
class RiskFilterV3:
    """风控筛选条件"""
    
    # 排除行业
    exclude_industries: List[str] = field(default_factory=lambda: [
        "有色金属", "钢铁", "采掘", "建筑材料",
        "房地产", "银行", "非银金融", "公用事业",
    ])
    
    # ST/退市风险
    exclude_st: bool = True
    exclude_suspend: bool = True
    
    # 上市时间
    min_list_days: int = 60        # 最低上市天数
    
    # 流动性
    min_turnover: float = 0.01     # 最低换手率
    min_avg_amount: float = 5000   # 最低日均成交额(万)
    
    def to_dict(self) -> Dict:
        return {
            "exclude_industries": self.exclude_industries,
            "exclude_st": self.exclude_st,
            "exclude_suspend": self.exclude_suspend,
            "min_list_days": self.min_list_days,
            "min_turnover": self.min_turnover,
            "min_avg_amount": self.min_avg_amount,
        }


@dataclass
class FilterOptionsV3:
    """
    V3.0 完整筛选选项
    
    包含四大筛选维度：
    1. 基本面 (Fundamental)
    2. 技术面 (Technical)
    3. 催化剂 (Catalyst)
    4. 风控 (Risk)
    """
    
    style: FilterStyle = FilterStyle.BALANCED
    
    fundamental: FundamentalFilterV3 = field(default_factory=FundamentalFilterV3)
    technical: TechnicalFilterV3 = field(default_factory=TechnicalFilterV3)
    catalyst: CatalystFilterV3 = field(default_factory=CatalystFilterV3)
    risk: RiskFilterV3 = field(default_factory=RiskFilterV3)
    
    # 权重 (用于综合评分)
    weights: Dict[str, float] = field(default_factory=lambda: {
        "fundamental": 0.40,
        "technical": 0.30,
        "catalyst": 0.15,
        "risk": 0.15,
    })
    
    def to_dict(self) -> Dict:
        return {
            "style": self.style.value,
            "fundamental": self.fundamental.to_dict(),
            "technical": self.technical.to_dict(),
            "catalyst": self.catalyst.to_dict(),
            "risk": self.risk.to_dict(),
            "weights": self.weights,
        }


# ============ 预设筛选配置 ============

class FilterPresets:
    """预设筛选配置工厂"""
    
    @staticmethod
    def conservative() -> FilterOptionsV3:
        """
        保守型配置
        
        特点: 重基本面，低风险，适合价值投资
        """
        options = FilterOptionsV3(style=FilterStyle.CONSERVATIVE)
        
        # 基本面要求严格
        options.fundamental = FundamentalFilterV3(
            min_market_cap=50.0,
            max_market_cap=2000.0,
            min_roe=0.15,
            min_gross_margin=0.30,
            min_net_margin=0.10,
            min_revenue_growth=0.15,
            min_profit_growth=0.20,
            max_profit_growth=3.0,
            max_pe=30.0,
            max_peg=1.5,
            max_debt_ratio=0.50,
        )
        
        # 技术面要求宽松
        options.technical = TechnicalFilterV3(
            min_mom_5d=-0.10,
            min_mom_20d=-0.05,
            max_mom_5d=0.15,
            min_price_pos_60d=0.10,
            max_price_pos_60d=0.70,
            min_vol_ratio=0.5,
            max_vol_ratio=3.0,
            require_ma_golden_cross=False,
            above_ma20=False,
            above_ma60=True,
            min_rsi=25.0,
            max_rsi=70.0,
        )
        
        # 催化剂不要求
        options.catalyst = CatalystFilterV3(
            require_hot_industry=False,
            min_industry_score=30.0,
            require_net_inflow=False,
            require_north_inflow=False,
        )
        
        # 风控严格
        options.risk = RiskFilterV3(
            exclude_industries=[
                "有色金属", "钢铁", "采掘", "建筑材料",
                "房地产", "银行", "非银金融", "公用事业",
                "农林牧渔", "医药生物", "交通运输",
            ],
            exclude_st=True,
            exclude_suspend=True,
            min_list_days=180,
            min_turnover=0.02,
            min_avg_amount=10000,
        )
        
        # 权重偏向基本面
        options.weights = {
            "fundamental": 0.55,
            "technical": 0.15,
            "catalyst": 0.10,
            "risk": 0.20,
        }
        
        return options
    
    @staticmethod
    def balanced() -> FilterOptionsV3:
        """
        平衡型配置 (默认)
        
        特点: 基本面+技术面均衡，适合中长期投资
        注意: 条件已放宽以适应数据缺失情况
        """
        options = FilterOptionsV3(style=FilterStyle.BALANCED)
        
        # 基本面适中 (放宽条件，允许更多股票通过)
        options.fundamental = FundamentalFilterV3(
            min_market_cap=20.0,       # 放宽市值下限
            max_market_cap=800.0,      # 放宽市值上限
            min_roe=0.05,              # 放宽ROE要求
            min_gross_margin=0.10,     # 放宽毛利率要求
            min_net_margin=0.0,        # 放宽净利率要求
            min_revenue_growth=-0.10,  # 允许小幅下滑
            min_profit_growth=-0.10,   # 允许小幅下滑
            max_profit_growth=10.0,    # 放宽上限
            max_pe=80.0,               # 放宽PE上限
            max_peg=5.0,               # 放宽PEG上限
            max_debt_ratio=0.70,       # 放宽负债率
        )
        
        # 技术面适中 (放宽条件)
        options.technical = TechnicalFilterV3(
            min_mom_5d=-0.15,          # 放宽5日动量
            min_mom_20d=-0.10,         # 放宽20日动量
            max_mom_5d=0.30,           # 放宽上限
            min_price_pos_60d=0.10,    # 放宽价格位置
            max_price_pos_60d=0.95,    # 放宽上限
            min_vol_ratio=0.5,         # 放宽量比
            max_vol_ratio=8.0,         # 放宽上限
            require_ma_golden_cross=False,
            above_ma20=False,          # 不强制要求
            above_ma60=False,
            min_rsi=20.0,
            max_rsi=85.0,
        )
        
        # 催化剂一般
        options.catalyst = CatalystFilterV3(
            require_hot_industry=False,
            min_industry_score=30.0,   # 降低行业分数要求
            require_net_inflow=False,
            require_north_inflow=False,
            min_limit_up_count=0,
            max_limit_up_count=10,
        )
        
        # 风控标准
        options.risk = RiskFilterV3(
            exclude_industries=[
                "银行", "非银金融",  # 只排除最基本的
            ],
            exclude_st=True,
            exclude_suspend=True,
            min_list_days=30,          # 放宽上市天数
            min_turnover=0.005,        # 放宽换手率
            min_avg_amount=2000,       # 放宽成交额
        )
        
        # 权重均衡
        options.weights = {
            "fundamental": 0.40,
            "technical": 0.30,
            "catalyst": 0.15,
            "risk": 0.15,
        }
        
        return options
    
    @staticmethod
    def aggressive() -> FilterOptionsV3:
        """
        激进型配置
        
        特点: 重题材+动量，适合短线交易
        """
        options = FilterOptionsV3(style=FilterStyle.AGGRESSIVE)
        
        # 基本面宽松
        options.fundamental = FundamentalFilterV3(
            min_market_cap=20.0,
            max_market_cap=300.0,
            min_roe=0.05,
            min_gross_margin=0.10,
            min_net_margin=0.0,
            min_revenue_growth=0.0,
            min_profit_growth=-0.20,  # 允许利润下滑
            max_profit_growth=10.0,
            max_pe=100.0,
            max_peg=5.0,
            max_debt_ratio=0.70,
        )
        
        # 技术面严格
        options.technical = TechnicalFilterV3(
            min_mom_5d=0.0,           # 5日要求涨
            min_mom_20d=0.05,         # 20日涨幅>5%
            max_mom_5d=0.30,
            min_price_pos_60d=0.40,   # 相对高位
            max_price_pos_60d=0.95,
            min_vol_ratio=1.2,        # 放量
            max_vol_ratio=8.0,
            require_ma_golden_cross=True,  # 要求金叉
            above_ma20=True,
            above_ma60=False,
            min_rsi=40.0,
            max_rsi=90.0,
        )
        
        # 催化剂要求高
        options.catalyst = CatalystFilterV3(
            require_hot_industry=True,     # 要求热门行业
            min_industry_score=60.0,
            require_net_inflow=True,       # 要求净流入
            min_net_inflow=0.5,
            require_north_inflow=False,
            min_limit_up_count=0,
            max_limit_up_count=10,
        )
        
        # 风控相对宽松
        options.risk = RiskFilterV3(
            exclude_industries=[
                "银行", "非银金融", "公用事业",
            ],
            exclude_st=True,
            exclude_suspend=True,
            min_list_days=30,
            min_turnover=0.03,
            min_avg_amount=3000,
        )
        
        # 权重偏向技术和催化剂
        options.weights = {
            "fundamental": 0.15,
            "technical": 0.40,
            "catalyst": 0.35,
            "risk": 0.10,
        }
        
        return options
    
    @staticmethod
    def trend() -> FilterOptionsV3:
        """
        趋势型配置
        
        特点: 跟随趋势，适合波段操作
        """
        options = FilterOptionsV3(style=FilterStyle.TREND)
        
        # 基本面适中
        options.fundamental = FundamentalFilterV3(
            min_market_cap=30.0,
            max_market_cap=800.0,
            min_roe=0.08,
            min_gross_margin=0.15,
            min_net_margin=0.03,
            min_revenue_growth=0.05,
            min_profit_growth=0.05,
            max_profit_growth=5.0,
            max_pe=60.0,
            max_peg=3.0,
            max_debt_ratio=0.65,
        )
        
        # 技术面严格
        options.technical = TechnicalFilterV3(
            min_mom_5d=0.02,           # 短期上涨
            min_mom_20d=0.05,          # 中期上涨
            max_mom_5d=0.25,
            min_price_pos_60d=0.30,
            max_price_pos_60d=0.90,
            min_vol_ratio=1.0,
            max_vol_ratio=4.0,
            require_ma_golden_cross=False,
            above_ma20=True,           # 站上20日线
            above_ma60=True,           # 站上60日线
            min_rsi=35.0,
            max_rsi=75.0,
        )
        
        # 催化剂适中
        options.catalyst = CatalystFilterV3(
            require_hot_industry=False,
            min_industry_score=45.0,
            require_net_inflow=False,
            min_net_inflow=-0.5,
            require_north_inflow=False,
        )
        
        # 风控标准
        options.risk = RiskFilterV3(
            exclude_industries=[
                "有色金属", "钢铁", "采掘", "建筑材料",
                "房地产", "银行", "非银金融",
            ],
            exclude_st=True,
            exclude_suspend=True,
            min_list_days=90,
            min_turnover=0.02,
            min_avg_amount=5000,
        )
        
        # 权重偏向技术
        options.weights = {
            "fundamental": 0.25,
            "technical": 0.45,
            "catalyst": 0.15,
            "risk": 0.15,
        }
        
        return options
    
    @staticmethod
    def event() -> FilterOptionsV3:
        """
        事件驱动型配置
        
        特点: 关注催化剂，适合事件驱动策略
        """
        options = FilterOptionsV3(style=FilterStyle.EVENT)
        
        # 基本面宽松
        options.fundamental = FundamentalFilterV3(
            min_market_cap=20.0,
            max_market_cap=500.0,
            min_roe=0.05,
            min_gross_margin=0.10,
            min_net_margin=0.0,
            min_revenue_growth=-0.10,
            min_profit_growth=-0.30,
            max_profit_growth=10.0,
            max_pe=80.0,
            max_peg=5.0,
            max_debt_ratio=0.70,
        )
        
        # 技术面适中
        options.technical = TechnicalFilterV3(
            min_mom_5d=0.0,
            min_mom_20d=-0.05,
            max_mom_5d=0.30,
            min_price_pos_60d=0.20,
            max_price_pos_60d=0.95,
            min_vol_ratio=1.5,         # 放量
            max_vol_ratio=10.0,
            require_ma_golden_cross=False,
            above_ma20=False,
            above_ma60=False,
            min_rsi=25.0,
            max_rsi=85.0,
        )
        
        # 催化剂要求高
        options.catalyst = CatalystFilterV3(
            require_hot_industry=True,
            min_industry_score=60.0,
            require_net_inflow=True,
            min_net_inflow=1.0,
            require_north_inflow=False,
            min_limit_up_count=1,       # 至少有过涨停
            max_limit_up_count=10,
        )
        
        # 风控相对宽松
        options.risk = RiskFilterV3(
            exclude_industries=[
                "银行", "非银金融", "公用事业",
            ],
            exclude_st=True,
            exclude_suspend=True,
            min_list_days=30,
            min_turnover=0.03,
            min_avg_amount=3000,
        )
        
        # 权重偏向催化剂
        options.weights = {
            "fundamental": 0.15,
            "technical": 0.25,
            "catalyst": 0.45,
            "risk": 0.15,
        }
        
        return options
    
    @staticmethod
    def get_preset(style: FilterStyle) -> FilterOptionsV3:
        """根据风格获取预设配置"""
        preset_map = {
            FilterStyle.CONSERVATIVE: FilterPresets.conservative,
            FilterStyle.BALANCED: FilterPresets.balanced,
            FilterStyle.AGGRESSIVE: FilterPresets.aggressive,
            FilterStyle.TREND: FilterPresets.trend,
            FilterStyle.EVENT: FilterPresets.event,
        }
        return preset_map.get(style, FilterPresets.balanced)()
    
    @staticmethod
    def adapt_to_market(
        base_options: FilterOptionsV3,
        market_condition: MarketCondition,
    ) -> FilterOptionsV3:
        """
        根据市场状态调整筛选条件
        
        Args:
            base_options: 基础筛选选项
            market_condition: 市场状态
            
        Returns:
            调整后的筛选选项
        """
        import copy
        options = copy.deepcopy(base_options)
        
        if market_condition == MarketCondition.BULL:
            # 牛市: 放宽技术面，提高催化剂要求
            options.technical.min_mom_5d = 0.0
            options.technical.max_price_pos_60d = 0.95
            options.catalyst.require_hot_industry = True
            options.fundamental.max_pe = options.fundamental.max_pe * 1.5
            logger.info("FilterPresets: 牛市模式 - 放宽估值，关注动量")
            
        elif market_condition == MarketCondition.BEAR:
            # 熊市: 收紧基本面，提高风控要求
            options.fundamental.min_roe *= 1.5
            options.fundamental.max_pe *= 0.6
            options.fundamental.max_peg *= 0.6
            options.technical.max_price_pos_60d = 0.60
            options.risk.min_avg_amount *= 2
            logger.info("FilterPresets: 熊市模式 - 收紧估值，提高流动性要求")
            
        elif market_condition == MarketCondition.VOLATILE:
            # 震荡市: 收紧技术面，关注区间操作
            options.technical.min_price_pos_60d = 0.25
            options.technical.max_price_pos_60d = 0.70
            options.technical.min_rsi = 35
            options.technical.max_rsi = 65
            logger.info("FilterPresets: 震荡模式 - 关注区间，避免追高杀跌")
        
        return options


# ============ 股票筛选器 ============

class StockFilterV3:
    """
    V3.0 股票筛选器
    
    使用 FilterOptionsV3 进行多维度股票筛选
    """
    
    def __init__(self, options: FilterOptionsV3 = None):
        self.options = options or FilterPresets.balanced()
        self._filtered_stocks: List[Dict] = []
        self._filter_stats: Dict[str, int] = {}
    
    def filter_stocks(self, stocks_data: List[Dict]) -> List[Dict]:
        """
        执行筛选
        
        Args:
            stocks_data: 股票数据列表
            
        Returns:
            通过筛选的股票列表
        """
        self._filter_stats = {
            "total": len(stocks_data),
            "risk_filtered": 0,
            "fundamental_filtered": 0,
            "technical_filtered": 0,
            "catalyst_filtered": 0,
            "passed": 0,
        }
        
        filtered = []
        
        for stock in stocks_data:
            # 1. 风控筛选 (优先)
            if not self._pass_risk_filter(stock):
                self._filter_stats["risk_filtered"] += 1
                continue
            
            # 2. 基本面筛选
            if not self._pass_fundamental_filter(stock):
                self._filter_stats["fundamental_filtered"] += 1
                continue
            
            # 3. 技术面筛选
            if not self._pass_technical_filter(stock):
                self._filter_stats["technical_filtered"] += 1
                continue
            
            # 4. 催化剂筛选
            if not self._pass_catalyst_filter(stock):
                self._filter_stats["catalyst_filtered"] += 1
                continue
            
            filtered.append(stock)
        
        self._filter_stats["passed"] = len(filtered)
        self._filtered_stocks = filtered
        
        logger.info(f"StockFilterV3: 筛选完成 - {self._filter_stats}")
        
        return filtered
    
    def _pass_risk_filter(self, stock: Dict) -> bool:
        """风控筛选"""
        r = self.options.risk
        
        # ST/退市风险
        if r.exclude_st:
            name = stock.get("name", "")
            if name and ("ST" in name or "退" in name):
                return False
        
        # 停牌
        if r.exclude_suspend and stock.get("is_suspended", False):
            return False
        
        # 行业排除 (只有当有行业信息时才过滤)
        industry = stock.get("industry", "")
        if industry and industry in r.exclude_industries:
            return False
        
        # 上市天数 (如果没有数据，默认通过)
        list_days = stock.get("list_days")
        if list_days is not None and list_days < r.min_list_days:
            return False
        
        # 换手率 (如果没有数据，默认通过)
        turnover = stock.get("turnover")
        if turnover is not None and turnover < r.min_turnover:
            return False
        
        # 成交额 (如果没有数据，默认通过)
        avg_amount = stock.get("avg_amount")
        if avg_amount is not None and avg_amount < r.min_avg_amount:
            return False
        
        return True
    
    def _pass_fundamental_filter(self, stock: Dict) -> bool:
        """基本面筛选"""
        f = self.options.fundamental
        
        # 市值 (必须有)
        market_cap = stock.get("market_cap")
        if market_cap is None or market_cap == 0:
            return False
        if not (f.min_market_cap <= market_cap <= f.max_market_cap):
            return False
        
        # ROE (可选, 默认通过)
        roe = stock.get("roe")
        if roe is not None and roe < f.min_roe:
            return False
        
        # 毛利率 (可选, 默认通过)
        gross_margin = stock.get("gross_margin")
        if gross_margin is not None and gross_margin < f.min_gross_margin:
            return False
        
        # 净利率 (可选, 默认通过)
        net_margin = stock.get("net_margin")
        if net_margin is not None and net_margin < f.min_net_margin:
            return False
        
        # 营收增速 (可选, 默认通过)
        revenue_growth = stock.get("revenue_growth")
        if revenue_growth is not None and revenue_growth < f.min_revenue_growth:
            return False
        
        # 净利润增速 (可选, 默认通过)
        profit_growth = stock.get("profit_growth")
        if profit_growth is not None:
            if not (f.min_profit_growth <= profit_growth <= f.max_profit_growth):
                return False
        
        # PE (可选)
        pe = stock.get("pe_ratio")
        if pe is not None and pe > 0 and pe > f.max_pe:
            return False
        
        # PEG (可选)
        peg = stock.get("peg")
        if peg is not None and peg > 0 and peg > f.max_peg:
            return False
        
        # 资产负债率 (可选, 默认通过)
        debt_ratio = stock.get("debt_ratio")
        if debt_ratio is not None and debt_ratio > f.max_debt_ratio:
            return False
        
        return True
    
    def _pass_technical_filter(self, stock: Dict) -> bool:
        """技术面筛选"""
        t = self.options.technical
        
        # 5日动量 (可选)
        mom_5d = stock.get("mom_5d")
        if mom_5d is not None:
            if not (t.min_mom_5d <= mom_5d <= t.max_mom_5d):
                return False
        
        # 20日动量 (可选)
        mom_20d = stock.get("mom_20d")
        if mom_20d is not None:
            if mom_20d < t.min_mom_20d:
                return False
        
        # 价格位置 (可选)
        price_pos = stock.get("price_pos_60d")
        if price_pos is not None:
            if not (t.min_price_pos_60d <= price_pos <= t.max_price_pos_60d):
                return False
        
        # 量比 (可选)
        vol_ratio = stock.get("vol_ratio")
        if vol_ratio is not None:
            if not (t.min_vol_ratio <= vol_ratio <= t.max_vol_ratio):
                return False
        
        # 均线 (只有当明确要求且有数据时才检查)
        if t.require_ma_golden_cross:
            ma_cross = stock.get("ma_golden_cross")
            if ma_cross is not None and not ma_cross:
                return False
        
        if t.above_ma20:
            above_ma = stock.get("above_ma20")
            if above_ma is not None and not above_ma:
                return False
        
        if t.above_ma60:
            above_ma = stock.get("above_ma60")
            if above_ma is not None and not above_ma:
                return False
        
        # RSI (可选)
        rsi = stock.get("rsi")
        if rsi is not None:
            if not (t.min_rsi <= rsi <= t.max_rsi):
                return False
        
        return True
    
    def _pass_catalyst_filter(self, stock: Dict) -> bool:
        """催化剂筛选"""
        c = self.options.catalyst
        
        # 热门行业
        if c.require_hot_industry:
            if not stock.get("is_hot_industry", False):
                return False
        
        # 行业得分
        industry_score = stock.get("industry_score", 50)
        if industry_score < c.min_industry_score:
            return False
        
        # 净流入
        if c.require_net_inflow:
            net_inflow = stock.get("net_inflow", 0)
            if net_inflow < c.min_net_inflow:
                return False
        
        # 北向资金
        if c.require_north_inflow:
            north_flow = stock.get("north_flow", 0)
            if north_flow < c.min_north_inflow:
                return False
        
        # 涨停次数
        limit_up_count = stock.get("limit_up_count_20d", 0)
        if not (c.min_limit_up_count <= limit_up_count <= c.max_limit_up_count):
            return False
        
        return True
    
    def get_filter_stats(self) -> Dict:
        """获取筛选统计"""
        return self._filter_stats
    
    def get_summary(self) -> str:
        """获取筛选摘要"""
        stats = self._filter_stats
        
        return f"""
📊 筛选结果摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

筛选风格: {self.options.style.value}

📈 统计:
   • 输入股票: {stats.get('total', 0)} 只
   • 风控淘汰: {stats.get('risk_filtered', 0)} 只
   • 基本面淘汰: {stats.get('fundamental_filtered', 0)} 只
   • 技术面淘汰: {stats.get('technical_filtered', 0)} 只
   • 催化剂淘汰: {stats.get('catalyst_filtered', 0)} 只
   • 通过筛选: {stats.get('passed', 0)} 只

📊 通过率: {stats.get('passed', 0) / max(stats.get('total', 1), 1) * 100:.1f}%
""".strip()


# ============ 便捷函数 ============

def filter_stocks(
    stocks_data: List[Dict],
    style: FilterStyle = FilterStyle.BALANCED,
    market_condition: MarketCondition = None,
) -> List[Dict]:
    """
    便捷函数：筛选股票
    
    Args:
        stocks_data: 股票数据列表
        style: 筛选风格
        market_condition: 市场状态 (可选)
        
    Returns:
        通过筛选的股票列表
    """
    options = FilterPresets.get_preset(style)
    
    if market_condition:
        options = FilterPresets.adapt_to_market(options, market_condition)
    
    filter_v3 = StockFilterV3(options)
    return filter_v3.filter_stocks(stocks_data)


def get_filter_options(style: FilterStyle) -> FilterOptionsV3:
    """
    便捷函数：获取筛选选项
    """
    return FilterPresets.get_preset(style)
