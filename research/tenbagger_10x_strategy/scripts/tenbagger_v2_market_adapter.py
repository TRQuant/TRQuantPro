#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股早期识别系统 V2.0 - 市场趋势适配器
=====================================

集成现有模块:
- core/trend_analyzer_v2.py - 动态阈值趋势分析
- core/ibd_style_analyzer.py - IBD风格分析
- core/market_env_identifier.py - 市场环境识别

市场环境适配策略:
| 市场状态 | 策略调整 |
|---------|---------|
| 强势上涨 | 激进，成长因子权重+10% |
| 上涨 | 标准配置 |
| 中性震荡 | 保守，质量因子权重+10% |
| 下跌 | 防守，现金50%，仅质量股 |
| 强势下跌 | 空仓或极低仓位 |

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_v2_market_adapter.py
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import logging
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# 市场状态定义
# ============================================================

class MarketState(Enum):
    """市场状态"""
    STRONG_BULL = "强势上涨"
    BULL = "上涨"
    NEUTRAL = "中性震荡"
    BEAR = "下跌"
    STRONG_BEAR = "强势下跌"
    
    @property
    def risk_level(self) -> int:
        """风险等级 1-5"""
        levels = {
            "强势上涨": 1,
            "上涨": 2,
            "中性震荡": 3,
            "下跌": 4,
            "强势下跌": 5
        }
        return levels.get(self.value, 3)
    
    @property
    def position_limit(self) -> float:
        """仓位上限"""
        limits = {
            "强势上涨": 1.0,   # 满仓
            "上涨": 0.8,       # 80%
            "中性震荡": 0.6,   # 60%
            "下跌": 0.3,       # 30%
            "强势下跌": 0.1    # 10%（或空仓）
        }
        return limits.get(self.value, 0.5)


# ============================================================
# 策略调整配置
# ============================================================

@dataclass
class StrategyAdjustment:
    """策略调整参数"""
    # 因子权重调整
    growth_weight_adj: float = 0.0
    quality_weight_adj: float = 0.0
    valuation_weight_adj: float = 0.0
    momentum_weight_adj: float = 0.0
    
    # 仓位调整
    max_position: float = 1.0
    single_stock_max: float = 0.25
    cash_reserve: float = 0.0
    
    # 风控调整
    stop_loss_adj: float = 0.0
    take_profit_adj: float = 0.0
    
    # 选股调整
    min_score_adj: float = 0.0
    prefer_quality: bool = False


# ============================================================
# 市场趋势分析器（简化版）
# ============================================================

