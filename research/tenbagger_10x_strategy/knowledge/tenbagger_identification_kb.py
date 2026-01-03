#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tenbagger Identification Knowledge Base - 十倍股识别知识库
=========================================================

基于彼得·林奇理论和网络研究构建的十倍股识别系统：
1. 基本面特征：财务健康、高成长、低估值
2. 行业特征：高成长行业、渗透率低
3. 技术特征：突破形态、资金流入
4. 估值特征：PEG<1、市值小
5. 分阶段识别：S0-S5成长阶段

数据来源：网络研究、彼得林奇《战胜华尔街》、量化实践
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np
import pandas as pd


# ============== 十倍股成长阶段 ==============

class TenbaggerStage(Enum):
    """十倍股成长阶段"""
    S0_SEED = "S0_SEED"               # 种子期：刚起步，风险最高
    S1_EMERGENCE = "S1_EMERGENCE"      # 萌芽期：开始显露潜力
    S2_ACCELERATION = "S2_ACCELERATION" # 加速期：业绩爆发
    S3_EXPANSION = "S3_EXPANSION"      # 扩张期：市场认可
    S4_MATURITY = "S4_MATURITY"        # 成熟期：增长放缓
    S5_DECLINE = "S5_DECLINE"          # 衰退期：避免买入


# ============== 阶段特征定义 ==============

STAGE_CHARACTERISTICS = {
    TenbaggerStage.S0_SEED: {
        'description': '种子期：市值极小，尚未盈利或刚开始盈利',
        'market_cap_range': (0, 30),  # 亿元
        'revenue_growth': (-50, 50),  # 可能还在亏损
        'profit_growth': None,  # 可能无利润
        'roe_range': (-20, 10),
        'risk_level': 'extreme',
        'position_weight': 0.05,  # 极小仓位
        'hold_period': '3-5年',
        'upside_potential': '10-50倍',
        'key_indicators': ['研发投入', '专利数量', '行业空间'],
    },
    TenbaggerStage.S1_EMERGENCE: {
        'description': '萌芽期：开始盈利，业绩初现',
        'market_cap_range': (30, 100),
        'revenue_growth': (20, 100),
        'profit_growth': (0, 200),
        'roe_range': (5, 15),
        'risk_level': 'high',
        'position_weight': 0.10,
        'hold_period': '2-3年',
        'upside_potential': '5-20倍',
        'key_indicators': ['营收增速', '毛利率提升', '市场份额'],
    },
    TenbaggerStage.S2_ACCELERATION: {
        'description': '加速期：业绩爆发，最佳买入期',
        'market_cap_range': (100, 300),
        'revenue_growth': (30, 80),
        'profit_growth': (50, 150),
        'roe_range': (15, 30),
        'risk_level': 'medium',
        'position_weight': 0.25,  # 最大仓位
        'hold_period': '1-2年',
        'upside_potential': '3-10倍',
        'key_indicators': ['净利润增速', 'ROE提升', '机构持仓'],
    },
    TenbaggerStage.S3_EXPANSION: {
        'description': '扩张期：市场认可，估值提升',
        'market_cap_range': (300, 1000),
        'revenue_growth': (20, 50),
        'profit_growth': (20, 80),
        'roe_range': (20, 40),
        'risk_level': 'medium-low',
        'position_weight': 0.20,
        'hold_period': '1年',
        'upside_potential': '1.5-3倍',
        'key_indicators': ['估值水平', '行业地位', '分红能力'],
    },
    TenbaggerStage.S4_MATURITY: {
        'description': '成熟期：增长放缓，适合价值投资',
        'market_cap_range': (1000, 5000),
        'revenue_growth': (5, 20),
        'profit_growth': (5, 30),
        'roe_range': (15, 30),
        'risk_level': 'low',
        'position_weight': 0.15,
        'hold_period': '长期持有',
        'upside_potential': '1-2倍',
        'key_indicators': ['分红率', '现金流', '护城河'],
    },
    TenbaggerStage.S5_DECLINE: {
        'description': '衰退期：避免买入',
        'market_cap_range': (0, float('inf')),
        'revenue_growth': (-50, 5),
        'profit_growth': (-100, 0),
        'roe_range': (-20, 10),
        'risk_level': 'avoid',
        'position_weight': 0,
        'hold_period': '不持有',
        'upside_potential': '无',
        'key_indicators': ['债务风险', '业务萎缩'],
    },
}


# ============== 十倍股筛选条件 ==============

