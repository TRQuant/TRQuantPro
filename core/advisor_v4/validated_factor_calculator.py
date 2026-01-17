#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
已验证因子计算器（基于历史10%+高收益案例）
==========================================

核心原则：
1. 所有因子必须基于历史10%+高收益案例提取和验证
2. 每个因子都要有理论假设和逻辑
3. 不能简单堆砌聚宽因子库
4. 优先使用已验证有效的因子

因子来源：
- 基于438个历史10%+周收益案例的因子分析
- 参考：docs/HIGH_RETURN_FACTOR_RESEARCH.md
- 核心因子：20日动量、相对位置、市值、5日动量、换手率、ROE、增长率

理论假设：
1. 动量驱动假设：适度上涨趋势（20日动量5%~30%）能延续
2. 低位反弹假设：相对位置<80%的股票反弹概率高
3. 市值弹性假设：中小市值（30~200亿）弹性大，易被资金推动
4. 短期确认假设：5日动量(-5%~10%)确认短期趋势
5. 流动性假设：换手率反映市场关注度和资金流入
6. 基本面底线假设：ROE>0确保基本面不恶化
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class FactorHypothesis:
    """因子假设和理论"""
    name: str
    theory: str  # 理论假设
    logic: str   # 逻辑说明
    validation: str  # 验证结果（基于历史案例）
    weight: float = 1.0  # 权重（基于有效性排序）


# 所有已验证因子名称（导出供其他模块使用）
ALL_VALIDATED_FACTORS = [
    "momentum_20d",
    "rel_position",
    "market_cap",
    "momentum_5d",
    "turnover_rate",
    "roe",
    "growth",
]

# 已验证因子定义（基于438个10%+案例的分析）
VALIDATED_FACTORS = {
    "momentum_20d": FactorHypothesis(
        name="20日动量",
        theory="动量驱动假设：适度上涨趋势能延续，但过热（>30%）风险高",
        logic="历史案例显示，20日动量在5%~30%区间的股票，平均收益21.59%，命中率最高",
        validation="99个动量驱动型案例，平均收益21.59%，有效性⭐⭐⭐⭐⭐",
        weight=1.0  # 最重要因子
    ),
    "rel_position": FactorHypothesis(
        name="相对位置",
        theory="低位反弹假设：相对位置<80%的股票反弹概率高，避免追高",
        logic="248个低位反弹型案例显示，相对位置在1.2%~55.1%区间的股票，平均收益15.62%",
        validation="低位反弹型案例占比56.6%，有效性⭐⭐⭐⭐",
        weight=0.9
    ),
    "market_cap": FactorHypothesis(
        name="市值",
        theory="市值弹性假设：中小市值（30~200亿）弹性大，易被资金推动",
        logic="166个小市值型案例（<50亿）占比37.9%，平均收益17.47%，弹性明显大于大盘股",
        validation="小市值案例占比37.9%，有效性⭐⭐⭐⭐",
        weight=0.85
    ),
    "momentum_5d": FactorHypothesis(
        name="5日动量",
        theory="短期确认假设：5日动量(-5%~10%)确认短期趋势，避免过热",
        logic="适度动量（-5%~10%）既能捕捉趋势，又避免追高，历史验证命中率高",
        validation="短期动量确认，有效性⭐⭐⭐",
        weight=0.75
    ),
    "turnover_rate": FactorHypothesis(
        name="换手率",
        theory="流动性假设：换手率反映市场关注度和资金流入",
        logic="高换手率表明市场关注度高，资金流入活跃，有利于价格上涨",
        validation="流动性因子，有效性⭐⭐⭐",
        weight=0.7
    ),
    "roe": FactorHypothesis(
        name="ROE",
        theory="基本面底线假设：ROE>0确保基本面不恶化，避免踩雷",
        logic="虽然高收益主要来自动量而非价值，但ROE>0是底线，避免基本面恶化股票",
        validation="基本面筛选，有效性⭐⭐",
        weight=0.5
    ),
    "growth": FactorHypothesis(
        name="净利润增长率",
        theory="成长性假设：高增长股票有业绩支撑，但非必要条件",
        logic="优质成长型案例仅占2.5%，说明高收益主要来自动量而非价值，但增长>0是加分项",
        validation="成长性因子，有效性⭐⭐",
        weight=0.4
    ),
}


