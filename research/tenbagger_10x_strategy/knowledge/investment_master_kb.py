#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Investment Master Knowledge Base - 投资大师知识库
=================================================

基于《A股市场成长型投资者及中小机构调研报告》构建
整合林园、但斌、段永平、陈发树、葛卫东、赵建平、冯柳等大师的投资智慧

大师分类:
1. 长期价值派: 林园、但斌、段永平
2. 逆向抄底派: 陈发树、冯柳、赵军
3. 成长趋势派: 葛卫东、赵建平
4. 分散价值派: 徐开东、夏重阳&张素芬

Author: TRQuant Team
Date: 2025-12-27
Reference: A股市场成长型投资者及中小机构调研报告
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


class MasterStyle(Enum):
    """投资大师风格分类"""
    LONG_TERM_VALUE = "长期价值"      # 林园、但斌、段永平
    CONTRARIAN = "逆向抄底"           # 陈发树、冯柳、赵军
    GROWTH_MOMENTUM = "成长趋势"      # 葛卫东、赵建平
    DIVERSIFIED_VALUE = "分散价值"    # 徐开东、夏重阳


# ==================== 大师核心策略 ====================

@dataclass
class MasterStrategy:
    """大师策略数据类"""
    name: str
    style: MasterStyle
    core_idea: str
    holding_period: str  # 持股周期
    concentration: str   # 集中度: 高/中/低
    sectors: List[str]   # 偏好行业
    criteria: Dict[str, any]  # 选股标准
    risk_control: Dict[str, any]  # 风控规则
    success_cases: List[str]  # 成功案例


# 林园策略 - "民间股神"，8000元到20亿
LINYUAN_STRATEGY = MasterStrategy(
    name="林园",
    style=MasterStyle.LONG_TERM_VALUE,
    core_idea="垄断性消费+医药，长期持有，复利增长",
    holding_period="5-20年",
    concentration="高",
    sectors=["白酒", "医药", "消费垄断"],
    criteria={
        # 财务指标（基于林园选股核心财务指标）
        "roe_min": 15,           # ROE>15%
        "gross_margin_min": 60,  # 毛利率>60%（垄断特征）
        "net_margin_min": 20,    # 净利率>20%
        "profit_growth_min": 15, # 净利润增速>15%
        "debt_ratio_max": 40,    # 负债率<40%
        "pe_range": (15, 40),    # 合理PE范围
        # 行业特征
        "monopoly_required": True,      # 垄断性
        "consumer_brand": True,         # 消费品牌
        "pricing_power": True,          # 定价权
    },
    risk_control={
        "stop_loss": None,       # 林园不设止损，坚持长期
        "position_limit": 0.30,  # 单票最高30%
        "hold_through_bear": True,  # 穿越熊市
    },
    success_cases=["贵州茅台(25万倍)", "云南白药", "片仔癀"]
)


# 但斌策略 - "时间的玫瑰"
DANBIN_STRATEGY = MasterStrategy(
    name="但斌",
    style=MasterStyle.LONG_TERM_VALUE,
    core_idea="投资伟大公司，与时间做朋友",
    holding_period="10年+",
    concentration="高",
    sectors=["白酒", "互联网", "消费"],
    criteria={
        "market_cap_min": 500,   # 市值>500亿（大公司）
        "roe_min": 20,           # ROE>20%
        "revenue_growth_min": 10,
        "profit_growth_min": 15,
        "brand_value": True,     # 品牌价值
        "moat": True,            # 护城河
    },
    risk_control={
        "stop_loss": None,
        "position_limit": 0.40,
        "hold_through_bear": True,
    },
    success_cases=["贵州茅台", "腾讯控股"]
)


