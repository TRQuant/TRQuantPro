#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarketRegimeDetector - 市场环境判断模块
========================================

核心功能：
1. 识别市场所处阶段（牛市/熊市/震荡市）
2. 提供市场环境指标
3. 预测市场趋势
4. 与策略切换系统联动

市场环境定义：
- BULL: 牛市 - 上升趋势，成交活跃，做多策略
- BEAR: 熊市 - 下降趋势，避险为主，防守策略
- VOLATILE: 震荡市 - 无明显趋势，区间操作
- RECOVERY: 复苏期 - 熊转牛过渡，布局时机
- DISTRIBUTION: 派发期 - 牛转熊过渡，减仓时机

指标体系：
1. 宏观层面：PMI、M2、社融、利率
2. 市场层面：指数趋势、成交量、涨跌比
3. 情绪层面：换手率、新高新低比、融资余额
4. 技术层面：均线系统、动量指标、波动率
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """市场环境阶段"""
    BULL = "BULL"              # 牛市
    BEAR = "BEAR"              # 熊市
    VOLATILE = "VOLATILE"      # 震荡市
    RECOVERY = "RECOVERY"      # 复苏期（熊转牛）
    DISTRIBUTION = "DISTRIBUTION"  # 派发期（牛转熊）


REGIME_DESCRIPTIONS = {
    MarketRegime.BULL: "牛市 - 趋势向上，做多为主，持股待涨",
    MarketRegime.BEAR: "熊市 - 趋势向下，防守为主，现金为王",
    MarketRegime.VOLATILE: "震荡市 - 区间波动，高抛低吸，控制仓位",
    MarketRegime.RECOVERY: "复苏期 - 底部企稳，布局时机，逢低建仓",
    MarketRegime.DISTRIBUTION: "派发期 - 顶部震荡，逐步减仓，锁定利润"
}


# 策略推荐映射
REGIME_STRATEGY_MAP = {
    MarketRegime.BULL: {
        "position": 0.8,        # 仓位建议
        "strategy": ["momentum", "growth", "tenbagger"],  # 推荐策略
        "risk_level": "aggressive",  # 风险偏好
        "focus": "主线赛道龙头，高成长科技股"
    },
    MarketRegime.BEAR: {
        "position": 0.2,
        "strategy": ["defensive", "dividend", "bond"],
        "risk_level": "conservative",
        "focus": "高股息防守股，现金为王"
    },
    MarketRegime.VOLATILE: {
        "position": 0.5,
        "strategy": ["swing", "mean_reversion", "options"],
        "risk_level": "moderate",
        "focus": "波段操作，高抛低吸"
    },
    MarketRegime.RECOVERY: {
        "position": 0.6,
        "strategy": ["value", "turnaround", "early_stage"],
        "risk_level": "moderate",
        "focus": "底部布局，十倍股早期识别"
    },
    MarketRegime.DISTRIBUTION: {
        "position": 0.4,
        "strategy": ["momentum_exit", "hedging", "cash"],
        "risk_level": "conservative",
        "focus": "逢高减仓，落袋为安"
    }
}


@dataclass
class MarketIndicators:
    """市场指标数据"""
    # 宏观指标
    pmi: float = 50.0           # PMI指数 (>50扩张)
    m2_growth: float = 0.0      # M2同比增速
    social_finance: float = 0.0  # 社融增速
    interest_rate: float = 0.0   # 基准利率
    
    # 市场指标
    index_ma20: float = 0.0     # 指数20日均线位置
    index_ma60: float = 0.0     # 指数60日均线位置
    index_ma250: float = 0.0    # 指数250日均线位置
    index_position: float = 0.5  # 指数相对位置 (0-1)
    
    volume_ratio: float = 1.0   # 成交量比 (vs 20日均量)
    advance_decline: float = 0.5  # 涨跌比
    limit_up_ratio: float = 0.0   # 涨停比例
    limit_down_ratio: float = 0.0  # 跌停比例
    
    # 情绪指标
    turnover_rate: float = 0.0   # 平均换手率
    new_high_count: int = 0      # 创新高股票数
    new_low_count: int = 0       # 创新低股票数
    margin_balance: float = 0.0  # 融资余额
    margin_change: float = 0.0   # 融资余额变化
    
    # 技术指标
    rsi: float = 50.0           # RSI指标
    macd_hist: float = 0.0      # MACD柱状图
    volatility: float = 0.0     # 波动率
    atr_ratio: float = 1.0      # ATR比率
    
    # 时间
    date: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RegimeResult:
    """市场环境判断结果"""
    regime: MarketRegime
    confidence: float           # 判断置信度 (0-1)
    score: float               # 综合得分 (-100 to 100)
    
    # 分项得分
    macro_score: float = 0.0   # 宏观得分
    market_score: float = 0.0  # 市场得分
    sentiment_score: float = 0.0  # 情绪得分
    technical_score: float = 0.0  # 技术得分
    
    # 建议
    strategy_advice: Dict = field(default_factory=dict)
    
    # 趋势预测
    trend_prediction: str = ""  # 趋势预测
    risk_warning: str = ""      # 风险提示
    
    # 历史对比
    regime_duration: int = 0    # 当前环境持续天数
    previous_regime: str = ""   # 上一个环境
    
    # 时间
    analysis_date: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['regime'] = self.regime.value
        return result


