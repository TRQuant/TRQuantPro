#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股核心策略知识库 V1.0
===========================

基于本地研究成果整合，融合：
1. TENBAGGER_CASE_STUDY.md - 南大光电/卓胜微/斯达半导等历史案例
2. tenbagger_identification_kb.py - 阶段识别与评分系统
3. StageMachine - 状态机与事件驱动
4. MainlineBasedScanner - 市场主线扫描

核心理念：
- 十倍股 = 市场主线 × 早期阶段 × 业绩拐点 × 长期持有
- 关键是找到S1-S2阶段的潜力股，在市场主线启动时介入

数据来源：本地研究成果
创建时间：2025-12-27
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np


# ============== 历史十倍股案例总结 ==============

HISTORICAL_TENBAGGERS = {
    # 案例来源：TENBAGGER_CASE_STUDY.md
    
    "南大光电_300346": {
        "period": "2019-2021",
        "sector": "半导体/光刻胶",
        "start_price": 8,
        "peak_price": 90,
        "return": "10x+",
        "early_features": {
            "market_cap": 30,        # 亿元，小市值
            "revenue_growth": 0.18,   # 18%
            "profit_growth": 0.25,    # 25%
            "gross_margin": 0.42,     # 42%
            "roe": 0.08,              # 8% (成长期可接受较低)
            "rd_ratio": 0.12,         # 12% 高研发
        },
        "catalyst": ["国产替代政策", "光刻胶技术验证", "大客户突破"],
        "entry_stage": "S2",  # 导入期
        "hold_period": "2年",
        "key_lesson": "技术突破+国产替代双重催化，小市值弹性大",
    },
    
    "卓胜微_300782": {
        "period": "2019-2021",
        "sector": "半导体/射频芯片",
        "start_price": 30,
        "peak_price": 400,
        "return": "13x+",
        "early_features": {
            "market_cap": 50,
            "revenue_growth": 0.40,
            "profit_growth": 0.50,
            "gross_margin": 0.45,
            "roe": 0.20,
            "rd_ratio": 0.08,
        },
        "catalyst": ["5G换机潮", "国产替代", "华为供应链"],
        "entry_stage": "S2",
        "hold_period": "2年",
        "key_lesson": "高增速+高ROE，行业景气度是关键",
    },
    
    "斯达半导_603290": {
        "period": "2020-2021",
        "sector": "半导体/IGBT",
        "start_price": 20,
        "peak_price": 400,
        "return": "20x+",
        "early_features": {
            "market_cap": 80,
            "revenue_growth": 0.35,
            "profit_growth": 0.60,
            "gross_margin": 0.35,
            "roe": 0.18,
        },
        "catalyst": ["新能源车爆发", "IGBT国产替代"],
        "entry_stage": "S2-S3",
        "hold_period": "1.5年",
        "key_lesson": "下游需求爆发+细分领域龙头",
    },
    
    "宁德时代_300750": {
        "period": "2018-2021",
        "sector": "新能源/动力电池",
        "start_price": 25,
        "peak_price": 690,
        "return": "27x+",
        "early_features": {
            "market_cap": 500,  # 相对较大
            "revenue_growth": 0.50,
            "profit_growth": 0.40,
            "gross_margin": 0.30,
            "roe": 0.15,
        },
        "catalyst": ["新能源补贴", "特斯拉供应链", "行业渗透率提升"],
        "entry_stage": "S3",
        "hold_period": "3年",
        "key_lesson": "行业龙头+渗透率拐点+超长周期持有",
    },
    
    "比亚迪_002594": {
        "period": "2020-2022",
        "sector": "新能源/整车",
        "start_price": 50,
        "peak_price": 330,
        "return": "6.6x",
        "early_features": {
            "market_cap": 1500,
            "revenue_growth": 0.20,
            "profit_growth": -0.10,  # 初期利润下滑
        },
        "catalyst": ["刀片电池发布", "新能源车销量爆发", "燃油车禁售预期"],
        "entry_stage": "S2",  # 困境反转
        "hold_period": "2年",
        "key_lesson": "困境反转型+技术突破+行业风口",
    },
}


# ============== 十倍股早期特征提取 ==============

