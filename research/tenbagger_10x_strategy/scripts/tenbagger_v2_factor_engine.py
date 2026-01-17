#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 因子计算引擎
=====================================

因子体系:
1. 核心因子 (保留验证有效的6因子, 55.3%回测)
   - 成长因子 (30%): 营收增速、利润增速
   - 质量因子 (25%): ROE、ROA
   - 估值因子 (15%): PE、PB、PEG
   - 动量因子 (15%): 20d/60d动量
   - 规模因子 (10%): 市值30-150亿
   - 技术因子 (5%): 均线多头

2. 创新因子 (新增4因子)
   - 营收加速度 (10%): 本期增速-上期增速
   - 资金流向 (8%): 主力净流入/成交额
   - 北向资金 (5%): 北向持仓变化率
   - 舆情热度 (2%): AkShare舆情指数

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_factor_engine.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 因子权重配置
# ============================================================

@dataclass
class FactorWeights:
    """因子权重配置 - 基于历史10倍股特征优化"""
    
    # 核心因子权重 (已验证有效)
    growth: float = 0.30      # 成长因子
    quality: float = 0.25     # 质量因子
    valuation: float = 0.15   # 估值因子
    momentum: float = 0.15    # 动量因子
    scale: float = 0.10       # 规模因子
    technical: float = 0.05   # 技术因子
    
    # 创新因子权重 (新增)
    acceleration: float = 0.10  # 成长加速度
    money_flow: float = 0.08    # 资金流向
    north_money: float = 0.05   # 北向资金
    sentiment: float = 0.02     # 舆情热度
    
    def get_core_weights(self) -> Dict[str, float]:
        """获取核心因子权重"""
        return {
            'growth': self.growth,
            'quality': self.quality,
            'valuation': self.valuation,
            'momentum': self.momentum,
            'scale': self.scale,
            'technical': self.technical
        }
    
    def get_new_weights(self) -> Dict[str, float]:
        """获取新增因子权重"""
        return {
            'acceleration': self.acceleration,
            'money_flow': self.money_flow,
            'north_money': self.north_money,
            'sentiment': self.sentiment
        }
    
    def normalize(self):
        """归一化权重"""
        total = sum(self.get_core_weights().values()) + sum(self.get_new_weights().values())
        if total != 1.0:
            factor = 1.0 / total
            self.growth *= factor
            self.quality *= factor
            self.valuation *= factor
            self.momentum *= factor
            self.scale *= factor
            self.technical *= factor
            self.acceleration *= factor
            self.money_flow *= factor
            self.north_money *= factor
            self.sentiment *= factor


# ============================================================
# 因子评分器
# ============================================================