@dataclass
class TenbaggerCriteria:
    """十倍股筛选条件"""
    
    # === 基本面条件 ===
    # 营收增长 (必须)
    min_revenue_growth: float = 0.20  # 年增长>=20%
    
    # 净利润增长 (必须)
    min_profit_growth: float = 0.30  # 年增长>=30%
    
    # ROE (必须)
    min_roe: float = 0.15  # ROE>=15%
    
    # 毛利率 (可选但重要)
    min_gross_margin: float = 0.30  # 毛利率>=30%
    
    # 净利率 (可选)
    min_net_margin: float = 0.10  # 净利率>=10%
    
    # 资产负债率 (必须)
    max_debt_ratio: float = 0.60  # 负债率<=60%
    
    # === 估值条件 ===
    # PEG (核心指标)
    max_peg: float = 1.0  # PEG<=1 被低估
    
    # PE (可选)
    max_pe: float = 50  # PE<=50
    min_pe: float = 5   # PE>=5 (排除异常)
    
    # 市值 (重要)
    min_market_cap: float = 30   # 最小30亿
    max_market_cap: float = 500  # 最大500亿 (小市值更有潜力)
    
    # === 技术面条件 ===
    # 价格位置
    min_price_vs_52w_low: float = 0.20  # 距离52周低点至少20%
    max_price_vs_52w_high: float = 0.30 # 距离52周高点不超过30%
    
    # 动量
    min_momentum_20d: float = 0.0  # 20日动量为正
    
    # 成交量
    min_volume_ratio: float = 1.0  # 成交量高于平均


# ============== 十倍股评分系统 ==============