# 段永平策略 - "中国巴菲特"
DUANYONGPING_STRATEGY = MasterStrategy(
    name="段永平",
    style=MasterStyle.LONG_TERM_VALUE,
    core_idea="买股票就是买公司，10年尺度评估",
    holding_period="10年",
    concentration="极高",
    sectors=["科技", "消费", "互联网"],
    criteria={
        # 段永平20条投资原则核心
        "dcf_value": True,       # 现金流折现
        "business_model": True,  # 商业模式清晰
        "management": True,      # 管理层优秀
        "roe_min": 15,
        "profit_growth_min": 20,
        "market_leader": True,   # 行业领导者
        "undervalued": True,     # 低估值
    },
    risk_control={
        "stop_loss": None,       # "如果不想持有10年，就不要持有10天"
        "position_limit": 0.50,  # 极度集中
        "margin_of_safety": 0.30,  # 安全边际30%
    },
    success_cases=["网易(0.8→100美元，百倍)", "苹果", "茅台", "腾讯"]
)


# 陈发树策略 - "超级牛散"
CHENFASHU_STRATEGY = MasterStrategy(
    name="陈发树",
    style=MasterStyle.CONTRARIAN,
    core_idea="逆向抄底行业龙头，集中重仓",
    holding_period="3-5年",
    concentration="极高",
    sectors=["新能源", "矿业", "消费"],
    criteria={
        "market_cap_range": (100, 2000),  # 中大市值
        "industry_leader": True,          # 行业龙头
        "price_at_bottom": True,          # 价格在底部
        "sector_trough": True,            # 行业低谷期
        "profit_growth_potential": 50,    # 潜在增速>50%
    },
    risk_control={
        "stop_loss": 0.20,       # 20%止损
        "position_limit": 0.50,  # 重仓
        "entry_timing": "行业低谷",
    },
    success_cases=["紫金矿业(数百倍)", "隆基绿能(5元→73元，十倍)"]
)


# 葛卫东策略 - 期货大佬转战A股
GEWEIDONG_STRATEGY = MasterStrategy(
    name="葛卫东",
    style=MasterStyle.GROWTH_MOMENTUM,
    core_idea="科技成长龙头，长期陪伴",
    holding_period="3-5年",
    concentration="高",
    sectors=["AI", "芯片", "新能源", "高科技"],
    criteria={
        "market_cap_range": (100, 1000),
        "sector": ["AI", "芯片", "锂电", "新能源"],
        "tech_leader": True,     # 技术领先
        "profit_growth_min": 30,
        "revenue_growth_min": 30,
        "rd_ratio_min": 5,       # 研发占比>5%
    },
    risk_control={
        "stop_loss": 0.15,
        "position_limit": 0.25,
        "sector_rotation": True,
    },
    success_cases=["科大讯飞(翻倍)", "兆易创新(IPO前潜伏)"]
)


# 赵建平策略 - A股"常青树"
ZHAOJIANPING_STRATEGY = MasterStrategy(
    name="赵建平",
    style=MasterStyle.GROWTH_MOMENTUM,
    core_idea="穿越周期，分散布局成长股",
    holding_period="1-3年",
    concentration="中",
    sectors=["电子科技", "消费", "AI"],
    criteria={
        "market_cap_range": (30, 300),  # 中小市值
        "profit_growth_min": 25,
        "revenue_growth_min": 20,
        "sector_hot": True,      # 景气行业
        "new_theme": True,       # 新兴主题
    },
    risk_control={
        "stop_loss": 0.12,
        "position_limit": 0.12,  # 分散到9-10只
        "num_stocks": 10,
        "sector_diversified": True,
    },
    success_cases=["酒鬼酒(10倍)", "AI概念股(130%)", "10年270倍增长"]
)