@dataclass
class TenbaggerEarlySignals:
    """十倍股早期信号特征
    
    基于历史案例总结的关键早期特征
    """
    
    # === 财务特征 (从案例中提取) ===
    
    # 市值区间（亿元）- 小市值优先
    ideal_market_cap_range: Tuple[float, float] = (30, 200)  # 30-200亿最佳
    acceptable_market_cap_range: Tuple[float, float] = (20, 500)  # 可接受范围
    
    # 营收增速 - 关注加速
    min_revenue_growth: float = 0.15  # >=15%
    ideal_revenue_growth: float = 0.30  # 理想>=30%
    
    # 利润增速 - 核心指标
    min_profit_growth: float = 0.20  # >=20%
    ideal_profit_growth: float = 0.50  # 理想>=50%
    
    # ROE - 成长期可放宽
    min_roe: float = 0.05  # >=5% (放宽，很多十倍股早期ROE不高)
    ideal_roe: float = 0.15  # 理想>=15%
    
    # 毛利率 - 护城河指标
    min_gross_margin: float = 0.25  # >=25%
    ideal_gross_margin: float = 0.40  # 理想>=40%
    
    # 研发投入 - 科技股重要
    min_rd_ratio: float = 0.05  # >=5%
    ideal_rd_ratio: float = 0.10  # 理想>=10%
    
    # === 成长加速特征 ===
    
    # 连续改善季度数
    min_consecutive_improvement: int = 2  # 至少2个季度
    
    # 增速环比提升
    growth_acceleration_required: bool = True
    
    # === 阶段特征 ===
    
    # 最佳介入阶段
    ideal_entry_stages: List[str] = field(default_factory=lambda: ["S1", "S2"])
    
    # 持有阶段
    hold_stages: List[str] = field(default_factory=lambda: ["S2", "S3", "S4"])
    
    # 退出阶段
    exit_stages: List[str] = field(default_factory=lambda: ["S5"])


# ============== 十倍股买入规则 ==============

TENBAGGER_BUY_RULES = {
    "rule_1_small_cap": {
        "name": "小市值优先",
        "description": "市值30-200亿，弹性最大",
        "weight": 15,
        "check": lambda mc: 30 <= mc <= 200,
        "score_func": lambda mc: 15 if 30 <= mc <= 100 else 10 if 100 < mc <= 200 else 5 if mc < 30 else 0,
    },
    
    "rule_2_high_growth": {
        "name": "高成长性",
        "description": "净利润增速>30%，营收增速>20%",
        "weight": 25,
        "check": lambda pg, rg: pg > 0.30 and rg > 0.20,
        "score_func": lambda pg, rg: min(25, (pg * 30 + rg * 20)),
    },
    
    "rule_3_growth_acceleration": {
        "name": "增长加速",
        "description": "连续2个季度以上业绩改善",
        "weight": 15,
        "check": lambda q1_growth, q2_growth: q2_growth > q1_growth,
    },
    
    "rule_4_industry_leader": {
        "name": "细分龙头",
        "description": "细分行业前3名",
        "weight": 10,
        "check": lambda rank: rank <= 3,
    },
    
    "rule_5_catalyst": {
        "name": "催化剂明确",
        "description": "有明确的政策/技术/需求催化剂",
        "weight": 15,
        "check": lambda has_catalyst: has_catalyst,
    },
    
    "rule_6_stage": {
        "name": "阶段合适",
        "description": "处于S1-S2阶段（早期验证/导入期）",
        "weight": 10,
        "check": lambda stage: stage in ["S1", "S2"],
        "score_func": lambda stage: 10 if stage == "S2" else 7 if stage == "S1" else 3 if stage == "S3" else 0,
    },
    
    "rule_7_low_attention": {
        "name": "低关注度",
        "description": "研报覆盖少，机构持仓低",
        "weight": 10,
        "check": lambda report_count, inst_ratio: report_count < 10 and inst_ratio < 0.30,
    },
}


# ============== 十倍股卖出规则 ==============

TENBAGGER_SELL_RULES = {
    "sell_1_target_reached": {
        "name": "目标达成",
        "description": "涨幅达到目标（如3倍、5倍、10倍）部分止盈",
        "action": "partial_sell",
        "ratios": {
            3.0: 0.20,   # 涨3倍卖20%
            5.0: 0.30,   # 涨5倍再卖30%
            10.0: 0.50,  # 涨10倍再卖50%（保留部分）
        },
    },
    
    "sell_2_stage_mature": {
        "name": "阶段成熟",
        "description": "进入S5成熟期，十倍股特征消失",
        "action": "full_sell",
        "trigger": lambda stage: stage == "S5",
    },
    
    "sell_3_growth_slowdown": {
        "name": "增长放缓",
        "description": "连续2季度增速下滑且低于20%",
        "action": "partial_sell",
        "trigger": lambda q1_growth, q2_growth: q2_growth < q1_growth and q2_growth < 0.20,
    },
    
    "sell_4_falsified": {
        "name": "逻辑证伪",
        "description": "核心逻辑被证伪（客户丢失、技术失败等）",
        "action": "full_sell",
        "trigger": lambda falsified: falsified,
    },
    
    "sell_5_valuation_extreme": {
        "name": "估值过高",
        "description": "PE>100且PEG>3",
        "action": "partial_sell",
        "trigger": lambda pe, peg: pe > 100 and peg > 3,
    },
    
    "sell_6_max_hold_period": {
        "name": "最长持有期",
        "description": "持有超过5年考虑全部退出",
        "action": "review",
        "max_years": 5,
    },
}