class ValidatedFactorCalculator:
    """基于历史验证的因子计算器"""

    def __init__(self, verbose: bool = True):
        """
        初始化已验证因子计算器

        Args:
            verbose: 是否输出详细信息
        """
        self.verbose = verbose
        self.jq = None
        self._init_jqdata()

    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager

            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config("jqdata")
            jq.auth(jq_config.get("username"), jq_config.get("password"))
            self.jq = jq
            if self.verbose:
                print("✅ JQData连接成功 (ValidatedFactorCalculator)")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
            raise

    def calculate_momentum_20d(self, codes: List[str], date: str) -> pd.Series:
        """
        计算20日动量（已验证核心因子）

        理论假设：适度上涨趋势（5%~30%）能延续
        验证结果：99个动量驱动型案例，平均收益21.59%
        """
        try:
            prices = self.jq.get_price(
                codes,
                end_date=date,
                count=21,
                frequency="daily",
                fields=["close"],
                panel=False,
                fq="post",
            )

            if prices is None or prices.empty:
                return pd.Series(index=codes, dtype=float)

            # 计算20日动量
            momentum = {}
            for code in codes:
                code_prices = prices[prices["code"] == code]["close"]
                if len(code_prices) >= 21:
                    momentum[code] = (code_prices.iloc[-1] / code_prices.iloc[0] - 1.0) * 100.0
                else:
                    momentum[code] = 0.0

            return pd.Series(momentum)

        except Exception as e:
            logger.warning(f"计算20日动量失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_rel_position(self, codes: List[str], date: str) -> pd.Series:
        """
        计算相对位置（已验证核心因子）

        理论假设：相对位置<80%的股票反弹概率高
        验证结果：248个低位反弹型案例，平均收益15.62%
        """
        try:
            prices = self.jq.get_price(
                codes,
                end_date=date,
                count=21,
                frequency="daily",
                fields=["high", "low", "close"],
                panel=False,
                fq="post",
            )

            if prices is None or prices.empty:
                return pd.Series(index=codes, dtype=float)

            # 计算相对位置
            rel_pos = {}
            for code in codes:
                code_data = prices[prices["code"] == code]
                if len(code_data) >= 20:
                    high_20 = code_data["high"].tail(20).max()
                    low_20 = code_data["low"].tail(20).min()
                    close = code_data["close"].iloc[-1]

                    if high_20 > low_20:
                        rel_pos[code] = (close - low_20) / (high_20 - low_20) * 100.0
                    else:
                        rel_pos[code] = 50.0
                else:
                    rel_pos[code] = 50.0

            return pd.Series(rel_pos)

        except Exception as e:
            logger.warning(f"计算相对位置失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_momentum_5d(self, codes: List[str], date: str) -> pd.Series:
        """
        计算5日动量（已验证因子）

        理论假设：短期动量(-5%~10%)确认趋势，避免过热
        验证结果：适度动量区间命中率高
        """
        try:
            prices = self.jq.get_price(
                codes,
                end_date=date,
                count=6,
                frequency="daily",
                fields=["close"],
                panel=False,
                fq="post",
            )

            if prices is None or prices.empty:
                return pd.Series(index=codes, dtype=float)

            momentum = {}
            for code in codes:
                code_prices = prices[prices["code"] == code]["close"]
                if len(code_prices) >= 6:
                    momentum[code] = (code_prices.iloc[-1] / code_prices.iloc[0] - 1.0) * 100.0
                else:
                    momentum[code] = 0.0

            return pd.Series(momentum)

        except Exception as e:
            logger.warning(f"计算5日动量失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_market_cap(self, codes: List[str], date: str) -> pd.Series:
        """
        计算市值（已验证因子）

        理论假设：中小市值（30~200亿）弹性大
        验证结果：166个小市值案例占比37.9%，平均收益17.47%
        """
        try:
            q = self.jq.query(self.jq.valuation.code, self.jq.valuation.market_cap).filter(
                self.jq.valuation.code.in_(codes)
            )
            df = self.jq.get_fundamentals(q, date=date)

            if df is None or df.empty:
                return pd.Series(index=codes, dtype=float)

            # 市值单位：亿元
            market_cap_dict = dict(zip(df["code"], df["market_cap"] / 100000000))
            return pd.Series(market_cap_dict).reindex(codes, fill_value=0.0)

        except Exception as e:
            logger.warning(f"计算市值失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_turnover_rate(self, codes: List[str], date: str) -> pd.Series:
        """
        计算换手率（已验证因子）

        理论假设：换手率反映市场关注度和资金流入
        验证结果：流动性因子，有效性⭐⭐⭐
        """
        try:
            q = self.jq.query(
                self.jq.valuation.code, self.jq.valuation.turnover_ratio
            ).filter(self.jq.valuation.code.in_(codes))
            df = self.jq.get_fundamentals(q, date=date)

            if df is None or df.empty:
                return pd.Series(index=codes, dtype=float)

            turnover_dict = dict(zip(df["code"], df["turnover_ratio"]))
            return pd.Series(turnover_dict).reindex(codes, fill_value=0.0)

        except Exception as e:
            logger.warning(f"计算换手率失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_roe(self, codes: List[str], date: str) -> pd.Series:
        """
        计算ROE（已验证因子）

        理论假设：ROE>0确保基本面不恶化
        验证结果：基本面底线，有效性⭐⭐
        """
        try:
            q = self.jq.query(self.jq.indicator.code, self.jq.indicator.roe).filter(
                self.jq.indicator.code.in_(codes)
            )
            df = self.jq.get_fundamentals(q, date=date)

            if df is None or df.empty:
                return pd.Series(index=codes, dtype=float)

            roe_dict = dict(zip(df["code"], df["roe"]))
            return pd.Series(roe_dict).reindex(codes, fill_value=0.0)

        except Exception as e:
            logger.warning(f"计算ROE失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_growth(self, codes: List[str], date: str) -> pd.Series:
        """
        计算净利润增长率（已验证因子）

        理论假设：增长>0是加分项，但非必要条件
        验证结果：成长性因子，有效性⭐⭐
        """
        try:
            q = self.jq.query(
                self.jq.indicator.code, self.jq.indicator.inc_net_profit_year_on_year
            ).filter(self.jq.indicator.code.in_(codes))
            df = self.jq.get_fundamentals(q, date=date)

            if df is None or df.empty:
                return pd.Series(index=codes, dtype=float)

            growth_dict = dict(zip(df["code"], df["inc_net_profit_year_on_year"]))
            return pd.Series(growth_dict).reindex(codes, fill_value=0.0)

        except Exception as e:
            logger.warning(f"计算净利润增长率失败: {e}")
            return pd.Series(index=codes, dtype=float)

    def calculate_all_validated_factors(
        self,
        codes: List[str],
        date: str,
        factor_selection: Optional[List[str]] = None,
        factor_weights: Optional[Dict[str, float]] = None,
    ) -> pd.DataFrame:
        """
        计算已验证因子（支持动态因子选择和权重配置）

        Args:
            codes: 股票代码列表
            date: 日期
            factor_selection: 因子选择（如果为None，使用全部7个因子）
            factor_weights: 因子权重（如果为None，使用默认权重）

        Returns:
            DataFrame包含选择的已验证因子和综合得分
        """
        if not codes:
            return pd.DataFrame(columns=["code"])

        # 默认使用全部因子
        if factor_selection is None:
            factor_selection = list(ALL_VALIDATED_FACTORS)
        
        # 默认使用理论权重
        if factor_weights is None:
            factor_weights = {f: VALIDATED_FACTORS[f].weight for f in factor_selection}
            total = sum(factor_weights.values())
            factor_weights = {f: w / total for f, w in factor_weights.items()}

        df = pd.DataFrame({"code": codes})

        # 计算各因子（仅计算选择的因子）
        if self.verbose:
            print(f"计算已验证因子（选择 {len(factor_selection)} 个因子）...")

        # 因子计算映射
        factor_calculators = {
            "momentum_20d": self.calculate_momentum_20d,
            "rel_position": self.calculate_rel_position,
            "market_cap": self.calculate_market_cap,
            "momentum_5d": self.calculate_momentum_5d,
            "turnover_rate": self.calculate_turnover_rate,
            "roe": self.calculate_roe,
            "growth": self.calculate_growth,
        }

        # 计算选择的因子
        for factor in factor_selection:
            if factor in factor_calculators:
                df[factor] = factor_calculators[factor](codes, date)

        # 计算综合得分（使用自定义权重）
        df = self._calculate_validated_score(df, factor_selection, factor_weights)

        return df

    def _calculate_validated_score(
        self,
        df: pd.DataFrame,
        factor_selection: Optional[List[str]] = None,
        factor_weights: Optional[Dict[str, float]] = None,
    ) -> pd.DataFrame:
        """
        计算已验证因子综合得分（支持动态权重）

        Args:
            df: 包含因子值的DataFrame
            factor_selection: 因子选择（如果为None，使用全部因子）
            factor_weights: 因子权重（如果为None，使用默认权重）
        """
        if factor_selection is None:
            factor_selection = list(ALL_VALIDATED_FACTORS)
        
        if factor_weights is None:
            factor_weights = {f: VALIDATED_FACTORS[f].weight for f in factor_selection}
            total = sum(factor_weights.values())
            factor_weights = {f: w / total for f, w in factor_weights.items()}

        scores = pd.Series(0.0, index=df.index)

        # 因子评分函数映射
        score_functions = {
            "momentum_20d": self._score_momentum_20d,
            "rel_position": self._score_rel_position,
            "market_cap": self._score_market_cap,
            "momentum_5d": self._score_momentum_5d,
            "turnover_rate": self._score_turnover_rate,
            "roe": self._score_roe,
            "growth": self._score_growth,
        }

        # 计算加权得分
        for factor in factor_selection:
            if factor in df.columns and factor in score_functions:
                factor_score = df[factor].apply(score_functions[factor])
                weight = factor_weights.get(factor, 0.0)
                scores += factor_score * weight

        # 归一化到0-100分
        total_weight = sum(factor_weights.values())
        if total_weight > 0:
            df["validated_score"] = (scores / total_weight * 100).clip(0, 100)
        else:
            df["validated_score"] = 50.0  # 默认得分

        return df

    def _score_momentum_20d(self, value: float) -> float:
        """20日动量评分（核心因子）"""
        if np.isnan(value):
            return 0.0

        # 最优区间：5%~30%
        if 5.0 <= value <= 30.0:
            # 中心值17.5%得分最高
            center = 17.5
            distance = abs(value - center)
            return max(0.0, 1.0 - distance / 12.5)  # 距离中心越近得分越高
        elif value < 5.0:
            # 低于5%：线性递减
            return max(0.0, value / 5.0 * 0.5)
        else:
            # 高于30%：过热，得分递减
            return max(0.0, 1.0 - (value - 30.0) / 20.0)

    def _score_rel_position(self, value: float) -> float:
        """相对位置评分（核心因子）"""
        if np.isnan(value):
            return 0.5

        # 最优区间：<80%
        if value <= 80.0:
            # 越低越好（但不要极端低，避免垃圾股）
            if value <= 30.0:
                return 1.0  # 低位，得分最高
            else:
                return 1.0 - (value - 30.0) / 50.0 * 0.3  # 30%~80%线性递减
        else:
            # 高于80%：高位，得分低
            return max(0.0, 1.0 - (value - 80.0) / 20.0)

    def _score_market_cap(self, value: float) -> float:
        """市值评分（核心因子）"""
        if np.isnan(value) or value <= 0:
            return 0.0

        # 最优区间：30~200亿
        if 30.0 <= value <= 200.0:
            # 中心值115亿得分最高
            center = 115.0
            distance = abs(value - center)
            return max(0.0, 1.0 - distance / 85.0)
        elif value < 30.0:
            # 太小：风险高
            return max(0.0, value / 30.0 * 0.7)
        else:
            # 太大：弹性小
            return max(0.0, 1.0 - (value - 200.0) / 300.0)

    def _score_momentum_5d(self, value: float) -> float:
        """5日动量评分（确认因子）"""
        if np.isnan(value):
            return 0.5

        # 最优区间：-5%~10%
        if -5.0 <= value <= 10.0:
            # 中心值2.5%得分最高
            center = 2.5
            distance = abs(value - center)
            return max(0.0, 1.0 - distance / 7.5)
        elif value < -5.0:
            # 过度回调
            return max(0.0, (value + 10.0) / 5.0 * 0.5)
        else:
            # 过热
            return max(0.0, 1.0 - (value - 10.0) / 15.0)

    def _score_turnover_rate(self, value: float) -> float:
        """换手率评分（流动性因子）"""
        if np.isnan(value) or value <= 0:
            return 0.0

        # 适度换手（2%~10%）得分高
        if 2.0 <= value <= 10.0:
            return 1.0
        elif value < 2.0:
            # 流动性不足
            return value / 2.0 * 0.7
        else:
            # 过度换手（可能是出货）
            return max(0.0, 1.0 - (value - 10.0) / 20.0)

    def _score_roe(self, value: float) -> float:
        """ROE评分（基本面底线）"""
        if np.isnan(value):
            return 0.0

        # >0得分高
        if value > 0:
            return min(1.0, value / 10.0)  # 最高10%ROE得满分
        else:
            return 0.0

    def _score_growth(self, value: float) -> float:
        """净利润增长率评分（成长性因子）"""
        if np.isnan(value):
            return 0.0

        # >0得分高
        if value > 0:
            return min(1.0, value / 100.0)  # 最高100%增长得满分
        else:
            return 0.0

    def get_factor_hypotheses(self) -> Dict[str, FactorHypothesis]:
        """获取所有因子的假设和理论"""
        return VALIDATED_FACTORS.copy()