class TenbaggerScorer:
    """十倍股评分系统
    
    总分100分：
    - 基本面 40分
    - 成长性 30分
    - 估值 15分
    - 技术面 15分
    """
    
    WEIGHTS = {
        'fundamental': 0.40,
        'growth': 0.30,
        'valuation': 0.15,
        'technical': 0.15
    }
    
    @staticmethod
    def score_fundamental(roe: float, gross_margin: float, net_margin: float,
                          debt_ratio: float, cash_ratio: float = 0) -> Tuple[float, Dict]:
        """基本面评分 (0-100)"""
        score = 0
        details = {}
        
        # ROE评分 (40分)
        if roe >= 0.30:
            roe_score = 40
        elif roe >= 0.20:
            roe_score = 30
        elif roe >= 0.15:
            roe_score = 20
        elif roe >= 0.10:
            roe_score = 10
        else:
            roe_score = 0
        score += roe_score
        details['roe'] = roe_score
        
        # 毛利率评分 (25分)
        if gross_margin >= 0.50:
            gm_score = 25
        elif gross_margin >= 0.40:
            gm_score = 20
        elif gross_margin >= 0.30:
            gm_score = 15
        elif gross_margin >= 0.20:
            gm_score = 10
        else:
            gm_score = 0
        score += gm_score
        details['gross_margin'] = gm_score
        
        # 负债率评分 (20分) - 越低越好
        if debt_ratio <= 0.30:
            debt_score = 20
        elif debt_ratio <= 0.45:
            debt_score = 15
        elif debt_ratio <= 0.60:
            debt_score = 10
        elif debt_ratio <= 0.70:
            debt_score = 5
        else:
            debt_score = 0
        score += debt_score
        details['debt_ratio'] = debt_score
        
        # 净利率评分 (15分)
        if net_margin >= 0.20:
            nm_score = 15
        elif net_margin >= 0.15:
            nm_score = 12
        elif net_margin >= 0.10:
            nm_score = 8
        elif net_margin >= 0.05:
            nm_score = 4
        else:
            nm_score = 0
        score += nm_score
        details['net_margin'] = nm_score
        
        return score, details
    
    @staticmethod
    def score_growth(revenue_growth: float, profit_growth: float,
                     revenue_growth_3y: float = None) -> Tuple[float, Dict]:
        """成长性评分 (0-100)"""
        score = 0
        details = {}
        
        # 营收增速评分 (40分)
        if revenue_growth >= 0.50:
            rg_score = 40
        elif revenue_growth >= 0.30:
            rg_score = 30
        elif revenue_growth >= 0.20:
            rg_score = 20
        elif revenue_growth >= 0.10:
            rg_score = 10
        else:
            rg_score = 0
        score += rg_score
        details['revenue_growth'] = rg_score
        
        # 净利润增速评分 (50分) - 最重要
        if profit_growth >= 1.00:
            pg_score = 50
        elif profit_growth >= 0.50:
            pg_score = 40
        elif profit_growth >= 0.30:
            pg_score = 30
        elif profit_growth >= 0.20:
            pg_score = 20
        elif profit_growth >= 0.10:
            pg_score = 10
        else:
            pg_score = 0
        score += pg_score
        details['profit_growth'] = pg_score
        
        # 3年复合增长 (10分)
        if revenue_growth_3y is not None:
            if revenue_growth_3y >= 0.30:
                rg3_score = 10
            elif revenue_growth_3y >= 0.20:
                rg3_score = 7
            elif revenue_growth_3y >= 0.10:
                rg3_score = 4
            else:
                rg3_score = 0
            score += rg3_score
            details['revenue_growth_3y'] = rg3_score
        
        return score, details
    
    @staticmethod
    def score_valuation(peg: float, pe: float, market_cap: float) -> Tuple[float, Dict]:
        """估值评分 (0-100)"""
        score = 0
        details = {}
        
        # PEG评分 (50分) - 核心
        if peg <= 0.5:
            peg_score = 50
        elif peg <= 0.8:
            peg_score = 40
        elif peg <= 1.0:
            peg_score = 30
        elif peg <= 1.5:
            peg_score = 15
        else:
            peg_score = 0
        score += peg_score
        details['peg'] = peg_score
        
        # PE评分 (25分)
        if 10 <= pe <= 25:
            pe_score = 25
        elif 25 < pe <= 35:
            pe_score = 18
        elif 35 < pe <= 50:
            pe_score = 10
        elif 5 <= pe < 10:
            pe_score = 15
        else:
            pe_score = 0
        score += pe_score
        details['pe'] = pe_score
        
        # 市值评分 (25分) - 小市值加分
        if 30 <= market_cap <= 100:
            mc_score = 25  # 最佳
        elif 100 < market_cap <= 300:
            mc_score = 20
        elif 300 < market_cap <= 500:
            mc_score = 12
        elif 500 < market_cap <= 1000:
            mc_score = 5
        else:
            mc_score = 0
        score += mc_score
        details['market_cap'] = mc_score
        
        return score, details
    
    @staticmethod
    def score_technical(momentum_20d: float, volume_ratio: float,
                        price_position: float, macd_signal: int = 0) -> Tuple[float, Dict]:
        """技术面评分 (0-100)"""
        score = 0
        details = {}
        
        # 动量评分 (40分)
        if momentum_20d >= 0.15:
            mom_score = 40
        elif momentum_20d >= 0.08:
            mom_score = 30
        elif momentum_20d >= 0.03:
            mom_score = 20
        elif momentum_20d >= 0:
            mom_score = 10
        else:
            mom_score = 0
        score += mom_score
        details['momentum'] = mom_score
        
        # 成交量评分 (30分)
        if volume_ratio >= 2.0:
            vol_score = 30
        elif volume_ratio >= 1.5:
            vol_score = 25
        elif volume_ratio >= 1.2:
            vol_score = 20
        elif volume_ratio >= 1.0:
            vol_score = 10
        else:
            vol_score = 0
        score += vol_score
        details['volume'] = vol_score
        
        # 价格位置评分 (30分) - 不追高
        # price_position: 0=52周低点, 1=52周高点
        if 0.3 <= price_position <= 0.6:
            pos_score = 30  # 中间位置最佳
        elif 0.2 <= price_position < 0.3:
            pos_score = 25  # 偏低位
        elif 0.6 < price_position <= 0.7:
            pos_score = 20  # 偏高位
        elif price_position < 0.2:
            pos_score = 15  # 可能还在下跌
        else:
            pos_score = 0  # 太高了
        score += pos_score
        details['position'] = pos_score
        
        return score, details
    
    @classmethod
    def calculate_total_score(cls, fundamental_score: float, growth_score: float,
                              valuation_score: float, technical_score: float) -> float:
        """计算总得分"""
        total = (
            fundamental_score * cls.WEIGHTS['fundamental'] +
            growth_score * cls.WEIGHTS['growth'] +
            valuation_score * cls.WEIGHTS['valuation'] +
            technical_score * cls.WEIGHTS['technical']
        )
        return total


# ============== 十倍股识别器 ==============