# ============== 市场主线识别 ==============

class MainlineType(Enum):
    """市场主线类型"""
    TECH_SUBSTITUTION = "国产替代"  # 半导体、材料
    NEW_ENERGY = "新能源革命"       # 锂电、光伏、风电
    CONSUMPTION_UPGRADE = "消费升级" # 白酒、医美、新消费
    AI_DIGITAL = "数字经济"         # AI、云计算、数据中心
    BIO_PHARMA = "生物医药"         # 创新药、医疗器械
    ADVANCED_MANUFACTURING = "高端制造"  # 机器人、数控


MAINLINE_INDICATORS = {
    MainlineType.TECH_SUBSTITUTION: {
        "description": "国产替代主线，关注半导体设备、材料、芯片设计",
        "key_sectors": ["半导体", "电子元器件", "新材料"],
        "policy_keywords": ["国产替代", "自主可控", "卡脖子"],
        "typical_tenbaggers": ["南大光电", "卓胜微", "斯达半导"],
        "entry_timing": "政策发布后6-12个月，技术验证阶段",
        "position_weight": 0.25,
    },
    
    MainlineType.NEW_ENERGY: {
        "description": "新能源革命主线，关注锂电、光伏、整车",
        "key_sectors": ["新能源", "锂电池", "光伏", "储能"],
        "policy_keywords": ["碳中和", "新能源", "渗透率"],
        "typical_tenbaggers": ["宁德时代", "比亚迪", "隆基股份"],
        "entry_timing": "渗透率5%-20%阶段，业绩拐点",
        "position_weight": 0.30,
    },
    
    MainlineType.AI_DIGITAL: {
        "description": "数字经济主线，关注AI应用、算力、数据",
        "key_sectors": ["人工智能", "云计算", "数据中心", "软件"],
        "policy_keywords": ["数字经济", "人工智能", "算力"],
        "typical_tenbaggers": ["科大讯飞", "浪潮信息"],
        "entry_timing": "技术突破后应用爆发期",
        "position_weight": 0.20,
    },
}


# ============== 阶段化持仓策略 ==============

STAGE_POSITION_STRATEGY = {
    "S0": {
        "name": "观察期",
        "description": "早期信号，高度不确定",
        "max_position": 0.03,  # 最大3%
        "stop_loss": 0.25,     # 止损25%
        "take_profit": None,   # 不设止盈
        "hold_min_months": 6,
        "action": "小仓观察",
    },
    
    "S1": {
        "name": "验证期",
        "description": "初步验证，潜力待确认",
        "max_position": 0.08,  # 最大8%
        "stop_loss": 0.20,
        "take_profit": 0.50,   # 涨50%部分止盈
        "hold_min_months": 3,
        "action": "逐步建仓",
    },
    
    "S2": {
        "name": "导入期（最佳买入点）",
        "description": "成长黄金期，业绩拐点",
        "max_position": 0.15,  # 最大15%
        "stop_loss": 0.15,
        "take_profit": 1.00,   # 涨100%部分止盈
        "hold_min_months": 6,
        "action": "★重点买入★",
    },
    
    "S3": {
        "name": "放量期",
        "description": "快速增长确认，关注估值",
        "max_position": 0.12,
        "stop_loss": 0.12,
        "take_profit": 0.50,
        "hold_min_months": 3,
        "action": "持有为主，逢高减仓",
    },
    
    "S4": {
        "name": "加速期",
        "description": "接近成熟，注意风险",
        "max_position": 0.08,
        "stop_loss": 0.10,
        "take_profit": 0.30,
        "hold_min_months": 1,
        "action": "逐步退出",
    },
    
    "S5": {
        "name": "成熟期",
        "description": "主流共识，十倍股特征消失",
        "max_position": 0.05,
        "stop_loss": 0.08,
        "take_profit": 0.20,
        "hold_min_months": 0,
        "action": "全部退出",
    },
}


# ============== 早期进入算法 ==============