# 冯柳策略 - 高毅资产
FENGLIU_STRATEGY = MasterStrategy(
    name="冯柳",
    style=MasterStyle.CONTRARIAN,
    core_idea="弱者体系，逆向精选，精准抄底",
    holding_period="1-2年",
    concentration="中高",
    sectors=["医药", "消费", "科技"],
    criteria={
        "price_at_low": True,    # 价格处于低位
        "fundamentals_turn": True,  # 基本面拐点
        "ignored_by_market": True,  # 被市场忽略
        "institutional_low": True,  # 机构持仓低
        "roe_min": 10,
        "profit_growth_potential": 30,
    },
    risk_control={
        "stop_loss": 0.15,
        "position_limit": 0.20,
        "contrarian_timing": True,
    },
    success_cases=["医药抄底", "亿联网络"]
)


# 赵军（淡水泉）策略
ZHAOJUN_STRATEGY = MasterStrategy(
    name="赵军(淡水泉)",
    style=MasterStyle.CONTRARIAN,
    core_idea="逆向投资，冷门淘金，自下而上",
    holding_period="1-3年",
    concentration="中",
    sectors=["多行业轮动"],
    criteria={
        "market_cap_range": (50, 500),
        "ignored_sector": True,  # 被忽略的行业
        "value_underestimate": True,
        "profit_growth_min": 15,
        "pe_below_average": True,
    },
    risk_control={
        "stop_loss": 0.10,
        "position_limit": 0.10,
        "sector_rotation": True,
        "diversified": True,
    },
    success_cases=["年化近59%业绩", "百亿私募"]
)


# 徐开东策略
XUKAIDONG_STRATEGY = MasterStrategy(
    name="徐开东",
    style=MasterStyle.DIVERSIFIED_VALUE,
    core_idea="传统行业价值洼地，低价安全边际",
    holding_period="2-5年",
    concentration="低",
    sectors=["央企改革", "传统行业", "低估值"],
    criteria={
        "pe_max": 15,            # 低PE
        "pb_max": 1.5,           # 低PB
        "dividend_yield_min": 3, # 股息率>3%
        "state_owned": True,     # 国企
        "value_revaluation": True,  # 价值重估潜力
    },
    risk_control={
        "stop_loss": 0.08,
        "position_limit": 0.08,
        "num_stocks": 15,
        "sector_diversified": True,
    },
    success_cases=["中特估概念股(60%涨幅)", "15家公司前十股东"]
)


# 夏重阳&张素芬策略
XIAZHONGYANG_STRATEGY = MasterStrategy(
    name="夏重阳&张素芬",
    style=MasterStyle.DIVERSIFIED_VALUE,
    core_idea="极度分散，长线持有，滚雪球",
    holding_period="5-10年",
    concentration="极低",
    sectors=["多行业分散"],
    criteria={
        "market_cap_range": (30, 300),
        "profit_growth_min": 10,
        "roe_min": 10,
        "stable_growth": True,
    },
    risk_control={
        "stop_loss": 0.10,
        "position_limit": 0.06,  # 极度分散
        "num_stocks": 16,
        "long_term_hold": True,
    },
    success_cases=["20万→13亿，18年", "15家公司股东"]
)


# ==================== 综合大师选股规则 ====================