class TenbaggerIdentifier:
    """十倍股识别器
    
    综合基本面、成长性、估值、技术面进行识别
    """
    
    def __init__(self, criteria: TenbaggerCriteria = None):
        self.criteria = criteria or TenbaggerCriteria()
        self.scorer = TenbaggerScorer()
    
    def identify_stage(self, market_cap: float, revenue_growth: float,
                       profit_growth: float, roe: float) -> TenbaggerStage:
        """识别所处阶段"""
        
        # 衰退期判断
        if profit_growth < 0 and revenue_growth < 0.05:
            return TenbaggerStage.S5_DECLINE
        
        # 根据市值和增速判断阶段
        if market_cap < 30:
            return TenbaggerStage.S0_SEED
        elif market_cap < 100:
            if profit_growth >= 0.50 or revenue_growth >= 0.30:
                return TenbaggerStage.S1_EMERGENCE
            else:
                return TenbaggerStage.S0_SEED
        elif market_cap < 300:
            if profit_growth >= 0.30 and roe >= 0.15:
                return TenbaggerStage.S2_ACCELERATION
            else:
                return TenbaggerStage.S1_EMERGENCE
        elif market_cap < 1000:
            if profit_growth >= 0.20:
                return TenbaggerStage.S3_EXPANSION
            else:
                return TenbaggerStage.S4_MATURITY
        else:
            if profit_growth >= 0.15:
                return TenbaggerStage.S4_MATURITY
            else:
                return TenbaggerStage.S5_DECLINE
    
    def is_potential_tenbagger(self, roe: float, gross_margin: float, net_margin: float,
                               debt_ratio: float, revenue_growth: float, profit_growth: float,
                               peg: float, pe: float, market_cap: float,
                               momentum_20d: float, volume_ratio: float,
                               price_position: float) -> Tuple[bool, float, TenbaggerStage, Dict]:
        """判断是否为潜在十倍股
        
        Returns:
            (是否符合, 总得分, 阶段, 详细得分)
        """
        # 计算各维度得分
        fund_score, fund_detail = self.scorer.score_fundamental(
            roe, gross_margin, net_margin, debt_ratio
        )
        growth_score, growth_detail = self.scorer.score_growth(
            revenue_growth, profit_growth
        )
        val_score, val_detail = self.scorer.score_valuation(
            peg, pe, market_cap
        )
        tech_score, tech_detail = self.scorer.score_technical(
            momentum_20d, volume_ratio, price_position
        )
        
        # 总分
        total_score = self.scorer.calculate_total_score(
            fund_score, growth_score, val_score, tech_score
        )
        
        # 识别阶段
        stage = self.identify_stage(market_cap, revenue_growth, profit_growth, roe)
        
        # 详细得分
        details = {
            'fundamental': {'score': fund_score, 'detail': fund_detail},
            'growth': {'score': growth_score, 'detail': growth_detail},
            'valuation': {'score': val_score, 'detail': val_detail},
            'technical': {'score': tech_score, 'detail': tech_detail},
            'total': total_score,
            'stage': stage.value
        }
        
        # 判断是否符合
        # 基本条件：总分>=60, 成长性>=40, 基本面>=30
        is_potential = (
            total_score >= 60 and
            growth_score >= 40 and
            fund_score >= 30 and
            stage not in [TenbaggerStage.S5_DECLINE, TenbaggerStage.S4_MATURITY]
        )
        
        return is_potential, total_score, stage, details


# ============== 根据阶段的持仓策略 ==============

STAGE_POSITION_STRATEGY = {
    TenbaggerStage.S0_SEED: {
        'max_position': 0.05,
        'stop_loss': 0.20,
        'take_profit': 1.00,  # 翻倍才考虑止盈
        'hold_strategy': '长期持有，等待爆发',
        'rebalance_freq': 60,  # 季度调仓
    },
    TenbaggerStage.S1_EMERGENCE: {
        'max_position': 0.10,
        'stop_loss': 0.15,
        'take_profit': 0.80,
        'hold_strategy': '中长期持有',
        'rebalance_freq': 30,
    },
    TenbaggerStage.S2_ACCELERATION: {
        'max_position': 0.25,  # 最大仓位
        'stop_loss': 0.12,
        'take_profit': 0.50,
        'hold_strategy': '重点持仓，追踪业绩',
        'rebalance_freq': 15,
    },
    TenbaggerStage.S3_EXPANSION: {
        'max_position': 0.20,
        'stop_loss': 0.10,
        'take_profit': 0.35,
        'hold_strategy': '逐步兑现利润',
        'rebalance_freq': 10,
    },
    TenbaggerStage.S4_MATURITY: {
        'max_position': 0.15,
        'stop_loss': 0.08,
        'take_profit': 0.25,
        'hold_strategy': '价值投资，长期分红',
        'rebalance_freq': 20,
    },
    TenbaggerStage.S5_DECLINE: {
        'max_position': 0,
        'stop_loss': 0,
        'take_profit': 0,
        'hold_strategy': '不持有',
        'rebalance_freq': 0,
    },
}


# ============== 导出 ==============

__all__ = [
    'TenbaggerStage',
    'STAGE_CHARACTERISTICS',
    'TenbaggerCriteria',
    'TenbaggerScorer',
    'TenbaggerIdentifier',
    'STAGE_POSITION_STRATEGY'
]







































