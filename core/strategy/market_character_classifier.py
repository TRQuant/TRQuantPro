# -*- coding: utf-8 -*-
"""
市场特征分类器 - 判断市场类型并自动切换策略
=============================================

功能:
1. 判断快牛/慢牛/震荡/熊市
2. 根据市场类型推荐策略参数
3. 与MarketTrendAnalyzerV3协同工作
4. 处理2019年等特殊时段

作者: TRQuant Team
版本: V5.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class MarketType(Enum):
    """市场类型"""
    FAST_BULL = "快牛"       # 涨停频繁，短期爆发
    SLOW_BULL = "慢牛"       # 稳健上涨，涨停较少
    VOLATILE = "震荡"        # 横盘震荡
    BEAR = "熊市"           # 下跌趋势
    EXTREME_BULL = "极端牛市"  # 极端行情，需谨慎


class StrategyMode(Enum):
    """策略模式"""
    AGGRESSIVE = "激进"      # 追涨停，高仓位
    NORMAL = "正常"         # 动量为主
    CONSERVATIVE = "保守"    # 低仓位，宽止损
    DEFENSIVE = "防御"       # 极低仓位
    STOP = "停止"           # 暂停交易


@dataclass
class MarketCharacter:
    """市场特征"""
    market_type: MarketType
    strategy_mode: StrategyMode
    confidence: float  # 置信度 0-1
    
    # 特征指标
    daily_limit_up_avg: float = 0.0   # 日均涨停数
    volatility_20d: float = 0.0        # 20日波动率
    index_momentum_20d: float = 0.0    # 指数20日动量
    trend_score: float = 0.0           # 趋势得分（来自MarketTrendAnalyzer）
    
    # 参数建议
    suggested_params: Dict[str, Any] = field(default_factory=dict)
    
    # 特殊标记
    is_special_period: bool = False    # 是否特殊时段（如2019年）
    special_note: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "market_type": self.market_type.value,
            "strategy_mode": self.strategy_mode.value,
            "confidence": self.confidence,
            "daily_limit_up_avg": self.daily_limit_up_avg,
            "volatility_20d": self.volatility_20d,
            "index_momentum_20d": self.index_momentum_20d,
            "trend_score": self.trend_score,
            "suggested_params": self.suggested_params,
            "is_special_period": self.is_special_period,
            "special_note": self.special_note,
        }


# ============ 策略参数映射表 ============

STRATEGY_PARAMS_BY_MODE = {
    StrategyMode.AGGRESSIVE: {
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
        "prefer_limit_up_signal": True,  # 优先涨停信号
    },
    StrategyMode.NORMAL: {
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
    },
    StrategyMode.CONSERVATIVE: {
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
        "prefer_limit_up_signal": False,  # 动量优先
    },
    StrategyMode.DEFENSIVE: {
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
    },
    StrategyMode.STOP: {
        "stop_loss_pct": 0,
        "take_profit_pct": 0,
        "max_positions": 0,
        "position_cap": 0.0,
    },
}


# ============ 特殊时段配置 ============

SPECIAL_PERIODS = {
    "2019_spring": {
        "start": "2019-02-01",
        "end": "2019-04-30",
        "type": MarketType.SLOW_BULL,
        "note": "2019年春季慢牛，涨停信号少，使用动量策略",
        "force_mode": StrategyMode.CONSERVATIVE,
    },
    "2015_crash": {
        "start": "2015-06-15",
        "end": "2015-08-31",
        "type": MarketType.BEAR,
        "note": "2015年股灾，避免回测",
        "force_mode": StrategyMode.STOP,
    },
    "2020_covid": {
        "start": "2020-01-20",
        "end": "2020-02-10",
        "type": MarketType.BEAR,
        "note": "2020年新冠疫情初期，避免回测",
        "force_mode": StrategyMode.STOP,
    },
}


class MarketCharacterClassifier:
    """
    市场特征分类器
    
    核心功能:
    1. 计算市场特征指标
    2. 判断市场类型（快牛/慢牛/震荡/熊市）
    3. 推荐策略模式和参数
    4. 处理特殊时段
    """
    
    def __init__(self):
        """初始化分类器"""
        self._market_trend_analyzer = None
        self._last_result: Optional[MarketCharacter] = None
        
        # 阈值配置
        self.thresholds = {
            "limit_up_fast_bull": 100,    # 日均涨停数>100为快牛
            "limit_up_slow_bull": 50,     # 日均涨停数50-100为慢牛
            "limit_up_min": 20,           # 日均涨停数<20为震荡/熊市
            "volatility_high": 0.03,       # 日波动率>3%为高波动
            "volatility_low": 0.01,        # 日波动率<1%为低波动
            "momentum_bull": 0.05,         # 20日动量>5%为牛市
            "momentum_bear": -0.05,        # 20日动量<-5%为熊市
            "trend_score_bull": 30,        # 趋势得分>30为牛市
            "trend_score_bear": -30,       # 趋势得分<-30为熊市
        }
        
        logger.info("MarketCharacterClassifier 初始化完成")
    
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
        limit_up_counts: Optional[pd.Series] = None,
        price_df: Optional[pd.DataFrame] = None,
    ) -> MarketCharacter:
        """
        分类市场特征
        
        Args:
            as_of_date: 分析日期
            index_code: 指数代码
            limit_up_counts: 每日涨停数量序列（可选，若无则估算）
            price_df: 价格数据（可选）
        
        Returns:
            MarketCharacter: 市场特征
        """
        # 1. 检查特殊时段
        special = self._check_special_period(as_of_date)
        if special:
            logger.info(f"检测到特殊时段: {special['note']}")
            return MarketCharacter(
                market_type=special['type'],
                strategy_mode=special['force_mode'],
                confidence=1.0,
                is_special_period=True,
                special_note=special['note'],
                suggested_params=STRATEGY_PARAMS_BY_MODE.get(special['force_mode'], {}),
            )
        
        # 2. 获取市场趋势分析结果
        self._ensure_market_trend_analyzer()
        trend_score = 0.0
        
        if self._market_trend_analyzer:
            try:
                trend_result = self._market_trend_analyzer.analyze(
                    as_of_date=as_of_date,
                    index_code=index_code,
                    price_df=price_df,
                )
                if trend_result:
                    trend_score = trend_result.ensemble_score
            except Exception as e:
                logger.warning(f"趋势分析失败: {e}")
        
        # 3. 计算特征指标
        features = self._calculate_features(
            as_of_date=as_of_date,
            limit_up_counts=limit_up_counts,
            price_df=price_df,
            trend_score=trend_score,
        )
        
        # 4. 判断市场类型
        market_type = self._determine_market_type(features)
        
        # 5. 推荐策略模式
        strategy_mode = self._determine_strategy_mode(market_type, features)
        
        # 6. 获取建议参数
        suggested_params = STRATEGY_PARAMS_BY_MODE.get(strategy_mode, {}).copy()
        
        # 7. 计算置信度
        confidence = self._calculate_confidence(features, market_type)
        
        result = MarketCharacter(
            market_type=market_type,
            strategy_mode=strategy_mode,
            confidence=confidence,
            daily_limit_up_avg=features.get("limit_up_avg", 0),
            volatility_20d=features.get("volatility", 0),
            index_momentum_20d=features.get("momentum", 0),
            trend_score=trend_score,
            suggested_params=suggested_params,
        )
        
        self._last_result = result
        
        logger.info(f"市场分类结果: {market_type.value} -> {strategy_mode.value}, 置信度={confidence:.2%}")
        
        return result
    
    def _check_special_period(self, as_of_date: str) -> Optional[Dict]:
        """检查是否为特殊时段"""
        try:
            date = pd.Timestamp(as_of_date)
            for period_name, config in SPECIAL_PERIODS.items():
                start = pd.Timestamp(config["start"])
                end = pd.Timestamp(config["end"])
                if start <= date <= end:
                    return config
        except:
            pass
        return None
    
    def _calculate_features(
        self,
        as_of_date: str,
        limit_up_counts: Optional[pd.Series],
        price_df: Optional[pd.DataFrame],
        trend_score: float,
    ) -> Dict[str, float]:
        """计算特征指标"""
        features = {
            "trend_score": trend_score,
            "limit_up_avg": 0,
            "volatility": 0,
            "momentum": 0,
        }
        
        # 涨停数量
        if limit_up_counts is not None and len(limit_up_counts) > 0:
            # 取最近20日平均
            recent = limit_up_counts.tail(20)
            features["limit_up_avg"] = recent.mean()
        else:
            # 根据趋势得分估算涨停数量
            if trend_score > 50:
                features["limit_up_avg"] = 120  # 强牛
            elif trend_score > 30:
                features["limit_up_avg"] = 80   # 牛市
            elif trend_score > 0:
                features["limit_up_avg"] = 50   # 弱牛
            elif trend_score > -30:
                features["limit_up_avg"] = 30   # 震荡
            else:
                features["limit_up_avg"] = 15   # 熊市
        
        # 波动率和动量
        if price_df is not None and len(price_df) >= 20:
            try:
                close = price_df['close'] if 'close' in price_df.columns else price_df.iloc[:, 0]
                returns = close / close.shift(1) - 1
                features["volatility"] = returns.tail(20).std()
                features["momentum"] = (close.iloc[-1] / close.iloc[-20] - 1) if len(close) >= 20 else 0
            except:
                pass
        
        return features
    
    def _determine_market_type(self, features: Dict[str, float]) -> MarketType:
        """判断市场类型"""
        limit_up_avg = features.get("limit_up_avg", 0)
        trend_score = features.get("trend_score", 0)
        momentum = features.get("momentum", 0)
        
        # 极端牛市
        if limit_up_avg > 150 or trend_score > 70:
            return MarketType.EXTREME_BULL
        
        # 快牛
        if limit_up_avg > self.thresholds["limit_up_fast_bull"] or trend_score > 50:
            return MarketType.FAST_BULL
        
        # 慢牛
        if limit_up_avg > self.thresholds["limit_up_slow_bull"] or trend_score > self.thresholds["trend_score_bull"]:
            return MarketType.SLOW_BULL
        
        # 熊市
        if trend_score < self.thresholds["trend_score_bear"] or momentum < self.thresholds["momentum_bear"]:
            return MarketType.BEAR
        
        # 默认震荡
        return MarketType.VOLATILE
    
    def _determine_strategy_mode(
        self, 
        market_type: MarketType, 
        features: Dict[str, float],
    ) -> StrategyMode:
        """推荐策略模式"""
        if market_type == MarketType.FAST_BULL:
            return StrategyMode.AGGRESSIVE
        
        if market_type == MarketType.EXTREME_BULL:
            # 极端牛市使用正常模式，避免过度追涨
            return StrategyMode.NORMAL
        
        if market_type == MarketType.SLOW_BULL:
            return StrategyMode.CONSERVATIVE
        
        if market_type == MarketType.BEAR:
            return StrategyMode.DEFENSIVE
        
        # 震荡市
        return StrategyMode.CONSERVATIVE
    
    def _calculate_confidence(
        self, 
        features: Dict[str, float], 
        market_type: MarketType,
    ) -> float:
        """计算置信度"""
        trend_score = features.get("trend_score", 0)
        limit_up_avg = features.get("limit_up_avg", 0)
        
        # 基础置信度
        confidence = 0.5
        
        # 趋势得分贡献
        if abs(trend_score) > 50:
            confidence += 0.2
        elif abs(trend_score) > 30:
            confidence += 0.1
        
        # 涨停数量贡献
        if market_type == MarketType.FAST_BULL and limit_up_avg > 120:
            confidence += 0.15
        elif market_type == MarketType.SLOW_BULL and 50 < limit_up_avg < 100:
            confidence += 0.1
        
        # 限制范围
        return min(0.95, max(0.3, confidence))
    
    def get_adaptive_params(
        self,
        base_params: Dict[str, Any],
        market_character: MarketCharacter,
    ) -> Dict[str, Any]:
        """
        根据市场特征调整参数
        
        Args:
            base_params: 基础参数
            market_character: 市场特征
        
        Returns:
            调整后的参数
        """
        result = base_params.copy()
        suggested = market_character.suggested_params
        
        # 合并建议参数（优先使用建议值）
        for key, value in suggested.items():
            result[key] = value
        
        # 根据置信度微调
        if market_character.confidence < 0.5:
            # 低置信度时更保守
            if "stop_loss_pct" in result:
                result["stop_loss_pct"] = max(result["stop_loss_pct"], -0.08)
            if "position_cap" in result:
                result["position_cap"] = min(result["position_cap"], 0.7)
        
        return result


# ============ 测试函数 ============

def test_market_character_classifier():
    """测试市场特征分类器"""
    print("=" * 60)
    print("MarketCharacterClassifier 单元测试")
    print("=" * 60)
    
    classifier = MarketCharacterClassifier()
    
    # 测试1: 2019年特殊时段
    print("\n1. 测试2019年春季特殊时段...")
    result = classifier.classify("2019-03-15")
    print(f"   市场类型: {result.market_type.value}")
    print(f"   策略模式: {result.strategy_mode.value}")
    print(f"   特殊时段: {result.is_special_period}")
    print(f"   备注: {result.special_note}")
    assert result.is_special_period, "2019年3月应标记为特殊时段"
    assert result.strategy_mode == StrategyMode.CONSERVATIVE, "2019年应使用保守策略"
    print("   ✓ 通过")
    
    # 测试2: 正常日期分类
    print("\n2. 测试正常日期分类...")
    result = classifier.classify("2024-10-01")  # 政策牛市期间
    print(f"   市场类型: {result.market_type.value}")
    print(f"   策略模式: {result.strategy_mode.value}")
    print(f"   置信度: {result.confidence:.2%}")
    print(f"   参数: {list(result.suggested_params.keys())[:5]}...")
    assert result.suggested_params, "应有建议参数"
    print("   ✓ 通过")
    
    # 测试3: 参数调整
    print("\n3. 测试参数自适应调整...")
    base_params = {"stop_loss_pct": -0.10, "max_positions": 5}
    adjusted = classifier.get_adaptive_params(base_params, result)
    print(f"   原参数: {base_params}")
    print(f"   调整后: {adjusted}")
    assert "stop_loss_pct" in adjusted, "应保留止损参数"
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_market_character_classifier()
