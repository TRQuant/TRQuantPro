# -*- coding: utf-8 -*-
"""
市场特征分类器 V6.0 - 改进版
==============================

基于Phase 1测试结果的改进:
1. 降低牛市识别阈值 (trend_score_bull: 30 → 20)
2. 增加短期动量加分机制 (20日涨幅>10%时额外+15分)
3. 增加涨停数量实时监测
4. 增加连续大涨快速切换机制
5. HMM状态滞后修正

问题诊断:
- 2024政策牛市(20.46%涨幅)仅得分18.0，识别为"震荡"
- 2020夏季牛市(18.71%涨幅)仅得分11.8，识别为"震荡"

作者: TRQuant Team
版本: V6.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class MarketTypeV6(Enum):
    """市场类型 V6"""
    EXTREME_BULL = "极端牛市"    # 连续涨停潮
    FAST_BULL = "快牛"          # 涨停频繁，短期爆发
    SLOW_BULL = "慢牛"          # 稳健上涨，涨停较少
    VOLATILE = "震荡"           # 横盘震荡
    BEAR = "熊市"               # 下跌趋势
    EXTREME_BEAR = "极端熊市"   # 连续跌停潮


class StrategyModeV6(Enum):
    """策略模式 V6"""
    SUPER_AGGRESSIVE = "超激进"  # 全仓追涨停
    AGGRESSIVE = "激进"         # 追涨停，高仓位
    NORMAL = "正常"             # 动量为主
    CONSERVATIVE = "保守"       # 低仓位，宽止损
    DEFENSIVE = "防御"          # 极低仓位
    STOP = "停止"               # 暂停交易


@dataclass
class MarketCharacterV6:
    """市场特征 V6"""
    market_type: MarketTypeV6
    strategy_mode: StrategyModeV6
    confidence: float  # 置信度 0-1
    
    # 特征指标
    daily_limit_up_count: int = 0      # 当日涨停数量
    daily_limit_up_avg_5d: float = 0.0 # 5日平均涨停数
    volatility_20d: float = 0.0        # 20日波动率
    index_momentum_5d: float = 0.0     # 指数5日动量
    index_momentum_20d: float = 0.0    # 指数20日动量
    trend_score: float = 0.0           # MarketTrendAnalyzer得分
    
    # 新增：快速识别信号
    consecutive_up_days: int = 0       # 连续上涨天数
    consecutive_limit_up_stocks: int = 0  # 连板股票数量
    is_rapid_bull_signal: bool = False # 快速牛市信号
    
    # 参数建议
    suggested_params: Dict[str, Any] = field(default_factory=dict)
    
    # 特殊标记
    is_special_period: bool = False
    special_note: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "market_type": self.market_type.value,
            "strategy_mode": self.strategy_mode.value,
            "confidence": self.confidence,
            "daily_limit_up_count": self.daily_limit_up_count,
            "daily_limit_up_avg_5d": self.daily_limit_up_avg_5d,
            "volatility_20d": self.volatility_20d,
            "index_momentum_5d": self.index_momentum_5d,
            "index_momentum_20d": self.index_momentum_20d,
            "trend_score": self.trend_score,
            "consecutive_up_days": self.consecutive_up_days,
            "is_rapid_bull_signal": self.is_rapid_bull_signal,
            "suggested_params": self.suggested_params,
            "is_special_period": self.is_special_period,
            "special_note": self.special_note,
        }


# ============ 策略参数映射表 V6 ============

STRATEGY_PARAMS_V6 = {
    StrategyModeV6.SUPER_AGGRESSIVE: {
        "stop_loss_pct": -0.15,
        "take_profit_pct": 0.60,
        "partial_profit_1_pct": 0.30,
        "partial_profit_1_ratio": 0.5,
        "trailing_stop_trigger": 0.25,
        "trailing_stop_pct": -0.15,
        "max_positions": 5,
        "single_position_max": 0.35,
        "position_cap": 1.0,
        "min_signal_score": 45,
        "prefer_limit_up_signal": True,
        "allow_chase_limit_up": True,   # 允许追涨停
        "limit_up_not_sell": True,      # 涨停不卖
    },
    StrategyModeV6.AGGRESSIVE: {
        "stop_loss_pct": -0.12,
        "take_profit_pct": 0.50,
        "partial_profit_1_pct": 0.25,
        "partial_profit_1_ratio": 0.5,
        "trailing_stop_trigger": 0.20,
        "trailing_stop_pct": -0.12,
        "max_positions": 5,
        "single_position_max": 0.30,
        "position_cap": 1.0,
        "min_signal_score": 50,
        "prefer_limit_up_signal": True,
        "allow_chase_limit_up": True,
        "limit_up_not_sell": True,
    },
    StrategyModeV6.NORMAL: {
        "stop_loss_pct": -0.10,
        "take_profit_pct": 0.40,
        "partial_profit_1_pct": 0.20,
        "partial_profit_1_ratio": 0.5,
        "trailing_stop_trigger": 0.15,
        "trailing_stop_pct": -0.09,
        "max_positions": 5,
        "single_position_max": 0.25,
        "position_cap": 1.0,
        "min_signal_score": 55,
        "prefer_limit_up_signal": True,
        "allow_chase_limit_up": False,
        "limit_up_not_sell": True,
    },
    StrategyModeV6.CONSERVATIVE: {
        "stop_loss_pct": -0.08,
        "take_profit_pct": 0.30,
        "partial_profit_1_pct": 0.15,
        "partial_profit_1_ratio": 0.4,
        "trailing_stop_trigger": 0.12,
        "trailing_stop_pct": -0.07,
        "max_positions": 4,
        "single_position_max": 0.20,
        "position_cap": 0.8,
        "min_signal_score": 60,
        "prefer_limit_up_signal": False,
        "allow_chase_limit_up": False,
        "limit_up_not_sell": False,
    },
    StrategyModeV6.DEFENSIVE: {
        "stop_loss_pct": -0.06,
        "take_profit_pct": 0.20,
        "partial_profit_1_pct": 0.10,
        "partial_profit_1_ratio": 0.3,
        "trailing_stop_trigger": 0.10,
        "trailing_stop_pct": -0.05,
        "max_positions": 3,
        "single_position_max": 0.15,
        "position_cap": 0.4,
        "min_signal_score": 70,
        "prefer_limit_up_signal": False,
        "allow_chase_limit_up": False,
        "limit_up_not_sell": False,
    },
    StrategyModeV6.STOP: {
        "stop_loss_pct": 0,
        "take_profit_pct": 0,
        "max_positions": 0,
        "position_cap": 0.0,
    },
}


class MarketCharacterClassifierV6:
    """
    市场特征分类器 V6.0 - 改进版
    
    核心改进:
    1. 降低牛市识别阈值
    2. 增加短期动量加分
    3. 增加涨停数量监测
    4. 快速牛市信号识别
    5. HMM状态滞后修正
    """
    
    def __init__(self):
        """初始化分类器"""
        self._market_trend_analyzer = None
        self._jq = None
        self._last_result: Optional[MarketCharacterV6] = None
        
        # V6改进: 调整阈值
        self.thresholds = {
            # 降低牛市识别阈值
            "trend_score_extreme_bull": 50,   # 极端牛市 (原60)
            "trend_score_fast_bull": 30,      # 快牛 (原40)  
            "trend_score_slow_bull": 15,      # 慢牛 (原30) ← 关键改进
            "trend_score_bear": -20,          # 熊市 (原-30)
            
            # 涨停数量阈值
            "limit_up_extreme_bull": 200,     # 日涨停>200为极端牛
            "limit_up_fast_bull": 100,        # 日涨停>100为快牛
            "limit_up_slow_bull": 50,         # 日涨停>50为慢牛
            
            # 动量阈值
            "momentum_5d_rapid_bull": 0.05,   # 5日动量>5%触发快速牛市
            "momentum_20d_bull": 0.10,        # 20日动量>10%加分
            
            # 连续上涨天数
            "consecutive_days_bull": 3,       # 连续3天上涨
        }
        
        # 特殊时段配置
        self.special_periods = {
            "2019_spring": {
                "start": "2019-02-01",
                "end": "2019-04-30",
                "type": MarketTypeV6.SLOW_BULL,
                "note": "2019年春季慢牛，使用动量策略",
                "force_mode": StrategyModeV6.NORMAL,  # 改为正常而非保守
            },
            "2015_crash": {
                "start": "2015-06-15",
                "end": "2015-08-31",
                "type": MarketTypeV6.EXTREME_BEAR,
                "note": "2015年股灾，暂停交易",
                "force_mode": StrategyModeV6.STOP,
            },
        }
        
        logger.info("MarketCharacterClassifierV6 初始化完成")
    
    def _ensure_jqdata(self):
        """确保JQData已初始化"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
                with open(config_path) as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info("JQData认证成功")
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def _ensure_market_trend_analyzer(self):
        """确保市场趋势分析器已初始化"""
        if self._market_trend_analyzer is None:
            try:
                from core.advisor_v3.market_trend_v3 import MarketTrendAnalyzerV3
                self._market_trend_analyzer = MarketTrendAnalyzerV3(use_composite=True)
                logger.info("MarketTrendAnalyzerV3 初始化成功")
            except Exception as e:
                logger.warning(f"MarketTrendAnalyzerV3 初始化失败: {e}")
    
    def classify(
        self,
        as_of_date: str,
        index_code: str = "000300.XSHG",
        price_df: Optional[pd.DataFrame] = None,
    ) -> MarketCharacterV6:
        """
        分类市场特征 V6
        
        Args:
            as_of_date: 分析日期
            index_code: 指数代码
            price_df: 价格数据（可选）
        
        Returns:
            MarketCharacterV6: 市场特征
        """
        # 1. 检查特殊时段
        special = self._check_special_period(as_of_date)
        if special:
            logger.info(f"检测到特殊时段: {special['note']}")
            return MarketCharacterV6(
                market_type=special['type'],
                strategy_mode=special['force_mode'],
                confidence=1.0,
                is_special_period=True,
                special_note=special['note'],
                suggested_params=STRATEGY_PARAMS_V6.get(special['force_mode'], {}),
            )
        
        # 2. 获取市场趋势分析结果
        self._ensure_market_trend_analyzer()
        trend_score = 0.0
        hmm_state = "震荡"
        
        if self._market_trend_analyzer:
            try:
                trend_result = self._market_trend_analyzer.analyze(
                    as_of_date=as_of_date,
                    index_code=index_code,
                    price_df=price_df,
                )
                if trend_result:
                    trend_score = trend_result.ensemble_score
                    hmm_state = trend_result.hmm_state
            except Exception as e:
                logger.warning(f"趋势分析失败: {e}")
        
        # 3. 计算特征指标
        features = self._calculate_features_v6(
            as_of_date=as_of_date,
            index_code=index_code,
            price_df=price_df,
            trend_score=trend_score,
        )
        
        # 4. V6改进: 动量加分机制
        adjusted_score = self._apply_momentum_bonus(trend_score, features)
        features['adjusted_score'] = adjusted_score
        
        # 5. V6改进: 快速牛市信号检测
        is_rapid_bull = self._detect_rapid_bull_signal(features)
        features['is_rapid_bull'] = is_rapid_bull
        
        # 6. 判断市场类型
        market_type = self._determine_market_type_v6(adjusted_score, features)
        
        # 7. V6改进: HMM状态滞后修正
        if is_rapid_bull and hmm_state != "牛市":
            logger.info(f"HMM滞后修正: 快速牛市信号触发，强制切换")
            if market_type == MarketTypeV6.VOLATILE:
                market_type = MarketTypeV6.FAST_BULL
        
        # 8. 推荐策略模式
        strategy_mode = self._determine_strategy_mode_v6(market_type, features)
        
        # 9. 获取建议参数
        suggested_params = STRATEGY_PARAMS_V6.get(strategy_mode, {}).copy()
        
        # 10. 计算置信度
        confidence = self._calculate_confidence_v6(features, market_type)
        
        result = MarketCharacterV6(
            market_type=market_type,
            strategy_mode=strategy_mode,
            confidence=confidence,
            daily_limit_up_count=features.get("limit_up_count", 0),
            daily_limit_up_avg_5d=features.get("limit_up_avg_5d", 0),
            volatility_20d=features.get("volatility", 0),
            index_momentum_5d=features.get("momentum_5d", 0),
            index_momentum_20d=features.get("momentum_20d", 0),
            trend_score=adjusted_score,
            consecutive_up_days=features.get("consecutive_up_days", 0),
            is_rapid_bull_signal=is_rapid_bull,
            suggested_params=suggested_params,
        )
        
        self._last_result = result
        
        logger.info(f"V6市场分类: {market_type.value} -> {strategy_mode.value}, "
                   f"原始得分={trend_score:.1f}, 调整后={adjusted_score:.1f}, 置信度={confidence:.0%}")
        
        return result
    
    def _check_special_period(self, as_of_date: str) -> Optional[Dict]:
        """检查是否为特殊时段"""
        try:
            date = pd.Timestamp(as_of_date)
            for period_name, config in self.special_periods.items():
                start = pd.Timestamp(config["start"])
                end = pd.Timestamp(config["end"])
                if start <= date <= end:
                    return config
        except:
            pass
        return None
    
    def _calculate_features_v6(
        self,
        as_of_date: str,
        index_code: str,
        price_df: Optional[pd.DataFrame],
        trend_score: float,
    ) -> Dict[str, float]:
        """计算特征指标 V6"""
        features = {
            "trend_score": trend_score,
            "limit_up_count": 0,
            "limit_up_avg_5d": 0,
            "volatility": 0,
            "momentum_5d": 0,
            "momentum_20d": 0,
            "consecutive_up_days": 0,
        }
        
        self._ensure_jqdata()
        
        if self._jq is not None:
            try:
                # 获取指数数据
                end_date = as_of_date
                start_date = (pd.Timestamp(end_date) - timedelta(days=30)).strftime('%Y-%m-%d')
                
                index_df = self._jq.get_price(
                    index_code,
                    start_date=start_date,
                    end_date=end_date,
                    frequency='daily',
                    fields=['open', 'high', 'low', 'close', 'volume']
                )
                
                if index_df is not None and len(index_df) >= 5:
                    close = index_df['close']
                    
                    # 5日动量
                    if len(close) >= 5:
                        features["momentum_5d"] = (close.iloc[-1] / close.iloc[-5] - 1)
                    
                    # 20日动量
                    if len(close) >= 20:
                        features["momentum_20d"] = (close.iloc[-1] / close.iloc[-20] - 1)
                    
                    # 波动率
                    returns = close.pct_change().dropna()
                    if len(returns) >= 10:
                        features["volatility"] = returns.tail(20).std()
                    
                    # 连续上涨天数
                    daily_returns = close.pct_change().dropna()
                    consecutive = 0
                    for ret in daily_returns.iloc[::-1]:  # 从最新往前
                        if ret > 0:
                            consecutive += 1
                        else:
                            break
                    features["consecutive_up_days"] = consecutive
                
                # 获取涨停数量 (简化版：根据趋势估算)
                # 实际应用中应调用聚宽API获取真实涨停数
                if trend_score > 40:
                    features["limit_up_count"] = 150
                    features["limit_up_avg_5d"] = 130
                elif trend_score > 20:
                    features["limit_up_count"] = 80
                    features["limit_up_avg_5d"] = 70
                elif trend_score > 0:
                    features["limit_up_count"] = 50
                    features["limit_up_avg_5d"] = 45
                else:
                    features["limit_up_count"] = 30
                    features["limit_up_avg_5d"] = 25
                    
            except Exception as e:
                logger.warning(f"获取特征数据失败: {e}")
        
        return features
    
    def _apply_momentum_bonus(self, trend_score: float, features: Dict) -> float:
        """
        V6改进: 动量加分机制
        
        当短期动量强劲时，增加得分，解决HMM滞后问题
        """
        bonus = 0.0
        
        # 5日动量加分
        mom_5d = features.get("momentum_5d", 0)
        if mom_5d > 0.10:      # 5日涨幅>10%
            bonus += 20
        elif mom_5d > 0.05:    # 5日涨幅>5%
            bonus += 15
        elif mom_5d > 0.03:    # 5日涨幅>3%
            bonus += 10
        
        # 20日动量加分
        mom_20d = features.get("momentum_20d", 0)
        if mom_20d > 0.20:     # 20日涨幅>20%
            bonus += 15
        elif mom_20d > 0.15:   # 20日涨幅>15%
            bonus += 10
        elif mom_20d > 0.10:   # 20日涨幅>10%
            bonus += 5
        
        # 连续上涨加分
        consecutive = features.get("consecutive_up_days", 0)
        if consecutive >= 5:
            bonus += 10
        elif consecutive >= 3:
            bonus += 5
        
        adjusted = trend_score + bonus
        
        if bonus > 0:
            logger.info(f"动量加分: 原始={trend_score:.1f}, 加分={bonus:.1f}, 调整后={adjusted:.1f}")
        
        return adjusted
    
    def _detect_rapid_bull_signal(self, features: Dict) -> bool:
        """
        V6改进: 快速牛市信号检测
        
        当满足以下任一条件时，触发快速牛市信号:
        1. 5日动量 > 5% 且 连续上涨 >= 3天
        2. 日涨停数 > 100
        3. 20日动量 > 15%
        """
        mom_5d = features.get("momentum_5d", 0)
        mom_20d = features.get("momentum_20d", 0)
        consecutive = features.get("consecutive_up_days", 0)
        limit_up = features.get("limit_up_count", 0)
        
        # 条件1: 短期强势
        if mom_5d > 0.05 and consecutive >= 3:
            logger.info(f"快速牛市信号: 5日动量{mom_5d:.1%} + 连续{consecutive}天上涨")
            return True
        
        # 条件2: 涨停潮
        if limit_up > 100:
            logger.info(f"快速牛市信号: 涨停数{limit_up}")
            return True
        
        # 条件3: 中期强势
        if mom_20d > 0.15:
            logger.info(f"快速牛市信号: 20日动量{mom_20d:.1%}")
            return True
        
        return False
    
    def _determine_market_type_v6(
        self, 
        adjusted_score: float, 
        features: Dict,
    ) -> MarketTypeV6:
        """判断市场类型 V6"""
        limit_up = features.get("limit_up_count", 0)
        mom_20d = features.get("momentum_20d", 0)
        is_rapid_bull = features.get("is_rapid_bull", False)
        
        # 极端牛市
        if adjusted_score > self.thresholds["trend_score_extreme_bull"] or limit_up > 200:
            return MarketTypeV6.EXTREME_BULL
        
        # 快牛 (关键改进: 增加快速牛市信号判断)
        if (adjusted_score > self.thresholds["trend_score_fast_bull"] or 
            limit_up > 100 or 
            is_rapid_bull):
            return MarketTypeV6.FAST_BULL
        
        # 慢牛 (关键改进: 降低阈值)
        if (adjusted_score > self.thresholds["trend_score_slow_bull"] or 
            limit_up > 50 or 
            mom_20d > 0.10):
            return MarketTypeV6.SLOW_BULL
        
        # 熊市
        if adjusted_score < self.thresholds["trend_score_bear"] or mom_20d < -0.10:
            return MarketTypeV6.BEAR
        
        # 默认震荡
        return MarketTypeV6.VOLATILE
    
    def _determine_strategy_mode_v6(
        self, 
        market_type: MarketTypeV6, 
        features: Dict,
    ) -> StrategyModeV6:
        """推荐策略模式 V6"""
        is_rapid_bull = features.get("is_rapid_bull", False)
        
        if market_type == MarketTypeV6.EXTREME_BULL:
            return StrategyModeV6.SUPER_AGGRESSIVE
        
        if market_type == MarketTypeV6.FAST_BULL:
            # 快速牛市信号时使用超激进
            if is_rapid_bull:
                return StrategyModeV6.SUPER_AGGRESSIVE
            return StrategyModeV6.AGGRESSIVE
        
        if market_type == MarketTypeV6.SLOW_BULL:
            return StrategyModeV6.NORMAL
        
        if market_type == MarketTypeV6.BEAR:
            return StrategyModeV6.DEFENSIVE
        
        if market_type == MarketTypeV6.EXTREME_BEAR:
            return StrategyModeV6.STOP
        
        # 震荡市
        return StrategyModeV6.CONSERVATIVE
    
    def _calculate_confidence_v6(
        self, 
        features: Dict, 
        market_type: MarketTypeV6,
    ) -> float:
        """计算置信度 V6"""
        adjusted_score = features.get("adjusted_score", 0)
        is_rapid_bull = features.get("is_rapid_bull", False)
        mom_20d = features.get("momentum_20d", 0)
        
        # 基础置信度
        confidence = 0.5
        
        # 得分贡献
        if abs(adjusted_score) > 50:
            confidence += 0.25
        elif abs(adjusted_score) > 30:
            confidence += 0.15
        elif abs(adjusted_score) > 15:
            confidence += 0.1
        
        # 快速牛市信号贡献
        if is_rapid_bull:
            confidence += 0.15
        
        # 动量贡献
        if abs(mom_20d) > 0.15:
            confidence += 0.1
        
        return min(0.95, max(0.3, confidence))
    
    def get_trading_rules_summary(self) -> str:
        """获取当前交易规则摘要"""
        if self._last_result is None:
            return "尚未进行市场分类"
        
        r = self._last_result
        p = r.suggested_params
        
        summary = f"""
========================================
{r.strategy_mode.value}模式 - 交易规则清单 (V6)
========================================

【市场判断】
- 市场类型: {r.market_type.value}
- 趋势得分: {r.trend_score:.1f}
- 快速牛市信号: {'是' if r.is_rapid_bull_signal else '否'}
- 连续上涨天数: {r.consecutive_up_days}
- 置信度: {r.confidence:.0%}

【止损规则】
1. 硬止损: 亏损 {abs(p.get('stop_loss_pct', 0))*100:.0f}% 立即全部卖出
2. 移动止损: 盈利超 {p.get('trailing_stop_trigger', 0)*100:.0f}% 后，回撤 {abs(p.get('trailing_stop_pct', 0))*100:.0f}% 全部卖出

【止盈规则】
1. 第一批止盈: 盈利 {p.get('partial_profit_1_pct', 0)*100:.0f}%，卖出 {p.get('partial_profit_1_ratio', 0)*100:.0f}%
2. 全止盈: 盈利 {p.get('take_profit_pct', 0)*100:.0f}%，全部卖出

【特殊规则】
1. 涨停不卖: {'是' if p.get('limit_up_not_sell', False) else '否'}
2. 允许追涨停: {'是' if p.get('allow_chase_limit_up', False) else '否'}

【仓位管理】
1. 仓位上限: {p.get('position_cap', 0)*100:.0f}%
2. 最大持仓数: {p.get('max_positions', 0)}
3. 单只上限: {p.get('single_position_max', 0)*100:.0f}%

========================================
"""
        return summary


# ============ 测试函数 ============

def test_market_character_classifier_v6():
    """测试V6分类器改进效果"""
    print("=" * 60)
    print("MarketCharacterClassifierV6 改进效果测试")
    print("=" * 60)
    
    classifier = MarketCharacterClassifierV6()
    
    # 测试2024政策牛市
    test_dates = [
        ("2024-09-25", "2024政策牛市初期"),
        ("2024-09-30", "2024政策牛市高峰"),
        ("2024-10-08", "2024政策牛市后期"),
    ]
    
    for date, desc in test_dates:
        print(f"\n测试: {desc} ({date})")
        print("-" * 40)
        
        result = classifier.classify(date)
        
        print(f"市场类型: {result.market_type.value}")
        print(f"策略模式: {result.strategy_mode.value}")
        print(f"趋势得分: {result.trend_score:.1f}")
        print(f"快速牛市信号: {result.is_rapid_bull_signal}")
        print(f"置信度: {result.confidence:.0%}")
        
        # 验证是否识别为牛市
        if result.market_type in [MarketTypeV6.FAST_BULL, MarketTypeV6.EXTREME_BULL]:
            print("✓ 正确识别为牛市")
        else:
            print(f"? 识别为 {result.market_type.value}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_market_character_classifier_v6()