class MasterSelectionRules:
    """基于大师策略的综合选股规则"""
    
    # 所有大师共识的核心指标
    CONSENSUS_CRITERIA = {
        # 基本面必备条件
        "roe_min": 10,           # 所有大师都要求ROE>10%
        "profit_growth_min": 15, # 利润增长>15%
        "revenue_growth_min": 10,# 营收增长>10%
        "debt_ratio_max": 60,    # 负债率<60%
        
        # 估值合理
        "pe_max": 50,            # PE不超过50
        "peg_max": 2.0,          # PEG<2
    }
    
    # 不同风格的附加条件
    STYLE_CRITERIA = {
        MasterStyle.LONG_TERM_VALUE: {
            "market_cap_min": 200,    # 大市值
            "roe_min": 15,
            "gross_margin_min": 40,
            "brand_value": True,
            "holding_years": 5,
        },
        MasterStyle.CONTRARIAN: {
            "price_position_max": 0.4,  # 价格位置<40%（低位）
            "institutional_ratio_max": 0.20,  # 机构持仓低
            "sector_sentiment": "bearish",  # 行业悲观
            "holding_years": 2,
        },
        MasterStyle.GROWTH_MOMENTUM: {
            "market_cap_range": (30, 500),
            "profit_growth_min": 25,
            "revenue_growth_min": 20,
            "sector": "growth",
            "holding_years": 2,
        },
        MasterStyle.DIVERSIFIED_VALUE: {
            "pe_max": 20,
            "pb_max": 2.0,
            "dividend_yield_min": 2,
            "holding_years": 3,
        },
    }
    
    @classmethod
    def get_scoring_weights(cls, style: MasterStyle) -> Dict[str, float]:
        """获取不同风格的评分权重"""
        base_weights = {
            "roe": 0.15,
            "profit_growth": 0.20,
            "revenue_growth": 0.10,
            "gross_margin": 0.10,
            "debt_ratio": 0.05,
            "pe": 0.10,
            "peg": 0.10,
            "market_cap": 0.05,
            "price_position": 0.10,
            "momentum": 0.05,
        }
        
        # 根据风格调整权重
        if style == MasterStyle.LONG_TERM_VALUE:
            base_weights["roe"] = 0.25
            base_weights["gross_margin"] = 0.15
            base_weights["momentum"] = 0.00
            
        elif style == MasterStyle.CONTRARIAN:
            base_weights["price_position"] = 0.25
            base_weights["pe"] = 0.15
            base_weights["momentum"] = 0.00
            
        elif style == MasterStyle.GROWTH_MOMENTUM:
            base_weights["profit_growth"] = 0.30
            base_weights["revenue_growth"] = 0.15
            base_weights["momentum"] = 0.10
            
        elif style == MasterStyle.DIVERSIFIED_VALUE:
            base_weights["pe"] = 0.20
            base_weights["dividend_yield"] = 0.15
            base_weights["debt_ratio"] = 0.10
            
        return base_weights