class EarlyEntryAlgorithm:
    """早期进入算法
    
    综合多个信号判断最佳介入时机
    """
    
    # 信号权重
    SIGNAL_WEIGHTS = {
        "stage_s1_s2": 25,           # 阶段S1-S2
        "growth_acceleration": 20,    # 增长加速
        "small_cap_bonus": 15,        # 小市值加分
        "mainline_hot": 15,           # 市场主线热门
        "low_attention": 10,          # 低关注度
        "catalyst_clear": 10,         # 催化剂明确
        "technical_breakout": 5,      # 技术突破
    }
    
    # 信号阈值
    ENTRY_THRESHOLD = 65  # 总分>=65分才考虑介入
    STRONG_BUY_THRESHOLD = 80  # >=80分强烈推荐
    
    @classmethod
    def calculate_entry_score(
        cls,
        stage: str,
        market_cap: float,
        revenue_growth: float,
        profit_growth: float,
        prev_profit_growth: float,
        mainline_score: float,
        research_report_count: int,
        institution_ratio: float,
        has_catalyst: bool,
        technical_breakout: bool = False,
    ) -> Tuple[float, Dict[str, float], str]:
        """计算进入得分
        
        Returns:
            (总分, 各项得分详情, 建议)
        """
        scores = {}
        
        # 1. 阶段得分 (25分)
        if stage == "S2":
            scores["stage_s1_s2"] = 25
        elif stage == "S1":
            scores["stage_s1_s2"] = 20
        elif stage == "S3":
            scores["stage_s1_s2"] = 10
        else:
            scores["stage_s1_s2"] = 0
        
        # 2. 增长加速 (20分)
        if profit_growth > prev_profit_growth and profit_growth > 0.30:
            scores["growth_acceleration"] = 20
        elif profit_growth > prev_profit_growth:
            scores["growth_acceleration"] = 15
        elif profit_growth > 0.30:
            scores["growth_acceleration"] = 10
        else:
            scores["growth_acceleration"] = 0
        
        # 3. 小市值加分 (15分)
        if 30 <= market_cap <= 100:
            scores["small_cap_bonus"] = 15
        elif 100 < market_cap <= 200:
            scores["small_cap_bonus"] = 12
        elif 200 < market_cap <= 500:
            scores["small_cap_bonus"] = 8
        else:
            scores["small_cap_bonus"] = 0
        
        # 4. 市场主线 (15分)
        scores["mainline_hot"] = min(15, mainline_score * 0.15)
        
        # 5. 低关注度 (10分)
        if research_report_count < 5 and institution_ratio < 0.10:
            scores["low_attention"] = 10
        elif research_report_count < 10 and institution_ratio < 0.20:
            scores["low_attention"] = 7
        else:
            scores["low_attention"] = 0
        
        # 6. 催化剂 (10分)
        scores["catalyst_clear"] = 10 if has_catalyst else 0
        
        # 7. 技术突破 (5分)
        scores["technical_breakout"] = 5 if technical_breakout else 0
        
        # 计算总分
        total_score = sum(scores.values())
        
        # 生成建议
        if total_score >= cls.STRONG_BUY_THRESHOLD:
            advice = "★★★ 强烈推荐买入"
        elif total_score >= cls.ENTRY_THRESHOLD:
            advice = "★★ 可以买入"
        elif total_score >= 50:
            advice = "★ 关注观察"
        else:
            advice = "暂不推荐"
        
        return total_score, scores, advice


# ============== 防过拟合验证规则 ==============

ANTI_OVERFIT_RULES = {
    "rule_1_minimum_samples": {
        "name": "最小样本数",
        "description": "至少有10只历史十倍股满足条件",
        "min_count": 10,
    },
    
    "rule_2_out_of_sample": {
        "name": "样本外验证",
        "description": "在未参与建模的时间段验证",
        "required": True,
    },
    
    "rule_3_sector_diversity": {
        "name": "行业多样性",
        "description": "筛选结果至少覆盖3个行业",
        "min_sectors": 3,
    },
    
    "rule_4_no_hindsight": {
        "name": "避免后见之明",
        "description": "使用可获取的历史数据，不使用未来数据",
        "required": True,
    },
    
    "rule_5_param_stability": {
        "name": "参数稳定性",
        "description": "参数微调不应显著改变结果",
        "sensitivity_test": True,
    },
}


# ============== 导出 ==============

__all__ = [
    'HISTORICAL_TENBAGGERS',
    'TenbaggerEarlySignals',
    'TENBAGGER_BUY_RULES',
    'TENBAGGER_SELL_RULES',
    'MainlineType',
    'MAINLINE_INDICATORS',
    'STAGE_POSITION_STRATEGY',
    'EarlyEntryAlgorithm',
    'ANTI_OVERFIT_RULES',
]







