class FactorScorer:
    """因子评分器 - 基于历史10倍股特征"""
    
    # 历史10倍股特征阈值（来自东吴证券研究+数据挖掘）
    TENBAGGER_FEATURES = {
        'market_cap_optimal': (30, 150),      # 最优市值区间（亿）
        'market_cap_range': (20, 1000),       # 可接受市值范围
        'pe_optimal': (20, 40),               # 最优PE区间
        'pe_range': (5, 100),                 # 可接受PE范围
        'roe_min': 13,                        # ROE下限
        'revenue_growth_min': 30,             # 营收增速下限
        'profit_growth_min': 50,              # 利润增速下限
        'gross_margin_min': 30,               # 毛利率下限
    }
    
    @classmethod
    def score_growth(cls, revenue_growth: float, profit_growth: float) -> Tuple[float, Dict]:
        """
        成长因子评分 (0-100)
        
        评分逻辑:
        - 营收增速: >50% 满分50分, >30% 40分, >15% 25分
        - 利润增速: >80% 满分50分, >50% 40分, >20% 25分
        """
        score = 0
        details = {}
        
        # 营收增速评分 (50分)
        if revenue_growth >= 50:
            rev_score = 50
        elif revenue_growth >= 30:
            rev_score = 40
        elif revenue_growth >= 15:
            rev_score = 25
        elif revenue_growth >= 0:
            rev_score = 10
        else:
            rev_score = 0
        score += rev_score
        details['revenue_growth'] = {'value': revenue_growth, 'score': rev_score}
        
        # 利润增速评分 (50分)
        if profit_growth >= 80:
            profit_score = 50
        elif profit_growth >= 50:
            profit_score = 40
        elif profit_growth >= 20:
            profit_score = 25
        elif profit_growth >= 0:
            profit_score = 10
        else:
            profit_score = 0
        score += profit_score
        details['profit_growth'] = {'value': profit_growth, 'score': profit_score}
        
        return score, details
    
    @classmethod
    def score_quality(cls, roe: float, roa: float = None, 
                      gross_margin: float = None, net_margin: float = None) -> Tuple[float, Dict]:
        """
        质量因子评分 (0-100)
        
        评分逻辑:
        - ROE: >20% 满分40分, >15% 35分, >10% 25分, >5% 15分
        - ROA: >10% 满分20分, >5% 15分
        - 毛利率: >40% 满分20分, >30% 15分
        - 净利率: >15% 满分20分, >10% 15分
        """
        score = 0
        details = {}
        
        # ROE评分 (40分)
        if roe >= 20:
            roe_score = 40
        elif roe >= 15:
            roe_score = 35
        elif roe >= 10:
            roe_score = 25
        elif roe >= 5:
            roe_score = 15
        else:
            roe_score = 0
        score += roe_score
        details['roe'] = {'value': roe, 'score': roe_score}
        
        # ROA评分 (20分)
        if roa is not None:
            if roa >= 10:
                roa_score = 20
            elif roa >= 5:
                roa_score = 15
            elif roa >= 0:
                roa_score = 5
            else:
                roa_score = 0
            score += roa_score
            details['roa'] = {'value': roa, 'score': roa_score}
        
        # 毛利率评分 (20分)
        if gross_margin is not None:
            if gross_margin >= 40:
                gm_score = 20
            elif gross_margin >= 30:
                gm_score = 15
            elif gross_margin >= 20:
                gm_score = 10
            else:
                gm_score = 0
            score += gm_score
            details['gross_margin'] = {'value': gross_margin, 'score': gm_score}
        
        # 净利率评分 (20分)
        if net_margin is not None:
            if net_margin >= 15:
                nm_score = 20
            elif net_margin >= 10:
                nm_score = 15
            elif net_margin >= 5:
                nm_score = 10
            else:
                nm_score = 0
            score += nm_score
            details['net_margin'] = {'value': net_margin, 'score': nm_score}
        
        return score, details
    
    @classmethod
    def score_valuation(cls, pe: float, pb: float = None, 
                        peg: float = None, market_cap: float = None) -> Tuple[float, Dict]:
        """
        估值因子评分 (0-100)
        
        评分逻辑:
        - PE: 20-40最优(30分), 10-20或40-60(20分)
        - PB: 2-5最优(25分)
        - PEG: <1最优(25分), 1-2(15分)
        - 市值: 30-150亿最优(20分)
        """
        score = 0
        details = {}
        
        # PE评分 (30分) - 适度估值最佳
        if 20 <= pe <= 40:
            pe_score = 30  # 最优区间
        elif 10 <= pe < 20 or 40 < pe <= 60:
            pe_score = 20
        elif 5 <= pe < 10 or 60 < pe <= 100:
            pe_score = 10
        elif pe > 0:
            pe_score = 5
        else:
            pe_score = 0  # 亏损
        score += pe_score
        details['pe'] = {'value': pe, 'score': pe_score}
        
        # PB评分 (25分)
        if pb is not None:
            if 2 <= pb <= 5:
                pb_score = 25
            elif 1 <= pb < 2 or 5 < pb <= 8:
                pb_score = 15
            elif pb > 0:
                pb_score = 5
            else:
                pb_score = 0
            score += pb_score
            details['pb'] = {'value': pb, 'score': pb_score}
        
        # PEG评分 (25分)
        if peg is not None:
            if 0 < peg <= 0.5:
                peg_score = 25  # 严重低估
            elif 0.5 < peg <= 1:
                peg_score = 20  # 低估
            elif 1 < peg <= 2:
                peg_score = 15  # 合理
            elif peg > 2:
                peg_score = 5
            else:
                peg_score = 0
            score += peg_score
            details['peg'] = {'value': peg, 'score': peg_score}
        
        # 市值评分 (20分) - 小市值更优
        if market_cap is not None:
            if 30 <= market_cap <= 150:
                mc_score = 20  # 最优区间
            elif 20 <= market_cap < 30 or 150 < market_cap <= 300:
                mc_score = 15
            elif 300 < market_cap <= 500:
                mc_score = 10
            elif 500 < market_cap <= 1000:
                mc_score = 5
            else:
                mc_score = 0
            score += mc_score
            details['market_cap'] = {'value': market_cap, 'score': mc_score}
        
        return score, details
    
    @classmethod
    def score_momentum(cls, momentum_5d: float = None, momentum_20d: float = None,
                       momentum_60d: float = None, relative_strength: float = None) -> Tuple[float, Dict]:
        """
        动量因子评分 (0-100)
        
        评分逻辑:
        - 5日动量: >5%得20分
        - 20日动量: >15%得30分
        - 60日动量: >30%得30分
        - 相对强度: >70得20分
        """
        score = 0
        details = {}
        
        # 5日动量 (20分)
        if momentum_5d is not None:
            if momentum_5d >= 10:
                m5_score = 20
            elif momentum_5d >= 5:
                m5_score = 15
            elif momentum_5d >= 0:
                m5_score = 10
            else:
                m5_score = 0
            score += m5_score
            details['momentum_5d'] = {'value': momentum_5d, 'score': m5_score}
        
        # 20日动量 (30分)
        if momentum_20d is not None:
            if momentum_20d >= 20:
                m20_score = 30
            elif momentum_20d >= 10:
                m20_score = 20
            elif momentum_20d >= 0:
                m20_score = 10
            else:
                m20_score = 0
            score += m20_score
            details['momentum_20d'] = {'value': momentum_20d, 'score': m20_score}
        
        # 60日动量 (30分)
        if momentum_60d is not None:
            if momentum_60d >= 40:
                m60_score = 30
            elif momentum_60d >= 20:
                m60_score = 20
            elif momentum_60d >= 0:
                m60_score = 10
            else:
                m60_score = 0
            score += m60_score
            details['momentum_60d'] = {'value': momentum_60d, 'score': m60_score}
        
        # 相对强度 (20分)
        if relative_strength is not None:
            if relative_strength >= 80:
                rs_score = 20
            elif relative_strength >= 60:
                rs_score = 15
            elif relative_strength >= 40:
                rs_score = 10
            else:
                rs_score = 0
            score += rs_score
            details['relative_strength'] = {'value': relative_strength, 'score': rs_score}
        
        return score, details
    
    @classmethod
    def score_scale(cls, market_cap: float) -> Tuple[float, Dict]:
        """
        规模因子评分 (0-100)
        
        历史10倍股特征:
        - 起步市值均值17亿，30亿以下占78%
        - 最优区间: 30-150亿（有成长空间又有一定规模）
        """
        score = 0
        details = {}
        
        if 30 <= market_cap <= 100:
            score = 100  # 最佳区间
        elif 100 < market_cap <= 150:
            score = 80
        elif 20 <= market_cap < 30:
            score = 70
        elif 150 < market_cap <= 300:
            score = 60
        elif 300 < market_cap <= 500:
            score = 40
        elif 500 < market_cap <= 800:
            score = 20
        else:
            score = 0
        
        details['market_cap'] = {'value': market_cap, 'score': score}
        return score, details
    
    @classmethod
    def score_technical(cls, ma_bullish: bool = None, volume_ratio: float = None,
                        rsi: float = None, is_new_high: bool = None,
                        price_position: float = None) -> Tuple[float, Dict]:
        """
        技术因子评分 (0-100)
        
        评分逻辑:
        - 均线多头: 是则30分
        - 量比放大: >1.5得25分
        - RSI: 40-70最优(25分)
        - 创新高: 是则20分
        """
        score = 0
        details = {}
        
        # 均线多头 (30分)
        if ma_bullish is not None:
            ma_score = 30 if ma_bullish else 0
            score += ma_score
            details['ma_bullish'] = {'value': ma_bullish, 'score': ma_score}
        
        # 量比 (25分)
        if volume_ratio is not None:
            if volume_ratio >= 2.0:
                vr_score = 25
            elif volume_ratio >= 1.5:
                vr_score = 20
            elif volume_ratio >= 1.2:
                vr_score = 15
            elif volume_ratio >= 1.0:
                vr_score = 10
            else:
                vr_score = 0
            score += vr_score
            details['volume_ratio'] = {'value': volume_ratio, 'score': vr_score}
        
        # RSI (25分) - 不超买不超卖最佳
        if rsi is not None:
            if 40 <= rsi <= 60:
                rsi_score = 25  # 中性区最佳
            elif 60 < rsi <= 70 or 30 <= rsi < 40:
                rsi_score = 20
            elif rsi > 70:  # 超买
                rsi_score = 5
            elif rsi < 30:  # 超卖
                rsi_score = 10
            else:
                rsi_score = 0
            score += rsi_score
            details['rsi'] = {'value': rsi, 'score': rsi_score}
        
        # 创新高 (20分)
        if is_new_high is not None:
            nh_score = 20 if is_new_high else 0
            score += nh_score
            details['is_new_high'] = {'value': is_new_high, 'score': nh_score}
        
        return score, details
    
    @classmethod
    def score_acceleration(cls, revenue_accel: float = None, 
                          profit_accel: float = None,
                          consecutive_improve: int = None) -> Tuple[float, Dict]:
        """
        成长加速度评分 (0-100) - 创新因子
        
        评分逻辑:
        - 营收加速度 > 0: 40分 (加速增长)
        - 利润加速度 > 0: 40分
        - 连续改善 >= 2季度: 20分
        """
        score = 0
        details = {}
        
        # 营收加速度 (40分)
        if revenue_accel is not None:
            if revenue_accel > 10:
                ra_score = 40
            elif revenue_accel > 5:
                ra_score = 30
            elif revenue_accel > 0:
                ra_score = 20
            else:
                ra_score = 0
            score += ra_score
            details['revenue_acceleration'] = {'value': revenue_accel, 'score': ra_score}
        
        # 利润加速度 (40分)
        if profit_accel is not None:
            if profit_accel > 15:
                pa_score = 40
            elif profit_accel > 5:
                pa_score = 30
            elif profit_accel > 0:
                pa_score = 20
            else:
                pa_score = 0
            score += pa_score
            details['profit_acceleration'] = {'value': profit_accel, 'score': pa_score}
        
        # 连续改善 (20分)
        if consecutive_improve is not None:
            if consecutive_improve >= 3:
                ci_score = 20
            elif consecutive_improve >= 2:
                ci_score = 15
            elif consecutive_improve >= 1:
                ci_score = 10
            else:
                ci_score = 0
            score += ci_score
            details['consecutive_improve'] = {'value': consecutive_improve, 'score': ci_score}
        
        return score, details
    
    @classmethod
    def score_money_flow(cls, main_net_inflow_ratio: float = None,
                         days_net_inflow: int = None) -> Tuple[float, Dict]:
        """
        资金流向评分 (0-100) - 创新因子
        
        评分逻辑:
        - 主力净流入占比 > 10%: 50分
        - 连续净流入天数 >= 3天: 50分
        """
        score = 0
        details = {}
        
        # 主力净流入占比 (50分)
        if main_net_inflow_ratio is not None:
            if main_net_inflow_ratio > 15:
                mf_score = 50
            elif main_net_inflow_ratio > 10:
                mf_score = 40
            elif main_net_inflow_ratio > 5:
                mf_score = 30
            elif main_net_inflow_ratio > 0:
                mf_score = 15
            else:
                mf_score = 0
            score += mf_score
            details['main_net_inflow'] = {'value': main_net_inflow_ratio, 'score': mf_score}
        
        # 连续净流入 (50分)
        if days_net_inflow is not None:
            if days_net_inflow >= 5:
                dni_score = 50
            elif days_net_inflow >= 3:
                dni_score = 40
            elif days_net_inflow >= 2:
                dni_score = 25
            elif days_net_inflow >= 1:
                dni_score = 10
            else:
                dni_score = 0
            score += dni_score
            details['days_net_inflow'] = {'value': days_net_inflow, 'score': dni_score}
        
        return score, details