class MasterScorer:
    """大师风格评分器"""
    
    @staticmethod
    def calculate_linyuan_score(
        roe: float, gross_margin: float, net_margin: float,
        profit_growth: float, debt_ratio: float, pe: float,
        is_consumer: bool = False, is_pharma: bool = False
    ) -> float:
        """计算林园风格得分
        
        林园核心: 垄断消费+医药，高毛利，长期持有
        """
        score = 0
        
        # ROE得分 (25分)
        if roe >= 20:
            score += 25
        elif roe >= 15:
            score += 20
        elif roe >= 10:
            score += 10
            
        # 毛利率得分 (25分) - 林园强调垄断特征
        if gross_margin >= 70:
            score += 25
        elif gross_margin >= 60:
            score += 20
        elif gross_margin >= 50:
            score += 15
        elif gross_margin >= 40:
            score += 10
            
        # 净利率得分 (15分)
        if net_margin >= 25:
            score += 15
        elif net_margin >= 20:
            score += 12
        elif net_margin >= 15:
            score += 8
            
        # 利润增长得分 (15分)
        if profit_growth >= 25:
            score += 15
        elif profit_growth >= 15:
            score += 10
        elif profit_growth >= 10:
            score += 5
            
        # 负债率得分 (10分)
        if debt_ratio <= 30:
            score += 10
        elif debt_ratio <= 40:
            score += 7
        elif debt_ratio <= 50:
            score += 3
            
        # 行业加分 (10分)
        if is_consumer:
            score += 5
        if is_pharma:
            score += 5
            
        return min(score, 100)
    
    @staticmethod
    def calculate_contrarian_score(
        price_position: float, pe: float, pe_history_percentile: float,
        institutional_ratio: float, profit_growth_yoy: float,
        sector_sentiment: str = "neutral"
    ) -> float:
        """计算逆向抄底风格得分
        
        陈发树/冯柳核心: 行业低谷，价格底部，基本面拐点
        """
        score = 0
        
        # 价格位置得分 (30分) - 越低越好
        if price_position <= 0.2:
            score += 30
        elif price_position <= 0.3:
            score += 25
        elif price_position <= 0.4:
            score += 20
        elif price_position <= 0.5:
            score += 10
            
        # PE历史百分位得分 (20分)
        if pe_history_percentile <= 10:
            score += 20
        elif pe_history_percentile <= 20:
            score += 15
        elif pe_history_percentile <= 30:
            score += 10
            
        # 机构持仓得分 (15分) - 低机构更好
        if institutional_ratio <= 0.10:
            score += 15
        elif institutional_ratio <= 0.15:
            score += 12
        elif institutional_ratio <= 0.20:
            score += 8
            
        # 利润增长拐点 (20分)
        if profit_growth_yoy >= 30:
            score += 20
        elif profit_growth_yoy >= 20:
            score += 15
        elif profit_growth_yoy >= 10:
            score += 10
        elif profit_growth_yoy >= 0:
            score += 5
            
        # 行业情绪得分 (15分)
        if sector_sentiment == "bearish":
            score += 15
        elif sector_sentiment == "neutral":
            score += 8
            
        return min(score, 100)
    
    @staticmethod
    def calculate_growth_score(
        profit_growth: float, revenue_growth: float,
        market_cap: float, rd_ratio: float,
        momentum_20d: float, is_tech: bool = False
    ) -> float:
        """计算成长趋势风格得分
        
        葛卫东/赵建平核心: 高增长科技股，趋势确认
        """
        score = 0
        
        # 利润增长得分 (30分)
        if profit_growth >= 50:
            score += 30
        elif profit_growth >= 35:
            score += 25
        elif profit_growth >= 25:
            score += 20
        elif profit_growth >= 15:
            score += 10
            
        # 营收增长得分 (20分)
        if revenue_growth >= 40:
            score += 20
        elif revenue_growth >= 30:
            score += 15
        elif revenue_growth >= 20:
            score += 10
            
        # 市值得分 (15分) - 中小市值更好
        if 30 <= market_cap <= 200:
            score += 15
        elif 200 < market_cap <= 500:
            score += 10
        elif market_cap < 30:
            score += 5
            
        # 研发占比得分 (10分)
        if rd_ratio >= 10:
            score += 10
        elif rd_ratio >= 5:
            score += 7
        elif rd_ratio >= 3:
            score += 4
            
        # 动量得分 (15分)
        if momentum_20d >= 0.15:
            score += 15
        elif momentum_20d >= 0.10:
            score += 12
        elif momentum_20d >= 0.05:
            score += 8
            
        # 科技加分 (10分)
        if is_tech:
            score += 10
            
        return min(score, 100)
    
    @staticmethod
    def calculate_value_score(
        pe: float, pb: float, dividend_yield: float,
        roe: float, debt_ratio: float, is_soe: bool = False
    ) -> float:
        """计算分散价值风格得分
        
        徐开东核心: 低估值，高股息，国企改革
        """
        score = 0
        
        # PE得分 (25分)
        if pe <= 10:
            score += 25
        elif pe <= 15:
            score += 20
        elif pe <= 20:
            score += 15
        elif pe <= 25:
            score += 8
            
        # PB得分 (20分)
        if pb <= 1.0:
            score += 20
        elif pb <= 1.5:
            score += 15
        elif pb <= 2.0:
            score += 10
            
        # 股息率得分 (20分)
        if dividend_yield >= 5:
            score += 20
        elif dividend_yield >= 4:
            score += 15
        elif dividend_yield >= 3:
            score += 10
        elif dividend_yield >= 2:
            score += 5
            
        # ROE得分 (15分)
        if roe >= 15:
            score += 15
        elif roe >= 12:
            score += 10
        elif roe >= 10:
            score += 7
            
        # 负债率得分 (10分)
        if debt_ratio <= 40:
            score += 10
        elif debt_ratio <= 50:
            score += 7
        elif debt_ratio <= 60:
            score += 4
            
        # 国企加分 (10分)
        if is_soe:
            score += 10
            
        return min(score, 100)