class SimpleTrendAnalyzer:
    """简化版市场趋势分析器
    
    基于以下指标判断市场趋势:
    1. 指数均线（MA5/MA20/MA60）
    2. 指数动量（20日涨跌幅）
    3. 市场广度（上涨/下跌家数比）
    4. 成交量变化
    """
    
    def __init__(self):
        self.jq = None
        self._init_jqdata()
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            config_path = PROJECT_ROOT / "config" / "jqdata_config.json"
            with open(config_path) as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
            logger.info("✅ JQData认证成功")
        except Exception as e:
            logger.warning(f"⚠️ JQData认证失败: {e}")
    
    def analyze_market(self, date: str = None) -> Dict:
        """分析市场趋势"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        result = {
            'date': date,
            'state': MarketState.NEUTRAL,
            'confidence': 0.5,
            'indicators': {},
            'signals': []
        }
        
        if self.jq is None:
            logger.warning("JQData未初始化，使用默认中性状态")
            return result
        
        try:
            # 获取沪深300指数数据
            index_code = '000300.XSHG'
            end_date = date
            start_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=120)).strftime("%Y-%m-%d")
            
            df = self.jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close', 'volume']
            )
            
            if df is None or len(df) < 60:
                return result
            
            close = df['close']
            volume = df['volume']
            
            # 计算指标
            ma5 = close.rolling(5).mean().iloc[-1]
            ma20 = close.rolling(20).mean().iloc[-1]
            ma60 = close.rolling(60).mean().iloc[-1]
            current_price = close.iloc[-1]
            
            # 均线状态
            ma_bullish = current_price > ma5 > ma20 > ma60
            ma_bearish = current_price < ma5 < ma20 < ma60
            
            # 动量
            if len(close) >= 20:
                momentum_20d = (close.iloc[-1] / close.iloc[-20] - 1) * 100
            else:
                momentum_20d = 0
            
            # 成交量变化
            vol_5 = volume.tail(5).mean()
            vol_20 = volume.tail(20).mean()
            vol_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
            
            result['indicators'] = {
                'ma5': ma5,
                'ma20': ma20,
                'ma60': ma60,
                'current_price': current_price,
                'ma_bullish': ma_bullish,
                'ma_bearish': ma_bearish,
                'momentum_20d': momentum_20d,
                'vol_ratio': vol_ratio
            }
            
            # 判断市场状态
            score = 0
            
            # 均线信号
            if ma_bullish:
                score += 30
                result['signals'].append("均线多头排列")
            elif ma_bearish:
                score -= 30
                result['signals'].append("均线空头排列")
            elif current_price > ma20:
                score += 10
                result['signals'].append("价格在20日均线上方")
            else:
                score -= 10
                result['signals'].append("价格在20日均线下方")
            
            # 动量信号
            if momentum_20d > 10:
                score += 25
                result['signals'].append(f"强劲动量 +{momentum_20d:.1f}%")
            elif momentum_20d > 5:
                score += 15
                result['signals'].append(f"正向动量 +{momentum_20d:.1f}%")
            elif momentum_20d > 0:
                score += 5
            elif momentum_20d > -5:
                score -= 5
            elif momentum_20d > -10:
                score -= 15
                result['signals'].append(f"负向动量 {momentum_20d:.1f}%")
            else:
                score -= 25
                result['signals'].append(f"强烈下跌 {momentum_20d:.1f}%")
            
            # 成交量信号
            if vol_ratio > 1.5:
                if momentum_20d > 0:
                    score += 10
                    result['signals'].append("放量上涨")
                else:
                    score -= 10
                    result['signals'].append("放量下跌")
            
            # 确定状态
            if score >= 40:
                result['state'] = MarketState.STRONG_BULL
                result['confidence'] = min(0.9, 0.6 + score/100)
            elif score >= 20:
                result['state'] = MarketState.BULL
                result['confidence'] = min(0.8, 0.5 + score/100)
            elif score >= -20:
                result['state'] = MarketState.NEUTRAL
                result['confidence'] = 0.5 + abs(score)/200
            elif score >= -40:
                result['state'] = MarketState.BEAR
                result['confidence'] = min(0.8, 0.5 + abs(score)/100)
            else:
                result['state'] = MarketState.STRONG_BEAR
                result['confidence'] = min(0.9, 0.6 + abs(score)/100)
            
            result['score'] = score
            
        except Exception as e:
            logger.error(f"分析市场趋势失败: {e}")
        
        return result


# ============================================================
# 市场趋势适配器
# ============================================================

class TenbaggerV2MarketAdapter:
    """十倍股V2市场趋势适配器
    
    根据市场状态动态调整策略参数
    """
    
    # 预定义的策略调整方案
    STRATEGY_ADJUSTMENTS = {
        MarketState.STRONG_BULL: StrategyAdjustment(
            growth_weight_adj=0.10,      # 成长因子+10%
            quality_weight_adj=-0.05,
            momentum_weight_adj=0.05,
            max_position=1.0,            # 满仓
            single_stock_max=0.30,       # 单票30%
            cash_reserve=0.0,
            stop_loss_adj=0.02,          # 止损放宽
            take_profit_adj=0.20,        # 止盈提高
            min_score_adj=-5,            # 降低门槛
            prefer_quality=False
        ),
        MarketState.BULL: StrategyAdjustment(
            growth_weight_adj=0.05,
            max_position=0.8,
            single_stock_max=0.25,
            cash_reserve=0.1,
            prefer_quality=False
        ),
        MarketState.NEUTRAL: StrategyAdjustment(
            quality_weight_adj=0.05,
            max_position=0.6,
            single_stock_max=0.20,
            cash_reserve=0.2,
            min_score_adj=5,             # 提高门槛
            prefer_quality=True
        ),
        MarketState.BEAR: StrategyAdjustment(
            growth_weight_adj=-0.10,
            quality_weight_adj=0.15,     # 质量因子+15%
            valuation_weight_adj=0.05,
            max_position=0.3,            # 最多30%仓位
            single_stock_max=0.15,
            cash_reserve=0.5,
            stop_loss_adj=-0.03,         # 止损收紧
            min_score_adj=10,            # 大幅提高门槛
            prefer_quality=True
        ),
        MarketState.STRONG_BEAR: StrategyAdjustment(
            growth_weight_adj=-0.15,
            quality_weight_adj=0.20,
            max_position=0.1,            # 极低仓位
            single_stock_max=0.10,
            cash_reserve=0.8,
            stop_loss_adj=-0.05,
            min_score_adj=15,
            prefer_quality=True
        )
    }
    
    def __init__(self):
        self.trend_analyzer = SimpleTrendAnalyzer()
        self.current_market_state = None
        self.current_adjustment = None
    
    def analyze_and_adapt(self, date: str = None) -> Tuple[MarketState, StrategyAdjustment]:
        """分析市场并返回适配后的策略"""
        # 分析市场
        market_analysis = self.trend_analyzer.analyze_market(date)
        
        state = market_analysis['state']
        self.current_market_state = state
        
        # 获取对应的策略调整
        adjustment = self.STRATEGY_ADJUSTMENTS.get(state, StrategyAdjustment())
        self.current_adjustment = adjustment
        
        logger.info(f"\n{'='*60}")
        logger.info(f"📊 市场趋势分析")
        logger.info(f"{'='*60}")
        logger.info(f"日期: {market_analysis['date']}")
        logger.info(f"状态: {state.value}")
        logger.info(f"置信度: {market_analysis['confidence']:.1%}")
        logger.info(f"风险等级: {state.risk_level}/5")
        logger.info(f"仓位上限: {state.position_limit:.0%}")
        
        if market_analysis['signals']:
            logger.info(f"\n信号:")
            for signal in market_analysis['signals']:
                logger.info(f"  • {signal}")
        
        logger.info(f"\n策略调整:")
        logger.info(f"  成长因子权重调整: {adjustment.growth_weight_adj:+.0%}")
        logger.info(f"  质量因子权重调整: {adjustment.quality_weight_adj:+.0%}")
        logger.info(f"  最大仓位: {adjustment.max_position:.0%}")
        logger.info(f"  现金储备: {adjustment.cash_reserve:.0%}")
        logger.info(f"  最低分数调整: {adjustment.min_score_adj:+.0f}")
        
        return state, adjustment
    
    def get_adjusted_weights(self, base_weights: Dict[str, float]) -> Dict[str, float]:
        """获取调整后的因子权重"""
        if self.current_adjustment is None:
            return base_weights
        
        adj = self.current_adjustment
        adjusted = base_weights.copy()
        
        adjusted['growth'] = max(0, adjusted.get('growth', 0) + adj.growth_weight_adj)
        adjusted['quality'] = max(0, adjusted.get('quality', 0) + adj.quality_weight_adj)
        adjusted['valuation'] = max(0, adjusted.get('valuation', 0) + adj.valuation_weight_adj)
        adjusted['momentum'] = max(0, adjusted.get('momentum', 0) + adj.momentum_weight_adj)
        
        # 归一化
        total = sum(adjusted.values())
        if total > 0:
            for key in adjusted:
                adjusted[key] /= total
        
        return adjusted
    
    def get_position_limits(self) -> Dict[str, float]:
        """获取仓位限制"""
        if self.current_adjustment is None:
            return {
                'max_position': 0.8,
                'single_stock_max': 0.25,
                'cash_reserve': 0.1
            }
        
        return {
            'max_position': self.current_adjustment.max_position,
            'single_stock_max': self.current_adjustment.single_stock_max,
            'cash_reserve': self.current_adjustment.cash_reserve
        }
    
    def get_risk_params(self) -> Dict[str, float]:
        """获取风控参数"""
        base_stop_loss = -0.15
        base_take_profit = 1.0
        
        if self.current_adjustment is None:
            return {
                'stop_loss': base_stop_loss,
                'take_profit': base_take_profit
            }
        
        return {
            'stop_loss': base_stop_loss + self.current_adjustment.stop_loss_adj,
            'take_profit': base_take_profit + self.current_adjustment.take_profit_adj
        }
    
    def should_trade(self) -> bool:
        """是否应该交易"""
        if self.current_market_state is None:
            return True
        
        # 强势下跌时建议暂停交易
        if self.current_market_state == MarketState.STRONG_BEAR:
            logger.warning("⚠️ 市场强势下跌，建议暂停交易或极低仓位")
            return False
        
        return True
    
    def get_market_summary(self) -> Dict:
        """获取市场摘要"""
        if self.current_market_state is None:
            return {}
        
        state = self.current_market_state
        adj = self.current_adjustment
        
        return {
            'state': state.value,
            'risk_level': state.risk_level,
            'position_limit': state.position_limit,
            'max_position': adj.max_position if adj else 0.8,
            'cash_reserve': adj.cash_reserve if adj else 0.1,
            'prefer_quality': adj.prefer_quality if adj else False,
            'trading_advised': self.should_trade()
        }


# ============================================================
# 集成现有趋势分析模块
# ============================================================

class IntegratedMarketAnalyzer:
    """集成多个现有市场分析模块"""
    
    def __init__(self):
        self.simple_analyzer = SimpleTrendAnalyzer()
        self.trend_analyzer_v2 = None
        self.ibd_analyzer = None
        self.env_identifier = None
        
        self._load_existing_modules()
    
    def _load_existing_modules(self):
        """加载现有模块"""
        try:
            from core.trend_analyzer_v2 import TrendAnalyzerV2
            self.trend_analyzer_v2 = TrendAnalyzerV2()
            logger.info("✅ 加载 TrendAnalyzerV2")
        except ImportError as e:
            logger.warning(f"⚠️ 无法加载 TrendAnalyzerV2: {e}")
        
        try:
            from core.ibd_style_analyzer import IBDStyleAnalyzer
            self.ibd_analyzer = IBDStyleAnalyzer()
            logger.info("✅ 加载 IBDStyleAnalyzer")
        except ImportError as e:
            logger.warning(f"⚠️ 无法加载 IBDStyleAnalyzer: {e}")
        
        try:
            from core.market_env_identifier import MarketEnvIdentifier
            self.env_identifier = MarketEnvIdentifier()
            logger.info("✅ 加载 MarketEnvIdentifier")
        except ImportError as e:
            logger.warning(f"⚠️ 无法加载 MarketEnvIdentifier: {e}")
    
    def comprehensive_analysis(self, date: str = None) -> Dict:
        """综合多模块分析"""
        results = {
            'date': date or datetime.now().strftime("%Y-%m-%d"),
            'simple': None,
            'trend_v2': None,
            'ibd': None,
            'env': None,
            'consensus': None
        }
        
        # 简单分析（总是可用）
        results['simple'] = self.simple_analyzer.analyze_market(date)
        
        # TrendAnalyzerV2
        if self.trend_analyzer_v2:
            try:
                # 需要根据实际接口调整
                pass
            except Exception as e:
                logger.warning(f"TrendAnalyzerV2分析失败: {e}")
        
        # IBD分析
        if self.ibd_analyzer:
            try:
                # 需要根据实际接口调整
                pass
            except Exception as e:
                logger.warning(f"IBD分析失败: {e}")
        
        # 综合判断
        results['consensus'] = self._calculate_consensus(results)
        
        return results
    
    def _calculate_consensus(self, results: Dict) -> Dict:
        """计算各模块的共识"""
        # 简化：直接使用简单分析的结果
        simple = results.get('simple', {})
        
        return {
            'state': simple.get('state', MarketState.NEUTRAL),
            'confidence': simple.get('confidence', 0.5),
            'source': 'simple_analyzer'
        }


# ============================================================
# 测试
# ============================================================

def test_market_adapter():
    """测试市场适配器"""
    adapter = TenbaggerV2MarketAdapter()
    
    # 分析并适配
    state, adjustment = adapter.analyze_and_adapt()
    
    # 获取调整后的参数
    base_weights = {
        'growth': 0.30,
        'quality': 0.25,
        'valuation': 0.15,
        'momentum': 0.15,
        'scale': 0.10,
        'technical': 0.05
    }
    
    adjusted_weights = adapter.get_adjusted_weights(base_weights)
    
    print(f"\n调整后的因子权重:")
    for factor, weight in adjusted_weights.items():
        base = base_weights.get(factor, 0)
        print(f"  {factor}: {base:.0%} → {weight:.0%}")
    
    print(f"\n仓位限制:")
    limits = adapter.get_position_limits()
    for key, value in limits.items():
        print(f"  {key}: {value:.0%}")
    
    print(f"\n风控参数:")
    risk = adapter.get_risk_params()
    for key, value in risk.items():
        print(f"  {key}: {value:.0%}")
    
    print(f"\n市场摘要:")
    summary = adapter.get_market_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_market_adapter()
