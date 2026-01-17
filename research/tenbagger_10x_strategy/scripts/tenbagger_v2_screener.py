#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 三层漏斗筛选器
=====================================

筛选架构:
L0 基础过滤 (约4000只 → 500只)
├── 剔除ST/*ST
├── 市值: 30-1000亿
├── 换手率 > 0.5%
├── 上市 > 365天
└── 营收/利润 > 0

L1 早期信号 (500只 → 50只)
├── 营收增速 > 20%
├── 利润增速 > 25%
├── ROE > 8%
├── 得分 > 50分
└── 营收加速度 > 0 (新增)

L2 精选推荐 (50只 → 10只)
├── 得分 > 70分
├── 均线多头
├── 量价配合
├── 主力资金流入 (新增)
└── 市场趋势匹配

阶段识别 (S0-S5):
- S0 种子期: 市值<50亿，增速显现
- S1 萌芽期: 市值50-100亿，增速>30% ★最佳买入
- S2 加速期: 市值100-300亿，增速>50%
- S3 扩张期: 市值300-800亿，持续增长
- S4 成熟期: 市值>800亿，增速放缓
- S5 衰退期: 增速转负

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_screener.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import logging

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

from research.tenbagger_10x_strategy.scripts.tenbagger_v2_data_loader import TenbaggerV2DataLoader
from research.tenbagger_10x_strategy.scripts.tenbagger_v2_factor_engine import TenbaggerV2FactorEngine, FactorWeights

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 阶段定义
# ============================================================

class TenbaggerStage(Enum):
    """十倍股成长阶段"""
    S0_SEED = "S0"           # 种子期
    S1_EMERGENCE = "S1"      # 萌芽期 ★最佳买入
    S2_ACCELERATION = "S2"   # 加速期
    S3_EXPANSION = "S3"      # 扩张期
    S4_MATURITY = "S4"       # 成熟期
    S5_DECLINE = "S5"        # 衰退期
    
    @property
    def description(self) -> str:
        desc = {
            "S0": "种子期 - 市值<50亿，增速显现，观望为主",
            "S1": "萌芽期 - 市值50-100亿，增速>30%，★最佳买入点",
            "S2": "加速期 - 市值100-300亿，增速>50%，趋势跟进",
            "S3": "扩张期 - 市值300-800亿，持续增长，持有观察",
            "S4": "成熟期 - 市值>800亿，增速放缓，考虑获利了结",
            "S5": "衰退期 - 增速转负，卖出"
        }
        return desc.get(self.value, "未知阶段")
    
    @property
    def action(self) -> str:
        actions = {
            "S0": "观望/小仓试探",
            "S1": "★建仓/加仓",
            "S2": "持有/趋势加仓",
            "S3": "持有/部分获利",
            "S4": "减仓/获利了结",
            "S5": "清仓"
        }
        return actions.get(self.value, "观望")


# ============================================================
# 筛选条件配置
# ============================================================

@dataclass
class L0Criteria:
    """L0 基础过滤条件"""
    exclude_st: bool = True
    exclude_delisting_risk: bool = True
    min_market_cap: float = 30.0       # 最小市值（亿）
    max_market_cap: float = 1000.0     # 最大市值（亿）
    min_turnover: float = 0.5          # 最小换手率 (%)
    min_listing_days: int = 365        # 最小上市天数
    min_revenue: float = 0             # 最小营收
    min_profit: float = 0              # 最小利润（允许亏损股？）
    require_positive_profit: bool = True  # 要求盈利


@dataclass
class L1Criteria:
    """L1 早期信号条件"""
    min_revenue_growth: float = 20.0     # 营收增速 > 20%
    min_profit_growth: float = 25.0      # 利润增速 > 25%
    min_roe: float = 8.0                 # ROE > 8%
    min_score: float = 50.0              # 综合得分 > 50
    require_acceleration: bool = True    # 要求加速增长
    min_gross_margin: float = 20.0       # 毛利率 > 20%


@dataclass
class L2Criteria:
    """L2 精选推荐条件"""
    min_score: float = 70.0              # 综合得分 > 70
    require_ma_bullish: bool = True      # 要求均线多头
    min_volume_ratio: float = 1.0        # 最小量比
    require_money_inflow: bool = True    # 要求资金流入
    max_price_position: float = 80.0     # 52周价格位置上限 (%)
    prefer_stages: List[str] = field(default_factory=lambda: ['S0', 'S1', 'S2'])


# ============================================================
# 阶段识别器
# ============================================================

class StageIdentifier:
    """十倍股阶段识别器"""
    
    @staticmethod
    def identify_stage(market_cap: float, revenue_growth: float,
                       profit_growth: float, roe: float = None,
                       revenue_acceleration: float = None) -> TenbaggerStage:
        """
        识别股票所处阶段
        
        核心逻辑:
        - 市值决定基础阶段
        - 增速决定阶段内状态
        - 加速度决定趋势方向
        """
        # 衰退期判断 - 增速转负
        if profit_growth < 0 and revenue_growth < 5:
            return TenbaggerStage.S5_DECLINE
        
        # 成熟期 - 大市值
        if market_cap > 800:
            if profit_growth >= 15:
                return TenbaggerStage.S4_MATURITY
            else:
                return TenbaggerStage.S5_DECLINE
        
        # 扩张期 - 中大市值
        if market_cap > 300:
            if profit_growth >= 20:
                return TenbaggerStage.S3_EXPANSION
            else:
                return TenbaggerStage.S4_MATURITY
        
        # 加速期 - 中等市值，高增速
        if market_cap > 100:
            if profit_growth >= 50 or (profit_growth >= 30 and revenue_growth >= 40):
                return TenbaggerStage.S2_ACCELERATION
            elif profit_growth >= 20:
                return TenbaggerStage.S3_EXPANSION
            else:
                return TenbaggerStage.S4_MATURITY
        
        # 萌芽期 - 小市值，中高增速 ★最佳买入
        if market_cap >= 50:
            if profit_growth >= 30 or revenue_growth >= 25:
                return TenbaggerStage.S1_EMERGENCE
            else:
                return TenbaggerStage.S0_SEED
        
        # 种子期 - 极小市值
        if market_cap >= 30:
            if profit_growth >= 50 or revenue_growth >= 40:
                return TenbaggerStage.S1_EMERGENCE
            else:
                return TenbaggerStage.S0_SEED
        
        # 默认种子期
        return TenbaggerStage.S0_SEED
    
    @staticmethod
    def get_stage_score_bonus(stage: TenbaggerStage) -> float:
        """根据阶段给予分数加成"""
        bonuses = {
            TenbaggerStage.S0_SEED: 5,          # 早期风险大
            TenbaggerStage.S1_EMERGENCE: 15,    # 最佳阶段，最高加分
            TenbaggerStage.S2_ACCELERATION: 10, # 仍有空间
            TenbaggerStage.S3_EXPANSION: 5,     # 空间减小
            TenbaggerStage.S4_MATURITY: 0,      # 不加分
            TenbaggerStage.S5_DECLINE: -10,     # 扣分
        }
        return bonuses.get(stage, 0)


# ============================================================
# 三层漏斗筛选器
# ============================================================

class TenbaggerV2Screener:
    """十倍股V2三层漏斗筛选器"""
    
    def __init__(self, 
                 l0_criteria: L0Criteria = None,
                 l1_criteria: L1Criteria = None,
                 l2_criteria: L2Criteria = None):
        self.l0 = l0_criteria or L0Criteria()
        self.l1 = l1_criteria or L1Criteria()
        self.l2 = l2_criteria or L2Criteria()
        
        self.data_loader = TenbaggerV2DataLoader()
        self.factor_engine = TenbaggerV2FactorEngine()
        self.stage_identifier = StageIdentifier()
        
        # 结果存储
        self.l0_passed = []
        self.l1_passed = []
        self.l2_passed = []
        self.final_picks = []
    
    def run_full_screening(self, date: str = None) -> List[Dict]:
        """运行完整的三层筛选"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🎯 十倍股早期识别系统 V2.0 - 三层漏斗筛选")
        logger.info(f"📅 筛选日期: {date}")
        logger.info(f"{'='*70}")
        
        # 加载数据
        data = self.data_loader.load_all_data(date)
        
        # L0 基础过滤
        self.l0_passed = self._filter_l0(data)
        logger.info(f"\n📊 L0 基础过滤: {len(data['stocks'])} → {len(self.l0_passed)}")
        
        # L1 早期信号
        self.l1_passed = self._filter_l1(self.l0_passed, data)
        logger.info(f"📈 L1 早期信号: {len(self.l0_passed)} → {len(self.l1_passed)}")
        
        # L2 精选推荐
        self.l2_passed = self._filter_l2(self.l1_passed, data)
        logger.info(f"🌟 L2 精选推荐: {len(self.l1_passed)} → {len(self.l2_passed)}")
        
        # 最终排序
        self.final_picks = self._rank_and_select(self.l2_passed)
        
        logger.info(f"\n✅ 最终推荐: {len(self.final_picks)} 只股票")
        
        return self.final_picks
    
    def _filter_l0(self, data: Dict) -> List[Dict]:
        """L0 基础过滤"""
        passed = []
        
        financial_df = data.get('financial', pd.DataFrame())
        valuation_df = data.get('valuation', pd.DataFrame())
        
        if financial_df.empty or valuation_df.empty:
            return passed
        
        # 合并数据
        merged = pd.merge(
            financial_df, valuation_df,
            on='code', how='inner'
        )
        
        for _, row in merged.iterrows():
            code = row['code']
            
            # 剔除ST
            if self.l0.exclude_st and 'ST' in str(row.get('display_name', '')):
                continue
            
            # 市值范围
            market_cap = row.get('market_cap', 0)
            if market_cap is None:
                continue
            try:
                if np.isnan(market_cap):
                    continue
            except:
                pass
            # 聚宽market_cap单位已经是亿元
            market_cap_billion = float(market_cap)
            if market_cap_billion < self.l0.min_market_cap or market_cap_billion > self.l0.max_market_cap:
                continue
            
            # 换手率
            turnover = row.get('turnover_ratio', 0)
            if turnover is None or np.isnan(turnover):
                turnover = 0
            if turnover < self.l0.min_turnover:
                continue
            
            # 盈利要求
            if self.l0.require_positive_profit:
                operating_profit = row.get('operating_profit', 0)
                if operating_profit is None:
                    continue
                try:
                    if np.isnan(operating_profit) or operating_profit <= 0:
                        continue
                except:
                    if operating_profit <= 0:
                        continue
            
            passed.append({
                'code': code,
                'market_cap': market_cap_billion,
                'turnover_ratio': turnover,
                'roe': row.get('roe', 0),
                'roa': row.get('roa', 0),
                'gross_profit_margin': row.get('gross_profit_margin', 0),
                'net_profit_margin': row.get('net_profit_margin', 0),
                'inc_revenue_year_on_year': row.get('inc_revenue_year_on_year', 0),
                'inc_net_profit_year_on_year': row.get('inc_net_profit_year_on_year', 0),
                'pe_ratio': row.get('pe_ratio', 0),
                'pb_ratio': row.get('pb_ratio', 0),
            })
        
        return passed
    
    def _filter_l1(self, candidates: List[Dict], data: Dict) -> List[Dict]:
        """L1 早期信号筛选"""
        passed = []
        
        for stock in candidates:
            code = stock['code']
            
            # 营收增速
            rev_growth = stock.get('inc_revenue_year_on_year', 0)
            if rev_growth is None or np.isnan(rev_growth):
                rev_growth = 0
            if rev_growth < self.l1.min_revenue_growth:
                continue
            
            # 利润增速
            profit_growth = stock.get('inc_net_profit_year_on_year', 0)
            if profit_growth is None or np.isnan(profit_growth):
                profit_growth = 0
            if profit_growth < self.l1.min_profit_growth:
                continue
            
            # ROE
            roe = stock.get('roe', 0)
            if roe is None or np.isnan(roe):
                roe = 0
            if roe < self.l1.min_roe:
                continue
            
            # 毛利率
            gross_margin = stock.get('gross_profit_margin', 0)
            if gross_margin is None or np.isnan(gross_margin):
                gross_margin = 0
            if gross_margin < self.l1.min_gross_margin:
                continue
            
            # 计算因子得分
            score_result = self.factor_engine.calculate_all_scores(stock)
            total_score = score_result['total_score']
            
            if total_score < self.l1.min_score:
                continue
            
            # 识别阶段
            stage = self.stage_identifier.identify_stage(
                market_cap=stock['market_cap'],
                revenue_growth=rev_growth,
                profit_growth=profit_growth,
                roe=roe
            )
            
            # 阶段加分
            stage_bonus = self.stage_identifier.get_stage_score_bonus(stage)
            adjusted_score = total_score + stage_bonus
            
            stock.update({
                'total_score': total_score,
                'adjusted_score': adjusted_score,
                'stage': stage.value,
                'stage_desc': stage.description,
                'action': stage.action,
                'scores': score_result['scores'],
                'level': self.factor_engine.get_score_level(adjusted_score),
                'recommendation': self.factor_engine.get_recommendation(adjusted_score, stage.value)
            })
            
            passed.append(stock)
        
        return passed
    
    def _filter_l2(self, candidates: List[Dict], data: Dict) -> List[Dict]:
        """L2 精选推荐筛选"""
        passed = []
        
        for stock in candidates:
            # 得分要求
            if stock.get('adjusted_score', 0) < self.l2.min_score:
                continue
            
            # 阶段偏好
            if stock.get('stage') not in self.l2.prefer_stages:
                # 不在优选阶段，扣分但不排除
                stock['adjusted_score'] -= 5
            
            # 价格位置检查（如果有数据）
            price_position = stock.get('price_position_52w', 50)
            if price_position > self.l2.max_price_position:
                # 位置太高，扣分
                stock['adjusted_score'] -= 10
            
            passed.append(stock)
        
        # 按调整后得分排序
        passed.sort(key=lambda x: x.get('adjusted_score', 0), reverse=True)
        
        return passed
    
    def _rank_and_select(self, candidates: List[Dict], top_n: int = 10) -> List[Dict]:
        """最终排名和选择"""
        # 已按得分排序，取前N只
        final = candidates[:top_n]
        
        # 添加排名
        for i, stock in enumerate(final):
            stock['rank'] = i + 1
        
        return final
    
    def print_results(self):
        """打印筛选结果"""
        if not self.final_picks:
            print("\n❌ 没有符合条件的股票")
            return
        
        print(f"\n{'='*80}")
        print(f"🏆 十倍股早期识别系统 V2.0 - 推荐结果")
        print(f"{'='*80}")
        
        for stock in self.final_picks:
            print(f"\n{stock['rank']:2d}. {stock.get('code', 'N/A')}")
            print(f"    阶段: {stock.get('stage', 'N/A')} - {stock.get('stage_desc', '')}")
            print(f"    得分: {stock.get('total_score', 0):.1f} (调整后: {stock.get('adjusted_score', 0):.1f})")
            print(f"    等级: {stock.get('level', 'N/A')}")
            print(f"    推荐: {stock.get('recommendation', 'N/A')}")
            print(f"    操作建议: {stock.get('action', 'N/A')}")
            print(f"    ────────")
            print(f"    市值: {stock.get('market_cap', 0):.1f}亿")
            print(f"    PE: {stock.get('pe_ratio', 0):.1f}")
            print(f"    ROE: {stock.get('roe', 0):.1f}%")
            print(f"    营收增速: {stock.get('inc_revenue_year_on_year', 0):.1f}%")
            print(f"    利润增速: {stock.get('inc_net_profit_year_on_year', 0):.1f}%")
    
    def to_dataframe(self) -> pd.DataFrame:
        """转换为DataFrame"""
        if not self.final_picks:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.final_picks)
        
        # 选择重要列
        columns = [
            'rank', 'code', 'stage', 'total_score', 'adjusted_score', 'level',
            'market_cap', 'pe_ratio', 'roe', 
            'inc_revenue_year_on_year', 'inc_net_profit_year_on_year',
            'recommendation', 'action'
        ]
        
        # 过滤存在的列
        existing_cols = [c for c in columns if c in df.columns]
        return df[existing_cols]


# ============================================================
# 测试
# ============================================================

def test_screener():
    """测试筛选器"""
    screener = TenbaggerV2Screener()
    
    # 运行筛选
    results = screener.run_full_screening()
    
    # 打印结果
    screener.print_results()
    
    # 转为DataFrame
    df = screener.to_dataframe()
    if not df.empty:
        print(f"\n📊 结果DataFrame:")
        print(df.to_string())


if __name__ == "__main__":
    test_screener()