# ==================== 综合大师策略整合器 ====================

class MasterStrategyIntegrator:
    """大师策略整合器
    
    根据市场环境选择合适的大师风格
    """
    
    # 市场环境与大师风格匹配
    REGIME_STYLE_MAPPING = {
        "BULL_EARLY": [MasterStyle.GROWTH_MOMENTUM, MasterStyle.CONTRARIAN],
        "BULL_MID": [MasterStyle.LONG_TERM_VALUE, MasterStyle.GROWTH_MOMENTUM],
        "BULL_LATE": [MasterStyle.LONG_TERM_VALUE, MasterStyle.DIVERSIFIED_VALUE],
        "BEAR_PANIC": [MasterStyle.DIVERSIFIED_VALUE],  # 熊市恐慌期少操作
        "BEAR_GRINDING": [MasterStyle.CONTRARIAN, MasterStyle.DIVERSIFIED_VALUE],
        "VOLATILE_UP": [MasterStyle.GROWTH_MOMENTUM, MasterStyle.CONTRARIAN],
        "VOLATILE_DOWN": [MasterStyle.CONTRARIAN, MasterStyle.DIVERSIFIED_VALUE],
        "VOLATILE_RANGE": [MasterStyle.DIVERSIFIED_VALUE, MasterStyle.CONTRARIAN],
    }
    
    # 每种风格的代表大师
    STYLE_MASTERS = {
        MasterStyle.LONG_TERM_VALUE: [LINYUAN_STRATEGY, DANBIN_STRATEGY, DUANYONGPING_STRATEGY],
        MasterStyle.CONTRARIAN: [CHENFASHU_STRATEGY, FENGLIU_STRATEGY, ZHAOJUN_STRATEGY],
        MasterStyle.GROWTH_MOMENTUM: [GEWEIDONG_STRATEGY, ZHAOJIANPING_STRATEGY],
        MasterStyle.DIVERSIFIED_VALUE: [XUKAIDONG_STRATEGY, XIAZHONGYANG_STRATEGY],
    }
    
    @classmethod
    def get_recommended_style(cls, market_regime: str) -> List[MasterStyle]:
        """根据市场环境获取推荐的大师风格"""
        return cls.REGIME_STYLE_MAPPING.get(market_regime, [MasterStyle.DIVERSIFIED_VALUE])
    
    @classmethod
    def get_position_limit(cls, market_regime: str, style: MasterStyle) -> float:
        """根据市场环境和风格获取仓位限制"""
        base_limits = {
            MasterStyle.LONG_TERM_VALUE: 0.30,
            MasterStyle.CONTRARIAN: 0.25,
            MasterStyle.GROWTH_MOMENTUM: 0.20,
            MasterStyle.DIVERSIFIED_VALUE: 0.10,
        }
        
        regime_multipliers = {
            "BULL_EARLY": 1.2,
            "BULL_MID": 1.0,
            "BULL_LATE": 0.8,
            "BEAR_PANIC": 0.3,
            "BEAR_GRINDING": 0.5,
            "VOLATILE_UP": 0.9,
            "VOLATILE_DOWN": 0.6,
            "VOLATILE_RANGE": 0.7,
        }
        
        base = base_limits.get(style, 0.15)
        multiplier = regime_multipliers.get(market_regime, 0.7)
        return base * multiplier
    
    @classmethod
    def calculate_integrated_score(
        cls,
        stock_data: Dict,
        market_regime: str = "VOLATILE_RANGE"
    ) -> Tuple[float, MasterStyle, str]:
        """计算综合大师得分
        
        Args:
            stock_data: 股票数据字典
            market_regime: 市场环境
            
        Returns:
            (综合得分, 最佳风格, 推荐大师)
        """
        scorer = MasterScorer()
        
        # 提取数据
        roe = stock_data.get('roe', 0)
        gross_margin = stock_data.get('gross_margin', 0)
        net_margin = stock_data.get('net_margin', 0)
        profit_growth = stock_data.get('profit_growth', 0)
        revenue_growth = stock_data.get('revenue_growth', 0)
        debt_ratio = stock_data.get('debt_ratio', 50)
        pe = stock_data.get('pe', 20)
        pb = stock_data.get('pb', 2)
        market_cap = stock_data.get('market_cap', 100)
        price_position = stock_data.get('price_position', 0.5)
        momentum_20d = stock_data.get('momentum_20d', 0)
        dividend_yield = stock_data.get('dividend_yield', 0)
        is_consumer = stock_data.get('is_consumer', False)
        is_pharma = stock_data.get('is_pharma', False)
        is_tech = stock_data.get('is_tech', False)
        is_soe = stock_data.get('is_soe', False)
        
        # 计算各风格得分
        scores = {}
        
        scores[MasterStyle.LONG_TERM_VALUE] = scorer.calculate_linyuan_score(
            roe, gross_margin, net_margin, profit_growth, debt_ratio, pe,
            is_consumer, is_pharma
        )
        
        scores[MasterStyle.CONTRARIAN] = scorer.calculate_contrarian_score(
            price_position, pe, 30, 0.15, profit_growth
        )
        
        scores[MasterStyle.GROWTH_MOMENTUM] = scorer.calculate_growth_score(
            profit_growth, revenue_growth, market_cap, 5, momentum_20d, is_tech
        )
        
        scores[MasterStyle.DIVERSIFIED_VALUE] = scorer.calculate_value_score(
            pe, pb, dividend_yield, roe, debt_ratio, is_soe
        )
        
        # 根据市场环境调整权重
        recommended_styles = cls.get_recommended_style(market_regime)
        
        # 加权计算最终得分
        if recommended_styles:
            primary_style = recommended_styles[0]
            weights = {style: 0.1 for style in MasterStyle}
            weights[primary_style] = 0.4
            if len(recommended_styles) > 1:
                weights[recommended_styles[1]] = 0.3
        else:
            weights = {style: 0.25 for style in MasterStyle}
            
        total_score = sum(scores[style] * weights[style] for style in scores)
        
        # 找出最佳风格
        best_style = max(scores, key=scores.get)
        best_master = cls.STYLE_MASTERS[best_style][0].name
        
        return total_score, best_style, best_master


# ==================== 导出 ====================

ALL_MASTER_STRATEGIES = [
    LINYUAN_STRATEGY,
    DANBIN_STRATEGY,
    DUANYONGPING_STRATEGY,
    CHENFASHU_STRATEGY,
    GEWEIDONG_STRATEGY,
    ZHAOJIANPING_STRATEGY,
    FENGLIU_STRATEGY,
    ZHAOJUN_STRATEGY,
    XUKAIDONG_STRATEGY,
    XIAZHONGYANG_STRATEGY,
]

__all__ = [
    'MasterStyle',
    'MasterStrategy',
    'MasterSelectionRules',
    'MasterScorer',
    'MasterStrategyIntegrator',
    'ALL_MASTER_STRATEGIES',
    'LINYUAN_STRATEGY',
    'DANBIN_STRATEGY',
    'DUANYONGPING_STRATEGY',
    'CHENFASHU_STRATEGY',
    'GEWEIDONG_STRATEGY',
    'ZHAOJIANPING_STRATEGY',
    'FENGLIU_STRATEGY',
    'ZHAOJUN_STRATEGY',
    'XUKAIDONG_STRATEGY',
    'XIAZHONGYANG_STRATEGY',
]







