class MarketRegimeDetector:
    """
    市场环境检测器
    
    核心算法：
    1. 多指标综合评分
    2. 趋势与波动率分析
    3. 市场广度分析
    4. 宏观环境判断
    """
    
    def __init__(self):
        self._jq = None
        self._history: List[RegimeResult] = []
        self._current_regime: Optional[MarketRegime] = None
        self._regime_start_date: Optional[str] = None
        
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                # 从配置加载凭证
                import json
                config_path = "/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json"
                with open(config_path, 'r') as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info(f"JQData认证成功: {config['username']}")
            except Exception as e:
                logger.error(f"JQData认证失败: {e}")
                raise
    
    def get_market_indicators(self, date: str = None) -> MarketIndicators:
        """
        获取市场指标
        
        Args:
            date: 日期，默认最新
            
        Returns:
            MarketIndicators实例
        """
        self._ensure_jqdata()
        jq = self._jq
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        indicators = MarketIndicators(date=date)
        
        try:
            # 获取上证指数数据
            index_code = "000001.XSHG"
            end_date = datetime.strptime(date, "%Y-%m-%d")
            start_date = end_date - timedelta(days=365)
            
            # 获取行情数据
            df = jq.get_price(
                index_code,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=date,
                frequency='daily',
                fields=['close', 'volume', 'money']
            )
            
            if df is not None and len(df) > 0:
                close = df['close'].values
                volume = df['volume'].values
                
                # 计算均线
                if len(close) >= 20:
                    indicators.index_ma20 = np.mean(close[-20:])
                if len(close) >= 60:
                    indicators.index_ma60 = np.mean(close[-60:])
                if len(close) >= 250:
                    indicators.index_ma250 = np.mean(close[-250:])
                
                # 指数相对位置 (过去一年最高最低)
                high = np.max(close)
                low = np.min(close)
                current = close[-1]
                if high > low:
                    indicators.index_position = (current - low) / (high - low)
                
                # 成交量比
                if len(volume) >= 20:
                    avg_volume = np.mean(volume[-20:])
                    if avg_volume > 0:
                        indicators.volume_ratio = volume[-1] / avg_volume
                
                # 计算RSI
                if len(close) >= 14:
                    indicators.rsi = self._calculate_rsi(close, 14)
                
                # 计算波动率
                if len(close) >= 20:
                    returns = np.diff(np.log(close[-21:]))
                    indicators.volatility = np.std(returns) * np.sqrt(252) * 100  # 年化波动率%
                
                # 计算MACD
                if len(close) >= 26:
                    macd, signal, hist = self._calculate_macd(close)
                    indicators.macd_hist = hist[-1] if len(hist) > 0 else 0
            
            # 获取全市场涨跌统计
            all_stocks = jq.get_all_securities(types=['stock'], date=date)
            if all_stocks is not None and len(all_stocks) > 0:
                stock_list = all_stocks.index.tolist()[:500]  # 取前500只
                
                prices = jq.get_price(
                    stock_list,
                    end_date=date,
                    count=2,
                    frequency='daily',
                    fields=['close']
                )
                
                if prices is not None and len(prices) > 0:
                    # 计算涨跌比
                    advances = 0
                    declines = 0
                    for stock in stock_list:
                        try:
                            if stock in prices.minor_axis:
                                stock_data = prices.minor_xs(stock)['close'].values
                                if len(stock_data) >= 2:
                                    if stock_data[-1] > stock_data[-2]:
                                        advances += 1
                                    else:
                                        declines += 1
                        except:
                            pass
                    
                    total = advances + declines
                    if total > 0:
                        indicators.advance_decline = advances / total
            
            # 获取宏观数据 (PMI)
            try:
                from jqdatasdk import macro
                q = jq.query(macro.MAC_MANUFACTURING_PMI).order_by(
                    macro.MAC_MANUFACTURING_PMI.stat_month.desc()
                ).limit(1)
                pmi_data = macro.run_query(q)
                if pmi_data is not None and len(pmi_data) > 0:
                    indicators.pmi = float(pmi_data['pmi'].iloc[0])
            except Exception as e:
                logger.debug(f"获取PMI数据失败: {e}")
            
        except Exception as e:
            logger.error(f"获取市场指标失败: {e}")
        
        return indicators
    
    def detect_regime(self, date: str = None) -> RegimeResult:
        """
        检测市场环境
        
        Args:
            date: 日期
            
        Returns:
            RegimeResult实例
        """
        indicators = self.get_market_indicators(date)
        
        # 计算各维度得分 (-100 to 100)
        macro_score = self._calc_macro_score(indicators)
        market_score = self._calc_market_score(indicators)
        sentiment_score = self._calc_sentiment_score(indicators)
        technical_score = self._calc_technical_score(indicators)
        
        # 加权综合得分
        weights = {
            'macro': 0.15,
            'market': 0.35,
            'sentiment': 0.20,
            'technical': 0.30
        }
        
        total_score = (
            macro_score * weights['macro'] +
            market_score * weights['market'] +
            sentiment_score * weights['sentiment'] +
            technical_score * weights['technical']
        )
        
        # 判断市场环境
        regime, confidence = self._determine_regime(total_score, indicators)
        
        # 生成结果
        result = RegimeResult(
            regime=regime,
            confidence=confidence,
            score=total_score,
            macro_score=macro_score,
            market_score=market_score,
            sentiment_score=sentiment_score,
            technical_score=technical_score,
            strategy_advice=REGIME_STRATEGY_MAP[regime],
            trend_prediction=self._predict_trend(total_score, indicators),
            risk_warning=self._generate_risk_warning(indicators),
            analysis_date=indicators.date or datetime.now().strftime("%Y-%m-%d")
        )
        
        # 更新历史
        self._update_history(result)
        
        return result
    
    def _calc_macro_score(self, ind: MarketIndicators) -> float:
        """计算宏观得分"""
        score = 0.0
        
        # PMI贡献 (50为中性)
        if ind.pmi > 0:
            score += (ind.pmi - 50) * 3  # 每偏离1点贡献3分
        
        # M2增速贡献
        score += ind.m2_growth * 2
        
        # 利率贡献 (利率下降利好)
        score -= ind.interest_rate * 5
        
        return max(-100, min(100, score))
    
    def _calc_market_score(self, ind: MarketIndicators) -> float:
        """计算市场得分"""
        score = 0.0
        
        # 均线系统
        if ind.index_ma20 > 0 and ind.index_ma60 > 0:
            if ind.index_ma20 > ind.index_ma60:
                score += 20  # 短期均线在上，多头排列
            else:
                score -= 20  # 空头排列
        
        if ind.index_ma60 > 0 and ind.index_ma250 > 0:
            if ind.index_ma60 > ind.index_ma250:
                score += 15
            else:
                score -= 15
        
        # 指数位置
        position_score = (ind.index_position - 0.5) * 60
        score += position_score
        
        # 成交量
        if ind.volume_ratio > 1.5:
            score += 10  # 放量
        elif ind.volume_ratio < 0.7:
            score -= 10  # 缩量
        
        # 涨跌比
        score += (ind.advance_decline - 0.5) * 40
        
        return max(-100, min(100, score))
    
    def _calc_sentiment_score(self, ind: MarketIndicators) -> float:
        """计算情绪得分"""
        score = 0.0
        
        # 换手率 (适度换手为佳)
        if 2 < ind.turnover_rate < 5:
            score += 10
        elif ind.turnover_rate > 8:
            score -= 10  # 过热
        
        # 新高新低比
        if ind.new_high_count > 0 or ind.new_low_count > 0:
            ratio = ind.new_high_count / max(ind.new_low_count, 1)
            score += min(30, max(-30, (ratio - 1) * 15))
        
        # 融资变化
        score += ind.margin_change * 10
        
        return max(-100, min(100, score))
    
    def _calc_technical_score(self, ind: MarketIndicators) -> float:
        """计算技术得分"""
        score = 0.0
        
        # RSI
        if ind.rsi > 70:
            score -= (ind.rsi - 70) * 2  # 超买
        elif ind.rsi < 30:
            score += (30 - ind.rsi) * 2  # 超卖
        else:
            score += (ind.rsi - 50)  # 中性区域
        
        # MACD
        score += min(20, max(-20, ind.macd_hist * 5))
        
        # 波动率 (低波动利好)
        if ind.volatility > 0:
            if ind.volatility < 15:
                score += 10
            elif ind.volatility > 30:
                score -= 15
        
        return max(-100, min(100, score))
    
    def _determine_regime(self, score: float, ind: MarketIndicators) -> Tuple[MarketRegime, float]:
        """
        确定市场环境
        
        Args:
            score: 综合得分
            ind: 指标
            
        Returns:
            (环境, 置信度)
        """
        # 基于得分判断
        if score > 40:
            regime = MarketRegime.BULL
            confidence = min(1.0, (score - 40) / 60 * 0.5 + 0.5)
        elif score < -40:
            regime = MarketRegime.BEAR
            confidence = min(1.0, (-score - 40) / 60 * 0.5 + 0.5)
        elif 10 < score <= 40:
            # 可能是复苏期
            if ind.index_position < 0.4:
                regime = MarketRegime.RECOVERY
                confidence = 0.6
            else:
                regime = MarketRegime.BULL
                confidence = 0.5
        elif -40 <= score < -10:
            # 可能是派发期
            if ind.index_position > 0.6:
                regime = MarketRegime.DISTRIBUTION
                confidence = 0.6
            else:
                regime = MarketRegime.BEAR
                confidence = 0.5
        else:
            regime = MarketRegime.VOLATILE
            confidence = 0.4 + abs(score) / 100 * 0.2
        
        # 波动率修正
        if ind.volatility > 25:
            if regime in [MarketRegime.BULL, MarketRegime.BEAR]:
                confidence *= 0.9  # 高波动降低置信度
        
        return regime, confidence
    
    def _predict_trend(self, score: float, ind: MarketIndicators) -> str:
        """预测趋势"""
        if score > 30:
            if ind.rsi > 70:
                return "短期可能回调，中期看多"
            return "趋势向上，持股待涨"
        elif score < -30:
            if ind.rsi < 30:
                return "短期可能反弹，中期看空"
            return "趋势向下，谨慎观望"
        else:
            return "震荡整理，等待方向选择"
    
    def _generate_risk_warning(self, ind: MarketIndicators) -> str:
        """生成风险提示"""
        warnings = []
        
        if ind.rsi > 80:
            warnings.append("RSI严重超买")
        elif ind.rsi < 20:
            warnings.append("RSI严重超卖")
        
        if ind.volatility > 35:
            warnings.append("波动率过高")
        
        if ind.volume_ratio > 2.5:
            warnings.append("成交量异常放大")
        elif ind.volume_ratio < 0.5:
            warnings.append("成交量严重萎缩")
        
        if ind.pmi < 48:
            warnings.append("PMI处于收缩区间")
        
        return "；".join(warnings) if warnings else "无特别风险提示"
    
    def _update_history(self, result: RegimeResult):
        """更新历史记录"""
        self._history.append(result)
        
        # 检查环境变化
        if self._current_regime != result.regime:
            result.previous_regime = self._current_regime.value if self._current_regime else ""
            self._current_regime = result.regime
            self._regime_start_date = result.analysis_date
            result.regime_duration = 0
        else:
            # 计算持续天数
            if self._regime_start_date:
                try:
                    start = datetime.strptime(self._regime_start_date, "%Y-%m-%d")
                    end = datetime.strptime(result.analysis_date, "%Y-%m-%d")
                    result.regime_duration = (end - start).days
                except:
                    pass
        
        # 只保留最近100条
        if len(self._history) > 100:
            self._history = self._history[-100:]
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """计算RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices[-(period+1):])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9):
        """计算MACD"""
        def ema(data, period):
            alpha = 2 / (period + 1)
            result = np.zeros_like(data)
            result[0] = data[0]
            for i in range(1, len(data)):
                result[i] = alpha * data[i] + (1 - alpha) * result[i-1]
            return result
        
        ema_fast = ema(prices, fast)
        ema_slow = ema(prices, slow)
        macd_line = ema_fast - ema_slow
        signal_line = ema(macd_line, signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def get_strategy_recommendation(self, regime: MarketRegime = None) -> Dict[str, Any]:
        """
        获取策略推荐
        
        Args:
            regime: 市场环境，默认使用当前检测结果
            
        Returns:
            策略推荐
        """
        if regime is None:
            result = self.detect_regime()
            regime = result.regime
        
        advice = REGIME_STRATEGY_MAP[regime].copy()
        advice['regime'] = regime.value
        advice['description'] = REGIME_DESCRIPTIONS[regime]
        
        return advice
    
    def get_history_regimes(self, days: int = 30) -> List[Dict]:
        """获取历史环境记录"""
        return [r.to_dict() for r in self._history[-days:]]


# 全局实例
_detector: Optional[MarketRegimeDetector] = None


def get_market_regime_detector() -> MarketRegimeDetector:
    """获取市场环境检测器"""
    global _detector
    if _detector is None:

