# ============================================================
# 因子引擎
# ============================================================

class TenbaggerV2FactorEngine:
    """十倍股V2因子计算引擎"""
    
    def __init__(self, weights: FactorWeights = None):
        self.weights = weights or FactorWeights()
        self.scorer = FactorScorer()
    
    def calculate_all_scores(self, stock_data: Dict) -> Dict:
        """
        计算所有因子得分
        
        Args:
            stock_data: 包含财务、估值、技术等数据的字典
            
        Returns:
            包含各维度得分和总分的字典
        """
        scores = {}
        details = {}
        
        # 1. 成长因子
        growth_score, growth_detail = self.scorer.score_growth(
            revenue_growth=stock_data.get('inc_revenue_year_on_year', 0),
            profit_growth=stock_data.get('inc_net_profit_year_on_year', 0)
        )
        scores['growth'] = growth_score
        details['growth'] = growth_detail
        
        # 2. 质量因子
        quality_score, quality_detail = self.scorer.score_quality(
            roe=stock_data.get('roe', 0),
            roa=stock_data.get('roa'),
            gross_margin=stock_data.get('gross_profit_margin'),
            net_margin=stock_data.get('net_profit_margin')
        )
        scores['quality'] = quality_score
        details['quality'] = quality_detail
        
        # 3. 估值因子
        pe = stock_data.get('pe_ratio', 0)
        profit_growth = stock_data.get('inc_net_profit_year_on_year', 0)
        peg = pe / profit_growth if profit_growth > 0 and pe > 0 else None
        
        valuation_score, valuation_detail = self.scorer.score_valuation(
            pe=pe,
            pb=stock_data.get('pb_ratio'),
            peg=peg,
            market_cap=stock_data.get('market_cap')
        )
        scores['valuation'] = valuation_score
        details['valuation'] = valuation_detail
        
        # 4. 动量因子
        momentum_score, momentum_detail = self.scorer.score_momentum(
            momentum_5d=stock_data.get('momentum_5d'),
            momentum_20d=stock_data.get('momentum_20d'),
            momentum_60d=stock_data.get('momentum_60d'),
            relative_strength=stock_data.get('relative_strength')
        )
        scores['momentum'] = momentum_score
        details['momentum'] = momentum_detail
        
        # 5. 规模因子
        scale_score, scale_detail = self.scorer.score_scale(
            market_cap=stock_data.get('market_cap', 0)
        )
        scores['scale'] = scale_score
        details['scale'] = scale_detail
        
        # 6. 技术因子
        technical_score, technical_detail = self.scorer.score_technical(
            ma_bullish=stock_data.get('ma_bullish'),
            volume_ratio=stock_data.get('volume_ratio'),
            rsi=stock_data.get('rsi_14'),
            is_new_high=stock_data.get('is_new_high_20d'),
            price_position=stock_data.get('price_position_52w')
        )
        scores['technical'] = technical_score
        details['technical'] = technical_detail
        
        # 7. 成长加速度 (创新因子)
        accel_score, accel_detail = self.scorer.score_acceleration(
            revenue_accel=stock_data.get('revenue_acceleration'),
            profit_accel=stock_data.get('profit_acceleration'),
            consecutive_improve=stock_data.get('consecutive_improve')
        )
        scores['acceleration'] = accel_score
        details['acceleration'] = accel_detail
        
        # 8. 资金流向 (创新因子)
        money_score, money_detail = self.scorer.score_money_flow(
            main_net_inflow_ratio=stock_data.get('main_net_inflow_ratio'),
            days_net_inflow=stock_data.get('days_net_inflow')
        )
        scores['money_flow'] = money_score
        details['money_flow'] = money_detail
        
        # 计算加权总分
        total_score = self._calculate_weighted_score(scores)
        
        return {
            'total_score': total_score,
            'scores': scores,
            'details': details
        }
    
    def _calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """计算加权总分"""
        weights = self.weights
        
        # 核心因子
        core_score = (
            scores.get('growth', 0) * weights.growth +
            scores.get('quality', 0) * weights.quality +
            scores.get('valuation', 0) * weights.valuation +
            scores.get('momentum', 0) * weights.momentum +
            scores.get('scale', 0) * weights.scale +
            scores.get('technical', 0) * weights.technical
        )
        
        # 创新因子
        new_score = (
            scores.get('acceleration', 0) * weights.acceleration +
            scores.get('money_flow', 0) * weights.money_flow
        )
        
        # 总分 = 核心因子 + 创新因子
        total = core_score + new_score
        
        return round(total, 2)
    
    def get_score_level(self, total_score: float) -> str:
        """根据总分确定等级"""
        if total_score >= 80:
            return 'S+'  # 顶级潜力
        elif total_score >= 70:
            return 'S'   # 优秀
        elif total_score >= 60:
            return 'A'   # 良好
        elif total_score >= 50:
            return 'B'   # 一般
        elif total_score >= 40:
            return 'C'   # 观察
        else:
            return 'D'   # 排除
    
    def get_recommendation(self, total_score: float, stage: str = None) -> str:
        """根据得分和阶段给出推荐"""
        level = self.get_score_level(total_score)
        
        if level in ['S+', 'S'] and stage in ['S0', 'S1']:
            return '🔥 强烈推荐 - 早期布局'
        elif level in ['S+', 'S']:
            return '⭐ 推荐关注'
        elif level == 'A' and stage in ['S1', 'S2']:
            return '👍 值得关注'
        elif level == 'A':
            return '📊 观察名单'
        elif level == 'B':
            return '⏳ 等待时机'
        else:
            return '❌ 暂不推荐'


# ============================================================
# 测试
# ============================================================

def test_factor_engine():
    """测试因子引擎"""
    engine = TenbaggerV2FactorEngine()
    
    # 模拟股票数据
    test_data = {
        'code': '300750.XSHE',
        'name': '宁德时代',
        # 财务
        'inc_revenue_year_on_year': 45.0,
        'inc_net_profit_year_on_year': 60.0,
        'roe': 18.5,
        'roa': 8.2,
        'gross_profit_margin': 35.0,
        'net_profit_margin': 12.0,
        # 估值
        'pe_ratio': 35.0,
        'pb_ratio': 4.5,
        'market_cap': 120.0,  # 亿
        # 动量
        'momentum_5d': 3.5,
        'momentum_20d': 12.0,
        'momentum_60d': 25.0,
        # 技术
        'ma_bullish': True,
        'volume_ratio': 1.3,
        'rsi_14': 55.0,
        'is_new_high_20d': False,
        # 加速度
        'revenue_acceleration': 5.0,
        'profit_acceleration': 8.0,
        'consecutive_improve': 2,
        # 资金流
        'main_net_inflow_ratio': 8.0,
        'days_net_inflow': 3
    }
    
    result = engine.calculate_all_scores(test_data)
    
    print(f"\n{'='*60}")
    print(f"📊 因子评分测试 - {test_data['name']}")
    print(f"{'='*60}")
    print(f"\n总分: {result['total_score']}")
    print(f"等级: {engine.get_score_level(result['total_score'])}")
    print(f"推荐: {engine.get_recommendation(result['total_score'], 'S1')}")
    
    print(f"\n各维度得分:")
    for factor, score in result['scores'].items():
        print(f"  {factor}: {score}")


if __name__ == "__main__":
    test_factor_engine()
